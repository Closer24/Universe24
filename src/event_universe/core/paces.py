"""The composed paces, the law's two functions of the content and the two factors they scale (ALGEBRA.md #the-paces; the principle C, the same clock and the same ruler for every act, the owner's word of 2026-10-01, 17:02 and 17:10): the clock p_0(c) = Gamma (1 - 1 / Gamma)^c to the unit, in exact integers (Gamma - 1)^c over Gamma^(c - 1) with one division rounded half up (c = 0 gives Gamma; a negative content, a hill, the same fraction turned over, Gamma^(1 - c) over (Gamma - 1)^(-c)), and the Link's pace the clock twice, p_a(c) = p_0(c)^2 / Gamma rounded once (h N = 1, the ruler goes with the clock), the clock the primary number and its square derived, so no act takes a root; the group law p_0(c_1 + c_2) = p_0(c_1) p_0(c_2) / Gamma exact in the rationals and within the roundings' floor here (one and a half units on the clock, four and a half on the Link's pace). Each value is computed exactly once per (Gamma, content) in the run and kept in a memo like the loader's constants, cleared per run (`clear_memo`), no table in any file and no number here: per Gamma two sides, the hollows (c >= 0) and the hills (c < 0), each filled lazily through the largest size |c| seen by a running fraction, the numerator and the wall each grown by one factor per content (Gamma - 1 and Gamma for a hollow, Gamma and Gamma - 1 for a hill) with one rounded division per content, bit for bit the independent power rounded once (`clock_alone`, the oracle) at a fortieth of its cost over a deep well; the vectorised entries look every Node's content up through the memo in the array's own kind. The write's factor on a held row's source, the source per proper volume and the act per proper interval booked once on each, p_x p_y p_z / (p_0 Gamma^2) on a count and p_x p_y p_z / (p_0^2 Gamma) on a Wronskian, which carries one N of its own (the mathematician's vector form, #1572 comment 5933195756; the advisor's rule, #1563 comment 5933967219), is one rounding of the count times the three paces over the one wall, the product exact in Python's integers beyond the width (the advisor's and the mathematician's lines, #1563 comments 5959617991 and 5960096992 and #1572 comment 5959853571: one write, one act, a symmetric function of the three axes), and the turn's factor p_0 / Gamma on the angle one division rounded half up at the read, each 1 at the vacuum's paces. In the rationals the clock is above 0 at every content, so the guard's lower side, a pace below 0, is never met and a collapse ends in a frozen clock; in the integers the Link's pace rounds to 0 first, where p_0^2 falls below Gamma div 2, at the content about (Gamma div 2) ln(2 Gamma), and the clock itself where Gamma (1 - 1 / Gamma)^c falls below 1 / 2, at about Gamma ln(2 Gamma) (`frozen_content` computes the first; 28,206 and 56,352 at Gamma 6,000, 3,793 and 7,598 at 1,000, both beyond 3 Gamma): the loader refuses a content at or beyond the Link's zero as it refuses the pace 0 today, and the guard's upper side on the squares stands for a hill as it stands."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cache
from typing import Any

import numpy as np

from event_universe.core.rule3 import division_forward


def rounded(numerator: Any, wall: Any) -> Any:
    """The numerator over the wall rounded half up in one division of the division act, (2 numerator + wall) div (2 wall), the count's own rounding (share.quanta_of, (share + W_c div 2) div W_c) in the one act, no remainder kept: a pace and a factor are coefficients of the interval and no level; integers or whole-board arrays alike."""
    return division_forward(numerator + numerator, wall + wall, wall)[0]


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
    """The least content at which the Link's pace rounds to 0 at Gamma, p_0^2 below Gamma div 2, about (Gamma div 2) ln(2 Gamma), before the clock's own zero at about Gamma ln(2 Gamma) (28,206 and 56,352 at Gamma 6,000; 3,793 and 7,598 at 1,000): the content from which the loader refuses, as it refuses the pace 0 today; found by doubling and halving on the clock's own power (`clock_alone`), the memo untouched."""
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


def looked_up(function: Callable[[int, int], int], gamma: int, contents: Any) -> Any:
    """A function of the content at every Node: a scalar content as it is; an array looked up through the memo and spread back over the Nodes in the array's own kind (the hardware's integers or Python's, the loader's choice by the width), on every value from its least to its largest where that range is narrower than the board (one table indexed by the content, no sort) and on its distinct values otherwise (a sparse spread, sorted once); the same integers either way."""
    values = np.asarray(contents)
    if values.ndim == 0:
        return function(gamma, int(values))
    low, high = int(values.min()), int(values.max())
    if high - low < values.size:
        table = [function(gamma, c) for c in range(low, high + 1)]
        return np.array(table, dtype=values.dtype)[(values - low).astype(int)]
    distinct, inverse = np.unique(values, return_inverse=True)
    table = [function(gamma, int(c)) for c in distinct.tolist()]
    return np.array(table, dtype=values.dtype)[np.asarray(inverse).reshape(values.shape)]


