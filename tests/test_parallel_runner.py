"""Single-world worker selection preserves runner evidence and releases resources."""

import json
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization
from tools.benchmark_engine import benchmark, trace
from tools.make_parallel_benchmark_input import configuration

ROOT = Path(__file__).resolve().parents[1]


def test_parallel_runner_preserves_physics_and_records_host_execution(tmp_path):
    raw = configuration(cells=8, ticks=2)
    raw["observer"] = {"position": [0, 0, 0]}
    source = tmp_path / "pairs.json"
    source.write_text(json.dumps(raw))
    outputs = [tmp_path / "serial", tmp_path / "parallel"]
    for workers, output in zip((1, 2), outputs, strict=True):
        run_initialization(source, output, workers=workers, parallel_threshold=1, chunk_size=2)
    for name in ("initialization.json", "events.jsonl", "state.json", "observations.json"):
        assert (outputs[0] / name).read_bytes() == (outputs[1] / name).read_bytes()
    serial, parallel = [json.loads((output / "run.json").read_text()) for output in outputs]
    assert parallel["execution"]["evaluated_proposals"] > 0
    assert parallel["execution"]["closed"]
    assert parallel["accounting_balanced_at_every_completed_tick"]
    for metadata in (serial, parallel):
        metadata.pop("elapsed_seconds")
        metadata.pop("execution")
    assert serial == parallel
    assert not list(tmp_path.rglob("*.html")) and not list(tmp_path.rglob("*.gif"))


@pytest.mark.parametrize(
    "options", [{"workers": 0}, {"workers": True}, {"parallel_threshold": 0}, {"chunk_size": False}]
)
def test_invalid_execution_options_fail_before_output_creation(tmp_path, options):
    output = tmp_path / "result"
    with pytest.raises(ValueError):
        run_initialization(ROOT / "examples/basic.json", output, **options)
    assert not output.exists()


def test_runner_closes_workers_and_preserves_failure_evidence(tmp_path, monkeypatch):
    closed = []
    close = Simulation.close
    step = Simulation.step

    def fail(world):
        step(world)
        raise ValueError("controlled post-step failure")

    def observed_close(world):
        close(world)
        closed.append(world.execution_report()["closed"])

    monkeypatch.setattr(Simulation, "step", fail)
    monkeypatch.setattr(Simulation, "close", observed_close)
    source = tmp_path / "pairs.json"
    source.write_text(json.dumps(configuration(cells=8, ticks=2)))
    output = tmp_path / "failed"
    with pytest.raises(ValueError, match="controlled post-step failure"):
        run_initialization(source, output, workers=2, parallel_threshold=1, chunk_size=2)
    metadata = json.loads((output / "run.json").read_text())
    assert metadata["status"] == "failed" and metadata["tick"] == 1
    assert metadata["execution"]["evaluated_proposals"] == 8
    assert closed == [True]
    assert (output / "events.jsonl").stat().st_size > 0
    assert (output / "state.json").is_file()


def test_parallel_benchmark_reports_execution_but_hashes_only_physics(tmp_path):
    raw = configuration(cells=4, ticks=2)
    initial = parse_initial_state(raw)
    options = {"workers": 2, "parallel_threshold": 1, "chunk_size": 1}
    assert trace(initial, 2) == trace(initial, 2, **options)
    source = tmp_path / "pairs.json"
    source.write_text(json.dumps(raw))
    result = benchmark(source, tmp_path / "evidence", 2, 1, **options)
    assert result["execution_options"] == options
    assert result["executions"][0]["evaluated_proposals"] == 8
    assert result["executions"][0]["closed"]
    assert result["trace"]["error"] is None
