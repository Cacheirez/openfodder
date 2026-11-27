"""Self-contained canvas review using the exact compiled 12x derivative pixels."""
import argparse,base64,json,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--headers',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();frames={}
for s in (2,7):
 for f in range(3):
  name='c01_12.hpp' if(s,f)==(7,0) else f'pilot_{s}_{f}_12.hpp'
  values=[int(x) for x in re.findall(r'(\d+)u', (a.headers/name).read_text())];assert len(values)==224*144
  raw=bytes(v for c in values for v in ((c>>16)&255,(c>>8)&255,c&255,c>>24))
  frames[f'{s}/{f}']=base64.b64encode(raw).decode()
html='''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Lote animado C01</title>
<style>body{background:#172420;color:#eee;font:17px system-ui;max-width:1000px;margin:30px auto;padding:20px}canvas{background:#354638;border:1px solid #70816a;width:384px;max-width:100%;image-rendering:auto}button,input{font:inherit;margin:12px}section{display:flex;flex-wrap:wrap;gap:24px}p{line-height:1.5}small{color:#b6c5bb}</style>
<h1>Lote animado · dos orientaciones</h1><p>Derivados exactos de 12×. Revisión aislada del ciclo 0–1–2–1; el juego conserva sus propios contadores. La velocidad de este visor es solo de revisión.</p>
<button id="pause">Pausar</button><label>Milisegundos por pose <input id="speed" type="range" min="80" max="400" value="180"></label><span id="pose"></span>
<section><div><h2>Hoja 2 · izquierda</h2><canvas id="left" width="192" height="168"></canvas></div><div><h2>Hoja 7 · diagonal</h2><canvas id="right" width="192" height="168"></canvas></div></section>
<p><small>Comprobar alternancia de piernas, estabilidad de casco/cuerpo y apoyo. C01 (7/0) permanece intacto. Son seis claves de un solo soldado; las demás vuelven al clásico. No es una prueba de rendimiento ni una captura de la fase.</small></p>
<script>
const frames=FRAMES;
const sequence=[0,1,2,1];let step=0,running=true,last=0;
function draw(key,canvas){const bytes=Uint8ClampedArray.from(atob(frames[key]),c=>c.charCodeAt(0));canvas.getContext('2d').putImageData(new ImageData(bytes,192,168),0,0);}
function paint(){const f=sequence[step];draw('2/'+f,document.getElementById('left'));draw('7/'+f,document.getElementById('right'));document.getElementById('pose').textContent='Pose '+f;}
document.getElementById('pause').onclick=()=>{running=!running;document.getElementById('pause').textContent=running?'Pausar':'Reanudar';};
function tick(t){if(running&&t-last>=Number(document.getElementById('speed').value)){step=(step+1)%4;paint();last=t;}requestAnimationFrame(tick);}paint();requestAnimationFrame(tick);
</script></html>'''.replace('FRAMES',json.dumps(frames,separators=(',',':')))
a.out.write_text(html)
