"""Export private CF1 enemy references from retained, hashed native banks.

No retail pixels or native resource banks are written to the repository. Source
catalog rows define the extraction, independently of poses observed in a replay.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image
from inventory_enemy_states import inventory
from prepare_player_catalog import indices, signature


def build(resources, out):
    assert not out.exists(), 'Preserve previous references'
    retained = {}
    for fmt, directory in resources:
        assert fmt in (0, 1)
        for path in sorted(directory.glob('*.json')):
            row = json.loads(path.read_text(encoding='utf-8'))
            segment = row.get('segment')
            if row.get('format') != fmt or segment not in (0, 1):
                continue
            data = (directory/row['resource_file']).read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            assert digest == row['resource_sha256'], 'Native bank hash mismatch'
            retained.setdefault((fmt, segment), {})[digest] = (row, data)
    assert set(retained) == {(fmt, seg) for fmt in (0, 1) for seg in (0, 1)}
    catalog = inventory()
    # Complete bounds validation before writing any reference.
    captures = []
    for fmt, name in enumerate(('PC', 'Amiga')):
        for slot in catalog['platforms'][name]['slots']:
            metadata = slot['metadata']
            segment = {'eGFX_IN_GAME':0, 'eGFX_IN_GAME2':1}[metadata[1]]
            offset = int(metadata[0], 0)
            width = int(metadata[4], 0) if fmt == 0 else (int(metadata[4], 0)-1)*16
            height = int(metadata[5], 0)
            palette = int(metadata[6], 0) if fmt == 0 else 0
            for digest, (row, data) in sorted(retained[fmt, segment].items()):
                raw = indices(data, offset, width, height, fmt, row['layout_height'])
                assert len(raw) == width*height
                if slot['sheet'] == 0x7c:
                    assert not any(raw), 'Native hidden marker unexpectedly writes'
                captures.append((fmt, slot, row, digest, width, height, palette, raw))
    out.mkdir(parents=True)
    (out/'native').mkdir()
    audit = []
    for fmt, slot, row, digest, width, height, palette, raw in captures:
        pixels = bytearray()
        for value in raw:
            color = row['colors'][palette+value]
            pixels.extend(((color>>16)&255, (color>>8)&255, color&255, 255 if value else 0))
        name = f"{fmt}-{slot['actor_type']}-{slot['sheet']:02x}-f{slot['frame']}-{digest[:8]}.png"
        image = Image.frombytes('RGBA', (width, height), bytes(pixels))
        image.save(out/'native'/name)
        audit.append(dict(format=fmt, type=slot['actor_type'], sheet=slot['sheet'],
            frame=slot['frame'], resource_sha256=digest, native_signature=signature(raw,width,height),
            width=width, height=height, reference='native/'+name,
            bbox=image.getchannel('A').getbbox(), opaque_pixels=sum(bool(v) for v in raw)))
    (out/'native-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    summary = dict(schema=1, scope='private references; no art/visual acceptance',
        captures=len(audit), resources=[dict(format=fmt,segment=seg,sha256=sha)
            for (fmt,seg),items in sorted(retained.items()) for sha in sorted(items)],
        by_format={str(fmt):sum(r['format']==fmt for r in audit) for fmt in (0,1)},
        opaque_contracts=sum(r['opaque_pixels']>0 for r in audit),
        unique_rasters=len({r['native_signature'] for r in audit}))
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--resources', nargs=2, action='append', required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    build([(int(fmt), Path(path)) for fmt,path in a.resources], a.out)
