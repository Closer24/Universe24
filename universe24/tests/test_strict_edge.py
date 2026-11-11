"""Exact locality and inverse checks for the explicitly different edge experiment."""
import unittest

import numpy as np

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import DIRECTIONS, lattice
from universe24.core.tensor import LocalityError, compose
from universe24.layers.one import one_system
from universe24.layers.strict_edge import single_edge_realization
from universe24.prepare.strict_edge import lift_seed


class StrictEdgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # A declared x-link reads a neighboring parallel x-link in y. It is
        # storage-local, but the union of physical endpoints is not one edge.
        cls.source = Tensor([GearType("node"), GearType("link", link=0)], [
            ("node", 2, (("node", (1,0,0), "b"),)),
            ("node", 1, (("node", (0,0,0), "b"),)*3),
            ("link", 1, (("link", (0,1,0), "b"),)),
            ("node", 1, (("link", (0,0,0), "b"),))])
        cls.k = 1
        cls.realization = single_edge_realization(cls.source, stiffness=cls.k)
        cls.tensor = cls.realization.tensor
        cls.engine = Engine(cls.tensor)

    def test_all_physical_supports_and_links(self):
        source, t = self.source, self.tensor
        self.assertEqual(len(source.support_violations()), 1)
        self.assertEqual(t.support_violations(), [])
        self.assertEqual(t.rank, 4)
        self.assertEqual((source.G, t.G), (2, 3))
        self.assertEqual(len(self.realization.link_mediators), 1)
        # Retained edges have real endpoints; no metadata deletion masquerades as a fix.
        self.assertEqual(t.gears[:source.G], source.gears)
        for m in t.monomials:
            pts = t.physical_support(m)
            self.assertLessEqual(len(pts), 2)
            if len(pts) == 2:
                self.assertEqual(sum(abs(a-b) for a,b in zip(*pts)), 1)
        self.assertEqual(Tensor.from_json(t.to_json(), strict_support=True), t)
        with self.assertRaises(LocalityError):
            Tensor.from_json(source.to_json(), strict_support=True)

    def test_independent_polynomial_and_endpoint_forces(self):
        # Validate ALL original rows, not only a sample or the builder's own data.
        rng = np.random.default_rng(53)
        t, e = self.tensor, self.engine
        arrays = [rng.integers(-3, 4, (t.G, 27)), rng.integers(-3, 4, (t.G, 27)),
                  rng.integers(0, e.D, (t.G, 27))]
        state = State(3, *arrays)
        remap = dict(self.realization.link_mediators)
        rows = [remap.get(i, i) for i in range(self.source.G)]
        old_view = State(3, *(getattr(state, f)[rows].copy() for f in ('a','b','r')))
        expected = np.zeros_like(state.b, dtype=object)
        original_inputs = Engine(self.source).inputs(old_view)
        expected[rows] = original_inputs
        lat = lattice(3)
        for link, hub in self.realization.link_mediators:
            axis = self.source.gears[link].link
            direction = DIRECTIONS[2*axis]
            for n in range(lat.N):
                xyz = lat.coords(n)
                plus = lat.index(*((xyz[j]+direction[j]) % 3 for j in range(3)))
                minus = lat.index(*((xyz[j]-direction[j]) % 3 for j in range(3)))
                expected[link,n] = ((e.D-2*self.k)*int(state.b[link,n])
                    + self.k*(int(state.b[hub,n])+int(state.b[hub,plus])))
                expected[hub,n] += self.k*(int(state.b[link,n])+int(state.b[link,minus])
                                           -2*int(state.b[hub,n]))
        np.testing.assert_array_equal(e.inputs(state), expected)

    def test_inverse_on_unconstrained_extended_state(self):
        rng = np.random.default_rng(59)
        t, e = self.tensor, self.engine
        a = rng.integers(-5, 6, (t.G, 27)).astype(object)
        b = rng.integers(-5, 6, a.shape).astype(object)
        r = rng.integers(0, e.D, a.shape).astype(object)
        a[-1,0], b[0,1] = 2**80, -(2**81)
        state = State(3,a,b,r)
        self.assertTrue(e.rewind(e.run(state,3),3).same_as(state))
        vac = e.vacuum(3,[2]*t.G)
        self.assertTrue(e.run(vac,3).same_as(vac))

    def test_seed_lift_is_initial_data_only(self):
        e = Engine(self.source)
        seed = e.vacuum(3,[2]*self.source.G)
        seed.b[0,0] = 7
        lifted = lift_seed(seed,self.realization)
        for field in ('a','b','r'):
            np.testing.assert_array_equal(getattr(lifted,field)[:seed.G],getattr(seed,field))
        link,hub = self.realization.link_mediators[0]
        lifted.b[hub,0] = 123
        self.assertNotEqual(lifted.b[link,0],123)
        self.assertNotEqual(seed.b[link,0],123)
        with self.assertRaises(ValueError):lift_seed(lifted,self.realization)

    def test_same_state_same_tick_strict_rewrite_is_impossible(self):
        # Old link(x) depends on link(x+e_y), outside its physical edge.
        old = Engine(self.source)
        s0 = old.vacuum(5,[2]*self.source.G)
        s1 = s0.copy(); lat=lattice(5); origin=lat.index(2,2,2)
        neighbor=lat.index(2,3,2); g=self.source.gear_index('link')
        s1.b[g,neighbor] = old.D
        old0,old1=old.step(s0),old.step(s1)
        self.assertEqual(int(old1.b[g,origin])-int(old0.b[g,origin]),2)
        a,b=lift_seed(s0,self.realization),lift_seed(s1,self.realization)
        a,b=self.engine.step(a),self.engine.step(b)
        self.assertEqual(a.gear(g,origin),b.gear(g,origin))
        a,b=self.engine.step(a),self.engine.step(b)
        self.assertNotEqual(a.gear(g,origin),b.gear(g,origin))

    def test_stiffness_is_explicit_and_validated(self):
        for value in (None,0,-1,True,1.5,2):
            with self.assertRaises(ValueError):single_edge_realization(self.source,stiffness=value)
        with self.assertRaises(ValueError):single_edge_realization(self.tensor,stiffness=self.k)

    def test_source_view_is_passive_and_not_the_full_state(self):
        from universe24.observe.strict_edge import source_coordinate_view
        seed=Engine(self.source).vacuum(3,[2]*self.source.G)
        lifted=lift_seed(seed,self.realization)
        self.assertTrue(source_coordinate_view(lifted,self.realization).same_as(seed))
        link,hub=self.realization.link_mediators[0]
        lifted.b[link,0]=11;lifted.b[hub,0]=23
        view=source_coordinate_view(lifted,self.realization)
        self.assertEqual(view.b[link,0],23)
        view.b[link,0]=99
        self.assertEqual(lifted.b[hub,0],23)
        self.assertEqual(lifted.b[link,0],11)
        with self.assertRaises(ValueError):source_coordinate_view(seed,self.realization)


if __name__ == '__main__':
    unittest.main()
