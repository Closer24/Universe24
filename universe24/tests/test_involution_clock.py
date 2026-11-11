"""Independent permutation oracle for the fixed Rule3 involution embedding."""
from __future__ import annotations

import unittest

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.reciprocity import check_reciprocity
from universe24.layers.involution_clock import build_involution_clock
from universe24.observe.readout import official_clicks


def local_swap(values):
    """Independent Fredkin truth-table action, not polynomial evaluation."""
    result = values.copy()
    selected = np.flatnonzero(values[0] == 1)
    result[1, selected], result[2, selected] = values[2, selected], values[1, selected]
    return result


def wire_swap(values, L, axis):
    """Independent explicit disjoint swaps of endpoint channel instances."""
    result = values.copy()
    for x in range(L):
        for y in range(L):
            for z in range(L):
                here = (x, y, z)
                there = list(here)
                there[axis] = (there[axis] + 1) % L
                source = (x * L + y) * L + z
                target = (there[0] * L + there[1]) * L + there[2]
                result[2, source] = values[1, target]
                result[1, target] = values[2, source]
    return result


def prepared_seed(tensor, *, L=3, rng_seed=5):
    rng = np.random.default_rng(rng_seed)
    b = rng.integers(0, 2, size=(tensor.G, L ** 3))
    # The large-Q test includes remainders too big for the int64 path.
    D = 6 * tensor.Q
    r = np.array([[int((g + 1) * (node + 3)) % D for node in range(L ** 3)]
                  for g in range(tensor.G)], dtype=object)
    r[0, 0] = D - 1
    return State(L, local_swap(b), b, r)


