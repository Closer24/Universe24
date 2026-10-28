"""Rule3 in one place, written as the law writes it, the flux form (ALGEBRA.md #the-line, #the-direction, #the-tick): w (a_next - 2 a_now + a_before) + r' - r = SUM over the clock's six meshes of R_ij (m_ij - a_now) - D_i a_now, the grip R_ij = 2 pinion p_i^2 Q_ij G^2 of each mesh read from the clock's end (the mesh rate squared times the mesh's factor), the spring D_i = 12 (rim - pinion) p_0^2 G^2 of the clock (the rate's alone, 0 for the unsprung hand), the teeth w = 6 rim Gamma^2 G^2, the fine tooth r kept in [0, w). One function steps every plain gear at every clock going either way (`rule3`), the sum over the meshes gathered by the step's module (flux.py) and handed in as one array; the one carry under it is the core's act (core/acts.carry, NL-S1; the former carried_division and division_forward, the same act by two names, kept by name), which the carries and the remainder readings call on a numerator. The hold S_i = 2 w - D_i - SUM_j R_ij is derived here for the readings that name it, the form's clock term; the click's face reads the flux form's total (`pull_total`) with the face's pull 0 (features/click `presented`); the law's first form, SUM R_ij m_ij + S a_now - w a_before + r, the same integers by the identity, is written in no file of src/ (tools/step_oracle.py keeps it as the step's oracle). The largest integer whose square is at most a count is found by a bisection on the wind reading and no root (`largest_below`); the gearing's integers from the rates stand beside (`gearing`, `spring`), the rates themselves the composed rates' two functions of the load (core/rates.py; ALGEBRA.md #the-rates)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, NamedTuple

from event_universe.core.acts import carry
from event_universe.core.spokes import AXES, SIDES, SPOKES

# a clock's grips, one per spoke in spoke order [+X, -X, +Y, -Y, +Z, -Z], R_ij = 2 pinion p_i^2 Q_ij G^2
# on the mesh to that neighbour; integers or the loop's integer arrays
Grips = tuple[Any, ...]
HELD_DRIVE_WEIGHT = (
    AXES + 1
)  # the held drive's (d + 1) X (...) p_0: X = Gamma (Gamma / p_0)^(d + 1), dX/dU = (d + 1) X
WINDING_WEIGHT = AXES  # a hand's winding (SPOKES / 2) T s: a rest mode's wind SPOKES s |W| at a winding, |W| = T div 2


class Gearing(NamedTuple):
    """Rule3's integers at a clock, the law's four names: the six grips R_ij in spoke order, the hold S_i of the first form (2 w - D_i - SUM_j R_ij, named by the form's clock term and the click's face), the teeth w and the spring D_i (`gearing`, `readings.gearing_of`)."""

    grips: Grips
    hold: Any
    teeth: Any
    spring: Any


def teeth_of(rim: Any, full_rate: Any, mesh_unit: Any = 1) -> Any:
    """The teeth w = 6 rim Gamma^2 G^2, the train's one divisor at every clock and every load (ALGEBRA.md #the-line)."""
    return SPOKES * rim * full_rate * full_rate * mesh_unit * mesh_unit


def spring(pinion: Any, rim: Any, rate: Any, mesh_unit: Any = 1) -> Any:
    """The clock's spring D_i = 12 (rim - pinion) p_0^2 G^2 (ALGEBRA.md #the-line, the flux form): the shortfall of the six grips and the hold under twice the teeth, 2 w - S_i - SUM_j R_ij, the rate's alone, 0 for every train with pinion = rim (unsprung), the one term of Rule3's gear that is the clock's own and not a mesh's."""
    return (SPOKES + SPOKES) * (rim - pinion) * rate * rate * mesh_unit * mesh_unit


