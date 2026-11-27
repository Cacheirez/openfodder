import unittest
from generate_enemy_pose_table import contracts


class EnemyPoseTableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rows=contracts()

    def test_source_denominator(self):
        self.assertEqual(len(self.rows),965)
        self.assertEqual([sum(r['produced'] for r in self.rows if r['format']==f) for f in (0,1)],[339,340])
        self.assertEqual(len({(r['format'],r['type'],r['sheet'],r['frame']) for r in self.rows}),965)

    def test_initial_injury_keeps_enemy_identity_and_human_person(self):
        for r in self.rows:
            if r['type']==5 and r['sheet']==0x21:self.assertEqual((r['role'],r['personMask']),(2,1))
            if r['type']==5 and r['sheet']==0x42:self.assertEqual((r['role'],r['personMask']),(2,2))
            if r['type']==106:self.assertEqual(r['personMask'],4)

    def test_shadows_and_marker_are_separate_roles(self):
        for f in (0,1):
            shadows=[r for r in self.rows if r['format']==f and r['role']==4]
            self.assertEqual({(r['type'],r['sheet'],r['frame']) for r in shadows},{(22,0x8d,2),(22,0x97,0),(22,0x97,1)})
            self.assertTrue(all(r['produced'] and r['personMask']==0 for r in shadows))
            self.assertEqual(sum(r['format']==f and r['role']==6 for r in self.rows),4)

    def test_unproduced_rows_do_not_become_art(self):
        for r in self.rows:
            if r['type'] in (5,36) and r['sheet']==0x69 and r['frame']==2:self.assertFalse(r['produced'])
            if r['type']==36 and r['sheet']==0xa8:self.assertEqual(r['produced'],r['frame']==2)
            self.assertEqual(r['invisible'],r['sheet']==0x7c)


if __name__=='__main__':unittest.main()
