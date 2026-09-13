"""Finite emission and dissipation through real causal ownership transitions."""

import json
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE, pack, unpack
from event_universe.core.spatial_state import DecayDefinition, SpatialPacket
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization
from tests.test_spatial_engine import ORIGIN, document, offset, value


def finite_document(**kwargs):
    raw = document(**kwargs)
    raw["schema_version"] = 2
    raw["model_id"] = "finite-dissipative-contract-v1"
    raw["spatial_fields"][0].update(
        axis_weights=[1, 0, 0],
        octant_weights=[1, 0, 0, 0, 0, 0, 0, 0],
        decay={"retain_numerator": 1, "retain_denominator": 2, "residue": "dissipate"},
    )
    for rule in raw["emissions"]:
        rule["budget"] = 5
    return raw


def all_records(world):
    records = [r for node in world.nodes.values() for r in node.records if r is not None]
    records.extend(p.record for links in world.links.values() for p in links if p is not None)
    return records


def assert_balanced(world, initial):
    losses, sources = world.dissipation_totals(), world.source_totals()
    for name, total in world.totals().items():
        assert tuple(a + b for a, b in zip(total, losses[name], strict=True)) == tuple(
            a + b for a, b in zip(initial[name], sources[name], strict=True)
        )
    assert all(item["balanced"] for item in world.spatial_accounting().values())