def gearing(
    pinion: Any,
    rim: Any,
    full_rate: Any,
    rate: Any,
    mesh_rate: Any,
    factors: tuple[Any, ...] | None = None,
    mesh_unit: Any = 1,
) -> Gearing:
    """The gearing's integers at a clock from its rates, the Gearing (the six grips, S, w, D), the rate the clock's and the tension the mesh's (ALGEBRA.md #the-rates, The clock is the Clock's, the tension is the Mesh's; The rates compose): the rate p_0 = Gamma (1 - 1 / Gamma)^c to the unit from the clock's load c, the reading train's own notch among it, the primary number whose square enters the spring (`rates.rate_of`); the mesh rate p_i = p_0^2 / Gamma, the rate twice, on every one of its six meshes (`rates.mesh_rate_of`); each mesh's factor Q_ij, one integer per mesh in the unit G^2 of the run's mesh unit G (`mesh_factor`, read the same from both ends; None: no tension, G^2 on every mesh); the grip R_ij = 2 pinion p_i^2 Q_ij per spoke, the product and not the sum; the teeth w (`teeth_of`); the spring D (`spring`); the hold S = 2 w - D - SUM over the six spokes of R_ij, 12 (rim Gamma^2 - (rim - pinion) p_0^2) G^2 - SUM R_ij as the law's first form writes it, the same integer; at the vacuum's rates p_0 = p_i = Gamma the plain gearing of the ratio."""
    square = mesh_unit * mesh_unit
    mesh_rate_squared = mesh_rate * mesh_rate
    meshes = (square,) * SPOKES if factors is None else factors
    grips = tuple((mesh_rate_squared + mesh_rate_squared) * factor * pinion for factor in meshes)
    teeth, own = teeth_of(rim, full_rate, mesh_unit), spring(pinion, rim, rate, mesh_unit)
    return Gearing(grips, teeth + teeth - own - sum(grips), teeth, own)


def mesh_factor(full_rate: Any, mesh_unit: Any, tension: Any) -> Any:
    """The mesh's factor Q_ij, the one place of its form (ALGEBRA.md #the-rates, The clock is the Clock's, the tension is the Mesh's; the Boss's tally): q_ij^2 / Gamma^2 = (Gamma - t_a(i, j))^2 / Gamma^2 tallied squared as one integer per mesh in the unit G^2 of the run's mesh unit G, Q_ij = (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2 by the carry, rounded once to the nearest from the mesh's tension t and read the same from both ends; the step's coefficient matrix M is symmetric at uniform rates alone, and D M is symmetric at every rate with D = diag(1 / p_i^2), so the weighted form is exact at rates fixed in time; G^2 with no tension, 0 where the tension reaches Gamma (the mesh's coefficient 0), the tension resolved to Gamma / (2 G^2)."""
    rate = full_rate - tension
    teeth = full_rate * full_rate
    return carry(mesh_unit * mesh_unit * rate * rate, teeth, half(teeth))[0]


def least_at(above: Callable[[int], bool]) -> int:
    """The least positive count at which `above` holds, by comparisons alone (the one search of the settings' amplitudes and the unspringing's rise; its four spellings kept by name): the bound doubled from 1 until it holds, then halved between the last count below and the first above."""
    high = 1
    while not above(high):
        high += high
    low = 0
    while high - low > 1:
        middle = int(half(low + high))
        low, high = (middle, high) if not above(middle) else (low, middle)
    return high


def pull_total(pull: Any, hairspring: Any, teeth: Any, now: Any, other: Any) -> Any:
    """The flux form's total before the fine tooth and the carry, in the order the amplitude bound is derived for (ENGINE.md, The amplitude bound): w (2 a_now - a_before) - D a_now + SUM over the six meshes of R_ij (m_ij - a_now); `rule3` carries it, the click's face reads it (features/click `presented`)."""
    return teeth * (now + now - other) - hairspring * now + pull


def rule3(
    pull: Any, hairspring: Any, teeth: Any, now: Any, other: Any, fine: Any, going: int = 1
) -> tuple[Any, Any]:
    """Rule3's gear in the law's flux form, one tick in `going` sigma (ALGEBRA.md #the-line, #the-direction): w a_next + r' = w (2 a_now - a_before) - D a_now + SUM over the six meshes of R_ij (m_ij - a_now) + r (`pull_total`), the sum over the meshes `pull` gathered mesh by mesh by the step's module (flux.py, one difference per mesh, each end's own grip), the clock's spring `hairspring` (D_i), the carry the core's act (core/acts.carry, the former carried_division kept by name); +1 from (a_now, a_before, r) to (a_next, r'), -1 from (a_now, a_next, r') back to (a_before, r), the same pull read from the same notch. A gear with no meshes and the spring 2 w - 2 K on the teeth w is the rotation act a_next = (2 K a_now + r) div w - a_before (features/standard, the standard; features/click `rotated`)."""
    return carry(pull_total(pull, hairspring, teeth, now, other), teeth, fine, going)


def mesh_unit_of(full_rate: Any) -> int:
    """The mesh unit G derived from Gamma (K-S1, the owner's word of 2026-10-25: the conditions in the laws and the code enforces them; no key of the file): the least G at which one notch of tension at the vacuum resolves in the mesh's factor, Q(1) < Q(0) in `mesh_factor`, 2 G^2 (2 Gamma - 1) > Gamma^2, found by a search by comparisons (16 at Gamma 1,000)."""
    mesh_unit = 1
    while (mesh_unit + mesh_unit) * mesh_unit * (full_rate + full_rate - 1) <= full_rate * full_rate:
        mesh_unit += 1
    return mesh_unit


