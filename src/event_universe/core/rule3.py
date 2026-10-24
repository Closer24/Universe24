"""Rule3 in one place, written as the law writes it, the flux line (ALGEBRA.md #the-line, #the-direction, #the-interval): w (a_next - 2 a_now + a_before) + r' - r = SUM over the Node's six Links of R_ij (m_ij - a_now) - D_i a_now, the reach R_ij = 2 num p_i^2 Q_ij G^2 of each Link read from the Node's end (the Node's pace squared times the Link's factor), the mass D_i = 12 (den - num) p_0^2 G^2 of the Node (the clock's alone, 0 for light), the wall w = 6 den Gamma^2 G^2, the remainder r kept in [0, w). One function steps every plain line at every Node in either direction (`rule3`), the sum over the Links gathered by the step's module (flux.py) and handed in as one array; the one carried division under it (`carried_division`) is the division act with the remainder kept, which the division act's two functions call on a numerator. The own weight S_i = 2 w - D_i - SUM_j R_ij is derived here for the readings that name it, the form's Node term; the click's face reads the flux line's total (`flux_total`) with the face's arrival 0 (features/click `presented`); the law's first form, SUM R_ij m_ij + S a_now - w a_before + r, the same integers by the identity, is written in no file of src/ (tools/step_oracle.py keeps it as the step's oracle). The largest integer whose square is at most a count is found by a bisection on the share reading and no root (`largest_below`); the rule's integers from the paces stand beside (`coefficients`, `mass`), the paces themselves the composed clock's two functions of the content (core/paces.py; ALGEBRA.md #the-paces)."""

from __future__ import annotations

from typing import Any, NamedTuple

from event_universe.core.ports import PORTS

# the Node's reaches, one per Port in Port order [+X, -X, +Y, -Y, +Z, -Z], R_ij = 2 num p_i^2 Q_ij G^2 on
# the Link to that neighbour; integers or the loop's integer arrays
Reads = tuple[Any, ...]


class Rule(NamedTuple):
    """Rule3's integers at a Node, the law's four names: the six reaches R_ij in Port order, the own weight S_i of the first form (2 w - D_i - SUM_j R_ij, named by the form's Node term and the click's face), the wall w and the mass D_i (`rule_integers`, `node.rule_of`)."""

    reaches: Reads
    self_coefficient: Any
    wall: Any
    mass: Any


def wall_of(den: Any, gamma: Any, unit: Any = 1) -> Any:
    """The wall w = 6 den Gamma^2 G^2, the family's one divisor at every Node and every content (ALGEBRA.md #the-line)."""
    return 6 * den * gamma * gamma * unit * unit


def mass(num: Any, den: Any, clock: Any, unit: Any = 1) -> Any:
    """The Node's mass D_i = 12 (den - num) p_0^2 G^2 (ALGEBRA.md #the-line, the flux form): the shortfall of the six reaches and the own weight under twice the wall, 2 w - S_i - SUM_j R_ij, the clock's alone, 0 for every family with num = den (light), the one term of Rule3's line that is the Node's own and not a Link's."""
    return 12 * (den - num) * clock * clock * unit * unit


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
    reaches = tuple(2 * node_squared * factor * num for factor in links)
    wall, own = wall_of(den, gamma, unit), mass(num, den, clock, unit)
    return Rule(reaches, wall + wall - own - sum(reaches), wall, own)


def coefficients(
    num: Any,
    den: Any,
    gamma: Any,
    clock: Any,
    pace: Any,
    factors: tuple[Any, ...] | None = None,
    unit: Any = 1,
) -> tuple[Reads, Any, Any]:
    """The rule's first three integers, (the six reaches, S, w), as the readings of the first form name them (`rule_integers` for the four)."""
    reaches, self_coefficient, wall, _mass = rule_integers(num, den, gamma, clock, pace, factors, unit)
    return reaches, self_coefficient, wall


def link_factor(gamma: Any, unit: Any, tension: Any) -> Any:
    """The Link's factor Q_ij, the one place of its form (ALGEBRA.md #the-paces, The clock is the Node's, the tension is the Link's; the Boss's booking): q_ij^2 / Gamma^2 = (Gamma - t_a(i, j))^2 / Gamma^2 booked squared as one integer per Link in the unit G^2 of the run's Link unit G, Q_ij = (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2 by the division act, rounded once to the nearest from the Link's tension t and read the same from both ends; the step's coefficient matrix M is symmetric at uniform paces alone, and D M is symmetric at every pace with D = diag(1 / p_i^2), so the weighted form is exact at paces fixed in time; G^2 with no tension, 0 where the tension reaches Gamma (the Link's coefficient 0), the tension resolved to Gamma / (2 G^2)."""
    pace = gamma - tension
    wall = gamma * gamma
    half = division_forward(wall, 2, 0)[0]
    return division_forward(unit * unit * pace * pace, wall, half)[0]


