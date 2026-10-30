"""Two hands bound by coupling rows run as one clock, on 7a's own act and tables (exact integers; phases read in floats).

usage: python -I f2_fusion_on_the_act.py <tensor24 src>
The universe: A and B, two Gaussian hands of one kind (A1, then T1), each W = W+ = 1,000, s = 1, its spring D = 30; H, an A1
gear held at 1 (s = 0); coupling rows through 7a's load.plan: J_A = g C[K; A1, K](H, B) and J_B = g C[K; A1, K](H, A), part
by part, g = 10. One Node-clock (the board 1 x 1 x 1, so no Mesh pulls). Derived from the act's linear part: a free hand
turns by w with 2 - 2 cos w = s D / W; bound, the pair's two modes turn by w_S (D - g) and w_O (D + g). Measured over 2,000
ticks: each hand's turn, the composite's turn (C_K on the two hands, the product of the Gaussian parts), the kinds' turns
for T1 hands (A1, E, T2 even under the exchange, T1 odd), the fill of the shares at every tick, and the run back.
"""

import math
import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import home  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, State  # noqa: E402
from tensor24.runner import board as B  # noqa: E402
from tensor24.runner import load as L  # noqa: E402

GAMMA, SHAPE, W, D, G, TICKS, R = 1000, (1, 1, 1), 1000, 30, 10, 2000, 10**9
NAMES = ("A1", "A2", "E", "T1", "T2")
lab = {n: j for j, n in enumerate(NAMES)}
obj = lambda x: np.asarray(x, dtype=object)  # noqa: E731
kinds, tables = main.made(SHAPE)
labels, dims = tuple(n.upper() for n in kinds._fields), tuple(k.shape[-1] for k in kinds)
nb, meshes = B.board(SHAPE)
n = nb.shape[1]
turn = lambda q: 2 * math.asin(math.sqrt(q) / 2)  # noqa: E731
w0, wS, wO = turn(D / W), turn((D - G) / W), turn((D + G) / W)


def build(kind, g):
    trains, found = L.trains_of(
        [{"name": "A", "kinds": [kind], "part": 2}, {"name": "B", "kinds": [kind], "part": 2}, {"name": "H", "kinds": ["A1"], "part": 1}],
        labels, dims)
    assert not found, found
    couplings = []
    for p in (0, 1):
        couplings.append([2, 0, 0, 0, 1, 0, p, 0, 0, 0, p, g])  # J_A, part p = g C[K; A1, K](H, B part p)
        couplings.append([2, 0, 0, 0, 0, 0, p, 0, 1, 0, p, g])  # J_B, part p = g C[K; A1, K](H, A part p)
    plan, refused = L.plan(couplings, trains, tables, labels, 3)
    assert not refused, refused
    rows = sum(t.rows() for t in trains)
    held = rows - 1
    col = lambda v: obj(np.array(v).reshape(-1, 1))  # noqa: E731
    ws = [W] * held + [1]
    gearing = Gearing(col(ws), col(ws), col([1] * held + [0]), col([D] * held + [0]), 1, col([1] * rows))
    layout = Layout(nb, meshes, obj(np.zeros((rows, 3 * n), int)), gearing, plan, obj(np.full((1, n), GAMMA)), GAMMA)
    return trains, layout, rows, ws


def start(trains, rows, ws, u, v, w_even, w_odd):
    """A = S + D and B = S - D, S = (u + v) / 2 turning by w_even and D = (u - v) / 2 by w_odd from the before slot."""
    a, b = obj(np.zeros((rows, n), int)), obj(np.zeros((rows, n), int))
    for x in range(len(u)):
        s_, d_ = (u[x] + v[x]) / 2, (u[x] - v[x]) / 2
        back_s = complex(s_ * math.cos(w_even), -s_ * math.sin(w_even))
        back_d = complex(d_ * math.cos(w_odd), -d_ * math.sin(w_odd))
        for t, now, before in ((trains[0], u[x], back_s + back_d), (trains[1], v[x], back_s - back_d)):
            a[t.row(0, x, 0), 0] = now
            b[t.row(0, x, 0), 0] = round(before.real)
            b[t.row(0, x, 1), 0] = round(before.imag)
    a[rows - 1, 0] = b[rows - 1, 0] = 1  # H held at 1
    r = obj(np.array([[home(x, 0)] for x in ws]))
    zero = obj(np.zeros((rows, n), int))
    one = obj(np.zeros((1, n), int))
    return State(a, b, r, zero.copy(), zero.copy(), one, one.copy(), one.copy())


