"""Rule3 in one place, written as the law writes it, the flux line (ALGEBRA.md #the-line, #the-direction, #the-interval): w (a_next - 2 a_now + a_before) + r' - r = SUM over the Node's six Links of R_ij (m_ij - a_now) - D_i a_now, the reach R_ij = 2 num p_i^2 Q_ij G^2 of each Link read from the Node's end (the Node's pace squared times the Link's factor), the mass D_i = 12 (den - num) p_0^2 G^2 of the Node (the clock's alone, 0 for light), the wall w = 6 den Gamma^2 G^2, the remainder r kept in [0, w). One function steps every plain line at every Node in either direction (`rule3`), the sum over the Links gathered by the step's module (flux.py) and handed in as one array; the one carried division under it is the core's act (core/acts.divide, NL-S1; the former carried_division kept by name), which the division act's two functions call on a numerator. The own weight S_i = 2 w - D_i - SUM_j R_ij is derived here for the readings that name it, the form's Node term; the click's face reads the flux line's total (`flux_total`) with the face's arrival 0 (features/click `presented`); the law's first form, SUM R_ij m_ij + S a_now - w a_before + r, the same integers by the identity, is written in no file of src/ (tools/step_oracle.py keeps it as the step's oracle). The largest integer whose square is at most a count is found by a bisection on the share reading and no root (`largest_below`); the rule's integers from the paces stand beside (`coefficients`, `mass`), the paces themselves the composed clock's two functions of the content (core/paces.py; ALGEBRA.md #the-paces)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, NamedTuple

from event_universe.core.acts import divide
from event_universe.core.ports import PORTS

# the Node's reaches, one per Port in Port order [+X, -X, +Y, -Y, +Z, -Z], R_ij = 2 num p_i^2 Q_ij G^2 on
# the Link to that neighbour; integers or the loop's integer arrays
Reads = tuple[Any, ...]
HELD_WRITE_WEIGHT = (
    4  # the held write's 4 X (...) p_0 (the hypothesis The stress's trace is the time line's, d + 1)
)
UNIT_WEIGHT = 3  # the plane's unit 3 T s (the conventions' row 12)


class Rule(NamedTuple):
    """Rule3's integers at a Node, the law's four names: the six reaches R_ij in Port order, the own weight S_i of the first form (2 w - D_i - SUM_j R_ij, named by the form's Node term and the click's face), the wall w and the mass D_i (`rule_integers`, `node.rule_of`)."""

    reaches: Reads
    self_coefficient: Any
    wall: Any
    mass: Any


def wall_of(den: Any, gamma: Any, unit: Any = 1) -> Any:
    """The wall w = 6 den Gamma^2 G^2, the family's one divisor at every Node and every content (ALGEBRA.md #the-line)."""
    return PORTS * den * gamma * gamma * unit * unit


def mass(num: Any, den: Any, clock: Any, unit: Any = 1) -> Any:
    """The Node's mass D_i = 12 (den - num) p_0^2 G^2 (ALGEBRA.md #the-line, the flux form): the shortfall of the six reaches and the own weight under twice the wall, 2 w - S_i - SUM_j R_ij, the clock's alone, 0 for every family with num = den (light), the one term of Rule3's line that is the Node's own and not a Link's."""
    return (PORTS + PORTS) * (den - num) * clock * clock * unit * unit


def rule_integers(
    num: Any,
    den: Any,
    gamma: Any,
    clock: Any,
    pace: Any,
    factors: tuple[Any, ...] | None = None,
    unit: Any = 1,
) -> Rule:
    """The rule's integers at a Node from its paces, the Rule (the six reaches, S, w, D), the clock the Node's and the tension the Link's (ALGEBRA.md #the-paces, The clock is the Node's, the tension is the Link's; The paces compose): the clock p_0 = Gamma (1 - 1 / Gamma)^c to the unit from the Node's content c, the reading row's own level among it, the primary number whose square enters the mass (`paces.clock_of`); the Node's pace p_i = p_0^2 / Gamma, the clock twice, on every one of its six Links (`paces.link_pace_of`); each Link's factor Q_ij, one integer per Link in the unit G^2 of the run's Link unit G (`link_factor`, read the same from both ends; None: no tension, G^2 on every Link); the reach R_ij = 2 num p_i^2 Q_ij per Port, the product and not the sum; the wall w (`wall_of`); the mass D (`mass`); the own weight S = 2 w - D - SUM over the six Ports of R_ij, 12 (den Gamma^2 - (den - num) p_0^2) G^2 - SUM R_ij as the law's first form writes it, the same integer; at the vacuum's paces p_0 = p_i = Gamma the plain rule of the pair."""
    square = unit * unit
    node_squared = pace * pace
    links = (square,) * PORTS if factors is None else factors
    reaches = tuple((node_squared + node_squared) * factor * num for factor in links)
    wall, own = wall_of(den, gamma, unit), mass(num, den, clock, unit)
    return Rule(reaches, wall + wall - own - sum(reaches), wall, own)


