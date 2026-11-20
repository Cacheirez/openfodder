"""Bind five observed and qualified lower-aim poses; never the unobserved batch."""
import argparse
import hashlib
import json
from pathlib import Path
from prepare_damage_candidate import native


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('base', 'out'):
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--native-json', type=Path, action='append', required=True)
    p.add_argument('--resources', type=Path, action='append', required=True)
    a = p.parse_args()
    contract = json.loads((Path(__file__).resolve().parents[2] /
                          'assets/modernization/demo-a1-observed-aim.json').read_text())
    assert {b['sheet'] for b in contract['bindings']} == set(range(0x12, 0x17))
    assert len(contract['bindings']) == 5
    result = json.loads((a.base / 'candidate-manifest.json').read_text())
    assert len(result['assets']) == 244 and len(result['bindings']) == 391
    assets = {r['id']: r for r in result['assets']}
    for identifier, expected in contract['qualified_asset_descriptors'].items():
        descriptor = json.dumps(assets[identifier], sort_keys=True, separators=(',', ':')).encode()
        assert hashlib.sha256(descriptor).hexdigest() == expected
    inputs = {r['key']: (path, r) for path in a.native_json
              for r in [json.loads(path.read_text())]}
    keys = {b['key'] for b in result['bindings']}
    for binding in contract['bindings']:
        key = binding['key']
        assert key not in keys
        path, row = inputs[key]
        resource = next(d for d in a.resources if (d / row['resource_file']).is_file())
        row, _, _ = native(path, resource, key)
        assert row['type'] == row['person'] == row['animation'] == row['vehicle'] == row['destroy'] == 0
        assert row['format'] == 1 and row['segment'] == 0
        assert (row['sheet'], row['frame'], row['columns'], row['rows']) == (binding['sheet'], 0, 2, 14)
        assert row['mod_x'] == row['mod_y'] == row['palette'] == row['resource_palette'] == 0
        result['bindings'].append(dict(key=key, decision='replace-art', assets=binding['assets']))
    assert not a.out.exists(), 'Use a fresh output directory'
    payloads = []
    for asset in result['assets']:
        assert Path(asset['file']).name == asset['file']
        raw = (a.base / asset['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == asset['sha256']
        payloads.append((asset['file'], raw))
    a.out.mkdir(parents=True)
    for name, raw in payloads:
        (a.out / name).write_bytes(raw)
    (a.out / 'candidate-manifest.json').write_text(json.dumps(result, indent=2) + '\n')
    print('PASS five observed/qualified aim keys, unchanged bodies/shadows and previous 391 bindings; 244/396')


if __name__ == '__main__':
    main()
