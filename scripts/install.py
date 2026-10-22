#!/usr/bin/env python3
"""Safely copy the portable skill to one known project-local agent directory."""
import argparse,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'skills/market-analysis-atlas'
TARGETS={'codex':'.agents/skills','claude-code':'.claude/skills','cursor':'.agents/skills','opencode':'.opencode/skills','gemini-cli':'.agents/skills','universal':'.agents/skills'}
def install(project,agent,force=False,dry_run=False):
    dest=(project/TARGETS[agent]/SOURCE.name).resolve()
    if dest==SOURCE.resolve():return dest,'source-is-present'
    if dest.exists() and not force:raise FileExistsError('Already exists: '+str(dest))
    if dry_run:return dest,'dry-run'
    dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():
        if not dest.is_dir() or dest.is_symlink():raise ValueError('Refusing to overwrite symlink/non-directory')
        shutil.rmtree(dest)
    shutil.copytree(SOURCE,dest)
    return dest,'installed'
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project',type=Path,default=Path.cwd())
    p.add_argument('--agent',choices=sorted(TARGETS),default='universal')
    p.add_argument('--force',action='store_true');p.add_argument('--dry-run',action='store_true')
    a=p.parse_args(argv)
    try:
        dest,status=install(a.project.expanduser().resolve(),a.agent,a.force,a.dry_run)
        print(status,':',dest);return 0
    except (OSError,ValueError) as e:print('ERROR:',e,file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
