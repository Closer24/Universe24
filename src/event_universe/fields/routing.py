"""Fixed-state balanced neighbor routing and exact fractional movement credit."""

from event_universe.core.disturbance_state import MAX_VALUE, CostMeter, bounded
from event_universe.core.integer import checked_work

from .ratios import Ratio, gcd


def balanced_port(
    weights: tuple[int, ...],
    counts: tuple[int, ...],
    previous: tuple[int, ...],
    meter: CostMeter,
    loads: tuple[int, ...] | None = None,
) -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    """Select the next lane of the reduced weight cycle.

    Every lane is used exactly its reduced weight per cycle, so directional
    ratios are exact. Without loads the least-served lane goes first; with
    loads the cheapest eligible lane goes first and the cycle only fixes the
    order within it.
    """
    if len(weights) != 6 or len(counts) != 6 or len(previous) != 6:
        raise ValueError("balanced routing requires six fixed lanes")
    if loads is not None and len(loads) != 6:
        raise ValueError("least-delay routing requires six lane loads")
    meter.charge("route", 512)
    factor = 0
    for weight in weights:
        if weight < 0:
            raise ValueError("negative routing weight")
        factor = gcd(factor, bounded(weight))
    if not factor:
        raise ValueError("balanced routing requires a nonzero direction")
    reduced = tuple(weight // factor for weight in weights)
    current = list(counts if previous == reduced else (0,) * 6)
    if any(type(n) is not int or n < 0 or n > w for n, w in zip(current, reduced, strict=True)):
        raise ValueError("invalid balanced routing counters")
    if all(n == w for n, w in zip(current, reduced, strict=True)):
        current = [0] * 6
    selected = -1
    for port, weight in enumerate(reduced):
        if not weight or current[port] == weight:
            continue
        if selected < 0:
            selected = port
            continue
        if loads is not None and loads[port] != loads[selected]:
            if loads[port] < loads[selected]:
                selected = port
            continue
        if checked_work((2 * current[port] + 1) * reduced[selected]) < checked_work(
            (2 * current[selected] + 1) * weight
        ):
            selected = port
    current[selected] += 1
    return selected, tuple(current), reduced


def rate_credit(
    numerator: int, denominator: int, rate: int, divisor: int, meter: CostMeter
) -> tuple[bool, int, int]:
    meter.charge("route", 65536)
    if not (0 <= numerator < denominator <= MAX_VALUE):
        raise ValueError("invalid fractional movement credit")
    if not (0 <= rate <= divisor) or divisor <= 0:
        raise ValueError("movement rate must be between zero and one hop per base interval")
    total = Ratio(numerator, denominator).add(Ratio(rate, divisor))
    move = total.numerator >= total.denominator
    if move:
        total = total.add(Ratio(-1))
    return move, bounded(total.numerator), bounded(total.denominator)
