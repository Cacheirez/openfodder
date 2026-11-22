import unittest
from pathlib import Path
from check_final_timer_equivalence import function
from player_map_associations import check_capture_roles


class CaptureRoleBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(__file__).resolve().parents[2]
        cls.code=function((root/'Source/WindowHD.cpp').read_text(encoding='utf-8'),
            'openfodder::NativeAmiga8Frame cSurface::CaptureNativeAmiga8Frame(')

    def test_opt_in_enemy_roles_allowed(self):check_capture_roles(self.code)

    def test_native_map_corpse_cannot_be_added_to_enemy_role(self):
        with self.assertRaises(AssertionError):check_capture_roles(self.code.replace('state.type==106','state.type==27'))

    def test_ungated_enemy_role_rejected(self):
        with self.assertRaises(AssertionError):check_capture_roles(self.code.replace('openfodder::CF1EnemyCatalogEnabled() && (state.type==5','(state.type==5'))

    def test_second_assignment_rejected(self):
        with self.assertRaises(AssertionError):check_capture_roles(self.code+'\nn.role=2;')


if __name__=='__main__':unittest.main()
