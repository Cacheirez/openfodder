"""Real surface audit/publication with the C01 RGBA pilot; SDL is a fixture."""
import os, subprocess, tempfile, re
from pathlib import Path
from check_pause_presentation import build_code

def main():
    root=Path(__file__).resolve().parents[2]
    for file,name,expected in [('Source/PC/SpriteData_PC.hpp','stru_330FC','2248, eGFX_IN_GAME, 0, 0, 16, 14, 160, 0, 0'),('Source/Amiga/SpriteData_Amiga.hpp','stru_8C4A8','562, eGFX_IN_GAME, 0, 0, 2, 14, 13440, 0x0, 0')]:
        source=(root/file).read_text()
        rows=re.search(r'\b'+name+r'\[[^\]]*\]\s*=\s*\{\s*\{([^}]+)',source).group(1)
        assert rows.strip()==expected, 'Original anchor contract changed: '+name
    code=build_code(root).split('struct Window{')[0]+(root/'tools/modernization/soldier_art_cases.inc').read_text()
    with tempfile.TemporaryDirectory(prefix='soldier-art-') as td:
        generator=Path(td)/'prepare';header=Path(td)/'pixels.hpp'
        subprocess.run(['g++','-std=c++14','-O2','-I',str(root/'Source'),str(root/'tools/modernization/build_soldier_art.cpp'),'-o',str(generator)],check=True)
        subprocess.run([str(generator),str(root/'assets/modernization/soldier-c01/source.png'),str(header)],check=True)
        assert header.read_bytes()==(root/'Source/Utils/SoldierArtPixels.hpp').read_bytes(), 'C01 asset drift'
        src=Path(td)/'test.cpp';exe=Path(td)/'test';src.write_text(code)
        subprocess.run(['g++','-std=c++14','-O1','-g','-pthread','-fsanitize=address,undefined','-fno-sanitize-recover=all','-I',str(root/'Source'),str(src),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True,env={**os.environ,'OPENFODDER_PRESENT_MISSION_LAYERS':'1','OPENFODDER_SOLDIER_ART':'1','ASAN_OPTIONS':os.environ.get('ASAN_OPTIONS','detect_leaks=0')})
if __name__=='__main__':main()
