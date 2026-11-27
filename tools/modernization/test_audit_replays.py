"""Regression checks for the audit gate, not for Cannon Fodder gameplay."""
import unittest
from audit_replays import parse_log, evaluate


class AuditTests(unittest.TestCase):
    def report(self, log):
        return dict(parse_log(log), timed_out=False, returncode=0, campaign=None, verdict="PASS")

    good = "::notice::Test Demo - Mission 1 Phase 1: Phase Complete (42ms) [Passed]"

    def test_completed_phase(self):
        self.assertEqual(evaluate(self.report(self.good)), [])

    def test_campaign_success_without_phases_is_empty(self):
        self.assertTrue(evaluate(self.report("::notice::Test Campaign - Demo:  (1ms) [Passed]")))

    def test_skipped_not_counted_as_pass(self):
        r = self.report(self.good+"\n::notice::Test Demo - Mission 2: No test found (0ms) [Skipped]")
        self.assertEqual(r["phases_passed"], 1)
        self.assertTrue(evaluate(r))
        self.assertEqual(evaluate(r, allow_skips=True), [])

    def test_error_even_with_zero_exit(self):
        self.assertTrue(evaluate(self.report(self.good+"\n::error::Phase failed")))

    def test_crash_and_timeout(self):
        for change in ({"returncode": -11}, {"timed_out": True}):
            r = self.report(self.good)
            r.update(change)
            self.assertTrue(evaluate(r))

    def test_reference_ignores_timing_but_not_missing_tests(self):
        baseline = self.report(self.good)
        self.assertEqual(evaluate(self.report(self.good.replace("42ms", "900ms")), baseline), [])
        self.assertTrue(evaluate(self.report(self.good.replace("Phase 1:", "Phase 2:")), baseline))
        self.assertTrue(evaluate(self.report(self.good+"\n"+self.good), baseline))

    def test_failed_reference_rejected(self):
        baseline = self.report(self.good)
        baseline["verdict"] = "FAIL"
        self.assertTrue(evaluate(self.report(self.good), baseline))

    def test_different_campaign_rejected(self):
        baseline = self.report(self.good)
        baseline["campaign"] = "Other"
        self.assertTrue(evaluate(self.report(self.good), baseline))


if __name__ == "__main__":
    unittest.main()
