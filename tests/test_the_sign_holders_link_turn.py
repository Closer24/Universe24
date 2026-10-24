"""The sign's Link phase in the fold form (ALGEBRA.md, The sign holder rotates the two-part record; The constants): the Link's turn by the sign holder's odd lines is the exact tangent half-angle triple rebooked in the Link's unit with one rounding per part, X^c even and X^s odd in the Link's level, so the pair read from the two ends is exact by direction and the count is conserved by Hermiticity; the odd lines' source is the two Links' Wronskian currents summed unhalved over the doubled wall 2 E_s T. On the one universe file's families (examples/events/universe24), the electron plane reading the charge holder, on the bare 3-cube torus."""

from fractions import Fraction

import numpy as np

from event_universe import flux, node, plane, records
from event_universe.core.ports import LINK_UNIT, PORT_SIDES, Wrap
from event_universe.core.rule3 import rule_integers
from event_universe.loader.derived import held_write_of
from event_universe.loader.universe import SIGN, universe_of
from tests.laws_universe import CUBE, GAMMA, SMALL

INTEGERS, FAMILIES = universe_of(SMALL)  # the tests' small universe, den 1,021 with its two points
NAMES = [family.name for family in FAMILIES]
CHARGE = NAMES.index(SIGN)
ELECTRON = min(
    (i for i, f in enumerate(FAMILIES) if f.plane),
    key=lambda i: FAMILIES[i].pair[1] ** 2 - FAMILIES[i].pair[0] ** 2,
)  # the least leg, the lighter point
PAIR, UNIT, T = FAMILIES[ELECTRON].pair, LINK_UNIT, INTEGERS["quantum_action"]
SHAPE, TORUS = (CUBE,) * 3, Wrap(True, True, True)


def test_the_sign_pair_is_even_and_odd_in_the_links_level():
    """Over every Link level n in [-4 Gamma, 4 Gamma] at the vacuum's factor G^2: X^c(-n) = X^c(n) and X^s(-n) = -X^s(n) exactly, so the pair read from the Link's other end is the conjugate bit for bit; the pair's magnitude is X_ij = 2 num G^2 to one level, (X^c)^2 + (X^s)^2 within 2 X + 1 of X^2; X^c = X and X^s = 0 at n = 0; at n = 4 Gamma (the tangent half-angle 1, the guard's edge) the pair is (0, X), a quarter turn; and the two parts' sum never passes X sqrt 2 + 1, the bound's room (`derived.turned_room`)."""
    wall, unit = plane.link_wall(GAMMA), UNIT * UNIT
    levels = np.arange(-wall, wall + 1, dtype=object)
    (even,), (odd,) = plane.sign_pairs(PAIR, GAMMA, (unit,), (levels,))
    even, odd = np.asarray(even, dtype=object), np.asarray(odd, dtype=object)
    x = 2 * PAIR[0] * unit
    assert np.array_equal(even, even[::-1]) and np.array_equal(odd, -odd[::-1])
    assert (np.abs(even * even + odd * odd - x * x) <= 2 * x + 1).all()
    assert (even[wall], odd[wall]) == (x, 0) and (even[-1], odd[-1]) == (0, x)
    assert (even[0], odd[0]) == (0, -x) and (np.abs(even) + np.abs(odd)).max() <= x * 14143 // 10000 + 1


