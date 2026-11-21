"""Build a private, finite CF1 pose catalog from retained native resources and verified modern assets.

Native PNGs/resources stay in --out, never in the public repository. All source slots
are enumerated, including ones absent from the replay that retained the resource.
"""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from PIL import Image
from generate_player_pose_table import contracts
from inventory_player_states import art_reuse,inventory


def digest(data):
    return hashlib.sha256(data).hexdigest()


def indices(data,offset,width,height,fmt,layout_height):
    stride=160 if fmt==0 else 40
    end=offset+(height-1)*stride+(width//2 if fmt==0 else width//8)+(0 if fmt==0 else 3*layout_height*40)
    assert 0<=offset<end<=len(data),'Complete native raster bounds'
    out=bytearray()
    for y in range(height):
        for x in range(width):
            if fmt==0:
                pixel=data[offset+y*160+x//2];value=pixel&15 if x&1 else pixel>>4
            else:
                value=sum((1<<p) for p in range(4) if data[offset+p*layout_height*40+y*40+x//8]&(0x80>>(x&7)))
            out.append(value)
    return bytes(out)


def signature(raw,width,height):
    return digest(b'CF1POSE\x01'+width.to_bytes(8,'little')+height.to_bytes(8,'little')+raw)


def build(base,resources,out,extra=()):
    catalog=inventory() # Native table generation is independent; candidate art integrity is mandatory here.
    assert not out.exists(),'Preserve prior candidates'
    out.mkdir(parents=True);(out/'native').mkdir()
    original=json.loads((base/'candidate-manifest.json').read_text())
    assets=list(original['assets']);locations={a['id']:base/a['file'] for a in assets};art={}
    for package in extra:
        for asset in json.loads((package/'manifest.json').read_text())['assets']:
            assert asset['id'] not in locations,'Duplicate modern asset'
            assets.append(asset);locations[asset['id']]=package/asset['file']
    for asset in assets:
        match=re.fullmatch(r's(\d+)-f(\d+)-(8|12)',asset['id'])
        if match:sheet,frame,density=map(int,match.groups())
        else:
            match=re.fullmatch(r'player-(?:fall|swim|hitdeath|pose)-([0-9a-f]+)-f(\d+)-(8|12)x',asset['id'])
            if not match:continue
            sheet=int(match[1],16);frame=int(match[2]);density=int(match[3])
        assert (sheet,frame,density) not in art
        art[sheet,frame,density]=asset['id']
    aliases=art_reuse()
    active={(r['actor_type'],r['sheet'],r['frame']) for info in catalog['platforms'].values() for r in info['required']}
    for alias in aliases:
        if (alias['actor_type'],alias['sheet'],alias['frame']) not in active:continue
        for density in (8,12):
            target=(alias['sheet'],alias['frame'],density);source=(alias['source_sheet'],alias['source_frame'],density)
            assert source in art,'Explicit reuse needs a verified source asset'
            if alias.get('kind')=='master-reexport':
                assert target in art,'Reused master needs its verified target derivatives'
            else:
                assert target not in art,'Duplicate explicit reused pose'
                art[target]=art[source]
    for asset in assets:
        raw=locations[asset['id']].read_bytes();assert digest(raw)==asset['sha256']
        shutil.copyfile(locations[asset['id']],out/asset['file'])
    retained={}
    for fmt,directory in resources:
        for path in sorted(directory.glob('*.json')):
            row=json.loads(path.read_text());key=(fmt,row.get('segment'))
            if row.get('format')!=fmt or row.get('segment') not in (0,1):continue
            data=(directory/row['resource_file']).read_bytes();assert digest(data)==row['resource_sha256']
            retained.setdefault(key,{})[row['resource_sha256']]=(row,data)
    poses=[];audit=[];gaps=[];pose_signatures={}
    for fmt,actor,sheet,frame,metadata,hidden,role in contracts():
        segment={'eGFX_IN_GAME':0,'eGFX_IN_GAME2':1}[metadata[1]]
        offset=int(metadata[0],0);width=int(metadata[4],0) if fmt==0 else (int(metadata[4],0)-1)*16
        height=int(metadata[5],0);palette=int(metadata[6],0) if fmt==0 else 0
        hashes=[]
        for resource_hash,(row,data) in retained[fmt,segment].items():
            raw=indices(data,offset,width,height,fmt,row['layout_height']);sha=signature(raw,width,height)
            if sha not in hashes:hashes.append(sha)
            assert not hidden or not any(raw),'Hidden slot writes native pixels'
            pixels=bytearray()
            for value in raw:
                color=row['colors'][palette+value]
                pixels.extend(((color>>16)&255,(color>>8)&255,color&255,255 if value else 0))
            name=f'{fmt}-{actor}-{sheet:02x}-f{frame}-{resource_hash[:8]}.png'
            Image.frombytes('RGBA',(width,height),bytes(pixels)).save(out/'native'/name)
            audit.append(dict(format=fmt,type=actor,sheet=sheet,frame=frame,resource_sha256=resource_hash,
                native_signature=sha,width=width,height=height,reference='native/'+name))
        ids={} if hidden or role==0 else {str(d):art[sheet,frame,d] for d in (8,12) if (sheet,frame,d) in art}
        pose_signatures[fmt,actor,sheet,frame]=set(hashes)
        if actor==0 and 0x30<=sheet<0x38:continue # Audited dormant rows, not runtime body/art requirements.
        if hidden or role==0 or len(ids)==2:
            poses.append(dict(format=fmt,type=actor,sheet=sheet,frame=frame,native_signatures=hashes,assets=ids))
        else:gaps.append(dict(format=fmt,type=actor,sheet=sheet,frame=frame,role=role,width=width,height=height))
    for alias in aliases:
        for fmt in (0,1):
            assert pose_signatures[fmt,0,alias['sheet'],alias['frame']]==pose_signatures[fmt,0,alias['source_sheet'],alias['source_frame']],'Explicit reuse native raster differs'
    sources=[dict(format=fmt,segment=segment,sha256=sha) for (fmt,segment),items in sorted(retained.items()) for sha in sorted(items)]
    manifest=dict(version=3,assets=assets,bindings=[],player_catalog=dict(schema=1,complete=not gaps,keep_verified_native=True,native_resources=sources,poses=poses))
    manifest['player_catalog']['required_slots']=len(poses)+len(gaps)
    (out/'candidate-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (out/'native-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    (out/'missing-art.json').write_text(json.dumps(gaps,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(slots=len(poses)+len(gaps),covered=len(poses),missing=len(gaps),assets=len(assets),complete=not gaps)))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',type=Path,required=True);p.add_argument('--resources',action='append',nargs=2,metavar=('FORMAT','DIRECTORY'),required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--art',type=Path,action='append',default=[]);a=p.parse_args()
    build(a.base,[(int(fmt),Path(path)) for fmt,path in a.resources],a.out,a.art)
