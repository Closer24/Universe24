"""Fixed-state balanced neighbor routing and exact fractional movement credit."""

from event_universe.core.disturbance_state import (
    CARDINAL_OFFSETS,
    MAX_PORTS,
    MAX_VALUE,
    Address3,
    CostMeter,
    bounded,
)
from event_universe.core.integer import ceil_div, checked_work, dot_product

from .ratios import Ratio, gcd


def direction_weights(
    direction: tuple[int, ...],
    offsets: tuple[Address3, ...],
    policy: str,
    meter: CostMeter,
) -> tuple[int, ...]:
    """Map a local vector to explicitly selected directional affinities.

    Positive-dot is an affinity policy, not an assertion of exact straight-line
    velocity on arbitrary graphs. The cardinal policy preserves the old tariff
    and six-axis routing exactly.
    """
    if len(direction) != 3 or not 2 <= len(offsets) <= MAX_PORTS:
        raise ValueError("directional routing requires a vector and bounded port list")
    for component in direction:
        bounded(component)
    if policy == "cardinal":
        if offsets != CARDINAL_OFFSETS:
            raise ValueError("cardinal direction policy requires the default six offsets")
        return (
            max(0, direction[0]),
            max(0, -direction[0]),
            max(0, direction[1]),
            max(0, -direction[1]),
            max(0, direction[2]),
            max(0, -direction[2]),
        )
    if policy != "positive-dot":
        raise ValueError("unknown transport direction policy")
    scores = []
    for offset in offsets:
        if len(offset) != 3 or any(
            type(value) is not int or value not in (-1, 0, 1) for value in offset
        ):
            raise ValueError("routing offsets require three bounded unit components")
        meter.charge("evaluate")
        scores.append(bounded(max(0, dot_product(direction, offset))))
    return tuple(scores)


def balanced_port(
    weights: tuple[int, ...], counts: tuple[int, ...], previous: tuple[int, ...], meter: CostMeter
) -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    if (
        not 2 <= len(weights) <= MAX_PORTS
        or len(counts) != len(weights)
        or len(previous) != len(weights)
    ):
        raise ValueError("balanced routing requires matching bounded fixed lanes")
    meter.charge("route", ceil_div(checked_work(512 * len(weights)), 6))
    factor = 0
    for weight in weights:
        if weight < 0:
            raise ValueError("negative routing weight")
        factor = gcd(factor, bounded(weight))
    if not factor:
        raise ValueError("balanced routing requires a nonzero direction")
    reduced = tuple(weight // factor for weight in weights)
    current = list(counts if previous == reduced else (0,) * len(weights))
    if any(type(n) is not int or n < 0 or n > w for n, w in zip(current, reduced, strict=True)):
        raise ValueError("invalid balanced routing counters")
    if all(n == w for n, w in zip(current, reduced, strict=True)):
        current = [0] * len(weights)
    selected = -1
    for port, weight in enumerate(reduced):
        if not weight or current[port] == weight:
            continue
        if selected < 0 or checked_work((2 * current[port] + 1) * reduced[selected]) < checked_work(
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
