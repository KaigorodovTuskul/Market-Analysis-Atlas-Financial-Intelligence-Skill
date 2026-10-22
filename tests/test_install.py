import sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from install import install

class InstallerTests(unittest.TestCase):
    def test_dry_run_and_install(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            dest,state=install(root,'codex',dry_run=True)
            self.assertEqual(state,'dry-run');self.assertFalse(dest.exists())
            dest,state=install(root,'codex')
            self.assertEqual(state,'installed');self.assertTrue((dest/'SKILL.md').exists())
            with self.assertRaises(FileExistsError):install(root,'codex')
            dest,state=install(root,'codex',force=True)
            self.assertEqual(state,'installed')

if __name__=='__main__':unittest.main()
