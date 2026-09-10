"""Numerical contracts and independent low-speed mechanics comparisons."""

from itertools import permutations, product

import pytest

from event_universe.core.state import DIRECTIONS, MAX_CORE_INT
from event_universe.dynamics.field_action import UnifiedFieldAction
from event_universe.dynamics.movement import advance_movement
from event_universe.dynamics.rate import StepRate, step_rate
from event_universe.dynamics.transit import depart_movement, transit_ticks
from event_universe.dynamics.turning import FieldTurning, full_response

ZERO = (0, 0, 0)
ACTION = UnifiedFieldAction(FieldTurning(full_response), advance_movement)


def act(p, g=ZERO, *, field=ZERO, rem=ZERO, budget=0, phase=0, den=1, cap=60):
    return ACTION.apply(p, field, g, rem, budget, phase, numerator=1, denominator=den, speed_cap=cap)


@pytest.mark.parametrize(
    "gradient,expected",
    [((2, 0, 0), (6, 0, 0)), ((-2, 0, 0), (2, 0, 0)), ((0, 1, 0), (4, 1, 0)), ((-2, 1, 0), (2, 1, 0))],
)
def test_one_impulse_controls_both_timing_and_direction(gradient, expected):
    result = act((4, 0, 0), gradient, cap=12)
    assert result.response.momentum == expected
    assert result.response.field_momentum == tuple(-x for x in gradient)
    assert result.motion.budget == sum(abs(x) for x in expected)


def first_hop_after_impulse(gradient):
    p, field, rem, budget, phase = (4, 0, 0), ZERO, ZERO, 0, 0
    for tick in range(1, 13):
        result = act(
            p, gradient if tick == 1 else ZERO, field=field, rem=rem, budget=budget, phase=phase, cap=12
        )
        p, field, rem = result.response[:3]
        direction, phase, budget = result.motion
        if direction >= 0:
            return tick, direction
    raise AssertionError("no hop")


def test_forward_and_opposing_impulses_change_next_event_time():
    assert first_hop_after_impulse((2, 0, 0)) == (2, 0)
    assert first_hop_after_impulse(ZERO) == (3, 0)
    assert first_hop_after_impulse((-2, 0, 0)) == (6, 0)


def displacement_for_cycle(p):
    position, budget, phase = [0, 0, 0], 0, 0
    for _ in range(60):
        result = act(p, budget=budget, phase=phase)
        direction, phase, budget = result.motion
        assert result.response.momentum == p
        if direction >= 0:
            position = [a + b for a, b in zip(position, DIRECTIONS[direction], strict=True)]
    assert budget == 0
    return tuple(position)


def test_true_rotation_preserves_geometric_speed_not_hop_count():
    # Independent 3-4-5 triangle: both paths displace five units in 60 ticks.
    p = act((5, 0, 0), (-2, 4, 0)).response.momentum
    assert p == (3, 4, 0)
    assert displacement_for_cycle((5, 0, 0)) == (5, 0, 0)
    assert displacement_for_cycle(p) == (3, 4, 0)
    assert step_rate((5, 0, 0), 60) == StepRate(5, 60)
    assert step_rate(p, 60) == StepRate(7, 60)


def test_a_finite_sideways_kick_is_not_a_pure_rotation():
    before, impulse = (5, 0, 0), (0, 1, 0)
    after = act(before, impulse).response.momentum
    assert after == (5, 1, 0)
    assert sum(x * x for x in after) == 26
    # Exact midpoint-work identity; not the incorrect old-velocity dot product.
    twice_work = sum((a + b) * i for a, b, i in zip(before, after, impulse, strict=True))
    assert twice_work == 1


@pytest.mark.parametrize("order", list(permutations(range(3))))
@pytest.mark.parametrize("signs", list(product((-1, 1), repeat=3)))
def test_action_and_complete_cycle_respect_signed_axis_symmetries(order, signs):
    def transform(v):
        return tuple(signs[i] * v[order[i]] for i in range(3))

    initial, impulse, expected = transform((4, 2, 1)), transform((-1, 2, -2)), transform((3, 4, -1))
    result = act(initial, impulse)
    assert result.response.momentum == expected
    assert result.response.field_momentum == tuple(-x for x in impulse)
    assert displacement_for_cycle(expected) == expected


def test_stop_reverse_start_and_unchanged_field_are_one_vector_rule():
    assert act((2, 0, 0), (-2, 0, 0)).response.momentum == ZERO
    assert act((2, 0, 0), (-2, 0, 0)).motion.direction == -1
    assert act((2, 0, 0), (-5, 0, 0)).response.momentum == (-3, 0, 0)
    assert act(ZERO, (2, -1, 0)).response.momentum == (2, -1, 0)
    assert act((3, 2, 1), ZERO).response.momentum == (3, 2, 1)


def test_subunit_impulse_accumulates_and_exchanges_without_speed_force():
    p, field, rem = (4, 0, 0), ZERO, ZERO
    for tick in range(1, 65):
        result = act(p, (-1, 1, 0), field=field, rem=rem, den=64)
        p, field, rem = result.response[:3]
        assert tuple(a + b for a, b in zip(p, field, strict=True)) == (4, 0, 0)
        if tick < 64:
            assert p == (4, 0, 0) and rem == (-tick, tick, 0)
    assert p == (3, 1, 0) and rem == ZERO


def test_direction_is_not_normalized_or_clipped_when_rate_reaches_capacity():
    result = act((11, 0, 0), (10, 10, 0), cap=12)
    assert result.response.momentum == (21, 10, 0)
    assert result.response.field_momentum == (-10, -10, 0)
    assert result.motion.direction in range(6) and result.motion.budget == 0
    assert step_rate(result.response.momentum, 12) == StepRate(12, 12)


def test_the_same_action_resolves_link_transits_from_updated_momentum():
    action = UnifiedFieldAction(FieldTurning(full_response), depart_movement)
    durations = []
    for impulse in ((2, 0, 0), ZERO, (-2, 0, 0)):
        result = action.apply(
            (4, 0, 0), ZERO, impulse, ZERO, 0, 0, numerator=1, denominator=1, speed_cap=12
        )
        durations.append(transit_ticks(10, result.response.momentum, 12))
    assert durations == [20, 30, 60]


@pytest.mark.parametrize(
    "p,g,field", [((MAX_CORE_INT, 0, 0), (1, 0, 0), ZERO), (ZERO, (1, 0, 0), (-MAX_CORE_INT, 0, 0))]
)
def test_action_rejects_overflow_on_either_side_before_movement(p, g, field):
    def forbidden_movement(*args, **kwargs):
        raise AssertionError("invalid exchange reached movement")

    action = UnifiedFieldAction(FieldTurning(full_response), forbidden_movement)
    with pytest.raises(OverflowError):
        action.apply(p, field, g, ZERO, 0, 0, numerator=1, denominator=1, speed_cap=12)


@pytest.mark.parametrize(
    "momentum,cap", [((1, 2), 12), ((True, 0, 0), 12), ((1.0, 0, 0), 12), ((1, 0, 0), 0)]
)
def test_rate_rejects_non_integer_or_invalid_state(momentum, cap):
    with pytest.raises((TypeError, ValueError)):
        step_rate(momentum, cap)
