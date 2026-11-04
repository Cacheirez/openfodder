import tempfile
import unittest
from pathlib import Path
from ordered_soldier_coverage import report


class OrderedCoverageTests(unittest.TestCase):
    def transaction(self, attempt=1, outcome='published', decision='replace', **counts):
        command = (f'SOLDIER_ORDERED_COMMAND: attempt={attempt} scene=2 interval=3 order=4 '
                   f'slot=0 generation=5 type=0 sheet=7 frame=0 key={"a"*64} decision={decision} density=8\n')
        summary = dict(expected=1, observed=1, replace=int(decision == 'replace'),
                       keep=int(decision == 'keep'), missing=int(decision == 'missing'), density=8)
        summary.update(counts)
        return command + f'SOLDIER_ORDERED_RESULT: attempt={attempt} outcome={outcome} ' + ' '.join(f'{k}={v}' for k, v in summary.items()) + '\n'

    def run_log(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'engine.log'
            path.write_text(text)
            return report([path])

    def test_repeated_presentation_is_one_producer_command(self):
        result = self.run_log(self.transaction() + self.transaction(2))
        self.assertEqual(result['attempts'], 2)
        self.assertEqual(result['published_command_presentations'], 2)
        self.assertEqual(result['unique_producer_commands'], 1)
        self.assertEqual(result['unique_published_variant_commands'], 1)
        self.assertEqual(len(result['entity_states']), 1)
        self.assertEqual(result['entity_states'][0]['published_presentations'], 2)
        self.assertEqual(result['verdict'], 'PENDING')

    def test_recovery_and_missing_are_not_publication(self):
        for outcome, decision in [('missing-variant', 'missing'), ('classic-recovered', 'replace'),
                                  ('recovery-failed', 'replace'), ('no-body', 'keep'), ('interrupted', 'replace')]:
            result = self.run_log(self.transaction(outcome=outcome, decision=decision))
            self.assertEqual(result['published_command_presentations'], 0)
            self.assertEqual(result['unique_published_variant_commands'], 0)

    def test_partial_census_and_empty_log(self):
        self.assertEqual(self.run_log('')['verdict'], 'PENDING')
        result = self.run_log(self.transaction(outcome='interrupted', expected=2))
        self.assertEqual(result['unresolved_commands'], 1)
        result = self.run_log('SOLDIER_ORDERED_RESULT: attempt=1 outcome=manifest-invalid expected=2 observed=0 replace=0 keep=0 missing=0 density=8\n')
        self.assertEqual(result['unresolved_commands'], 2)

    def test_invalid_evidence_fails_closed(self):
        good = self.transaction()
        for text in [good.splitlines()[0]+'\n', good + good, good.replace('observed=1', 'observed=0'),
                     good.replace('expected=1', 'expected=2'), good.replace('decision=replace', 'decision=missing'),
                     good.replace('density=8', 'density=12', 1), good.replace('order=4', 'order=-1'),
                     good.replace(' frame=0', ''), good.replace('outcome=published', 'outcome=unknown')]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.run_log(text)


if __name__ == '__main__':
    unittest.main()
