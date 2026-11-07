"""Differential mission/pause scheduling with real coordinator bodies and surfaces.
The producer, input, timer and SDL doubles are explicit; not a full game replay.
GPL-3.0-or-later.
"""
import os
import subprocess
import tempfile
from pathlib import Path
from check_final_timer_equivalence import function
from check_pause_presentation import build_code
from mission_contract import OLD, NEW, canonical_mission
from pause_contract import NEW as PAUSE_NEW
BASELINE = 'a133afb8188a26f51e703b7a81576cf1b9264f67'

def main():
    root = Path(__file__).resolve().parents[2]
    current = (root/'Source/Fodder.cpp').read_text()
    original = subprocess.check_output(['git','show',BASELINE+':Source/Fodder.cpp'],cwd=root,text=True)
    assert current.count('        mSurface->CommitPauseBacking(scene);\n') == 1
    assert canonical_mission(current).replace('        mSurface->CommitPauseBacking(scene);\n', '') == original, 'All other mission/scene effects must stay unchanged'
    # Reuse real cSurface methods + synthetic SDL storage, not the pause driver.
    code = build_code(root).split('struct Window{')[0]
    code += (root/'tools/modernization/mission_presentation_fixture.inc').read_text()
    for name in ('Interrupt_Redraw','Video_Sleep','Phase_Paused','Video_SurfaceRender'):
        sig = 'void cFodder::'+name+'('
        code += function(current,sig)+'\n'
        old = function(original,sig).replace('cFodder::'+name+'(', 'cFodder::Legacy'+name+'(')
        if name == 'Video_Sleep': old = old.replace('Video_SurfaceRender(', 'LegacyVideo_SurfaceRender(')
        code += old+'\n'
    scheduled = function(current,'void cFodder::Video_SurfaceRender(')
    scheduled = scheduled.replace('cFodder::Video_SurfaceRender(', 'cFodder::ScheduledVideo_SurfaceRender(')
    pure = '''        const auto presented = openfodder::RasterizeMissionPresentation(scene);
        pSurface->ApplyPresentation(presented);'''
    assert NEW.count(pure) == 1
    scheduled = scheduled.replace(pure, '''        missionFrames.push_back({scene, mWindow->ends});
        for (int n=0;n<repeats;++n) {
'''+pure+'''
            mWindow->RenderAt(pSurface);
        }
        mWindow->FrameEnd();
        return;''')
    code += scheduled+'\n'
    sleep = function(current,'void cFodder::Video_Sleep(').replace('cFodder::Video_Sleep(', 'cFodder::ScheduledVideo_Sleep(')
    code += sleep.replace('Video_SurfaceRender(', 'ScheduledVideo_SurfaceRender(')+'\n'
    paused = function(current,'void cFodder::Phase_Paused(').replace('cFodder::Phase_Paused(', 'cFodder::ScheduledPhase_Paused(')
    start = PAUSE_NEW.index('        const auto presented')
    paused = paused.replace(PAUSE_NEW, PAUSE_NEW[:start]+'''        pauseFrames.push_back({scene, mWindow->ends});
        for (int n=0;n<repeats;++n) {
'''+PAUSE_NEW[start:]+'''
            mWindow->RenderAt(mSurface);
        }''').replace('''
        mWindow->RenderAt(mSurface);
        mWindow->FrameEnd();''','''
        mWindow->FrameEnd();''')
    code += paused+'\n'
    code += (root/'tools/modernization/mission_presentation_cases.inc').read_text()
    with tempfile.TemporaryDirectory(prefix='mission-equivalence-') as td:
        src=Path(td)/'test.cpp'; exe=Path(td)/'test'; src.write_text(code)
        subprocess.run(['g++','-std=c++14','-O1','-g','-fsanitize=address,undefined',
                        '-fno-sanitize-recover=all','-pthread','-I',str(root/'Source'),str(src),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True,env={**os.environ,'ASAN_OPTIONS':os.environ.get('ASAN_OPTIONS','detect_leaks=0')})
if __name__ == '__main__': main()
