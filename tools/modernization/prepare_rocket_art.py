"""Extend the exact walk/aim/grenade assets with reviewed retained rocket poses."""
import argparse
import base64
import hashlib
import json
from pathlib import Path

from prepare_grenade_art import prepare as prepare_previous
from prepare_walk_art_review import ROOT, derive_frame

CONFIG = ROOT / 'assets/modernization/soldier-rocket/manifest.json'


def prepare(out, c01, batch, asset):
    config = json.loads(CONFIG.read_text())
    directions = sorted({f['sheet'] - 0x39 for f in config['frames']})
    assert [(f['sheet'], f['frame']) for f in config['frames']] == [
        (0x39 + d, f) for d in directions for f in range(3)]
    for f in config['frames']:
        assert hashlib.sha256((ROOT / 'assets/modernization' / f['asset']).read_bytes()).hexdigest() == f['source_sha256']
    previous = prepare_previous(out, c01, batch, asset)
    manifest = json.loads((out / 'candidate-manifest.json').read_text())
    # Preserve every existing descriptor, file and binding; no prior pose regenerated differently.
    old_assets = json.loads(json.dumps(manifest['assets']))
    old_bindings = json.loads(json.dumps(manifest['bindings']))
    old_hashes = {a['file']: hashlib.sha256((out / a['file']).read_bytes()).hexdigest() for a in old_assets}
    for f in config['frames']:
        for density in (8, 12):
            descriptor, _ = derive_frame(out, f, density, c01, batch, asset)
            manifest['assets'].append(descriptor)
    for row in config['bindings']:
        assert row['animation'] == 0 and row['sheet'] - 0x39 in directions and row['frame'] in range(3)
        manifest['bindings'].append(dict(key=row['key'], decision='replace-art', assets={
            str(d): f"s{row['sheet']}-f{row['frame']}-{d}" for d in (8, 12)}))
    assert len(manifest['assets']) == 112 + 6 * len(directions)
    assert len(manifest['bindings']) == len({b['key'] for b in manifest['bindings']}) == 222 + 12 * len(directions)
    assert manifest['assets'][:112] == old_assets and manifest['bindings'][:222] == old_bindings
    assert all(hashlib.sha256((out / name).read_bytes()).hexdigest() == digest for name, digest in old_hashes.items())
    assert [f for f in config['frames'] if f['sheet'] == 64] == config['preserved_first_direction_frames']
    assert [r for r in config['bindings'] if r['sheet'] == 64] == config['preserved_first_direction_bindings']
    assert [a for a in manifest['assets'] if a['id'].startswith('s64-')] == config['preserved_first_direction_assets']
    (out / 'candidate-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    preview = {a['id']: base64.b64encode((out / (a['id'] + '.png')).read_bytes()).decode()
               for a in manifest['assets'] if int(a['id'].split('-')[0][1:]) in directions + [16 + d for d in directions] + [57 + d for d in directions]}
    html = '''<!doctype html><html lang="es"><meta charset="utf-8"><title>Lanzacohetes: direcciones 0, 1 y 7</title>
<style>body{background:#18251e;color:#eee;font:17px system-ui;padding:24px}img{width:288px;height:252px;background:#354638}button,select{font:inherit;margin:8px}section{display:flex;gap:12px;flex-wrap:wrap}</style>
<h1>Lanzacohetes · direcciones 0, 1 y 7 · revisión interna</h1><p>Tres frames conservados por el selector, sin ciclo de retroceso inventado. La prueba jugando y la cobertura completa de campaña siguen pendientes.</p>
<label>Dirección <select id="direction"><option>0</option><option>1</option><option>7</option></select></label><label>Frame retenido <select id="frame"><option>0</option><option>1</option><option>2</option></select></label><label>Densidad <select id="density"><option>12</option><option>8</option></select></label><button id="play">Pausar</button><button id="step">Paso</button><span id="label"></span><br><img id="body" alt="Transición marcha y lanzacohetes"><section id="poses"></section>
<p>Ritmo ilustrativo. El visor mantiene el frame de cohete, no anima 0–1–2. El motor conserva sus llamadas y relojes.</p>
<script>const images=IMAGES;let phase=0,run=true;function seq(){let f=Number(document.getElementById('frame').value);let d=Number(document.getElementById('direction').value);return [[d,0],[d,1],[d,2],[d,1],[d+16,0],[d,f],...Array.from({length:7},()=>[57+d,f]),[d,f],[d,0],[d,1],[d,2],[d,1]]}function paint(){let [s,f]=seq()[phase%seq().length],d=document.getElementById('density').value;document.getElementById('body').src='data:image/png;base64,'+images['s'+s+'-f'+f+'-'+d];document.getElementById('label').textContent='Hoja '+s+' · frame '+f;document.getElementById('poses').replaceChildren(...[0,1,2].map(f=>{let im=new Image;im.src='data:image/png;base64,'+images['s'+(57+Number(document.getElementById('direction').value))+'-f'+f+'-'+d];im.alt='Cohete frame '+f;return im}))}function next(){phase=(phase+1)%seq().length;paint()}for(let id of ['direction','frame','density'])document.getElementById(id).onchange=()=>{phase=0;paint()};document.getElementById('play').onclick=()=>run=!run;document.getElementById('step').onclick=next;setInterval(()=>{if(run)next()},180);paint();</script></html>'''
    (out / 'rocket-review.html').write_text(html.replace('IMAGES', json.dumps(preview)), encoding='utf-8')
    result = dict(status='PENDING campaign and Miguel in-game acceptance',
                  directions=directions, rocket_frames=len(config['frames']), assets=len(manifest['assets']),
                  bindings=len(manifest['bindings']), reconstructed_rocket_keys=len(config['bindings']),
                  previous_124_assets='verified separately against D0; original 112 and first rocket trio checked here', previous=previous,
                  manifest_sha256=hashlib.sha256((out / 'candidate-manifest.json').read_bytes()).hexdigest())
    (out / 'rocket-preparation.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('out', 'c01-builder', 'batch-builder', 'asset-builder'):
        parser.add_argument('--' + name, type=lambda x: Path(x).resolve(), required=True)
    a = parser.parse_args()
    r = prepare(a.out, a.c01_builder, a.batch_builder, a.asset_builder)
    print({k: v for k, v in r.items() if k != 'previous'})
