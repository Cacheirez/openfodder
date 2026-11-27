import copy
import unittest
from prepare_enemy_technical_candidate import select_player


class EnemyCandidateTests(unittest.TestCase):
    def setUp(self):
        self.base=dict(version=3,assets=[dict(id=str(d),density=d) for d in (8,12)],bindings=[],
            player_catalog=dict(schema=1,complete=True,poses=[dict(assets={'8':'8','12':'12'}),dict(assets={})]))

    def test_both_densities_preserve_original(self):
        before=copy.deepcopy(self.base)
        for density in (8,12):
            candidate=select_player(self.base,density)
            self.assertEqual(candidate['player_catalog']['poses'][0]['assets'],{str(density):str(density)})
            self.assertEqual(candidate['player_catalog']['poses'][1]['assets'],{})
            self.assertEqual(len(candidate['assets']),1)
        self.assertEqual(self.base,before)

    def test_incomplete_protagonists_rejected(self):
        self.base['player_catalog']['complete']=False
        with self.assertRaises(AssertionError):select_player(self.base,8)

    def test_missing_selected_density_rejected(self):
        self.base['player_catalog']['poses'][0]['assets'].pop('12')
        with self.assertRaises(KeyError):select_player(self.base,12)


if __name__=='__main__':unittest.main()
