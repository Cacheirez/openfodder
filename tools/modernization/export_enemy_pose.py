"""Export a single source-defined enemy pose using the established C++ builders."""
import argparse
import hashlib
import json
from pathlib import Path
from inventory_enemy_states import ROOT, inventory
from export_player_pose import export


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
    export(a.source,a.atlas,a.sheet,a.frame,a.type,a.family,a.out,a.builders,a.work,placement,crop,
           native_format=a.native_format,contract_rows=contracts(),asset_prefix='enemy-v2' if a.identity==2 else 'enemy')
    if identity:
        path=a.out/'manifest.json';m=json.loads(path.read_text(encoding='utf-8'))
        m['enemy_identity']=2;m['identity_master_sha256']=identity['source_sha256']
        path.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
