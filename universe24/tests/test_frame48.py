"""Independent continuum checks, exact lift, and explicit failed GR gates."""
from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import sympy as sp

from experiments.geometry.full_gr_audit import einstein_from_jet, symbolic_jet
from universe24.algebra.frame_equations import FIELDS, ANTISYMMETRIC, SYMMETRIC, equations
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import lattice
from universe24.layers.frame48 import compile_frame48
from universe24.observe.frame48 import bank_values, diagnostics, inverse_metric_at
from universe24.prepare.frame48 import flat_values, prepare, increment


class Frame48Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.program = compile_frame48()

    def test_coordinate_geometry_oracle_in_rotated_inhomogeneous_frame(self):
        t, x, y, z = coords = sp.symbols('t x y z', real=True)
        lengths = (2+t*x, 3+t+x*x, 2+t*t+x*y)
        spatial = sp.diag(*(v*v for v in lengths))
        rotation = sp.Matrix([[sp.Rational(3, 5), sp.Rational(4, 5), 0],
                              [-sp.Rational(4, 5), sp.Rational(3, 5), 0], [0, 0, 1]])
        B = rotation*sp.diag(*(1/v for v in lengths))
        invB, invg = B.inv(), spatial.inv()
        K = -B*spatial.diff(t)*B.T/2
        spatial_coords = coords[1:]
        christoffel = [[[sum(invg[i, l]*(spatial[l, k].diff(spatial_coords[j])
            +spatial[l, j].diff(spatial_coords[k])-spatial[j, k].diff(spatial_coords[l]))
            for l in range(3))/2 for k in range(3)] for j in range(3)] for i in range(3)]
        fields = {f'B{a}{i}': B[a, i] for a in range(3) for i in range(3)}
        fields.update({f'K{a}{b}': K[a, b] for a, b in SYMMETRIC})
        fields.update({f'G{a}{b}{c}': sum(invB[i, a]*B[c, j]*(B[b, i].diff(spatial_coords[j])
            +sum(christoffel[i][j][k]*B[b, k] for k in range(3)))
            for i in range(3) for j in range(3))
            for a, b in ANTISYMMETRIC for c in range(3)})
        point = {t: 0, x: 1, y: 0, z: 0}
        at = lambda value: sp.simplify(value.subs(point))
        sampled_fields = {name: at(value) for name, value in fields.items()}
        derivatives = {(name, i): at(value.diff(q)) for name, value in fields.items()
                       for i, q in enumerate(spatial_coords)}
        rhs, constraints, ricci = equations(sampled_fields, lambda name, i: derivatives[name, i])
        for name in FIELDS:
            if name.startswith(('B', 'G')):
                self.assertEqual(sp.simplify(rhs[name]-at(fields[name].diff(t))), 0, name)
        self.assertTrue(all(value == 0 for name, value in constraints.items()
                            if name.startswith(('C', 'Ricci_antisym'))))
        # Freeze t to obtain a product spacetime with the same spatial Ricci.
        static_metric = sp.diag(-1, spatial.subs(t, 0))
        coordinate = einstein_from_jet(*symbolic_jet(static_metric, coords, point))['Ricci'][1:, 1:]
        frame_ricci = B.subs(point)*coordinate*B.subs(point).T
        self.assertEqual(sp.Matrix(ricci), frame_ricci)

    def test_curved_kasner_continuum_equations_against_full_4d_oracle(self):
        t, x, y, z = coords = sp.symbols('t x y z', positive=True)
        powers = (sp.Rational(2, 3), sp.Rational(2, 3), -sp.Rational(1, 3))
        fields = {name: sp.Integer(0) for name in FIELDS}
        for i, p in enumerate(powers):
            fields[f'B{i}{i}'], fields[f'K{i}{i}'] = t**(-p), -p/t
        rhs, constraints, _ = equations(fields, lambda name, i: 0)
        self.assertTrue(all(sp.simplify(v) == 0 for v in constraints.values()))
        self.assertTrue(all(sp.simplify(rhs[name]-value.diff(t)) == 0 for name, value in fields.items()))
        metric = sp.diag(-1, *(t**(2*p) for p in powers))
        oracle = einstein_from_jet(*symbolic_jet(metric, coords, {t: 8, x: 0, y: 0, z: 0}))
        self.assertEqual(oracle['G'], sp.zeros(4))
        self.assertTrue(any(v != 0 for a in oracle['Riemann'] for b in a for c in b for v in c))

    def test_48_channel_local_quadratic_tensor(self):
        tensor = self.program.tensor
        self.assertEqual(tensor.G, 48)
        self.assertEqual(tensor.support_violations(), [])
        self.assertEqual(tensor.rank, 3)
        self.assertTrue(tensor.b_only)
        self.assertTrue(all(m.coeff % 3 == 0 for m in tensor.monomials))
        self.assertFalse(any('clock' in name for name in tensor.names))

    def test_reversible_lift_with_spatial_coupling_and_nonzero_remainders(self):
        rng = np.random.default_rng(48)
        old, current = [rng.integers(-1, 2, size=(24, 27)).astype(object) for _ in range(2)]
        r = np.arange(48*27).reshape(48, 27) % 6
        seed = prepare(self.program, old, current, L=3, remainders=r)
        state, engine = seed, Engine(self.program.tensor)
        for _ in range(3):
            new = old+increment(self.program, current, lattice(3))
            before, state = state, engine.step(state)
            np.testing.assert_array_equal(bank_values(state, 'X'), current)
            np.testing.assert_array_equal(bank_values(state, 'Y'), new)
            np.testing.assert_array_equal(state.r, r)
            self.assertTrue(engine.inverse_step(state).same_as(before))
            old, current = current, new
        self.assertTrue(engine.rewind(state, 3).same_as(seed))

    def test_flat_solution_runs_without_horizon_growth(self):
        values = flat_values(3)
        seed = prepare(self.program, values, values, L=3)
        engine = Engine(self.program.tensor)
        result = engine.run(seed, 120)
        self.assertTrue(result.same_as(seed))
        self.assertTrue(engine.rewind(result, 120).same_as(seed))
        self.assertEqual(inverse_metric_at(values), sp.diag(-1, 1, 1, 1))

    def test_big_integer_nonlinear_data_rewinds(self):
        values = flat_values(3)
        values[FIELDS.index('K00')] = 2**70
        seed = prepare(self.program, values, values, L=3)
        engine = Engine(self.program.tensor)
        result = engine.run(seed, 2)
        self.assertGreater(result.max_abs(), 2**100)
        self.assertTrue(engine.rewind(result, 2).same_as(seed))

    def test_individually_constrained_slices_do_not_guarantee_constraint_preservation(self):
        old, current = flat_values(3), flat_values(3)
        old[FIELDS.index('K00')] = 1
        current[FIELDS.index('K11')] = 1
        self.assertTrue(diagnostics(old, L=3)['all_discrete_constraints_zero'])
        self.assertTrue(diagnostics(current, L=3)['all_discrete_constraints_zero'])
        seed = prepare(self.program, old, current, L=3)
        after = Engine(self.program.tensor).step(seed)
        report = diagnostics(bank_values(after), L=3)
        self.assertEqual(report['peak_constraints']['H'], '4')
        self.assertFalse(report['all_discrete_constraints_zero'])
        self.assertTrue(Engine(self.program.tensor).inverse_step(after).same_as(seed))

    def test_non_degeneracy_is_not_automatic(self):
        old, current = flat_values(3), flat_values(3)
        old[FIELDS.index('B00')] = 2
        current[FIELDS.index('K00')] = -1
        seed = prepare(self.program, old, current, L=3)
        after = Engine(self.program.tensor).step(seed)
        self.assertEqual(diagnostics(bank_values(after), L=3)['singular_nodes'], 27)
        with self.assertRaisesRegex(ValueError, 'Degenerate'):
            inverse_metric_at(bank_values(after))

    def test_fractional_refinement_is_rejected_not_hidden(self):
        half_grid = compile_frame48(dt=Fraction(1, 2), dx=Fraction(1, 2))
        self.assertEqual(half_grid.tensor.G, 48)
        with self.assertRaisesRegex(ValueError, 'noninteger coefficient'):
            compile_frame48(dt=Fraction(1, 4), dx=Fraction(1, 4))
        for dt in (Fraction(1, 2), Fraction(1, 16)):
            with self.assertRaisesRegex(ValueError, 'noninteger coefficient'):
                compile_frame48(dt=dt)
        for value in (0, -1):
            with self.assertRaises(ValueError):
                compile_frame48(dx=value)
        with self.assertRaises(TypeError):
            compile_frame48(dt=0.5)
        values = flat_values(3).astype(float)
        with self.assertRaises(TypeError):
            prepare(self.program, values, values, L=3)
        with self.assertRaises(TypeError):
            increment(self.program, values, lattice(3))
        with self.assertRaises(TypeError):
            inverse_metric_at(values)

    def test_full_trace_replay_evidence_and_failed_gates(self):
        from experiments.geometry.frame48_audit import audit
        with tempfile.TemporaryDirectory() as directory:
            report = audit(directory)
            records = [json.loads(line) for line in
                       (Path(directory)/'off_constraint_spatial.jsonl').read_text().splitlines()]
            engine = Engine(Tensor.from_dict(records[0]['tensor']))
            state = State.from_dict(records[1]['state'])
            for tick, record in enumerate(records[2:], 1):
                state = engine.step(state)
                self.assertEqual(tick, record['tick'])
                self.assertTrue(state.same_as(State.from_dict(record['state'])))
            fixture = Path(__file__).resolve().parents[2]/'docs/evidence/frame48_research.json'
            expected = json.loads(fixture.read_text())
            for key in ('source_sha256', 'gates', 'tensor_fingerprint', 'cases', 'manifest'):
                self.assertEqual(report[key], expected[key])
            self.assertFalse(report['gates']['general_einstein_solver_validated'])
            self.assertFalse(report['gates']['retained_physical_clock'])
            self.assertTrue(report['kasner_reference']['errors_decrease'])


if __name__ == '__main__':
    unittest.main()
