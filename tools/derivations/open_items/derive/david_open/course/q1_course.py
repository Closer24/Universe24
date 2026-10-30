"""The great clock's course under the load c with the spring of one notch, on stage 7a's own act (exact integers).

usage: python3 -I q1_course.py <tensor24 src> <engine-5.0 src>
  (1) the board's mean count under a held density, every Node-clock alike (p17 (4)'s setting, Gamma 1,000, W = Gamma / 2,
      D = 1, the source 900 a tick): 30 swings, each swing's top and bottom, the period, the discrete energy, the run back;
  (2) a seed: held sources at three Node-clocks of an 8^3 board (Gamma 1,200, W = 600, D = 1, the grip W / 6 per Mesh):
      the board's summed count against the k = 0 law, the local tops' ticks (how far the tops part), the run back;
  (3) the turnover T at the top against the forward swing: a moving matter gear sources the count; run A swings on, run B
      applies T = (a, b, r, go) -> (b, a, w - 1 - r, 1 - go) on every gear at the mean count's first top. T S T = S^-1 is
      checked first on random states;
  (4) the late acceleration: the Mesh's proper length h = Y(c) / Gamma (the ruler from the head's table, a hill read at 0)
      against the proper time, dtau = (Gamma / Y) dt, along (1)'s first swing and a weak one, and a source raised in the
      decelerating phase.
The comparisons below are the probe's readings, outside the act; the act holds none.
"""
import math
import sys

sys.path.insert(0, sys.argv[1])
sys.path.insert(1, sys.argv[2])
import numpy as np  # noqa: E402

from event_universe.core import rates  # noqa: E402
from tensor24.algebra.carry import home  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, State  # noqa: E402


def board(shape):
    xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    steps = [sign * axis for axis in np.eye(3, dtype=int) for sign in (1, -1)]
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % sides), shape) for s in steps])


def meshes_of(nb):
    axes, n = np.arange(len(nb)) // 2, nb.shape[1]
    own, theirs = axes[:, None] * n + np.arange(n)[None, :], axes[:, None] * n + nb
    return np.where((np.arange(len(nb)) % 2 == 0)[:, None], own, theirs)


def obj(x):
    return np.asarray(x, dtype=object)


def layout_of(nb, grip, gearing, plan, gamma):
    n = nb.shape[1]
    return Layout(nb, meshes_of(nb), grip, gearing, plan, obj(np.full((1, n), gamma)), gamma)


def equal(s, t):
    return all(np.array_equal(x, y) for x, y in zip(s, t, strict=True))


def zeros(rows, n):
    return obj(np.zeros((rows, n), int))


def run(layout, s, ticks, keep=False):
    outs, states = [], []
    for _ in range(ticks):
        if keep:
            states.append(s)
        s, out = step.tick(layout, s, 1)
        outs.append(out)
    return s, outs, states


def back(layout, s, outs):
    for out in reversed(outs):
        s = step.untick(layout, s, out)
    return s


def extrema(path):
    tops = [t for t in range(1, len(path) - 1) if path[t - 1] < path[t] >= path[t + 1]]
    lows = [t for t in range(1, len(path) - 1) if path[t - 1] > path[t] <= path[t + 1]]
    return tops, lows


# (1) the mean count under a held density ------------------------------------------------------------------------------
GAMMA = 1000
w, D, m = GAMMA // 2, 1, 30
S = m * m
nb = board((2, 2, 2))
n = nb.shape[1]
plan = Plan(np.array([1], np.intp), np.array([1], np.intp), obj([1]), np.array([0], np.intp))  # J_0 = m m
gearing = Gearing(obj([[w], [1]]), obj([[w], [1]]), 1, obj([[D], [0]]), 1, obj([[1], [1]]))
lay1 = layout_of(nb, zeros(2, 3 * n), gearing, plan, GAMMA)
a = obj(np.vstack([np.zeros((1, n), int), np.full((1, n), m)]))
start = State(a, a.copy(), obj(np.vstack([np.full((1, n), home(w, 0)), np.zeros((1, n), int)])), zeros(2, n),
              zeros(2, n), zeros(1, n), zeros(1, n), zeros(1, n))
