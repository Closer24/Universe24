"""Replay optional integer experiments and their explicit failure evidence."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class IntegerGeometryEvidence(unittest.TestCase):
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
