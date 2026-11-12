"""Retained memory changes later dynamics without a decoder callback."""
import unittest

import numpy as np

from universe24.core.engine import Engine
from validation.selection.pointer import (POINTER_NAME, append_native_pointer,
                                          inspect_control, native_control, velocity)


class SelectionPointerTests(unittest.TestCase):
    def test_causal_write_persistence_then_feedback(self):
        result = inspect_control(native_control(side=5))
        rows = result["local_ticks"]
        self.assertEqual(rows[0]["pulse"], [0, 0])
        self.assertEqual(rows[1]["pulse"], [1, 0])
        self.assertEqual(rows[1]["record_velocity"], [0, 0])
        self.assertTrue(all(row["record_velocity"] == [1, 0] for row in rows[2:]))
        self.assertEqual(rows[2]["response"], [0, 0])
        self.assertEqual(rows[3]["response"], [1, 0])
        self.assertTrue(result["independent_scalar_oracle"])
        self.assertTrue(result["exact_complete_rewind"])

    def test_no_source_and_disconnected_are_not_filtered(self):
        quiet = inspect_control(native_control(side=5, amplitude=0))
        self.assertTrue(all(row["outcomes"] == [] and row["response"] == [0, 0]
                            for row in quiet["local_ticks"]))
        disconnected = inspect_control(native_control(side=5, feedback=0))
        self.assertTrue(all(row["response"] == [0, 0] for row in disconnected["local_ticks"]))
        self.assertEqual(disconnected["local_ticks"][2]["outcomes"], ["left"])

    def test_double_source_does_not_choose_a_single_winner(self):
        result = inspect_control(native_control(side=5, second_amplitude=1))
        self.assertEqual(result["local_ticks"][2]["outcomes"], ["left", "right"])

    def test_periodic_return_changes_record_again(self):
        result = inspect_control(native_control(side=5), steps=7)
        rows = result["local_ticks"]
        self.assertEqual(rows[6]["record_velocity"], [1, 0])
        self.assertEqual(rows[7]["record_velocity"], [2, 0])

    def test_matched_current_state_different_history_changes_future(self):
        ordinary = native_control(side=5)
        changed = native_control(side=5, history=2)
        self.assertTrue(np.array_equal(ordinary.seed.b, changed.seed.b))
        self.assertTrue(np.array_equal(ordinary.seed.r, changed.seed.r))
        self.assertFalse(np.array_equal(ordinary.seed.a, changed.seed.a))
        left = Engine(ordinary.tensor).step(ordinary.seed)
        right = Engine(changed.tensor).step(changed.seed)
        self.assertEqual(ordinary.tensor.fingerprint, changed.tensor.fingerprint)
        self.assertFalse(np.array_equal(left.b[2], right.b[2]))

    def test_all_directions_carries_and_signed_amplitude(self):
        for direction in range(6):
            for carry in range(6):
                result = inspect_control(native_control(side=5, direction=direction,
                                                        carry=carry, amplitude=-2), steps=3)
                self.assertEqual(result["local_ticks"][2]["record_velocity"], [4, 0])
                self.assertEqual(result["local_ticks"][3]["response"], [4, 0])

    def test_append_velocity_identity_and_declared_raw_feedback(self):
        base = native_control(side=5)
        n = base.seed.N
        appended = append_native_pointer(base, writer_name="control.pulse", writer_power=2,
                                         feedback_target="control.response",
                                         memory_a=[[-3] * n], memory_b=[[2] * n],
                                         memory_r=[[i % 6 for i in range(n)]])
        index = appended.tensor.gear_index(POINTER_NAME)
        before = appended.seed
        after = Engine(appended.tensor).step(before)
        expected = velocity(before, index) + before.b[0] ** 2
        self.assertTrue(np.array_equal(velocity(after, index), expected))
        self.assertTrue(np.array_equal(after.r[index], before.r[index]))
        self.assertTrue(Engine(appended.tensor).inverse_step(after).same_as(before))
        self.assertEqual(appended.tensor.G, 4)
        self.assertIn("not supplied", appended.model["physical_record_stress"])
        self.assertIn("not a proved", appended.model["projective_feedback"])

    def test_append_rejects_invalid_degree_and_inexact_initialization(self):
        base = native_control(side=5)
        with self.assertRaises(ValueError):
            append_native_pointer(base, writer_name="control.pulse", writer_power=3,
                                  clock_name="control.response")
        with self.assertRaises((ValueError, TypeError)):
            append_native_pointer(base, writer_name="control.pulse", memory_b=[[0.5] * base.seed.N])
        with self.assertRaises(ValueError):
            append_native_pointer(base, writer_name="control.pulse", feedback=True)


if __name__ == "__main__":
    unittest.main()
