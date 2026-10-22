"""The composed paces, the law's two functions of the content and the two factors they scale (ALGEBRA.md #the-paces; the principle C, the same clock and the same ruler for every act, the owner's word): the clock p_0(c) = Gamma (1 - 1 / Gamma)^c to the unit, in exact integers (Gamma - 1)^c over Gamma^(c - 1) with one division rounded half up (c = 0 gives Gamma; a negative content, a hill, the same fraction turned over, Gamma^(1 - c) over (Gamma - 1)^(-c)), and the Link's pace the clock twice, p_a(c) = p_0(c)^2 / Gamma rounded once (h N = 1, the ruler goes with the clock), the clock the primary number and its square derived, so no act takes a root; the group law p_0(c_1 + c_2) = p_0(c_1) p_0(c_2) / Gamma exact in the rationals and within the roundings' floor here (one and a half units on the clock, four and a half on the Link's pace). Each value is computed exactly once per (Gamma, content) in the run and kept in a memo like the loader's constants, cleared per run (`clear_memo`), no table in any file and no number here: per Gamma two sides, the hollows (c >= 0) and the hills (c < 0), each filled lazily through the largest size |c| seen by a running fraction, the numerator and the wall each grown by one factor per content (Gamma - 1 and Gamma for a hollow, Gamma and Gamma - 1 for a hill) with one rounded division per content, bit for bit the independent power rounded once (`clock_alone`, the oracle) at a fortieth of its cost over a deep well; the vectorised entries look every Node's content up through the memo in the array's own kind. The write's factor on a held row's source, the source per proper volume and the act per proper interval booked once on each, p_x p_y p_z / (p_0 Gamma^2) on a count and p_x p_y p_z / (p_0^2 Gamma) on a Wronskian, which carries one N of its own (the mathematician's vector form; the advisor's rule), is one rounding of the count times the three paces over the one wall, the product exact in Python's integers beyond the width (the advisor's and the mathematician's lines: one write, one act, a symmetric function of the three axes), and the turn's factor p_0 / Gamma on the angle one division rounded half up at the read, each 1 at the vacuum's paces; beside the rounding the units' other arithmetic, the integer sine of a pair, den sin omega to the unit by the one search (`sine_den`, row 12 of the conventions, W_rec = W_c sin omega_0). In the rationals the clock is above 0 at every content, so the guard's lower side, a pace below 0, is never met and a collapse ends in a frozen clock; in the integers the Link's pace rounds to 0 first, where p_0^2 falls below Gamma div 2, at the content about (Gamma div 2) ln(2 Gamma), and the clock itself where Gamma (1 - 1 / Gamma)^c falls below 1 / 2, at about Gamma ln(2 Gamma) (`frozen_content` computes the first; 28,206 and 56,352 at Gamma 6,000, 3,793 and 7,598 at 1,000, both beyond 3 Gamma): the loader refuses a content at or beyond the Link's zero as it refuses the pace 0 today, and the guard's upper side on the squares stands for a hill as it stands."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from functools import cache
from typing import Any

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import division_forward, largest_below

COUNT_POWER = 2  # the proper-interval powers of a count's write, p_x p_y p_z / (p_0 Gamma^2)
WRONSKIAN_POWER = 1  # the proper-interval power of a Wronskian's write, p_x p_y p_z / (p_0^2 Gamma)


def rounded(numerator: Any, wall: Any) -> Any:
    """The numerator over the wall rounded half up in one division of the division act, (2 numerator + wall) div (2 wall), the count's own rounding (share.quanta_of, (share + W_c div 2) div W_c) in the one act, no remainder kept: a pace and a factor are coefficients of the interval and no level; integers or whole-board arrays alike."""
    return division_forward(numerator + numerator, wall + wall, wall)[0]


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


def node_paces(gamma: int, contents: Any) -> tuple[Any, Any]:
    """The two paces of a Node at every Node from its content, (p_0, p_i): the clock and the Node's pace, the clock twice (`clock_of`, `link_pace_of`), the integers Rule3's coefficients are read from (core/rule3.coefficients); (Gamma, Gamma) at the vacuum."""
    return clock_of(gamma, contents), link_pace_of(gamma, contents)