ticks = 4300
s, outs, states = run(lay1, start, ticks, keep=True)
states.append(s)
path = [int(x.a[0, 0]) for x in states]  # the count at the tick's start, the bang at tick 0
tops, lows = extrema(path)
cstar = S // D
print("(1) the board's mean count under a held density, Gamma 1,000, W = 500, D = 1, the source 900 (rest c* = 900):")
print(f"  {len(tops)} tops in {ticks} ticks; the first at tick {tops[0]} reading {path[tops[0]]:,} (2 c* = {2 * cstar:,})")
print(f"  the tops read {min(path[t] for t in tops):,} to {max(path[t] for t in tops):,}; the bottoms"
      f" {min(path[t] for t in lows):,} to {max(path[t] for t in lows):,}")
per = [b - a for a, b in zip(tops, tops[1:])]
print(f"  the periods top to top: {min(per)} to {max(per)} ticks, mean {sum(per) / len(per):.3f};"
      f" 2 pi sqrt(W / D) = {2 * math.pi * math.sqrt(w / D):.3f}")


def energy(st, prev, w, D, cstar):
    p = w * (st.a[0, 0] - st.b[0, 0]) + (st.r[0, 0] - home(w, st.go[0, 0]))
    return p * p + w * D * (st.a[0, 0] - cstar) * (st.b[0, 0] - cstar)


E = [energy(x, None, w, D, cstar) for x in states[1:]]
first_mean, last_mean = sum(E[:140]) / 140, sum(E[-140:]) / 140
print(f"  the discrete energy p^2 + W D (a - c*)(a- - c*): start {E[0]:,}, range {min(E):,} to {max(E):,}"
      f" ({(max(E) - min(E)) / E[0]:.2%} of the start); its mean over the first swing {first_mean:,.0f} and over the"
      f" last {last_mean:,.0f} ({last_mean / first_mean - 1:+.4%}); over 214 swings see q1b_energy.txt")
print(f"  the run back through {ticks} ticks: exact {equal(back(lay1, s, outs), start)}")

# the acceleration of the Mesh's proper length along the first swing --------------------------------------------------
LAM = math.log(GAMMA / (GAMMA - 1))  # h = Y(c) / Gamma = (Gamma / (Gamma - 1))^c on the hills' side: ln h = LAM c


def signs_of(states, w, D, S, lam):
    """The sign of d2h / dtau2 at each tick: h = e^(lam c), dtau = dt / h (h N = 1), so d2h / dtau2 = lam h^3 (c'' + 2 lam c'^2),
    with c' = p / W the stride read with its fine tooth and c'' = (S - D a) / W the act's own push, both exact."""
    out = []
    for st in states:
        p = int(w * (st.a[0, 0] - st.b[0, 0]) + (st.r[0, 0] - home(w, st.go[0, 0])))
        acc = (S - D * int(st.a[0, 0])) / w + 2 * lam * (p / w) ** 2
        out.append((1 if acc > 0 else -1, p))
    return out


def phases(sg, upto):
    runs, cur = [], None
    for t in range(1, upto + 1):
        if sg[t][0] != cur:
            runs.append((t, '+' if sg[t][0] > 0 else '-'))
            cur = sg[t][0]
    return runs


def top_of(sg):
    return next(t for t in range(2, len(sg)) if sg[t - 1][1] > 0 >= sg[t][1])


