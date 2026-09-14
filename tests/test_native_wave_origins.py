"""Configured local origin contacts run through the primary headless Simulation."""

import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.initialization import parse_initial_state
from event_universe.integration.event_runtime import NativeEventResolver
from event_universe.runner import run_initialization

from .support.quantum import probability

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/quantum/wave_origins.json"


def configuration():
    return json.loads(EXAMPLE.read_text())


@pytest.mark.parametrize("terminal", [False, True])
@pytest.mark.parametrize("ticket", [0, 1])
def test_native_overlap_lifecycle_and_conditional_continuation(terminal, ticket):
    raw = configuration()
    program = raw["event_program"]
    program["tickets"] = [ticket]
    if not terminal:
        program["wave_interactions"][0].update(
            terminal_outcomes=[],
            terminal_origins=[],
            instrument=[[[1, 0], [0, 0]], [[0, 0], [0, 1]]],
        )
    world = Simulation(parse_initial_state(raw))
    resolver = world._resolver
    assert isinstance(resolver, NativeEventResolver)
    network = resolver.space
    waves = network.waves
    signal = waves.names["signal"]
    source = world.event_space.event(signal)
    initial = world.nodes
    assert all(world._nodes[a].event_references is bank for a, bank in waves.banks.items())
    world.step()
    assert waves.banks[(1, 0, 0)].origins == (signal,)
    assert not network.records
    assert probability(network.query(0)) == probability(network.query(1)) == Fraction(1, 2)
    world.step()
    record = network.records[0]
    assert record.outcome == ticket
    assert record.event_id in world.event_space.ancestors(record.event_id)
    assert signal in world.event_space.ancestors(record.event_id)
    closed = terminal and ticket == 1
    assert world.event_space.resolution(signal) == (record.event_id if closed else None)
    assert all(signal in bank.origins for bank in waves.banks.values())
    # Frozen NodeViews do not turn into a remotely mutable status channel.
    assert initial[(1, 0, 0)].event_origins == ()
    assert world.event_space.event(signal) is source
    world.step()
    assert all((signal not in bank.origins) == closed for bank in waves.banks.values())
    before = network.joint_density(), network.heads, network.physical_ticks
    world.step()
    if closed:
        assert before == (network.joint_density(), network.heads, network.physical_ticks)
        assert len(network.records) == 1
    else:
        assert len(network.records) == 2
    world.step()
    expected = (0, 0, 0) if closed else (0, 1, 0) if ticket else (1, 0, 0)
    assert tuple(probability(network.query(q)) for q in range(3)) == expected
    assert sum(expected) == (0 if closed else 1)
    assert resolver.draws == 1
    assert all(not node_state_violations(node) for node in world._nodes.values())
    report = world.computation_report()
    assert report["resolver"]["model"] == "local-quantum-events-v3"
    assert report["event_ledger_cost"] == report["resolver"]["wave_control_cost"] > 0
    assert report["model_operations_cost"] == report["event_ledger_cost"]
    assert report["carrier_model_operations_cost"] == 0
    assert report["resolver"]["node_wave_origins"]


def test_unmatched_wave_rule_reserves_only_the_two_actual_checks():
    raw = configuration()
    raw["shape"] = [2, 1, 1]
    program = raw["event_program"]
    program.update(capacity=6, addresses=[[0, 0, 0], [1, 0, 0]], layers=[])
    program["waves"][1]["register_index"] = 1
    program["wave_interactions"][0].update(address=[1, 0, 0], register_index=1)
    world = Simulation(parse_initial_state(raw))
    assert world.event_space.next_id == 4
    world.step()
    assert world.event_space.next_id == 6
    assert world.event_space.model_cost == 2
    assert not world._resolver.space.records


def test_inactive_world_advances_at_capacity_without_dummy_requests():
    raw = configuration()
    world = Simulation(parse_initial_state(raw))
    resolver = world._resolver
    for _ in range(3):
        world.step()
    # End the remaining probe through a local declared instrument, then allow
    # exactly its two resident checks before reaching the finite audit bound.
    waves = resolver.space.waves
    origin = waves.names["probe"]
    from .support.quantum import POSITION

    resolver.space.interact(
        500, 2, POSITION, origins=(origin,), terminal_origins=(origin,), terminal_outcomes=(0,)
    )
    # Two resident reads, one inert gate and one invalidated null certificate.
    world.event_space.capacity = world.event_space.next_id + 4
    world.step()
    at_capacity = world.event_space.next_id
    assert at_capacity == world.event_space.capacity
    assert all(not bank.origins for bank in waves.banks.values())
    world.step()
    assert world.event_space.next_id == at_capacity


@pytest.mark.parametrize(
    "case",
    [
        "untagged_gate",
        "unknown_gate_origin",
        "too_many_sources",
        "duplicate_origins",
        "unknown_origin",
        "bad_terminal",
        "foreign_terminal",
        "legacy_binding",
    ],
)
def test_invalid_wave_configuration_rejects_before_world_construction(case):
    raw = configuration()
    program = raw["event_program"]
    contact = program["wave_interactions"][0]
    if case == "untagged_gate":
        del program["layers"][0]["operations"][0]["origins"]
    elif case == "unknown_gate_origin":
        program["layers"][0]["operations"][0]["origins"] = ["missing"]
    elif case == "too_many_sources":
        program["waves"] = [{"name": f"wave_{i}", "register_index": 0} for i in range(7)]
    elif case == "duplicate_origins":
        contact["origins"] = ["signal", "signal"]
    elif case == "unknown_origin":
        contact["origins"] = ["signal", "missing"]
    elif case == "bad_terminal":
        contact["terminal_outcomes"] = [2]
    elif case == "foreign_terminal":
        contact["terminal_origins"] = ["missing"]
    else:
        program["bindings"] = [{}]
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_origin_names_are_data_and_recorded_run_is_headless(tmp_path):
    raw = configuration()
    renamed = deepcopy(raw)
    program = renamed["event_program"]
    labels = {"signal": "first_event", "probe": "second_event"}
    for wave in program["waves"]:
        wave["name"] = labels[wave["name"]]
    for layer in program["layers"]:
        for op in layer["operations"]:
            op["origins"] = [labels[n] for n in op["origins"]]
    for contact in program["wave_interactions"]:
        for member in ("origins", "terminal_origins"):
            contact[member] = [labels[n] for n in contact[member]]
    worlds = [Simulation(parse_initial_state(data)) for data in (raw, renamed)]
    for world in worlds:
        for _ in range(raw["ticks"]):
            world.step()
    assert worlds[0].nodes == worlds[1].nodes
    assert worlds[0].event_space.events == worlds[1].event_space.events
    output = tmp_path / "output"
    run_initialization(EXAMPLE, output)
    metadata = json.loads((output / "run.json").read_text())
    assert metadata["display"] == "none"
    assert not any(p.suffix in (".html", ".gif", ".png") for p in output.iterdir())
