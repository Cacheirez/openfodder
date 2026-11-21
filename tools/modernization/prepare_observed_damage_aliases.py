"""Reconstruct four observed aliases; reuse existing art without changing pixels.

Requires private native snapshots/resources. Never infers an unknown key from
sheet/frame similarity. Existing full raster, palette and geometry must hash to
the already bound source key when only animation is changed.
"""
import argparse
import hashlib
import json
from pathlib import Path
from prepare_damage_candidate import native


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base', type=Path, required=True)
    p.add_argument('--native-json', type=Path, action='append', required=True)
    p.add_argument('--resources', type=Path, action='append', required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    root = Path(__file__).resolve().parents[2]
    contract = json.loads((root / 'assets/modernization/demo-a1-player-damage-aliases.json').read_text())
    assert len(contract['bindings']) == 4
    manifest = json.loads((a.base / 'candidate-manifest.json').read_text())
    assert len(manifest['assets']) == 244 and len(manifest['bindings']) == 387
    bindings = {b['key']: b for b in manifest['bindings']}
    inputs = {r['key']: (path, r) for path in a.native_json
              for r in [json.loads(path.read_text())]}
    for alias in contract['bindings']:
        key, source = alias['key'], alias['source_key']
        assert key not in bindings and source in bindings
        path, row = inputs[key]
        resources = next(d for d in a.resources if (d / row['resource_file']).is_file())
        row, _, compute = native(path, resources, key)
        assert row['type'] == row['person'] == row['vehicle'] == row['destroy'] == 0
        assert row['format'] == 1
        assert (row['sheet'], row['frame'], row['animation']) == (
            alias['sheet'], alias['frame'], alias['animation'])
        assert compute(alias['source_animation']) == source
        original = bindings[source]
        assert original['decision'] == 'replace-art' and original['assets'] == alias['assets']
        manifest['bindings'].append(dict(key=key, decision='replace-art', assets=original['assets']))
    assert not a.out.exists(), 'Use a fresh output directory'
    payloads = []
    for asset in manifest['assets']:
        assert Path(asset['file']).name == asset['file']
        raw = (a.base / asset['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == asset['sha256']
        payloads.append((asset['file'], raw))
    a.out.mkdir(parents=True)
    for name, raw in payloads:
        (a.out / name).write_bytes(raw)
    (a.out / 'candidate-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('PASS four observed native aliases, unchanged art/ground shadows; 244 assets / 391 bindings')


if __name__ == '__main__':
    main()
