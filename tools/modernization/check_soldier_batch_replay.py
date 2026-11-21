"""Require six actual SDL publications and original H3 for the full public Amiga campaign."""
import argparse, hashlib, json, os, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--exe',type=Path,required=True);p.add_argument('--data',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 exe,data,out=a.exe.resolve(),a.data.resolve(),a.out.resolve();out.mkdir(parents=True,exist_ok=False);traces=out/'traces';traces.mkdir()
 env={k:v for k,v in os.environ.items() if not k.startswith('OPENFODDER_')}
 env.update(SDL_VIDEODRIVER='dummy',SDL_RENDER_DRIVER='software',SDL_AUDIODRIVER='dummy',OPENFODDER_CAPTURE_SOLDIER='1',OPENFODDER_PRESENT_MISSION_LAYERS='1',OPENFODDER_MISSION_SCREEN_TRANSFORM='1',OPENFODDER_MISSION_SCREEN_FIT='1',OPENFODDER_SOLDIER_HD='12',OPENFODDER_SOLDIER_BATCH='1',OPENFODDER_HD_DIAGNOSTICS='1',OPENFODDER_TRACE_DIR=str(traces))
 command=[str(exe),'--appveyor','--unit-test','--nosound','--window','--alternate-mouse','--campaign','Amiga The One']
 with (out/'engine.log').open('w') as log:subprocess.run(command,cwd=data,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=600,check=True)
 reference=json.loads((ROOT/'tools/modernization/reference-gameplay-v1.json').read_text());reference['phases']=[x for x in reference['phases'] if x['campaign']=='Amiga The One'];reference['total_phases']=len(reference['phases']);reference['total_samples']=sum(x['samples'] for x in reference['phases']);baseline=out/'baseline.json';baseline.write_text(json.dumps(reference))
 result=subprocess.run([sys.executable,str(ROOT/'tools/modernization/check_gameplay_baseline.py'),'--baseline',str(baseline),'--traces',str(traces)],capture_output=True,text=True,check=True)
 log=(out/'engine.log').read_text();keys=sorted({(int(s),int(f)) for s,f in re.findall(r'SOLDIER_BATCH_PUBLISHED: sheet=(\d+) frame=(\d+)',log)})
 assert keys==[(s,f) for s in (2,7) for f in range(3)],f'Missing actual HD publication keys: {keys}'
 report=dict(verdict='PASS',keys=keys,h3=result.stdout.strip(),exe_sha256=hashlib.sha256(exe.read_bytes()).hexdigest(),command=command,scope='SDL software/dummy, full Amiga campaign, actual published keys; no GPU/FPS claim')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
