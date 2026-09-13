"""One bounded node clock freezes field and carrier work until a shared commit."""

import json
from copy import deepcopy
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import pack, unpack
from event_universe.core.spatial_state import SpatialPacket
from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_finite_spatial_engine import all_records, finite_document
from .test_spatial_causal_events import single_packet, traced
from .test_spatial_engine import ORIGIN as FIELD_ORIGIN
from .test_spatial_engine import document
from .test_spatial_interactions import ORIGIN, carrier, exchange


def delayed(raw):
    raw = deepcopy(raw)
    raw["spatial_computation_delay"] = True
    return raw


@pytest.mark.parametrize("value", [1, 0, "true", None, {}])
def test_delay_switch_requires_a_boolean(value):
    raw = single_packet()
    raw["spatial_computation_delay"] = value
    with pytest.raises(ValueError, match="spatial_computation_delay"):
        parse_initial_state(raw)


@pytest.mark.parametrize("cost,commit,arrival", [(68, 0, 2), (69, 2, 4), (169, 4, 6)])
def test_field_only_budget_boundaries_preserve_originals_until_commit(cost, commit, arrival):
    raw = delayed(single_packet())
    raw["normal_budget"] = 100
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    planner = world._spatial.planner
    assert world._spatial._services.node_merge_cost == 32
    world._spatial._services = replace(
        world._spatial._services, planner=lambda *args: replace(planner(*args), cost=cost)
    )
    for tick in range(1, arrival + 1):
        world.step()
        assert world.totals()["radiation"] == (8,)
        if tick < commit:
            assert world.spatial_values((2, 0, 0))["radiation"]["value"] == (8,)
            assert not world.snapshot()["spatial_transfers"]
        assert not [e for e in events if e["event"] == "spatial_received" and e["tick"] < arrival]
    sends = [e for e in events if e["event"] == "spatial_sent"]
    receives = [e for e in events if e["event"] == "spatial_received"]
    assert [(e["tick"], e["arrival_tick"]) for e in sends] == [(commit, arrival)]
    assert receives[0]["tick"] == arrival


def test_omitted_and_disabled_switch_have_identical_legacy_states_and_events():
    raw = traced(single_packet())
    plain_events, disabled_events = [], []
    plain = Simulation(parse_initial_state(raw), observer=plain_events.append)
    raw["spatial_computation_delay"] = False
    disabled = Simulation(parse_initial_state(raw), observer=disabled_events.append)
    for _ in range(12):
        plain.step()
        disabled.step()
        assert plain.snapshot() == disabled.snapshot()
        assert plain.computation_report() == disabled.computation_report()
    assert plain_events == disabled_events


@pytest.mark.parametrize("moving", [False, True])
def test_shared_budget_counts_field_and_carrier_work_once_and_defers_emission(moving):
    raw = delayed(finite_document(source=True, moving=moving, travel=2))
    raw["normal_budget"] = 40
    raw["disturbance_types"][0]["defaults"]["strength"] = 2
    world = Simulation(parse_initial_state(traced(raw)))
    field_planner, carrier_planner = world._spatial.planner, world._planner
    world._spatial._services = replace(
        world._spatial._services, planner=lambda *args: replace(field_planner(*args), cost=20)
    )
    world._services = replace(
        world._services, planner=lambda *args: replace(carrier_planner(*args), cost=20)
    )
    initial_record = all_records(world)[0]
    world.step()
    pending = next(node.pending for node in world.nodes.values() if node.pending is not None)
    assert (pending.plan.cost, pending.ready_tick, pending.next_tick) == (72, 2, 4)
    assert all_records(world) == [initial_record]
    assert world.source_totals()["radiation"] == (0,)
    assert world.totals()["radiation"] == (0,)
    assert world.computation_report()["model_operations_cost"] == 72
    assert world.computation_report()["event_ledger_cost"] == 72
    world.step()
    assert world.source_totals()["radiation"] == (2,)
    assert unpack(all_records(world)[0].emission_remaining[0]) == (3,)
    assert world.computation_report()["model_operations_cost"] == 72
    assert all(p.arrival_tick == 4 for links in world._spatial.links.values() for p in links if p)
    assert bool(world.snapshot()["transfers"]) == moving
    assert all(row["balanced"] for row in world.spatial_accounting().values())


