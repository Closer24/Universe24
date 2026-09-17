"""Independent numerical contracts for shared decoded integer calculations."""

import pytest

from event_universe.core.integer import (
    MAX_WORK_INT,
    add_components,
    ceil_div,
    checked_sum,
    checked_work,
    cross_product,
    dot_product,
    signed_divrem,
    subtract_components,
)


@pytest.mark.parametrize(
    "numerator,denominator,expected",
    [(0, 7, 0), (1, 7, 1), (14, 7, 2), (15, 7, 3), (MAX_WORK_INT, 1, MAX_WORK_INT)],
)
def test_ceiling_division(numerator, denominator, expected):
    assert ceil_div(numerator, denominator) == expected


@pytest.mark.parametrize("numerator,denominator", [(-1, 2), (1, 0), (1, -2)])
def test_ceiling_requires_nonnegative_ratio(numerator, denominator):
    with pytest.raises(ValueError):
        ceil_div(numerator, denominator)


@pytest.mark.parametrize("numerator,denominator", [(True, 1), (1, False), (1.5, 2)])
def test_ceiling_requires_integers(numerator, denominator):
    with pytest.raises(TypeError):
        ceil_div(numerator, denominator)


def test_ceiling_preserves_adjusted_numerator_bound():
    with pytest.raises(OverflowError):
        ceil_div(MAX_WORK_INT, 2)
    with pytest.raises(OverflowError):
        ceil_div(MAX_WORK_INT + 1, 1)


@pytest.mark.parametrize("value,expected", [(7, (2, 1)), (-7, (-2, -1)), (-2, (0, -2)), (0, (0, 0))])
def test_signed_division_rounds_toward_zero_and_keeps_residue(value, expected):
    assert signed_divrem(value, 3) == expected


@pytest.mark.parametrize("numerator", [-129, -65, -1, 0, 1, 65, 129])
@pytest.mark.parametrize("denominator", [1, 12, 64])
def test_signed_remainder_is_exact(numerator, denominator):
    quotient, remainder = signed_divrem(numerator, denominator)
    assert numerator == quotient * denominator + remainder
    assert abs(remainder) < denominator
    assert remainder == 0 or (remainder > 0) == (numerator > 0)


def test_working_register_is_bounded():
    assert checked_work(MAX_WORK_INT) == MAX_WORK_INT
    assert checked_work(-MAX_WORK_INT) == -MAX_WORK_INT
    with pytest.raises(OverflowError):
        checked_work(MAX_WORK_INT + 1)
    with pytest.raises(OverflowError):
        checked_work(-MAX_WORK_INT - 1)
    with pytest.raises(TypeError):
        checked_work(True)


@pytest.mark.parametrize(
    "operation,left,right,expected",
    [
        (add_components, (3, -4, 0), (-1, 7, -2), (2, 3, -2)),
        (subtract_components, (3, -4, 0), (-1, 7, -2), (4, -11, 2)),
        (dot_product, (3, -4, 2), (-1, 7, -2), -35),
        (dot_product, (3, 4, 0), (3, 4, 0), 25),
        (add_components, (MAX_WORK_INT,), (-MAX_WORK_INT,), (0,)),
        (subtract_components, (-MAX_WORK_INT,), (-MAX_WORK_INT,), (0,)),
        (dot_product, (MAX_WORK_INT,), (1,), MAX_WORK_INT),
        (add_components, (), (), ()),
        (subtract_components, (), (), ()),
        (dot_product, (), (), 0),
    ],
)
def test_component_operations(operation, left, right, expected):
    assert operation(left, right) == expected


@pytest.mark.parametrize("operation", [add_components, subtract_components, dot_product])
@pytest.mark.parametrize("left,right", [((1,), (1, 2)), ((1, 2), (1,))])
def test_components_do_not_silently_truncate_or_broadcast(operation, left, right):
    with pytest.raises(ValueError):
        operation(left, right)


@pytest.mark.parametrize(
    "operation,left,right",
    [
        (add_components, (MAX_WORK_INT,), (1,)),
        (add_components, (-MAX_WORK_INT,), (-1,)),
        (subtract_components, (-MAX_WORK_INT,), (1,)),
        (subtract_components, (MAX_WORK_INT,), (-1,)),
        (dot_product, (MAX_WORK_INT, MAX_WORK_INT), (2, -2)),
        (dot_product, (MAX_WORK_INT, 1, -1), (1, 1, 1)),
        (cross_product, (0, MAX_WORK_INT, MAX_WORK_INT), (0, 2, 2)),
        (cross_product, (0, MAX_WORK_INT, 1), (0, -1, 1)),
    ],
)
def test_component_overflow_cannot_be_hidden_by_cancellation(operation, left, right):
    with pytest.raises(OverflowError):
        operation(left, right)


@pytest.mark.parametrize(
    "left,right,expected",
    [
        ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        ((0, 1, 0), (1, 0, 0), (0, 0, -1)),
        ((2, -3, 4), (-1, 5, 2), (-26, -8, 7)),
        ((2, -3, 4), (4, -6, 8), (0, 0, 0)),
        ((0, 0, 0), (2, -3, 4), (0, 0, 0)),
    ],
)
def test_right_handed_cross_product(left, right, expected):
    assert cross_product(left, right) == expected


@pytest.mark.parametrize(
    "left,right", [((1,), (1, 2, 3)), ((1, 2, 3), (1, 2)), ((1, 2, 3, 4), (1, 2, 3))]
)
def test_cross_product_requires_three_components(left, right):
    with pytest.raises(ValueError):
        cross_product(left, right)


@pytest.mark.parametrize(
    "values,expected", [((), 0), ((3, -7, 2), -2), ((MAX_WORK_INT, -MAX_WORK_INT), 0)]
)
def test_ordered_sum(values, expected):
    assert checked_sum(iter(values)) == expected


@pytest.mark.parametrize("values", [(MAX_WORK_INT, 1, -1), (-MAX_WORK_INT, -1, 1)])
def test_sum_checks_partial_totals(values):
    with pytest.raises(OverflowError):
        checked_sum(values)
