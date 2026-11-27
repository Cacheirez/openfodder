"""Pure mission layer assembly. Not a full engine replay or production wiring test."""
import os
from pathlib import Path
import subprocess
import tempfile

def main():
    root = Path(__file__).resolve().parents[2]
    with tempfile.TemporaryDirectory(prefix='mission-layers-') as td:
        binary = Path(td)/'test'
        subprocess.run(['g++', '-std=c++14', '-O1', '-g', '-fsanitize=address,undefined',
                        '-fno-sanitize-recover=all', '-I', str(root/'Source'),
                        str(root/'tools/modernization/mission_layers_fixture.cpp'), '-o', str(binary)], check=True)
        subprocess.run([str(binary)], check=True, env={**os.environ,
            'ASAN_OPTIONS': os.environ.get('ASAN_OPTIONS', 'detect_leaks=0')})

if __name__ == '__main__':
    main()
