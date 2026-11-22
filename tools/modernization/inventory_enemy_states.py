"""Source inventory of CF1 enemy infantry; metadata, never retail pixels.

Enemy selectors share scratch mode state with the player, not its reachability
proof. Retain mode-zero rows and the follower's DC idle explicitly. Runtime
signatures, art bindings and visual acceptance are separate later gates.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from check_sprite_table_lengths import ARRAY, COMMENT, check
from check_final_timer_equivalence import function

ROOT = Path(__file__).resolve().parents[2]
GROUPS = ('walk', 'damage_override', 'damage_ballistic', 'mode_zero',
          'swim', 'grenade', 'aim_low', 'rocket', 'fall')
LOOKUP = [*range(0x42, 0x4a), *range(0x62, 0x6a),
          0x6a, 0x6b, 0x64, 0x6d, 0x6e, 0x6f, 0x70, 0x71,
          *range(0x72, 0x7a), *range(0x5a, 0x62), *range(0x4a, 0x52),
          *range(0x52, 0x5a), *range(0xa8, 0xb0), *range(0xb8, 0xc0)]
ROUTES = {
    'Sprite_Handle_Enemy': ('Sprite_Troop.cpp', 'void'),
    'Sprite_Handle_Enemy_Rocket': ('Sprite_Projectiles.cpp', 'void'),
    'Sprite_Handle_Enemy_Leader': ('Sprite_Troop.cpp', 'void'),
    'Sprite_Handle_Soldier_Animation': ('Sprite_Troop.cpp', 'int16'),
    'Sprite_Handle_Troop_Animation': ('Sprite_Troop.cpp', 'void'),
    'Sprite_Handle_Troop_Direct_TowardWeaponTarget_WithRestore': ('Sprite_Troop.cpp', 'void'),
    'Sprite_Create_Enemy': ('Sprite_Troop.cpp', 'int16'),
    'Sprite_Handle_Player_Shadow': ('Sprite_Troop.cpp', 'void'),
    'Sprite_Create_Player_Shadow': ('Sprite_Troop.cpp', 'void'),
    'Sprite_Update_Direction_Anim': ('Sprite_Core.cpp', 'void'),
    'Sprite_Handle_Hostage': ('Sprite_Civilian.cpp', 'void'),
    'Sprite_Handle_Hostage_Movement': ('Sprite_Civilian.cpp', 'void'),
    'Sprite_Handle_Hostage_FrameUpdate': ('Sprite_Civilian.cpp', 'void'),
    'Sprite_Handle_Hostage_FrameUpdate2': ('Sprite_Civilian.cpp', 'void'),
    'Sprite_Hostage_Update_IdleFrame': ('Sprite_Civilian.cpp', 'void'),
    'Sprite_Handle_Flashing_Light': ('Sprite_Effects.cpp', 'void'),
}


def table(text):
    body = re.search(r'int16 mSprite_AnimationEnemyPtrs\[\]\s*=\s*\{([\s\S]*?)\};', text)[1]
    values = [int(v.strip(), 0) for v in COMMENT.sub('', body).split(',') if v.strip()]
    assert values == LOOKUP, 'Enemy selector changed: research before extending bindings'
    return values


def audit_routes(codes):
    enemy = codes['Sprite_Handle_Enemy']
    rocket = codes['Sprite_Handle_Enemy_Rocket']
    soldier = codes['Sprite_Handle_Soldier_Animation']
    ordinary = codes['Sprite_Handle_Troop_Animation']
    assert 'Sprite_Handle_Soldier_Animation(' in enemy and 'mPersonType = eSprite_PersonType_AI;' in enemy
    assert enemy.index('Sprite_Handle_Soldier_Animation(') < enemy.index('mPersonType = eSprite_PersonType_AI;')
    assert 'pSprite->mFrameIndex = 1;' in enemy
    assert 'pSprite->mFrameIndex = 2;' in rocket and 'pSprite->mFiredWeaponType = 3;' in rocket
    assert all(s in soldier for s in ('Data0 = 0x63;', 'pSprite->mSheetIndex = 0x7A;',
        'pSprite->mSheetIndex = 0xA7;', 'pSprite->mSheetIndex = 0xCC;',
        'pSprite->mFrameIndex = 4;', 'pSprite->mFrameIndex %= 2;'))
    assert all(s in ordinary for s in ('pSprite->mSheetIndex = 0xDC;',
        'pSprite->mFollowTarget', 'else if (!word_3AA1D)', 'Data28 + Data8 + 0x18'))
    assert 'Sprite_Handle_Hostage(pSprite);' in codes['Sprite_Handle_Enemy_Leader']
    leader = codes['Sprite_Handle_Hostage']
    assert all(s in leader for s in ('pSprite->mPersonType = eSprite_PersonType_Native;',
        'pSprite->mSheetIndex = 0xD9;', 'pSprite->mSheetIndex = 0xD8;',
        'pSprite->mSheetIndex = 0x7C;', 'Data24->mSpriteType = eSprite_Flashing_Light;'))
    assert 'Sprite_Create_Player_Shadow(' not in leader
    assert 'Data28->mFollowTarget = pSprite;' in codes['Sprite_Handle_Hostage_Movement']
    assert 'pSprite->mSheetIndex = 0xDA;' in codes['Sprite_Hostage_Update_IdleFrame']
    assert 'pSprite->mSheetIndex = 0xC4;' in codes['Sprite_Handle_Flashing_Light']
    creator = codes['Sprite_Create_Player_Shadow']
    assert all(s in creator for s in ('Data2C->mSheetIndex = 0x8D;',
        'Data2C->mFrameIndex = 2;', 'Data2C->mAIAggression = pSprite->mSpriteType;'))


def inventory(root=ROOT):
    source = (root/'Source/Sprites.cpp').read_text(encoding='utf-8')
    lookup = table(source)
    codes = {}
    routes = []
    for name, (file, kind) in ROUTES.items():
        relative = 'Source/Sprites/' + file
        text = (root/relative).read_text(encoding='utf-8')
        code = function(text, kind+' cFodder::'+name+'(')
        codes[name] = code
        routes.append(dict(function=name, file=relative,
            line=text[:text.index(code)].count('\n')+1,
            sha256=hashlib.sha256(code.encode()).hexdigest()))
    audit_routes(codes)
    platforms = {}
    for platform in ('Amiga', 'PC'):
        text = (root/f'Source/{platform}/SpriteData_{platform}.hpp').read_text(encoding='utf-8')
        _, tables = check(text)
        arrays = {name: [[v.strip() for v in row.split(',')]
                        for row in re.findall(r'\{([^{}]+)\}', COMMENT.sub('', data))]
                  for name, _, data in ARRAY.findall(text)}
        refs = tables[f'mSpriteSheetTypes_InGame_{platform}']
        slots = {}

        def add(actor, sheet, frames, family, **context):
            for frame in frames:
                rows = arrays[refs[sheet]]
                assert 0 <= frame < len(rows), 'Native frame extent changed'
                slot = slots.setdefault((actor, sheet, frame), dict(actor_type=actor,
                    sheet=sheet, frame=frame, metadata=rows[frame], roles=[]))
                slot['roles'].append(dict(family=family, **context))

        for actor in (5, 36):
            for group, family in enumerate(GROUPS):
                for direction in range(8):
                    sheet = lookup[8*group+direction]
                    add(actor, sheet, range(len(arrays[refs[sheet]])), family,
                        direction=direction, table_offset=group*8)
            for sheet, family in ((0x7a, 'sinking'), (0xa7, 'slide'),
                                  (0xcc, 'vehicle_transition')):
                add(actor, sheet, range(len(arrays[refs[sheet]])), family)
            add(actor, 0x63, (0, 1), 'bleeding_irrecoverable')
            add(actor, 0x7c, (0, 1), 'native_hidden_marker')
            add(actor, 0xdc, (0,), 'follower_guard_idle')
        for sheet in (0xd8, 0xd9):
            add(106, sheet, range(24), 'leader_walk', native_person=2)
        add(106, 0xda, range(3), 'leader_idle', native_person=2)
        add(106, 0x7c, (0,), 'leader_hidden_vehicle', native_person=2)
        for sheet, frame, stage in ((0x8d, 2, 'creation'), (0x97, 0, 'air'), (0x97, 1, 'ground')):
            for owner in (5, 36):
                add(22, sheet, (frame,), 'owned_shadow', owner_type=owner, stage=stage)
        # Marker effect is associated, never a body or a fused body layer.
        add(41, 0xc4, range(4), 'leader_marker_association', owner_type=106)
        rows = sorted(slots.values(), key=lambda s:(s['actor_type'],s['sheet'],s['frame']))
        if platform == 'Amiga':
            demo = tables['mSpriteSheetTypes_InGame_Amiga_TheOne']
            assert all(refs[s['sheet']] == demo[s['sheet']] for s in rows), 'Amiga retail/demo divergence'
        by_actor = {str(actor):sum(s['actor_type']==actor for s in rows) for actor in (5,36,106,22,41)}
        unique = len({tuple(s['metadata']) for s in rows})
        platforms[platform] = dict(slots=rows, counts=dict(contracts=len(rows),
            by_actor=by_actor, unique_metadata_rows=unique))
    return dict(schema=1, revision=1, status='source inventory; runtime reachability refinements pending; not art completeness',
        actors=[dict(type=5, name='enemy infantry'), dict(type=36, name='enemy rocket infantry'),
                dict(type=106, name='enemy leader; native hostage controller, not ordinary infantry')],
        groups=list(GROUPS), routes=routes, platforms=platforms,
        cautions=['Enemy scratch mode-zero cannot inherit the protagonist dormant proof; keep 72..79',
            'Map enemies start with native person zero until first normal handler; injury before that needs explicit provenance research',
            'Type36 forces frame2 after selector: do not drop rocket frames based on player firing timing',
            'Type5 follower can draw DC when guarding hostage or leader; not a new civilian actor',
            'CC and 7C need native raster/no-write verification; no dummy body or guessed effect',
            'Shared metadata is a reuse candidate, never automatic artistic or identity equivalence',
            'Leader106 reuses native hostage visuals; scope is this actor, not modernization of civilians',
            'Leader light C4 remains an independent ordered association; do not fuse with body',
            'No shadow creation in leader handler: do not invent a leader ground shadow'],
        next='Refine producer bounds and native initial-person/vehicle transitions; then harvest private native references and signatures',
        invariants=['No simulation/AI/RNG/clock/direction/frame changes',
                    'No retail pixel data in this inventory', 'Protagonist art and classic mode independent'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,default=ROOT/'docs/modernization/evidence/enemy-state-catalog-v1.json')
    p.add_argument('--check',action='store_true')
    args=p.parse_args();result=inventory()
    if args.check:
        assert json.loads(args.out.read_text(encoding='utf-8'))==result, 'Enemy source catalog drift'
    else:
        args.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v['counts'] for k,v in result['platforms'].items()}))


if __name__ == '__main__':
    main()