def link_factor(gamma: Any, unit: Any, tension: Any) -> Any:
    """The Link's factor Q_ij, the one place of its form (ALGEBRA.md #the-paces, The clock is the Node's, the tension is the Link's; the Boss's booking): q_ij^2 / Gamma^2 = (Gamma - t_a(i, j))^2 / Gamma^2 booked squared as one integer per Link in the unit G^2 of the run's Link unit G, Q_ij = (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2 by the division act, rounded once to the nearest from the Link's tension t and read the same from both ends; the step's coefficient matrix M is symmetric at uniform paces alone, and D M is symmetric at every pace with D = diag(1 / p_i^2), so the weighted form is exact at paces fixed in time; G^2 with no tension, 0 where the tension reaches Gamma (the Link's coefficient 0), the tension resolved to Gamma / (2 G^2)."""
    pace = gamma - tension
    wall = gamma * gamma
    return division_forward(unit * unit * pace * pace, wall, half(wall))[0]


def scaled(rule: Rule, scale: Any) -> Rule:
    """A rule's four names scaled alike (the reaches, the own weight, the wall, the mass): the line's units a multiple, its quotients unchanged, a term the scale carries exact inside the division (SR-S3); the identity at 1."""
    if scale == 1:
        return rule
    return Rule(
        tuple(scale * x for x in rule.reaches),
        scale * rule.self_coefficient,
        scale * rule.wall,
        scale * rule.mass,
    )


def least_at(above: Callable[[int], bool]) -> int:
    """The least positive count at which `above` holds, by comparisons alone (the one search of the lays' amplitudes and the merger's rise; its four spellings kept by name): the bound doubled from 1 until it holds, then halved between the last count below and the first above."""
    high = 1
    while not above(high):
        high += high
    low = 0
    while high - low > 1:
        middle = int(half(low + high))
        low, high = (middle, high) if not above(middle) else (low, middle)
    return high


def flux_total(flux: Any, mass: Any, wall: Any, now: Any, other: Any) -> Any:
    """The flux line's total before the remainder and the division, in the order the amplitude bound is derived for (ENGINE.md, The amplitude bound): w (2 a_now - a_before) - D a_now + SUM over the six Links of R_ij (m_ij - a_now); `rule3` divides it, the click's face reads it (features/click `presented`)."""
    return wall * (now + now - other) - mass * now + flux


def rule3(
    flux: Any, mass: Any, wall: Any, now: Any, other: Any, remainder: Any, direction: int = 1
) -> tuple[Any, Any]:
    """Rule3's line in the law's flux form, one interval in `direction` sigma (ALGEBRA.md #the-line, #the-direction): w a_next + r' = w (2 a_now - a_before) - D a_now + SUM over the six Links of R_ij (m_ij - a_now) + r (`flux_total`), the sum over the Links `flux` gathered Link by Link by the step's module (flux.py, one difference per Link, each end's own reach), the Node's mass `mass` (D_i), the division the carried one (`carried_division`); +1 from (a_now, a_before, r) to (a_next, r'), -1 from (a_now, a_next, r') back to (a_before, r), the same flux read from the same level. A line with no Links and the mass 2 w - 2 K on the wall w is the rotation act a_next = (2 K a_now + r) div w - a_before (features/phase, the phase line; features/click `rotated`)."""
    return divide(flux_total(flux, mass, wall, now, other), wall, remainder, direction)


def division_forward(numerator: Any, wall: Any, carry: Any) -> tuple[Any, Any]:
    """Rule3's division act forward: (numerator + carry) div wall and the remainder, the one carried division on a numerator (ALGEBRA.md #the-four-acts)."""
    return divide(numerator, wall, carry, 1)


def link_unit_of(gamma: Any) -> int:
    """The Link's unit G derived from Gamma (K-S1, the owner's word of 2026-10-25: the conditions in the laws and the code enforces them; no key of the file): the least G at which one level of tension at the vacuum resolves in the Link's factor, Q(1) < Q(0) in `link_factor`, 2 G^2 (2 Gamma - 1) > Gamma^2, found by a search by comparisons (16 at Gamma 1,000)."""
    unit = 1
    while (unit + unit) * unit * (gamma + gamma - 1) <= gamma * gamma:
        unit += 1
    return unit


