"""Audit maps preserve exact counters and all six remainder values."""
import json
import unittest
import numpy as np
from universe24.core import Engine, State, Tensor
from universe24.core.reversors import GEAR_MAPS, GroupLinearMap, remainder_map, reversor_check, uniform


def scalar_remainder(name, r):
    if name == "id": return r
    if name == "M": return 5-r
    if name == "Mp": return 4-r if r % 2 == 0 else 6-r
    if name == "JR": return r ^ 1
    if name == "rhoL0": return 4+2*(r % 2)-r
    raise ValueError(name)


class ReversorExactness(unittest.TestCase):
    def test_all_six_remainders(self):
        for dtype in (np.int64, object):
            values = np.arange(6, dtype=dtype)
            for name in ("id", "M", "Mp", "JR", "rhoL0"):
                expected = [scalar_remainder(name, r) for r in range(6)]
                self.assertEqual(remainder_map(name, values, 6).tolist(), expected)
                self.assertTrue(all(0 <= r < 6 for r in expected))

    def test_bigint_gearwise_maps_and_snapshot_roundtrip(self):
        tensor = Tensor(["g"], [])
        a = np.array([[2**100 + n for n in range(27)]], dtype=object)
        state = State(3, a, -2*a, np.arange(27).reshape(1,27) % 6)
        for name, (swap, negate, rm) in GEAR_MAPS.items():
            transform = uniform(tensor, name)
            result = transform(state)
            for n in range(27):
                ai, bi, ri = state.gear(0,n)
                if swap: ai,bi = bi,ai
                if negate: ai,bi = -ai,-bi
                self.assertEqual(result.gear(0,n), (ai,bi,scalar_remainder(rm,ri)))
            reloaded = State.from_dict(json.loads(json.dumps(result.to_dict())))
            self.assertTrue(transform(reloaded).same_as(state), name)

    def test_signed_group_map_and_mirror(self):
        tensor = Tensor(["g", "h"], [])
        engine = Engine(tensor)
        state = engine.vacuum(3,[0,1])
        state.a = state.a.astype(object); state.b = state.b.astype(object)
        state.a[:] = [[2**100]*27,[-2**102]*27]
        state.b[:] = [[-2**101]*27,[2**103]*27]
        for name in ("M", "Mp"):
            transform = GroupLinearMap(tensor,["g","h"],[[0,-1],[-1,0]],neg_r=name)
            result = transform(state)
            for target,source in ((0,1),(1,0)):
                ai,bi,ri = state.gear(source,0)
                self.assertEqual(result.gear(target,0),(-ai,-bi,scalar_remainder(name,ri)))
            self.assertTrue(transform(result).same_as(state))
        self.assertTrue(engine.mirror(engine.mirror(state)).same_as(state))

    def test_reversibility_does_not_imply_arbitrary_mirror_symmetry(self):
        z=(0,0,0)
        tensor=Tensor(["g","h"],[("h",2,(("g",z,"a"),))])
        a=np.arange(27,dtype=np.int64).reshape(1,27)-13
        pair=State(3,np.vstack([a,a+1]),np.vstack([2-a,3-a]),np.vstack([a % 6,(a+1) % 6]))
        engine=Engine(tensor)
        self.assertTrue(engine.inverse_step(engine.step(pair)).same_as(pair))
        self.assertFalse(reversor_check(uniform(tensor,"rhoL0"),engine,[pair],1)["ok"])
