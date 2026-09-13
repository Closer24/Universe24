"""Bounded field provenance must explain existing dynamics without changing it."""

import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_finite_spatial_engine import all_records, finite_document
from .test_spatial_coupling import document as coupling_document
from .test_spatial_engine import ORIGIN, document
from .test_spatial_interactions import ORIGIN as JOINT_ORIGIN
from .test_spatial_interactions import exchange


def traced(raw, capacity=100_000):
    raw = deepcopy(raw)
    raw["event_program"] = {"model": "causal-events-v1", "capacity": capacity}
    return raw


@pytest.mark.parametrize("entry", ["parse", "runtime", "simulation"])
def test_typed_conservation_composition_is_rejected_before_runtime_allocation(entry, monkeypatch):
    from event_universe.core.event_space import CausalEventSpace
    from event_universe.integration.event_program import parse_event_program
    from event_universe.integration.event_runtime import NativeEventResolver, build_event_runtime

    from .test_local_conservation import converging_packets

    initial = replace(
        parse_initial_state(converging_packets()),
        event_program=json.dumps({"model": "causal-events-v1", "capacity": 10000}),
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("Unsupported composition must fail before runtime allocation")

    monkeypatch.setattr(CausalEventSpace, "__init__", forbidden)
    monkeypatch.setattr(NativeEventResolver, "__init__", forbidden)
    start = {"parse": parse_event_program, "runtime": build_event_runtime, "simulation": Simulation}
    with pytest.raises(ValueError, match="conservation audit does not support native event programs"):
        start[entry](initial)


def pulse(*, travel=2):
    raw = document(travel=travel)
    raw["spatial_seeds"] = [{"position": list(ORIGIN), "field": "radiation", "populations": [27] * 8}]
    return raw


def test_field_packets_retain_local_sources_and_full_link_time():
    trace = []
    world = Simulation(parse_initial_state(traced(pulse())), observer=trace.append)
    events = world.event_space
    assert events is not None and world._resolver is None
    assert events.next_id == 1
    source = events.event(0)
    assert (source.kind, source.owner, source.tick) == ("spatial_source", "spatial", 0)
    world.step()
    assert not any(e.kind == "spatial_received" for e in events.events)
    sends = [e for e in events.events if e.kind == "spatial_sent"]
    assert len(sends) == 6
    assert len({e.parents for e in sends}) == 1  # Sibling sends do not cause one another.
    world.step()
    receipts = [e for e in events.events if e.kind == "spatial_received"]
    assert len(receipts) == 6
    for receipt in receipts:
        parents = [events.event(p) for p in receipt.parents]
        assert len(parents) == 1 and parents[0] in sends
        assert receipt.tick - parents[0].tick == 2
        assert source.id in events.ancestors(receipt.id)
    assert world.totals()["radiation"] == (216,)
    assert {e["event_id"] for e in trace} == set(range(events.next_id))


@pytest.mark.parametrize("moving", [False, True])
def test_tracing_preserves_field_carrier_states_costs_and_waits(moving):
    raw = document(source=True, moving=moving, budget=5, travel=2)
    ordinary = Simulation(parse_initial_state(raw))
    recorded = Simulation(parse_initial_state(traced(raw)))
    for _ in range(12):
        ordinary.step()
        recorded.step()
        assert ordinary.snapshot() == recorded.snapshot()
        assert all_records(ordinary) == all_records(recorded)
        for position, node in recorded._spatial.nodes.items():
            assert (
                replace(node, cause_id=None, sample_cause_id=None, cost_cause_id=None)
                == ordinary._spatial.nodes[position]
            )
        assert ordinary.spatial_accounting() == recorded.spatial_accounting()
        for key, value in ordinary.computation_report().items():
            assert recorded.computation_report()[key] == value
        assert (
            recorded.computation_report()["event_ledger_cost"]
            == recorded.computation_report()["model_operations_cost"]
        )
    events = recorded.event_space
    starts = [e for e in events.events if e.kind == "cycle_started"]
    assert starts and any(
        events.event(parent).kind == "spatial_cycle" for e in starts for parent in e.parents
    )


def test_spatial_departure_capacity_failure_preserves_the_whole_local_owner():
    # One root fits, but one cycle plus six outgoing events needs seven more slots.
    world = Simulation(parse_initial_state(traced(pulse(), capacity=7)))
    before = world.snapshot()
    with pytest.raises(OverflowError, match="causal event capacity"):
        world.step()
    assert world.faulted
    assert world.snapshot() == before
    assert world.event_space.next_id == 1
    with pytest.raises(RuntimeError, match="cannot continue"):
        world.step()


def single_packet(*, boundary="periodic"):
    raw = pulse()
    raw.update(shape=[3, 1, 1], boundary=boundary)
    raw["spatial_fields"][0]["axis_weights"] = [1, 0, 0]
    raw["spatial_seeds"][0].update(position=[2, 0, 0], populations=[8, 0, 0, 0, 0, 0, 0, 0])
    return raw


@pytest.mark.parametrize(
    "boundary,kind", [("periodic", "spatial_received"), ("open", "spatial_escaped")]
)
@pytest.mark.parametrize("capacity", [3, 4])
def test_exact_link_completion_capacity_and_fail_stop_ownership(boundary, kind, capacity):
    world = Simulation(parse_initial_state(traced(single_packet(boundary=boundary), capacity)))
    world.step()
    assert world.event_space.next_id == 3
    assert world.totals()["radiation"] == (8,)
    before = world.snapshot()["spatial_transfers"]
    if capacity == 3:
        with pytest.raises(OverflowError, match="causal event capacity"):
            world.step()
        assert world.snapshot()["spatial_transfers"] == before
        assert world.totals()["radiation"] == (8,)
        assert world.escaped_totals()["radiation"] == (0,)
        assert world.event_space.next_id == 3
    else:
        world.step()
        last = world.event_space.events[-1]
        assert (last.kind, last.tick, last.parents) == (kind, 2, (2,))
        assert not world.snapshot()["spatial_transfers"]
        assert world.totals()["radiation"] == ((8,) if boundary == "periodic" else (0,))
    assert all(item["balanced"] for item in world.spatial_accounting().values())


def test_periodic_return_is_a_new_event_with_an_acyclic_history():
    world = Simulation(parse_initial_state(traced(single_packet())))
    for _ in range(6):
        world.step()
    events = world.event_space
    returned = events.events[-1]
    assert (returned.kind, returned.addresses, returned.tick) == ("spatial_received", ((2, 0, 0),), 6)
    assert 0 in events.ancestors(returned.id)
    assert all(p < e.id for e in events.events for p in e.parents)
    assert world.totals()["radiation"] == (8,)


@pytest.mark.parametrize("decay", [False, True])
def test_zero_result_retains_both_arrival_causes_and_atomic_decay(decay):
    raw = finite_document(travel=2) if decay else document(travel=2)
    raw["spatial_fields"][0]["axis_weights"] = [1, 0, 0]
    raw["spatial_seeds"] = [
        {"position": [14, 15, 15], "field": "radiation", "populations": [1, 0, 0, 0, 0, 0, 0, 0]},
        {
            "position": [16, 15, 15],
            "field": "radiation",
            "populations": [0, 0, 0, 0, 1 if decay else -1, 0, 0, 0],
        },
    ]
    expected_events = 8 if decay else 7
    world = Simulation(parse_initial_state(traced(raw, expected_events)))
    world.step()
    world.step()
    events = world.event_space
    receipt = next(e for e in events.events if e.kind == "spatial_received")
    assert len(receipt.parents) == 2
    assert {events.event(p).kind for p in receipt.parents} == {"spatial_sent"}
    assert {0, 1}.issubset(events.ancestors(receipt.id))
    assert world.spatial_values(ORIGIN)["radiation"]["value"] == (0,)
    assert world.dissipation_totals()["radiation"] == ((2,) if decay else (0,))
    assert events.next_id == expected_events
    failed = Simulation(parse_initial_state(traced(raw, expected_events - 1)))
    failed.step()
    before = failed.snapshot()["spatial_transfers"]
    with pytest.raises(OverflowError, match="causal event capacity"):
        failed.step()
    assert failed.event_space.next_id == 6
    assert failed.snapshot()["spatial_transfers"] == before
    assert failed.dissipation_totals()["radiation"] == (0,)


def test_finite_emission_links_carrier_source_and_preserves_spent_allowance():
    raw = finite_document(source=True, moving=True, budget=8)
    raw["disturbance_types"][0]["defaults"]["strength"] = 2
    ordinary = Simulation(parse_initial_state(raw))
    world = Simulation(parse_initial_state(traced(raw)))
    for _ in range(20):
        ordinary.step()
        world.step()
        assert world.snapshot() == ordinary.snapshot()
        assert all_records(world) == all_records(ordinary)
    events = world.event_space
    source = next(e for e in events.events if e.kind == "source")
    emission = next(e for e in events.events if e.kind == "spatial_cycle")
    assert source.id in emission.parents
    start = next(e for e in events.events if e.kind == "cycle_started")
    assert emission.id in start.parents
    sent = next(e for e in events.events if e.kind == "sent")
    assert emission.id in events.ancestors(sent.id)
    assert world.source_totals()["radiation"] == (5,)


def test_delayed_joint_commit_keeps_frozen_sample_and_later_field_causes_distinct():
    raw = exchange(delayed=True, incoming=True)
    raw["spatial_interactions"][0]["invariants"] = raw["spatial_interactions"][0]["invariants"][:1]
    ordinary = Simulation(parse_initial_state(raw))
    world = Simulation(parse_initial_state(traced(raw)))
    world.step()
    ordinary.step()
    pending = world.nodes[JOINT_ORIGIN].pending
    events = world.event_space
    start = events.event(pending.cause_id)
    seed = next(
        e for e in events.events if e.kind == "spatial_source" and e.addresses == (JOINT_ORIGIN,)
    )
    later = next(
        e for e in events.events if e.kind == "spatial_received" and e.addresses == (JOINT_ORIGIN,)
    )
    assert seed.id in start.parents and later.id not in events.ancestors(start.id)
    while world.tick < pending.ready_tick:
        world.step()
        ordinary.step()
        assert world.snapshot() == ordinary.snapshot()
    joint = next(e for e in events.events if e.kind == "spatial_coupled")
    assert {start.id, later.id}.issubset(events.ancestors(joint.id))
    assert world._spatial.nodes[JOINT_ORIGIN].cause_id == joint.id
    assert world.totals()["quantity"] == (8,)
    assert world.spatial_values(JOINT_ORIGIN)["quantity"]["value"] == (6,)


def test_reaction_created_packets_refer_to_joint_commit_before_observer_runs():
    raw = coupling_document()
    raw["link_ticks"] = 2
    world = Simulation(parse_initial_state(traced(raw)))
    observed = []

    def observe(event):
        if event["event"] == "cycle_committed":
            packets = [p for links in world._spatial.links.values() for p in links if p is not None]
            assert packets and all(
                world.event_space.event(p.cause_id).kind == "spatial_coupled" for p in packets
            )
            observed.append(event)

    world._observer = observe
    world.step()
    assert observed
    events = world.event_space
    joint = next(e for e in events.events if e.kind == "spatial_coupled")
    world.step()
    receipts = [e for e in events.events if e.kind == "spatial_received"]
    assert receipts and all(joint.id in e.parents for e in receipts)
    assert world.totals()["inventory"] == (5, 0, 0)


@pytest.mark.parametrize("cancel", [False, True])
def test_joint_reaction_replaces_or_cancels_same_tick_packet_provenance(cancel):
    raw = coupling_document(vector=(8, 0, 0))
    raw["link_ticks"] = 2
    raw["spatial_seeds"] = [
        {
            "position": list(ORIGIN),
            "field": "inventory",
            "populations": [[-1, 1, 0] if cancel else [2, 0, 0]] * 8,
        }
    ]
    ordinary = Simulation(parse_initial_state(raw))
    trace = []
    world = Simulation(parse_initial_state(traced(raw)), observer=trace.append)
    world.step()
    ordinary.step()
    assert world.snapshot() == ordinary.snapshot()
    events = world.event_space
    joint = next(e for e in events.events if e.kind == "spatial_coupled")
    sends = [e for e in events.events if e.kind == "spatial_sent"]
    assert len(sends) == 2 and {e.id for e in sends}.issubset(events.ancestors(joint.id))
    amended = next(e for e in trace if e["event"] == "spatial_coupled")
    assert len(amended["spatial_departures"]) == (0 if cancel else 2)
    world.step()
    ordinary.step()
    assert world.snapshot() == ordinary.snapshot()
    receipts = [e for e in events.events if e.kind == "spatial_received"]
    assert len(receipts) == (0 if cancel else 2)
    assert all(joint.id in e.parents for e in receipts)
    assert world.totals()["inventory"] == ((0, 8, 0) if cancel else (24, 0, 0))


def test_joint_capacity_failure_keeps_both_owners_and_original_packet_causes():
    raw = coupling_document(vector=(8, 0, 0))
    raw["link_ticks"] = 2
    raw["spatial_seeds"] = [
        {"position": list(ORIGIN), "field": "inventory", "populations": [[2, 0, 0]] * 8}
    ]
    # Two sources, one field cycle/two sends, one carrier start: six events.
    # The joint carrier commit and coupling need two more, not just one.
    world = Simulation(parse_initial_state(traced(raw, 7)))
    with pytest.raises(OverflowError, match="causal event capacity"):
        world.step()
    assert world.event_space.next_id == 6
    assert world.nodes[ORIGIN].pending is not None
    assert world.spatial_accounting()["inventory"]["reactions"] == (0, 0, 0)
    assert world.totals()["inventory"] == (24, 0, 0)
    assert all(
        world.event_space.event(p.cause_id).kind == "spatial_sent"
        for p in world._spatial.links[ORIGIN]
        if p is not None
    )


def test_classical_recording_never_queries_quantum_or_traverses_ancestors(monkeypatch):
    from event_universe.core.event_space import CausalEventSpace
    from event_universe.integration.event_runtime import NativeEventResolver

    def forbidden(*args, **kwargs):
        raise AssertionError("Ordinary field provenance must not evaluate quantum or history")

    monkeypatch.setattr(NativeEventResolver, "__init__", forbidden)
    monkeypatch.setattr(CausalEventSpace, "ancestors", forbidden)
    world = Simulation(parse_initial_state(traced(single_packet(), capacity=100)))
    with pytest.raises(OverflowError, match="causal event capacity"):
        for _ in range(100):
            world.step()
    assert world.faulted and world.event_space.next_id <= 100
    assert len(world._spatial.nodes) == 3
    assert not world._nodes
    assert max(len(e.parents) for e in world.event_space.events) <= 2


@pytest.mark.parametrize("capacity,status", [(4, "completed"), (3, "failed")])
def test_headless_runner_retains_graph_and_failure_metadata(tmp_path, capacity, status):
    raw = traced(single_packet(), capacity)
    raw["ticks"] = 2
    initial = tmp_path / "initial.json"
    initial.write_text(json.dumps(raw), encoding="utf-8")
    output = tmp_path / "run"
    if status == "failed":
        with pytest.raises(OverflowError, match="causal event capacity"):
            run_initialization(initial, output)
    else:
        run_initialization(initial, output)
    metadata = json.loads((output / "run.json").read_text(encoding="utf-8"))
    assert metadata["status"] == status
    assert metadata["accounting_balanced_at_every_completed_tick"]
    assert "resolver" not in metadata["computation"]
    graph = [
        json.loads(line)
        for line in (output / "causal-events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(graph) == capacity
    assert {e["owner"] for e in graph} == {"spatial"}
    assert not (output / "run.html").exists()


def test_shipped_encounter_retains_two_histories_after_signed_field_cancels():
    raw = json.loads(
        (Path(__file__).resolve().parents[1] / "examples/spatial_causal_events.json").read_text(
            encoding="utf-8"
        )
    )
    world = Simulation(parse_initial_state(raw))
    for _ in range(raw["ticks"]):
        world.step()
        assert world.totals()["signal"] == (0,)
        assert world.spatial_accounting()["signal"]["balanced"]
    events = world.event_space
    encounter = next(
        e for e in events.events if e.kind == "spatial_received" and e.addresses == ((4, 2, 2),)
    )
    assert encounter.tick == 6 and len(encounter.parents) == 2
    assert {0, 1}.issubset(events.ancestors(encounter.id))
    assert events.next_id == 20
    assert world._spatial._active == set()
    assert not world.snapshot()["spatial_transfers"]
