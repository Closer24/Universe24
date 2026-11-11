"""Audit maps must remain exact across arbitrary divisors and snapshot storage."""
import json
import unittest

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.reversors import (
    GEAR_MAPS, GroupLinearMap, remainder_map, reversor_check, uniform,
)


def scalar_remainder(name, r, D):
    if name == 'id':
        return r
    if name == 'M':
        return D - 1 - r
    if name == 'Mp':
        return D - 2 - r if r % 2 == 0 else D - r
    if name == 'JR':
        return r ^ 1
    if name == 'rhoL0':
        Q = D // 6
        return 4*Q + 2*(r % (2*Q)) - r
    raise ValueError(name)


class ReversorExactness(unittest.TestCase):
    def test_large_divisor_remainder_maps(self):
        Q = 1 << 80
        for r in (np.array([0, 1, 2], dtype=np.int64),
                  np.array([3*Q-1, 3*Q, 6*Q-2, 6*Q-1], dtype=object)):
            for name in ('id', 'M', 'Mp', 'JR', 'rhoL0'):
                expected = [scalar_remainder(name, int(v), 6*Q) for v in r]
                self.assertEqual(remainder_map(name,r,6*Q).tolist(), expected)

    def test_all_gearwise_maps_with_compacted_remainders(self):
        Q = 1 << 80
        tensor = Tensor(['g'], [], Q=Q)
        a = np.arange(27, dtype=np.int64).reshape(1,27)-13
        state = State(3,a,-2*a,(a % 3))
        for name, (swap, negate, rm) in GEAR_MAPS.items():
            transform = uniform(tensor,Q,name)
            result = transform(state)
            for n in range(27):
                ai, bi, ri = state.gear(0,n)
                if swap:
                    ai,bi = bi,ai
                if negate:
                    ai,bi = -ai,-bi
                self.assertEqual(result.gear(0,n),(ai,bi,scalar_remainder(rm,ri,6*Q)))
            # Serializing either side must not change the map or its involution.
            reloaded = State.from_dict(json.loads(json.dumps(result.to_dict())))
            self.assertTrue(transform(reloaded).same_as(state), name)

    def test_large_divisor_signed_group_map_and_mirror(self):
        Q = 1 << 80
        tensor = Tensor(['g','h'], [], Q=Q)
        e = Engine(tensor,Q)
        state = e.vacuum(3,[0,1])
        state.a[:] = [[3]*27,[-4]*27]
        state.b[:] = [[-5]*27,[6]*27]
        for neg_r in ('M', 'Mp'):
            transform = GroupLinearMap(tensor,Q,['g','h'],[[0,-1],[-1,0]],neg_r=neg_r)
            result = transform(state)
            for target, source in ((0,1),(1,0)):
                ai,bi,ri = state.gear(source,0)
                self.assertEqual(result.gear(target,0),(-ai,-bi,scalar_remainder(neg_r,ri,6*Q)))
            self.assertTrue(transform(result).same_as(state))
        self.assertTrue(e.mirror(e.mirror(state)).same_as(state))

    def test_q_lattice_certificate_is_sufficient_not_necessary(self):
        z = (0,0,0)
        # b(b-1) is even for every integer b; neither coefficient is even.
        tensor = Tensor(['g'],[('g',1,(('g',z,'b'),('g',z,'b'))),
                              ('g',-1,(('g',z,'b'),))],Q=2)
        a = np.arange(27,dtype=np.int64).reshape(1,27)-13
        state = State(3,a,2-a,a % 12)
        self.assertEqual(len(tensor.q_lattice_violations(('g',))),2)
        self.assertTrue(reversor_check(uniform(tensor,2,'rhoL0'),Engine(tensor,2),[state],1)['ok'])
        # A validated old-a DAG has an inverse, but the same mirror need not be it.
        old_a = Tensor(['g','h'],[('h',2,(('g',z,'a'),))],Q=2)
        pair = State(3,np.vstack([a,a+1]),np.vstack([2-a,3-a]),np.vstack([a % 12,(a+1) % 12]))
        self.assertEqual(old_a.q_lattice_violations(('*',)),[])
        e = Engine(old_a,2)
        self.assertTrue(e.inverse_step(e.step(pair)).same_as(pair))
        self.assertFalse(reversor_check(uniform(old_a,2,'rhoL0'),e,[pair],1)['ok'])
