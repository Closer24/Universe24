"""The retired resolution-lift experiment must not silently claim fixed-six physics."""
import unittest
from universe24.tools.connected_clocks import RETIRED_REASON, build_candidate, paired_control

class ConnectedClocksRetirementTests(unittest.TestCase):
    def test_old_candidate_fails_explicitly(self):
        self.assertIn("fixed-six", RETIRED_REASON)
        with self.assertRaisesRegex(NotImplementedError, "retired"):
            build_candidate(L=3, rng_seed=13)

    def test_old_control_is_not_a_current_physics_result(self):
        with self.assertRaisesRegex(NotImplementedError, "No gravity-dependent"):
            paired_control(None,None,steps=4)
