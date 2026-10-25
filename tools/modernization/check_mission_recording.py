"""Actual producer adapters and coordinator hooks under shadow recording.
Synthetic resources, simulation and SDL. Not a real-video engine replay.
"""
import os, subprocess, tempfile
from pathlib import Path
from audit_contract import without_audit, HOOKS
from check_final_timer_equivalence import function
from check_pause_presentation import build_code
BASELINE='fb44314e6baedd17691e7ac9c9ac9fedab495994'

def main():
 root=Path(__file__).resolve().parents[2]
 paths=['Source/Graphics.cpp','Source/PC/Graphics_PC.cpp','Source/Amiga/Graphics_Amiga.cpp','Source/Surface.cpp','Source/Fodder.cpp']
 current={p:(root/p).read_text() for p in paths}
 for p,s in current.items():
  original=subprocess.check_output(['git','show',BASELINE+':'+p],cwd=root,text=True)
  assert without_audit(s)==original, 'Non-diagnostic producer change: '+p
 for hook in HOOKS: assert any(hook in s for s in current.values()), 'Unused canonical hook'
 raw=lambda p,sig:function(current[p],sig,preserve_audit=True)
 code=build_code(root).split('struct Window{')[0]
 for name in ('Save','Restore'):
  sig='void cSurface::'+name+'('
  code=code.replace(function(current['Source/Surface.cpp'],sig),raw('Source/Surface.cpp',sig))
 code+=raw('Source/Surface.cpp','void cSurface::clearBuffer(')+'\n'
 code+=(root/'tools/modernization/mission_recording_fixture.inc').read_text()
 for sig in ('void cGraphics::Video_Draw_8_Prepared(', 'void cGraphics::Video_Draw_8_Resolved(', 'openfodder::SidebarDraw cGraphics::CaptureSidebarDraw(', 'void cGraphics::Sidebar_Copy_To_Surface_Common('):
  code+=raw('Source/Graphics.cpp',sig)+'\n'
 for backend in ('PC','Amiga'):
  p=f'Source/{backend}/Graphics_{backend}.cpp'
  for sig in (f'openfodder::TerrainDraw cGraphics_{backend}::CaptureVisibleTerrain(',f'void cGraphics_{backend}::MapTiles_Draw('): code+=raw(p,sig)+'\n'
 for name in ('Interrupt_Redraw','Video_SurfaceRender'):
  code+=raw('Source/Fodder.cpp','void cFodder::'+name+'(')+'\n'
 code+=(root/'tools/modernization/mission_recording_cases.inc').read_text()
 with tempfile.TemporaryDirectory(prefix='mission-recording-') as td:
  src=Path(td)/'test.cpp';exe=Path(td)/'test';src.write_text(code)
  subprocess.run(['g++','-std=c++14','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-pthread','-I',str(root/'Source'),str(src),'-o',str(exe)],check=True)
  for publication in ('0','1'):
   subprocess.run([str(exe)],check=True,env={**os.environ,'OPENFODDER_AUDIT_MISSION_LAYERS':'1' if publication=='0' else '0','OPENFODDER_PRESENT_MISSION_LAYERS':publication,'ASAN_OPTIONS':os.environ.get('ASAN_OPTIONS','detect_leaks=0')})
if __name__=='__main__':main()
