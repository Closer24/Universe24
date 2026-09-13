"""Completed local work can drive emission without traveling inside a carrier."""

from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import (
    MAX_VALUE,
    OPERATIONS,
    CostMeter,
    Expression,
    OperationCosts,
)
from event_universe.fields.disturbances import evaluate
from event_universe.initialization import parse_initial_state


def document():
    return {
        "schema_version": 2,
        "model_id": "node-work-readout-test",
        "shape": [9, 9, 9],
        "boundary": "open",
        "ticks": 8,
        "link_ticks": 1,
        "normal_budget": 100000,
        "slots_per_node": 2,
        "operation_costs": dict.fromkeys(OPERATIONS, 1),
        "fields": [
            {
                "name": "heading",
                "components": 3,
                "signed": True,
                "conserved": True,
                "units": "integer",
                "extensive": True,
            },
            {
                "name": "load",
                "components": 3,
                "signed": True,
                "conserved": True,
                "units": "integer",
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "body",
                "fields": ["heading"],
                "defaults": {"heading": [1, 0, 0]},
                "transport": {
                    "mode": "move",
                    "direction_field": "heading",
                    "rate": 1,
                    "rate_denominator": 2,
                },
            }
        ],
        "seeds": [{"type": "body", "position": [3, 3, 3]}],
        "spatial_fields": [
            {
                "field": "load",
                "transport": "outward",
                "baseline": [0, 0, 0],
                "decay": {"retain_numerator": 1, "retain_denominator": 2},
            }
        ],
        "emissions": [
            {
                "type": "body",
                "field": "load",
                "source": True,
                "budget": [1000000] * 3,
                "amount": {"op": "mul", "args": [{"node": "committed_cost"}, [1, 1, 1]]},
            }
        ],
    }


def test_work_is_zero_before_commit_and_remains_at_departure_node():
    world = Simulation(parse_initial_state(document()))
    world.step()
    first = world.nodes[(3, 3, 3)].committed_cost
    assert first > 0
    assert world.source_totals()["load"] == (0, 0, 0)
    world.step()
    assert world.source_totals()["load"] == (first,) * 3
    assert any(r is not None for r in world.nodes[(4, 3, 3)].records)
    assert world.nodes[(4, 3, 3)].committed_cost == 0
    previous = world.source_totals()["load"]
    world.step()
    # The new Node has no completed carrier work yet. The carried emitter
    # allowance arrives, but the source Node's cost register does not.
    assert world.source_totals()["load"] == previous
    assert world.nodes[(4, 3, 3)].committed_cost > 0
    assert world.nodes[(3, 3, 3)].committed_cost > 0


def test_pending_cost_is_not_observable_as_completed_work():
    raw = document()
    raw["normal_budget"] = 1
    world = Simulation(parse_initial_state(raw))
    world.step()
    node = world.nodes[(3, 3, 3)]
    assert node.pending is not None and node.last_cost > 0
    assert node.committed_cost == 0
    world.step()
    assert node.committed_cost == 0
    assert world.source_totals()["load"] == (0, 0, 0)


@pytest.mark.parametrize("value", [None, -1, True, MAX_VALUE + 1])
def test_node_readout_rejects_missing_or_invalid_context(value):
    with pytest.raises(ValueError):
        evaluate(
            Expression("node_cost"),
            (),
            (),
            CostMeter(OperationCosts((1,) * len(OPERATIONS))),
            node_cost=value,
        )


@pytest.mark.parametrize(
    "leaf", [{"node": "global_cost"}, {"node": "committed_cost", "field": "heading"}]
)
def test_no_global_or_mixed_node_readout_is_accepted(leaf):
    raw = document()
    raw["emissions"][0]["amount"]["args"][0] = leaf
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_node_readout_is_not_an_implicit_transport_input():
    raw = document()
    raw["disturbance_types"][0]["transport"]["rate"] = {"node": "committed_cost"}
    with pytest.raises(ValueError, match="only to emission"):
        parse_initial_state(raw)


def test_expression_uses_scalar_integer_readout_inside_existing_operations():
    expression = Expression("mul", (Expression("node_cost"), Expression("literal", literal=(1, -2, 0))))
    assert evaluate(
        expression, (), (), CostMeter(OperationCosts((1,) * len(OPERATIONS))), node_cost=7
    ) == (7, -14, 0)


def test_legacy_emission_without_node_readout_is_unchanged():
    raw = deepcopy(document())
    raw["emissions"][0]["amount"] = [12, 0, 0]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert world.source_totals()["load"] == (12, 0, 0)


def test_rejected_transaction_does_not_publish_pending_work():
    from tests.test_spatial_interactions import ORIGIN, exchange

    world = Simulation(parse_initial_state(exchange(delayed=True, incoming=True)))
    world.step()
    ready = world.nodes[ORIGIN].pending.ready_tick
    while world.tick < ready - 1:
        world.step()
    previous = world.nodes[ORIGIN].committed_cost
    with pytest.raises(ValueError, match="invariant"):
        world.step()
    assert world.nodes[ORIGIN].committed_cost == previous


def test_rational_projection_receives_the_same_explicit_local_readout():
    raw = document()
    raw["emissions"][0]["amount"] = {
        "op": "mul",
        "args": [
            {"op": "rational_floor", "args": [{"op": "ratio", "args": [{"node": "committed_cost"}, 2]}]},
            [1, 1, 1],
        ],
    }
    initial = parse_initial_state(raw)
    assert evaluate(
        initial.emissions[0].amount, (), (), CostMeter(initial.operation_costs), node_cost=7
    ) == (3, 3, 3)
