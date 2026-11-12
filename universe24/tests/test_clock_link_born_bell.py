"""Falsifying count/weight controls for the research observer, not Born success."""
import unittest

from universe24.core import State, Tensor
from universe24.core.tensor import GearType
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol
from validation.clock_links.born_bell_audit import audit


def mechanical_base():
    """Two inert carrier ports isolate apparatus logic; not the 44-field model."""
    tensor = Tensor([GearType("field.phi", "audit"), GearType("field.chi", "audit")], [])
    seed = State(3, *[[[0] * 27 for _ in range(2)] for _ in range(3)])
    channels = [{"index": index, "name": gear.name, "label": gear.label,
                 "owner": "test_carrier", "purpose": "mechanical apparatus regression only"}
                for index, gear in enumerate(tensor.gears)]
    return create_bundle(tensor, seed, channels=channels, protocol=default_protocol(),
                         model={"id": "test-carrier", "version": "1", "domain": "test fixture"})


class ClockLinkBornBellTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report, cls.trials = audit(mechanical_base())
        cls.cases = {row["case"]: row for row in cls.report["cases"]}

    def test_intensity_weights_do_not_become_one_winner_counts(self):
        row = self.cases["unequal_9_1"]
        self.assertEqual(row["binary_counts"], [36, 36])
        self.assertEqual(row["share_of_binary_events"], ["1/2", "1/2"])
        self.assertEqual(row["share_of_quotient_weights"], ["9/10", "1/10"])
        self.assertEqual(row["outcomes"], {"none": 0, "single": 0, "multiple": 36})
        self.assertEqual(row["C2_selected_trials"], 0)
        self.assertEqual(self.report["Born_binary_frequencies"], "failed")

    def test_zero_and_stationary_nonzero_both_have_empty_detector_stream(self):
        for label in ("zero_source", "stationary_nonzero"):
            self.assertEqual(self.cases[label]["binary_counts"], [0, 0])
            self.assertEqual(self.cases[label]["outcomes"]["none"], 36)
        self.assertEqual(self.cases["stationary_nonzero"]["intensities"], [2, 2])
        obstruction = self.report["receiver_indistinguishability"]
        self.assertEqual([row["Born_ratio_reference"] for row in obstruction["cases"]],
                         [["5/6", "1/6"], ["1/6", "5/6"]])
        self.assertTrue(all(row["four_receiver_records"] == [] for row in obstruction["cases"]))

    def test_all_preparations_rewind_and_phase_controls_interfere(self):
        self.assertEqual(len(self.trials), 252)
        self.assertTrue(all(row["complete_rewind"] for row in self.trials))
        phase = {row["case"]: row["coherent_intensity"] for row in self.report["phase_controls"]}
        self.assertEqual(phase, {"constructive": 4, "destructive": 0,
                                 "quadrature": 2, "common_rotation": 4})
        for label in ("unequal_scaled_36_4", "common_quarter_turn"):
            self.assertEqual(self.cases[label]["share_of_quotient_weights"], ["9/10", "1/10"])
            self.assertEqual(self.cases[label]["binary_counts"], [36, 36])

    def test_local_clock_randomness_retains_chsh_bound(self):
        self.assertEqual(self.report["local_CHSH"]["models_checked"], 6561)
        self.assertEqual(self.report["local_CHSH"]["maximum_CHSH"], "2")
        self.assertFalse(self.report["local_CHSH"]["whole_board_clock_exemption"])
        self.assertEqual(self.report["complexity_postweighting"]["positive_integer_cases"], 1296)
        self.assertEqual(self.report["Bell_violation_from_Engine"], "not_tested")


if __name__ == "__main__":
    unittest.main()