def fitted(series, turns):
    """The least-squares fit of a complex record by the given turns per tick: its relative residual (a reading)."""
    t = np.arange(len(series))
    basis = np.stack([np.exp(1j * w * t) for w in turns], axis=1)
    coef, *_ = np.linalg.lstsq(basis, series, rcond=None)
    return float(np.linalg.norm(series - basis @ coef) / np.linalg.norm(series))


def hand(trains, s, t):
    d = trains[t].dims[0]
    return [complex(int(s.a[trains[t].row(0, x, 0), 0]), int(s.a[trains[t].row(0, x, 1), 0])) for x in range(d)]


def gauss(trains, s, t):
    d = trains[t].dims[0]
    return [(int(s.a[trains[t].row(0, x, 0), 0]), int(s.a[trains[t].row(0, x, 1), 0])) for x in range(d)]


def cmul(p, q):
    return (p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0])


def composite(kind, m, u, v):
    """C_m[kind, kind] on two Gaussian hands, exact: each entry the sum of the table's terms, Gaussian products."""
    c = np.asarray(tables[(lab[kind], lab[kind], lab[m])], dtype=object)
    out = []
    for x in range(c.shape[0]):
        re = im = 0
        for y in range(c.shape[1]):
            for z in range(c.shape[2]):
                if c[x, y, z]:
                    pr = cmul(u[y], v[z])
                    re += int(c[x, y, z]) * pr[0]
                    im += int(c[x, y, z]) * pr[1]
        out.append((re, im))
    return out


def slope(phases):
    unwrapped = np.unwrap(np.array(phases))
    return (unwrapped[-1] - unwrapped[0]) / (len(phases) - 1)


def phase_of(entries):
    """The turn of a list of Gaussian entries: the phase of its largest entry (a reading)."""
    re, im = max(entries, key=lambda e: e[0] * e[0] + e[1] * e[1])
    return math.atan2(im, re)


def run(layout, s):
    states, outs = [s], []
    for _ in range(TICKS):
        s, o = step.tick(layout, s, 1)
        states.append(s)
        outs.append(o)
    return states, outs


def same(s, t):
    return all(np.array_equal(np.asarray(x), np.asarray(y)) for x, y in zip(s, t, strict=True))


print(f"derived from the act's linear part (W {W}, D {D}, g {G}): a free hand turns by w0 = {w0:.9f} a tick; bound, the even")
print(f"mode by w_S = {wS:.9f} and the odd mode by w_O = {wO:.9f}; the free composite by 2 w0 = {2 * w0:.9f}, the bound even")
print(f"composite by 2 w_S = {2 * wS:.9f}: the binding lowers the pair's turn by {2 * (w0 - wS):.9f} a tick")

print("\n1. Two A1 hands, equal at the start:")
for g, w, label in ((0, w0, "free (g = 0)"), (G, wS, f"bound (g = {G})")):
    trains, layout, rows, ws = build("A1", g)
    s0 = start(trains, rows, ws, [R], [R], w, w)
    states, outs = run(layout, s0)
    ph_a = slope([phase_of(gauss(trains, s, 0)) for s in states])
    ph_c = slope([phase_of(composite("A1", "A1", gauss(trains, s, 0), gauss(trains, s, 1))) for s in states])
    equal = all(gauss(trains, s, 0) == gauss(trains, s, 1) for s in states)
    back = states[-1]
    for o in reversed(outs):
        back = step.untick(layout, back, o)
    print(f"   {label}: a hand turns by {ph_a:.9f} (derived {w:.9f}); the composite A x B by {ph_c:.9f} (derived {2 * w:.9f});"
          f" the two hands equal bit for bit at every tick {equal}; the run back exact {same(back, s0)}")

