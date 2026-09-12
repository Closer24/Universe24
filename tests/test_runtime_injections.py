"""Configured runtime injections add generic disturbances as explicit source events."""

import json
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_RUNTIME_INJECTIONS, unpack
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def document() -> dict[str, object]:
    return json.loads((EXAMPLES / "basic.json").read_text(encoding="utf-8"))


def injection(
    *,
    tick: int = 1,
    position: list[int] | None = None,
    type_name: str = "carrier",
    values: dict[str, object] | None = None,
) -> dict[str, object]:
    result: dict[str, object] = {
        "tick": tick,
        "position": [8, 8, 8] if position is None else position,
        "type": type_name,
    }
    if values is not None:
        result["values"] = values
    return result


def records_at(world: Simulation, position: tuple[int, int, int]):
    cell = world.cells.get(position)
    return () if cell is None else tuple(record for record in cell.records if record is not None)


def test_runtime_injection_reuses_seed_payload_validation_and_type_defaults() -> None:
    raw = document()
    raw["runtime_injections"] = [
        injection(values={"mass": 5, "charge": 3, "velocity": [0, -2, 1]})
    ]
    initial = parse_initial_state(raw)
    scheduled = initial.runtime_injections[0]
    assert scheduled.tick == 1
    assert scheduled.position == (8, 8, 8)
    assert initial.disturbances[scheduled.record.type_index].name == "carrier"
    assert tuple(unpack(value) for value in scheduled.record.values) == (
        (5,),
        (3,),
        (0, -2, 1),
        (0,),
        (0,),
    )


def test_runtime_injection_appears_exactly_at_tick_and_is_accounted_as_source() -> None:
    raw = document()
    raw["runtime_injections"] = [
        injection(values={"mass": 5, "charge": 3, "velocity": [0, 0, 0]})
    ]
    events: list[dict[str, object]] = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    target = (8, 8, 8)
    initial_mass = world.totals()["mass"]
    initial_charge = world.totals()["charge"]
    assert records_at(world, target) == ()

    world.step()

    placed = records_at(world, target)
    assert len(placed) == 1
    assert world.record_values(placed[0]) == {
        "mass": (5,),
        "charge": (3,),
        "velocity": (0, 0, 0),
    }
    assert world.totals()["mass"] == tuple(value + 5 for value in initial_mass)
    assert world.totals()["charge"] == tuple(value + 3 for value in initial_charge)
    assert world.source_totals()["mass"] == (5,)
    assert world.source_totals()["charge"] == (3,)
    injected = [event for event in events if event["event"] == "runtime_injected"]
    assert injected == [
        {
            "event": "runtime_injected",
            "tick": 1,
            "position": target,
            "disturbance": "carrier",
            "values": {"mass": (5,), "charge": (3,), "velocity": (0, 0, 0)},
        }
    ]
    assert world.computation_report()["runtime_injections_applied"] == 1


def test_runtime_injection_batch_fails_before_mutation_when_capacity_is_full() -> None:
    raw = document()
    raw["slots_per_cell"] = 1
    raw["seeds"] = [
        {
            "position": [8, 8, 8],
            "type": "carrier",
            "values": {"mass": 2, "charge": 0, "velocity": [0, 0, 0]},
        }
    ]
    raw["runtime_injections"] = [injection(values={"mass": 7, "charge": 0})]
    world = Simulation(parse_initial_state(raw))
    before = world.snapshot()

    with pytest.raises(ValueError, match="runtime injection capacity exceeded"):
        world.step()

    assert world.faulted
    assert world.source_totals()["mass"] == (0,)
    assert world.computation_report()["runtime_injections_applied"] == 0
    after_records = records_at(world, (8, 8, 8))
    assert len(after_records) == 1
    assert world.record_values(after_records[0])["mass"] == (2,)
    assert before["cells"][0]["disturbances"][0]["values"]["mass"] == (2,)


def test_runtime_injection_cannot_change_a_cell_with_a_frozen_pending_cycle() -> None:
    raw = document()
    raw["slots_per_cell"] = 2
    raw["normal_budget"] = 1
    raw["seeds"] = [
        {
            "position": [8, 8, 8],
            "type": "local_work",
            "values": {"computation": 20},
        }
    ]
    raw["runtime_injections"] = [injection(type_name="local_work", values={"computation": 0})]
    world = Simulation(parse_initial_state(raw))

    with pytest.raises(ValueError, match="pending local cycle"):
        world.step()

    assert world.source_totals() == {"mass": (0,), "charge": (0,), "signal": (0,)}
    assert world.computation_report()["runtime_injections_applied"] == 0


@pytest.mark.parametrize(
    ("entry", "message"),
    [
        (injection(tick=0), "tick"),
        (injection(position=[17, 0, 0]), "within shape"),
        (injection(type_name="unknown"), "unknown name"),
        (injection(values={"signal": 1}), "unknown keys"),
    ],
)
def test_invalid_runtime_injection_is_rejected_before_running(
    entry: dict[str, object], message: str
) -> None:
    raw = document()
    raw["runtime_injections"] = [entry]
    with pytest.raises(ValueError, match=message):
        parse_initial_state(raw)


def test_runtime_injection_configuration_has_fixed_global_and_local_capacity() -> None:
    raw = document()
    raw["seeds"] = []
    raw["slots_per_cell"] = 1
    raw["runtime_injections"] = [injection(), injection()]
    with pytest.raises(ValueError, match="same tick and position exceed slots_per_cell"):
        parse_initial_state(raw)

    raw["runtime_injections"] = [
        injection(tick=index + 1, position=[index % 17, 0, 0], type_name="local_work")
        for index in range(MAX_RUNTIME_INJECTIONS + 1)
    ]
    with pytest.raises(ValueError, match="runtime_injections"):
        parse_initial_state(raw)


@pytest.mark.visualization
def test_runner_records_runtime_injection_in_visualized_tick(tmp_path: Path) -> None:
    raw = document()
    raw["ticks"] = 2
    raw["runtime_injections"] = [
        injection(values={"mass": 5, "charge": 3, "velocity": [0, 0, 0]})
    ]
    source = tmp_path / "input.json"
    source.write_text(json.dumps(raw), encoding="utf-8")
    output = tmp_path / "run"

    path = run_initialization(source, output, visualize=True)

    assert path == output / "run.html"
    assert path.is_file()
    events = [json.loads(line) for line in (output / "events.jsonl").read_text().splitlines()]
    assert [(event["event"], event["tick"]) for event in events if event["event"] == "runtime_injected"] == [
        ("runtime_injected", 1)
    ]
    metadata = json.loads((output / "run.json").read_text())
    assert metadata["runtime_injections_scheduled"] == 1
    assert metadata["computation"]["runtime_injections_applied"] == 1
    assert metadata["accounting_balanced_at_every_completed_tick"]
    assert '"tick": 1' in path.read_text(encoding="utf-8")
