"""Presentation sink provenance/geometry and actual PNG storage replacement.
Actual cSurface methods, controlled SDL/STB doubles. No real decoder/GPU claim.
GPL-3.0-or-later.
"""
import os
from pathlib import Path
import subprocess
import tempfile
from check_final_timer_equivalence import function
from check_pause_presentation import build_code
from audit_contract import without_audit
BASELINE = '049439d56126e95b56eebd183e4f42610d8b6821'

def main():
    root=Path(__file__).resolve().parents[2]
    surface=without_audit((root/'Source/Surface.cpp').read_text())
    original=subprocess.check_output(['git','show',BASELINE+':Source/Surface.cpp'],cwd=root,text=True)
    # All original surface operations remain identical except these four
    # presentation methods and a fresh identity after successful replacement.
    canonical=surface
    for name,oldtype,newtype in [('CapturePresentation','openfodder::PresentationSurface','openfodder::PresentationSurface'),
                                  ('ApplyPresentation','void','bool'),('CommitPauseBacking','void','bool')]:
        canonical=canonical.replace(function(surface,newtype+' cSurface::'+name+'('),
                                    function(original,oldtype+' cSurface::'+name+'('))
    matcher=function(surface,'bool cSurface::PresentationDestinationMatches(')
    canonical=canonical.replace(matcher+'\n\n','')
    renewal='    mPresentationDestination = std::make_shared<const openfodder::PresentationDestination>();\n'
    assert canonical.count(renewal)==1
    assert canonical.replace(renewal,'')==original, 'Unexpected changes to classic surface effects'
    prefix=build_code(root).split('struct Window{')[0]
    # Count uploads so rejection must also leave SDL untouched.
    prefix=prefix.replace('void SDL_UpdateTexture(SDL_Texture*,void*,void*,int){}',
                          'int updates=0;void SDL_UpdateTexture(SDL_Texture*,void*,void*,int){++updates;}')
    code=prefix+(root/'tools/modernization/presentation_destination_fixture.inc').read_text()
    code+=function(surface,'bool cSurface::LoadPng(')
    code+=(root/'tools/modernization/presentation_destination_cases.inc').read_text()
    with tempfile.TemporaryDirectory(prefix='presentation-destination-') as td:
        src=Path(td)/'test.cpp';exe=Path(td)/'test';src.write_text(code)
        subprocess.run(['g++','-std=c++14','-O1','-g','-fsanitize=address,undefined',
                        '-fno-sanitize-recover=all','-I',str(root/'Source'),str(src),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True,env={**os.environ,'ASAN_OPTIONS':os.environ.get('ASAN_OPTIONS','detect_leaks=0')})
if __name__=='__main__':main()
