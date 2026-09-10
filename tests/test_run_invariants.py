"""Detect violations without hiding the underlying candidate-model failure."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Config
from event_universe.diagnostics.frames import Slice
from event_universe.diagnostics.invariants import InertialMotionViolation, require_inertial_momentum
from event_universe.runner import run_scenario
from event_universe.scenarios import Scenario, get_scenario


def test_one_unit_self_impulse_is_rejected():
    with pytest.raises(InertialMotionViolation, match="tick 45"):
        require_inertial_momentum((1, 1, 0), (1, 0, 0), pid=0, tick=45)


def test_unchanged_momentum_is_accepted():
    require_inertial_momentum((3, -2, 1), (3, -2, 1), pid=9, tick=12)


def test_real_self_force_stops_run_even_when_failure_tick_is_not_sampled():
    scenario = Scenario(
        "isolated-self-force-rejection",
        Config(nx=257, ny=257, nz=257, c_units=12, force_den=12),
        ((0, 128, 128, 128, 1, 1, 0),),
        72,
        Slice("XY", 128),
    )
    output = Path("artifacts/isolated-run-rejected")
    with pytest.raises(InertialMotionViolation, match="tick 45"):
        run_scenario(scenario, output, frame_stride=64)
    metadata = json.loads((output / "run.json").read_text())
    assert metadata["status"] == "failed"
    assert metadata["isolated_momentum_check"] == "failed"
    assert metadata["report"]["tick"] == 45
    assert metadata["momentum_equal_at_every_completed_tick"]  # Total conservation is insufficient.
    assert "expected (1, 1, 0), actual (1, 0, 0)" in metadata["error"]
    html = (output / "run.html").read_text()
    assert "FAILED RUN" in html and "ticks 0–45" in html
    assert "data:image/gif;base64," in html
    assert (output / "events.jsonl").read_text()


def test_isolated_stationary_run_remains_valid(tmp_path):
    run_scenario(replace(get_scenario("stationary"), ticks=2), tmp_path)
    metadata = json.loads((tmp_path / "run.json").read_text())
    assert metadata["status"] == "completed"
    assert metadata["isolated_momentum_check"] == "passed"


def test_external_particle_interaction_is_not_misclassified_as_self_force(tmp_path):
    run_scenario(replace(get_scenario("contact"), ticks=16), tmp_path, frame_stride=16)
    metadata = json.loads((tmp_path / "run.json").read_text())
    assert metadata["status"] == "completed"
    assert metadata["isolated_momentum_check"] == "not_applicable"
