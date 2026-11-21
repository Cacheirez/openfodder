"""Validate all 24 synthetic pose bindings through actual Window/SDL publication."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile
from ordered_soldier_coverage import report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', type=Path, required=True)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='ordered-assets-') as tmp:
        tmp = Path(tmp)
        (tmp/'nested').mkdir()
        log = tmp/'engine.log'
        with log.open('w') as stream:
            subprocess.run([str(args.exe.resolve())], cwd=tmp,
                           env={**os.environ, 'OPENFODDER_ORDERED_COVERAGE': '1'},
                           stdout=stream, stderr=subprocess.STDOUT, check=True, timeout=120)
        result = report([log])
        assert result['outcomes'] == {'published': 128}, result
        assert result['unique_producer_commands'] == 256, result
        assert result['published_command_presentations'] == 256, result
        assert result['unresolved_commands'] == 0, result
        assert len(result['variants']) == 96, result  # 24 keys * PC/Amiga * 8x/12x
        assert result['verdict'] == 'PENDING', result
        assert 'PASS external assets:' in log.read_text()
    print('PASS external assets: 128 actual SDL intervals, 256 commands, 96 variant/density entries; artistic acceptance PENDING')


if __name__ == '__main__':
    main()
