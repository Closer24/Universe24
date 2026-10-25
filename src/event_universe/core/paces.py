"""The composed paces, the law's two functions of the content (ALGEBRA.md #the-paces; K-S4, the owner's approved sentence built 2026-10-25): the clock p_0(c) = Gamma (1 - 1 / Gamma)^c to the unit by ONE carried division per content, p_0(c + 1) = (p_0(c) (Gamma - 1) + r_c) div Gamma with the remainder r carried in [0, Gamma) and started at the half wall (the engine's rounding), Gamma at c = 0; a negative content, a hill, the same act turned over, p_0(c - 1) = (p_0(c) Gamma + r) div (Gamma - 1); the Link's pace the clock twice, p_a(c) = p_0(c)^2 div Gamma rounded once (h N = 1, the ruler goes with the clock), the clock the primary number and its square derived, so no act takes a root and every integer stays within the width (the memo's running fraction of 4.0, the one transient beyond 128 bits, is gone). The table per Gamma holds each content's clock and remainder once, two sides, the hollows (c >= 0) and the hills (c < 0); the vectorised entries look every Node's content up in the array's own kind. The rounding of a coefficient (`rounded`, half up) and of a signed one (`odd_rounded`, half away from zero), and the integer sine of a pair (`sine_den`) stand beside. The Link's pace rounds to 0 first, where p_0^2 falls below Gamma div 2 (`frozen_content`, the horizon's content): the Node there is read by no Link and clicks nothing."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cache
from typing import Any

import numpy as np

from event_universe.core.rule3 import division_forward, half, largest_below


def rounded(numerator: Any, wall: Any) -> Any:
    """The numerator over the wall rounded half up in one division of the division act, (2 numerator + wall) div (2 wall), no remainder kept: a pace and a factor are coefficients of the interval and no level; integers or whole-board arrays alike."""
    return division_forward(numerator + numerator, wall + wall, wall)[0]


def odd_rounded(numerator: Any, wall: Any) -> Any:
    """The numerator over the wall rounded half away from zero, the law's rounding of a signed coefficient in one division of the division act: `rounded`'s carry, the wall, on a numerator at or above 0 and the carry's ones' complement at the doubled wall, wall - 1, on a numerator below 0, bit for bit sign(x) rounded(|x|, wall), odd at every integer; integers or whole-board arrays alike, the complement in the numerator's own kind."""
    signed = np.asarray(numerator)
    kind, below = signed.dtype, signed < 0
    complemented = below.astype(kind) if below.ndim else int(below)
    return division_forward(numerator + numerator, wall + wall, wall - complemented)[0]


def sine_den(num: int, den: int, scale: int = 1) -> int:
    """The integer sine of a pair at a scale, scale den sin omega to the unit: the largest x with x^2 <= scale^2 (den^2 - num^2), one search on the whole product (`rule3.largest_below`), no root and no division before the search; 0 at |num| = den, a pair at the gap 0."""
    return largest_below(scale * scale * (den * den - num * num))


@dataclass
class Side:
    """One side of the clock's table at one Gamma, the hollows or the hills: the clocks and the Links' paces found so far by the content's size |c|, and the carried division's state at the next content, its clock and its remainder, the numerator's factor and the wall."""

    factor: int
    wall: int
    pace: int
    carry: int
    clocks: list[int] = field(default_factory=list)
    links: list[int] = field(default_factory=list)

    def reach(self, gamma: int, size: int) -> None:
        """The side filled through the size |c|, one carried division per content, and the Link's pace from each clock, p_0^2 over Gamma rounded once."""
        while len(self.clocks) <= size:
            self.clocks.append(self.pace)
            self.links.append(int(rounded(self.pace * self.pace, gamma)))
            pace, carry = division_forward(self.pace * self.factor, self.wall, self.carry)
            self.pace, self.carry = int(pace), int(carry)


@cache
def sides(gamma: int) -> tuple[Side, Side]:
    """The table at one Gamma, the hollows' side and the hills', each starting at the vacuum's clock Gamma with its remainder at the half wall, the hollows by Gamma - 1 over Gamma per content and the hills by Gamma over Gamma - 1."""
    return (
        Side(gamma - 1, gamma, gamma, int(half(gamma))),
        Side(gamma, gamma - 1, gamma, int(half(gamma - 1))),
    )


def side_of(gamma: int, content: int) -> Side:
    """The side of the table the content falls on, the hollows' at or above 0 and the hills' below, filled through the content's size."""
    hollows, hills = sides(gamma)
    side = hills if content < 0 else hollows
    side.reach(gamma, abs(content))
    return side


def clock(gamma: int, content: int) -> int:
    """The clock's pace at a Node of content c, p_0 = Gamma (1 - 1 / Gamma)^c to the unit by the carried division (`Side.reach`)."""
    return side_of(gamma, content).clocks[abs(content)]


def link_pace(gamma: int, content: int) -> int:
    """The Link's pace at the content c, the clock twice: p_a = p_0^2 div Gamma rounded once from the clock's integer, Gamma at the vacuum; the pace of every Link of a Node from the Node's own content, before the Link's own tension enters."""
    return side_of(gamma, content).links[abs(content)]


def frozen_content(gamma: int) -> int:
    """The least content at which the Link's pace rounds to 0 at Gamma, p_0^2 below Gamma div 2 (the horizon's content, about (Gamma div 2) ln(2 Gamma)): the table walked from the vacuum to the first 0."""
    hollows = sides(gamma)[0]
    content = 0
    while True:
        hollows.reach(gamma, content)
        if hollows.links[content] == 0:
            return content
        content += 1


def looked_up(found: Callable[[Side], list[int]], gamma: int, contents: Any) -> Any:
    """One of the table's two functions of the content at every Node (`found`, a side's clocks or its Links' paces): a scalar content as it is; an empty array as it is; an array looked up through the table and spread back over the Nodes in the array's own kind, on every value from its least to its largest where that range is narrower than the board and on its distinct values otherwise; the same integers either way."""
    values = np.asarray(contents)
    if values.ndim == 0:
        return found(side_of(gamma, int(values)))[abs(int(values))]
    if values.size == 0:
        return values
    low, high = int(values.min()), int(values.max())
    if high - low < values.size:
        hollows, hills = sides(gamma)
        hollows.reach(gamma, max(high, 0))
        hills.reach(gamma, max(-low, 0))
        below = found(hills)[-low : max(-high - 1, 0) : -1] if low < 0 else []
        table = below + found(hollows)[max(low, 0) : high + 1]
        return np.array(table, dtype=values.dtype)[(values - low).astype(int)]
    distinct, inverse = np.unique(values, return_inverse=True)
    table = [found(side_of(gamma, int(c)))[abs(int(c))] for c in distinct.tolist()]
    return np.array(table, dtype=values.dtype)[np.asarray(inverse).reshape(values.shape)]


def clock_of(gamma: int, contents: Any) -> Any:
    """The clock's pace at every Node from the Node's content (`clock` through the table)."""
    return looked_up(lambda side: side.clocks, gamma, contents)


def link_pace_of(gamma: int, contents: Any) -> Any:
    """The Link's pace at every Node from the content read on the Link (`link_pace` through the table)."""
    return looked_up(lambda side: side.links, gamma, contents)
