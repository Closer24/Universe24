"""Active local transitions keep bounded work and state independent of remote growth."""

import sys
from collections import Counter
from dataclasses import fields, is_dataclass, replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import Packet, pack, unpack
from event_universe.core.event_space import CausalEventSpace
from event_universe.core.node_services import NodeEvents
from event_universe.core.source_envelope_node import EnvelopeGate, EnvelopePacket, SourceEnvelopeNode
from event_universe.core.source_envelope_state import EnvelopeAmplitude
from event_universe.core.spatial_state import SpatialPacket
from event_universe.core.topology import neighbor_address
from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.fields.source_envelope import local_output
from event_universe.initialization import parse_initial_state

from .support.contact import ROTATION
from .support.disturbances import document, kind

SOURCE = (3, 3, 3)
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
    ledger = CausalEventSpace(remote_count + 32)
    for index in range(remote_count):
        ledger.append(tick=0, addresses=((20 + index, 20, 20),), owner="state", kind="source")
    events = NodeEvents(ledger, None)
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
            return node.last_cost, retained_slots(node), len(ledger.events) - remote_count

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
            return retained_slots(node), len(ledger.events) - remote_count

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
            assert len(node.output) == 12
            return retained_slots(node), len(ledger.events) - remote_count

    # The same real services still run; only prohibited host read paths are poisoned.
    world._nodes = world._links = ForbiddenWorld()
    if world._spatial is not None:
        world._spatial._nodes = world._spatial._links = ForbiddenWorld()
    return node, action, result


@pytest.mark.parametrize("owner", ["carrier", "spatial", "envelope"])
@pytest.mark.parametrize("port", range(6))
def test_active_local_transition_is_independent_of_remote_world_and_event_growth(owner, port):
    observations = []
    for remote_count in (0, 8, 128):
        node, action, result = fixture(owner, port, remote_count)
        work = counted_transition(action)
        assert not node_state_violations(node)
        observations.append((work, result()))
    assert observations[0] == observations[1] == observations[2]
