"""The breaker's rows for the paper's theorems (the method of 2026-10-04: a breaker tries to break a printed claim on the smallest configuration, inside the claim's stated condition and outside it; the strong word stays only where the claim holds inside and breaks outside). Each row function is one row of paper/claims_breakers.json of the kind (a), pure algebra of Rule3's line: exact rationals, boards of 2x2x2 to 4x4x4 Nodes, steps in the tens, draws in the hundreds, nothing of the engine and no world file. Every step of the line is rule3.py's or proofs_ground.py's, every form proofs_form.py's or proofs_booking.py's, every credit bell.py's; this module holds no arithmetic of the law of its own. The rows of the conserved form, the Wronskian, the share and the flux are in counterexample_forms.py, the derived rows of the paper's tables in counterexample_derived.py, the registry and the Markdown report in counterexamples.py.

A Row: the claim's key (its opening words, the JSON key), whether the claim held inside its condition, whether it broke outside it (None where the claim states no condition to step outside of), and the witness in one string. Every random choice comes from random.Random(SEED), SEED = 24, so a run reproduces.
"""

from __future__ import annotations

import math
import random
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bell  # noqa: E402
import rule3  # noqa: E402
from proofs_ground import (  # noqa: E402
    SEED,
    box_arrivals,
    box_index,
    box_nodes,
    integer_witness,
    pairs,
    read,
    step_line,
)

PORTS, AXES = rule3.PORTS, rule3.AXES
SHAPES = ((2, 2, 2), (3, 2, 2), (4, 3, 2))  # the smallest boards with every axis of two or more Nodes


@dataclass(frozen=True)
class Row:
    key: str
    holds_inside: bool
    breaks_outside: bool | None
    witness: str


Board = tuple[list[list[int]], list[int], list[list[int]]]  # arrivals, clocks, Link factors


def uneven_board(draw: random.Random, shape: tuple[int, int, int], gamma: int) -> Board:
    """A periodic board of the shape with integer-read clocks and Link factors read the same from both ends (proofs_ground.integer_witness), the paces uneven and a tension on the Links."""
    arrivals = box_arrivals(shape)
    _, clocks, factors = integer_witness(draw, arrivals, gamma, tension=True)
    return arrivals, clocks, factors


def levels(draw: random.Random, count: int, size: int = 40) -> list[int]:
    return [draw.randint(-size, size) for _ in range(count)]


def weighted_currents(
    factors: Sequence[Sequence[int]],
    arrivals: Sequence[Sequence[int]],
    i: int,
    now: Sequence[Fraction | int],
    before: Sequence[Fraction | int],
    num: int,
    gamma: int,
) -> Fraction:
    """The six currents into the Node i, each with its Link's factor squared (rule3.link_current)."""
    return sum(
        (
            rule3.link_current(num, now[i], before[i], now[j], before[j], factors[i][port], gamma)
            for port, j in enumerate(arrivals[i])
        ),
        Fraction(0),
    )


