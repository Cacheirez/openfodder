"""Combine reviewed D6 or green A assets with the exact m1p2 associated keys.

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


def prepare(base, out, with_roof=False):
    source = base.read_bytes()
    green_a = hashlib.sha256(source.replace(b'\r\n', b'\n')).hexdigest() == GREEN_A_SHA256
    if not green_a and hashlib.sha256(source).hexdigest() != D6_SHA256:
        raise ValueError('Expected the reviewed D6 or green A manifest')
    if with_roof and not green_a:
        raise ValueError('The reviewed roof requires the green A manifest')
    manifest = json.loads(source)
    additions = json.loads((ROOT / 'assets/modernization/demo-a1-associated.json').read_text())
    assert len(manifest['assets']) == 160 and len(manifest['bindings']) == 318
    assert all(b['decision'] == 'replace-art' for b in manifest['bindings'])
    assert len(additions['bindings']) == 6
    assert {(b['type'], b['sheet'], b['frame']) for b in additions['bindings']} == {
        (21, 0x95, 0), (21, 0x95, 4), (21, 0x7c, 0), (19, 0x98, 0), (19, 0x98, 1), (15, 0x91, 0)}
    assert all(b['decision'] == 'keep-associated' for b in additions['bindings'])
    kept = [b for b in additions['bindings'] if with_roof or b['type'] != 15]
    # Validate all existing bytes before creating an output directory.
    for asset in manifest['assets']:
        path = Path(asset['file'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Non-relative asset path')
        if hashlib.sha256((base.parent / path).read_bytes()).hexdigest() != asset['sha256']:
            raise ValueError('Changed asset: ' + str(path))
    manifest['bindings'] += [dict(key=b['key'], decision=b['decision']) for b in kept]
    assert len({b['key'] for b in manifest['bindings']}) == len(manifest['bindings'])
    out.mkdir(parents=True, exist_ok=False)
    for asset in manifest['assets']:
        target = out / asset['file']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(base.parent / asset['file'], target)
    path = out / 'candidate-manifest.json'
    path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return dict(assets=160, replace=318, keep=len(kept), bindings=len(manifest['bindings']),
                manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=lambda p: Path(p).resolve(), required=True)
    parser.add_argument('--out', type=lambda p: Path(p).resolve(), required=True)
    parser.add_argument('--with-roof', action='store_true',
                        help='Retain the exact Amiga 0x91/F0 roof on green A with F4')
    args = parser.parse_args()
    print(json.dumps(prepare(args.base, args.out, args.with_roof)))
