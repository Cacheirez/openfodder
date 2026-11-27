import copy
import unittest
from enemy_native_formats import empty_signature, source_art_formats


class EnemyNativeFormatTests(unittest.TestCase):
    def setUp(self):
        self.guard = dict(type=5, sheet=0xdc, frame=0)
        self.proof = dict(format=1, segment=0, logical_size=[16, 14], bbox=None, opaque_pixels=0,
            native_signature=empty_signature(16, 14),
            resource_sha256='7a44b4a6dafa1350da974825ea1e2028fd5d3d946f415781966ea1cadc9bb134')
        self.export = dict(native=[dict(format=0)], native_no_write=[self.proof])

    def test_existing_two_format_contract_unchanged(self):
        self.assertEqual(source_art_formats(dict(type=5, sheet=0x42, frame=0),
            dict(native=[dict(format=0), dict(format=1)]), {0, 1}), {0, 1})

    def test_missing_art_format_needs_signed_empty_command(self):
        with self.assertRaises(AssertionError):
            source_art_formats(self.guard, dict(native=[dict(format=0)]), {0, 1})

    def test_guard_and_all_leader_frames_preserve_empty_amiga(self):
        poses = [self.guard] + [dict(type=106, sheet=s, frame=f)
            for s, count in ((0xd8, 24), (0xd9, 24), (0xda, 3)) for f in range(count)]
        self.assertEqual(len(poses), 52)
        for pose in poses:
            with self.subTest(pose=pose):
                self.assertEqual(source_art_formats(pose, self.export, {0, 1}), {0})

    def test_nonempty_unknown_or_changed_native_evidence_rejected(self):
        for key, value in [('native_signature', '0'*64), ('resource_sha256', '0'*64),
                           ('logical_size', [16, 13]), ('bbox', [0, 0, 1, 1]),
                           ('opaque_pixels', 1), ('format', 0), ('segment', 1)]:
            export = copy.deepcopy(self.export);export['native_no_write'][0][key] = value
            with self.subTest(field=key), self.assertRaises(AssertionError):
                source_art_formats(self.guard, export, {0, 1})

    def test_no_write_does_not_waive_other_enemy_artwork(self):
        for pose in [dict(type=5, sheet=0x42, frame=0), dict(type=36, sheet=0xdc, frame=0),
                     dict(type=106, sheet=0xd8, frame=24), dict(type=106, sheet=0xda, frame=3)]:
            with self.subTest(pose=pose), self.assertRaises(AssertionError):
                source_art_formats(pose, self.export, {0, 1})

    def test_duplicate_or_drawn_empty_format_rejected(self):
        for export in [dict(native=[dict(format=0), dict(format=0)]),
                       dict(native=[dict(format=0), dict(format=1)], native_no_write=[self.proof]),
                       dict(native=[dict(format=0)], native_no_write=[self.proof, self.proof])]:
            with self.subTest(export=export), self.assertRaises(AssertionError):
                source_art_formats(self.guard, export, {0, 1})


if __name__ == '__main__':
    unittest.main()
