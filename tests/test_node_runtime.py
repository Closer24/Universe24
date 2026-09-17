"""Independent bounded Node execution, timing and transport ownership checks."""

from dataclasses import replace

import pytest

from event_universe.core.disturbance_node import DisturbanceNode
from event_universe.core.disturbance_state import Packet, pack, unpack
from event_universe.core.node_ports import PortBank
from event_universe.core.node_services import NodeAccounting, NodeEvents, NodeServices, WorkLedger
from event_universe.core.spatial_state import SpatialPacket
from event_universe.disturbance_api import Simulation
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.fields.record_operations import RecordOperations
from event_universe.initialization import parse_initial_state
from tests.support.disturbances import document, kind
from tests.test_local_field_rules import ORIGIN, field, invariant, local, operation, seed, value
from tests.test_local_field_rules import document as spatial_document
from tests.test_node_rule_contract import indexed_document, node_profile
from tests.test_spatial_interactions import exchange


def local_fixture(*, policy_type=RecordOperations, budget=10000, travel=1, mode="move"):
    initial = parse_initial_state(
        document(
            [kind("parcel", mode=mode, weights=[1, 0, 0, 0, 0, 0])],
            [((0, 0, 0), "parcel")],
            capacity=2,
            budget=budget,
            travel=travel,
        )
    )
    record = initial.seeds[0].record
    definitions = replace(initial, seeds=())
    law = DisturbanceLaw(initial.fields, initial.disturbances, (), initial.operation_costs)
    services = NodeServices(
        definitions,
        law,
        policy_type(initial.fields, initial.disturbances),
        NodeEvents(None),
        NodeAccounting(WorkLedger(), [[0]]),
        frozenset(),
        (0,) * 6,
    )
    node = DisturbanceNode(
        (None, None),
        (),
        position=(1, 0, 0),
        output=PortBank((None,) * 12),
        arrival_mask=(0,) * 6,
        delay_counts=(0,) * 6,
    )
    return node, services, record


@pytest.mark.parametrize("fault", ["neighbor", "time", "mutable"])
def test_isolated_node_rejects_invalid_delivery_without_changing_owners(fault):
    node, services, record = local_fixture()
    packet = Packet(3, (0, 0, 0), 0, record)
    if fault == "neighbor":
        packet = replace(packet, origin=(7, 0, 0))
    elif fault == "time":
        packet = replace(packet, arrival_tick=2)
    arrivals = [packet] if fault == "mutable" else (packet,)
    before = replace(node)
    with pytest.raises(ValueError):
        node.receive(arrivals, 3, services)
    assert node == before
    assert not any(node.output.packets)


def test_completed_zero_receipt_sets_its_port_mask_without_a_world():
    node, services, record = local_fixture()
    zero = replace(record, values=(pack((0,)),))
    node.receive((Packet(3, (0, 0, 0), 0, zero),), 3, services)
    assert node.records == (zero, None)
    assert node.arrival_mask == (0, 1, 0, 0, 0, 0)
    assert node.received_count == 1
    assert services.initial.seeds == ()


def test_node_retains_delay_counts_and_originals_until_the_legacy_commit():
    node, services, record = local_fixture(budget=1, travel=2)
    node.records = (record, None)
    node.advance(0, services)
    # Read, route, send and commit cost four: three extra link intervals.
    assert node.pending.ready_tick == 6
    assert node.pending.next_tick == 8
    assert node.delay_counts == (3,) * 6
    assert node.records[0] is record
    node.advance(5, services, window_closed=True)
    assert node.records[0] is record
    assert not any(node.output.packets)
    node.advance(6, services, window_closed=True)
    assert node.records == (None, None)
    assert node.output.packets[0].arrival_tick == 8
    assert node.delay_counts == (3,) * 6


def test_rejected_pending_slot_rewrite_keeps_the_entire_arrival_batch_uncommitted():
    class InvalidPolicy(RecordOperations):
        def receive(self, resident, arrivals, locked):
            return (arrivals[0], resident[1])

    node, services, record = local_fixture(policy_type=InvalidPolicy, budget=1, travel=2)
    node.records = (record, None)
    node.advance(0, services)
    incoming = replace(record, values=(pack((2,)),))
    before = replace(node)
    with pytest.raises(ValueError, match="pending local slot"):
        node.receive((Packet(3, (0, 0, 0), 0, incoming),), 3, services)
    assert node == before


@pytest.mark.parametrize(
    "fault, message",
    [
        ({"type_index": 3}, "index exceeds local capacity"),
        ({"values": ((0,),)}, "invalid positive integer component code"),
        ({"values": ([1],)}, "requires an immutable tuple"),
    ],
)
def test_isolated_node_rejects_a_malformed_delivered_record_at_its_boundary(fault, message):
    node, services, record = local_fixture()
    before = replace(node)
    with pytest.raises(ValueError, match=message):
        node.receive((Packet(3, (0, 0, 0), 0, replace(record, **fault)),), 3, services)
    assert node == before
    assert not any(node.output.packets)


