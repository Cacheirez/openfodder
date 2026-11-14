"""A-only local manual diagnostic. Reuse A.1, normal clock, no delivery package.

Each invocation copies the existing public data to a fresh output directory
and keeps the full engine log locally. No existing
launcher, executable, manifest, replay or game settings are overwritten.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

from ordered_soldier_coverage import report

EXE_SHA = '04e6d63e7335f41f539665409b610cd920c729e4e65d3fcad17c37287a7d7b3b'
MANIFEST_SHA = 'dd81d551031cfc8ac0265c4979c80575fcf31c1bb9166ebc8a563fb216a18147'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--classic', action='store_true')
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    source = args.source.resolve()
    manifest = source / 'art-complete/candidate-manifest.json'
    if sha(source / 'data/openfodder.exe') != EXE_SHA or sha(manifest) != MANIFEST_SHA:
        parser.error('A.1 executable/manifest does not match the verified handoff')
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    data = out / 'data'
    shutil.copytree(source / 'data', data)
    assert sha(data / 'openfodder.exe') == EXE_SHA
    # Process-local environment: no persistent settings or security changes.
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(('OPENFODDER_', 'SDL_'))}
    env.update(SDL_RENDER_DRIVER='software',
               OPENFODDER_PRESENT_MISSION_LAYERS='1',
               OPENFODDER_CAPTURE_SOLDIER='1',
               OPENFODDER_SOLDIER_HD='0' if args.classic else '12',
               OPENFODDER_SOLDIER_BATCH='0', OPENFODDER_SOLDIER_ART='0',
               OPENFODDER_REPLACE_SOLDIER_POSE='0', OPENFODDER_HD_COMPARE='0',
               OPENFODDER_MISSION_SCREEN_TRANSFORM='1',
               OPENFODDER_MISSION_SCREEN_FIT='1',
               OPENFODDER_SOLDIER_ORDERED_MANIFEST=str(manifest),
               OPENFODDER_ORDERED_COVERAGE='1', OPENFODDER_ORDERED_KEYS='1',
               OPENFODDER_HD_DIAGNOSTICS='1')
    # --appveyor only preserves redirected diagnostic streams on Windows;
    # it does not select --unit-test or alter the interrupt cadence.
    command = [str(data / 'openfodder.exe'), '--appveyor', '--nosound', '--window',
               '--window-scale', '3', '--alternate-mouse', '--campaign',
               'Amiga The One', '--mission', '1', '--phase', '2', '--skipbriefing']
    info = dict(schema=1, scope='A.1 manual diagnostic; visual acceptance PENDING',
                classic=args.classic, command=command, environment_overrides={
                    k: v for k, v in env.items() if k.startswith(('OPENFODDER_', 'SDL_'))},
                exe_sha256=EXE_SHA, manifest_sha256=MANIFEST_SHA,
                unit_test=False, playback=False, sound=False,
                clock='unmodified normal production cadence, default 20ms interrupt',
                started_utc=datetime.now(timezone.utc).isoformat())
    (out / 'session.json').write_text(json.dumps(info, indent=2) + '\n')
    print('A.1 manual, reloj normal, renderizado software, sin sonido.', flush=True)
    print('Cierra la ventana del juego para terminar. Evidencia: ' + str(out), flush=True)
    if args.prepare_only:
        return
    started = time.monotonic()
    outcomes, keeps, missing = Counter(), Counter(), {}
    first_pub = last_pub = None
    next_status = 5
    with (out / 'engine.log').open('w') as log, (out / 'presentation-times.jsonl').open('w') as timing:
        process = subprocess.Popen(command, cwd=data, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True)
        try:
            for line in process.stdout:
                elapsed = time.monotonic() - started
                log.write(line)
                log.flush()
                if 'SOLDIER_ORDERED_RESULT:' in line:
                    row = dict(s.split('=', 1) for s in line.split(': ', 1)[1].split())
                    outcomes[row['outcome']] += 1
                    if row['outcome'] == 'published':
                        first_pub = elapsed if first_pub is None else first_pub
                        last_pub = elapsed
                if 'SOLDIER_ORDERED_COMMAND:' in line:
                    row = dict(s.split('=', 1) for s in line.split(': ', 1)[1].split())
                    if row['decision'] == 'keep':
                        keeps[(row['type'], row['sheet'], row['frame'])] += 1
                    elif row['decision'] == 'missing' and row['key'] not in missing:
                        missing[row['key']] = dict(wall_seconds=elapsed, **row)
                if 'SOLDIER_ORDERED_RESULT:' in line or 'SOLDIER_HD_REASON:' in line:
                    timing.write(json.dumps(dict(wall_seconds=elapsed, record=line.strip())) + '\n')
                    timing.flush()
                if elapsed >= next_status:
                    print('t=%.0fs HD=%d retornos=%d' % (
                        elapsed, outcomes['published'], outcomes['missing-variant']), flush=True)
                    next_status = elapsed + 5
            process.wait()
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=10)
    info.update(returncode=process.returncode, wall_seconds=time.monotonic() - started,
                outcomes=dict(outcomes), first_publication_wall=first_pub,
                last_publication_wall=last_pub, missing_first_occurrences=list(missing.values()),
                kept_commands=[dict(type=k[0], sheet=k[1], frame=k[2], count=v)
                               for k, v in sorted(keeps.items())])
    (out / 'session.json').write_text(json.dumps(info, indent=2) + '\n')
    coverage = report([out / 'engine.log'])
    (out / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
    print(json.dumps({k: info[k] for k in ('returncode', 'wall_seconds', 'outcomes')}))


if __name__ == '__main__':
    main()
