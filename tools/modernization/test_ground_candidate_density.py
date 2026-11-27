import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from prepare_ground_shadows import prepare


class GroundCandidateDensityTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.paint=self.root/'paint';self.paint.mkdir()
        self.base=self.root/'base';self.base.mkdir()
        raw=bytes([255])*16*14*8*8*4
        self.body=dict(id='enemy-v2-walk-42-f0-8x',file='body.rgba',density=8,width=16,height=14,sha256=hashlib.sha256(raw).hexdigest())
        (self.base/'body.rgba').write_bytes(raw)
        shade=bytes([80])*7*3*8*8*4
        self.shadow=dict(id='ground-shadow-7x3-8x',file='shadow.rgba',density=8,width=7,height=3,sha256=hashlib.sha256(shade).hexdigest())
        (self.paint/'shadow.rgba').write_bytes(shade)
        (self.paint/'manifest.json').write_text(json.dumps(dict(assets=[self.shadow])))
        self.manifest=dict(version=4,density=8,assets=[self.body],bindings=[],player_catalog={'unchanged':1},enemy_catalog={'unchanged':2})
        self.placements=dict(groups=[dict(width=7,x_quarters=20,y_quarters=52,owner_type=5,bodies=[
            dict(id=self.body['id'],sha256=self.body['sha256']),dict(id='enemy-v2-walk-42-f0-12x',sha256='0'*64)])])

    def run_prepare(self):
        base=self.base/'candidate-manifest.json';base.write_text(json.dumps(self.manifest))
        placements=self.root/'placements.json';placements.write_text(json.dumps(self.placements))
        with patch('prepare_ground_shadows.PAINT',self.paint):return prepare(base,self.root/'out',placements)

    def test_selected_density_and_catalogs_preserved(self):
        self.assertEqual(self.run_prepare(),(1,2,0))
        result=json.loads((self.root/'out/candidate-manifest.json').read_text())
        self.assertEqual(result['enemy_catalog'],self.manifest['enemy_catalog'])
        self.assertEqual(result['player_catalog'],self.manifest['player_catalog'])
        self.assertEqual(hashlib.sha256((self.root/'out/body.rgba').read_bytes()).hexdigest(),self.body['sha256'])

    def test_changed_body_rejected_before_output(self):
        self.placements['groups'][0]['bodies'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):self.run_prepare()
        self.assertFalse((self.root/'out').exists())

    def test_missing_selected_body_not_treated_as_other_density(self):
        self.placements['groups'][0]['bodies'][0]['id']='missing-8x'
        with self.assertRaises(ValueError):self.run_prepare()
        self.assertFalse((self.root/'out').exists())

    def test_foreign_density_rejected(self):
        self.manifest['density']=12
        with self.assertRaises(ValueError):self.run_prepare()
        self.assertFalse((self.root/'out').exists())

    def owner_fixture(self):
        self.body['id']='enemy-v2-prone-52-f0-8x'
        self.placements['groups'][0]['bodies'][0]['id']=self.body['id']
        self.placements['groups'][0]['bodies'][1]['id']='enemy-v2-prone-52-f0-12x'
        self.manifest['enemy_catalog']=dict(poses=[dict(format=0,type=t,sheet=0x52,frame=0,
            assets={'8':self.body['id']},native_signatures=['a'*64],no_write_signatures=[]) for t in (5,36)])

    def test_owner_metadata_split_preserves_pixels_and_native_contract(self):
        self.owner_fixture();self.assertEqual(self.run_prepare(),(1,3,0))
        result=json.loads((self.root/'out/candidate-manifest.json').read_text())
        bodies={a['id']:a for a in result['assets']};poses=result['enemy_catalog']['poses']
        ordinary=bodies[poses[0]['assets']['8']];rocket=bodies[poses[1]['assets']['8']]
        self.assertEqual(ordinary['sha256'],rocket['sha256'])
        self.assertEqual(ordinary['file'],rocket['file'])
        self.assertEqual(ordinary['ground_shadow']['owner_type'],5)
        self.assertEqual(rocket['ground_shadow']['owner_type'],36)

    def test_owner_split_rejects_different_native_raster_before_output(self):
        self.owner_fixture();self.manifest['enemy_catalog']['poses'][1]['native_signatures']=['b'*64]
        with self.assertRaises(ValueError):self.run_prepare()
        self.assertFalse((self.root/'out').exists())


if __name__=='__main__':unittest.main()
