"""Conservation guards reject complete ownership transitions before mutation."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_engine import DisturbanceEngine
from event_universe.core.disturbance_state import MAX_VALUE, Packet, pack, unpack
from event_universe.core.spatial_state import SpatialPacket
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.fields.record_operations import RecordOperations
from event_universe.initialization import parse_initial_state

from .support.disturbances import document, field, kind
from .test_local_field_rules import document as spatial_document
from .test_local_field_rules import invariant, local, operation, seed
from .test_node_conservation_configuration import large_initial_readouts
from .test_node_rule_contract import node_profile

ORIGIN = (0, 0, 0)
TARGET = (1, 0, 0)


def squared(expression):
    return operation("mul", expression, expression)


@pytest.mark.parametrize("incoming", [1, -1])
def test_carrier_receipt_checks_individual_nonlinear_owners_before_merge(incoming):
    raw = node_profile(
        document(
            [kind("parcel", mode="split", values={"quantity": 1})],
            [(TARGET, "parcel")],
            fields=[field("quantity")],
            capacity=2,
        )
    )
    raw["conservation_contract"]["quantities"][0]["carriers"][0]["value"] = squared(
        {"field": "quantity"}
    )
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    # Both records have the same genuine travel-port tag, as after a previous
    # receipt from the same neighbor; distinct channels never merge.
    resident = replace(world.nodes[TARGET].records[0], channel_code=2)
    world._nodes[TARGET].records = (resident, None)
    packet = Packet(1, ORIGIN, 0, replace(resident, values=(pack((incoming,)),)))
    world._links[ORIGIN] = (packet,) + (None,) * 11
    world.tick = 1
    node = world._nodes[TARGET]
    before, before_node = world.inventory_view(), replace(node)
    events.clear()
    # Each owner has squared amount one: two originals measure 2, while the
    # proposed sum measures 4 (parallel signs) or 0 (opposite signs).
    with pytest.raises(ValueError, match="carrier receipt.*declared stock"):
        world._deliver()
    assert world.inventory_view() == before
    assert node == before_node
    assert world.links[ORIGIN][0] is packet
    assert unpack(node.records[0].values[0]) == (1,)
    assert events == []


@pytest.mark.parametrize("incoming", [1, -1])
def test_spatial_receipt_checks_individual_nonlinear_packets_before_merge(incoming):
    raw = node_profile(spatial_document([field("quantity")], [seed("quantity", 1, TARGET)]))
    quantity = raw["conservation_contract"]["quantities"][0]
    quantity["carriers"][0]["value"] = squared({"field": "quantity"})
    quantity["spatial"] = squared(local("quantity"))
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    spatial = world._spatial
    populations = (pack((incoming,)),) + (pack((0,)),) * 7
    packet = SpatialPacket(1, ORIGIN, 0, (populations,))
    spatial.links[ORIGIN] = (packet,) + (None,) * 5
    node = spatial.nodes[TARGET]
    before, before_node = world.inventory_view(), replace(node)
    events.clear()
    with pytest.raises(ValueError, match="spatial receipt.*declared stock"):
        spatial.deliver(1)
    assert world.inventory_view() == before
    assert node == before_node
    assert spatial.links[ORIGIN][0] is packet
    assert unpack(node.states[0].populations[0]) == (1,)
    assert events == []


@pytest.mark.parametrize("component, quantity", [(1, "declared_momentum"), (4, "declared_charge")])
def test_joint_field_reaction_cannot_preserve_energy_while_violating_another_readout(
    component, quantity
):
    path = Path(__file__).resolve().parents[1] / "examples/node-vector/two-fields.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    rule = raw["spatial_interactions"][0]
    left = {"field": "first", "side": "left"}
    right = local("second")
    energy = operation(
        "add",
        {"op": "component", "args": [left], "index": 0},
        {"op": "component", "args": [right], "index": 0},
    )
    rule["invariants"] = [invariant("energy_only", energy)]
    delta = [0] * 8
    delta[component] = 1
    rule["assignments"][1]["expression"] = operation("add", left, delta)
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()
    assert world.tick == 1
    node = world._nodes[(2, 2, 2)]
    pending = node.pending
    assert pending.ready_tick == 2
    before = world.inventory_view()
    before_sources = world.source_totals()
    with pytest.raises(ValueError, match=f"carrier interaction commit.*{quantity}"):
        world.step()
    assert world.faulted
    assert world.inventory_view() == before
    assert node.pending is pending
    assert world.source_totals() == before_sources
    assert not any(event["event"] in ("cycle_committed", "spatial_coupled", "sent") for event in events)


def test_public_node_execution_cannot_drop_its_configured_conservation_contract():
    raw = node_profile(document([kind("parcel")], [(ORIGIN, "parcel")]))
    initial = parse_initial_state(raw)
    with pytest.raises(ValueError, match="conservation contract and balance guard"):
        Simulation(replace(initial, conservation_contract=None))


def test_injected_node_engine_requires_its_guard_even_with_valid_initialization():
    raw = node_profile(document([kind("parcel")], [(ORIGIN, "parcel")]))
    initial = parse_initial_state(raw)
    law = DisturbanceLaw(initial.fields, initial.disturbances, (), initial.operation_costs)
    policy = RecordOperations(initial.fields, initial.disturbances)
    with pytest.raises(ValueError, match="conservation contract and balance guard"):
        DisturbanceEngine(initial, law, record_policy=policy)


@pytest.mark.parametrize("owner", ["carrier", "spatial"])
@pytest.mark.parametrize("missing", ["contract", "guard"])
def test_direct_local_services_cannot_disable_the_mandatory_guard(owner, missing):
    raw = node_profile(spatial_document([field("quantity")]))
    world = Simulation(parse_initial_state(raw))
    services = world._services if owner == "carrier" else world._spatial._services
    with pytest.raises(ValueError, match="conservation contract and balance guard"):
        if missing == "contract":
            replace(services, initial=replace(services.initial, conservation_contract=None))
        else:
            replace(services, balance_guard=None)


def test_public_readouts_sum_many_local_owners_without_counting_pending_proposals():
    path = Path(__file__).resolve().parents[1] / "examples/node-vector/six-records.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    # Seven valid local groups contain 42 records globally, exceeding the local
    # record cap while keeping each individual Node within its configured size.
    raw["seeds"] = [
        {**seed, "position": [group % 5, group // 5, 0]} for group in range(7) for seed in raw["seeds"]
    ]
    world = Simulation(parse_initial_state(raw))
    original = world.conservation_report()["node_contract"]
    assert original["scope"] == "resident_and_in_flight"
    assert [quantity["value"] for quantity in original["quantities"]] == [
        (147,),
        (21, 0, 0),
        (0,),
        (0, 105, 0),
    ]
    world.step()
    assert all(node.pending is not None for node in world.nodes.values())
    before, cost = world.inventory_view(), world.computation_report()
    assert world.conservation_report()["node_contract"] == original
    assert world.conservation_report()["node_contract"] == original
    assert world.inventory_view() == before
    assert world.computation_report() == cost
    original["quantities"][0]["value"] = (-1,)
    assert world.conservation_report()["node_contract"]["quantities"][0]["value"] == (147,)


def test_carrier_receipt_checks_joint_local_accumulation_with_existing_field():
    world = Simulation(parse_initial_state(large_initial_readouts(7, spatial=True)))
    node, spatial = world._nodes[ORIGIN], world._spatial.nodes[ORIGIN]
    packet = Packet(1, (1, 0, 0), 1, node.records[0])
    before, mask = world.inventory_view(), node.arrival_mask
    with pytest.raises(OverflowError, match="64-bit"):
        node.receive((packet,), 1, world._services, spatial=spatial)
    assert world.inventory_view() == before
    assert node.arrival_mask == mask


def test_spatial_receipt_checks_joint_local_accumulation_with_existing_carriers():
    raw = large_initial_readouts(8, spatial=True)
    raw["spatial_seeds"][0]["populations"] = [0] * 8
    world = Simulation(parse_initial_state(raw))
    node = world._nodes[ORIGIN]
    spatial = world._spatial.nodes[ORIGIN]
    packet = SpatialPacket(1, (1, 0, 0), 1, ((pack((MAX_VALUE,)),) + (pack((0,)),) * 7,))
    before, mask = world.inventory_view(), spatial.arrival_mask
    with pytest.raises(OverflowError, match="64-bit"):
        spatial.receive((packet,), 1, world._spatial._services, carrier=node)
    assert world.inventory_view() == before
    assert spatial.arrival_mask == mask


def test_unmeasurable_external_state_has_an_explicit_report_error_without_partial_values():
    world = Simulation(parse_initial_state(large_initial_readouts(8)))
    node = world._nodes[ORIGIN]
    # Simulate an unsupported external mutation after valid preflight. A failed
    # diagnostic must still be serializable when the runner saves failure evidence.
    records = list(node.records)
    records[records.index(None)] = records[0]
    node.records = tuple(records)
    before = world.inventory_view()
    report = world.conservation_report()["node_contract"]
    assert "64-bit" in report["measurement_error"]
    assert all(quantity["value"] is None for quantity in report["quantities"])
    json.dumps(report)
    assert world.inventory_view() == before
