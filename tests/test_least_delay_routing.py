"""Least-delay routing: the cheapest eligible lane goes first; directional ratios stay exact.

With `least_delay_routing`, a carrier's balanced router and an outward field's
carried split both read the computation load pricing each port and take the
cheapest eligible option first. Every lane still receives exactly its weight
per reduced cycle, so only the order within a cycle changes; the deflection is
therefore bounded by one cycle and a straight mover with a single lane is
never turned.
"""

import pytest

from event_universe.core.disturbance_state import (
    OPERATIONS,
    CostMeter,
    FieldDefinition,
    OperationCosts,
    pack,
)
from event_universe.core.spatial_state import SpatialFieldDefinition, SpatialState
from event_universe.fields.routing import balanced_port
from event_universe.fields.spatial import split_outward_carried
from event_universe.initialization import parse_initial_state

METER = CostMeter(OperationCosts((1,) * len(OPERATIONS)))


def cycle(weights, loads, steps):
    counts, previous, chosen = (0,) * 6, (0,) * 6, []
    for _ in range(steps):
        port, counts, previous = balanced_port(weights, counts, previous, METER, loads=loads)
        chosen.append(port)
    return chosen


def test_cheapest_eligible_lane_goes_first_and_the_cycle_ratio_is_exact():
    weights = (1, 0, 1, 0, 0, 0)
    assert cycle(weights, None, 4) == [0, 2, 0, 2]
    assert cycle(weights, (5, 0, 1, 0, 0, 0), 4) == [2, 0, 2, 0]
    assert cycle(weights, (1, 0, 5, 0, 0, 0), 4) == [0, 2, 0, 2]


def test_ratios_survive_any_load_pattern():
    weights = (2, 0, 1, 0, 0, 0)
    for loads in ((9, 0, 0, 0, 0, 0), (0, 0, 9, 0, 0, 0), (3, 0, 3, 0, 0, 0)):
        chosen = cycle(weights, loads, 12)
        assert chosen.count(0) == 8 and chosen.count(2) == 4
        assert all(chosen[i : i + 3].count(0) == 2 for i in range(0, 12, 3))


def test_a_single_lane_is_never_redirected():
    assert cycle((0, 0, 3, 0, 0, 0), (0, 0, 99, 0, 0, 0), 3) == [2, 2, 2]


def first_port(outgoing):
    return next(port for port, bundle in enumerate(outgoing) if bundle[0][0] != pack((0,))[0])


def test_carried_split_prefers_the_least_loaded_axis_for_indivisible_units():
    field = FieldDefinition("radiation", 1, "unit", False, True, extensive=True)
    definition = SpatialFieldDefinition(field=0, baseline=pack((0,)))
    zero = pack((0,))
    populations = (pack((1,)),) + (zero,) * 7  # one unit in octant +++
    state = SpatialState(populations, (zero,) * 8, (zero,) * 6)
    unloaded, _, _ = split_outward_carried(state, definition, field, CostMeter(OperationCosts((1,) * 9)))
    loaded, _, _ = split_outward_carried(
        state, definition, field, CostMeter(OperationCosts((1,) * 9)), port_loads=(9, 0, 9, 0, 0, 0)
    )
    assert first_port(unloaded) == 0
    assert first_port(loaded) == 4


def base_document():
    return {
        "schema_version": 1,
        "model_id": "least-delay-contract-v1",
        "shape": [9, 5, 5],
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100,
        "ticks": 1,
        "computation_field": "computation",
        "delay_direction": "along",
        "least_delay_routing": True,
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
        ],
        "disturbance_types": [
            {
                "name": "mass body",
                "fields": ["mass"],
                "defaults": {"mass": 1},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [{"field": "computation", "baseline": 0, "transport": "outward"}],
        "emissions": [
            {"type": "mass body", "field": "computation", "amount": 10, "denominator": 1, "source": True}
        ],
        "seeds": [{"position": [4, 2, 2], "type": "mass body"}],
    }


def test_least_delay_requires_a_delay_direction_and_is_boolean():
    assert parse_initial_state(base_document()).least_delay_routing is True
    doc = base_document()
    doc.pop("delay_direction")
    with pytest.raises(ValueError, match="requires delay_direction"):
        parse_initial_state(doc)
    doc = base_document()
    doc["least_delay_routing"] = "yes"
    with pytest.raises(ValueError, match="boolean"):
        parse_initial_state(doc)
