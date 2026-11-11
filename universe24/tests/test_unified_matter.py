"""Explicit optional integer matter/link composition, not particle physics."""
import unittest
from universe24.core import compose,Engine
from universe24.layers.unified_matter import build_unified_matter
from universe24.prepare import vacuum_state
class MatterLinkTests(unittest.TestCase):
    def test_explicit_small_integer_parameters(self):
        om=build_unified_matter(A=1,kd=1,kw=0,mass=2,lam=0)
        t=compose(*om.blocks);e=Engine(t);seed=vacuum_state(t,3,*om.blocks)
        self.assertTrue(e.run(seed,3).same_as(seed))
        seed.b[0,0]=1
        self.assertTrue(e.rewind(e.run(seed,2),2).same_as(seed))
        self.assertTrue(all(type(m.coeff)is int and m.degree<=3 for m in t.monomials))
