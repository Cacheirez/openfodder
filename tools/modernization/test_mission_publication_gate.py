"""A completed replay with a recoverable sanitizer warning must still fail."""
import unittest
from check_mission_publication_replays import sanitizer_findings


class PublicationGateTests(unittest.TestCase):
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
