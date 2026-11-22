"""Exercise the actual CF1 ownership capture, including creation and late owner updates."""
from pathlib import Path
import argparse
import os
import subprocess
import tempfile
from check_final_timer_equivalence import function


def build_code(root):
    actual = function((root/'Source/WindowHD.cpp').read_text(encoding='utf-8'),
                      'openfodder::NativeAmiga8Frame cSurface::CaptureNativeAmiga8Frame(')
    fixture = function((root/'tools/modernization/test_native_player_catalog.cpp').read_text(encoding='utf-8'),
                       'static PreparedSpriteDraw fixture(')
    return r'''
#include "Utils/NativePlayerCatalog.hpp"
#include <cassert>
#include <cstring>
#include <iostream>
using namespace openfodder;
'''+fixture+r'''
constexpr int eSprite_Enemy=5,eGFX_IN_GAME=0,eGFX_IN_GAME2=1;
struct Version{bool isCannonFodder1()const{return true;}bool isAmigaTheOne()const{return true;}};
struct Actor {
 uint64_t mPresentationGeneration=0;int mSpriteType=0,mPersonType=0,mAIAggression=0;
 Actor *mOwnerSprite=nullptr,*mCurrentVehicle=nullptr;int16_t mPosX=32,mPosY=20,mHeight=12;
};
struct Row{uint16_t mLoadSegment,mLoadOffset;int16_t mColCount,mRowCount,mModX,mModY;};
struct Fodder{
 Version version;Version* mVersionCurrent=&version;std::vector<Actor> mSprites=std::vector<Actor>(2);Row row{};
 const Row* Sprite_Get_Sheet(int,int)const{return &row;}
} engine;
Fodder* g_Fodder=&engine;
struct cSurface{static NativeAmiga8Frame CaptureNativeAmiga8Frame(const PreparedSpriteDraw&,bool);};
'''+actual+r'''
int main(){
#ifdef _WIN32
 _putenv_s("OPENFODDER_PLAYER_CATALOG","1");
#else
 setenv("OPENFODDER_PLAYER_CATALOG","1",1);
#endif
 size_t cases=0;
 for(const auto& slot:CF1PlayerNativeSlots)if(slot.role==3){
  auto p=fixture(slot);p.soldier.slot=1;
  auto& owner=engine.mSprites[0];auto& shadow=engine.mSprites[1];owner={};shadow={};
  owner.mPresentationGeneration=6;shadow.mPresentationGeneration=p.soldier.generation;
  shadow.mSpriteType=22;shadow.mOwnerSprite=&owner;shadow.mCurrentVehicle=&owner;
  engine.row={uint16_t(slot.segment),uint16_t(slot.offset),int16_t(slot.columns),int16_t(slot.rows),int16_t(slot.modX),int16_t(slot.modY)};
  auto capture=[&](){return cSurface::CaptureNativeAmiga8Frame(p,false);};
  auto n=capture();assert(n.cf1 && n.role==3 && n.ownerType==0 && n.ownerSlot==0 && n.ownerGeneration==6);++cases;
  // The native shadow draw remains valid after its owner moves/changes height.
  owner.mPosX+=7;owner.mPosY-=3;owner.mHeight=slot.frame==0?0:32;
  p.nativeAmiga8=capture();ValidateCF1NativeSprite(p,384,384*272);assert(p.nativeAmiga8.role==3);++cases;
  owner.mSpriteType=4;assert(capture().role==3);++cases; // owner destroyed later in this tick
  shadow.mCurrentVehicle=nullptr;assert(!capture().cf1);++cases;shadow.mCurrentVehicle=&owner;
  shadow.mOwnerSprite=nullptr;assert(!capture().cf1);++cases;shadow.mOwnerSprite=&owner;
  owner.mPresentationGeneration=0;assert(!capture().cf1);++cases;owner.mPresentationGeneration=6;
  shadow.mPresentationGeneration++;assert(!capture().cf1);++cases;shadow.mPresentationGeneration--;
  shadow.mOwnerSprite=shadow.mCurrentVehicle=&shadow;assert(!capture().cf1);++cases;
  shadow.mOwnerSprite=shadow.mCurrentVehicle=&owner;
  shadow.mAIAggression=owner.mSpriteType=5;n=capture();assert(n.cf1 && !n.role && n.ownerType==5);++cases;
  engine.row.mLoadOffset++;assert(!capture().cf1);++cases;
 }
 std::cout<<"PASS actual shadow capture: "<<cases<<" cases; creation/update rows, late movement/destruction, pointer/generation identity, foreign owner and source rejection\n";
}
'''


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emit', type=Path)
    p.add_argument('--compiler', default='g++')
    a = p.parse_args()
    root = Path(__file__).resolve().parents[2]
    code = build_code(root)
    if a.emit:
        a.emit.write_text(code,encoding='utf-8')
    else:
        with tempfile.TemporaryDirectory(prefix='player-shadow-capture-') as td:
            source,exe = Path(td)/'test.cpp',Path(td)/'test'
            source.write_text(code,encoding='utf-8')
            subprocess.run([a.compiler,'-std=c++14','-O1','-g','-fsanitize=address,undefined',
                '-I',str(root/'Source'),'-I',str(root/'tools/modernization'),str(source),'-o',str(exe)],check=True)
            subprocess.run([str(exe)],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=1:halt_on_error=1',
                'UBSAN_OPTIONS':'halt_on_error=1:print_stacktrace=1','LSAN_OPTIONS':'exitcode=23'})