def test_policy_output_that_is_not_a_delivered_record_is_still_validated():
    class SmugglingPolicy(RecordOperations):
        def receive(self, resident, arrivals, locked):
            return (replace(arrivals[0], type_index=3), resident[1])

    node, services, record = local_fixture(policy_type=SmugglingPolicy)
    before = replace(node)
    with pytest.raises(ValueError, match="index exceeds local capacity"):
        node.receive((Packet(3, (0, 0, 0), 0, record),), 3, services)
    assert node == before


def counted_record_validation(monkeypatch):
    """Count boundary validations by record identity across every importing module."""
    from event_universe.core import disturbance_engine, disturbance_node, node_boundary

    validated = []
    original = node_boundary.validate_record

    def counting(initial, record):
        validated.append(record)
        original(initial, record)

    for module in (node_boundary, disturbance_node, disturbance_engine):
        monkeypatch.setattr(module, "validate_record", counting)
    return validated


def test_each_delivered_record_is_validated_exactly_once_per_receipt(monkeypatch):
    validated = counted_record_validation(monkeypatch)
    node, services, record = local_fixture()
    second = replace(record, values=(pack((2,)),))
    packets = (Packet(3, (0, 0, 0), 0, record), Packet(3, (2, 0, 0), 1, second))
    node.receive(packets, 3, services)
    assert node.records == (record, second)
    assert [id(item) for item in validated] == [id(record), id(second)]
    # A merged record is a new object: it is validated once more than its inputs.
    validated.clear()
    split_node, split_services, split_record = local_fixture(mode="split")
    split_node.records = (split_record, None)
    incoming = replace(split_record, values=(pack((2,)),))
    split_node.receive((Packet(3, (0, 0, 0), 0, incoming),), 3, split_services)
    assert unpack(split_node.records[0].values[0]) == (3,)
    assert len(validated) == 2 and validated[0] is incoming and validated[1] is split_node.records[0]


def test_transport_validates_each_delivered_record_once_at_the_receiving_node(monkeypatch):
    validated = counted_record_validation(monkeypatch)
    world = Simulation(
        parse_initial_state(
            document(
                [kind("parcel", mode="move", weights=[1, 0, 0, 0, 0, 0])],
                [((0, 0, 0), "parcel")],
                capacity=2,
            )
        )
    )
    record = world.nodes[(0, 0, 0)].records[0]
    world._nodes[(0, 0, 0)].records = (None, None)
    packet = Packet(1, (0, 0, 0), 0, record)
    world._links[(0, 0, 0)] = (packet,) + (None,) * 11
    world.tick = 1
    validated.clear()
    world._deliver()
    assert world._nodes[(1, 0, 0)].records[0] is record
    assert world._links[(0, 0, 0)][0] is None
    assert len(validated) == 1 and validated[0] is record
    malformed = Packet(1, (1, 0, 0), 0, replace(record, type_index=3))
    world._links[(1, 0, 0)] = (malformed,) + (None,) * 11
    with pytest.raises(ValueError, match="index exceeds local capacity"):
        world._deliver()
    assert world._nodes[(2, 0, 0)].records == (None, None)
    assert world._links[(1, 0, 0)][0] is malformed


def test_spatial_zero_receipt_mask_is_consumed_by_one_local_input_window():
    world = Simulation(parse_initial_state(spatial_document([field("vector", 3)])))
    spatial = world._spatial
    node = spatial._at((1, 0, 0))
    zero = pack((0, 0, 0))
    packet = SpatialPacket(1, (0, 0, 0), 0, ((zero,) * 8,))
    notifications = node.receive((packet,), 1, spatial._services)
    assert node.arrival_mask == (0, 1, 0, 0, 0, 0)
    assert node.received_count == 1
    assert notifications[0]["received_fields"][1] == {"vector": (0, 0, 0)}
    node.advance(1, None, spatial._services)
    assert node.arrival_mask == (0,) * 6
    assert node.received_count == 0


def test_node_view_exposes_read_only_retained_delay_counts():
    initial = parse_initial_state(
        document(
            [kind("parcel", mode="move", weights=[1, 0, 0, 0, 0, 0])],
            [((0, 0, 0), "parcel")],
            budget=1,
            travel=2,
        )
    )
    world = Simulation(initial)
    world.step()
    view = world.snapshot()["nodes"][0]
    assert view["delay_counts"] == (3,) * 6
    view["delay_counts"] = (999,) * 6
    assert world.snapshot()["nodes"][0]["delay_counts"] == (3,) * 6


@pytest.mark.parametrize("price", [1, 19])
def test_explicit_carrier_interaction_completes_at_k_independent_of_cost(price):
    raw = indexed_document(count=2, roles=2, k=3)
    raw["normal_budget"] = 1
    raw["operation_costs"] = {name: price for name in raw["operation_costs"]}
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for _ in range(2):
        world.step()
        assert [unpack(r.values[0])[0] for r in world.nodes[(0, 0, 0)].records if r] == [1, 2]
    world.step()
    assert [unpack(r.values[0])[0] for r in world.nodes[(0, 0, 0)].records if r] == [2, 1]
    assert [e["tick"] for e in events if e["event"] == "cycle_committed"] == [3]
    assert world.snapshot()["nodes"][0]["delay_counts"] == (0,) * 6


