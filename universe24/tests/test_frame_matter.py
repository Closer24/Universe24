"""Independent sourced-Einstein/field checks and explicit discrete failures."""
from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import sympy as sp

from experiments.geometry.full_gr_audit import einstein_from_jet, symbolic_jet
from universe24.algebra.frame_equations import ANTISYMMETRIC, SYMMETRIC
from universe24.algebra.frame_matter import FIELDS, COMPONENTS, equations, stress_energy
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import lattice
from universe24.layers.frame48 import compile_frame48
from universe24.layers.frame_matter import compile_matter_frame
from universe24.observe.frame_matter import bank_values, diagnostics
from universe24.prepare.frame48 import prepare as prepare_vacuum
from universe24.prepare.frame_matter import flat_values, prepare, increment


def zero_fields():
    return {name: sp.Integer(0) for name in FIELDS}


class MatterFrameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.program = compile_matter_frame()

    def test_stress_and_gravitational_source_against_four_tensor(self):
        fields = {name: sp.Integer(i % 5-2) for i, name in enumerate(FIELDS)}
        fields['dust_amplitude'] = 2
        mass_squared = 2
        eta = sp.diag(-1, 1, 1, 1)
        stress4 = sp.zeros(4)
        for phi, pi, gradient in COMPONENTS:
            covector = sp.Matrix([fields[pi]]+[fields[f'{gradient}{a}'] for a in range(3)])
            lagrangian = ((covector.T*eta*covector)[0]+mass_squared*fields[phi]**2)/2
            stress4 += covector*covector.T-eta*lagrangian
        stress4[0, 0] += fields['dust_amplitude']**2
        matter = stress_energy(fields, mass_squared)
        self.assertEqual(matter['rho'], stress4[0, 0])
        self.assertEqual(sp.Matrix(matter['j']), -stress4[1:, 0])
        self.assertEqual(sp.Matrix(matter['S']), stress4[1:, 1:])
        from universe24.algebra.frame_equations import equations as vacuum
        bare, _, _ = vacuum(fields, lambda name, i: 0)
        sourced, _, _ = equations(fields, lambda name, i: 0, mass_squared)
        trace4 = sp.trace(eta*stress4)
        for a, b in SYMMETRIC:
            self.assertEqual(sourced[f'K{a}{b}']-bare[f'K{a}{b}'],
                             -(stress4[a+1, b+1]-int(a == b)*trace4/2))

    def test_nonvacuum_scalar_kasner_against_full_einstein_tensor(self):
        t, x, y, z = coords = sp.symbols('t x y z', positive=True)
        powers, amplitude = (sp.Rational(2, 3), sp.Rational(1, 3), 0), sp.Rational(2, 3)
        fields = zero_fields()
        for i, p in enumerate(powers):
            fields[f'B{i}{i}'], fields[f'K{i}{i}'] = t**(-p), -p/t
        fields['phi'], fields['Pi'] = amplitude*sp.log(t), amplitude/t
        rhs, constraints, _ = equations(fields, lambda name, i: 0, mass_squared=0)
        self.assertTrue(all(sp.simplify(v) == 0 for v in constraints.values()))
        for name in FIELDS:
            self.assertEqual(sp.simplify(rhs[name]-sp.diff(fields[name], t)), 0, name)
        metric = sp.diag(-1, *(t**(2*p) for p in powers))
        stress4 = sp.diag(amplitude**2/(2*t*t),
                         *(amplitude**2*t**(2*p)/(2*t*t) for p in powers))
        point = {t: 8, x: 0, y: 0, z: 0}
        oracle = einstein_from_jet(*symbolic_jet(metric, coords, point))
        self.assertNotEqual(oracle['G'], sp.zeros(4))
        self.assertEqual(oracle['G'], stress4.subs(point))

    def test_dust_flrw_against_full_einstein_tensor(self):
        t, x, y, z = coords = sp.symbols('t x y z', positive=True)
        fields = zero_fields()
        for i in range(3):
            fields[f'B{i}{i}'], fields[f'K{i}{i}'] = t**(-sp.Rational(2, 3)), -sp.Rational(2, 3)/t
        fields['dust_amplitude'] = 2/(sp.sqrt(3)*t)
        rhs, constraints, _ = equations(fields, lambda name, i: 0)
        self.assertTrue(all(sp.simplify(v) == 0 for v in constraints.values()))
        for name in FIELDS:
            self.assertEqual(sp.simplify(rhs[name]-sp.diff(fields[name], t)), 0, name)
        metric = sp.diag(-1, *([t**sp.Rational(4, 3)]*3))
        point = {t: 8, x: 0, y: 0, z: 0}
        oracle = einstein_from_jet(*symbolic_jet(metric, coords, point))
        self.assertEqual(oracle['G'], sp.diag((fields['dust_amplitude']**2).subs(point), 0, 0, 0))

    def test_inhomogeneous_scalar_rhs_against_coordinate_wave_operator(self):
        t, x, y, z = coords = sp.symbols('t x y z', real=True)
        spatial_coords = coords[1:]
        lengths = (2+t*x, 3+t+x*x, 2+t*t+x*y)
        spatial = sp.diag(*(v*v for v in lengths))
        rotation = sp.Matrix([[sp.Rational(3, 5), sp.Rational(4, 5), 0],
                              [-sp.Rational(4, 5), sp.Rational(3, 5), 0], [0, 0, 1]])
        B = rotation*sp.diag(*(1/v for v in lengths))
        invB, invg = B.inv(), spatial.inv()
        K = -B*spatial.diff(t)*B.T/2
        christoffel = [[[sum(invg[i, l]*(spatial[l, k].diff(spatial_coords[j])
            +spatial[l, j].diff(spatial_coords[k])-spatial[j, k].diff(spatial_coords[l]))
            for l in range(3))/2 for k in range(3)] for j in range(3)] for i in range(3)]
        fields = zero_fields()
        fields.update({f'B{a}{i}': B[a, i] for a in range(3) for i in range(3)})
        fields.update({f'K{a}{b}': K[a, b] for a, b in SYMMETRIC})
        fields.update({f'G{a}{b}{c}': sum(invB[i, a]*B[c, j]*(B[b, i].diff(spatial_coords[j])
            +sum(christoffel[i][j][k]*B[b, k] for k in range(3)))
            for i in range(3) for j in range(3)) for a, b in ANTISYMMETRIC for c in range(3)})
        scalars = (t*t+t*x+x*y+z, t*y+x*x+y*z)
        for (phi, pi, q), value in zip(COMPONENTS, scalars):
            fields[phi], fields[pi] = value, value.diff(t)
            for a in range(3):
                fields[f'{q}{a}'] = sum(B[a, i]*value.diff(spatial_coords[i]) for i in range(3))
        point = {t: 0, x: 1, y: 0, z: 0}
        at = lambda v: sp.simplify(sp.sympify(v).subs(point))
        derivatives = {(name, i): at(sp.diff(value, coordinate)) for name, value in fields.items()
                       for i, coordinate in enumerate(spatial_coords)}
        rhs, constraints, _ = equations({name: at(value) for name, value in fields.items()},
                                       lambda name, i: derivatives[name, i], mass_squared=2)
        volume = sp.prod(lengths)
        for phi, pi, q in COMPONENTS:
            value = fields[phi]
            box = (-sp.diff(volume*value.diff(t), t)
                   +sum(sp.diff(volume*invg[i, i]*value.diff(coordinate), coordinate)
                        for i, coordinate in enumerate(spatial_coords)))/volume
            self.assertEqual(at(rhs[pi]-value.diff(t, 2)), at(box-2*value))
            for a in range(3):
                self.assertEqual(rhs[f'{q}{a}'], at(fields[f'{q}{a}'].diff(t)))
                self.assertEqual(constraints[f'{q}_gradient{a}'], 0)

    def test_common_metric_link_length_angle_and_tidal_identity(self):
        # Independent continuum geometry oracle only; no dynamic-ratio readout API.
        t = sp.Symbol('t', real=True)
        B0 = sp.Matrix([[2, 1, 0], [0, 1, 1], [0, 0, 3]])
        K = sp.Matrix([[1, 2, 0], [2, -1, 1], [0, 1, 2]])
        B = B0+t*K*B0
        metric = (B.T*B).inv()
        v, w = sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0])
        lv, lw = B0.T.inv()*v, B0.T.inv()*w
        l2, w2, dot = (v.T*metric*v)[0], (w.T*metric*w)[0], (v.T*metric*w)[0]
        at = lambda expression: sp.simplify(expression.subs(t, 0))
        self.assertEqual(at(sp.diff(l2, t)), -2*(lv.T*K*lv)[0])
        cosine = dot/sp.sqrt(l2*w2)
        sv, sw = lv/sp.sqrt(lv.dot(lv)), lw/sp.sqrt(lw.dot(lw))
        expected = -2*(sv.T*K*sw)[0]+sv.dot(sw)*((sv.T*K*sv)[0]+(sw.T*K*sw)[0])
        self.assertEqual(sp.simplify(at(sp.diff(cosine, t))-expected), 0)
        self.assertEqual(at(sp.diff(1-l2, t)), 2*(lv.T*K*lv)[0])
        # Scalar Ricci focusing: trace(dot K-K^2)=(rho+S)/2+Hamiltonian defect.
        fields = {name: sp.Integer(i % 4-1) for i, name in enumerate(FIELDS)}
        rhs, constraints, matter = equations(fields, lambda name, i: 0)
        tidal_trace = sum(rhs[f'K{a}{a}'] for a in range(3))-sum(
            fields[f'K{min(a,b)}{max(a,b)}']**2 for a in range(3) for b in range(3))
        self.assertEqual(sp.simplify(tidal_trace-(matter['rho']+sum(matter['S'][a][a] for a in range(3)))/2),
                         constraints['H'])

    def test_exact_pair_map_with_matter_and_vacuum_reduction(self):
        rng, lat = np.random.default_rng(70), lattice(3)
        old, current = [rng.integers(-1, 2, (35, lat.N)).astype(object) for _ in range(2)]
        r = np.arange(70*lat.N).reshape(70, lat.N) % 6
        seed = prepare(self.program, old, current, L=3, remainders=r)
        engine, state = Engine(self.program.tensor), seed
        for _ in range(3):
            expected = old+increment(self.program, current, lat)
            before, state = state, engine.step(state)
            np.testing.assert_array_equal(bank_values(state, 'X'), current)
            np.testing.assert_array_equal(bank_values(state), expected)
            np.testing.assert_array_equal(state.r, r)
            self.assertTrue(engine.inverse_step(state).same_as(before))
            old, current = current, expected
        self.assertTrue(engine.rewind(state, 3).same_as(seed))
        geometry = rng.integers(-1, 2, (24, lat.N)).astype(object)
        values = flat_values(3)
        values[:24] = geometry
        matter_state = prepare(self.program, values, values, L=3)
        vacuum_program = compile_frame48()
        vacuum_state = prepare_vacuum(vacuum_program, geometry, geometry, L=3)
        for _ in range(3):
            matter_state = engine.step(matter_state)
            vacuum_state = Engine(vacuum_program.tensor).step(vacuum_state)
            for attr in ('a', 'b', 'r'):
                selected = np.concatenate((getattr(matter_state, attr)[:24], getattr(matter_state, attr)[35:59]))
                np.testing.assert_array_equal(selected, getattr(vacuum_state, attr))
            self.assertTrue(all(v == 0 for v in bank_values(matter_state)[24:].flat))

    def test_bidirectional_backreaction_same_tensor(self):
        flat, sourced = flat_values(3), flat_values(3)
        sourced[FIELDS.index('phi')] = 1
        engine = Engine(self.program.tensor)
        plain = engine.step(prepare(self.program, flat, flat, L=3))
        for source in ('phi', 'chi', 'dust_amplitude'):
            probe = flat.copy()
            probe[FIELDS.index(source)] = 1
            changed = engine.step(prepare(self.program, probe, probe, L=3))
            for a in range(3):
                np.testing.assert_array_equal(bank_values(changed)[FIELDS.index(f'K{a}{a}')], -1)
            self.assertFalse(np.array_equal(bank_values(changed)[:24], bank_values(plain)[:24]))
        # Geometric feedback into the same scalar momentum.
        sourced[FIELDS.index('Pi')] = 2
        other = sourced.copy()
        other[FIELDS.index('K00')] = 1
        p0 = bank_values(engine.step(prepare(self.program, sourced, sourced, L=3)))[FIELDS.index('Pi')]
        p1 = bank_values(engine.step(prepare(self.program, other, other, L=3)))[FIELDS.index('Pi')]
        np.testing.assert_array_equal(p1-p0, 4)

    def test_constraints_can_fail_but_squared_dust_stays_nonnegative(self):
        values = flat_values(3)
        for name, value in (('K00', -1), ('K11', -1), ('phi', 1), ('Pi', 1)):
            values[FIELDS.index(name)] = value
        self.assertTrue(diagnostics(values, L=3)['all_discrete_constraints_zero'])
        after = Engine(self.program.tensor).step(prepare(self.program, values, values, L=3))
        self.assertEqual(diagnostics(bank_values(after), L=3)['peak_constraints']['H'], '34')
        dust = flat_values(3)
        dust[FIELDS.index('dust_amplitude')], dust[FIELDS.index('K00')] = 1, -2
        seed = prepare(self.program, dust, dust, L=3)
        after = Engine(self.program.tensor).step(seed)
        np.testing.assert_array_equal(bank_values(after)[FIELDS.index('dust_amplitude')], -1)
        self.assertEqual(diagnostics(bank_values(after), L=3)['negative_dust_nodes'], 0)
        self.assertTrue(Engine(self.program.tensor).inverse_step(after).same_as(seed))

    def test_flux_product_rule_and_scalar_gradient_are_not_assumed(self):
        values = flat_values(3)
        rng = np.random.default_rng(16)
        for name in ('phi', 'Pi', 'Q0', 'chi', 'Pi_chi', 'W0'):
            values[FIELDS.index(name)] = rng.integers(-2, 3, 27).astype(object)
        report = diagnostics(values, L=3)
        self.assertNotEqual(report['peak_energy_balance_defect'], '0')
        self.assertNotEqual(report['peak_charge_balance_defect'], '0')
        self.assertNotEqual(report['peak_constraints']['Q_gradient0'], '0')

    def test_continuum_energy_and_charge_balance_with_product_rule(self):
        fields = {name: sp.Symbol(name, real=True) for name in FIELDS}
        for a in range(3):
            for i in range(3):
                fields[f'B{a}{i}'] = int(a == i)
        for a, b in ANTISYMMETRIC:
            for c in range(3):
                fields[f'G{a}{b}{c}'] = 0
        derivatives = {(name, i): sp.Symbol(f'd{i}_{name}', real=True) for name in FIELDS for i in range(3)}
        for phi, _, q in COMPONENTS:
            for i in range(3):
                derivatives[phi, i] = fields[f'{q}{i}']
        rhs, _, matter = equations(fields, lambda name, i: derivatives[name, i])
        def derivative(expression, i):
            return sum(sp.diff(expression, fields[name])*derivatives[name, i]
                       for name in FIELDS if isinstance(fields[name], sp.Symbol))
        rho_dot = sum(sp.diff(matter['rho'], fields[name])*rhs[name]
                      for name in FIELDS if isinstance(fields[name], sp.Symbol))
        charge_dot = sum(sp.diff(matter['charge'], fields[name])*rhs[name]
                         for name in FIELDS if isinstance(fields[name], sp.Symbol))
        trace = sum(fields[f'K{a}{a}'] for a in range(3))
        work = sum(fields[f'K{min(a,b)}{max(a,b)}']*matter['S'][a][b] for a in range(3) for b in range(3))
        self.assertEqual(sp.expand(rho_dot+sum(derivative(matter['j'][a], a) for a in range(3))
                                   -trace*matter['rho']-work), 0)
        self.assertEqual(sp.expand(charge_dot+sum(derivative(matter['charge_flux'][a], a) for a in range(3))
                                   -trace*matter['charge']), 0)

    def test_same_homogeneous_matter_sources_as_default_adm(self):
        from universe24.layers.adm import FIELDS as ADM_FIELDS, PAIRS, ArrayField, system
        B = sp.Matrix([[2, 1, 0], [0, 1, 1], [0, 0, 3]])
        K = sp.Matrix([[1, 2, 0], [2, -1, 1], [0, 1, 2]])
        metric, coordinate_K = (B.T*B).inv(), B.inv()*K*B.T.inv()
        fields = zero_fields()
        fields.update({f'B{a}{i}': B[a, i] for a in range(3) for i in range(3)})
        fields.update({f'K{a}{b}': K[a, b] for a, b in SYMMETRIC})
        fields.update(phi=2, Pi=3, chi=-1, Pi_chi=2, dust_amplitude=2)
        rhs, constraints, matter = equations(fields, lambda name, i: 0)
        adm = {name: np.full((3, 3, 3), Fraction(0), dtype=object)
               for name in ADM_FIELDS+('chi', 'Pi_chi', 'rho_dark')}
        for i, j in PAIRS:
            adm[f'g{i}{j}'][:] = Fraction(metric[i, j])
            adm[f'K{i}{j}'][:] = Fraction(coordinate_K[i, j])
        adm['alpha'][:] = Fraction(1)
        for name in ('phi', 'Pi', 'chi', 'Pi_chi'):
            adm[name][:] = Fraction(fields[name])
        adm['rho_dark'][:] = Fraction(fields['dust_amplitude']**2)
        adm_rhs, adm_constraints, diagnostic = system({name: ArrayField(value) for name, value in adm.items()}, lapse='geodesic')
        at = lambda array: sp.Rational(array.data.flat[0])
        k_dot_coordinate = sp.Matrix([[at(adm_rhs[f'K{min(i,j)}{max(i,j)}']) for j in range(3)] for i in range(3)])
        k_dot_frame = B*k_dot_coordinate*B.T+2*K*K
        for a, b in SYMMETRIC:
            self.assertEqual(rhs[f'K{a}{b}'], k_dot_frame[a, b])
        for name in ('phi', 'Pi', 'chi', 'Pi_chi'):
            self.assertEqual(rhs[name], at(adm_rhs[name]))
        self.assertEqual(2*fields['dust_amplitude']*rhs['dust_amplitude'], at(adm_rhs['rho_dark']))
        self.assertEqual(matter['rho'], at(diagnostic['rho']))
        self.assertEqual(constraints['H'], at(adm_constraints['H']))

    def test_channel_support_bigints_and_input_contract(self):
        tensor = self.program.tensor
        self.assertEqual((tensor.G, tensor.rank), (70, 3))
        self.assertEqual(tensor.support_violations(), [])
        self.assertTrue(tensor.b_only)
        self.assertTrue(all(m.coeff % 3 == 0 for m in tensor.monomials))
        for kwargs in ({'dt': Fraction(1, 16)}, {'dt': Fraction(1, 2), 'dx': Fraction(1, 2)}):
            with self.assertRaisesRegex(ValueError, 'noninteger'):
                compile_matter_frame(**kwargs)
        self.assertEqual(compile_matter_frame(dx=Fraction(1, 2)).tensor.G, 70)
        for value in (0.5, True, np.float32(1)):
            with self.assertRaises(TypeError):
                compile_matter_frame(mass_squared=value)
        with self.assertRaises(ValueError):
            compile_matter_frame(mass_squared=-1)
        values = flat_values(3)
        with self.assertRaises(TypeError):
            prepare(self.program, values.astype(float), values, L=3)
        values[FIELDS.index('phi')] = 2**70
        state = prepare(self.program, values, values, L=3)
        engine = Engine(tensor)
        after = engine.run(state, 2)
        self.assertGreater(after.max_abs().bit_length(), 140)
        self.assertTrue(engine.rewind(after, 2).same_as(state))

    def test_exact_reversal_does_not_establish_linear_mode_stability(self):
        # Frozen flat KG: leapfrog eigenvalues satisfy z^2-2*i*h*omega*z-1=0.
        # L=3, dx=h=m=1 and k_i=2*pi/3 give omega^2=13/4 > 1.
        omega = sp.sqrt(13)/2
        unstable = sp.I*(omega+sp.sqrt(omega**2-1))
        self.assertEqual(sp.simplify(unstable**2-2*sp.I*omega*unstable-1), 0)
        self.assertGreater(float(sp.Abs(unstable)), 1)

    def test_audit_replay_and_source_hashed_evidence(self):
        from experiments.geometry.frame_matter_audit import audit
        with tempfile.TemporaryDirectory() as directory:
            report = audit(directory)
            records = [json.loads(line) for line in (Path(directory)/'spatial_matter.jsonl').read_text().splitlines()]
            engine = Engine(Tensor.from_dict(records[0]['tensor']))
            state = State.from_dict(records[1]['state'])
            for record in records[2:]:
                state = engine.step(state)
                self.assertTrue(state.same_as(State.from_dict(record['state'])))
            fixture = Path(__file__).resolve().parents[2]/'docs/evidence/frame_matter.json'
            expected = json.loads(fixture.read_text())
            for key in ('cases', 'gates', 'manifest', 'tensor_fingerprint', 'source_sha256'):
                self.assertEqual(report[key], expected[key])
            self.assertFalse(report['gates']['general_einstein_solver_validated'])
            self.assertTrue(report['gates']['bidirectional_scalar_dust_coupling'])


if __name__ == '__main__':
    unittest.main()
