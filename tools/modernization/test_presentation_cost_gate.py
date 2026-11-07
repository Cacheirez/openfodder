import unittest
from measure_presentation_cost import validate_mode


class MeasurementGateTests(unittest.TestCase):
    def test_modes_must_be_observed_not_just_requested(self):
        audit = 'MISSION_LAYER_AUDIT: verified real producer interval\n'
        publication = 'MISSION_LAYER_PRESENT: published verified orders\n'
        for mode, log in [('classic', ''), ('audit', audit), ('publication', audit+publication)]:
            validate_mode(log, mode)
        for mode, log in [('classic', audit), ('audit', ''), ('publication', audit),
                          ('audit', audit+publication), ('classic', 'MISSION_PAUSE_PROBE: completed'),
                          ('classic', 'MISSION_LAYER_SCHEDULE: 5 presentations per mission call'),
                          ('classic', 'runtime error: overflow')]:
            with self.subTest(mode=mode, log=log), self.assertRaises(RuntimeError):
                validate_mode(log, mode)


if __name__ == '__main__':
    unittest.main()
