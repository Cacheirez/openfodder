"""Actual pause loop and surface adapters: legacy pixels and 0/1/5 logical effects.
Synthetic input/SDL/resource loaders; no claim of GPU or commercial scene coverage.
"""
import os, subprocess, tempfile
from pathlib import Path
from check_final_timer_equivalence import function
from pause_contract import OLD, NEW, canonical_pause
BASELINE='d35e2675ffbbc79f8bf21eb961d78c06d74abd14'
def main():
 root=Path(__file__).resolve().parents[2]
 source=(root/'Source/Surface.cpp').read_text()
 fodder=(root/'Source/Fodder.cpp').read_text()
 original=subprocess.check_output(['git','show',BASELINE+':Source/Fodder.cpp'],cwd=root,text=True)
 assert canonical_pause(fodder)==original, 'Only the pure pause presentation block may change'
 header=(root/'Source/Surface.hpp').read_text().replace('protected:', 'public:')
 code=r'''
#include "Utils/PausePresentation.hpp"
#include <array>
#include <string>
#include <cassert>
#include <cstring>
#include <iostream>
using uint8=uint8_t;using int8=int8_t;using int16=int16_t;using uint32=uint32_t;
struct cDimension;struct SDL_Texture{};struct SDL_PixelFormatDetails{};
struct SDL_Surface{int w,h,pitch,format;void* pixels;};
const SDL_PixelFormatDetails* SDL_GetPixelFormatDetails(int){static SDL_PixelFormatDetails f;return &f;}
uint32 SDL_MapRGB(const SDL_PixelFormatDetails*,void*,uint8 r,uint8 g,uint8 b){return 0xFF000000u|(uint32(r)<<16)|(uint32(g)<<8)|b;}
void SDL_UpdateTexture(SDL_Texture*,void*,void*,int){}
void SDL_FillSurfaceRect(SDL_Surface* s,void*,uint32 c){for(int y=0;y<s->h;++y)std::fill_n(static_cast<uint32*>(s->pixels)+y*s->pitch/4,s->w,c);}
void SDL_Delay(int){}
int pad=0;
'''+header+r'''
cSurface::cSurface(size_t w,size_t h){
 mWidth=w;mHeight=h;mSurfaceBufferSize=w*h;mIsLoadedImage=false;mPaletteAdjusting=false;mTexture=nullptr;
 mSurfaceBuffer=new uint8[w*h];mSurfaceBufferSaved=new uint8[w*h];
 mSDLSurface=new SDL_Surface{int(w),int(h),int((w+pad)*4),1,new uint32[(w+pad)*h]};
}
cSurface::~cSurface(){delete[] mSurfaceBuffer;delete[] mSurfaceBufferSaved;delete[] static_cast<uint32*>(mSDLSurface->pixels);delete mSDLSurface;}
'''
 for sig in ['void cSurface::'+n+'(' for n in ['draw','clearSDLSurface','surfaceSetToPalette','surfaceSetToPaletteNew','palette_SetFromNew','paletteNew_SetDimmed','Save','Restore','ApplyPresentation','mergeSurfaceBuffer']]+['bool cSurface::palette_FadeTowardNew(','inline void cSurface::paletteSDLColorSet(','openfodder::SurfaceDraw cSurface::CaptureDraw(','openfodder::RGBLayer cSurface::CaptureRGBLayer(','openfodder::PresentationSurface cSurface::CapturePresentation(']:
  code+=function(source,sig)+'\n'
 code+=r'''
void fill(cSurface& s,int seed,bool loaded){
 s.mIsLoadedImage=loaded;
 for(size_t i=0;i<s.mSurfaceBufferSize;++i)s.mSurfaceBuffer[i]=uint8(i*31+seed);
 s.Save();
 for(size_t i=0;i<255;++i){s.mPalette[i].mRed=(seed+i)%64;s.mPalette[i].mGreen=(3*i+seed)%64;s.mPalette[i].mBlue=(7*i+seed)%64;}
 s.surfaceSetToPalette();s.paletteNew_SetDimmed(64);
 auto p=static_cast<uint32*>(s.mSDLSurface->pixels);
 for(size_t i=0;i<size_t(s.mSDLSurface->pitch/4*s.mSDLSurface->h);++i)p[i]=i%3?uint32(i+seed):0;
}
std::vector<uint32> logical(const cSurface& s){
 std::vector<uint32> v;
 for(size_t i=0;i<s.mSurfaceBufferSize;++i){v.push_back(s.mSurfaceBuffer[i]);v.push_back(s.mSurfaceBufferSaved[i]);}
 for(size_t i=0;i<255;++i){for(int c=0;c<3;++c){auto a=s.mPalette[i],b=s.mPaletteNew[i];v.push_back(a.getPos(c));v.push_back(b.getPos(c));}v.push_back(s.mPaletteSDL[i]);}
 v.push_back(s.mPaletteAdjusting);v.push_back(s.mIsLoadedImage);return v;
}
struct Window{
 int ends=0,cycles=0;std::vector<std::vector<uint32>> frames;
 void RenderAt(cSurface* s){frames.push_back(*s->CaptureRGBLayer().pixels);}
 void FrameEnd(){++ends;}void Cycle(){++cycles;}
};
struct Graphics {int palette=0,tiles=0,sidebar=0;void PaletteSet(){++palette;}void MapTiles_Draw(){++tiles;}void Sidebar_Copy_To_Surface(){++sidebar;}};
struct cFodder{
 cSurface *mSurface,*mSurface2;Window *mWindow;Graphics *mGraphics;
 bool mPhase_Paused=true,mPhase_Aborted=true;int events=0,prepares=0,sprites=0,repeats=1,mode=0;
 std::vector<std::vector<uint32>> trace;
 std::vector<openfodder::PausePresentation> retained;
 void Draw_Phase_Paused(){++prepares;mSurface->paletteNew_SetDimmed(64);}
 void Sprites_Draw(){++sprites;}
 void eventsProcess(){
  ++events;
  if(events==2 || events==4){ // Replace both surfaces, destroying the original resources.
   auto w=mSurface->GetWidth()+16,h=mSurface->GetHeight()+1;delete mSurface;delete mSurface2;
   mSurface=new cSurface(w,h);mSurface2=new cSurface(w,h);
   fill(*mSurface,events+11,(mode+events/2)%2);fill(*mSurface2,events+29,(mode/2+events/2)%2);
   mSurface->Restore();
  }
  if(events==6)mPhase_Paused=false;
  auto a=logical(*mSurface),b=logical(*mSurface2);a.insert(a.end(),b.begin(),b.end());
  a.insert(a.end(),{uint32(events),uint32(prepares),uint32(sprites),uint32(mPhase_Paused),uint32(mPhase_Aborted),uint32(mWindow->cycles),uint32(mWindow->ends)});trace.push_back(a);
 }
 void Phase_Paused();void LegacyPause();void ScheduledPause();
};
'''
 code+=function(original,'void cFodder::Phase_Paused(').replace('cFodder::Phase_Paused(', 'cFodder::LegacyPause(')
 actual=function(fodder,'void cFodder::Phase_Paused(')
 code+=actual
 # Exercise the actual loop with the pure presentation block scheduled 0/1/N.
 scheduled=actual.replace('cFodder::Phase_Paused(', 'cFodder::ScheduledPause(')
 start=NEW.index('        const auto presented')
 scheduled=scheduled.replace(NEW,NEW[:start]+'''        retained.push_back(scene);
        for(int n=0;n<repeats;++n) {
'''+NEW[start:]+'''
            mWindow->RenderAt(mSurface);
        }''').replace('''
        mWindow->RenderAt(mSurface);
        mWindow->FrameEnd();''','''
        mWindow->FrameEnd();''')
 code+=scheduled
 code+=r'''
struct Result{std::vector<std::vector<uint32>> trace,frames;std::vector<uint32> state;int prepares,sprites,palette,tiles,sidebar;};
Result run(int w,int h,int mode,int repeats,int variant){
 Window window;Graphics graphics;cFodder f;
 f.mSurface=new cSurface(w,h);f.mSurface2=new cSurface(w,h);f.mWindow=&window;f.mGraphics=&graphics;f.mode=mode;f.repeats=repeats;
 fill(*f.mSurface,3,mode%2);fill(*f.mSurface2,7,mode/2);
 if(variant==0)f.LegacyPause();else if(variant==1)f.Phase_Paused();else f.ScheduledPause();
 Result r{f.trace,window.frames,logical(*f.mSurface),f.prepares,f.sprites,graphics.palette,graphics.tiles,graphics.sidebar};
 auto second=logical(*f.mSurface2);r.state.insert(r.state.end(),second.begin(),second.end());r.state.push_back(f.mPhase_Aborted);
 delete f.mSurface;delete f.mSurface2;
 // Every generation survives destruction, copy and reuse; output is independent.
 for(size_t i=0;i<f.retained.size();++i){auto copy=f.retained[i];const auto expected=openfodder::RasterizePausePresentation(copy);for(int n=0;n<3;++n){auto out=openfodder::RasterizePausePresentation(copy);assert(out.background.pixels==expected.background.pixels);assert(out.text.pixels==expected.text.pixels);out.background.pixels[0]^=123;}}
 return r;
}
int main(){size_t cases=0;
 for(int w:{32,80,400})for(int h:{32,49})for(int padding:{0,3})for(int mode=0;mode<4;++mode){
  pad=padding;auto old=run(w,h,mode,1,0),actual=run(w,h,mode,1,1);
  assert(old.frames==actual.frames&&old.trace==actual.trace&&old.state==actual.state);
  for(int n:{0,1,5}){auto r=run(w,h,mode,n,2);
   assert(r.trace==old.trace&&r.state==old.state);assert(r.prepares==1&&r.sprites==1&&r.palette==1&&r.tiles==1&&r.sidebar==1);
   assert(r.frames.size()==old.frames.size()*n);
   for(size_t i=0;i<old.frames.size();++i)for(int k=0;k<n;++k)assert(r.frames[i*n+k]==old.frames[i]);
   ++cases;
  }
 }
 std::cout<<"PASS: "<<cases<<" pause schedules; actual legacy/current loops, 0/1/5 presentations, fades, resume, resource replacement/destruction, retained generations and independent outputs\n";
}
'''
 with tempfile.TemporaryDirectory(prefix='pause-equivalence-') as td:
  src=Path(td)/'test.cpp';exe=Path(td)/'test';src.write_text(code)
  subprocess.run(['g++','-std=c++14','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-I',str(root/'Source'),str(src),'-o',str(exe)],check=True)
  subprocess.run([str(exe)],check=True,env={**os.environ,'ASAN_OPTIONS':os.environ.get('ASAN_OPTIONS','detect_leaks=0')})
if __name__=='__main__':main()
