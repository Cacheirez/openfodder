"""Regression tests for the narrow H2 index/ASan gate. GPL-3.0-or-later."""
import unittest
from check_ubsan_indices import assess

GOOD = {"verdict":"PASS","phases_passed":29,"skipped":0,"returncode":0}

class IndexGateTests(unittest.TestCase):
    def test_nominal(self):
        self.assertEqual(assess(GOOD, "No issues")[0], [])
    def test_existing_nonindex_warnings_not_hidden(self):
        defects, indices, others = assess(GOOD, 
            "Source/Camera.cpp:305: runtime error: left shift of negative value -1\n"
            "Source/stdafx.hpp:92: runtime error: load of misaligned address")
        self.assertEqual(defects, [])
        self.assertEqual(len(indices), 0)
        self.assertEqual(len(others), 2)
    def test_index_is_failure(self):
        defects, indices, _ = assess(GOOD, 
            "Source/Sprites/Sprite_Core.cpp:2036: runtime error: index 9 out of bounds for type 'sSprite *[9]'")
        self.assertTrue(defects)
        self.assertEqual(len(indices), 1)
    def test_asan_is_failure(self):
        self.assertTrue(assess(GOOD, "ERROR: AddressSanitizer: global-buffer-overflow")[0])
    def test_incomplete_replay_is_failure(self):
        self.assertTrue(assess({**GOOD,"phases_passed":11}, "")[0])

if __name__ == "__main__":
    unittest.main()
