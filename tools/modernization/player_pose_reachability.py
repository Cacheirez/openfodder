"""Closed producer audit for the dormant CF1 squad-mode-zero sprite table.

Declared table rows are not automatically protagonist states. New mode stores or
call paths must invalidate this proof before changing the required-art boundary.
"""
from collections import Counter
import hashlib
import re
from check_final_timer_equivalence import function
from check_sprite_table_lengths import COMMENT

EXPECTED_MODE_REFS=Counter({
    ('Source/Fodder.hpp','uint16word_3BED5[5];'):1,
    **{('Source/Fodder.cpp',f'word_3BED5[{i}]=2;'):1 for i in range(5)},
    ('Source/CampaignSelect.cpp','word_3AA1D=word_3BED5[0];'):1,
    ('Source/Squad.cpp','if(word_3BED5[Data0]){'):1,
    ('Source/Sprites/Sprite_Troop.cpp','word_3AA1D=word_3BED5[pSprite->field_32];'):1,
    ('Source/Sprites/Sprite_Troop.cpp','Data0=word_3BED5[pSprite->field_32];'):1,
})
EXPECTED_SCRATCH_STORES=Counter({
    ('Source/Fodder.cpp','word_3AA1D=0;'):1,
    ('Source/CampaignSelect.cpp','word_3AA1D=word_3BED5[0];'):1,
    ('Source/Sprites/Sprite_Troop.cpp','word_3AA1D=word_3BED5[pSprite->field_32];'):1,
})


def check_mode_references(mode_refs,scratch_stores):
    assert Counter(mode_refs)==EXPECTED_MODE_REFS,'Squad-mode references changed; re-audit reachability'
    assert Counter(scratch_stores)==EXPECTED_SCRATCH_STORES,'Scratch mode stores changed; re-audit reachability'


def audit(root):
    refs=[];stores=[];evidence=[]
    for path in sorted((root/'Source').rglob('*')):
        if path.suffix not in ('.cpp','.hpp'):continue
        source=path.read_text(encoding='utf-8')
        clean=COMMENT.sub(lambda m:'\n'*m[0].count('\n'),source)
        for line_number,line in enumerate(clean.splitlines(),1):
            compact=re.sub(r'\s+','',line);file=path.relative_to(root).as_posix()
            if re.search(r'\bword_3BED5\b',line):
                refs.append((file,compact));evidence.append(dict(file=file,line=line_number,code=compact))
            if re.search(r'\bword_3AA1D\s*=(?!=)',line):stores.append((file,compact))
    check_mode_references(refs,stores)
    troop=(root/'Source/Sprites/Sprite_Troop.cpp').read_text(encoding='utf-8')
    player=function(troop,'void cFodder::Sprite_Handle_Player(')
    marker='word_3AA1D = word_3BED5[pSprite->field_32];';prefix=player[:player.index(marker)]
    assert 'goto ' not in COMMENT.sub('',prefix),'Player entry can bypass the mode read'
    normal=r'\bSprite_Handle_Troop_(?:Animation|Direct_\w+)\('
    assert not re.search(normal,prefix),'Normal selector called before player mode read'
    checked={}
    for name,kind in (('Sprite_Handle_Soldier_Animation','int16'),('Sprite_Handle_Player_MissionOver','int16')):
        code=function(troop,kind+' cFodder::'+name+'(')
        assert not re.search(normal,code) and not re.search(r'Data28[^;]*0x18',code)
        checked[name]=hashlib.sha256(code.encode()).hexdigest()
    vehicle=(root/'Source/Sprites/Sprite_Vehicle.cpp').read_text(encoding='utf-8')
    enter=function(vehicle,'void cFodder::Sprite_Handle_Player_Enter_Vehicle(')
    assert not re.search(normal,enter)
    animation=function(troop,'void cFodder::Sprite_Handle_Troop_Animation(')
    compact=re.sub(r'\s+','',COMMENT.sub('',animation))
    assert 'elseif(!word_3AA1D){pSprite->mSheetIndex=*(Data28+Data8+0x18);pSprite->mFrameIndex=mSprite_Frame_2;}' in compact
    core=(root/'Source/Sprites/Sprite_Core.cpp').read_text(encoding='utf-8')
    fall=function(core,'void cFodder::Sprite_Update_Direction_Anim(')
    assert 'Data28+=((0x80+Data8)/2);' in re.sub(r'\s+','',fall) and 'pSprite->mFrameIndex = 0;' in fall
    fodder=(root/'Source/Fodder.cpp').read_text(encoding='utf-8')
    assert 'Phase_EngineReset();Phase_SquadPrepare();' in re.sub(r'\s+','',COMMENT.sub('',fodder))
    for name,code in [('Sprite_Handle_Player',player),('Sprite_Handle_Troop_Animation',animation),
                      ('Sprite_Handle_Player_Enter_Vehicle',enter),('Sprite_Update_Direction_Anim',fall)]:
        checked[name]=hashlib.sha256(code.encode()).hexdigest()
    return dict(status='declared mode-zero branch not produced by current CF1 human controls',
        scope='normal current CF1 campaign/control paths; not arbitrary debug/memory mutation or future features',
        mode_array='word_3BED5[5]',initialized_values=[2]*5,mode_references=evidence,
        scratch_stores=[dict(file=file,code=code) for file,code in sorted(stores)],
        functions=checked,latent_sheets=list(range(0x30,0x38)),
        actual_fall_sheets=list(range(0xb0,0xb8)),actual_fall_frame=0,
        conclusion='Keep 24 declared rows per format as a source-only audit; do not invent protagonist artwork or count them as required runtime poses')
