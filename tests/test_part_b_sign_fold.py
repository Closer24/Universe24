"""Part B, the sign's Link phase in the fold form (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record; the two hands' lines of 2026-10-09, the advisor's (a), (c) and (1), the mathematician's (a) and (L2)): the Link's turn by the sign holder's odd lines is the exact tangent half-angle triple rebooked in the Link's unit with one rounding per part, X^c even and X^s odd in the Link's level n, so that the pair read from the two ends is exact by direction and the count is conserved by Hermiticity; the odd lines' source is the two Links' Wronskian currents summed unhalved over the doubled wall; the time turn stays the one shear. Every test under 30 seconds."""

from fractions import Fraction

import numpy as np

from event_universe import flux, node, records
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import rule_integers
from event_universe.loader.derived import held_write_of
from event_universe.plane import link_levels, link_pairs, link_wall, sign_pairs
from tests.laws import CHARGE, TURNING
from tests.laws import TURNING_T as T

GAMMA, PAIR, UNIT = 6000, (4000, 6000), 16
NAMES = [family.name for family in TURNING]
CHARGED = NAMES.index("charged")


def test_the_sign_pair_is_even_and_odd_in_the_links_level():
    """(a) Over every Link level n in [-4 Gamma, 4 Gamma] at the vacuum's factor G^2: X^c(-n) = X^c(n) and X^s(-n) = -X^s(n) exactly, so the pair read from the Link's other end is the conjugate bit for bit; the pair's magnitude is X_ij = 2 num G^2 to one level, (X^c)^2 + (X^s)^2 within 2 X + 1 of X^2; X^c = X and X^s = 0 at n = 0; at n = 4 Gamma (the tangent half-angle 1, the guard's edge) the pair is (0, X), a quarter turn; and the two parts' sum never passes X sqrt 2 + 1, the bound's room (`derived.turned_room`)."""
    wall, unit = link_wall(GAMMA), UNIT * UNIT
    levels = np.arange(-wall, wall + 1, dtype=object)
    (even,), (odd,) = sign_pairs(PAIR, GAMMA, (unit,), (levels,))
    even, odd = np.asarray(even, dtype=object), np.asarray(odd, dtype=object)
    x = 2 * PAIR[0] * unit
    assert np.array_equal(even, even[::-1]) and np.array_equal(odd, -odd[::-1])
    assert (np.abs(even * even + odd * odd - x * x) <= 2 * x + 1).all()
    assert (even[wall], odd[wall]) == (x, 0) and (even[-1], odd[-1]) == (0, x)
    assert (even[0], odd[0]) == (0, -x) and (np.abs(even) + np.abs(odd)).max() <= x * 14143 // 10000 + 1


