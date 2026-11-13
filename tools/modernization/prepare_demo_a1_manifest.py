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


def prepare(base, out, with_roof=False, with_grenade_box=False, with_enemy_prone=False,
            with_enemy_walk=False):
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
    assert len(additions['bindings']) == 7
    assert {(b['type'], b['sheet'], b['frame']) for b in additions['bindings']} == {
        (21, 0x95, 0), (21, 0x95, 4), (21, 0x7c, 0), (19, 0x98, 0), (19, 0x98, 1),
        (15, 0x91, 0), (37, 0xc2, 0)}
    assert all(b['decision'] == 'keep-associated' for b in additions['bindings'])
    enabled = {15: with_roof or with_grenade_box, 37: with_grenade_box}
    kept = [b for b in additions['bindings'] if enabled.get(b['type'], True)]
    manifest['bindings'] += [dict(key=b['key'], decision=b['decision']) for b in kept]
    asset_sources = [(base.parent, asset) for asset in manifest['assets']]
    for include, directory in ((with_enemy_prone, ENEMY_PRONE_DIR), (with_enemy_walk, ENEMY_WALK_DIR)):
        if not include:
            continue
        enemy = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
        asset_sources += [(directory, asset) for asset in enemy['assets']]
        manifest['assets'] += enemy['assets']
        manifest['bindings'] += enemy['bindings']
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
    args = parser.parse_args()
    print(json.dumps(prepare(args.base, args.out, args.with_roof, args.with_grenade_box,
                             args.with_enemy_prone, args.with_enemy_walk)))
