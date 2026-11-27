"""Qualify existing E01 foot contacts against approved ground paint, without pixel edits."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from inventory_enemy_states import ROOT
from prepare_ground_shadows import checked_file, PAINT


def pose_assets(pose):
    groups=pose.get('assets_by_format',{'common':pose['assets']})
    return {a['id']:a for group in groups.values() for a in group.values()}.values()


def picture(asset,path):
    raw=path.read_bytes();d=asset['density'];width=asset['width']*d;alpha=raw[3::4]
    bottom=max(i//width for i,v in enumerate(alpha) if v>=128)+1
    points=[(i%width,i//width) for i,v in enumerate(alpha) if i//width>=bottom-d//2 and v>=128]
    support=[(i%width,i//width,v) for i,v in enumerate(alpha) if i//width>=max(0,bottom-3*d) and v>=128]
    mass=sum(v for _,_,v in support);assert mass and points
    return dict(id=asset['id'],sha256=asset['sha256'],d=d,points=points,bottom=bottom/d,
        cx=sum((x+.5)*v for x,_,v in support)/mass/d,cy=sum((y+.5)*v for _,y,v in support)/mass/d,
        span=(max(x for x,_,_ in support)-min(x for x,_,_ in support)+1)/d)


def qualifies(image,plate,width,xq,yq):
    d=image['d'];cx=xq/4+plate['cx'];cy=yq/4+plate['cy']
    if cx<=image['cx']+.25 or cy<=image['cy']+.25:return False
    dx=xq*d//4;dy=yq*d//4
    return all(0<=x-dx<width*d and 0<=y-dy<3*d and plate['alpha'][(y-dy)*width*d+x-dx]>=16 for x,y in image['points'])


def qualify():
    from check_enemy_art import registry
    available=registry(2);paint=json.loads((PAINT/'manifest.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((PAINT/paint['source']['file']).read_bytes()).hexdigest()==paint['source']['sha256']
    plates={};paint_hashes={}
    for a in paint['assets']:
        path=checked_file(PAINT,a);alpha=path.read_bytes()[3::4];d=a['density'];width=a['width'];mass=sum(alpha);assert mass
        plates[width,d]=dict(alpha=alpha,cx=sum((i%(width*d)+.5)*v for i,v in enumerate(alpha))/mass/d,
                            cy=sum((i//(width*d)+.5)*v for i,v in enumerate(alpha))/mass/d)
        paint_hashes[a['id']]=a['sha256']
    groups={};excluded=[]
    for pose in available['poses']:
        sheet=pose['sheet']
        if pose['family']=='walk' and 0x42<=sheet<=0x49:family,direction='walk',sheet-0x42
        elif pose['family']=='pose' and 0x4a<=sheet<=0x51:family,direction='grenade',sheet-0x4a
        elif pose['family']=='prone' and 0x52<=sheet<=0x59:family,direction='aim',sheet-0x52
        elif pose['family']=='prone' and 0x10<=sheet<=0x17:family,direction='aim',sheet-0x10
        elif pose['family']=='pose' and 0xa8<=sheet<=0xaf and pose['frame']==2:family,direction='rocket',sheet-0xa8
        elif pose['family']=='pose' and sheet in (0xa4,0xa7) and pose['frame'] in range(8):
            family,direction='slide',pose['frame']
        elif pose['family']=='pose' and sheet==0xdc and pose['frame']==0:
            family,direction='guard',0
        elif pose['family']=='pose' and sheet==0xd8 and pose['frame'] in range(21):
            # E2.LEADER.D0..D6.AUD: own PC rasters have embedded lower-right contacts.
            # Other leader directions/sheets need their own contact audit first.
            family,direction='leader-d8',pose['frame']//3
        elif pose['family']=='pose' and 0x5a<=sheet<=0x61 and pose['frame'] in (0,1):
            excluded.append(dict(sheet=sheet,frame=pose['frame'],reason='Native swimming waterline; no ground component',
                assets=[dict(id=a['id'],sha256=a['sha256']) for a in pose_assets(pose)]))
            continue
        elif pose['family']=='death' and (0x62<=sheet<=0x71 or 0x20<=sheet<=0x2f) and pose['frame'] in (0,1):
            excluded.append(dict(sheet=sheet,frame=pose['frame'],reason='Native damage/airborne state; retain specific and independent shadow commands, no added ground component',
                assets=[dict(id=a['id'],sha256=a['sha256']) for a in pose_assets(pose)]))
            continue
        elif pose['family']=='pose' and ((sheet in (0x72,0x73) and pose['frame'] in (0,1,2)) or (sheet==0x74 and pose['frame'] in (0,1))):
            excluded.append(dict(sheet=sheet,frame=pose['frame'],reason='Verified native body equality with falling B8..BF; retain independent height-driven shadows, no added ground component',
                assets=[dict(id=a['id'],sha256=a['sha256']) for a in pose_assets(pose)]))
            continue
        elif pose['family']=='pose' and sheet==0x74 and pose['frame']==2:
            excluded.append(dict(sheet=sheet,frame=2,reason='Source-known mode-zero frame with format-specific native anchors; no added ground, independent commands retained',
                assets=[dict(id=a['id'],sha256=a['sha256']) for a in pose_assets(pose)]))
            continue
        elif pose['family']=='pose' and sheet in (0x75,0x76,0x77,0x78,0x79) and pose['frame'] in range(3):
            excluded.append(dict(sheet=sheet,frame=pose['frame'],reason='Audited mode-zero body with own format masks/anchors; no new floor inferred from silhouette, independent commands retained; global shadow acceptance pending',
                assets=[dict(id=a['id'],sha256=a['sha256']) for a in pose_assets(pose)]))
            continue
        elif pose['family']=='pose' and 0xb0<=sheet<=0xbf and pose['frame']==0:
            excluded.append(dict(sheet=sheet,frame=0,reason='Native falling body with separate height-driven shadow; no added ground component',
                assets=[dict(id=a['id'],sha256=a['sha256']) for a in pose_assets(pose)]))
            continue
        elif pose['family']=='pose' and sheet in (0x38,0x7a) and pose['frame'] in range(6):
            excluded.append(dict(sheet=sheet,frame=pose['frame'],reason='Audited native sinking with progressive rowsToSkip; no added floor or painted waterline',
                assets=[dict(id=a['id'],sha256=a['sha256']) for a in pose_assets(pose)]))
            continue
        else:raise ValueError('New family needs source/contact review before qualification')
        path=ROOT/pose['manifest'];manifest=json.loads(path.read_text(encoding='utf-8'))
        if family=='leader-d8':
            assert manifest['pose']['type']==106 and all(a.get('native_formats')==[0] for a in manifest['assets'])
        g=groups.setdefault((family,direction),[])
        for a in manifest['assets']:g.append(picture(a,checked_file(path.parent,a)))
    result=[];pending=[]
    for (family,direction),images in sorted(groups.items()):
        preferred=round((min(p['bottom'] for p in images)-1)*4)
        minwidth=max(7,min(16,math.ceil(max(p['span'] for p in images)+2)));answer=None
        widths=sorted({width for width,density in plates if density==12 and width>=minwidth and
                       all((width,p['d']) in plates for p in images)})
        for width in widths:
            ideal=round((sum(p['cx'] for p in images)/len(images)+1.6-plates[width,12]['cx'])*4)
            candidates=sorted(((x,y) for x in range(-16,65) for y in range(max(0,preferred-4),min(60,preferred+4)+1)),
                              key=lambda p:(p[0]-ideal)**2+(p[1]-preferred)**2)
            for xq,yq in candidates:
                if all(qualifies(p,plates[width,p['d']],width,xq,yq) for p in images):answer=(width,xq,yq);break
            if answer:break
        if answer is None:
            pending.append(dict(family=family,direction=direction));continue
        width,xq,yq=answer
        result.append(dict(family=family,direction=direction,owner_type=106 if family=='leader-d8' else 36 if family=='rocket' else 5,width=width,height=3,
            x_quarters=xq,y_quarters=yq,bodies=[dict(id=p['id'],sha256=p['sha256']) for p in images],
            checks=[dict(id=p['id'],contact_pixels=len(p['points']),all_contact_covered=True,
                         support_center=[p['cx'],p['cy']],shadow_center=[xq/4+plates[width,p['d']]['cx'],yq/4+plates[width,p['d']]['cy']]) for p in images]))
    return dict(schema=1,status='Technical alpha/contact qualification only; Miguel enemy visual acceptance pending',
        identity=2,paint_source_sha256=paint['source']['sha256'],paint_assets_sha256=paint_hashes,
        body_pixels_unchanged=True,stable_placement_within_direction=True,groups=result,pending=pending,
        excluded_ground_poses=excluded)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--check',action='store_true');a=p.parse_args();r=qualify()
    if a.check:assert json.loads(a.out.read_text(encoding='utf-8'))==r,'Enemy contact qualification drift'
    else:a.out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(groups=len(r['groups']),body_derivatives=sum(len(g['bodies']) for g in r['groups']),pending=r['pending'])))
    if r['pending']:raise SystemExit(1)
