#!/usr/bin/env python3
"""Offline search, inspect and coverage for the Market Analysis Atlas Agent Skill."""
import argparse, json, re, sys, unicodedata
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/market-analysis-atlas'

def normalize(v):
    v=unicodedata.normalize('NFKD',v).casefold()
    return re.sub(r'[^\w]+',' ',v).strip()

def load(include_index=False):
    curated=[json.loads(l) for l in (SKILL/'data/terms.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    # Attach only independently checked direct URLs, never inferred article slugs.
    verified=json.loads((SKILL/'data/verified-links.json').read_text(encoding='utf-8'))['links']
    for entry in curated:
        if entry['id'] in verified:
            entry['source_url']=verified[entry['id']]
            entry['source_link_status']='independently_verified'
    if include_index:
        seen={normalize(e['term']) for e in curated}
        for filename in ('investopedia-index.jsonl','imported-index.jsonl'):
            path=SKILL/'data'/filename
            if not path.exists():continue
            for l in path.read_text(encoding='utf-8').splitlines():
                record=json.loads(l)
                if normalize(record['term']) not in seen:
                    curated.append(record);seen.add(normalize(record['term']))
    return curated

def rank(rec,query):
    q=normalize(query);name=normalize(rec['term']);desc=normalize(rec.get('definition',''))
    if not q:return 1
    if q==name:return 100
    if name.startswith(q):return 70
    if q in name:return 50
    if all(w in name for w in q.split()):return 35
    if q in desc:return 15
    if all(w in desc for w in q.split()):return 5
    return 0

def run(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('query',nargs='?',default='',help='Search query (omit to list category)')
    p.add_argument('--category',help='Restrict taxonomy category')
    p.add_argument('--limit',type=int,default=15)
    p.add_argument('--include-index',action='store_true',help='Include title-only external catalog if imported')
    p.add_argument('--json',action='store_true',help='Machine readable JSON')
    p.add_argument('--detail',action='store_true',help='Show full available original record and related diagram')
    p.add_argument('--stats',action='store_true',help='Coverage by domain and provenance')
    a=p.parse_args(argv)
    items=load(a.include_index)
    if a.stats:
        r={'total':len(items),'categories':dict(sorted(Counter(e['category'] for e in items).items())),
           'definition_count':sum(bool(e.get('definition')) for e in items),'index_only_count':sum(e.get('status')=='index_only' for e in items),
           'diagram_count':len(list((SKILL/'assets/charts').glob('*.svg')))}
        print(json.dumps(r,ensure_ascii=False,indent=2));return 0
    matches=[(rank(e,a.query),e) for e in items if not a.category or e['category']==a.category]
    matches.sort(key=lambda t:(-t[0],t[1]['term'].casefold()))
    if a.query:matches=[(n,e) for n,e in matches if n]
    output=[]
    for _,r in matches[:max(0,a.limit)]:
        if a.detail:
            copy=dict(r)
            img=SKILL/'assets/charts'/(r['id']+'.svg')
            if img.is_file():copy['diagram']=str(img.relative_to(ROOT))
            output.append(copy)
        else:output.append({key:r[key] for key in ('term','category','definition','source_url') if key in r})
    if a.json:print(json.dumps(output,ensure_ascii=False,indent=2))
    else:
        for e in output:
            print(f"[{e['category']}] {e['term']}: {e.get('definition','Index link only; content not available offline.')}")
            if 'formula' in e: print('  Formula:',e['formula'])
            if 'diagram' in e:print('  Diagram:',e['diagram'])
            if 'source_url' in e:print('  Source:',e['source_url'])
    return 0 if output else 1

if __name__=='__main__':sys.exit(run())
