"""Carried source fractions survive frozen proposals and moving between nodes."""

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS, unpack
from event_universe.initialization import parse_initial_state

ORIGIN = (3, 3, 3)


def initialization(*, reporter=False):
    return {
        "schema_version": 1,
        "model_id": "delayed-carried-source-residual-v1",
        "shape": [19, 19, 19],
        "slots_per_node": 3,
        "link_ticks": 1,
        "normal_budget": 10,
        "ticks": 12,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "stock", "components": 1, "units": "unit", "signed": True, "conserved": True},
            {"name": "radiation", "components": 1, "units": "unit", "signed": True, "conserved": True},
            {"name": "work", "components": 1, "units": "cost", "signed": False, "conserved": False},
        ],
        "disturbance_types": [
            {
                "name": "emitter",
                "fields": ["stock"],
                "defaults": {"stock": 2},
                "transport": {"mode": "move", "weights": [1, 0, 0, 0, 0, 0]},
                "updates": [{"field": "stock", "source": True, "expression": 99}],
            },
            {
                "name": "reporter",
                "fields": ["work"],
                "transport": {"mode": "hold"},
                "cost_field": "work",
            },
        ],
        "seeds": [{"position": list(ORIGIN), "type": "emitter"}]
        + ([{"position": list(ORIGIN), "type": "reporter"}] if reporter else []),
        "spatial_fields": [{"field": "radiation", "baseline": 0, "transport": "outward"}],
        "emissions": [
            {"type": "emitter", "field": "radiation", "amount": 1, "denominator": 101, "source": True}
        ],
    }


def test_delayed_departure_uses_latest_carried_fraction_but_frozen_physical_values():
    world = Simulation(parse_initial_state(initialization()))
    world.step()
    pending = world.nodes[ORIGIN].pending
    assert pending is not None
    ready = pending.ready_tick
    assert 2 <= ready < 101
    while world.tick < ready:
        record = next(record for record in world.nodes[ORIGIN].records if record is not None)
        assert world.record_values(record) == {"stock": (2,)}
        assert unpack(record.emission_remainders[0]) == (world.tick,)
        assert world.nodes[ORIGIN].pending == pending
        world.step()
    packet = next(packet for packet in world.links[ORIGIN] if packet is not None)
    assert world.record_values(packet.record) == {"stock": (99,)}
    assert unpack(packet.record.emission_remainders[0]) == (ready,)
    assert world.source_totals() == {"stock": (97,), "radiation": (0,)}
    world.step()
    destination = (4, 3, 3)
    record = next(record for record in world.nodes[destination].records if record is not None)
    assert unpack(record.emission_remainders[0]) == (ready,)
    world.step()
    record = next(record for record in world.nodes[destination].records if record is not None)
    assert unpack(record.emission_remainders[0]) == (ready + 1,)
    assert world.source_totals()["radiation"] == (0,)


def test_co_resident_emitters_keep_independent_fractional_ownership():
    raw = initialization()
    raw["normal_budget"] = 10000
    raw["disturbance_types"][0]["transport"] = {"mode": "hold"}
    raw["disturbance_types"][0]["updates"] = []
    raw["emissions"][0]["denominator"] = 2
    raw["seeds"].append({"position": list(ORIGIN), "type": "emitter"})
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert world.source_totals()["radiation"] == (0,)
    records = [record for record in world.nodes[ORIGIN].records if record is not None]
    assert [unpack(record.emission_remainders[0]) for record in records] == [(1,), (1,)]
    world.step()
    assert world.source_totals()["radiation"] == (2,)
    records = [record for record in world.nodes[ORIGIN].records if record is not None]
    assert [unpack(record.emission_remainders[0]) for record in records] == [(0,), (0,)]


def test_configured_cost_reporter_matches_full_cost_used_for_delay():
    raw = initialization(reporter=True)
    raw["normal_budget"] = 10000
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()
    cycle = next(
        event for event in events if event["event"] == "cycle_started" and event["position"] == ORIGIN
    )
    reporter = next(record for record in world.nodes[ORIGIN].records if record is not None)
    assert world.record_values(reporter) == {"work": (cycle["cost"],)}
    field_cycle = next(
        event for event in events if event["event"] == "spatial_cycle" and event["position"] == ORIGIN
    )
    assert cycle["cost"] > field_cycle["cost"] > 0
