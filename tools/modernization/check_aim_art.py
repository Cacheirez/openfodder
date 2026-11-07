"""Verify native-selected walk/idle/aim/walk with two bodies through actual WindowHD."""
import argparse,hashlib,json,os,subprocess,tempfile
from pathlib import Path
from prepare_aim_art import prepare
from ordered_soldier_coverage import report
from prepare_walk24 import CONFIG as WALK_CONFIG

def check(a,out):
    preparation=prepare(out/'art',a.c01_builder,a.batch_builder,a.asset_builder)
    selection=json.loads(subprocess.check_output([str(a.selector_exe)],text=True));assert len(selection)==80
    native=bool(a.native_aim)
    rows=[]
    if native:
        for p in a.native_aim.glob('*.json'):
            if len(p.stem)==64:rows.append(dict(row=json.loads(p.read_text()),directory=str(a.native_aim)))
        assert len(rows)==32
        for b in json.loads(WALK_CONFIG.read_text())['bindings']:
            sources=[folder/(b['key']+'.json') for folder in a.native_walk]
            sources=[p for p in sources if p.exists()]
            canonical=lambda p:json.dumps({k:v for k,v in json.loads(p.read_text()).items() if k not in ('direction','face','tick')},sort_keys=True)
            assert sources and len({canonical(p) for p in sources})==1
            rows.append(dict(row=json.loads(sources[0].read_text()),directory=str(sources[0].parent)))
        assert len(rows)==126
    (out/'art/transition-input.json').write_text(json.dumps(dict(native=native,selection=selection,rows=rows)))
    env={**os.environ,'OPENFODDER_AIM_ART':str(out/'art'),'OPENFODDER_ORDERED_COVERAGE':'1'}
    log=out/'window.log'
    with log.open('w') as f:subprocess.run([str(a.exe)],cwd=out,env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=180)
    census=report([log]);expected=600 if native else 640
    assert census['outcomes']=={'published':expected,'missing-variant':3},census
    assert census['published_command_presentations']==expected*2,census
    assert census['verdict']=='PENDING'
    assert 'PASS aim transition' in log.read_text()
    result=dict(status='PASS bounded aim transitions; full soldiers and user acceptance PENDING',mode='real resource source-derived aim plus observed walk' if native else 'controlled source metadata, explicit test-only bindings',intervals=expected,bodies=expected*2,sequences=60 if native else 64,source_selector_assertions=152,source_selector_samples=80,densities=[8,12],rejections=3,walking='48 descriptors unchanged; C01 exact in WindowHD fixture',log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),preparation=preparation,limits=['source-table reconstruction is not runtime coverage','two ordinary Amiga walk keys still missing; partial group excludes two paired directions','full campaign/GPU/CD32 and user visual acceptance pending'])
    (out/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='preparation'});return result
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('exe','selector-exe','c01-builder','batch-builder','asset-builder'):p.add_argument('--'+name,type=lambda x:Path(x).resolve(),required=True)
    p.add_argument('--native-aim',type=lambda x:Path(x).resolve());p.add_argument('--native-walk',type=lambda x:Path(x).resolve(),action='append',default=[]);p.add_argument('--out',type=lambda x:Path(x).resolve());a=p.parse_args()
    if a.out:a.out.mkdir(parents=True,exist_ok=False);check(a,a.out)
    else:
        with tempfile.TemporaryDirectory(prefix='aim-art-') as tmp:check(a,Path(tmp))
