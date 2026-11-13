"""One fixed six-face law: exact algebra, positive sectors and saved replay.

These are mechanical contracts, not Einstein or quantum acceptance tests.
The truth-table and scalar oracles do not call the Engine evaluator.
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
from universe24.model import (MODEL_ID, coupling_tensor, face_roots, face_roles,
                              decode_faces, sector_map, make_model_bundle,
                              prepare_fields, electromagnetic_fields)
from universe24.runtime import main
from universe24.system.bundle import load_bundle
from universe24.system.checks import scalar_step
from universe24.system.runtime import run_bundle, verify_run


COLLISION = {
    (0, 0, 0): (0, 0, 0), (0, 0, 1): (0, 1, 0),
    (0, 1, 0): (0, 0, 1), (0, 1, 1): (1, 1, 0),
    (1, 0, 0): (1, 0, 0), (1, 0, 1): (1, 0, 1),
    (1, 1, 0): (0, 1, 1), (1, 1, 1): (1, 1, 1),
}


def independent_step(values, L, rr):
    """Stream one face, then apply an independent eight-entry collision table."""
    direction = rr['direction']
    axis = next(i for i, value in enumerate(direction) if value)
    p, m, c = [(values[rr[name]] - 1).reshape(L, L, L)
               for name in ('signal', 'memory', 'clock')]
    p = np.roll(p, direction[axis], axis=axis)
    triples = [COLLISION[tuple(map(int, bits))] for bits in zip(p.flat, m.flat, c.flat)]
    return np.asarray(triples, dtype=object).T + 1


def encoded_face(rr, triple):
    values = {channel: 1 for channel in rr['labels']}
    values.update({channel: 2 for channel in rr['marker_one']})
    values.update({rr[name]: bit + 1 for name, bit in zip(('signal', 'memory', 'clock'), triple)})
    return values


class UnifiedModelContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tensor = coupling_tensor()
        cls.engine = Engine(cls.tensor)

    def test_fixed_cubic_tensor_scalar_oracle_and_all_48_covariances(self):
        law = self.tensor
        self.assertEqual(law.G, 48)
        self.assertEqual(len(law.monomials), 2400)
        self.assertEqual({m.target for m in law.monomials}, set(range(48)))
        self.assertEqual(max(len(m.factors) for m in law.monomials), 3)
        self.assertTrue(all(m.coeff % 3 == 0 for m in law.monomials))
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

    def test_complete_local_polynomial_identity_on_all_phase_and_neighbor_codes(self):
        # Exhaust all 8 local, 8 incoming and 8 outgoing triples in each of 8
        # marker phases. Exact covariance carries this identity to every face.
        terms = [term for term in self.tensor.monomials if term.target == 0]
        direction = face_roles(0)['direction']
        zero, plus = (0, 0, 0), tuple(direction)
        minus = tuple(-v for v in direction)
        bits = tuple(itertools.product((0, 1), repeat=3))
        for phase in range(8):
            rr = face_roles(group().power(1, phase))
            for local, incoming, outgoing in itertools.product(bits, repeat=3):
                values = {zero: encoded_face(rr, local), minus: encoded_face(rr, incoming),
                          plus: encoded_face(rr, outgoing)}
                forward = COLLISION[(incoming[0], local[1], local[2])]
                inverse = (COLLISION[outgoing][0], *COLLISION[local][1:])
                expected = 3 * (encoded_face(rr, forward)[0] + encoded_face(rr, inverse)[0])
                actual = 0
                for term in terms:
                    value = term.coeff
                    for factor in term.factors:
                        self.assertEqual(factor.field, 'b')
                        value *= values[factor.offset][factor.gear]
                    actual += value
                self.assertEqual(actual, expected, (phase, local, incoming, outgoing))
        for before, after in COLLISION.items():
            self.assertEqual(COLLISION[after], before)
            self.assertEqual(sum(before), sum(after))

    def test_all_six_faces_preserve_spatial_positive_sectors_in_all_marker_phases(self):
        rng = np.random.default_rng(7114)
        for phase in range(8):
            with self.subTest(phase=phase):
                fields = {name: rng.integers(0, 2, (6, 27)).astype(object)
                          for name in ('signal', 'memory', 'clock')}
                carry = rng.integers(1, 6, (48, 27))
                initial = prepare_fields(L=3, phases=tuple((phase + face) % 8 for face in range(6)),
                                         carry=carry, **fields)
                decoded = decode_faces(initial.b, 3)
                self.assertEqual(len(decoded), 6)
                self.assertEqual(sorted(g for rr in decoded for g in rr['labels']), list(range(48)))
                state = initial
                for _ in range(4):
                    next_state = self.engine.step(state)
                    np.testing.assert_array_equal(next_state.b, sector_map(state.b, 3))
                    np.testing.assert_array_equal(next_state.a, sector_map(next_state.b, 3, inverse=True))
                    np.testing.assert_array_equal(next_state.r, initial.r)
                    self.assertTrue(all(int(v) in (1, 2) for bank in (next_state.a, next_state.b) for v in bank.flat))
                    for rr in decoded:
                        expected = independent_step(state.b, 3, rr)
                        for name, row in zip(('signal', 'memory', 'clock'), expected):
                            np.testing.assert_array_equal(next_state.b[rr[name]], row)
                        for marker in rr['marker_zero'] + rr['marker_one']:
                            np.testing.assert_array_equal(next_state.b[marker], initial.b[marker])
                        p, m, c = [state.b[rr[name]] - 1 for name in ('signal', 'memory', 'clock')]
                        pn, mn, cn = [next_state.b[rr[name]] - 1 for name in ('signal', 'memory', 'clock')]
                        np.testing.assert_array_equal(mn + cn - mn * cn, m + c - m * c)
                        direction = rr['direction']
                        axis = next(i for i, value in enumerate(direction) if value)
                        incoming = np.roll(p.reshape(3, 3, 3), direction[axis], axis=axis).reshape(-1)
                        np.testing.assert_array_equal(pn + mn * cn - p - m * c, incoming - p)
                    self.assertTrue(self.engine.inverse_step(next_state).same_as(state))
                    state = next_state
                self.assertTrue(self.engine.rewind(state, 4).same_as(initial))

    def test_free_signal_translates_and_transverse_readout_in_all_48_modes(self):
        for root in range(48):
            with self.subTest(root=root):
                bundle = make_model_bundle(L=3, root=root, signal_sites=(0,), memory_sites=(), clock_sites=())
                rr, rotation = face_roles(root), group().rotations[root]
                direction = rr['direction']
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

    def test_clock_phase_intervention_and_reciprocal_feedback(self):
        memory_phase = make_model_bundle(L=5, root=0, signal_sites=(0,), memory_sites=(2,), clock_sites=())
        clock_phase = make_model_bundle(L=5, root=0, signal_sites=(0,), memory_sites=(), clock_sites=(2,))
        self.assertEqual(memory_phase.tensor.fingerprint, clock_phase.tensor.fingerprint)
        a, b = memory_phase.seed, clock_phase.seed
        rr = face_roles(0)
        quiet = make_model_bundle(L=5, root=0, signal_sites=(), memory_sites=(), clock_sites=(2,)).seed
        np.testing.assert_array_equal(a.b[rr['signal']], b.b[rr['signal']])
        differences, feedback = [], []
        for _ in range(4):
            a, b, quiet = (self.engine.step(state) for state in (a, b, quiet))
            differences.append(not np.array_equal(a.b[rr['signal']], b.b[rr['signal']]))
            feedback.append(any(not np.array_equal(b.b[rr[name]], quiet.b[rr[name]])
                                for name in ('memory', 'clock')))
        self.assertTrue(any(differences))
        self.assertTrue(any(feedback))
        self.assertTrue(self.engine.rewind(a, 4).same_as(memory_phase.seed))
        self.assertTrue(self.engine.rewind(b, 4).same_as(clock_phase.seed))

    def test_six_simultaneous_bursts_have_exact_busy_intervals(self):
        L = 7
        coords = np.indices((L, L, L)).reshape(3, -1)
        fields = {name: np.zeros((6, L**3), dtype=object) for name in ('signal', 'memory', 'clock')}
        for face, root in enumerate(face_roots()):
            direction = face_roles(root)['direction']
            axis = next(k for k, value in enumerate(direction) if value)
            size = face % 3 + 1
            fields['memory'][face] = (coords[axis] == 3).astype(object) * 1
            fields['signal'][face] = np.isin(coords[axis], [(3 - direction[axis] * k) % L
                                                           for k in range(1, size + 1)]).astype(object) * 1
        initial = prepare_fields(L=L, **fields)
        state = initial
        occupied = [[] for _ in range(6)]
        for tick in range(1, 5):
            state = self.engine.step(state)
            for face, rr in enumerate(decode_faces(state.b, L)):
                direction = rr['direction']
                axis = next(k for k, value in enumerate(direction) if value)
                site = [0, 0, 0]
                site[axis] = 3
                node = state.lattice.index(*site)
                m, c = (int(state.b[rr[name], node]) - 1 for name in ('memory', 'clock'))
                if m * c:
                    occupied[face].append(tick)
        for face, ticks in enumerate(occupied):
            self.assertEqual(ticks, list(range(1, face % 3 + 2)))
        self.assertTrue(self.engine.rewind(state, 4).same_as(initial))

    def test_actual_busy_traffic_delays_causal_output_difference(self):
        # Paired interventions differ only in the leading incoming bit. Later
        # traffic is identical: this tests information delay, not packet IDs.
        L = 7
        coords = np.indices((L, L, L)).reshape(3, -1)
        fields = {name: np.zeros((6, L**3), dtype=object)
                  for name in ('signal', 'memory', 'clock')}
        targets, neighbours, lengths = [], [], []
        for face, root in enumerate(face_roots()):
            direction = face_roles(root)['direction']
            axis = next(k for k, value in enumerate(direction) if value)
            length = face % 3 + 1
            lengths.append(length)
            fields['memory'][face] = (coords[axis] == 3).astype(object) * 1
            fields['signal'][face] = np.isin(coords[axis],
                [(3 - direction[axis] * k) % L for k in range(1, length + 1)]).astype(object) * 1
            target = [0, 0, 0]
            target[axis] = 3
            neighbour = target.copy()
            neighbour[axis] += direction[axis]
            targets.append(tuple(target))
            neighbours.append(tuple(neighbour))
        control_signal = fields['signal'].copy()
        for face, root in enumerate(face_roots()):
            direction = face_roles(root)['direction']
            axis = next(k for k, value in enumerate(direction) if value)
            control_signal[face, coords[axis] == (3 - direction[axis]) % L] = 0
        experiment = prepare_fields(L=L, **fields)
        control = prepare_fields(L=L, signal=control_signal,
                                 memory=fields['memory'], clock=fields['clock'])
        decoded = decode_faces(experiment.b, L)
        differences = {'target': [[] for _ in range(6)],
                       'neighbour': [[] for _ in range(6)]}
        for tick in range(1, 6):
            experiment, control = self.engine.step(experiment), self.engine.step(control)
            for face, rr in enumerate(decoded):
                for name, locations in (('target', targets), ('neighbour', neighbours)):
                    node = experiment.lattice.index(*locations[face])
                    if experiment.b[rr['signal'], node] != control.b[rr['signal'], node]:
                        differences[name][face].append(tick)
        for face, length in enumerate(lengths):
            with self.subTest(face=face, burst_length=length):
                self.assertTrue(differences['target'][face])
                self.assertTrue(differences['neighbour'][face])
                self.assertEqual(differences['target'][face][0], length + 1)
                self.assertEqual(differences['neighbour'][face][0], length + 2)

    def test_arbitrary_bigint_state_rewinds_exactly(self):
        rng = np.random.default_rng(7115)
        banks = [rng.integers(-2, 3, (48, 27)).astype(object) * (1 << 70) for _ in range(2)]
        arbitrary = State(3, *banks, rng.integers(0, 6, (48, 27)))
        after = self.engine.step(arbitrary)
        self.assertTrue(after.same_as(scalar_step(self.tensor, arbitrary)))
        self.assertTrue(self.engine.inverse_step(after).same_as(arbitrary))

    def test_input_contract_rejects_inexact_incomplete_or_unmarked_preparations(self):
        for options in ({'root': True}, {'root': 48}, {'L': True}, {'L': 2},
                        {'signal_sites': (3,), 'L': 3}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                make_model_bundle(**options)
        empty = np.zeros((6, 27), dtype=object)
        for invalid in (np.zeros((6, 26), dtype=object), np.full((6, 27), 2, dtype=object),
                        np.full((6, 27), 0.5, dtype=object), np.full((6, 27), True, dtype=object)):
            with self.assertRaises(ValueError):
                prepare_fields(L=3, signal=invalid, memory=empty, clock=empty)
        for phases in ((0,) * 5, (0,) * 5 + (8,), (0,) * 5 + (True,)):
            with self.assertRaises(ValueError):
                prepare_fields(L=3, signal=empty, memory=empty, clock=empty, phases=phases)
        for carry in (np.zeros((48, 27), dtype=int), np.full((48, 27), 6),
                      np.ones((48, 26)), np.full((48, 27), 1.5)):
            with self.assertRaises(ValueError):
                prepare_fields(L=3, signal=empty, memory=empty, clock=empty, carry=carry)
        values = make_model_bundle(L=3, root=0).seed.b.copy()
        values[face_roles(0)['signal'], 0] = 3
        with self.assertRaises(ValueError):
            sector_map(values, 3)
        values = make_model_bundle(L=3, root=0).seed.b.copy()
        values[face_roles(0)['marker_one'][0], 0] = 1
        with self.assertRaises(ValueError):
            decode_faces(values, 3)

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
