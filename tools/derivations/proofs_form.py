"""The conserved form's checks and the step's own (ALGEBRA.md, The direction, The conserved form, The sign is the rotation sense, The paces, The integer budget of a derived row, The integer-exact constructions; the paper's Theorems 1 and 3, S.9, S.32, S.33, S.48): every statement quoted in its function's docstring with its place, exact in Fractions and in Python's integers at random witnesses on small periodic boards with Link factors, the symmetric cases (uniform paces, no tension, static angles) forced.

Usage: `python tools/derivations/proofs_form.py` prints every verdict.
"""

from __future__ import annotations

import cmath
import math
import random
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule3  # noqa: E402
from proofs_ground import (  # noqa: E402
    PORTS,
    SEED,
    Check,
    Gaussian,
    angles,
    apply_read,
    box_arrivals,
    draw_angle,
    integer_witness,
    link_factors,
    pairs,
    read,
    run,
    step_integer,
    step_line,
)

Board = tuple[tuple[int, int, int], list[list[int]]]
BOARDS: tuple[Board, ...] = (
    ((3, 1, 1), box_arrivals((3, 1, 1))),
    ((4, 1, 1), box_arrivals((4, 1, 1))),
    ((2, 2, 1), box_arrivals((2, 2, 1))),
    ((2, 2, 2), box_arrivals((2, 2, 2))),
)


