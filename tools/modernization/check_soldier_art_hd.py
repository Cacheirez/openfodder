"""Generate original C01 densities and exercise the isolated C++ compositor."""
from pathlib import Path
import os, subprocess, tempfile, hashlib, json
ROOT=Path(__file__).resolve().parents[2]
def main():
    source=ROOT/'assets/modernization/soldier-c01/source.png'
    assert hashlib.sha256(source.read_bytes()).hexdigest()=='9fb5dd519e8589de6c6420e4385c8eb2e12ac1f24c83f9a64678a2d943e31c77'
    with tempfile.TemporaryDirectory(prefix='c01-hd-') as td:
        td=Path(td);gen=td/'prepare';exe=td/'test'
        subprocess.run(['g++','-std=c++14','-O2','-I',str(ROOT/'Source'),str(ROOT/'tools/modernization/build_soldier_art.cpp'),'-o',str(gen)],check=True)
        for d in (1,8,12):
            subprocess.run([str(gen),str(source),str(td/f'c01_{d}.hpp'),str(d)],check=True)
        assert (td/'c01_1.hpp').read_bytes()==(ROOT/'Source/Utils/SoldierArtPixels.hpp').read_bytes()
        subprocess.run(['g++','-std=c++14','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-I',str(ROOT/'Source'),'-I',str(td),str(ROOT/'tools/modernization/test_soldier_art_hd.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0'})
if __name__=='__main__':main()
