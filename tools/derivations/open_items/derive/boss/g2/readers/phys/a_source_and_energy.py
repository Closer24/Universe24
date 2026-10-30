"""Hostile physicist, check A: term 13's probe 2 (the uniform swing on one Node-clock, term 5 in energy units,
T_d = 1000) re-read in whole numbers.

Clock: the clock's hand swings on its spring while its own 00 slot is wound by the hand's strides.
Algebra: an integer replica of n2b_lib.tick_first on one site, checked bit for bit against it; then the 00 source
actually pushed each round (J00 = 2 W (sigma_b^2 + sigma_a^2) - 2 g a^2 with sigma = p div W) against the act's own
energy 2E = p+^2 / W + g a a+ (the leapfrog's exact invariant), window by window; the floor's share of the source
(J00 less the same source with (2 (p_b^2 + p_a^2)) div W in place of 2 W sigma^2); the ii slot's sign and the
light-against-clock ratio grip / rest; the 00 gear's energy against the matter's.
Board: one Node-clock, as in t13_probe.py section 2.
Clicks: the texts read the 00 source as the swing's energy and W's growth as that energy draining into the clock's
rate; this check asks whether the pushed source is the energy at the strides the probe runs at (0 to 2).

Run: <t24b>/.venv/bin/python -I a_source_and_energy.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "copy" / "n2_second"))

import numpy as np  # noqa: E402
from n2b_lib import (  # noqa: E402
    A1ROWS,
    FAMILIES,
    ROWS,
    S0I,
    S00,
    SII,
    SJK,
    State,
    carry,
    join,
    layout,
    spring,
    table,
    terms,
    tick_first,
    to_first,
)

REST, GRIP, G, TD = 3000, 500, 210, 1000
CLOCK = A1ROWS[0]
UNIT = 7 * ROWS


def at(plane, row):
    return plane * ROWS + row


def pairs_(c, rows):
    return [(rows[i], rows[j], int(c[i, j])) for i in range(len(rows)) for j in range(len(rows)) if c[i, j]]


def energy_source(families=FAMILIES):
    """Verbatim from t13_probe.py: term 5 in the act's energy units, twice over."""
    now, rate = [], []
    for rows, c in families:
        for x, y, cxy in pairs_(c, rows):
            now.append((at(0, x), at(0, y), UNIT, -2 * G * cxy, S00))
            now += [(at(0, x), at(0, y), UNIT, 2 * G * cxy, s) for s in SII]
            for i in range(3):
                now.append((at(1 + i, x), at(1 + i, y), UNIT, GRIP * cxy, SII[i]))
            for k in range(3):
                i, j = (k + 1) % 3, (k + 2) % 3
                now.append((at(1 + i, x), at(1 + j, y), UNIT, GRIP * cxy, SJK[k]))
            for plane in (5, 6):
                rate.append((at(plane, x), at(plane, y), at(0, S00), 2 * cxy, S00))
                rate.append((at(plane, x), at(plane, y), UNIT, 2 * REST * cxy, S00))
                for i in range(3):
                    rate.append((at(plane, x), at(1 + i, y), at(0, S00), cxy, S0I[i]))
                    rate.append((at(plane, x), at(1 + i, y), UNIT, REST * cxy, S0I[i]))
    return terms(now), terms(rate)


T5, RATE = energy_source()
SPRING = terms(spring(G, [(A1ROWS, table("A1"))]))
NOW = join(SPRING, T5)
L1 = layout((1, 1, 1), REST, REST, GRIP, 1, TD, clock="others")


def start(p5):
    a = np.zeros((ROWS, 1), dtype=object)
    s = to_first(L1, State(a, a.copy(), 0 * a, 0 * a))
    s.b[CLOCK, 0] = p5
    return s


def tick1(x, exact=False):
    """One round of the first-order form on one site, Python integers: (a5, p5, c00, p00, rd00, ii, pii, rdii).
    exact=True sources the 00 slot by (2 (p_b^2 + p_a^2)) div W in place of 2 W (sigma_b^2 + sigma_a^2)."""
    a5, p5, c00, p00, rd00, ii, pii, rdii = x
    w = REST + c00
    sb, _ = carry(p5, w, 0)
    q5 = -G * a5  # the spring through the matter's drive at T_d = 1
    pa = p5 + q5
    sa, _ = carry(pa, w, 0)
    floor_part = 2 * w * (sb * sb + sa * sa)
    exact_part, _ = carry(2 * (p5 * p5 + pa * pa), w, 0)
    j00 = -2 * G * a5 * a5 + (exact_part if exact else floor_part)
    jii = 2 * G * a5 * a5
    q00, rd00n = carry(j00, TD, rd00)
    qii, rdiin = carry(jii, TD, rdii)
    p5n, p00n, piin = pa, p00 + q00, pii + qii
    a5n = a5 + carry(p5n, w, 0)[0]
    c00n = c00 + carry(p00n, REST, 0)[0]
    iin = ii + carry(piin, w, 0)[0]
    return (a5n, p5n, c00n, p00n, rd00n, iin, piin, rdiin), (j00, floor_part - exact_part, sb, sa, w)


def permille(num, den):
    q, _ = carry(1000 * num, den, 0)
    return int(q)


print("== A0. the harness: the integer replica against n2b_lib.tick_first (probe 2's lay, p = 10 rest), 3000 rounds")
s = start(10 * REST)
x = (0, 10 * REST, 0, 0, 0, 0, 0, 0)
agree = True
for _ in range(3000):
    s = tick_first(L1, s, NOW, RATE)
    x, _ = tick1(x)
    got = (int(s.a[CLOCK, 0]), int(s.b[CLOCK, 0]), int(s.a[S00, 0]), int(s.b[S00, 0]), int(s.rd[S00, 0]), int(s.a[SII[0], 0]), int(s.b[SII[0], 0]), int(s.rd[SII[0], 0]))
    agree &= got == x
