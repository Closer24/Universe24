"""ag2's one-Node tests of Rule3's step and the paces (the brief's items 1, 2 and 4a), integers only: the flux form and the first form one integer; the carried division's inverse exact; the one rule of the remainder (the mirror an involution, the ones' complement commuting with the floor, the two's complement failing where the wall divides); the odd rounding sign(x) rounded(|x|); the composed clock the exact power rounded half up at every content to the frozen one; the Link's pace the clock twice; the Wronskian even under the conjugation composed with time's exchange. Room: tests/test_rule3.py (the step), tests/test_integer_algebra.py (the identities)."""

from __future__ import annotations

import random

from event_universe.core import paces
from event_universe.core.rule3 import (
    carried_division,
    division_forward,
    flux_total,
    mirrored,
    rule3,
    rule_integers,
)
from event_universe.links import cross

gamma_toy, den_toy, unit_toy = 1000, 1021, 16  # the toy den of the law's tests and the Link unit at Gamma 1,000 (K-S1)
cases = 2000


def rounded_half_up(numerator: int, wall: int) -> int:
    """The exact rounding half up of a non-negative rational, (2 n + w) div (2 w), written apart from paces.rounded."""
    return (2 * numerator + wall) // (2 * wall)


def test_the_flux_form_and_the_first_form_are_one_integer() -> None:
    """ALGEBRA.md, The line and The flux form of Rule3: w (2 a - b) - D a + SUM R_j (m_j - a) = SUM R_j m_j + S a - w b with S = 2 w - D - SUM R_j, at every pace and every pair; the remainder in [0, w)."""
    rng = random.Random(7)
    for _ in range(cases):
        content = rng.randrange(0, 3000)
        clock, pace = paces.clock(gamma_toy, content), paces.link_pace(gamma_toy, content)
        num = rng.randrange(1, den_toy + 1)
        factors = tuple(rng.randrange(0, unit_toy * unit_toy + 1) for _ in range(6))
        rule = rule_integers(num, den_toy, gamma_toy, clock, pace, factors, unit_toy)
        a, b = rng.randrange(-10**9, 10**9), rng.randrange(-10**9, 10**9)
        m = [rng.randrange(-10**9, 10**9) for _ in range(6)]
        flux = sum(r * (mj - a) for r, mj in zip(rule.reaches, m, strict=True))
        first = sum(r * mj for r, mj in zip(rule.reaches, m, strict=True)) + rule.self_coefficient * a - rule.wall * b
        assert flux_total(flux, rule.mass, rule.wall, a, b) == first
        assert rule.self_coefficient == 2 * rule.wall - rule.mass - sum(rule.reaches)
        r = rng.randrange(0, rule.wall)
        a_next, r_next = rule3(flux, rule.mass, rule.wall, a, b, r, 1)
        assert 0 <= r_next < rule.wall
        assert rule.wall * a_next + r_next == first + r


def test_the_carried_division_is_its_own_inverse_at_direction_minus_one() -> None:
    """ALGEBRA.md, The direction: forward (a_now, a_before, r) to (a_next, r'); backward from (a_now, a_next, r') with the same flux the pair (a_before, r), bit for bit."""
    rng = random.Random(11)
    for _ in range(cases):
        wall = rng.randrange(1, 10**12)
        total = rng.randrange(-10**15, 10**15)
        r = rng.randrange(0, wall)
        q, r2 = carried_division(total, wall, r, 1)
        assert 0 <= r2 < wall and q * wall + r2 == total + r
        q_back, r_back = carried_division(total, wall, r2, -1)
        assert (q_back, r_back) == (q, r)  # sigma (u div w) with u = -total + r2 = r - q w: the quotient q and the remainder r back
        content = rng.randrange(0, 2000)
        clock, pace = paces.clock(gamma_toy, content), paces.link_pace(gamma_toy, content)
        rule = rule_integers(rng.randrange(1, den_toy + 1), den_toy, gamma_toy, clock, pace, None, unit_toy)
        a, b, rr = rng.randrange(-10**6, 10**6), rng.randrange(-10**6, 10**6), rng.randrange(0, rule.wall)
        flux = rng.randrange(-10**20, 10**20)
        a_next, r_next = rule3(flux, rule.mass, rule.wall, a, b, rr, 1)
        back = rule3(flux, rule.mass, rule.wall, a, a_next, r_next, -1)
        assert back == (b, rr)


