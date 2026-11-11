"""Default Universe24 integration, conjugate matter, and event provenance."""
from fractions import Fraction
import gzip
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from universe24.core import Engine
from universe24.layers.adm import compile_adm, system, flat_data, ArrayField
from universe24.prepare.einstein import inhomogeneous_scalar, numeric_fields
from validation.adm_reference import run, replay_trace
from universe24.tests.test_adm_integer import execute


class UniverseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.program, cls.parameters = compile_adm(complex_matter=True, dark_matter=True,
                                                  scale=65536, dt=Fraction(1, 128))
        data = flat_data(3, 65536)
        values = {'phi': Fraction(1, 8), 'Pi': Fraction(3, 32),
                  'chi': Fraction(1, 64), 'Pi_chi': Fraction(1, 32),
                  'rho_dark': Fraction(1, 4096), 'K00': Fraction(-1, 16), 'K11': Fraction(-1, 16)}
        # Exact flat homogeneous Hamiltonian constraint, including BOTH scalar
        # components and dark energy density. Momentum constraints vanish.
        twice_rho = sum(values[k] ** 2 for k in ('phi', 'Pi', 'chi', 'Pi_chi')) + 2 * values['rho_dark']
        values['K22'] = (twice_rho - 2 * values['K00'] * values['K11']) / (2 * (values['K00'] + values['K11']))
        for name, value in values.items():
            assert (value * 65536).denominator == 1
            data[name] = np.full((3, 3, 3), int(value * 65536), dtype=object)
        cls.data = data
        cls.final = execute(cls.program, data)
        opposite = {k: (-v if k in ('chi', 'Pi_chi') else v.copy()) for k, v in data.items()}
        cls.conjugate = execute(cls.program, opposite)

    def test_charge_conjugation_through_integer_engine(self):
        p = self.program
        for step in (0, 1):
            charge = p.read(self.final, f'{step}.matter.charge')
            self.assertNotEqual(charge, 0)
            self.assertEqual(charge, -p.read(self.conjugate, f'{step}.matter.charge'))
            for name in self.parameters['fields']:
                sign = -1 if name in ('chi', 'Pi_chi') else 1
                self.assertEqual(p.read(self.final, f'{step}.{name}'),
                                 sign * p.read(self.conjugate, f'{step}.{name}'))
            for i in range(4):
                for j in range(i, 4):
                    for quantity in ('metric', 'stress'):
                        key = f'{step}.{quantity}.{i}{j}'
                        self.assertEqual(p.read(self.final, key), p.read(self.conjugate, key))
            self.assertGreater(p.read(self.final, f'{step}.source.rho_scalar'), 0)
            self.assertGreater(p.read(self.final, f'{step}.source.rho_dark'), 0)
        for name in ('H', 'M0', 'M1', 'M2'):
            self.assertEqual(p.read(self.final, f'0.constraint.{name}'), 0)

    def test_both_scalar_components_source_curvature(self):
        fields = numeric_fields(self.data, 65536)
        rhs, _, diagnostic = system(fields, lapse='geodesic')
        fields2 = dict(fields, chi=fields['chi'] * 2)
        rhs2, _, diagnostic2 = system(fields2, lapse='geodesic')
        delta_v = 3 * float(Fraction(1, 64) ** 2) / 2
        self.assertAlmostEqual(float((rhs2['K00'].data - rhs['K00'].data).flat[0]), -delta_v)
        self.assertGreater(float(diagnostic2['rho'].data.flat[0]), float(diagnostic['rho'].data.flat[0]))
        faster = dict(fields, K00=fields['K00'] * 2)
        rhs3, _, _ = system(faster, lapse='geodesic')
        self.assertNotEqual(float(rhs['Pi_chi'].data.flat[0]), float(rhs3['Pi_chi'].data.flat[0]))

    def test_constrained_board_contains_opposite_charges(self):
        data, scale, _ = inhomogeneous_scalar(3, dark_matter=True, complex_matter=True)
        _, constraints, diagnostic = system(numeric_fields(data, scale), dx=Fraction(1, 3), lapse='geodesic')
        self.assertLess(np.max(abs(constraints['H'].data)), 1e-5)
        self.assertTrue(all(np.max(abs(constraints[f'M{i}'].data)) < 1e-12 for i in range(3)))
        q = diagnostic['charge'].data
        self.assertLess(q.min(), 0)
        self.assertGreater(q.max(), 0)
        self.assertTrue(np.all(diagnostic['rho'].data > 0))

    def test_current_and_stress_against_independent_minkowski_formula(self):
        fields = numeric_fields(flat_data(3), 4096)
        x = 2 * np.pi * np.indices((3, 3, 3))[0] / 3
        fields.update(phi=ArrayField(np.cos(x)), chi=ArrayField(np.sin(x)),
                      Pi=ArrayField(-np.sin(x)), Pi_chi=ArrayField(np.cos(x)))
        _, _, diagnostic = system(fields, dx=Fraction(1, 3))
        np.testing.assert_allclose(diagnostic['current4'][0].data, 1, atol=1e-14)
        np.testing.assert_allclose(diagnostic['charge_spatial_defect'].data, 0, atol=1e-13)
        np.testing.assert_allclose(diagnostic['T4'][0][0].data, diagnostic['rho'].data, atol=1e-14)

    def test_board_and_official_events_replay_actual_state(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            report = run(self.program, self.data, self.parameters, out)
            board = json.loads((out / 'event_board.json').read_text())
            self.assertEqual(board['tensor_fingerprint'], self.program.tensor.fingerprint)
            self.assertEqual(report['event_board']['physical_events'], 54)
            event = board['frames'][1]['events'][0]
            self.assertEqual(event['fields']['chi'], float(self.program.read(self.final, '1.chi')))
            self.assertEqual(event['stress'][0][0], float(self.program.read(self.final, '1.stress.00')))
            self.assertEqual(event['clocks']['normal_rate'], float(self.program.read(self.final, '1.alpha')))
            self.assertEqual(event['clocks']['grid_rate_squared'], -event['metric'][0][0])
            self.assertEqual(event['clocks']['grid_worldline'], 'timelike')
            with gzip.open(out / 'event_tensors_1.json.gz', 'rt') as stream:
                exact_event = json.load(stream)[0]
            pair = exact_event['clocks']['grid_rate_squared']
            self.assertEqual(Fraction(int(pair['numerator_hex'], 16), int(pair['denominator_hex'], 16)),
                             -self.program.read(self.final, '1.metric.00'))
            self.assertIn('Universe24', (out / 'board.html').read_text())
            with gzip.open(out / 'official_events.jsonl.gz', 'rt') as stream:
                self.assertEqual(json.loads(next(stream))['format'], 'Universe24-official-events-v1')
                saved = [json.loads(line) for line in stream]
            actual = []
            engine = Engine(self.program.tensor)
            states = iter(replay_trace(out / 'full_trace.jsonl.gz'))
            before = next(states)
            for tick, after in enumerate(states, 1):
                clicks = engine.clicks(before, after, tick).select('official')
                actual.extend([[tick, int(g), int(n), format(int(q), 'x'), int(k)]
                               for g, n, q, k in zip(clicks.gear, clicks.node, clicks.quotient, clicks.kind)])
                before = after
            self.assertEqual(saved, actual)
            self.assertEqual(len(saved), report['official_event_records'])
            self.assertGreater(len(saved), 0)

    def test_clock_and_workspace_have_audit_labels(self):
        self.assertTrue(all(g.label == 'audit' for g in self.program.tensor.gears if g.name.startswith('clock.')))
        self.assertTrue(any(g.label == 'official' for g in self.program.tensor.gears))
        self.assertTrue(any(g.label == 'audit' for g in self.program.tensor.gears if g.name.startswith('arithmetic.')))

    def test_default_entry_point_is_integrated_runtime(self):
        from universe24.__main__ import main
        from universe24.runtime import main as runtime_main
        self.assertIs(main, runtime_main)
        self.assertEqual(compile_adm.__module__, 'universe24.layers.adm')


if __name__ == '__main__':
    unittest.main()