def witness(
    draw: random.Random, arrivals: Sequence[Sequence[int]], gamma: int, uniform: bool, tension: bool
):
    """Clocks and Link factors of a board: the vacuum's (uniform, no tension) when forced, else random contents and random Link factors read the same from both ends."""
    count = len(arrivals)
    clocks = (
        [gamma] * count if uniform else [draw.randint(max(1, gamma // 2), gamma) for _ in range(count)]
    )
    factors = link_factors(
        arrivals, draw if tension else None, gamma, spread=gamma // 3 if tension else 0
    )
    return clocks, factors


def weighted_form(reads, selves, wall, paces, arrivals, now, before, num: int, gamma: int) -> Fraction:
    """E of The conserved form: SUM_i [w (now_i^2 + before_i^2) - S_i now_i before_i] / p_i^2 - 2 num SUM_i SUM_(j ~ i) (q_ij^2 / Gamma^2) now_i before_j, the Link's factor squared read off R_ij = 2 num p_i^2 q_ij^2 / Gamma^2 as R_ij / (2 num p_i^2)."""
    total = Fraction(0)
    for i, ports in enumerate(arrivals):
        total += (
            wall * (Fraction(now[i]) ** 2 + Fraction(before[i]) ** 2) - selves[i] * now[i] * before[i]
        ) / paces[i] ** 2
        for port, j in enumerate(ports):
            total -= 2 * num * (reads[i][port] / (2 * num * paces[i] ** 2)) * now[i] * before[j]
    return total


def plain_form(reads, selves, wall, paces, arrivals, now, before, num: int) -> Fraction:
    """The same form with the plain Link term -2 num SUM_i now_i S_6(before)_i, the Link factor dropped (S.32)."""
    total = Fraction(0)
    for i, ports in enumerate(arrivals):
        total += (
            wall * (Fraction(now[i]) ** 2 + Fraction(before[i]) ** 2) - selves[i] * now[i] * before[i]
        ) / paces[i] ** 2
        total -= 2 * num * sum(Fraction(now[i]) * before[j] for j in ports)
    return total


def two_level_form(reads, selves, wall, paces, arrivals, x, y) -> Fraction:
    """Q(x, y) = x . D x + y . D y - x . D M y with D = diag(1 / p_i^2) and M the line's matrix (The conserved form's proof): E = w Q."""
    read_y = apply_read(arrivals, reads, selves, y)
    return sum(
        (Fraction(x[i]) ** 2 + Fraction(y[i]) ** 2 - Fraction(x[i]) * read_y[i] / wall) / paces[i] ** 2
        for i in range(len(x))
    )


def check_rule3s_coefficients_are_the_reads_own_without_tension() -> Check:
    """The paces: p_a(i, j)^2 = p_i^2 q_ij^2 / Gamma^2 with p_i = p_0(i)^2 / Gamma, so at q_ij = Gamma the Link's read coefficient 2 num p_i^2 q_ij^2 / Gamma^2 is rule3.coefficients' R_a = 2 num p_a^2 at p_a = p_i and the self coefficient 12 den Gamma^2 - 12 (den - num) p_0^2 - SUM over the six Ports of R_ij is rule3's S: the general read of proofs_ground and the derivations' Rule3 are one line where no tension stands."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 8):
        gamma = draw.randint(2, 40)
        for _shape, arrivals in BOARDS:
            clocks, factors = witness(draw, arrivals, gamma, uniform=False, tension=False)
            wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
            for i in range(len(arrivals)):
                own_wall, own_reads, own_self = rule3.coefficients(
                    num, den, gamma, clocks[i], (paces[i],) * 3
                )
                if (
                    wall != own_wall
                    or selves[i] != own_self
                    or any(reads[i][port] != own_reads[port // 2] for port in range(PORTS))
                ):
                    return False, {
                        "pair": (num, den),
                        "Node": i,
                        "rule3": (own_wall, own_reads, own_self),
                        "read": (wall, reads[i], selves[i]),
                    }
    return True, {"pairs": 8, "boards": len(BOARDS)}


def check_theorem_3_the_weighted_form_is_exact_in_the_line() -> Check:
    """Theorem 3 (ALGEBRA.md, The conserved form; the paper's Section 4.3; S.48): without the rounding the line is a_next + a_before = M a_now; with D = diag(1 / p_i^2), p_i = p_0(i)^2 / Gamma, D M is symmetric under the law's read coefficient R_a(i -> j) = 2 num p_i^2 q_ij^2 / Gamma^2 with q_ij = q_ji, and Q(x, y) = x . D x + y . D y - x . D M y satisfies Q(a_next, a_now) = Q(a_now, a_before); multiplied by w this is E, exact for any field and any tensions; checked in exact fractions on four periodic boards over several intervals, the vacuum's paces and the no-tension cases forced, and E = w Q."""
    draw = random.Random(SEED)
    intervals = 0
    for num, den in pairs(draw, 6):
        gamma = draw.randint(3, 30)
        for shape, arrivals in BOARDS:
            for uniform, tension in ((True, False), (False, False), (True, True), (False, True)):
                clocks, factors = witness(draw, arrivals, gamma, uniform, tension)
                wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
                for i, ports in enumerate(arrivals):
                    for port, j in enumerate(ports):
                        partner = (
                            port if i == j else arrivals[j].index(i)
                        )  # a folded axis's self-Link is its own partner
                        if reads[i][port] / paces[i] ** 2 != reads[j][partner] / paces[j] ** 2:
                            return False, {"D M not symmetric at": (i, j)}
                now = [Fraction(draw.randint(-50, 50)) for _ in arrivals]
                before = [Fraction(draw.randint(-50, 50)) for _ in arrivals]
                start = weighted_form(reads, selves, wall, paces, arrivals, now, before, num, gamma)
                if start != wall * two_level_form(reads, selves, wall, paces, arrivals, now, before):
                    return False, {"E is not w Q": (shape, uniform, tension)}
                for _ in range(5):
                    now, before = step_line(arrivals, reads, selves, wall, now, before), now
                    intervals += 1
                    if (
                        weighted_form(reads, selves, wall, paces, arrivals, now, before, num, gamma)
                        != start
                    ):
                        return False, {
                            "pair": (num, den),
                            "board": shape,
                            "uniform": uniform,
                            "tension": tension,
                        }
    return True, {"intervals checked": intervals}


def check_the_plain_form_fails_under_a_tension_the_two_witnesses_of_s32() -> Check:
    """S.32, the conserved form's Link factor, two witnesses: three Nodes along x with y and z folded, [1, 1], Gamma = 4, q = 2 (R = 8, w = 96, S = 144), now = (1, 0, 0), before = 0: one step gives next = (11 / 6, 1 / 12, 1 / 12), the plain form goes from 6 to -21 / 4 and Eq. (6) stays 6; 3^3 Nodes at [2, 3], Gamma = 10, q = 5 (R = 100, w = 1,800, S = 1,800), a uniform now = 3 over before = 0: next = 4 at every Node with the remainder 0, the plain form per Node from 162 to -54 and Eq. (6) 162 (4,374 over the board); at q = Gamma the two forms coincide."""
    arrivals = box_arrivals((3, 1, 1))
    wall, reads, selves, paces = read(arrivals, [4, 4, 4], [[2] * PORTS] * 3, 1, 1, 4)
    if (wall, reads[0][0], selves[0]) != (96, 8, 144):
        return False, {"first witness coefficients": (wall, reads[0][0], selves[0])}
    now, before = [Fraction(1), Fraction(0), Fraction(0)], [Fraction(0)] * 3
    after = step_line(arrivals, reads, selves, wall, now, before)
    first = (
        after,
        plain_form(reads, selves, wall, paces, arrivals, now, before, 1),
        plain_form(reads, selves, wall, paces, arrivals, after, now, 1),
        weighted_form(reads, selves, wall, paces, arrivals, now, before, 1, 4),
        weighted_form(reads, selves, wall, paces, arrivals, after, now, 1, 4),
    )
    first_holds = first == (
        [Fraction(11, 6), Fraction(1, 12), Fraction(1, 12)],
        6,
        Fraction(-21, 4),
        6,
        6,
    )
    arrivals = box_arrivals((3, 3, 3))
    wall, reads, selves, paces = read(arrivals, [10] * 27, [[5] * PORTS] * 27, 2, 3, 10)
    now, before, remainders = [3] * 27, [0] * 27, [0] * 27
    levels, carried = step_integer(arrivals, reads, selves, wall, now, before, remainders)
    second = (
        (wall, reads[0][0], selves[0]),
        set(levels),
        set(carried),
        plain_form(reads, selves, wall, paces, arrivals, now, before, 2) / 27,
        plain_form(reads, selves, wall, paces, arrivals, levels, now, 2) / 27,
        weighted_form(reads, selves, wall, paces, arrivals, now, before, 2, 10) / 27,
        weighted_form(reads, selves, wall, paces, arrivals, levels, now, 2, 10),
    )
    second_holds = second == ((1800, 100, 1800), {4}, {0}, 162, -54, 162, 4374)
    gamma = 7
    arrivals = box_arrivals((3, 1, 1))
    wall, reads, selves, paces = read(arrivals, [gamma] * 3, [[gamma] * PORTS] * 3, 2, 3, gamma)
    now, before = [Fraction(5), Fraction(-2), Fraction(1)], [Fraction(3), Fraction(0), Fraction(-4)]
    coincide = plain_form(reads, selves, wall, paces, arrivals, now, before, 2) == weighted_form(
        reads, selves, wall, paces, arrivals, now, before, 2, gamma
    )
    return first_holds and second_holds and coincide, {"first": first, "second": second}


def check_the_remainders_walk_of_the_form() -> Check:
    """The conserved form's proof, last sentence; row 7 of The conventions and the units; the paper's Section 4.3: with the rounding, the integer step's next = next* + (r - r') / w adds to the two-level form Q the walk SUM_i epsilon_i (next_i - before_i) with epsilon_i = (r_i - r_i') / w, so E = w Q walks by SUM_i (r_i - r_i') (next_i - before_i) / p_i^2 (rule3.form_walk), each term below one unit of the level's change; and the three-level form E_3 = SUM_i (now_i^2 - next_i before_i) / p_i^2 walks by SUM_i [epsilon_i(t) next_i - epsilon_i(t + 1) now_i] / p_i^2; exact in integers on the four boards with tensions, 40 intervals each."""
    draw = random.Random(SEED)
    steps = 0
    for num, den in pairs(draw, 5):
        for shape, arrivals in BOARDS:
            gamma, clocks, factors = integer_witness(draw, arrivals, draw.randint(2, 9), tension=True)
            wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
            count = len(arrivals)
            now = [draw.randint(-300, 300) for _ in range(count)]
            before = [draw.randint(-300, 300) for _ in range(count)]
            remainders = [draw.randint(0, int(wall) - 1) for _ in range(count)]
            levels, carried = step_integer(arrivals, reads, selves, wall, now, before, remainders)
            for _ in range(40):
                energy = weighted_form(reads, selves, wall, paces, arrivals, now, before, num, gamma)
                after = weighted_form(reads, selves, wall, paces, arrivals, levels, now, num, gamma)
                walk = sum(
                    Fraction((r - r_out) * (nxt - prev)) / paces[i] ** 2
                    for i, (r, r_out, nxt, prev) in enumerate(
                        zip(remainders, carried, levels, before, strict=True)
                    )
                )
                if after - energy != walk:
                    return False, {
                        "pair": (num, den),
                        "board": shape,
                        "E walk": after - energy,
                        "claimed": walk,
                    }
                if after - energy != rule3.form_walk(
                    remainders, carried, levels, before, node_paces=paces
                ):
                    return False, {"rule3.form_walk differs": shape}
                further, carried_further = step_integer(
                    arrivals, reads, selves, wall, levels, now, carried
                )
                three_now = sum(
                    Fraction(now[i] ** 2 - levels[i] * before[i]) / paces[i] ** 2 for i in range(count)
                )
                three_next = sum(
                    Fraction(levels[i] ** 2 - further[i] * now[i]) / paces[i] ** 2 for i in range(count)
                )
                epsilon_now = [
                    Fraction(r - r_out, wall) for r, r_out in zip(remainders, carried, strict=True)
                ]
                epsilon_next = [
                    Fraction(r - r_out, wall) for r, r_out in zip(carried, carried_further, strict=True)
                ]
                claimed = sum(
                    (epsilon_now[i] * levels[i] - epsilon_next[i] * now[i]) / paces[i] ** 2
                    for i in range(count)
                )
                if three_next - three_now != claimed:
                    return False, {
                        "pair": (num, den),
                        "board": shape,
                        "E_3 walk": three_next - three_now,
                        "claimed": claimed,
                    }
                now, before, remainders, levels, carried = levels, now, carried, further, carried_further
                steps += 1
    return True, {"integer steps": steps}


def check_the_three_level_form_equals_the_two_level_form() -> Check:
    """Row 7 of The conventions and the units: the two-level form Q = SUM_i (now_i^2 + before_i^2) / p_i^2 - (1 / w) SUM_i (SUM_j R_ij now_j + S_i now_i) before_i / p_i^2 equals the three-level form E_3 = SUM_i D_i / p_i^2, D_i = now_i^2 - next_i before_i, exactly under the line (D M symmetric), and D_i = b^2 sin^2 omega on a plane wave; exact fractions on the four boards with tensions, and the plane wave at a rational angle."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 6):
        gamma = draw.randint(3, 20)
        for shape, arrivals in BOARDS:
            clocks, factors = witness(draw, arrivals, gamma, uniform=False, tension=True)
            wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
            now = [Fraction(draw.randint(-50, 50)) for _ in arrivals]
            before = [Fraction(draw.randint(-50, 50)) for _ in arrivals]
            after = step_line(arrivals, reads, selves, wall, now, before)
            three = sum(
                (now[i] ** 2 - after[i] * before[i]) / paces[i] ** 2 for i in range(len(arrivals))
            )
            if three != two_level_form(reads, selves, wall, paces, arrivals, now, before):
                return False, {"pair": (num, den), "board": shape}
    for rotation in angles(draw, 9):
        for phase in angles(draw, 9)[3:]:
            amplitude = draw.randint(1, 100)
            now, before, after = (
                amplitude * phase.re,
                amplitude * (phase * rotation).re,
                amplitude * (phase * rotation.conj()).re,
            )
            if now * now - after * before != amplitude * amplitude * rotation.im**2:
                return False, {
                    "plane wave D": (now * now - after * before, amplitude * amplitude * rotation.im**2)
                }
    return True, {"pairs": 6}


def forms_change_under_moving_paces() -> tuple[bool, bool, list]:
    """(the paper's transposed identity and the weighted identity hold, the law's form without the transpose holds at every witness, the departures of the law's form) for the form's change where the paces move, computed once for the two checks below."""
    draw = random.Random(SEED)
    departures = []
    for num, den in pairs(draw, 4):
        gamma = draw.randint(4, 20)
        for shape, arrivals in BOARDS[1:]:
            for uniform in (True, False):
                clocks_1, factors_1 = witness(draw, arrivals, gamma, uniform, tension=not uniform)
                clocks_2, factors_2 = witness(draw, arrivals, gamma, uniform, tension=not uniform)
                if uniform:  # one content over the board at each read, the two reads different
                    clocks_1 = [draw.randint(gamma // 2, gamma)] * len(arrivals)
                    clocks_2 = [draw.randint(gamma // 2, gamma)] * len(arrivals)
                wall, reads_1, selves_1, _ = read(arrivals, clocks_1, factors_1, num, den, gamma)
                _, reads_2, selves_2, paces_2 = read(arrivals, clocks_2, factors_2, num, den, gamma)
                count = len(arrivals)
                now = [Fraction(draw.randint(-50, 50)) for _ in range(count)]
                before = [Fraction(draw.randint(-50, 50)) for _ in range(count)]
                after = step_line(arrivals, reads_1, selves_1, wall, now, before)
                further = step_line(arrivals, reads_2, selves_2, wall, after, now)
                total_now = sum(now[i] ** 2 - after[i] * before[i] for i in range(count))
                total_next = sum(after[i] ** 2 - further[i] * now[i] for i in range(count))
                m1_now = [v / wall for v in apply_read(arrivals, reads_1, selves_1, now)]
                m2_now = [v / wall for v in apply_read(arrivals, reads_2, selves_2, now)]
                m2_transposed_now = [Fraction(0)] * count  # (M(t + 1)^T a_now)_j = SUM_i M_ij now_i
                for i, ports in enumerate(arrivals):
                    m2_transposed_now[i] += selves_2[i] / wall * now[i]
                    for port, j in enumerate(ports):
                        m2_transposed_now[j] += reads_2[i][port] / wall * now[i]
                with_transpose = sum(after[i] * (m1_now[i] - m2_transposed_now[i]) for i in range(count))
                without = sum(after[i] * (m1_now[i] - m2_now[i]) for i in range(count))
                if total_next - total_now != with_transpose:
                    return (
                        False,
                        False,
                        [("paper's form fails", shape, total_next - total_now, with_transpose)],
                    )
                if uniform and without != with_transpose:
                    return False, False, [("uniform paces, the two forms differ", shape)]
                if not uniform and without != with_transpose:
                    departures.append((shape, total_next - total_now - without))
                weighted_now = sum(
                    (now[i] ** 2 - after[i] * before[i]) / paces_2[i] ** 2 for i in range(count)
                )
                weighted_next = sum(
                    (after[i] ** 2 - further[i] * now[i]) / paces_2[i] ** 2 for i in range(count)
                )
                claimed = sum(after[i] * (m1_now[i] - m2_now[i]) / paces_2[i] ** 2 for i in range(count))
                if weighted_next - weighted_now != claimed:
                    return (
                        False,
                        False,
                        [("weighted form's change fails", shape, weighted_next - weighted_now, claimed)],
                    )
    return True, not departures, departures


def check_the_forms_change_under_moving_paces() -> Check:
    """The paper's Section 4.3: where the paces move, the total form D = |a_now|^2 - <a_next, a_before> changes exactly, in the rationals, by D(t + 1) - D(t) = <a_next, (M(t) - M(t + 1)^T) a_now>, M symmetric at uniform paces alone, where the transpose drops; for the weighted form E = SUM_i (now_i^2 - next_i before_i) / p_i^2 with the weights of the paces at t + 1, E(t + 1) - E(t) = a_next^T D (M(t) - M(t + 1)) a_now; exact fractions, two reads with different contents on three boards, the uniform case forced."""
    paper_holds, _, departures = forms_change_under_moving_paces()
    return paper_holds, {"witnesses with differing paces": len(departures) + 4}


def check_the_laws_form_change_without_the_transpose() -> Check:
    """The mass defect is the form's fall at a kept count (ALGEBRA.md, The surplus leaves): "the line a_next = M(t) a_now - a_before with the paces changing in time changes the total form D = |a_now|^2 - <a_next, a_before> by exactly D(t + 1) - D(t) = <a_next, (M(t) - M(t + 1)) a_now> (Theorem, from the line by substitution)": the identity as printed holds where M(t + 1) is symmetric, the paces uniform over the board, which is where its check was run; where the paces differ across the board the exact change carries M(t + 1)^T (the paper's Section 4.3), and the law's form departs from it; a finding, the law's line to carry the transpose or the clause "at paces uniform over the board"."""
    _, law_holds, departures = forms_change_under_moving_paces()
    return law_holds, {
        "the law's form departs at differing paces by": departures[:3],
        "cases": len(departures),
    }


def check_theorem_1_the_direction() -> Check:
    """Theorem 1 (ALGEBRA.md, The direction; S.48): with u = sigma (SUM_a R_a arr_a + S x - w y) + rho, z = sigma (u div w), rho' = u mod w, the forward call (x, y, rho) = (a_now, a_before, r) gives (a_next, r') and the backward call (a_now, a_next, r') gives (a_before, r) bit for bit; the proof's identity -floor(u / w) = ceil(-u / w) and ceil((w a - r) / w) = a for 0 <= r < w; the identities checked for every residue of u modulo w at every w to 40 (both sides shift by one when u shifts by w, so the residues prove every integer), the round trip on rule3.step and rule3.step_backward at random integers on a chain."""
    for wall in range(1, 41):
        for u in range(-wall, wall):
            if math.ceil(Fraction(-u, wall)) != -(u // wall):  # -floor(u / w) = ceil(-u / w)
                return False, {"w": wall, "u": u}
        for a in range(-3, 4):
            for r in range(wall):
                if math.ceil(Fraction(wall * a - r, wall)) != a:  # ceil((w a - r) / w) = a
                    return False, {"ceiling identity": (wall, a, r)}
    draw = random.Random(SEED)
    arrivals = rule3.chain_arrivals(7)
    trips = 0
    for num, den in pairs(draw, 6):
        gamma = draw.randint(2, 50)
        clock, links = (
            draw.randint(1, gamma),
            (draw.randint(1, gamma), draw.randint(1, gamma), draw.randint(1, gamma)),
        )
        wall = rule3.coefficients(num, den, gamma, clock, links)[0]
        now = [draw.randint(-(10**6), 10**6) for _ in range(7)]
        before = [draw.randint(-(10**6), 10**6) for _ in range(7)]
        remainders = [draw.randint(0, wall - 1) for _ in range(7)]
        for _ in range(20):
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
                for i in range(7)
            ]
            levels, carried = [s[0] for s in stepped], [s[1] for s in stepped]
            back = [
                rule3.step_backward(
                    now[i],
                    levels[i],
                    [now[j] for j in arrivals[i]],
                    num,
                    den,
                    carried[i],
                    gamma,
                    clock,
                    links,
                )
                for i in range(7)
            ]
            if [b[0] for b in back] != before or [b[1] for b in back] != remainders:
                return False, {
                    "pair": (num, den),
                    "back": back,
                    "before": before,
                    "remainders": remainders,
                }
            now, before, remainders = levels, now, carried
            trips += 1
    return True, {"round trips": trips}


def check_the_complement_identity_of_the_cubes_symmetry() -> Check:
    """The cube's symmetry (ALGEBRA.md, The direction), the proof's act (1): for a signed component every term of the numerator is negated and the remainder is w - 1 - r, so u(g x) = w - 1 - u, and floor((w - 1 - u) / w) = -floor(u / w) for every integer u, the ones' complement commuting with the floor division by a positive wall; its remainder (w - 1 - u) mod w = w - 1 - r'; and the zero-remainder lay is not symmetric, floor(-u / w) = -ceil(u / w) differing from -floor(u / w) wherever w does not divide u; every residue of u at every w to 60."""
    for wall in range(1, 61):
        for u in range(-2 * wall, 2 * wall):
            quotient, remainder = divmod(u, wall)
            image_quotient, image_remainder = divmod(wall - 1 - u, wall)
            if image_quotient != -quotient or image_remainder != wall - 1 - remainder:
                return False, {"w": wall, "u": u}
            if ((-u) // wall == -quotient) != (u % wall == 0):
                return False, {"zero-remainder mirror": (wall, u)}
    return True, {"walls": 60}


def check_the_wronskian_is_conserved_with_the_forms_weights() -> Check:
    """The sign is the rotation sense (ALGEBRA.md, The paces); S.9: the two parts (re, im) step by the same read matrix M with D M symmetric, and W = re_now^T D im_before - im_now^T D re_before is invariant under the line; per Node W_i / p_i^2 changes by (2 num / w) (q_ij^2 / Gamma^2) (im_i re_j - re_i im_j) summed over the six Ports at the levels now, the Wronskian's current, (num / (3 den)) (im_i re_j - re_i im_j) per Port for the integer W_i at the vacuum's paces; S.9's witness, a chain of three at Gamma = 2, [1, 1], re_now = (0, 3, 0), im_now = (3, 0, 0), zeros before, steps to (1, 4, 1) and (4, 1, 1) with no remainder, W_0 from 0 to 3, W_0 / p_0^2 by 3 / 4, the current (2 / 24) 9 = 3 / 4; and the integer step's counterexample, at [2, 3] a uniform level (1, 3) over zeros steps to (1, 4) and W goes from 0 to -1; exact fractions and integers."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 5):
        gamma = draw.randint(3, 20)
        for shape, arrivals in BOARDS:
            clocks, factors = witness(draw, arrivals, gamma, uniform=False, tension=True)
            wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
            count = len(arrivals)
            re_now, im_now = (
                [Fraction(draw.randint(-40, 40)) for _ in range(count)],
                [Fraction(draw.randint(-40, 40)) for _ in range(count)],
            )
            re_before, im_before = (
                [Fraction(draw.randint(-40, 40)) for _ in range(count)],
                [Fraction(draw.randint(-40, 40)) for _ in range(count)],
            )
            total = sum(
                (re_now[i] * im_before[i] - im_now[i] * re_before[i]) / paces[i] ** 2
                for i in range(count)
            )
            re_next, im_next = (
                step_line(arrivals, reads, selves, wall, re_now, re_before),
                step_line(arrivals, reads, selves, wall, im_now, im_before),
            )
            for i, ports in enumerate(arrivals):
                change = (
                    (re_next[i] * im_now[i] - im_next[i] * re_now[i])
                    - (re_now[i] * im_before[i] - im_now[i] * re_before[i])
                ) / paces[i] ** 2
                current = sum(
                    2
                    * num
                    / wall
                    * (reads[i][port] / (2 * num * paces[i] ** 2))
                    * (im_now[i] * re_now[j] - re_now[i] * im_now[j])
                    for port, j in enumerate(ports)
                )
                if change != current:
                    return False, {
                        "pair": (num, den),
                        "board": shape,
                        "Node": i,
                        "change": change,
                        "current": current,
                    }
            if (
                sum(
                    (re_next[i] * im_now[i] - im_next[i] * re_now[i]) / paces[i] ** 2
                    for i in range(count)
                )
                != total
            ):
                return False, {"pair": (num, den), "board": shape, "moved": "the total W"}
    arrivals = rule3.chain_arrivals(3)
    re_now, im_now = [0, 3, 0], [3, 0, 0]
    re_step = [rule3.step(re_now[i], 0, [re_now[j] for j in arrivals[i]], 1, 1, 0, 2) for i in range(3)]
    im_step = [rule3.step(im_now[i], 0, [im_now[j] for j in arrivals[i]], 1, 1, 0, 2) for i in range(3)]
    re_next, im_next = [s[0] for s in re_step], [s[0] for s in im_step]
    remainders = {s[1] for s in re_step + im_step}
    wronskian = re_next[0] * im_now[0] - im_next[0] * re_now[0]
    current = Fraction(2, 24) * sum(im_now[0] * re_now[j] - re_now[0] * im_now[j] for j in arrivals[0])
    witness_holds = (re_next, im_next, remainders, wronskian, Fraction(wronskian, 4), current) == (
        [1, 4, 1],
        [4, 1, 1],
        {0},
        3,
        Fraction(3, 4),
        Fraction(3, 4),
    )
    # one Node with every axis folded: the six arrivals are the Node's own level
    re_one, im_one = (
        rule3.step(1, 0, [1] * PORTS, 2, 3, 0, 5)[0],
        rule3.step(3, 0, [3] * PORTS, 2, 3, 0, 5)[0],
    )
    counterexample = (re_one, im_one, re_one * 3 - im_one * 1)
    return witness_holds and counterexample == (1, 4, -1), {
        "S.9 witness": (re_next, im_next, wronskian, current),
        "integer counterexample W": counterexample,
    }


def plane_step(
    arrivals,
    reads,
    selves,
    wall,
    z_now: list[Gaussian],
    z_before: list[Gaussian],
    time_now: list[Gaussian],
    time_before: list[Gaussian],
    link_phase: list[list[Gaussian]],
) -> list[Gaussian]:
    """The plane record's step under the holder of the sign in the law's convention (row 9 of The conventions and the units): e^(i theta_t) z_next + e^(-i theta_(t-1)) z_before = (S z_now + SUM over the Ports of R_ij e^(+/- i theta_a) z_j) / w, the level before under the previous interval's angle, the level next under this one's, the Link's phase +theta_a through the +a Port and -theta_a through the -a Port (link_phase[i][port] the unit read through that Port)."""
    found = []
    for i, ports in enumerate(arrivals):
        right = z_now[i] * selves[i]
        for port, j in enumerate(ports):
            right = right + z_now[j] * link_phase[i][port] * reads[i][port]
        right = right / wall
        found.append((right - z_before[i] * time_before[i].conj()) * time_now[i].conj())
    return found


def wronskian_with_angle(z_now: Gaussian, z_before: Gaussian, time_before: Gaussian) -> Fraction:
    """W = Im(conj(z_now) e^(-i theta_(t-1)) z_before), the Wronskian read under the previous interval's angle, the law's conserved density under the time-Link turn (the plain re_now im_before - im_now re_before at theta = 0)."""
    return (z_now.conj() * time_before.conj() * z_before).im


def check_the_wronskian_under_the_time_link_turn_for_any_angle_in_time() -> Check:
    """What the GameBoard conserves (ALGEBRA.md, The conserved form); row 9; S.33 (a); the audit's item 2 (the advisor's 5977935062): under the rotation the plane record's level before is turned by the holder's level at the previous interval and its level next by the level now, so b_t = z_t e^(i Phi_t) with Phi_(t + 1) - Phi_t = theta_t obeys the flat recurrence exactly for any level in time, and the per-Node continuity identity w [W_i(t + 1) - W_i(t)] + SUM_a [R_a g_(i, i+a) - R_a g_(i-a, i)] = 0 holds at every Node and interval for any paces, any Link phases and any time angles, g_ij = Im(conj(z_i) e^(i theta_ij) z_j) antisymmetric, W_i = Im(conj(z_now) e^(-i theta_(t-1)) z_before); the weighted total SUM_i W_i / p_i^2 is then exactly conserved; the one-theta form (the paper's 5.5 sentence, one theta on both levels) conserves W at a static angle only: at the audit's one-Node witness (2 cos omega = 1, z_0 = 1, z_(-1) = e^(i pi / 3), theta_0 = 0, theta_1 = pi / 2) |z_2| = 1.93 against the law's 1.00; exact Gaussian rationals, the static and the phase-free cases forced."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 4):
        gamma = draw.randint(3, 20)
        for shape, arrivals in BOARDS:
            clocks, factors = witness(draw, arrivals, gamma, uniform=False, tension=True)
            wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
            count = len(arrivals)
            for static, plain in ((True, True), (True, False), (False, True), (False, False)):
                z_now = [Gaussian(draw.randint(-30, 30), draw.randint(-30, 30)) for _ in range(count)]
                z_before = [Gaussian(draw.randint(-30, 30), draw.randint(-30, 30)) for _ in range(count)]
                time_before = [Gaussian(1, 0) if static else draw_angle(draw) for _ in range(count)]
                phases: list[list[Gaussian]] = []
                table: dict[tuple[int, int, int], Gaussian] = {}
                for i, ports in enumerate(arrivals):
                    row = []
                    for port, j in enumerate(ports):
                        key = (min(i, j), max(i, j), port // 2 if i == j else -1)
                        if key not in table:
                            table[key] = Gaussian(1, 0) if plain or i == j else draw_angle(draw)
                        unit = table[key]
                        row.append(unit if (i < j or i == j) else unit.conj())
                    phases.append(row)
                for _ in range(6):
                    time_now = time_before if static else [draw_angle(draw) for _ in range(count)]
                    z_next = plane_step(
                        arrivals, reads, selves, wall, z_now, z_before, time_now, time_before, phases
                    )
                    for i, ports in enumerate(arrivals):
                        change = wall * (
                            wronskian_with_angle(z_next[i], z_now[i], time_now[i])
                            - wronskian_with_angle(z_now[i], z_before[i], time_before[i])
                        )
                        flux = Fraction(0)
                        for port, j in enumerate(ports):
                            g_ij = (z_now[i].conj() * phases[i][port] * z_now[j]).im
                            flux += reads[i][port] * g_ij
                        if change + flux != 0:
                            return False, {
                                "pair": (num, den),
                                "board": shape,
                                "Node": i,
                                "static": static,
                                "plain": plain,
                                "change + flux": change + flux,
                            }
                    before_total = sum(
                        wronskian_with_angle(z_now[i], z_before[i], time_before[i]) / paces[i] ** 2
                        for i in range(count)
                    )
                    after_total = sum(
                        wronskian_with_angle(z_next[i], z_now[i], time_now[i]) / paces[i] ** 2
                        for i in range(count)
                    )
                    if before_total != after_total:
                        return False, {
                            "pair": (num, den),
                            "board": shape,
                            "total W": (before_total, after_total),
                        }
                    z_now, z_before, time_before = z_next, z_now, time_now
    # the audit's one-Node witness, in floats: 2 cos omega = 1, z_0 = 1, z_(-1) = e^(i pi / 3), theta_0 = 0, theta_1 = pi / 2, the angle before the first step 0
    turns = [cmath.exp(1j * 0.0), cmath.exp(1j * math.pi / 2)]
    z_prev, z_cur = cmath.exp(1j * math.pi / 3), complex(1, 0)
    previous = cmath.exp(1j * 0.0)
    for turn in turns:  # the law: e^(i theta_t) z_next + e^(-i theta_(t-1)) z_before = z_now
        z_cur, z_prev, previous = (z_cur - previous.conjugate() * z_prev) * turn.conjugate(), z_cur, turn
    z_prev_one, z_cur_one = cmath.exp(1j * math.pi / 3), complex(1, 0)
    for turn in turns:  # the one-theta form: e^(-i theta) z_next + e^(i theta) z_before = z_now
        z_cur_one, z_prev_one = turn * (z_cur_one - turn * z_prev_one), z_cur_one
    moduli = (round(abs(z_cur), 2), round(abs(z_cur_one), 2))
    return moduli == (1.0, 1.93), {
        "|z_2| under the law's two-angle step and under the one-theta form": moduli
    }


def check_the_sign_currents_flux_over_density() -> Check:
    """S.33 (b); S.61 row 8: for the plane record z = A e^(i (k . x - omega t)) the density rho = w W = w A^2 sin omega and the flux through the Link (i, i + a) is R_a g_(i, i+a) = R_a A^2 sin k_a, so flux over density is (R_a / w) sin k_a / sin omega = d omega / dk_a, the current rho v exactly; the law's Node current J_a = g_(i, i+a) + g_(i-a, i) = 2 A^2 sin k_a obeys J_a = (6 den / num) W v on a plane record at the vacuum's paces, nature's j = rho v with the band's constant and no sin omega_b; the Wronskian and the Link quantity exact in Gaussian rationals at rational angles, the group velocity the band's."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 5):
        gamma = draw.randint(2, 20)
        wall, reads, _ = rule3.coefficients(num, den, gamma)
        for rotation in angles(draw, 8):
            for wave in angles(draw, 8):
                amplitude = draw.randint(1, 30)
                for phase in angles(draw, 6)[2:]:
                    z_now, z_before, z_plus, z_minus = (
                        Gaussian(amplitude, 0) * phase * u
                        for u in (Gaussian(1, 0), rotation, wave, wave.conj())
                    )
                    wronskian = (z_now.conj() * z_before).im
                    g_plus, g_minus = (
                        (z_now.conj() * z_plus).im,
                        (z_minus.conj() * z_now).im,
                    )  # g_(i, i+a) and g_(i-a, i)
                    if (
                        wronskian != amplitude**2 * rotation.im
                        or g_plus != amplitude**2 * wave.im
                        or g_minus != amplitude**2 * wave.im
                    ):
                        return False, {"pair": (num, den), "W or g": (wronskian, g_plus, g_minus)}
                    if rotation.im:
                        velocity = (
                            Fraction(reads[0], wall) * wave.im / rotation.im
                        )  # (R / w) sin k / sin omega, the band's group velocity
                        if (
                            Fraction(reads[0]) * g_plus / (wall * wronskian) != velocity
                            or g_plus + g_minus != Fraction(6 * den, num) * wronskian * velocity
                        ):
                            return False, {
                                "pair": (num, den),
                                "flux over density": Fraction(reads[0]) * g_plus / (wall * wronskian),
                            }
    return True, {"pairs": 5}


def check_the_velocity_invariant_of_the_massless_row() -> Check:
    """The click writes on the GameBoard, the restoring front's third test (ALGEBRA.md); ENGINE.md, the face's kicks: for a record at uniform paces with S + SUM R = 2 w (the massless row in a world without a holder of the content) the velocity sum D_t = SUM now - SUM before is kept by the line, and with the carry the integer V = w (SUM now - SUM before) + SUM r is exactly invariant on a periodic board, since summing the integer line over the board gives w (SUM next - SUM now) + SUM r' = (S + SUM R - 2 w) SUM now + w (SUM now - SUM before) + SUM r; for a gapped pair the term -12 (den - num) Gamma^2 SUM now is what moves it; exact integers on the periodic chain and box, 100 intervals, by rule3.step."""
    draw = random.Random(SEED)
    for shape, arrivals in BOARDS:
        count = len(arrivals)
        for num, den in ((1, 1), (2, 3), (4000, 6000)):
            gamma = draw.randint(2, 30)
            wall, reads, self_coefficient = rule3.coefficients(num, den, gamma)
            now = [draw.randint(-500, 500) for _ in range(count)]
            before = [draw.randint(-500, 500) for _ in range(count)]
            remainders = [draw.randint(0, wall - 1) for _ in range(count)]
            invariant = wall * (sum(now) - sum(before)) + sum(remainders)
            for _ in range(100):
                stepped = [
                    rule3.step(
                        now[i], before[i], [now[j] for j in arrivals[i]], num, den, remainders[i], gamma
                    )
                    for i in range(count)
                ]
                levels, carried = [s[0] for s in stepped], [s[1] for s in stepped]
                moved = (
                    wall * (sum(levels) - sum(now))
                    + sum(carried)
                    - (wall * (sum(now) - sum(before)) + sum(remainders))
                )
                if moved != (self_coefficient + 6 * reads[0] - 2 * wall) * sum(now):
                    return False, {"pair": (num, den), "board": shape, "moved": moved}
                if num == den and wall * (sum(levels) - sum(now)) + sum(carried) != invariant:
                    return False, {"massless V moved": shape}
                now, before, remainders = levels, now, carried
    return True, {"boards": len(BOARDS)}


def check_the_writes_total_is_exact_over_any_window() -> Check:
    """The integer-exact constructions are the preferred ones (4) (ALGEBRA.md, The generator): the sum over the window's n intervals of the written q_t is (the sum of the numerators + r_0 - r_n) / w exactly, the remainders telescoping, so the quantity written differs from the line's sum over w by (r_0 - r_n) / w, in (-1, 1); and The integer budget of a derived row: at a Node the terms (r_i - r_i') / w telescope over any n intervals to (r_0 - r_n) / w; exact integers at random numerators and walls."""
    draw = random.Random(SEED)
    for _ in range(50):
        wall = draw.randint(1, 10**6)
        remainder = draw.randint(0, wall - 1)
        start = remainder
        numerators = [draw.randint(-(10**9), 10**9) for _ in range(draw.randint(1, 60))]
        written = 0
        for numerator in numerators:
            quotient, remainder = divmod(numerator + remainder, wall)
            written += quotient
        if (
            Fraction(written) != Fraction(sum(numerators) + start - remainder, wall)
            or not -1 < Fraction(start - remainder, wall) < 1
        ):
            return False, {"wall": wall, "written": written}
    return True, {"windows": 50}


if __name__ == "__main__":
    sys.exit(run(sys.modules[__name__]))
