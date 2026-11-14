"""Executable mathematical specification, NOT the game's SDL/input adapter.
Exact rationals avoid a self-fulfilling tolerance in the inverse checks.
GPL-3.0-or-later.
"""
from dataclasses import dataclass
from fractions import Fraction as F
import unittest

MODES = [(640,480),(800,600),(1024,768),(1152,864),(1280,960),
         (1400,1050),(1600,1200),(1920,1440),(2048,1536),(2560,1920),
         (2880,2160),(1280,720),(1600,900),(1920,1080),(2560,1440),
         (3200,1800),(3840,2160),(1366,768)]


def inside(p, rect):
    x, y, w, h = rect
    return x <= p[0] < x+w and y <= p[1] < y+h


@dataclass(frozen=True)
class Transform:
    window: tuple
    output: tuple
    logical: tuple
    aspect: tuple = (F(1), F(1))

    def __post_init__(self):
        for values in (self.window, self.output, self.logical, self.aspect):
            if len(values) != 2 or any(F(v) <= 0 for v in values):
                raise ValueError('Positive finite dimensions required')

    @property
    def scale(self):
        k = min(F(self.output[i]) / (self.logical[i]*self.aspect[i]) for i in (0,1))
        return tuple(k * a for a in self.aspect)

    @property
    def rect(self):
        size = tuple(self.logical[i]*self.scale[i] for i in (0,1))
        return tuple((self.output[i]-size[i])/2 for i in (0,1)) + size

    def to_output(self, p):
        return tuple(self.rect[i]+p[i]*self.scale[i] for i in (0,1))

    def to_canvas(self, p):
        return tuple((p[i]-self.rect[i])/self.scale[i] for i in (0,1))

    def window_to_output(self, p):
        return tuple(F(p[i])*self.output[i]/self.window[i] for i in (0,1))

    def output_to_window(self, p):
        return tuple(F(p[i])*self.window[i]/self.output[i] for i in (0,1))

    def hit_world(self, window_point, map_rect, camera, ui_rects=()):
        physical = self.window_to_output(window_point)
        if not inside(physical, self.rect):
            return None
        canvas = self.to_canvas(physical)
        if any(inside(canvas, r) for r in ui_rects) or not inside(canvas, map_rect):
            return None
        return tuple(camera[i]+canvas[i]-map_rect[i] for i in (0,1))


class ContractTests(unittest.TestCase):
    def test_known_examples(self):
        t = Transform((1280,720),(1920,1080),(320,200),(F(5,6),F(1)))
        self.assertEqual(t.rect, (240,0,1440,1080))
        self.assertEqual(t.scale, (F(9,2),F(27,5)))
        self.assertEqual(t.window_to_output((640,360)), (960,540))
        self.assertEqual(t.to_canvas((960,540)), (160,100))
        self.assertEqual(Transform((1920,1080),(3840,2160),(320,200),
                                   (F(5,6),F(1))).rect, (480,0,2880,2160))
        self.assertEqual(Transform((1920,1080),(1920,1080),(320,225),
                                   (F(15,16),F(1))).scale, (F(9,2),F(24,5)))
        self.assertEqual(Transform((1920,1080),(1920,1080),(320,200)).rect,
                         (96,0,1728,1080))

    def test_matrix_inverse_and_containment(self):
        combinations = 0
        for output in MODES + [(1001,777),(1919,1079)]:
            for dpi in [F(1),F(5,4),F(3,2),F(7,4),F(2),F(3)]:
                # Rounding produces distinct effective X/Y ratios.
                window = tuple(max(1,int(F(v)/dpi)) for v in output)
                for logical in [(320,200),(320,225),(320,260)]:
                    aspect = (F(4*logical[1],3*logical[0]),F(1))
                    t = Transform(window,output,logical,aspect)
                    x,y,w,h = t.rect
                    self.assertGreaterEqual(x,0); self.assertGreaterEqual(y,0)
                    self.assertLessEqual(x+w,output[0]); self.assertLessEqual(y+h,output[1])
                    self.assertEqual(w/h,F(4,3))
                    for p in [(0,0),(F(1,2),F(1,2)),
                              (F(logical[0],2),F(logical[1],2)),
                              (logical[0]-F(1,2),logical[1]-F(1,2))]:
                        physical=t.to_output(p)
                        self.assertEqual(t.to_canvas(physical),p)
                        self.assertEqual(t.window_to_output(t.output_to_window(physical)),physical)
                    self.assertFalse(inside((x+w,y+h/2),t.rect))
                    self.assertFalse(inside((x+w/2,y+h),t.rect))
                    combinations += 1
        self.assertEqual(combinations,360)

    def test_bands_hud_and_fractional_camera(self):
        t=Transform((1280,720),(1920,1080),(320,200),(F(5,6),F(1)))
        region=(64,0,256,200); camera=(F(401,4),F(201,2))
        self.assertIsNone(t.hit_world((100,360),region,camera))  # physical band
        point=lambda p:t.output_to_window(t.to_output(p))
        self.assertIsNone(t.hit_world(point((32,50)),region,camera))  # sidebar
        self.assertIsNone(t.hit_world(point((160,100)),region,camera,[(150,90,20,20)]))
        self.assertEqual(t.hit_world(point((160,100)),region,camera),
                         (F(785,4),F(401,2)))
        self.assertEqual(t.hit_world(point((64,0)),region,camera),camera)
        self.assertIsNone(t.hit_world(point((320,100)),region,camera))

    def test_density_and_internal_target_do_not_move_anchor(self):
        t=Transform((1920,1080),(3840,2160),(320,200),(F(5,6),F(1)))
        anchor=(F(201,2),F(401,4))
        for density in [1,2,4,8,12]:
            source_anchor=(8*density,14*density)
            texel=(10*density,7*density)
            canvas=tuple(anchor[i]+F(texel[i]-source_anchor[i],density) for i in (0,1))
            self.assertEqual(t.to_output(canvas),t.to_output((anchor[0]+2,anchor[1]-7)))
            restored=tuple(anchor[i]+F(source_anchor[i]-source_anchor[i],density) for i in (0,1))
            self.assertEqual(t.to_output(restored),t.to_output(anchor))
        for internal in [(640,400),(1280,800),(2880,2160)]:
            q=tuple(anchor[i]*F(internal[i],t.logical[i]) for i in (0,1))
            physical=tuple(t.rect[i]+q[i]*t.rect[i+2]/internal[i] for i in (0,1))
            self.assertEqual(physical,t.to_output(anchor))

    def test_invalid_geometry(self):
        for bad in [(0,1),(-1,200),(float('nan'),1),(float('inf'),1)]:
            for slot in range(4):
                args=[(1280,720),(1920,1080),(320,200),(1,1)]
                args[slot]=bad
                with self.assertRaises((ValueError,OverflowError)):
                    Transform(*args)


if __name__ == '__main__':
    unittest.main(verbosity=2)
