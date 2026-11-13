"""One fixed 48-channel law: exact algebra, prepared sectors and saved replay.

These are mechanical contracts and finite sector checks, not Einstein or
quantum acceptance tests. The truth-table oracle does not evaluate the tensor.
"""
import contextlib
import io
import itertools
from pathlib import Path
import tempfile
import unittest

import numpy as np

from universe24.algebra.group_2o import group
from universe24.core import Engine, State
from universe24.core.symmetry import act, require_equivariant
from universe24.model import (MODEL_ID, coupling_tensor, roles, sector_map,
                              make_model_bundle, prepare_fields,
                              electromagnetic_fields)
from universe24.runtime import main
from universe24.system.bundle import load_bundle
from universe24.system.checks import scalar_step
from universe24.system.runtime import run_bundle, verify_run


# Independent Boolean permutation: signal, retained memory, clock phase.
COLLISION = {
    (0, 0, 0): (0, 0, 0), (0, 0, 1): (0, 1, 0),
    (0, 1, 0): (0, 0, 1), (0, 1, 1): (1, 1, 0),
    (1, 0, 0): (1, 0, 0), (1, 0, 1): (1, 0, 1),
    (1, 1, 0): (0, 1, 1), (1, 1, 1): (1, 1, 1),
}


def independent_step(values, L, root):
    """Stream along the selected cube face, then apply the eight-entry table."""
    rr = roles(root)
    direction = tuple(row[0] for row in group().rotations[root])
    axis = next(i for i, value in enumerate(direction) if value)
    p, m, c = [(values[rr[name]] - 1).reshape(L, L, L)
               for name in ('signal', 'memory', 'clock')]
    p = np.roll(p, direction[axis], axis=axis)
    triples = [COLLISION[tuple(map(int, bits))] for bits in zip(p.flat, m.flat, c.flat)]
    return np.asarray(triples, dtype=object).T + 1


class UnifiedModelContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tensor = coupling_tensor()
        cls.engine = Engine(cls.tensor)

    def test_fixed_cubic_tensor_scalar_oracle_and_all_48_covariances(self):
        law = self.tensor
        self.assertEqual(law.G, 48)
        self.assertEqual(len(law.monomials), 1968)
        self.assertEqual({m.target for m in law.monomials}, set(range(48)))
        self.assertEqual(max(len(m.factors) for m in law.monomials), 3)
        require_equivariant(law)
        rng = np.random.default_rng(7113)
        state = State(3, rng.integers(-4, 5, (48, 27)),
                      rng.integers(-4, 5, (48, 27)),
                      rng.integers(0, 6, (48, 27)))
        after = self.engine.step(state)
        self.assertTrue(after.same_as(scalar_step(law, state)))
        self.assertTrue(self.engine.inverse_step(after).same_as(state))
        for k in range(48):
            with self.subTest(rotation=k):
                self.assertTrue(self.engine.step(act(state, k)).same_as(act(after, k)))

    def test_boolean_collision_is_closed_involutive_and_conservative(self):
        self.assertEqual(set(COLLISION), set(itertools.product((0, 1), repeat=3)))
        rr = roles()
        for before, after in COLLISION.items():
            self.assertTrue(all(v in (0, 1) for v in after))
            self.assertEqual(COLLISION[after], before)
            self.assertEqual(sum(before), sum(after))
            fields = {name: np.full(27, bit, dtype=object)
                      for name, bit in zip(('signal', 'memory', 'clock'), before)}
            state = self.engine.step(prepare_fields(L=3, **fields))
            for name, bit in zip(('signal', 'memory', 'clock'), after):
                np.testing.assert_array_equal(state.b[rr[name]], np.full(27, bit + 1))

    def test_all_orientations_preserve_arbitrary_spatial_positive_sectors(self):
        rng = np.random.default_rng(7114)
        for root in range(48):
            with self.subTest(root=root):
                rr = roles(root)
                self.assertEqual(len(set(rr.values())), 5)
                fields = {name: rng.integers(0, 2, 27).astype(object)
                          for name in ('signal', 'memory', 'clock')}
                initial = prepare_fields(L=3, root=root, counter_start=2, **fields)
                state = initial
                initial_count = sum(int(v) - 1 for name in fields for v in initial.b[rr[name]])
                for tick in range(1, 3):
                    expected = independent_step(state.b, 3, root)
                    next_state = self.engine.step(state)
                    np.testing.assert_array_equal(next_state.b, sector_map(state.b, 3, root))
                    for name, row in zip(('signal', 'memory', 'clock'), expected):
                        np.testing.assert_array_equal(next_state.b[rr[name]], row)
                    np.testing.assert_array_equal(next_state.a,
                                                  sector_map(next_state.b, 3, root, inverse=True))
                    np.testing.assert_array_equal(next_state.r, initial.r)
                    self.assertTrue(all(int(v) >= 1 for bank in
                                        (next_state.a, next_state.b, next_state.r) for v in bank.flat))
                    count = sum(int(v) - 1 for name in fields for v in next_state.b[rr[name]])
                    self.assertEqual(count, initial_count)
                    p, m, c = [state.b[rr[name]] - 1 for name in ('signal', 'memory', 'clock')]
                    pn, mn, cn = [next_state.b[rr[name]] - 1 for name in ('signal', 'memory', 'clock')]
                    np.testing.assert_array_equal(mn + cn - mn * cn, m + c - m * c)
                    direction = tuple(row[0] for row in group().rotations[root])
                    axis = next(i for i, value in enumerate(direction) if value)
                    incoming = np.roll(p.reshape(3, 3, 3), direction[axis], axis=axis).reshape(-1)
                    np.testing.assert_array_equal(pn + mn * cn - p - m * c, incoming - p)
                    np.testing.assert_array_equal(next_state.b[rr['counter']],
                                                  initial.b[rr['counter']] + tick)
                    self.assertTrue(self.engine.inverse_step(next_state).same_as(state))
                    state = next_state
                self.assertTrue(self.engine.rewind(state, 2).same_as(initial))

    def test_free_signal_translates_and_transverse_readout_in_every_orientation(self):
        for root in range(48):
            with self.subTest(root=root):
                bundle = make_model_bundle(L=3, root=root, signal_sites=(0,), memory_sites=(), clock_sites=())
                rr, rotation = roles(root), group().rotations[root]
                direction = tuple(row[0] for row in rotation)
                axis = next(i for i, value in enumerate(direction) if value)
                after = self.engine.step(bundle.seed)
                expected = np.roll(bundle.seed.b[rr['signal']].reshape(3, 3, 3), direction[axis], axis=axis)
                np.testing.assert_array_equal(after.b[rr['signal']], expected.reshape(-1))
                electric, magnetic = electromagnetic_fields(after)
                p = after.b[rr['signal']] - 1
                for i in range(3):
                    np.testing.assert_array_equal(electric[i], rotation[i][1] * p)
                    np.testing.assert_array_equal(magnetic[i], rotation[i][2] * p)
                self.assertTrue(all(v == 0 for v in electric[axis]))
                self.assertTrue(all(v == 0 for v in sum(electric[i] * magnetic[i] for i in range(3))))
                self.assertTrue(all(v == 0 for v in sum(electric[i] ** 2 - magnetic[i] ** 2 for i in range(3))))

    def test_clock_phase_intervention_changes_signal_under_same_tensor(self):
        memory_phase = make_model_bundle(L=5, signal_sites=(0,), memory_sites=(2,), clock_sites=())
        clock_phase = make_model_bundle(L=5, signal_sites=(0,), memory_sites=(), clock_sites=(2,))
        self.assertEqual(memory_phase.tensor.fingerprint, clock_phase.tensor.fingerprint)
        a, b = memory_phase.seed, clock_phase.seed
        rr = roles()
        signal = rr['signal']
        quiet = make_model_bundle(L=5, signal_sites=(), memory_sites=(), clock_sites=(2,)).seed
        np.testing.assert_array_equal(a.b[signal], b.b[signal])
        differences, feedback = [], []
        for _ in range(4):
            a, b = self.engine.step(a), self.engine.step(b)
            quiet = self.engine.step(quiet)
            differences.append(not np.array_equal(a.b[signal], b.b[signal]))
            feedback.append(any(not np.array_equal(b.b[rr[name]], quiet.b[rr[name]])
                                for name in ('memory', 'clock')))
        self.assertTrue(any(differences))
        self.assertTrue(any(feedback))
        self.assertTrue(self.engine.rewind(a, 4).same_as(memory_phase.seed))
        self.assertTrue(self.engine.rewind(b, 4).same_as(clock_phase.seed))

    def test_unbounded_counter_and_arbitrary_bigint_state_rewind_exactly(self):
        initial = make_model_bundle(L=3, counter_start=1 << 90).seed
        state, counter = initial, roles()['counter']
        for tick in range(1, 5):
            state = self.engine.step(state)
            np.testing.assert_array_equal(state.b[counter], initial.b[counter] + tick)
        self.assertTrue(self.engine.rewind(state, 4).same_as(initial))
        rng = np.random.default_rng(7115)
        banks = [rng.integers(-2, 3, (48, 27)).astype(object) * (1 << 70) for _ in range(2)]
        arbitrary = State(3, *banks, rng.integers(0, 6, (48, 27)))
        after = self.engine.step(arbitrary)
        self.assertTrue(after.same_as(scalar_step(self.tensor, arbitrary)))
        self.assertTrue(self.engine.inverse_step(after).same_as(arbitrary))

    def test_busy_input_prolongs_stored_occupancy_without_losing_signal(self):
        # Same initial clock phase in every case. Extra incoming ones pass
        # while occupancy remains stored: this is residence, not a FIFO claim.
        rr, target, L = roles(), 3, 7
        for length in (1, 2, 3):
            with self.subTest(incoming_burst=length):
                initial = make_model_bundle(
                    L=L, signal_sites=tuple(target-k for k in range(1, length+1)),
                    memory_sites=(target,), clock_sites=()).seed
                state, stored = initial, []
                node = state.lattice.index(target, 0, 0)
                for tick in range(5):
                    p, m, c = [state.b[rr[name]]-1 for name in ('signal', 'memory', 'clock')]
                    stored.append(int(m[node]*c[node]))
                    self.assertEqual(sum(map(int, p+m*c)), length*L*L)
                    if tick < 4:
                        state = self.engine.step(state)
                self.assertEqual(stored, [0]+[1]*length+[0]*(4-length))
                self.assertTrue(self.engine.rewind(state, 4).same_as(initial))

    def test_input_contract_rejects_inexact_or_incomplete_preparations(self):
        for options in ({'root': True}, {'root': 48}, {'L': True}, {'L': 2},
                        {'signal_sites': (3,), 'L': 3}, {'counter_start': 1.5}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                make_model_bundle(**options)
        empty = np.zeros(27, dtype=object)
        for invalid in (np.zeros(26, dtype=object), np.full(27, 2, dtype=object),
                        np.full(27, 0.5, dtype=object), np.full(27, True, dtype=object)):
            with self.subTest(invalid=invalid[0]), self.assertRaises(ValueError):
                prepare_fields(L=3, signal=invalid, memory=empty, clock=empty)
        values = make_model_bundle(L=3).seed.b.copy()
        values[roles()['signal'], 0] = 3
        with self.assertRaises(ValueError):
            sector_map(values, 3)
        values = make_model_bundle(L=3).seed.b.copy()
        values[roles()['selector'], 0] = 1
        with self.assertRaises(ValueError):
            sector_map(values, 3)

    def test_canonical_bundle_replay_and_physics_gate(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            path = Path(tmp)
            bundle = make_model_bundle(L=3)
            self.assertEqual(bundle.model['id'], MODEL_ID)
            main(['prepare-model', '--size', '3', '--out', str(path / 'bundle')])
            restored = load_bundle(path / 'bundle')
            self.assertEqual(restored.tensor.fingerprint, self.tensor.fingerprint)
            self.assertTrue(restored.seed.same_as(bundle.seed))
            report = run_bundle(restored, path / 'run', 3)
            self.assertEqual(report, verify_run(path / 'run'))
            with self.assertRaises(SystemExit) as caught:
                main(['verify', '--run', str(path / 'run'), '--require-physics'])
            self.assertEqual(caught.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
