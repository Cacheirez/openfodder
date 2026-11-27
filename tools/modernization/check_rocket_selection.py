"""Check native CF1 rocket body selection, including caller frame restoration.

No artwork, projectiles or gameplay changes. Geometry remains stubbed as in the
aim fixture; seven selector calls are not seven game ticks or display frames.
GPL-3.0-or-later.
"""
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

from check_aim_selection import BASE, ROOT, source as aim_source
from check_final_timer_equivalence import function
from check_sprite_table_lengths import ARRAY, COMMENT, check


def classic(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT, text=True)


def metadata():
    """Read only the rocket group and its actual CF1 arrays, not a new census."""
    path = 'Source/Sprites.cpp'
    text = (ROOT / path).read_text()
    pattern = r'int16 mSprite_AnimationHumanPtrs\[\]\s*=\s*\{([\s\S]*?)\};'
    table = re.search(pattern, text).group(1)
    assert table == re.search(pattern, classic(path)).group(1)
    sheets = [int(x.strip(), 0) for x in COMMENT.sub('', table).split(',') if x.strip()][0x38:0x40]
    assert sheets == list(range(0x39, 0x41))
    result = {}
    for platform in ('PC', 'Amiga'):
        path = f'Source/{platform}/SpriteData_{platform}.hpp'
        text = (ROOT / path).read_text()
        old = classic(path)
        counts, tables = check(text)
        old_counts, old_tables = check(old)
        table_name = f'mSpriteSheetTypes_InGame_{platform}'
        arrays = {name: COMMENT.sub('', body).split() for name, _, body in ARRAY.findall(text)}
        old_arrays = {name: COMMENT.sub('', body).split() for name, _, body in ARRAY.findall(old)}
        rows = []
        for direction, sheet in enumerate(sheets):
            name = tables[table_name][sheet]
            assert name == old_tables[table_name][sheet]
            assert arrays[name] == old_arrays[name] and counts[name] == old_counts[name]
            rows.append(dict(direction=direction, sheet=sheet, array=name,
                             declared_frames=counts[name], tested_body_frames=[0, 1, 2]))
        assert [r['declared_frames'] for r in rows] == [3, 3, 3, 3, 3, 4, 3, 3]
        result[platform] = rows
    # Audit creation separately: no claim of executing projectile allocation.
    path = 'Source/Sprites/Sprite_Projectiles.cpp'
    sig = 'int16 cFodder::Sprite_Create_Rocket('
    body = function((ROOT / path).read_text(), sig)
    assert body == function(classic(path), sig)
    assert 'pSprite->mWeaponAnimTick = 1;' in body
    assert 'pSprite->mTurnTowardEnemy = -1;' in body
    assert 'pSprite->mFiredWeaponType = 3;' in body
    return result


