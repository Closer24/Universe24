"""New fixed-six default regression; old scaled traces are not reused.

This checks a direct scalar receiver oracle against the compiled engine. It
separately verifies all retained counters and remainders, including negative
inputs and Python big integers, then rewinds the entire preparation exactly.
"""
from __future__ import annotations

import unittest
import numpy as np

from universe24.core import State
from universe24.core.lattice import lattice
from validation.demos.reference_model.run_reference import build
from universe24.observe.reference_model import state_hash


def scalar_step(tensor, state):
    lat=lattice(state.L)
    a=np.asarray(state.b,dtype=object).copy()
    b=np.empty(a.shape,dtype=object)
    r=np.empty(a.shape,dtype=object)
    for node in range(state.N):
        xyz=lat.coords(node)
        inputs=[0]*tensor.G
        for monomial in tensor.monomials:
            value=monomial.coeff
            for factor in monomial.factors:
                position=tuple((xyz[k]+factor.offset[k])%state.L for k in range(3))
                value*=int(getattr(state,factor.field)[factor.gear,lat.index(*position)])
            inputs[monomial.target]+=value
        for gear in range(tensor.G):
            quotient,remainder=divmod(2*inputs[gear]+int(state.r[gear,node]),6)
            b[gear,node]=quotient-int(state.a[gear,node])
            r[gear,node]=remainder
    return State(state.L,a,b,r)


class TestMigration(unittest.TestCase):
    def test_fixed_six_default_has_no_scale_parameter(self):
        _,tensor,engine,initial,report=build(3,'pulse',13)
        self.assertEqual((tensor.G,len(tensor),engine.D),(48,288,6))
        self.assertEqual(report['kind'],'pulse')
        self.assertNotIn('Q',tensor.to_dict())
        self.assertFalse(hasattr(engine,'Q'))
        final=initial
        records=0
        for tick in range(1,21):
            following=engine.step(final)
            records+=len(engine.clicks(final,following,tick).select('official'))
            final=following
        self.assertEqual(records,75)
        self.assertTrue(engine.rewind(final,20).same_as(initial))
        self.assertEqual(state_hash(final,np.arange(48)),
                         state_hash(engine.run(initial,20),np.arange(48)))

    def test_scalar_oracle_matches_negative_and_bigint_full_states(self):
        _,tensor,engine,_,_=build(3,'none',13)
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

    def test_old_seed_preset_is_not_silently_reinterpreted(self):
        with self.assertRaises(ValueError):
            build(3,'jpure',13)
