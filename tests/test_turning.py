import pytest

from event_universe.core.state import MAX_CORE_INT, MAX_WORK_INT
from event_universe.dynamics import FieldTurning
from event_universe.dynamics.turning import TurningResult, dominant_axis_transverse, full_response

ZERO = (0, 0, 0)


def test_full_response_exchanges_every_component_and_keeps_signed_residue():
    turning = FieldTurning(select_direction=full_response)
    result = turning.apply((3, -2, 0), (7, 8, 9), (5, -7, 2), (1, -1, 0), numerator=2, denominator=3)
    assert result == TurningResult((6, -7, 1), (4, 13, 8), (2, 0, 1), (3, -5, 1))


def test_custom_direction_uses_the_shared_accumulator_and_exchange():
    def z_only(momentum, field_vector):
        assert momentum == (4, 0, 0)
        return 0, 0, field_vector[2]

    result = FieldTurning(select_direction=z_only).apply(
        (4, 0, 0), ZERO, (50, 60, -3), ZERO, numerator=2, denominator=4
    )
    assert result == TurningResult((4, 0, -1), (0, 0, 1), (0, 0, -2), (0, 0, -1))


@pytest.mark.parametrize("sign", [-1, 1])
@pytest.mark.parametrize("denominator", [1, 12, 64])
def test_fractional_turning_preserves_exact_exchange_at_each_step(sign, denominator):
    turning = FieldTurning(select_direction=full_response)
    momentum, reservoir, remainders = (3, 0, 0), (0, 2, 0), ZERO
    for step in range(1, denominator + 1):
        result = turning.apply(
            momentum, reservoir, (0, sign, 0), remainders, numerator=1, denominator=denominator
        )
        momentum, reservoir, remainders = result.momentum, result.field_momentum, result.remainders
        assert tuple(a + b for a, b in zip(momentum, reservoir, strict=True)) == (3, 2, 0)
        assert momentum[1] * denominator + remainders[1] == step * sign
    assert momentum == (3, sign, 0) and remainders == ZERO


@pytest.mark.parametrize(
    "momentum,expected",
    [
        ((4, 1, 0), (0, 6, 7)),
        ((1, -4, 0), (5, 0, 7)),
        ((0, 1, -4), (5, 6, 0)),
        ((2, -2, 2), (0, 6, 7)),
        ((0, 2, -2), (5, 0, 7)),
        (ZERO, (5, 6, 7)),
    ],
)
def test_dominant_axis_policy_is_explicit_about_stationary_motion_and_ties(momentum, expected):
    assert dominant_axis_transverse(momentum, (5, 6, 7)) == expected


def test_exchange_can_span_two_valid_register_extremes():
    result = FieldTurning(select_direction=full_response).apply(
        (-MAX_CORE_INT, 0, 0),
        (MAX_CORE_INT, 0, 0),
        (2 * MAX_CORE_INT, 0, 0),
        ZERO,
        numerator=1,
        denominator=1,
    )
    assert result.momentum == (MAX_CORE_INT, 0, 0)
    assert result.field_momentum == (-MAX_CORE_INT, 0, 0)
    assert result.impulse == (2 * MAX_CORE_INT, 0, 0)


@pytest.mark.parametrize(
    "momentum,reservoir", [((MAX_CORE_INT, 0, 0), ZERO), (ZERO, (-MAX_CORE_INT, 0, 0))]
)
def test_overflow_on_either_side_rejects_the_entire_exchange(momentum, reservoir):
    with pytest.raises(OverflowError, match="32-bit"):
        FieldTurning(select_direction=full_response).apply(
            momentum, reservoir, (1, 0, 0), ZERO, numerator=1, denominator=1
        )


def test_turning_bounds_intermediate_products():
    with pytest.raises(OverflowError, match="64-bit"):
        FieldTurning(select_direction=full_response).apply(
            ZERO, ZERO, (MAX_WORK_INT, 0, 0), ZERO, numerator=2, denominator=MAX_CORE_INT
        )


@pytest.mark.parametrize("denominator,remainders", [(0, ZERO), (7, (7, 0, 0)), (7, (0, -7, 0))])
def test_invalid_response_denominator_or_remainder_is_rejected(denominator, remainders):
    with pytest.raises(ValueError):
        FieldTurning(select_direction=full_response).apply(
            ZERO, ZERO, ZERO, remainders, numerator=1, denominator=denominator
        )
