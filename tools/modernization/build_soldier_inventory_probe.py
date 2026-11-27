"""Emit a diagnostic copy of the actual producer; never edit the shipped engine.
GPL-3.0-or-later. Records prepared first-player bodies, not final HD eligibility.
"""
from pathlib import Path
import argparse
ROOT=Path(__file__).resolve().parents[2]
NEEDLE='        state.segment = metadata->mLoadSegment;\n'
PROBE=r'''        std::fprintf(stderr,"PILOT_BODY: %d %d %d %zu %d %d %d %d %d %d %d %d %d %d %d %d %d\n",
            int(mGame_Data.mMission_Number),int(mGame_Data.mMission_Phase),int(state.tick),slot,
            int(sheet),int(frame),int(state.animation),int(sprite->mFaceDirection),int(state.direction),
            int(input.columns),int(input.rows),int(input.modX),int(input.modY),int(input.rowsToSkip),
            int(sprite->mInWater),int(sprite->mFiredWeaponType),int(state.segment));
'''
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--emit',type=Path,required=True);a=ap.parse_args()
    source=(ROOT/'Source/Sprites/Sprite_Core.cpp').read_text()
    assert source.count(NEEDLE)==1,'Producer changed; inspect before instrumenting'
    a.emit.write_text(source.replace(NEEDLE,NEEDLE+PROBE))