def cube_group_commutes_with_rule3() -> Row:
    """Section 3.1, S.4: the cube's 48 maps (the signed permutations of the axes) commute with Rule3's integer step on a 3x3x3 periodic board at uniform paces, the remainders carried along; outside the group, the band's cos omega at |k| = 0.5 per Link differs along an axis, a face diagonal and the body diagonal (the lattice's anisotropy, S.21), so the continuum's rotations are no symmetry: the claim holds if the three differ."""
    draw = random.Random(SEED)
    shape = (3, 3, 3)
    nodes, arrivals = box_nodes(shape), box_arrivals(shape)
    misses = 0
    for num, den in pairs(draw, 3):
        gamma = draw.randint(2, 6)
        pace = draw.randint(1, gamma)
        wall, _, _ = rule3.coefficients(num, den, gamma, pace, (pace,) * AXES)
        now, before = levels(draw, len(nodes)), levels(draw, len(nodes))
        remainders = [draw.randint(0, wall - 1) for _ in nodes]

        def stepped(
            now: list[int],
            before: list[int],
            remainders: list[int],
            pair=(num, den),
            paces=(gamma, pace),
        ) -> list[tuple[int, int]]:
            return [
                rule3.step(
                    now[i],
                    before[i],
                    [now[j] for j in arrivals[i]],
                    pair[0],
                    pair[1],
                    remainders[i],
                    paces[0],
                    paces[1],
                    (paces[1],) * AXES,
                )
                for i in range(len(nodes))
            ]

        for axes in permutations(range(AXES)):
            for signs in product((1, -1), repeat=AXES):

                def image(index: int, signs=signs, axes=axes) -> int:  # where the map sends the Node
                    x = nodes[index]
                    moved = [signs[a] * x[axes[a]] for a in range(AXES)]
                    return box_index(shape, moved[0], moved[1], moved[2])

                def mapped(values: list[int]) -> list[int]:
                    out = [0] * len(nodes)
                    for index, value in enumerate(values):
                        out[image(index)] = value
                    return out

                direct = stepped(now, before, remainders)
                via_map = stepped(mapped(now), mapped(before), mapped(remainders))
                # the map applied after the step: the Node `index` lands at image(index)
                mapped_direct = [(0, 0)] * len(nodes)
                for index, pair in enumerate(direct):
                    mapped_direct[image(index)] = pair
                misses += via_map != mapped_direct
    light = (1, 1)
    along = {
        "axis": (0.5, 0.0, 0.0),
        "face diagonal": (0.5 / math.sqrt(2), 0.5 / math.sqrt(2), 0.0),
        "body diagonal": (0.5 / math.sqrt(3),) * 3,
    }
    cosines = {name: rule3.dispersion_at_paces(k, *light, 1, 1, (1, 1, 1)) for name, k in along.items()}
    expected = {"axis": 0.9592, "face diagonal": 0.9588, "body diagonal": 0.9586}
    as_printed = all(round(cosines[name], 4) == expected[name] for name in along)
    distinct = len({round(c, 6) for c in cosines.values()}) == 3
    return Row(
        "So Lorentzs group and the continuums rotations are no symmet",
        misses == 0 and as_printed,
        distinct,
        f"48 maps x 3 pairs on 3x3x3, misses {misses}; cos omega at |k| = 0.5 on [1, 1]: "
        + ", ".join(f"{n} {c:.4f}" for n, c in cosines.items()),
    )


def pi_mode_multiplier(num: int, den: int, gamma: int, pace: int) -> tuple[Fraction, Fraction]:
    """(the multiplier 2 cos omega of the mode at wave number pi on every axis, (S - 2 SUM_a R_a) / w, and of the mode at wave number 0, (S + 2 SUM_a R_a) / w) at p_0 = p_a = pace, from rule3.coefficients."""
    wall, reads, self_coefficient = rule3.coefficients(num, den, gamma, pace, (pace,) * AXES)
    return (
        Fraction(self_coefficient - 2 * sum(reads), wall),
        Fraction(self_coefficient + 2 * sum(reads), wall),
    )


def one_mode_orbit(multipliers: Sequence[Fraction], steps: int) -> Fraction:
    """The largest |a_t| of a_next + a_before = m_t a_now from (a_0, a_1) = (0, 1), the two-level recurrence of one mode, m_t cycling through `multipliers`."""
    before, now, largest = Fraction(0), Fraction(1), Fraction(1)
    for t in range(steps):
        before, now = now, multipliers[t % len(multipliers)] * now - before
        largest = max(largest, abs(now))
    return largest


def guard_bounds_the_pi_mode_at_fixed_coefficients() -> Row:
    """Section 3.4, S.3 (the guard): at p_0 = p_a = p with p^2 <= P^2 = 2 den Gamma^2 div (den + |num|) both extreme multipliers (the mode at pi on every axis and the mode at 0) lie in [-2, 2], so no mode grows exponentially, and the pi mode's orbit over 40 steps stays under the linear bound t + 1; at p = P + 1 the pi mode's multiplier falls below -2 (growth without bound, the first half); outside the fence 'at coefficients fixed in time': the paces alternating between 1 and P, each inside the guard, drive the pi mode beyond the linear bound (the parametric case, S.3's own caveat)."""
    draw = random.Random(SEED)
    inside, beyond, parametric = True, True, True
    witnesses = []
    for num, den in [*pairs(draw, 4), (-1, 2), (-3, 4)]:
        gamma = draw.randint(2, 12)
        edge = math.isqrt(rule3.guard_edge_squared(num, den, gamma))
        for pace in sorted({1, edge, draw.randint(1, edge)}):
            multipliers = pi_mode_multiplier(num, den, gamma, pace)
            inside &= all(-2 <= m <= 2 for m in multipliers)
            inside &= one_mode_orbit([multipliers[0]], 40) <= 41
        lowest = min(pi_mode_multiplier(num, den, gamma, edge + 1))
        beyond &= lowest < -2
        extreme = (
            0 if num > 0 else 1
        )  # the lowest mode: at pi for a positive numerator, at 0 for a negative one
        alternating = one_mode_orbit(
            [
                pi_mode_multiplier(num, den, gamma, 1)[extreme],
                pi_mode_multiplier(num, den, gamma, edge)[extreme],
            ],
            40,
        )
        parametric &= alternating > 41
        witnesses.append(
            f"[{num}, {den}] Gamma {gamma} P {edge}: beyond P {float(lowest):.3f}, parametric {float(alternating):.2e}"
        )
    return Row(
        "Beyond P the mode at wave number pi on every axis grows with",
        inside,
        beyond and parametric,
        "; ".join(witnesses[:3]) + " ...",
    )


