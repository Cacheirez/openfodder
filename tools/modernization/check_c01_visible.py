"""Reproduce C01 on the full public PC Format replay and retain a visible comparison.
GPL-3.0-or-later. Uses unchanged H3 reference, not a synthetic replacement scene.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
from audit_replays import parse_log
from check_mission_publication_replays import sanitizer_findings
from verify_gameplay_determinism import sha_manifest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--exe', type=Path, required=True)
    ap.add_argument('--data', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    exe, data, out = a.exe.resolve(), a.data.resolve(), a.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    reference = json.loads((root/'tools/modernization/reference-gameplay-v1.json').read_text())
    reference['phases'] = [p for p in reference['phases'] if p['campaign'] == 'PC Format']
    assert len(reference['phases']) == 8
    reference['total_phases'] = 8
    reference['total_samples'] = sum(p['samples'] for p in reference['phases'])
    baseline = out/'baseline-selection.json'
    baseline.write_text(json.dumps(reference, indent=2)+'\n')
    fixture_hash, _ = sha_manifest(data/'Tests')
    results = {'verdict': 'FAIL', 'campaign': 'PC Format', 'scope': '8 reference phases',
               'executable_sha256': hashlib.sha256(exe.read_bytes()).hexdigest(), 'densities': []}
    try:
        for density in (8, 12):
            work = out/str(density)
            trace = work/'traces'
            trace.mkdir(parents=True)
            env = dict(os.environ, OPENFODDER_SOLDIER_HD=str(density),
                       OPENFODDER_PRESENT_MISSION_LAYERS='1', OPENFODDER_CAPTURE_SOLDIER='1',
                       OPENFODDER_SOLDIER_ART='0', OPENFODDER_REPLACE_SOLDIER_POSE='0',
                       OPENFODDER_AUDIT_MISSION_LAYERS='0', OPENFODDER_MISSION_SCREEN_TRANSFORM='1',
                       OPENFODDER_MISSION_SCREEN_FIT='1', OPENFODDER_HD_DIAGNOSTICS='1',
                       OPENFODDER_HD_COMPARE='1', OPENFODDER_TEST_FIRST_PHASE='0',
                       OPENFODDER_TEST_MISSION_PAUSE='0', OPENFODDER_TRACE_DIR=str(trace),
                       OPENFODDER_TRACE_REPLAY_SHA256=fixture_hash,
                       OPENFODDER_TRACE_SETTINGS_SHA256=hashlib.sha256(f'C01-visible-{density}'.encode()).hexdigest())
            env.pop('OPENFODDER_TEST_MISSION_PRESENTATIONS', None)
            with (work/'engine.log').open('wb') as log:
                subprocess.run([str(exe), '--appveyor', '--unit-test', '--nosound', '--window',
                                '--alternate-mouse', '--campaign', 'PC Format'],
                               cwd=data, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=600, check=True)
            log = (work/'engine.log').read_text(errors='replace')
            report = parse_log(log)
            assert report['phases_passed'] == 8 and not report['errors'] and not report['skipped']
            assert not sanitizer_findings(log)
            assert 'SOLDIER_HD_SDL: published native background and HD patch' in log
            assert f'SOLDIER_HD_COMPARE: saved C01_{density}.html' in log
            assert 'SOLDIER_HD_REASON:' in log
            subprocess.run([sys.executable, str(root/'tools/modernization/check_gameplay_baseline.py'),
                            '--baseline', str(baseline), '--traces', str(trace)], check=True)
            files = []
            for suffix in ('.html', '_clasico.bmp', '_fondo.bmp', '_parche.bmp'):
                name = f'C01_{density}'+suffix
                source = data/name
                raw = source.read_bytes()
                if suffix.endswith('.bmp'):
                    assert raw[:2] == b'BM'
                    width, height = struct.unpack_from('<ii', raw, 18)
                    if suffix == '_parche.bmp':
                        assert (width, abs(height)) == (16*density, 14*density)
                shutil.copy2(source, work/name)
                files.append({'name': name, 'sha256': hashlib.sha256(raw).hexdigest()})
            results['densities'].append({'density': density, 'canonical_states': reference['total_samples'],
                                         'hd_published': True, 'files': files})
        results['verdict'] = 'PASS'
    except (AssertionError, OSError, subprocess.SubprocessError) as exc:
        results['failure'] = str(exc) or type(exc).__name__
    (out/'report.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(results, indent=2))
    return 0 if results['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
