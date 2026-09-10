import pytest

from event_universe.core.state import MAX_CORE_INT, MINUS_X, MINUS_Y, MINUS_Z, PLUS_X, PLUS_Y, PLUS_Z
from event_universe.dynamics.movement import MovementResult, advance_movement, choose_axis


@pytest.mark.parametrize(
    "momentum,direction",
    [
        ((1, 0, 0), PLUS_X),
        ((-1, 0, 0), MINUS_X),
        ((0, 1, 0), PLUS_Y),
        ((0, -1, 0), MINUS_Y),
        ((0, 0, 1), PLUS_Z),
        ((0, 0, -1), MINUS_Z),
    ],
)
def test_axis_selection_keeps_the_sign_of_each_cardinal_direction(momentum, direction):
    assert choose_axis(momentum, 0) == (direction, 0)


def test_diagonal_axis_sequence_preserves_component_counts_over_a_full_cycle():
    phase = 0
    directions = []
    for _ in range(6):
        direction, phase = choose_axis((3, -2, 1), phase)
        directions.append(direction)
    assert directions == [PLUS_X, PLUS_X, PLUS_X, MINUS_Y, MINUS_Y, PLUS_Z]
    assert phase == 0


def test_quarter_speed_accumulates_three_ticks_and_hops_on_the_fourth():
    budget, phase = 0, 0
    results = []
    for _ in range(4):
        result = advance_movement((3, 0, 0), budget, phase, speed_cap=12)
        results.append(result)
        budget, phase = result.budget, result.phase
    assert results == [
        MovementResult(-1, 0, 3),
        MovementResult(-1, 0, 6),
        MovementResult(-1, 0, 9),
        MovementResult(PLUS_X, 1, 0),
    ]


def test_diagonal_budget_and_phase_produce_a_known_next_step():
    assert advance_movement((3, -2, 1), 8, 4, speed_cap=12) == MovementResult(MINUS_Y, 5, 2)


def test_stationary_particle_keeps_its_unused_budget_and_phase():
    assert advance_movement((0, 0, 0), 5, 2, speed_cap=12) == MovementResult(-1, 2, 5)


@pytest.mark.parametrize("speed", [12, 120, MAX_CORE_INT])
def test_speed_cap_allows_exactly_one_hop_even_at_large_momentum(speed):
    result = advance_movement((speed, 0, 0), 5, 0, speed_cap=12)
    assert result == MovementResult(PLUS_X, 1, 5)


@pytest.mark.parametrize("budget,phase,speed_cap", [(-1, 0, 12), (12, 0, 12), (0, -1, 12), (0, 0, 0)])
def test_invalid_movement_state_is_rejected(budget, phase, speed_cap):
    with pytest.raises(ValueError):
        advance_movement((3, 0, 0), budget, phase, speed_cap=speed_cap)
