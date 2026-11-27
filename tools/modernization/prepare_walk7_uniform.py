"""Reproduce the option A masters for walking direction 7. GPL-3.0-or-later."""
import argparse
import json
from pathlib import Path

from PIL import Image

from prepare_c01_uniform_sample import (
    OPTIONS, PANELS, PROTECTED, digest, recolour, uniform_mask, verify, verify_protected,
)
from prepare_walk24 import CONFIG, ROOT

# Same 397 × 600 inspection grid as C01. The upper panels follow the same
# silhouette, while the trouser panels follow the moving knees and cuffs.
TROUSERS = {
    1: (
        ((105, 377), (141, 395), (177, 402), (190, 416), (192, 466),
         (170, 485), (143, 486), (119, 477), (99, 449), (98, 417)),
        ((201, 407), (224, 417), (249, 423), (277, 424), (283, 442),
         (270, 466), (249, 485), (220, 488), (201, 470), (194, 440)),
    ),
    2: (
        ((106, 380), (147, 395), (177, 402), (187, 416), (169, 443),
         (167, 471), (150, 493), (121, 509), (104, 506), (91, 481),
         (88, 454), (98, 428), (99, 406)),
        ((198, 405), (222, 415), (245, 420), (269, 424), (269, 438),
         (253, 452), (227, 457), (207, 452), (188, 442)),
    ),
}


def prepare(out):
    frames = [frame for frame in json.loads(CONFIG.read_text())["frames"] if frame["sheet"] == 7]
    out.mkdir(parents=True, exist_ok=True)
    for frame in frames:
        number = frame["frame"]
        source_path = ROOT / "assets/modernization" / frame["asset"]
        if digest(source_path.read_bytes()) != frame["source_sha256"]:
            raise ValueError(f"Master hash mismatch: {source_path}")
        with Image.open(source_path) as image:
            source = image.convert("RGBA")
        crop = frame["crop"]
        if number == 0:
            panels, protected = PANELS, PROTECTED
        else:
            panels = PANELS[:6] + TROUSERS[number]
            protected = {
                **PROTECTED,
                "left boot": (132, 514, 165, 554) if number == 1 else (100, 532, 136, 578),
                "right boot": (213, 520, 249, 558) if number == 1 else (218, 468, 247, 497),
            }
        mask = uniform_mask(source, crop, panels)
        master = recolour(source, mask, OPTIONS["A"])
        changes = verify(source, master, mask)
        verify_protected(source, master, crop, protected)
        path = out / f"s7-f{number}-verde-a.png"
        with path.open("xb") as stream:
            master.save(stream, format="PNG")
        print(f"{path.name} {digest(path.read_bytes())} mask={digest(mask.tobytes())} pixels={changes}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    prepare(parser.parse_args().out)
