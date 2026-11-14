import unittest
from measure_hd_replay_cost import validate_mode


class HDMeasurementGateTests(unittest.TestCase):
    complete = ''.join(f'::notice::Test Amiga The One {i}: Phase Complete (10ms) [Passed]\n' for i in range(3))
    audit = 'MISSION_LAYER_AUDIT: verified real producer interval\n'
    publication = 'MISSION_LAYER_PRESENT: published verified orders\n'
    hd = 'SOLDIER_HD_SDL: published native background and HD patch\n'

    def test_actual_path_required(self):
        for mode in ('classic', 'publication', 'hd8', 'hd12'):
            log = self.complete
            if mode != 'classic':
                log += self.audit+self.publication
            if mode.startswith('hd'):
                log += self.hd
            validate_mode(log, mode)
        for mode, extra in [('classic', self.audit), ('classic', self.hd),
                            ('publication', self.audit), ('publication', self.audit+self.publication+self.hd),
                            ('hd8', self.audit+self.publication), ('hd12', '')]:
            with self.subTest(mode=mode), self.assertRaises(RuntimeError):
                validate_mode(self.complete+extra, mode)

    def test_contamination_and_incomplete_replay_rejected(self):
        for extra in ('MISSION_PAUSE_PROBE: completed', 'MISSION_LAYER_SCHEDULE: 5',
                      'SOLDIER_HD_COMPARE: saved C01_12.html', 'SOLDIER_HD_REASON: paused',
                      'runtime error: overflow', '::error::bad phase',
                      '::notice::Test Amiga: absent (1ms) [Skipped]'):
            with self.subTest(extra=extra), self.assertRaises(RuntimeError):
                validate_mode(self.complete+extra, 'classic')
        with self.assertRaises(RuntimeError):
            validate_mode('', 'classic')
        with self.assertRaises(ValueError):
            validate_mode(self.complete, 'unknown')


if __name__ == '__main__':
    unittest.main()
