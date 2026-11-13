"""Reversible capacity scattering: algebra, causal controls and honest limits.

Independent local gates and transport oracles never feed the Engine. Passing
these tests does not establish Einstein geometry or universal load balancing.
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
from universe24.model import (MODEL_ID, coupling_tensor, frames, decode_occupation,
                              edge_quartets, edge_gate, sector_map,
                              make_model_bundle, prepare_occupation)
from universe24.runtime import main
from universe24.system.bundle import load_bundle
from universe24.system.checks import scalar_step
from universe24.system.runtime import run_bundle, verify_run


GROUP = group()
TAB = GROUP.multiplication
FRAME = tuple(tuple(rotation[i][0] for i in range(3)) for rotation in GROUP.rotations)
EDGE = next(g for g in range(48) if GROUP.power(g, 2) == GROUP.central
            and FRAME[g] == (-1, 0, 0))
TURN = next(g for g, rotation in enumerate(GROUP.rotations)
            if tuple(rotation[i][0] for i in range(3)) == (0, 1, 0)
            and tuple(rotation[i][1] for i in range(3)) == (0, 0, 1))
ONSITE = TAB[GROUP.inverses[TURN]][EDGE]


def independent_gate(word, inverse=False):
    """Exactly three occupied slots hold; otherwise the quartet rotates."""
    if sum(word) == 3:
        return tuple(word)
    return tuple(word[(i + (1 if inverse else -1)) % 4] for i in range(4))


def independent_quartets(L):
    used, result = set(), []
    for label in range(48):
        for at in range(L**3):
            if (label, at) in used:
                continue
            xyz = np.unravel_index(at, (L, L, L))
            near = np.ravel_multi_index(tuple((xyz[i] + FRAME[label][i]) % L
                                             for i in range(3)), (L, L, L))
            quartet = tuple((TAB[label][GROUP.power(EDGE, k)], at if k % 2 == 0 else near)
                            for k in range(4))
            if used.intersection(quartet):
                raise AssertionError('edge partition overlaps')
            used.update(quartet)
            result.append(quartet)
    if len(used) != 48 * L**3:
        raise AssertionError('edge partition is incomplete')
    return tuple(result)


def independent_step(bits, L, inverse=False):
    if inverse:
        bits = bits[[TAB[label][GROUP.inverses[ONSITE]] for label in range(48)]]
    result = np.empty_like(bits)
    for quartet in independent_quartets(L):
        word = tuple(int(bits[index]) for index in quartet)
        for index, value in zip(quartet, independent_gate(word, inverse)):
            result[index] = value
    if not inverse:
        result = result[[TAB[label][ONSITE] for label in range(48)]]
    return result


def unconditional_transport(bits, L):
    """Permutation-only control: same turns and hops, with no capacity hold."""
    result = np.empty_like(bits)
    for label, direction in enumerate(FRAME):
        axis = next(i for i, value in enumerate(direction) if value)
        result[TAB[label][TURN]] = np.roll(bits[label].reshape(L, L, L),
                                         direction[axis], axis=axis).reshape(-1)
    return result


class UnifiedModelContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tensor = coupling_tensor()
        cls.engine = Engine(cls.tensor)

    def test_fixed_cubic_tensor_scalar_oracle_and_all_48_covariances(self):
        law = self.tensor
        self.assertEqual(tuple(frames()), FRAME)
        self.assertEqual(law.G, 48)
        self.assertEqual(len(law.monomials), 672)
        self.assertEqual({term.target for term in law.monomials}, set(range(48)))
        self.assertEqual(max(len(term.factors) for term in law.monomials), 3)
        self.assertTrue(all(term.coeff % 3 == 0 for term in law.monomials))
        require_equivariant(law)
        rng = np.random.default_rng(4501)
        state = State(3, rng.integers(-4, 5, (48, 27)), rng.integers(-4, 5, (48, 27)),
                      rng.integers(0, 6, (48, 27)))
        after = self.engine.step(state)
        self.assertTrue(after.same_as(scalar_step(law, state)))
        self.assertTrue(self.engine.inverse_step(after).same_as(state))
        for k in range(48):
            with self.subTest(rotation=k):
                self.assertTrue(self.engine.step(act(state, k)).same_as(act(after, k)))

    def test_all_local_gate_words_and_complete_cubic_identity(self):
        for word in itertools.product((0, 1), repeat=4):
            expected = independent_gate(word)
            self.assertEqual(tuple(edge_gate(word)), expected)
            self.assertEqual(tuple(edge_gate(expected, inverse=True)), word)
            self.assertEqual(sum(expected), sum(word))
        for L in (3, 4):
            self.assertEqual(tuple(edge_quartets(L)), independent_quartets(L))
        terms = [term for term in self.tensor.monomials if term.target == 0]
        zero = (0, 0, 0)
        forward_root = TAB[0][ONSITE]
        forward = [(TAB[forward_root][GROUP.power(EDGE, k)],
                    zero if k % 2 == 0 else FRAME[forward_root]) for k in range(4)]
        inverse = [(TAB[TAB[0][GROUP.power(EDGE, k)]][GROUP.inverses[ONSITE]],
                    zero if k % 2 == 0 else FRAME[0]) for k in range(4)]
        keys = tuple(sorted(set(forward + inverse)))
        for bits in itertools.product((0, 1), repeat=len(keys)):
            values = dict(zip(keys, bits))
            expected = 6 + 3 * independent_gate(tuple(values[key] for key in forward))[0]
            expected += 3 * independent_gate(tuple(values[key] for key in inverse), True)[0]
            actual = 0
            for term in terms:
                value = term.coeff
                for factor in term.factors:
                    self.assertEqual(factor.field, 'b')
                    value *= 1 + values[factor.gear, factor.offset]
                actual += value
            self.assertEqual(actual, expected, bits)

    def test_arbitrary_spatial_occupation_is_positive_conservative_and_reversible(self):
        rng = np.random.default_rng(4502)
        for case in range(6):
            with self.subTest(case=case):
                initial = prepare_occupation(L=3, occupation=rng.integers(0, 2, (48, 27)),
                                             carry=rng.integers(1, 6, (48, 27)))
                charge = int(sum((initial.b - 1).flat))
                state = initial
                for _ in range(6):
                    after = self.engine.step(state)
                    np.testing.assert_array_equal(after.b, 1 + independent_step(state.b - 1, 3))
                    np.testing.assert_array_equal(after.a, 1 + independent_step(after.b - 1, 3, True))
                    np.testing.assert_array_equal(after.b, sector_map(state.b, 3))
                    np.testing.assert_array_equal(after.r, initial.r)
                    self.assertTrue(all(int(v) in (1, 2) for bank in (after.a, after.b) for v in bank.flat))
                    self.assertEqual(int(sum((after.b - 1).flat)), charge)
                    self.assertTrue(self.engine.inverse_step(after).same_as(state))
                    state = after
                self.assertTrue(self.engine.rewind(state, 6).same_as(initial))

    def test_free_carrier_has_explicit_microscopic_turning_path(self):
        L = 7
        for root in range(48):
            with self.subTest(root=root):
                occupation = np.zeros((48, L**3), dtype=object)
                xyz = np.array((3, 3, 3))
                occupation[root, np.ravel_multi_index(tuple(xyz), (L, L, L))] = 1
                state = prepare_occupation(L=L, occupation=occupation)
                label = root
                for _ in range(6):
                    xyz = (xyz + np.array(FRAME[label])) % L
                    label = TAB[label][TURN]
                    state = self.engine.step(state)
                    expected = np.zeros_like(occupation)
                    expected[label, np.ravel_multi_index(tuple(xyz), (L, L, L))] = 1
                    np.testing.assert_array_equal(state.b - 1, expected)
                self.assertEqual(label, root)

    def test_downstream_congestion_changes_node_load_not_only_channel_phase(self):
        L, N = 5, 125
        empty = np.zeros((48, N), dtype=object)
        probe, background = empty.copy(), empty.copy()
        source = np.ravel_multi_index((2, 2, 2), (L, L, L))
        downstream = np.ravel_multi_index((3, 2, 2), (L, L, L))
        probe[0, source] = 1
        background[EDGE, downstream] = 1
        background[GROUP.power(EDGE, 3), downstream] = 1
        bits = (empty, probe, background, probe + background)
        states = [prepare_occupation(L=L, occupation=values) for values in bits]
        # No nonlinear interaction is smuggled into preparation histories.
        for bank in ('a', 'b'):
            np.testing.assert_array_equal(getattr(states[3], bank) - getattr(states[2], bank),
                                          getattr(states[1], bank) - getattr(states[0], bank))
        states = [self.engine.step(state) for state in states]
        interaction = states[3].b - states[2].b - states[1].b + states[0].b
        node_interaction = interaction.sum(axis=0)
        self.assertEqual(int(node_interaction[source]), -1)
        self.assertEqual(int(node_interaction[downstream]), 1)
        self.assertEqual(int(sum(abs(v) for v in node_interaction)), 2)
        self.assertEqual(int(sum((states[3].b - states[2].b).flat)), 1)
        control = [unconditional_transport(values, L) for values in bits]
        self.assertFalse(np.any(control[3] - control[2] - control[1] + control[0]))

    def test_default_burst_halo_activates_capacity_feedback(self):
        bundle = make_model_bundle(L=5, pattern='burst', radius=0)
        bits = bundle.seed.b - 1
        self.assertEqual(int(sum(bits.flat)), 54)
        after = self.engine.step(bundle.seed).b - 1
        control = unconditional_transport(bits, 5)
        self.assertFalse(np.array_equal(after.sum(axis=0), control.sum(axis=0)))
        self.assertEqual(int(sum(after.flat)), 54)
        symmetric = make_model_bundle(L=5, pattern='burst', radius=0, halo=False)
        self.assertEqual(int(sum((symmetric.seed.b - 1).flat)), 48)
        np.testing.assert_array_equal(self.engine.step(symmetric.seed).b - 1,
                                      unconditional_transport(symmetric.seed.b - 1, 5))

    def test_symmetric_burst_is_a_free_control_not_adaptive_redistribution(self):
        L = 5
        occupation = np.zeros((48, L**3), dtype=object)
        occupation[:, np.ravel_multi_index((2, 2, 2), (L, L, L))] = 1
        state = prepare_occupation(L=L, occupation=occupation)
        control = occupation.copy()
        for _ in range(15):
            state = self.engine.step(state)
            control = unconditional_transport(control, L)
            np.testing.assert_array_equal(state.b - 1, control)

    def test_capacity_scattering_can_improve_or_worsen_window_concentration(self):
        # Preserve both outcomes. A finite reversible gate is not a universal
        # equalizer, and cherry-picking only the better seed would hide that.
        L = 5
        coords = np.indices((L, L, L)).reshape(3, -1)
        patch = np.all((coords >= 1) & (coords <= 2), axis=0)
        differences = {}
        for seed in (9200, 9205):
            rng = np.random.default_rng(seed)
            occupation = np.zeros((48, L**3), dtype=object)
            occupation[:, patch] = rng.integers(0, 2, (48, int(sum(patch))))
            state = prepare_occupation(L=L, occupation=occupation)
            control = occupation.copy()
            accumulated = 0
            for _ in range(30):
                state = self.engine.step(state)
                control = unconditional_transport(control, L)
                q, q0 = (state.b - 1).sum(axis=0), control.sum(axis=0)
                self.assertEqual(int(sum(q)), int(sum(q0)))
                accumulated += int(sum(q*q) - sum(q0*q0))
            differences[seed] = accumulated
        self.assertGreater(differences[9200], 0)
        self.assertLess(differences[9205], 0)

    def test_homogeneous_preparation_does_not_create_spatial_load_gradient(self):
        channels = np.random.default_rng(4503).integers(0, 2, (48, 1))
        state = prepare_occupation(L=3, occupation=np.repeat(channels, 27, axis=1))
        for _ in range(8):
            state = self.engine.step(state)
            np.testing.assert_array_equal(state.b, np.repeat(state.b[:, :1], 27, axis=1))

    def test_arbitrary_bigint_state_rewinds_exactly(self):
        rng = np.random.default_rng(4504)
        banks = [rng.integers(-2, 3, (48, 27)).astype(object) * (1 << 70) for _ in range(2)]
        state = State(3, *banks, rng.integers(0, 6, (48, 27)))
        after = self.engine.step(state)
        self.assertTrue(after.same_as(scalar_step(self.tensor, state)))
        self.assertTrue(self.engine.inverse_step(after).same_as(state))

    def test_input_contract_rejects_inexact_incomplete_preparations(self):
        for options in ({'root': True}, {'root': 48}, {'L': True}, {'L': 2},
                        {'pattern': 'matter'}, {'radius': -1}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                make_model_bundle(**options)
        for occupation in (np.zeros((48, 26), dtype=object), np.full((48, 27), 2, dtype=object),
                           np.full((48, 27), 0.5, dtype=object), np.full((48, 27), True, dtype=object)):
            with self.assertRaises(ValueError):
                prepare_occupation(L=3, occupation=occupation)
        empty = np.zeros((48, 27), dtype=object)
        for carry in (np.zeros((48, 27), dtype=int), np.full((48, 27), 6),
                      np.ones((48, 26)), np.full((48, 27), 1.5)):
            with self.assertRaises(ValueError):
                prepare_occupation(L=3, occupation=empty, carry=carry)
        with self.assertRaises(ValueError):
            decode_occupation(np.full((48, 27), 3), 3)

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
