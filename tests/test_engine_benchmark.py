"""Benchmark evidence includes executed events, frozen proposals and stable repeats."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from tests.test_disturbance_engine import document, kind
from tools import make_scheduling_benchmark_inputs as scheduling_inputs
from tools.benchmark_engine import benchmark, physical_state, trace

ROOT = Path(__file__).resolve().parents[1]


def test_trace_repeats_exactly_and_detects_pending_proposal_changes():
    initial = parse_initial_state(
        document(
            [kind("moving", mode="move", weights=[1, 0, 0, 0, 0, 0])],
            [((2, 2, 2), "moving")],
            budget=1,
        )
    )
    left, right = trace(initial, 6), trace(initial, 6)
    assert left == right and left["error"] is None
    assert left["events"] > 0 and len(set(left["state_hashes"])) > 1
    world = Simulation(initial)
    world.step()
    cell = world._cells[(2, 2, 2)]
    assert cell.pending is not None
    before = physical_state(world)
    cell.pending = replace(cell.pending, next_tick=cell.pending.next_tick + 1)
    assert physical_state(world) != before


def test_headless_benchmark_keeps_checks_and_separates_timing_from_trace(tmp_path):
    result = benchmark(ROOT / "examples/basic.json", tmp_path / "sample", 2, 2)
    assert result["trace"]["error"] is None and result["trace"]["tick"] == 2
    assert len(result["stepping_seconds"]) == len(result["audited_seconds"]) == 2
    assert len(result["trace"]["state_hashes"]) == 3
    assert (tmp_path / "sample/audit-001/run.json").is_file()
    assert not list(tmp_path.rglob("*.html")) and not list(tmp_path.rglob("*.gif"))


def test_scheduling_inputs_have_independent_moving_and_stationary_controls(tmp_path, monkeypatch):
    destination = tmp_path / "inputs"
    monkeypatch.setattr("sys.argv", ["make-inputs", "--output", str(destination)])
    scheduling_inputs.main()
    sparse = Simulation(parse_initial_state(json.loads((destination / "sparse.json").read_text())))
    dense = Simulation(parse_initial_state(json.loads((destination / "dense.json").read_text())))
    sparse.step()
    dense.step()
    assert sparse.tick == dense.tick == 1
    assert sparse.totals() == {"inventory": (1,)}
    assert not any(record is not None for record in sparse.cells[(0, 0, 0)].records)
    assert sum(record is not None for record in sparse.cells[(1, 0, 0)].records) == 1
    assert dense.totals() == {"inventory": (100,)}
    assert set(dense.cells) == {(x, y, 0) for x in range(10) for y in range(10)}
    assert all(sum(record is not None for record in cell.records) == 1 for cell in dense.cells.values())
    assert dense.computation_report()["local_cycles_started"] == 100


def test_input_builder_rejects_unrelated_files_before_registering_retention(tmp_path, monkeypatch):
    destination = tmp_path / "existing"
    destination.mkdir()
    keep = destination / "user-notes.txt"
    keep.write_text("preserve this work", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["make-inputs", "--output", str(destination)])

    def unexpected_lease(*args, **kwargs):
        pytest.fail("a nonempty directory was enrolled in retention")

    monkeypatch.setattr(scheduling_inputs, "ArtifactLease", unexpected_lease)
    with pytest.raises(SystemExit) as failure:
        scheduling_inputs.main()
    assert failure.value.code == 2
    assert list(destination.iterdir()) == [keep]
    assert keep.read_text(encoding="utf-8") == "preserve this work"
