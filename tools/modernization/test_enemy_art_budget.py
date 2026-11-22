"""Reject unsafe reuse and incorrect budget assumptions in the planning tool."""
import unittest
from unittest.mock import patch
from measure_enemy_art_budget import measure


class EnemyBudgetTests(unittest.TestCase):
    def setUp(self):
        self.catalog = dict(revision=4, platforms={n:dict(slots=[
            dict(actor_type=5, sheet=0x49, frame=0, produced=True),
            dict(actor_type=5, sheet=0x51, frame=0, produced=True),
            dict(actor_type=106, sheet=0xd8, frame=0, produced=True)]) for n in ('PC','Amiga')})
        self.audit = [dict(format=f, type=t, sheet=s, frame=0, width=16, height=14,
                           resource_sha256='a'*64, native_signature=h*64, opaque_pixels=opaque)
                      for f in (0,1) for t,s,h,opaque in [(5,0x49,'b',60),(5,0x51,'b',60),(106,0xd8,'0',0)]]
        self.player = dict(assets=[dict(width=16,height=14,density=d) for d in (8,12)])

    def report(self):
        with patch('measure_enemy_art_budget.explicit_aliases',return_value=[((0x51,0),(0x49,0),'verified fixture')]):
            return measure(self.catalog,self.audit,self.player)

    def test_budget_counts_both_poses_without_speculative_alias_saving(self):
        r=self.report()
        self.assertEqual(r['distinct_opaque_body_poses'],2)
        self.assertEqual(r['density_estimates']['12']['enemy_body_upper_bound_bytes'],2*16*14*12*12*4)
        self.assertEqual(len(r['resource_specific_no_write_bodies']),2)

    def test_matching_geometry_does_not_excuse_different_raster(self):
        self.audit[1]['native_signature']='c'*64
        with self.assertRaisesRegex(AssertionError,'raster differs'):self.report()

    def test_unproduced_alias_cannot_be_activated(self):
        self.catalog['platforms']['PC']['slots'][0]['produced']=False
        with self.assertRaisesRegex(AssertionError,'not a produced'):self.report()

    def test_catalog_audit_drift_rejected(self):
        self.audit.pop()
        with self.assertRaisesRegex(AssertionError,'drift'):self.report()

    def test_selected_density_must_leave_real_budget(self):
        self.player['assets']*=1000
        with self.assertRaises(AssertionError):self.report()


if __name__=='__main__':unittest.main()
