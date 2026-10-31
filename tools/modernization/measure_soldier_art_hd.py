"""Reproducible synthetic C01 CPU/memory probe. No game/GPU/FPS claims.
GPL-3.0-or-later. Linux measurement, actual unchanged retained C++ compositor.
"""
import argparse, hashlib, json, math, os, platform, statistics, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
MODES=(0,1,8,12,108,112)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    try:return Path(p).read_text().strip()
    except OSError:return 'unavailable'
def stats(values):
    s=sorted(values)
    return {'n':len(s),'median':statistics.median(s),'p95':s[math.ceil(.95*len(s))-1],
            'p99':s[math.ceil(.99*len(s))-1],'min':s[0],'max':s[-1]}
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--samples',type=int,default=200)
    ap.add_argument('--rounds',type=int,default=3)
    ap.add_argument('--warmup',type=int,default=20)
    args=ap.parse_args()
    if not 100<=args.samples<=10000 or not 3<=args.rounds<=20 or not 1<=args.warmup<=1000:ap.error('invalid sample bounds')
    if platform.system()!='Linux':ap.error('RSS metric currently defined only for Linux')
    args.out.mkdir(parents=True,exist_ok=False)
    source=ROOT/'assets/modernization/soldier-c01/source.png'
    assert sha(source)=='9fb5dd519e8589de6c6420e4385c8eb2e12ac1f24c83f9a64678a2d943e31c77'
    report={'verdict':'FAIL','base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
      'method':'fresh child process per mode/case/round; rotated mode order; warmup excluded; timed compose plus output destruction; PNG decode/asset creation, scene construction and full hash excluded',
      'host':{'platform':platform.platform(),'cpu':next((s.split(':',1)[1].strip() for s in read('/proc/cpuinfo').splitlines() if s.startswith('model name')),'unknown'),
        'cpu_max':read('/sys/fs/cgroup/cpu.max'),'memory_max':read('/sys/fs/cgroup/memory.max')},
      'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0],
      'flags':['-std=c++14','-O3','-DNDEBUG'],
      'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'tools/modernization/benchmark_soldier_art_hd.cpp',ROOT/'tools/modernization/measure_soldier_art_hd.py',ROOT/'tools/modernization/test_soldier_art_hd.cpp',ROOT/'tools/modernization/build_soldier_art.cpp',source]+sorted((ROOT/'Source/Utils').glob('*.hpp'))},
      'limits':['Synthetic retained scenes; not measured gameplay or complete frame latency','Shared Linux VM, not user Windows/GPU','No SDL upload, GPU, display scaling, vsync, animation or multi-actor HD','RSS is whole child high-water mark, includes allocator/warmup and fixtures; not exact compositor allocation','Percentiles descriptive, no acceptance threshold; H3 untouched but this probe does not run H3'],
      'runs':[],'summary':[]}
    try:
      with tempfile.TemporaryDirectory(prefix='c01-cost-') as td:
        td=Path(td);gen=td/'builder';exe=td/'benchmark'
        subprocess.run(['g++','-std=c++14','-O2','-I',str(ROOT/'Source'),str(ROOT/'tools/modernization/build_soldier_art.cpp'),'-o',str(gen)],check=True)
        for d in (1,8,12):subprocess.run([str(gen),str(source),str(td/f'c01_{d}.hpp'),str(d)],check=True)
        assert (td/'c01_1.hpp').read_bytes()==(ROOT/'Source/Utils/SoldierArtPixels.hpp').read_bytes()
        report['derived_sha256']={str(d):sha(td/f'c01_{d}.hpp') for d in (1,8,12)}
        subprocess.run(['g++',*report['flags'],'-I',str(ROOT/'Source'),'-I',str(td),str(ROOT/'tools/modernization/benchmark_soldier_art_hd.cpp'),'-o',str(exe)],check=True)
        report['executable_sha256']=sha(exe)
        for r in range(args.rounds):
          for plat in (0,1,2):
            for complexity in (0,1):
              order=MODES[r%len(MODES):]+MODES[:r%len(MODES)]
              for mode in order:
                raw=subprocess.check_output([str(exe),str(plat),str(complexity),str(mode),str(args.samples),str(args.warmup),str(r)],text=True)
                run=json.loads(raw);report['runs'].append(run)
              print(f'round={r} platform={plat} complexity={complexity} complete',flush=True)
        for plat in (0,1,2):
          for complexity in (0,1):
            for mode in MODES:
              rows=[r for r in report['runs'] if (r['platform'],r['complexity'],r['mode'])==(plat,complexity,mode)]
              assert len({r['output_fnv64'] for r in rows})==1
              report['summary'].append({'platform':plat,'complexity':complexity,'mode':mode,
                'wall_ms':stats([v for r in rows for v in r['wall_ms']]),'cpu_ms':stats([v for r in rows for v in r['cpu_ms']]),
                'round_medians_ms':[statistics.median(r['wall_ms']) for r in rows],
                'peak_rss_kib':stats([r['peak_process_rss_kib'] for r in rows]),'output_bytes':rows[0]['output_bytes'],'asset_bytes':rows[0]['asset_bytes']})
        report['verdict']='PASS'
    finally:
      (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary'],indent=2))
if __name__=='__main__':main()
