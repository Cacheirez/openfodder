"""Closed CF1 protagonist pose inventory from selectors and bounded native tables.

Metadata only. Reachability evidence is explicit; declared surplus rows are not
silently called animation states. Runtime/resource/art validation is separate.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from check_sprite_table_lengths import ARRAY, COMMENT, check
from check_final_timer_equivalence import function

ROOT = Path(__file__).resolve().parents[2]
GROUPS = ('walk', 'damage_override', 'damage_ballistic', 'low_locomotion',
          'swim', 'grenade_throw', 'aim_low', 'rocket_fire', 'fall')
SPECIALS = {0x38: ('salute_or_sinking', 0), 0x41: ('jump_celebration', 0),
            0x9f: ('celebration_loop', 0), 0xa4: ('slide', 0),
            0xcc: ('vehicle_enter', 0), 0x9e: ('floating_body', 27)}
STATES = {'None': 0, 'Hit': 1, 'Hit2': 2, 'Hit3': 3, 'Die1': 5,
          'Die2': 6, 'Die3': 7, 'Die4': 9, 'Die5': 10,
          'Slide1': 50, 'Slide2': 51, 'Slide3': 52,
          'Vehicle_Enter': 90, 'Vehicle_Inside': 91}
ROUTES = {
    'Sprite_Handle_Player': ('Source/Sprites/Sprite_Troop.cpp', 'void',
        'dispatch: vehicle, injury/death/slide, mission-over, ordinary selector'),
    'Sprite_Handle_Soldier_Animation': ('Source/Sprites/Sprite_Troop.cpp', 'int16',
        'all injury/death states; Die5 -> 0x21 F0/F1 + blood; hidden 0x7C; slide 0xA4; enter 0xCC'),
    'Sprite_Handle_Troop_Animation': ('Source/Sprites/Sprite_Troop.cpp', 'void',
        'nine human table groups; 0xDC branch is nonhuman follower, excluded'),
    'Sprite_Handle_Player_MissionOver': ('Source/Sprites/Sprite_Troop.cpp', 'int16',
        '0x38 F0..5, 0x41 F0..5, 0x9F from fixed 0,1,2,3,2,1,2 sequence; water crop/height kept'),
    'Sprite_Update_Direction_Anim': ('Source/Sprites/Sprite_Core.cpp', 'void',
        'human table offset 0x40, frame 0, original face quantization'),
    'Sprite_Frame_Modifier_Update': ('Source/Sprites/Sprite_Core.cpp', 'void',
        'native clocks generate 0-1-2-1, not display FPS'),
    'Sprite_Handle_Player_InVehicle': ('Source/Sprites/Sprite_Vehicle.cpp', 'void',
        '0x7C/F0, hidden; vehicle art is a different family'),
    'Sprite_Troop_EnterVehicle_Finish': ('Source/Sprites/Sprite_Troop.cpp', 'int16',
        '0x7C/F0 then normal state'),
    'Sprite_Handle_Floating_Dead_Soldier': ('Source/Sprites/Sprite_Troop.cpp', 'void',
        'type27 -> 0x9E, frame retained from initialized/map state'),
    'Sprite_Handle_Player_Shadow': ('Source/Sprites/Sprite_Troop.cpp', 'void',
        'associated type22 0x97 F0/F1; owner/height offset (+5+h/4,-3+h/4), separate order'),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def art_reuse():
    path=ROOT/'assets/modernization/player-pose-reuse.json'
    if not path.exists():return []
    root=json.loads(path.read_text(encoding='utf-8'));assert root['schema']==1
    rows=root['entries'];assert isinstance(rows,list) and len(rows)<=32
    targets=set()
    for row in rows:
        assert row['actor_type']==0 and row['status']=='internally-reviewed-native-identical' and row['review']
        assert row.get('kind','asset') in ('asset','master-reexport')
        if row.get('kind')=='master-reexport':assert re.fullmatch(r'[0-9a-f]{64}',row['source_master_sha256'])
        assert all(type(row[k]) is int and 0<=row[k]<256 for k in ('sheet','frame','source_sheet','source_frame'))
        target=(row['sheet'],row['frame']);assert target not in targets;targets.add(target)
    return rows


def validate_art_reuse(slots,aliases):
    targets=set()
    for row in aliases:
        target=(row['sheet'],row['frame']);source=(row['source_sheet'],row['source_frame'])
        assert target not in targets and target!=source;targets.add(target)
        assert target in slots and source in slots,'Reuse outside finite source catalog'
        assert slots[target]==slots[source],'Reuse requires exact native table geometry/source'


def masters(reuse_rows=None):
    result = {}
    for name in ('soldier-walk24', 'soldier-aim', 'soldier-grenade', 'soldier-rocket'):
        path = ROOT / 'assets/modernization' / name / 'manifest.json'
        for row in json.loads(path.read_text(encoding='utf-8'))['frames']:
            source = row.get('uniform_a', row)
            image = ROOT / 'assets/modernization' / source['asset']
            assert image.is_file() and sha(image) == source['source_sha256']
            result[(row['sheet'], row['frame'])] = image.relative_to(ROOT).as_posix()
    for path in sorted((ROOT / 'assets/modernization').glob('demo-a1-player-*/manifest.json')):
        for asset in json.loads(path.read_text(encoding='utf-8')).get('assets', []):
            match = re.fullmatch(r'player-(?:fall|swim|hitdeath|pose)-([0-9a-f]+)-f(\d+)-8x', asset['id'])
            if match:
                raw = path.parent / asset['file']
                assert raw.is_file() and sha(raw) == asset['sha256']
                result[(int(match[1], 16), int(match[2]))] = raw.relative_to(ROOT).as_posix()
    for alias in (art_reuse() if reuse_rows is None else reuse_rows):
        target=(alias['sheet'],alias['frame']);source=(alias['source_sheet'],alias['source_frame'])
        assert source in result,'Explicit reuse needs an existing immutable master'
        if alias.get('kind')=='master-reexport':
            assert target in result,'Master reuse requires explicit target derivatives'
            source_file=ROOT/result[source];target_file=ROOT/result[target]
            source_master=source_file.parent/'source.png' if source_file.suffix=='.rgba' else source_file
            target_master=target_file.parent/'source.png' if target_file.suffix=='.rgba' else target_file
            assert sha(source_master)==sha(target_master)==alias['source_master_sha256'],'Reused master image differs'
        else:
            assert target not in result,'Duplicate explicit reused pose'
            result[target]=result[source]
    return result


def inventory(include_art=True):
    sprites = (ROOT / 'Source/Sprites.cpp').read_text(encoding='utf-8')
    header = (ROOT / 'Source/Sprites.hpp').read_text(encoding='utf-8')
    body = re.search(r'int16 mSprite_AnimationHumanPtrs\[\]\s*=\s*\{([\s\S]*?)\};', sprites)[1]
    lookup = [int(v.strip(), 0) for v in COMMENT.sub('', body).split(',') if v.strip()]
    assert len(lookup) == 72, 'New animation group requires research'
    enum = re.search(r'enum eSprite_Anim\s*\{([\s\S]*?)\};', header)[1]
    states = {k: int(v, 0) for k, v in re.findall(r'eSprite_Anim_(\w+)\s*=\s*(0x[0-9a-fA-F]+|\d+)', enum)}
    assert states == STATES, 'Unclassified animation state'
    sequence = re.search(r'mSprite_Player_MissionOver_Frames\[\]\s*=\s*\{([\s\S]*?)\};', sprites)[1]
    assert [int(x.strip()) for x in sequence.split(',') if x.strip()] == [0, 1, 2, 3, 2, 1, 2]
    routes = []
    for name, (file, result_type, evidence) in ROUTES.items():
        text = (ROOT / file).read_text(encoding='utf-8')
        code = function(text, result_type + ' cFodder::' + name + '(')
        routes.append(dict(function=name, file=file, line=text[:text.index(code)].count('\n') + 1,
                           sha256=hashlib.sha256(code.encode()).hexdigest(), evidence=evidence,
                           sheet_assignments=re.findall(r'(\w+->mSheetIndex\s*=\s*[^;]+);', code)))
    # Guard the important exceptional routes, not the misleading table comments.
    soldier = function((ROOT/'Source/Sprites/Sprite_Troop.cpp').read_text(encoding='utf-8'), 'int16 cFodder::Sprite_Handle_Soldier_Animation(')
    assert 'Data0 = 0x21;' in soldier and 'pSprite->mFrameIndex = 1;' in soldier
    assert 'pSprite->mSheetIndex = 0xCC;' in soldier and 'pSprite->mFrameIndex = 4;' in soldier
    art = masters() if include_art else {}
    platforms = {}
    for platform in ('Amiga', 'PC'):
        path = ROOT / f'Source/{platform}/SpriteData_{platform}.hpp'
        text = path.read_text(encoding='utf-8');counts,tables = check(text)
        arrays = {name: [[v.strip() for v in row.split(',')] for row in re.findall(r'\{([^{}]+)\}', COMMENT.sub('', data))]
                  for name, _, data in ARRAY.findall(text)}
        refs = tables[f'mSpriteSheetTypes_InGame_{platform}']
        slots = {}
        for group in range(9):
            for direction in range(8):
                sheet = lookup[8*group+direction]
                for frame, metadata in enumerate(arrays[refs[sheet]]):
                    key = (sheet, frame)
                    slot = slots.setdefault(key, dict(sheet=sheet, frame=frame, actor_type=0, roles=[], metadata=metadata))
                    slot['roles'].append(dict(family=GROUPS[group], direction=direction, table_offset=8*group))
        for sheet, (family, actor_type) in SPECIALS.items():
            for frame, metadata in enumerate(arrays[refs[sheet]]):
                slots[(sheet,frame)] = dict(sheet=sheet, frame=frame, actor_type=actor_type,
                    roles=[dict(family=family)], metadata=metadata)
        required=[];surplus=[]
        for key, slot in sorted(slots.items()):
            # The extra fourth rocket row is declared but no legitimate selector
            # generates it. Keep it visible as surplus rather than author a guess.
            if any(r['family']=='rocket_fire' for r in slot['roles']) and slot['frame']>2:
                surplus.append(dict(**slot,reason='rocket selector increments then resets at >=2; normal collision carry is modulo 2'))
                continue
            slot['master'] = art.get(key)
            same = [k for k in art if k[0]<len(refs) and k[1]<len(arrays[refs[k[0]]]) and arrays[refs[k[0]]][k[1]]==slot['metadata']]
            slot['exact_native_metadata_reuse'] = [dict(sheet=k[0],frame=k[1],master=art[k]) for k in same if k!=key]
            slot['art_state'] = 'master_present' if slot['master'] else 'exact_reuse_candidate' if same else 'missing'
            required.append(slot)
        validate_art_reuse({(row['sheet'],row['frame']):row['metadata'] for row in required},art_reuse())
        if platform=='Amiga':
            demo=tables['mSpriteSheetTypes_InGame_Amiga_TheOne']
            assert all(refs[s['sheet']]==demo[s['sheet']] for s in required), 'Retail/demo protagonist table divergence'
        platforms[platform]=dict(required=required,surplus=surplus,hidden=[dict(sheet=0x7c,frame=f,metadata=arrays[refs[0x7c]][f],classification='verify no native writes; not new artwork') for f in (0,1)],
            counts=dict(required=len(required),masters=sum(s['art_state']=='master_present' for s in required),exact_reuse_candidates=sum(s['art_state']=='exact_reuse_candidate' for s in required),missing=sum(s['art_state']=='missing' for s in required),surplus=len(surplus)))
    files=['Source/Sprites.hpp','Source/Sprites.cpp','Source/Sprites/Sprite_Troop.cpp','Source/Sprites/Sprite_Core.cpp','Source/Sprites/Sprite_Vehicle.cpp','Source/Amiga/SpriteData_Amiga.hpp','Source/PC/SpriteData_PC.hpp']
    return dict(schema=1,scope='CF1 protagonist mission actor state machine plus floating human body; table/selector and master audit, not runtime or artistic acceptance',states=states,groups=list(GROUPS),routes=routes,platforms=platforms,art_reuse=art_reuse(),
        sources={f:hashlib.sha256((ROOT/f).read_text(encoding='utf-8').encode()).hexdigest() for f in files},invariants=['native clocks/selectors unchanged','only frame metadata, no commercial bitmap data','animation variants do not automatically require distinct artwork','metadata aliases across different actions require artistic/semantic review, not automatic reuse','hidden markers need producer verification, never dummy bodies'],
        exceptional_states=[dict(state='Die5',sheet=0x21,frames=[0,1],clock='field_2A & 7; no FPS clock',associated='independent blood trail'),dict(state='Vehicle_Inside',sheet=0xcc,frames=[4,3,2,1,0],then='0x7C/F0 invisible'),dict(state='None / squad mode 0',sheets=list(range(0x30,0x38)),frames=[0,1,2],note='low-locomotion branch; squad modes initialize to 2; latent branch retained, not called death by its table label')],
        boundaries=['CF2/enemies/vehicle body art excluded','associated shadows,blood,ranks,projectiles,texts require validated native ordered commands','palette/phase/renderer recovery remains independent of protagonist art coverage','CD32 source tables covered; commercial CD32 runtime data not present in public replay directory'],
        reachability_notes=['floating frame is retained; both declared variants conservatively inventoried for map/saved state','rocket declared row 3 surplus, normal authored rows 0..2 retained','0x38 has both final and sinking contexts; position/height/crop do not create another artwork','retail Amiga/TheOne protagonist table entries exactly identical; text sheets A0/A1 differ, not merged'])


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'docs/modernization/evidence/player-state-catalog-v1.json');p.add_argument('--check',action='store_true');a=p.parse_args()
    result=inventory()
    if a.check:
        assert json.loads(a.out.read_text(encoding='utf-8'))==result, 'Player state catalog drift; research/update required'
    else:
        a.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v['counts'] for k,v in result['platforms'].items()}))


if __name__=='__main__':main()
