"""Execute original troop selectors, including frame retention, without changing gameplay.
Extracts actual current bodies and requires equality to the accepted classic base.
"""
import argparse,json,re,subprocess,tempfile
from pathlib import Path
from check_final_timer_equivalence import function
ROOT=Path(__file__).resolve().parents[2]
BASE='5e6a4f3834a0a491468ea659f45f8e5f4fb785a8'

def source():
    path='Source/Sprites/Sprite_Troop.cpp';text=(ROOT/path).read_text();old=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT,text=True)
    signatures=['void cFodder::Sprite_Handle_Troop_Animation(', 'void cFodder::Sprite_Handle_Troop_Direct_TowardMouse(', 'void cFodder::Sprite_Handle_Troop_Direct_TowardWeaponTarget_WithRestore(']
    bodies=[]
    for sig in signatures:
        body=function(text,sig);assert body==function(old,sig), 'selector differs from classic; review required';bodies.append(body)
    table=(ROOT/'Source/Sprites.cpp').read_text();arrays=[]
    for who in ('Human','Enemy'):
        arrays.append(re.search(r'int16 mSprite_Animation'+who+r'Ptrs\[\]\s*=\s*\{[\s\S]*?\};',table).group())
    harness=r'''
#ifdef NDEBUG
#undef NDEBUG
#endif
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using int16=int16_t;
constexpr int eSprite_PersonType_Human=0,eTerrainFeature_Water=1;
struct sMapTarget{int mX=-1;};struct Troop{int mAnimationVariant=0;};
struct sSprite{int mPersonType=0,mFollowTarget=0,mPosX=0,mPosY=0,mTargetX=0,mTargetY=0,mSheetIndex=0,mFrameIndex=0,mTurnTowardEnemy=0,field_43=0,mInWater=0,mFaceDirection=0,field_32=0,mNextWalkTargetIndex=0,mTerrainType=0,mFiredWeaponType=0,mWeaponCooldown=2,mWeaponAnimTick=0,mDirection=123,mWeaponTargetX=0,mWeaponTargetY=0;Troop* mMissionTroop=nullptr;};
#define INVALID_SPRITE_PTR reinterpret_cast<sSprite*>(-1)
'''+ '\n'.join(arrays)+r'''
const int16* mSprite_AnimationPtrs[]={mSprite_AnimationHumanPtrs,mSprite_AnimationEnemyPtrs};
struct cFodder{
int word_3ABB1=0,word_3AA1D=1,mSprite_Bumped_Into_SquadMember=0,mDirectionMod=0,mSprite_FaceWeaponTarget=0,word_3B2F3=1,mStoredSpriteFrame=0,mSprite_Frame_3=0,mSprite_Frame_2=0,mSprite_Frame_1=0,mTmp_FrameNumber=0,mMouseX=0,mMouseY=0,mCameraX=0,mCameraY=0,requestedFace=0;
sMapTarget target;sMapTarget* mSquad_WalkTargets[1]={&target};sSprite* mSquads[1][1]={{nullptr}};
void Sprite_Direction_Between_Points(sSprite*,int,int){} // Geometry is outside selector scope.
void Sprite_Set_Direction_To_Next(sSprite*p){p->mFaceDirection=requestedFace;}
void Sprite_Handle_Troop_Animation(sSprite*);
void Sprite_Handle_Troop_Direct_TowardMouse(sSprite*);
void Sprite_Handle_Troop_Direct_TowardWeaponTarget_WithRestore(sSprite*);
};
'''+ '\n'.join(bodies)+r'''
int main(){
std::cout<<"[";bool comma=false;int checks=0;
for(int direction=0;direction<8;++direction){
 cFodder e;sSprite p;e.mSquads[0][0]=&p;e.requestedFace=direction*2;p.mFaceDirection=direction*2;
 auto emit=[&](const char* mode){if(comma)std::cout<<",";comma=true;std::cout<<"{\"direction\":"<<direction<<",\"mode\":\""<<mode<<"\",\"sheet\":"<<p.mSheetIndex<<",\"frame\":"<<p.mFrameIndex<<"}";};
 for(int f:{0,1,2,1}){e.mSprite_Frame_1=f;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==direction&&p.mFrameIndex==f);emit("walk");++checks;}
 p.field_43=-1;e.mSprite_Frame_1=2;e.Sprite_Handle_Troop_Direct_TowardMouse(&p);assert(p.mSheetIndex==direction&&p.mFrameIndex==1);emit("idle-retained");++checks;
 e.mSprite_FaceWeaponTarget=1;e.Sprite_Handle_Troop_Direct_TowardWeaponTarget_WithRestore(&p);assert(p.mSheetIndex==16+direction&&p.mFrameIndex==0);emit("aim-prone");++checks;
 // Retained field_43 must not restore a walking frame into a single-frame aiming sheet.
 p.mFrameIndex=2;e.Sprite_Handle_Troop_Direct_TowardMouse(&p);assert(p.mSheetIndex==16+direction&&p.mFrameIndex==0);++checks;
 // A water target follows the swim route, not the prone branch.
 p.mTerrainType=eTerrainFeature_Water;p.mInWater=1;e.mSprite_Frame_1=1;e.mSprite_Frame_2=1;e.mSprite_Bumped_Into_SquadMember=0;p.field_43=0;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==24+direction&&p.mFrameIndex==1);++checks;
 p.mInWater=0;p.mTerrainType=0;p.field_43=0;e.mSprite_FaceWeaponTarget=0;
 for(int f:{0,1,2,1}){e.mSprite_Frame_1=f;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==direction&&p.mFrameIndex==f);emit("walk-resumed");++checks;}
 // Facing, not movement direction, selects the body; direction modulo is original.
 e.mDirectionMod=2;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==(direction+1)%8&&p.mDirection==123);++checks;
 // Moving leader must not use the stationary target branch.
 p.mFaceDirection=direction*2;e.mDirectionMod=0;e.mSprite_FaceWeaponTarget=1;p.mPosX=1;p.mTargetX=0;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==direction);++checks;
 // The same restriction applies to followers, with leader position and word_3B2F3.
 sSprite leader;e.mSquads[0][0]=&leader;leader.mPosX=1;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==direction);++checks;
 leader.mPosX=0;e.word_3B2F3=0;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==direction);++checks;
 e.word_3B2F3=1;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==16+direction&&p.mFrameIndex==0);++checks;
 // Other squad posture modes remain original, and are not silently bound as low aim.
 e.mSquads[0][0]=&p;p.mPosX=0;e.word_3AA1D=2;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==16+direction&&p.mFrameIndex==0);++checks;
 e.mSprite_FaceWeaponTarget=0;e.word_3AA1D=0;p.field_43=0;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==48+direction);++checks;
}
std::cout<<"]\n";assert(checks==152);
}
'''
    return harness

def check(compiler,out):
    with tempfile.TemporaryDirectory(prefix='aim-selection-') as tmp:
        folder=Path(tmp);cpp=folder/'selection.cpp';exe=folder/'selection';cpp.write_text(source())
        subprocess.run([compiler,'-std=c++14','-O1',str(cpp),'-o',str(exe)],check=True)
        rows=json.loads(subprocess.check_output([str(exe)],text=True));assert len(rows)==80
        if out:out.write_text(json.dumps(rows,indent=2)+'\n')
        print('PASS actual classic selectors: 152 assertions, eight directions, 80 transition samples; geometry stubbed, simulation untouched')
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--compiler',default='g++');p.add_argument('--out',type=Path);p.add_argument('--emit',type=Path);a=p.parse_args();
 if a.emit:a.emit.write_text(source())
 else:check(a.compiler,a.out)
