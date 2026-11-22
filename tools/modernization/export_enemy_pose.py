"""Export a single source-defined enemy pose using the established C++ builders."""
import argparse
from pathlib import Path
from inventory_enemy_states import inventory
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
    a=p.parse_args()
    export(a.source,a.atlas,a.sheet,a.frame,a.type,a.family,a.out,a.builders,a.work,
           native_format=a.native_format,contract_rows=contracts(),asset_prefix='enemy')
