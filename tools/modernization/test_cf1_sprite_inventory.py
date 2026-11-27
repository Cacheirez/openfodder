import struct
import unittest
from inventory_cf1_sprites import spt_types, map_resources


class InventoryTests(unittest.TestCase):
    def test_records_are_ten_bytes_and_big_endian(self):
        data=struct.pack('>10H',124,0,300,400,51,124,0,10,20,4)
        self.assertEqual(dict(spt_types(data)),{51:1,4:1})
        for invalid in (b'',data[:-1],b'RNC\x01'+bytes(16),struct.pack('>5H',0,0,0,0,118)):
            with self.subTest(invalid=invalid),self.assertRaises(ValueError):spt_types(invalid)

    def test_base_and_sub_graphics_are_independent(self):
        data=bytearray(96);data[:3]=b'jun';data[16:19]=b'ice'
        result=map_resources(bytes(data))
        self.assertEqual(result['ingame2'],'juncopt.lbm')
        self.assertEqual(result['ingame1'],'icearmy.lbm')
        with self.assertRaises(ValueError):map_resources(bytes(data[:90]))


if __name__ == '__main__':unittest.main()
