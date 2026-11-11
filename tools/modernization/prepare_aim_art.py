"""Prepare aim derivatives and merge unchanged walking assets; no launcher changes."""
import argparse,base64,hashlib,json
from pathlib import Path
from prepare_walk24 import prepare as prepare_walk
from prepare_walk_art_review import ROOT,derive_frame,verify_masters
CONFIG=ROOT/'assets/modernization/soldier-aim/manifest.json'
def prepare(out,c01,batch,asset):
 config=json.loads(CONFIG.read_text());assert len(config['frames'])==8
 for frame in config['frames']:
  verify_masters(frame)
 assert [f['sheet'] for f in config['frames']]==list(range(16,24))
 walk=prepare_walk(out,c01,batch,asset);manifest=json.loads((out/'candidate-manifest.json').read_text());images={}
 for frame in config['frames']:
  for d in (8,12):
   descriptor,picture=derive_frame(out,frame,d,c01,batch,asset)
   rgba=(out/descriptor['file']).read_bytes();top=(14-frame['placement'][2])*d
   assert not any(rgba[:16*d*top*4]) and any(rgba[3::4]), 'aim height/anchor lost'
   manifest['assets'].append(descriptor);images[f"{frame['sheet']}/0/{d}"]=base64.b64encode(picture).decode()
 for row in config['bindings']:
  assert row['animation']==0 and row['sheet'] in range(16,24) and row['frame']==0
  manifest['bindings'].append(dict(key=row['key'],decision='replace-art',assets={str(d):f"s{row['sheet']}-f0-{d}" for d in (8,12)}))
 assert len(manifest['assets'])==64 and len(manifest['bindings'])==len({b['key'] for b in manifest['bindings']})==126
 (out/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 for sheet in range(8):
  for f in range(3):
   for d in (8,12):images[f'{sheet}/{f}/{d}']=base64.b64encode((out/f's{sheet}-f{f}-{d}.png').read_bytes()).decode()
 # Display only modern artwork; original references remain private.
 html='''<!doctype html><html lang="es"><meta charset="utf-8"><title>Marcha y apuntado</title><style>body{background:#18251e;color:#eee;font:17px system-ui;padding:24px}main{display:flex;flex-wrap:wrap;gap:12px}article{background:#354638;padding:12px}img{width:192px;height:168px}button,select{font:inherit;margin:8px}</style><h1>Marcha → reposo/apuntado → marcha</h1><p>Revisión interna; aceptación de Miguel pendiente. Reposo conserva el frame original de marcha; el apuntado al objetivo selecciona la familia baja 0x30. No cubre otros estados ni campaña completa.</p><button id="play">Pausar</button><button id="next">Paso</button><select id="density"><option>12</option><option>8</option></select><span id="phase"></span><main id="cards"></main><p>Ritmo ilustrativo. El juego conserva sus contadores y selección.</p><script>const images=IMAGES,sequence=[0,1,2,1,'idle','aim',0,1,2,1];let step=0,run=true;function paint(){let f=sequence[step],d=document.getElementById('density').value;document.getElementById('phase').textContent=step+' · '+f;document.getElementById('cards').replaceChildren(...Array.from({length:8},(_,s)=>{let a=document.createElement('article'),p=document.createElement('p'),im=new Image;p.textContent='Dirección '+s;im.src='data:image/png;base64,'+images[(f==='aim'?s+16:s)+'/'+(f==='idle'?1:f==='aim'?0:f)+'/'+d];a.append(p,im);return a}));}function next(){step=(step+1)%sequence.length;paint()}document.getElementById('play').onclick=()=>run=!run;document.getElementById('next').onclick=next;document.getElementById('density').onchange=paint;setInterval(()=>{if(run)next()},240);paint();</script></html>'''
 (out/'review.html').write_text(html.replace('IMAGES',json.dumps(images)),encoding='utf-8')
 result=dict(status='PENDING user visual acceptance and full coverage',aim_frames=8,aim_assets=16,total_assets=64,total_bindings=126,source_derived_aim_keys=32,replay_observed_aim_keys=sum(r['replay_observed'] for r in config['bindings']),walking=walk,manifest_sha256=hashlib.sha256((out/'candidate-manifest.json').read_bytes()).hexdigest())
 (out/'aim-preparation.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for name in ('out','c01-builder','batch-builder','asset-builder'):p.add_argument('--'+name,type=lambda x:Path(x).resolve(),required=True)
 a=p.parse_args();r=prepare(a.out,a.c01_builder,a.batch_builder,a.asset_builder);print({k:v for k,v in r.items() if k!='walking'})
