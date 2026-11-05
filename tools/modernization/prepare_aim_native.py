"""Reconstruct local prone/aim references from real walk resources and source tables.
Original bytes/palettes/rasters stay local. Reconstructed keys are not replay observations.
"""
import argparse,hashlib,json,shutil,subprocess
from pathlib import Path
from inventory_soldier_catalog import inventory
ROOT=Path(__file__).resolve().parents[2]

def prepare(snapshots,out,rekey,renderer):
    out.mkdir(parents=True,exist_ok=False)
    catalog=inventory();groups={}
    for folder in snapshots:
        for p in folder.glob('*.json'):
            r=json.loads(p.read_text())
            if r['type']==0 and r['animation']==0 and r['sheet']<8:
                key=(r['format'],r['resource_sha256'],tuple(r['colors']))
                if key not in groups or r['key']<groups[key][0]['key']:groups[key]=(r,folder)
    if not groups:raise ValueError('no verified resource/palette groups')
    records=[]
    for (fmt,digest,_),(template,folder) in sorted(groups.items()):
        resource=folder/template['resource_file']
        if hashlib.sha256(resource.read_bytes()).hexdigest()!=digest:raise ValueError('changed native resource')
        shutil.copyfile(resource,out/template['resource_file'])
        directions=catalog['platforms']['Amiga' if fmt else 'PC']['player']['groups'][6]['directions']
        assert [r['sheet'] for r in directions]==list(range(16,24))
        for direction in directions:
            spec=dict(template=template,metadata=[int(v,0) if i!=1 else 0 for i,v in enumerate(direction['frames'][0])],sheet=direction['sheet'],direction=direction['direction_index'])
            input_file=out/'input.json';input_file.write_text(json.dumps(spec))
            row_file=out/'row.json';subprocess.run([str(rekey),str(input_file),str(out),str(row_file)],check=True)
            row=json.loads(row_file.read_text());key=row['key'];target=out/(key+'.json');row_file.rename(target)
            raster=out/(key+'.rgba');result=json.loads(subprocess.check_output([str(renderer),str(target),str(out),str(raster)],text=True))
            assert result['width']==16 and result['height']==14 and any(raster.read_bytes()[3::4])
            records.append({k:row[k] for k in ('key','source_key','format','sheet','frame','animation','resource_sha256','derivation')})
    (out/'input.json').unlink();(out/'public-report.json').write_text(json.dumps(dict(scope='prone/aim source-derived references; not runtime coverage',references=records),indent=2)+'\n')
    return records
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--snapshots',type=lambda x:Path(x).resolve(),action='append',required=True)
 for name in ('out','rekey','renderer'):p.add_argument('--'+name,type=lambda x:Path(x).resolve(),required=True)
 a=p.parse_args();print('references',len(prepare(a.snapshots,a.out,a.rekey,a.renderer)))
