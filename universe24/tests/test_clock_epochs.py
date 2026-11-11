"""Deterministic public clock reports do not alter autonomous trajectories."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.tensor import GearType
from universe24.observe.reference_model import state_hash
from validation.tools.clock_epochs import main, prepare_baseline, run_epochs

ZERO = (0, 0, 0)


def fixture():
    gears = [GearType("clock.hand"), GearType("reader.mode"),
             GearType("clock.audit", label="audit")]
    tensor = Tensor(gears, [("clock.hand", 3, (("clock.hand", ZERO, "b"),)),
                           ("clock.audit", 3, (("clock.audit", ZERO, "b"),))])
    a = np.zeros((3, 27), dtype=np.int64)
    b = np.ones((3, 27), dtype=np.int64)
    return tensor, State(3, a, b, a.copy())


def deterministic_part(report):
    return {key: value for key, value in report.items()
            if key not in ("forward_seconds", "rewind_seconds")}


class ClockEpochTests(unittest.TestCase):
    def test_periodic_fixture_distinguishes_crossing_echo_and_full_state(self):
        tensor, seed = fixture()
        result = run_epochs(tensor, seed, steps=12, hand_indices=[0], reader_indices=[1],
                            sample_every=1, record_symbols=True)
        self.assertTrue(result["exact_rewind"])
        self.assertTrue(result["caller_seed_unchanged"])
        self.assertEqual(result["completed_steps"], 12)
        self.assertEqual(result["exact_full_seed_recurrence_steps"], [12])
        self.assertEqual([row["step"] for row in result["reader_b_echoes"]], [2, 4, 6, 8, 10])
        self.assertEqual([row["step"] for row in result["hand_zero_crossings"]], [3, 6, 9, 12])
        self.assertTrue(all(row["zero_plateau_steps"] == 1 for row in result["hand_zero_crossings"]))
        self.assertTrue(all(row["updates"] == 6 for row in result["same_direction_hand_epochs"]))
        self.assertEqual(result["final_state_hash"], result["initial_state"]["hash"])
        self.assertEqual(result["official_records_by_sector"]["clock"], 8 * 27)
        self.assertEqual(result["official_records_by_sector"]["reader"], 0)
        self.assertEqual(result["symbols"]["counts"]["reader"], [0, 12, 0])
        self.assertEqual(result["symbols"]["sector_order"], ["clock", "reader"])
        self.assertEqual(len(result["symbols"]["series"]), 12)
        self.assertEqual(sum(sum(row) for row in result["symbols"]["transition_counts"]["clock"]), 11)
        json.dumps(result)  # public report contains JSON-native data only

    def test_repeatability_and_observer_noninterference(self):
        tensor, seed = fixture()
        saved, fingerprint = seed.copy(), tensor.fingerprint
        kwargs = dict(steps=13, hand_indices=[0], reader_indices=[1], sample_every=3)
        first = run_epochs(tensor, seed, **kwargs)
        second = run_epochs(tensor, seed, **kwargs)
        self.assertEqual(deterministic_part(first), deterministic_part(second))
        changed_observer = run_epochs(tensor, seed, steps=13, sample_every=1, record_symbols=True,
                                     sector_indices={"all": [0, 1, 2]})
        expected = Engine(tensor).run(seed, 13)
        self.assertEqual(first["final_state_hash"], state_hash(expected, np.arange(tensor.G)))
        self.assertEqual(changed_observer["final_state_hash"], first["final_state_hash"])
        self.assertTrue(seed.same_as(saved))
        self.assertEqual(tensor.fingerprint, fingerprint)
        self.assertIsNone(first["symbols"]["series"])
        self.assertEqual(changed_observer["hand_zero_crossings"], [])
        self.assertEqual(changed_observer["reader_b_echoes"], [])

    def test_resource_gates_stop_after_complete_observed_updates(self):
        tensor = Tensor(["grow"], [("grow", 6, (("grow", ZERO, "b"),) * 2)])
        seed = State(3, [[0] * 27], [[2] * 27], [[0] * 27])
        result = run_epochs(tensor, seed, steps=10, max_counter_bits=2)
        self.assertEqual(result["stop_reason"], "counter_bit_limit")
        self.assertEqual(result["completed_steps"], 1)
        self.assertEqual(result["observed_steps"], 1)
        self.assertEqual(result["final_state_hash"], state_hash(Engine(tensor).step(seed), [0]))
        self.assertTrue(result["exact_rewind"])
        self.assertEqual(result["official_records"], 27)
        initial_stop = run_epochs(tensor, seed, steps=10, max_counter_bits=1)
        self.assertEqual(initial_stop["stop_reason"], "initial_counter_bit_limit")
        self.assertEqual(initial_stop["completed_steps"], 0)
        self.assertTrue(initial_stop["exact_rewind"])
        self.assertEqual(initial_stop["final_state_hash"], initial_stop["initial_state"]["hash"])
        tensor, seed = fixture()
        with patch("validation.tools.clock_epochs.time.monotonic", side_effect=[0, 2, 3, 4, 5]):
            wall_stop = run_epochs(tensor, seed, steps=10, max_seconds=1)
        self.assertEqual(wall_stop["stop_reason"], "forward_wall_budget")
        self.assertEqual(wall_stop["completed_steps"], 1)
        self.assertEqual(wall_stop["rewind_seconds"], 1)
        self.assertTrue(wall_stop["exact_rewind"])

    def test_parameters_and_observer_partitions_validated(self):
        tensor, seed = fixture()
        for key, value in [("steps", 0), ("steps", True), ("max_counter_bits", -1),
                           ("sample_every", 0), ("record_symbols", 1),
                           ("max_seconds", float("inf")), ("max_seconds", True),
                           ("echo_threshold", (0, 20)), ("echo_threshold", (1, 0)),
                           ("hand_indices", [0, 0]), ("reader_indices", [3]),
                           ("hand_indices", [True]), ("sector_indices", {"only": [0]}),
                           ("sector_indices", {"a": [0, 1], "b": [1, 2]})]:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                run_epochs(tensor, seed, **dict(dict(steps=2), **{key: value}))
        bad = seed.copy()
        bad.r[0, 0] = 6
        with self.assertRaises(ValueError):
            run_epochs(tensor, bad, steps=2)
        with self.assertRaises(TypeError):
            run_epochs(None, seed, steps=2)

    def test_sector_growth_is_visible_under_large_constant_background(self):
        tensor = Tensor(['background.hand', 'probe.unstable'],
                        [('background.hand', 6, (('background.hand', ZERO, 'b'),)),
                         ('probe.unstable', 9, (('probe.unstable', ZERO, 'b'),))])
        a = [[1 << 50] * 27, [0] * 27]
        b = [[1 << 50] * 27, [1] * 27]
        seed = State(3, a, b, [[0] * 27] * 2)
        result = run_epochs(tensor, seed, steps=10, sample_every=1)
        self.assertEqual(result['peak_counter_bits'], 51)
        bounds = result['sector_counter_bounds']
        self.assertEqual(bounds['background']['initial'], bounds['background']['final'])
        self.assertGreater(bounds['probe']['final'], 10000 * bounds['probe']['initial'])
        self.assertEqual(bounds['probe']['peak'], bounds['probe']['final'])
        self.assertTrue(result['exact_rewind'])

    def test_zero_reader_norm_disables_echo_and_zero_departure_is_not_crossing(self):
        tensor = Tensor(["drift"], [("drift", 3, ())])
        seed = State(3, [[0] * 27], [[0] * 27], [[0] * 27])
        result = run_epochs(tensor, seed, steps=2, hand_indices=[0], reader_indices=[0], sample_every=1)
        self.assertEqual(result["hand_zero_crossings"], [])
        self.assertEqual(result["reader_b_echoes"], [])
        self.assertTrue(all(row["reader_b_distance"] is None for row in result["samples"]))

    def test_declared_seed_divisor_is_only_initial_data(self):
        tensor, source, metadata = prepare_baseline(L=3)
        other_tensor, reduced, other_metadata = prepare_baseline(L=3, seed_divisor=16)
        self.assertEqual(tensor, other_tensor)
        self.assertEqual(metadata["source_seed_hash"], other_metadata["source_seed_hash"])
        np.testing.assert_array_equal(source.r, reduced.r)
        rows = metadata["scaled_gear_indices"]
        other_rows = [g for g in range(tensor.G) if g not in rows]
        for field in ("a", "b"):
            np.testing.assert_array_equal(getattr(source, field)[other_rows], getattr(reduced, field)[other_rows])
            for old, new in zip(getattr(source, field)[rows].flat, getattr(reduced, field)[rows].flat):
                expected = int(old) // 16 if old >= 0 else -((-int(old)) // 16)
                self.assertEqual(int(new), expected)
        for bad in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                prepare_baseline(seed_divisor=bad)

    def test_cli_writes_only_requested_compact_json(self):
        Path("runs").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir="runs") as folder:
            path = Path(folder) / "report.json"
            with contextlib.redirect_stdout(io.StringIO()):
                report = main(["--steps", "1", "--seed-kind", "none", "--seed-divisor", "16",
                               "--out", str(path)])
            saved = json.loads(path.read_text())
            self.assertEqual(saved, report)
            self.assertEqual(saved["preparation"]["seed_divisor"], 16)
            self.assertTrue(saved["exact_rewind"])
            self.assertEqual([entry.name for entry in Path(folder).iterdir()], ["report.json"])


if __name__ == "__main__":
    unittest.main()