def carried_division(total: Any, wall: Any, remainder: Any, direction: int = 1) -> tuple[Any, Any]:
    """The one carried division of the law (ALGEBRA.md #the-four-acts, #the-direction): u = sigma total + r, the quotient sigma (u div w) and the remainder u mod w kept in [0, w) for a total of either sign; +1 forward, -1 the same act back, exact: from the quotient and the remainder the forward act wrote, the level and the remainder before it."""
    total = direction * total + remainder
    quotient = total // wall
    return direction * quotient, total - wall * quotient


def flux_total(flux: Any, mass: Any, wall: Any, now: Any, other: Any) -> Any:
    """The flux line's total before the remainder and the division, in the order the amplitude bound is derived for (ENGINE.md, The amplitude bound): w (2 a_now - a_before) - D a_now + SUM over the six Links of R_ij (m_ij - a_now); `rule3` divides it, the click's face reads it (features/click `presented`)."""
    return wall * (now + now - other) - mass * now + flux


def rule3(
    flux: Any, mass: Any, wall: Any, now: Any, other: Any, remainder: Any, direction: int = 1
) -> tuple[Any, Any]:
    """Rule3's line in the law's flux form, one interval in `direction` sigma (ALGEBRA.md #the-line, #the-direction): w a_next + r' = w (2 a_now - a_before) - D a_now + SUM over the six Links of R_ij (m_ij - a_now) + r (`flux_total`), the sum over the Links `flux` gathered Link by Link by the step's module (flux.py, one difference per Link, each end's own reach), the Node's mass `mass` (D_i), the division the carried one (`carried_division`); +1 from (a_now, a_before, r) to (a_next, r'), -1 from (a_now, a_next, r') back to (a_before, r), the same flux read from the same level. A line with no Links and the mass 2 w - 2 K on the wall w is the rotation act a_next = (2 K a_now + r) div w - a_before (features/phase, the phase line; features/click `rotated`)."""
    return carried_division(flux_total(flux, mass, wall, now, other), wall, remainder, direction)


def division_forward(numerator: Any, wall: Any, carry: Any) -> tuple[Any, Any]:
    """Rule3's division act forward: (numerator + carry) div wall and the remainder, the one carried division on a numerator (ALGEBRA.md #the-four-acts)."""
    return carried_division(numerator, wall, carry, 1)


def division_back(numerator: Any, wall: Any, carry: Any) -> tuple[Any, Any]:
    """The division act one interval back by the carried division's direction -1: from the remainder after, the quotient the forward act wrote and the remainder before it, exact (ALGEBRA.md #the-direction)."""
    return carried_division(numerator, wall, carry, -1)


def largest_below(square: int) -> int:
    """The largest x with x^2 <= square, found by a bisection on the share reading x * x against square: products and comparisons of integers, no division on the count and no root (the hands' prescription for the rotation unit, `paces.rotation_unit`, applied to a count: a search by comparisons, issue #1793 comment 6077053307, "no root anywhere"). The upper end is the smallest power of two whose square exceeds square, found by doubling; the halving of the span of candidates is the division act on a count, `division_forward(low + high, 2, 0)`, kind D in the acts table (tests/test_the_acts_table.py), its remainder discarded; 0 at 0; a negative square is refused by name (ALGEBRA.md #the-four-acts, #the-guard)."""
    if square < 0:
        raise ValueError(f"no integer has a square at most {square}: the search is refused")
    high = 1
    while high * high <= square:
        high = high + high
    low = 0
    while high - low > 1:
        middle = int(division_forward(low + high, 2, 0)[0])
        if middle * middle <= square:
            low = middle
        else:
            high = middle
    return low


def form_term(self_coefficient: Any, wall: Any, now: Any, before: Any) -> Any:
    """The conserved form's term at one Node from the rule's integers, w (now^2 + before^2) - S now before (ALGEBRA.md #the-conserved-form)."""
    return wall * (now * now + before * before) - self_coefficient * now * before


def partial_rooms(
    self_coefficient: Any, wall: Any, mass: Any, links: Any, arrivals: Any
) -> tuple[Any, ...]:
    """The rooms of the flux line's five partial sums at a level A, each the factor of A (ENGINE.md, The amplitude bound): the free term 3 w, the mass D, the Node's own terms |2 w - D| + w, the Links' sum `links` (2 SUM_j |R_ij| on a plain line, a Node at +A among six neighbours at -A; more on a turned or folded plane, whose Links reach further), and the whole total `arrivals` + w + |S| with the remainder, w - 1 more than A times it, `arrivals` the six arrivals' reads (SUM_j |R_ij| on a plain line; under the pair's two parts on a turned or folded plane, the loader's `bound_under_rooms`)."""
    return (
        3 * wall,
        mass,
        abs(wall + wall - mass) + wall,
        links,
        arrivals + wall + abs(self_coefficient),
    )
