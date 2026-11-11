"""Independent GR identities and actual integer evolution of a small sector."""
from fractions import Fraction as F
import unittest
import numpy as np
import sympy as sp

from universe24.core import Engine, Tensor
from universe24.layers.conformal_flrw import build, SOURCES
from universe24.prepare.conformal_flrw import prepare
from universe24.observe.conformal_flrw import sample
from universe24.tests.test_migration import scalar_step


class ConformalFLRWTests(unittest.TestCase):
    def test_metric_derived_einstein_and_geodesics(self):
        t, x, y, z = sp.symbols('eta x y z', positive=True)
        A, B = sp.symbols('A B', nonnegative=True)
        coords = (t, x, y, z)
        a = A*t*t+B*t
        g = sp.diag(-a*a, a*a, a*a, a*a)
        inv = g.inv()
        gamma = [[[sp.simplify(sum(inv[i, l]*(sp.diff(g[l, k], coords[j])
                    + sp.diff(g[l, j], coords[k])-sp.diff(g[j, k], coords[l]))
                    for l in range(4))/2) for k in range(4)] for j in range(4)] for i in range(4)]
        ricci = sp.Matrix(4, 4, lambda i, j: sp.simplify(sum(
            sp.diff(gamma[k][i][j], coords[k])-sp.diff(gamma[k][i][k], coords[j])
            + sum(gamma[k][i][j]*gamma[l][k][l]-gamma[l][i][k]*gamma[k][j][l]
                  for l in range(4)) for k in range(4))))
        G = sp.simplify(ricci-g*sp.trace(inv*ricci)/2)
        rho, p = 12*A/a**3+3*B*B/a**4, B*B/a**4
        self.assertEqual(sp.simplify(G-sp.diag(rho*a*a, p*a*a, p*a*a, p*a*a)), sp.zeros(4))
        # Comoving timelike and axial null geodesics, including the affine
        # parameter. A straight conformal path alone is not this check.
        for velocity, clock_rate, norm in ((sp.Matrix([1/a, 0, 0, 0]), a, -1),
                                           (sp.Matrix([1/a**2, 1/a**2, 0, 0]), a*a, 0)):
            for i in range(4):
                residual = sp.diff(velocity[i], t)/clock_rate + sum(
                    gamma[i][j][k]*velocity[j]*velocity[k] for j in range(4) for k in range(4))
                self.assertEqual(sp.simplify(residual), 0)
            self.assertEqual(sp.simplify((velocity.T*g*velocity)[0]), norm)
        tau = A*t**3/3+B*t*t/2
        lam = A*A*t**5/5+A*B*t**4/2+B*B*t**3/3
        self.assertEqual(sp.diff(tau, t), a)
        self.assertEqual(sp.simplify(sp.diff(lam, t)-a*a), 0)
        self.assertEqual(sp.simplify(sp.diff(rho, t)+3*sp.diff(a, t)/a*(rho+p)), 0)

    def test_sources_clocks_bigints_and_exact_inverse(self):
        for dust, B in (((1, 0, 0), 0), ((0, 1, 0), 0), ((0, 0, 1), 0),
                        ((0, 0, 0), 2), ((1, 2, 3), 4), ((2**80, 3, 4), 2**70)):
            tensor, seed = prepare(Q=7, dust=dust, radiation=B)
            engine, state, oracle = Engine(tensor), seed, seed
            for _ in range(7):
                before = state
                state, oracle = engine.step(state), scalar_step(tensor, oracle)
                self.assertTrue(state.same_as(oracle))
                self.assertTrue(engine.inverse_step(state).same_as(before))
                values = sample(state, Q=7)
                self.assertEqual(values['einstein_residual'], [0]*4)
                self.assertEqual(values['friedmann_residual'], 0)
                self.assertTrue(np.array_equal(state.r, seed.r))
            self.assertTrue(engine.rewind(state, 7).same_as(seed))
            self.assertEqual(tensor.G, 8)
            self.assertLessEqual(tensor.rank, 4)
            self.assertEqual(tensor.support_violations(), [])

    def test_refinement_matches_at_same_physical_time_without_more_channels(self):
        observations = []
        for Q in (2, 4, 8):
            tensor, seed = prepare(Q=Q, q0=2*Q)
            final = Engine(tensor).run(seed, 4*Q)
            observations.append(sample(final, Q=Q))
            self.assertEqual(tensor.G, 8)
        self.assertEqual(observations[0], observations[1])
        self.assertEqual(observations[1], observations[2])

    def test_matter_antimatter_exchange_preserves_geometry_and_clocks(self):
        outcomes = []
        for dust in ((2, 7, 3), (7, 2, 3)):
            tensor, seed = prepare(dust=dust)
            outcomes.append(sample(Engine(tensor).run(seed, 9)))
        for key in ('metric', 'proper_time', 'null_affine_parameter', 'rho', 'pressure'):
            self.assertEqual(outcomes[0][key], outcomes[1][key])
        # This is equality of two dust species, not a Dirac/annihilation model.

    def test_actual_source_terms_drive_geometry_and_clock(self):
        tensor, seed = prepare(dust=(1, 2, 3), radiation=4)
        broken = tensor.to_dict()
        broken['monomials'] = [m for m in broken['monomials'] if not (
            m[0] == 'geometry.s' and any(f[0] in SOURCES for f in m[2]))]
        broken['designated_one_way'] = [d for d in broken['designated_one_way'] if d[0] != 'geometry.s']
        good = Engine(tensor).step(seed)
        bad = Engine(Tensor.from_dict(broken, strict_support=True)).step(seed)
        self.assertTrue(np.all(good.b[1]-bad.b[1] == 2*sum((1, 2, 3))))
        with self.assertRaisesRegex(ValueError, 'invariant'):
            sample(bad)
        empty_clock = tensor.to_dict()
        empty_clock['monomials'] = [m for m in empty_clock['monomials'] if not (
            m[0] == 'clock.c6' and any(f[0] in SOURCES or f[0] == 'radiation.b' for f in m[2]))]
        empty_clock['designated_one_way'] = [d for d in empty_clock['designated_one_way'] if d[0] != 'clock.c6']
        wrong = Engine(Tensor.from_dict(empty_clock, strict_support=True)).step(seed)
        self.assertFalse(np.array_equal(wrong.b[2], good.b[2]))
        with self.assertRaisesRegex(ValueError, 'invariant'):
            sample(wrong)

    def test_invalid_preparation_and_nonuniform_states_rejected(self):
        for kwargs in ({'Q': 0}, {'Q': True}, {'dust': (-1, 0, 0)}, {'q0': 1},
                       {'radiation': 1.2}, {'dust': (0, 0, 0), 'radiation': 0}):
            with self.assertRaises(ValueError):
                prepare(**kwargs)
        _, seed = prepare()
        copy = seed.copy()
        sample(seed)
        self.assertTrue(seed.same_as(copy))
        seed.b[1, 0] += 1
        with self.assertRaisesRegex(ValueError, 'homogeneity'):
            sample(seed)


if __name__ == '__main__':
    unittest.main()
