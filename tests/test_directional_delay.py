"""Independent directional waiting, ownership and fixed transit expectations."""

from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state


def configuration(load=(6, -4, 0), tau=1):
    return {
        "schema_version": 1,
        "model_id": "directional-delay-acceptance-v1",
        "shape": [17, 17, 17],
        "boundary": "open",
        "slots_per_cell": 8,
        "link_ticks": tau,
        "normal_budget": 1000000,
        "ticks": 12,
        "directional_delay": {
            "model_id": "positive-projection-origin-wait-v1",
            "field": "load",
            "divisor": 2,
        },
        "operation_costs": {
            k: 1
            for k in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {"name": n, "components": c, "units": "test unit", "signed": True, "conserved": True}
            for n, c in (("mass", 1), ("momentum", 3), ("load", 3), ("pulse", 3))
        ],
        "disturbance_types": [
            {
                "name": "probe",
                "fields": ["mass", "momentum"],
                "defaults": {"mass": 1, "momentum": [1, 0, 0]},
                "transport": {"mode": "move", "direction_field": "momentum"},
            }
        ],
        "spatial_fields": [
            {"field": "load", "baseline": list(load), "transport": "local"},
            {"field": "pulse", "baseline": [0, 0, 0], "transport": "outward"},
        ],
        "spatial_seeds": [{"position": [8, 8, 8], "field": "pulse", "populations": [[24, 0, 0]] * 8}],
        "seeds": [{"position": [8, 8, 8], "type": "probe"}],
    }


@pytest.mark.parametrize("tau", [1, 2])
def test_field_and_carrier_share_frozen_wait_and_fixed_link_time(tau):
    raw = configuration(tau=tau)
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    initial = world.totals()
    world.step()
    packet = world.snapshot()["transfers"][0]
    assert packet["phase"] == "waiting"
    assert packet["dispatch_tick"] == 3 * tau
    assert packet["arrival_tick"] == 4 * tau
    for _ in range(4 * tau - 1):
        world.step()
        assert world.totals()["mass"] == initial["mass"]
        assert world.totals()["momentum"] == initial["momentum"]
        assert world.totals()["pulse"] == initial["pulse"]
    field_departures = {
        e["port"]: e["tick"]
        for e in events
        if e["event"] == "spatial_sent" and e["position"] == (8, 8, 8)
    }
    assert field_departures == {0: 3 * tau, 1: 0, 2: 0, 3: 2 * tau, 4: 0, 5: 0}
    carrier = next(e for e in events if e["event"] == "sent")
    assert carrier["tick"] == 3 * tau and carrier["arrival_tick"] == 4 * tau
    for e in events:
        if e["event"] in ("sent", "spatial_sent"):
            assert e["arrival_tick"] - e["tick"] == tau


def test_reverse_vector_reverses_slow_ports():
    raw = configuration((-6, 4, 0))
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()
    waits = {e["port"]: e["dispatch_tick"] for e in events if e["event"] == "spatial_departure_waiting"}
    assert waits == {1: 3, 2: 2}


@pytest.mark.parametrize("tick", [1, 3, 4])
def test_checkpoint_preserves_waiting_and_dispatched_ownership(tmp_path, tick):
    raw = configuration()
    world = Simulation(parse_initial_state(raw))
    for _ in range(tick):
        world.step()
    checkpoint = world.save_checkpoint(tmp_path / "state.json")
    resumed = Simulation.from_checkpoint(checkpoint)
    assert resumed.snapshot() == world.snapshot()
    for _ in range(5):
        world.step()
        resumed.step()
        assert resumed.snapshot() == world.snapshot()


def test_oblique_carrier_keeps_control_port_sequence():
    raw = configuration((2, 0, 0))
    raw["spatial_seeds"] = []
    raw["seeds"][0]["values"] = {"momentum": [2, 1, 0]}
    sequences = []
    for enabled in (False, True):
        candidate = deepcopy(raw)
        if not enabled:
            candidate.pop("directional_delay")
        events = []
        world = Simulation(parse_initial_state(candidate), observer=events.append)
        for _ in range(12):
            world.step()
        sequences.append([e["port"] for e in events if e["event"] == "sent"])
    assert sequences[1] == sequences[0][: len(sequences[1])]


def test_overflow_cannot_remove_owned_payload():
    raw = configuration((1073741823, 0, 0), tau=2)
    raw["directional_delay"]["divisor"] = 1
    world = Simulation(parse_initial_state(raw))
    before = world.totals()
    with pytest.raises(ValueError, match="bound"):
        world.step()
    assert world.totals() == before


