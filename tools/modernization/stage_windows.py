"""Stage a Windows test build with only the seven bundled demo data sets.

Uses a new directory and excludes git metadata, saved games and retail data.
SPDX-License-Identifier: GPL-3.0-or-later
"""
from pathlib import Path
import argparse
import json
import shutil
import subprocess


DEMO_DIRS = ('Plus', 'AmigaTheOne', 'AmigaAction', 'AmigaAlienLevels',
             'AmigaFormat_XMAS', 'AmigaFormat_NVF', 'PCFormat')


def stage(root, output, report):
    result = json.loads(report.read_text(encoding='utf-8'))
    if result.get('verdict') != 'PASS' or result.get('phases_passed') != 29 or result.get('skipped') != 0:
        raise ValueError('Expected a passing run with 29 phases and no skipped tests')
    run = root / 'Run'
    required = ('openfodder.exe', 'SDL3.dll', 'SDL3_mixer.dll')
    for name in required:
        if not (run / name).is_file():
            raise FileNotFoundError(run / name)
    output.mkdir(parents=True, exist_ok=False)
    for name in required:
        shutil.copy2(run / name, output / name)
    for name in DEMO_DIRS:
        shutil.copytree(run / 'Data' / name, output / 'Data' / name,
                        ignore=shutil.ignore_patterns('.git', '__pycache__'))
    for name in ('Campaigns', 'Scripts'):
        shutil.copytree(run / name, output / name, ignore=shutil.ignore_patterns('.git', '__pycache__'))
    (output / 'Saves').mkdir()
    shutil.copy2(run / 'about.png', output / 'about.png')
    for path in root.glob('COPYING*'):
        shutil.copy2(path, output / path.name)
    shutil.copy2(run / 'README.md', output / 'DATOS_DEMOS.md')
    shutil.copy2(root / 'docs/modernization/PRIMER_ARRANQUE_WINDOWS.md', output / 'LEEME.md')
    shutil.copy2(root / 'docs/modernization/VALIDAR_RATON_WINDOWS_H5.md', output / 'VALIDAR_RATON_H5.md')
    for name in ('PROBAR_RATON_H5.cmd', 'COMPARAR_RATON_CLASICO.cmd', 'PROBAR_RESOLUCIONES_H5.cmd', 'PROBAR_OPCIONES_H5.cmd', 'PROBAR_ESCENAS_H5.cmd', 'PROBAR_HD_8X.cmd', 'PROBAR_HD_12X.cmd'):
        text = (root / 'tools/modernization/windows' / name).read_text(encoding='ascii')
        (output / name).write_bytes(text.replace('\r\n', '\n').replace('\n', '\r\n').encode('ascii'))
    shutil.copy2(report, output / 'PRUEBAS.json')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    (output / 'VERSION.txt').write_text(commit+'\n', encoding='utf-8')
    (output / 'INICIAR.cmd').write_bytes(b'@echo off\r\ncd /d "%~dp0"\r\nopenfodder.exe --window --skipintro\r\nif errorlevel 1 pause\r\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    stage(args.root.resolve(), args.out.resolve(), args.report.resolve())
