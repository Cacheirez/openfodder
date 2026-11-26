"""Reuse one E01 falling pose only after exact source-native equivalence.

This copies authored pixels into a separate, source-produced enemy pose package.
It never aliases runtime contracts, signs new banks or generates image content.
"""
import argparse
import copy
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image
from inventory_enemy_states import ROOT, inventory

SOURCES=((0x72,0),(0x72,1),(0x72,2),(0x73,0),(0x73,1),(0x73,2),(0x74,0),(0x74,1))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def reuse(direction,atlas,out=None):
    assert direction in range(8)
    sheet=0xb8+direction;source_sheet,source_frame=SOURCES[direction]
    source=ROOT/f'assets/modernization/demo-a1-enemy-v2-pose-{source_sheet:02x}-f{source_frame}'
    out=out or ROOT/f'assets/modernization/demo-a1-enemy-v2-pose-{sheet:02x}-f0'
    assert not out.exists(),'Preserve previous pose packages'
    original=json.loads((source/'manifest.json').read_text(encoding='utf-8'))
    identity=json.loads((ROOT/'assets/modernization/enemy-identity-v2/manifest.json').read_text(encoding='utf-8'))
    assert identity['status']=='approved-by-Miguel' and original['enemy_identity']==2
    assert original['identity_master_sha256']==identity['source_sha256']
    assert sha(source/'source.png')==original['source']['sha256']
    native=json.loads((atlas/'native-audit.json').read_text(encoding='utf-8'))
    catalog=inventory();evidence=[];native_rows=[]
    for fmt,platform in ((0,'PC'),(1,'Amiga')):
        slots=catalog['platforms'][platform]['slots']
        base=next(s for s in slots if (s['actor_type'],s['sheet'],s['frame'])==(5,source_sheet,source_frame))
        assert base['produced']
        references=[r for r in native if (r['format'],r['type'],r['sheet'],r['frame'])==(fmt,5,source_sheet,source_frame)]
        assert references
        for actor in (5,36):
            target=next(s for s in slots if (s['actor_type'],s['sheet'],s['frame'])==(actor,sheet,0))
            assert target['produced'] and any(r['family']=='fall' and r['direction']==direction for r in target['roles'])
            assert target['metadata']==base['metadata'],'Native geometry/offset/palette differs'
            for ref in references:
                target_ref=next(r for r in native if (r['format'],r['type'],r['sheet'],r['frame'],r['resource_sha256'])==
                    (fmt,actor,sheet,0,ref['resource_sha256']))
                assert (target_ref['width'],target_ref['height'],target_ref['native_signature'])==(ref['width'],ref['height'],ref['native_signature'])
                box=list(Image.open(atlas/target_ref['reference']).getchannel('A').getbbox())
                prior=next(n for n in original['export']['native'] if n['format']==fmt)
                assert box==prior['bbox'] and prior['native_signature']==target_ref['native_signature']
                if actor==5:native_rows.append(dict(format=fmt,native_signature=target_ref['native_signature'],bbox=box))
                evidence.append(dict(format=fmt,type=actor,sheet=sheet,frame=0,resource_sha256=ref['resource_sha256'],
                    native_signature=ref['native_signature'],source_sheet=source_sheet,source_frame=source_frame))
    assert {n['format'] for n in native_rows}=={0,1}
    manifest=copy.deepcopy(original);manifest['pose']=dict(type=5,sheet=sheet,frame=0)
    manifest['status']='Exact E01 falling body reuse with independent native contracts; Miguel gameplay pending'
    manifest['assets']=[];manifest['export']['native']=native_rows
    manifest['source']['reused_from']=(source/'source.png').relative_to(ROOT).as_posix()
    manifest['source']['generator']='reuse-existing-E01-source; no new ImageGen call'
    manifest['authoring_reuse']=dict(source_manifest=(source/'manifest.json').relative_to(ROOT).as_posix(),
        source_sha256=sha(source/'source.png'),generation_metadata_sha256=sha(source/'generation.json'),
        reason='Exact native body/geometry/offset/palette equality verified; own falling actor/person contracts and independent shadow semantics retained')
    out.mkdir(parents=True);shutil.copyfile(source/'source.png',out/'source.png')
    for asset in original['assets']:
        assert 'native_formats' not in asset,'This verified falling reuse expects a common-format body'
        assert sha(source/asset['file'])==asset['sha256']
        a=copy.deepcopy(asset);old_id=a['id'];new_id=f"enemy-v2-pose-{sheet:02x}-f0-{a['density']}x"
        a['id']=new_id;a['file']=new_id+'.rgba'
        shutil.copyfile(source/asset['file'],out/a['file'])
        shutil.copyfile((source/asset['file']).with_suffix('.png'),(out/a['file']).with_suffix('.png'))
        manifest['assets'].append(a)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    generation=dict(generator='reuse-existing-E01-source and derivatives; no new ImageGen call',identity=2,
        transparent_background=True,reused_from=(source/'source.png').relative_to(ROOT).as_posix(),
        source_sha256=sha(source/'source.png'),original_generation_metadata=(source/'generation.json').relative_to(ROOT).as_posix(),
        original_generation_metadata_sha256=sha(source/'generation.json'),target=dict(types=[5,36],sheet=sheet,frame=0,direction=direction),
        review='Native equality and art hashes verified; runtime integration and Miguel gameplay pending')
    (out/'generation.json').write_text(json.dumps(generation,indent=2)+'\n',encoding='utf-8')
    (out/'reuse-evidence.json').write_text(json.dumps(dict(native_cases=evidence,source_manifest=manifest['authoring_reuse']['source_manifest'],
        source_sha256=manifest['source']['sha256'],no_ground_component=True,not_runtime_alias=True),indent=2)+'\n',encoding='utf-8')
    return dict(direction=direction,sheet=sheet,frame=0,native_cases=len(evidence),source_sha256=sha(source/'source.png'),
        assets=len(manifest['assets']),path=str(out))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--direction',type=int,choices=range(8),required=True)
    parser.add_argument('--atlas',type=Path,required=True)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    print(json.dumps(reuse(args.direction,args.atlas,args.out)))
