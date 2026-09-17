"""Active local transitions keep bounded work and state independent of remote growth."""

import sys
from collections import Counter
from dataclasses import fields, is_dataclass, replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS, OperationCosts, Packet, pack, unpack
from event_universe.core.node_services import NodeEvents
from event_universe.core.source_envelope_node import (
    OUTPUT_SLOTS,
    EnvelopeGate,
    EnvelopePacket,
    SourceEnvelopeNode,
)
from event_universe.core.source_envelope_state import EnvelopeAmplitude
from event_universe.core.spatial_state import SpatialPacket
from event_universe.core.topology import neighbor_address
from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.fields.source_envelope import local_output
from event_universe.initialization import parse_initial_state

from .support.disturbances import document, kind

SOURCE = (3, 3, 3)
MIDDLE = (2, 1, 1)
ROTATION = [[5, 0, 0, 0], [0, 3, -4, 0], [0, 4, 3, 0], [0, 0, 0, 5]]
INVERSE = [[5, 0, 0, 0], [0, 3, 4, 0], [0, -4, 3, 0], [0, 0, 0, 5]]
PACKAGE = str(Path(__file__).resolve().parents[1] / "src/event_universe").lower()
MIXER = tuple(tuple((value, 0) for value in row) for row in ROTATION)


class ForbiddenWorld:
    def __getattr__(self, name):
        raise AssertionError("local transition attempted to access a world index")

    def __getitem__(self, key):
        raise AssertionError("local transition attempted to read another Node")

    def __iter__(self):
        raise AssertionError("local transition attempted to scan the world")

    def __len__(self):
        raise AssertionError("local transition attempted to count global state")


def retained_slots(value):
    """Count the recursive payload, including pending states and output ownership."""
    if value is None or type(value) is int:
        return 1
    if type(value) is tuple:
        return 1 + sum(retained_slots(item) for item in value)
    if is_dataclass(value):
        return 1 + sum(retained_slots(getattr(value, field.name)) for field in fields(value))
    raise AssertionError(f"unexpected retained state type: {type(value).__name__}")


def counted_transition(action):
    counts = Counter()

    def trace(frame, event, arg):
        if event == "line" and frame.f_code.co_filename.lower().startswith(PACKAGE):
            counts[(frame.f_code.co_filename, frame.f_code.co_name)] += 1
        return trace

    previous = sys.gettrace()
    try:
        sys.settrace(trace)
        action()
    finally:
        sys.settrace(previous)
    assert counts
    return counts


def fixture(owner, port, remote_count):
    tick = 3 + 100 * remote_count
    weights = [int(index == port) for index in range(6)]
    raw = document(
        [kind("parcel", mode="move", weights=weights)],
        [(SOURCE, "parcel"), *[((20 + index, 20, 20), "parcel") for index in range(remote_count)]],
        capacity=2,
    )
    raw["shape"] = [256 if remote_count == 0 else 1_000_000] * 3
    if owner == "spatial":
        raw["spatial_fields"] = [{"field": "inventory", "baseline": 0, "transport": "outward"}]
    initial = parse_initial_state(raw)
    world = Simulation(initial)
    assert len(world.nodes) == remote_count + 1
    events = NodeEvents(None)
    origin = neighbor_address(SOURCE, port ^ 1, initial.shape, initial.boundary)

    if owner == "carrier":
        node = world._nodes[SOURCE]
        record = node.records[0]
        node.records = (None, None)
        services = replace(world._services, events=events)

        def action():
            node.receive((Packet(tick, origin, port, record),), tick, services)
            node.advance(tick, services)

        def result():
            packets = tuple(packet for packet in node.output.packets if packet is not None)
            assert node.records == (None, None)
            assert len(packets) == 1
            packet = packets[0]
            assert (packet.port, packet.arrival_tick, unpack(packet.record.values[0])) == (
                port,
                tick + 1,
                (1,),
            )
            return node.last_cost, retained_slots(node)

    elif owner == "spatial":
        node = world._spatial._at(SOURCE)
        services = replace(world._spatial._services, events=events)
        population = (pack((8,)),) * 8

        def action():
            node.receive((SpatialPacket(tick, origin, port, (population,)),), tick, services)
            node.advance(tick, None, services)

        def result():
            packets = tuple(packet for packet in node.output.packets if packet is not None)
            assert packets and all(packet.arrival_tick == tick + 1 for packet in packets)
            local = sum(unpack(value)[0] for state in node.states for value in state.populations)
            outgoing = sum(
                unpack(value)[0] for packet in packets for row in packet.fields for value in row
            )
            assert local + outgoing == 64
            return retained_slots(node)

    else:
        node = SourceEnvelopeNode(SOURCE, source_id=1, amplitude=EnvelopeAmplitude(1))

        def action():
            node.start_gate(
                tick, 0, EnvelopeGate(matrix_index=0, row=0, port=port ^ 1), 0, 1, 0, 4, events
            )
            node.receive(
                EnvelopePacket(tick + 1, origin, port, 1, EnvelopeAmplitude(), epoch=0),
                tick + 1,
                1,
                0,
                events,
                costs=initial.operation_costs,
            )
            assert node.complete(
                tick + 1, local_output, (MIXER,), initial.operation_costs, (port ^ 1,), 0, 1, events
            )

        def result():
            assert node.amplitude == EnvelopeAmplitude(3, 0, 5)
            assert node.pending_gate is None and node.incoming_gate is None
            assert len(node.output) == OUTPUT_SLOTS
            return retained_slots(node)

    # The same real services still run; only prohibited host read paths are poisoned.
    world._nodes = world._links = ForbiddenWorld()
    if world._spatial is not None:
        world._spatial._nodes = world._spatial._links = ForbiddenWorld()
    return node, action, result


