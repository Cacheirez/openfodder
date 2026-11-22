"""Guard source audit boundaries that previously caused missing soldier states."""
import copy
import unittest
from check_final_timer_equivalence import function
from inventory_enemy_states import ROOT, ROUTES, audit_routes, inventory, table


class EnemyInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = inventory()
        cls.codes = {name:function((ROOT/'Source/Sprites'/file).read_text(encoding='utf-8'),
                                  kind+' cFodder::'+name+'(')
                     for name,(file,kind) in ROUTES.items()}

    def reject_change(self, name, before, after):
        codes = copy.copy(self.codes)
        self.assertIn(before, codes[name])
        codes[name] = codes[name].replace(before, after)
        with self.assertRaises(AssertionError):
            audit_routes(codes)

    def test_no_silent_lookup_extension(self):
        source = (ROOT/'Source/Sprites.cpp').read_text(encoding='utf-8')
        self.assertEqual(len(table(source)), 72)
        start = source.index('int16 mSprite_AnimationEnemyPtrs[]')
        changed = source[:start]+source[start:].replace('0x72', '0x30', 1)
        with self.assertRaises(AssertionError):
            table(changed)

    def test_enemy_mode_zero_and_follower_not_dropped(self):
        for platform in self.catalog['platforms'].values():
            rows = {(s['actor_type'],s['sheet'],s['frame']) for s in platform['slots']}
            for actor in (5,36):
                self.assertTrue({(actor,s,f) for s in range(0x72,0x7a) for f in range(3)} <= rows)
                self.assertIn((actor,0xdc,0), rows)
                self.assertIn((actor,0xa8,2), rows)

    def test_rocket_override_is_not_player_timing(self):
        self.reject_change('Sprite_Handle_Enemy_Rocket', 'pSprite->mFrameIndex = 2;', 'pSprite->mFrameIndex = 0;')

    def test_pre_first_update_person_remains_explicit(self):
        self.reject_change('Sprite_Handle_Enemy', 'mPersonType = eSprite_PersonType_AI;', 'mPersonType = eSprite_PersonType_Human;')

    def test_wounded_and_sinking_are_distinct(self):
        for before in ('Data0 = 0x63;', 'pSprite->mSheetIndex = 0x7A;'):
            self.reject_change('Sprite_Handle_Soldier_Animation', before, before.replace('0x', '0x1'))

    def test_shadow_creation_is_included(self):
        self.reject_change('Sprite_Create_Player_Shadow', 'Data2C->mFrameIndex = 2;', 'Data2C->mFrameIndex = 1;')
        for platform in self.catalog['platforms'].values():
            shadows = [s for s in platform['slots'] if s['actor_type']==22]
            self.assertEqual(len(shadows), 3)
            self.assertTrue(all({r['owner_type'] for r in s['roles']}=={5,36} for s in shadows))

    def test_leader_controller_is_not_infantry(self):
        self.reject_change('Sprite_Handle_Enemy_Leader', 'Sprite_Handle_Hostage(pSprite);', 'Sprite_Handle_Enemy(pSprite);')
        for platform in self.catalog['platforms'].values():
            leader = [s for s in platform['slots'] if s['actor_type']==106]
            self.assertEqual({s['sheet'] for s in leader}, {0xd8,0xd9,0xda,0x7c})

    def test_absent_leader_shadow_cannot_be_invented(self):
        codes = copy.copy(self.codes)
        codes['Sprite_Handle_Hostage'] += '\nSprite_Create_Player_Shadow(pSprite);'
        with self.assertRaises(AssertionError):
            audit_routes(codes)


if __name__ == '__main__':
    unittest.main()
