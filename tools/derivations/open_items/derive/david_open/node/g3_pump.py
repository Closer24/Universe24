"""G3's ninth text: the held rows Mesh-less against the size's pump (the eighth physicist's r1, case (A)), and the
angle's drift on the act.

On the act the night builds (node-live 939fa65a7, engine/step.tick), the law on two held rows, V = hat (|k|^2 - n)^2
laid as its three monomials (hat 1, n = R^2 with R = 5^5, W = 2,000 n). The hat's push on the angle row,
-4 hat (|k|^2 - n) k_1, beats with the size: with Meshes (grip W/6) a size off its rest pumps the angle's waves whose
beat is near a quarter of its own, half its frequency (the physicist's r1, Mathieu's primary resonance). With the held
rows Mesh-less (grip 0), as the frame lays them, the angle has no wave to fall into.

(A') a ring of 256, every Node-clock laid still at (R + 312, 0), the size off its rest by a tenth of R, the angle
     seeded k_1 = 100 at one Node-clock, and at every Node-clock; per 250 rounds over 3,000, the largest |k_1| over the
     ring and the size's swing at Node-clock 128 (its most less its least of |k|^2 - n over the window, in ppm of n).
(B') Mesh-less, each Node-clock its own hand: Node-clock i laid still at (R + d_i, 100), d_i from -3,000 (g3_hat's
     near-top lay) to 1,875, past the top where (R + d)^2 = 2 n, near 1,294; per 1,000 rounds over 6,000 the largest
     |k_1|, the range of |k|^2 - n, and the largest turn |k_0 b_1 - k_1 b_0|, now against before, 0 at the lay. The
     hat's push is along k, so in the continuum the turn is kept and a still lay's angle stays in proportion to its
     size; on the act the edge rounds the counts the hat reads.

Whole numbers only: every division Rule3's carry; no float, root, logarithm, exponential, circular function or search.
Usage: python3 -I g3_pump.py <src of node-live at 939fa65a7>
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import pushes  # noqa: E402
from tensor24.engine.state import Click, Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402

KEY = 5**5
N = KEY * KEY
W = 2000 * N
GH = carry(W, 6, 0)[0]
GRIPS = GH
UNIT = -1
SCALE = 10**40
MODE = (2, 1, -1, -2, -1, 1)
NONE_I = np.zeros(0, dtype=np.intp)
NONE_O = np.zeros(0, dtype=object)
UNREAD = Read(NONE_I, NONE_O, NONE_I)
NOPLAN = Plan(NONE_I, NONE_I, NONE_I, NONE_O, NONE_I)


def hat_terms(rows, hat, n):
    terms = []
    for i, a in enumerate(rows):
        terms.append((hat, (a, a, a, a)))
        for b in rows[i + 1:]:
            terms.append((2 * hat, (a, a, b, b)))
        terms.append((-2 * hat * n, (a, a, UNIT, UNIT)))
    return terms


def plan_of(terms):
    factor = np.array([f for f, _ in terms], dtype=object)
    legs = tuple(np.array([leg[i] for _, leg in terms], dtype=np.intp) for i in range(4))
    return pushes(factor, legs)


def layout(shape, grips, terms, teeth=W):
    nb = board(shape)
    sites = nb.shape[1]
    spokes, meshes = geometry(nb, 3)
    rows = len(grips)
    grip = np.zeros((rows, 3 * sites), dtype=object)
    for row, g in enumerate(grips):
        grip[row, :] = g
    ones = np.ones((rows, 1), dtype=object)
    gearing = Gearing(teeth * ones, ones, ones.copy(), ones.copy(), ones.copy())
    click = Click(NONE_I, NONE_I, NONE_O, NONE_I, np.ones((1, 1), dtype=object))
    parts = [nb, spokes, meshes, grip, gearing, plan_of(terms), UNREAD, UNREAD, click, NOPLAN]
    parts += [NOPLAN] * (len(Layout._fields) - len(parts))
    return Layout(*parts), sites


def still(a):
    rows, sites = a.shape
    zero = np.zeros((rows, sites), dtype=object)
    return State(a.copy(), a.copy(), zero.copy(), zero.copy(), np.zeros((1, sites), dtype=object))


def flips(values):
    count, last = 0, 0
    for v in values:
        sign = (v > 0) - (v < 0)
        if sign and last and sign != last:
            count += 1
        if sign:
            last = sign
    return count


def ring_flips(values):
    size = len(values)
    return sum(int(values[i] * values[carry(i + 1, size, 0)[1]] < 0) for i in range(size))


def ppm(part, whole):
    return carry(1000000 * part, whole, 0)[0]


def case_a(size_off, seed, sites_n=256, rounds=3000, window=250, probe_site=128):
    lay, sites = layout((sites_n, 1, 1), [GRIPS, GRIPS], hat_terms((0, 1), 1, N))
    a = np.zeros((2, sites), dtype=object)
    a[0, :] = KEY + size_off
    a[1, 0] = seed
    s = still(a)
    rows, top, lo, hi = [], 0, None, None
    for t in range(1, rounds + 1):
        s = step.tick(lay, s)
        top = max(top, int(max(abs(v) for v in s.a[1].tolist())))
        sz = int(s.a[0, probe_site]) ** 2 + int(s.a[1, probe_site]) ** 2 - N
        lo = sz if lo is None else min(lo, sz)
        hi = sz if hi is None else max(hi, sz)
        if carry(t, window, 0)[1] == 0:
            rows.append(f"{t}: |k_1| {top}, swing {ppm(hi - lo, N)}")
            top, lo, hi = 0, None, None
    return rows, ring_flips([int(v) for v in s.a[1].tolist()])



GRIPS = 0
print("(A') r1's case (A) with the held rows Mesh-less (grip 0), a ring of 256; per 250 rounds the largest |k_1| over"
      " the ring and the size's swing at Node-clock 128 in ppm of n:", flush=True)
for label, off, seed in (("the size off its rest by 312, the angle seeded 100 at one Node-clock", 312, 100),
                         ("the size off its rest by 312, the angle seeded 100 at every Node-clock", 312, -100)):
    if seed < 0:
        lay, sites = layout((256, 1, 1), [GRIPS, GRIPS], hat_terms((0, 1), 1, N))
        a = np.zeros((2, sites), dtype=object)
        a[0, :] = KEY + off
        a[1, :] = 100
        s = still(a)
        top_all, lo, hi, rows = 0, None, None, []
        for t in range(1, 3001):
            s = step.tick(lay, s)
            top_all = max(top_all, int(max(abs(v) for v in s.a[1].tolist())))
            sz = int(s.a[0, 128]) ** 2 + int(s.a[1, 128]) ** 2 - N
            lo = sz if lo is None else min(lo, sz)
            hi = sz if hi is None else max(hi, sz)
            if carry(t, 250, 0)[1] == 0:
                rows.append(f"{t}: |k_1| {top_all}, swing {ppm(hi - lo, N)}")
                top_all, lo, hi = 0, None, None
        print(f"  {label}: " + "; ".join(rows), flush=True)
    else:
        rows, fl = case_a(off, seed)
        print(f"  {label}: " + "; ".join(rows) + f"; k_1's sign changes around the ring at the end {fl}", flush=True)


def case_b(offsets, seed=100, rounds=6000, window=1000):
    """Mesh-less, each Node-clock its own hand: Node-clock i laid still at (R + offsets[i], seed)."""
    sites_n = len(offsets)
    lay, sites = layout((sites_n, 1, 1), [0, 0], hat_terms((0, 1), 1, N))
    a = np.zeros((2, sites), dtype=object)
    for i, off in enumerate(offsets):
        a[0, i] = KEY + off
        a[1, i] = seed
    s = still(a)
    tops = [[0] * sites for _ in range(carry(rounds, window, 0)[0])]
    lo_k = [None] * sites
    hi_k = [None] * sites
    hi_l = [0] * sites
    for t in range(1, rounds + 1):
        s = step.tick(lay, s)
        w = carry(t - 1, window, 0)[0]
        for i in range(sites):
            k0, k1 = int(s.a[0, i]), int(s.a[1, i])
            b0, b1 = int(s.b[0, i]), int(s.b[1, i])
            tops[w][i] = max(tops[w][i], abs(k1))
            sz = k0 * k0 + k1 * k1 - N
            lo_k[i] = sz if lo_k[i] is None else min(lo_k[i], sz)
            hi_k[i] = sz if hi_k[i] is None else max(hi_k[i], sz)
            hi_l[i] = max(hi_l[i], abs(k0 * b1 - k1 * b0))
    out = []
    for i, off in enumerate(offsets):
        per = ", ".join(str(tops[w][i]) for w in range(len(tops)))
        q = carry(2000 * off, KEY, 0)[0]
        out.append(f"  laid at R + ({off}), 2 d / R = {q} thousandths: the largest |k_1| per "
                   f"{window} rounds {per}; |k|^2 - n from {ppm(lo_k[i], N)} to {ppm(hi_k[i], N)} ppm of n; "
                   f"the largest |k_0 b_1 - k_1 b_0| (the hand's turn, now against before) {hi_l[i]}")
    return out


print("(B') the held rows Mesh-less, each Node-clock its own hand, laid still with the angle at 100 and the size off"
      " its rest by d, 6,000 rounds (60 of the size's beats); the hat's push is along k, so the hand's turn, now"
      " against before, starts at 0:", flush=True)
for row in case_b([50, 100, 312, 625, 938, 1250, 1294, 1300, 1406, 1875, -50, -312, -1250, -3000]):
    print(row, flush=True)