def axis_pace(pace: Any, gamma: int, ahead: Any, behind: Any) -> Any:
    """A Node's pace along one axis, p_a(i) = p_i (q_(i, i+a) + q_(i, i-a)) / (2 Gamma) rounded once: the Node's pace p_i times the mean of its two a-Links' factors q = Gamma - t from the Links' tensions `ahead` (through the +a Port) and `behind` (through the -a Port), one reading per axis through its two Ports, as the tension is the mean of its two ends' parts; the ruler of the axis is h_a = p_0 / p_a (ALGEBRA.md #the-paces, The write per proper volume and per proper interval, the vector form); p_i with no tension."""
    return rounded(pace * (gamma + gamma - ahead - behind), gamma + gamma)


def write_factor(
    count: Any,
    p_x: Any,
    p_y: Any,
    p_z: Any,
    p_0: Any,
    gamma: int,
    intervals: int,
    carried: bool = False,
    parts: int = 1,
) -> Any:
    """A held row's write per proper volume and per proper interval (the advisor's rule: the source per proper volume, 1 / (h_x h_y h_z) = p_x p_y p_z / p_0^3, and the act per proper interval, N = p_0 / Gamma, booked once on each): the source scaled by N^intervals p_x p_y p_z / p_0^3, the product of the three axes' rulers over the clock (the vector form; a count source, the form D of the pace-act holders, takes two proper-interval powers, N^2 / h^3 = p_x p_y p_z / (p_0 Gamma^2), a Wronskian source, the sign's row, carrying one N of its own, takes one, N / h^3 = p_x p_y p_z / (p_0^2 Gamma), the caller choosing by the holder's declared act), booked as one rounding half up of the count times p_x p_y p_z over the one wall Gamma^intervals p_0^(3 - intervals), no remainder, a symmetric function of the three paces to the bit, so that a lay with the cube's symmetry keeps its 48 images under the write (ALGEBRA.md, The write per proper volume and per proper interval and The cube's symmetry; the body round's reading departed at the interval 516 under the three roundings in the order x, y, z); the product in Python's integers, exact beyond the width (at the amplitude bound the numerator 2 A^2 P^3 passes 63 bits on every shipped universe, 3.7 x 10^19 at Gamma 6,000: the loader's width gate holds the factor's value, the booking times at most (P / Gamma)^3, inside the width, `derived.write_rooms`), and the value back in the count's own kind; the count itself at the vacuum's paces (every factor 1); at a frozen clock, p_0 at 0, the clock's wall is 1 as the share's is, the numerator 0 with the Link's pace. Under `carried`, the held row's key `factor: carried` (ALGEBRA.md, The write per proper volume and per proper interval, the clause of 2026-10-22; loader/universe.factor_of), the two terms themselves unrounded, the product and the wall (`write_factor_terms`), the factor then a coefficient of the numerator inside the held write's one carried division at the wall E_s T times this wall per Node, the write's one remainder carrying it (records.write_sources): one function, the switch at its caller. `parts` multiplies the wall inside the same rounding: the trace's three on the traceless stress of the held row's key `pressure: trace`, (3 T_aa - SUM_b T_bb) over 3 (records.write_sources), so that the traceless part takes no rounding of its own."""
    if carried:
        return write_factor_terms(count, p_x, p_y, p_z, p_0, gamma, intervals, parts)
    clock = p_0 + (p_0 == 0)
    wall = gamma**intervals * clock ** (3 - intervals) * parts
    kind = np.asarray(count).dtype  # the count's own kind, the run's
    if within_width(kind, wall, count, p_x, p_y, p_z):
        product = np.asarray(count, dtype=kind)
        for pace in (p_x, p_y, p_z):
            product = product * np.asarray(pace, dtype=kind)
        return np.asarray(rounded(product, wall)).astype(kind)
    at = np.asarray(count) != 0  # the factor is 0 where the count is: Python's integers where it is not
    if at.ndim == 0:
        return np.asarray(rounded(np.asarray(count, dtype=object) * p_x * p_y * p_z, wall)).astype(kind)
    product = np.asarray(count)[at].astype(object)
    for pace in (p_x, p_y, p_z):
        product = product * at_nodes(pace, at)
    found = np.zeros(at.shape, dtype=kind)
    found[at] = rounded(product, at_nodes(wall, at))
    return found


