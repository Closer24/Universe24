"""Explicit fixed-tensor clock modulation; retired calibration is rejected."""
import unittest
import numpy as np
from universe24.core import Tensor,State,Engine
from universe24.layers.clockgen import build_clockgen,clockgen_system,one_system_clock,clock_window
class ClockModulationTests(unittest.TestCase):
    def test_polynomial_and_inverse(self):
        for mode in ('drive','param'):
            block=build_clockgen(kappa=2,mode=mode,hand='hand',lapse='field')
            tensor=Tensor(['hand','field'],block.terms,strict_support=True);e=Engine(tensor)
            b=np.arange(54).reshape(2,27)%5-2;s=State(3,b+1,b,np.zeros_like(b))
            expected=2*b[0]*(b[1] if mode=='param' else 1)
            np.testing.assert_array_equal(e.inputs(s)[1],expected)
            self.assertTrue(e.rewind(e.run(s,5),5).same_as(s))
    def test_automatic_calibration_removed(self):
        for fn in (clockgen_system,one_system_clock,lambda:clock_window(3)):
            with self.assertRaises(NotImplementedError):fn()
