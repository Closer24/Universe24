"""Prepared laws preserve ordered integer results, failures, tariffs, and input ownership."""

from dataclasses import replace

import pytest

from event_universe.core.disturbance_state import (
    MAX_VALUE,
    CostMeter,
    Expression,
    OperationCosts,
    pack,
)
from event_universe.core.integer import MAX_WORK_INT
from event_universe.fields import expressions
from event_universe.fields.disturbances import evaluate
from event_universe.fields.ratios import Ratio


def literal(*values):
    return Expression("literal", literal=values)


def operation(name, *arguments, **settings):
    return Expression(name, arguments, **settings)


def meter(price=1):
    return CostMeter(OperationCosts((price,) * 9))


@pytest.mark.parametrize(
    "law,expected,cost",
    [
        (literal(-2, 5, 3), (-2, 5, 3), 1),
        (operation("add", literal(-2, 5, 3), literal(4)), (2, 9, 7), 3),
        (operation("sub", literal(4), literal(-2, 5, 3)), (6, -1, 1), 3),
        (operation("mul", literal(-2, 5, 3), literal(-3)), (6, -15, -9), 3),
        (operation("min", literal(-2, 5, 3), literal(4)), (-2, 4, 3), 3),
        (operation("max", literal(-2, 5, 3), literal(4)), (4, 5, 4), 3),
        (operation("exact_div", literal(-6, 9, 0), literal(-3)), (2, -3, 0), 3),
        (operation("neg", literal(-2, 5, 3)), (2, -5, -3), 2),
        (operation("abs", literal(-2, 5, 3)), (2, 5, 3), 2),
        (operation("sum", literal(-2, 5, 3)), (6,), 2),
        (operation("component", literal(-2, 5, 3), component=1), (5,), 2),
        (operation("dot", literal(-2, 5, 3), literal(4, 1, -2)), (-9,), 3),
        (operation("cross", literal(1, 2, 3), literal(3, -1, 2)), (7, 7, -7), 3),
        (operation("vector", literal(3), literal(-1), literal(7)), (3, -1, 7), 4),
        (operation("eq", literal(-3), literal(-3)), (1,), 3),
        (operation("eq", literal(-3), literal(3)), (0,), 3),
        (operation("gt", literal(-3), literal(-4)), (1,), 3),
        (operation("gt", literal(-3), literal(3)), (0,), 3),
        (
            operation("transform", literal(-2, 5, 3), matrix=((0, -1, 0), (1, 0, 0), (0, 0, 1))),
            (-5, -2, 3),
            2,
        ),
    ],
)
def test_integer_operators_have_independent_values_and_node_prices(law, expected, cost):
    for _ in range(2):
        charged = meter(7)
        assert evaluate(law, (), (), charged) == expected
        assert charged.total == 7 * cost


def test_repeated_subexpression_is_evaluated_and_charged_twice():
    child = operation("add", literal(2), literal(5))
    charged = meter()
    assert evaluate(operation("mul", child, child), (), (), charged) == (49,)
    assert charged.total == 7


@pytest.mark.parametrize("leaf", ["field", "flux", "received", "outgoing"])
def test_cached_plan_reads_each_current_input_and_cost_setting(leaf):
    law = Expression(leaf, field=1, side=1, port=4)
    for value, price in ((3, 2), (-7, 5), (0, 3)):
        values = (pack((0,)), pack((value, 2, -1)))
        charged = meter(price)
        assert evaluate(
            law,
            (pack((17,)), pack((19, 23, 29))),
            values,
            charged,
            values,
            ports=(values,) * 6,
            outgoing=(values,) * 6,
        ) == (value, 2, -1)
        assert charged.total == price


