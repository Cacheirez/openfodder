"""Compare retained RGB conversion with original Surface.cpp, including effects.
Synthetic SDL XRGB surfaces; real draw, fade, palette and Save/Restore bodies.
GPU/PNG composition and complete frame scheduling are outside this test.
"""
import os
from pathlib import Path
import subprocess
import tempfile
from check_final_timer_equivalence import function
from pause_contract import canonical_pause
BASELINE = 'c6af094c49641018b6dea6dc77cbe731a7ea0218'

def main():
    root = Path(__file__).resolve().parents[2]
    old = subprocess.check_output(['git','show',BASELINE+':Source/Surface.cpp'],cwd=root,text=True)
    new = (root/'Source/Surface.cpp').read_text()
    signatures = ['void cSurface::'+n+'(' for n in ('palette_SetToBlack','palette_SetFromNew','paletteNew_SetToBlack','paletteNew_SetDimmed','paletteSet','surfaceSetToPalette','surfaceSetToPaletteNew','Save','Restore','clearBuffer')]
    # copyFrom is now compared by check_surface_layers_equivalence.py.
    signatures += ['bool cSurface::palette_FadeTowardNew(', 'inline void cSurface::paletteSDLColorSet(']
    for sig in signatures:
        assert function(old,sig) == function(new,sig),sig
    # All callers still place fade/Save/Restore at the same points.
    for p in (root/'Source').rglob('*.cpp'):
        if p.name=='Surface.cpp': continue
        s=p.read_text()
        if any(x in s for x in ('->Save(', '->Restore(', '->palette_FadeTowardNew(', '->surfaceSetToPaletteNew(')):
            reference=subprocess.check_output(['git','show',BASELINE+':'+p.relative_to(root).as_posix()],cwd=root,text=True)
            # These producer-only functions have their own original-body suite.
            # None may contain a fade/Save/Restore caller: those remain guarded.
            if p.name in ('Graphics_PC.cpp','Graphics_Amiga.cpp'):
                backend='PC' if p.name=='Graphics_PC.cpp' else 'Amiga'
                names=['Video_Draw_16','MapOverview_Render_Tiles']
                names+=['Load_And_Draw_Image','HeliIntro_BlitMaskedAlignedX','HeliIntroBlit_OpaqueAlignedX'] if backend=='PC' else ['Video_Draw_8_Alt','Video_Draw_16_Offset','Service_Draw']
                effects=('->Save(', '->Restore(', '->palette_FadeTowardNew(', '->surfaceSetToPaletteNew(')
                for name in names:
                    sig=f'void cGraphics_{backend}::{name}('
                    a,b=function(s,sig),function(reference,sig)
                    assert not any(e in a or e in b for e in effects),sig
                    s=s.replace(a,'');reference=reference.replace(b,'')
                captured=function(s,f'openfodder::IndexedProducerDraw cGraphics_{backend}::CaptureOverviewTile(')
                assert not any(e in captured for e in effects)
                s=s.replace(captured,'').replace('#include "Utils/IndexedProducer.hpp"','')
                s='\n'.join(l for l in s.splitlines() if l.strip())
                reference='\n'.join(l for l in reference.splitlines() if l.strip())
            if p.name=='Fodder.cpp': s=canonical_pause(s)
            assert s==reference,p
    header=(root/'Source/Surface.hpp').read_text()
    palette=header[header.index('class cPalette {'):header.index('class cSurface {')]
    code=r'''
#include "Utils/SurfaceDraw.hpp"
#include "Utils/SurfaceLayers.hpp"
#include <algorithm>
#include <cassert>
#include <cstring>
#include <iostream>
using uint8=uint8_t;using int8=int8_t;using int16=int16_t;using uint32=uint32_t;
constexpr size_t g_MaxColors=255;
struct SDL_PixelFormatDetails {};
struct SDL_Surface {int w,h,pitch,format=1;void* pixels;};
const SDL_PixelFormatDetails* SDL_GetPixelFormatDetails(int){static SDL_PixelFormatDetails f;return &f;}
uint32 SDL_MapRGB(const SDL_PixelFormatDetails*,void*,uint8 r,uint8 g,uint8 b){return (uint32(r)<<16)|(uint32(g)<<8)|b;}
int updates=0;
void SDL_UpdateTexture(void*,void*,void*,int){++updates;}
'''+palette+r'''
struct cSurface {
 bool mIsLoadedImage=false,mPaletteAdjusting=false;
 cPalette mPalette[255],mPaletteNew[255];uint32 mPaletteSDL[255]{};
 std::vector<uint8> input,saved;std::vector<uint32> output;
 uint8 *mSurfaceBuffer,*mSurfaceBufferSaved;size_t mSurfaceBufferSize,mWidth,mHeight;
 SDL_Surface surface;SDL_Surface* mSDLSurface;void* mTexture=nullptr;int clears=0;
 cSurface(size_t w,size_t h):input(w*h),saved(w*h),output(w*h+8,0xACACACAC),mSurfaceBuffer(input.data()),mSurfaceBufferSaved(saved.data()),mSurfaceBufferSize(w*h),mWidth(w),mHeight(h),surface{int(w),int(h),int(w*4),1,output.data()},mSDLSurface(&surface){}
 void clearSDLSurface(uint32 c=0){++clears;std::fill(output.begin(),output.begin()+mWidth*mHeight,c);}
 void LegacyDraw(int16,int16);void draw(int16,int16);
 openfodder::SurfaceDraw CaptureDraw(int16,int16)const;
 void palette_SetToBlack();void palette_SetFromNew();void paletteNew_SetToBlack();void paletteNew_SetDimmed(uint8);
 void paletteSet(cPalette*,uint32=0,uint32=255,bool=false);
 void surfaceSetToPalette();void surfaceSetToPaletteNew();void paletteSDLColorSet(size_t,cPalette*);
 bool palette_FadeTowardNew();void Save();void Restore();void clearBuffer(size_t);void copyFrom(const cSurface*);
};
'''
    code+='\n'.join(function(new,s) for s in signatures)
    code+=function(old,'void cSurface::draw(').replace('cSurface::draw(', 'cSurface::LegacyDraw(')
    code+=function(new,'openfodder::SurfaceDraw cSurface::CaptureDraw(')
    code+=function(new,'void cSurface::draw(')
    code+=r'''
void equal(const cSurface& a,const cSurface& b){
 assert(a.input==b.input&&a.saved==b.saved&&a.output==b.output);
 assert(!memcmp(a.mPalette,b.mPalette,sizeof a.mPalette));assert(!memcmp(a.mPaletteNew,b.mPaletteNew,sizeof a.mPaletteNew));
 assert(!memcmp(a.mPaletteSDL,b.mPaletteSDL,sizeof a.mPaletteSDL));assert(a.mPaletteAdjusting==b.mPaletteAdjusting);assert(a.clears==b.clears);
}
int main(){size_t cases=0;
 for(size_t w:{32,48,80,400})for(size_t h:{32,49,280})for(int sx:{0,1,16})for(int sy:{0,1,16})for(int mode=0;mode<8;++mode)for(int textured=0;textured<2;++textured){
  cSurface a(w,h),b(w,h);cPalette p[255];
  for(size_t i=0;i<255;++i){p[i].mRed=(i*7)%64;p[i].mGreen=(i*11)%64;p[i].mBlue=(i*17)%64;}
  for(size_t i=0;i<w*h;++i)a.input[i]=b.input[i]=uint8(i*31+mode);
  if(textured)a.mTexture=b.mTexture=&a;
  a.Save();b.Save();a.paletteSet(p,0,255,true);b.paletteSet(p,0,255,true);
  // Target/current/effective palette deliberately differ in several modes.
  for(auto& c:p){c.mRed=63-c.mRed;c.mGreen=63-c.mGreen;c.mBlue=63-c.mBlue;}
  a.paletteSet(p);b.paletteSet(p);
  if(mode==1){a.surfaceSetToPaletteNew();b.surfaceSetToPaletteNew();}
  if(mode==2){a.palette_SetFromNew();b.palette_SetFromNew();}
  if(mode==3){a.paletteNew_SetDimmed(127);b.paletteNew_SetDimmed(127);}
  if(mode==4){a.paletteNew_SetToBlack();b.paletteNew_SetToBlack();}
  if(mode==5){a.palette_SetToBlack();b.palette_SetToBlack();}
  if(mode==6){a.clearBuffer(17);b.clearBuffer(17);}
  if(mode==7){a.mIsLoadedImage=b.mIsLoadedImage=true;}
  for(int step=0;step<16;++step){
   if(step){assert(a.palette_FadeTowardNew()==b.palette_FadeTowardNew());}
   if(step==3){a.input[0]=b.input[0]=99;a.Restore();b.Restore();}
   const auto prior=b.input, saved=b.saved;const bool adjusting=b.mPaletteAdjusting;const int clears=b.clears;
   const auto captured=b.CaptureDraw(sx,sy);assert(prior==b.input&&saved==b.saved&&adjusting==b.mPaletteAdjusting&&clears==b.clears);
   updates=0;a.LegacyDraw(sx,sy);int legacyUpdates=updates;updates=0;b.draw(sx,sy);assert(updates==legacyUpdates);equal(a,b);
   if(!b.mIsLoadedImage){
    auto target=openfodder::RasterizeSurface(captured);assert(std::equal(target.pixels.begin(),target.pixels.end(),a.output.begin()));
    auto independent=target;independent.pixels[0]^=1;assert(independent.pixels!=target.pixels);
    for(int n=0;n<3;++n)assert(openfodder::RasterizeSurface(captured).pixels==target.pixels);
   }else assert(!captured.indices);
   ++cases;
  }
 }
 openfodder::SurfaceDraw retained;std::vector<uint32> expected;std::weak_ptr<const std::vector<uint8>> weak;
 {
  cSurface s(48,49);for(size_t i=0;i<s.input.size();++i)s.input[i]=i%256;
  cPalette p[255];for(size_t i=0;i<255;++i){p[i].mRed=i%64;p[i].mGreen=(i*3)%64;p[i].mBlue=(i*7)%64;}
  s.paletteSet(p,0,255,true);retained=s.CaptureDraw(1,1);weak=retained.indices;expected=openfodder::RasterizeSurface(retained).pixels;
  s.clearBuffer(3);s.palette_SetToBlack();s.Save();s.Restore();s.input.resize(100000);s.saved.clear();
 }
 auto copied=retained;auto moved=std::move(copied);retained={};assert(!weak.expired());
 assert(openfodder::RasterizeSurface(moved).pixels==expected);moved={};assert(weak.expired());
 std::cout<<"PASS: "<<cases<<" surface cases; effective colors, fade/Save/Restore order, owned outputs, retained lifetimes and repeated conversion\n";
}
'''
    with tempfile.TemporaryDirectory() as d:
        source=Path(d)/'test.cpp';source.write_text(code);exe=Path(d)/'test'
        subprocess.run(['g++','-std=c++14','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-I'+str(root/'Source'),str(source),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True,env={**os.environ,'ASAN_OPTIONS':os.environ.get('ASAN_OPTIONS','detect_leaks=1')})
if __name__=='__main__': main()
