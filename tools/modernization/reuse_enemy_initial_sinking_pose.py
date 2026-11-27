"""Export one initial-person sinking pose from a verified E01 body master."""
import argparse
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image
from inventory_enemy_states import ROOT
from generate_enemy_pose_table import contracts
from reuse_enemy_fall_pose import sha


def reuse(frame, atlas, builders, work, out=None):
    assert frame in range(6)
    source = ROOT / f'assets/modernization/demo-a1-enemy-v2-pose-7a-f{frame}'
    out = out or ROOT / f'assets/modernization/demo-a1-enemy-v2-pose-38-f{frame}'
    assert not out.exists(), 'Preserve previous packages'
    original = json.loads((source / 'manifest.json').read_text(encoding='utf-8'))
    generation = json.loads((source / 'generation.json').read_text(encoding='utf-8'))
    assert original['enemy_identity'] == 2 and sha(source / 'source.png') == original['source']['sha256']
    reference = f'assets/modernization/demo-a1-player-pose-38-f{frame}/source.png'
    assert generation['references'][0] == reference and (ROOT / reference).is_file()
    friendly = json.loads((ROOT / reference).with_name('manifest.json').read_text(encoding='utf-8'))
    native = json.loads((atlas / 'native-audit.json').read_text(encoding='utf-8'))
    rows = []
    evidence = []
    for fmt in (0, 1):
        slot = next(s for s in contracts() if (s['format'], s['type'], s['sheet'], s['frame']) == (fmt, 5, 0x38, frame))
        assert slot['produced'] and slot['personMask'] == 1
        matches = [n for n in native if (n['format'], n['type'], n['sheet'], n['frame']) == (fmt, 5, 0x38, frame)]
        assert len(matches) == 1, 'Review resource-specific target explicitly'
        n = matches[0]
        ref = next(s for s in friendly['export']['native'] if s['format'] == fmt)
        assert ref['native_signature'] == n['native_signature']
        box = list(Image.open(atlas / n['reference']).getchannel('A').getbbox())
        rows.append(dict(format=fmt, native_signature=n['native_signature'], bbox=box))
        evidence.append(dict(format=fmt, type=5, person=0, sheet=0x38, frame=frame,
                             resource_sha256=n['resource_sha256'], native_signature=n['native_signature']))
    assert rows[0]['bbox'] == rows[1]['bbox']
    box = rows[0]['bbox']
    placement = original['export']['placement']
    assert placement['y'] + placement['height'] == box[3]
    fits = box[0] <= placement['x'] and placement['x'] + placement['width'] <= box[2]
    if fits:
        out.mkdir(parents=True)
        m = copy.deepcopy(original)
        m['pose'] = dict(type=5, sheet=0x38, frame=frame)
        m['export']['native'] = rows
        m['assets'] = []
        shutil.copyfile(source / 'source.png', out / 'source.png')
        for asset in original['assets']:
            a = copy.deepcopy(asset)
            a['id'] = f"enemy-v2-pose-38-f{frame}-{a['density']}x"
            a['file'] = a['id'] + '.rgba'
            shutil.copyfile(source / asset['file'], out / a['file'])
            shutil.copyfile((source / asset['file']).with_suffix('.png'), (out / a['file']).with_suffix('.png'))
            m['assets'].append(a)
    else:
        # Same master and scale, but this native mask needs its own horizontal anchor.
        width = placement['width']
        assert width <= box[2] - box[0]
        x = max(box[0], min(box[2] - width, round((box[0] + box[2] - width) / 2)))
        args = [sys.executable, str(ROOT / 'tools/modernization/export_enemy_pose.py'),
                '--identity', '2', '--source', str(source / 'source.png'), '--atlas', str(atlas),
                '--sheet', '0x38', '--frame', str(frame), '--family', 'pose',
                '--placement', f"{x},{placement['y']},{width},{placement['height']}",
                '--crop', ','.join(map(str, original['export']['crop'])),
                '--out', str(out), '--builders', str(builders), '--work', str(work)]
        subprocess.run(args, check=True)
        m = json.loads((out / 'manifest.json').read_text(encoding='utf-8'))
    for asset in m['assets']:
        d = asset['density']
        bounds = Image.open((out / asset['file']).with_suffix('.png')).getchannel('A').getbbox()
        assert box[0]*d <= bounds[0] < bounds[2] <= box[2]*d
        assert box[1]*d <= bounds[1] < bounds[3] == box[3]*d
    m['status'] = 'E01 initial sinking master reuse; runtime integration and Miguel gameplay pending'
    m['authoring_reuse'] = dict(source_manifest=(source / 'manifest.json').relative_to(ROOT).as_posix(),
        source_sha256=sha(source / 'source.png'), generation_metadata_sha256=sha(source / 'generation.json'),
        reason='Original friendly pose reference verified against own initial native signature; no runtime alias')
    m['source']['reused_from'] = (source / 'source.png').relative_to(ROOT).as_posix()
    (out / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n', encoding='utf-8')
    g = dict(generator='reuse existing E01 master; no ImageGen call', identity=2,
             source_sha256=sha(source / 'source.png'), reused_from=m['source']['reused_from'],
             original_generation_metadata=(source / 'generation.json').relative_to(ROOT).as_posix(),
             original_generation_metadata_sha256=sha(source / 'generation.json'),
             original_pose_reference=reference, pose_reference_sha256=sha(ROOT / reference),
             target=dict(type=5, person=0, sheet=0x38, frame=frame),
             derivatives_copied_unchanged=fits, ground='none; preserve native crop and independent commands')
    (out / 'generation.json').write_text(json.dumps(g, indent=2) + '\n', encoding='utf-8')
    (out / 'reuse-evidence.json').write_text(json.dumps(dict(native_cases=evidence,
        source_sha256=g['source_sha256'], derivatives_copied_unchanged=fits,
        not_runtime_alias=True, placement=m['export']['placement']), indent=2) + '\n', encoding='utf-8')
    return dict(frame=frame, native_cases=len(evidence), assets=len(m['assets']), copied=fits)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--frame', type=int, choices=range(6), required=True)
    for name in ('atlas', 'builders', 'work'):
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--out', type=Path)
    a = p.parse_args()
    print(json.dumps(reuse(a.frame, a.atlas, a.builders, a.work, a.out)))
