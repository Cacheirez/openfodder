"""Pin the reviewed Window adapter and its unchanged predecessor.
The functional Window/Mouse suite tests the accepted implementation. These
hashes protect entire source files, not gameplay reference states.
GPL-3.0-or-later.
"""
import hashlib
CLASSIC = 'ba86d285726380e33855d5de583d9cae6f51ea9d7a2ca281e64c488e31ba1208'
INTEGRATED = 'fc1dd9e8aeaebdad881ff8b7dc9e9fe95e82ac5874432804b7e0c7e6ff0f6a29'

def verify_window_integration(current, original):
    digest=lambda s:hashlib.sha256(s.encode()).hexdigest()
    assert digest(original)==CLASSIC, "Unexpected classic Window baseline"
    assert digest(current)==INTEGRATED, "Window adapter changed; review its real-method integration tests"
