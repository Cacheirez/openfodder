"""Execute original normal posture/fire/grenade selection; keep unavailable mode 0 explicit."""
import argparse,json,re,subprocess,tempfile
from pathlib import Path
from check_aim_selection import source as aim_source,ROOT,BASE

def audit_mode_zero():
    # Every named reference is inventoried; indirect/pointer writes would also name the array.
    references=[];writes=[]
    for p in sorted((ROOT/'Source').rglob('*')):
        if not p.is_file() or p.suffix not in ('.cpp','.hpp'):continue
        for line,text in enumerate(p.read_text(encoding="utf-8").splitlines(),1):
            if 'word_3BED5' in text:
                references.append(dict(path=str(p.relative_to(ROOT)),line=line,text=text.strip()))
                if re.search(r'word_3BED5\s*\[[^]]+\]\s*=',text):writes.append(text.strip())
    assert len(writes)==5 and all(re.fullmatch(r'word_3BED5\[[0-4]\] = 2;',r) for r in writes),writes
    return dict(status='No normal CF1 setter for mode 0 found; initialization writes only 2',references=references,scope='source reachability audit, not a universal proof against arbitrary external memory/state mutation')

def source():
    prefix=aim_source().split('int main(){',1)[0]
    troop=(ROOT/'Source/Sprites/Sprite_Troop.cpp').read_text()
    old=subprocess.check_output(['git','show',BASE+':Source/Sprites/Sprite_Troop.cpp'],cwd=ROOT,text=True)
    def idle(text):return text.split('loc_194A0:;',1)[1].split('//loc_194CB',1)[0]
    assert idle(troop)==idle(old)
    prefix=prefix.replace('void Sprite_Handle_Troop_Animation(sSprite*);','void Sprite_Handle_Troop_Animation(sSprite*);\nvoid OriginalIdleModeZero(sSprite*);')
    prefix+='\nvoid cFodder::OriginalIdleModeZero(sSprite* pSprite){'+idle(troop)+'}\n'
    return prefix+r'''
int main(){
 std::cout<<"[";bool comma=false;int checks=0;
 for(int direction=0;direction<8;++direction){
  cFodder e;sSprite p;Troop troop;p.mMissionTroop=&troop;troop.mAnimationVariant=2;e.mSquads[0][0]=&p;e.requestedFace=direction*2;p.mFaceDirection=direction*2;e.word_3AA1D=2;
  auto emit=[&](const char* mode){if(comma)std::cout<<",";comma=true;std::cout<<"{\"direction\":"<<direction<<",\"mode\":\""<<mode<<"\",\"sheet\":"<<p.mSheetIndex<<",\"frame\":"<<p.mFrameIndex<<"}";};
  for(int f:{0,1,2,1}){e.mSprite_Frame_3=f;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==direction&&p.mFrameIndex==f);emit("walk");++checks;}
  p.field_43=-1;e.mSprite_Frame_3=2;e.Sprite_Handle_Troop_Direct_TowardMouse(&p);assert(p.mSheetIndex==direction&&p.mFrameIndex==1);emit("idle-retained");++checks;
  e.mSprite_FaceWeaponTarget=1;e.Sprite_Handle_Troop_Direct_TowardWeaponTarget_WithRestore(&p);assert(p.mSheetIndex==16+direction&&p.mFrameIndex==0);emit("aim");++checks;
  e.mSprite_FaceWeaponTarget=0;p.field_43=0;
  for(int f:{0,1,2,1}){e.mSprite_Frame_3=f;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==direction&&p.mFrameIndex==f);emit("walk");++checks;}
  // The grenade branch resets a stale tick, shows 0,0,1,1,2,2, then returns through native posture selection.
  p.mFiredWeaponType=1;p.mWeaponAnimTick=99;e.mSprite_Frame_3=1;
  for(int tick=0;tick<7;++tick){
   e.Sprite_Handle_Troop_Animation(&p);
   if(tick<6){assert(p.mSheetIndex==8+direction&&p.mFrameIndex==tick/2&&p.mFiredWeaponType==1);emit("grenade");}
   else{assert(p.mSheetIndex==direction&&p.mFrameIndex==1&&p.mFiredWeaponType==0&&p.mWeaponAnimTick==0&&p.mTurnTowardEnemy==0);emit("grenade-return");}
   ++checks;
  }
  for(int f:{0,1,2,1}){e.mSprite_Frame_3=f;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==direction&&p.mFrameIndex==f);emit("walk-resumed");++checks;}
  // Shooting and animation variants reuse the exact walking keys, never a new artistic clock.
  p.mFiredWeaponType=2;p.mWeaponCooldown=3;e.mSprite_Frame_3=5;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==direction&&p.mFrameIndex==2&&p.mWeaponCooldown==2);++checks;
  e.word_3AA1D=1;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==direction&&p.mFrameIndex==0&&p.mWeaponCooldown==1);++checks;
  e.Sprite_Handle_Troop_Animation(&p);assert(p.mFiredWeaponType==0);++checks;
  // Internal mode 0 is preserved/tested, not promoted to normal CF1 art or death coverage.
  e.word_3AA1D=0;
  for(int f:{0,1,2,1}){e.mSprite_Frame_2=f;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==48+direction&&p.mFrameIndex==f);++checks;}
  e.OriginalIdleModeZero(&p);assert(p.mSheetIndex==48+direction&&p.mFrameIndex==0);++checks;
  p.field_43=0;e.word_3AA1D=2;e.mSprite_Frame_3=1;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==direction&&p.mFrameIndex==1);++checks;
  p.mSheetIndex=48+direction;p.mFrameIndex=2;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==48+direction&&p.mFrameIndex==0);++checks;
  e.mSprite_Frame_3=2;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==direction&&p.mFrameIndex==2);++checks;
  // Water and a valid stationary target keep their original higher-priority branches.
  p.mInWater=1;e.mSprite_Frame_1=1;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==24+direction&&p.mFrameIndex==1);++checks;
  p.mInWater=0;e.mSprite_FaceWeaponTarget=1;e.Sprite_Handle_Troop_Animation(&p);assert(p.mSheetIndex==16+direction&&p.mFrameIndex==0);++checks;
 }
 std::cout<<"]\n";assert(checks==272);
}
'''
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--emit',type=Path);p.add_argument('--out',type=Path);p.add_argument('--audit',type=Path);a=p.parse_args();audit=audit_mode_zero()
 if a.audit:a.audit.write_text(json.dumps(audit,indent=2)+'\n')
 if a.emit:a.emit.write_text(source())
 else:
  with tempfile.TemporaryDirectory(prefix='grenade-selection-') as tmp:
   f=Path(tmp);(f/'selection.cpp').write_text(source());subprocess.run(['g++','-std=c++14','-O1','-DNDEBUG','-fsanitize=undefined','-fno-sanitize-recover=all',str(f/'selection.cpp'),'-o',str(f/'selection')],check=True)
   rows=json.loads(subprocess.check_output([str(f/'selection')],text=True));assert len(rows)==168
   if a.out:a.out.write_text(json.dumps(rows,indent=2)+'\n')
   print('PASS 272 source-selector assertions, 168 samples, mode0 audit; grenade timing 0,0,1,1,2,2 and native return')
