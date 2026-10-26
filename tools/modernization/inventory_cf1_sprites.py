"""Read-only CF1 MAP/SPT census; emits counts, never source pixels or coordinates.
Original::loadCF1Spt consumes five big-endian words per record (10 bytes).
Uncompressed original resources only; unsupported input fails explicitly.
GPL-3.0-or-later.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import struct


def spt_types(data):
    if data.startswith(b'RNC'):
        raise ValueError('Compressed SPT requires the existing bounded resource loader')
    if not data or len(data) % 10:
        raise ValueError('SPT must contain complete 10-byte records')
    types = [record[4] for record in struct.iter_unpack('>5H', data)]
    if any(t >= 118 for t in types):
        raise ValueError('Sprite type outside the current dispatch table')
    return Counter(types)


def map_resources(data):
    if len(data) < 0x60 or data.startswith(b'RNC'):
        raise ValueError('Expected uncompressed CF1 MAP header')
    base, sub = data[:3].decode('ascii'), data[16:19].decode('ascii')
    if not re.fullmatch('[a-z]{3}', base) or not re.fullmatch('[a-z]{3}', sub):
        raise ValueError('Unsupported tileset prefix')
    return {'base_tileset': base, 'sub_tileset': sub,
            'ingame2': base+'copt.lbm', 'ingame1': sub+'army.lbm'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, required=True, help='Private Amiga_CD resource directory')
    parser.add_argument('--campaign', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    enum = (root/'Source/Sprites.hpp').read_text().split('enum eSprites {', 1)[1].split('};', 1)[0]
    names = {int(number): name for name, number in re.findall(r'eSprite_(\w+)\s*=\s*(\d+)', enum)}
    handlers = {}
    for path in sorted((root/'Source/Sprites').glob('*.cpp')):
        for match in re.finditer(r'(?:void|int16) cFodder::Sprite_Handle_(\w+)\(', path.read_text()):
            handlers[match.group(1)] = str(path.relative_to(root))
    campaign = json.loads(args.campaign.read_text())
    phases, totals, maps = [], Counter(), defaultdict(list)
    for mission_id, mission in enumerate(campaign['Missions'], 1):
        for phase_id, phase in enumerate(mission['Phases'], 1):
            name = phase['MapName']
            if not re.fullmatch(r'mapm\d+', name):
                raise ValueError('Only original mapmN names supported')
            spt, terrain = (args.data/(name+'.spt')).read_bytes(), (args.data/(name+'.map')).read_bytes()
            counts, resources = spt_types(spt), map_resources(terrain)
            for filename in (resources['ingame1'], resources['ingame2']):
                if not (args.data/filename).is_file():
                    raise ValueError('Missing graphics resource: '+filename)
            totals.update(counts)
            for sprite_type in counts:
                maps[sprite_type].append(name)
            phases.append(dict(mission=mission_id, phase=phase_id, map=name,
                               spt_sha256=hashlib.sha256(spt).hexdigest(),
                               map_sha256=hashlib.sha256(terrain).hexdigest(),
                               resources=resources, counts=dict(sorted(counts.items()))))
    if len({p['map'] for p in phases}) != len(phases):
        raise ValueError('Repeated map reference; coverage must be reviewed')
    report = dict(schema=1, scope='CF1 authored SPT records, including Null placeholders; not runtime coverage',
                  campaign_sha256=hashlib.sha256(args.campaign.read_bytes()).hexdigest(),
                  phase_count=len(phases), mission_count=len(campaign['Missions']),
                  authored_records=sum(totals.values()), null_records=totals[4],
                  distinct_authored_types=len(totals), phases=phases,
                  types=[dict(id=t, name=names.get(t, 'Reserved_'+str(t)), authored_count=totals[t],
                              maps=maps[t], handler=handlers.get(names.get(t, '')),
                              capabilities_status='Needs handler/state/terrain review; not inferred from the name')
                         for t in sorted(totals)],
                  declared_types_absent_from_spt=[dict(id=t, name=n) for t,n in sorted(names.items()) if t not in totals],
                  limitations=['SPT absence does not mean absence at runtime',
                               'Destructibility and control are conditional, not SPT boolean fields',
                               'CF2-only declarations are not CD32 assets',
                               'Does not enumerate terrain tiles or all animation states'])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('phase_count','mission_count','authored_records','null_records','distinct_authored_types')},indent=2))


if __name__ == '__main__':
    main()