@pytest.mark.parametrize("travel", [1, 2, 3])
def test_pulse_decays_only_on_completed_links_and_stops_at_zero(travel):
    raw = finite_document(travel=travel)
    raw["fields"][-1]["signed"] = False
    raw["spatial_seeds"] = [
        {"position": list(ORIGIN), "field": "radiation", "populations": [20, 0, 0, 0, 0, 0, 0, 0]}
    ]
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()
    sequence = (20, 10, 5, 2, 1, 0)
    for tick in range(1, 6 * travel + 1):
        world.step()
        expected = sequence[min(tick // travel, 5)]
        assert world.totals()["radiation"] == (expected,)
        assert_balanced(world, initial)
        if tick % travel == 0 and expected:
            assert value(world, offset(ORIGIN, (tick // travel, 0, 0))) == (expected,)
    assert world.dissipation_totals()["radiation"] == (20,)
    assert not world.snapshot()["spatial_transfers"]


@pytest.mark.parametrize("moving", [False, True])
def test_emission_budget_travels_and_stays_exhausted(moving):
    raw = finite_document(source=True, moving=moving)
    raw["disturbance_types"][0]["defaults"]["strength"] = 2
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()
    for source, remaining in ((2, 3), (4, 1), (5, 0), (5, 0), (5, 0), (5, 0)):
        world.step()
        assert world.source_totals()["radiation"] == (source,)
        assert unpack(all_records(world)[0].emission_remaining[0]) == (remaining,)
        assert_balanced(world, initial)
    assert world.totals()["radiation"] == (0,)
    assert world.dissipation_totals()["radiation"] == (5,)
    assert all(node.last_cost == 0 for node in world._spatial.nodes.values())


def test_fractional_emission_finishes_once_and_does_not_leave_debt():
    raw = finite_document(source=True, moving=True)
    raw["disturbance_types"][0]["defaults"]["strength"] = 1
    raw["emissions"][0].update(denominator=3, budget=1)
    world = Simulation(parse_initial_state(raw))
    for expected in (0, 0, 1, 1, 1, 1, 1):
        world.step()
        assert world.source_totals()["radiation"] == (expected,)
    record = all_records(world)[0]
    assert unpack(record.emission_remaining[0]) == (0,)
    assert unpack(record.emission_remainders[0]) == (0,)


def test_frozen_delayed_departure_does_not_restore_spent_emission_budget():
    raw = finite_document(source=True, moving=True, budget=8)
    raw["disturbance_types"][0]["defaults"]["strength"] = 2
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()
    world.step()
    pending = world.nodes[ORIGIN].pending
    assert pending is not None and pending.ready_tick > 3
    for _ in range(pending.ready_tick + 5):
        world.step()
        assert_balanced(world, initial)
    record = all_records(world)[0]
    assert unpack(record.emission_remaining[0]) == (0,)
    assert world.source_totals()["radiation"] == (5,)
    assert world.nodes[ORIGIN].records == (None,) * 4


def test_neighbor_packets_decay_separately_before_they_merge():
    raw = finite_document()
    raw["spatial_seeds"] = [
        {
            "position": list(offset(ORIGIN, (-1, 0, 0))),
            "field": "radiation",
            "populations": [1, 0, 0, 0, 0, 0, 0, 0],
        },
        {
            "position": list(offset(ORIGIN, (1, 0, 0))),
            "field": "radiation",
            "populations": [0, 0, 0, 0, 1, 0, 0, 0],
        },
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert value(world, ORIGIN) == (0,)
    assert world.dissipation_totals()["radiation"] == (2,)


def test_baseline_survives_while_emitted_deviation_extinguishes():
    raw = finite_document(source=True, baseline=7)
    raw["emissions"][0]["budget"] = 1
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()
    world.step()
    assert value(world, ORIGIN) == value(world, offset(ORIGIN, (1, 0, 0))) == (7,)
    assert world.totals()["radiation"] == (7 * 31**3,)
    assert_balanced(world, initial)


def test_failed_delivery_commits_neither_loss_nor_packet_removal():
    raw = finite_document()
    raw["spatial_seeds"] = [
        {
            "position": list(ORIGIN),
            "field": "radiation",
            "populations": [MAX_VALUE, 0, 0, 0, 0, 0, 0, 0],
        },
    ]
    world = Simulation(parse_initial_state(raw))
    engine = world._spatial
    source = offset(ORIGIN, (-1, 0, 0))
    population = (pack((MAX_VALUE,)),) + (pack((0,)),) * 7
    packet = SpatialPacket(1, source, 0, (population,))
    engine.links[source] = (packet,) + (None,) * 5
    old_states = engine.nodes[ORIGIN].states
    with pytest.raises(ValueError, match="bound"):
        engine.deliver(1)
    assert engine.nodes[ORIGIN].states == old_states
    assert engine.links[source][0] == packet
    assert world.dissipation_totals()["radiation"] == (0,)
    assert engine.nodes[ORIGIN].received_decay_cost == 0


def test_unsigned_packet_is_validated_before_decay_can_erase_it():
    raw = finite_document()
    raw["fields"][-1]["signed"] = False
    raw["spatial_fields"][0]["decay"]["retain_numerator"] = 0
    world = Simulation(parse_initial_state(raw))
    population = (pack((-1,)),) + (pack((0,)),) * 7
    packet = SpatialPacket(1, ORIGIN, 0, (population,))
    world._spatial.links[ORIGIN] = (packet,) + (None,) * 5
    with pytest.raises(ValueError, match="negative"):
        world._spatial.deliver(1)
    assert world._spatial.links[ORIGIN][0] == packet
    assert world.dissipation_totals()["radiation"] == (0,)


def test_partial_budget_metadata_cannot_reinitialize_an_exhausted_emitter():
    raw = finite_document(source=True)
    world = Simulation(parse_initial_state(raw))
    world.step()
    record = all_records(world)[0]
    world._nodes[ORIGIN].records = (
        replace(record, emission_remainders=(), emission_phases=()),
        None,
        None,
        None,
    )
    # Invoke the law directly: an exhausted source need not be scheduled again.
    with pytest.raises(ValueError, match="partial"):
        world._spatial.planner(world._spatial.nodes[ORIGIN].states, world._nodes[ORIGIN].records, 0)


def test_runner_distinguishes_dissipation_accounting_from_physical_conservation(tmp_path):
    raw = finite_document(source=True)
    initial = tmp_path / "initial.json"
    initial.write_text(json.dumps(raw), encoding="utf-8")
    output = tmp_path / "run"
    run_initialization(initial, output, ticks=8)
    metadata = json.loads((output / "run.json").read_text())
    assert metadata["status"] == "completed"
    assert metadata["display"] == "none"
    assert metadata["spatial_policy"] == "finite-dissipative-v1"
    assert metadata["accounting_balanced_at_every_completed_tick"] is True
    assert metadata["conserved_at_every_completed_tick"] is False
    assert metadata["dissipation_totals"]["radiation"] == [5]
    assert metadata["spatial_accounting"]["radiation"]["balanced"] is True
    assert not list(output.glob("*.html"))


def localizing_document(**kwargs):
    raw = finite_document(**kwargs)
    raw["model_id"] = "finite-localizing-contract-v1"
    # The default residue: omit the key to select localizing decay.
    del raw["spatial_fields"][0]["decay"]["residue"]
    return raw


def localized(world, position):
    return world.spatial_values(position)["radiation"]["localized"]


@pytest.mark.parametrize(("travel", "shared_clock"), [(1, False), (2, False), (1, True)])
def test_localizing_decay_preserves_total_flux_and_deposits_stationary_stock(travel, shared_clock):
    raw = localizing_document(travel=travel)
    raw["spatial_computation_delay"] = shared_clock
    raw["fields"][-1]["signed"] = False
    raw["spatial_seeds"] = [
        {"position": list(ORIGIN), "field": "radiation", "populations": [20, 0, 0, 0, 0, 0, 0, 0]}
    ]
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()
    moving = (20, 10, 5, 2, 1, 0)
    deposits = (0, 10, 5, 3, 1, 1)
    for tick in range(1, 8 * travel + 1):
        world.step()
        links = min(tick // travel, 5)
        # Total flux never changes: moving stock plus stationary deposits is 20.
        assert world.totals()["radiation"] == (20,)
        assert world.dissipation_totals()["radiation"] == (0,)
        assert world.localized_totals()["radiation"] == (sum(deposits[: links + 1]),)
        assert_balanced(world, initial)
        if tick % travel == 0 and moving[links]:
            assert value(world, offset(ORIGIN, (links, 0, 0))) == (moving[links],)
    for links, deposit in enumerate(deposits):
        assert localized(world, offset(ORIGIN, (links, 0, 0))) == (deposit,)
    assert localized(world, offset(ORIGIN, (6, 0, 0))) == (0,)
    assert not world.snapshot()["spatial_transfers"]
    accounting = world.spatial_accounting()["radiation"]
    assert accounting["localized"] == (20,) and accounting["dissipated"] == (0,)
    assert accounting["balanced"]


def test_localizing_neighbor_packets_deposit_separately_before_they_merge():
    raw = localizing_document()
    raw["spatial_seeds"] = [
        {
            "position": list(offset(ORIGIN, (-1, 0, 0))),
            "field": "radiation",
            "populations": [1, 0, 0, 0, 0, 0, 0, 0],
        },
        {
            "position": list(offset(ORIGIN, (-2, 0, 0))),
            "field": "radiation",
            "populations": [2, 0, 0, 0, 0, 0, 0, 0],
        },
    ]
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    initial = world.totals()
    world.step()
    # Both single units become stationary at the receiving Nodes; nothing merges first.
    assert value(world, ORIGIN) == (0,) and localized(world, ORIGIN) == (1,)
    assert value(world, offset(ORIGIN, (-1, 0, 0))) == (1,)
    assert localized(world, offset(ORIGIN, (-1, 0, 0))) == (1,)
    world.step()
    assert localized(world, ORIGIN) == (2,) and value(world, ORIGIN) == (0,)
    assert world.totals()["radiation"] == (3,)
    assert world.dissipation_totals()["radiation"] == (0,)
    assert_balanced(world, initial)
    decayed = [event for event in events if event["event"] == "spatial_decayed"]
    assert decayed and all(event["dissipated"] == {} for event in decayed)
    assert [event["localized"] for event in decayed if event["tick"] == 1] == [
        {"radiation": (1,)},
        {"radiation": (1,)},
    ]


def test_localizing_deposit_is_not_transported_by_later_arrivals():
    raw = localizing_document()
    raw["spatial_seeds"] = [
        {"position": list(ORIGIN), "field": "radiation", "populations": [4, 0, 0, 0, 0, 0, 0, 0]},
        {
            "position": list(offset(ORIGIN, (-2, 0, 0))),
            "field": "radiation",
            "populations": [8, 0, 0, 0, 0, 0, 0, 0],
        },
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    first = offset(ORIGIN, (1, 0, 0))
    assert localized(world, first) == (2,) and value(world, first) == (2,)
    for _ in range(2):
        world.step()
    # The second pulse reaches this Node as 2 and deposits 1 more, while the
    # earlier deposit stayed put instead of leaving with the moving stock.
    assert localized(world, first) == (3,) and value(world, first) == (1,)
    assert world.totals()["radiation"] == (12,)


def test_decay_residue_is_validated_and_recorded(tmp_path):
    raw = localizing_document()
    raw["spatial_fields"][0]["decay"]["residue"] = "evaporate"
    with pytest.raises(ValueError, match="residue"):
        parse_initial_state(raw)
    raw["spatial_fields"][0]["decay"]["residue"] = 1
    with pytest.raises(ValueError, match="residue"):
        parse_initial_state(raw)
    raw = localizing_document(source=True)
    raw["disturbance_types"][0]["defaults"]["strength"] = 2
    path = tmp_path / "localizing.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=6)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text())
    assert metadata["spatial_policy"] == "finite-localizing-v1"
    assert metadata["spatial_decay_residue"] == ["localize"]
    assert DecayDefinition(1, 2) == DecayDefinition(1, 2, "localize")
    assert metadata["dissipation_totals"]["radiation"] == [0]
    assert metadata["localized_totals"]["radiation"] == [5]
    assert metadata["final_totals"]["radiation"] == [5]
    assert metadata["accounting_balanced_at_every_completed_tick"]