def write_factor_terms(
    count: Any, p_x: Any, p_y: Any, p_z: Any, p_0: Any, gamma: int, intervals: int, parts: int = 1
) -> tuple[Any, Any]:
    """The write's factor as its two terms, the numerator count p_x p_y p_z and the wall Gamma^intervals p_0^(3 - intervals), unrounded, whose quotient rounded half up is `write_factor`'s value bit for bit at every Node (the clock's wall 1 at a frozen clock as there): the terms of the held row's key `factor: carried`, the product a coefficient of the numerator inside the held write's one carried division at the wall E_s T times this wall per Node (records.write_sources; the end's booking, the reader's form of 2026-10-22), in Python's integers, exact beyond the width at every Node (the sum over a row's sources and the remainder join it before the division), the array's shape the count's or the paces'; `parts` multiplies the wall as in `write_factor`."""
    clock = np.asarray(p_0 + (p_0 == 0), dtype=object)
    wall = gamma**intervals * clock ** (3 - intervals) * parts
    product = np.asarray(count, dtype=object)
    for pace in (p_x, p_y, p_z):
        product = product * np.asarray(pace, dtype=object)
    return product, wall


def at_nodes(value: Any, nodes: np.ndarray) -> Any:
    """A read integer at the Nodes a mask names, one per Node named, in the mask's order; a scalar as it is."""
    return value[nodes] if np.ndim(value) else value


def within_width(kind: Any, wall: Any, *factors: Any) -> bool:
    """Whether one rounding of the factors' product over the wall (`rounded`, twice the product plus the wall over twice the wall) is computed in the hardware's integers of `kind`, the count's own: where the rounding's total at its largest, twice the product of the factors' largest sizes plus the largest wall, lies inside the host's width (core/integer.py, `MAX_WORK_INT`, the working bound), every intermediate product below it, so that the hardware's floor is Python's; False where it does not or where the kind is Python's already, and the product is taken in Python's integers, exact beyond the width; the same integers either way, the width's room read as the loader reads it and no number of the law."""
    if kind == np.dtype(object):  # Python's integers already, exact beyond the width
        return False
    bound = 2
    for factor in factors:
        bound *= int(np.abs(np.asarray(factor)).max())
    return bool(bound + int(np.asarray(wall).max()) <= MAX_WORK_INT)


def exponent_products(exponents: Sequence[int]) -> tuple[int, list[int]]:
    """The exponents' product P and, per exponent, the product of the others, P / n_f with no division (the hill's weight and the eras' readings form their fractions over these, `motion_weight`, board_readings.eras): (1, []) for no exponent."""
    others = [1] * len(exponents)
    for f, _exponent in enumerate(exponents):
        for g, other in enumerate(exponents):
            if g != f:
                others[f] = others[f] * other
    return (others[0] * exponents[0] if exponents else 1), others


def motion_weight(
    sources: Sequence[Any], exponents: Sequence[int], wall: int, gamma: int, own: int
) -> Any:
    """The hill's weight at every Node (ALGEBRA.md, The uniform mode carried by Rule3's own k = 0 line; The motion of gravity's row is a hill at the symmetry's weight; The hill's weight is the write's mix; The board's interval is no observable; hypotheses under their own names, 2026-10-22): K = (E_s T / Gamma) SUM_f s_f / SUM_f (s_f / n_f), `sources` the row's time line's sources at every Node, each family's form at the write's factor times its read weight (the integers records.write_sources sums), `exponents` the pairs' integers under the row's booking (`FamilyRule.exponent`: 5 for a pair with a gap at rest and 6 for the massless pair under the form's own clock, one above each under the law's booking), `wall` the write's wall E_s T; one rounding half up (`rounded`, kind D) of wall x P x SUM_f s_f over gamma x SUM_f s_f x (P / n_f), P the exponents' product and P / n_f the product of the other exponents (`exponent_products`), so that no division stands before the rounding (the same fraction as over the exponents' least common multiple, no gcd and no second carried division; the genericity hand: the weight is the write-weighted exponent n_eff in every booking): for one form rounded(n E_s T, Gamma) exactly, an integer where Gamma divides n E_s T (30 and 36 at T 36,000) and a coefficient of the interval otherwise (27 from 27.31 at T 32,768; "a pace and a factor are coefficients of the interval and no level"); where every source is 0 at a Node, and where no source is handed (the row's key `weight: gap`, the one-form K at the exponent `own` for every Node), the weight is rounded(own x wall, gamma), `own` the pair's integer the caller names (the row's own pair's where nothing sources the Node, 6 for the massless row of the content), never a division by 0; the Node reads its own sources and nothing of the board (the owner's locality decision of 2026-10-22); in the array's own kind, Python's integers beyond the width as `write_factor` has them (`within_width`)."""
    fallback = rounded(own * wall, gamma)  # the one-form K at the pair's integer `own`
    if not exponents:
        return fallback
    product, others = exponent_products(exponents)
    total: Any = 0
    weighed: Any = 0
    for source, other in zip(sources, others, strict=True):
        total, weighed = total + source, weighed + source * other
    weighed = np.asarray(weighed)
    empty = weighed == 0  # nothing sources the Node: the row's own pair's weight
    kind = np.asarray(total).dtype
    if within_width(kind, gamma * (weighed + empty), wall * product, total):
        denominator = gamma * (weighed + empty)
    else:  # Python's integers beyond the width, the empty Nodes' wall 1
        total = np.asarray(total, dtype=object)
        denominator = gamma * (np.asarray(weighed, dtype=object) + np.asarray(empty, dtype=object))
    found = np.where(empty, fallback, rounded(wall * product * total, denominator))
    return np.asarray(found).astype(kind)


