"""Hostile physicist, check E: does the hand's energy drain into the clock's rate as the beat's adiabatic invariant
demands (t13 section 3, probe 2: 'its energy drains into the clock's rate, as the beat's adiabatic invariant E / omega
demands')? E / omega with omega^2 = g / W means E^2 W is kept while W moves slowly.

Clock: one hand on its spring winding its own 00 slot, as in t13 probe 2, at two scales: the probe's (W = 3000,
stride 10, amplitude 38 notches) and a large one (W = 3 x 10^6, stride 530, amplitude 2000 notches) where the
drift's floor is a part in 2000 of the swing instead of a part in 40.
Algebra: whole numbers; the one-site replica of the first-order form (checked against tick_first in check A); the
invariant read as (2E)^2 W against its start, 2E = p+^2 / W + g a a+.
Board: one Node-clock.
Clicks: n/a; this reads the board's own books, which the texts quote.

Run: <t24b>/.venv/bin/python -I e_adiabatic.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "copy" / "n2_second"))

from n2b_lib import carry  # noqa: E402


def tick1(x, rest, g, td):
    a5, p5, c00, p00, rd00 = x
    w = rest + c00
    sb, _ = carry(p5, w, 0)
    pa = p5 - g * a5
    sa, _ = carry(pa, w, 0)
    j00 = -2 * g * a5 * a5 + 2 * w * (sb * sb + sa * sa)
    q00, rd00n = carry(j00, td, rd00)
    p00n = p00 + q00
    a5n = a5 + carry(pa, w, 0)[0]
    c00n = c00 + carry(p00n, rest, 0)[0]
    return (a5n, pa, c00n, p00n, rd00n), j00, w


def permille(num, den):
    q, _ = carry(1000 * num, den, 0)
    return int(q)


def course(rest, g, td, stride0, rounds, step):
    x = (0, stride0 * rest, 0, 0, 0)
    e0 = carry((stride0 * rest) ** 2, rest, 0)[0]  # 2E at the start
    inv0 = e0 * e0 * rest
    print(f"  W = {rest}, g = {g} (omega^2 = g / W = {permille(g, rest)} permille), T_d = {td}, stride {stride0} (amplitude about {stride0 * 1000 // 265} notches)")
    print("  round | W | W / W0 permille | 2E = p+^2 / W + g a a+ | (2E)^2 W against the start, permille (1000 if adiabatic) | <J00> / <2E> over the last window, permille | the hand's largest |stride| in the window")
    sj = se = 0
    smax = 0
    for t in range(rounds + 1):
        if t % step == 0:
            a5, p5, c00 = x[0], x[1], x[2]
            w = rest + c00
            two_e = carry(p5 * p5 + g * w * prev_a * a5, w, 0)[0] if t else e0
            print(f"  {t:5d} | {w:9d} | {permille(w, rest):6d} | {two_e:12d} | {permille(two_e * two_e * w, inv0):6d} | {permille(sj, se) if se else 'n/a':>6} | {smax}")
            sj = se = 0
            smax = 0
        if t < rounds:
            prev_a = x[0]
            x, j00, w = tick1(x, rest, g, td)
            sj += j00
            se += carry(x[1] * x[1] + g * w * prev_a * x[0], w, 0)[0]
            smax = max(smax, abs(x[0] - prev_a))


print("== E1. the probe's scale (t13 probe 2 as shipped)")
course(3000, 210, 1000, 10, 3000, 500)
print("\n== E2. the large scale: the same omega^2, the floor a part in 2000 of the swing, T_d scaled so W moves at a like pace")
course(3 * 10**6, 210 * 10**3, 10**4, 530, 3000, 500)
print("\n== E3. the large scale, a slower wind (T_d ten times larger), to see the invariant where W moves slowly")
course(3 * 10**6, 210 * 10**3, 10**5, 530, 6000, 1000)
print("  reading: where the floor is small the invariant holds and the energy drains; at the probe's scale it does not: the hand's energy is held up by the drift's rounding, and what winds W is not the swing's energy")
