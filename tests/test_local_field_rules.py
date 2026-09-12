"""Independent local component, port ownership and causal transport contracts."""

import json
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE, OPERATIONS
from event_universe.initialization import parse_initial_state

ORIGIN = (2, 2, 2)
PORTS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
EXAMPLE = Path(__file__).resolve().parents[1] / "examples/local_field_rules.json"


def field(name, components=1, *, conserved=False):
    return {
        "name": name,
        "components": components,
        "units": "configured unit",
        "signed": True,
        "conserved": conserved,
    }


def local(name):
    return {"field": name, "side": "right"}


def operation(name, *args):
    return {"op": name, "args": list(args)}


def seed(name, value, position=ORIGIN):
    zero = [0, 0, 0] if isinstance(value, list) else 0
    return {"position": list(position), "field": name, "populations": [value] + [zero] * 7}


def document(fields, seeds=()):
    return {
        "schema_version": 1,
        "model_id": "configured-local-field-contract-v1",
        "shape": [5, 5, 5],
        "slots_per_cell": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": 4,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": fields,
        "disturbance_types": [
            {"name": "held", "fields": [f["name"] for f in fields], "transport": {"mode": "hold"}}
        ],
        "seeds": [],
        "spatial_fields": [
            {
                "field": f["name"],
                "baseline": [0, 0, 0] if f["components"] == 3 else 0,
                "transport": "local",
            }
            for f in fields
        ],
        "spatial_seeds": list(seeds),
    }


def value(world, name, position=ORIGIN):
    return world.spatial_values(position)[name]["value"]


def invariant(name, expression):
    return {"name": name, "expression": expression}


def test_example_rotates_two_vectors_from_one_snapshot_and_coexists_with_outward_field():
    raw = json.loads(EXAMPLE.read_text())
    origin = tuple(raw["spatial_seeds"][0]["position"])
    raw["fields"].append(field("outward_inventory", conserved=True))
    raw["spatial_fields"].append({"field": "outward_inventory", "baseline": 0, "transport": "outward"})
    raw["spatial_seeds"].append(
        {"position": list(origin), "field": "outward_inventory", "populations": [27] * 8}
    )
    world = Simulation(parse_initial_state(raw))
    cycle = [
        ((0, 0, 0), (-3, -4, 0)),
        ((-3, -4, 0), (0, 0, 0)),
        ((0, 0, 0), (3, 4, 0)),
        ((3, 4, 0), (0, 0, 0)),
    ]
    for tick, expected in enumerate(cycle, 1):
        world.step()
        observed = (value(world, "a", origin), value(world, "b", origin))
        assert observed == expected
        assert sum(component * component for vector in observed for component in vector) == 25
        assert world.totals()["outward_inventory"] == (216,)
        accounting = world.spatial_accounting()
        assert all(item["balanced"] for item in accounting.values())
        assert accounting["a"]["sources"] == accounting["b"]["sources"] == (0, 0, 0)
        assert accounting["a"]["transformations"] == tuple(
            current - initial for current, initial in zip(observed[0], (3, 4, 0), strict=True)
        )
        assert accounting["b"]["transformations"] == observed[1]
        if tick == 1:
            for direction in PORTS:
                neighbor = tuple(p + d for p, d in zip(origin, direction, strict=True))
                assert value(world, "outward_inventory", neighbor) == (36,)


def test_retained_stock_and_six_outputs_own_inventory_once_and_wait_a_full_link():
    raw = document([field("inventory", conserved=True)], [seed("inventory", 84)])
    raw["link_ticks"] = 2
    portion = operation("exact_div", local("inventory"), 7)
    assignments = [{"field": "inventory", "expression": portion}]
    assignments.extend({"field": "inventory", "port": p, "expression": portion} for p in range(6))
    total = local("inventory")
    for port in range(6):
        total = operation("add", total, {"outgoing": "inventory", "port": port})
    raw["field_rules"] = [
        {
            "name": "seven_equal_owners",
            "assignments": assignments,
            "invariants": [invariant("stock", total)],
        }
    ]
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()
    assert value(world, "inventory") == (12,)
    assert world.totals()["inventory"] == (84,)
    for direction in PORTS:
        neighbor = tuple(p + d for p, d in zip(ORIGIN, direction, strict=True))
        assert value(world, "inventory", neighbor) == (0,)
    world.step()
    assert value(world, "inventory") == (12,)
    for port, direction in enumerate(PORTS):
        neighbor = tuple(p + d for p, d in zip(ORIGIN, direction, strict=True))
        state = world.spatial_values(neighbor)["inventory"]
        assert state["value"] == (12,)
        assert state["directions"][port] == (12,)
    sent = [event for event in events if event["event"] == "spatial_sent"]
    assert len(sent) == 6 and {event["port"] for event in sent} == set(range(6))
    assert all(event["arrival_tick"] - event["tick"] == 2 for event in sent)
    assert world.totals()["inventory"] == (84,)
    assert world.source_totals()["inventory"] == (0,)


