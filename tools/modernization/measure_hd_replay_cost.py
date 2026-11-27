"""Whole-engine HD replay cost with immutable H3; Linux software SDL, not GPU FPS.
GPL-3.0-or-later. Fresh processes, excluded warmups and rotating mode order.
"""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys

from audit_replays import parse_log
from check_mission_publication_replays import sanitizer_findings
from verify_gameplay_determinism import sha_manifest

ROOT = Path(__file__).resolve().parents[2]
MODES = ('classic', 'publication', 'hd8', 'hd12')
CHILD = '''import json,resource,subprocess,sys,time
c=json.load(open(sys.argv[1]));start=time.perf_counter()
with open(c['log'],'wb') as log:
 p=subprocess.run(c['command'],cwd=c['cwd'],stdout=log,stderr=subprocess.STDOUT,timeout=600)
elapsed=time.perf_counter()-start;r=resource.getrusage(resource.RUSAGE_CHILDREN)
json.dump(dict(returncode=p.returncode,wall_seconds=elapsed,user_seconds=r.ru_utime,
 system_seconds=r.ru_stime,peak_rss_kib=r.ru_maxrss),open(c['metrics'],'w'))
sys.exit(p.returncode)
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_mode(log, mode):
    if mode not in MODES:
        raise ValueError('Unknown measurement mode')
    expected = {'MISSION_LAYER_AUDIT: verified real producer interval': mode != 'classic',
                'MISSION_LAYER_PRESENT: published verified orders': mode != 'classic',
                'SOLDIER_HD_SDL: published native background and HD patch': mode.startswith('hd')}
    for marker, required in expected.items():
        if (marker in log) != required:
            raise RuntimeError('Inactive or unexpected measured path: '+marker)
    if any(marker in log for marker in ('MISSION_PAUSE_PROBE:', 'MISSION_LAYER_SCHEDULE:',
                                       'SOLDIER_HD_COMPARE:', 'SOLDIER_HD_REASON:')):
        raise RuntimeError('Measurement contaminated by diagnostic/export scheduling')
    result = parse_log(log)
    if result['phases_passed'] != 3 or result['errors'] or result['skipped'] or sanitizer_findings(log):
        raise RuntimeError('Incomplete or invalid Amiga replay')


def read_optional(path):
    try:
        return Path(path).read_text().strip()
    except OSError:
        return 'unavailable'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--exe', type=Path, required=True)
    ap.add_argument('--data', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--rounds', type=int, default=3)
    ap.add_argument('--build-description', required=True)
    args = ap.parse_args()
    if platform.system() != 'Linux' or not 3 <= args.rounds <= 20:
        ap.error('Linux required; rounds must be 3..20')
    exe, data, out = args.exe.resolve(), args.data.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    baseline_source = ROOT/'tools/modernization/reference-gameplay-v1.json'
    reference = json.loads(baseline_source.read_text())
    reference['phases'] = [p for p in reference['phases'] if p['campaign'] == 'Amiga The One']
    assert len(reference['phases']) == 3
    reference['total_phases'] = 3
    reference['total_samples'] = sum(p['samples'] for p in reference['phases'])
    baseline = out/'baseline-selection.json'
    baseline.write_text(json.dumps(reference, indent=2)+'\n')
    fixture_hash, fixture_count = sha_manifest(data/'Tests')
    report = dict(verdict='FAIL', commit=subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
                  executable_sha256=sha(exe), build_description=args.build_description,
                  fixtures_sha256=fixture_hash, fixture_count=fixture_count,
                  baseline_sha256=sha(baseline_source), tool_sha256=sha(Path(__file__)),
                  host=platform.platform(), cpu=next((s.split(':',1)[1].strip() for s in read_optional('/proc/cpuinfo').splitlines() if s.startswith('model name')), 'unknown'),
                  cpu_max=read_optional('/sys/fs/cgroup/cpu.max'), memory_max=read_optional('/sys/fs/cgroup/memory.max'),
                  campaign='Amiga The One', rounds=args.rounds, runs=[], summary={},
                  method='Full three-phase campaign; one excluded warmup/mode, rotated order, fresh process per sample; identical executable, FIT, no sound and trace I/O; no export or pause probe',
                  limits=['Whole-process wall/CPU and high-water RSS, not per-frame latency or GPU time',
                          'Shared Linux software SDL; not user Windows, UHD, hardware GPU or VRAM',
                          'Three measured samples per mode by default; no p95/p99 or performance acceptance threshold',
                          'Publication includes semantic capture; HD comparison isolates its additional path',
                          'HD marker confirms at least one publication, not replacement rate or per-patch cost'])
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    try:
        for round_id in range(-1, args.rounds):
            rotation = 0 if round_id < 0 else round_id % len(MODES)
            for mode in MODES[rotation:]+MODES[:rotation]:
                work = out/f'round-{round_id}-{mode}'
                trace = work/'traces'
                trace.mkdir(parents=True)
                env = {k:v for k,v in os.environ.items() if not k.startswith('OPENFODDER_')}
                env.update(SDL_VIDEODRIVER='dummy', SDL_RENDER_DRIVER='software', SDL_AUDIODRIVER='dummy',
                           OPENFODDER_PRESENT_MISSION_LAYERS='0' if mode == 'classic' else '1',
                           OPENFODDER_CAPTURE_SOLDIER='0' if mode == 'classic' else '1',
                           OPENFODDER_SOLDIER_HD=mode[2:] if mode.startswith('hd') else '0',
                           OPENFODDER_SOLDIER_ART='0', OPENFODDER_REPLACE_SOLDIER_POSE='0',
                           OPENFODDER_AUDIT_MISSION_LAYERS='0', OPENFODDER_MISSION_SCREEN_TRANSFORM='1',
                           OPENFODDER_MISSION_SCREEN_FIT='1', OPENFODDER_HD_DIAGNOSTICS='0',
                           OPENFODDER_HD_COMPARE='0', OPENFODDER_TEST_FIRST_PHASE='0',
                           OPENFODDER_TEST_MISSION_PAUSE='0', OPENFODDER_TRACE_DIR=str(trace),
                           OPENFODDER_TRACE_REPLAY_SHA256=fixture_hash,
                           OPENFODDER_TRACE_SETTINGS_SHA256=hashlib.sha256(('hd-cost-v1:'+mode).encode()).hexdigest())
                config = dict(command=[str(exe), '--appveyor', '--unit-test', '--nosound', '--window',
                                       '--alternate-mouse', '--campaign', 'Amiga The One'],
                              cwd=str(data), log=str(work/'engine.log'), metrics=str(work/'metrics.json'))
                (work/'child.json').write_text(json.dumps(config))
                subprocess.run([sys.executable, '-c', CHILD, str(work/'child.json')], env=env, check=True, timeout=630)
                validate_mode((work/'engine.log').read_text(errors='replace'), mode)
                with (work/'h3.log').open('w') as log:
                    subprocess.run([sys.executable, str(ROOT/'tools/modernization/check_gameplay_baseline.py'),
                                    '--baseline', str(baseline), '--traces', str(trace)], stdout=log, stderr=subprocess.STDOUT, check=True)
                metrics = json.loads((work/'metrics.json').read_text())
                metrics['cpu_seconds'] = metrics['user_seconds']+metrics['system_seconds']
                assert sha(exe) == report['executable_sha256']
                report['runs'].append(dict(round=round_id, warmup=round_id < 0, mode=mode,
                                           canonical_states=reference['total_samples'], **metrics))
                (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
                print(f'round={round_id} mode={mode} H3=PASS wall={metrics["wall_seconds"]:.3f}s CPU={metrics["cpu_seconds"]:.3f}s RSS={metrics["peak_rss_kib"]}KiB', flush=True)
        for mode in MODES:
            rows = [r for r in report['runs'] if r['mode'] == mode and not r['warmup']]
            report['summary'][mode] = {}
            for key in ('wall_seconds','cpu_seconds','peak_rss_kib'):
                values = [r[key] for r in rows]
                report['summary'][mode][key] = dict(n=len(values), median=statistics.median(values), minimum=min(values), maximum=max(values))
        assert sha_manifest(data/'Tests')[0] == fixture_hash and sha(baseline_source) == report['baseline_sha256']
        report['verdict'] = 'PASS'
    except (OSError, RuntimeError, ValueError, AssertionError, subprocess.SubprocessError) as exc:
        report['failure'] = str(exc) or type(exc).__name__
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    # Exact trace/log evidence, compact enough to retain with the report.
    with gzip.open(out/'logs-traces.json.gz', 'wt') as archived:
        json.dump({str(p.relative_to(out)):p.read_text(errors='replace') for p in sorted(out.rglob('*'))
                   if p.is_file() and p.suffix in ('.log', '.jsonl')}, archived)
    print(json.dumps(report['summary'], indent=2))
    return 0 if report['verdict'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
