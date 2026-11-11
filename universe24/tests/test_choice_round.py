"""Former round-cone calibration is not a propagation certificate."""
import unittest
from universe24.core import compose,Engine
from universe24.layers.gravity import build_metric,light_spec
class InertialFieldTests(unittest.TestCase):
    def test_legacy_headroom_has_zero_spatial_weight(self):
        block=build_metric();tensor=compose(block)
        self.assertEqual(block.params['spatial_wave_speed_squared'],'0')
        self.assertTrue(all(f.offset==(0,0,0) for m in tensor.monomials for f in m.factors))
        self.assertTrue(all(m.coeff==6 for m in tensor.monomials))
        self.assertEqual(light_spec('field').laplacian,{'L':0})