print("(4) the Mesh's proper length h = Y(c) / Gamma against the proper time, from the bang (c = 0 at rest):")
sg = signs_of(states, w, D, S, LAM)
tp = top_of(sg)
print(f"  the strong swing (c* = 900): d2h / dtau2 by tick to the top at {tp} (the stride's sign turn): {phases(sg, tp)};"
      f" a quarter period is {math.pi / 2 * math.sqrt(w / D):.1f}, and the count passes c* at tick"
      f" {next(t for t in range(len(path)) if path[t] >= cstar)}")

a_w = obj(np.vstack([np.zeros((1, n), int), np.full((1, n), 3)]))
st_w = State(a_w, a_w.copy(), obj(np.vstack([np.full((1, n), home(w, 0)), np.zeros((1, n), int)])), zeros(2, n),
             zeros(2, n), zeros(1, n), zeros(1, n), zeros(1, n))
_, _, sw = run(lay1, st_w, 200, keep=True)
sgw = signs_of(sw, w, D, 9, LAM)
tpw = top_of(sgw)
print(f"  the weak swing (c* = 9): the top at {tpw} reading {int(sw[tpw].a[0, 0])}; d2h / dtau2 by tick: {phases(sgw, tpw)}")

a_d = obj(np.vstack([np.zeros((1, n), int), np.full((1, n), m)]))
st_d = State(a_d, a_d.copy(), obj(np.vstack([np.full((1, n), home(w, 0)), np.zeros((1, n), int)])), zeros(2, n),
             zeros(2, n), zeros(1, n), zeros(1, n), zeros(1, n))
s_d, _, sd = run(lay1, st_d, 62, keep=True)
raised = State(obj(np.vstack([s_d.a[0:1], np.full((1, n), 45)])), obj(np.vstack([s_d.b[0:1], np.full((1, n), 45)])),
               s_d.r, s_d.go, s_d.rd, s_d.ph, s_d.c, s_d.tn)  # the held source 30 -> 45: 900 -> 2,025 at tick 62
_, _, sd2 = run(lay1, raised, 140, keep=True)
sgd = signs_of(sd, w, D, S, LAM) + signs_of(sd2, w, D, 2025, LAM)
tpd = top_of(sgd)
print(f"  the source raised from 900 to 2,025 at tick 62, inside the decelerating phase, the count then {int(sd2[0].a[0, 0]):,} (above its old rest):"
      f" the top at {tpd}; d2h / dtau2 by tick: {phases(sgd, tpd)}")


# (2) a seed: three held sources on an 8^3 board -----------------------------------------------------------------------
G2 = 1200
w2, D2, g2 = G2 // 2, 1, G2 // 12  # W = 600, D / W = 2 / Gamma, the grip W / 6 per Mesh (the cone 1/6)
shape = (8, 8, 8)
nb2 = board(shape)
n2 = nb2.shape[1]
grip2 = obj(np.vstack([np.full((1, 3 * n2), g2), np.zeros((1, 3 * n2), int)]))
gearing2 = Gearing(obj([[w2], [1]]), obj([[w2], [1]]), 1, obj([[D2], [0]]), 1, obj([[1], [1]]))
plan2 = Plan(np.array([1], np.intp), np.array([1], np.intp), obj([100]), np.array([0], np.intp))  # J_0 = 100 m m
lay2 = layout_of(nb2, grip2, gearing2, plan2, G2)
src = np.zeros(n2, int)
for where, mm in (((1, 1, 1), 40), ((5, 2, 6), 30), ((3, 6, 3), 20)):
    src[np.ravel_multi_index(where, shape)] = mm
a2 = obj(np.vstack([np.zeros((1, n2), int), src[None, :]]))
start2 = State(a2, a2.copy(), obj(np.vstack([np.full((1, n2), home(w2, 0)), np.zeros((1, n2), int)])), zeros(2, n2),
               zeros(2, n2), zeros(1, n2), zeros(1, n2), zeros(1, n2))
