"""Exact algebra checks for the optional clock network, not physical certificates."""
import unittest
import numpy as np
from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import DIRECTIONS, ZERO
from universe24.core.reciprocity import check_reciprocity
from universe24.layers.clock_network import InvariantPort, build_clock_network, one_invariant_ports

class ClockNetworkTests(unittest.TestCase):

    def test_expanded_polynomial_matches_potential_derivatives(self):
        source = Tensor([GearType('x'), GearType('y', sign=-1, sign_why='signed-gradient control'), GearType('u', link=0), GearType('v', link=0)], [])
        ports = [InvariantPort('node', ('x', 'y'), (1, 2), (2, -1), 3, 7), InvariantPort('edge', ('u', 'v'), (2, 1), (4, 0), 2)]
        net = build_clock_network(source, ports, sectors=('node', 'edge'), spring=5, spatial_spring=2, strict_support=True)
        t = net.tensor
        e = Engine(t)
        b = np.arange(t.G * 27).reshape(t.G, 27) % 11 - 5
        s = State(3, np.zeros_like(b), b, np.full_like(b, 3))
        expected = np.zeros_like(b, dtype=object)
        master = net.clock_index()
        clock_ids = [net.clock_index(n) for n in ('master', 'node', 'edge')]
        for c in clock_ids:
            expected[c] = net.clock_coefficient * b[c]
            for direction in DIRECTIONS:
                expected[c] += net.spatial_spring * (b[c, s.lattice.shift_index(direction)] - b[c])
        for sector in net.sectors:
            c = net.clock_index(sector)
            expected[c] += net.spring * (b[master] - b[c])
            expected[master] += net.spring * (b[c] - b[master])
        for p in net.ports:
            c = net.clock_index(p.sector)
            gs = [t.gear_index(n) for n in p.gears]
            axis = t.gears[gs[0]].link
            for n in range(s.N):
                endpoints = [n] if axis is None else [n, int(s.lattice.shift_index(DIRECTIONS[2 * axis])[n])]
                values = [int(b[g, n]) + v for g, v in zip(gs, p.shifts)]
                E = sum((w * y * y for w, y in zip(p.weights, values)))
                for end in endpoints:
                    expected[c, end] -= p.coupling * int(b[c, end]) * (E - p.counterterm)
                c2 = sum((int(b[c, end]) ** 2 for end in endpoints))
                for g, w, y in zip(gs, p.weights, values):
                    expected[g, n] -= t.gears[g].sign * p.coupling * w * y * c2
        np.testing.assert_array_equal(e.inputs(s), expected)
        self.assertTrue(check_reciprocity(t).ok)
        self.assertEqual(t.support_violations(), [])
        self.assertEqual(t.rank, 4)

    def test_inverse_keeps_old_a_dag_and_large_integer_state(self):
        source = Tensor(['x', 'y'], [('x', 7, (('y', ZERO, 'a'),))])
        net = build_clock_network(source, [InvariantPort('sector', ('x', 'y'))], sectors=('sector',), spring=1, strict_support=True)
        e = Engine(net.tensor)
        s = e.vacuum(3, [5] * net.tensor.G)
        s.a[:] = 1
        s.b[:] = 2
        b = s.b.astype(object)
        b[0, 0] = 1 << 80
        s = State(3, s.a, b, s.r)
        forward = e.run(s, 3)
        self.assertTrue(e.rewind(forward, 3).same_as(s))
        self.assertTrue(e.run(e.rewind(s, 3), 3).same_as(s))
        self.assertGreater(e.stats['pyint_steps'], 0)
        self.assertEqual(len(source.stages), 2)
        self.assertEqual(len(net.tensor.stages), 2)

    def test_full_affine_link_norm_covariance_of_added_force(self):
        from universe24.layers.gauge import ALGEBRAS
        names = ('U0', 'U1', 'U2', 'U3')
        source = Tensor([GearType(n, link=0) for n in names], [])
        p = InvariantPort('s', names, shifts=(8, 0, 0, 0))
        net = build_clock_network(source, [p], sectors=('s',), spring=2, strict_support=True)
        e = Engine(net.tensor)
        s = e.vacuum(3, [3] * net.tensor.G)
        s.b[:] = np.arange(net.tensor.G * 27).reshape(net.tensor.G, 27) % 7 - 3
        original = e.inputs(s)
        shift = np.array([8, 0, 0, 0])[:, None]
        for q in ALGEBRAS['su2'].group:
            R = np.asarray(ALGEBRAS['su2'].left_matrix(q), dtype=np.int64)
            transformed = s.copy()
            transformed.b[:4] = R @ (s.b[:4] + shift) - shift
            response = e.inputs(transformed)
            np.testing.assert_array_equal(response[:4], R @ original[:4])
            np.testing.assert_array_equal(response[4:], original[4:])

    def test_declared_port_validation_and_source_locality_scope(self):
        source = Tensor([GearType('x'), GearType('u', link=0), GearType('v', link=1)], [])
        invalid = [InvariantPort('other', ('x',)), InvariantPort('s', ('x', 'x')), InvariantPort('s', ('x',), weights=(True,)), InvariantPort('s', ('x',), shifts=(0, 1)), InvariantPort('s', ('u', 'v')), InvariantPort('s', ('x', 'u'))]
        for p in invalid:
            with self.assertRaises(ValueError):
                build_clock_network(source, [p], sectors=('s',), spring=1)
        with self.assertRaises(ValueError):
            build_clock_network(source, [], sectors=('s',), spring=0)
        with self.assertRaises(ValueError):
            build_clock_network(source, [], sectors=('master',), spring=1)
        wide = Tensor(source.gears, [('u', 1, (('v', ZERO, 'b'),))])
        build_clock_network(wide, [], sectors=('s',), spring=1)
        with self.assertRaises(ValueError):
            build_clock_network(wide, [], sectors=('s',), spring=1, strict_support=True)
if __name__ == '__main__':
    unittest.main()
