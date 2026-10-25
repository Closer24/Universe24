"""The composed paces, the law's two functions of the content and the two factors they scale (ALGEBRA.md #the-paces; the principle C, the same clock and the same ruler for every act, the owner's word): the clock p_0(c) = Gamma (1 - 1 / Gamma)^c to the unit, in exact integers (Gamma - 1)^c over Gamma^(c - 1) with one division rounded half up (c = 0 gives Gamma; a negative content, a hill, the same fraction turned over, Gamma^(1 - c) over (Gamma - 1)^(-c)), and the Link's pace the clock twice, p_a(c) = p_0(c)^2 / Gamma rounded once (h N = 1, the ruler goes with the clock), the clock the primary number and its square derived, so no act takes a root; the group law p_0(c_1 + c_2) = p_0(c_1) p_0(c_2) / Gamma exact in the rationals and within the roundings' floor here (one and a half units on the clock, four and a half on the Link's pace). Each value is computed exactly once per (Gamma, content) in the run and kept in a memo like the loader's constants, cleared per run (`clear_memo`), no table in any file and no number here: per Gamma two sides, the hollows (c >= 0) and the hills (c < 0), each filled lazily through the largest size |c| seen by a running fraction, the numerator and the wall each grown by one factor per content (Gamma - 1 and Gamma for a hollow, Gamma and Gamma - 1 for a hill) with one rounded division per content, bit for bit the independent power rounded once (`clock_alone`, the oracle) at a fortieth of its cost over a deep well; the vectorised entries look every Node's content up through the memo in the array's own kind. The write's factor on a held row's source, the source per proper volume and the act per proper interval booked once on each, p_x p_y p_z / (p_0 Gamma^2) on a count and p_x p_y p_z / (p_0^2 Gamma) on a Wronskian, which carries one N of its own (the mathematician's vector form; the advisor's rule), is one rounding of the count times the three paces over the one wall, the product exact in Python's integers beyond the width (the advisor's and the mathematician's lines: one write, one act, a symmetric function of the three axes), and the turn's factor p_0 / Gamma on the angle one division rounded half away from zero at the read (`odd_rounded`, the law's rounding of a signed coefficient), each 1 at the vacuum's paces; beside the rounding the units' other arithmetic, the integer sine of a pair, den sin omega to the unit by the one search (`sine_den`, row 12 of the conventions, W_rec = W_c sin omega_0). In the rationals the clock is above 0 at every content, so the guard's lower side, a pace below 0, is never met and a collapse ends in a frozen clock; in the integers the Link's pace rounds to 0 first, where p_0^2 falls below Gamma div 2, at the content about (Gamma div 2) ln(2 Gamma), and the clock itself where Gamma (1 - 1 / Gamma)^c falls below 1 / 2, at about Gamma ln(2 Gamma) (`frozen_content` computes the first; 28,206 and 56,352 at Gamma 6,000, 3,793 and 7,598 at 1,000, both beyond 3 Gamma): the loader refuses a content at or beyond the Link's zero as it refuses the pace 0, and the guard's upper side on the squares stands for a hill as it is."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cache
from typing import Any

import numpy as np

from event_universe.core.rule3 import division_forward, largest_below


def rounded(numerator: Any, wall: Any) -> Any:
    """The numerator over the wall rounded half up in one division of the division act, (2 numerator + wall) div (2 wall), the count's own rounding (share.quanta_of, (share + W_c div 2) div W_c) in the one act, no remainder kept: a pace and a factor are coefficients of the interval and no level; integers or whole-board arrays alike."""
    return division_forward(numerator + numerator, wall + wall, wall)[0]


def odd_rounded(numerator: Any, wall: Any) -> Any:
    """The numerator over the wall rounded half away from zero, the law's rounding of a signed coefficient in one division of the division act: `rounded`'s carry, the wall, on a numerator at or above 0 and the carry's ones' complement at the doubled wall, wall - 1, on a numerator below 0, (2 numerator + wall - [numerator < 0]) div (2 wall), bit for bit sign(x) rounded(|x|, wall), odd at every integer, odd_rounded(-x, wall) = -odd_rounded(x, wall), where `rounded` is not at a tie 2 x = wall mod 2 wall (the rounding derived on positive quantities, where the two are one function; the law's mirror of a carry, the complement at the wall, records.complement, deciding the negative side, 2026-10-25); no remainder kept; integers or whole-board arrays alike, the complement in the numerator's own kind."""
    signed = np.asarray(numerator)
    kind, below = signed.dtype, signed < 0  # the numerator's own kind, the sign's mask
    complemented = below.astype(kind) if below.ndim else int(below)
    return division_forward(numerator + numerator, wall + wall, wall - complemented)[0]


def sine_den(num: int, den: int, scale: int = 1) -> int:
    """The integer sine of a pair at a scale, scale den sin omega to the unit: the largest x with x^2 <= scale^2 (den^2 - num^2), one search on the whole product (`rule3.largest_below`), no root and no division before the search (ALGEBRA.md, The conventions and the units, row 12, the family's quantum, largest_below(9 T^2 (den^2 - num^2)) = W_c sin omega_0 to the unit, one root on the whole product, and row 13, the lay by the count, the level before turned by s = sin omega den; Every step derived from the law's lines, where it can be, the sine record's start largest_below(R^2 (den^2 - num^2)) div den); the units' arithmetic beside the rounding, the engine's one spelling of its sines: the standing lay's (`features/click.standing`, `invariant`), the packet's and the source's R sin Omega den at the reference scale and the transverse D sin k (`emission.laid_packet`, `emission.start_of`, `resonance.unit_weight`), the reference records' (`resonance.references_of`), the family's quantum (`loader/derived.count_wall`) and the passage's sin omega and sin k (`loader/window.passage`); 0 at |num| = den, a massless pair."""
    return largest_below(scale * scale * (den * den - num * num))


