"""Exercise actual native fade and target accessor with read-only HD RGB transfer."""
from pathlib import Path
import argparse
import os
import subprocess
import tempfile
from check_final_timer_equivalence import function


def build_code(root):
    surface = (root / 'Source/Surface.cpp').read_text(encoding='utf-8')
    header = (root / 'Source/Surface.hpp').read_text(encoding='utf-8')
    code = r'''
#include "Utils/PaletteTransfer.hpp"
#include <cassert>
#include <iostream>
using uint8=uint8_t;using int8=int8_t;
const size_t g_MaxColors=255;
'''+function(header, 'class cPalette')+r''';
class cSurface {
public:
 cPalette mPalette[255],mPaletteNew[255];bool mPaletteAdjusting=true;
 void surfaceSetToPalette(){}
 bool palette_FadeTowardNew();
'''+function(header, 'inline std::array<uint32_t,255> missionPaletteTarget()')+r'''
};
'''+function(surface, 'bool cSurface::palette_FadeTowardNew(')+r'''
std::array<uint32_t,255> colors(const cPalette* values){
 std::array<uint32_t,255> result{};
 for(size_t i=0;i<255;++i)result[i]=0xff000000u|(uint32_t(values[i].mRed*4)<<16)|
     (uint32_t(values[i].mGreen*4)<<8)|uint32_t(values[i].mBlue*4);
 return result;
}
int main(){
 size_t cases=0;
 for(bool out:{false,true}){
  cSurface s;
  for(size_t i=0;i<255;++i){auto& p=out?s.mPalette[i]:s.mPaletteNew[i];
   p.mRed=i%64;p.mGreen=(i*3)%64;p.mBlue=(i*7)%64;}
  const auto reference=colors(out?s.mPalette:s.mPaletteNew);
  unsigned steps=0;
  while(s.mPaletteAdjusting){
   const auto before=colors(s.mPalette),target=colors(s.mPaletteNew);const bool flag=s.mPaletteAdjusting;
   assert(s.missionPaletteTarget()==target);
   openfodder::MissionPaletteTransfer transfer;assert(transfer.build(reference,before));
   for(size_t i=0;i<255;++i)assert(transfer.pixel(reference[i])==before[i]);
   assert(before==colors(s.mPalette) && target==colors(s.mPaletteNew) && flag==s.mPaletteAdjusting);
   ++cases;assert(++steps<256);s.palette_FadeTowardNew();
  }
 }
 openfodder::MissionPaletteTransfer t;std::array<uint32_t,255> a{},b{};
 assert(!t.build(a,b));a[0]=16;b[0]=17;assert(!t.build(a,b));
 a[1]=16;b[0]=8;b[1]=7;assert(!t.build(a,b));
 a[1]=32;b[0]=12;b[1]=8;assert(!t.build(a,b));
 for(size_t i=0;i<255;++i){a[i]=uint32_t(i)*0x010101u;b[i]=uint32_t(i/2)*0x010101u;}
 openfodder::MissionPaletteArt art;assert(art.transfer.build(a,b));
 auto pixels=std::make_shared<const std::vector<uint32_t>>(std::vector<uint32_t>{0x80604020u,0x00123456u});
 const auto snapshot=*pixels;auto first=art.pixels(pixels);assert(art.pixels(pixels)==first && art.bytes==8 && *pixels==snapshot);
 assert(((*first)[0]>>24)==0x80 && ((*first)[1]>>24)==0);
 openfodder::MissionPaletteArt capped;capped.bytes=8u*1024u*1024u;
 bool rejected=false;try{capped.pixels(pixels);}catch(const std::length_error&){rejected=true;}assert(rejected);
 std::cout<<"PASS native palette transfer: "<<cases<<" actual fade states; native knots exact, accessor/read-only, invalid mappings, immutable shared RGB/alpha and allocation cap\n";
}
'''
    return code


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emit', type=Path)
    p.add_argument('--compiler', default='g++')
    a = p.parse_args()
    root = Path(__file__).resolve().parents[2]
    code = build_code(root)
    if a.emit:
        a.emit.write_text(code, encoding='utf-8')
    else:
        with tempfile.TemporaryDirectory(prefix='mission-palette-') as td:
            source, exe = Path(td)/'test.cpp', Path(td)/'test'
            source.write_text(code, encoding='utf-8')
            subprocess.run([a.compiler,'-std=c++14','-O1','-g','-fsanitize=address,undefined',
                            '-I',str(root/'Source'),str(source),'-o',str(exe)],check=True)
            subprocess.run([str(exe)],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=1:halt_on_error=1',
                'UBSAN_OPTIONS':'halt_on_error=1:print_stacktrace=1','LSAN_OPTIONS':'exitcode=23'})
