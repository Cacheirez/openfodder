"""Build private density-specific development candidates, never a final enemy review.

Native banks remain outside Git. Recompute every produced source signature from
hashed resources. Retain the frozen player assets and copy only approved E01/v2
enemy artwork; missing bodies are explicit verified-native development draws.
"""
import argparse
import copy
import hashlib
import json
import shutil
from pathlib import Path
from generate_enemy_pose_table import ROOT, contracts
from prepare_ground_shadows import checked_file


def load(path):return json.loads(path.read_text(encoding='utf-8'))


def select_player(original,density):
    assert density in (8,12)
    assert original['version']==3 and original['player_catalog']['schema']==1
    result=copy.deepcopy(original)
    result['version']=4;result['density']=density
    result['assets']=[a for a in result['assets'] if a['density']==density]
    c=result['player_catalog'];assert c['complete']
    c['schema']=2;c['density']=density
    for p in c['poses']:
        if p['assets']:p['assets']={str(density):p['assets'][str(density)]}
    assert result['bindings']==[], 'Only source catalogs are supported'
    return result


def build(base,resources,out,density):
    from check_enemy_art import registry
    from prepare_player_catalog import indices, signature
    assert not out.exists(),'Preserve previous candidates'
    original=load(base/'candidate-manifest.json');result=select_player(original,density)
    assets={a['id']:a for a in result['assets']}
    locations={a['id']:checked_file(base,a) for a in result['assets']}
    retained={}
    for fmt,directory in resources:
        for path in sorted(directory.glob('*.json')):
            row=load(path);segment=row.get('segment')
            if row.get('format')!=fmt or segment not in (0,1):continue
            assert Path(row['resource_file']).name==row['resource_file']
            data=(directory/row['resource_file']).read_bytes();sha=hashlib.sha256(data).hexdigest()
            assert sha==row['resource_sha256'],'Retained resource changed'
            retained.setdefault((fmt,segment),{})[sha]=(row,data)
    assert set(retained)=={(f,s) for f in (0,1) for s in (0,1)}
    sources=[dict(format=f,segment=s,sha256=h) for (f,s),items in sorted(retained.items()) for h in sorted(items)]
    assert sources==sorted(original['player_catalog']['native_resources'],key=lambda s:(s['format'],s['segment'],s['sha256'])), 'Frozen player/native bank set differs'
    available=registry(2);art={}
    for pose in available['poses']:
        package=ROOT/pose['manifest'];manifest=load(package)
        for a in manifest['assets']:
            if a['density']!=density:continue
            assert a['id'] not in assets
            locations[a['id']]=checked_file(package.parent,a);assets[a['id']]=copy.deepcopy(a)
            formats=a.get('native_formats',[n['format'] for n in manifest['export']['native']])
            for fmt in formats:
                key=fmt,pose['sheet'],pose['frame']
                assert key not in art, 'Conflicting enemy art for native format'
                art[key]=a['id']
    player_shadows={(p['format'],p['sheet'],p['frame']):p for p in original['player_catalog']['poses'] if p['type']==22}
    poses=[];evidence=[];missing=[];counts={}
    for slot in contracts():
        if not slot['produced']:continue
        fmt,actor,sheet,frame=(slot[k] for k in ('format','type','sheet','frame'))
        width=slot['columns'] if fmt==0 else (slot['columns']-1)*16;height=slot['rows']
        hashes=set();empty=set()
        for resource_hash,(row,data) in retained[fmt,slot['segment']].items():
            raw=indices(data,slot['offset'],width,height,fmt,row['layout_height'])
            sha=signature(raw,width,height);hashes.add(sha)
            if not any(raw):empty.add(sha)
            evidence.append(dict(format=fmt,type=actor,sheet=sheet,frame=frame,resource_sha256=resource_hash,
                native_signature=sha,no_write=not any(raw),width=width,height=height,
                layout_height=row['layout_height'],resource_file=row['resource_file']))
        assert not slot['invisible'] or hashes==empty,'Native hidden marker writes'
        ids={}
        if slot['role']==4:
            reference=player_shadows[fmt,sheet,frame]
            assert hashes==set(reference['native_signatures']),'Independent shadow native raster differs from protagonist'
            identity=reference['assets'][str(density)];a=assets[identity]
            assert (a['width'],a['height'])==(width,height)
            ids={str(density):identity}
        elif slot['role']==2 and hashes!=empty and (fmt,sheet,frame) in art:
            identity=art[fmt,sheet,frame];a=assets[identity]
            assert (a['width'],a['height'])==(width,height)
            ids={str(density):identity}
        kind='no-write' if hashes==empty else 'modern' if ids else 'native-marker' if slot['role']==6 else 'classic-missing-art'
        counts[kind]=counts.get(kind,0)+1
        if kind=='classic-missing-art':missing.append(dict(format=fmt,type=actor,sheet=sheet,frame=frame))
        poses.append(dict(format=fmt,type=actor,sheet=sheet,frame=frame,native_signatures=sorted(hashes),no_write_signatures=sorted(empty),assets=ids))
    result['assets']=list(assets.values())
    result['enemy_catalog']=dict(schema=1,density=density,complete_art=not missing,native_resources=sources,poses=poses)
    total=sum(a['width']*a['height']*density*density*4 for a in assets.values())
    assert total<=64*1024*1024,'Unchanged 64 MiB asset budget'
    leaves={}
    for a in assets.values():
        assert a['file'] not in leaves or leaves[a['file']]==a['sha256'],'Conflicting asset filenames'
        leaves[a['file']]=a['sha256']
    out.mkdir(parents=True)
    for a in assets.values():shutil.copyfile(locations[a['id']],out/a['file'])
    summary=dict(schema=1,status='PRIVATE TECHNICAL DEVELOPMENT; partial enemies, not final gameplay review',density=density,
        enemy_contracts=len(poses),representations=counts,available_enemy_body_poses=available['counts']['poses'],
        assets=len(assets),asset_bytes=total,missing_body_contracts=len(missing),modern_owned_shadow_contracts=6,
        enemy_ground_contact='Pending qualification/attachment for normal modern bodies; independent shadows reused by exact native equality',
        frozen_player_manifest_sha256=hashlib.sha256((base/'candidate-manifest.json').read_bytes()).hexdigest(),
        guarantees=['Frozen player body/shadow bytes and pose bindings preserved for selected density',
            'Every produced enemy source slot signed; no observed/unknown keys added',
            'No incomplete enemy art declared complete; no native pixels copied to public repository'])
    for name,obj in [('candidate-manifest.json',result),('native-evidence.json',evidence),('missing-art.json',missing),('technical-summary.json',summary)]:
        (out/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
    return summary


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--resources',nargs=2,action='append',required=True)
    p.add_argument('--density',type=int,choices=(8,12),required=True);a=p.parse_args()
    print(json.dumps(build(a.base,[(int(f),Path(p)) for f,p in a.resources],a.out,a.density)))
