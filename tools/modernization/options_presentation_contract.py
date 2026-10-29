"""Pin the reviewed H5.6 menu while preserving the original surface-effects gate.
The transaction methods have their real-method fixture/CTest. This gate allows
only that exact menu revision, not arbitrary changes to palette callers.
GPL-3.0-or-later.
"""
import hashlib
from check_final_timer_equivalence import function

CLASSIC = '592f2e31a2a97c3f6921246b27c5b7df48116bfc708dd278e47c0aa77913f212'
INTEGRATED = '8948a6b35f9a1fbe1d92c75067ae814188f7ed0c41d78897404fbc8f3fa2e9af'
EFFECTS = ('->Save(', '->Restore(', '->palette_FadeTowardNew(', '->surfaceSetToPaletteNew(')

def verify_options_presentation(current, original):
    digest = lambda s: hashlib.sha256(s.encode()).hexdigest()
    assert digest(original) == CLASSIC, 'Unexpected classic options menu'
    assert digest(current) == INTEGRATED, 'Options menu changed; review transaction and palette scheduling'
    # Both explicit fades remain in Options_Menu_Run, before callback setup
    # and under the original palette-adjusting condition in the menu loop.
    def effect_lines(s):
        return [line.strip() for line in s.splitlines() if any(e in line for e in EFFECTS)]
    assert effect_lines(current) == effect_lines(original)
    signature = 'bool cFodder::Options_Menu_Run('
    for source in (current, original):
        body = function(source, signature)
        assert effect_lines(body) == effect_lines(source)
        assert 'if (mSurface->isPaletteAdjusting())\n            mSurface->palette_FadeTowardNew();' in body
        assert body.index('mSurface->palette_FadeTowardNew();') < body.index('mInterruptCallback = [this]')
