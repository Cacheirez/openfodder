import copy
import unittest
from qualify_enemy_ground_contact import qualifies


class EnemyContactTests(unittest.TestCase):
    def setUp(self):
        self.image=dict(d=8,points=[(8,8),(16,8)],cx=1,cy=.5)
        self.plate=dict(alpha=bytes([255])*56*24,cx=3.5,cy=1.5)

    def test_contact_and_lower_right_projection(self):
        self.assertTrue(qualifies(self.image,self.plate,7,0,0))

    def test_one_unsupported_contact_rejects_whole_placement(self):
        plate=copy.deepcopy(self.plate);alpha=bytearray(plate['alpha']);alpha[8*56+16]=0;plate['alpha']=bytes(alpha)
        self.assertFalse(qualifies(self.image,plate,7,0,0))

    def test_wrong_light_direction_rejected(self):
        for key in ('cx','cy'):
            plate=copy.deepcopy(self.plate);plate[key]=0
            self.assertFalse(qualifies(self.image,plate,7,0,0))

    def test_contact_outside_shadow_rejected(self):
        self.assertFalse(qualifies(self.image,self.plate,7,16,0))


if __name__=='__main__':unittest.main()
