#!/usr/bin/env python3
"""Opt-in, robots-aware catalog of article titles/URLs only; NEVER download article text/images.

Run only where site conditions and permissions allow crawling. This is an optional
link discovery utility; it is not an authorization or completeness guarantee.
"""
from __future__ import annotations
import argparse, html, json, sys, time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser
from atlas import SKILL, normalize
AGENT='MarketAnalysisAtlas-ReferenceIndexer/1.0 (+https://github.com/)'  # polite identifier
INDEX_URL='https://www.investopedia.com/financial-term-dictionary-4769738'
LETTERS={chr(ord('a')+i):f'https://www.investopedia.com/terms-beginning-with-{chr(ord("a")+i)}-{4769351+i}' for i in range(26)}

class TermLinks(HTMLParser):
    def __init__(self,base_url):
        super().__init__(convert_charrefs=True);self.base_url=base_url;self.in_h1=False;self.started=False
        self.ended=False;self.anchor=None;self.anchor_depth=0;self.terms=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='h1':self.in_h1=True
        if tag=='a' and self.started and not self.ended:
            self.anchor=(attrs.get('href',''),[])
    def handle_data(self,text):
        if self.in_h1 and 'Terms Beginning With' in text:self.started=True
        if 'More Terms' in text and self.started:self.ended=True
        if self.anchor:self.anchor[1].append(text)
    def handle_endtag(self,tag):
        if tag=='h1':self.in_h1=False
        if tag=='a' and self.anchor:
            href,title=self.anchor;self.anchor=None
            name=' '.join(''.join(title).split())
            url=urljoin(self.base_url,html.unescape(href))
            parsed=urlparse(url)
            if parsed.hostname not in ('investopedia.com','www.investopedia.com'):return
            if not parsed.path or 'terms-beginning' in parsed.path or parsed.path in ('/','/financial-term-dictionary-4769738'):return
            if not name or len(name)>160 or any(x in name.casefold() for x in ('sign up','read more','subscribe','newsletter')):return
            self.terms.append({'term':name,'source_url':url.split('#')[0].split('?')[0]})

def extract_terms(markup,base_url):
    parser=TermLinks(base_url);parser.feed(markup);return parser.terms

def fetch(url,timeout=25):
    with urlopen(Request(url,headers={'User-Agent':AGENT,'Accept':'text/html'}),timeout=timeout) as resp:
        typ=resp.headers.get('Content-Type','')
        if 'text/html' not in typ:raise ValueError('Unexpected content type: '+typ)
        return resp.read(4_000_000).decode('utf-8','replace')

def run(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--allow-site-fetch',action='store_true',help='Explicit authorization to perform remote requests')
    p.add_argument('--letters',default='abcdefghijklmnopqrstuvwxyz',help='Subset of letter pages')
    p.add_argument('--delay',type=float,default=3.0,help='Delay between requests (>=2 seconds)')
    p.add_argument('--output',type=Path,default=SKILL/'data/investopedia-index.jsonl')
    a=p.parse_args(argv)
    if not a.allow_site_fetch:p.error('No network by default. Pass --allow-site-fetch after reviewing site terms and robots rules.')
    if a.delay<2:p.error('--delay must be >= 2 seconds')
    # Explicit HTTP-success requirement: RobotFileParser.read() can silently
    # classify some HTTP failures as allow-all. Fail closed instead.
    robots_url='https://www.investopedia.com/robots.txt'
    rp=RobotFileParser();rp.set_url(robots_url)
    try:
        req=Request(robots_url,headers={'User-Agent':AGENT,'Accept':'text/plain'})
        with urlopen(req,timeout=25) as response:
            if response.status != 200:raise ValueError(f'HTTP {response.status}')
            policy=response.read(2_000_000).decode('utf-8','replace')
        if not policy.strip():raise ValueError('Empty robots policy')
        rp.parse(policy.splitlines())
    except Exception as e:p.error(f'Could not verify robots policy; fail closed: {e}')
    delay=max(a.delay, float(rp.crawl_delay(AGENT) or 0), float(rp.crawl_delay('*') or 0))
    seen={};logs=[]
    for letter in dict.fromkeys(a.letters.lower()):
        if letter not in LETTERS:p.error('Unsupported character: '+letter)
        url=LETTERS[letter]
        if not rp.can_fetch(AGENT,url):
            logs.append({'letter':letter,'state':'robots_disallowed'});continue
        try:
            raw=fetch(url)
            terms=extract_terms(raw,url)
            if not terms:logs.append({'letter':letter,'state':'no_terms_or_layout_changed'});continue
            for t in terms:
                key=normalize(t['term']);seen.setdefault(key,{'id':key.replace(' ','-'),'term':t['term'],
                    'category':'unclassified','status':'index_only','source_url':t['source_url'],
                    'provenance':'remote-title-and-link-only','source_index':url})
            logs.append({'letter':letter,'state':'ok','count':len(terms)})
        except Exception as exc:
            logs.append({'letter':letter,'state':'fetch_failed','error':str(exc)[:200]})
        time.sleep(delay)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(''.join(json.dumps(v,ensure_ascii=False,sort_keys=True)+'\n' for v in sorted(seen.values(),key=lambda d:d['term'].casefold())),encoding='utf-8')
    report={'source':INDEX_URL,'mode':'title-link-only','items':len(seen),'pages':logs,'complete':len([r for r in logs if r['state']=='ok'])==26}
    (a.output.parent/'index-sync-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))
    return 0 if len(seen) else 1
if __name__=='__main__':sys.exit(run())
