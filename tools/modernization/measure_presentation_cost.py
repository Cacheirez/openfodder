"""Bounded whole-replay wall-time comparison; NOT frame latency or GPU throughput.
Same executable, fixtures, SDL software driver and H3 traces in every mode.
GPL-3.0-or-later.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys

from check_mission_publication_replays import sanitizer_findings
from verify_gameplay_determinism import sha_manifest

MODES = ('classic', 'audit', 'publication')


def validate_mode(log, mode):
    audit = 'MISSION_LAYER_AUDIT: verified real producer interval' in log
    publication = 'MISSION_LAYER_PRESENT: published verified orders' in log
    if audit != (mode != 'classic') or publication != (mode == 'publication'):
        raise RuntimeError('Inactive or unexpected presentation mode: ' + mode)
    if 'MISSION_PAUSE_PROBE:' in log or 'MISSION_LAYER_SCHEDULE:' in log:
        raise RuntimeError('Measurement contaminated by a diagnostic schedule')
    if sanitizer_findings(log):
        raise RuntimeError('Sanitizer finding in measured replay')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', type=Path, required=True)
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--rounds', type=int, default=3)
    args = parser.parse_args()
    if not 3 <= args.rounds <= 30:
        parser.error('--rounds must be between 3 and 30')
    root = Path(__file__).resolve().parents[2]
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    fixture_hash, count = sha_manifest(args.data.resolve()/'Tests')
    source = root/'tools/modernization/reference-gameplay-v1.json'
    reference = json.loads(source.read_text())
    names = {'PC_Format_m1_p1.jsonl', 'Amiga_The_One_m1_p1.jsonl'}
    reference['phases'] = [p for p in reference['phases'] if p['file'] in names]
    if {p['file'] for p in reference['phases']} != names:
        raise RuntimeError('Missing immutable phase reference')
    reference['total_phases'] = 2
    reference['total_samples'] = sum(p['samples'] for p in reference['phases'])
    baseline = out/'baseline-selection.json'
    baseline.write_text(json.dumps(reference, indent=2)+'\n')
    results = dict(verdict='FAIL', executable_sha256=hashlib.sha256(args.exe.read_bytes()).hexdigest(),
                   fixtures_sha256=fixture_hash, fixture_count=count,
                   baseline_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                   host=platform.platform(), machine=platform.machine(), rounds=args.rounds,
                   output_directory=str(out),
                   metric='whole child process wall seconds, including startup, trace I/O and teardown',
                   scope='PC/Amiga first phases; software SDL; no sound; one mission presentation',
                   limitations=['Shared host, not a controlled Windows/GPU benchmark',
                                'No per-frame p95/p99, CPU attribution, memory or upload counts',
                                'Small sample; timings are observations, not acceptance thresholds'],
                   runs=[], summary={})
    try:
        # One excluded warmup per mode; rotate order to reduce fixed-order bias.
        for round_id in range(-1, args.rounds):
            order = MODES if round_id < 0 else MODES[round_id % 3:] + MODES[:round_id % 3]
            for mode in order:
                traces = []
                samples = {}
                for slug, campaign in [('pc', 'PC Format'), ('amiga', 'Amiga The One')]:
                    directory = out/f'round-{round_id}-{mode}-{slug}'
                    trace = out/f'trace-{round_id}-{mode}-{slug}'
                    trace.mkdir()
                    traces.append(str(trace))
                    env = dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_RENDER_DRIVER='software',
                               SDL_AUDIODRIVER='dummy', OPENFODDER_TEST_FIRST_PHASE='1',
                               OPENFODDER_TEST_MISSION_PAUSE='0',
                               OPENFODDER_PRESENT_MISSION_LAYERS='1' if mode == 'publication' else '0',
                               OPENFODDER_AUDIT_MISSION_LAYERS='1' if mode == 'audit' else '0',
                               OPENFODDER_TRACE_DIR=str(trace),
                               OPENFODDER_TRACE_REPLAY_SHA256=fixture_hash,
                               OPENFODDER_TRACE_SETTINGS_SHA256=hashlib.sha256(('cost-v1:'+mode).encode()).hexdigest())
                    env.pop('OPENFODDER_TEST_MISSION_PRESENTATIONS', None)
                    subprocess.run([sys.executable, str(root/'tools/modernization/audit_replays.py'),
                                    '--exe', str(args.exe.resolve()), '--data', str(args.data.resolve()),
                                    '--out', str(directory), '--campaign', campaign, '--video', '--timeout', '180'],
                                   env=env, check=True, stdout=subprocess.DEVNULL)
                    report = json.loads((directory/'report.json').read_text())
                    if report['phases_passed'] != 1 or report['skipped'] or report['executable_sha256'] != results['executable_sha256']:
                        raise RuntimeError('Incomplete or changed measured executable')
                    validate_mode((directory/'engine.log').read_text(), mode)
                    samples[slug] = report['seconds']
                checked = subprocess.run([sys.executable, str(root/'tools/modernization/check_gameplay_baseline.py'),
                                          '--baseline', str(baseline), '--traces', *traces], capture_output=True, text=True)
                (out/f'baseline-{round_id}-{mode}.log').write_text(checked.stdout+checked.stderr)
                if checked.returncode:
                    raise RuntimeError('H3 rejected measured sample: '+checked.stdout.strip())
                results['runs'].append(dict(round=round_id, warmup=round_id < 0, mode=mode,
                                            seconds=samples, canonical_states=reference['total_samples']))
                print(f'round={round_id} mode={mode} H3=PASS seconds={samples}', flush=True)
        for mode in MODES:
            results['summary'][mode] = {}
            for slug in ('pc', 'amiga'):
                values = [r['seconds'][slug] for r in results['runs'] if r['mode'] == mode and not r['warmup']]
                results['summary'][mode][slug] = dict(median=statistics.median(values), minimum=min(values), maximum=max(values), n=len(values))
        results['verdict'] = 'PASS'
    except (RuntimeError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        results['failure'] = str(exc)
    (out/'report.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(results['summary'], indent=2))
    return 0 if results['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
