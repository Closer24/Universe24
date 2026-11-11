"""Exact fixed-six reciprocal clock and recording-sum coupling."""
import unittest
import numpy as np
from universe24.core import Tensor,State,Engine
from universe24.core.reciprocity import check_reciprocity
from universe24.layers.clock_bridge import build_clock_record_bridge
class ClockBridgeTests(unittest.TestCase):
    def test_inputs_are_gradient_and_inverse_is_exact(self):
        block=build_clock_record_bridge(clock='c',positive='p',negative='m',kappa=1,include_free_clock=True)
        t=Tensor(['c','p','m'],block.terms,strict_support=True);e=Engine(t)
        self.assertTrue(check_reciprocity(t).ok)
        b=np.arange(81).reshape(3,27)-30;s=State(3,b+5,b,np.arange(81).reshape(3,27)%6)
        u=e.inputs(s)
        np.testing.assert_array_equal(u[0],3*b[0]-b[1]-b[2]);np.testing.assert_array_equal(u[1],-b[0]);np.testing.assert_array_equal(u[2],-b[0])
        self.assertTrue(e.rewind(e.run(s,20),20).same_as(s))
    def test_record_remainder_changes_later_clock(self):
        for kappa in (0,1):
            block=build_clock_record_bridge(clock='c',positive='p',negative='m',kappa=kappa,include_free_clock=True)
            t=Tensor(['c','p','m'],list(block.terms)+[('p',1,()),('m',1,())]);e=Engine(t)
            seed=e.vacuum(3,[0]*t.G);other=seed.copy();other.r[1:]=5
            first=e.step(seed);first_other=e.step(other)
            self.assertFalse(np.array_equal(first.b[1:],first_other.b[1:]))
            self.assertEqual(np.array_equal(e.step(first).b[0],e.step(first_other).b[0]),kappa==0)
    def test_big_counters_keep_same_small_remainder_domain(self):
        block=build_clock_record_bridge(clock='c',positive='p',negative='m',kappa=1)
        t=Tensor(['c','p','m'],block.terms);e=Engine(t)
        a=np.full((3,27),1<<90,dtype=object);s=State(3,a,-a,np.full((3,27),5))
        self.assertTrue(e.rewind(e.run(s,12),12).same_as(s))
