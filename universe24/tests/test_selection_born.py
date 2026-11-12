"""Independent outcome/measure checks on the new native selectors."""
from fractions import Fraction
import gzip
from itertools import product
from pathlib import Path
import tempfile
import unittest

from universe24.core import Engine, exact_json
from universe24.system.decoder import decode_transition, make_transition
from validation.selection.pointer import native_control
from validation.selection.born import (
    bell_control, cycle_measures, gate_audit, literal_gate, pointer_audit, row_step, verify_saved,
)


class NativeSelectionBornTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gate = gate_audit(carries=(0,))
        cls.pointer = pointer_audit(carries=(0,))

    def test_exclusive_condition_retains_origin_in_memory(self):
        for m, x, y in product((0, 1), repeat=3):
            memory, xp, yp = literal_gate((m, x, y))
            self.assertEqual(xp+yp, x+y)
            if x+y == 1:
                self.assertEqual((xp, yp), (1-m, m))
                self.assertEqual(memory, m ^ y)
        self.assertEqual(len({literal_gate(bits) for bits in product((0, 1), repeat=3)}), 8)

    def test_full_sector_uniformity_and_ready_condition_differ(self):
        self.assertTrue(self.gate["uniform_sector_invariant"])
        self.assertEqual(self.gate["ready_sector_size"], 64)
        self.assertEqual(self.gate["ready_sector_surviving"], 27)
        self.assertEqual(self.gate["uniform_one_particle_local"]["probabilities"]["preferred"], "1/2")
        self.assertEqual(self.gate["ready_one_particle_local"]["probabilities"]["preferred"], "1")

    def test_stationary_translation_symmetric_measures_not_unique(self):
        witnesses = cycle_measures()["stationary_same_particle_number_witnesses"]
        self.assertEqual([row["preferred_lane_probability"] for row in witnesses], ["1/3", "1"])
        for row in witnesses:
            cycle = list(map(tuple, row["cycle"]))
            self.assertEqual([row_step(state) for state in cycle], cycle[1:]+cycle[:1])
            self.assertTrue(row["stationary"] and row["translation_invariant"])

    def test_fixed_gate_transports_a_declared_measure_without_identifying_it(self):
        self.assertTrue(all(row["declared_P_memory_ready"] == row["observed_P_preferred"]
                            for row in self.gate["declared_measure_sensitivity"]))
        self.assertFalse(self.gate["Born_measure_derived"])

    def test_pointer_positive_record_is_not_an_exclusive_two_source_choice(self):
        rows = self.pointer["rows"]
        ready = [row for row in rows if row["family"] == "ready_grid"]
        self.assertEqual(sum(row["outcome"] == "multiple" for row in ready), 16)
        self.assertEqual(sum(row["outcome"] in ("preferred", "other") for row in ready), 8)
        self.assertEqual(sum(row["outcome"] == "none" for row in ready), 1)
        canceled = next(row for row in rows if row["history"] == -1)
        self.assertEqual(canceled["decision_velocity"], [0, 1])
        self.assertEqual(canceled["outcome"], "other")
        self.assertTrue(all(row["complete_inverse"] for row in rows))

    def test_local_stochastic_gate_responses_obey_chsh(self):
        report = bell_control()
        self.assertEqual(report["stochastic_mean_models"], 6561)
        self.assertEqual(Fraction(report["maximum_CHSH"]), 2)
        self.assertTrue(all(row["CHSH"] == 2 for row in report["exact_response_tables"]))
        self.assertEqual(report["physical_Bell_violation"], "not_tested")

    def test_saved_verifier_rejects_valid_but_disconnected_pointer_steps(self):
        bundle = native_control(side=5)
        seed = bundle.seed
        after = Engine(bundle.tensor).step(seed)
        rows = []
        for step in (1, 2):
            # Both transitions are individually lawful but the second starts
            # from the original seed instead of the preceding final state.
            transition = make_transition(bundle.tensor, seed, after,
                                         run_id="pointer:0:0", step=step)
            rows.append({"family": "pointer", "transition": transition,
                         "events": decode_transition(transition, bundle.tensor)})
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bad.jsonl.gz"
            with gzip.open(path, "wt") as stream:
                for row in rows:
                    stream.write(exact_json.dumps(row)+"\n")
            with self.assertRaisesRegex(ValueError, "disconnected"):
                verify_saved(path, {bundle.tensor.fingerprint: bundle.tensor})


if __name__ == "__main__":
    unittest.main()
