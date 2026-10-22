#!/usr/bin/env python3
"""Dependency-free structural, content and SVG integrity checks."""
import json,re,sys
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'skills/market-analysis-atlas'

def validate():
    errors=[]
    skill=(S/'SKILL.md').read_text(encoding='utf-8')
    if not skill.startswith('---\n'):errors.append('No frontmatter')
    if not re.search(r'(?m)^name: market-analysis-atlas\s*$',skill):errors.append('Unexpected skill name')
    if not re.search(r'(?m)^description: .+',skill):errors.append('Missing description')
    if len(skill.splitlines())>500:errors.append('SKILL.md should stay <=500 lines')
    for doc in [S/'SKILL.md',*S.rglob('*.md'),ROOT/'README.md',ROOT/'README.ru.md']:
        if not doc.is_file():errors.append('Missing file: '+str(doc));continue
        for link in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):
            if link.startswith(('https://','http://','#','mailto:')):continue
            if any(x in link for x in ('?','%20')):continue
            target=(doc.parent/link.split('#',1)[0]).resolve()
            if not target.is_relative_to(ROOT.resolve()) or not target.exists():errors.append(f'Broken reference {doc}: {link}')
    try:
        terms=[json.loads(l) for l in (S/'data/terms.jsonl').read_text(encoding='utf-8').splitlines()]
    except Exception as e:return ['Unreadable dataset: '+str(e)]
    ids=Counter(t.get('id','') for t in terms)
    if len(terms)<500:errors.append(f'Expected >=500 substantive terms, got {len(terms)}')
    if any(n!=1 for n in ids.values()):errors.append('Duplicate IDs')
    for t in terms:
        for key in ('id','term','category','definition','pitfall','provenance','investopedia_index'):
            if not t.get(key):errors.append('Missing '+key+' on '+str(t.get('term')))
        if len(t['definition'])<40:errors.append('Definition too short: '+t['term'])
        if t['provenance']!='original-authored':errors.append('Unexpected provenance')
    images=list((S/'assets/charts').glob('*.svg'))
    if len(images)!=100:errors.append(f'Expected 100 SVGs, got {len(images)}')
    for im in images:
        source=im.read_text(encoding='utf-8')
        if '<svg ' not in source or 'Not market data' not in source:errors.append('Nonconforming schematic: '+im.name)
    try:
        patterns=json.loads((S/'data/patterns.json').read_text(encoding='utf-8'))
        if len(patterns)!=100:errors.append('Invalid patterns manifest')
        for p in patterns:
            if not (S/'data'/p['image']).is_file():errors.append('Missing pattern graphic: '+p['id'])
    except (ValueError,OSError,KeyError) as e:errors.append('Invalid patterns manifest: '+str(e))
    return errors

if __name__=='__main__':
    failures=validate()
    if failures:
        print('\n'.join('FAIL: '+str(x) for x in failures),file=sys.stderr);sys.exit(1)
    print('PASS: manifest, frontmatter, 533 definitions, 100 original schematics, references')
