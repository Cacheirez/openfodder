"""Execute actual Clear/scene-reset/capture adapters on controlled input values.
No replacement simulation; SDL and sheet lookup are fixtures. GPL-3.0-or-later.
"""
import os
from pathlib import Path
import subprocess
import tempfile
from check_final_timer_equivalence import function


def main():
    root = Path(__file__).resolve().parents[2]
    sprite = (root/'Source/Sprites.cpp').read_text(encoding='utf-8')
    core = (root/'Source/Sprites/Sprite_Core.cpp').read_text(encoding='utf-8')
    code = r'''
#include <vector>
#include <cassert>
#include <cstdlib>
#include <string>
#include <iostream>
#include "Types.hpp"
struct cPosition { cPosition(int,int){} };
#include "Sprites.hpp"
#include "SpriteSheet.hpp"
#include "Utils/ResolvedSpriteResource.hpp"
struct Params { size_t mSpritesMax=3; };
struct cFodder {
 Params params;Params* mParams=&params;
 std::vector<sSprite> mSprites; sSprite mSprite_Spare;int mSprite_SpareUsed=0;
 bool mPhase_In_Progress=true,mPhase_Paused=false,mPhase_ShowMapOverview=false;
 uint64_t mPresentationScene=0;
 int16 mMission_EngineTicks=17;int32 mCameraX=123456,mCameraY=234567;
 sSpriteSheet sheet{};
 void Squad_Set_Squad_Leader(){}
 const sSpriteSheet* Sprite_Get_Sheet(int16,int16){return &sheet;}
 void Sprite_Clear_All();
 void CaptureSoldierSemantic(sSprite*,int16,int16,const openfodder::SpriteDrawInput&,openfodder::PreparedSpriteDraw&);
};
'''
    for text, signature in [(sprite,'void sSprite::Clear()'), (core,'void cFodder::Sprite_Clear_All()'), (core,'void cFodder::CaptureSoldierSemantic(')]:
        code += function(text, signature, preserve_audit=True)+'\n'
    code += r'''
int main(){
 cFodder e;e.Sprite_Clear_All();
 auto& s=e.mSprites[0];s.mPosX=70;s.mPosY=80;s.mPosXFrac=123;s.mPosYFrac=-456;
 s.mHeightFrac=789;s.mDirection=42;s.mAnimState=2;e.sheet.mLoadSegment=3;
 openfodder::SpriteDrawInput input;input.spriteX=70;input.spriteY=80;input.modX=-2;input.modY=3;
 input.source=reinterpret_cast<const uint8_t*>(1); // Must never escape into snapshot.
 auto capture=[&](sSprite* p){openfodder::PreparedSpriteDraw out;out.draw.visible=true;
  e.CaptureSoldierSemantic(p,7,4,input,out);return out.soldier;};
 auto first=capture(&s);assert(first.valid&&first.slot==0&&first.scene==e.mPresentationScene);
 assert(first.generation==s.mPresentationGeneration&&first.tick==17&&first.cameraX==123456);
 assert(first.xFraction==123&&first.yFraction==-456&&first.heightFraction==789);
 assert(first.geometry.modX==-2&&first.geometry.modY==3&&!first.geometry.source);
 assert(first.segment==3&&first.sheet==7&&first.frame==4&&first.animation==2&&first.direction==42);
 auto repeated=capture(&s);assert(first.generation==repeated.generation&&first.scene==repeated.scene);
 e.mSprites[1].mPosX=80;assert(!capture(&e.mSprites[1]).valid);
 e.mPhase_Paused=true;assert(!capture(&s).valid);e.mPhase_Paused=false;
 e.mPhase_ShowMapOverview=true;assert(!capture(&s).valid);e.mPhase_ShowMapOverview=false;
 e.mPhase_In_Progress=false;assert(!capture(&s).valid);e.mPhase_In_Progress=true;
 s.mInVehicle=-1;assert(!capture(&s).valid);s.mInVehicle=0;
 s.mPendingDestroy=1;assert(!capture(&s).valid);s.mPendingDestroy=0;
 s.mSpriteType=eSprite_Explosion;assert(!capture(&s).valid);s.mSpriteType=eSprite_Player;
 s.Clear();s.mPosX=70;assert(capture(&s).generation!=first.generation);
 auto authored=e.mSprites;e.Sprite_Clear_All();e.mSprites=authored;
 assert(capture(&e.mSprites[0]).scene!=first.scene); // Reload same authored slots.
 assert(first.geometry.spriteX==70&&first.xFraction==123); // Old value retained.
 std::cout<<"PASS actual soldier capture: metadata, guards, same-slot Clear and scene reload\n";
}
'''
    with tempfile.TemporaryDirectory(prefix='soldier-semantic-') as td:
        source=Path(td)/'test.cpp';exe=Path(td)/'test';source.write_text(code)
        subprocess.run(['g++','-std=c++14','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all','-I',str(root/'Source'),str(source),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],env={**os.environ,'OPENFODDER_CAPTURE_SOLDIER':'1','ASAN_OPTIONS':os.environ.get('ASAN_OPTIONS','detect_leaks=0')},check=True)

if __name__=='__main__':
    main()