def motion_term(now: Any, before: Any, weight: Any, wall: Any, direction: int = 1) -> tuple[Any, Any]:
    """The hill's write at every Node, the one function of its form (the Boss's seam of 2026-10-22): the term the one write's numerator gains and the divisor the write divides by, from the row's own two levels as the direction finds them (forward the interval's start, v_in = now - before; backward the post-state, v_out = now - before, the same function at -1), the weight K and the write's wall W. The symmetric hill (the symmetric hill's derivation M11j, 2026-10-22, read cold by the reader; ALGEBRA.md, The motion of gravity's row is a hill at the symmetry's weight; The write per proper volume and per proper interval, the clause of 2026-10-22: the kinetic form a level's intensity and no count, its two board-interval differences its own proper-interval booking, so the proper volume divides nothing; Every row reads the content, the hypothesis's one exception): the drag the product of the incoming and the outgoing velocities, -K (a_next - a_now) (a_now - a_before), implicit in a_next by the one carried division of the write's numerator less K (now - before)^2 at the wall W + sigma K (now - before), so that the line W (v_out - v_in) + r' - r = c - K v_in v_out is invariant under the reversal exactly on the integers (the velocities map v_in -> -v_out, the remainders exchange their roles as the carried division's direction does), the drag booked at the step's centre, second-order in the interval, the outgoing velocity bounded for v_in > 0 (no overshoot, no sign flip); the term -K (now - before)^2 at the divisor W + direction x K (now - before), the product in the levels' kind, exact in Python's integers beyond the width as the factor's numerator is (`within_width`); the Node's own two levels and nothing of the board (the owner's locality decision of 2026-10-22). The one-sided form, the term -K v_in^2 at the divisor W itself (the design's; the law's text names it), is superseded by this body on the smoke's finding of 2026-10-22, the one-Node seed's level thrown into a growing swing by a drag that read the incoming velocity alone. The wall's pole: the divisor is below 1 where v_in is at or below -W / K, a contraction at |H| at or beyond 1 / c per interval, and the write refuses it by name (features/held_write); backward the pole stands at v_out = W / K."""
    velocity = now - before
    kind = np.asarray(velocity).dtype
    if not within_width(kind, 0, weight, velocity, velocity):
        velocity, weight = np.asarray(velocity, dtype=object), np.asarray(weight, dtype=object)
    return -(weight * velocity * velocity), wall + direction * (weight * velocity)


def motion_returns(carry: Any, divisor: Any, weight: Any, after: Any, before: Any) -> Any:
    """Whether the forward act's carry in lies below the backward wall at every Node, W - K v_out = (W + K v_in) - K (a_next - a_before), `divisor` the forward act's wall, `after` the level after the write and `before` the level before the interval (the symmetric hill's derivation M11j, 1.3; the reversibility hand's Lemma 1 at the backward wall): where it does the interval's run back at the Node is exact, the same function at -1 returning the quotient and the carry in; where it does not the backward act folds the level before by one and the remainder by the wall, at the rate 2 c H per Node per interval (the Jacobian theorem: an act on the Node's own state with a remainder of bounded range collides about an attracting fixed point), so the forward act names the intervals whose run back fails (`Lattice.unreturning`) and the run back refuses by name there (`Lattice.motion_back`); a reading of the forward act's own numbers, no act."""
    return carry < divisor - weight * (after - before)


def turn_factor(angle: Any, p_0: Any, gamma: int) -> Any:
    """The turn per proper interval: the sign's level read into a plane's phase scaled by p_0 / Gamma, one division rounded half up at the read; the angle itself at the vacuum's clock."""
    return rounded(angle * p_0, gamma)


def clear_memo() -> None:
    """The memo cleared at a run's start, so that the paces are computed again once per (Gamma, content) within the run and nothing is kept between runs."""
    sides.cache_clear()
