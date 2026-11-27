"""Reuse the two source-identical E01 direction7 grenade poses, never guess others."""
import argparse
import copy
import json
import shutil
from pathlib import Path
from PIL import Image
from inventory_enemy_states import ROOT
from generate_enemy_pose_table import contracts
from reuse_enemy_fall_pose import sha


def reuse(frame, atlas, out=None):
    assert frame in (0, 2), 'Only source-proven endpoints'
    source_frame = {0: 0, 2: 1}[frame]
    source = ROOT / f'assets/modernization/demo-a1-enemy-v2-walk-49-f{source_frame}'
    out = out or ROOT / f'assets/modernization/demo-a1-enemy-v2-pose-51-f{frame}'
    assert not out.exists(), 'Preserve previous exports'
    original = json.loads((source / 'manifest.json').read_text(encoding='utf-8'))
    assert original['enemy_identity'] == 2
    assert sha(source / 'source.png') == original['source']['sha256']
    native = json.loads((atlas / 'native-audit.json').read_text(encoding='utf-8'))
    slots = contracts()
    rows, proof = [], []
    for fmt in (0, 1):
        slot = next(s for s in slots if (s['format'], s['type'], s['sheet'], s['frame']) == (fmt, 5, 0x51, frame))
        assert slot['produced'] and slot['personMask'] == 2
        target = [n for n in native if (n['format'], n['type'], n['sheet'], n['frame']) == (fmt, 5, 0x51, frame)]
        origin = [n for n in native if (n['format'], n['type'], n['sheet'], n['frame']) == (fmt, 5, 0x49, source_frame)]
        assert len(target) == len(origin) == 1, 'Review resource variants explicitly'
        n, old = target[0], origin[0]
        assert (n['width'], n['height'], n['native_signature']) == (old['width'], old['height'], old['native_signature'])
        assert n['resource_sha256'] == old['resource_sha256']
        box = list(Image.open(atlas / n['reference']).getchannel('A').getbbox())
        for asset in original['assets']:
            assert 'native_formats' not in asset and sha(source / asset['file']) == asset['sha256']
            d = asset['density']
            bounds = Image.open((source / asset['file']).with_suffix('.png')).getchannel('A').getbbox()
            assert box[0]*d <= bounds[0] < bounds[2] <= box[2]*d
            assert box[1]*d <= bounds[1] < bounds[3] == box[3]*d
        rows.append(dict(format=fmt, native_signature=n['native_signature'], bbox=box))
        proof.append(dict(format=fmt, type=5, person=1, sheet=0x51, frame=frame,
                          source_sheet=0x49, source_frame=source_frame,
                          resource_sha256=n['resource_sha256'], native_signature=n['native_signature']))
    m = copy.deepcopy(original)
    m['pose'] = dict(type=5, sheet=0x51, frame=frame)
    m['assets'] = []
    m['export']['native'] = rows
    m['authoring_reuse'] = dict(source_manifest=(source / 'manifest.json').relative_to(ROOT).as_posix(),
        source_sha256=sha(source / 'source.png'), generation_metadata_sha256=sha(source / 'generation.json'),
        reason='Both full native signatures/dimensions and own anchors equal; no runtime alias')
    out.mkdir(parents=True)
    shutil.copyfile(source / 'source.png', out / 'source.png')
    for asset in original['assets']:
        a = copy.deepcopy(asset)
        a['id'] = f"enemy-v2-pose-51-f{frame}-{a['density']}x"
        a['file'] = a['id'] + '.rgba'
        shutil.copyfile(source / asset['file'], out / a['file'])
        shutil.copyfile((source / asset['file']).with_suffix('.png'), (out / a['file']).with_suffix('.png'))
        m['assets'].append(a)
    (out / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n', encoding='utf-8')
    generation = dict(generator='reuse existing E01 source and derivatives; no ImageGen call',
        identity=2, source_sha256=sha(source / 'source.png'), original_generation_metadata=(source / 'generation.json').relative_to(ROOT).as_posix(),
        original_generation_metadata_sha256=sha(source / 'generation.json'), native_cases=proof,
        review='Exact native equivalence and own bounds; gameplay/shadow acceptance pending')
    (out / 'generation.json').write_text(json.dumps(generation, indent=2) + '\n', encoding='utf-8')
    print(f'PASS51/F{frame}:2native signatures and copied E01 derivatives; no runtime alias')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--frame', type=int, choices=(0, 2), required=True)
    p.add_argument('--atlas', type=Path, required=True)
    args = p.parse_args()
    reuse(args.frame, args.atlas)
