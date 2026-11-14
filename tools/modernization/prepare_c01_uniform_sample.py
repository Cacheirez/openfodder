"""Prepare the C01 (7/0) uniform colour sample. GPL-3.0-or-later."""
import argparse
import hashlib
import re
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from prepare_walk_art_review import png

SOURCE = Path(__file__).resolve().parents[2] / "assets/modernization/soldier-c01/source.png"
SOURCE_SHA = "9fb5dd519e8589de6c6420e4385c8eb2e12ac1f24c83f9a64678a2d943e31c77"
CROP = (406, 176, 969, 1026)
OPTIONS = {"A": (0.77, 0.90, 0.83), "B": (0.60, 0.81, 0.80)}
GRID = (397, 600)

# Inspection grid of the approved alpha crop, 397 by 600. Trace the textile
# panels separately to exclude face, hands, leather, rifle and boots.
PANELS = (
    ((57, 0), (330, 0), (337, 169), (300, 206), (235, 225), (160, 223),
     (110, 203), (58, 168)),
    ((0, 216), (56, 172), (71, 171), (98, 193), (90, 247), (87, 271),
     (105, 288), (84, 308), (68, 339), (37, 332), (0, 304)),
    ((306, 202), (328, 211), (363, 302), (351, 363), (332, 378), (331, 364),
     (318, 350), (303, 343), (286, 345), (275, 349), (278, 317), (291, 296)),
    ((136, 215), (149, 238), (174, 255), (191, 275), (229, 258), (260, 236),
     (254, 273), (249, 310), (213, 297), (185, 272), (157, 259), (134, 242)),
    ((194, 276), (218, 259), (252, 259), (249, 307), (232, 305)),
    ((108, 345), (121, 359), (143, 369), (167, 362), (188, 358), (203, 359),
     (207, 396), (190, 405), (178, 397), (147, 396), (102, 384)),
    ((105, 383), (150, 396), (187, 403), (192, 430), (171, 453), (147, 465),
     (109, 464), (78, 432), (83, 410)),
    ((199, 398), (229, 417), (247, 417), (267, 425), (290, 425), (306, 418),
     (315, 444), (314, 470), (301, 482), (269, 500), (229, 488), (211, 460)),
)
PROTECTED = {
    "face": (174, 226, 235, 249),
    "right hand": (273, 386, 288, 408),
    "left hand": (101, 308, 153, 335),
    "strap": (272, 245, 286, 278),
    "rifle": (178, 297, 197, 316),
    "left boot": (118, 494, 156, 543),
    "right boot": (260, 528, 309, 562),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def ramp(value, start, end):
    return min(1, max(0, (value - start) / (end - start)))


def source_point(x, y, crop=CROP):
    left, top, right, bottom = crop
    return (round(left + x * (right - left) / GRID[0]),
            round(top + y * (bottom - top) / GRID[1]))


def uniform_mask(source, crop=CROP, panels=PANELS):
    outline = Image.new("L", source.size)
    draw = ImageDraw.Draw(outline)
    for panel in panels:
        draw.polygon([source_point(x, y, crop) for x, y in panel], fill=255)
    outline = outline.filter(ImageFilter.GaussianBlur(2))
    hue, saturation, _ = source.convert("HSV").split()
    alpha = source.getchannel("A")
    # A soft chroma gate preserves warm leather and skin, and dark neutral metal.
    weights = bytes(round(region * ramp(h, 28, 35) * ramp(-h, -60, -49)
                          * ramp(s, 22, 62)) if a >= 16 else 0
                    for region, h, s, a in zip(outline.tobytes(), hue.tobytes(),
                                              saturation.tobytes(), alpha.tobytes()))
    return Image.frombytes("L", source.size, weights)


def recolour(source, mask, factors):
    rgb = source.convert("RGB").tobytes()
    edited = bytes(round(value * (1 - mask_value / 255 * (1 - factors[channel])))
                   for index, mask_value in enumerate(mask.tobytes())
                   for channel, value in enumerate(rgb[index*3:index*3+3]))
    result = Image.frombytes("RGB", source.size, edited)
    result.putalpha(source.getchannel("A"))
    return result


def derive(builder, source, scratch, density):
    header = scratch / "pixels.hpp"
    subprocess.run([builder, source, header, str(density)], check=True)
    packed = [int(value) for value in re.findall(r"(\d+)u", header.read_text())]
    size = (16 * density, 14 * density)
    rgba = bytes(v for c in packed for v in ((c >> 16) & 255, (c >> 8) & 255, c & 255, c >> 24))
    return Image.frombytes("RGBA", size, rgba)


def verify(current, edited, mask):
    if current.size != edited.size or current.getchannel("A").tobytes() != edited.getchannel("A").tobytes():
        raise ValueError("Geometry or alpha changed")
    changes = sum(a != b for a, b in zip(current.getdata(), edited.getdata()))
    if not changes or any(a != b and not weight
                          for a, b, weight in zip(current.getdata(), edited.getdata(), mask.getdata())):
        raise ValueError("Missing recolour or change outside the mask")
    return changes


def verify_protected(source, master, crop=CROP, regions=PROTECTED):
    for name, (left, top, right, bottom) in regions.items():
        box = (*source_point(left, top, crop), *source_point(right, bottom, crop))
        if source.crop(box).tobytes() != master.crop(box).tobytes():
            raise ValueError(f"Protected region changed: {name}")


def derivative_mask(source, mask, scratch, builder, density):
    # Build a white marker only in affected input pixels, using the same
    # alpha and the exact same area bins as the production derivative.
    marker = mask.point(lambda value: 255 if value else 0).convert("RGB")
    marker.putalpha(source.getchannel("A"))
    path = scratch / "marker.png"
    marker.save(path)
    return derive(builder, path, scratch, density).getchannel("R")


def compare(captures, out, density, sprites, font):
    prefix = f"C01_{density}"
    html = (captures / f"{prefix}.html").read_text(encoding="utf-8")
    position = re.search(r"x=(\d+),y=(\d+),density=(\d+),sceneId=(\d+)", html)
    x, y, recorded_density, scene = map(int, position.groups())
    if recorded_density != density or scene != 815 or (x, y) != (155, 56):
        raise ValueError("Expected the PC Format capture of C01, scene 815")
    box = (x, y, x+16, y+14)
    background = Image.open(captures / f"{prefix}_fondo.bmp").convert("RGBA")
    classic = Image.open(captures / f"{prefix}_clasico.bmp").convert("RGBA")
    patch = Image.open(captures / f"{prefix}_parche.bmp").convert("RGB")
    ground = background.crop(box).resize(sprites[0].size, Image.Resampling.NEAREST)
    overlays = [Image.alpha_composite(ground, sprite) for sprite in sprites]
    if overlays[0].convert("RGB").tobytes() != patch.tobytes():
        raise ValueError("Current C01 does not reproduce the recorded SDL patch")

    close_size = (192, 168)
    terrain_box = (x-20, y-16, x+36, y+30)
    board = Image.new("RGB", (960, 488), "#18221d")
    draw = ImageDraw.Draw(board)
    title = ImageFont.truetype(font, size=24)
    caption = ImageFont.truetype(font, size=18)
    draw.text((24, 14), f"C01 · Marcha 7/0 · Recurso {density}×", font=title, fill="#f0f4ed")
    draw.text((24, 456), "Arriba, ampliación de la pose. Abajo, recorte de terreno a 4×.", font=caption,
              fill="#c6d1c7")
    for i, (label, overlay) in enumerate(zip(("Clásico", "C01 actual", "A", "B"), [None, *overlays])):
        left = 24 + 232*i
        draw.text((left, 56), label, font=caption, fill="#f0f4ed")
        if overlay is None:
            close = classic.crop(box).resize(close_size, Image.Resampling.NEAREST)
            terrain = classic.crop(terrain_box).resize((224, 184), Image.Resampling.NEAREST)
        else:
            close = overlay.resize(close_size, Image.Resampling.LANCZOS)
            terrain = background.crop(terrain_box).resize((224, 184), Image.Resampling.NEAREST)
            terrain.paste(overlay.resize((64, 56), Image.Resampling.BOX), (80, 64))
        board.paste(close, (left, 82))
        board.paste(terrain, (left, 258))
    board.save(out / f"comparacion-local-{density}x.png")
    print(f"{density}x: current C01 matches the recorded SDL patch")


def prepare(args):
    if digest(SOURCE.read_bytes()) != SOURCE_SHA:
        raise ValueError("C01 source hash mismatch")
    args.out.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGBA")
    mask = uniform_mask(source)
    print(f"mask L SHA-256 {digest(mask.tobytes())}")
    with TemporaryDirectory(dir=args.out) as temporary:
        scratch = Path(temporary)
        masters = {}
        for name, factors in OPTIONS.items():
            master = recolour(source, mask, factors)
            changed = verify(source, master, mask)
            verify_protected(source, master)
            path = scratch / f"{name}.png"
            master.save(path)
            masters[name] = path
            print(f"{name} master: {changed} changed pixels; RGBA SHA-256 {digest(master.tobytes())}")
        for density in (8, 12):
            original = derive(args.builder, SOURCE, scratch, density)
            if args.reference_rgba and original.tobytes() != (
                    args.reference_rgba / f"s7-f0-{density}.rgba").read_bytes():
                raise ValueError("C01 differs from the previously verified walk asset")
            support = derivative_mask(source, mask, scratch, args.builder, density)
            sprites = [original]
            for name, master_path in masters.items():
                sprite = derive(args.builder, master_path, scratch, density)
                changed = verify(original, sprite, support)
                asset = png(*sprite.size, sprite.tobytes())
                (args.out / f"c01-verde-{name.lower()}-{density}x.png").write_bytes(asset)
                print(f"{name} {density}x: {changed} changed pixels; PNG SHA-256 {digest(asset)}")
                sprites.append(sprite)
            if args.captures:
                compare(args.captures, args.out, density, sprites, args.font)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--builder", type=Path, required=True, help="openfodder_art_builder executable")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--reference-rgba", type=Path, help="optional verified walk asset directory")
    parser.add_argument("--captures", type=Path, help="local C01_8/12 HTML and BMP exports")
    parser.add_argument("--font", default="arial.ttf", help="TrueType font for the local comparisons")
    prepare(parser.parse_args())
