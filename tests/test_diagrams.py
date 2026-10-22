import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class DiagramTests(unittest.TestCase):
    def test_manifest_matches_images(self):
        import json
        skill=ROOT/'skills/market-analysis-atlas'
        entries=json.loads((skill/'data/patterns.json').read_text(encoding='utf-8'))
        self.assertEqual(len(entries),100)
        for e in entries:
            image=skill/'data'/e['image']
            self.assertTrue(image.is_file(),e['term'])
            src=image.read_text(encoding='utf-8')
            self.assertIn('Synthetic schematic',src)
            self.assertIn('role="img"',src)
            self.assertNotIn('investopedia.com',src)

if __name__=='__main__':unittest.main()
