#!/usr/bin/env python3
"""Reproducible release ZIP with a single top-level repository directory."""
from __future__ import annotations
import argparse,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXCLUDES={'.git','__pycache__','.pytest_cache','.venv','.mypy_cache'}

def pack(dst):
    dst=dst.expanduser().resolve()
    dst.parent.mkdir(parents=True,exist_ok=True)
    files=sorted(p for p in ROOT.rglob('*') if p.is_file() and not set(p.parts)&EXCLUDES and not p.name.endswith(('.pyc','.pyo')))
    with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for file in files:
            arcname='market-analysis-atlas/'+file.relative_to(ROOT).as_posix()
            info=zipfile.ZipInfo(arcname,date_time=(2026,10,23,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=(0o644<<16)
            z.writestr(info,file.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(dst) as z:
        corrupt=z.testzip()
        if corrupt:raise ValueError('Corrupt ZIP member: '+corrupt)
    print(f'Packed {len(files)} files into {dst} ({dst.stat().st_size:,} bytes)')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT.parent/'market-analysis-atlas.zip')
    pack(p.parse_args().output)
