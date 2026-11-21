"""Export one authorized CF1 master using the existing exact crop/box-filter builders.

The private source atlas supplies the native box, never a guessed silhouette or
an observed variant key. Keep the generated original and record every placement.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from PIL import Image
from prepare_walk_art_review import png
from generate_player_pose_table import contracts


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export(source,atlas,sheet,frame,actor,family,out,builders,work,placement=None,shared_crop=None,native_format=None):
    assert not out.exists(),'Preserve existing masters/derivatives'
    native=[r for r in json.loads((atlas/'native-audit.json').read_text()) if (r['type'],r['sheet'],r['frame'])==(actor,sheet,frame)]
    declared_formats={fmt for fmt,t,s,f,*_ in contracts() if (t,s,f)==(actor,sheet,frame)}
    formats=declared_formats if native_format is None else {native_format}
    assert formats<=declared_formats,'Unknown source format'
    if native_format is not None:native=[r for r in native if r['format']==native_format]
    preferred_format=1 if native_format is None else native_format
    assert {r['format'] for r in native}==formats and preferred_format in formats,'Source-defined format coverage'
    row=next(r for r in native if r['format']==preferred_format)
    width,height=row['width'],row['height'];assert width==16 and height<=14
    boxes=[]
    for r in native:
        assert (r['width'],r['height'])==(width,height)
        box=Image.open(atlas/r['reference']).getchannel('A').getbbox();assert box
        boxes.append(dict(format=r['format'],native_signature=r['native_signature'],bbox=list(box)))
    x,y,right,bottom=next(b['bbox'] for b in boxes if b['format']==preferred_format)
    if placement:
        px,py,pw,ph=placement
        assert pw>0 and ph>0 and x<=px<px+pw<=right and y<=py<py+ph<=bottom,'Art placement must stay within the verified native box'
        x,y,right,bottom=px,py,px+pw,py+ph
    image=Image.open(source);assert image.mode=='RGBA'
    crop=image.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();assert crop
    if shared_crop:
        left,top,right_edge,bottom_edge=shared_crop
        assert 0<=left<right_edge<=image.width and 0<=top<bottom_edge<=image.height
        assert max(left,crop[0])<min(right_edge,crop[2]) and max(top,crop[1])<min(bottom_edge,crop[3])
        crop=shared_crop # One authoring canvas/anchor across an animation, no per-frame rescaling.
    out.mkdir(parents=True);work.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,out/'source.png');assets=[]
    for density in (8,12):
        name=f'player-{family}-{sheet:02x}-f{frame}-{density}x';header=work/f'{name}.hpp'
        subprocess.run([str(builders/'openfodder_batch_builder.exe'),str(source),str(header),str(density),'PlayerPose',
            *map(str,crop),str(x),str(right-x),str(bottom-y)],check=True)
        values=[int(v) for v in re.findall(r'(\d+)u',header.read_text())];assert len(values)==16*14*density*density
        rgba=bytes(v for c in values for v in ((c>>16)&255,(c>>8)&255,c&255,c>>24))
        shift=(14-bottom)*density*16*density*4;assert shift>=0 and not any(rgba[:shift])
        rgba=(rgba[shift:]+bytes(shift))[:16*height*density*density*4]
        image_path=out/f'{name}.png';image_path.write_bytes(png(16*density,height*density,rgba))
        raw=out/f'{name}.rgba'
        result=json.loads(subprocess.check_output([str(builders/'openfodder_ordered_asset_builder.exe'),str(image_path),str(raw),name,'16',str(height),str(density)]))
        assert raw.read_bytes()==rgba and sha(raw)==result['sha256']
        box=Image.frombytes('RGBA',(16*density,height*density),rgba).getchannel('A').getbbox()
        assert box and x*density<=box[0]<box[2]<=right*density and y*density<=box[1]<box[3]<=bottom*density
        assets.append(result)
    manifest=dict(status='Authorized autonomous protagonist art; internal inspection and exact export; not global visual/gameplay acceptance',
        pose=dict(type=actor,sheet=sheet,frame=frame),assets=assets,bindings=[],
        source=dict(file='source.png',size=list(image.size),mode=image.mode,sha256=sha(source),generator='built-in image_gen; original preserved'),
        export=dict(builder='existing build_soldier_batch.cpp + build_ordered_soldier_asset.cpp',crop=list(crop),placement=dict(x=x,y=y,width=right-x,height=bottom-y),
                    logical_size=[width,height],native=boxes,ground_shadow='none; preserve independent native commands'))
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(sheet=sheet,frame=frame,source_sha256=sha(source),assets=[a['id'] for a in assets],placement=manifest['export']['placement'])))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--crop',help='Explicit shared left,top,right,bottom authoring crop; original retained')
    p.add_argument('--native-format',type=int,choices=(0,1),help='Explicit format-specific art, e.g. PC entry effect with empty Amiga counterpart')
    for name in ('source','atlas','out','builders','work'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--sheet',type=lambda v:int(v,0),required=True);p.add_argument('--frame',type=int,required=True);p.add_argument('--type',type=int,default=0);p.add_argument('--family',choices=['hitdeath','pose'],default='pose');p.add_argument('--placement',help='Explicit x,y,width,height within native box; never changes logical geometry');a=p.parse_args()
    placement=tuple(map(int,a.placement.split(','))) if a.placement else None
    export(a.source,a.atlas,a.sheet,a.frame,a.type,a.family,a.out,a.builders,a.work,placement,
           tuple(map(int,a.crop.split(','))) if a.crop else None,native_format=a.native_format)
