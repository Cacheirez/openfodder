"""Single-pose replacement and classic fallback, PC/Amiga, ASan/UBSan.
Synthetic sprites only. Not manual GPU or CD32 campaign evidence.
"""
import os
from pathlib import Path
import subprocess
import tempfile


def main():
    root = Path(__file__).resolve().parents[2]
    with tempfile.TemporaryDirectory(prefix='soldier-pose-') as temp:
        exe = Path(temp)/'test'
        subprocess.run(['g++', '-std=c++14', '-O1', '-g', '-fsanitize=address,undefined',
                        '-fno-sanitize-recover=all', '-I', str(root/'Source'), '-x', 'c++',
                        str(root/'tools/modernization/soldier_pose_cases.inc'), '-o', str(exe)], check=True)
        subprocess.run([str(exe)], check=True, env={**os.environ,
                       'ASAN_OPTIONS': os.environ.get('ASAN_OPTIONS', 'detect_leaks=0')})


if __name__ == '__main__':
    main()
