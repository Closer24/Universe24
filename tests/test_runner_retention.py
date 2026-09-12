"""Retention surrounds complete runner lifetimes without changing physical artifacts."""

import json
import time
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.legacy_runner import run_scenario
from event_universe.retention import cleanup_expired
from event_universe.runner import run_initialization
from event_universe.scenarios import get_scenario

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("legacy", [False, True])
def test_relative_output_in_sibling_directory_is_registered(tmp_path, monkeypatch, legacy):
    working = tmp_path / "working"
    working.mkdir()
    monkeypatch.chdir(working)
    output = Path("../runs/result")
    if legacy:
        run_scenario(replace(get_scenario("stationary"), ticks=0), output)
    else:
        run_initialization(ROOT / "examples/basic.json", output, ticks=0)
    assert (output / "run.json").is_file()
    report = cleanup_expired(tmp_path / "runs", now=time.time() + 86410)
    assert not report["errors"]
    assert not output.exists()


@pytest.mark.parametrize("legacy", [False, True])
@pytest.mark.parametrize("existing", [False, True])
def test_fresh_runs_expire_after_completion_without_touching_original_input(tmp_path, legacy, existing):
    original = tmp_path / "original.json"
    original.write_bytes((ROOT / "examples/basic.json").read_bytes())
    output = tmp_path / "result"
    if existing:
        output.mkdir()
    if legacy:
        run_scenario(replace(get_scenario("stationary"), ticks=0), output)
    else:
        run_initialization(original, output, ticks=0)
    assert json.loads((output / "run.json").read_text())["status"] == "completed"
    cleanup_expired(tmp_path, now=time.time() + 86390)
    assert output.exists()
    cleanup_expired(tmp_path, now=time.time() + 86410)
    assert not output.exists()
    assert original.read_bytes() == (ROOT / "examples/basic.json").read_bytes()


@pytest.mark.parametrize("legacy", [False, True])
def test_nonempty_output_is_rejected_without_changing_existing_files(tmp_path, legacy):
    output = tmp_path / "result"
    output.mkdir()
    original = output / "settings.json"
    original.write_bytes(b'{"keep":"original"}')
    with pytest.raises(ValueError, match="empty output"):
        if legacy:
            run_scenario(replace(get_scenario("stationary"), ticks=0), output)
        else:
            run_initialization(ROOT / "examples/basic.json", output, ticks=0)
    assert list(output.iterdir()) == [original]
    assert original.read_bytes() == b'{"keep":"original"}'


def test_cleanup_cannot_remove_an_active_generic_run(tmp_path, monkeypatch):
    output = tmp_path / "active"
    original_step = Simulation.step
    checks = []

    def step(world):
        cleanup_expired(tmp_path, now=time.time() + 172800)
        checks.append((output / "initialization.json").is_file())
        original_step(world)

    monkeypatch.setattr(Simulation, "step", step)
    run_initialization(ROOT / "examples/basic.json", output, ticks=2)
    assert checks == [True, True]
    assert (output / "run.json").is_file()


def test_failed_run_releases_files_only_after_error_metadata_is_saved(tmp_path, monkeypatch):
    output = tmp_path / "failed"

    def fail(world):
        raise ValueError("controlled failure")

    monkeypatch.setattr(Simulation, "step", fail)
    with pytest.raises(ValueError, match="controlled failure"):
        run_initialization(ROOT / "examples/basic.json", output, ticks=1)
    assert json.loads((output / "run.json").read_text())["status"] == "failed"
    cleanup_expired(tmp_path, now=time.time() + 86410)
    assert not output.exists()
