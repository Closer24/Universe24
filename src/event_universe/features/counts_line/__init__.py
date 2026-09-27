"""The count's line: T c_next + r' = T c_now + SUM over the six Ports of F_ij + r, Rule3 for the family of clicks at every Node with the record's current as its read and the quantum's norm T as its wall, F_ij = weight (now_i before_j - before_i now_j) the current into Node i from its neighbour j, the booking of the record's levels at the Link's two ends (the pair's second level added), the click the division's carry of one whole quantum, the inverse the same line with the current reversed (ALGEBRA.md 9.121 item 3, 9.119 item 1, 9.57 (1))."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.register import Declaration
from event_universe.core.rule3 import rule3

Vector = tuple[Any, Any, Any]
PORTS = 6  # a Node's six Ports, the lattice's own integer (Rule3's 6)
PRODUCTS = 2  # the current's two products, now_i before_j and before_i now_j
PAIRS = 2  # a record's level pairs, (now, before) and the second level's, each level bounded by A


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
    """The line's writes: the count and its remainder after the act, and the inflow per axis it read, the current into the Node through the axis's two Ports."""

    count: Any
    remainder: Any
    net: Vector


def current(weight: int, here: Levels, there: Levels) -> Any:
    """The current into the Node here from the Node there through their Link, the booking weight (now_i before_j - before_i now_j), positive inward as the ladder reads it, the second level's term added on a pair (ALGEBRA.md 9.121 item 2 (c), 9.50 (13))."""
    found = here.now * there.before - here.before * there.now
    if here.im_now is not None and there.im_now is not None:
        found = found + here.im_now * there.im_before - here.im_before * there.im_now
    return weight * found


def bound(term: CountTerm) -> int:
    """The largest total the line reaches at a Node whose levels stand at A: one current per Port, the weight times the two products of two levels at A on each level pair, T (most + 1) and the remainder below T (ALGEBRA.md 9.57 (2))."""
    current_bound = term.weight * PRODUCTS * PAIRS * term.amplitude * term.amplitude
    return PORTS * current_bound + term.norm * (term.most + 1) + term.norm


def check(term: CountTerm, start: CountStart) -> None:
    """The refusals by name: T and the weight from 1, the direction +1 or -1, six Links, the total within int64."""
    if term.norm < 1 or term.weight < 1:
        raise ValueError(f"the count's line needs T = {term.norm} and the weight {term.weight} from 1")
    if start.direction not in (1, -1):
        raise ValueError(f"the count's line runs in the direction +1 or -1, got {start.direction}")
    if len(start.links) != PORTS:
        raise ValueError(f"the count's line reads six Links, one per Port, got {len(start.links)}")
    if bound(term) > MAX_WORK_INT:
        raise ValueError(
            f"the count's line at A = {term.amplitude}, the weight {term.weight}, T = {term.norm} and "
            f"the count up to {term.most} reaches the total {bound(term)}, beyond int64: the run is refused"
        )


def apply(term: CountTerm, start: CountStart, own: None = None) -> CountWrites:
    """The primitive at (ii), bound to the loop (the line keeps no own record, `own` is None): the inflow per axis, the current into the Node through its +a and -a Ports, read by Rule3 with the coefficient sigma on each axis and T on the count over the wall T (ALGEBRA.md 9.121 item 3)."""
    check(term, start)
    net = []
    for axis in range(3):
        through_plus = current(term.weight, start.here, start.links[2 * axis])
        through_minus = current(term.weight, start.here, start.links[2 * axis + 1])
        net.append(through_plus + through_minus)
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
    name="the count's line",
    place="(ii)",
    reads=("the record's levels at the Node and across its six Ports", "T", "the current's weight"),
    writes=("the count at a Node", "the count's remainder"),
    function=apply,
    section="9.121 item 3; 9.119 item 1; 9.57 (1)",
    word="after the step",
)
