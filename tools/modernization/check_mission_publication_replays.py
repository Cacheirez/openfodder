"""Real software-video publication, mandatory contrast and original H3 states.
Runs PC/Amiga demos at the existing cadence, not a whole-engine 0/1/N scheduler.
GPL-3.0-or-later.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from verify_gameplay_determinism import sha_manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--exe', type=Path, required=True)
    p.add_argument('--data', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--timeout', type=int, default=1200)
    args = p.parse_args()
    root = Path(__file__).resolve().parents[2]
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    fixture_hash, count = sha_manifest(args.data.resolve() / 'Tests')
    settings = {'flags': ['--appveyor', '--unit-test', '--nosound'],
                'publication': True, 'contrast': True, 'cadence': 'classic'}
    settings_hash = hashlib.sha256(json.dumps(settings, sort_keys=True).encode()).hexdigest()
    results = {'verdict': 'FAIL', 'settings': settings, 'fixtures_sha256': fixture_hash,
               'fixture_count': count, 'campaigns': []}
    traces = []
    try:
        for slug, campaign, phases in [('pc', 'PC Format', 8), ('amiga', 'Amiga The One', 3)]:
            trace = out / (slug + '-traces')
            trace.mkdir()
            traces.append(str(trace))
            env = dict(os.environ, OPENFODDER_PRESENT_MISSION_LAYERS='1',
                       OPENFODDER_AUDIT_MISSION_LAYERS='0',
                       OPENFODDER_TRACE_DIR=str(trace),
                       OPENFODDER_TRACE_REPLAY_SHA256=fixture_hash,
                       OPENFODDER_TRACE_SETTINGS_SHA256=settings_hash)
            subprocess.run([sys.executable, str(root/'tools/modernization/audit_replays.py'),
                            '--exe', str(args.exe.resolve()), '--data', str(args.data.resolve()),
                            '--out', str(out/slug), '--campaign', campaign, '--video',
                            '--timeout', str(args.timeout)], env=env, check=True)
            report = json.loads((out/slug/'report.json').read_text())
            log = (out/slug/'engine.log').read_text(errors='replace')
            if report['phases_passed'] != phases or report['skipped']:
                raise RuntimeError('Incomplete campaign: ' + campaign)
            for marker in ('MISSION_LAYER_AUDIT: verified real producer interval',
                           'MISSION_LAYER_PRESENT: published verified orders'):
                if marker not in log:
                    raise RuntimeError('Inactive publication/contrast: ' + campaign)
            results['campaigns'].append({'campaign': campaign, 'phases': phases,
                                        'seconds': report['seconds'],
                                        'executable_sha256': report['executable_sha256']})
        subprocess.run([sys.executable, str(root/'tools/modernization/check_gameplay_baseline.py'),
                        '--baseline', str(root/'tools/modernization/reference-gameplay-v1.json'),
                        '--traces', *traces], check=True)
        results.update(verdict='PASS', canonical_states=11361)
    except (subprocess.CalledProcessError, RuntimeError, OSError, ValueError) as exc:
        results['failure'] = str(exc)
    (out/'report.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(results, indent=2))
    return 0 if results['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
