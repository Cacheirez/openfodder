"""Coverage must fail closed: static tables or observed partial keys aren't acceptance."""
import tempfile
import unittest
import json
from pathlib import Path
from soldier_coverage import report, classify

class CoverageTests(unittest.TestCase):
    def test_committed_walk_fixture_matches_current_engine_tables(self):
        root=Path(__file__).resolve().parents[2]
        committed=json.loads((root/'docs/modernization/evidence/soldier-coverage-matrix.json').read_text())
        self.assertEqual(committed['walk24'],report()['walk24'])
    def test_catalog(self):
        r=report()
        self.assertEqual(r['static_rows'],637)
        self.assertEqual(len(r['walk24']),96)
        for platform in ('PC','Amiga'):
            for actor in ('player','enemy'):
                keys=[x for x in r['walk24'] if x['platform']==platform and x['actor']==actor]
                self.assertEqual({(x['direction'],x['frame']) for x in keys},{(d,f) for d in range(8) for f in range(3)})
        self.assertEqual(r['verdict'],'PENDING')
        self.assertTrue(all(s=='pending' for s in r['scenarios'].values()))
    def test_partial_or_empty_log_cannot_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'capture.log'
            p.write_text('SOLDIER_BATCH_PUBLISHED: sheet=7 frame=0 count=1\n')
            self.assertEqual(report([p])['verdict'],'PENDING')
            p.write_text('SOLDIER_CAPTURE: scene=1\n')
            with self.assertRaises(ValueError):report([p])
    def test_repeated_audit_is_not_another_producer_draw(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'capture.log'
            fields=dict(scene=1,interval=2,order=3,slot=0,generation=4,tick=5,type=0,person=0,
                sheet=7,frame=0,animation=0,direction=0,face=0,vehicle=0,destroy=0,
                format=1,segment=0,resource=1,offset=562,palette=0,width=320,height=32,
                planes=4,skip=0,crop=0,x=20,y=20,columns=2,rows=14)
            line='SOLDIER_CAPTURE: '+' '.join(f'{k}={v}' for k,v in fields.items())+'\n'
            p.write_text(line*2)
            r=report([p]);self.assertEqual(r['captured_draws'],1)
            self.assertEqual(r['duplicate_audits'],1);self.assertEqual(r['entities'],1)
            self.assertEqual(r['verdict'],'PENDING')
    def test_unknown_body_type_and_families(self):
        base=dict(type=12,format=1,sheet=7,frame=0)
        self.assertEqual(classify(base,{(1,7,0)}),'unexpected_body_type')
        for t,c in [(36,'enemy_rocket'),(27,'floating_dead_soldier'),(72,'civilian_or_hostage'),(22,'associated_effect')]:
            self.assertEqual(classify({**base,'type':t},set()),c)
if __name__=='__main__':unittest.main()
