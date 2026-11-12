"""Exact physical-packet accounting and retained-history acceptance controls."""
from itertools import product
import unittest

import numpy as np

from universe24.core import DIRECTIONS, Engine, State
from validation.local_unification import native


class NativeLocalUnificationTests(unittest.TestCase):
    def test_collision_involution_and_positive_velocity_accounts(self):
        for bits in product((0, 1), repeat=4):
            out = native.gate(bits)
            self.assertEqual(native.gate(out), bits)
            self.assertEqual(sum(out), sum(bits))
            self.assertEqual(out[0]+out[2], bits[0]+bits[2])
            self.assertEqual(out[1]+out[3], bits[1]+bits[3])
            self.assertEqual(out[0]+out[1], bits[0]+bits[1])
            self.assertEqual(out[2]+out[3], bits[2]+bits[3])
        # Ready record sends either SINGLE carrier to the plus port and keeps
        # its origin in the recoiling record.  No and double outcomes stay.
        self.assertEqual(native.gate((1, 0, 0, 1)), (0, 1, 1, 0))
        self.assertEqual(native.gate((1, 0, 1, 0)), (1, 0, 1, 0))
        self.assertEqual(native.gate((1, 0, 0, 0)), (1, 0, 0, 0))
        self.assertEqual(native.gate((1, 0, 1, 1)), (1, 0, 1, 1))

    def test_same_receiver_repeats_with_exported_complete_records(self):
        selected_by_control = {}
        for label, coupled, moving in (("on", True, True), ("off", False, True),
                                        ("stationary_records", True, False)):
            tensor, seed, protocol = native.repeated_fixture(coupled=coupled, stream_records=moving)
            state = seed
            engine = Engine(tensor)
            selected = []
            for step in range(1, 7):
                incoming = tuple(int(x) for x in state.b[4:8, protocol["receiver"]])
                after = engine.step(state)
                output = tuple(int(x) for x in after.b[:4, protocol["receiver"]])
                if incoming == (1, 0, 0, 1) and output == (0, 1, 1, 0):
                    selected.append(step)
                self.assertTrue(np.array_equal(after.b, native.first_order(
                    state.b, seed.L, coupled=coupled, stream_records=moving)))
                self.assertTrue(engine.inverse_step(after).same_as(state))
                state = after
            self.assertTrue(engine.rewind(state, 6).same_as(seed))
            selected_by_control[label] = selected
        self.assertEqual(selected_by_control["on"], [1, 2, 5, 6])
        self.assertEqual(selected_by_control["off"], [])
        self.assertNotEqual(selected_by_control["stationary_records"], [1, 2, 5, 6])

    def test_all_axes_nonzero_carries_and_full_inverse(self):
        rng = np.random.default_rng(6302)
        for direction in DIRECTIONS:
            tensor = native.build_tensor(direction)
            self.assertEqual(tensor.G, 8)
            self.assertLessEqual(tensor.rank, 4)
            self.assertFalse(tensor.support_violations())
            self.assertTrue(all(f.field == "b" for m in tensor.monomials for f in m.factors))
            current = rng.integers(0, 2, size=(8, 27)).astype(object)
            carries = np.asarray([[(g+n) % 6 for n in range(27)] for g in range(8)], dtype=object)
            seed = native.prepare_state(current, 3, direction, remainders=carries)
            state = seed
            engine = Engine(tensor)
            for step in range(1, 7):
                after = engine.step(state)
                self.assertTrue(np.array_equal(after.b, native.first_order(state.b, 3, direction)))
                self.assertTrue(np.array_equal(after.r, carries))
                self.assertEqual(native.totals(after.b), native.totals(seed.b))
                self.assertTrue(native.validate_prepared_state(after, direction))
                self.assertTrue(engine.inverse_step(after).same_as(state))
                self.assertTrue(all(int(k) == 0 for k in engine.clicks(state, after, step).kind))
                state = after
            self.assertTrue(engine.rewind(state, 6).same_as(seed))

    def test_history_condition_is_necessary_and_not_a_runtime_projection(self):
        tensor = native.build_tensor()
        current = np.zeros((8, 27), dtype=object)
        good = native.prepare_state(current, 3)
        bad = good.copy()
        bad.a[0, 0] = 1
        with self.assertRaises(ValueError):
            native.validate_prepared_state(bad)
        after = Engine(tensor).step(bad)
        self.assertEqual(int(after.b[0, 0]), -1)
        self.assertTrue(Engine(tensor).inverse_step(after).same_as(bad))
        self.assertEqual(int(bad.a[0, 0]), 1)

    def test_complete_carrier_matched_record_intervention(self):
        for coupled in (True, False):
            tensor, left, right = native.matched_record_pair(coupled=coupled)
            for field in ("a", "b", "r"):
                self.assertTrue(np.array_equal(getattr(left, field)[list(native.ROLES["carrier"])],
                                               getattr(right, field)[list(native.ROLES["carrier"])]))
            self.assertEqual(native.totals(left.b)["energy"], native.totals(right.b)["energy"])
            self.assertNotEqual(native.totals(left.b)["momentum"], native.totals(right.b)["momentum"])
            engine = Engine(tensor)
            after_left, after_right = engine.step(left), engine.step(right)
            differences = int(np.sum(after_left.b[list(native.ROLES["carrier"])] !=
                                     after_right.b[list(native.ROLES["carrier"])]))
            self.assertEqual(differences, 2 if coupled else 0)
            self.assertTrue(engine.inverse_step(after_left).same_as(left))
            self.assertTrue(engine.inverse_step(after_right).same_as(right))

    def test_independent_spatial_oracle_crosses_a_periodic_seam(self):
        current = np.zeros((8, 27), dtype=object)
        current[0, 18] = 1  # A record+ at (2,0,0), goes to B at (0,0,0).
        seed = native.prepare_state(current, 3)
        after = Engine(native.build_tensor()).step(seed)
        self.assertEqual(int(after.b[4, 0]), 1)
        self.assertEqual(sum(int(v) for v in after.b.flat), 1)
        self.assertTrue(np.array_equal(native.first_order(after.b, 3, inverse=True), current))

    def test_invalid_domains_cannot_inherit_the_sector_theorem(self):
        with self.assertRaises(ValueError):
            native.build_tensor(coupled=1)
        with self.assertRaises(ValueError):
            native.build_tensor(stream_records=0)
        with self.assertRaises(ValueError):
            native.build_tensor(direction=(True, 0, 0))
        with self.assertRaises(ValueError):
            native.build_tensor(direction=(1, 1, 0))
        current = np.zeros((8, 27), dtype=object)
        for invalid in (True, 0.0, 2, -1):
            bad = current.copy(); bad[0, 0] = invalid
            with self.assertRaises(ValueError):
                native.prepare_state(bad, 3)
            with self.assertRaises(ValueError):
                native.totals(bad)
        carries = current.copy(); carries[0, 0] = 6
        with self.assertRaises(ValueError):
            native.prepare_state(current, 3, remainders=carries)
        with self.assertRaises(ValueError):
            native.repeated_fixture(L=5)


if __name__ == "__main__":
    unittest.main()
