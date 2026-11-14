"""Prepare actual art and check its continuous controlled Window/SDL publication."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
from ordered_soldier_coverage import report
from prepare_walk_art_review import prepare


def check(args, out):
    prepared = prepare(out/'art', args.c01_builder, args.batch_builder, args.asset_builder)
    log = out/'window.log'
    with log.open('w') as stream:
        subprocess.run([str(args.exe)], cwd=out,
            env={**os.environ, 'OPENFODDER_ORDERED_COVERAGE': '1',
                 'OPENFODDER_WALK_ART_REVIEW': str(out/'art')},
            stdout=stream, stderr=subprocess.STDOUT, check=True, timeout=120)
    census = report([log])
    assert census['outcomes'] == {'published': 32}, census
    assert census['published_command_presentations'] == 64, census
    assert census['unique_producer_commands'] == 64, census
    assert census['unresolved_commands'] == 0, census
    assert len(census['variants']) == 24, census
    assert census['verdict'] == 'PENDING', census
    assert 'PASS real walk art:' in log.read_text()
    result = dict(status='PASS controlled publication; visual/campaign acceptance PENDING',
        preparation=prepared, outcomes=census['outcomes'], published_bodies=64,
        controlled_variant_density_entries=24, c01_byte_comparison='PASS 8x/12x',
        scope='3 keys direction 7; controlled PC/Amiga resources, two person/palette variants, water/occlusion',
        campaign_bindings='13 explicit observed candidates prepared, NOT exercised by controlled fixture',
        pending=['other 21 walk keys', 'native pose correspondence', 'campaign resource/palette review',
                 'other states/enemies/transitions', 'GPU/CD32', 'user visual acceptance'])
    (out/'validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'preparation'}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('exe', 'c01-builder', 'batch-builder', 'asset-builder'):
        parser.add_argument('--'+name, type=lambda s: Path(s).resolve(), required=True)
    parser.add_argument('--out', type=lambda s: Path(s).resolve())
    args = parser.parse_args()
    if args.out:
        args.out.mkdir(parents=True, exist_ok=False)
        check(args, args.out)
    else:
        with tempfile.TemporaryDirectory(prefix='walk-art-') as tmp:
            check(args, Path(tmp))


if __name__ == '__main__':
    main()
