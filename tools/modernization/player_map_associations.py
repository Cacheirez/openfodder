"""Keep independent native map actors out of the protagonist body-art scope."""
from collections import Counter
import hashlib
import re
from check_final_timer_equivalence import function
from check_sprite_table_lengths import COMMENT


def check_capture_roles(code):
    capture=re.sub(r'\s+','',COMMENT.sub('',code))
    assert 'if(state.type==0&&state.personType==0)n.role=1;' in capture
    enemy='elseif(openfodder::CF1EnemyCatalogEnabled()&&(state.type==5||state.type==36||state.type==106))n.role=2;'
    assert enemy in capture and capture.count('n.role=2;')==1, 'Enemy body role must remain opt-in and type-bounded'
    assert 'state.type==27' not in capture, 'Native map corpse must never become a body-art actor'


def audit(root):
    troop=(root/'Source/Sprites/Sprite_Troop.cpp').read_text(encoding='utf-8')
    core=(root/'Source/Sprites/Sprite_Core.cpp').read_text(encoding='utf-8')
    functions={name:function(troop,signature+' cFodder::'+name+'(') for name,signature in (
        ('Sprite_Handle_Player','void'),('Sprite_Handle_Soldier_Animation','int16'),
        ('Sprite_Troop_Dies','int16'),('Sprite_Handle_Floating_Dead_Soldier','void'))}
    human=functions['Sprite_Troop_Dies'].split('if (pSprite->mSpriteType == eSprite_Enemy_Rocket')[0]
    assert 'Soldier_Died(pSprite->mMissionTroop)' in human and 'INVALID_SPRITE_PTR' in human
    assert 'return Sprite_Destroy_Wrapper(pSprite);' in human
    for name in ('Sprite_Handle_Player','Sprite_Handle_Soldier_Animation','Sprite_Troop_Dies'):
        code=functions[name]
        assert 'eSprite_Floating_Dead_Soldier' not in code and '0x9E' not in code and 'Sprite_Add(' not in code
    functions['Sprite_Destroy']=function(core,'int16 cFodder::Sprite_Destroy(')
    assert 'pSprite->mSpriteType = eSprite_Null;' in functions['Sprite_Destroy']
    floating=functions['Sprite_Handle_Floating_Dead_Soldier']
    assert 'pSprite->mSheetIndex = 0x9E;' in floating and 'mMissionTroop' not in floating
    assert not re.search(r'mFrameIndex\s*=',COMMENT.sub('',floating))
    functions['Map_Load_Sprites']=function((root/'Source/Map/MapRuntime.cpp').read_text(encoding='utf-8'),'void cFodder::Map_Load_Sprites(')
    assert 'mSprites = mMapLoaded->getSprites();' in functions['Map_Load_Sprites']
    functions['loadCF1Spt']=function((root/'Source/Map/Original.cpp').read_text(encoding='utf-8'),'void cOriginalMap::loadCF1Spt(')
    assert 'Sprite->mSpriteType = ax;' in functions['loadCF1Spt']
    functions['CaptureNativeAmiga8Frame']=function((root/'Source/WindowHD.cpp').read_text(encoding='utf-8'),'openfodder::NativeAmiga8Frame cSurface::CaptureNativeAmiga8Frame(')
    check_capture_roles(functions['CaptureNativeAmiga8Frame'])
    symbolic=[];factory_calls=Counter()
    for path in sorted((root/'Source').rglob('*.cpp')):
        code=COMMENT.sub('',path.read_text(encoding='utf-8'));name=path.relative_to(root).as_posix()
        symbolic += [name]*len(re.findall(r'\beSprite_Floating_Dead_Soldier\b',code))
        factory_calls[name]+=len(re.findall(r'\bSprite_Add\s*\(',code))
    assert symbolic==['Source/CampaignSelect.cpp'],'Floating actor producers changed; re-audit scope'
    assert +factory_calls==Counter({'Source/Map/MapData.cpp':2,'Source/Map/MapRuntime.cpp':1,'Source/Sprites/Sprite_Core.cpp':1})
    return dict(status='native map association, not a protagonist death-state body',type=27,sheet=0x9e,frames=[0,1],
        human_death='unlink mission troop then destroy current sprite as Null; never convert to type 27',
        origin='SPT map types / generic map structure factory; CampaignSelect separate preview actor',
        runtime_policy='four mandatory native-only catalog entries, canonical geometry plus full resource/raster signatures; no modern body assets accepted',
        symbolic_producer_files=symbolic,generic_map_factory_references=dict(+factory_calls),
        functions={name:hashlib.sha256(code.encode()).hexdigest() for name,code in functions.items()})
