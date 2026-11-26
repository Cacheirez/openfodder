"""Prepare one initial-person enemy aim pose from its existing E01 master."""
import argparse
import copy
import json
import re
import shutil
from pathlib import Path
from PIL import Image
from inventory_enemy_states import ROOT, inventory
from reuse_enemy_fall_pose import sha

def reuse(direction,atlas,out=None):
    assert direction in range(8);sheet=0x10+direction;source_sheet=0x52+direction
    source=ROOT/f'assets/modernization/demo-a1-enemy-v2-prone-{source_sheet:02x}-f0'
    out=out or ROOT/f'assets/modernization/demo-a1-enemy-v2-prone-{sheet:02x}-f0'
    assert not out.exists(),'Preserve previous pose packages'
    original=json.loads((source/'manifest.json').read_text(encoding='utf-8'))
    generation=json.loads((source/'generation.json').read_text(encoding='utf-8'))
    assert original['enemy_identity']==2 and sha(source/'source.png')==original['source']['sha256']
    reference=generation['references'][0]
    match=re.search(r'/s(\d+)-f0-verde-a\.png$',reference)
    assert match and int(match[1])==sheet and (ROOT/reference).is_file(),'Verify original friendly aim direction before reuse'
    native=json.loads((atlas/'native-audit.json').read_text(encoding='utf-8'));catalog=inventory();rows=[];evidence=[]
    for fmt,platform in ((0,'PC'),(1,'Amiga')):
        slot=next(s for s in catalog['platforms'][platform]['slots'] if (s['actor_type'],s['sheet'],s['frame'])==(5,sheet,0))
        assert slot['produced'] and any(s['family']=='initial_person_zero_injury' and s.get('native_person')==0 and
            s.get('source_group')=='aim_low' and s.get('direction')==direction for s in slot['roles'])
        matches=[x for x in native if (x['format'],x['type'],x['sheet'],x['frame'])==(fmt,5,sheet,0)]
        assert len(matches)==1,'Explicit native resource review needed'
        n=matches[0];box=list(Image.open(atlas/n['reference']).getchannel('A').getbbox());place=original['export']['placement']
        assert place['y']+place['height']==box[3],'Own lower anchor differs; re-export explicitly'
        for a in original['assets']:
            assert sha(source/a['file'])==a['sha256'] and 'native_formats' not in a
            density=a['density'];actual=Image.open((source/a['file']).with_suffix('.png')).getchannel('A').getbbox()
            assert box[0]*density<=actual[0]<actual[2]<=box[2]*density and box[1]*density<=actual[1]<actual[3]<=box[3]*density
        rows.append(dict(format=fmt,native_signature=n['native_signature'],bbox=box))
        evidence.append(dict(format=fmt,type=5,person=0,sheet=sheet,frame=0,resource_sha256=n['resource_sha256'],native_signature=n['native_signature']))
    m=copy.deepcopy(original);m['pose']=dict(type=5,sheet=sheet,frame=0);m['assets']=[];m['export']['native']=rows
    m['status']='E01initial-person aim art reuse; ground eligibility/runtime integration and Miguel gameplay pending'
    m['authoring_reuse']=dict(source_manifest=(source/'manifest.json').relative_to(ROOT).as_posix(),source_sha256=sha(source/'source.png'),
        generation_metadata_sha256=sha(source/'generation.json'),reason='Shared table aim action/direction/frame and original friendly reference verified; own initial-person signatures and anchors')
    m['source']['reused_from']=(source/'source.png').relative_to(ROOT).as_posix()
    out.mkdir(parents=True);shutil.copyfile(source/'source.png',out/'source.png')
    for asset in original['assets']:
        a=copy.deepcopy(asset);a['id']=f"enemy-v2-prone-{sheet:02x}-f0-{a['density']}x";a['file']=a['id']+'.rgba'
        shutil.copyfile(source/asset['file'],out/a['file']);shutil.copyfile((source/asset['file']).with_suffix('.png'),(out/a['file']).with_suffix('.png'));m['assets'].append(a)
    (out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
    g=dict(generator='reuse-existing-E01-source and derivatives; no new ImageGen call',identity=2,transparent_background=True,
        source_sha256=sha(source/'source.png'),reused_from=(source/'source.png').relative_to(ROOT).as_posix(),
        original_generation_metadata=(source/'generation.json').relative_to(ROOT).as_posix(),original_generation_metadata_sha256=sha(source/'generation.json'),
        original_pose_reference=reference,friendly_reference_sha256=sha(ROOT/reference),target=dict(type=5,person=0,sheet=sheet,frame=0,direction=direction),
        review='Art/native bounds verified; Slide2 initial-person ground eligibility must be integrated before gameplay')
    (out/'generation.json').write_text(json.dumps(g,indent=2)+'\n',encoding='utf-8')
    (out/'reuse-evidence.json').write_text(json.dumps(dict(native_cases=evidence,source_manifest=m['authoring_reuse']['source_manifest'],
        source_sha256=m['source']['sha256'],not_runtime_alias=True,initial_person_zero=True,ground_contract='Existing aim ground qualified separately; runtime initial-person eligibility pending'),indent=2)+'\n',encoding='utf-8')
    return dict(direction=direction,sheet=sheet,frame=0,native_cases=len(evidence),source_sha256=sha(source/'source.png'),assets=len(m['assets']))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--direction',type=int,choices=range(8),required=True);p.add_argument('--atlas',type=Path,required=True);p.add_argument('--out',type=Path)
    a=p.parse_args();print(json.dumps(reuse(a.direction,a.atlas,a.out)))
