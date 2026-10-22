import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from atlas import normalize,rank,load

class AtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.items=load()
    def test_counts_and_categories(self):
        self.assertEqual(len(self.items),533)
        self.assertEqual(len({x['id'] for x in self.items}),len(self.items))
        self.assertEqual(len({x['category'] for x in self.items}),10)
    def test_exact_ranking_beats_fuzzy(self):
        exact=next(x for x in self.items if x['term']=='Duration')
        other=next(x for x in self.items if x['term']=='Modified Duration')
        self.assertGreater(rank(exact,'Duration'),rank(other,'Duration'))
    def test_normalization(self):
        self.assertEqual(normalize('  Piotroski  F-Score '),'piotroski f score')
    def test_grounded_formula_and_warnings(self):
        picks={x['term']:x for x in self.items}
        self.assertIn('projected distributable cash flows',picks['Discounted Cash Flow (DCF)']['definition'])
        self.assertIn('formula',picks['Relative Strength Index (RSI)'])
        self.assertIn('formula',picks['Gross Domestic Product (GDP)'])
        self.assertTrue(all(x['pitfall'] for x in self.items))
    def test_no_pretend_live_data(self):
        self.assertTrue(all(x['provenance']=='original-authored' for x in self.items))
        self.assertTrue(all('investopedia_index' in x for x in self.items))
        self.assertEqual(sum('source_url' in x for x in self.items),2)

if __name__=='__main__':unittest.main()