def test_arrival_during_joint_wait_is_preserved_without_changing_the_frozen_sample():
    raw = delayed(exchange(delayed=True, incoming=True))
    raw["normal_budget"] = 40
    raw["spatial_interactions"][0]["invariants"] = raw["spatial_interactions"][0]["invariants"][:1]
    world = Simulation(parse_initial_state(traced(raw)))
    field_planner = world._spatial.planner
    world._spatial._services = replace(
        world._spatial._services, planner=lambda *args: replace(field_planner(*args), cost=1)
    )
    world.step()
    pending = world.nodes[ORIGIN].pending
    assert pending is not None and pending.ready_tick > 1
    assert world._spatial.nodes[ORIGIN].incoming
    assert carrier(world) == (5,)
    assert world.spatial_values(ORIGIN)["quantity"]["value"] == (2,)
    assert world.totals()["quantity"] == (8,)
    events = world.event_space
    arrival = next(e for e in events.events if e.kind == "spatial_received" and e.addresses == (ORIGIN,))
    assert arrival.id not in events.ancestors(pending.cause_id)
    while world.tick < pending.ready_tick:
        world.step()
        assert world.totals()["quantity"] == (8,)
    assert carrier(world) == (2,)
    assert world.spatial_values(ORIGIN)["quantity"]["value"] == (6,)
    assert not world._spatial.nodes[ORIGIN].incoming
    joint = next(e for e in events.events if e.kind == "spatial_coupled")
    assert arrival.id in events.ancestors(joint.id)


def test_late_merge_cannot_bypass_a_joint_nonlinear_guard():
    raw = delayed(exchange(delayed=True, incoming=True))
    raw["normal_budget"] = 40
    world = Simulation(parse_initial_state(raw))
    planner = world._spatial.planner
    world._spatial._services = replace(
        world._spatial._services, planner=lambda *args: replace(planner(*args), cost=1)
    )
    world.step()
    ready = world.nodes[ORIGIN].pending.ready_tick
    while world.tick < ready - 1:
        world.step()
    before = world._spatial.nodes[ORIGIN].states
    incoming = world._spatial.nodes[ORIGIN].incoming
    with pytest.raises(ValueError, match="invariant"):
        world.step()
    assert world.faulted and world.nodes[ORIGIN].pending is not None
    assert carrier(world) == (5,)
    assert world._spatial.nodes[ORIGIN].states == before
    assert world._spatial.nodes[ORIGIN].incoming == incoming
    assert world.totals()["quantity"] == (8,)


@pytest.mark.parametrize("capacity", [4, 5])
def test_ready_commit_reserves_all_events_before_mutating_field_stock(capacity):
    raw = delayed(single_packet())
    raw["normal_budget"] = 100
    world = Simulation(parse_initial_state(traced(raw, capacity)))
    planner = world._spatial.planner
    world._spatial._services = replace(
        world._spatial._services, planner=lambda *args: replace(planner(*args), cost=169)
    )
    world.step()
    original = world._spatial.nodes[(2, 0, 0)].states
    for _ in range(2):
        world.step()
    assert world.event_space.next_id == 2
    if capacity == 4:
        with pytest.raises(OverflowError, match="causal event capacity"):
            world.step()
        assert world.faulted and world.event_space.next_id == 2
        assert world._spatial.nodes[(2, 0, 0)].states == original
        assert world.nodes[(2, 0, 0)].pending is not None
        assert not world.snapshot()["spatial_transfers"]
    else:
        world.step()
        assert world.event_space.next_id == 5
        assert world.nodes[(2, 0, 0)].pending is None
        packet = next(p for p in world._spatial.links[(2, 0, 0)] if p)
        assert packet.arrival_tick == 6
        assert world.event_space.event(packet.cause_id).kind == "spatial_sent"
    assert world.totals()["radiation"] == (8,)


