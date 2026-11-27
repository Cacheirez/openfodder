"""Inventory source-defined soldier frames; metadata only, no commercial image extraction.
GPL-3.0-or-later. Dynamic routes require runtime coverage, not inferred from this census.
"""
import argparse, hashlib, json, re
from pathlib import Path
from check_sprite_table_lengths import ARRAY, COMMENT, check
ROOT=Path(__file__).resolve().parents[2]
GROUPS=['walk','death_1','death_2','death_3_table_label','swim','throw','prone','rocket','standing_weapon']
DIRECTIONS=['forward','forward_left','left','left_away','away','away_right','right','right_forward']
def inventory():
 source=ROOT/'Source/Sprites.cpp';text=source.read_text();actors={}
 for actor,label in [('player','Human'),('enemy','Enemy')]:
  body=re.search(r'int16 mSprite_Animation'+label+r'Ptrs\[\]\s*=\s*\{([\s\S]*?)\};',text).group(1)
  keys=[int(v.strip(),0) for v in COMMENT.sub('',body).split(',') if v.strip()]
  assert len(keys)==72
  actors[actor]=keys
 result={'scope':'Static metadata for CF1 PC/Amiga human/enemy lookup tables; not runtime completeness, commercial variants or visual approval. Special direct routes listed separately for inspection.', 'metadata_fields':['mLoadOffset','mLoadSegment','field_4','field_6','mColCount','mRowCount','mPalleteIndex','mModX','mModY'],'sources':{},'platforms':{},'additional_sheet_metadata':{},'direct_route_candidates':[]}
 paths=[source,ROOT/'Source/SpriteSheet.hpp']
 for platform in ('PC','Amiga'):
  path=ROOT/f'Source/{platform}/SpriteData_{platform}.hpp';paths.append(path);text=path.read_text();counts,tables=check(text)
  arrays={name:[[v.strip() for v in row.split(',')] for row in re.findall(r'\{([^{}]+)\}',COMMENT.sub('',body))] for name,_,body in ARRAY.findall(text)}
  refs=tables[f'mSpriteSheetTypes_InGame_{platform}'];summary={}
  for actor,keys in actors.items():
   groups=[]
   for group in range(9):
    directions=[]
    for d in range(8):
     sheet=keys[group*8+d];name=refs[sheet];frames=arrays[name];assert len(frames)==counts[name] and all(len(f)==9 for f in frames)
     directions.append({'direction_index':d,'direction_label':DIRECTIONS[d],'sheet':sheet,'sheet_hex':hex(sheet),'array':name,'frames':frames,'frame_count':len(frames)})
    groups.append({'lookup_group':GROUPS[group],'lookup_offset':group*8,'directions':directions})
   summary[actor]={'unique_sheets':len(set(keys)),'unique_sheet_frame_keys':sum(counts[refs[k]] for k in set(keys)),'groups':groups}
  result['platforms'][platform]=summary
  # Includes declared death sheets bypassed by the animation aliases, special
  # bodies, shadows/ranks, hostage and hidden markers. Not all are authored bodies.
  extra=[0x2a,0x6c,0x38,0x41,0x7a,0x7b,0x7c,0x8d,0x95,0x97,0x9e,0x9f,0xa4,0xa7,0xcc,0xdc,0xe5,0xe6]
  result['additional_sheet_metadata'][platform]=[
   {'sheet':k,'sheet_hex':hex(k),'array':refs[k],'frame_count':counts[refs[k]],'frames':arrays[refs[k]],
    'note':'Declared table entry; inspect special/associated route and runtime reachability'} for k in extra]

 for name in ('Sprite_Troop.cpp','Sprite_Core.cpp','Sprite_Civilian.cpp'):
  path=ROOT/'Source/Sprites'/name;paths.append(path)
  for number,line in enumerate(path.read_text().splitlines(),1):
   match=re.search(r'\bmSheetIndex\s*=\s*(0x[0-9A-Fa-f]+|\d+)\s*;',line)
   if match:result['direct_route_candidates'].append({'source':str(path.relative_to(ROOT)),'line':number,'sheet':int(match.group(1),0),'statement':line.strip(),'classification':'inspect body/effect/hidden marker before authoring'})
 for candidate in result['direct_route_candidates']:
  lines=(ROOT/candidate['source']).read_text().splitlines()
  functions=re.findall(r'(?:void|int\d*|sSprite\*|bool)\s+cFodder::(\w+)\(', '\n'.join(lines[:candidate['line']]))
  function=functions[-1] if functions else 'unresolved'
  candidate['function']=function
  if candidate['sheet']==0x7c: category='hidden_or_placeholder_not_authored_body'
  elif 'Shadow' in function: category='associated_shadow'
  elif 'Rank' in function: category='associated_rank_or_bonus'
  elif any(x in function for x in ('Hostage','Civilian','Native')): category='civilian_or_hostage_separate_family'
  elif any(x in function for x in ('Soldier','Troop','Player_MissionOver')): category='soldier_special_body_or_transition'
  else: category='other_scene_or_effect_not_automatically_soldier'
  candidate['classification']=category
 for p in paths:result['sources'][str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args();result=inventory();a.out.write_text(json.dumps(result,indent=2)+'\n')
 for platform,actors in result['platforms'].items():
  for actor,info in actors.items():
   print(platform,actor,info['unique_sheets'],info['unique_sheet_frame_keys'],[(g['lookup_group'],[d['frame_count'] for d in g['directions']]) for g in info['groups']])
 print('Direct candidates:',len(result['direct_route_candidates']))
