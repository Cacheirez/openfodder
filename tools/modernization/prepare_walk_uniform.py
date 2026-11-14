"""Shared export of direction-specific option A masters. GPL-3.0-or-later."""
import json

from PIL import Image

from prepare_c01_uniform_sample import (
    OPTIONS, digest, recolour, uniform_mask, verify, verify_protected,
)
from prepare_walk24 import CONFIG, ROOT


def prepare(out, sheet, panels, protected):
    frames = [frame for frame in json.loads(CONFIG.read_text())["frames"] if frame["sheet"] == sheet]
    out.mkdir(parents=True, exist_ok=True)
    for frame in frames:
        number = frame["frame"]
        source_path = ROOT / "assets/modernization" / frame["asset"]
        if digest(source_path.read_bytes()) != frame["source_sha256"]:
            raise ValueError(f"Master hash mismatch: {source_path}")
        with Image.open(source_path) as image:
            source = image.convert("RGBA")
        crop = frame["crop"]
        mask = uniform_mask(source, crop, panels[number])
        master = recolour(source, mask, OPTIONS["A"])
        changes = verify(source, master, mask)
        verify_protected(source, master, crop, protected[number])
        path = out / f"s{sheet}-f{number}-verde-a.png"
        with path.open("xb") as stream:
            master.save(stream, format="PNG")
        print(f"{path.name} {digest(path.read_bytes())} mask={digest(mask.tobytes())} pixels={changes}")
