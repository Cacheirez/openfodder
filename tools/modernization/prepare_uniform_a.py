"""Reproduce the batch of option A masters and RGBA hashes. GPL-3.0-or-later."""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from prepare_c01_uniform_sample import OPTIONS, digest, recolour, uniform_mask, verify
from prepare_walk_art_review import ROOT, derive_frame


FAMILIES = ('walk24', 'aim', 'grenade', 'rocket')
ASSETS = ROOT / 'assets/modernization'
CROP_PANEL = (((0, 0), (397, 0), (397, 600), (0, 600)),)

# Coordinates in the crop, normalised to the 86 × 129 review grid.
# Grenades are held in frames 0 and 1. Frame 2 has an empty throwing hand.
GRENADES = {
    8: ((11, 41, 32, 62), (13, 0, 31, 17)),
    9: ((10, 42, 25, 61), (17, 0, 34, 17)),
    10: ((27, 47, 43, 67), (73, 0, 86, 17)),
    11: ((74, 43, 86, 57), (40, 0, 55, 15)),
    12: ((66, 35, 81, 48), (55, 0, 73, 17)),
    13: ((46, 38, 62, 56), (53, 1, 66, 17)),
    14: ((25, 40, 47, 57), (9, 0, 30, 18)),
    15: ((10, 42, 28, 57), (9, 0, 32, 18)),
}

# Weapon silhouettes cover the common position of the tube in the three
# retained frames. Include the coloured rings and both ends of the tube.
ROCKETS = {
    57: ((0, 24), (15, 20), (22, 35), (34, 43), (48, 52), (59, 74),
         (68, 79), (68, 100), (39, 100), (38, 81), (31, 62),
         (22, 49), (10, 44), (0, 39)),
    58: ((0, 76), (33, 53), (63, 36), (66, 22), (86, 20),
         (86, 44), (65, 51), (38, 71), (0, 101)),
    59: ((0, 43), (34, 46), (60, 44), (86, 38),
         (86, 63), (57, 62), (39, 66), (0, 67)),
    60: ((0, 14), (17, 17), (33, 28), (55, 37), (86, 38),
         (86, 61), (61, 59), (42, 50), (21, 39), (0, 32)),
    61: ((12, 0), (27, 0), (29, 22), (26, 38), (31, 48),
         (37, 61), (37, 73), (8, 73), (8, 58), (15, 43)),
    62: ((15, 47), (34, 43), (51, 28), (69, 16), (86, 10),
         (86, 28), (65, 40), (44, 53), (36, 65), (15, 65)),
    63: ((0, 44), (23, 44), (42, 48), (86, 43),
         (86, 68), (39, 65), (20, 70), (0, 70)),
    64: ((0, 26), (14, 26), (35, 47), (59, 62), (86, 74),
         (86, 95), (69, 95), (44, 77), (21, 62), (0, 49)),
}


def equipment_mask(source, crop, sheet, number):
    left, top, right, bottom = crop

    def point(x, y):
        return (round(left + x * (right - left) / 86),
                round(top + y * (bottom - top) / 129))

    equipment = Image.new('L', source.size)
    draw = ImageDraw.Draw(equipment)
    if sheet in ROCKETS:
        draw.polygon([point(*vertex) for vertex in ROCKETS[sheet]], fill=255)
    if sheet in GRENADES and number < 2:
        x1, y1, x2, y2 = GRENADES[sheet][number]
        draw.rectangle((*point(x1, y1), *point(x2, y2)), fill=255)
    return equipment


def prepare_frame(out, frame, family, builders, recorded):
    sheet, number = frame['sheet'], frame['frame']
    path = ASSETS / frame['asset']
    if digest(path.read_bytes()) != frame['source_sha256']:
        raise ValueError(f'master hash mismatch: {path}')
    with Image.open(path) as image:
        source = image.convert('RGBA')
    crop = frame['crop']
    mask = uniform_mask(source, crop, CROP_PANEL)
    equipment = equipment_mask(source, crop, sheet, number)
    protected = ImageChops.lighter(equipment, equipment.filter(ImageFilter.GaussianBlur(3)))
    mask = ImageChops.multiply(mask, ImageChops.invert(protected))
    master = recolour(source, mask, OPTIONS['A'])
    changes = verify(source, master, mask)

    asset = Path(f'soldier-{family}/uniform-a/s{sheet}-f{number}-verde-a.png')
    target = out / asset
    target.parent.mkdir(parents=True, exist_ok=True)
    master.save(target)
    result = dict(asset=asset.as_posix(), source_sha256=digest(target.read_bytes()),
                  rgba_sha256={})
    scratch = out / 'derivatives'
    scratch.mkdir(exist_ok=True)
    for density in (8, 12):
        descriptor, _ = derive_frame(scratch, {**frame, 'asset': target.resolve()}, density, *builders)
        result['rgba_sha256'][str(density)] = descriptor['sha256']
    if recorded and result != recorded:
        raise ValueError(f'reproduction mismatch: {asset}')
    print(f'{asset.name}: {changes} RGB pixels; mask {digest(mask.tobytes())}', flush=True)
    return result


def prepare(out, builders):
    out.mkdir(parents=True, exist_ok=False)
    for family in FAMILIES:
        config_path = ASSETS / f'soldier-{family}/manifest.json'
        config = json.loads(config_path.read_text())
        for frame in config['frames']:
            if family == 'walk24' and frame['sheet'] >= 4:
                continue
            original = {k: v for k, v in frame.items() if k != 'uniform_a'}
            frame['uniform_a'] = prepare_frame(out, original, family, builders, frame.get('uniform_a'))
        (out / f'soldier-{family}/manifest.json').write_text(json.dumps(config, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('out', 'c01-builder', 'batch-builder', 'asset-builder'):
        parser.add_argument('--' + name, type=lambda value: Path(value).resolve(), required=True)
    args = parser.parse_args()
    prepare(args.out, (args.c01_builder, args.batch_builder, args.asset_builder))
