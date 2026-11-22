"""Reproduce the enemy art registry; this is not a runtime coverage verdict."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from PIL import Image
from inventory_enemy_states import ROOT, inventory


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def registry():
    catalog=inventory()
    slots={(s['actor_type'],s['sheet'],s['frame'])
           for pl in catalog['platforms'].values() for s in pl['slots'] if s['produced']}
    poses={}
    for path in sorted((ROOT/'assets/modernization').glob('demo-a1-enemy-*/manifest.json')):
        m=json.loads(path.read_text(encoding='utf-8'))
        for asset in m['assets']:
            match=re.fullmatch(r'enemy-(walk|death|prone|pose)-([0-9a-f]+)-f(\d+)-(8|12)x',asset['id'])
            assert match, 'Unclassified enemy asset ID'
            family,sheet,frame,density=match.groups();sheet=int(sheet,16);frame=int(frame);density=int(density)
            actors=[t for t in (5,36,106) if (t,sheet,frame) in slots]
            assert actors, 'Artwork outside produced enemy source bounds'
            assert asset['density']==density and asset['width']==16 and 0<asset['height']<=14
            raw=path.parent/asset['file'];assert sha(raw)==asset['sha256']
            size=(asset['width']*density,asset['height']*density)
            assert len(raw.read_bytes())==size[0]*size[1]*4
            png=raw.with_suffix('.png');image=Image.open(png)
            assert image.mode=='RGBA' and image.size==size and image.tobytes()==raw.read_bytes()
            assert image.getchannel('A').getbbox(), 'No empty modern body'
            source=path.parent/'source.png';assert Image.open(source).mode=='RGBA'
            if 'source' in m:
                assert sha(source)==m['source']['sha256']
                assert m['pose']['type'] in actors and m['pose']['sheet']==sheet and m['pose']['frame']==frame
                assert m['export']['ground_shadow']=='none; preserve independent native commands'
                assert {x['format'] for x in m['export']['native']}=={0,1}
                for native in m['export']['native']:
                    box=native['bbox'];actual=image.getchannel('A').getbbox()
                    assert box[0]*density<=actual[0]<actual[2]<=box[2]*density
                    assert box[1]*density<=actual[1]<actual[3]<=box[3]*density
            key=(sheet,frame)
            entry=poses.setdefault(key,dict(sheet=sheet,frame=frame,family=family,
                manifest=path.relative_to(ROOT).as_posix(),source_sha256=sha(source),assets={}))
            assert entry['source_sha256']==sha(source) and str(density) not in entry['assets']
            entry['assets'][str(density)]=dict(id=asset['id'],sha256=asset['sha256'],size=list(size))
    assert all(set(e['assets'])=={'8','12'} for e in poses.values())
    return dict(schema=1,status='internally checked available masters; not runtime integration or Miguel acceptance',
        poses=[poses[k] for k in sorted(poses)],counts=dict(poses=len(poses),assets=2*len(poses)))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,default=ROOT/'assets/modernization/enemy-pose-art.json')
    p.add_argument('--check',action='store_true');a=p.parse_args();r=registry()
    if a.check:
        assert json.loads(a.out.read_text(encoding='utf-8'))==r, 'Enemy art registry drift'
    else:
        a.out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(r['counts']))
