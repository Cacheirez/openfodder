"""Actual Window render/present/inverse and alternate Mouse block, with SDL doubles.
No real GPU/input claim. GPL-3.0-or-later.
"""
from pathlib import Path
import os, subprocess, tempfile
from check_final_timer_equivalence import function
from screen_mouse_contract import without_screen_mouse
from screen_window_contract import verify_window_integration

ROOT=Path(__file__).resolve().parents[2]


def build():
    window=(ROOT/'Source/Window.cpp').read_text()
    classic_window=subprocess.check_output(['git','show','ff15219680b289abf207fdc23fc436a9f390e649:Source/Window.cpp'],cwd=ROOT,text=True)
    verify_window_integration(window,classic_window)
    mouse=(ROOT/'Source/Mouse.cpp').read_text()
    old=subprocess.check_output(['git','show','7eeb6f777cc2ddfd9c615a2a94eef69bd3625c41:Source/Mouse.cpp'],cwd=ROOT,text=True)
    signature='if (mStartParams->mMouseAlternative)'
    block=function(mouse,signature)
    assert without_screen_mouse(mouse)==old, 'Other mouse effects changed'
    prefix=r'''
#include <cassert>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <cstdio>
#include <string>
#include <mutex>
#include <atomic>
#include <stdexcept>
#include "Utils/ScreenTransform.hpp"
using int16=int16_t;
struct SDL_Window{};struct SDL_Renderer{};struct SDL_Texture{};
struct SDL_FRect{float x,y,w,h;};struct SDL_Rect{int x,y,w,h;};
enum SDL_RendererLogicalPresentation{SDL_LOGICAL_PRESENTATION_DISABLED,SDL_LOGICAL_PRESENTATION_LETTERBOX};
struct SDL_DisplayMode{int w=1920,h=1080;};using SDL_DisplayID=int;
int ww=640,wh=400,pw=640,ph=400;bool drawOK=true,presentOK=true,target=false,clip=false,sizeOK=true;
float rendererScale=1;int viewportX=0;bool logical=false;
SDL_FRect drawnSource{},drawnDestination{};int draws=0;
bool SDL_GetWindowSize(SDL_Window*,int*w,int*h){*w=ww;*h=wh;return sizeOK;}
bool SDL_GetRenderOutputSize(SDL_Renderer*,int*w,int*h){*w=pw;*h=ph;return sizeOK;}
SDL_Texture* SDL_GetRenderTarget(SDL_Renderer*){static SDL_Texture t;return target?&t:nullptr;}
bool SDL_GetRenderScale(SDL_Renderer*,float*x,float*y){*x=*y=rendererScale;return true;}
bool SDL_GetRenderViewport(SDL_Renderer*,SDL_Rect*r){*r={viewportX,0,pw,ph};return true;}
bool SDL_RenderClipEnabled(SDL_Renderer*){return clip;}
bool SDL_GetRenderLogicalPresentation(SDL_Renderer*,int*w,int*h,SDL_RendererLogicalPresentation*m){*w=*h=0;*m=logical?SDL_LOGICAL_PRESENTATION_LETTERBOX:SDL_LOGICAL_PRESENTATION_DISABLED;return true;}
bool SDL_RenderTexture(SDL_Renderer*,SDL_Texture*,SDL_FRect*s,SDL_FRect*d){drawnSource=*s;drawnDestination=*d;++draws;return drawOK;}
bool SDL_RenderPresent(SDL_Renderer*){return presentOK;}
bool systemCursor=false;
bool SDL_ShowCursor(){systemCursor=true;return true;}
bool SDL_HideCursor(){systemCursor=false;return true;}
void SDL_SetRenderDrawColor(SDL_Renderer*,int,int,int,int){}void SDL_RenderClear(SDL_Renderer*){}
SDL_DisplayID SDL_GetDisplayForWindow(SDL_Window*){return 1;}SDL_DisplayID SDL_GetPrimaryDisplay(){return 1;}
const SDL_DisplayMode* SDL_GetCurrentDisplayMode(SDL_DisplayID){static SDL_DisplayMode m;return &m;}
struct cDimension{int mWidth=320,mHeight=200;int getWidth()const{return mWidth;}int getHeight()const{return mHeight;}};
struct cSurface{int width=352,height=232;SDL_Texture* GetTexture(){return nullptr;}int GetWidth(){return width;}int GetHeight(){return height;}};
struct cWindow{
 SDL_Window*mWindow=nullptr;SDL_Renderer*mRenderer=nullptr;bool mWindowMode=true;
 cDimension mScreenSize;std::mutex mScreenTransformMutex;
 openfodder::ScreenTransform mPendingScreenTransform,mPresentedScreenTransform;
 bool mPendingScreenClassic=false,mPresentedScreenClassic=false;
 std::atomic<bool> mMissionCursorInBand{false};bool mSystemMissionCursorShown=false;
 void SetMissionCursorInBand(bool v){mMissionCursorInBand.store(v);}
 bool IsMissionCursorInBand() const;
 cDimension GetWindowSize(){return {640,mScreenSize.mHeight*2};}
 void RenderAt(cSurface*,bool=false);void RenderShrunk(cSurface*);void FrameEnd();void InvalidateScreenTransform();
 openfodder::ScreenMouseResult MapMissionMouse(int,int,int16&,int16&);
};
struct Params{bool mUnitTesting=true,mMouseAlternative=true,mMouseLocked=false,mIntegerScaling=false,mDemoPlayback=false;};
struct cFodder{
 Params params;Params*mParams=&params,*mStartParams=&params;cWindow*mWindow=nullptr;
 cSurface* mSurfaceMapOverview=nullptr;
 bool mPhase_In_Progress=true,mPhase_Paused=false,mPhase_ShowMapOverview=false,mInterruptCallback=false,mWindow_Focus=true;
 struct {int mX=0,mY=0;}mMouse_EventLastPosition;
 int16 mInputMouseX=0,mInputMouseY=0;int mMouse_EventLastButtonsPressed=0,mMouseButtonStatus=0;
 void HandleAlternate();
};cFodder fodder; cFodder*g_Fodder=&fodder;
const int16 MOUSE_POSITION_X_ADJUST=-32,MOUSE_POSITION_Y_ADJUST=4;
'''
    code=prefix
    for sig in ['void cWindow::RenderAt(', 'void cWindow::RenderShrunk(', 'void cWindow::FrameEnd(',
                'bool cWindow::IsMissionCursorInBand(', 'void cWindow::InvalidateScreenTransform(', 'openfodder::ScreenMouseResult cWindow::MapMissionMouse(']:
        code+=function(window,sig)+'\n'
    code+='void cFodder::HandleAlternate(){const cDimension scale{2,2};mMouseButtonStatus=mMouse_EventLastButtonsPressed;'+block+'}\n'
    code+=r'''
int main(){
 setenv("OPENFODDER_MISSION_SCREEN_TRANSFORM","1",1);
 cWindow win;cSurface image;fodder.mWindow=&win;
 using R=openfodder::ScreenMouseResult;int16 x=123,y=456;
 assert(win.MapMissionMouse(100,100,x,y)==R::Blocked);
 win.RenderAt(&image,true);
 assert(win.MapMissionMouse(100,100,x,y)==R::Blocked); // pending is not presented
 win.FrameEnd();
 assert(drawnSource.x==16 && drawnSource.y==16 && drawnDestination.w==640);
 // Exhaustive legacy quantization at every window coordinate, PC and Amiga.
 int points=0;
 for(int h:{200,225}){
   wh=ph=h*2;win.mScreenSize.mHeight=h;win.RenderAt(&image,true);win.FrameEnd();
   for(int py=0;py<wh;++py)for(int px=0;px<ww;++px){
     assert(win.MapMissionMouse(px,py,x,y)==R::Mapped);
     assert(x==px/2-32 && y==py/2+4);++points;
   }
 }
 assert(points==544000);
 wh=ph=400;win.mScreenSize.mHeight=200;
 // Actual destination remains 640x400; enlarged window leaves uncovered bands.
 ww=pw=1001;wh=ph=777;win.RenderAt(&image,true);win.FrameEnd();
 assert(win.MapMissionMouse(640,200,x,y)==R::Blocked);
 assert(win.MapMissionMouse(300,400,x,y)==R::Blocked);
 assert(win.MapMissionMouse(-1,20,x,y)==R::Blocked);
 // Held band press cannot become a world order on re-entry.
 fodder.mMouse_EventLastPosition={800,200};fodder.mMouse_EventLastButtonsPressed=1;
 fodder.HandleAlternate();assert(fodder.mMouseButtonStatus==0);
 fodder.mMouse_EventLastPosition={200,200};fodder.HandleAlternate();
 assert(fodder.mMouseButtonStatus==0 && fodder.mInputMouseX==68 && fodder.mInputMouseY==104);
 fodder.mMouse_EventLastButtonsPressed=0;fodder.HandleAlternate();
 fodder.mMouse_EventLastButtonsPressed=1;fodder.HandleAlternate();assert(fodder.mMouseButtonStatus==1);
 // DPI inverse must track what was actually drawn, not multiply the canvas again.
 ww=320;wh=200;pw=640;ph=400;win.RenderAt(&image,true);win.FrameEnd();
 assert(win.MapMissionMouse(160,100,x,y)==R::Mapped && x==128 && y==104);
 auto origin=win.mPresentedScreenTransform.StorageToOutput({16,16});assert(origin.x==0 && origin.y==0);
 ++ww;assert(win.MapMissionMouse(160,100,x,y)==R::Blocked);--ww;
 win.InvalidateScreenTransform();assert(win.MapMissionMouse(100,100,x,y)==R::Blocked);
 win.RenderAt(&image,true);presentOK=false;win.FrameEnd();assert(win.MapMissionMouse(100,100,x,y)==R::Blocked);presentOK=true;
 drawOK=false;win.RenderAt(&image,true);win.FrameEnd();assert(win.MapMissionMouse(100,100,x,y)==R::Blocked);drawOK=true;

 // Fit: independent expected rect and inverse, all target modes and DPI ratios.
 setenv("OPENFODDER_MISSION_SCREEN_FIT","1",1);
 int fitCases=0;
 for(auto size : {cDimension{640,480},{800,600},{1024,768},{1152,864},
    {1280,960},{1400,1050},{1600,1200},{1920,1440},{2048,1536},{2880,2160},
    {1280,720},{1600,900},{1920,1080},{2560,1440},{3200,1800},{3840,2160},
    {1366,768},{2560,1920},{1001,777}}) {
  for(int dpi : {100,125,150,175,200,300})for(int h : {200,225}) {
   pw=size.mWidth;ph=size.mHeight;ww=pw*100/dpi;wh=ph*100/dpi;
   win.mScreenSize.mHeight=h;
   win.InvalidateScreenTransform();
   assert(win.MapMissionMouse(ww/2,wh/2,x,y)==R::Blocked);
   win.RenderAt(&image,true);win.FrameEnd();
   assert(win.mPresentedScreenTransform.valid);
   const double scale=std::min(double(pw)/320,double(ph)/h);
   assert(std::abs(drawnDestination.w-320*scale)<0.001);
   assert(std::abs(drawnDestination.h-h*scale)<0.001);
   assert(std::abs(drawnDestination.x-(pw-320*scale)/2)<0.001);
   assert(std::abs(drawnDestination.y-(ph-h*scale)/2)<0.001);
   for(int cy=0;cy<wh;cy+=7)for(int cx=0;cx<ww;cx+=7) {
    const double ox=double(cx)*pw/ww,oy=double(cy)*ph/wh;
    const auto d=drawnDestination;
    const bool inside=ox>=d.x && oy>=d.y && ox<double(d.x)+d.w && oy<double(d.y)+d.h;
    const auto result=win.MapMissionMouse(cx,cy,x,y);
    assert(result==(inside?R::Mapped:R::Band));
    if(inside) {
     assert(x==int(std::floor((ox-d.x)*320/d.w))-32);
     assert(y==int(std::floor((oy-d.y)*h/d.h))+4);
    }
   }
   ++fitCases;
  }
 }
 assert(fitCases==228);

 // User report: UHD desktop at 300%. Sweep into/out of both bands with no
 // click, using actual Mouse adapter. In-band position retention is explicit;
 // the first in-image sample must update immediately (no delayed recapture).
 pw=3840;ph=2160;ww=1280;wh=720;
 for(int h : {200,225}) {
  win.mScreenSize.mHeight=h;win.RenderAt(&image,true);win.FrameEnd();
  fodder.mMouse_EventLastButtonsPressed=0;
  for(int direction : {-1,1})for(int i=0;i<ww;++i) {
   const int cx=direction>0?i:ww-1-i;
   const int16 beforeX=fodder.mInputMouseX,beforeY=fodder.mInputMouseY;
   const auto result=win.MapMissionMouse(cx,wh/2,x,y);
   fodder.mMouse_EventLastPosition={cx,wh/2};fodder.HandleAlternate();
   if(result==R::Mapped) {
    assert(fodder.mInputMouseX==x && fodder.mInputMouseY==y);
   } else {
    assert(result==R::Band);
    assert(fodder.mInputMouseX==beforeX && fodder.mInputMouseY==beforeY);
   }
   assert(fodder.mMouseButtonStatus==0);
   assert(win.IsMissionCursorInBand()==(result==R::Band));
   win.RenderAt(&image,true);win.FrameEnd();
   assert(systemCursor==(result==R::Band));
  }
 }
 // Suppression is presentation-only; scope changes restore the native cursor policy.
 win.SetMissionCursorInBand(true);
 fodder.mPhase_Paused=true;assert(!win.IsMissionCursorInBand());fodder.mPhase_Paused=false;
 fodder.params.mDemoPlayback=true;assert(!win.IsMissionCursorInBand());fodder.params.mDemoPlayback=false;
 win.RenderAt(&image,false);win.FrameEnd();assert(!systemCursor);
 win.SetMissionCursorInBand(false);
 // New bands also suppress a held press on re-entry.
 pw=ww=1920;ph=wh=1080;win.mScreenSize.mHeight=200;
 win.RenderAt(&image,true);win.FrameEnd();
 fodder.mMouse_EventLastPosition={0,540};fodder.mMouse_EventLastButtonsPressed=1;
 fodder.HandleAlternate();assert(fodder.mMouseButtonStatus==0);
 fodder.mMouse_EventLastPosition={960,540};fodder.HandleAlternate();
 assert(fodder.mMouseButtonStatus==0 && fodder.mInputMouseX==128 && fodder.mInputMouseY==104);
 fodder.mMouse_EventLastButtonsPressed=0;fodder.HandleAlternate();
 fodder.mMouse_EventLastButtonsPressed=1;fodder.HandleAlternate();assert(fodder.mMouseButtonStatus==1);
 unsetenv("OPENFODDER_MISSION_SCREEN_FIT");
 win.RenderAt(&image,true);win.FrameEnd();
 assert(drawnDestination.x==0 && drawnDestination.w==640 && drawnDestination.h==400);
 ww=320;wh=200;pw=640;ph=400;
 setenv("OPENFODDER_MISSION_SCREEN_FIT","1",1);
 // Unsupported SDL state falls back as a pair: original draw and classic mouse.
 for(int mode=0;mode<5;++mode){
   target=mode==0;clip=mode==1;logical=mode==2;rendererScale=mode==3?2:1;viewportX=mode==4?1:0;
   win.RenderAt(&image,true);win.FrameEnd();assert(win.MapMissionMouse(100,100,x,y)==R::Classic);
   assert(drawnDestination.x==0 && drawnDestination.w==640 && drawnDestination.h==400);
 }
 target=clip=logical=false;rendererScale=1;viewportX=0;
 win.RenderAt(&image,true);win.FrameEnd();fodder.mWindow_Focus=false;
 assert(win.MapMissionMouse(100,100,x,y)==R::Blocked);fodder.mWindow_Focus=true;
 fodder.mPhase_Paused=true;assert(win.MapMissionMouse(100,100,x,y)==R::Classic);fodder.mPhase_Paused=false;
 fodder.mPhase_ShowMapOverview=true;assert(win.MapMissionMouse(100,100,x,y)==R::Classic);fodder.mPhase_ShowMapOverview=false;
 win.RenderAt(&image,false);win.FrameEnd();assert(win.MapMissionMouse(100,100,x,y)==R::Classic);
 win.RenderAt(&image,true);win.FrameEnd();win.RenderShrunk(&image);win.FrameEnd();assert(!win.mPresentedScreenTransform.valid);
 win.mWindowMode=false;assert(win.MapMissionMouse(100,100,x,y)==R::Classic);win.mWindowMode=true;
 fodder.params.mMouseLocked=true;assert(win.MapMissionMouse(100,100,x,y)==R::Classic);fodder.params.mMouseLocked=false;
 unsetenv("OPENFODDER_MISSION_SCREEN_TRANSFORM");win.RenderAt(&image,true);win.FrameEnd();assert(win.MapMissionMouse(100,100,x,y)==R::Classic);

 // Overview regression: full source, legacy aspect, fitted physical output;
 // it never publishes a mission input transform (overview exits on a click).
 setenv("OPENFODDER_MISSION_SCREEN_TRANSFORM","1",1);
 setenv("OPENFODDER_MISSION_SCREEN_FIT","1",1);
 cSurface overview;fodder.mSurfaceMapOverview=&overview;
 fodder.mPhase_ShowMapOverview=true;fodder.mPhase_Paused=true;
 int overviewCases=0;
 for(auto output : {cDimension{640,480},{1280,720},{1920,1080},{2560,1440},
                    {3840,2160},{1001,777}})
 for(int dpi : {100,125,150,175,200,300})for(int h : {200,225})
 for(int mapSize : {256,1024,2048}) {
  pw=output.mWidth;ph=output.mHeight;ww=pw*100/dpi;wh=ph*100/dpi;
  win.mScreenSize.mHeight=h;overview.width=overview.height=mapSize;
  win.RenderShrunk(&overview);win.FrameEnd();
  const double scale=std::min(double(pw)/320,double(ph)/h);
  assert(std::abs(drawnDestination.w-320*scale)<0.001);
  assert(std::abs(drawnDestination.h-h*scale)<0.001);
  assert(std::abs(drawnDestination.x-(pw-320*scale)/2)<0.001);
  assert(std::abs(drawnDestination.y-(ph-h*scale)/2)<0.001);
  assert(drawnSource.x==0 && drawnSource.y==0);
  assert(drawnSource.w==mapSize && drawnSource.h==mapSize);
  assert(!win.mPresentedScreenTransform.valid && !systemCursor);
  assert(win.MapMissionMouse(ww/2,wh/2,x,y)==R::Classic);
  ++overviewCases;
 }
 assert(overviewCases==216);
 pw=3840;ph=2160;ww=1280;wh=720;win.mScreenSize.mHeight=200;
 // The same source presented elsewhere, and unsupported renderer states,
 // keep their exact old rectangle. F11 remains centered by its original mode.
 for(int mode=0;mode<13;++mode) {
  fodder.mPhase_ShowMapOverview=mode!=0;fodder.mPhase_In_Progress=mode!=1;
  fodder.params.mMouseAlternative=mode!=2;fodder.params.mMouseLocked=mode==3;
  target=mode==4;clip=mode==5;logical=mode==6;rendererScale=mode==7?2:1;
  viewportX=mode==8?1:0;sizeOK=mode!=9;
  setenv("OPENFODDER_MISSION_SCREEN_FIT",mode==10?"0":"1",1);
  setenv("OPENFODDER_MISSION_SCREEN_TRANSFORM",mode==12?"0":"1",1);
  win.RenderShrunk(mode==11?&image:&overview);win.FrameEnd();
  assert(drawnDestination.x==0 && drawnDestination.y==0);
  assert(drawnDestination.w==640 && drawnDestination.h==400);
 }
 fodder.mPhase_ShowMapOverview=fodder.mPhase_In_Progress=true;
 fodder.params.mMouseAlternative=true;fodder.params.mMouseLocked=false;
 target=clip=logical=false;rendererScale=1;viewportX=0;sizeOK=true;
 setenv("OPENFODDER_MISSION_SCREEN_TRANSFORM","1",1);
 win.mWindowMode=false;win.RenderShrunk(&overview);win.FrameEnd();
 assert(drawnDestination.x==640 && drawnDestination.y==340); // 1920x1080 display double
 assert(drawnDestination.w==640 && drawnDestination.h==400);
 win.mWindowMode=true;fodder.mPhase_ShowMapOverview=fodder.mPhase_Paused=false;
 win.RenderAt(&image,true);win.FrameEnd();
 assert(win.mPresentedScreenTransform.valid);
 assert(win.MapMissionMouse(ww/2,wh/2,x,y)==R::Mapped && x==128 && y==104);
 puts("PASS: actual render/present/mouse methods; 544000 PC/Amiga coordinates; 228 mission fit + 216 overview cases up to UHD, DPI, bands, held press, fallback and lifecycle");
}
'''
    return code


def main():
    with tempfile.TemporaryDirectory(prefix='screen-transform-') as td:
        src=Path(td)/'test.cpp';exe=Path(td)/'test';src.write_text(build())
        subprocess.run(['g++','-std=c++14','-O1','-g','-pthread','-fsanitize=address,undefined',
                        '-fno-sanitize-recover=all','-I',str(ROOT/'Source'),str(src),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0'})

if __name__=='__main__':main()
