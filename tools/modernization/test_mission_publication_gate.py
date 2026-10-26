"""A completed replay with a recoverable sanitizer warning must still fail."""
import unittest
from check_mission_publication_replays import sanitizer_findings, verify_pause_probe, verify_soldier_probe


class PublicationGateTests(unittest.TestCase):
    def test_soldier_probe_requires_each_scene(self):
        a='SOLDIER_SEMANTIC: verified original resource in mission composition scene=13\n'
        b=a.replace('13', '42')
        self.assertEqual(verify_soldier_probe(a+b, 2), 2)
        for log in ('', a, a+a):
            with self.assertRaises(RuntimeError):
                verify_soldier_probe(log, 2)

    def test_pause_probe_requires_unique_complete_pairs(self):
        a='MISSION_PAUSE_PROBE: completed PC Format:1:1:8\nMISSION_PAUSE_PROBE: resumed PC Format:1:1:8\n'
        b=a.replace(':8', ':16')
        self.assertEqual(verify_pause_probe(a+b, 1), 2)
        for log in ('', a, a+a, a+b.replace('resumed', 'missing')):
            with self.subTest(log=log), self.assertRaises(RuntimeError):
                verify_pause_probe(log, 1)

    def test_successful_completion_does_not_hide_recoverable_findings(self):
        for finding in ('source.cpp:42: runtime error: signed integer overflow',
                        'WARNING: ThreadSanitizer: data race',
                        'ERROR: LeakSanitizer: detected memory leaks',
                        'SUMMARY: AddressSanitizer: heap-buffer-overflow',
                        'AddressSanitizer:DEADLYSIGNAL'):
            with self.subTest(finding=finding):
                self.assertEqual(sanitizer_findings(finding+'\n::notice::Test PC: Phase Complete (1ms) [Passed]\n'), [finding])

    def test_clean_diagnostic_markers_are_not_errors(self):
        self.assertEqual(sanitizer_findings('MISSION_LAYER_AUDIT: verified real producer interval\nMISSION_LAYER_PRESENT: published verified orders\n'), [])


if __name__ == '__main__':
    unittest.main()