def clock_of(gamma: int, contents: Any) -> Any:
    """The clock's pace at every Node from the Node's content, `clock` through the memo (the read's p_0, whose square enters the self coefficient S)."""
    return looked_up(clock, gamma, contents)


def link_pace_of(gamma: int, contents: Any) -> Any:
    """The Link's pace at every Node from the content read on the Link, `link_pace` through the memo (the read's p_a per Port, whose square enters R_ij; the share's weights and the least pace read the same)."""
    return looked_up(link_pace, gamma, contents)


def node_paces(gamma: int, contents: Any) -> tuple[Any, Any]:
    """The two paces of a Node at every Node from its content, (p_0, p_i): the clock and the Node's pace, the clock twice (`clock_of`, `link_pace_of`), the integers Rule3's coefficients are read from (core/rule3.coefficients); (Gamma, Gamma) at the vacuum."""
    return clock_of(gamma, contents), link_pace_of(gamma, contents)


def axis_pace(pace: Any, gamma: int, ahead: Any, behind: Any) -> Any:
    """A Node's pace along one axis, p_a(i) = p_i (q_(i, i+a) + q_(i, i-a)) / (2 Gamma) rounded once: the Node's pace p_i times the mean of its two a-Links' factors q = Gamma - t from the Links' tensions `ahead` (through the +a Port) and `behind` (through the -a Port), one reading per axis through its two Ports, as the tension is the mean of its two ends' parts; the ruler of the axis is h_a = p_0 / p_a (ALGEBRA.md #the-paces, The write per proper volume and per proper interval, the vector form); p_i with no tension."""
    return rounded(pace * (gamma + gamma - ahead - behind), gamma + gamma)


def write_factor(count: Any, p_x: Any, p_y: Any, p_z: Any, p_0: Any, gamma: int, intervals: int) -> Any:
    """A held row's write per proper volume and per proper interval (the advisor's rule, #1563 comment 5933967219: the source per proper volume, 1 / (h_x h_y h_z) = p_x p_y p_z / p_0^3, and the act per proper interval, N = p_0 / Gamma, booked once on each): the source scaled by N^intervals p_x p_y p_z / p_0^3, the product of the three axes' rulers over the clock (the vector form; a count source, the form D of the pace-act holders, takes two proper-interval powers, N^2 / h^3 = p_x p_y p_z / (p_0 Gamma^2), a Wronskian source, the sign's row, carrying one N of its own, takes one, N / h^3 = p_x p_y p_z / (p_0^2 Gamma), the caller choosing by the holder's declared act), booked as one rounding half up of the count times p_x p_y p_z over the one wall Gamma^intervals p_0^(3 - intervals), no remainder, a symmetric function of the three paces to the bit, so that a lay with the cube's symmetry keeps its 48 images under the write (ALGEBRA.md, The write per proper volume and per proper interval and The cube's symmetry; the body round's reading departed at the interval 516 under the three roundings in the order x, y, z, #1563 comment 5959617991 and #1572 comment 5959853571); the product in Python's integers, exact beyond the width (at the amplitude bound the numerator 2 A^2 P^3 passes 63 bits on every shipped universe, 3.7 x 10^19 at Gamma 6,000: the loader's width gate holds the factor's value, the booking times at most (P / Gamma)^3, inside the width, `derived.write_rooms`), and the value back in the count's own kind; the count itself at the vacuum's paces (every factor 1); at a frozen clock, p_0 at 0, the clock's wall is 1 as the share's is, the numerator 0 with the Link's pace."""
    clock = p_0 + (p_0 == 0)
    wall = gamma**intervals * clock ** (3 - intervals)
    kind = np.asarray(count).dtype  # the count's own kind, the run's
    return np.asarray(rounded(np.asarray(count, dtype=object) * p_x * p_y * p_z, wall)).astype(kind)


def turn_factor(angle: Any, p_0: Any, gamma: int) -> Any:
    """The turn per proper interval: the sign's level read into a plane's phase scaled by p_0 / Gamma, one division rounded half up at the read; the angle itself at the vacuum's clock."""
    return rounded(angle * p_0, gamma)


def clear_memo() -> None:
    """The memo cleared at a run's start, so that the paces are computed again once per (Gamma, content) within the run and nothing is kept between runs."""
    sides.cache_clear()
