"""Bounded local wait schedules shared by record and spatial output owners."""

from .disturbance_state import DirectionalDelayDefinition, bounded
from .integer import ceil_div, checked_work


def cycle_timing(cost: int, budget: int, link_ticks: int) -> tuple[int, int]:
    """Original scalar timing; the base link transit is counted exactly once."""
    if min(bounded(budget), bounded(link_ticks)) < 1 or bounded(cost) < 0:
        raise ValueError("invalid cost, normal budget, or fixed link time")
    cycles = max(1, ceil_div(cost, budget))
    return bounded(checked_work((cycles - 1) * link_ticks)), bounded(checked_work(cycles * link_ticks))


def directional_timing(
    cost: int,
    budget: int,
    link_ticks: int,
    definition: DirectionalDelayDefinition,
    ports: tuple[int, ...],
    *,
    weights: tuple[int, ...] | None = None,
) -> tuple[int, int, tuple[int, ...]]:
    """Return common commit wait, next-cycle interval and six output waits.

    The common prefix is the shortest participating output wait. An atomic transaction
    commits once after this prefix; other outputs then wait in fixed cell-owned
    dispatch slots. The cell starts no new batch before this batch drains.
    Durations round upward explicitly; they are not conserved inventory.
    """
    extra, _ = cycle_timing(cost, budget, link_ticks)
    weights = definition.weights if weights is None else weights
    if len(weights) != 6 or any(bounded(weight) < 0 for weight in weights):
        raise ValueError("directional timing needs six nonnegative bounded weights")
    waits = tuple(
        bounded(ceil_div(checked_work(extra * weight), definition.denominator)) for weight in weights
    )
    for port in ports:
        if type(port) is not int or not 0 <= port < 6:
            raise ValueError("directional delay port must be between zero and five")
    common = min((waits[port] for port in ports), default=min(waits))
    latest = max((common, *(waits[port] for port in ports)))
    return common, bounded(checked_work(latest + link_ticks)), waits
