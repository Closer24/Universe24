"""Directional computation delay: departures are priced by the load travelling along or against them.

With `delay_direction`, the computation field no longer delays the whole cycle;
each departure through a port waits for k computed from the load delivered
through the matching channel: the field travelling in the same direction
("along") or towards the departure ("against"). A probe moving away from the
emitting mass is therefore slowed under "along" and free under "against",
and a probe moving towards it the reverse, while a resting body never moves.
"""

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_initial_state

SOURCE = 20


def document(start_x, momentum, direction, *, budget=100, emission=24000, ticks=60, extra=None):
    doc = {
        "schema_version": 1,
        "model_id": "directional-delay-contract-v1",
        "boundary": "open",
        "shape": [41, 5, 5],
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": budget,
        "ticks": ticks,
        "computation_field": "computation",
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "mass", "components": 1, "units": "unit", "signed": False, "conserved": True},
            {
                "name": "momentum",
                "components": 3,
                "units": "c/120",
                "signed": True,
                "conserved": False,
                "scale": 120,
            },
            {
                "name": "computation",
                "components": 1,
                "units": "load unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "mass body",
                "fields": ["mass"],
                "defaults": {"mass": 1},
                "transport": {"mode": "hold"},
            },
            {
                "name": "probe",
                "fields": ["mass", "momentum"],
                "defaults": {"mass": 1, "momentum": momentum},
                "transport": {
                    "mode": "move",
                    "direction_field": "momentum",
                    "rate": {"op": "sum", "args": [{"op": "abs", "args": [{"field": "momentum"}]}]},
                    "rate_denominator": 120,
                },
            },
        ],
        "spatial_fields": [{"field": "computation", "baseline": 0, "transport": "outward"}],
        "emissions": [
            {
                "type": "mass body",
                "field": "computation",
                "amount": emission,
                "denominator": 1,
                "source": True,
            }
        ],
        "seeds": [
            {"position": [SOURCE, 2, 2], "type": "mass body"},
            {"position": [start_x, 2, 2], "type": "probe"},
        ],
    }
    if direction is not None:
        doc["delay_direction"] = direction
    doc.update(extra or {})
    return doc


def hop_ticks(doc):
    events = []
    world = Simulation(parse_initial_state(doc), observer=events.append)
    for _ in range(doc["ticks"]):
        world.step()
    ticks = [e["tick"] for e in events if e.get("event") == "sent" and e.get("disturbance") == "probe"]
    arrivals = [
        e["arrival_tick"] - e["tick"]
        for e in events
        if e.get("event") == "sent" and e.get("disturbance") == "probe"
    ]
    return ticks, arrivals, world


def gaps(ticks):
    return [b - a for a, b in zip(ticks, ticks[1:], strict=False)]


AWAY, TOWARD = (22, [60, 0, 0]), (30, [-60, 0, 0])


def test_along_delays_the_climb_out_and_leaves_the_fall_in_free():
    away, _, _ = hop_ticks(document(*AWAY, "along"))
    toward, _, _ = hop_ticks(document(*TOWARD, "along"))
    assert max(gaps(away)) > 2
    assert gaps(toward)[:11] == [2] * 11


def test_against_delays_the_approach_and_leaves_the_climb_out_free():
    away, _, _ = hop_ticks(document(*AWAY, "against"))
    toward, _, _ = hop_ticks(document(*TOWARD, "against"))
    assert gaps(away)[:11] == [2] * 11
    assert max(gaps(toward)) > 2


def test_isotropic_delay_slows_both_directions():
    away, _, _ = hop_ticks(document(*AWAY, None))
    toward, _, _ = hop_ticks(document(*TOWARD, None))
    assert max(gaps(away)) > 2 and max(gaps(toward)) > 2


@pytest.mark.parametrize("direction", [None, "along", "against"])
def test_extra_delay_is_reported_on_the_departure_and_a_resting_body_stays(direction):
    ticks, arrivals, world = hop_ticks(document(*TOWARD, direction))
    assert all(a >= 1 for a in arrivals)
    if direction is not None:
        assert max(arrivals) > 1 or max(gaps(ticks)) > 2
    doc = document(21, [0, 0, 0], direction, ticks=30)
    _, _, world = hop_ticks(doc)
    assert any(
        r is not None and world.record_values(r).get("momentum") == (0, 0, 0)
        for r in world.nodes[(21, 2, 2)].records
    )


RAY_FIELD = {
    "field": "computation",
    "baseline": 0,
    "transport": "ray",
    "headings": [[24, 0, 0], [-24, 0, 0], [0, 24, 0], [0, -24, 0], [0, 0, 24], [0, 0, -24]],
    "rays_per_tick": 6,
    "ray_slots": 64,
}


def ray_document(start_x, momentum, direction):
    doc = document(start_x, momentum, direction)
    doc["spatial_fields"] = [RAY_FIELD]
    return doc


def test_a_ray_field_prices_departures_by_delivered_ray_arrivals():
    """A ray field may be the computation field: its arrivals per travel port are the load."""
    along, _, _ = hop_ticks(ray_document(*AWAY, "along"))
    against, _, _ = hop_ticks(ray_document(*AWAY, "against"))
    isotropic, _, world = hop_ticks(ray_document(*AWAY, None))
    # The +x ray travels with the departing probe: "along" delays it, "against" reads the
    # -x channel, which no ray reaches beyond the source, and leaves it free.
    assert max(gaps(along)) > 2
    assert gaps(against)[:11] == [2] * 11
    assert max(gaps(isotropic)) > 2
    assert world.spatial_values((22, 2, 2))["computation"]["ray_count"] >= 0


@pytest.mark.parametrize(
    ("extra", "message"),
    [
        ({"delay_direction": "sideways"}, "along or against"),
        ({"delay_direction": "along", "computation_field": None}, "requires computation_field"),
        ({"delay_direction": "along", "spatial_computation_delay": True}, "default clock"),
    ],
)
def test_rejected_delay_direction_settings(extra, message):
    doc = document(*TOWARD, None, extra={k: v for k, v in extra.items() if v is not None})
    for key, value in extra.items():
        if value is None:
            doc.pop(key, None)
    with pytest.raises(ValueError, match=message):
        parse_initial_state(doc)