t2 = 470
s2, outs2, st2 = run(lay2, start2, t2, keep=True)
st2.append(s2)
total = [int(x.a[0].sum()) for x in st2]
imp = [int((w2 * (x.a[0] - x.b[0]) + (x.r[0] - home(w2, x.go[0]))).sum()) for x in st2]
law = all(imp[t + 1] - imp[t] == 100 * int((src * src).sum()) - D2 * total[t] for t in range(t2))
tt, tl = extrema(total)
print("(2) a seed on an 8^3 board, Gamma 1,200, W = 600, D = 1, the grip 100 per Mesh, held sources 160,000, 90,000 and"
      " 40,000 a tick at three Node-clocks:")
print(f"  the board's summed impulse moves by SUM K - D SUM a at every tick of {t2}: {law}")
print(f"  the summed count's tops at {tt[:3]} and lows at {tl[:3]} (2 pi sqrt(Gamma / 2) = {2 * math.pi * math.sqrt(G2 / 2):.1f});"
      f" the top reads {total[tt[0]]:,} against 2 SUM S / D = {200 * int((src * src).sum()):,}")
cols = np.array([[int(v) for v in x.a[0]] for x in st2])
swing = int(round(2 * math.pi * math.sqrt(G2 / 2)))
own = [int(np.argmax(cols[: swing + 1, site])) for site in range(n2)]
ring = [len(extrema(list(cols[: swing + 1, site]))[0]) for site in range(n2)]
print(f"  each Node-clock's own top in the first swing (its largest count to tick {swing}): ticks {min(own)} to {max(own)},"
      f" median {int(np.median(own))}, against the summed count's {tt[0]}; local tops per Node-clock in that swing:"
      f" {min(ring)} to {max(ring)}, median {int(np.median(ring))}")
for where in ((1, 1, 1), (5, 2, 6), (3, 6, 3), (5, 5, 5)):
    p_ = cols[:, np.ravel_multi_index(where, shape)]
    tp, lw = extrema(list(p_[: swing + 1]))
    print(f"  the Node-clock {where}: its own top at {int(np.argmax(p_[: swing + 1]))} reading {int(max(p_[: swing + 1])):,};"
          f" its first local tops at {tp[:5]}")
print(f"  the run back through {t2} ticks: exact {equal(back(lay2, s2, outs2), start2)}")


# (3) the turnover T at the top against the forward swing --------------------------------------------------------------
def turn(s, ws):
    """T on every gear: (a, b, r, go) -> (b, a, w - 1 - r, 1 - go), the drive's fine tooth kept (T_d = 1 here)."""
    wcol = obj(np.array(ws)[:, None])
    return State(s.b.copy(), s.a.copy(), wcol - 1 - s.r, 1 - s.go, s.rd.copy(), s.ph, s.c, s.tn)


shape3 = (6, 6, 6)
nb3 = board(shape3)
n3 = nb3.shape[1]
wm, Dm = 600, 6  # the matter gear: W 600, its spring 6 (its rest beat 0.1 a tick), the grip 100 per Mesh
plan3 = Plan(np.array([1], np.intp), np.array([1], np.intp), obj([1]), np.array([0], np.intp))  # J_0 = m m
grip3 = obj(np.vstack([np.full((1, 3 * n3), g2), np.full((1, 3 * n3), g2)]))
gearing3 = Gearing(obj([[w2], [wm]]), obj([[w2], [wm]]), 1, obj([[D2], [Dm]]), 1, obj([[1], [1]]))
lay3 = layout_of(nb3, grip3, gearing3, plan3, G2)
rng = np.random.default_rng(3)

