"""Extend the immutable walk/aim set with explicitly reviewed grenade poses."""
import argparse,base64,hashlib,json
from pathlib import Path
from prepare_aim_art import prepare as prepare_aim
from prepare_walk_art_review import ROOT,derive_frame,verify_masters
CONFIG=ROOT/'assets/modernization/soldier-grenade/manifest.json'
def prepare(out,c01,batch,asset):
 c=json.loads(CONFIG.read_text());directions=sorted({f['sheet']-8 for f in c['frames']})
 assert [(f['sheet'],f['frame']) for f in c['frames']]==[(d+8,f) for d in directions for f in range(3)]
 for f in c['frames']:verify_masters(f)
 previous=prepare_aim(out,c01,batch,asset);manifest=json.loads((out/'candidate-manifest.json').read_text())
 for f in c['frames']:
  for d in (8,12):descriptor,_=derive_frame(out,f,d,c01,batch,asset);manifest['assets'].append(descriptor)
 for r in c['bindings']:
  assert r['animation']==0 and r['sheet']-8 in directions and r['frame'] in range(3)
  manifest['bindings'].append(dict(key=r['key'],decision='replace-art',assets={str(d):f"s{r['sheet']}-f{r['frame']}-{d}" for d in (8,12)}))
 assert len(manifest['assets'])==64+6*len(directions)
 assert len(manifest['bindings'])==len({b['key'] for b in manifest['bindings']})==126+12*len(directions)
 (out/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 images={}
 for a in manifest['assets']:images[a['id']]=base64.b64encode((out/(a['id']+'.png')).read_bytes()).decode()
 html='''<!doctype html><html lang="es"><meta charset="utf-8"><title>Granadas y posturas</title><style>body{background:#18251e;color:#eee;font:17px system-ui;padding:24px}main{display:flex;flex-wrap:wrap;gap:12px}article{background:#354638;padding:12px}img{width:192px;height:168px}button,select{font:inherit;margin:8px}</style><h1>Marcha, reposo/apuntado y granada</h1><p>Revisión interna; aceptación visual pendiente. No sustituye una campaña completa. La granada arrojada la dibuja el motor por separado.</p><button id="play">Pausar</button><button id="next">Paso</button><select id="density"><option>12</option><option>8</option></select><span id="phase"></span><main id="cards"></main><p>Ritmo ilustrativo. Selección y ticks del juego intactos.</p><script>const images=IMAGES,directions=DIRECTIONS,sequence=[[0,0],[0,1],[0,2],[0,1],[0,1],[16,0],[0,0],[0,1],[0,2],[0,1],[8,0],[8,0],[8,1],[8,1],[8,2],[8,2],[0,1],[0,0],[0,1],[0,2],[0,1]];let phase=0,run=true;function paint(){let [offset,f]=sequence[phase],d=document.getElementById('density').value;document.getElementById('phase').textContent=phase+' · '+(offset===8?'granada '+f:offset===16?'apuntado':'marcha/reposo '+f);document.getElementById('cards').replaceChildren(...directions.map(s=>{let a=document.createElement('article'),p=document.createElement('p'),im=new Image;p.textContent='Dirección '+s;im.src='data:image/png;base64,'+images['s'+(s+offset)+'-f'+f+'-'+d];a.append(p,im);return a}));}function next(){phase=(phase+1)%sequence.length;paint()}document.getElementById('play').onclick=()=>run=!run;document.getElementById('next').onclick=next;document.getElementById('density').onchange=paint;setInterval(()=>{if(run)next()},180);paint();</script></html>'''
 (out/'review.html').write_text(html.replace('IMAGES',json.dumps(images)).replace('DIRECTIONS',json.dumps(directions)),encoding='utf-8')
 result=dict(status='PENDING full campaign and Miguel acceptance',directions=directions,grenade_frames=len(c['frames']),assets=len(manifest['assets']),bindings=len(manifest['bindings']),source_derived_grenade_keys=len(c['bindings']),previous=previous,manifest_sha256=hashlib.sha256((out/'candidate-manifest.json').read_bytes()).hexdigest())
 (out/'grenade-preparation.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for name in ('out','c01-builder','batch-builder','asset-builder'):p.add_argument('--'+name,type=lambda x:Path(x).resolve(),required=True)
 a=p.parse_args();r=prepare(a.out,a.c01_builder,a.batch_builder,a.asset_builder);print({k:v for k,v in r.items() if k!='previous'})
