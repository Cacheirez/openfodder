"""Combine reviewed D6 or green A assets with exact m1p2 keys and optional art.

No observation-driven approval, art generation or launcher activation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
D6_SHA256 = 'fa4cc26bd5ca25e8a7cd28ca0f3747b2c3e3c908a3645ededc2bf2363a5e0dd1'
GREEN_A_SHA256 = '96c0dd694171c39b19ff44190931164b6a60696e962d1933ff7749d3ccb7eb39'
ENEMY_PRONE_DIR = ROOT / 'assets/modernization/demo-a1-enemy-prone'
ENEMY_WALK_DIR = ROOT / 'assets/modernization/demo-a1-enemy-walk-45-f1'
ENEMY_DEATH_DIR = ROOT / 'assets/modernization/demo-a1-enemy-death-71-f1'
ENEMY_WALK_44_DIR = ROOT / 'assets/modernization/demo-a1-enemy-walk-44-f1'
ENEMY_DEATH_KEY = 'f06b98d0debe93b676cd17ba89a9b76e2b91484a08507c83e8d66215dc8237fb'
ENEMY_HIT_KEY = 'd615161944fbf97e9e07f29f4de6849c927c0d4e20087cbb981ec3c73e11dc45'
GROUND_HOLE_KEY = 'b27064e821fb760e4ec5e37a830ac2e35b81b46490abf208da81cc928cf63cf4'
TREE_90_KEY = 'a835b7ae71451ea0a37ea0a0c1e77da13a45f003b0cf218314edc6e0c79a1a2d'
BULLET_7F_KEY = '6c2cdf76311d72391780febb69499a2f1b94325ed1509838b7af65f3141d5981'


def prepare(base, out, with_roof=False, with_grenade_box=False, with_enemy_prone=False,
            with_enemy_walk=False, with_enemy_death=False, with_player_shadow=False,
            with_enemy_hit=False, with_enemy_walk_44=False, with_ground_hole=False,
            with_tree_90=False, with_bullet_7f=False):
    with_tree_90 = with_tree_90 or with_bullet_7f
    with_ground_hole = with_ground_hole or with_tree_90
    with_enemy_walk_44 = with_enemy_walk_44 or with_ground_hole
    with_enemy_hit = with_enemy_hit or with_enemy_walk_44
    with_player_shadow = with_player_shadow or with_enemy_hit
    with_enemy_death = with_enemy_death or with_player_shadow
    with_enemy_walk = with_enemy_walk or with_enemy_death
    with_enemy_prone = with_enemy_prone or with_enemy_walk
    with_grenade_box = with_grenade_box or with_enemy_prone
    source = base.read_bytes()
    green_a = hashlib.sha256(source.replace(b'\r\n', b'\n')).hexdigest() == GREEN_A_SHA256
    if not green_a and hashlib.sha256(source).hexdigest() != D6_SHA256:
        raise ValueError('Expected the reviewed D6 or green A manifest')
    if (with_roof or with_grenade_box) and not green_a:
        raise ValueError('The roof, grenade box and enemy options require the green A manifest')
    manifest = json.loads(source)
    additions = json.loads((ROOT / 'assets/modernization/demo-a1-associated.json').read_text())
    assert len(manifest['assets']) == 160 and len(manifest['bindings']) == 318
    assert all(b['decision'] == 'replace-art' for b in manifest['bindings'])
    assert len(additions['bindings']) == 8
    assert {(b['type'], b['sheet'], b['frame']) for b in additions['bindings']} == {
        (21, 0x95, 0), (21, 0x95, 4), (21, 0x7c, 0), (19, 0x98, 0), (19, 0x98, 1),
        (15, 0x91, 0), (37, 0xc2, 0), (22, 0x97, 1)}
    assert all(b['decision'] == 'keep-associated' for b in additions['bindings'])
    enabled = {15: with_roof or with_grenade_box, 37: with_grenade_box, 22: False}
    kept = [b for b in additions['bindings'] if enabled.get(b['type'], True)]
    manifest['bindings'] += [dict(key=b['key'], decision=b['decision']) for b in kept]
    asset_sources = [(base.parent, asset) for asset in manifest['assets']]
    for include, directory in ((with_enemy_prone, ENEMY_PRONE_DIR),
                               (with_enemy_walk, ENEMY_WALK_DIR),
                               (with_enemy_death, ENEMY_DEATH_DIR)):
        if not include:
            continue
        enemy = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
        asset_sources += [(directory, asset) for asset in enemy['assets']]
        manifest['assets'] += enemy['assets']
        manifest['bindings'] += enemy['bindings']
    if with_player_shadow:
        shadow = next(b for b in additions['bindings'] if b['type'] == 22)
        kept.append(shadow)
        manifest['bindings'].append(dict(key=shadow['key'], decision=shadow['decision']))
    if with_enemy_hit:
        death = next(b for b in manifest['bindings'] if b['key'] == ENEMY_DEATH_KEY)
        manifest['bindings'].append(dict(death, key=ENEMY_HIT_KEY))
    if with_enemy_walk_44:
        walk = json.loads((ENEMY_WALK_44_DIR / 'manifest.json').read_text(encoding='utf-8'))
        asset_sources += [(ENEMY_WALK_44_DIR, asset) for asset in walk['assets']]
        manifest['assets'] += walk['assets']
        manifest['bindings'] += walk['bindings']
    if with_ground_hole:
        ground_hole = dict(key=GROUND_HOLE_KEY, decision='keep-associated')
        kept.append(ground_hole)
        manifest['bindings'].append(ground_hole)
    if with_tree_90:
        tree = dict(key=TREE_90_KEY, decision='keep-associated')
        kept.append(tree)
        manifest['bindings'].append(tree)
    if with_bullet_7f:
        bullet = dict(key=BULLET_7F_KEY, decision='keep-associated')
        kept.append(bullet)
        manifest['bindings'].append(bullet)
    assert len({b['key'] for b in manifest['bindings']}) == len(manifest['bindings'])
    # Validate all existing bytes before creating an output directory.
    for directory, asset in asset_sources:
        path = Path(asset['file'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Non-relative asset path')
        if hashlib.sha256((directory / path).read_bytes()).hexdigest() != asset['sha256']:
            raise ValueError('Changed asset: ' + str(path))
    out.mkdir(parents=True, exist_ok=False)
    for directory, asset in asset_sources:
        target = out / asset['file']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(directory / asset['file'], target)
    path = out / 'candidate-manifest.json'
    path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return dict(assets=len(manifest['assets']), replace=len(manifest['bindings']) - len(kept),
                keep=len(kept), bindings=len(manifest['bindings']),
                manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=lambda p: Path(p).resolve(), required=True)
    parser.add_argument('--out', type=lambda p: Path(p).resolve(), required=True)
    parser.add_argument('--with-roof', action='store_true',
                        help='Retain the exact Amiga 0x91/F0 roof on green A with F4')
    parser.add_argument('--with-grenade-box', action='store_true',
                        help='Retain the exact Amiga 0xC2/F0 grenade box on green A with F4 and roof')
    parser.add_argument('--with-enemy-prone', action='store_true',
                        help='Replace the exact Amiga 0x59/F0 enemy on the green A candidate')
    parser.add_argument('--with-enemy-walk', action='store_true',
                        help='Replace the exact Amiga 0x45/F1 enemy on the green A candidate with 0x59/F0')
    parser.add_argument('--with-enemy-death', action='store_true',
                        help='Add the exact Amiga 0x71/F1 enemy to the green A candidate with 0x45/F1')
    parser.add_argument('--with-player-shadow', action='store_true',
                        help='Retain the exact Amiga 0x97/F1 shadow on the green A candidate with 0x71/F1')
    parser.add_argument('--with-enemy-hit', action='store_true',
                        help='Reuse the Amiga 0x71/F1 Die2 assets for the exact Hit variant')
    parser.add_argument('--with-enemy-walk-44', action='store_true',
                        help='Add the exact Amiga 0x44/F1 enemy to the green A candidate with Hit')
    parser.add_argument('--with-ground-hole', action='store_true',
                        help='Retain the exact Amiga GroundHole 0x7C/F0 on the green A candidate with 0x44/F1')
    parser.add_argument('--with-tree-90', action='store_true',
                        help='Retain the exact Amiga tree 0x90/F0 on the green A candidate with GroundHole')
    parser.add_argument('--with-bullet-7f', action='store_true',
                        help='Retain the exact Amiga bullet 0x7F/F0 on the green A candidate with the tree')
    args = parser.parse_args()
    print(json.dumps(prepare(args.base, args.out, args.with_roof, args.with_grenade_box,
                             args.with_enemy_prone, args.with_enemy_walk, args.with_enemy_death,
                             args.with_player_shadow, args.with_enemy_hit, args.with_enemy_walk_44,
                             args.with_ground_hole, args.with_tree_90, args.with_bullet_7f)))
