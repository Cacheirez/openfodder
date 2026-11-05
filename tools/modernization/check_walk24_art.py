"""Verify full walking art through actual Window/SDL, with explicit source scope."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from ordered_soldier_coverage import report
from prepare_walk24 import prepare, CONFIG


def check(args, out):
    preparation = prepare(out/'art', args.c01_builder, args.batch_builder, args.asset_builder)
    env = {**os.environ, 'OPENFODDER_ORDERED_COVERAGE': '1', 'OPENFODDER_WALK24_ART': str(out/'art')}
    native = bool(args.native_snapshots)
    if native:
        config = json.loads(CONFIG.read_text())
        rows = [json.loads((args.native_snapshots/(b['key']+'.json')).read_text()) for b in config['bindings']]
        assert all(row['animation'] == 0 for row in rows) and len(rows) == 94
        input_path = out/'native-input.json'
        input_path.write_text(json.dumps(dict(snapshots=str(args.native_snapshots), rows=rows)))
        env['OPENFODDER_WALK24_NATIVE_INPUT'] = str(input_path)
    else:
        env.pop('OPENFODDER_WALK24_NATIVE_INPUT', None)
    log = out/'window.log'
    with log.open('w') as stream:
        subprocess.run([str(args.exe)], cwd=out, env=env, stdout=stream,
                       stderr=subprocess.STDOUT, check=True, timeout=180)
    census = report([log])
    published, variants = (236, 188) if native else (256, 192)
    assert census['outcomes'] == {'published': published, 'missing-variant': 3}, census
    assert census['published_command_presentations'] == published*2, census
    assert len([r for r in census['variants'] if r.get('published_presentations')]) == variants, census
    assert census['verdict'] == 'PENDING'
    assert ('PASS walk24 '+('real' if native else 'controlled')) in log.read_text()
    result = dict(status='PASS isolated artistic walk; full soldiers and visual acceptance PENDING',
        mode='real unmodified native keys' if native else 'controlled keys explicitly rebound',
        artistic_keys=24, rgba_assets=48, published_intervals=published, published_bodies=published*2,
        published_variant_density_entries=variants, scope_rejections=3,
        c01='byte-identical 8x/12x', log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),
        preparation=preparation, pending=['two unobserved Amiga ordinary keys', 'other states/enemies',
            'campaign-wide HD without normal fallback', 'transitions/GPU/CD32', 'user visual acceptance'])
    (out/'validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'preparation'}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('exe', 'c01-builder', 'batch-builder', 'asset-builder'):
        p.add_argument('--'+name, type=lambda s: Path(s).resolve(), required=True)
    p.add_argument('--native-snapshots', type=lambda s: Path(s).resolve())
    p.add_argument('--out', type=lambda s: Path(s).resolve())
    a = p.parse_args()
    if a.out:
        a.out.mkdir(parents=True, exist_ok=False)
        check(a, a.out)
    else:
        with tempfile.TemporaryDirectory(prefix='walk24-') as tmp:
            check(a, Path(tmp))
