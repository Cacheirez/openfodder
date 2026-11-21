"""Verify the source denominator and exceptional branches, independently of logs."""
import unittest
from inventory_player_states import inventory,art_reuse,validate_art_reuse,masters
from player_pose_reachability import check_mode_references,EXPECTED_MODE_REFS,EXPECTED_SCRATCH_STORES
import copy


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=inventory()

    def test_denominator(self):
        self.assertEqual(len(self.catalog['states']),14)
        self.assertEqual(len(self.catalog['groups']),9)
        self.assertEqual(self.catalog['platforms']['Amiga']['counts']['required'],165)
        self.assertEqual(self.catalog['platforms']['PC']['counts']['required'],164)
        for platform in ('PC','Amiga'):
            self.assertEqual(len(self.catalog['platforms'][platform]['latent']),24)

    def test_long_wounded_and_final_and_vehicle_are_not_omitted(self):
        for platform in ('Amiga','PC'):
            poses={(p['actor_type'],p['sheet'],p['frame']) for p in self.catalog['platforms'][platform]['required']}
            expected={(0,0x21,f) for f in (0,1)}
            expected|={(0,s,f) for s,n in ((0x38,6),(0x41,6),(0x9f,4),(0xa4,8),(0xcc,5)) for f in range(n)}
            expected|={(27,0x9e,f) for f in (0,1)}
            self.assertTrue(expected<=poses)
            self.assertEqual(len(poses),len(self.catalog['platforms'][platform]['required']))

    def test_invisible_is_not_unapproved_art(self):
        for platform in ('Amiga','PC'):
            data=self.catalog['platforms'][platform]
            self.assertEqual({(p['sheet'],p['frame']) for p in data['hidden']},{(0x7c,0),(0x7c,1)})
            self.assertFalse(any(p['sheet']==0x7c for p in data['required']))

    def test_declared_extra_and_native_aliases_are_explicit(self):
        for platform in ('Amiga','PC'):
            data=self.catalog['platforms'][platform]
            self.assertEqual([(p['sheet'],p['frame']) for p in data['surplus']],[(0x3e,3)])
            self.assertTrue(any(p['exact_native_metadata_reuse'] for p in data['required']))
        self.assertIn('Sprite_Handle_Soldier_Animation',{r['function'] for r in self.catalog['routes']})
        self.assertTrue(any(s['state']=='Die5' and s['sheet']==0x21 for s in self.catalog['exceptional_states']))

    def test_reuse_rejects_different_or_unknown_native_pose(self):
        aliases=art_reuse()
        for platform in ('PC','Amiga'):
            info=self.catalog['platforms'][platform]
            slots={(r['sheet'],r['frame']):r['metadata'] for r in info['required']+info['latent']}
            validate_art_reuse(slots,aliases)
            if not aliases:continue
            bad=copy.deepcopy(aliases);bad[0]['source_sheet']=0;bad[0]['source_frame']=0
            with self.assertRaises(AssertionError):validate_art_reuse(slots,bad)
            bad=copy.deepcopy(aliases);bad[0]['sheet']=255
            with self.assertRaises(AssertionError):validate_art_reuse(slots,bad)
            with self.assertRaises(AssertionError):validate_art_reuse(slots,aliases+[aliases[0]])
        for row in aliases:
            if row.get('kind')=='master-reexport':
                bad=copy.deepcopy(aliases);bad[aliases.index(row)]['source_master_sha256']='0'*64
                with self.assertRaises(AssertionError):masters(bad)

    def test_dormant_boundary_rejects_a_new_zero_mode_store(self):
        self.assertEqual(self.catalog['reachability']['initialized_values'],[2]*5)
        refs=list(EXPECTED_MODE_REFS.elements());stores=list(EXPECTED_SCRATCH_STORES.elements())
        refs.append(('Source/Squad.cpp','word_3BED5[0]=0;'))
        with self.assertRaises(AssertionError):check_mode_references(refs,stores)


if __name__=='__main__':unittest.main()
