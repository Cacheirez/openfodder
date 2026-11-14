"""Run the actual Window fixture with diagnostics off/on and validate evidence."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile
from ordered_soldier_coverage import report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', type=Path, required=True)
    parser.add_argument('--hybrid', action='store_true')
    args = parser.parse_args()
    exe = args.exe.resolve()
    with tempfile.TemporaryDirectory(prefix='ordered-coverage-') as tmp:
        path = Path(tmp)/'engine.log'
        if args.hybrid:
            env = {**os.environ, 'OPENFODDER_ORDERED_COVERAGE': '1',
                   'OPENFODDER_TEST_ORDERED_HYBRID': '1'}
            with path.open('w') as log:
                subprocess.run([str(exe)], cwd=tmp, env=env, stdout=log, stderr=subprocess.STDOUT,
                               check=True, timeout=120)
            result = report([path])
            assert 'PASS hybrid Window:' in path.read_text(), result['outcomes']
            assert result['outcomes']['published'] == 20, result['outcomes']
            assert result['outcomes']['classic-recovered'] == 4, result['outcomes']
            for density in (8, 12):
                trees = [r for r in result['entity_states'] if r['type'] == 14 and r['density'] == density]
                assert len(trees) == 2, trees
                assert sum(r.get('resolution_keep', 0) for r in trees) == 4, trees
                assert sum(r['resolution_missing'] for r in trees) == 2, trees
            print('PASS hybrid coverage: 8x/12x, two HD actors, native tree and complete recovery')
            return
        for enabled in ('0', '1'):
            env = {**os.environ, 'OPENFODDER_ORDERED_COVERAGE': enabled}
            with path.open('w') as log:
                subprocess.run([str(exe)], cwd=tmp, env=env, stdout=log, stderr=subprocess.STDOUT,
                               check=True, timeout=120)
            result = report([path])
            if enabled == '0':
                assert result['attempts'] == 0, result
            else:
                assert result['outcomes'] == dict(published=16, **{'missing-variant': 8,
                    'classic-recovered': 2, 'recovery-failed': 2, 'no-body': 2,
                    'interrupted': 2, 'manifest-invalid': 1}), result
                assert result['published_command_presentations'] == 24, result
                assert result['unique_producer_commands'] == 3, result
                assert result['unique_published_variant_commands'] == 4, result
                assert result['unresolved_commands'] == 4, result
                assert result['verdict'] == 'PENDING', result
        print('PASS ordered coverage: real Window/SDL outcomes, opt-in, partial census, repeated presentations; acceptance PENDING')


if __name__ == '__main__':
    main()