def test_the_one_rule_of_the_remainder_mirror_complements_and_odd_rounding() -> None:
    """The one rule of the remainder, cases (iii) and (iv): the mirror w - 1 - r is an involution on [0, w); floor((w - 1 - u) div w) = -floor(u div w) for every integer u (the ones' complement commutes with the floor division); the two's complement w - r fails exactly where w divides u; the odd rounding is sign(x) rounded(|x|, w) and odd at every integer."""
    rng = random.Random(13)
    twos_failed = twos_cases = 0
    for _ in range(cases):
        wall = rng.randrange(1, 10**9)
        r = rng.randrange(0, wall)
        assert mirrored(mirrored(r, wall, 1), wall, 1) == r
        assert 0 <= mirrored(r, wall, 1) < wall
        assert mirrored(r, wall, 2) == r
        u = rng.randrange(-10**15, 10**15)
        assert (wall - 1 - u) // wall == -(u // wall)
        u2 = u - u % wall if rng.randrange(2) else u
        twos_cases += 1
        if ((wall - u2) // wall != -(u2 // wall)) == (u2 % wall == 0):
            twos_failed += 1
        x = rng.randrange(-10**12, 10**12)
        odd = int(paces.odd_rounded(x, wall))
        sign = 1 if x >= 0 else -1
        assert odd == sign * rounded_half_up(abs(x), wall)
        assert int(paces.odd_rounded(-x, wall)) == -odd
        assert int(paces.rounded(abs(x), wall)) == rounded_half_up(abs(x), wall)
        half = division_forward(wall, 2, 0)[0]
        assert division_forward(abs(x) + abs(x), wall + wall, wall)[0] == rounded_half_up(abs(x), wall)
        assert half == wall // 2
    assert twos_failed == twos_cases


def test_the_composed_clock_is_the_exact_power_rounded_half_up_to_the_frozen_content() -> None:
    """ALGEBRA.md, The paces and The paces compose (PC-S1): p_0(c) = Gamma (1 - 1 / Gamma)^c rounded half up, by one carried division per content at the wall Gamma from N_0 = Gamma^3 and r_0 = Gamma div 2, bit for bit the exact rational Gamma (Gamma - 1)^c / Gamma^c rounded, for every content from the hill -300 to the frozen content; the Link's pace p_0^2 div Gamma rounded once; the frozen content the least with the Link's pace 0."""
    frozen = paces.frozen_content(gamma_toy)
    assert paces.certified(gamma_toy) == frozen
    power_up, power_down = 1, 1  # (Gamma - 1)^c and Gamma^c
    for c in range(frozen + 1):
        exact = rounded_half_up(gamma_toy * power_up, power_down)
        clock = paces.clock(gamma_toy, c)
        assert clock == exact, (c, clock, exact)
        assert paces.link_pace(gamma_toy, c) == rounded_half_up(clock * clock, gamma_toy)
        power_up, power_down = power_up * (gamma_toy - 1), power_down * gamma_toy
    assert paces.link_pace(gamma_toy, frozen) == 0
    assert all(paces.link_pace(gamma_toy, c) > 0 for c in range(frozen))
    power_up, power_down = 1, 1  # Gamma^|c| and (Gamma - 1)^|c| on the hills
    for size in range(1, 301):
        power_up, power_down = power_up * gamma_toy, power_down * (gamma_toy - 1)
        assert paces.clock(gamma_toy, -size) == rounded_half_up(gamma_toy * power_up, power_down)
    assert paces.clock(gamma_toy, 0) == gamma_toy and paces.link_pace(gamma_toy, 0) == gamma_toy
    power_up, power_down, c = 1, 1, 0  # the frozen content derived: the least c with the exact clock at most 22, since rounded(p^2, 1000) = 0 iff p^2 < 500
    while rounded_half_up(gamma_toy * power_up, power_down) > 22:
        power_up, power_down, c = power_up * (gamma_toy - 1), power_down * gamma_toy, c + 1
    assert frozen == c == 3793


def test_the_wronskian_is_even_under_the_conjugation_composed_with_times_exchange() -> None:
    """The swap at the top (ws1): W = re_now im_before - im_now re_before is odd under T_0 (now and before exchanged), odd under C (im negated), even under C T_0; the exchange's remainders mirrored once for the re line and twice (kept) for the im line by the one rule."""
    rng = random.Random(17)
    for _ in range(cases):
        rn, rb, jn, jb = (rng.randrange(-10**9, 10**9) for _ in range(4))
        w = cross(rn, jn, rb, jb)
        assert cross(rb, jb, rn, jn) == -w
        assert cross(rn, -jn, rb, -jb) == -w
        assert cross(rb, -jb, rn, -jn) == w