def delayed_field_document():
    raw = node_profile(spatial_document([field("quantity", conserved=True)], [seed("quantity", 8)]))
    total = operation("add", local("quantity"), {"outgoing": "quantity", "port": 0})
    raw["field_rules"] = [
        {
            "name": "release",
            "k": 2,
            "assignments": [
                {"field": "quantity", "expression": 0},
                {"field": "quantity", "port": 0, "expression": local("quantity")},
            ],
            "invariants": [invariant("stock", total)],
        }
    ]
    return raw


def test_field_duration_ends_before_exactly_one_following_link_interval():
    events = []
    world = Simulation(parse_initial_state(delayed_field_document()), observer=events.append)
    world.step()
    assert value(world, "quantity") == (8,)
    assert not world.snapshot()["spatial_transfers"]
    world.step()
    assert value(world, "quantity") == (0,)
    assert world.snapshot()["spatial_transfers"][0]["arrival_tick"] == 3
    assert [e["tick"] for e in events if e["event"] == "spatial_cycle"] == [2]
    world.step()
    assert value(world, "quantity", (3, 2, 2)) == (8,)


def test_field_wait_keeps_new_arrivals_in_a_separate_input_window():
    world = Simulation(parse_initial_state(delayed_field_document()))
    world.step()
    engine = world._spatial
    node = engine.nodes[ORIGIN]
    population = (pack((5,)),) + (pack((0,)),) * 7
    node.receive((SpatialPacket(1, (1, 2, 2), 0, (population,)),), 1, engine._services)
    assert value(world, "quantity") == (13,)
    node.commit_ready(2, None, engine._services)
    assert value(world, "quantity") == (5,)
    assert node.states[0].delivered[0] == pack((5,))
    assert node.states[0].received_mask == 1
    assert node.received_count == 1
    assert node.arrival_mask == (0, 1, 0, 0, 0, 0)
    assert unpack(node.output.packets[0].fields[0][0]) == (8,)


def test_completed_zero_packet_can_activate_an_explicit_presence_rule():
    raw = delayed_field_document()
    raw["spatial_seeds"] = []
    raw["field_rules"][0]["when"] = {"received_present": "quantity", "port": 0}
    world = Simulation(parse_initial_state(raw))
    engine = world._spatial
    node = engine._at(ORIGIN)
    node.receive((SpatialPacket(1, (1, 2, 2), 0, ((pack((0,)),) * 8,)),), 1, engine._services)
    node.advance(1, None, engine._services)
    assert node.pending.ready_tick == 3
    assert node.pending.plan.interaction_ticks == 2
    assert node.states[0].received_mask == 0


def test_colocated_field_and_carrier_interactions_each_receive_a_turn():
    raw = node_profile(exchange())
    raw["spatial_interactions"][0]["k"] = 3
    raw["field_rules"] = [
        {
            "name": "retain",
            "k": 2,
            "assignments": [{"field": "quantity", "expression": local("quantity")}],
            "invariants": [invariant("stock", local("quantity"))],
        }
    ]
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for _ in range(10):
        world.step()
    assert [e["tick"] for e in events if e["event"] == "spatial_cycle"] == [2, 7]
    assert [e["tick"] for e in events if e["event"] == "cycle_committed"] == [5, 10]


def test_one_step_interaction_releases_only_at_completion_then_crosses_one_link():
    raw = delayed_field_document()
    raw["field_rules"][0]["k"] = 1
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert world.tick == 1
    assert value(world, "quantity") == (0,)
    assert value(world, "quantity", (3, 2, 2)) == (0,)
    assert world.snapshot()["spatial_transfers"][0]["arrival_tick"] == 2
    world.step()
    assert value(world, "quantity", (3, 2, 2)) == (8,)


def test_carrier_only_presence_rule_consumes_one_zero_receipt_once():
    raw = node_profile(exchange())
    raw["spatial_seeds"] = []
    raw["spatial_interactions"][0].update(k=2, when={"received_present": "quantity", "port": 0})
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    engine = world._spatial
    node = engine._at(ORIGIN)
    node.receive((SpatialPacket(0, (1, 2, 2), 0, ((pack((0,)),) * 8,)),), 0, engine._services)
    world.step()
    assert world.nodes[ORIGIN].pending.ready_tick == 2
    assert value(world, "quantity") == (0,)
    world.step()
    assert value(world, "quantity") == (5,)
    assert node.sample_received_masks == (0,)
    for _ in range(5):
        world.step()
    delayed = [e for e in events if e["event"] == "cycle_started" and e["ready_tick"] > e["tick"]]
    assert len(delayed) == 1
    assert value(world, "quantity") == (5,)
