"""Reject invalid observable seed totals before a simulation or output is created."""

import pytest

from event_universe.core.disturbance_state import MAX_VALUE, OPERATIONS
from event_universe.initialization import parse_initial_state


def initialization(baseline, populations):
    return {
        "schema_version": 1,
        "model_id": "spatial-seed-boundary-v1",
        "shape": [3, 3, 3],
        "slots_per_node": 1,
        "link_ticks": 1,
        "normal_budget": 1000,
        "ticks": 0,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "signal", "components": 1, "units": "unit", "signed": False, "conserved": True}
        ],
        "disturbance_types": [{"name": "held", "fields": ["signal"], "transport": {"mode": "hold"}}],
        "seeds": [],
        "spatial_fields": [{"field": "signal", "baseline": baseline, "transport": "outward"}],
        "spatial_seeds": [{"position": [1, 1, 1], "field": "signal", "populations": populations}],
    }


@pytest.mark.parametrize(
    ("baseline", "populations"),
    [(0, [MAX_VALUE] * 8), (1, [MAX_VALUE] + [0] * 7)],
)
def test_combined_spatial_seed_value_is_rejected_during_parsing(baseline, populations):
    with pytest.raises(ValueError, match="bound"):
        parse_initial_state(initialization(baseline, populations))


def test_baseline_and_seed_can_reach_the_exact_register_bound():
    initial = parse_initial_state(initialization(1, [MAX_VALUE - 1] + [0] * 7))
    assert len(initial.spatial_seeds) == 1