class InvolutionClockTests(unittest.TestCase):
    def test_all_boolean_triples_are_involutions(self):
        values = np.array([[c, left, right] for c in (0, 1)
                           for left in (0, 1) for right in (0, 1)], dtype=np.int64).T
        np.testing.assert_array_equal(local_swap(local_swap(values)), values)
        self.assertEqual(sorted(map(tuple, local_swap(values).T)), sorted(map(tuple, values.T)))

    def test_many_ticks_match_independent_alternating_oracle(self):
        for Q, axis, spectators in ((1, 0, 0), (17, 1, 0), (2 ** 80 + 1, 2, 45)):
            with self.subTest(Q=Q, axis=axis, spectators=spectators):
                tensor = build_involution_clock(Q=Q, axis=axis, spectators=spectators)
                engine = Engine(tensor, Q)
                seed = prepared_seed(tensor)
                state, expected_b = seed, seed.b.copy()
                data_count = int(seed.b[1:3].sum())
                total_clicks = 0
                for tick in range(1, 121):
                    previous_b = expected_b
                    expected_b = (wire_swap(previous_b, seed.L, axis) if tick % 2
                                  else local_swap(previous_b))
                    next_state = engine.step(state)
                    np.testing.assert_array_equal(next_state.a, previous_b)
                    np.testing.assert_array_equal(next_state.b, expected_b)
                    np.testing.assert_array_equal(next_state.r, seed.r)
                    np.testing.assert_array_equal(next_state.b[0], seed.b[0])
                    self.assertTrue(np.all((next_state.a == 0) | (next_state.a == 1)))
                    self.assertTrue(np.all((next_state.b == 0) | (next_state.b == 1)))
                    self.assertEqual(int(next_state.b[1:3].sum()), data_count)
                    # The complete two-time state contains the alternating phase.
                    phase_a = (wire_swap(next_state.b, seed.L, axis) if tick % 2
                               else local_swap(next_state.b))
                    np.testing.assert_array_equal(next_state.a, phase_a)
                    self.assertTrue(engine.inverse_step(next_state).same_as(state))
                    clicks = official_clicks(engine, state, next_state, tick)
                    total_clicks += len(clicks)
                    self.assertTrue(np.all(clicks.kind == 0))
                    # ell = old a + new b; choose only changed official triples.
                    independent_quotient = state.a + expected_b
                    changed = (state.a != previous_b) | (state.b != expected_b)
                    hit = (independent_quotient != 0) & changed
                    hit[0] = False
                    hit[3:] = False
                    nodes, gears = np.nonzero(hit.T)
                    np.testing.assert_array_equal(clicks.node, nodes)
                    np.testing.assert_array_equal(clicks.gear, gears)
                    np.testing.assert_array_equal(clicks.quotient, independent_quotient[gears, nodes])
                    state = next_state
                self.assertGreater(total_clicks, 0)
                self.assertTrue(engine.rewind(state, 120).same_as(seed))

    def test_single_pulse_propagates_and_control_seed_reflects_it(self):
        tensor = build_involution_clock(Q=5)
        engine = Engine(tensor, 5)
        L, N = 5, 125
        b = np.zeros((3, N), dtype=np.int64)
        b[0] = 1
        b[2, 0] = 1
        r = np.arange(3 * N).reshape(3, N) % engine.D
        seed = State(L, local_swap(b), b, r)
        # Same tensor; the second preparation changes one retained control bit.
        mirrored_b = b.copy()
        mirrored_b[0, L * L] = 0
        mirror = State(L, local_swap(mirrored_b), mirrored_b, r)
        state = seed
        for tick in range(1, 2 * L + 1):
            state = engine.step(state)
            position = ((tick + 1) // 2) % L
            channel = 1 if tick % 2 else 2
            expected = np.zeros((2, N), dtype=np.int64)
            expected[channel - 1, position * L * L] = 1
            np.testing.assert_array_equal(state.b[1:3], expected)
        self.assertTrue(state.same_as(seed))
        open_after_four = engine.run(seed, 4)
        reflected_after_four = engine.run(mirror, 4)
        self.assertEqual(int(open_after_four.b[2, 2 * L * L]), 1)
        self.assertEqual(int(reflected_after_four.b[1, 0]), 1)
        self.assertEqual(int(reflected_after_four.b[0, L * L]), 0)
        self.assertTrue(engine.rewind(reflected_after_four, 4).same_as(mirror))

    def test_disabled_swaps_make_an_exact_period_four_edge_clock(self):
        tensor = build_involution_clock()
        b = np.zeros((3, 27), dtype=np.int64)
        b[2, 0] = 1
        seed = State(3, b.copy(), b, np.zeros_like(b))  # P=identity for c=0
        engine = Engine(tensor, 1)
        state = seed
        for tick in range(1, 5):
            state = engine.step(state)
            if tick < 4:
                self.assertFalse(state.same_as(seed))
        self.assertTrue(state.same_as(seed))

    def test_locality_rank_padding_and_nonreciprocity_are_explicit(self):
        tensor = build_involution_clock(spectators=45)
        self.assertEqual(tensor.G, 48)
        self.assertEqual(tensor.rank, 3)
        self.assertTrue(tensor.b_only)
        self.assertEqual(tensor.support_violations(), [])
        self.assertEqual(len(tensor.designations), 4)
        self.assertEqual(sum("spectator" in name for name in tensor.names), 45)
        designated = check_reciprocity(tensor)
        self.assertTrue(designated.ok)  # exceptions declared, not a reciprocal full map
        self.assertEqual(len(designated.designated), 4)
        stripped = Tensor(tensor.gears, tensor.monomials, Q=tensor.Q)
        self.assertFalse(check_reciprocity(stripped).ok)

    def test_invalid_initial_phase_or_control_is_outside_the_theorem(self):
        tensor = build_involution_clock()
        engine = Engine(tensor, 1)
        seed = prepared_seed(tensor)
        wrong_phase = seed.copy()
        wrong_phase.a[1, 0] += 7
        after = engine.step(wrong_phase)
        self.assertFalse(np.all((after.b == 0) | (after.b == 1)))
        self.assertTrue(engine.inverse_step(after).same_as(wrong_phase))
        # The polynomial is intentionally not asserted to be Fredkin at c=2.
        b = np.zeros((3, 27), dtype=np.int64)
        b[0] = 2
        b[2, 0] = 1
        arbitrary = State(3, b.copy(), b, np.zeros_like(b))
        self.assertGreater(engine.step(arbitrary).max_abs(), 1)

    def test_builder_parameter_validation(self):
        for keyword, value in (("Q", 0), ("Q", True), ("Q", 1.5), ("axis", 3),
                               ("axis", True), ("spectators", -1), ("spectators", True),
                               ("namespace", ""), ("namespace", "not.a.namespace")):
            with self.subTest(keyword=keyword, value=value), self.assertRaises(ValueError):
                build_involution_clock(**{keyword: value})


if __name__ == "__main__":
    unittest.main()
