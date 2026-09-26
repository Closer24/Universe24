"""The count's line: T c_next + r' = T c_now + SUM_a (F_a^- - F_a^+) + r, Rule3 for the family of clicks at every Node with the record's current as its read and the quantum's norm T as its wall, the current through a Link the booking weight (now_i before_j - before_i now_j) of the record's levels at its two ends (the pair's second level added), the click the division's carry of one whole quantum, the inverse the same line with the current reversed (ALGEBRA.md 9.121 item 3, 9.119 item 1, 9.57 (1))."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.register import Declaration
from event_universe.core.rule3 import rule3

PORTS = ("+x", "-x", "+y", "-y", "+z", "-z")
Vector = tuple[Any, Any, Any]


@dataclass(frozen=True)
class Levels:
    """A record's levels at one Node or across one Port: now, before, and the pair's second level now and before (None on a record with one level)."""

    now: Any
    before: Any
    im_now: Any | None
    im_before: Any | None


@dataclass(frozen=True)
class CountTerm:
    """The family of clicks' declaration: T, the quantum's norm (the count's wall); the current's weight (num, 9.119 item 1 (e)); the amplitude bound A of the record's levels; the largest count."""

    norm: int
    weight: int
    amplitude: int
    most: int


@dataclass(frozen=True)
class CountStart:
    """The interval's reading after the step: the count c and its remainder r at every Node, the record's levels here and across the six Ports in the order +x, -x, +y, -y, +z, -z (the neighbour's levels as the send put them on the Link), the direction +1 forward, -1 backward."""

    count: Any
    remainder: Any
    here: Levels
    links: tuple[Levels, ...]
    direction: int


@dataclass(frozen=True)
class CountWrites:
    """The line's writes: the count and its remainder after the act, and the net current per axis it read, F_a^- - F_a^+."""

    count: Any
    remainder: Any
    net: Vector


def current(weight: int, here: Levels, there: Levels) -> Any:
    """The current from one Node to the other through the Link, the booking weight (now_i before_j - before_i now_j), the second level's term added on a pair (ALGEBRA.md 9.121 item 2 (c), 9.50 (13))."""
    found = here.now * there.before - here.before * there.now
    if here.im_now is not None and there.im_now is not None:
        found = found + here.im_now * there.im_before - here.im_before * there.im_now
    return weight * found


def bound(term: CountTerm) -> int:
    """The largest total the line reaches at a Node whose levels stand at A: six currents of weight x 4 A^2 (two levels), T (most + 1) and the remainder (ALGEBRA.md 9.57 (2))."""
    return (
        6 * term.weight * 4 * term.amplitude * term.amplitude + term.norm * (term.most + 1) + term.norm
    )


def check(term: CountTerm, start: CountStart) -> None:
    """The refusals by name: T and the weight from 1, the direction +1 or -1, six Links, the total within int64."""
    if term.norm < 1 or term.weight < 1:
        raise ValueError(f"the count's line needs T = {term.norm} and the weight {term.weight} from 1")
    if start.direction not in (1, -1):
        raise ValueError(f"the count's line runs in the direction +1 or -1, got {start.direction}")
    if len(start.links) != 6:
        raise ValueError(f"the count's line reads six Links, one per Port, got {len(start.links)}")
    if bound(term) > MAX_WORK_INT:
        raise ValueError(
            f"the count's line at A = {term.amplitude}, the weight {term.weight}, T = {term.norm} and "
            f"the count up to {term.most} reaches the total {bound(term)}, beyond int64: the run is refused"
        )


def apply(term: CountTerm, start: CountStart) -> CountWrites:
    """The primitive at (ii): the net current per axis, entering through -a less leaving through +a, read by Rule3 with the coefficient sigma on each axis and T on the count over the wall T (ALGEBRA.md 9.121 item 3)."""
    check(term, start)
    net = []
    for axis in range(3):
        leaving = current(term.weight, start.here, start.links[2 * axis])
        entering = current(term.weight, start.links[2 * axis + 1], start.here)
        net.append(entering - leaving)
    sigma = start.direction
    count, remainder = rule3(
        (sigma, sigma, sigma),
        (net[0], net[1], net[2]),
        term.norm,
        term.norm,
        start.count,
        0,
        start.remainder,
    )
    return CountWrites(count, remainder, (net[0], net[1], net[2]))


DECLARATION = Declaration(
    "the count's line",
    "(ii)",
    ("the record's levels at the Node and across its six Ports", "T", "the current's weight"),
    ("the count at a Node", "the count's remainder"),
    None,
    apply,
    "9.121 item 3; 9.119 item 1; 9.57 (1)",
    word="after the step",
)
