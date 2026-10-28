"""Real software-video publication, mandatory contrast and original H3 states.
Runs PC/Amiga demos with optional 0/1/5 mission presentations per engine call.
Other scenes and interactive pause are outside this scheduling scope.
GPL-3.0-or-later.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
from verify_gameplay_determinism import sha_manifest


def sanitizer_findings(log):
    # UBSan can report an error and still return zero unless configured to halt.
    # Never treat replay completion or equal gameplay hashes as a clean memory run.
    pattern = r"runtime error:|(?:ERROR|WARNING|SUMMARY):\s*(?:AddressSanitizer|LeakSanitizer|ThreadSanitizer)|AddressSanitizer:DEADLYSIGNAL"
    return [line for line in log.splitlines() if re.search(pattern, line, re.I)]


def verify_pause_probe(log, phases):
    completed = re.findall(r'^MISSION_PAUSE_PROBE: completed (.+)$', log, re.M)
    resumed = re.findall(r'^MISSION_PAUSE_PROBE: resumed (.+)$', log, re.M)
    if len(completed) != 2 * phases or len(set(completed)) != len(completed) or resumed != completed:
        raise RuntimeError('Incomplete SDL pause/resume probe')
    return len(completed)


def verify_soldier_probe(log, phases):
    scenes = re.findall(r'^SOLDIER_SEMANTIC: verified original resource in mission composition scene=(\d+)$', log, re.M)
    if len(scenes) != phases or len(set(scenes)) != phases:
        raise RuntimeError('Incomplete semantic soldier scene coverage')
    return len(scenes)


def verify_pose_probe(log, phases):
    scenes = re.findall(r'^SOLDIER_POSE: verified replacement scene=(\d+)$', log, re.M)
    if len(scenes) != phases or len(set(scenes)) != phases:
        raise RuntimeError('Incomplete soldier pose replacement coverage')
    return len(scenes)


def art_probe_scenes(log):
    scenes = re.findall(r'^SOLDIER_ART: verified bounded RGBA replacement scene=(\d+)$', log, re.M)
    if len(scenes) != len(set(scenes)):
        raise RuntimeError('Duplicate art scene coverage')
    return len(scenes)


def require_art_coverage(campaigns):
    if sum(c['art_scenes'] for c in campaigns) == 0:
        raise RuntimeError('Art pilot never replaced its selected pose')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--exe', type=Path, required=True)
    p.add_argument('--data', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--presentations', type=int, choices=(0, 1, 5), help='Test-only mission presentation count; production cadence stays unchanged')
    p.add_argument('--first-phase', action='store_true', help='Explicit partial scope: first PC and Amiga phases only')
    p.add_argument('--pause-probe', action='store_true', help='Opt-in bounded SDL P-key pause/resume at mission ticks 8 and 16')
    p.add_argument('--soldier-probe', action='store_true', help='Require semantic soldier reproduction with original resources')
    p.add_argument('--pose-probe', action='store_true', help='Replace one original indexed pose and require per-scene evidence; implies soldier capture')
    p.add_argument('--screen-probe', action='store_true', help='Require presented mission transform and inverse; replay input remains canonical')
    p.add_argument('--art-probe', action='store_true', help='C01 RGBA pilot; require at least one actual selected-pose replacement across the declared campaigns')
    p.add_argument('--timeout', type=int, default=1200)
    args = p.parse_args()
    args.soldier_probe = args.soldier_probe or args.pose_probe or args.art_probe
    root = Path(__file__).resolve().parents[2]
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    fixture_hash, count = sha_manifest(args.data.resolve() / 'Tests')
    settings = {'flags': ['--appveyor', '--unit-test', '--nosound'],
                'publication': True, 'contrast': True, 'cadence': 'classic producers', 'mission_presentations': args.presentations if args.presentations is not None else 1,
                'pause_probe': args.pause_probe, 'soldier_probe': args.soldier_probe, 'pose_probe': args.pose_probe, 'art_probe': args.art_probe,
                'coverage': 'first phase per campaign' if args.first_phase else '11 reference phases'}
    if args.screen_probe:
        settings['flags'] += ['--window', '--alternate-mouse']
        settings['screen_probe'] = True
        settings['screen_fit'] = True
    settings_hash = hashlib.sha256(json.dumps(settings, sort_keys=True).encode()).hexdigest()
    results = {'verdict': 'FAIL', 'settings': settings, 'fixtures_sha256': fixture_hash,
               'fixture_count': count, 'campaigns': []}
    traces = []
    try:
        for slug, campaign, phases in [('pc', 'PC Format', 8), ('amiga', 'Amiga The One', 3)]:
            if args.first_phase:
                phases = 1
            trace = out / (slug + '-traces')
            trace.mkdir()
            traces.append(str(trace))
            env = dict(os.environ, OPENFODDER_PRESENT_MISSION_LAYERS='1',
                       OPENFODDER_MISSION_SCREEN_TRANSFORM='1' if args.screen_probe else '0',
                       OPENFODDER_MISSION_SCREEN_FIT='1' if args.screen_probe else '0',
                       OPENFODDER_AUDIT_MISSION_LAYERS='0',
                       OPENFODDER_SOLDIER_ART='1' if args.art_probe else '0',
                       OPENFODDER_REPLACE_SOLDIER_POSE='1' if args.pose_probe else '0',
                       OPENFODDER_CAPTURE_SOLDIER='1' if args.soldier_probe else '0',
                       OPENFODDER_TEST_FIRST_PHASE='1' if args.first_phase else '0',
                       OPENFODDER_TEST_MISSION_PAUSE='1' if args.pause_probe else '0',
                       OPENFODDER_TRACE_DIR=str(trace),
                       OPENFODDER_TRACE_REPLAY_SHA256=fixture_hash,
                       OPENFODDER_TRACE_SETTINGS_SHA256=settings_hash)
            env.pop('OPENFODDER_TEST_MISSION_PRESENTATIONS', None)
            if args.presentations is not None:
                env['OPENFODDER_TEST_MISSION_PRESENTATIONS'] = str(args.presentations)
            subprocess.run([sys.executable, str(root/'tools/modernization/audit_replays.py'),
                            '--exe', str(args.exe.resolve()), '--data', str(args.data.resolve()),
                            '--out', str(out/slug), '--campaign', campaign, '--video',
                            '--timeout', str(args.timeout)] + (['--screen-probe'] if args.screen_probe else []), env=env, check=True)
            report = json.loads((out/slug/'report.json').read_text())
            log = (out/slug/'engine.log').read_text(errors='replace')
            findings = sanitizer_findings(log)
            if findings:
                raise RuntimeError('Sanitizer findings in ' + campaign + ': ' + findings[0])
            if report['phases_passed'] != phases or report['skipped']:
                raise RuntimeError('Incomplete campaign: ' + campaign)
            markers = ['MISSION_LAYER_AUDIT: verified real producer interval']
            if args.soldier_probe:
                markers.append('SOLDIER_SEMANTIC: verified original resource in mission composition')
            published = 'MISSION_LAYER_PRESENT: published verified orders'
            if args.presentations == 0:
                if published in log:
                    raise RuntimeError('Unexpected mission publication in zero schedule: ' + campaign)
            else:
                markers.append(published)
            if args.presentations is not None:
                markers.append(f'MISSION_LAYER_SCHEDULE: {args.presentations} presentations per mission call')
            if args.screen_probe:
                markers.append('SCREEN_TRANSFORM: presented mission and verified mouse inverse')
                if args.pause_probe:
                    markers.append('SCREEN_TRANSFORM: fitted pause without mission input')
            for marker in markers:
                if marker not in log:
                    raise RuntimeError('Inactive publication/contrast/schedule: ' + campaign)
            soldier_scenes = verify_soldier_probe(log, phases) if args.soldier_probe else 0
            pose_scenes = verify_pose_probe(log, phases) if args.pose_probe else 0
            pauses = verify_pause_probe(log, phases) if args.pause_probe else 0
            results['campaigns'].append({'campaign': campaign, 'phases': phases,
                                        'pause_transitions': pauses, 'soldier_scenes': soldier_scenes, 'pose_scenes': pose_scenes, 'art_scenes': art_probe_scenes(log) if args.art_probe else 0,
                                        'seconds': report['seconds'],
                                        'executable_sha256': report['executable_sha256']})
        if args.art_probe:
            require_art_coverage(results['campaigns'])
        baseline = root/'tools/modernization/reference-gameplay-v1.json'
        expected_states = 11361
        if args.first_phase:
            # Select immutable existing hashes; never generate new expected states.
            reference = json.loads(baseline.read_text())
            names = {'PC_Format_m1_p1.jsonl', 'Amiga_The_One_m1_p1.jsonl'}
            reference['phases'] = [p for p in reference['phases'] if p['file'] in names]
            if {p['file'] for p in reference['phases']} != names:
                raise RuntimeError('Missing first-phase reference')
            reference['total_phases'] = 2
            expected_states = sum(p['samples'] for p in reference['phases'])
            reference['total_samples'] = expected_states
            results['baseline_source_sha256'] = hashlib.sha256(baseline.read_bytes()).hexdigest()
            baseline = out/'baseline-selection.json'
            baseline.write_text(json.dumps(reference, indent=2)+'\n')
        subprocess.run([sys.executable, str(root/'tools/modernization/check_gameplay_baseline.py'),
                        '--baseline', str(baseline),
                        '--traces', *traces], check=True)
        results.update(verdict='PASS', canonical_states=expected_states)
    except (subprocess.CalledProcessError, RuntimeError, OSError, ValueError) as exc:
        results['failure'] = str(exc)
    (out/'report.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(results, indent=2))
    return 0 if results['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
