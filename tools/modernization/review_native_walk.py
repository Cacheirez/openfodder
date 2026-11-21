"""Verify real native walk snapshots and compare them with the current HD cycle.
GPL-3.0-or-later. Output contains original artwork: keep the output local.
Only public-report.json and a compressed diagnostic log are suitable as evidence.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
from ordered_soldier_coverage import report
from prepare_walk_art_review import png

ROOT = Path(__file__).resolve().parents[2]


def review(snapshots, art, renderer, window_exe, out):
    config = json.loads((ROOT/'assets/modernization/soldier-walk-review/review.json').read_text())
    out.mkdir(parents=True, exist_ok=False)
    rows = {}
    rendered = []
    pictures = {}
    for source in sorted(snapshots.glob('*.json')):
        row = json.loads(source.read_text())
        key = row['key']
        if source.name != key+'.json' or key in rows:
            raise ValueError('snapshot identity/duplicate')
        rgba_path = out/(key+'.rgba')
        result = json.loads(subprocess.check_output([str(renderer), str(source), str(snapshots), str(rgba_path)], text=True))
        rgba = rgba_path.read_bytes()
        if hashlib.sha256(rgba).hexdigest() != result['rgba_sha256']:
            raise ValueError('native raster output hash')
        pictures[key] = base64.b64encode(png(result['width'], result['height'], rgba)).decode()
        rows[key] = row
        rendered.append(dict(**result, animation=row['animation'], person=row['person'],
            palette_sha256=hashlib.sha256(json.dumps(row['colors'], separators=(',', ':')).encode()).hexdigest()))
    # Require the actual 24 ordinary walk keys per platform, independent of HD coverage.
    for platform in (0, 1):
        keys = {(r['sheet'], r['frame']) for r in rendered if r['format'] == platform and r['animation'] == 0}
        if keys != {(s, f) for s in range(8) for f in range(3)}:
            raise ValueError('native walk coverage incomplete for platform '+str(platform))
    chosen = [rows[b['key']] for b in config['bindings']]
    if len(chosen) != 13 or sum(r['animation'] == 0 for r in chosen) != 12:
        raise ValueError('candidate set changed: inspect state classification')
    if [r['animation'] for r in chosen if r['animation'] != 0] != [0x32]:
        raise ValueError('unexpected non-walk state')
    native_input = dict(manifest=str(art/'candidate-manifest.json'), snapshots=str(snapshots), rows=chosen)
    (out/'native-input.json').write_text(json.dumps(native_input, indent=2)+'\n')
    log = out/'window.log'
    with log.open('w') as stream:
        subprocess.run([str(window_exe)], env={**os.environ, 'OPENFODDER_ORDERED_COVERAGE': '1',
            'OPENFODDER_WALK_NATIVE_REVIEW': str(out)}, cwd=out, stdout=stream,
            stderr=subprocess.STDOUT, check=True, timeout=120)
    census = report([log])
    assert census['outcomes'] == {'published': 34}, census
    assert census['published_command_presentations'] == 68, census
    assert census['unresolved_commands'] == 0 and len(census['variants']) == 26, census
    assert 'PASS native walk:' in log.read_text()
    public = dict(schema=1, status='PASS native reconstruction and bounded real-key SDL; artistic acceptance PENDING',
        native_snapshots=len(rows), native_walk_keys_per_platform=24, native_rasters=rendered,
        candidate_keys_reproduced=[r['key'] for r in chosen], ordinary_walk_bindings=12,
        additional_state=dict(animation=0x32, name='Slide1', key=next(r['key'] for r in chosen if r['animation'])),
        cycles='four real-resource/palette groups, native 0-1-2-1; no synthetic rebinding',
        actual_sdl_intervals=34, published_bodies=68, variant_density_entries=26,
        c01='byte-identical 8x/12x in actual real-key SDL fixture',
        log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),
        limitations=['Only direction 7 has three current review derivatives', 'Other 21 artistic walk keys pending',
            'Remaining states/enemies/transitions pending', 'This isolated scene is not full campaign HD coverage',
            'GPU/CD32 and user artistic acceptance pending'],
        privacy='Original resource bytes, native rasters, palette snapshots and comparison HTML remain local')
    (out/'public-report.json').write_text(json.dumps(public, indent=2)+'\n')
    cards = []
    for r in sorted(rendered, key=lambda r: (r['format'], r['resource_sha256'], r['animation'], r['sheet'], r['frame'])):
        modern = ''
        if r['sheet'] == 7:
            modern = '<img class="hd" alt="HD candidato" src="data:image/png;base64,'+base64.b64encode((art/f"s7-f{r['frame']}-12.png").read_bytes()).decode()+'">'
        cards.append('<article><p>'+('PC' if r['format'] == 0 else 'Amiga')+f" · {r['sheet']}/{r['frame']} · anim {r['animation']} · "+r['resource_sha256'][:8]+'</p><img alt="Nativo real" src="data:image/png;base64,'+pictures[r['key']]+'">'+modern+'<small>'+r['key']+'</small></article>')
    (out/'native-comparison.html').write_text('''<!doctype html><html lang="es"><meta charset="utf-8"><title>Contraste nativo real</title>
<style>body{font:16px system-ui;background:#18251e;color:#eee;padding:24px}main{display:flex;flex-wrap:wrap;gap:12px}article{background:#354638;padding:12px;width:420px}img{width:192px;height:168px;image-rendering:pixelated}.hd{image-rendering:auto}small{display:block;overflow-wrap:anywhere}</style>
<h1>Contraste con recursos y paletas reales</h1><p>Uso local: contiene gráficos originales. Todas las claves verificadas contra sus bytes; animación 50 es Slide1, no marcha ordinaria. HD de dirección 7 provisional; resto del arte pendiente. No equivale a campaña completa ni a aceptación del usuario.</p><main>'''+''.join(cards)+'</main></html>')
    print(json.dumps({k: public[k] for k in ('status', 'native_snapshots', 'actual_sdl_intervals', 'published_bodies')}))
    return public


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('snapshots', 'art', 'renderer', 'window-exe', 'out'):
        parser.add_argument('--'+name, type=lambda s: Path(s).resolve(), required=True)
    args = parser.parse_args()
    review(args.snapshots, args.art, args.renderer, args.window_exe, args.out)
