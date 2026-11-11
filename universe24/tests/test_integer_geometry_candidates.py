"""Replay optional integer experiments and their explicit failure evidence."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class IntegerGeometryEvidence(unittest.TestCase):
    def test_retired_variable_divisor_runners_fail_explicitly(self):
        retired = ("conformal_metric_probe", "conformal_nonlinear_clock",
                   "phase_metric_probe", "link_metric_check", "carry_locked_metric",
                   "planar_tt_sector", "metric_obstruction_check")
        for name in retired:
            with self.subTest(experiment=name):
                result = subprocess.run(
                    [sys.executable, str(ROOT/"experiments"/"geometry"/(name+".py"))],
                    cwd=ROOT, capture_output=True, text=True, timeout=10)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Retired experiment:", result.stderr)

    def test_published_evidence_replays_from_current_sources(self):
        """Detect stale evidence, changed trajectories, or lost negative controls."""
        output_root = ROOT / "runs" / "tests"
        output_root.mkdir(parents=True, exist_ok=True)
        scripts = ("reciprocal_metric_candidate", "metric_transport_candidate",
                   "exact_constraint_audit")
        with tempfile.TemporaryDirectory(dir=output_root) as directory:
            for name in scripts:
                with self.subTest(experiment=name):
                    output = Path(directory) / (name + ".json")
                    subprocess.run(
                        [sys.executable, str(ROOT / "experiments" / "geometry" / (name + ".py")),
                         "--out", str(output)], cwd=ROOT, check=True,
                        capture_output=True, text=True, timeout=60)
                    actual = json.loads(output.read_text())
                    expected = json.loads((ROOT / "docs" / "evidence" / (name + ".json")).read_text())
                    self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
