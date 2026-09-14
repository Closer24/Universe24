"""Exact interference controls do not silently assert trajectory emergence."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_saved_quantum_classical_experiment_reports_physical_limits(tmp_path):
    output = tmp_path / "quantum-classical"
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "examples/quantum/quantum_classical_check.py"),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    report = json.loads((output / "summary.json").read_text())
    assert report["numerical_checks"] == "pass"
    assert report["quantum_to_classical_trajectory_claim"] == "not_established"
    assert [row["visibility"] for row in report["dephasing"]] == [
        "1",
        "9/25",
        "81/625",
        "729/15625",
        "6561/390625",
    ]
    assert report["environment"]["reused_environment"][2]["probabilities"] == ["1", "0"]
    assert report["environment"]["discarded_record_reversal"]["probabilities"] == ["1/2", "1/2"]
    assert report["classical_probabilities"]["records"] == 0
    trajectories = report["trajectory_controls"]
    assert trajectories["classical_trajectory_emergence"] == "not_established"
    assert [row["localized_sample_count"] for row in trajectories["cases"]] == [93, 72, 0]
    assert not trajectories["moving_capture_rejection"]["valid"]
    assert not list(output.rglob("*.html"))
    for row in report["dephasing"]:
        for phase in row["phases"]:
            folder = output / phase["run"]
            assert (folder / "causal-events.jsonl").stat().st_size > 0
            saved_input = json.loads((folder / "initialization.json").read_text())
            assert "tickets" not in saved_input["event_program"]