@pytest.mark.parametrize("owner", ["carrier", "spatial", "envelope"])
@pytest.mark.parametrize("port", range(6))
def test_active_local_transition_is_independent_of_remote_world_size(owner, port):
    observations = []
    for remote_count in (0, 8, 128):
        node, action, result = fixture(owner, port, remote_count)
        work = counted_transition(action)
        assert not node_state_violations(node)
        observations.append((work, result()))
    assert observations[0] == observations[1] == observations[2]


# Source-envelope gate and terminal transitions on the Node alone.


def test_null_during_frozen_pair_preserves_the_complete_unitary_snapshot():
    costs = OperationCosts((1,) * len(OPERATIONS))
    events = NodeEvents(None)
    left = SourceEnvelopeNode(SOURCE, source_id=1, amplitude=EnvelopeAmplitude(3, 0, 5))
    right = SourceEnvelopeNode(MIDDLE, source_id=1, amplitude=EnvelopeAmplitude(4, 0, 5))
    matrices = tuple(
        tuple(tuple((value, 0) for value in row) for row in matrix) for matrix in (ROTATION, INVERSE)
    )
    for epoch in range(2):
        tick = epoch * 2
        left.start_gate(tick, epoch, EnvelopeGate(epoch, 0, 0), 0, 1, 1, 4, events)
        right.start_gate(tick, epoch, EnvelopeGate(epoch, 1, 1), 0, 1, 1, 4, events)
        from_left, from_right = left.output[0], right.output[1]
        right.receive(from_left, tick + 1, 1, 0, events, costs=costs)
        left.receive(from_right, tick + 1, 1, 0, events, costs=costs)
        left.clear_output(0, from_left)
        right.clear_output(1, from_right)
        if epoch == 0:
            left.null(tick + 1, None)
            assert left.amplitude == EnvelopeAmplitude()
            assert left.pending_gate.amplitude == EnvelopeAmplitude(3, 0, 5)
        left.complete(tick + 2, local_output, matrices, costs, (0,), 0, 1, events)
        right.complete(tick + 2, local_output, matrices, costs, (1,), 0, 1, events)
        if epoch == 0:
            assert (left.amplitude, right.amplitude) == (
                EnvelopeAmplitude(-7, 0, 25),
                EnvelopeAmplitude(24, 0, 25),
            )
    assert (left.amplitude, right.amplitude) == (EnvelopeAmplitude(3, 0, 5), EnvelopeAmplitude(4, 0, 5))


def test_duplicate_terminal_is_ignored_without_restarting_or_forwarding():
    costs = OperationCosts(
        tuple(7 if name == "receive" else 3 if name == "read" else 1 for name in OPERATIONS)
    )
    published: list[dict[str, object]] = []
    events = NodeEvents(published.append)
    node = SourceEnvelopeNode(SOURCE, source_id=7, amplitude=EnvelopeAmplitude(1))
    first = EnvelopePacket(1, MIDDLE, 1, 7, None)
    node.receive(first, 1, 1, 0, events, costs=costs)
    assert node.complete(1, local_output, (), costs, (0,), 0, 1, events)
    assert node.retired == 7
    outputs, generation, cause = node.output, node.generation, node.cause_id
    assert outputs[6] is not None
    duplicate = EnvelopePacket(2, MIDDLE, 1, 7, None)
    node.receive(duplicate, 2, 1, 5, events, costs=costs)
    assert published[-1]["event"] == "source-terminal-ignored"
    assert node.pending_stop is None
    assert node.output is outputs
    assert node.generation == generation and node.cause_id == cause
    assert node.amplitude == EnvelopeAmplitude() and node.retired == 7


def test_terminal_commits_before_later_amplitude_and_prevents_resurrection():
    costs = OperationCosts((1,) * len(OPERATIONS))
    published: list[dict[str, object]] = []
    events = NodeEvents(published.append)
    node = SourceEnvelopeNode(SOURCE, source_id=7, amplitude=EnvelopeAmplitude(3, 0, 5))
    node.start_gate(0, 0, EnvelopeGate(0, 0, 0), 2, 1, 1, 4, events)
    node.receive(EnvelopePacket(1, MIDDLE, 1, 7, None), 1, 1, 1, events, costs=costs)

    def forbidden(*args, **kwargs):
        raise AssertionError("a retired source must not evaluate a late amplitude")

    assert node.pending_stop.ready_tick == 2
    assert node.pending_gate.ready_tick == 4
    node.complete(2, forbidden, (), costs, (0,), 0, 1, events)
    assert node.retired == 7 and node.amplitude == EnvelopeAmplitude()
    outputs = node.output
    arriving = EnvelopePacket(3, MIDDLE, 1, 7, EnvelopeAmplitude(4, 0, 5), epoch=0)
    node.receive(arriving, 3, 1, 1, events, costs=costs)
    assert node.incoming_gate is arriving
    node.complete(4, forbidden, (), costs, (0,), 0, 1, events)
    assert node.retired == node.source_id == 7
    assert node.amplitude == EnvelopeAmplitude()
    assert node.pending_gate is None and node.incoming_gate is None
    assert node.output is outputs
    assert not [message for message in published if message["event"] == "source-gate-committed"]
