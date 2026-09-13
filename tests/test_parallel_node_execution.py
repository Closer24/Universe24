"""Deterministic tick barriers for parallel active-Node planning."""

import json
from dataclasses import replace
from pathlib import Path
from threading import Event, Thread

import pytest

from event_universe import Simulation
from event_universe.initialization import load_initial_state, parse_initial_state
from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("example", "ticks", "shared_delay"),
    [
        ("basic.json", 8, False),
        ("finite_fields.json", 8, False),
        ("finite_fields.json", 8, True),
        ("three_mass_finite.json", 8, False),
        ("spatial_turning.json", 4, False),
        ("local_lorentz_field.json", 8, False),
        ("open_world.json", 8, False),
    ],
)
def test_parallel_node_planning_matches_serial_state_events_and_cost(
    example: str, ticks: int, shared_delay: bool
) -> None:
    path = ROOT / "examples" / example
    if shared_delay:
        document = json.loads(path.read_text(encoding="utf-8"))
        document["spatial_computation_delay"] = True
        initial = parse_initial_state(document)
    else:
        initial = load_initial_state(path)
    serial_events: list[dict[str, object]] = []
    parallel_events: list[dict[str, object]] = []
    serial = Simulation(initial, observer=serial_events.append)
    parallel = Simulation(initial, observer=parallel_events.append, node_workers=2)
    try:
        for _ in range(ticks):
            serial.step()
            parallel.step()
            assert parallel.snapshot() == serial.snapshot()
            assert parallel.totals() == serial.totals()
            assert parallel.source_totals() == serial.source_totals()
            assert parallel.dissipation_totals() == serial.dissipation_totals()
            assert parallel.escaped_totals() == serial.escaped_totals()
        assert parallel_events == serial_events
        assert parallel.computation_report() == serial.computation_report()
        report = parallel.execution_report()
        assert report["backend"] == "isolated-interpreters"
        assert report["node_workers"] == 2
        assert report["disturbance_node_tasks"] > 0
        assert report["parallel_batches"] > 0
        assert report["largest_batch"] > 0
        if example != "basic.json":
            assert report["spatial_node_tasks"] > 0
    finally:
        serial.close()
        parallel.close()


@pytest.mark.parametrize("workers", [True, 0, 65])
def test_node_worker_count_is_bounded(workers: object) -> None:
    initial = load_initial_state(ROOT / "examples" / "basic.json")
    with pytest.raises(ValueError, match="node_workers"):
        Simulation(initial, node_workers=workers)  # type: ignore[arg-type]


def test_event_program_rejects_parallel_execution_before_a_run() -> None:
    initial = load_initial_state(ROOT / "examples" / "quantum" / "native_classical.json")
    with pytest.raises(ValueError, match="event program"):
        Simulation(initial, node_workers=2)


def test_only_one_caller_can_advance_a_tick() -> None:
    initial = load_initial_state(ROOT / "examples" / "basic.json")
    world = Simulation(initial)
    entered, release = Event(), Event()
    original = world._planner

    def blocking(records, residuals, received):
        entered.set()
        assert release.wait(timeout=5)
        return original(records, residuals, received)

    world._services = replace(world._services, planner=blocking)
    worker = Thread(target=world.step)
    worker.start()
    assert entered.wait(timeout=5)
    try:
        with pytest.raises(RuntimeError, match="one caller"):
            world.step()
    finally:
        release.set()
        worker.join(timeout=5)
        world.close()
    assert not worker.is_alive()


def test_runner_records_parallel_host_execution_separately_from_model_cost(tmp_path: Path) -> None:
    artifact = run_initialization(ROOT / "examples" / "basic.json", tmp_path, ticks=2, node_workers=2)
    metadata = json.loads(artifact.read_text(encoding="utf-8"))
    assert metadata["status"] == "completed"
    assert metadata["execution"]["backend"] == "isolated-interpreters"
    assert metadata["execution"]["node_workers"] == 2
    assert metadata["execution"]["disturbance_node_tasks"] > 0
    assert metadata["computation"]["model_operations_cost"] > 0


@pytest.mark.parametrize(
    "example",
    [
        "node-vector/two-fields.json",
        "node-vector/joint-reaction.json",
        "computational-response/moving-pair.json",
    ],
)
def test_local_node_profiles_keep_parallel_events_and_committed_work(example):
    initial = load_initial_state(ROOT / "examples" / example)
    serial_events, parallel_events = [], []
    with (
        Simulation(initial, observer=serial_events.append) as serial,
        Simulation(initial, observer=parallel_events.append, node_workers=2) as parallel,
    ):
        for _ in range(8):
            serial.step()
            parallel.step()
            assert parallel.snapshot() == serial.snapshot()
            assert parallel.computation_report() == serial.computation_report()
            assert parallel_events == serial_events
        assert parallel.execution_report()["spatial_node_tasks"] > 0


def test_parallel_execution_does_not_allocate_fields_for_uncoupled_carriers():
    from .test_node_work_emission import document

    raw = document()
    raw["emissions"] = []
    initial = parse_initial_state(raw)
    with Simulation(initial) as serial, Simulation(initial, node_workers=2) as parallel:
        for _ in range(4):
            serial.step()
            parallel.step()
            assert parallel.snapshot() == serial.snapshot()
            assert not serial._spatial.nodes
            assert not parallel._spatial.nodes
