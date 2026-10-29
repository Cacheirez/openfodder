"""Exercise actual menu transactions, INI persistence and SDL window methods.
SDL doubles deliberately inject failures; no physical desktop claim. GPL-3.0-or-later.
"""
from pathlib import Path
import os, subprocess, tempfile, sys
from check_final_timer_equivalence import function
ROOT=Path(__file__).resolve().parents[2]

def build():
    menu=(ROOT/'Source/OptionsMenu.cpp').read_text()
    params=(ROOT/'Source/Parameters.cpp').read_text()
    window=(ROOT/'Source/Window.cpp').read_text()
    prefix=r'''
#ifdef NDEBUG
#undef NDEBUG
#endif
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <cstdio>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <mutex>
#include <map>
#include "Utils/ini.hpp"
#ifdef _WIN32
int setenv(const char* k,const char* v,int){return _putenv_s(k,v);}
int unsetenv(const char* k){return _putenv_s(k, "");}
#endif
using int16=int16_t;using int32=int32_t;using uint8=uint8_t;using uint32=uint32_t;
enum class ePlatform{Any,Amiga,PC};enum class eGame{CF1,CF2};
#define protected public
#include "Parameters.hpp"
#undef protected
void sFodderParameters::PrepareOptions(){} bool sFodderParameters::ProcessCLI(int,char**){return true;}
struct ResourceMan{void addDir(const std::string&) {}} resource;
ResourceMan*g_ResourceMan=&resource;
std::string str_to_lower(std::string s){for(auto&c:s)c=char(std::tolower(c));return s;}
bool saveFail=false;
bool SDL_RenamePath(const char*a,const char*b){
 if(saveFail)return false;
#ifdef _WIN32
 // Model SDL replacement semantics, which differ from Windows std::rename.
 std::remove(b);
#endif
 return std::rename(a,b)==0;
}
bool SDL_RemovePath(const char*a){return std::remove(a)==0;}
struct SDL_Window{};
const unsigned SDL_WINDOW_FULLSCREEN=1,SDL_WINDOW_MAXIMIZED=2,SDL_WINDOW_RESIZABLE=4;
struct SDL_DisplayMode{int w=3840,h=2160;}display;
int calls=0,failAt=0;bool denied=false;
bool ok(){return ++calls!=failAt;}
struct Physical {int x=30,y=40,w=640,h=400;unsigned flags=4;bool relative=false;} physical;
bool SDL_GetWindowSize(SDL_Window*,int*w,int*h){*w=physical.w;*h=physical.h;return true;}
bool SDL_GetWindowPosition(SDL_Window*,int*x,int*y){*x=physical.x;*y=physical.y;return true;}
unsigned SDL_GetWindowFlags(SDL_Window*){return physical.flags;}
bool SDL_GetWindowRelativeMouseMode(SDL_Window*){return physical.relative;}
bool SDL_SetWindowFullscreen(SDL_Window*,bool v){if(!ok())return false;if(!denied)physical.flags=(physical.flags&~1u)|(v?1:0);return true;}
bool SDL_SyncWindow(SDL_Window*){return ok();}
bool SDL_RestoreWindow(SDL_Window*){if(!ok())return false;physical.flags&=~2u;return true;}
bool SDL_SetWindowResizable(SDL_Window*,bool v){if(!ok())return false;physical.flags=(physical.flags&~4u)|(v?4:0);return true;}
bool SDL_SetWindowSize(SDL_Window*,int w,int h){if(!ok())return false;if(!denied){physical.w=w;physical.h=h;}return true;}
bool SDL_SetWindowPosition(SDL_Window*,int x,int y){if(!ok())return false;physical.x=x;physical.y=y;return true;}
bool SDL_MaximizeWindow(SDL_Window*){if(!ok())return false;physical.flags|=2;return true;}
bool SDL_SetWindowRelativeMouseMode(SDL_Window*,bool v){if(!ok())return false;physical.relative=v;return true;}
using SDL_DisplayID=int;int SDL_GetPrimaryDisplay(){return 1;}
int SDL_GetDisplayForWindow(SDL_Window*){return 1;}
const SDL_DisplayMode* SDL_GetCurrentDisplayMode(int){return &display;}
struct cDimension{unsigned mWidth=320,mHeight=200;bool operator==(const cDimension& b)const{return mWidth==b.mWidth && mHeight==b.mHeight;}};
struct cWindow {
 SDL_Window raw;SDL_Window*mWindow=&raw;
 cDimension mOriginalResolution,mScreenSize;
 int sizeCalls=0,toggleCalls=0;
 void SetWindowSize(int){++sizeCalls;}void ToggleFullscreen(){++toggleCalls;}
 void SetOriginalRes(const cDimension&);void SetScreenSize(const cDimension&);
 uint8 mScaler=2,mScalerPrevious=2;bool mWindowMode=true,mResized=false;
 bool invalidated=false,band=true;
'''
    prefix+=function((ROOT/'Source/Window.hpp').read_text(),'struct PresentationState')+';\n'
    prefix+=r'''
 bool CapturePresentation(PresentationState&)const;
 bool ApplyPresentation(const PresentationState&);
 bool PreviewPresentation(bool,int,bool,bool);
 int16 CalculateFullscreenSize();
 void InvalidateScreenTransform(){invalidated=true;}
 void SetMissionCursorInBand(bool b){band=b;}
 bool isFullscreen()const{return !mWindowMode;}
 void SetMouseSpeed(float){}
};
#define private public
#include "OptionsMenu.hpp"
#undef private
struct cFodder;
struct sGUI_Element {int field_0=0;int16 mX=0,mY=0,mWidth=0,mHeight=0;
 void(cFodder::*mMouseInsideFuncPtr)()=nullptr;
 void(*mOnClick)(void*,int16,int16)=nullptr;void*mCtx=nullptr;int16 mAction=0,mArg=0;};
struct cFodder{sFodderParameters start,runtime; sFodderParameters*mStartParams=&start,*mParams=&runtime;
 cWindow window;cWindow*mWindow=&window;int mMouseX=0,mMouseY=0;
 int16 mMouse_Button_Left_Toggle=0,mMouse_Button_Right_Toggle=0,mButtonPressLeft=0,mButtonPressRight=0;
 int mMouseButtonStatus=0;bool mMouse_Exit_Loop=false,mMouse_Button_LeftRight_Toggle=false;
 bool mMouse_Button_LeftRight_Toggle2=false,mSquad_Member_Fire_CoolDown_Override=false;
 sGUI_Element*mGUI_Elements=nullptr;
 void Mouse_UpdateButtons();int16 Mouse_Button_Left_Toggled();
 void GUI_Handle_Element_Mouse_Check(sGUI_Element*);void OptionsClickFrame();
}fodder;
cFodder*g_Fodder=&fodder;
uint32_t now=1000;uint32_t now_ms_u32(){return now;}
#define PLATFORM_BASED(a,b) (a)
'''
    gui=(ROOT/'Source/GUI_Element.cpp').read_text()
    mouse=(ROOT/'Source/Mouse.cpp').read_text()
    loop=function(menu,'bool cFodder::Options_Menu_Run')
    click=loop.split('// Mouse click processing',1)[1].split('if (mPhase_EscapeKeyAbort',1)[0]
    assert 'GUI_Handle_Element_Mouse_Check(mGUI_Elements);' in click
    code=prefix
    for name in ['CapturePresentation','ApplyPresentation','PreviewPresentation','CalculateFullscreenSize']:
        sig=('int16' if name=='CalculateFullscreenSize' else 'bool')+' cWindow::'+name
        code+=function(window,sig)+'\n'
    for sig in ['void cWindow::SetOriginalRes','void cWindow::SetScreenSize']:code+=function(window,sig)+'\n'
    for name in ['SaveIni','ProcessINI']:code+=function(params,'bool sFodderParameters::'+name)+'\n'
    code+=function(menu,'static int clamp_int')+'\n'
    code+=function(menu,'static inline bool IsAdjustAction').replace('GUIACT_', 'cOptionsMenu::GUIACT_')+'\n'
    code+='cOptionsMenu::cOptionsMenu()=default; cOptionsMenu::~cOptionsMenu()=default;\n'
    for ret,name in [('void','Open'),('void','Close'),('bool','AllowInput'),('void','BuildItems'),('void','BuildPageItems'),('void','ChangePage'),('void','RestoreSnapshot'),('bool','PresentationChanged'),('void','SaveOrPreview'),('void','Confirm'),('int','GetInt'),('void','SetInt'),('std::string','FormatValue'),('void','Tick'),('void','OnUp'),('void','OnDown'),('void','OnBack'),('void','Adjust'),('void','ResetDefaults'),('void','OnRowClick')]:
        code+=function(menu,ret+' cOptionsMenu::'+name)+'\n'
    code+=function(mouse,'void cFodder::Mouse_UpdateButtons')+'\n'
    code+=function(gui,'int16 cFodder::Mouse_Button_Left_Toggled')+'\n'
    code+=function(gui,'void cFodder::GUI_Handle_Element_Mouse_Check')+'\n'
    code+='void cFodder::OptionsClickFrame(){'+click+'}\n'
    code+=function(menu,'static void Gui_OptionsMenu_Click')+'\n'
    code+=r'''
std::string disk(){std::ifstream f("openfodder.ini");std::ostringstream s;s<<f.rdbuf();return s.str();}
void reset(){fodder.start.clear();fodder.runtime.clear();fodder.start.mWindowMode=true;
 fodder.start.mMouseAlternative=true;fodder.runtime=fodder.start;physical={};
 fodder.window.mWindowMode=true;fodder.window.mScaler=2;fodder.window.mScalerPrevious=2;
 calls=failAt=0;denied=saveFail=false;now+=20000;assert(fodder.start.SaveIni());}
void edit(cOptionsMenu&m){m.SetInt(cOptionsMenu::OPT_PRESENTATION,1);m.SetInt(cOptionsMenu::OPT_WINDOW_SCALE,3);}
int main(){
 unsetenv("OPENFODDER_MISSION_SCREEN_TRANSFORM");unsetenv("OPENFODDER_MISSION_SCREEN_FIT");
 // Old/absent/invalid preference defaults to classic, round trip and overrides.
 for(const char*value:{"", "classic", "garbage", "FIT", "fit"}) {
  std::ofstream("openfodder.ini")<<"[openfodder]\npresentation="<<value<<"\n";
  sFodderParameters p;assert(p.ProcessINI());assert(p.mFitPresentation==(std::string(value)=="fit"));
 }
 std::remove("openfodder.ini");sFodderParameters p;assert(p.SaveIni());
 p.mFitPresentation=true;assert(p.SaveIni());sFodderParameters loaded;assert(loaded.ProcessINI());assert(loaded.ScreenFitEnabled());
 setenv("OPENFODDER_MISSION_SCREEN_FIT","0",1);assert(!loaded.ScreenFitEnabled());unsetenv("OPENFODDER_MISSION_SCREEN_FIT");
 // Edit/defaults/cancel never write or apply anything.
 reset();auto original=disk();{cOptionsMenu m;m.Open();edit(m);m.ResetDefaults();assert(disk()==original);assert(!fodder.start.mFitPresentation);m.OnBack();assert(!m.WasApplied());}
 // Real mouse latch -> actual loop dispatch -> GUI hit test -> actual menu callback.
 // A normal press held >90ms used to toggle repeatedly; release must rearm it.
 for(int option:{cOptionsMenu::OPT_PRESENTATION,cOptionsMenu::OPT_ALTERNATE_MOUSE,cOptionsMenu::OPT_MOUSE_LOCKED}) {
  reset();cOptionsMenu m;m.Open();int row=0;
  while(m.mItems[row].id!=option)++row;
  sGUI_Element elements[2];elements[0].field_0=1;elements[0].mWidth=200;elements[0].mHeight=100;
  elements[0].mOnClick=Gui_OptionsMenu_Click;elements[0].mCtx=&m;
  elements[0].mAction=cOptionsMenu::GUIACT_OPT_ROW_PRIMARY;elements[0].mArg=row;
  fodder.mGUI_Elements=elements;fodder.mMouseX=0;fodder.mMouseY=0;
  fodder.mMouseButtonStatus=0;fodder.Mouse_UpdateButtons();
  const int before=m.GetInt(option);auto saved=disk();
  for(int frame=0;frame<120;++frame){now+=16;fodder.mMouseButtonStatus=1;fodder.Mouse_UpdateButtons();fodder.OptionsClickFrame();assert(m.GetInt(option)==!before);}
  assert(disk()==saved);fodder.mMouseButtonStatus=0;fodder.Mouse_UpdateButtons();fodder.OptionsClickFrame();
  now+=150;fodder.mMouseButtonStatus=1;fodder.Mouse_UpdateButtons();fodder.OptionsClickFrame();assert(m.GetInt(option)==before);
  // Press outside then drag inside: no action without a new press.
  fodder.mMouseButtonStatus=0;fodder.Mouse_UpdateButtons();
  now+=150;fodder.mMouseX=500;fodder.mMouseButtonStatus=1;fodder.Mouse_UpdateButtons();fodder.OptionsClickFrame();
  fodder.mMouseX=0;now+=150;fodder.Mouse_UpdateButtons();fodder.OptionsClickFrame();assert(m.GetInt(option)==before);
 }
 // Holding SAVE across the redraw must not confirm KEEP automatically.
 reset();{cOptionsMenu m;m.Open();edit(m);sGUI_Element elements[2];
 elements[0].field_0=1;elements[0].mWidth=200;elements[0].mHeight=100;
 elements[0].mOnClick=Gui_OptionsMenu_Click;elements[0].mCtx=&m;elements[0].mAction=cOptionsMenu::GUIACT_OPT_SAVE;
 fodder.mGUI_Elements=elements;fodder.mMouseX=fodder.mMouseY=0;
 fodder.mMouseButtonStatus=0;fodder.Mouse_UpdateButtons();auto saved=disk();
 for(int frame=0;frame<120;++frame){now+=16;fodder.mMouseButtonStatus=1;fodder.Mouse_UpdateButtons();fodder.OptionsClickFrame();assert(m.mConfirmation.pending&&!m.WasApplied()&&disk()==saved);}
 fodder.mMouseButtonStatus=0;fodder.Mouse_UpdateButtons();fodder.OptionsClickFrame();
 fodder.mMouseButtonStatus=1;fodder.Mouse_UpdateButtons();fodder.OptionsClickFrame();assert(m.WasApplied());}
 puts("PASS: actual mouse/GUI/menu dispatch, held toggles, release/repress, outside drag and separate SAVE/KEEP clicks");
 // Countdown boundary, including wraparound. No frame/simulation counters involved.
 for(uint32_t start:{100u,0xfffffff0u}) {
  reset();original=disk();now=start;cOptionsMenu m;m.Open();edit(m);m.SaveOrPreview();assert(m.mConfirmation.pending);
  assert(disk()==original);now+=14999;m.Tick();assert(m.mConfirmation.pending);
  ++now;m.Tick();assert(!m.mConfirmation.pending && !fodder.start.mFitPresentation);
  assert(physical.w==640 && physical.h==400 && !m.WasApplied());
 }
 // Expired KEEP must revert even if Tick has not run yet.
 reset();{cOptionsMenu m;m.Open();edit(m);m.SaveOrPreview();now+=15000;m.Confirm();assert(!m.WasApplied()&&!fodder.start.mFitPresentation);}
 // Confirm and reload, then explicit cancel and escape.
 reset();{cOptionsMenu m;m.Open();edit(m);m.SaveOrPreview();assert(physical.w==960);m.Confirm();assert(m.WasApplied());sFodderParameters v;assert(v.ProcessINI()&&v.mFitPresentation&&v.mWindowScale==3);}
 for(bool escape:{false,true}){reset();cOptionsMenu m;m.Open();edit(m);m.SaveOrPreview();
 if(escape)m.OnBack();else m.OnRowClick(cOptionsMenu::GUIACT_OPT_CANCEL,0);
 assert(!m.mConfirmation.pending&&!fodder.start.mFitPresentation&&physical.w==640);}
 // Every SDL request can fail; original state remains recoverable and no save occurs.
 reset();int count;{cOptionsMenu m;m.Open();edit(m);m.SaveOrPreview();count=calls;m.RestoreSnapshot();}
 for(int i=1;i<=count;++i){reset();auto before=disk();cOptionsMenu m;m.Open();edit(m);failAt=i;m.SaveOrPreview();assert(!m.mConfirmation.pending);assert(!m.WasApplied());assert(disk()==before);assert(physical.w==640);assert(fodder.window.invalidated&&!fodder.window.band);}
 reset();{cOptionsMenu m;m.Open();edit(m);denied=true;m.SaveOrPreview();assert(!m.mConfirmation.pending&&!m.WasApplied());}
 reset();{auto before=disk();cOptionsMenu m;m.Open();edit(m);m.SaveOrPreview();saveFail=true;m.Confirm();assert(!m.WasApplied()&&disk()==before&&physical.w==640);}
 // Failed restoration retains its snapshot, blocks saving, and can be retried.
 reset();{auto before=disk();cOptionsMenu m;m.Open();edit(m);m.SaveOrPreview();
 failAt=calls+1;m.RestoreSnapshot();assert(m.mPreviewApplied && m.mStatus=="RESTORE FAILED");
 assert(disk()==before);failAt=0;m.SaveOrPreview();assert(!m.mPreviewApplied && !m.WasApplied() && disk()==before && physical.w==640);}
 // External F11/resize during confirmation cannot save a stale candidate.
 reset();{auto before=disk();cOptionsMenu m;m.Open();edit(m);m.SaveOrPreview();physical.w+=10;m.Confirm();assert(!m.WasApplied()&&disk()==before&&physical.w==640);}
 // Fullscreen/maximized snapshot restoration and fresh geometry invalidation.
 for(unsigned flags:{0u,2u,4u,6u,1u,5u}){reset();physical.flags=flags;fodder.window.mWindowMode=!(flags&1);
 cWindow::PresentationState state;assert(fodder.window.CapturePresentation(state));
 assert(fodder.window.PreviewPresentation(true,3,true,false));assert(fodder.window.ApplyPresentation(state));
 assert(physical.flags==flags&&physical.w==640&&physical.x==30&&physical.y==40);}
 // Logical scene changes keep an explicitly maximized FIT window maximized.
 reset();fodder.start.mFitPresentation=true;physical.flags=6;
 auto& win=fodder.window;win.sizeCalls=win.toggleCalls=0;
 win.SetOriginalRes({320,225});assert(win.sizeCalls==0 && win.toggleCalls==0 && physical.flags==6);
 win.SetScreenSize({320,225});assert(win.invalidated);
 fodder.start.mFitPresentation=false;win.SetOriginalRes({320,200});assert(win.sizeCalls==1);
 win.mWindowMode=false;win.SetOriginalRes({320,225});assert(win.toggleCalls==2);
 puts("PASS: real options menu, INI round trips/overrides, 15s/wraparound, confirm/cancel/escape, failed save, SDL failure injection and restored window state");
}
'''
    return code

def main():
    with tempfile.TemporaryDirectory(prefix='presentation-options-') as td:
        src=Path(td)/'test.cpp';exe=Path(td)/'test';src.write_text(build())
        subprocess.run(['g++','-std=c++14','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-I',str(ROOT/'Source'),str(src),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],cwd=td,check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0'})
if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--emit': Path(sys.argv[2]).write_text(build())
    else: main()
