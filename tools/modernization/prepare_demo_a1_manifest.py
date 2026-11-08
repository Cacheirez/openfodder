"""Combine the exact D6 assets with the four reviewed m1p2 scenery keys.

No observation-driven approval, art generation or launcher activation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
D6_SHA256 = 'fa4cc26bd5ca25e8a7cd28ca0f3747b2c3e3c908a3645ededc2bf2363a5e0dd1'


def prepare(base, out):
    if hashlib.sha256(base.read_bytes()).hexdigest() != D6_SHA256:
        raise ValueError('Expected the exact reviewed D6 manifest')
    manifest = json.loads(base.read_text())
    additions = json.loads((ROOT / 'assets/modernization/demo-a1-associated.json').read_text())
    assert len(manifest['assets']) == 160 and len(manifest['bindings']) == 318
    assert all(b['decision'] == 'replace-art' for b in manifest['bindings'])
    assert len(additions['bindings']) == 4
    assert {(b['type'], b['sheet'], b['frame']) for b in additions['bindings']} == {
        (21, 0x95, 0), (21, 0x7c, 0), (19, 0x98, 0), (19, 0x98, 1)}
    # Validate all existing bytes before creating an output directory.
    for asset in manifest['assets']:
        path = Path(asset['file'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Non-relative asset path')
        if hashlib.sha256((base.parent / path).read_bytes()).hexdigest() != asset['sha256']:
            raise ValueError('Changed D6 asset: ' + str(path))
    manifest['bindings'] += [dict(key=b['key'], decision='keep-associated') for b in additions['bindings']]
    assert len({b['key'] for b in manifest['bindings']}) == 322
    out.mkdir(parents=True, exist_ok=False)
    for asset in manifest['assets']:
        target = out / asset['file']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(base.parent / asset['file'], target)
    path = out / 'candidate-manifest.json'
    path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return dict(assets=160, replace=318, keep=4, bindings=322,
                manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=lambda p: Path(p).resolve(), required=True)
    parser.add_argument('--out', type=lambda p: Path(p).resolve(), required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.base, args.out)))
