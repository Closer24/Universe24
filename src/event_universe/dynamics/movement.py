"""Integer movement budget and digital axis selection, shared by candidate models."""

from collections.abc import Callable
from typing import NamedTuple, Protocol

from event_universe.core.state import (
    MINUS_X,
    MINUS_Y,
    MINUS_Z,
    PLUS_X,
    PLUS_Y,
    PLUS_Z,
    Vector,
    bounded_gcd,
    checked,
    checked_work,
    reduced_ratio,
)


class MovementResult(NamedTuple):
    direction: int
    phase: int
    budget: int
    budget_den: int = 1


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


def speed_ratio(momentum: Vector, mass: int, momentum_den: int, speed_cap: int) -> tuple[int, int]:
    """Return the capped L1 momentum/mass budget rate as integer numerator/denominator."""
    if len(momentum) != 3:
        raise ValueError("exactly three momentum components are required")
    for value in (*momentum, mass, momentum_den, speed_cap):
        checked(value)
    if min(mass, momentum_den, speed_cap) <= 0:
        raise ValueError("mass, denominator and speed cap must be positive")
    denominator = checked_work(mass * momentum_den)
    cap = checked_work(speed_cap * denominator)
    numerator = min(checked_work(sum(abs(value) for value in momentum)), cap)
    return reduced_ratio(numerator, denominator)


def advance_movement(
    momentum: Vector,
    budget: int,
    phase: int,
    *,
    speed_cap: int,
    mass: int = 1,
    momentum_den: int = 1,
    budget_den: int = 1,
    select_axis: Callable[[Vector, int], tuple[int, int]] = choose_axis,
) -> MovementResult:
    """Request at most one hop, retaining fractional speed and existing movement credit."""
    for value in (budget, budget_den, phase):
        checked(value)
    if budget_den <= 0 or not 0 <= budget < checked_work(speed_cap * budget_den) or phase < 0:
        raise ValueError("invalid movement budget, phase or speed cap")
    speed_num, speed_den = speed_ratio(momentum, mass, momentum_den, speed_cap)
    common = checked_work((budget_den // bounded_gcd(budget_den, speed_den)) * speed_den)
    total = checked_work(
        checked_work(budget * (common // budget_den)) + checked_work(speed_num * (common // speed_den))
    )
    threshold = checked_work(speed_cap * common)
    if total < threshold:
        numerator, denominator = reduced_ratio(total, common)
        return MovementResult(-1, phase, numerator, denominator)
    direction, next_phase = select_axis(momentum, phase)
    numerator, denominator = reduced_ratio(total - threshold, common)
    return MovementResult(direction, next_phase, numerator, denominator)


class MovementRule(Protocol):
    def __call__(
        self,
        momentum: Vector,
        budget: int,
        phase: int,
        *,
        speed_cap: int,
        mass: int = 1,
        momentum_den: int = 1,
        budget_den: int = 1,
    ) -> MovementResult: ...


def choose_balanced_axis(momentum: Vector, phase: int) -> tuple[int, int]:
    """Interleave cardinal hops with bounded prefix error and one phase register.

    First distribute x versus yz, then y versus z among the remaining hops.
    For fixed momentum starting at phase zero, x differs from its ideal hop
    count by less than one node; y and z differ by less than two nodes.
    Axis ordering is explicit: this is not exact rotational invariance.
    """
    if len(momentum) != 3:
        raise ValueError("exactly three momentum components are required")
    for value in (*momentum, phase):
        checked(value)
    if phase < 0:
        raise ValueError("nonnegative phase required")
    ax, ay, az = (abs(value) for value in momentum)
    total = checked(ax + ay + az)
    if total == 0:
        return -1, phase
    slot = phase % total
    after = checked(slot + 1)
    before_x = checked_work(slot * ax) // total
    after_x = checked_work(after * ax) // total
    if after_x > before_x:
        direction = PLUS_X if momentum[0] >= 0 else MINUS_X
    else:
        remaining = checked(ay + az)
        other_slot = slot - before_x
        before_y = checked_work(other_slot * ay) // remaining
        after_y = checked_work((other_slot + 1) * ay) // remaining
        if after_y > before_y:
            direction = PLUS_Y if momentum[1] >= 0 else MINUS_Y
        else:
            direction = PLUS_Z if momentum[2] >= 0 else MINUS_Z
    return direction, after % total


def advance_balanced_movement(
    momentum: Vector,
    budget: int,
    phase: int,
    *,
    speed_cap: int,
    mass: int = 1,
    momentum_den: int = 1,
    budget_den: int = 1,
) -> MovementResult:
    """Use the shared speed budget with balanced rather than grouped axis steps."""
    return advance_movement(
        momentum,
        budget,
        phase,
        speed_cap=speed_cap,
        select_axis=choose_balanced_axis,
        mass=mass,
        momentum_den=momentum_den,
        budget_den=budget_den,
    )
