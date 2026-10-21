"""Guard the audited legacy visibility contract (H3.6).

Fail when a new read or write of mWasDrawn is added without explicitly
reviewing how it affects gameplay. No game resources required.
GPL-3.0-or-later.
"""
from collections import Counter
from pathlib import Path
import sys

EXPECTED = {
    "Source/Sprites.hpp": 1,                    # Declares state
    "Source/Sprites.cpp": 1,                    # Initializes state
    "Source/Sprites/Sprite_Core.cpp": 2,        # Sole runtime writer
    "Source/Sprites/Sprite_Civilian.cpp": 4,    # Gameplay decisions
    "Source/Sprites/Sprite_Effects.cpp": 2,     # Effects and map operations
    "Source/Sprites/Sprite_Projectiles.cpp": 1,
    "Source/Sprites/Sprite_Troop.cpp": 1,
    "Source/Sprites/Sprite_Vehicle.cpp": 1,
    "Source/GameplayTrace.cpp": 1,              # Read-only audit
}

def main():
    root = Path(__file__).resolve().parents[2]
    observed = Counter()
    for file in (root/"Source").rglob("*"):
        if file.suffix not in (".cpp", ".hpp") or not file.is_file():
            continue
        data = file.read_text(encoding="utf-8",errors="replace")
        count = data.count("mWasDrawn")
        if count:
            observed[file.relative_to(root).as_posix()] = count
    expected = Counter(EXPECTED)
    if observed != expected:
        print("FAIL: visibility field uses changed; re-audit before changing rendering")
        print("Expected:", dict(expected))
        print("Observed:", dict(observed))
        return 1
    print("PASS: H3.6 field references match the audited inventory:",
          sum(observed.values()), "occurrences across",len(observed),"files")
    return 0

if __name__ == "__main__":
    sys.exit(main())
