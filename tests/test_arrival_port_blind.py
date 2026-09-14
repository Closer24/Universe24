"""Arrival-port-blind sampling: inertial motion ignores own field, corner coarrival does not.

A carrier that arrived in this interval ignores, for this one sample, what was
delivered through the travel port it came in on. On a straight path the packet
emitted in the departure interval always shares that port, at any speed. At a
corner at maximum speed an own packet reaches the same node along the
alternate shortest path through a side port and still acts. Held carriers
never arrive, so external sources act in full.
"""

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_initial_state

CENTER = 3
STRAIGHT, ZIGZAG = [1, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0]


def document(*, seeds, ticks, hold=False, weights=None, rate=None, flag=True, extra=None):
    if hold:
        transport = {"mode": "hold"}
    elif weights is not None:
        transport = {
            "mode": "move",
            "weights": weights,
            "routing": "balanced",
            "rate": rate if rate is not None else 1,
            "rate_denominator": 1 if rate is None else 120,
        }
    else:
        transport = {
            "mode": "move",
            "direction_field": "momentum",
            "rate": {
                "op": "min",
                "args": [
                    120,
                    {
                        "op": "exact_div",
                        "args": [
                            {"op": "sum", "args": [{"op": "abs", "args": [{"field": "momentum"}]}]},
                            {"field": "mass"},
                        ],
                    },
                ],
            },
            "rate_denominator": 120,
        }
    doc = {
        "schema_version": 1,
        "model_id": "arrival-port-blind-contract-v1",
        "boundary": "open",
        "shape": [25, 11, 7],
        "slots_per_node": 4,
        "link_ticks": 1,
        "normal_budget": 1_000_000,
        "ticks": ticks,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "mass", "components": 1, "units": "unit", "signed": False, "conserved": True},
            {"name": "charge", "components": 1, "units": "unit", "signed": True, "conserved": True},
            {
                "name": "momentum",
                "components": 3,
                "units": "unit",
                "signed": True,
                "conserved": True,
                "extensive": True,
                "scale": 120,
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
                "fields": ["mass", "charge", "momentum"],
                "defaults": {"mass": 1, "charge": 1, "momentum": [0, 0, 0]},
                "transport": transport,
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
                "name": "charge_times_flux",
                "type": "body",
                "field": "momentum",
                "mode": "exchange",
                "amount": {
                    "op": "neg",
                    "args": [{"op": "mul", "args": [{"field": "charge"}, {"flux": "potential"}]}],
                },
                "denominator": 10,
            }
        ],
        "seeds": [{"position": list(p), "type": "body", "values": v} for p, v in seeds],
    }
    if flag:
        doc["arrival_port_blind"] = True
    doc.update(extra or {})
    return doc


def run(doc):
    events = []
    world = Simulation(parse_initial_state(doc), observer=events.append)
    for _ in range(doc["ticks"]):
        world.step()
    impulses = [e for e in events if e.get("event") == "spatial_coupled" and e.get("reaction")]
    bodies = sorted(
        (position, world.record_values(record)["charge"][0], world.record_values(record)["momentum"])
        for position, node in world.nodes.items()
        for record in node.records
        if record is not None
    )
    return impulses, bodies, world


@pytest.mark.parametrize(
    ("position", "momentum", "ticks"),
    [
        ((4, 5, CENTER), (15, 0, 0), 30),
        ((4, 5, CENTER), (120, 0, 0), 18),
        ((20, 5, CENTER), (-30, 0, 0), 30),
    ],
)
def test_straight_isolated_emitter_keeps_its_momentum_at_any_speed(position, momentum, ticks):
    impulses, bodies, world = run(
        document(seeds=[(position, {"momentum": list(momentum)})], ticks=ticks)
    )
    assert impulses == []
    assert bodies == [(bodies[0][0], 1, momentum)]
    assert world.totals()["momentum"] == momentum


def test_default_clock_still_documents_the_straight_self_push():
    impulses, _, _ = run(
        document(seeds=[((4, 5, CENTER), {"momentum": [15, 0, 0]})], ticks=12, flag=False)
    )
    assert impulses


def test_zigzag_at_maximum_speed_meets_its_own_field_through_a_side_port():
    impulses, bodies, _ = run(
        document(seeds=[((2, 1, CENTER), {"momentum": [60, 60, 0]})], ticks=16, weights=ZIGZAG)
    )
    assert impulses
    ((_, _, final),) = bodies
    assert final != (60, 60, 0)


def test_zigzag_below_maximum_speed_never_meets_its_own_field():
    impulses, bodies, _ = run(
        document(seeds=[((2, 1, CENTER), {"momentum": [60, 60, 0]})], ticks=40, weights=ZIGZAG, rate=30)
    )
    assert impulses == []
    assert bodies == [(bodies[0][0], 1, (60, 60, 0))]


@pytest.mark.parametrize(("right_charge", "sign"), [(1, 1), (-1, -1)])
def test_held_pair_keeps_the_full_configured_sign_rule(right_charge, sign):
    left, right = (9, 5, CENTER), (12, 5, CENTER)
    _, bodies, _ = run(
        document(seeds=[(left, {"charge": 1}), (right, {"charge": right_charge})], ticks=20, hold=True)
    )
    found = {p: m for p, _, m in bodies}
    assert found[left][0] * sign < 0 and found[right][0] * sign > 0


def test_overtaking_external_field_still_pushes_a_receding_carrier():
    # A held source behind a slowly receding like charge: repulsion keeps accelerating it.
    doc = document(
        seeds=[((6, 5, CENTER), {"momentum": [0, 0, 0]}), ((9, 5, CENTER), {"momentum": [12, 0, 0]})],
        ticks=40,
    )
    doc["disturbance_types"].append(
        {
            "name": "anchor",
            "fields": ["mass", "charge", "momentum"],
            "defaults": {"mass": 1, "charge": 1, "momentum": [0, 0, 0]},
            "transport": {"mode": "hold"},
        }
    )
    doc["emissions"][0]["type"] = "body"
    doc["emissions"].append({**doc["emissions"][0], "type": "anchor"})
    doc["seeds"][0]["type"] = "anchor"
    impulses, bodies, _ = run(doc)
    moving = next(m for p, _, m in bodies if p != (6, 5, CENTER))
    assert moving[0] > 12
    assert impulses


@pytest.mark.parametrize(
    ("extra", "message"),
    [
        ({"field_phase_first": True}, "alternative self-field policies"),
        ({"spatial_computation_delay": True}, "spatial_computation_delay"),
        ({"arrival_port_blind": 1}, "boolean"),
    ],
)
def test_rejected_combinations(extra, message):
    doc = document(seeds=[((4, 5, CENTER), {})], ticks=1)
    doc.update(extra)
    with pytest.raises(ValueError, match=message):
        parse_initial_state(doc)
