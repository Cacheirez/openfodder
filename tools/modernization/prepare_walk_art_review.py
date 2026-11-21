"""Prepare an internal art cycle using existing exact builders; never enable it in game.
GPL-3.0-or-later. Observed bindings remain candidates, not resource/visual approval.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import zlib

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT/'assets/modernization/soldier-walk-review/review.json'


def png(width, height, rgba):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind+data))
    scan = b''.join(b'\0'+rgba[y*width*4:(y+1)*width*4] for y in range(height))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(scan)) + chunk(b'IEND', b''))


def verify_masters(frame):
    for master in (frame, frame.get('uniform_a')):
        if master is None:
            continue
        source = ROOT/'assets/modernization'/master['asset']
        if hashlib.sha256(source.read_bytes()).hexdigest() != master['source_sha256']:
            raise ValueError(f'master hash mismatch: {source}')


def derive_frame(out, frame, density, c01_builder, batch_builder, asset_builder):
    """Shared exact derivative/export path for diagonal and full walking sets."""
    sheet, f = frame['sheet'], frame['frame']
    name = f's{sheet}-f{f}-{density}'
    header = out/(name+'.hpp')
    uniform = frame.get('uniform_a')
    source = ROOT/'assets/modernization'/(uniform or frame)['asset']
    if (sheet, f) == (7, 0):
        command = [c01_builder, source, header, density]
    else:
        command = [batch_builder, source, header, density, 'WalkReview', *frame['crop'], *frame['placement']]
    subprocess.run(list(map(str, command)), check=True)
    pixels = [int(v) for v in re.findall(r'(\d+)u', header.read_text())]
    if len(pixels) != 16*14*density*density:
        raise ValueError('unexpected derivative geometry')
    rgba = bytes(v for c in pixels for v in ((c >> 16) & 255, (c >> 8) & 255, c & 255, c >> 24))
    image = png(16*density, 14*density, rgba)
    image_path = out/(name+'.png')
    image_path.write_bytes(image)
    descriptor = json.loads(subprocess.check_output(list(map(str, [asset_builder, image_path,
        out/(name+'.rgba'), name, 16, 14, density])), text=True))
    if (out/descriptor['file']).read_bytes() != rgba:
        raise ValueError('export changed derivative bytes')
    if uniform and descriptor['sha256'] != uniform['rgba_sha256'][str(density)]:
        raise ValueError(f'option A RGBA hash mismatch: {name}')
    return descriptor, image


def prepare(out, c01_builder, batch_builder, asset_builder):
    config = json.loads(CONFIG.read_text())
    # Preflight all originals before producing anything. No changed master is silently accepted.
    for frame in config['frames']:
        source = ROOT/'assets/modernization'/frame['asset']
        if hashlib.sha256(source.read_bytes()).hexdigest() != frame['source_sha256']:
            raise ValueError('source hash mismatch: '+str(source))
    if hashlib.sha256((ROOT/config['variant_source']).read_bytes()).hexdigest() != config['variant_source_sha256']:
        raise ValueError('variant census changed; review explicit candidate keys')
    out.mkdir(parents=True, exist_ok=False)
    manifest = dict(version=2, assets=[], bindings=[])
    preview = {}
    for frame in config['frames']:
        for density in (8, 12):
            f = frame['frame']
            descriptor, image = derive_frame(out, frame, density, c01_builder, batch_builder, asset_builder)
            manifest['assets'].append(descriptor)
            preview[str(f)+'/'+str(density)] = base64.b64encode(image).decode()
    for row in config['bindings']:
        manifest['bindings'].append(dict(key=row['key'], decision='replace-art',
            assets={str(d): f"s7-f{row['frame']}-{d}" for d in (8, 12)}))
    (out/'candidate-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    report = dict(status='PENDING', scope='direction 7 only, three art keys, not full soldier coverage',
        source_config_sha256=hashlib.sha256(CONFIG.read_bytes()).hexdigest(),
        source_frames=config['frames'], candidate_bindings=config['bindings'], assets=manifest['assets'],
        sequence=config['sequence'], native_anchor=[0, 14],
        vertical_source_extent=850, previous_f2_vertical_source_extent=942,
        c01='original builder and source unchanged; exact derivative bytes retained',
        limitations=config['acceptance'])
    (out/'preparation.json').write_text(json.dumps(report, indent=2)+'\n')
    html = '''<!doctype html><html lang="es"><meta charset="utf-8"><title>Revisión interna · dirección 7</title>
<style>body{font:18px system-ui;background:#18251e;color:#eee;max-width:900px;margin:32px auto;padding:20px}img{width:384px;background:#354638}button,select{font:inherit;margin:8px}section{display:flex;gap:12px;flex-wrap:wrap}section img{width:192px}</style>
<h1>Dirección 7 · revisión interna pendiente</h1><p>C01 intacto. Pose 1 provisional; pose 2 candidata corregida. No acredita las 24 claves, variantes de campaña ni aceptación visual.</p>
<button id="play">Pausar</button><button id="step">Paso</button><label>Densidad <select id="density"><option>12</option><option>8</option></select></label><span id="label"></span><br><img id="cycle" alt="Ciclo diagonal candidato">
<section id="poses"></section><p>Ciclo ilustrativo 0–1–2–1 a 180 ms por pose. El motor conserva los contadores originales. La galería no sustituye un recorrido del juego.</p>
<script>const images=IMAGES,sequence=[0,1,2,1];let index=0,running=true;
function paint(){let d=document.getElementById('density').value;document.getElementById('cycle').src='data:image/png;base64,'+images[sequence[index]+'/'+d];document.getElementById('label').textContent='Frame '+sequence[index];document.getElementById('poses').replaceChildren(...[0,1,2].map(f=>{let im=new Image;im.src='data:image/png;base64,'+images[f+'/'+d];im.alt='Frame '+f;return im;}));}
document.getElementById('play').onclick=()=>{running=!running;document.getElementById('play').textContent=running?'Pausar':'Reanudar';};document.getElementById('step').onclick=()=>{index=(index+1)%4;paint();};document.getElementById('density').onchange=paint;setInterval(()=>{if(running){index=(index+1)%4;paint();}},180);paint();</script></html>'''
    (out/'review.html').write_text(html.replace('IMAGES', json.dumps(preview)))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('out', 'c01-builder', 'batch-builder', 'asset-builder'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    result = prepare(args.out.resolve(), args.c01_builder.resolve(), args.batch_builder.resolve(), args.asset_builder.resolve())
    print(json.dumps(dict(status=result['status'], assets=len(result['assets']), candidate_bindings=len(result['candidate_bindings']))))


if __name__ == '__main__':
    main()
