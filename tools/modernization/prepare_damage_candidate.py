"""Add only the verified falling alias to the isolated complete damage candidate.

Native inputs remain private. This validates provenance; it does not accept art
or promote other observed keys. The empty death marker is resolved by the engine.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

SOURCE = 'f2ddf9c44ea41ae03770069e9ce9566d32af64ddf1708b2f2a7c373f0b487270'
ALIAS = 'f62237ff841552359982d169df42a32f8c9270f598af5e624f6cf7db3a3abb06'
EMPTY = '82a12b8640bd6c6d5b5c7873771d81e47f102a89bba29000c0c1c44c93dfc81c'
FIELDS = ('format', 'type', 'person', 'sheet', 'frame', 'animation', 'segment',
          'vehicle', 'destroy', 'offset', 'layout_width', 'layout_height', 'planes',
          'resource_palette', 'palette', 'columns', 'rows', 'mod_x', 'mod_y')


def native(path, resources, expected):
    row = json.loads(path.read_text())
    resource = (resources / row['resource_file']).read_bytes()
    assert hashlib.sha256(resource).hexdigest() == row['resource_sha256']
    raster = b''.join(resource[row['offset'] + p * row['layout_height'] * 40 + y * 40:
                               row['offset'] + p * row['layout_height'] * 40 + y * 40 + (row['columns'] - 1) * 2]
                      for p in range(row['planes']) for y in range(row['rows']))
    assert len(raster) == row['planes'] * row['rows'] * (row['columns'] - 1) * 2
    def key(animation):
        values = {**row, 'animation': animation}
        return hashlib.sha256(struct.pack('<20q', 1, *(values[k] for k in FIELDS)) + raster +
                              struct.pack('<255Q', *(x & 0xffffff for x in row['colors']))).hexdigest()
    assert key(row['animation']) == row['key'] == expected
    return row, raster, key


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('base', 'fall_native', 'empty_native', 'resources', 'out'):
        p.add_argument('--' + name.replace('_', '-'), type=Path, required=True)
    a = p.parse_args()
    fall, _, key = native(a.fall_native, a.resources, ALIAS)
    assert (fall['type'], fall['sheet'], fall['frame'], fall['animation']) == (0, 0xb0, 0, 1)
    assert key(0) == SOURCE  # Entire raster, palette and geometry identical.
    empty, raster, _ = native(a.empty_native, a.resources, EMPTY)
    assert (empty['type'], empty['sheet'], empty['frame'], empty['animation']) == (0, 0x7c, 1, 6)
    assert not any(raster)  # Runtime additionally proves no producer writes.
    manifest = json.loads((a.base / 'candidate-manifest.json').read_text())
    assert len(manifest['assets']) == 244 and len(manifest['bindings']) == 386
    assert ALIAS not in {b['key'] for b in manifest['bindings']}
    source = next(b for b in manifest['bindings'] if b['key'] == SOURCE)
    assert source['decision'] == 'replace-art'
    manifest['bindings'].append({**source, 'key': ALIAS})
    assert not a.out.exists(), 'Use a fresh output; preserve previous evidence'
    payloads = []
    for asset in manifest['assets']:
        assert Path(asset['file']).name == asset['file']
        payload = (a.base / asset['file']).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == asset['sha256'], asset['id']
        payloads.append((asset['file'], payload))
    a.out.mkdir(parents=True)
    for name, payload in payloads:
        (a.out / name).write_bytes(payload)
    (a.out / 'candidate-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('PASS provenance, unchanged 244 assets/386 bindings + exact fall alias; 244/387; no unknown keys')


if __name__ == '__main__':
    main()