@pytest.mark.parametrize(
    "law,error,message,cost",
    [
        (operation("exact_div", literal(5), literal(2)), ValueError, "exact_div", 3),
        (operation("exact_div", literal(5), literal(0)), ValueError, "exact_div", 3),
        (Expression("field"), ValueError, "component code", 1),
        (Expression("flux"), ValueError, "local sample", 1),
        (Expression("received"), ValueError, "six explicitly", 1),
        (Expression("outgoing", port=7), ValueError, "six explicitly", 1),
        (operation("sum", literal(MAX_WORK_INT, 1, -1)), OverflowError, "64-bit", 2),
        (
            operation("dot", literal(MAX_WORK_INT, -MAX_WORK_INT, 0), literal(2, 2, 0)),
            OverflowError,
            "64-bit",
            3,
        ),
        (operation("add", literal(1, 2), literal(1, 2, 3)), ValueError, "component counts", 3),
        (operation("unsupported", literal(1), literal(2)), ValueError, "unknown expression", 3),
        (operation("neg"), IndexError, "tuple index", 1),
        (operation("add", literal(1)), IndexError, "tuple index", 2),
    ],
)
def test_cold_warm_and_evicted_plans_have_identical_failures(monkeypatch, law, error, message, cost):
    monkeypatch.setattr(expressions, "_plans", {})
    monkeypatch.setattr(expressions, "_PLAN_LIMIT", 1)
    for phase in ("cold", "warm", "evicted"):
        if phase == "evicted":
            evaluate(literal(91), (), (), meter())
            assert len(expressions._plans) == 1
        charged = meter(3)
        with pytest.raises(error, match=message):
            evaluate(law, ((0,),), (), charged)
        assert charged.total == 3 * cost


def test_children_fail_in_declared_order_before_later_inputs_are_read():
    failed_division = operation("exact_div", literal(5), literal(2))
    for children, message, cost in (
        ((failed_division, Expression("flux")), "exact_div", 4),
        ((Expression("flux"), failed_division), "local sample", 2),
    ):
        law = operation("add", *children)
        for _ in range(2):
            charged = meter()
            with pytest.raises(ValueError, match=message):
                evaluate(law, (), (), charged)
            assert charged.total == cost


def test_meter_overflow_precedes_input_access_even_after_preparation():
    law = Expression("field")
    assert evaluate(law, (pack((1,)),), (), meter()) == (1,)
    charged = meter()
    charged.total = MAX_VALUE
    with pytest.raises(ValueError, match="disturbance integer bound"):
        evaluate(law, ((0,),), (), charged)
    assert charged.total == MAX_VALUE


def test_cache_eviction_and_new_configuration_do_not_change_successful_results(monkeypatch):
    monkeypatch.setattr(expressions, "_plans", {})
    monkeypatch.setattr(expressions, "_PLAN_LIMIT", 1)
    law = operation("add", Expression("field"), literal(2))
    changed_law = replace(law, arguments=(Expression("field"), literal(9)))
    for current, expected in ((law, 5), (law, 5), (changed_law, 12), (law, 5)):
        charged = meter()
        assert evaluate(current, (pack((3,)),), (), charged) == (expected,)
        assert charged.total == 3
        assert len(expressions._plans) == 1


@pytest.mark.parametrize(
    "projection,expected", [("rational_whole", (-2,)), ("rational_remainder", (-1,))]
)
def test_rational_projection_keeps_exact_semantics_and_tariff(projection, expected):
    law = operation(projection, operation("ratio", literal(-7), literal(3)))
    for _ in range(2):
        charged = meter()
        assert evaluate(law, (), (), charged) == expected
        assert charged.total == 1 + 3 * 65536


def test_rational_regions_keep_127_bit_magnitudes_and_ordered_errors(monkeypatch):
    monkeypatch.setattr(expressions, "_plans", {})
    monkeypatch.setattr(expressions, "_PLAN_LIMIT", 1)
    largest = (1 << 127) - 1
    valid = operation("rational_key", literal(-largest))
    invalid = operation("rational_key", operation("mul", literal(largest), literal(2)))
    for _ in range(2):
        charged = meter()
        assert evaluate(valid, (), (), charged) == (-largest, 1)
        assert charged.total == 1 + 65536
        charged = meter()
        with pytest.raises(OverflowError, match="rational 127-bit bound"):
            evaluate(invalid, (), (), charged)
        assert charged.total == 1 + 3 * 65536


def test_rational_temporary_bounds_apply_before_reduction():
    largest = (1 << 255) - 1
    assert Ratio(largest, largest) == Ratio(1)
    with pytest.raises(OverflowError, match="rational 255-bit bound"):
        Ratio(largest + 1, largest + 1)
