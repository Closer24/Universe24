"""Full restart composes with CLI artifacts, cumulative ledgers and active leases."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.runner import run_checkpoint, run_initialization

from .test_checkpoint import scenario

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "case", ["basic.json", "finite-open", "native-delayed", "topology/bcc_vectors.json"]
)
def test_runner_restart_matches_continuous_events_and_cumulative_accounting(tmp_path, case):
    initial = tmp_path / "input.json"
    initial.write_text(json.dumps(scenario(case)), encoding="utf-8")
    continuous, first, rest = (tmp_path / name for name in ("continuous", "first", "rest"))
    checkpoint = first / "checkpoint.json"
    run_initialization(initial, continuous, ticks=8)
    run_initialization(initial, first, ticks=3, checkpoint=checkpoint)
    before = checkpoint.read_bytes()
    run_checkpoint(checkpoint, rest, ticks=5, checkpoint=rest / "checkpoint.json")
    assert checkpoint.read_bytes() == before
    assert read(continuous / "state.json") == read(rest / "state.json")
    assert (continuous / "events.jsonl").read_bytes() == (
        (first / "events.jsonl").read_bytes() + (rest / "events.jsonl").read_bytes()
    )
    complete, resumed = read(continuous / "run.json"), read(rest / "run.json")
    assert resumed["start_tick"] == 3 and resumed["completed_ticks"] == 5
    assert resumed["checkpoint_tick"] == resumed["tick"] == 8
    assert resumed["resumed_checkpoint_sha256"] == read(first / "run.json")["checkpoint_sha256"]
    for key in (
        "initial_totals",
        "final_totals",
        "source_totals",
        "escaped_totals",
        "dissipation_totals",
        "computation",
        "accounting_balanced_at_every_completed_tick",
    ):
        assert resumed[key] == complete[key]
    assert resumed["accounting_balanced_at_every_completed_tick"] is True


def test_default_resume_finishes_original_duration_without_replaying_steps(tmp_path, monkeypatch):
    raw = scenario("basic.json")
    raw["ticks"] = 7
    initial = tmp_path / "input.json"
    initial.write_text(json.dumps(raw), encoding="utf-8")
    checkpoint = tmp_path / "saved.json"
    run_initialization(initial, tmp_path / "first", ticks=3, checkpoint=checkpoint)
    steps = []
    actual = Simulation.step

    def step(world):
        steps.append(world.tick)
        actual(world)

    monkeypatch.setattr(Simulation, "step", step)
    run_checkpoint(checkpoint, tmp_path / "rest")
    assert steps == [3, 4, 5, 6]
    report = read(tmp_path / "rest/run.json")
    assert report["requested_ticks"] == 4 and report["tick"] == 7


def test_cli_continues_checkpoint_in_a_new_python_process(tmp_path):
    initial = ROOT / "examples/basic.json"
    checkpoint = tmp_path / "saved.json"
    run_initialization(initial, tmp_path / "first", ticks=2, checkpoint=checkpoint)
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUTF8": "1"}
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "event_universe",
            "--resume",
            str(checkpoint),
            "--ticks",
            "2",
            "--output",
            str(tmp_path / "resumed"),
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    run_initialization(initial, tmp_path / "complete", ticks=4)
    assert read(tmp_path / "resumed/state.json") == read(tmp_path / "complete/state.json")


def test_checkpoint_cannot_overwrite_inputs_or_reserved_run_artifacts(tmp_path):
    initial = tmp_path / "input.json"
    initial.write_text(json.dumps(scenario("basic.json")), encoding="utf-8")
    original = initial.read_bytes()
    for target in (initial, tmp_path / "out/state.json", tmp_path / "out/run.json"):
        with pytest.raises(ValueError, match="checkpoint"):
            run_initialization(initial, tmp_path / "out", ticks=0, checkpoint=target)
        assert initial.read_bytes() == original and not (tmp_path / "out").exists()


def test_failed_step_keeps_failure_evidence_without_saving_a_checkpoint(tmp_path, monkeypatch):
    def fail(world):
        raise ValueError("planned failure")

    monkeypatch.setattr(Simulation, "step", fail)
    target = tmp_path / "out/checkpoint.json"
    with pytest.raises(ValueError, match="planned failure"):
        run_initialization(ROOT / "examples/basic.json", tmp_path / "out", ticks=1, checkpoint=target)
    assert not target.exists()
    assert read(tmp_path / "out/run.json")["status"] == "failed"
