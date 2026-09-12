"""Atomic pair transactions preserve spatial response, ownership and local timing."""

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import unpack
from event_universe.initialization import parse_initial_state

from .test_disturbance_engine import document, field, kind

ORIGIN = (2, 2, 2)
BEFORE = {"left": (5, 0, 0), "right": (-1, 0, 0)}
AFTER = {"left": (0, -1, 0), "right": (0, 5, 0)}


def combined(*, budget=100000, couple_price=1):
    left = kind("left", values={"p": [5, 0, 0], "work": 0})
    left["cost_field"] = "work"
    raw = document(
        [left, kind("right", values={"p": [-1, 0, 0]})],
        [(ORIGIN, "left"), (ORIGIN, "right")],
        fields=[
            field("p", 3),
            field("turn", 3, conserved=False),
            field("signal", signed=False),
            field("work", conserved=False, extensive=False),
        ],
        budget=budget,
    )
    raw.update(schema_version=2, model_id="atomic-spatial-integration-v1", shape=[5, 5, 5])
    raw["operation_costs"]["couple"] = couple_price
    raw["spatial_fields"] = [
        {
            "field": name,
            "baseline": baseline,
            "transport": "outward",
            "axis_weights": [1, 0, 0],
            "octant_weights": [1] + [0] * 7,
            "decay": {"retain_numerator": 1, "retain_denominator": 2},
        }
        for name, baseline in (("p", [0, 0, 0]), ("turn", [0, 0, 1]), ("signal", 0))
    ]
    raw["emissions"] = [{"type": "left", "field": "signal", "amount": 1, "source": True, "budget": 3}]
    raw["spatial_couplings"] = [
        {
            "name": f"turn_{name}",
            "type": name,
            "field": "p",
            "mode": "rotation",
            "rotation": {"field": "turn", "side": "right"},
            "budget": [amount, amount, 0],
        }
        for name, amount in (("left", 5), ("right", 1))
    ]
    raw["interactions"] = [
        {
            "name": "swap_rotated_vectors",
            "left_type": "left",
            "right_type": "right",
            "when": {"op": "gt", "args": [{"op": "component", "args": [{"field": "p"}], "index": 1}, 0]},
            "assignments": [
                {"side": side, "field": "p", "expression": {"field": "p", "side": other}}
                for side, other in (("left", "right"), ("right", "left"))
            ],
            "invariants": [
                {
                    "name": "pair_squared_norm",
                    "expression": {
                        "op": "add",
                        "args": [
                            {"op": "dot", "args": [{"field": "p", "side": side}] * 2}
                            for side in ("left", "right")
                        ],
                    },
                }
            ],
        }
    ]
    return raw


def records(world):
    return {
        world.initial.disturbances[record.type_index].name: record
        for cell in world.cells.values()
        for record in cell.records
        if record is not None
    }


def vectors(world):
    return {name: world.record_values(record)["p"] for name, record in records(world).items()}


def assert_balance(world):
    for name, initial in {"p": (4, 0, 0), "signal": (0,)}.items():
        assert (
            tuple(
                value + lost + escaped - source
                for value, lost, escaped, source in zip(
                    world.totals()[name],
                    world.dissipation_totals()[name],
                    world.escaped_totals()[name],
                    world.source_totals()[name],
                    strict=True,
                )
            )
            == initial
        )
    assert all(item["balanced"] for item in world.spatial_accounting().values())


def test_rotation_precedes_atomic_swap_and_all_three_responses_use_configured_price():
    costs = []
    for price in (1, 7):
        events = []
        world = Simulation(parse_initial_state(combined(couple_price=price)), observer=events.append)
        world.step()
        assert vectors(world) == AFTER
        assert world.spatial_accounting()["p"]["reactions"] == (4, -4, 0)
        assert world.spatial_accounting()["p"]["current"] == (2, -2, 0)
        assert world.dissipation_totals()["p"] == (2, -2, 0)
        assert world.source_totals()["signal"] == (1,)
        cost = next(event["cost"] for event in events if event["event"] == "cycle_started")
        assert world.record_values(records(world)["left"])["work"] == (cost,)
        costs.append(cost)
        assert_balance(world)
    # Two spatial responses and one activated atomic transaction, priced six units higher.
    assert costs[1] - costs[0] == 18


def test_delayed_atomic_commit_keeps_frozen_response_and_current_finite_emission_allowance():
    events = []
    world = Simulation(parse_initial_state(combined(budget=200)), observer=events.append)
    world.step()
    started = next(event for event in events if event["event"] == "cycle_started")
    ready = started["ready_tick"]
    assert 3 <= ready <= 8
    while world.tick < ready:
        assert vectors(world) == BEFORE
        assert world.source_totals()["signal"] == (min(world.tick, 3),)
        assert unpack(records(world)["left"].emission_remaining[0]) == (max(3 - world.tick, 0),)
        assert world.spatial_accounting()["p"]["reactions"] == (0, 0, 0)
        assert_balance(world)
        world.step()
    assert vectors(world) == AFTER
    assert world.source_totals()["signal"] == (3,)
    assert unpack(records(world)["left"].emission_remaining[0]) == (0,)
    for record in records(world).values():
        assert all(not any(unpack(payload)) for payload in record.spatial_remaining)
    assert world.record_values(records(world)["left"])["work"] == (started["cost"],)
    assert world.spatial_accounting()["p"]["reactions"] == (4, -4, 0)
    assert_balance(world)


def test_new_transform_dot_and_gt_operators_keep_nested_delivered_flux_context():
    raw = combined()
    raw["fields"][1]["components"] = 1
    raw["spatial_fields"][1]["baseline"] = 0
    raw["spatial_seeds"] = [{"position": [1, 2, 2], "field": "turn", "populations": [24] + [0] * 7}]
    for rule in raw["spatial_couplings"]:
        rule.update(
            denominator=12,
            rotation={
                "op": "mul",
                "args": [
                    {
                        "op": "transform",
                        "args": [{"flux": "turn"}],
                        "matrix": [[0, 0, 0], [0, 0, 0], [1, 0, 0]],
                    },
                    {"op": "gt", "args": [{"op": "dot", "args": [{"flux": "turn"}, [1, 0, 0]]}, 0]},
                ],
            },
        )
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert vectors(world) == BEFORE
    assert world.spatial_values(ORIGIN)["turn"]["directions"][0] == (12,)
    world.step()
    assert vectors(world) == AFTER
    assert world.spatial_accounting()["p"]["reactions"] == (4, -4, 0)
    assert_balance(world)


def test_rejected_atomic_transaction_does_not_undo_an_independently_committed_emission():
    raw = combined()
    raw["interactions"][0]["assignments"][0]["expression"] = [0, 100, 0]
    world = Simulation(parse_initial_state(raw))
    with pytest.raises(ValueError, match="conservation"):
        world.step()
    assert world.faulted and vectors(world) == BEFORE
    assert all(cell.pending is None for cell in world.cells.values())
    assert world.spatial_accounting()["p"]["reactions"] == (0, 0, 0)
    assert world.source_totals()["signal"] == (1,)
    assert unpack(records(world)["left"].emission_remaining[0]) == (2,)
    assert_balance(world)
