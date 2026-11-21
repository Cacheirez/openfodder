"""Independent PNG-to-RGBA contract; Python stdlib only, no private artwork."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import zlib


def png(path, width, height, rgba):
    def chunk(kind, value):
        return struct.pack('>I', len(value)) + kind + value + struct.pack('>I', zlib.crc32(kind + value))
    data = b''.join(b'\0' + rgba[y*width*4:(y+1)*width*4] for y in range(height))
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
                     + chunk(b'IDAT', zlib.compress(data)) + chunk(b'IEND', b''))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', type=Path, required=True)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='ordered-export-') as tmp:
        tmp = Path(tmp)
        source, target = tmp/'input.png', tmp/'pose.rgba'
        for density in (8, 12):
            target.unlink(missing_ok=True)
            width, height = 16*density, 14*density
            # Include transparent RGB and partial alpha to detect premultiplication.
            rgba = bytes(v for y in range(height) for x in range(width)
                         for v in (x % 256, y % 256, (x+y) % 256, (0, 128, 255)[x % 3]))
            png(source, width, height, rgba)
            command = [str(args.exe.resolve()), str(source), str(target), 'pose', '16', '14', str(density)]
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            manifest = json.loads(result.stdout)
            assert manifest == dict(id='pose', file='pose.rgba', width=16, height=14, density=density,
                                    sha256=hashlib.sha256(rgba).hexdigest()), manifest
            assert target.read_bytes() == rgba
            assert subprocess.run(command, capture_output=True).returncode == 0  # Idempotent export.
            target.write_bytes(b'preserve this derivative')
            assert subprocess.run(command, capture_output=True).returncode != 0
            assert target.read_bytes() == b'preserve this derivative'
            original = source.read_bytes()
            same = [str(args.exe.resolve()), str(source), str(source), 'pose', '16', '14', str(density)]
            assert subprocess.run(same, capture_output=True).returncode != 0
            assert source.read_bytes() == original
        for width, height, density in [('17', '14', '12'), ('16', '-1', '12'), ('16', '14', '9'),
                                       ('353', '14', '12'), ('16x', '14', '12')]:
            target.unlink(missing_ok=True)
            result = subprocess.run([str(args.exe.resolve()), str(source), str(target), 'pose', width, height, density],
                                    capture_output=True)
            assert result.returncode != 0 and not target.exists()
        source.write_bytes(b'broken PNG')
        result = subprocess.run([str(args.exe.resolve()), str(source), str(target), 'pose', '16', '14', '12'], capture_output=True)
        assert result.returncode != 0 and not target.exists()
    print('PASS exact PNG/RGBA exporter: 8x/12x, SHA, alpha, byte order, dimensions and invalid inputs')


if __name__ == '__main__':
    main()