def test_signed_cancellation_uses_working_registers():
    raw = configuration((1073741823, 0, 0))
    raw["directional_delay"]["divisor"] = 1073741823
    raw["spatial_seeds"].append(
        {
            "position": [8, 8, 8],
            "field": "load",
            "populations": [[1, 0, 0], [-1, 0, 0]] + [[0, 0, 0]] * 6,
        }
    )
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert world.snapshot()["transfers"][0]["dispatch_tick"] == 1


def test_pending_checkpoint_requires_frozen_waits():
    from dataclasses import replace

    from event_universe.checkpoint_validation import validate_world

    raw = configuration()
    raw["normal_budget"] = 1
    world = Simulation(parse_initial_state(raw))
    world.step()
    cell = next(c for c in world._cells.values() if c.pending is not None)
    cell.pending = replace(cell.pending, plan=replace(cell.pending.plan, port_waits=()))
    with pytest.raises(ValueError, match="port waits"):
        validate_world(world)


def test_open_escape_happens_only_after_wait_and_transit():
    raw = configuration(tau=2)
    raw["seeds"][0]["position"] = [16, 8, 8]
    raw["spatial_seeds"][0]["position"] = [16, 8, 8]
    world = Simulation(parse_initial_state(raw))
    for _ in range(7):
        world.step()
        assert world.totals()["mass"] == (1,)
    world.step()
    assert world.totals()["mass"] == (0,)


def test_later_driver_arrival_does_not_reschedule_reserved_packets():
    raw = configuration()
    raw["spatial_fields"][0]["transport"] = "outward"
    raw["spatial_seeds"].append(
        {"position": [9, 8, 8], "field": "load", "populations": [[24, 0, 0]] * 8}
    )
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    initial = world.totals()
    world.step()
    first = world.snapshot()
    for _ in range(2):
        world.step()
        assert world.totals() == initial
    sent = [
        e
        for e in events
        if e["event"] in ("sent", "spatial_sent") and e["position"] == (8, 8, 8) and e["port"] == 0
    ]
    assert {e["event"] for e in sent} == {"sent", "spatial_sent"}
    assert all(e["tick"] == 3 and e["arrival_tick"] == 4 for e in sent)
    assert first["transfers"][0]["dispatch_tick"] == 3
    assert world._spatial.cells[(8, 8, 8)].port_waits[0] > 3


def test_zero_driver_has_zero_wait_but_metered_arithmetic():
    world = Simulation(parse_initial_state(configuration((0, 0, 0))))
    world.step()
    assert world._spatial.cells[(8, 8, 8)].port_waits == (0,) * 6
    assert world._spatial.cells[(8, 8, 8)].last_cost > 0


def test_typed_invalid_divisor_is_rejected():
    from dataclasses import replace

    initial = parse_initial_state(configuration())
    rule = replace(initial.directional_delay, divisor=0)
    with pytest.raises(ValueError, match="positive"):
        Simulation(replace(initial, directional_delay=rule))


def test_finite_emission_waits_and_decay_is_on_arrival():
    raw = configuration((6, 0, 0), tau=2)
    raw["schema_version"] = 2
    raw["spatial_seeds"] = []
    for field in raw["spatial_fields"]:
        field["transport"] = "outward"
        field["decay"] = {"retain_numerator": 1, "retain_denominator": 2}
        field["axis_weights"] = [1, 0, 0]
        field["octant_weights"] = [1, 0, 0, 0, 0, 0, 0, 0]
    raw["disturbance_types"][0]["transport"] = {"mode": "hold"}
    raw["disturbance_types"][0]["defaults"]["momentum"] = [16, 0, 0]
    raw["emissions"] = [
        {
            "type": "probe",
            "field": "pulse",
            "amount": {"field": "momentum"},
            "denominator": 1,
            "source": True,
            "budget": [32, 0, 0],
        }
    ]
    world = Simulation(parse_initial_state(raw))
    for _ in range(7):
        world.step()
        assert world.dissipation_totals()["pulse"] == (0, 0, 0)
        assert world.totals()["pulse"] == (16, 0, 0)
    world.step()
    assert world.dissipation_totals()["pulse"] == (8, 0, 0)
    assert world.totals()["pulse"] == (8, 0, 0)
    world.step()
    assert world.totals()["pulse"] == (24, 0, 0)
