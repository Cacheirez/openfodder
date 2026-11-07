"""Independent known-pixel and corruption checks for local native review tools."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile


def check(fixture, renderer, directory):
    subprocess.run([str(fixture), str(directory)], check=True)
    sources = list(directory.glob('*.json'))
    assert len(sources) == 2
    negatives = 0
    for source in sources:
        row = json.loads(source.read_text())
        out = directory/'pose.rgba'
        result = json.loads(subprocess.check_output([str(renderer), str(source), str(directory), str(out)], text=True))
        assert (result['width'], result['height']) == (16, 14)
        # Both fixtures encode alternating 1/2, through different legacy formats.
        # Derive RGB directly from the known fixture palette, independently of C++ raster.
        indices = [((1 if x % 2 == 0 else 2) | row['palette']) for y in range(14) for x in range(16)]
        expected = bytes(c for i in indices for c in ((row['colors'][i] >> 16) & 255,
            (row['colors'][i] >> 8) & 255, row['colors'][i] & 255, 255))
        assert out.read_bytes() == expected
        for field, value in [('key', '0'*64), ('resource_file', '../escape.bin'),
                             ('resource_sha256', '0'*64), ('columns', -1), ('rows', 273)]:
            changed = dict(row, **{field: value})
            bad = directory/'bad.json';bad.write_text(json.dumps(changed))
            tested = subprocess.run([str(renderer), str(bad), str(directory), str(out)], capture_output=True)
            assert tested.returncode != 0, (field, tested.stdout)
            assert out.read_bytes() == expected  # Failed input cannot overwrite the valid result.
            negatives += 1
        resource = directory/row['resource_file'];original = resource.read_bytes()
        resource.write_bytes(bytes([original[0] ^ 1])+original[1:])
        assert subprocess.run([str(renderer), str(source), str(directory), str(out)], capture_output=True).returncode != 0
        resource.write_bytes(original);negatives += 1
    print(f'PASS native snapshots: PC/Amiga known pixels, source/key integrity, duplicate capture, {negatives} negative cases')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture', type=lambda s: Path(s).resolve(), required=True)
    parser.add_argument('--renderer', type=lambda s: Path(s).resolve(), required=True)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='native-snapshot-') as tmp:
        check(args.fixture, args.renderer, Path(tmp))
