"""Fixed-six runtime regressions against an independent scalar receiver.

This checks a direct scalar receiver oracle against the compiled engine. It
separately verifies all retained counters and remainders, including negative
inputs and Python big integers, then rewinds the entire preparation exactly.
"""
from __future__ import annotations

import unittest
import numpy as np

from universe24.core import Engine, State
from universe24.system.checks import fixture, scalar_step


class TestMigration(unittest.TestCase):
    def test_fixed_six_default_has_no_scale_parameter(self):
        bundle=fixture()
        tensor,initial=bundle.tensor,bundle.seed
        engine=Engine(tensor)
        self.assertEqual((tensor.G,len(tensor),engine.D),(48,288,6))
        self.assertNotIn('Q',tensor.to_dict())
        self.assertFalse(hasattr(engine,'Q'))
        final=initial
        records=0
        for tick in range(1,21):
            following=engine.step(final)
            records+=len(engine.clicks(final,following,tick).select('official'))
            final=following
        self.assertGreater(records,0)
        self.assertTrue(engine.rewind(final,20).same_as(initial))
        self.assertTrue(final.same_as(engine.run(initial,20)))

    def test_scalar_oracle_matches_negative_and_bigint_full_states(self):
        tensor=fixture().tensor
        engine=Engine(tensor)
        rng=np.random.default_rng(59)
        a=rng.integers(-6,7,size=(tensor.G,27)).astype(object)
        b=rng.integers(-6,7,size=a.shape).astype(object)
        r=rng.integers(0,6,size=a.shape).astype(object)
        a[0,0]=-(1<<90)
        b[1,1]=1<<100
        initial=State(3,a,b,r)
        compiled=oracle=initial
        for _ in range(6):
            compiled=engine.step(compiled)
            oracle=scalar_step(tensor,oracle)
            self.assertTrue(compiled.same_as(oracle))
        self.assertTrue(engine.rewind(compiled,6).same_as(initial))