def test_the_wronskian_is_conserved_on_a_periodic_ring_under_the_folded_link_turn():
    """(the count, Theorem 3) On a ring of 64 in the vacuum's rule of the matter pair with the sign holder's x odd line at random levels within 3,000 per Node (|n| <= 6,000, inside the guard's 4 Gamma) and the time level 0, a random plane record within 5,000 stepped 200 intervals by `flux.step_family` with the Links' pairs: the summed Wronskian W = SUM Im(conj(z_now) z_before) over the ring drifts by no more than Rule3's own floor, SUM over the intervals and the Nodes of |re| + |im| (one level per part per Node per interval); and in exact rationals on a ring of 9, the same pairs (the engine's integers) with the division exact, W is conserved exactly, the drift 0 over 200 intervals (K = D M Hermitian: X^c even and X^s odd in n)."""
    ring, draw = Wrap(True, True, True), np.random.default_rng(7)
    states = [records.empty_state(f, (64, 1, 1), (), np.int64) for f in TURNING]
    zero = np.zeros((64, 1, 1), dtype=np.int64)
    odd = [draw.integers(-3000, 3001, (64, 1, 1)), zero, zero]
    states[CHARGE].lines = [records.Record(zero, zero, zero)] + [records.Record(v, v, zero) for v in odd]
    lines = [records.Record(*draw.integers(-5000, 5001, (3, 64, 1, 1))) for _ in range(2)]
    lines = [records.Record(r.now, r.before, np.abs(r.remainder)) for r in lines]
    rule = rule_integers(*PAIR, GAMMA, GAMMA, GAMMA)
    angles = node.turning(CHARGED, TURNING, states, 1)
    assert angles is not None
    pairs = link_pairs(PAIR, GAMMA, 0, (1,) * 6, None, link_levels(angles[1], ring, (-1, -1)))
    assert pairs is not None and any(np.asarray(p).any() for p in pairs[1])
    started = int(records.wronskian(lines, True).sum(dtype=object))
    floor = 0
    for _ in range(200):
        states[CHARGED].lines = lines
        floor += int((np.abs(lines[0].now) + np.abs(lines[1].now)).sum(dtype=object))
        lines = flux.step_family(CHARGED, TURNING, states, rule, ring, GAMMA, pairs=pairs)[0]
    drift = int(records.wronskian(lines, True).sum(dtype=object)) - started
    assert started != 0 and abs(drift) <= floor, (drift, floor)
    print(f"the ring of 64: W {started}, the drift over 200 intervals {drift} within the floor {floor}")
    n = 9  # the rational mirror: the same step in Fractions, the pairs the engine's integers
    levels = draw.integers(-3000, 3001, n)
    links = link_levels((levels.reshape(n, 1, 1), zero[:n], zero[:n]), ring, (-1, -1))
    even, odd_part = link_pairs(PAIR, GAMMA, 0, (1,) * 6, None, links)  # type: ignore[misc]
    even = [np.asarray(p, dtype=object).ravel() for p in even]
    odd_part = [np.asarray(p, dtype=object).ravel() for p in odd_part]
    reads, self_coefficient, wall, _mass = rule
    z = [complex(*draw.integers(-5000, 5001, 2)) for _ in range(n)]
    z = [(Fraction(int(v.real)), Fraction(int(v.imag))) for v in z]
    z_before = [(Fraction(int(a)), Fraction(int(b))) for a, b in draw.integers(-5000, 5001, (n, 2))]

    def wronskian(now, before):  # type: ignore[no-untyped-def]
        return sum(a[0] * b[1] - a[1] * b[0] for a, b in zip(now, before, strict=True))

    first = wronskian(z, z_before)
    for _ in range(200):
        following = []
        for i in range(n):
            re = self_coefficient * z[i][0] - wall * z_before[i][0]
            im = self_coefficient * z[i][1] - wall * z_before[i][1]
            for port, j in enumerate(((i + 1) % n, (i - 1) % n, i, i, i, i)):
                c, s_ = int(even[port][i]), int(odd_part[port][i])
                re += c * z[j][0] - s_ * z[j][1]
                im += s_ * z[j][0] + c * z[j][1]
            following.append((re / wall, im / wall))
        z, z_before = following, z
    assert wronskian(z, z_before) == first != 0


def test_the_halving_dropped_the_odd_line_over_the_doubled_wall():
    """(d) The sign holder's odd lines over the doubled wall 2 E_s T from the unhalved sum J against the halved path, (J + 1) div 2 over E_s T, both by the carried division from the half wall: with 2 (L_old W + r_old) - (L_new 2 W + r_new) = k_w x (the number of odd J so far) exactly at every interval (the half unit of current the halved path rounds up and the unhalved keeps in the remainder), so that the two are bit-identical, L_new = L_old and r_new = 2 r_old, while every J is even, and differ by the dropped half units otherwise; on random J within 10^6 over 300 intervals and on a plane wave's own current, J_x = 2 A^2 sin k, static; the walls of turning.json's sign holder (100 T, 200 T, 200 T, 200 T) per row."""
    write = held_write_of(TURNING, CHARGE, T)
    weight, wall = (
        TURNING[CHARGE].write,
        write.walls[0] // 2,
    )  # E_s T, the halved path's wall of this model
    assert (
        write.walls == (2 * wall,) * 4 * 2 and wall == 100 * T
    )  # every line of the sign holder over the doubled wall 2 E_s T: the odd lines since the halving was dropped, the time line since the Wronskian is booked centred on the triple, the two edges' sum (the centred count, 2026-10-23; the former time line's wall E_s T)
    draw = np.random.default_rng(11)
    for sources in (draw.integers(-(10**6), 10**6, 300), 2 * draw.integers(-(10**6), 10**6, 300)):
        old, new, odds = (0, wall // 2), (0, wall), 0
        for current in sources.tolist():
            gained, r_old = divmod(old[1] + weight * ((current + 1) // 2), wall)  # the halved path
            level_old = old[0] + gained
            gained, r_new = divmod(new[1] + weight * current, 2 * wall)  # the unhalved sum, doubled wall
            level_new = new[0] + gained
            old, new, odds = (level_old, r_old), (level_new, r_new), odds + current % 2
            assert 2 * (level_old * wall + r_old) - (level_new * 2 * wall + r_new) == weight * odds
        if not (sources % 2).any():
            assert new == (old[0], 2 * old[1])
