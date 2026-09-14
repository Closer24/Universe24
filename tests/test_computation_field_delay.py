"""A configured computation field adds its local value to the carrier cycle cost (Highlights 4.4).

The field is an ordinary conserved outward scalar field: its total stays
constant while it dilutes with distance. Where its local value is large the
cycle cost C exceeds the normal budget B and k = ceil(C / B) delays every
local cycle, so a held clock near the emitting mass completes fewer cycles.
No mass, distance or force enters the engine; only the field's local value.
"""

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_initial_state

SOURCE = 6
TICKS = 40


def document(*, budget, emission, computation_field="computation", distances=(1, 2, 3, 4, 8, 30)):
    doc = {
        "schema_version": 1,
        "model_id": "computation-field-delay-contract-v1",
        "boundary": "open",
        "shape": [41, 5, 5],
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": budget,
        "ticks": TICKS,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "mass", "components": 1, "units": "unit", "signed": False, "conserved": True},
            {
                "name": "clock",
                "components": 1,
                "units": "cycles",
                "signed": False,
                "conserved": False,
                "extensive": False,
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
                "name": "clock",
                "fields": ["mass", "clock"],
                "defaults": {"mass": 1, "clock": 0},
                "updates": [
                    {"field": "clock", "expression": {"op": "add", "args": [{"field": "clock"}, 1]}}
                ],
                "transport": {"mode": "hold"},
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
        "seeds": [{"position": [SOURCE, 2, 2], "type": "mass body"}]
        + [{"position": [SOURCE + d, 2, 2], "type": "clock"} for d in distances],
    }
    if computation_field is not None:
        doc["computation_field"] = computation_field
    return doc


def clocks(doc):
    world = Simulation(parse_initial_state(doc))
    for _ in range(doc["ticks"]):
        world.step()
    result = {}
    for position, node in world.nodes.items():
        for record in node.records:
            if record is not None and "clock" in world.record_values(record):
                result[position[0] - SOURCE] = world.record_values(record)["clock"][0]
    emitted = world.source_totals()["computation"][0]
    escaped = world.escaped_totals()["computation"][0]
    assert emitted == doc["emissions"][0]["amount"] * TICKS
    assert world.totals()["computation"] == (emitted - escaped,)
    return result


def test_clocks_slow_near_the_mass_and_recover_with_distance():
    near = clocks(document(budget=100, emission=24000))
    assert near[1] < near[2] < near[3] < near[4] < near[30] == TICKS
    assert near[8] == TICKS


def test_a_large_budget_removes_the_delay_without_changing_the_field():
    assert all(value == TICKS for value in clocks(document(budget=1_000_000, emission=24000)).values())


def test_without_a_computation_field_the_field_costs_only_its_operations():
    unpriced = clocks(document(budget=100, emission=24000, computation_field=None))
    assert all(value == TICKS for value in unpriced.values())


@pytest.mark.parametrize(
    ("patch", "message"),
    [
        ({"computation_field": "mass"}, "outward spatial field"),
        ({"computation_field": "nothing"}, "unknown name"),
    ],
)
def test_rejected_computation_field_selections(patch, message):
    doc = document(budget=100, emission=10)
    doc.update(patch)
    with pytest.raises(ValueError, match=message):
        parse_initial_state(doc)


def light_arrivals(mass_emission, observer=(22, 12, 1), budget=200, ticks=40):
    doc = {
        "schema_version": 1,
        "model_id": "computation-field-shared-clock-light-v1",
        "boundary": "open",
        "shape": [29, 25, 3],
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": budget,
        "ticks": ticks,
        "spatial_computation_delay": True,
        "computation_field": "computation",
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "mass", "components": 1, "units": "unit", "signed": False, "conserved": True},
            {
                "name": "computation",
                "components": 1,
                "units": "load unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "light",
                "components": 1,
                "units": "unit",
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
            {"name": "lamp", "fields": ["mass"], "defaults": {"mass": 1}, "transport": {"mode": "hold"}},
        ],
        "spatial_fields": [
            {"field": "computation", "baseline": 0, "transport": "outward"},
            {"field": "light", "baseline": 0, "transport": "outward"},
        ],
        "emissions": [
            {
                "type": "mass body",
                "field": "computation",
                "amount": mass_emission,
                "denominator": 1,
                "source": True,
            },
            {"type": "lamp", "field": "light", "amount": 2400, "denominator": 1, "source": True},
        ],
        "seeds": [
            {"position": [14, 12, 1], "type": "mass body"},
            {"position": [6, 12, 1], "type": "lamp"},
        ],
    }
    events = []
    world = Simulation(parse_initial_state(doc), observer=events.append)
    for _ in range(ticks):
        world.step()
    return sorted(
        e["tick"]
        for e in events
        if e.get("event") == "spatial_received"
        and tuple(e["position"]) == observer
        and any(f.get("light", (0,))[0] for f in e.get("received_fields", []))
    )


def test_under_the_shared_clock_the_load_delays_light_behind_the_mass():
    free = light_arrivals(0)
    assert free and free[0] == 16
    behind = light_arrivals(24000)
    assert not behind or behind[0] > 16
    beside = light_arrivals(24000, observer=(22, 18, 1))
    assert beside and beside[0] == light_arrivals(0, observer=(22, 18, 1))[0]


def test_signed_or_nonconserved_field_is_rejected():
    doc = document(budget=100, emission=10)
    doc["fields"][2]["conserved"] = False
    with pytest.raises(ValueError, match="conserved scalar"):
        parse_initial_state(doc)