def source():
    # These are the three actual current functions, required equal to classic.
    prefix = aim_source().split('int main(){', 1)[0]
    return prefix + r'''
int main(){
 int checks=0,samples=0;bool comma=false;
 auto expect=[&](bool value){assert(value);++checks;};
 std::cout<<"{\"samples\":[";
 auto emit=[&](int direction,const char* route,int start,int call,const sSprite& p){
  if(comma)std::cout<<",";comma=true;++samples;
  std::cout<<"{\"direction\":"<<direction<<",\"route\":\""<<route
   <<"\",\"initial_frame\":"<<start<<",\"call\":"<<call
   <<",\"sheet\":"<<p.mSheetIndex<<",\"frame\":"<<p.mFrameIndex
   <<",\"weapon_tick\":"<<p.mWeaponAnimTick<<",\"weapon_type\":"<<p.mFiredWeaponType<<"}";
 };
 for(int direction=0;direction<8;++direction){
  // Direct selection resets to zero. Both retained callers can restore 1/2.
  for(int route=0;route<3;++route)for(int start=0;start<3;++start){
   cFodder e;sSprite p;Troop troop;troop.mAnimationVariant=2;p.mMissionTroop=&troop;
   e.word_3AA1D=2;e.mSquads[0][0]=&p;e.requestedFace=direction*2;
   p.mFaceDirection=direction*2;p.mSheetIndex=direction;p.mFrameIndex=start;
   p.mFiredWeaponType=3;p.mWeaponAnimTick=1;p.mTurnTowardEnemy=-1;
   p.field_43=route? -1:0;e.mSprite_Frame_3=2;
   const char* name=route==0?"direct":route==1?"mouse-retained":"target-retained";
   for(int call=0;call<8;++call){
    if(route==0)e.Sprite_Handle_Troop_Animation(&p);
    else if(route==1)e.Sprite_Handle_Troop_Direct_TowardMouse(&p);
    else e.Sprite_Handle_Troop_Direct_TowardWeaponTarget_WithRestore(&p);
    if(call<7){
     expect(p.mSheetIndex==0x39+direction);
     expect(p.mFrameIndex==(route?start:0));
     expect(p.mWeaponAnimTick==call&&p.mFiredWeaponType==3&&p.mTurnTowardEnemy==-1);
    }else{
     expect(p.mSheetIndex==direction&&p.mFrameIndex==(route?start:2));
     expect(p.mWeaponAnimTick==0&&p.mFiredWeaponType==0&&p.mTurnTowardEnemy==0);
    }
    expect(p.mDirection==123); // Facing is independent of movement.
    emit(direction,name,start,call,p);
   }
   // Resume the native walk after releasing retained posture.
   p.field_43=0;
   for(int f:{0,1,2,1}){
    e.mSprite_Frame_3=f;e.Sprite_Handle_Troop_Animation(&p);
    expect(p.mSheetIndex==direction&&p.mFrameIndex==f);
   }
   e.mSprite_FaceWeaponTarget=1;e.Sprite_Handle_Troop_Animation(&p);
   expect(p.mSheetIndex==0x10+direction&&p.mFrameIndex==0);
  }
  // Calls without field_43 do not restore the incoming walk frame.
  for(int route=1;route<3;++route){
   cFodder e;sSprite p;e.word_3AA1D=2;e.mSquads[0][0]=&p;e.requestedFace=direction*2;
   p.mFaceDirection=direction*2;p.mSheetIndex=direction;p.mFrameIndex=2;p.mFiredWeaponType=3;
   if(route==1)e.Sprite_Handle_Troop_Direct_TowardMouse(&p);
   else e.Sprite_Handle_Troop_Direct_TowardWeaponTarget_WithRestore(&p);
   expect(p.mSheetIndex==0x39+direction&&p.mFrameIndex==0&&p.mWeaponAnimTick==0);
  }
  // A changed facing restarts the native hold on the new sheet.
  cFodder e;sSprite p;e.word_3AA1D=2;e.mSquads[0][0]=&p;p.mFaceDirection=direction*2;
  p.mSheetIndex=0x39+direction;p.mFrameIndex=0;p.mFiredWeaponType=3;p.mWeaponAnimTick=5;
  e.mDirectionMod=2;e.Sprite_Handle_Troop_Animation(&p);
  expect(p.mSheetIndex==0x39+(direction+1)%8&&p.mWeaponAnimTick==0&&p.mFrameIndex==0);
  e.mDirectionMod=0;
  // Stationary weapon-target aim precedes rocket and does not advance its tick.
  e.mSprite_FaceWeaponTarget=1;p.mWeaponAnimTick=4;
  e.Sprite_Handle_Troop_Animation(&p);
  expect(p.mSheetIndex==0x10+(direction+1)%8&&p.mFrameIndex==0);
  expect(p.mWeaponAnimTick==4&&p.mFiredWeaponType==3);
  e.mSprite_FaceWeaponTarget=0;e.Sprite_Handle_Troop_Animation(&p);
  expect(p.mSheetIndex==0x39+(direction+1)%8&&p.mWeaponAnimTick==0);
  // Rocket selection precedes swimming; water determines the return posture.
  p.mInWater=1;e.mSprite_Frame_1=1;
  for(int call=1;call<=7;++call){
   e.Sprite_Handle_Troop_Animation(&p);
   if(call<7)expect(p.mSheetIndex==0x39+(direction+1)%8&&p.mFrameIndex==0);
   else expect(p.mSheetIndex==0x18+(direction+1)%8&&p.mFrameIndex==1&&p.mFiredWeaponType==0);
  }
 }
 // Two actors share a selector context, but not tick, direction or retained frame.
 cFodder e;sSprite a,b;e.word_3AA1D=2;
 a.mSheetIndex=0x39;a.mFrameIndex=2;a.mWeaponAnimTick=1;a.mFiredWeaponType=3;a.field_43=-1;
 b.mSheetIndex=0x40;b.mFrameIndex=1;b.mWeaponAnimTick=4;b.mFiredWeaponType=3;b.field_43=-1;
 for(int call=0;call<3;++call){
  e.requestedFace=0;e.mSquads[0][0]=&a;e.Sprite_Handle_Troop_Direct_TowardWeaponTarget_WithRestore(&a);
  expect(a.mSheetIndex==0x39&&a.mFrameIndex==2&&a.mWeaponAnimTick==call+2);
  e.requestedFace=14;e.mSquads[0][0]=&b;e.Sprite_Handle_Troop_Direct_TowardMouse(&b);
  if(call<2)expect(b.mSheetIndex==0x40&&b.mFrameIndex==1&&b.mWeaponAnimTick==call+5);
  else expect(b.mSheetIndex==7&&b.mFrameIndex==1&&b.mFiredWeaponType==0);
 }
 expect(samples==576);
 std::cout<<"],\"assertions\":"<<checks<<",\"sample_count\":"<<samples<<"}\n";
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', type=Path)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--compiler', default='g++')
    args = parser.parse_args()
    tables = metadata()
    cpp = source()
    if args.emit:
        args.emit.write_text(cpp)
        return
    with tempfile.TemporaryDirectory(prefix='rocket-selection-') as tmp:
        folder = Path(tmp)
        (folder / 'selection.cpp').write_text(cpp)
        subprocess.run([args.compiler, '-std=c++14', '-O1', '-DNDEBUG', '-fsanitize=undefined',
                        '-fno-sanitize-recover=all', str(folder / 'selection.cpp'),
                        '-o', str(folder / 'selection')], check=True)
        result = json.loads(subprocess.check_output([str(folder / 'selection')], text=True))
    # Public metadata/state only; no resource or palette bytes.
    result['classic_base'] = BASE
    result['tables'] = tables
    result['limits'] = ['geometry stubbed; no full player handler or projectile allocation execution',
                        'selector invocation counts are not game ticks or display frames',
                        'frame 3 not selected in tested ordinary entry/retention paths; not a global reachability proof',
                        'no HD publication, new art, campaign, GPU/CD32 or user acceptance claim']
    if args.out:
        args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(f"PASS {result['assertions']} source-selector assertions, {result['sample_count']} samples; "
          'rocket frame 0 directly, frames 0/1/2 through retained callers; UBSan')


if __name__ == '__main__':
    main()
