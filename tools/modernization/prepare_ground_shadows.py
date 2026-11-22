"""Attach qualified ground paint to existing bodies without adding native keys.

The reviewed placement inventory pins every body hash. Water, damage, flight
and independent native shadows retain their existing descriptors and bindings.
"""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
PAINT = ROOT / 'assets/modernization/ground-shadow-paint'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def checked_file(directory, asset):
    name = asset['file']
    if Path(name).name != name or '/' in name or '\\' in name:
        raise ValueError('Expected a leaf asset filename')
    path = directory / name
    raw = path.read_bytes()
    expected_size = asset['width'] * asset['height'] * asset['density'] ** 2 * 4
    if len(raw) != expected_size or hashlib.sha256(raw).hexdigest() != asset['sha256']:
        raise ValueError(f'Invalid asset bytes: {asset["id"]}')
    return path


def prepare(base, out, placements_path=None):
    original = load(base)
    if original['version'] not in (2,3,4):
        raise ValueError('Expected ordered registry version 2, 3 or 4')
    density=original.get('density') if original['version']==4 else None
    if original['version']==4 and (type(density) is not int or density not in (8,12)):
        raise ValueError('Expected explicit density for version4')
    result = copy.deepcopy(original)
    assets = {a['id']: a for a in result['assets']}
    if len(assets) != len(result['assets']):
        raise ValueError('Duplicate body identifiers')
    if density is not None and any(a['density']!=density for a in result['assets']):
        raise ValueError('Asset differs from explicit selected density')
    sources = {a['id']: checked_file(base.parent, a) for a in result['assets']}
    paint = {a['id']: a for a in load(PAINT / 'manifest.json')['assets']}
    placements = load(placements_path or PAINT / 'placements.json')
    changed = set()
    for group in placements['groups']:
        for body in group['bodies']:
            identity = body['id']
            if density is not None and identity not in assets:
                suffix=re.search(r'-(8|12)x?$',identity)
                if suffix and int(suffix[1])!=density:continue
            if identity in changed or identity not in assets:
                raise ValueError(f'Missing or repeated qualified body: {identity}')
            asset = assets[identity]
            if asset['sha256'] != body['sha256']:
                raise ValueError(f'Body differs from qualified image: {identity}')
            shadow_id = f'ground-shadow-{group["width"]}x3-{asset["density"]}x'
            leaf = paint[shadow_id]
            component = dict(asset=shadow_id, x_quarters=group['x_quarters'],
                             y_quarters=group['y_quarters'], owner_type=group['owner_type'])
            if 'ground_shadow' in asset and asset['ground_shadow'] != component:
                raise ValueError(f'Conflicting ground shadow: {identity}')
            asset['ground_shadow'] = component
            if shadow_id in assets:
                if assets[shadow_id] != leaf:
                    raise ValueError(f'Conflicting paint: {shadow_id}')
            else:
                assets[shadow_id] = copy.deepcopy(leaf)
                result['assets'].append(assets[shadow_id])
                sources[shadow_id] = checked_file(PAINT, leaf)
            changed.add(identity)
    assert result['bindings'] == original['bindings']
    assert result.get('player_catalog') == original.get('player_catalog')
    assert result.get('enemy_catalog') == original.get('enemy_catalog')
    total=sum(a['width']*a['height']*a['density']**2*4 for a in result['assets'])
    if total>64*1024*1024:raise ValueError('Ground candidate exceeds 64 MiB')
    # Validate everything before creating the destination. Never overwrite a
    # candidate or mutate its source, including when paths alias each other.
    out.mkdir(parents=True, exist_ok=False)
    for asset in result['assets']:
        shutil.copyfile(sources[asset['id']], out / asset['file'])
    (out / 'candidate-manifest.json').write_text(
        json.dumps(result, indent=2) + '\n', encoding='utf-8')
    if original['version']==4:
        for name in ('native-evidence.json','missing-art.json'):
            if (base.parent/name).is_file():shutil.copyfile(base.parent/name,out/name)
        if (base.parent/'technical-summary.json').is_file():
            summary=load(base.parent/'technical-summary.json')
            summary['assets']=len(result['assets'])
            summary['asset_bytes']=total
            summary['enemy_ground_contact']='Technical contact qualification attached; Miguel visual acceptance pending'
            summary['qualified_ground_bodies']=len(changed)
            (out/'technical-summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    return len(changed), len(result['assets']), len(result['bindings'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--placements', type=Path, help='Explicit reviewed body hashes and ground placements')
    args = parser.parse_args()
    changed, assets, bindings = prepare(args.base, args.out, args.placements)
    print(f'PASS: {changed} qualified bodies, {assets} assets, {bindings} unchanged bindings')
