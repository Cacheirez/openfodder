"""Check native selected/retained rocket bodies in real WindowHD/SDL publication."""
import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

from ordered_soldier_coverage import report
from prepare_rocket_art import CONFIG, prepare
from prepare_grenade_art import CONFIG as GRENADE_CONFIG
from prepare_aim_art import CONFIG as AIM_CONFIG
from prepare_walk24 import CONFIG as WALK_CONFIG


def check(a, out):
    preparation = prepare(out / 'art', a.c01_builder, a.batch_builder, a.asset_builder)
    selector = json.loads(subprocess.check_output([str(a.selector_exe)], text=True))
    assert selector['sample_count'] == len(selector['samples']) == 576
    assert selector['assertions'] == 2703
    directions = preparation['directions']
    sequences = []
    for direction in directions:
        for route in ('direct', 'mouse-retained', 'target-retained'):
            for start in range(3):
                rocket = [r for r in selector['samples'] if r['direction'] == direction
                          and r['route'] == route and r['initial_frame'] == start]
                assert len(rocket) == 8 and [r['call'] for r in rocket] == list(range(8))
                walk = [dict(sheet=direction, frame=f) for f in (0, 1, 2, 1)]
                # Prefix/suffix reuse already verified walk/aim families. Rocket/return rows
                # come from actual extracted native functions, never an invented 0-1-2 cycle.
                prefix = walk + [dict(sheet=16 + direction, frame=0)] + walk + [dict(sheet=direction, frame=start)]
                rows = prefix + rocket + walk
                assert len(rows) == 22
                sequences.append(dict(direction=direction, route=route, initial_frame=start, rows=rows))
    native = bool(a.native_rocket)
    rows = []
    if native:
        for config, folder in ((CONFIG, a.native_rocket), (GRENADE_CONFIG, a.native_grenade), (AIM_CONFIG, a.native_aim)):
            assert folder, 'all native body families required'
            for binding in json.loads(config.read_text())['bindings']:
                p = folder / (binding['key'] + '.json')
                rows.append(dict(row=json.loads(p.read_text()), directory=str(folder)))
        for binding in json.loads(WALK_CONFIG.read_text())['bindings']:
            candidates = [p / (binding['key'] + '.json') for p in a.native_walk]
            candidates = [p for p in candidates if p.exists()]
            canonical = lambda p: json.dumps({k: v for k, v in json.loads(p.read_text()).items()
                                             if k not in ('direction', 'face', 'tick')}, sort_keys=True)
            assert candidates and len({canonical(p) for p in candidates}) == 1
            p = candidates[0]
            rows.append(dict(row=json.loads(p.read_text()), directory=str(p.parent)))
        assert len(rows) == preparation['bindings']
    # All four native groups have direction-0/1/2/3/4/7 walk keys. The two missing Amiga
    # direction-6 keys remain excluded, never manufactured as observations.
    assert directions == [0, 1, 2, 3, 4, 7], 'this microblock covers only directions 0, 1, 2, 3, 4 and 7'
    expected = len(sequences) * 22 * 4 * 2
    (out / 'art/transition-input.json').write_text(json.dumps(dict(
        native=native, rows=rows, directions=directions, sequences=sequences,
        sequence_length=22, other_choice_offset=10, expected_intervals=expected,
        assets=preparation['assets'], bindings=preparation['bindings'])))
    # D1 CI reached the fixed 240 s watchdog under ASan/UBSan.
    # Keep a finite watchdog, scaled to the number of presentations checked.
    timeout_seconds = max(240, expected // 8)
    log = out / 'window.log'
    with log.open('w') as f:
        subprocess.run([str(a.exe)], cwd=out, env={**os.environ,
                       'OPENFODDER_ROCKET_ART': str(out / 'art'), 'OPENFODDER_ORDERED_COVERAGE': '1'},
                       stdout=f, stderr=subprocess.STDOUT, check=True, timeout=timeout_seconds)
    census = report([log])
    assert census['outcomes'] == {'published': expected, 'missing-variant': 3}, census
    assert census['published_command_presentations'] == expected * 2 and census['verdict'] == 'PENDING'
    assert 'PASS rocket transition' in log.read_text()
    result = dict(status='PASS bounded directions 0, 1, 2, 3, 4 and 7; other directions/campaign/acceptance PENDING',
                  mode='source-reconstructed real resources' if native else 'controlled metadata and test-only keys',
                  directions=directions, intervals=expected, bodies=expected * 2,
                  sequences=expected // 22, densities=[8, 12], timeout_seconds=timeout_seconds, selector_assertions=2703,
                  selector_samples=576, three_rejections=True, c01='exact',
                  log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(), preparation=preparation,
                  limits=['geometry stubbed in selector fixture', 'prefix/suffix reuse prior walk/aim checks',
                          'reconstructed keys are not replay observations',
                          'CPU compositor reused as SDL expectation; no independent anatomical oracle',
                          'not full player handler, campaign, GPU/CD32, projectile or user in-game acceptance'])
    (out / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print({k: v for k, v in result.items() if k != 'preparation'})
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('exe', 'selector-exe', 'c01-builder', 'batch-builder', 'asset-builder'):
        parser.add_argument('--' + name, type=lambda x: Path(x).resolve(), required=True)
    for name in ('native-rocket', 'native-grenade', 'native-aim', 'out'):
        parser.add_argument('--' + name, type=lambda x: Path(x).resolve())
    parser.add_argument('--native-walk', type=lambda x: Path(x).resolve(), action='append', default=[])
    a = parser.parse_args()
    if a.out:
        a.out.mkdir(parents=True, exist_ok=False)
        check(a, a.out)
    else:
        with tempfile.TemporaryDirectory(prefix='rocket-art-') as tmp:
            check(a, Path(tmp))
