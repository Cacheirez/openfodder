"""Original surface copy/merges vs owned layer composition, ASan/UBSan.
Actual cSurface declarations and methods; synthetic SDL storage and texture sink.
"""
import os
from pathlib import Path
import subprocess
import tempfile
from check_final_timer_equivalence import function
BASELINE='ff15219680b289abf207fdc23fc436a9f390e649'

def main():
    root=Path(__file__).resolve().parents[2]
    def original(path): return subprocess.check_output(['git','show',BASELINE+':'+path],cwd=root,text=True)
    old=original('Source/Surface.cpp');new=(root/'Source/Surface.cpp').read_text()
    # Real callers preserve layer order, fade, minimap blink, callbacks and locks.
    # Producer changes have their own original-body suite; retain scene/loop guards here.
    for path in ('Source/Fodder.cpp','Source/Recruits.cpp','Source/Window.cpp'):
        assert (root/path).read_text()==original(path),path
    for name in ('Save','Restore','palette_FadeTowardNew','draw'):
        sig=('bool' if name=='palette_FadeTowardNew' else 'void')+' cSurface::'+name+'('
        assert function(new,sig)==function(old,sig),sig
    header=(root/'Source/Surface.hpp').read_text().replace('protected:', 'public:')
    header=header.replace('class cSurface {','class cSurface {\npublic:\n void OldCopy(const cSurface*); void OldMerge(const cSurface*); void OldRGB(const cSurface*);')
    code=r'''
#include <array>
#include <string>
#include <algorithm>
#include <cassert>
#include <cstring>
#include <iostream>
#include "Utils/SurfaceLayers.hpp"
using uint8=uint8_t;using uint32=uint32_t;using int16=int16_t;
struct cDimension;struct SDL_Texture{};
struct SDL_Surface{int w,h,pitch;void* pixels;};
int updates=0,padding=0;
void SDL_UpdateTexture(SDL_Texture*,void*,void*,int){++updates;}
'''+header+r'''
cSurface::cSurface(size_t w,size_t h){
 mWidth=w;mHeight=h;mSurfaceBufferSize=w*h;mIsLoadedImage=false;mPaletteAdjusting=false;mTexture=nullptr;
 mSurfaceBuffer=new uint8[w*h];mSurfaceBufferSaved=new uint8[w*h];
 mSDLSurface=new SDL_Surface{int(w),int(h),int((w+padding)*4),new uint32[(w+padding)*h+8]};
}
cSurface::~cSurface(){delete[] mSurfaceBuffer;delete[] mSurfaceBufferSaved;delete[] static_cast<uint32*>(mSDLSurface->pixels);delete mSDLSurface;}
'''
    for a,b in [('copyFrom','OldCopy'),('mergeFrom','OldMerge'),('mergeSurfaceBuffer','OldRGB')]:
        code+=function(old,'void cSurface::'+a+'(').replace('cSurface::'+a+'(', 'cSurface::'+b+'(')
        code+=function(new,'void cSurface::'+a+'(')
    for sig in ['openfodder::IndexedLayer cSurface::CaptureIndexedLayer(','openfodder::RGBLayer cSurface::CaptureRGBLayer(','IndexedSurfaceState cSurface::CaptureIndexedState(','void cSurface::Save(','void cSurface::Restore(']:code+=function(new,sig)
    code+=r'''
size_t rgbsize(const cSurface& s){return s.mSDLSurface->pitch/4*s.mSDLSurface->h;}
void fill(cSurface& s,int seed){
 for(size_t i=0;i<s.mSurfaceBufferSize;++i){s.mSurfaceBuffer[i]=(i%3)?uint8(i*11+seed):0;s.mSurfaceBufferSaved[i]=uint8(i*3+seed+17);}
 auto out=static_cast<uint32*>(s.mSDLSurface->pixels);
 for(size_t i=0;i<rgbsize(s)+8;++i)out[i]=(i%4==0)?0:((i%4==1)?0xFF000000:0x12340000+uint32(i+seed));
 for(size_t i=0;i<255;++i){s.mPalette[i].mRed=uint8(seed+i);s.mPalette[i].mBlue=uint8(i*3);s.mPaletteNew[i].mGreen=uint8(seed+91+i);s.mPaletteSDL[i]=uint32(seed*97+i);}
 s.mPaletteAdjusting=seed%2;s.mIsLoadedImage=seed%3==0;
}
void equal(const cSurface& a,const cSurface& b){
 assert(a.mSurfaceBufferSize==b.mSurfaceBufferSize);
 assert(!memcmp(a.mSurfaceBuffer,b.mSurfaceBuffer,a.mSurfaceBufferSize));
 assert(!memcmp(a.mSurfaceBufferSaved,b.mSurfaceBufferSaved,a.mSurfaceBufferSize));
 assert(!memcmp(a.mPalette,b.mPalette,sizeof a.mPalette));assert(!memcmp(a.mPaletteNew,b.mPaletteNew,sizeof a.mPaletteNew));
 assert(!memcmp(a.mPaletteSDL,b.mPaletteSDL,sizeof a.mPaletteSDL));
 assert(!memcmp(a.mSDLSurface->pixels,b.mSDLSurface->pixels,(rgbsize(a)+8)*4));
 assert(a.mPaletteAdjusting==b.mPaletteAdjusting&&a.mIsLoadedImage==b.mIsLoadedImage);
}
int main(){size_t cases=0;
 for(size_t sw:{16,32,64,80})for(size_t sh:{16,32,49})for(size_t dw:{16,32,64,80})for(size_t dh:{16,32,49})for(int sp:{0,3})for(int dp:{0,5})for(int texture:{0,1})for(int op=0;op<3;++op){
  if(op==0&&sw*sh<dw*dh)continue; // classic opaque-copy source extent contract
  padding=sp;cSurface source(sw,sh),sourceRef(sw,sh);fill(source,7);fill(sourceRef,7);
  padding=dp;cSurface a(dw,dh),b(dw,dh);fill(a,4);fill(b,4);
  if(texture)a.mTexture=b.mTexture=reinterpret_cast<SDL_Texture*>(1);
  auto indexed=source.CaptureIndexedState();auto rgb=source.CaptureRGBLayer();equal(source,sourceRef);
  updates=0;if(op==0)a.OldCopy(&source);if(op==1)a.OldMerge(&source);if(op==2)a.OldRGB(&source);const int oldUpdates=updates;
  updates=0;if(op==0)b.copyFrom(&source);if(op==1)b.mergeFrom(&source);if(op==2)b.mergeSurfaceBuffer(&source);assert(updates==oldUpdates);equal(a,b);equal(source,sourceRef);
  // Destination snapshots are reusable seeds; no live destination is retained.
  if(op==2){auto seed=sourceRef.CaptureRGBLayer();auto first=openfodder::MakeLayerTarget(seed);openfodder::CompositeLayer(first,rgb,true);
   for(int n=0;n<3;++n){auto again=openfodder::MakeLayerTarget(seed);openfodder::CompositeLayer(again,rgb,true);assert(again.pixels==first.pixels);}
  }
  ++cases;
 }
 // Valid self merges: no alias-dependent change, saved background stays.
 for(int op=1;op<3;++op){padding=2;cSurface a(32,32),b(32,32);fill(a,3);fill(b,3);
  if(op==0){a.OldCopy(&a);b.copyFrom(&b);}if(op==1){a.OldMerge(&a);b.mergeFrom(&b);}if(op==2){a.OldRGB(&a);b.mergeSurfaceBuffer(&b);}equal(a,b);
 }
 IndexedSurfaceState retained;openfodder::RGBLayer rgb;std::weak_ptr<const std::vector<uint8>> weak;std::weak_ptr<const std::vector<uint32>> rgbweak;
 std::vector<uint8> expected;std::vector<uint32> expectedRGB;
 {padding=4;cSurface source(32,49);fill(source,8);retained=source.CaptureIndexedState();rgb=source.CaptureRGBLayer();weak=retained.layer.pixels;rgbweak=rgb.pixels;
  expected=*retained.layer.pixels;expectedRGB=*rgb.pixels;source.Save();fill(source,99);source.Restore();}
 auto copy=retained;auto moved=std::move(copy);retained={};assert(!weak.expired());
 auto target=openfodder::MakeLayerTarget(moved.layer);assert(target.pixels==expected);target.pixels.resize(100000);target.pixels[0]=99;assert(*moved.layer.pixels==expected);
 auto converted=openfodder::MakeLayerTarget(rgb);assert(converted.pixels==expectedRGB);converted.pixels[0]^=1;assert(*rgb.pixels==expectedRGB);
 assert(moved.current[1].mRed==9&&moved.next[1].mGreen==100&&moved.effective[1]==777);
 moved={};rgb={};assert(weak.expired()&&rgbweak.expired());
 // Layer order is observable; RGB word-nonzero is not index-nonzero or alpha.
 uint32 bg[]={1,2,3},a[]={0,0xFF000000,9},b[]={7,8,0};
 auto seed=openfodder::CaptureLayer(bg,3,3,1,3);auto la=openfodder::CaptureLayer(a,3,3,1,3);auto lb=openfodder::CaptureLayer(b,3,3,1,3);
 auto ab=openfodder::MakeLayerTarget(seed),ba=ab;openfodder::CompositeLayer(ab,la,true);openfodder::CompositeLayer(ab,lb,true);openfodder::CompositeLayer(ba,lb,true);openfodder::CompositeLayer(ba,la,true);
 assert(ab.pixels!=ba.pixels&&ba.pixels[1]==0xFF000000);
 std::cout<<"PASS: "<<cases<<" layer adapter cases; indexed/RGB copy, padding, palettes, source/destination independence, self merges, order and retained lifetime\n";
}
'''
    with tempfile.TemporaryDirectory() as d:
        source=Path(d)/'layers.cpp';source.write_text(code);exe=Path(d)/'layers'
        subprocess.run(['g++','-std=c++14','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-I'+str(root/'Source'),str(source),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True,env={**os.environ,'ASAN_OPTIONS':os.environ.get('ASAN_OPTIONS','detect_leaks=1')})
if __name__=='__main__':main()
