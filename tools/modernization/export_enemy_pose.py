"""Export a single source-defined enemy pose using the established C++ builders."""
import argparse
import hashlib
import json
from pathlib import Path
from inventory_enemy_states import ROOT, inventory
from export_player_pose import export
from enemy_native_formats import audited_pc_only, source_art_formats
from PIL import Image


def contracts():
    c=inventory()
    return [(fmt,s['actor_type'],s['sheet'],s['frame'])
            for fmt,pl in ((0,'PC'),(1,'Amiga'))
            for s in c['platforms'][pl]['slots'] if s['produced']]


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source','atlas','out','builders','work'):
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--sheet',type=lambda s:int(s,0),required=True)
    p.add_argument('--frame',type=int,required=True)
    p.add_argument('--type',type=int,default=5)
    p.add_argument('--family',default='pose')
    p.add_argument('--native-format',type=int,choices=(0,1))
    p.add_argument('--identity',type=int,choices=(1,2),default=1)
    p.add_argument('--verified-empty-amiga',action='store_true',
                   help='PC-only audited guard/leader art; verify and retain empty Amiga command')
    p.add_argument('--placement',help='Explicit x,y,width,height inside verified native bounds')
    p.add_argument('--crop',help='Shared authoring left,top,right,bottom across this direction')
    a=p.parse_args()
    identity=None
    if a.identity==2:
        identity_path=ROOT/'assets/modernization/enemy-identity-v2/manifest.json'
        identity=json.loads(identity_path.read_text(encoding='utf-8'))
        assert identity['status']=='approved-by-Miguel' and identity['identity']==2
        master=identity_path.parent/'source.png'
        assert hashlib.sha256(master.read_bytes()).hexdigest()==identity['source_sha256']
    placement=tuple(map(int,a.placement.split(','))) if a.placement else None
    crop=tuple(map(int,a.crop.split(','))) if a.crop else None
    if placement is not None:assert len(placement)==4,'Expected four placement coordinates'
    if crop is not None:assert len(crop)==4,'Expected four crop coordinates'
    no_write=[]
    if a.verified_empty_amiga:
        assert a.identity==2 and a.native_format==0 and audited_pc_only(dict(type=a.type,sheet=a.sheet,frame=a.frame))
        atlas=json.loads((a.atlas/'native-audit.json').read_text(encoding='utf-8'))
        rows=[n for n in atlas if (n['format'],n['type'],n['sheet'],n['frame'])==(1,a.type,a.sheet,a.frame)]
        assert len(rows)==1,'Review native resource variants explicitly'
        n=rows[0];image=Image.open(a.atlas/n['reference'])
        assert image.size==(n['width'],n['height']) and image.getchannel('A').getbbox() is None
        no_write=[dict(format=1,segment=0,resource_sha256=n['resource_sha256'],native_signature=n['native_signature'],
                       logical_size=[n['width'],n['height']],bbox=n['bbox'],opaque_pixels=n['opaque_pixels'])]
        source_art_formats(dict(type=a.type,sheet=a.sheet,frame=a.frame),
                           dict(native=[dict(format=0)],native_no_write=no_write),{0,1})
    export(a.source,a.atlas,a.sheet,a.frame,a.type,a.family,a.out,a.builders,a.work,placement,crop,
           native_format=a.native_format,contract_rows=contracts(),asset_prefix='enemy-v2' if a.identity==2 else 'enemy')
    if identity:
        path=a.out/'manifest.json';m=json.loads(path.read_text(encoding='utf-8'))
        m['enemy_identity']=2;m['identity_master_sha256']=identity['source_sha256']
        if no_write:
            m['export']['native_no_write']=no_write
            for asset in m['assets']:
                old=a.out/asset['file'];name=asset['id'].replace(f"-{asset['density']}x",f"-pc-{asset['density']}x")
                new=a.out/(name+'.rgba');old.rename(new);old.with_suffix('.png').rename(new.with_suffix('.png'))
                asset.update(id=name,file=new.name,native_formats=[0])
        path.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
        if no_write:
            print(json.dumps(dict(verified_pc_assets=[x['id'] for x in m['assets']],
                                  empty_amiga_commands=len(no_write))))
