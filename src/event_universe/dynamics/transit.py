"""Generic departure and integer transit duration; no access to cells or the world."""

from event_universe.core.state import Vector, checked, checked_work
from event_universe.dynamics.movement import MovementResult, choose_axis
from event_universe.dynamics.rate import step_rate


def depart_movement(momentum: Vector, budget: int, phase: int, *, speed_cap: int) -> MovementResult:
    """Select a single edge now; the transport engine schedules its completion."""
    for value in (*momentum, budget, phase, speed_cap):
        checked(value)
    if speed_cap < 1 or phase < 0 or budget != 0:
        raise ValueError("invalid departure state")
    direction, next_phase = choose_axis(momentum, phase)
    return MovementResult(direction, next_phase, 0)


def transit_ticks(length: int, momentum: Vector, speed_cap: int) -> int:
    """Per-link travel from step rate; never borrow credit from another edge."""
    for value in (length, *momentum, speed_cap):
        checked(value)
    if length < 1 or speed_cap < 1:
        raise ValueError("positive length and speed cap required")
    speed = step_rate(momentum, speed_cap).numerator
    if not speed:
        raise ValueError("a resting particle cannot start a transit")
    required = checked_work(length * speed_cap)
    return checked(checked_work(required + speed - 1) // speed)
