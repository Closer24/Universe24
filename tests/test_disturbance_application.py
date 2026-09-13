"""Public generic initialization, reproducible runs, and explicit visual opt-in."""

import builtins
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_json
from event_universe.runner import main, run_initialization

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("ticks", [0, 12])
def test_open_runner_reports_escape_separately_from_dissipation(ticks, tmp_path):
    artifact = run_initialization(ROOT / "examples" / "open_world.json", tmp_path, ticks=ticks)
    metadata = json.loads(artifact.read_text(encoding="utf-8"))
    state = json.loads((tmp_path / "state.json").read_text(encoding="utf-8"))
    events = [
        json.loads(line) for line in (tmp_path / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    # Straight allocation phases (the default) let four more decaying units
    # dissipate before they reach the boundary; escape + dissipation stays 72.
    escaped = {"strength": [72], "radiation": [16]} if ticks else {"strength": [0], "radiation": [0]}
    assert metadata["status"] == "completed"
    assert metadata["completed_ticks"] == ticks
    assert metadata["boundary"] == state["boundary"] == "open"
    assert metadata["escaped_totals"] == state["escaped_totals"] == escaped
    assert metadata["dissipation_totals"] == {"strength": [0], "radiation": [56 if ticks else 0]}
    assert metadata["accounting_balanced_at_every_completed_tick"]
    assert metadata["conserved_at_every_completed_tick"] == (ticks == 0)
    assert metadata["display"] == "none"
    if ticks:
        exits = [event for event in events if event["event"] == "escaped"]
        assert len(exits) == 1 and exits[0]["tick"] == 1
        assert not any(event["event"] == "received" for event in events)
    else:
        assert events == []


def test_default_package_and_cli_import_only_generic_physics():
    script = """
import sys
sys.path.insert(0, sys.argv[1])
import event_universe.runner
assert event_universe.Simulation.__module__ == 'event_universe.disturbance_api'
for name in sys.modules:
    assert not name.startswith(('matplotlib', 'PIL', 'numpy',
        'event_universe.models', 'event_universe.particle_api', 'event_universe.particle_scenarios',
        'event_universe.core.state', 'event_universe.diagnostics')), name
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(ROOT / "src")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("example", ["basic", "exchange"])
def test_headless_runs_conserve_and_save_only_data(example, tmp_path, monkeypatch):
    original_import = builtins.__import__
    original_snapshot = Simulation.snapshot
    snapshots = []

    def reject_visuals(name, *args, **kwargs):
        assert not name.startswith(("event_universe.diagnostics", "matplotlib", "PIL", "numpy"))
        return original_import(name, *args, **kwargs)

    def count_snapshot(self):
        snapshots.append(self.tick)
        return original_snapshot(self)

    monkeypatch.setattr(builtins, "__import__", reject_visuals)
    monkeypatch.setattr(Simulation, "snapshot", count_snapshot)
    initial = ROOT / "examples" / f"{example}.json"
    artifact = run_initialization(initial, tmp_path)
    metadata = json.loads(artifact.read_text(encoding="utf-8"))
    assert artifact.name == "run.json"
    assert metadata["status"] == "completed"
    assert metadata["display"] == "none"
    assert metadata["completed_ticks"] == metadata["tick"] == 8
    assert metadata["conserved_at_every_completed_tick"]
    assert metadata["initial_totals"] == metadata["final_totals"]
    assert (tmp_path / "initialization.json").read_bytes() == initial.read_bytes()
    assert metadata["initialization_sha256"] == hashlib.sha256(initial.read_bytes()).hexdigest()
    assert snapshots == [8]  # Final report only; no per-tick visual captures.
    assert {item.name for item in tmp_path.iterdir()} == {
        "initialization.json",
        "state.json",
        "events.jsonl",
        "run.json",
    }
    assert (tmp_path / "events.jsonl").read_text(encoding="utf-8")


def test_saved_initialization_and_fingerprint_are_the_starting_payload(tmp_path, monkeypatch):
    initial = tmp_path / "input.json"
    source = (ROOT / "examples" / "exchange.json").read_bytes()
    initial.write_bytes(source)
    original_step = Simulation.step
    hashes = []

    def fingerprint():
        hashes.append("source-at-start")
        return hashes[-1]

    def edit_input_during_run(self):
        initial.write_text("{}", encoding="utf-8")
        original_step(self)

    monkeypatch.setattr("event_universe.runner.source_fingerprint", fingerprint)
    monkeypatch.setattr(Simulation, "step", edit_input_during_run)
    output = tmp_path / "result"
    run_initialization(initial, output, ticks=2)
    metadata = json.loads((output / "run.json").read_text(encoding="utf-8"))
    assert (output / "initialization.json").read_bytes() == source
    assert metadata["initialization_sha256"] == hashlib.sha256(source).hexdigest()
    assert metadata["source_sha256"] == "source-at-start"
    assert hashes == ["source-at-start"]


def test_failed_partial_tick_is_recorded_without_claiming_completed_step(tmp_path, monkeypatch):
    original_step = Simulation.step

    def fail_after_tick(self):
        original_step(self)
        raise ValueError("injected failure")

    monkeypatch.setattr(Simulation, "step", fail_after_tick)
    with pytest.raises(ValueError, match="injected failure"):
        run_initialization(ROOT / "examples" / "exchange.json", tmp_path)
    metadata = json.loads((tmp_path / "run.json").read_text(encoding="utf-8"))
    assert metadata["status"] == "failed"
    assert metadata["completed_ticks"] == 0
    assert metadata["tick"] == 1
    assert metadata["error"] == "injected failure"
    assert (tmp_path / "state.json").is_file()


def test_existing_artifacts_are_preserved(tmp_path):
    marker = tmp_path / "earlier.txt"
    marker.write_text("preserve", encoding="utf-8")
    with pytest.raises(ValueError, match="empty output directory"):
        run_initialization(ROOT / "examples" / "basic.json", tmp_path)
    assert marker.read_text(encoding="utf-8") == "preserve"
    assert list(tmp_path.iterdir()) == [marker]


@pytest.mark.parametrize("source", ['{"schema_version":1,"schema_version":1}', b'{"x":1,"x":2}'])
def test_same_strict_decoder_is_used_for_byte_snapshots(source):
    with pytest.raises(ValueError, match="duplicate JSON key"):
        parse_initial_json(source)


def test_cli_requires_initialization_file(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["event-universe"])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert "--init" in capsys.readouterr().err


@pytest.mark.parametrize("options,visualize", [([], False), (["--visualize"], True)])
def test_cli_visualization_is_explicit(options, visualize, tmp_path, monkeypatch):
    received = {}

    def run(path, output, **kwargs):
        received.update(kwargs)
        received["input"] = path
        return output / "run.json"

    monkeypatch.setattr("event_universe.runner.run_initialization", run)
    monkeypatch.setattr(
        sys, "argv", ["event-universe", "--init", "input.json", "--output", str(tmp_path), *options]
    )
    main()
    assert received["input"] == Path("input.json")
    assert received["visualize"] is visualize


def test_names_do_not_change_any_simulation_values_or_timing():
    source = (ROOT / "examples" / "basic.json").read_text(encoding="utf-8")
    renamed = source
    for before, after in (
        ("mass", "a"),
        ("charge", "b"),
        ("velocity", "direction"),
        ("signal", "quantity"),
        ("computation", "cost"),
        ("carrier", "thing"),
        ("pulse", "stream"),
        ("local_work", "meter"),
    ):
        renamed = renamed.replace(f'"{before}"', f'"{after}"')
    first = Simulation(parse_initial_json(source))
    second = Simulation(parse_initial_json(renamed))
    for _ in range(12):
        first.step()
        second.step()
        assert first.nodes == second.nodes
        assert first.links == second.links
        assert list(first.totals().values()) == list(second.totals().values())
