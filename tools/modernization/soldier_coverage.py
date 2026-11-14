"""A1 static matrix + observed producer keys. Capture never proves HD publication.
GPL-3.0-or-later. --require-complete fails until publication/visual evidence exists.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
from inventory_soldier_catalog import inventory

SCENARIOS = ['continuous_turn', 'walk_0_1_2_1', 'aim_independent_of_motion', 'fire',
             'grenade', 'water', 'damage_death', 'multiple_players_and_enemies',
             'occlusions', 'viewport_edges', 'vehicle_transition', 'palette_transition',
             'pause_resume', 'phase_transition', 'civilian_hostage', 'resource_variants_cd32']
BODY_TYPES = {0: 'player', 5: 'enemy', 36: 'enemy_rocket', 27: 'floating_dead_soldier'}
CIVILIAN_TYPES = {61, 62, 70, 71, 72, 83}
ASSOCIATED_TYPES = {2, 3, 6, 21, 22, 23, 33, 35, 93, 94, 95, 96, 98}

def matrix(catalog):
    rows = {}
    for platform, actors in catalog['platforms'].items():
        for actor, info in actors.items():
            for group in info['groups']:
                for direction in group['directions']:
                    for frame, metadata in enumerate(direction['frames']):
                        key = (platform, actor, direction['sheet'], frame)
                        row = rows.setdefault(key, dict(platform=platform, actor=actor,
                            sheet=direction['sheet'], frame=frame, metadata=metadata,
                            array=direction['array'], states=[], runtime='pending', art='missing', visual='pending'))
                        row['states'].append(dict(family=group['lookup_group'], direction=direction['direction_index']))
                        if actor == 'player' and group['lookup_group'] == 'walk' and direction['sheet'] in (2, 7) and frame in (0, 1, 2):
                            row['art'] = 'C01_accepted_master' if (direction['sheet'], frame) == (7, 0) else 'provisional_master'
    return list(rows.values())

def classify(record, body_keys):
    t = record['type']
    if record['sheet'] == 0x7c:
        return 'hidden_or_placeholder'
    if t in BODY_TYPES:
        return BODY_TYPES[t]
    if t in CIVILIAN_TYPES:
        return 'civilian_or_hostage'
    if t in ASSOCIATED_TYPES:
        return 'associated_effect'
    if (record['format'], record['sheet'], record['frame']) in body_keys:
        return 'unexpected_body_type'
    return 'other_or_unclassified'  # not silently accepted as harmless

def report(logs=()):
    catalog = inventory()
    rows = matrix(catalog)
    body_keys = {(0 if r['platform']=='PC' else 1, r['sheet'], r['frame']) for r in rows}
    observed = Counter()
    entities = set()
    record_count = 0
    seen_commands = set()
    duplicate_audits = 0
    # Keep resource versions, palettes, clipping, face/motion and person variant
    # separate. Intervals/ticks are counted, never mistaken for unique art keys.
    key_fields = ['type','person','sheet','frame','animation','direction','face','vehicle','destroy',
                  'format','segment','resource','offset','palette','width','height','planes','skip','crop']
    for path in logs:
        with Path(path).open(errors='replace') as stream:
            for line in stream:
                if 'SOLDIER_CAPTURE: ' not in line:
                    continue
                record = {k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line.split('SOLDIER_CAPTURE: ',1)[1])}
                required = set(key_fields + ['scene','interval','order','slot','generation','tick','x','y','columns','rows'])
                if not required <= record.keys():
                    raise ValueError(f'incomplete capture record in {path}')
                identity = (str(path),record['scene'],record['interval'],record['order'])
                if identity in seen_commands:
                    duplicate_audits += 1
                    continue
                seen_commands.add(identity)
                classification = classify(record, body_keys)
                observed[(str(path),classification,*(record[k] for k in key_fields))] += 1
                entities.add((str(path),record['scene'],record['slot'],record['generation']))
                record_count += 1
    observations=[]
    for key,count in sorted(observed.items()):
        row=dict(zip(key_fields,key[2:]));row.update(log=key[0],classification=key[1],draws=count,publication='unverified')
        observations.append(row)
    reached={(o['format'],o['sheet'],o['frame'], 'player' if o['type']==0 else 'enemy')
             for o in observations if o['type'] in (0,5,36)}
    for row in rows:
        if (0 if row['platform']=='PC' else 1,row['sheet'],row['frame'],row['actor']) in reached:
            row['runtime']='captured_not_publication'
    return dict(schema=1, verdict='PENDING', scope='CF1 static and producer coverage; not visual acceptance or complete CD32 variants',
        sources=catalog['sources'], static_rows=len(rows), rows=rows,
        special_routes=catalog['direct_route_candidates'], additional_sheets={
            platform:[{k:v for k,v in row.items() if k!='frames'} for row in sheets]
            for platform,sheets in catalog['additional_sheet_metadata'].items()},
        walk24=[dict(platform=r['platform'],actor=r['actor'],sheet=r['sheet'],frame=r['frame'],
                     direction=s['direction'],array=r['array'],metadata=r['metadata'],art=r['art'])
                for r in rows for s in r['states'] if s['family']=='walk'],
        scenarios={s:'pending' for s in SCENARIOS}, captured_draws=record_count, duplicate_audits=duplicate_audits, entities=len(entities),
        observations=observations, blockers=['Producer capture alone does not establish SDL publication; see ordered_soldier_coverage.py',
            'Full artwork/state/resource coverage pending', 'Continuous visual/CD32 validation pending'])

def write_report(path, result):
    # Keep one matrix row per line; metadata is still exact and machine-readable.
    parts=[]
    for key,value in result.items():
        if isinstance(value,list) and value and isinstance(value[0],dict):
            encoded='[\n'+',\n'.join('    '+json.dumps(row,separators=(',',':')) for row in value)+'\n  ]'
        else:
            encoded=json.dumps(value,ensure_ascii=False)
        parts.append('  '+json.dumps(key)+': '+encoded)
    path.write_text('{\n'+',\n'.join(parts)+'\n}\n')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log',action='append',type=Path,default=[])
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--require-complete',action='store_true')
    args=parser.parse_args();result=report(args.log)
    write_report(args.out,result)
    print(json.dumps({k:result[k] for k in ('verdict','static_rows','captured_draws','entities','blockers')}))
    return 1 if args.require_complete and result['verdict']!='PASS' else 0
if __name__=='__main__':raise SystemExit(main())
