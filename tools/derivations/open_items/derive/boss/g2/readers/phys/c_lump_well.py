"""Hostile physicist, check C: term 13's probe 3 (a lump on 3 x 3 x 16) re-read: is 'the well settles' a well?

Clock: one hand kicked at one Node-clock, term 5 in energy units, T_d = 1000, the 00 wave carrying the push.
Algebra: whole numbers; n2b_lib's first-order tick and metric_source on the real act; a Jacobi relaxation in scaled
integers for the static Poisson well the measured source would dig.
Board: 3 x 3 x 16 as in t13_probe.py section 3.
Clicks: a Newtonian well is a bump of the 00 slot at the lump against the far sites, of the lattice Green's
function's shape; this check reads (i) how big that bump can be for the source actually pushed, (ii) whether the
lump stays a lump (the hand's energy near the centre against the whole board), (iii) the site-to-site spread of c00
away from the lump against the quoted 'well'.

Run: <t24b>/.venv/bin/python -I c_lump_well.py
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
    metric_source,
    spring,
    step,
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
SH = (3, 3, 16)
Lb = layout(SH, REST, REST, GRIP, 1, TD, clock="others")
N = Lb.nb.shape[1]
centre = (1 * 3 + 1) * 16 + 8
far = (1 * 3 + 1) * 16 + 0
xyz = np.indices(SH).reshape(3, -1)
dz = np.minimum((xyz[2] - 8) % 16, (8 - xyz[2]) % 16)
near = dz <= 1  # the lump's own z slab and its two neighbours, all 9 sites of each


def permille(num, den):
    q, _ = carry(1000 * num, den, 0)
    return int(q)


print("== C1. the static Poisson well a source S (p00 counts a round at one site, its mean removed) digs on this torus: grip Lap c = -(S delta - S / N)")
print("  Jacobi relaxation in integers scaled by 10^6, 6000 sweeps")
SCALE = 10**6
nb = Lb.nb
for S in (300, 3000, 300000):
    src = np.full(N, -S * SCALE, dtype=object)  # -S/N scaled by N: multiply the equation by N to stay whole
    src = src + 0
    src[centre] += S * SCALE * N
    # equation times N: grip (sum_nb c - 6 c) N = -(S N delta - S) SCALE ... keep c scaled by SCALE * N * grip
    c = np.zeros(N, dtype=object)
    for _ in range(6000):
        c = (c[nb].sum(axis=0) + src) // 6  # c in units of 1 / (6 grip ... ) see below
    # c solves (sum_nb c - 6 c) = -src, i.e. grip Lap (c / (grip N SCALE)) = -(S delta - S / N)
    well = int(c[centre] - c[far])
    q, _ = carry(well * 1000, GRIP * N * SCALE, 0)
    print(f"  S = {S:6d} a round: well (centre less far) = {int(q)} / 1000 of a notch of c00")
print("  reading: t13's lump pushes about 300 a round through T_d = 1000 (measured below), so its static well is well under one notch: nothing a whole count can show")

print("\n== C2. probe 3's run: the quoted well against the spread of c00 away from the lump, the push's total, and where the hand's energy is")
a = np.zeros((ROWS, N), dtype=object)
s_ = to_first(Lb, State(a, a.copy(), 0 * a, 0 * a))
s_.b[CLOCK, centre] = 10 * REST
st = s_
print("  round | lump - far | c00 spread off the lump (max - min) | board mean c00 | sum J00 / T_d this round (all sites) | at the lump | share of sum p^2 (the hand's) within dz <= 1 permille | xx at lump | xx far | the hand's 2E on the board: sum p^2 / W + sum g a^2 + sum grip (delta a)^2 | sum p (kept)")
plus = Lb.nb[[0, 2, 4]]  # the + neighbour on each axis: each Mesh once
for t in range(1501):
    if t in (0, 10, 25, 50, 100, 200, 400, 800, 1200, 1500):
        c = st.a[S00]
        off = np.array([int(v) for i, v in enumerate(c) if i != centre], dtype=object)
        j = metric_source(Lb, st, NOW, RATE, first=True)
        tot, _ = carry(int(j[S00].sum()), TD, 0)
        here, _ = carry(int(j[S00][centre]), TD, 0)
        p2 = st.b[CLOCK] * st.b[CLOCK]
        share = permille(int(p2[near].sum()), int(p2.sum())) if int(p2.sum()) else 0
        mean, _ = carry(int(c.sum()), N, 0)
        w = REST + c
        kin = sum(int(carry(int(p2[i]), int(w[i]), 0)[0]) for i in range(N))
        pot = int((G * st.a[CLOCK] * st.a[CLOCK]).sum())
        da = st.a[CLOCK][plus] - st.a[CLOCK][None, :]
        mesh = int((GRIP * da * da).sum())
        print(f"  {t:5d} | {int(c[centre] - c[far]):6d} | {int(off.max() - off.min()):6d} | {int(mean):7d} | {int(tot):8d} | {int(here):6d} | {share:4d} | {int(st.a[SII[0], centre]):5d} | {int(st.a[SII[0], far]):5d} | {kin + pot + mesh:12d} = {kin} + {pot} + {mesh} | {int(st.b[CLOCK].sum())}")
    if t < 1500:
        st = tick_first(Lb, st, NOW, RATE)
print("  reading: the hand's energy leaves the centre in tens of rounds (nothing binds it in space: the spring is a potential in a, the Mesh spreads a as a massive wave), the quoted 'well' is of the size of the site-to-site spread of the 00 wave, the hand's energy on the board grows (the drift a+ = a + floor(p / W) moves a count a whole notch wherever p < 0, however small), and the total push is that grown energy, not the lump's")
