"""The booking's checks (ALGEBRA.md, The booking, The count is the record's share, The share's change is the currents, the share-conserved theorem, The tension, row 14 of The conventions and the units, The packet lay; the paper's Eqs. (7), (9), (10), (12 of S.50); S.5, S.7, S.50): the booking identity of the hole, the share identity at any paces with its integer term, the share conserved over a region, the plane wave's current and stress, the momentum flux with the remainders' term, the two share forms summed over the board, and the exact lay's operator line; exact in Fractions and integers at random witnesses, the symmetric cases forced.

Usage: `python tools/derivations/proofs_booking.py` prints every verdict.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule3  # noqa: E402
from proofs_ground import (  # noqa: E402
    PORTS,
    SEED,
    Check,
    angles,
    apply_read,
    box_arrivals,
    box_index,
    box_nodes,
    has_order,
    integer_witness,
    pairs,
    read,
    run,
    step_integer,
    step_line,
)

BOARDS = (box_arrivals((5, 1, 1)), box_arrivals((3, 2, 1)), box_arrivals((2, 2, 2)))


def hole_form(wall: int, reads: int, self_coefficient: int, arrivals, p, q) -> Fraction:
    """Q(p, q) = SUM_i [w p_i^2 + w q_i^2 - p_i (S q_i + SUM_j R_ij q_j)] at uniform coefficients (S.50, the hole's booking identity)."""
    return sum(
        wall * Fraction(p[i]) ** 2
        + wall * Fraction(q[i]) ** 2
        - Fraction(p[i]) * (self_coefficient * q[i] + reads * sum(q[j] for j in ports))
        for i, ports in enumerate(arrivals)
    )


def check_the_booking_identity_of_the_hole() -> Check:
    """S.50, the hole's booking identity (R289): with Q(p, q) the two-level form of a pair of consecutive levels at uniform coefficients, Rule3's line without the remainder, w (next_i + before_i) = S now_i + SUM_j R_ij now_j, gives Q(next, now) = Q(now, before) and, by R_ij = R_ji, Q(now, before) = w SUM_i D_i with D_i = now_i^2 - next_i before_i; a face writing x in place of the level v the step would write at one Node, the leaving level b standing, changes Q by (x - v) [w (x + v) - (S now_i + SUM_j R_ij now_j)] = w (x - v) (x - b), and the most one write removes is w (v - b)^2 / 4 at the midpoint; exact fractions on three periodic boards at the vacuum's and at uniform paces."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 6):
        gamma = draw.randint(2, 30)
        pace = draw.choice((gamma, draw.randint(1, gamma)))
        wall, reads, self_coefficient = rule3.coefficients(num, den, gamma, pace, (pace, pace, pace))
        for arrivals in BOARDS:
            count = len(arrivals)
            now = [Fraction(draw.randint(-60, 60)) for _ in range(count)]
            before = [Fraction(draw.randint(-60, 60)) for _ in range(count)]
            after = [
                (self_coefficient * now[i] + reads[0] * sum(now[j] for j in ports)) / wall - before[i]
                for i, ports in enumerate(arrivals)
            ]
            kept = hole_form(wall, reads[0], self_coefficient, arrivals, after, now)
            if kept != hole_form(wall, reads[0], self_coefficient, arrivals, now, before):
                return False, {"pair": (num, den), "differs": "Q(next, now) from Q(now, before)"}
            if kept != wall * sum(now[i] ** 2 - after[i] * before[i] for i in range(count)):
                return False, {"pair": (num, den), "differs": "Q from w SUM D"}
            node = draw.randrange(count)
            v, b = after[node], before[node]
            for x in (Fraction(draw.randint(-60, 60)), (v + b) / 2, v, b):
                written = list(after)
                written[node] = x
                change = hole_form(wall, reads[0], self_coefficient, arrivals, written, now) - kept
                if change != wall * (x - v) * (x - b):
                    return False, {
                        "pair": (num, den),
                        "x": x,
                        "change": change,
                        "w (x - v)(x - b)": wall * (x - v) * (x - b),
                    }
                if change < -wall * (v - b) ** 2 / 4:
                    return False, {"removed more than w (v - b)^2 / 4": x}
            if (
                hole_form(
                    wall,
                    reads[0],
                    self_coefficient,
                    arrivals,
                    [a if i != node else (v + b) / 2 for i, a in enumerate(after)],
                    now,
                )
                - kept
                != -wall * (v - b) ** 2 / 4
            ):
                return False, {"midpoint": node}
    return True, {"pairs": 6, "boards": len(BOARDS)}


def rational_share(wall, reads, selves, paces, arrivals, i: int, now, before) -> Fraction:
    """The share before its floor (Eq. (9); The count is the record's share): [w (now_i^2 + before_i^2) - S_i now_i before_i - now_i SUM_j R_ij before_j] / (2 p_i^2)."""
    link = sum(reads[i][port] * Fraction(before[j]) for port, j in enumerate(arrivals[i]))
    return (
        wall * (Fraction(now[i]) ** 2 + Fraction(before[i]) ** 2)
        - selves[i] * now[i] * before[i]
        - now[i] * link
    ) / (2 * paces[i] ** 2)


def check_the_share_identity_at_any_paces() -> Check:
    """The share's change is the currents (ALGEBRA.md); the paper's Eq. (10); S.5: at any paces, with the weighted share e_i and the line without its division, e_i(next*, now) - e_i(now, before) = SUM_j (q_ij^2 / Gamma^2) F_ij with F_ij = num (now_i before_j - before_i now_j), since R_ij / (2 p_i^2) = num q_ij^2 / Gamma^2 is the same from both ends; the integer step's next = next* + (r - r') / w adds -(next_i - before_i) (r'_i - r_i) / (2 p_i^2), because w (next_i + next*_i) - S_i now_i - SUM_j R_ij now_j = w (next_i - before_i); S.5's witnesses: a periodic chain of five Nodes at [2, 3], Gamma = 10, with contents 0 to 3 and Link factors 5 to 10 at random levels, with and without the division; and a uniform now = 3 over before = 0 at Gamma = 10, q = 5 reads 81 per Node where the mean-of-paces form read 324; exact fractions and integers."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 6):
        for arrivals in BOARDS:
            gamma, clocks, factors = integer_witness(draw, arrivals, draw.randint(2, 9), tension=True)
            wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
            count = len(arrivals)
            now = [draw.randint(-80, 80) for _ in range(count)]
            before = [draw.randint(-80, 80) for _ in range(count)]
            remainders = [draw.randint(0, int(wall) - 1) for _ in range(count)]
            exact_next = step_line(arrivals, reads, selves, wall, now, before)
            levels, carried = step_integer(arrivals, reads, selves, wall, now, before, remainders)
            for i, ports in enumerate(arrivals):
                change = rational_share(
                    wall, reads, selves, paces, arrivals, i, exact_next, now
                ) - rational_share(wall, reads, selves, paces, arrivals, i, now, before)
                currents = sum(
                    Fraction(factors[i][port]) ** 2
                    / gamma**2
                    * num
                    * (now[i] * before[j] - before[i] * now[j])
                    for port, j in enumerate(ports)
                )
                if change != currents:
                    return False, {"pair": (num, den), "Node": i, "change": change, "currents": currents}
                integer_change = rational_share(
                    wall, reads, selves, paces, arrivals, i, levels, now
                ) - rational_share(wall, reads, selves, paces, arrivals, i, now, before)
                term = -Fraction((levels[i] - before[i]) * (carried[i] - remainders[i])) / (
                    2 * paces[i] ** 2
                )
                if integer_change != currents + term:
                    return False, {
                        "pair": (num, den),
                        "Node": i,
                        "integer change": integer_change,
                        "currents + term": currents + term,
                    }
    arrivals = box_arrivals((5, 1, 1))
    wall, reads, selves, paces = read(
        arrivals, [10, 10, 9, 8, 7][:5], [[draw.randint(5, 10)] * PORTS for _ in range(5)], 2, 3, 10
    )
    # S.5's second witness: a uniform now = 3 over before = 0 at Gamma = 10, q = 5
    wall, reads, selves, paces = read(arrivals, [10] * 5, [[5] * PORTS] * 5, 2, 3, 10)
    uniform = rational_share(wall, reads, selves, paces, arrivals, 0, [3] * 5, [0] * 5)
    mean_of_paces = (
        wall * 9 / (2 * Fraction(10 * 5, 10) ** 2)
    )  # the Node term over twice the mean Link pace squared
    return uniform == 81 and mean_of_paces == 324, {"uniform witness": (uniform, mean_of_paces)}


def check_the_share_is_conserved_over_a_region() -> Check:
    """Theorem (ALGEBRA.md, The count is the record's share: the share is conserved at standing paces): over any region of Nodes whose paces stand, SUM e_i changes in one step by the weighted currents through the region's boundary Links and Rule3's remainder terms alone, exactly in rationals, the interior Links cancelling by F_ji = -F_ij and q_ji = q_ij; on a periodic board the total is constant up to the remainder terms; exact fractions on a chain of five with a region of two adjacent Nodes and on the whole board."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 6):
        arrivals = box_arrivals((5, 1, 1))
        gamma, clocks, factors = integer_witness(draw, arrivals, draw.randint(2, 9), tension=True)
        wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
        now = [draw.randint(-80, 80) for _ in range(5)]
        before = [draw.randint(-80, 80) for _ in range(5)]
        remainders = [draw.randint(0, int(wall) - 1) for _ in range(5)]
        levels, carried = step_integer(arrivals, reads, selves, wall, now, before, remainders)
        for region in ([1, 2], [0, 1, 2, 3, 4]):
            change = sum(
                rational_share(wall, reads, selves, paces, arrivals, i, levels, now)
                - rational_share(wall, reads, selves, paces, arrivals, i, now, before)
                for i in region
            )
            boundary = Fraction(0)
            for i in region:
                for port, j in enumerate(arrivals[i]):
                    if j not in region:
                        boundary += (
                            Fraction(factors[i][port]) ** 2
                            / gamma**2
                            * num
                            * (now[i] * before[j] - before[i] * now[j])
                        )
            remainder_terms = sum(
                -Fraction((levels[i] - before[i]) * (carried[i] - remainders[i])) / (2 * paces[i] ** 2)
                for i in region
            )
            if change != boundary + remainder_terms:
                return False, {
                    "pair": (num, den),
                    "region": region,
                    "change": change,
                    "boundary + remainders": boundary + remainder_terms,
                }
    return True, {"pairs": 6}


def check_the_vacuum_share() -> Check:
    """The count is the record's share: at the vacuum's paces the share is exactly 3 den (now_i^2 + before_i^2) - num now_i S_6(before)_i, S_6 the sum over the six Ports; exact integers on a periodic chain and box."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 6):
        gamma = draw.randint(2, 30)
        for arrivals in BOARDS:
            wall, reads, selves, paces = read(
                arrivals, [gamma] * len(arrivals), [[gamma] * PORTS] * len(arrivals), num, den, gamma
            )
            now = [draw.randint(-80, 80) for _ in arrivals]
            before = [draw.randint(-80, 80) for _ in arrivals]
            for i, ports in enumerate(arrivals):
                if rational_share(wall, reads, selves, paces, arrivals, i, now, before) != 3 * den * (
                    now[i] ** 2 + before[i] ** 2
                ) - num * now[i] * sum(before[j] for j in ports):
                    return False, {"pair": (num, den), "Node": i}
    return True, {"pairs": 6}


def check_the_plane_waves_current_and_form() -> Check:
    """The booking: a record of wave number k travelling from i to j has F_ij = -2 num |psi|^2 sin omega sin k for the plane record (re, im) = A (cos, sin)(k x - omega t), |psi|^2 = A^2, summed over its two lines; The velocity: for one real line F = num sin k sin omega A^2 in size and D = A^2 sin^2 omega, exact at every Node with no oscillating part; exact at rational angles, the symmetric angles forced."""
    draw = random.Random(SEED)
    for num in (1, 2, 7):
        for rotation in angles(draw, 8):
            for wave in angles(draw, 8):
                for phase in angles(draw, 8)[2:]:
                    amplitude = draw.randint(1, 50)
                    now_i, now_j = (
                        amplitude * phase.re,
                        amplitude * (phase * wave).re,
                    )  # j = i + 1 along the wave
                    before_i, before_j = (
                        amplitude * (phase * rotation).re,
                        amplitude * (phase * wave * rotation).re,
                    )
                    real_line = num * (now_i * before_j - before_i * now_j)
                    im_now_i, im_now_j = amplitude * phase.im, amplitude * (phase * wave).im
                    im_before_i, im_before_j = (
                        amplitude * (phase * rotation).im,
                        amplitude * (phase * wave * rotation).im,
                    )
                    both = real_line + num * (im_now_i * im_before_j - im_before_i * im_now_j)
                    if (
                        real_line != -num * amplitude**2 * rotation.im * wave.im
                        or both != -2 * num * amplitude**2 * rotation.im * wave.im
                    ):
                        return False, {
                            "num": num,
                            "F real line": real_line,
                            "F both lines": both,
                            "claimed": -num * amplitude**2 * rotation.im * wave.im,
                        }
                    after_i = amplitude * (phase * rotation.conj()).re
                    if now_i * now_i - after_i * before_i != amplitude**2 * rotation.im**2:
                        return False, {"D": now_i * now_i - after_i * before_i}
    return True, {"witnesses": 3 * 8 * 8 * 6}


def check_the_momentum_flux_identity_with_the_remainders() -> Check:
    """The tension (ALGEBRA.md, The primitives); the paper's Eq. (7); row 5 of The conventions and the units; S.48: with P_a(i) = (F_(i,i-a) - F_(i,i+a)) / num, positive for a record moving toward +a, Rule3's line gives at uniform coefficients w [P_a(t + 1) - P_a(t)] = SUM_b R_b [G_ab(i) - G_ab(i - b)], G_ab(i) = now_i (now_(i+a+b) - now_(i-a+b)) - now_(i+b) (now_(i+a) - now_(i-a)), and with the rounding the identity holds up to the remainders' term -[delta_i Delta_a now_i - now_i Delta_a delta_i], delta = r - r', Delta_a x_i = x_(i+a) - x_(i-a), exactly; and G_aa(i) = h_a(i) + h_a(i + a) with h_a(j) = now_(j-a) now_(j+a) - now_j^2; exact integers on a periodic 5-box at every Node and axis, anisotropic uniform Link paces included, by rule3.step."""
    draw = random.Random(SEED)
    shape = (5, 5, 5)
    nodes, arrivals = box_nodes(shape), box_arrivals(shape)
    unit = ((1, 0, 0), (0, 1, 0), (0, 0, 1))

    def at(levels, x, y, z) -> int:
        return levels[box_index(shape, x, y, z)]

    checks = 0
    for num, den in pairs(draw, 4):
        gamma = draw.randint(2, 20)
        clock = draw.randint(1, gamma)
        links = (draw.randint(1, gamma), draw.randint(1, gamma), draw.randint(1, gamma))
        wall, reads, _ = rule3.coefficients(num, den, gamma, clock, links)
        now = [draw.randint(-40, 40) for _ in nodes]
        before = [draw.randint(-40, 40) for _ in nodes]
        remainders = [draw.randint(0, wall - 1) for _ in nodes]
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
        levels, carried = [s[0] for s in stepped], [s[1] for s in stepped]
        delta = [r - r_out for r, r_out in zip(remainders, carried, strict=True)]
        for x, y, z in nodes:
            for a in range(3):
                ea = unit[a]
                plus = (x + ea[0], y + ea[1], z + ea[2])
                minus = (x - ea[0], y - ea[1], z - ea[2])
                momentum_now = (
                    at(now, x, y, z) * at(before, *minus) - at(before, x, y, z) * at(now, *minus)
                ) - (at(now, x, y, z) * at(before, *plus) - at(before, x, y, z) * at(now, *plus))
                momentum_next = (
                    at(levels, x, y, z) * at(now, *minus) - at(now, x, y, z) * at(levels, *minus)
                ) - (at(levels, x, y, z) * at(now, *plus) - at(now, x, y, z) * at(levels, *plus))
                flux = 0
                for b in range(3):
                    eb = unit[b]

                    def stress(
                        cx, cy, cz, now=now, ea=ea, eb=eb
                    ) -> int:  # G_ab at the Node (cx, cy, cz)
                        return at(now, cx, cy, cz) * (
                            at(now, cx + ea[0] + eb[0], cy + ea[1] + eb[1], cz + ea[2] + eb[2])
                            - at(now, cx - ea[0] + eb[0], cy - ea[1] + eb[1], cz - ea[2] + eb[2])
                        ) - at(now, cx + eb[0], cy + eb[1], cz + eb[2]) * (
                            at(now, cx + ea[0], cy + ea[1], cz + ea[2])
                            - at(now, cx - ea[0], cy - ea[1], cz - ea[2])
                        )

                    flux += reads[b] * (stress(x, y, z) - stress(x - eb[0], y - eb[1], z - eb[2]))
                centred_now = at(now, *plus) - at(now, *minus)
                centred_delta = at(delta, *plus) - at(delta, *minus)
                remainder_term = at(delta, x, y, z) * centred_now - at(now, x, y, z) * centred_delta
                if wall * (momentum_next - momentum_now) != flux - remainder_term:
                    return False, {
                        "pair": (num, den),
                        "Node": (x, y, z),
                        "axis": a,
                        "left": wall * (momentum_next - momentum_now),
                        "flux - remainders": flux - remainder_term,
                    }
                two_h = (at(now, *minus) * at(now, *plus) - at(now, x, y, z) ** 2) + (
                    at(now, x, y, z) * at(now, x + 2 * ea[0], y + 2 * ea[1], z + 2 * ea[2])
                    - at(now, *plus) ** 2
                )
                g_aa = at(now, x, y, z) * (
                    at(now, x + 2 * ea[0], y + 2 * ea[1], z + 2 * ea[2]) - at(now, x, y, z)
                ) - at(now, *plus) * (at(now, *plus) - at(now, *minus))
                if g_aa != two_h:
                    return False, {"G_aa is not h(i) + h(i + a) at": (x, y, z, a)}
                checks += 1
    return True, {"Node-axis checks": checks}


def check_the_plane_waves_stress() -> Check:
    """S.7, the tension of a plane wave; row 6 of The conventions and the units: for now_i = b cos(k x_i + phi) along the axis, G_aa = b^2 (cos 2k - 1) = -2 b^2 sin^2 k at every Node, so the Link's booking is -num G = 2 num b^2 sin^2 k and the Node's tension T_aa = -num h_a = num b^2 sin^2 k; for a wave with the components k_a, k_b the cross reading is G_ab = -2 b^2 sin k_a sin k_b; exact at rational angles."""
    draw = random.Random(SEED)
    for wave_a in angles(draw, 8):
        for wave_b in angles(draw, 8):
            for phase in angles(draw, 8)[1:]:
                b = draw.randint(1, 40)

                def level(
                    i: int, j: int, b=b, phase=phase, wave_a=wave_a, wave_b=wave_b
                ) -> Fraction:  # b cos(k_a i + k_b j + phi)
                    return b * (phase * wave_a**i * wave_b**j).re

                g_ab = level(0, 0) * (level(1, 1) - level(-1, 1)) - level(0, 1) * (
                    level(1, 0) - level(-1, 0)
                )
                g_aa = level(0, 0) * (level(2, 0) - level(0, 0)) - level(1, 0) * (
                    level(1, 0) - level(-1, 0)
                )
                h_a = level(-1, 0) * level(1, 0) - level(0, 0) ** 2
                if (
                    g_ab != -2 * b * b * wave_a.im * wave_b.im
                    or g_aa != -2 * b * b * wave_a.im**2
                    or h_a != -b * b * wave_a.im**2
                ):
                    return False, {"G_ab": g_ab, "G_aa": g_aa, "h_a": h_a}
    return True, {"witnesses": 8 * 8 * 7}


def two_share_forms_summed() -> tuple[bool, int]:
    """(the weighted sums agree and differ at a Node on every witness, the count of witnesses at differing paces where the unweighted sums differ), for the two checks of row 14 below."""
    draw = random.Random(SEED)
    unweighted_departures = 0
    for num, den in pairs(draw, 6):
        for arrivals in BOARDS:
            gamma, clocks, factors = integer_witness(draw, arrivals, draw.randint(2, 9), tension=True)
            wall, reads, selves, paces = read(arrivals, clocks, factors, num, den, gamma)
            count = len(arrivals)
            a = [Fraction(draw.randint(-50, 50)) for _ in range(count)]
            b = [Fraction(draw.randint(-50, 50)) for _ in range(count)]
            read_b, read_a = (
                apply_read(arrivals, reads, [Fraction(0)] * count, b),
                apply_read(arrivals, reads, [Fraction(0)] * count, a),
            )
            weighted = sum(a[i] * read_b[i] / paces[i] ** 2 for i in range(count)) == sum(
                b[i] * read_a[i] / paces[i] ** 2 for i in range(count)
            )
            if not weighted:
                return False, 0
            if sum(a[i] * read_b[i] for i in range(count)) != sum(
                b[i] * read_a[i] for i in range(count)
            ):
                unweighted_departures += 1
            at_a_node = any(a[i] * read_b[i] != b[i] * read_a[i] for i in range(count))
            if not at_a_node:
                return False, 0
            uniform_wall, uniform_reads, uniform_selves, uniform_paces = read(
                arrivals, [gamma] * count, [[gamma] * PORTS] * count, num, den, gamma
            )
            read_b, read_a = (
                apply_read(arrivals, uniform_reads, [Fraction(0)] * count, b),
                apply_read(arrivals, uniform_reads, [Fraction(0)] * count, a),
            )
            if sum(a[i] * read_b[i] for i in range(count)) != sum(
                b[i] * read_a[i] for i in range(count)
            ):
                return False, 0
    return True, unweighted_departures


def check_the_two_share_forms_summed_over_the_board() -> Check:
    """Row 14 of The conventions and the units: the share's one-sided form O - a SUM_j R_j b_j and the hole's symmetric form O + C / 2 with C = -a SUM_j R_j b_j - b SUM_j R_j a_j agree summed over the board and differ at a Node: exact with the share's weight 1 / p_i^2 inside, SUM_i a_i SUM_j R_ij b_j / p_i^2 = SUM_i b_i SUM_j R_ij a_j / p_i^2, since R_ij / p_i^2 = 2 num q_ij^2 / Gamma^2 is the same from both ends, and at uniform paces without the weight; exact fractions on three boards with tensions."""
    weighted_holds, _ = two_share_forms_summed()
    return weighted_holds, {"boards": len(BOARDS)}


def check_row_14s_unweighted_sum_as_printed() -> Check:
    """Row 14 of The conventions and the units, the equality as printed: "SUM_i a_i SUM_j R_ij b_j = SUM_i b_i SUM_j R_ij a_j by R's symmetry from both ends": R_ij = 2 num p_i^2 q_ij^2 / Gamma^2 carries the reading Node's own p_i^2 and is not symmetric where the paces differ, so the sums without the share's weight 1 / p_i^2 differ there (and agree at uniform paces); the row's equality holds with the weight inside, the share's own form; a finding on the row's wording."""
    _, departures = two_share_forms_summed()
    return departures == 0, {
        "witnesses at differing paces where the unweighted sums differ, of 18": departures
    }


def check_the_exact_lays_operator_line() -> Check:
    """The packet lay (ALGEBRA.md, The generator), the exact lay's line: with a = b e cos(k x) the now level and s = b e sin(k x) the same packet a quarter turn later, z = a + i s, and L the line's own read, (L f)_i = (S f_i + SUM over the six Ports of R f_j) / (2 w), whose eigenvalue on e^(i q x) is cos omega(q) (the line's dispersion), the record one interval earlier is z_(-1) = (L + i sqrt(1 - L^2)) z, so before = L a - sqrt(1 - L^2) s exactly, every component advanced by its own omega(q), the backward root 0; the per-component content: L e^(i q x) = cos omega(q) e^(i q x) exactly (the band), Re(b e^(i (q x + omega))) = cos omega a - sin omega s (the addition formula) at any rational angles, and the backward component beta = (e^(-i omega) - e^(-i omega(q))) / (2 i sin omega(q)) vanishes at omega = omega(q); the expansion about c = cos omega_k, before_i = (c a_i - s_k s_i) + [(L a)_i - c a_i] + (c / s_k) [(L s)_i - c s_i] + O((L - c)^2), its remainder (1 / 2) f''(c) (L - c)^2 with f = sqrt(1 - L^2), f'' = -1 / s_k^3 and L - c = -s_k v_g delta per component, -v_g^2 delta^2 / (2 s_k), checked by the residual's order 2 in delta and its coefficient; the plain lay's backward root |beta| = 0.02991 at delta = 0.05 and 0.05662 at 0.10 against the first order v_g delta / (2 sin omega) = 0.03173 and 0.06345 at the two slits' k = pi / 4."""
    draw = random.Random(SEED)
    for num, den in pairs(draw, 5):
        gamma = draw.randint(2, 20)
        wall, reads, self_coefficient = rule3.coefficients(num, den, gamma)
        for wave in angles(draw, 9):
            cosine = (
                Fraction(self_coefficient) + 2 * reads[0] * wave.re + 2 * reads[1] + 2 * reads[2]
            ) / (2 * wall)  # cos omega(q) along x
            for phase in angles(draw, 9)[2:]:
                b = draw.randint(1, 30)
                z = [b * (phase * wave**x) for x in range(-2, 3)]  # the component on a chain about x = 0
                read_at_zero = (
                    self_coefficient * z[2].re
                    + reads[0] * (z[3].re + z[1].re)
                    + 2 * reads[1] * z[2].re
                    + 2 * reads[2] * z[2].re
                ) / (2 * wall)
                if read_at_zero != cosine * z[2].re:
                    return False, {"L is not cos omega(q) on the component": (num, den)}
                for rotation in angles(draw, 7):  # Re(b e^(i (q x + omega))) = cos omega a - sin omega s
                    earlier = b * (phase * rotation).re
                    if earlier != rotation.re * z[2].re - rotation.im * z[2].im:
                        return False, {"addition formula": (num, den)}
    num, den = 1, 1
    k = math.pi / 4

    def omega(q: float) -> float:
        return math.acos((2 + math.cos(q)) / 3)

    c, s_k = math.cos(omega(k)), math.sin(omega(k))
    v_g = math.sin(k) / (3 * s_k)

    def remainder(
        delta: float,
    ) -> float:  # sqrt(1 - L^2) less its first order about c, on the component k + delta
        shift = math.cos(omega(k + delta)) - c
        return math.sin(omega(k + delta)) - (s_k - c / s_k * shift)

    held, orders = has_order(remainder, 2, step=0.08)
    coefficient = remainder(0.01) / 0.01**2
    claimed = -(v_g**2) / (2 * s_k)
    backward = []
    for delta in (0.05, 0.10):
        exact = abs(math.sin((omega(k) - omega(k + delta)) / 2)) / math.sin(
            omega(k + delta)
        )  # |beta| of the plain lay
        backward.append((round(exact, 5), round(v_g * delta / (2 * s_k), 5)))
    witness = backward == [(0.02991, 0.03173), (0.05662, 0.06345)]
    beta_at_band = abs(math.sin((omega(k) - omega(k)) / 2))
    return held and abs(coefficient / claimed - 1) < 0.02 and witness and beta_at_band == 0.0, {
        "remainder orders": orders,
        "coefficient against -v_g^2 / (2 s_k)": (coefficient, claimed),
        "plain lay's |beta| against the first order": backward,
    }


if __name__ == "__main__":
    sys.exit(run(sys.modules[__name__]))