def the_step_is_a_bijection() -> Row:
    """Theorem 1 (Section 4.1), 'The direction of time belongs to the clicks and not to the board': on a 3x3x3 periodic board at random integer paces the integer step followed by the backward act returns every level and remainder bit for bit over ten intervals, and distinct states map to distinct states; the click's draw is the NodeDetector's act (kind (e)) and no algebra of the line, so the claim has no outside to test here."""
    draw = random.Random(SEED)
    shape = (3, 3, 3)
    nodes, arrivals = box_nodes(shape), box_arrivals(shape)
    returns, injective = True, True
    for num, den in pairs(draw, 3):
        gamma = draw.randint(2, 9)
        clock, links = (
            draw.randint(1, gamma),
            (draw.randint(1, gamma), draw.randint(1, gamma), draw.randint(1, gamma)),
        )
        wall, _, _ = rule3.coefficients(num, den, gamma, clock, links)
        before, now = levels(draw, len(nodes)), levels(draw, len(nodes))
        remainders = [draw.randint(0, wall - 1) for _ in nodes]
        start = (list(before), list(now), list(remainders))
        images = set()
        for _ in range(10):
            stepped = [
                rule3.step(
                    now[i],
                    before[i],
                    [now[j] for j in arrivals[i]],
                    num,
                    den,
                    remainders[i],
                    gamma,
                    clock,
                    links,
                )
                for i in range(len(nodes))
            ]
            before, now, remainders = now, [s[0] for s in stepped], [s[1] for s in stepped]
            images.add((tuple(before), tuple(now), tuple(remainders)))
        injective &= len(images) == 10
        for _ in range(10):
            back = [
                rule3.step_backward(
                    before[i],
                    now[i],
                    [before[j] for j in arrivals[i]],
                    num,
                    den,
                    remainders[i],
                    gamma,
                    clock,
                    links,
                )
                for i in range(len(nodes))
            ]
            now, before, remainders = before, [b[0] for b in back], [b[1] for b in back]
        returns &= (before, now, remainders) == start
    return Row(
        "The direction of time belongs to the clicks and not to the b",
        returns and injective,
        None,
        "10 steps forward and 10 back on 3x3x3 at 3 pairs return the state bit for bit; the 10 images distinct; the click's draw is the engine's act, no outside here",
    )


