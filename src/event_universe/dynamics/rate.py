"""Cardinal step rate, distinct from geometric displacement speed."""

from typing import NamedTuple

from event_universe.core.state import Vector, checked, checked_work


class StepRate(NamedTuple):
    numerator: int
    denominator: int


def step_rate(momentum: Vector, speed_cap: int) -> StepRate:
    """Retain the existing one-hop capacity law in one reusable location.

    For constant unsaturated momentum on unit links, a complete digital cycle
    has displacement momentum/speed_cap per tick. The numerator counts steps,
    not Euclidean speed. Saturation is an anisotropic lattice rule, not SR.
    """
    if len(momentum) != 3:
        raise ValueError("exactly three momentum components are required")
    for value in (*momentum, speed_cap):
        checked(value)
    if speed_cap <= 0:
        raise ValueError("positive speed cap required")
    demand = checked_work(sum(abs(value) for value in momentum))
    return StepRate(min(demand, speed_cap), speed_cap)
