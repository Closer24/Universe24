"""Independent prefix, scale, sign and bound checks for the opt-in movement fix."""

from itertools import product

import pytest

from event_universe.core.state import DIRECTIONS, MAX_CORE_INT
from event_universe.dynamics.movement import advance_balanced_movement, choose_balanced_axis


def test_all_small_directions_have_bounded_prefix_error():
    for momentum in product(range(-3, 4), repeat=3):
        total = sum(abs(v) for v in momentum)
        if not total:
            continue
        phase = 0
        position = [0, 0, 0]
        for hop in range(1, 2 * total + 1):
            direction, phase = choose_balanced_axis(momentum, phase)
            for axis, delta in enumerate(DIRECTIONS[direction]):
                position[axis] += delta
                # Strict node bounds, checked without floating-point tolerances.
                bound = total if axis == 0 else 2 * total
                assert abs(position[axis] * total - hop * momentum[axis]) < bound
        assert position == [2 * v for v in momentum]
        assert phase == 0


def test_large_diagonal_does_not_walk_hundreds_of_nodes_on_one_axis():
    phase = 0
    counts = [0, 0, 0]
    for _ in range(10):
        direction, phase = choose_balanced_axis((600, 400, 0), phase)
        counts[direction // 2] += 1
    assert counts == [6, 4, 0]


def test_scaling_momentum_does_not_change_the_direction_sequence():
    a = b = 0
    for _ in range(100):
        da, a = choose_balanced_axis((3, -2, 1), a)
        db, b = choose_balanced_axis((300, -200, 100), b)
        assert da == db


def test_budget_keeps_the_same_rate_and_at_most_one_hop():
    budget = phase = hops = 0
    for _ in range(120):
        result = advance_balanced_movement((3, 2, 1), budget, phase, speed_cap=12)
        budget, phase = result.budget, result.phase
        hops += result.direction != -1
        assert 0 <= budget < 12
        assert -1 <= result.direction < 6
    assert hops == 60
    assert budget == 0


def test_zero_and_maximum_supported_momentum():
    assert choose_balanced_axis((0, 0, 0), 7) == (-1, 7)
    assert choose_balanced_axis((MAX_CORE_INT, 0, 0), MAX_CORE_INT - 1) == (0, 0)
    with pytest.raises(OverflowError):
        choose_balanced_axis((MAX_CORE_INT, 1, 0), 0)


@pytest.mark.parametrize("momentum,phase", [((1, 2), 0), ((True, 0, 0), 0), ((1, 0, 0), -1)])
def test_invalid_values_are_rejected(momentum, phase):
    with pytest.raises((ValueError, TypeError)):
        choose_balanced_axis(momentum, phase)
