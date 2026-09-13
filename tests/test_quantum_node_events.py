"""Native Nodes share current event references; spacetime retains the immutable past."""

import json
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.initialization import parse_initial_state
from event_universe.integration.event_runtime import NativeEventResolver
from event_universe.quantum import DeferredQuantum, EventNetworkConfig

from .test_quantum_event_network import CX, POSITION, H, Z, probability

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/quantum/event_paths.json"


def configuration():
    return json.loads(EXAMPLE.read_text())


def resolver(world):
    assert isinstance(world._resolver, NativeEventResolver)
    return world._resolver


@pytest.mark.parametrize("phase", [False, True])
@pytest.mark.parametrize("recorded", [None, 0, 1])
@pytest.mark.parametrize("checkpoint", [False, True])
def test_four_node_event_paths_interference_and_local_record(phase, recorded, checkpoint):
    raw = configuration()
    if phase:
        raw["event_program"]["layers"].insert(
            2, {"tick": 3, "operations": [{"register_indices": [2], "matrix": [[1, 0], [0, -1]]}]}
        )
    world = Simulation(parse_initial_state(raw))
    space = resolver(world).space
    addresses = space.config.addresses
    cursors = tuple(world._nodes[a].event_cursors[0] for a in addresses)
    assert all(c is world.event_space.cursors_at(a)[0] for c, a in zip(cursors, addresses, strict=True))
    initial_views = world.nodes
    initial_heads = space.heads
    assert all(e.owner == "quantum" for e in world.event_space.events)
    assert len(world.event_space.events) == 4
    for tick in range(1, 5):
        world.step()
        assert space.heads == tuple(c.head for c in cursors)
        assert all(
            world.nodes[a].event_heads == ((c.stream_id, c.head),)
            for a, c in zip(addresses, cursors, strict=True)
        )
        assert all(not node_state_violations(n) for n in world._nodes.values())
        if tick == 2:
            assert space.host_evaluated_nodes == 0
            assert world.event_space.ancestors(cursors[2].head) != world.event_space.ancestors(
                cursors[3].head
            )
            assert world.event_space.event(cursors[2].head).addresses == (addresses[0], addresses[2])
            assert world.event_space.event(cursors[3].head).addresses == (addresses[1], addresses[3])
            if recorded is not None:
                decision = space.prepare(70, 2, POSITION)
                assert probability(decision) == Fraction(1, 2)
                space.commit(decision, sum(decision.weights[:recorded]))
            before = space.joint_density()
            old_events, old_heads, old_ticks = (
                world.event_space.events,
                space.heads,
                space.physical_ticks,
            )
            if checkpoint:
                replacement = space.checkpoint(2)
                assert space.node_count == 1
                assert space.heads == (replacement,) * 4
                assert space.physical_ticks == old_ticks
                assert space.joint_density() == before
                assert world.event_space.events[: len(old_events)] == old_events
                assert all(world.event_space.event(head) is old_events[head] for head in old_heads)
                assert world.event_space.event(replacement).parents == ()
                assert world.event_space.ancestors(replacement) == (replacement,)
            assert space.tick == world.tick == 2
    assert tuple(initial_views[a].event_heads[0][1] for a in addresses) == initial_heads
    before = space.tick, space.heads, space.physical_ticks, space.events, space.records, world.nodes
    probabilities = tuple(probability(space.query(q)) for q in range(4))
    assert probabilities == (
        (0, 0, Fraction(1, 2), Fraction(1, 2))
        if recorded is not None
        else (0, 0, int(phase), int(not phase))
    )
    assert sum(probabilities) == 1
    assert before == (
        space.tick,
        space.heads,
        space.physical_ticks,
        space.events,
        space.records,
        world.nodes,
    )
    assert len(space.records) == int(recorded is not None)
    assert not world.snapshot()["nodes"] and not world.snapshot()["transfers"]
    report = world.computation_report()
    assert report["model_operations_cost"] == report["event_ledger_cost"] == 0
    assert report["local_cycles_started"] == 0
    assert len(report["resolver"]["node_event_heads"]) == 4


