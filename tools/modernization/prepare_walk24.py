"""Prepare the reviewed 24-key player walk, using the existing exact builders.
GPL-3.0-or-later. Not complete soldiers; no launcher or gameplay changes.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
from prepare_walk_art_review import ROOT, derive_frame

CONFIG = ROOT/'assets/modernization/soldier-walk24/manifest.json'


def prepare(out, c01_builder, batch_builder, asset_builder):
    config = json.loads(CONFIG.read_text())
    assert [(f['sheet'], f['frame']) for f in config['frames']] == [(s, f) for s in range(8) for f in range(3)]
    assert config['sequence'] == [0, 1, 2, 1]
    for frame in config['frames']:
        source = ROOT/'assets/modernization'/frame['asset']
        if hashlib.sha256(source.read_bytes()).hexdigest() != frame['source_sha256']:
            raise ValueError('master hash mismatch: '+str(source))
    if hashlib.sha256((ROOT/config['native_evidence']).read_bytes()).hexdigest() != config['native_evidence_sha256']:
        raise ValueError('native evidence changed; inspect bindings')
    assert len(config['bindings']) == len({b['key'] for b in config['bindings']}) == 94
    assert all(b['animation'] == 0 for b in config['bindings'])
    # One source scale per cycle; poses may translate to keep foot/helmet anchors.
    for sheet in range(7):
        frames = config['frames'][sheet*3:sheet*3+3]
        assert len({(f['crop'][2]-f['crop'][0], f['crop'][3]-f['crop'][1], tuple(f['placement'])) for f in frames}) == 1
    out.mkdir(parents=True, exist_ok=False)
    manifest = dict(version=2, assets=[], bindings=[])
    pictures = {}
    for frame in config['frames']:
        for density in (8, 12):
            descriptor, image = derive_frame(out, frame, density, c01_builder, batch_builder, asset_builder)
            manifest['assets'].append(descriptor)
            pictures[f"{frame['sheet']}/{frame['frame']}/{density}"] = base64.b64encode(image).decode()
    for b in config['bindings']:
        manifest['bindings'].append(dict(key=b['key'], decision='replace-art',
            assets={str(d): f"s{b['sheet']}-f{b['frame']}-{d}" for d in (8, 12)}))
    (out/'candidate-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    result = dict(status='PENDING user artistic acceptance and full soldier coverage', frames=24,
        assets=manifest['assets'], observed_native_bindings=94, unobserved=config['unobserved'],
        source_manifest_sha256=hashlib.sha256(CONFIG.read_bytes()).hexdigest(),
        scope=config['scope'], no_clock_changes=True, c01='original source and builder unchanged')
    (out/'preparation.json').write_text(json.dumps(result, indent=2)+'\n')
    html = '''<!doctype html><html lang="es"><meta charset="utf-8"><title>Marcha · ocho direcciones</title>
<style>body{font:17px system-ui;background:#18251e;color:#eee;padding:24px}button,select{font:inherit;margin:8px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}article{background:#354638;padding:12px}img{width:192px;height:168px}small{display:block}</style>
<h1>Marcha del jugador · 24 claves</h1><p>Revisión interna. C01 intacto; nuevas poses pendientes de aceptación artística. No incluye otros estados ni enemigos. No demuestra una campaña completa sin retornos al clásico.</p>
<button id="play">Pausar</button><button id="step">Paso</button><label>Densidad <select id="density"><option>12</option><option>8</option></select></label><label><input id="turn" type="checkbox">Giro continuo</label><span id="label"></span><main id="gallery"></main>
<p>Secuencia ilustrativa 0–1–2–1 a 180 ms por pose; el motor conserva sus contadores originales. Cambiar dirección no cambia el tamaño lógico.</p>
<script>const images=IMAGES,sequence=[0,1,2,1],names=['Delante','Delante / izquierda','Izquierda','Izquierda / atrás','Atrás','Atrás / derecha','Derecha','Derecha / delante'];let step=0,running=true,direction=0;
function paint(){let d=document.getElementById('density').value,turn=document.getElementById('turn').checked;document.getElementById('label').textContent='Frame '+sequence[step]+(turn?' · '+names[direction]:'');let rows=turn?[direction]:[0,1,2,3,4,5,6,7];document.getElementById('gallery').replaceChildren(...rows.map(s=>{let a=document.createElement('article'),t=document.createElement('p'),im=new Image;t.textContent=s+' · '+names[s];im.src='data:image/png;base64,'+images[s+'/'+sequence[step]+'/'+d];im.alt=t.textContent;a.append(t,im);return a;}));}
function next(){step=(step+1)%4;if(step===0)direction=(direction+1)%8;paint();}document.getElementById('play').onclick=()=>{running=!running;document.getElementById('play').textContent=running?'Pausar':'Reanudar';};document.getElementById('step').onclick=next;document.getElementById('density').onchange=paint;document.getElementById('turn').onchange=paint;setInterval(()=>{if(running)next();},180);paint();</script></html>'''
    (out/'review.html').write_text(html.replace('IMAGES', json.dumps(pictures)))
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('out', 'c01-builder', 'batch-builder', 'asset-builder'):
        p.add_argument('--'+name, type=lambda s: Path(s).resolve(), required=True)
    a = p.parse_args()
    print(json.dumps(prepare(a.out, a.c01_builder, a.batch_builder, a.asset_builder)))
