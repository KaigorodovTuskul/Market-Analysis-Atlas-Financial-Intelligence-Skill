#!/usr/bin/env python3
"""Import a lawfully supplied CSV containing term,source_url columns; title-only metadata."""
import argparse,csv,json,sys
from pathlib import Path
from urllib.parse import urlparse
from atlas import normalize,SKILL

def run(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv_path',type=Path)
    p.add_argument('--output',type=Path,default=SKILL/'data/imported-index.jsonl')
    a=p.parse_args(argv)
    unique={}
    with a.csv_path.open(encoding='utf-8-sig',newline='') as stream:
        for line in csv.DictReader(stream):
            term=(line.get('term') or '').strip();url=(line.get('source_url') or '').strip()
            if not term or len(term)>180 or urlparse(url).scheme not in ('http','https') or not urlparse(url).netloc:continue
            key=normalize(term)
            unique[key]={'id':key.replace(' ','-'),'term':term,'category':'unclassified','status':'index_only','source_url':url,'provenance':'user-provided-title-and-link'}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in unique.values()),encoding='utf-8')
    print('Imported',len(unique),'title/link records');return 0
if __name__=='__main__':sys.exit(run())
