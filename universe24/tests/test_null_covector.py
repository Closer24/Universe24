"""Exact algebra, compact Engine transport, and limits of the null ansatz."""
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import sympy as sp

from experiments.geometry.compact_null_wave import run
from universe24.algebra.null_covector import ETA, NullCoframe
from universe24.core import Engine, State, Tensor
from universe24.layers.null_wave import build
from universe24.observe.null_wave import geometry
from universe24.prepare.null_wave import prepare


class NullCovectorTests(unittest.TestCase):
    def test_symbolic_inverse_and_determinant_independent_oracle(self):
        F, P = sp.symbols('F P', real=True, nonzero=True)
        eta = sp.diag(*ETA)
        for values in ((1, 0, 0, -1), (5, 3, 4, 0), (3, -2, -1, 2)):
            ell = sp.Matrix(values)
            E = P*sp.eye(4)+F*(eta*ell)*ell.T
            self.assertEqual(sp.expand(E.det()), P**4)
            self.assertEqual(sp.simplify(E.inv()-(2*P*sp.eye(4)-E)/P**2), sp.zeros(4))
            for scale, profile in ((1, -9), (7, 0), (2**70, 2**90+17)):
                decoded = NullCoframe(scale, values).decode(profile)
                expected_E = E.subs({P: scale, F: profile})
                expected_g = expected_E.T*eta*expected_E
                self.assertEqual(sp.Matrix(decoded['coframe'].tolist()), expected_E)
                self.assertEqual(sp.Matrix(decoded['metric'].tolist()), expected_g)
                self.assertEqual(sp.Matrix(decoded['inverse_metric_numerator'].tolist())/scale**3,
                                 expected_g.inv())

    def test_batched_integers_and_mutable_input_are_safe(self):
        ell = [1, 0, 0, -1]
        calibration = NullCoframe(np.int64(3), ell)
        ell[0] = 4
        values = np.array([[0, 2**80], [-2**90, 7]], dtype=object)
        result = calibration.decode(values)
        expected = np.broadcast_to(9*np.eye(4, dtype=object), (2, 2, 4, 4))
        self.assertTrue(np.array_equal(result['coframe']@result['inverse_coframe_numerator'], expected))
        values[:] = 0
        self.assertNotEqual(result['coframe'][0, 1, 0, 3], 0)

    def test_invalid_null_vectors_and_inexact_data_rejected(self):
        for ell in ((0, 0, 0, 0), (1, 0, 0, 0), (1, 1), (1, 1, 1, 0)):
            with self.subTest(ell=ell), self.assertRaises(ValueError):
                NullCoframe(covector=ell)
        for p in (0, -1, [1]):
            with self.subTest(P=p), self.assertRaises(ValueError):
                NullCoframe(p)
        for value in (1.0, True, sp.Rational(1, 2)):
            with self.subTest(value=value), self.assertRaises(TypeError):
                NullCoframe().decode(value)
        with self.assertRaises(TypeError):
            NullCoframe(covector=(1.0, 0, 0, -1))

    def test_two_null_directions_do_not_share_the_inverse_shortcut(self):
        eta = np.diag(np.array(ETA, dtype=object))
        ell, other = np.array([1, 0, 0, -1]), np.array([1, 0, 0, 1])
        L = np.outer(eta@ell, ell)
        M = np.outer(eta@other, other)
        identity = np.eye(4, dtype=object)
        self.assertTrue(np.any((L+M)@(L+M)))
        self.assertFalse(np.array_equal((identity+L+M)@(identity-L-M), identity))
        self.assertEqual(sp.Matrix((2*identity+L+M).tolist()).det(), 0)

    def test_macro_translation_arbitrary_remainders_and_exact_rewind(self):
        tensor, L = build(), 3
        profile = np.array([(-1)**i*(2**80+i) for i in range(L**3)], dtype=object)
        r = np.arange(2*L**3).reshape(2, L**3) % 6
        seed = prepare(tensor, profile, L=L, remainders=r)
        engine = Engine(tensor)
        state = seed
        for tick in range(1, 2*L+1):
            before = state
            state = engine.step(state)
            self.assertTrue(engine.inverse_step(state).same_as(before))
            self.assertTrue(np.array_equal(state.r, r))
            if tick % 2 == 0:
                shift = seed.lattice.shift_index((0, 0, -tick//2))
                self.assertTrue(np.array_equal(state.a, seed.a[:, shift]))
                self.assertTrue(np.array_equal(state.b, seed.b[:, shift]))
                geometry(state, P=2**70)
        self.assertTrue(state.same_as(seed))
        self.assertTrue(engine.rewind(state, 2*L).same_as(seed))
        self.assertEqual(tensor.support_violations(), [])
        self.assertTrue(all(m.degree == 1 and m.coeff == 3 for m in tensor.monomials))

    def test_observer_is_passive_and_rejects_staggered_or_off_sector(self):
        tensor = build()
        seed = prepare(tensor, np.arange(27), L=3)
        saved = seed.copy()
        geometry(seed)
        self.assertTrue(seed.same_as(saved))
        with self.assertRaisesRegex(ValueError, 'macro snapshot'):
            geometry(Engine(tensor).step(seed))
        seed.a[0, 0] += 1
        with self.assertRaisesRegex(ValueError, 'macro snapshot'):
            geometry(seed)

    def test_seed_rejects_invalid_profile_and_remainders(self):
        tensor = build()
        for profile in (np.arange(26), np.zeros((3, 3, 3), dtype=int)):
            with self.assertRaises(ValueError):
                prepare(tensor, profile, L=3)
        with self.assertRaises(TypeError):
            prepare(tensor, np.arange(27, dtype=float), L=3)
        for r in (np.zeros(27, dtype=int), np.full((2, 27), 6), np.full((2, 27), -1)):
            with self.assertRaises(ValueError):
                prepare(tensor, np.arange(27), L=3, remainders=r)

    def test_off_preparation_drift_is_reversible_not_bounded(self):
        tensor = build()
        seed = prepare(tensor, np.zeros(27, dtype=int), L=3)
        seed.a[:] = 1
        engine, state = Engine(tensor), seed
        for tick in range(1, 13):
            state = engine.step(state)
            self.assertTrue(np.all(state.b == -tick))
        self.assertTrue(engine.rewind(state, 12).same_as(seed))

    def test_complete_trace_replays_and_matches_legacy_coframes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'trace.jsonl'
            report = run(trace_path=path)
            records = [json.loads(line) for line in path.read_text().splitlines()]
            engine = Engine(Tensor.from_dict(records[0]['tensor']))
            state = State.from_dict(records[1]['state'])
            for tick, record in enumerate(records[2:], 1):
                state = engine.step(state)
                self.assertEqual(record['tick'], tick)
                self.assertTrue(state.same_as(State.from_dict(record['state'])))
            self.assertEqual(report['comparison']['coframe_and_metric_mismatches'], 0)
            self.assertTrue(report['complete_state']['exact_cycle'])
            self.assertEqual(report['complete_state']['audit_click_classes'],
                             {'0': 2080, '1': 0, '2': 0})
            expected_path = Path(__file__).resolve().parents[2]/'docs/evidence/compact_null_wave.json'
            self.assertEqual(report, json.loads(expected_path.read_text()))


if __name__ == '__main__':
    unittest.main()
