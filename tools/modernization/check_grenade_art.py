"""Verify original posture/fire/grenade sequence with independent bodies in WindowHD."""
import argparse,hashlib,json,os,subprocess,tempfile
from pathlib import Path
from prepare_grenade_art import prepare
from prepare_aim_art import CONFIG as AIM_CONFIG
from prepare_walk24 import CONFIG as WALK_CONFIG
from ordered_soldier_coverage import report

def check(a,out):
 preparation=prepare(out/'art',a.c01_builder,a.batch_builder,a.asset_builder)
 selection=json.loads(subprocess.check_output([str(a.selector_exe)],text=True));assert len(selection)==168
 directions=preparation['directions'];native=bool(a.native_grenade);rows=[]
 if native:
  for p in a.native_grenade.glob('*.json'):
   if len(p.stem)==64:
    r=json.loads(p.read_text())
    if r['sheet']-8 in directions:rows.append(dict(row=r,directory=str(a.native_grenade)))
  assert len(rows)==12*len(directions)
  for b in json.loads(AIM_CONFIG.read_text())['bindings']:
   p=a.native_aim/(b['key']+'.json');rows.append(dict(row=json.loads(p.read_text()),directory=str(a.native_aim)))
  for b in json.loads(WALK_CONFIG.read_text())['bindings']:
   candidates=[p/(b['key']+'.json') for p in a.native_walk];candidates=[p for p in candidates if p.exists()]
   canonical=lambda p:json.dumps({k:v for k,v in json.loads(p.read_text()).items() if k not in ('direction','face','tick')},sort_keys=True)
   assert candidates and len({canonical(p) for p in candidates})==1
   p=candidates[0];rows.append(dict(row=json.loads(p.read_text()),directory=str(p.parent)))
  assert len(rows)==preparation['bindings']
 second=0 if len(directions)==1 else 1
 expected=168 if len(directions)==1 else (1260 if native else 1344)
 (out/'art/transition-input.json').write_text(json.dumps(dict(native=native,selection=selection,rows=rows,directions=directions,second_offset=second,expected_intervals=expected,assets=preparation['assets'],bindings=preparation['bindings'])))
 log=out/'window.log'
 with log.open('w') as f:subprocess.run([str(a.exe)],cwd=out,env={**os.environ,'OPENFODDER_GRENADE_ART':str(out/'art'),'OPENFODDER_ORDERED_COVERAGE':'1'},stdout=f,stderr=subprocess.STDOUT,check=True,timeout=240)
 census=report([log]);assert census['outcomes']=={'published':expected,'missing-variant':3},census
 assert census['published_command_presentations']==expected*2 and census['verdict']=='PENDING'
 assert 'PASS grenade transition' in log.read_text()
 result=dict(status='PASS bounded body transitions; full campaign and user acceptance PENDING',mode='real source-derived grenade/aim, observed walking' if native else 'controlled source metadata and test-only keys',directions=directions,intervals=expected,bodies=expected*2,sequences=expected//21,densities=[8,12],selector_assertions=272,selector_samples=168,three_rejections=True,c01='exact',previous_assets='64 descriptors must remain unchanged',log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),preparation=preparation,limits=['reconstruction is not runtime coverage','two ordinary Amiga walking keys still absent','projectile/other actors remain separate, not campaign coverage'])
 (out/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='preparation'});return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for name in ('exe','selector-exe','c01-builder','batch-builder','asset-builder'):p.add_argument('--'+name,type=lambda x:Path(x).resolve(),required=True)
 for name in ('native-grenade','native-aim','out'):p.add_argument('--'+name,type=lambda x:Path(x).resolve())
 p.add_argument('--native-walk',type=lambda x:Path(x).resolve(),action='append',default=[]);a=p.parse_args()
 if a.out:a.out.mkdir(parents=True,exist_ok=False);check(a,a.out)
 else:
  with tempfile.TemporaryDirectory(prefix='grenade-art-') as tmp:check(a,Path(tmp))
