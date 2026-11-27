"""Reproduce the enemy art registry; this is not a runtime coverage verdict."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from PIL import Image
from inventory_enemy_states import ROOT, inventory
from enemy_native_formats import source_art_formats


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def registry(identity=1):
    assert identity in (1,2)
    catalog=inventory()
    native_slots={(fmt,s['actor_type'],s['sheet'],s['frame'])
                  for fmt,pl in ((0,'PC'),(1,'Amiga'))
                  for s in catalog['platforms'][pl]['slots'] if s['produced']}
    slots={(s['actor_type'],s['sheet'],s['frame'])
           for pl in catalog['platforms'].values() for s in pl['slots'] if s['produced']}
    poses={}
    for path in sorted((ROOT/'assets/modernization').glob('demo-a1-enemy-*/manifest.json')):
        if ('-enemy-v2-' in path.parent.name)!=(identity==2):continue
        m=json.loads(path.read_text(encoding='utf-8'))
        if identity==2:
            master=ROOT/'assets/modernization/enemy-identity-v2'
            approved=json.loads((master/'manifest.json').read_text(encoding='utf-8'))
            assert approved['status']=='approved-by-Miguel' and sha(master/'source.png')==approved['source_sha256']
            assert m['enemy_identity']==2 and m['identity_master_sha256']==approved['source_sha256']
        if 'authoring_reuse' in m:
            reuse=m['authoring_reuse'];origin=ROOT/reuse['source_manifest']
            original=json.loads(origin.read_text(encoding='utf-8'))
            assert identity==2 and original['enemy_identity']==2
            assert original['identity_master_sha256']==m['identity_master_sha256']
            assert sha(origin.parent/'source.png')==reuse['source_sha256']==sha(path.parent/'source.png')
            assert sha(origin.parent/'generation.json')==reuse['generation_metadata_sha256']
        for asset in m['assets']:
            prefix='enemy-v2' if identity==2 else 'enemy'
            match=re.fullmatch(prefix+r'-(walk|death|prone|pose)-([0-9a-f]+)-f(\d+)(?:-(pc|amiga))?-(8|12)x',asset['id'])
            assert match, 'Unclassified enemy asset ID'
            family,sheet,frame,variant,density=match.groups();sheet=int(sheet,16);frame=int(frame);density=int(density)
            if variant:
                assert 'source' in m and asset.get('native_formats')==[0 if variant=='pc' else 1], 'Explicit native format tag'
            else:
                assert 'native_formats' not in asset, 'Format-specific assets require a tagged identity'
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
                expected_formats={fmt for fmt in (0,1) if (fmt,m['pose']['type'],sheet,frame) in native_slots}
                drawn_formats=source_art_formats(m['pose'],m['export'],expected_formats)
                selected_formats=set(asset.get('native_formats',drawn_formats))
                assert selected_formats and selected_formats<=drawn_formats, 'Unknown or no-write enemy art format'
                for native in m['export']['native']:
                    if native['format'] not in selected_formats:continue
                    box=native['bbox'];actual=image.getchannel('A').getbbox()
                    assert box[0]*density<=actual[0]<actual[2]<=box[2]*density
                    assert box[1]*density<=actual[1]<actual[3]<=box[3]*density
            key=(sheet,frame)
            entry=poses.setdefault(key,dict(sheet=sheet,frame=frame,family=family,
                manifest=path.relative_to(ROOT).as_posix(),source_sha256=sha(source),assets={}))
            target=entry.setdefault('assets_by_format',{}).setdefault(str(asset['native_formats'][0]),{}) if variant else entry['assets']
            assert entry['source_sha256']==sha(source) and str(density) not in target
            target[str(density)]=dict(id=asset['id'],sha256=asset['sha256'],size=list(size))
    for entry in poses.values():
        if 'assets_by_format' in entry:
            assert not entry['assets'], 'Do not mix common and format-specific art for a pose'
            manifest=json.loads((ROOT/entry['manifest']).read_text(encoding='utf-8'))
            assert {int(f) for f in entry['assets_by_format']}=={n['format'] for n in manifest['export']['native']}, 'Incomplete art format coverage'
            assert all(set(a)=={'8','12'} for a in entry['assets_by_format'].values())
            entry['assets']=entry['assets_by_format'].get('1',entry['assets_by_format'].get('0'))
    assert all(set(e['assets'])=={'8','12'} for e in poses.values())
    result=dict(schema=1,status='internally checked available masters; not runtime integration or Miguel acceptance',
        poses=[poses[k] for k in sorted(poses)],counts=dict(poses=len(poses),assets=sum(len({a['id'] for group in e.get('assets_by_format',{'common':e['assets']}).values() for a in group.values()}) for e in poses.values())))
    if identity==2:result['identity']=2
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path)
    p.add_argument('--identity',type=int,choices=(1,2),default=1)
    p.add_argument('--check',action='store_true');a=p.parse_args();r=registry(a.identity)
    if a.out is None:a.out=ROOT/f"assets/modernization/enemy-{'v2-' if a.identity==2 else ''}pose-art.json"
    if a.check:
        assert json.loads(a.out.read_text(encoding='utf-8'))==r, 'Enemy art registry drift'
    else:
        a.out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(r['counts']))
