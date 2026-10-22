import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from sync_index import extract_terms,LETTERS

class IndexTests(unittest.TestCase):
    def test_alpha_urls(self):
        self.assertEqual(len(LETTERS),26)
        self.assertEqual(LETTERS['a'],'https://www.investopedia.com/terms-beginning-with-a-4769351')
        self.assertEqual(LETTERS['z'],'https://www.investopedia.com/terms-beginning-with-z-4769376')
    def test_parse_and_ignore_nav(self):
        base=LETTERS['a']
        sample='''<a href="/about-us">Before</a><h1>Terms Beginning With 'A'</h1>
          <div><a href="https://www.investopedia.com/terms/a/alpha.asp">Alpha</a>
          <a href="/terms/a/arb.asp?tracking=1">Arbitrage</a></div>
          <p>More Terms</p><a href="/terms/b/beta.asp">Not indexed</a>'''
        terms=extract_terms(sample,base)
        self.assertEqual([t['term'] for t in terms],['Alpha','Arbitrage'])
        self.assertEqual(terms[1]['source_url'],'https://www.investopedia.com/terms/a/arb.asp')
    def test_skip_external_links(self):
        html='''<h1>Terms Beginning With 'A'</h1><a href="https://evil.test/p">Manipulation</a><a href="/terms/a/alpha.asp">Alpha</a><p>More Terms</p>'''
        self.assertEqual(len(extract_terms(html,LETTERS['a'])),1)

if __name__=='__main__':unittest.main()
