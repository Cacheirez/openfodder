"""Pin the reviewed Window adapter and its unchanged predecessor.
The functional Window/Mouse suite tests the accepted implementation. These
hashes protect entire source files, not gameplay reference states.
GPL-3.0-or-later.
"""
import hashlib
CLASSIC = 'ba86d285726380e33855d5de583d9cae6f51ea9d7a2ca281e64c488e31ba1208'
INTEGRATED = '33f5dd69d085d5440a9037224915b4ae5b981959a4d53217d1f62df04f5e9b7e'

def verify_window_integration(current, original):
    digest=lambda s:hashlib.sha256(s.encode()).hexdigest()
    assert digest(original)==CLASSIC, "Unexpected classic Window baseline"
    assert digest(current)==INTEGRATED, "Window adapter changed; review its real-method integration tests"
