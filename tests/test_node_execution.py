"""Local execution boundaries, clock-only completion and transfer failures."""

from dataclasses import FrozenInstanceError, fields, replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import Packet
from event_universe.core.event_space import CausalEventSpace
from event_universe.core.node_services import NodeEvents
from event_universe.core.spatial_state import SpatialPacket
from event_universe.core.topology import inverse_port, neighbor_address
from event_universe.initialization import parse_initial_state

from .test_disturbance_engine import document, kind
from .test_local_field_rules import ORIGIN, field, seed
from .test_local_field_rules import document as spatial_document
from .test_node_boundary import world
from .test_topology_invariants import configure


@pytest.mark.parametrize("topology,degree", [("line", 2), (None, 6), ("cubic", 26)])
def test_integer_delay_vector_and_completion_without_an_arrival(topology, degree):
    raw = document(
        [kind("parcel", mode="move", weights=[1, 0, 0, 0, 0, 0])],
        [((2, 2, 2), "parcel")],
        budget=10,
        travel=3,
        capacity=1,
    )
    if topology == "cubic":
        raw = configure(raw, topology)
        raw["normal_budget"] = 10
    elif topology == "line":
        raw["topology"] = {"model_id": "configured-ports-v1", "offsets": [[1, 0, 0], [-1, 0, 0]]}
    if topology:
        raw["disturbance_types"][0]["transport"]["weights"] = [1] + [0] * (degree - 1)
    simulation = Simulation(parse_initial_state(raw))
    node = simulation._nodes[(2, 2, 2)]
    planner = simulation._services.planner

    def priced(records, residuals, received):
        return replace(planner(records, residuals, received), cost=21)

    services = replace(simulation._services, planner=priced)
    node.advance(0, services)
    assert node.h == (6,) * degree
    assert all(type(delay) is int for delay in node.h)
    assert node.pending.ready_tick == 6 and node.pending.next_tick == 9
    for tick in range(1, 6):
        node.advance(tick, services, window_closed=True)
        assert node.pending is not None
        assert not any(node.output.packets)
    node.advance(6, services, window_closed=True)
    assert node.pending is None and node.available_tick == 9
    assert [packet.arrival_tick for packet in node.output.packets if packet] == [9]
    assert simulation.computation_report()["local_cycles_started"] == 1
    view = simulation.node_view(node.position).carrier
    assert view.h is node.h
    with pytest.raises(FrozenInstanceError):
        view.h = ()


def test_local_execution_has_no_world_index_or_definition_seed_access():
    simulation = world()
    node = simulation._nodes[(2, 2, 2)]
    services = simulation._services
    assert not services.initial.seeds and not services.initial.spatial_seeds
    assert not hasattr(node, "__dict__")
    for owner in (node, node.output, services, services.accounting, services.events):
        for name in ("nodes", "_nodes", "links", "_links", "graph", "event_space", "sources", "ledger"):
            assert not hasattr(owner, name)
    assert {member.name for member in fields(node)} >= {"records", "output", "h"}
    # Lose the host maps altogether: the actual local owner can still execute.
    simulation._nodes = {}
    simulation._links = {}
    node.advance(0, services)
    assert node.records == (None, None)
    assert len([packet for packet in node.output.packets if packet]) == 1


@pytest.mark.parametrize("lane", ["carrier", "spatial"])
def test_foreign_local_component_is_rejected_before_any_rule_runs(lane):
    simulation = Simulation(parse_initial_state(spatial_document([field("stock")], [seed("stock", 7)])))
    carrier = simulation._at(ORIGIN)
    foreign = simulation._spatial._at((4, 4, 4))
    before = simulation.snapshot()
    with pytest.raises(ValueError, match="same node"):
        if lane == "carrier":
            carrier.advance(
                0, simulation._services, spatial=foreign, spatial_services=simulation._spatial.services
            )
        else:
            foreign.advance(0, carrier, simulation._spatial.services)
    assert simulation.snapshot() == before


@pytest.mark.parametrize("defect", ["destination", "early", "mutable", "capacity"])
def test_misdispatched_carrier_batch_does_not_change_receiver(defect):
    simulation = world()
    record = simulation.initial.seeds[0].record
    receiver = simulation._at((3, 2, 2))
    packet = Packet(1, (2, 2, 2), 0, record)
    packets = (replace(packet, origin=(8, 2, 2)),) if defect == "destination" else (packet,)
    if defect == "mutable":
        packets = list(packets)
    elif defect == "capacity":
        packets *= len(receiver.output.packets) * simulation.initial.topology.degree + 1
    before = simulation.node_view(receiver.position)
    with pytest.raises(ValueError):
        receiver.receive(packets, 0 if defect == "early" else 1, simulation._services)
    assert simulation.node_view(receiver.position) == before


def test_causal_record_failure_after_receipt_cannot_duplicate_inventory():
    simulation = world()
    space = CausalEventSpace(shape=simulation.initial.shape)
    simulation._services = replace(simulation._services, events=NodeEvents(space, None))
    source = simulation._nodes[(2, 2, 2)]
    source.advance(0, simulation._services)
    packets = list(source.output.packets)
    packets[0] = replace(packets[0], cause_id=999)
    source.output.publish(tuple(packets))
    simulation.tick = 1
    with pytest.raises(ValueError, match="unknown causal"):
        simulation._deliver()
    assert simulation.totals() == {"inventory": (1,)}
    assert not any(source.output.packets)
    assert simulation.node_view((3, 2, 2)).carrier.records[0] is not None


@pytest.mark.parametrize("bad_tick", [-1, True, 0.5])
def test_clock_notice_requires_nonnegative_bounded_integer(bad_tick):
    simulation = world()
    before = simulation.snapshot()
    with pytest.raises(ValueError):
        simulation._nodes[(2, 2, 2)].advance(bad_tick, simulation._services)
    assert simulation.snapshot() == before


@pytest.mark.parametrize("defect", ["destination", "early", "boolean_tick", "boolean_arrival"])
def test_misdispatched_spatial_batch_does_not_change_receiver(defect):
    simulation = Simulation(parse_initial_state(spatial_document([field("stock")], [seed("stock", 7)])))
    spatial = simulation._spatial
    sender = spatial.nodes[ORIGIN]
    bundle = tuple(state.populations for state in sender.states)
    receiver = spatial._at((3, 2, 2))
    packet = SpatialPacket(1, ORIGIN, 0, bundle)
    if defect == "destination":
        packet = replace(packet, origin=(0, 0, 0))
    elif defect == "boolean_arrival":
        packet = replace(packet, arrival_tick=True)
    before = simulation.node_view(receiver.position)
    tick = 0 if defect == "early" else True if defect == "boolean_tick" else 1
    with pytest.raises(ValueError):
        receiver.receive((packet,), tick, spatial.services)
    assert simulation.node_view(receiver.position) == before


def test_custom_departure_capacity_can_merge_all_neighbor_banks():
    raw = document([kind("parcel", mode="split")], [((2, 2, 2), "parcel")], capacity=1)
    simulation = Simulation(parse_initial_state(raw))
    receiver = simulation._at((3, 3, 3))
    initial = simulation.initial
    record = initial.seeds[0].record
    packets = tuple(
        Packet(
            1,
            neighbor_address(receiver.position, inverse_port(port), initial.shape, initial.boundary),
            port,
            record,
        )
        for port in range(6)
        for _ in range(6)
    )
    receiver.receive(packets, 1, simulation._services)
    assert simulation.record_values(receiver.records[0])["inventory"] == (36,)
    assert receiver.received_count == 36
