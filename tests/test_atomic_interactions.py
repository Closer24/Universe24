"""Atomic transactions and an independently checked classical collision example."""

import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.reference_api import ReferenceSimulation as Simulation
from event_universe.reference_api import parse_reference_state as parse_initial_state

from .test_disturbance_engine import document, field, kind

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/04-unequal-mass-collision.json"


def collision():
    return json.loads(EXAMPLE.read_text())


def owned(world):
    records = [r for cell in world.cells.values() for r in cell.records if r is not None]
    records += [p.record for packets in world.links.values() for p in packets if p is not None]
    return {world.initial.disturbances[r.type_index].name: world.record_values(r) for r in records}


def test_unequal_mass_collision_reverses_both_bodies_and_preserves_physical_balances():
    events = []
    world = Simulation(parse_initial_state(collision()), observer=events.append)
    contact_seen = separating_seen = False
    for _ in range(360):
        world.step()
        values = owned(world)
        assert len(values) == 2
        assert world.totals() == {"mass": (5,), "momentum": (5, 0, 0)}
        assert world.source_totals() == {"mass": (0,), "momentum": (0, 0, 0)}
        # Independent rational diagnostic, never passed to the integer core.
        energy = sum(
            Fraction(sum(p * p for p in v["momentum"]), 2 * v["mass"][0]) for v in values.values()
        )
        assert energy == Fraction(35, 2)
        if world.tick == 120:
            assert len([r for r in world.cells[(7, 7, 7)].records if r is not None]) == 2
            assert values["Light body"]["momentum"] == (8, 0, 0)
            contact_seen = True
        if 121 <= world.tick < 160:
            assert values["Light body"]["momentum"] == (-4, 0, 0)
            assert values["Heavy body"]["momentum"] == (9, 0, 0)
            separating_seen = True  # No repeated reversal while still co-resident.
    assert contact_seen and separating_seen
    for position, expected in [((3, 7, 7), (-4, 0, 0)), ((13, 7, 7), (9, 0, 0))]:
        record = next(r for r in world.cells[position].records if r is not None)
        assert world.record_values(record)["momentum"] == expected
    for event in events:
        if event["event"] == "sent":
            assert event["arrival_tick"] == event["tick"] + 1
            assert 0 <= event["port"] < 6


def multifield():
    raw = document(
        [
            kind("first", values={"a": 4, "b": 0, "vector": [2, 0, 0]}),
            kind("second", values={"a": 2, "b": 0, "vector": [-2, 0, 0]}),
        ],
        [((2, 2, 2), "first"), ((2, 2, 2), "second")],
        fields=[
            field("a", conserved=False, signed=False),
            field("b", conserved=False, signed=False),
            field("vector", 3),
        ],
    )
    raw["interactions"] = [
        {
            "name": "conversion_and_rotation",
            "left_type": "first",
            "right_type": "second",
            "assignments": [
                {"side": "left", "field": "a", "expression": {"field": "a", "side": "right"}},
                {"side": "left", "field": "b", "expression": {"op": "sub", "args": [{"field": "a"}, 2]}},
                {"side": "right", "field": "a", "expression": 0},
            ],
            "invariants": [
                {
                    "name": "weighted_inventory",
                    "expression": {
                        "op": "add",
                        "args": [
                            {"op": "add", "args": [{"field": "a"}, {"field": "a", "side": "right"}]},
                            {
                                "op": "mul",
                                "args": [
                                    2,
                                    {
                                        "op": "add",
                                        "args": [{"field": "b"}, {"field": "b", "side": "right"}],
                                    },
                                ],
                            },
                        ],
                    },
                }
            ],
        }
    ]
    # Swapping and conversion together: (aL,aR,bL)=(4,2,0)->(2,0,2).
    for side in ("left", "right"):
        raw["interactions"][0]["assignments"].append(
            {
                "side": side,
                "field": "vector",
                "expression": {
                    "op": "transform",
                    "args": [{"field": "vector", "side": side}],
                    "matrix": [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
                },
            }
        )
    return raw


def test_multifield_conversion_and_vector_rotation_read_one_frozen_pair():
    world = Simulation(parse_initial_state(multifield()))
    world.step()
    assert owned(world) == {
        "first": {"a": (2,), "b": (2,), "vector": (0, 2, 0)},
        "second": {"a": (0,), "b": (0,), "vector": (0, -2, 0)},
    }


@pytest.mark.parametrize("failure", ["conserved", "invariant", "negative", "overflow", "fraction"])
def test_rejected_transaction_changes_no_record_or_pending_state(failure):
    raw = multifield()
    assignments = raw["interactions"][0]["assignments"]
    if failure == "conserved":
        assignments[-1]["expression"] = [0, 0, 0]
    elif failure == "invariant":
        assignments[1]["expression"] = 1
    elif failure == "negative":
        assignments[0]["expression"] = -1
    elif failure == "overflow":
        assignments[0]["expression"] = {"op": "add", "args": [MAX_VALUE, 1]}
    else:
        assignments[0]["expression"] = {"op": "exact_div", "args": [1, 2]}
    world = Simulation(parse_initial_state(raw))
    snapshot = world.snapshot()
    with pytest.raises((ValueError, OverflowError)):
        world.step()
    assert world.snapshot() == snapshot
    assert world.faulted
    assert all(cell.pending is None for cell in world.cells.values())


def test_conserved_pair_total_may_exceed_individual_payload_bound():
    raw = multifield()
    for definition in raw["disturbance_types"]:
        definition["defaults"]["vector"] = [MAX_VALUE, 0, 0]
    for assignment in raw["interactions"][0]["assignments"][-2:]:
        assignment["expression"]["matrix"] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert world.totals()["vector"] == (2 * MAX_VALUE, 0, 0)


@pytest.mark.parametrize(
    "malformation", ["duplicate", "matrix", "activation", "missing_invariants", "unknown_target"]
)
def test_invalid_interaction_schema_is_rejected(malformation):
    raw = multifield()
    rule = raw["interactions"][0]
    if malformation == "duplicate":
        rule["assignments"].append(deepcopy(rule["assignments"][0]))
    elif malformation == "matrix":
        rule["assignments"][-1]["expression"]["matrix"] = [[1, 0], [0, 1]]
    elif malformation == "activation":
        rule["when"] = [1, 0, 0]
    elif malformation == "missing_invariants":
        rule["invariants"] = []
    else:
        rule["assignments"][0]["field"] = "undeclared"
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_field_renaming_and_world_extension_do_not_change_local_collision():
    raw = collision()
    renamed = json.loads(json.dumps(raw).replace('"mass"', '"weight"').replace('"momentum"', '"motion"'))
    renamed["shape"] = [25, 25, 25]
    world = Simulation(parse_initial_state(renamed))
    for _ in range(121):
        world.step()
    assert owned(world)["Light body"]["motion"] == (-4, 0, 0)
    assert owned(world)["Heavy body"]["motion"] == (9, 0, 0)