# T S T = S^-1 on random states first
holds = 0
for _ in range(20):
    a_ = obj(np.vstack([rng.integers(-500, 500, (1, n3)), rng.integers(-60, 60, (1, n3))]))
    b_ = a_ - obj(np.vstack([rng.integers(-9, 9, (1, n3)), rng.integers(-5, 5, (1, n3))]))
    r_ = obj(np.vstack([rng.integers(0, w2, (1, n3)), rng.integers(0, wm, (1, n3))]))
    go_ = obj(rng.integers(0, 2, (2, n3)))
    x = State(a_, b_, r_, go_, zeros(2, n3), zeros(1, n3), zeros(1, n3), zeros(1, n3))
    y, _ = step.tick(lay3, turn(x, [w2, wm]), 1)
    z = turn(y, [w2, wm])
    y2, _ = step.tick(lay3, z, 1)
    holds += all(np.array_equal(y2[i], x[i]) for i in range(5))
print(f"(3) T S T S = 1 on random states of the 6^3 board (the count and a matter gear, J_0 = m m): {holds} of 20")

am = np.zeros(n3, int)
bm = np.zeros(n3, int)
for xyz in np.ndindex(shape3):
    d2 = sum((u - 2) ** 2 for u in xyz)
    am[np.ravel_multi_index(xyz, shape3)] = int(round(40 * math.exp(-d2 / 2.0)))
    d2b = (xyz[0] - 1.6) ** 2 + (xyz[1] - 2) ** 2 + (xyz[2] - 2) ** 2  # moving toward +x
    bm[np.ravel_multi_index(xyz, shape3)] = int(round(40 * math.exp(-d2b / 2.0)))
a3 = obj(np.vstack([np.zeros((1, n3), int), am[None, :]]))
b3 = obj(np.vstack([np.zeros((1, n3), int), bm[None, :]]))
start3 = State(a3, b3, obj(np.vstack([np.full((1, n3), home(w2, 0)), np.full((1, n3), home(wm, 0))])), zeros(2, n3),
               zeros(2, n3), zeros(1, n3), zeros(1, n3), zeros(1, n3))
_, _, fA = run(lay3, start3, 330, keep=True)
sumA = [int(x.a[0].sum()) for x in fA]
tstar = int(np.argmax(sumA[:170]))
low_A = 100 + int(np.argmin(sumA[100:230]))
print(f"  run A, the forward swing: the summed count's first top at {tstar} reading {sumA[tstar]:,}, its low at {low_A}"
      f" reading {sumA[low_A]:,} (2 pi sqrt(Gamma / 2) = {2 * math.pi * math.sqrt(G2 / 2):.1f})")
s_top = fA[tstar]
sB, _, fB = run(lay3, turn(s_top, [w2, wm]), tstar, keep=True)
mirror = turn(start3, [w2, wm])
same = all(np.array_equal(sB[i], mirror[i]) for i in range(5))
print(f"  run B, T on every gear at the first top (tick {tstar}), then {tstar} ticks: the gears equal T of the bang's: {same}")
sA2 = fA[2 * tstar]


def centroid(row):
    v = np.array([float(x) for x in row])
    wts = v * v
    xyz = np.array(list(np.ndindex(shape3)), float)
    return tuple(round(float(u), 2) for u in (wts[:, None] * xyz).sum(0) / wts.sum()), int(wts.sum())


print(f"  at tick {2 * tstar}: the matter's centroid and m m sum in run A {centroid(sA2.a[1])},"
      f" in run B {centroid(sB.a[1])}, at the bang {centroid(start3.a[1])}")
print(f"  the summed count at tick {2 * tstar}: run A {int(sA2.a[0].sum()):,}, run B {int(sB.a[0].sum()):,}")
dA = sum(abs(int(u) - int(v)) for u, v in zip(sA2.a[1], mirror.a[1])) + sum(abs(int(u) - int(v)) for u, v in zip(sA2.b[1], mirror.b[1]))
dB = sum(abs(int(u) - int(v)) for u, v in zip(sB.a[1], mirror.a[1])) + sum(abs(int(u) - int(v)) for u, v in zip(sB.b[1], mirror.b[1]))
print(f"  the matter's two slots against T of the bang's, summed |difference|: run A {dA:,}, run B {dB:,}")
