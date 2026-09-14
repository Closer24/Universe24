"""Flux-driven rotation under the default clock: inertial motion is self-blind, turning is not.

docs/SPATIAL_COUPLINGS.md "Straight motion and self interaction" states the
restricted geometric guarantee: own straight-line flux is parallel to a
cardinal carrier vector and cannot turn it, while a turn admits alternate
shortest paths where own field coarrives. field_phase_first removes the
coarrival on every path. An external transverse source must still turn a
held carrier, so the law is not a force-off model.
"""

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_initial_state

STRAIGHT, ZIGZAG = [1, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0]


def document(*, seeds, ticks, hold=False, weights=STRAIGHT, field_phase_first=False):
    return {
        "schema_version": 1,
        "model_id": "flux-rotation-self-interaction-contract-v1",
        "boundary": "open",
        "shape": [15, 11, 5],
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": 1_000_000,
        "ticks": ticks,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "charge", "components": 1, "units": "unit", "signed": True, "conserved": True},
            {
                "name": "momentum",
                "components": 3,
                "units": "unit",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "potential",
                "components": 1,
                "units": "unit",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "body",
                "fields": ["charge", "momentum"],
                "defaults": {"charge": 1, "momentum": [0, 0, 0]},
                "transport": (
                    {"mode": "hold"}
                    if hold
                    else {
                        "mode": "move",
                        "weights": weights,
                        "routing": "balanced",
                        "rate": 1,
                        "rate_denominator": 1,
                    }
                ),
            }
        ],
        "spatial_fields": [
            {"field": "potential", "baseline": 0, "transport": "outward"},
            {"field": "momentum", "baseline": [0, 0, 0], "transport": "outward"},
        ],
        "emissions": [
            {
                "type": "body",
                "field": "potential",
                "amount": {"op": "mul", "args": [{"field": "charge"}, 540]},
                "denominator": 1,
                "source": True,
            }
        ],
        "spatial_couplings": [
            {
                "name": "flux_quarter_turns",
                "type": "body",
                "field": "momentum",
                "mode": "rotation",
                "rotation": {"op": "mul", "args": [{"field": "charge"}, {"flux": "potential"}]},
                "denominator": 200,
                "axis_order": [0, 1, 2],
            }
        ],
        "seeds": [{"position": list(p), "type": "body", "values": v} for p, v in seeds],
        **({"field_phase_first": True} if field_phase_first else {}),
    }


def run(doc):
    turns = []
    world = Simulation(parse_initial_state(doc), observer=lambda e: turns.append(e))
    for _ in range(doc["ticks"]):
        world.step()
    reactions = [e for e in turns if e.get("event") == "spatial_coupled" and e.get("reaction")]
    momenta = [
        world.record_values(record)["momentum"]
        for node in world.nodes.values()
        for record in node.records
        if record is not None
    ]
    return reactions, momenta


def test_straight_max_speed_emitter_is_not_turned_by_its_own_flux():
    reactions, momenta = run(document(seeds=[((1, 5, 2), {"momentum": [120, 0, 0]})], ticks=10))
    assert reactions == []
    assert momenta == [(120, 0, 0)]


def test_zigzag_max_speed_emitter_meets_its_own_field_at_corners_and_turns():
    reactions, momenta = run(
        document(seeds=[((1, 1, 2), {"momentum": [60, 60, 0]})], ticks=10, weights=ZIGZAG)
    )
    assert reactions
    (final,) = momenta
    assert final != (60, 60, 0)
    assert sum(v * v for v in final) == 7200


def test_field_phase_first_removes_the_corner_self_turn():
    reactions, momenta = run(
        document(
            seeds=[((1, 1, 2), {"momentum": [60, 60, 0]})],
            ticks=10,
            weights=ZIGZAG,
            field_phase_first=True,
        )
    )
    assert reactions == []
    assert momenta == [(60, 60, 0)]


def test_external_transverse_source_still_turns_a_held_carrier():
    reactions, momenta = run(
        document(
            seeds=[((7, 5, 2), {"momentum": [120, 0, 0]}), ((7, 6, 2), {"momentum": [0, 0, 0]})],
            ticks=8,
            hold=True,
        )
    )
    assert reactions
    assert all(sum(v * v for v in m) in (0, 14400) for m in momenta)
    assert (120, 0, 0) not in momenta or len(reactions) >= 4


@pytest.mark.parametrize("weights", [STRAIGHT, ZIGZAG])
def test_rotation_preserves_the_carrier_norm_exactly(weights):
    _, momenta = run(document(seeds=[((1, 1, 2), {"momentum": [60, 60, 0]})], ticks=10, weights=weights))
    assert [sum(v * v for v in m) for m in momenta] == [7200]
