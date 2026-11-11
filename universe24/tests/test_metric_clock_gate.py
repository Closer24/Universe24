"""Retired physical presets cannot silently claim success for the new law."""
import unittest
from universe24.tools.metric_clock_gate import run_gate, main
from universe24.tools.connected_clocks import build_candidate
from universe24.tools.physics_gate import run


class MetricClockGateTests(unittest.TestCase):
    def test_variable_divisor_presets_fail_explicitly(self):
        for entry in (run_gate, build_candidate, run):
            with self.subTest(entry=entry.__module__), self.assertRaisesRegex(NotImplementedError, "retired"):
                entry()

    def test_old_metric_cli_explains_retirement(self):
        with self.assertRaisesRegex(SystemExit, "fixed-six"):
            main()