def shears_exact_angle() -> Row:
    """Section 5.5 ('The exact angle of the shears is 2 arctan(L p_0 / (2 Gamma^2)), which is (L / Gamma)(p_0 / Gamma) at small angles'), the ledger's row 9: the three shears x_1 = x - t y, y_1 = y + sin(theta) x_1, x_2 = x_1 - t y_1 at t = L p_0 / (2 Gamma^2) and sin theta = 2 t / (1 + t^2) turn (x, y) by the rotation with cos theta = (1 - t^2) / (1 + t^2), exactly in rationals at random L, p_0 and Gamma, and that angle is 2 arctan t; outside the small-angle form: at L of the order Gamma^2 / p_0 the product (L / Gamma)(p_0 / Gamma) departs from 2 arctan t by more than five percent."""
    draw = random.Random(SEED)
    exact, departs = True, False
    for _ in range(100):
        gamma = draw.randint(2, 50)
        p_0 = draw.randint(1, gamma)
        level = draw.choice(
            (
                draw.randint(-gamma, gamma),
                draw.randint(-2 * gamma * gamma // p_0, 2 * gamma * gamma // p_0),
            )
        )
        t = Fraction(level * p_0, 2 * gamma * gamma)
        sine, cosine = 2 * t / (1 + t * t), (1 - t * t) / (1 + t * t)
        x, y = Fraction(draw.randint(-30, 30)), Fraction(draw.randint(-30, 30))
        x_1 = x - t * y
        y_1 = y + sine * x_1
        x_2 = x_1 - t * y_1
        exact &= (x_2, y_1) == (cosine * x - sine * y, sine * x + cosine * y)
        angle = math.atan2(float(sine), float(cosine))
        exact &= abs(angle - 2 * math.atan(float(t))) < 1e-12
        small = (level / gamma) * (p_0 / gamma)
        if abs(t) > Fraction(1, 2):
            departs |= abs(small - angle) > 0.05 * abs(angle)
    return Row(
        "The exact angle of the shears is 2arctanL p0 2Gamma2 which i",
        exact,
        departs,
        "100 random (L, p_0, Gamma): the three shears equal the rotation by 2 arctan t exactly; the small-angle form departs by over 5 percent where |t| > 1 / 2",
    )


def chsh_of_local_responses_at_most_two() -> Row:
    """Section 9.4 ('every local credit of it gives |S| <= 2'): random local responses A(a, lambda), B(b, lambda) in {-1, +1} over a shared variable lambda with random rational weights, 300 draws, S = E(a, b) - E(a, b') + E(a', b) + E(a', b') with each E the weighted mean of the products: |S| <= 2 exactly, the pointwise combination being +-2; outside the local credits: the declared credit through the root gives S = 478 / 169 > 2 at the integer settings (bell.declared_pairs)."""
    draw = random.Random(SEED)
    bounded, pointwise = True, True
    for _ in range(300):
        count = draw.randint(1, 8)
        weights = [Fraction(draw.randint(1, 9)) for _ in range(count)]
        total = sum(weights)
        responses = [
            [draw.choice((-1, 1)) for _ in range(4)] for _ in range(count)
        ]  # A(a), A(a'), B(b), B(b')
        s = Fraction(0)
        for weight, (a, a_prime, b, b_prime) in zip(weights, responses, strict=True):
            combination = a * b - a * b_prime + a_prime * b + a_prime * b_prime
            pointwise &= abs(combination) == 2
            s += weight / total * combination
        bounded &= abs(s) <= 2
    root = bell.declared_pairs()[-1]
    return Row(
        "And a pair is one laid record its phase a shared classical v",
        bounded and pointwise,
        root > 2,
        f"300 random local response tables: |S| <= 2, each lambda's combination +-2; the root's credit S = {root} = {float(root):.4f}",
    )


def three_exact_massive_rotations() -> Row:
    """Section 6.1 ('exact in integers only where 2 cos omega_0 is an integer; three exact massive rotations, 2 cos omega_0 = 1, 0, -1 with the periods 6, 4, 3'): over every pair with den <= 60 and |num| < den, 2 num / den is an integer only at num / den in {1 / 2, 0, -1 / 2}; the one-Node integer step at Gamma = 1 from (1, 0) returns with every remainder 0 after 6, 4 and 3 steps at [1, 2], [0, 1], [-1, 2]; outside: at every other pair with den <= 12 the line without its division leaves the integers at the first step from (1, 0), and the carried step's remainders are not all 0 over 12 steps."""
    exact_pairs = sorted(
        {(num, den) for den in range(1, 61) for num in range(-den + 1, den) if (2 * num) % den == 0}
    )
    ratios = sorted({Fraction(num, den) for num, den in exact_pairs})
    only_three = ratios == [Fraction(-1, 2), Fraction(0), Fraction(1, 2)]
    periods = {}
    for num, den in ((1, 2), (0, 1), (-1, 2)):
        before, now, remainder = 0, 1, 0
        for t in range(1, 13):
            now, before, (now, remainder) = (
                now,
                now,
                rule3.step(now, before, [now] * PORTS, num, den, remainder, 1, 1, (1, 1, 1)),
            )
            if (before, now, remainder) == (0, 1, 0):
                periods[(num, den)] = t
                break
    periods_hold = periods == {(1, 2): 6, (0, 1): 4, (-1, 2): 3}
    leaves_integers, remainders_appear = True, True
    for den in range(1, 13):
        for num in range(-den + 1, den):
            if (2 * num) % den == 0:
                continue
            leaves_integers &= rule3.step_exact(1, 0, [1] * PORTS, num, den).denominator != 1
            before, now, remainder, seen_nonzero = 0, 1, 0, False
            for _ in range(12):
                now, before, (now, remainder) = (
                    now,
                    now,
                    rule3.step(now, before, [now] * PORTS, num, den, remainder, 1, 1, (1, 1, 1)),
                )
                seen_nonzero |= remainder != 0
            remainders_appear &= seen_nonzero
    return Row(
        "So the rule carries exactly three exact massive rotations 2c",
        only_three and periods_hold,
        leaves_integers and remainders_appear,
        f"integer 2 num / den strictly inside (-2, 2) only at {[str(r) for r in ratios]} over den <= 60; periods {periods}; every other pair with den <= 12 leaves the integers at step one and carries a remainder",
    )


def in_the_mode_span(
    vector: Sequence[Fraction], mode: Sequence[Fraction], shifted: Sequence[Fraction]
) -> bool:
    """Whether the vector is a rational combination of cos(k x) and cos(k (x - 1)), the two spanning vectors of the wave number k, solved on two Nodes and checked on the rest."""
    determinant = mode[0] * shifted[1] - mode[1] * shifted[0]
    alpha = (vector[0] * shifted[1] - vector[1] * shifted[0]) / determinant
    beta = (mode[0] * vector[1] - mode[1] * vector[0]) / determinant
    return all(vector[x] == alpha * mode[x] + beta * shifted[x] for x in range(len(vector)))


def plane_wave_keeps_its_wave_number() -> Row:
    """Section 6 (m), 'A free record keeps its wave number: Rule3 is invariant under the lattice's translations where the paces are uniform': on a periodic chain of six Nodes the mode at k = pi / 3 (cos(k x) rational) spans a two-dimensional space the line without its division maps into itself over twelve steps at the vacuum's paces, exactly; the integer step leaves that span by the remainders' walk, under one unit per Node per step; outside the fence of uniform paces, a content on one Node takes the line's own next out of the span."""
    draw = random.Random(SEED)
    count, arrivals = 6, rule3.chain_arrivals(6)
    mode = [
        Fraction(c) for c in (1, Fraction(1, 2), Fraction(-1, 2), -1, Fraction(-1, 2), Fraction(1, 2))
    ]  # cos(pi x / 3)
    shifted = [mode[(x - 1) % count] for x in range(count)]
    kept, walk_small, walk_nonzero, uneven_leaves = True, True, False, False
    for num, den in pairs(draw, 4):
        coefficients = [Fraction(draw.randint(-9, 9)) for _ in range(4)]
        before = [coefficients[0] * mode[x] + coefficients[1] * shifted[x] for x in range(count)]
        now = [coefficients[2] * mode[x] + coefficients[3] * shifted[x] for x in range(count)]
        for _ in range(12):
            before, now = (
                now,
                [
                    rule3.step_exact(now[i], before[i], [now[j] for j in arrivals[i]], num, den)
                    for i in range(count)
                ],
            )
            kept &= in_the_mode_span(now, mode, shifted)
        integer_before, integer_now = (
            [2 * c for c in mode],
            [4 * c for c in mode],
        )  # integer levels in the span
        exact_next = [
            rule3.step_exact(
                integer_now[i], integer_before[i], [integer_now[j] for j in arrivals[i]], num, den
            )
            for i in range(count)
        ]
        integer_next = [
            rule3.step(
                int(integer_now[i]),
                int(integer_before[i]),
                [int(integer_now[j]) for j in arrivals[i]],
                num,
                den,
            )[0]
            for i in range(count)
        ]
        departure = [Fraction(integer_next[i]) - exact_next[i] for i in range(count)]
        walk_small &= all(abs(d) < 1 for d in departure)
        walk_nonzero |= not in_the_mode_span([Fraction(v) for v in integer_next], mode, shifted)
        gamma = 4
        clocks = [gamma] * count
        clocks[2] = gamma - 1  # one Node's content
        wall, reads, selves, _ = read(
            arrivals, clocks, [[gamma] * PORTS for _ in range(count)], num, den, gamma
        )
        uneven_next = step_line(arrivals, reads, selves, wall, now, before)
        uneven_leaves |= not in_the_mode_span(uneven_next, mode, shifted)
    return Row(
        "itemm A free record keeps its wave number Rule3 is invariant",
        kept and walk_small,
        walk_nonzero and uneven_leaves,
        "k = pi / 3 on a 6-chain kept over 12 exact steps at 4 pairs; the integer step leaves the span by under one unit per Node; a content on one Node leaves the span",
    )