def test_counterflow_keeps_signed_vector_channels_separate_from_owned_stock():
    raw = document(
        [field("a", 3, conserved=True), field("probe", 3)],
        [seed("a", [0, 5, 0], (1, 2, 2)), seed("a", [0, -5, 0], (3, 2, 2))],
    )
    component_y = {"op": "component", "args": [local("a")], "index": 1}
    rules = []
    for port, sign in ((0, 1), (1, -1)):
        rules.append(
            {
                "name": f"route_{port}",
                "when": operation("gt", operation("mul", sign, component_y), 0),
                "assignments": [
                    {"field": "a", "expression": [0, 0, 0]},
                    {"field": "a", "port": port, "expression": local("a")},
                ],
                "invariants": [
                    invariant("inventory", operation("add", local("a"), {"outgoing": "a", "port": port}))
                ],
            }
        )
    incoming_y = [
        {"op": "component", "args": [{"received": "a", "port": port}], "index": 1} for port in (0, 1)
    ]
    rules.append(
        {
            "name": "read_directional_probe",
            "assignments": [
                {
                    "field": "probe",
                    "expression": operation("cross", [0, 0, 1], operation("vector", *incoming_y, 0)),
                }
            ],
            "invariants": [invariant("unchanged_stock", local("a"))],
        }
    )
    raw["field_rules"] = rules
    world = Simulation(parse_initial_state(raw))
    world.step()
    state = world.spatial_values(ORIGIN)["a"]
    assert state["value"] == (0, 0, 0)
    assert state["directions"][:2] == ((0, 5, 0), (0, -5, 0))
    assert value(world, "probe") == (0, 0, 0)
    world.step()
    assert value(world, "probe") == (5, 5, 0)
    assert world.totals()["a"] == (0, 0, 0)
    assert world.spatial_accounting()["a"]["balanced"]


@pytest.mark.parametrize("failure", ["invariant", "conserved", "overflow"])
def test_rejected_field_rule_preserves_all_local_owners(failure):
    raw = document(
        [field("a", 3), field("stock", conserved=True)], [seed("a", [3, 4, 0]), seed("stock", 7)]
    )
    expression = operation("neg", local("a"))
    invariant_expression = operation("dot", local("a"), local("a"))
    assignments = [{"field": "a", "expression": expression}]
    if failure == "invariant":
        assignments[0]["expression"] = [0, 0, 0]
    elif failure == "conserved":
        assignments.append({"field": "stock", "expression": 8})
    else:
        assignments[0]["expression"] = operation(
            "mul", MAX_VALUE, operation("mul", MAX_VALUE, operation("mul", MAX_VALUE, local("a")))
        )
    raw["field_rules"] = [
        {
            "name": "rejected",
            "assignments": assignments,
            "invariants": [invariant("norm", invariant_expression)],
        }
    ]
    world = Simulation(parse_initial_state(raw))
    before = world.snapshot()
    with pytest.raises((ValueError, OverflowError)):
        world.step()
    assert world.faulted
    assert world.snapshot() == before
    assert world.source_totals()["stock"] == (0,)


@pytest.mark.parametrize(
    "malformation", ["port", "group", "shape", "assignment_limit", "received_invariant"]
)
def test_local_schema_rejects_invalid_ports_groups_shapes_and_unbounded_rules(malformation):
    raw = json.loads(EXAMPLE.read_text())
    rule = raw["field_rules"][0]
    if malformation == "port":
        rule["assignments"][0]["port"] = 6
    elif malformation == "group":
        raw["field_groups"][0]["fields"] = ["a", "missing"]
    elif malformation == "shape":
        rule["assignments"][0]["expression"] = operation("vector", 1, 2)
    elif malformation == "assignment_limit":
        rule["assignments"] = [deepcopy(rule["assignments"][0]) for _ in range(33)]
    else:
        rule["invariants"][0]["expression"] = {"received": "a", "port": 0}
    with pytest.raises(ValueError):
        parse_initial_state(raw)