def test_invalid_joint_proposal_changes_neither_original_owner():
    raw = delayed(exchange())
    raw["spatial_interactions"][0]["assignments"][0]["expression"] = 99
    world = Simulation(parse_initial_state(traced(raw)))
    stock = world.totals()
    with pytest.raises(ValueError):
        world.step()
    assert world.faulted
    assert world.totals() == stock
    assert carrier(world) == (5,)
    assert world.spatial_values(ORIGIN)["quantity"]["value"] == (2,)
    assert not world._spatial.nodes[ORIGIN].pending
    assert world.event_space.next_id == 2


@pytest.mark.parametrize("enabled", [False, True])
def test_pending_and_idle_owners_remain_formula_free(enabled):
    raw = delayed(finite_document(source=True, moving=True, budget=8))
    raw["spatial_computation_delay"] = enabled
    world = Simulation(parse_initial_state(raw))
    for _ in range(60):
        world.step()
        for owner in (*world.nodes.values(), *world._spatial.nodes.values()):
            assert node_state_violations(owner) == ()
        assert len(all_records(world)) == 1
        assert all(row["balanced"] for row in world.spatial_accounting().values())


@pytest.mark.parametrize("components", [1, 3])
@pytest.mark.parametrize("travel", [1, 2])
def test_real_field_cost_controls_arrival_for_scalar_and_vector_fields(components, travel):
    raw = delayed(document(components=components, travel=travel, budget=40))
    amount = 8 if components == 1 else [8, -8, 16]
    zero = 0 if components == 1 else [0, 0, 0]
    raw["spatial_fields"][0]["baseline"] = zero
    raw["spatial_fields"][0]["axis_weights"] = [1, 0, 0]
    raw["spatial_seeds"] = [
        {"position": list(FIELD_ORIGIN), "field": "radiation", "populations": [amount] + [zero] * 7}
    ]
    trace = []
    world = Simulation(parse_initial_state(raw), observer=trace.append)
    world.step()
    start = next(e for e in trace if e["event"] == "cycle_started")
    cycles = max(1, (start["cost"] + 39) // 40)
    assert cycles > 1
    assert start["ready_tick"] == (cycles - 1) * travel
    assert world._spatial._services.node_merge_cost == 32 * components
    while world.tick < cycles * travel:
        world.step()
    sent = next(e for e in trace if e["event"] == "spatial_sent")
    received = next(e for e in trace if e["event"] == "spatial_received")
    assert sent["tick"] == (cycles - 1) * travel
    assert received["tick"] == cycles * travel
    assert world.totals()["radiation"] == ((8,) if components == 1 else (8, -8, 16))


def test_causal_graph_does_not_change_delayed_physics_or_work():
    raw = delayed(single_packet())
    raw["normal_budget"] = 40
    plain = Simulation(parse_initial_state(raw))
    recorded = Simulation(parse_initial_state(traced(raw)))
    for _ in range(100):
        plain.step()
        recorded.step()
        assert plain.snapshot() == recorded.snapshot()
        assert plain.spatial_accounting() == recorded.spatial_accounting()
        assert (
            plain.computation_report()["model_operations_cost"]
            == recorded.computation_report()["model_operations_cost"]
        )
        assert plain.totals()["radiation"] == (8,)
    assert len(plain._spatial.nodes) <= 3
    assert (
        recorded.computation_report()["event_ledger_cost"]
        == recorded.computation_report()["model_operations_cost"]
    )


def test_finite_decay_waits_for_arrival_and_source_allowance_stays_exhausted():
    raw = delayed(finite_document(source=True, moving=False, budget=40, travel=2))
    raw["disturbance_types"][0]["defaults"]["strength"] = 2
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    previous_loss = 0
    for _ in range(180):
        events.clear()
        world.step()
        loss = world.dissipation_totals()["radiation"][0]
        if loss != previous_loss:
            assert any(e["event"] == "spatial_received" for e in events)
        previous_loss = loss
        assert all(row["balanced"] for row in world.spatial_accounting().values())
        assert len(all_records(world)) == 1
    assert world.source_totals()["radiation"] == (5,)
    assert unpack(all_records(world)[0].emission_remaining[0]) == (0,)
    assert world.dissipation_totals()["radiation"] == (5,)


def test_passive_linear_conservation_counts_buffered_inputs_once():
    raw = delayed(exchange(delayed=True, incoming=True))
    raw["normal_budget"] = 40
    raw["spatial_interactions"][0]["invariants"] = raw["spatial_interactions"][0]["invariants"][:1]
    control = Simulation(parse_initial_state(raw))
    raw["conservation"] = {
        "name": "linear shared cycle inventory",
        "energy_units": "model amount",
        "momentum_units": "model momentum",
        "carriers": [
            {
                "requires": ["quantity"],
                "energy": {"field": "quantity", "side": "left"},
                "momentum": [0, 0, 0],
            }
        ],
        "spatial": {"energy": {"field": "quantity", "side": "right"}, "momentum": [0, 0, 0]},
    }
    audited = Simulation(parse_initial_state(raw))
    for _ in range(40):
        control.step()
        audited.step()
        assert control.snapshot() == audited.snapshot()
        assert control.computation_report() == audited.computation_report()
        assert audited.conservation_report()["status"] == "passed"
        assert audited.conservation_report()["current"]["energy"] == 8


def test_continuous_port_input_can_be_empty_without_retiming_frozen_output():
    raw = delayed(single_packet())
    raw.update(link_ticks=1, normal_budget=100)
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    planner = world._spatial.planner
    world._spatial._services = replace(
        world._spatial._services, planner=lambda *args: replace(planner(*args), cost=369)
    )
    world.step()
    pending = world.nodes[(2, 0, 0)].pending
    assert pending.ready_tick == 4  # C = 369 + 32; ceil(C/100) = 5.
    origin = (1, 0, 0)
    for tick, amount in ((2, 3), (3, 0), (4, 3)):
        if amount:
            bundle = ((pack((amount,)),) + (pack((0,)),) * 7,)
            world._spatial.links[origin] = (SpatialPacket(tick, origin, 0, bundle),) + (None,) * 5
        world.step()
        if tick < 4:
            assert world.nodes[(2, 0, 0)].pending is pending
            assert world.spatial_values((2, 0, 0))["radiation"]["value"] == (8,)
    receipts = [e for e in events if e["event"] == "spatial_received"]
    assert [(e["tick"], e["received_fields"][1]["radiation"]) for e in receipts] == [
        (2, (3,)),
        (4, (3,)),
    ]
    packet = next(p for p in world._spatial.links[(2, 0, 0)] if p)
    assert (packet.port, packet.arrival_tick) == (0, 5)
    assert world.spatial_values((2, 0, 0))["radiation"]["value"] == (6,)
    assert world.totals()["radiation"] == (14,)


def test_run_records_shared_clock_and_variable_emission_schedule(tmp_path):
    raw = delayed(single_packet())
    path = tmp_path / "input.json"
    path.write_text(json.dumps(raw))
    output = tmp_path / "run"
    run_initialization(path, output, ticks=6)
    metadata = json.loads((output / "run.json").read_text())
    assert metadata["spatial_computation_delay"] is True
    assert metadata["local_clock"] == "shared-field-carrier-cycle-v1"
    assert metadata["emission_interval_ticks"] is None
    assert not (output / "run.html").exists()