def test_the_wronskian_is_conserved_on_the_bare_torus_under_the_folded_link_turn():
    """The count conserved by Hermiticity (K = D M Hermitian, X^c even and X^s odd in n): the charge holder's free row with its x odd line at random levels within 3,000 per Node (inside the guard's 4 Gamma) and its time line 0, the electron plane at random levels within 5,000 stepped 200 intervals by `flux.step_family` with the Links' pairs: the summed Wronskian W = SUM Im(conj(z_now) z_before) over the torus drifts by no more than Rule3's own floor, SUM over the intervals and the Nodes of |re| + |im| (one level per part per Node per interval); and in exact rationals with the same pairs, the engine's integers, W is conserved exactly, the drift 0 over 200 intervals."""
    draw = np.random.default_rng(7)
    states = [records.empty_state(f, SHAPE, (), object) for f in FAMILIES]
    zero = np.zeros(SHAPE, dtype=object)
    odd = [draw.integers(-3000, 3001, SHAPE).astype(object), zero, zero]
    free = [records.Record(zero, zero, zero)] + [records.Record(v, v, zero) for v in odd]
    states[CHARGE].lines = free + states[CHARGE].lines[len(free) :]
    rule = rule_integers(*PAIR, GAMMA, GAMMA, GAMMA, None, UNIT)
    angles = node.turning(ELECTRON, FAMILIES, states, 1)
    assert angles is not None
    links = plane.link_levels(angles[1], TORUS, FAMILIES[CHARGE].link_read)
    pairs = plane.link_pairs(PAIR, GAMMA, 0, (UNIT * UNIT,) * 6, None, links)
    assert pairs is not None and any(np.asarray(p).any() for p in pairs[1])
    lines = [
        records.Record(*(draw.integers(-5000, 5001, SHAPE).astype(object) for _ in range(2)), zero)
        for _ in range(2)
    ]
    started, floor = int(records.wronskian(lines, True).sum()), 0
    for _ in range(200):
        states[ELECTRON].lines = lines
        floor += int((np.abs(lines[0].now) + np.abs(lines[1].now)).sum())
        lines = flux.step_family(ELECTRON, FAMILIES, states, rule, TORUS, GAMMA, pairs=pairs)[0]
    drift = int(records.wronskian(lines, True).sum()) - started
    assert started != 0 and abs(drift) <= floor, (drift, floor)
    print(
        f"the torus of {CUBE}^3: W {started}, the drift over 200 intervals {drift} within the floor {floor}"
    )
    reads, self_coefficient, wall, _mass = rule
    even = [np.asarray(p, dtype=object).reshape(-1) for p in pairs[0]]
    odd_part = [np.asarray(p, dtype=object).reshape(-1) for p in pairs[1]]
    index = np.arange(CUBE**3).reshape(SHAPE)
    neighbours = [np.roll(index, -side, axis).reshape(-1) for axis, side in PORT_SIDES]
    z = [(Fraction(int(a)), Fraction(int(b))) for a, b in draw.integers(-5000, 5001, (CUBE**3, 2))]
    z_before = [
        (Fraction(int(a)), Fraction(int(b))) for a, b in draw.integers(-5000, 5001, (CUBE**3, 2))
    ]

    def wronskian(now, before):  # type: ignore[no-untyped-def]
        return sum(a[0] * b[1] - a[1] * b[0] for a, b in zip(now, before, strict=True))

    first = wronskian(z, z_before)
    for _ in range(200):
        following = []
        for i in range(CUBE**3):
            re = self_coefficient * z[i][0] - wall * z_before[i][0]
            im = self_coefficient * z[i][1] - wall * z_before[i][1]
            for port in range(len(PORT_SIDES)):
                j, c, s_ = int(neighbours[port][i]), int(even[port][i]), int(odd_part[port][i])
                re += c * z[j][0] - s_ * z[j][1]
                im += s_ * z[j][0] + c * z[j][1]
            following.append((re / wall, im / wall))
        z, z_before = following, z
    assert wronskian(z, z_before) == first != 0


def test_the_sign_holders_lines_stand_at_the_doubled_wall():
    """Every line of the sign holder's one write at one wall, 2 E_s T times the readers' charge multiple (The constants: the count units brought to one wall), a multiple of 2 E_s T; and the odd lines' unhalved sum J over the doubled wall against the halved path (J + 1) div 2 over E_s T, both by the carried division from the half wall: 2 (L_old W + r_old) - (L_new 2 W + r_new) = k_w x (the number of odd J so far) exactly at every interval, so the two are bit-identical, L_new = L_old and r_new = 2 r_old, while every J is even, and differ by the dropped half units otherwise; on random J within 10^6 over 300 intervals."""
    write = held_write_of(FAMILIES, CHARGE, T, UNIT)
    weight, wall = FAMILIES[CHARGE].write, write.walls[0] // 2
    assert FAMILIES[CHARGE].level_weight is not None
    assert len(set(write.walls)) == 1 and wall % (FAMILIES[CHARGE].level_weight * T) == 0
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
