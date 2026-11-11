"""Independent physical controls for Einstein-derived integer FLRW evolution."""
from fractions import Fraction
import unittest
import numpy as np
import sympy as sp
from universe24.core import Engine
from experiments.geometry.einstein_friedmann import (
    build, prepare, validate_sector, run_case, negative_controls, local_readout,
)
from experiments.geometry.friedmann_derivation import audit
from experiments.geometry.simplex_metric import (
    EDGES, signed_intervals, metric_from_intervals, inertia, straight_path_refinement,
)
from experiments.geometry.full_gr_audit import (
    einstein_from_jet, einstein_from_link_jet, symbolic_jet, audit as general_audit,
)


class TestEinsteinFriedmann(unittest.TestCase):
    def test_action_and_full_equations_independently_derived(self):
        self.assertTrue(all(audit()['checks'].values()))

    def test_exact_proper_time_friedmann_law(self):
        result = run_case(1, L=3)
        final = result['samples'][-1]
        self.assertEqual(final['scale'], '3')
        self.assertEqual(final['proper_time'], '20')
        self.assertEqual(final['rho'], '1/1728')
        self.assertEqual(final['Kretschmann'], '1/1119744')
        self.assertEqual(final['R'], '0')
        self.assertEqual(result['max_Einstein_residual'], '0')
        self.assertTrue(result['all_rewinds_exact'])

    def test_same_solution_across_time_refinements(self):
        coarse, fine = run_case(1, L=3), run_case(2, L=3)
        for a, b in zip(coarse['samples'], fine['samples'][::2]):
            for key in ('scale', 'proper_time', 'rho', 'G_diagonal', 'T_diagonal'):
                self.assertEqual(a[key], b[key])

    def test_four_times_source_requires_double_initial_velocity(self):
        base, stronger = run_case(1, 8, L=3), run_case(1, 16, L=3)
        first, second = base['samples'][0], stronger['samples'][0]
        self.assertEqual(Fraction(second['comoving_energy']), 4*Fraction(first['comoving_energy']))
        self.assertEqual(Fraction(second['velocity']), 2*Fraction(first['velocity']))
        self.assertEqual(stronger['samples'][-1]['scale'], '4')
        _, p = build()
        with self.assertRaisesRegex(ValueError, 'constraint'):
            prepare(p, slope=8, energy=4*192)

    def test_contracting_and_flat_branches(self):
        contracting = run_case(1, -8, L=3)['samples'][-1]
        flat = run_case(1, 0, L=3)['samples'][-1]
        self.assertEqual(contracting['scale'], '1')
        self.assertEqual(contracting['proper_time'], '12')
        self.assertEqual(flat['scale'], '2')
        self.assertEqual(flat['proper_time'], '16')
        self.assertEqual(flat['Kretschmann'], '0')

    def test_reversibility_is_not_an_einstein_test(self):
        result = negative_controls()
        self.assertGreater(Fraction(result['wrong_source_max_Einstein_residual']), 0)
        self.assertGreater(Fraction(result['added_force_max_Einstein_residual']), 0)
        self.assertTrue(result['wrong_source_rewinds_exactly'])
        self.assertTrue(result['added_force_rewinds_exactly'])

    def test_heterogeneous_geometry_is_outside_this_evolution_sector(self):
        tensor, p = build()
        seed = prepare(p)
        seed.a[0, 0] += 1
        seed.b[0, 0] += 1
        with self.assertRaisesRegex(ValueError, 'homogeneous'):
            validate_sector(seed, p)
        engine = Engine(tensor, p['Q'])
        # The observer's restriction never becomes a veto inside the Engine.
        self.assertTrue(engine.inverse_step(engine.step(seed)).same_as(seed))

    def test_big_integer_fallback_and_remainder_independence(self):
        tensor, p = build(Q=7)
        p['scale'] = 1 << 70
        seed = prepare(p)
        self.assertEqual(seed.b.dtype, object)
        engine = Engine(tensor, p['Q'])
        after = engine.step(seed)
        self.assertEqual(int(after.b[0, 0])-int(seed.b[0, 0]), 8)
        np.testing.assert_array_equal(after.r, seed.r)
        self.assertTrue(engine.inverse_step(after).same_as(seed))
        self.assertEqual(local_readout(seed, after, p)['Einstein_residual'], [[0]*4 for _ in range(4)])

    def test_singularity_and_invalid_parameters_rejected(self):
        with self.assertRaisesRegex(ValueError, 'a=0'):
            run_case(1, -16, L=3)
        for args in ({'n': 3}, {'L': 2}, {'Q': 0}):
            with self.assertRaises(ValueError):
                build(**args)