def held_wall(weight: Any, den: Any, gamma: Any, action: Any, power: int) -> Any:
    """A held row's write wall (K-S1 to K-S3, Y-S1): weight den Gamma^power T with the trace's weight the universe file's `trace` key, the time line's at the power 4 and the nine lines' at 2."""
    return weight * den * gamma**power * action


def held_numerator(
    weight: Any, level: Any, forms: Any, trace: Any, clock: Any, den: Any, gamma: Any
) -> Any:
    """The carrier's time line's write numerator (the metric time line, the held write): 4 X (forms weight den Gamma^2 - trace p_0^2) p_0 with the trace's weight the universe file's `trace` key."""
    return (
        HELD_WRITE_WEIGHT
        * level
        * (forms * weight * den * gamma * gamma - trace * clock * clock)
        * clock
    )


def unit_of(sine: Any, action: Any) -> Any:
    """A plane's quantum, its unit 3 T s (the conventions' row 12: W_c sin omega_0 to the unit), s the pair's sine or den at the gap 0."""
    return UNIT_WEIGHT * action * sine


def signed_quotient(numerator: Any, wall: Any) -> Any:
    """The quotient of the magnitude with the sign after, sign(x) (|x| div w): the lay's rounding of a signed level at rest (the one rule's mirror by the numerator's sign at a remainder born at 0), so the negated vector's lay is the lay negated."""
    sign = (numerator >= 0) * 1 - (numerator < 0) * 1
    return sign * quotient(sign * numerator, wall)


def half(wall: Any) -> Any:
    """The half of a wall by the division act on 2, the remainder's start and the mean wall's factor (the halving's own 2)."""
    return division_forward(wall, 2, 0)[0]


def odd(count: Any) -> Any:
    """The parity of a count by the division act on 2, 1 where odd (the parity's own 2): the reversals' count, a line's odd part."""
    return division_forward(count, 2, 0)[1]


def share_weight(gamma: Any, unit: Any) -> Any:
    """The share's weight 2 Gamma^3 G^2, the exact take's scale (the fall f(s) over it; gram's wall its double)."""
    return (gamma + gamma) * gamma * gamma * unit * unit


def quotient(numerator: Any, wall: Any) -> Any:
    """The division act's quotient alone, numerator div wall with no carry (the digit on a lattice, the amplitude's share, the root's candidate)."""
    return division_forward(numerator, wall, 0)[0]


def remainder(numerator: Any, wall: Any) -> Any:
    """The division act's remainder alone, numerator mod wall in [0, wall) (the draw composed modulo the planes' count times the unit)."""
    return division_forward(numerator, wall, 0)[1]


def lattice(*values: Any) -> Any:
    """The greatest common divisor of integers by Euclid's division act (the remainder alone), the lattice of a line's remainders at a Node: gcd(w, D, R_1..R_6) on the Node's own lattice, gcd(w, R_ji) on a Link's."""
    found = 0
    for value in values:
        a, b = abs(found), abs(value)
        while b:
            a, b = b, remainder(a, b)
        found = a
    return found


def balanced_pair(product: int) -> tuple[int, int]:
    """The pair (a, b) with a b = product exactly and a the largest divisor at most largest_below(product), found by a search by comparisons down from the root's floor (MS-S1: the lay's two levels with A B = T div 2 for every row, the same two integers from T alone; 125 and 144 at T 36,000)."""
    a = largest_below(product)
    while remainder(product, a):
        a -= 1
    return a, quotient(product, a)


def largest_below(square: int) -> int:
    """The largest x with x^2 <= square, found by a bisection on the share reading x * x against square: products and comparisons of integers, no division on the count and no root (the hands' prescription for the rotation unit, `paces.rotation_unit`, applied to a count: a search by comparisons, issue #1793 comment 6077053307, "no root anywhere"). The upper end is the smallest power of two whose square exceeds square, found by doubling; the halving of the span of candidates is the division act on a count, `division_forward(low + high, 2, 0)`, kind D in the acts table (tests/test_the_acts_table.py), its remainder discarded; 0 at 0; a negative square is refused by name (ALGEBRA.md #the-four-acts, #the-guard)."""
    if square < 0:
        raise ValueError(f"no integer has a square at most {square}: the search is refused")
    high = 1
    while high * high <= square:
        high = high + high
    low = 0
    while high - low > 1:
        middle = int(half(low + high))
        if middle * middle <= square:
            low = middle
        else:
            high = middle
    return low