def clock_alone(gamma: int, content: int) -> int:
    """The clock's pace at one content by its own power, p_0 = Gamma (1 - 1 / Gamma)^c to the unit: Gamma (Gamma - 1)^c over Gamma^c in exact integers, the same fraction as (Gamma - 1)^c over Gamma^(c - 1), rounded half up once; Gamma at c = 0 (the vacuum, and a family that reads nothing); for a negative content, a hill, the fraction turned over, Gamma^(1 - c) over (Gamma - 1)^(-c), so that the group law p_0(c_1 + c_2) = p_0(c_1) p_0(c_2) / Gamma holds exactly in the rationals for every sign; the memo's oracle and the search's reading, computed alone and kept nowhere."""
    if content < 0:
        return int(rounded(gamma ** (1 - content), (gamma - 1) ** -content))
    return int(rounded(gamma * (gamma - 1) ** content, gamma**content))


@dataclass
class Side:
    """One side of the memo at one Gamma, the hollows or the hills: the clocks and the Links' paces found so far by the content's size |c|, and the running fraction of the next content, its numerator over its wall, each grown by its factor per content (`factors`, the numerator's and the wall's)."""

    factors: tuple[int, int]
    numerator: int
    wall: int
    clocks: list[int] = field(default_factory=list)
    links: list[int] = field(default_factory=list)

    def reach(self, gamma: int, size: int) -> None:
        """The side filled through the size |c| by the running fraction, one rounded division per content, each clock bit for bit `clock_alone`, and the Link's pace from each clock, p_0^2 over Gamma rounded once."""
        while len(self.clocks) <= size:
            pace = int(rounded(self.numerator, self.wall))
            self.clocks.append(pace)
            self.links.append(int(rounded(pace * pace, gamma)))
            self.numerator, self.wall = self.numerator * self.factors[0], self.wall * self.factors[1]


@cache
def sides(gamma: int) -> tuple[Side, Side]:
    """The memo at one Gamma, the hollows' side and the hills', each starting at the vacuum, Gamma over 1, and growing by Gamma - 1 over Gamma per content on the hollows' side and by Gamma over Gamma - 1 on the hills'."""
    return Side((gamma - 1, gamma), gamma, 1), Side((gamma, gamma - 1), gamma, 1)


def side_of(gamma: int, content: int) -> Side:
    """The side of the memo the content falls on, the hollows' at or above 0 and the hills' below, filled through the content's size."""
    hollows, hills = sides(gamma)
    side = hills if content < 0 else hollows
    side.reach(gamma, abs(content))
    return side


def clock(gamma: int, content: int) -> int:
    """The clock's pace at a Node of content c from the memo, p_0 = Gamma (1 - 1 / Gamma)^c to the unit (`clock_alone` for the fraction; `Side.reach` for the running fill)."""
    return side_of(gamma, content).clocks[abs(content)]


def link_pace(gamma: int, content: int) -> int:
    """The Link's pace at the content c from the memo, the clock twice: p_a = p_0^2 / Gamma rounded once from the clock's integer (h N = 1; the clock the primary number, its square derived, no root), Gamma at the vacuum; the pace of every Link of a Node from the Node's own content, before the Link's own tension enters."""
    return side_of(gamma, content).links[abs(content)]


def frozen_content(gamma: int) -> int:
    """The least content at which the Link's pace rounds to 0 at Gamma, p_0^2 below Gamma div 2, about (Gamma div 2) ln(2 Gamma), before the clock's own zero at about Gamma ln(2 Gamma) (28,206 and 56,352 at Gamma 6,000; 3,793 and 7,598 at 1,000): the content from which the loader refuses, as it refuses the pace 0; found by doubling and halving on the clock's own power (`clock_alone`), the memo untouched."""
    low, high = 0, 1
    while rounded(clock_alone(gamma, high) ** 2, gamma) > 0:
        high += high
    while high - low > 1:
        middle = int(division_forward(low + high, 2, 0)[0])
        if rounded(clock_alone(gamma, middle) ** 2, gamma) > 0:
            low = middle
        else:
            high = middle
    return high


def looked_up(found: Callable[[Side], list[int]], gamma: int, contents: Any) -> Any:
    """One of the memo's two functions of the content at every Node (`found`, a side's clocks or its Links' paces): a scalar content as it is; an empty array as it is; an array looked up through the memo and spread back over the Nodes in the array's own kind (the hardware's integers or Python's, the loader's choice by the width), on every value from its least to its largest where that range is narrower than the board (one table indexed by the content, the hills' side read downward through the contents below 0 and the hollows' side upward from 0, each filled through the farthest content once and sliced, no call per value and no sort) and on its distinct values otherwise (a sparse spread, sorted once); the same integers either way."""
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
    """The clock's pace at every Node from the Node's content, `clock` through the memo (the read's p_0, whose square enters the self coefficient S)."""
    return looked_up(lambda side: side.clocks, gamma, contents)


def link_pace_of(gamma: int, contents: Any) -> Any:
    """The Link's pace at every Node from the content read on the Link, `link_pace` through the memo (the read's p_a per Port, whose square enters R_ij; the share's weights and the least pace read the same)."""
    return looked_up(lambda side: side.links, gamma, contents)