print(f"  replica == tick_first on (a, p, c00, p00, r_d00, xx, p_xx, r_dxx) at every round: {agree}")

print("\n== A1. probe 2's run: the 00 source pushed each round against the act's energy 2E = p+^2 / W + g a a+, by windows of 500 rounds")
print("  window | <J00> (as pushed) | <2E_p> | <2E_sigma> = <W sigma_a^2 + g a a+> | <J00> / <2E_p> permille | floor's share of <J00> permille | rounds with sigma_a != 0 | W at end | xx at end | grip / rest permille")
x = (0, 10 * REST, 0, 0, 0, 0, 0, 0)
E0 = carry((10 * REST) ** 2, REST, 0)[0]  # 2E at the start: p^2 / W, the hand at the origin
for win in range(6):
    sj = s2p = s2s = sbias = moving = 0
    for _ in range(500):
        a5, p5 = x[0], x[1]
        x, (j00, bias, sb, sa, w) = tick1(x)
        a5n, p5n = x[0], x[1]
        sj += j00
        s2p += carry(p5n * p5n + G * w * a5 * a5n, w, 0)[0]
        s2s += w * (a5n - a5) ** 2 + G * a5 * a5n
        sbias += bias
        moving += 1 if sa != 0 else 0
    W = REST + x[2]
    grip = GRIP + 2 * x[5]
    print(f"  {win * 500:5d}-{win * 500 + 500:4d} | {carry(sj, 500, 0)[0]:9d} | {carry(s2p, 500, 0)[0]:8d} | {carry(s2s, 500, 0)[0]:8d} | {permille(sj, s2p) if s2p else 'n/a':>6} | {permille(sbias, sj):5d} | {moving:3d} | {W:7d} | {x[5]:6d} | {permille(grip, REST):5d}")
print(f"  2E at the start (p^2 / W, a = 0): {E0}; the 00 gear's p00 at round 3000: {x[3]}, its energy p00^2 / (2 rest) = {carry(x[3] * x[3], 2 * REST, 0)[0]} against the matter's E at the start {carry(E0, 2, 0)[0]}: ratio {permille(carry(x[3] * x[3], 2 * REST, 0)[0], carry(E0, 2, 0)[0])} permille")
print("  reading: the text's 'its mean over a swing is E' is P3's at stride 26,458; here the strides are 0 to 2 from round ~500 and <J00> is read against the act's own 2E")

print("\n== A2. the same lay with the 00 slot sourced by the act's p^2 / W (one carry) in place of W sigma^2: W over the rounds")
xf = (0, 10 * REST, 0, 0, 0, 0, 0, 0)
xe = (0, 10 * REST, 0, 0, 0, 0, 0, 0)
for t in range(3001):
    if t % 500 == 0:
        print(f"  round {t:5d}: W (floor source, the text's) = {REST + xf[2]:7d}; W (exact p^2 / W source) = {REST + xe[2]:7d}; the hand's p: {xf[1]:8d} / {xe[1]:8d}")
    if t < 3000:
        xf, _ = tick1(xf)
        xe, _ = tick1(xe, exact=True)

print("\n== A3. the ii slot under the written push (uniform swing: the gradient part is 0, the potential part +2V): sign and the clicks' light-against-clock ratio")
x = (0, 10 * REST, 0, 0, 0, 0, 0, 0)
for t in range(3001):
    if t % 500 == 0:
        c00, ii = x[2], x[5]
        grip = GRIP + 2 * ii
        W = REST + c00
        print(f"  round {t:5d}: c00 = {c00:7d}, each ii slot = {ii:7d} (the chosen -c00 / 12 would be {-carry(c00, 12, 0)[0]:7d}), grip = {grip:6d}; c^2 = grip / W = {permille(grip, W):5d} permille (1/6 = 167 at rest); c^2 / N^2 = grip / rest = {permille(grip, REST):5d} permille (167 at rest): light's Mesh in beats^2 = rest / grip = {permille(REST, grip):5d} permille (6000 at rest)")
    if t < 3000:
        x, _ = tick1(x)
print("  reading: the written push raises the grips where the matter is (gamma < 0 by P2's own reading, ii = +c00/12 -> gamma = -1), and in the clicks (lengths from light, time from the clock) the Mesh shortens: a contraction, light racing the clocks")

print("\n== A4. two hands a continuum reading cannot tell apart: p = -1 and p = +1 at a = 0 (|p| / W = 1 / 3000 of a notch per round), with the spring, 3000 rounds")
for p0 in (-1, 1):
    x = (0, p0, 0, 0, 0, 0, 0, 0)
    lo = hi = 0
    marks = []
    for t in range(3001):
        if t % 1000 == 0:
            marks.append((t, REST + x[2]))
        if t < 3000:
            x, _ = tick1(x)
            lo, hi = min(lo, x[0]), max(hi, x[0])
    print(f"  p = {p0:+d}: W at rounds 0, 1000, 2000, 3000: {[w for _, w in marks]}; the hand's count ranged over [{lo}, {hi}]")
print("  reading: the stride is floor(p / W), so p = -1 is a hand moving one notch down each round until the spring returns it: a one-notch relaxation swing whose source is 2W per moving round whatever its p-energy; p = +1 stands")
