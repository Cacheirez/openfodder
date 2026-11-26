"""Copy one verified E01 sliding master to its own initial-person contract."""
import argparse
import copy
import json
import shutil
from pathlib import Path
from PIL import Image
from inventory_enemy_states import ROOT
from generate_enemy_pose_table import contracts
from reuse_enemy_fall_pose import sha


def reuse(direction, atlas, out=None):
    assert direction in range(8)
    source = ROOT / f'assets/modernization/demo-a1-enemy-v2-pose-a7-f{direction}'
    out = out or ROOT / f'assets/modernization/demo-a1-enemy-v2-pose-a4-f{direction}'
    assert not out.exists(), 'Preserve previous exports'
    original = json.loads((source / 'manifest.json').read_text(encoding='utf-8'))
    generation = json.loads((source / 'generation.json').read_text(encoding='utf-8'))
    assert original['enemy_identity'] == 2 and sha(source / 'source.png') == original['source']['sha256']
    reference = f'assets/modernization/demo-a1-player-pose-a4-f{direction}/source.png'
    assert generation['references'][0] == reference and (ROOT / reference).is_file()
    friendly = json.loads((ROOT / reference).with_name('manifest.json').read_text(encoding='utf-8'))
    placement = original['export']['placement']
    body_bottom = friendly['export']['placement']['y'] + friendly['export']['placement']['height']
    assert placement['y'] + placement['height'] == body_bottom
    native = json.loads((atlas / 'native-audit.json').read_text(encoding='utf-8'))
    rows, proof = [], []
    for fmt in (0, 1):
        slot = next(s for s in contracts() if (s['format'], s['type'], s['sheet'], s['frame']) == (fmt, 5, 0xa4, direction))
        assert slot['produced'] and slot['personMask'] == 1
        matches = [n for n in native if (n['format'], n['type'], n['sheet'], n['frame']) == (fmt, 5, 0xa4, direction)]
        assert len(matches) == 1, 'Review resource variants explicitly'
        n = matches[0]
        reference_native = next(x for x in friendly['export']['native'] if x['format'] == fmt)
        assert reference_native['native_signature'] == n['native_signature']
        box = list(Image.open(atlas / n['reference']).getchannel('A').getbbox())
        for asset in original['assets']:
            assert sha(source / asset['file']) == asset['sha256'] and 'native_formats' not in asset
            d = asset['density']
            bounds = Image.open((source / asset['file']).with_suffix('.png')).getchannel('A').getbbox()
            assert box[0]*d <= bounds[0] < bounds[2] <= box[2]*d
            assert box[1]*d <= bounds[1] < bounds[3] == body_bottom*d <= box[3]*d
        rows.append(dict(format=fmt, native_signature=n['native_signature'], bbox=box))
        proof.append(dict(format=fmt, type=5, person=0, sheet=0xa4, frame=direction,
                          resource_sha256=n['resource_sha256'], native_signature=n['native_signature']))
    m = copy.deepcopy(original)
    m['pose'] = dict(type=5, sheet=0xa4, frame=direction)
    m['assets'] = []
    m['export']['native'] = rows
    m['status'] = 'E01 initial sliding art reuse; ground runtime integration/gameplay pending'
    m['authoring_reuse'] = dict(source_manifest=(source / 'manifest.json').relative_to(ROOT).as_posix(),
        source_sha256=sha(source / 'source.png'), generation_metadata_sha256=sha(source / 'generation.json'),
        reason='Original pose reference and own initial native signature/body anchor verified; no runtime alias')
    m['source']['reused_from'] = (source / 'source.png').relative_to(ROOT).as_posix()
    out.mkdir(parents=True)
    shutil.copyfile(source / 'source.png', out / 'source.png')
    for asset in original['assets']:
        a = copy.deepcopy(asset)
        a['id'] = f"enemy-v2-pose-a4-f{direction}-{a['density']}x"
        a['file'] = a['id'] + '.rgba'
        shutil.copyfile(source / asset['file'], out / a['file'])
        shutil.copyfile((source / asset['file']).with_suffix('.png'), (out / a['file']).with_suffix('.png'))
        m['assets'].append(a)
    (out / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n', encoding='utf-8')
    g = dict(generator='reuse existing E01 master and derivatives; no ImageGen call', identity=2,
             source_sha256=sha(source / 'source.png'), reused_from=m['source']['reused_from'],
             original_generation_metadata=(source / 'generation.json').relative_to(ROOT).as_posix(),
             original_generation_metadata_sha256=sha(source / 'generation.json'),
             original_pose_reference=reference, pose_reference_sha256=sha(ROOT / reference),
             target=dict(type=5, person=0, sheet=0xa4, frame=direction, direction=direction),
             ground='Existing slide contact reused; initial-person runtime eligibility pending')
    (out / 'generation.json').write_text(json.dumps(g, indent=2) + '\n', encoding='utf-8')
    (out / 'reuse-evidence.json').write_text(json.dumps(dict(native_cases=proof, not_runtime_alias=True,
        source_sha256=g['source_sha256'], derivatives_copied_unchanged=True,
        body_lower_anchor=body_bottom, initial_person_zero=True), indent=2) + '\n', encoding='utf-8')
    return dict(direction=direction, native_cases=len(proof), assets=len(m['assets']), body_lower_anchor=body_bottom)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--direction', type=int, choices=range(8), required=True)
    p.add_argument('--atlas', type=Path, required=True)
    p.add_argument('--out', type=Path)
    a = p.parse_args()
    print(json.dumps(reuse(a.direction, a.atlas, a.out)))
