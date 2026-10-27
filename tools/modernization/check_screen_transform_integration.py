"""Actual Window render/present/inverse and alternate Mouse block, with SDL doubles.
No real GPU/input claim. GPL-3.0-or-later.
"""
from pathlib import Path
import os, subprocess, tempfile
from check_final_timer_equivalence import function

ROOT=Path(__file__).resolve().parents[2]


def build():
    window=(ROOT/'Source/Window.cpp').read_text()
    mouse=(ROOT/'Source/Mouse.cpp').read_text()
    old=subprocess.check_output(['git','show','4052235a0792861de13949aa8e4039ae23312668:Source/Mouse.cpp'],cwd=ROOT,text=True)
    signature='if (mStartParams->mMouseAlternative)'
    block=function(mouse,signature)
    assert mouse.replace(block,function(old,signature))==old, 'Other mouse effects changed'
    prefix=r'''
#include <cassert>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <cstdio>
#include <string>
#include <mutex>
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
void SDL_SetRenderDrawColor(SDL_Renderer*,int,int,int,int){}void SDL_RenderClear(SDL_Renderer*){}
SDL_DisplayID SDL_GetDisplayForWindow(SDL_Window*){return 1;}SDL_DisplayID SDL_GetPrimaryDisplay(){return 1;}
const SDL_DisplayMode* SDL_GetCurrentDisplayMode(SDL_DisplayID){static SDL_DisplayMode m;return &m;}
struct cDimension{int mWidth=320,mHeight=200;int getWidth()const{return mWidth;}int getHeight()const{return mHeight;}};
struct cSurface{SDL_Texture* GetTexture(){return nullptr;}int GetWidth(){return 352;}int GetHeight(){return 232;}};
struct cWindow{
 SDL_Window*mWindow=nullptr;SDL_Renderer*mRenderer=nullptr;bool mWindowMode=true;
 cDimension mScreenSize;std::mutex mScreenTransformMutex;
 openfodder::ScreenTransform mPendingScreenTransform,mPresentedScreenTransform;
 bool mPendingScreenClassic=false,mPresentedScreenClassic=false;
 cDimension GetWindowSize(){return {640,mScreenSize.mHeight*2};}
 void RenderAt(cSurface*,bool=false);void RenderShrunk(cSurface*);void FrameEnd();void InvalidateScreenTransform();
 openfodder::ScreenMouseResult MapMissionMouse(int,int,int16&,int16&);
};
struct Params{bool mUnitTesting=true,mMouseAlternative=true,mMouseLocked=false,mIntegerScaling=false;};
struct cFodder{
 Params params;Params*mParams=&params,*mStartParams=&params;cWindow*mWindow=nullptr;
 bool mPhase_In_Progress=true,mPhase_Paused=false,mPhase_ShowMapOverview=false,mInterruptCallback=false,mWindow_Focus=true;
 struct {int mX=0,mY=0;}mMouse_EventLastPosition;
 int16 mInputMouseX=0,mInputMouseY=0;int mMouse_EventLastButtonsPressed=0,mMouseButtonStatus=0;
 void HandleAlternate();
};cFodder fodder; cFodder*g_Fodder=&fodder;
const int16 MOUSE_POSITION_X_ADJUST=-32,MOUSE_POSITION_Y_ADJUST=4;
'''
    code=prefix
    for sig in ['void cWindow::RenderAt(', 'void cWindow::RenderShrunk(', 'void cWindow::FrameEnd(',
                'void cWindow::InvalidateScreenTransform(', 'openfodder::ScreenMouseResult cWindow::MapMissionMouse(']:
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
 // Unsupported SDL state falls back as a pair: original draw and classic mouse.
 for(int mode=0;mode<5;++mode){
   target=mode==0;clip=mode==1;logical=mode==2;rendererScale=mode==3?2:1;viewportX=mode==4?1:0;
   win.RenderAt(&image,true);win.FrameEnd();assert(win.MapMissionMouse(100,100,x,y)==R::Classic);
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
 puts("PASS: actual render/present/mouse methods; 544000 PC/Amiga coordinates; DPI, bands, held press, fallback and lifecycle");
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