class TestLinkGeometry(unittest.TestCase):
    def test_full_off_diagonal_metric_round_trip(self):
        frame = sp.Matrix([[2, 1, 0, 0], [0, 2, 1, 0], [1, 0, 3, 1], [0, 1, 0, 2]])
        metric = frame.T * sp.diag(-1, 1, 1, 1) * frame
        basis = sp.Matrix([[1, 1, 0, 0], [0, 1, 0, 1], [0, 0, 2, 0], [0, 0, 0, 3]])
        self.assertEqual(metric_from_intervals(signed_intervals(metric, basis), basis), metric)

    def test_null_basis_signature(self):
        metric = sp.Matrix([[0, -1, 0, 0], [-1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        self.assertEqual(inertia(metric), (1, 3, 0))
        self.assertEqual(metric_from_intervals(signed_intervals(metric)), metric)

    def test_axes_do_not_determine_angles(self):
        first = sp.diag(-1, 2, 2, 2)
        second = first.copy()
        second[1, 2] = second[2, 1] = 1
        a, b = signed_intervals(first), signed_intervals(second)
        self.assertEqual([a[0, i] for i in range(1, 5)], [b[0, i] for i in range(1, 5)])
        self.assertNotEqual(a[2, 3], b[2, 3])

    def test_missing_lengths_wrong_signature_and_floats_rejected(self):
        valid = signed_intervals(sp.diag(-1, 1, 1, 1))
        incomplete = dict(valid)
        del incomplete[1, 4]
        with self.assertRaises(ValueError):
            metric_from_intervals(incomplete)
        euclidean = {edge: sp.Integer(1 if edge[0] == 0 else 2) for edge in EDGES}
        with self.assertRaises(ValueError):
            metric_from_intervals(euclidean)
        valid[0, 1] = -1.0
        with self.assertRaises(ValueError):
            metric_from_intervals(valid)

    def test_finite_curved_paths_only_approximate_local_metric(self):
        errors = [Fraction(row['max_metric_error']) for row in straight_path_refinement()]
        self.assertGreater(errors[-1], 0)
        for coarse, fine in zip(errors, errors[1:]):
            self.assertLess(fine, coarse)
            self.assertLess(abs(coarse/fine-2), Fraction(1, 100))


class TestGeneralEinsteinObserver(unittest.TestCase):
    def test_curved_vacuum_and_shifted_sourced_metric(self):
        result = general_audit()
        self.assertTrue(result['curved_Schwarzschild_vacuum_all_16_G_zero'])
        self.assertEqual(result['Schwarzschild_nonzero_Riemann_components'], 24)
        self.assertTrue(result['shifted_radiation_all_16_G_minus_T_zero'])
        self.assertEqual(result['shifted_radiation_G_01'], '1/256')
        # A complete observer must not be mislabeled a complete evolution law.
        self.assertFalse(result['compilation_barriers']['this_observer_compiles_dynamics'])

    def test_nonlinear_equations_from_integer_link_jets(self):
        t, x, y, z = sp.symbols('t x y z')
        metric = sp.Matrix([[-4+t*t, t*x, 0, 0], [t*x, 5+x*x, y*z, 0],
                            [0, y*z, 6+y*y, 0], [0, 0, 0, 7+z*z]])
        g, dg, ddg = symbolic_jet(metric, (t, x, y, z), {t: 0, x: 1, y: 0, z: 1})
        points = [sp.zeros(4, 1)] + [sp.eye(4)[:, i] for i in range(4)]
        def intervals(matrix):
            return {(i, j): ((points[j]-points[i]).T*matrix*(points[j]-points[i]))[0] for i, j in EDGES}
        link_jet = intervals(g), [intervals(v) for v in dg], [[intervals(v) for v in row] for row in ddg]
        self.assertTrue(all(v.is_Integer for v in link_jet[0].values()))
        direct = einstein_from_jet(g, dg, ddg)
        edges = einstein_from_link_jet(*link_jet)
        self.assertEqual(direct['G'], edges['G'])
        self.assertNotEqual(edges['G'], sp.zeros(4))
        # Independent analytic differentiation through the other implementation.
        from experiments.geometry.friedmann_derivation import curvature
        reference = curvature(metric, (t, x, y, z))[-1].subs({t: 0, x: 1, y: 0, z: 1})
        self.assertEqual(reference.applyfunc(sp.simplify), edges['G'])


if __name__ == '__main__':
    unittest.main()
