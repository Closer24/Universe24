"""Independent contracts for the new projective integer integration law."""
from fractions import Fraction as F
import unittest

import numpy as np

from universe24.core import Engine, Tensor
from universe24.core.lattice import lattice
from universe24.tests.test_migration import scalar_step
from validation.geometry.team48.refinement_integer_projective import (
    compile_projective, prepare, readout, build_charged,
)


class ProjectiveRefinementTests(unittest.TestCase):
    def test_mixed_degree_spatial_ratio_identity_and_complete_scalar_oracle(self):
        def equations(f, partial):
            return {'x': F(1, 7)+f['x']*f['y']+partial('y', 0),
                    'y': -F(2, 5)*f['y']+f['x']**3}

        program = compile_projective(('x', 'y'), equations,
                                     dt=F(1, 13), dx=F(2, 7), degree=3)
        lat = lattice(3)
        current = np.array([[F(n-13, 19) for n in range(27)],
                            [F((n % 7)-3, 11) for n in range(27)]], dtype=object)
        remainders = np.array([[(g+n) % 6 for n in range(27)]
                               for g in range(3)], dtype=object)
        initial = prepare(program, current, L=3, remainders=remainders)
        # Transport is tested too; a reloaded tensor must produce identical bytes.
        engine = Engine(Tensor.from_dict(program.tensor.to_dict(), strict_support=True))
        actual = oracle = initial
        old_physical = None
        for tick in range(4):
            now = readout(program, actual)
            # Independent explicit RHS, rather than calling the construction callback.
            derivative = ((now[1, lat.shift_index((1, 0, 0))]
                           - now[1, lat.shift_index((-1, 0, 0))]) / (2*program.dx))
            rhs = np.array([F(1, 7)+now[0]*now[1]+derivative,
                            -F(2, 5)*now[1]+now[0]**3], dtype=object)
            euler = now+program.dt*rhs
            following = engine.step(actual)
            oracle = scalar_step(program.tensor, oracle)
            self.assertTrue(following.same_as(oracle))
            expected = euler if tick == 0 else euler + F(
                int(actual.a[0, 0]), int(following.b[0, 0]))*(euler-old_physical)
            np.testing.assert_array_equal(readout(program, following), expected)
            np.testing.assert_array_equal(following.r, remainders)
            self.assertGreater(int(following.b[0, 0]), int(actual.b[0, 0]))
            old_physical, actual = now, following
        self.assertTrue(engine.rewind(actual, 4).same_as(initial))
        self.assertEqual(program.tensor.support_violations(), [])
        self.assertTrue(all(f.field == 'b' for m in program.tensor.monomials for f in m.factors))

    def test_real_charged_model_accepts_previously_rejected_refinement(self):
        for h in (F(1, 2), F(1, 4), F(1, 8)):
            program = build_charged(dt=h, dx=h)
            self.assertEqual(program.tensor.G, 41)
            self.assertLessEqual(program.tensor.rank, 4)
            self.assertEqual(program.tensor.support_violations(), [])
            self.assertTrue(all(m.coeff % 3 == 0 for m in program.tensor.monomials))

    def test_decoder_rejects_nonuniform_or_nonpositive_denominator(self):
        program = compile_projective(('x',), lambda f, d: {'x': f['x']**2})
        initial = prepare(program, np.ones((1, 27), dtype=object), L=3)
        for mutate in ('current', 'old', 'zero'):
            corrupt = initial.copy()
            if mutate == 'current':
                corrupt.b[0, 1] += 1
            elif mutate == 'old':
                corrupt.a[0, 1] += 1
            else:
                corrupt.b[0] = 0
            with self.assertRaises(ValueError):
                readout(program, corrupt)

    def test_compiler_enforces_budget_degree_and_exact_inputs(self):
        with self.assertRaises(ValueError):
            compile_projective(tuple('x'+str(i) for i in range(48)), lambda f, d: f)
        with self.assertRaises(ValueError):
            compile_projective(('x',), lambda f, d: {'x': f['x']**4}, degree=3)
        with self.assertRaises(TypeError):
            compile_projective(('x',), lambda f, d: f, dt=0.5)
        program = compile_projective(('x',), lambda f, d: {'x': f['x']})
        with self.assertRaises(TypeError):
            prepare(program, np.ones((1, 27)), L=3)

    def test_increasing_precision_does_not_add_retained_channels(self):
        # This only verifies representation, not an Einstein convergence gate.
        program = compile_projective(('x',), lambda f, d: {'x': -f['x']}, dt=F(1, 16))
        for bits in (4, 60, 130):
            state = prepare(program, np.full((1, 27), F(1, 3), dtype=object),
                            L=3, denominator=3*(1 << bits))
            self.assertEqual(state.G, 2)
            next_state = Engine(program.tensor).step(state)
            np.testing.assert_array_equal(readout(program, next_state),
                                          np.full((1, 27), F(5, 16), dtype=object))


if __name__ == '__main__':
    unittest.main()