@pytest.mark.parametrize("checkpoint", [False, True])
def test_checkpoint_does_not_restart_native_two_tick_link(checkpoint):
    raw = configuration()
    raw["link_ticks"] = 2
    raw["event_program"]["layers"] = [raw["event_program"]["layers"][0]]
    raw["event_program"]["layers"][0]["tick"] = 2
    world = Simulation(parse_initial_state(raw))
    space = resolver(world).space
    world.step()
    if checkpoint:
        space.checkpoint(0)
    assert space.physical_ticks == (0, 0, 0, 0)
    world.step()
    assert (probability(space.query(0)), probability(space.query(1))) == (Fraction(1, 2), Fraction(1, 2))
    assert space.physical_ticks == (2, 2, 0, 0)


def test_checkpoint_keeps_individual_times_and_still_rejects_early_link():
    raw = configuration()
    raw["link_ticks"] = 2
    layer = raw["event_program"]["layers"][0]
    layer["tick"] = 2
    raw["event_program"]["layers"] = [
        layer,
        {"tick": 3, "operations": [{"register_indices": [0], "matrix": [[1, 0], [0, -1]]}]},
        dict(layer, tick=4),
    ]
    world = Simulation(parse_initial_state(raw))
    space = resolver(world).space
    for _ in range(3):
        world.step()
    space.checkpoint(0)
    assert space.physical_ticks == (3, 2, 0, 0)
    before = space.events, space.heads, space.physical_ticks
    with pytest.raises(ValueError, match="precedes physical link time"):
        world.step()
    assert before == (space.events, space.heads, space.physical_ticks)


def test_independent_colocated_registers_join_as_a_joint_state():
    space = DeferredQuantum().bind_event_network(
        EventNetworkConfig(((0, 0, 0), (0, 0, 0)), register_names=("path", "record"))
    )
    a, b = space.event_space.cursors_at((0, 0, 0))
    space.step(((H, (0,)),))
    assert probability(space.query(0)) == Fraction(1, 2)
    assert probability(space.query(1)) == 0
    assert not set(space.event_space.ancestors(a.head)).intersection(space.event_space.ancestors(b.head))
    space.step(((CX, (0, 1)),))
    joint = space.heads[0]
    assert a.head == b.head == joint
    space.step(((Z, (0,)),))
    assert a.head != b.head
    assert space.event_space.event(a.head).parents == (joint,)
    assert b.head == joint
    density = space.joint_density()
    space.checkpoint(0)
    assert space.physical_ticks == (3, 2)
    assert space.joint_density() == density
    decision = space.prepare(80, 1, POSITION)
    assert probability(decision) == Fraction(1, 2)
    space.commit(decision, 0)
    assert probability(space.query(0)) == probability(space.query(1)) == 0


def test_long_event_spacetime_retains_fixed_cursor_storage_without_local_history():
    space = DeferredQuantum().bind_event_network(EventNetworkConfig(((0, 0, 0),)))
    cursor = space.event_space.cursors_at((0, 0, 0))[0]
    width = cursor.__sizeof__()
    for _ in range(2000):
        space.step(((Z, (0,)),))
    assert len(space.event_space.ancestors(cursor.head)) == 2001
    assert len(space.event_space.events) == 2001
    assert not hasattr(space, "history")
    assert all(not hasattr(event, "predecessors") for event in space.event_space.events)
    assert cursor.__sizeof__() == width
    assert not hasattr(cursor, "__dict__")
    assert space.host_evaluated_nodes == 0
    old_events = space.event_space.events
    replacement = space.checkpoint(0)
    assert space.node_count == 1 and len(space.event_space.events) == 2002
    assert space.event_space.events[: len(old_events)] == old_events
    assert space.event_space.ancestors(replacement) == (replacement,)
    assert cursor.__sizeof__() == width
