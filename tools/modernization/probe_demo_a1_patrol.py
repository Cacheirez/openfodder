"""Bounded input-only A.1 patrol probe; uses an existing binary/public replay.

Copies the data directory and changes only mouse states/events in its replay.
Seeds, parameters, original video ticks, entities and game code remain intact.
The replay ends by its normal input-exhaustion guard, not mission victory.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

from ordered_soldier_coverage import report


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--route', choices=['idle', 'loop', 'west-loop', 'bounded-loop',
                                           'balanced-loop'], required=True)
    parser.add_argument('--classic', action='store_true')
    args = parser.parse_args()
    source, out = args.source.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    data = out / 'data'
    shutil.copytree(source / 'data', data)
    replay = data / 'Tests/Amiga The One/m1p2.ofd'
    original = json.loads(replay.read_text())
    modified = json.loads(replay.read_text())
    # Preserve the complete original presentation cadence (92.8 nominal s).
    # Only the user's available mouse input changes, never engine state.
    points = [(220, 100), (220, 55), (150, 55), (150, 100)]
    for state in modified['mStates']:
        tick = state['1']
        if args.route in ('west-loop', 'bounded-loop', 'balanced-loop') and tick <= 150:
            continue
        if args.route in ('west-loop', 'bounded-loop', 'balanced-loop'):
            points = ([(188, 100), (188, 55), (218, 55), (218, 100)]
                      if args.route == 'balanced-loop' else
                      [(180, 100), (180, 55), (210, 55), (210, 100)]
                      if args.route == 'bounded-loop' else
                      [(198, 100), (150, 100), (150, 55), (198, 55)])
            phase = max(0, tick - 151)
            x, y = points[(phase // 180) % len(points)]
            pressed = phase % 180 < 6
            if args.route in ('bounded-loop', 'balanced-loop') and not pressed:
                x, y = 100, 77
        else:
            x, y = points[max(0, (tick - 60) // 180) % len(points)]
            pressed = args.route == 'loop' and tick >= 60 and (tick - 60) % 180 < 6
        state.update({'2': x, '3': y, '4': int(pressed)})
    modified['mEvents'] = []
    assert all(modified[k] == original[k] for k in original
               if k not in ('mStates', 'mEvents'))
    replay.write_text(json.dumps(modified, separators=(',', ':')))
    traces = out / 'traces'
    traces.mkdir()
    manifest = source / 'art-complete/candidate-manifest.json'
    env = dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy',
               SDL_RENDER_DRIVER='software', OPENFODDER_PRESENT_MISSION_LAYERS='1',
               OPENFODDER_CAPTURE_SOLDIER='1', OPENFODDER_SOLDIER_HD='12',
               OPENFODDER_SOLDIER_BATCH='0', OPENFODDER_SOLDIER_ART='0',
               OPENFODDER_REPLACE_SOLDIER_POSE='0', OPENFODDER_HD_COMPARE='0',
               OPENFODDER_AUDIT_MISSION_LAYERS='0',
               OPENFODDER_MISSION_SCREEN_TRANSFORM='1', OPENFODDER_MISSION_SCREEN_FIT='1',
               OPENFODDER_SOLDIER_ORDERED_MANIFEST=str(manifest),
               OPENFODDER_ORDERED_COVERAGE='1', OPENFODDER_ORDERED_KEYS='1',
               OPENFODDER_NATIVE_WALK_OUT=str(out / 'snapshots'),
               OPENFODDER_HD_DIAGNOSTICS='1', OPENFODDER_TEST_FIRST_PHASE='1',
               OPENFODDER_TEST_MISSION_PAUSE='0', OPENFODDER_TRACE_DIR=str(traces))
    env.pop('OPENFODDER_TEST_MISSION_PRESENTATIONS', None)
    if args.classic:
        env['OPENFODDER_SOLDIER_HD'] = '0'
    command = [str(data / 'openfodder.exe'), '--appveyor', '--unit-test',
               '--nosound', '--window', '--alternate-mouse', '--campaign',
               'Amiga The One', '--mission', '1', '--phase', '2']
    started = time.monotonic()
    with (out / 'engine.log').open('w') as log, (out / 'presentation-times.jsonl').open('w') as timing:
        process = subprocess.Popen(command, cwd=data, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True)
        try:
            for line in process.stdout:
                elapsed = time.monotonic() - started
                log.write(line)
                if 'SOLDIER_ORDERED_RESULT:' in line or 'SOLDIER_HD_REASON:' in line:
                    timing.write(json.dumps(dict(wall_seconds=elapsed, record=line.strip())) + '\n')
                if elapsed > 180:
                    raise TimeoutError('probe exceeded 180 seconds')
            process.wait(timeout=10)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
    wall = time.monotonic() - started
    coverage = report([out / 'engine.log'])
    (out / 'coverage.json').write_text(json.dumps(coverage, indent=2))
    samples = []
    for line in (traces / 'Amiga_The_One_m1_p2.jsonl').open():
        row = json.loads(line)
        if row['kind'] == 'tick':
            samples.append(row)
    enemies = [r for r in samples if any(s['type'] == 5 and s['was_drawn']
                                        for s in r['state']['sprites'])]
    summary = dict(route=args.route, classic=args.classic, command=command, returncode=process.returncode,
                   wall_seconds=round(wall, 3), samples=len(samples),
                   demo_ticks=[samples[0]['state']['game']['demo_tick'],
                               samples[-1]['state']['game']['demo_tick']],
                   first_enemy_demo_tick=(enemies[0]['state']['game']['demo_tick']
                                          if enemies else None),
                   live_players=dict(Counter(sum(s['type'] == 0 for s in r['state']['sprites'])
                                             for r in samples)),
                   exe_sha256=sha(data / 'openfodder.exe'),
                   manifest_sha256=sha(manifest), input_sha256=sha(replay),
                   original_input_sha256=sha(source / 'data/Tests/Amiga The One/m1p2.ofd'),
                   preserved_fields=[k for k in original if k not in ('mStates', 'mEvents')],
                   **{k: coverage[k] for k in ('attempts', 'outcomes',
                      'published_command_presentations', 'unresolved_commands')})
    (out / 'run.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