def held_teeth(weight: Any, rim: Any, full_rate: Any, key: Any, power: int) -> Any:
    """A held train's drive teeth (K-S1 to K-S3, Y-S1): weight rim Gamma^power T with the trace's weight the calibre's `trace` key, the time gear's at the power 4 and the nine gears' at 2."""
    return weight * rim * full_rate**power * key


def held_numerator(
    weight: Any, stretch: Any, forms: Any, trace: Any, rate: Any, rim: Any, full_rate: Any
) -> Any:
    """The regulator's time gear's drive numerator (the regulation's time gear, the held drive): 4 X (forms weight rim Gamma^2 - trace p_0^2) p_0 with the trace's weight the calibre's `trace` key."""
    return (
        HELD_DRIVE_WEIGHT
        * stretch
        * (forms * weight * rim * full_rate * full_rate - trace * rate * rate)
        * rate
    )


def winding_of(sine: Any, key: Any) -> Any:
    """A hand's winding, 3 T s (the conventions' row 12: W_c sin omega_0 to the unit), s the ratio's sine or the rim at the spring 0."""
    return WINDING_WEIGHT * key * sine


def signed_carries(numerator: Any, teeth: Any) -> Any:
    """The carries of the magnitude with the sign after, sign(x) (|x| div w): the setting's rounding of a signed notch at rest (the one rule's flip by the numerator's sign at a fine tooth born at 0), so the negated vector's setting is the setting negated."""
    sign = (numerator >= 0) * 1 - (numerator < 0) * 1
    return sign * carries(sign * numerator, teeth)


def half(teeth: Any) -> Any:
    """The half teeth by the carry on 2, the fine tooth's start and the mean teeth's factor (the halving's own 2)."""
    return carry(teeth, SIDES, 0)[0]


def mean_teeth_of(teeth: Any, before: Any, now: Any) -> Any:
    """The mean teeth (w div 2)(X_before + X_now) of the regulator's two notches, a driven gear's teeth: the one spelling for the tick, the setting's teeth and the reader's reckoning."""
    return half(teeth) * (before + now)


def odd(count: Any) -> Any:
    """The parity of a count by the carry on 2, 1 where odd (the parity's own 2): the reversals' count, a gear's odd part."""
    return carry(count, SIDES, 0)[1]


def wind_weight(full_rate: Any, mesh_unit: Any) -> Any:
    """The wind's weight 2 Gamma^3 G^2, the exact unwind's scale (the fall f(s) over it; hands.py's teeth its double)."""
    return (full_rate + full_rate) * full_rate * full_rate * mesh_unit * mesh_unit


def carries(numerator: Any, teeth: Any) -> Any:
    """The carry act's carries alone, numerator div teeth with no fine tooth carried in (the digit on a pitch, the amplitude's wind, the root's candidate)."""
    return carry(numerator, teeth, 0)[0]


def remainder(numerator: Any, teeth: Any) -> Any:
    """The carry act's fine tooth alone, numerator mod teeth in [0, teeth) (the vernier composed modulo the hands' count times the winding)."""
    return carry(numerator, teeth, 0)[1]


def pitch(*values: Any) -> Any:
    """The greatest common divisor of integers by Euclid's carry act (the remainder alone), the pitch of a gear's fine teeth at a clock: gcd(w, D, R_1..R_6) on the clock's own pitch, gcd(w, R_ji) on a mesh's."""
    found = 0
    for value in values:
        a, b = abs(found), abs(value)
        while b:
            a, b = b, remainder(a, b)
        found = a
    return found


def balanced_notches(product: int) -> tuple[int, int]:
    """The pair (a, b) with a b = product exactly and a the largest divisor at most largest_below(product), found by a search by comparisons down from the root's floor (MS-S1: the setting's two notches with A B = T div 2 for every train, the same two integers from T alone; 125 and 144 at T 36,000)."""
    a = largest_below(product)
    while remainder(product, a):
        a -= 1
    return a, carries(product, a)


def largest_below(square: int) -> int:
    """The largest x with x^2 <= square, found by a bisection on the wind reading x * x against square: products and comparisons of integers, no division on the count and no root (the hands' prescription for the rotation unit, `paces.rotation_unit`, applied to a count: a search by comparisons, issue #1793 comment 6077053307, "no root anywhere"). The upper end is the smallest power of two whose square exceeds square, found by doubling; the halving of the span of candidates is the carry on a count, `half(low + high)`, kind D in the acts table (tests/test_the_acts_table.py), its fine tooth discarded; 0 at 0; a negative square is refused by name (ALGEBRA.md #the-four-acts, #the-guard)."""
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
