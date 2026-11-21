"""Reconstruct private Window cases for explicit source catalog poses in both formats."""
import argparse
import hashlib
import json
import shutil
import struct
from pathlib import Path
from generate_player_pose_table import contracts


def build(resources,requested,out):
    assert not out.exists(),'Preserve earlier fixtures';out.mkdir(parents=True)
    seeds={}
    for fmt,directory in resources:
        for path in sorted(directory.glob('*.json')):
            row=json.loads(path.read_text());segment=row.get('segment')
            if row.get('format')==fmt and segment in (0,1):seeds.setdefault((fmt,segment),(row,directory))
    count=0
    for fmt,actor,sheet,frame,metadata,hidden,role in contracts():
        if (actor,sheet,frame) not in requested:continue
        assert role==1 and not hidden,'This fixture exercises protagonist bodies'
        segment={'eGFX_IN_GAME':0,'eGFX_IN_GAME2':1}[metadata[1]]
        seed,directory=seeds[fmt,segment];row=dict(seed,format=fmt,type=actor,person=0,sheet=sheet,frame=frame,animation=10,
            segment=segment,vehicle=0,destroy=0,offset=int(metadata[0],0),columns=int(metadata[4],0),rows=int(metadata[5],0),
            mod_x=int(metadata[7],0),mod_y=int(metadata[8],0),palette=int(metadata[6],0) if fmt==0 else 0)
        row['resource_palette']=row['palette'];data=(directory/row['resource_file']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==row['resource_sha256']
        stride=160 if fmt==0 else 40;planes=1 if fmt==0 else row['planes'];columns=row['columns']//2 if fmt==0 else (row['columns']-1)*2
        raster=b''.join(data[row['offset']+p*row['layout_height']*40+y*stride:row['offset']+p*row['layout_height']*40+y*stride+columns]
            for p in range(planes) for y in range(row['rows']))
        assert len(raster)==planes*row['rows']*columns
        fields=('format','type','person','sheet','frame','animation','segment','vehicle','destroy','offset','layout_width','layout_height','planes','resource_palette','palette','columns','rows','mod_x','mod_y')
        row['key']=hashlib.sha256(struct.pack('<20q',1,*(row[k] for k in fields))+raster+struct.pack('<255Q',*(c&0xffffff for c in row['colors']))).hexdigest()
        folder=out/f'{fmt}-{actor}-{sheet:02x}-f{frame}';folder.mkdir();(folder/'native-resources').mkdir()
        (folder/'native.json').write_text(json.dumps(row,indent=2)+'\n')
        shutil.copyfile(directory/row['resource_file'],folder/'native-resources'/row['resource_file']);count+=1
    assert count==2*len(requested),'Pose absent from one source format'
    print(f'PASS reconstructed {count} source-defined private Window fixtures, no log-discovery dependency')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--resources',nargs=2,action='append',required=True);p.add_argument('--pose',nargs=3,action='append',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    build([(int(fmt),Path(path)) for fmt,path in a.resources],{tuple(int(v,0) for v in pose) for pose in a.pose},a.out)
