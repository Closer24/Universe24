"""Acceptance tests for repeated use and negative organization claims."""
import unittest

from universe24.core import Engine
from validation.local_unification import native, organization


class LocalUnificationOrganizationTests(unittest.TestCase):
    def _fixture(self, *, remove_late=False, coupled=True):
        law, seed, spec = native.repeated_fixture(coupled=coupled)
        if remove_late:
            current = seed.b.copy()
            current[4, seed.lattice.index(-2, 0, 0)] = 0
            current[0, seed.lattice.index(-3, 0, 0)] = 0
            seed = native.prepare_state(current, seed.L, remainders=seed.r)
        engine, states = Engine(law), [seed]
        for _ in range(spec["steps"]):
            states.append(engine.step(states[-1]))
        return law, states

    def test_same_receiver_and_same_stream_repeats_without_reset(self):
        _, states = self._fixture()
        first = organization.functional_trace(states, collision_phase=0)
        second = organization.functional_trace(states, collision_phase=1)
        self.assertEqual([r["step"] for r in first["receiver_events"] if r["kind"] == "correction"], [1, 5])
        self.assertEqual([r["step"] for r in second["receiver_events"] if r["kind"] == "correction"], [2, 6])
        self.assertTrue(first["receiver_repeat_gate"])
        self.assertEqual(first["all_collision_count"], 6*7**3)
        totals = first["totals"]
        self.assertEqual(sum(totals.get(key, 0) for key in
                             ("correction", "unsorting", "tie", "unchanged_split")), 6*7**3)
        self.assertEqual(sum(totals.get(key, 0) for key in
                             ("ready_inputs", "depleted_inputs", "missing_inputs", "double_inputs")), 6*7**3)

    def test_same_law_late_supply_removal_blocks_second_task(self):
        law, states = self._fixture(remove_late=True)
        for phase in (0, 1):
            report = organization.functional_trace(states, collision_phase=phase)
            self.assertEqual(report["receiver_corrections"], 1)
            self.assertFalse(report["receiver_repeat_gate"])
        self.assertTrue(Engine(law).rewind(states[-1], 6).same_as(states[0]))

    def test_disconnected_collision_cannot_receive_functional_credit(self):
        _, states = self._fixture(coupled=False)
        report = organization.functional_trace(states, coupled=False)
        self.assertEqual(report["receiver_corrections"], 0)
        self.assertFalse(report["receiver_repeat_gate"])

    def test_invalid_or_fabricated_collision_is_rejected(self):
        _, states = self._fixture()
        bad = states[1].copy()
        bad.b[2, 0] = 0
        with self.assertRaises(ValueError):
            organization.collision_rows(states[0], bad)
        bad = states[1].copy()
        bad.b[0, 0] = 2
        with self.assertRaises(ValueError):
            organization.collision_rows(states[0], bad)

    def test_exact_preparation_bias_is_not_stationary_growth(self):
        report = organization.stationary_gate_check()
        self.assertEqual(report["exact_means"], {"ready": "1/2", "depleted": "-1/2", "uniform": "0"})
        self.assertEqual(len(report["rows"]), 16)
        self.assertFalse(report["physical_entropy_claim"])

    def test_random_frozen_and_periodic_controls_are_retained(self):
        controls = organization.structural_negative_controls()["controls"]
        self.assertEqual(set(controls), {"fresh_random", "frozen_random", "periodic"})
        self.assertEqual(max(controls["frozen_random"]["scores"]), 38)
        self.assertFalse(controls["frozen_random"]["growth"]["strict_growth"])
        self.assertFalse(controls["periodic"]["growth"]["strict_growth"])


if __name__ == "__main__":
    unittest.main()
