"""Negative checks for a static evidence manifest; these are not engine tests."""
import copy
import json
import unittest

from check_cd32_vehicle_capabilities import ROOT, MANIFEST, CENSUS, validate


class VehicleReviewTests(unittest.TestCase):
    def setUp(self):
        self.review = json.loads((ROOT / MANIFEST).read_text(encoding='utf-8'))
        self.census = json.loads((ROOT / CENSUS).read_text(encoding='utf-8'))

    def check(self, read=None):
        return validate(self.review, self.census, read or (lambda p: (ROOT / p).read_bytes()))

    def test_current_review(self):
        self.assertEqual(self.check()[1:], (7, 3))

    def test_changed_source_requires_review(self):
        path = self.review['sources'][0]['path']
        with self.assertRaisesRegex(ValueError, 'Source changed'):
            self.check(lambda p: (ROOT / p).read_bytes() + (b'\n' if p == path else b''))

    def test_windows_crlf_checkout(self):
        def crlf(path):
            return (ROOT / path).read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
        self.assertEqual(self.check(crlf)[1:], (7, 3))

    def test_real_change_in_crlf_is_rejected(self):
        path = self.review['sources'][0]['path']
        def changed(p):
            data = (ROOT / p).read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
            return data.replace(b'0x8B', b'0x8C') if p == path else data
        with self.assertRaisesRegex(ValueError, 'Source changed'):
            self.check(changed)

    def test_absent_type_is_not_covered(self):
        self.review['scenarios'][0]['types'].append(101)
        with self.assertRaisesRegex(ValueError, 'absent from SPT'):
            self.check()

    def test_wrong_graphics_reference(self):
        self.review['components'][0]['sheet'] = 0x8C
        with self.assertRaisesRegex(ValueError, 'another frame array'):
            self.check()

    def test_static_review_cannot_claim_execution(self):
        self.review['scenarios'][0]['execution'] = 'pass'
        with self.assertRaisesRegex(ValueError, 'runtime coverage'):
            self.check()

    def test_environment_mismatch(self):
        self.review['scenarios'][0]['resources'] = copy.deepcopy(self.review['scenarios'][1]['resources'])
        with self.assertRaisesRegex(ValueError, 'metadata differs'):
            self.check()


if __name__ == '__main__':
    unittest.main()