print("\n2. Two T1 hands, bound (g = 10):")
for label, u, v in (("equal at the start", [R, 2 * R // 3, -R // 2], [R, 2 * R // 3, -R // 2]),
                    ("unequal at the start", [R, 2 * R // 3, -R // 2], [-R // 3, R, R // 4])):
    trains, layout, rows, ws = build("T1", G)
    s0 = start(trains, rows, ws, u, v, wS, wO)
    states, outs = run(layout, s0)
    fills = 0
    odd_zero = True
    beats = {}
    for m in ("A1", "E", "T1", "T2"):
        beats[m] = []
    for s in states:
        hu, hv = gauss(trains, s, 0), gauss(trains, s, 1)
        norm = sum(re * re + im * im for re, im in hu) * sum(re * re + im * im for re, im in hv)
        total = Fraction(0)
        for m, n_m, form in (("A1", 3, [[1]]), ("E", 9, [[2, -1], [-1, 2]]), ("T1", 2, None), ("T2", 2, None)):
            y = composite("T1", m, hu, hv)
            if form is None or len(form) == 1:
                size = sum(re * re + im * im for re, im in y)
            else:
                (a0, b0), (a1, b1) = y
                size = 2 * (a0 * a0 + b0 * b0) - 2 * (a0 * a1 + b0 * b1) + 2 * (a1 * a1 + b1 * b1)
            total += Fraction(size, n_m)
            if any(re or im for re, im in y):
                beats[m].append(phase_of(y))
            else:
                beats[m].append(None)
        fills += total == norm
        odd_zero &= label.startswith("unequal") or not any(re or im for re, im in composite("T1", "T1", hu, hv))
    back = states[-1]
    for o in reversed(outs):
        back = step.untick(layout, back, o)
    print(f"   {label}: the fill SUM_m |C_m(A x B)|^2_m / n_m = |A|^2 |B|^2 at {fills} of {len(states)} ticks; the run back exact"
          f" {same(back, s0)}")
    if label.startswith("equal"):
        print(f"      the odd kind T1 (the cross) of two equal hands stays 0 at every tick: {odd_zero}")
        for m in ("A1", "E", "T2"):
            print(f"      {m} turns by {slope(beats[m]):.9f} a tick (derived 2 w_S = {2 * wS:.9f})")
    else:
        print(f"      the odd kind T1 turns by {slope([b for b in beats['T1'] if b is not None]):.9f} a tick "
              f"(derived w_S + w_O = {wS + wO:.9f})")
        for m in ("A1", "E", "T1", "T2"):
            series = np.array([complex(*composite("T1", m, gauss(trains, s, 0), gauss(trains, s, 1))[0]) for s in states])
            two = fitted(series, (2 * wS, 2 * wO))
            one = fitted(series, (wS + wO,))
            print(f"      {m}, its first component: the record fitted by the turns 2 w_S and 2 w_O leaves {two:.2e} of it;"
                  f" by the one turn w_S + w_O, {one:.2e}")

print("\n3. The composite written as a train of its own kind (A1, one Gaussian hand), its coefficients from its parts' alone:")
print("   the even pair turns by 2 w_S, and 2 - 2 cos 2w = q (4 - q) with q = s (D - g h) / W, so at W_c = W^2 and s_c = 1")
qn = 1 * (D - G * 1)
Wc, Dc = W * W, qn * (4 * W - qn)
print(f"   its spring is D_c = s (D - g h)(4 W - s (D - g h)) = {Dc}, whole, with W_c = {Wc}")
trains_c, found = L.trains_of([{"name": "C", "kinds": ["A1"], "part": 2}], labels, dims)
col = lambda v: obj(np.array(v).reshape(-1, 1))  # noqa: E731
lay_c = Layout(nb, meshes, obj(np.zeros((2, 3 * n), int)), Gearing(col([Wc, Wc]), col([Wc, Wc]), 1, col([Dc, Dc]), 1, col([1, 1])),
               L.plan([], trains_c, tables, labels, 3)[0], obj(np.full((1, n), GAMMA)), GAMMA)
amp = R * R // 10**6
a_c = obj(np.array([[amp], [0]]))
b_c = obj(np.array([[round(amp * math.cos(2 * wS))], [-round(amp * math.sin(2 * wS))]]))
zero2, one1 = obj(np.zeros((2, n), int)), obj(np.zeros((1, n), int))
s_c = State(a_c, b_c, obj(np.array([[home(Wc, 0)], [home(Wc, 0)]])), zero2.copy(), zero2.copy(), one1, one1.copy(), one1.copy())
states_c, outs_c = [s_c], []
for _ in range(TICKS):
    s_c, o = step.tick(lay_c, s_c, 1)
    states_c.append(s_c)
    outs_c.append(o)
turn_c = slope([math.atan2(int(s.a[1, 0]), int(s.a[0, 0])) for s in states_c])
back = states_c[-1]
for o in reversed(outs_c):
    back = step.untick(lay_c, back, o)
print(f"   measured: the written composite turns by {turn_c:.9f} a tick, the bound pair's composite reading by {2 * wS:.9f}"
      f" (derived); the run back exact {same(back, states_c[0])}")
DEN, G16 = 15162856759112389, 16
T_ex = 6 * DEN * GAMMA**2 * G16**2
print(f"   the price at the example universe: a train's W = 2 T is {(2 * T_ex).bit_length()} bits, so W_c = W^2 is"
      f" {((2 * T_ex) ** 2).bit_length()} bits, past the width 128, as the rim den^2 is (f1 item 4)")

print("\n4. The same composite booked at the parts' own teeth, W_c = W, D_c = s (D - g h)(4 W - s (D - g h)) div W, one carry at")
print("   load (a booking of the law's kind, as the rate line's), so no width is added:")
for Wb, Db, Gb in ((1000, 30, 10), (10**9 + 7, 3 * 10**7 + 1, 10**7)):
    qb = Db - Gb
    Dcb = qb * (4 * Wb - qb) // Wb
    exact_turn = 2 * turn(qb / Wb)
    lay_b = Layout(nb, meshes, obj(np.zeros((2, 3 * n), int)), Gearing(col([Wb, Wb]), col([Wb, Wb]), 1, col([Dcb, Dcb]), 1, col([1, 1])),
                   L.plan([], trains_c, tables, labels, 3)[0], obj(np.full((1, n), GAMMA)), GAMMA)
    a_b = obj(np.array([[R], [0]]))
    b_b = obj(np.array([[round(R * math.cos(exact_turn))], [-round(R * math.sin(exact_turn))]]))
    s_b = State(a_b, b_b, obj(np.array([[home(Wb, 0)], [home(Wb, 0)]])), zero2.copy(), zero2.copy(), one1, one1.copy(), one1.copy())
    ph = [math.atan2(int(s_b.a[1, 0]), int(s_b.a[0, 0]))]
    for _ in range(TICKS):
        s_b, _ = step.tick(lay_b, s_b, 1)
        ph.append(math.atan2(int(s_b.a[1, 0]), int(s_b.a[0, 0])))
    got = slope(ph)
    print(f"   W {Wb}, D {Db}, g {Gb}: D_c {Dcb}; the composite turns by {got:.12f}, the bound pair by {exact_turn:.12f};"
          f" apart by {abs(got - exact_turn) / exact_turn:.1e} of it")
