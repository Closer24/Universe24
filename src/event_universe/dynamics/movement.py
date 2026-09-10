"""Integer movement budget and digital axis selection, shared by candidate models."""

from typing import NamedTuple, Protocol

from event_universe.core.state import (
    MINUS_X,
    MINUS_Y,
    MINUS_Z,
    PLUS_X,
    PLUS_Y,
    PLUS_Z,
    Vector,
    checked,
    checked_work,
)
from event_universe.dynamics.rate import step_rate


class MovementResult(NamedTuple):
    direction: int
    phase: int
    budget: int


def choose_axis(momentum: Vector, phase: int) -> tuple[int, int]:
    """Preserve the v10 digital axis sequence, including its coordinate ordering."""
    px, py, pz = momentum
    ax, ay, az = abs(px), abs(py), abs(pz)
    total = checked_work(ax + ay + az)
    if total == 0:
        return -1, phase
    slot = phase % total
    next_phase = checked((slot + 1) % total)
    if slot < ax:
        return (PLUS_X if px >= 0 else MINUS_X), next_phase
    if slot < ax + ay:
        return (PLUS_Y if py >= 0 else MINUS_Y), next_phase
    return (PLUS_Z if pz >= 0 else MINUS_Z), next_phase


def advance_movement(momentum: Vector, budget: int, phase: int, *, speed_cap: int) -> MovementResult:
    """Request zero or one cardinal hop using the same rule for every speed."""
    if len(momentum) != 3:
        raise ValueError("exactly three momentum components are required")
    for value in (*momentum, budget, phase, speed_cap):
        checked(value)
    if speed_cap <= 0 or not 0 <= budget < speed_cap or phase < 0:
        raise ValueError("invalid movement budget, phase or speed cap")
    speed = step_rate(momentum, speed_cap).numerator
    next_budget = checked(budget + speed)
    if next_budget < speed_cap:
        return MovementResult(-1, phase, next_budget)
    direction, next_phase = choose_axis(momentum, phase)
    return MovementResult(direction, next_phase, next_budget - speed_cap)


class MovementRule(Protocol):
    def __call__(
        self, momentum: Vector, budget: int, phase: int, *, speed_cap: int
    ) -> MovementResult: ...
