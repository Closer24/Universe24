"""The composed paces, the law's two functions of the content (ALGEBRA.md #the-paces; PC-S1, the owner's approved sentence K-S4 in pc1's form, 2026-10-25): the clock p_0(c) = Gamma (1 - 1 / Gamma)^c to the unit, the exact power rounded half up once, by the law's carried division at the resolution Gamma^2: N_0 = Gamma^3 with the remainder r_0 = Gamma div 2, N(c + 1) Gamma + r(c + 1) = N(c) (Gamma - 1) + r(c), one carried division per content at the wall Gamma, the pace rounded(N, Gamma^2) half up, bit for bit the exact power at every content to the edge; a hill (c < 0) by the inverse factors, N Gamma + r over Gamma - 1; the Link's pace the clock twice, p_a = p_0^2 div Gamma rounded once (h N = 1, the ruler goes with the clock), the clock the primary number and its square derived, so no act takes a root and every integer stays within the width (40 bits at Gamma 1,000; the former running fraction of 4.0, the one transient beyond the former width, kept by name and gone). The loader certifies the margin once per Gamma, one pass to the frozen content, and refuses by name where the half lies within one of N (`certified`). The table per Gamma holds each content's clock once, two sides, the hollows (c >= 0) and the hills (c < 0); the vectorised entries look every Node's content up in the array's own kind. The one rounding of a coefficient (`rounded`, half up on the magnitude with the sign after, odd) and the integer sine of a pair (`sine_den`) stand beside. The Link's pace rounds to 0 first, where p_0^2 falls below Gamma div 2 (`frozen_content`, the horizon's content)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cache
from typing import Any

import numpy as np

from event_universe.core import acts
from event_universe.core.rule3 import half, largest_below


def rounded(numerator: Any, wall: Any) -> Any:
    """The one rounding of a coefficient of the Node (the one rule of the remainder; the former plain half-up rounding, the same integers at a numerator of either sign but a negative odd one, struck 2026-10-26 under NL-S1, its one read, the tension's mean, spelt as the division act's quotient in readings.link_factors; the former odd_rounded kept by name): the numerator over the wall rounded half up on the magnitude with the sign after, one carried division from the half wall at the doubled wall, the carry mirrored (acts.mirror, the former rule3.mirrored kept by name) where the numerator is negative, odd at every integer, no remainder kept, a pace and a factor being coefficients of the interval and no level; integers or whole-board arrays alike, the mirror in the numerator's own kind."""
    signed = np.asarray(numerator)
    kind, below = signed.dtype, signed < 0
    negative = below.astype(kind) if below.ndim else int(below)
    carry = wall + negative * (acts.mirror(wall, wall + wall, 1) - wall)
    return acts.divide(numerator + numerator, wall + wall, carry)[0]


def sine_den(num: int, den: int, scale: int = 1) -> int:
    """The integer sine of a pair at a scale, scale den sin omega to the unit: the largest x with x^2 <= scale^2 (den^2 - num^2), one search on the whole product (`rule3.largest_below`), no root and no division before the search; 0 at |num| = den, a pair at the gap 0."""
    return largest_below(scale * scale * (den * den - num * num))


@dataclass
class Side:
    """One side of the clock's table at one Gamma, the hollows or the hills: the clocks and the Links' paces found so far by the content's size |c|, and the carried division's state at the next content, N at the resolution Gamma^2 with its remainder, the numerator's factor and the wall."""

    factor: int
    wall: int
    scaled: int
    carry: int
    clocks: list[int] = field(default_factory=list)
    links: list[int] = field(default_factory=list)
    numerators: list[int] = field(default_factory=list)

    def reach(self, gamma: int, size: int) -> None:
        """The side filled through the size |c|: the pace rounded(N, Gamma^2) half up, the Link's pace from it, p_0^2 over Gamma rounded once, then one carried division per content."""
        while len(self.clocks) <= size:
            self.numerators.append(int(self.scaled))
            pace = int(rounded(self.scaled, gamma * gamma))
            self.clocks.append(pace)
            self.links.append(int(rounded(pace * pace, gamma)))
            scaled, carry = acts.divide(self.scaled * self.factor, self.wall, self.carry)
            self.scaled, self.carry = int(scaled), int(carry)

    def undecided(self, gamma: int, size: int) -> list[int]:
        """The contents through the size where the half lies within one of N, rounded(N - 1) != rounded(N + 1) at the resolution Gamma^2: none at a certified Gamma."""
        self.reach(gamma, size)
        found, scaled, carry = [], gamma * gamma * gamma, int(half(self.wall))
        for content in range(size + 1):
            if rounded(scaled - 1, gamma * gamma) != rounded(scaled + 1, gamma * gamma):
                found.append(content)
            scaled, carry = (int(x) for x in acts.divide(scaled * self.factor, self.wall, carry))
        return found


@cache
def sides(gamma: int) -> tuple[Side, Side]:
    """The table at one Gamma, the hollows' side and the hills', each starting at N_0 = Gamma^3 with its remainder at the half wall, the hollows by Gamma - 1 over Gamma per content and the hills by Gamma over Gamma - 1."""
    return (
        Side(gamma - 1, gamma, gamma * gamma * gamma, int(half(gamma))),
        Side(gamma, gamma - 1, gamma * gamma * gamma, int(half(gamma - 1))),
    )


@cache
def certified(gamma: int) -> int:
    """The loader's certificate once per Gamma: one pass to the frozen content on the hollows' side, refused by name where a content is undecided (the half within one of N); the frozen content returned."""
    frozen = frozen_content(gamma)
    undecided = sides(gamma)[0].undecided(gamma, frozen)
    if undecided:
        raise ValueError(
            f"the clock at Gamma {gamma} is undecided at the contents {undecided[0]}: the paces are refused"
        )
    return frozen


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


def numerator_of(gamma: int, contents: Any) -> Any:
    """The clock's numerator N(c) at every Node (the blind build of the carried paces): the table's scaled power before its rounding."""
    return looked_up(lambda side: side.numerators, gamma, contents)
