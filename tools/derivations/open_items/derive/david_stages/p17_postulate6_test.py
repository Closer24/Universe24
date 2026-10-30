"""David's probe for the Boss's 6485503701 item 5: Postulate 6's integer test, and which gear 7b's time train should hold.

usage: python3 -I p17_postulate6_test.py <tensor24 worktree>/src <engine-5.0 checkout>/src
On stage 7a's own step (tensor24.engine.step), exact integers throughout, the rate line from the head's core/rates:
  (1) the drive run back where its teeth fall between ticks. A drive whose teeth hold the gear's own notch (my 00:0x
      item 5 in the ruler Y, T_d = Y_n T_0) has new teeth at every tick, and the run back reads r_d as a remainder at
      this tick's T_d while the last tick kept it at its own; counted over random rounds, the teeth rising and the
      gear's own W handed to W+ as the controls;
  (2) the time gear as the count c, the law's load (p0 = Gamma (1 - 1 / Gamma)^c): two held matter gears, each a
      source m m through J, alone and together; c_12 - c_1 - c_2 + c_0 at every Node-clock and tick, on a uniform board
      at teeth 1 and 6 (the strides and the counts), and with the masses at two Node-clocks at teeth 6; the mutant, the
      head's law: the same act on the stretch X = Gamma (Gamma / p0)^4, the count read back from X (floats, for the
      size of the miss alone);
  (3) the rates compose by their product on the law's rate line: Gamma rate(c1 + c2) against rate(c1) rate(c2), and the
      stretch's mutant read through the same line;
  (4) the board's summed impulse moves by its summed kick less D times its summed count, exactly (the grips one per
      Mesh); and on a uniform board under a held source of 900 a tick, the count with no spring and with the clock's
      one notch, D / W = 2 / Gamma (ALGEBRA.md line 352): its top and its lows, or none;
  (5) the ruler Y with the self-source in its product form, Y+ Y- T_0 = Y^2 (T_0 + N), one Node-clock, standalone
      (it is no act of 7a): a geometric run kept to the remainder 0, and the composition's miss against the mutant's.
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

GAMMA = 1000


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


def layout_of(nb, grip, gearing, plan):
    n = nb.shape[1]
    return Layout(nb, meshes_of(nb), grip, gearing, plan, obj(np.full((1, n), GAMMA)), GAMMA)


def equal(s, t):
    return all(np.array_equal(x, y) for x, y in zip(s, t, strict=True))


# (1) the drive's teeth between ticks -----------------------------------------------------------------------------
def run_back_holds(rng, drives, ws):
    """Tick once per entry of drives (T_d) with the gear's teeth ws[i] -> ws[i + 1], then run back; True if exact."""
    nb = board((3, 3, 3))
    n = nb.shape[1]
    plan = Plan(np.array([0], np.intp), np.array([4], np.intp), obj([3]), np.array([0], np.intp))  # J = 3 a F
    grip = obj(rng.integers(-2, 3, (1, 3 * n)))
    a = obj(rng.integers(-10**6, 10**6, (1, n)))
    s = State(a, a - obj(rng.integers(-50, 50, (1, n))), obj(rng.integers(0, ws[0], (1, n))),
              obj(rng.integers(0, 2, (1, n))), obj(rng.integers(0, drives[0], (1, n))),
              obj(np.zeros((1, n), int)), obj(np.zeros((1, n), int)), obj(np.zeros((1, n), int)))
    start, layouts, outs = s, [], []
    for i, teeth in enumerate(drives):
        layouts.append(layout_of(nb, grip, Gearing(obj(ws[i]), obj(ws[i + 1]), 1, 0, 1, obj(teeth)), plan))
        s, out = step.tick(layouts[-1], s, 1)
        outs.append(out)
    for layout, out in zip(reversed(layouts), reversed(outs), strict=True):
        s = step.untick(layout, s, out)
    return equal(s, start)


rng = np.random.default_rng(29)
print("(1) the run back over two ticks, 300 random rounds each (a drive J = 3 a F, grips one per Mesh):")
for label, drives, ws in (
    ("the drive's teeth falling, T_d 9 then 4, W 5 throughout", (9, 4), (5, 5, 5)),
    ("the drive's teeth rising, T_d 4 then 9, W 5 throughout", (4, 9), (5, 5, 5)),
    ("the gear's teeth falling, W 9 to 4 to 7, T_d 6 throughout", (6, 6), (9, 4, 7)),
):
    held = sum(run_back_holds(rng, drives, ws) for _ in range(300))
    print(f"  {label}: exact in {held} of 300")


# (2) the count's composition ----------------------------------------------------------------------------------------
def count_run(shape, masses, w, drive, ticks, gear_start=0, factor=1, uniform=False):
    """Rows: 0 the time gear (its grip 1 per Mesh, its teeth w, its drive's teeth drive), 1 and 2 the matter gears, held
    (grip 0, teeth 1, no source of their own); J_0 = factor (m1 m1 + m2 m2). The matter sits at two Node-clocks, or at
    every Node-clock where uniform. Returns the time gear's notch and its stride, at every tick."""
    nb = board(shape)
    n = nb.shape[1]
    plan = Plan(np.array([1, 2], np.intp), np.array([1, 2], np.intp), obj([factor, factor]), np.array([0, 0], np.intp))
    grip = obj(np.vstack([np.ones((1, 3 * n), int), np.zeros((2, 3 * n), int)]))
    col = lambda v0, v1, v2: obj([[v0], [v1], [v2]])  # noqa: E731
    gearing = Gearing(col(w, 1, 1), col(w, 1, 1), 1, col(0, 0, 0), 1, col(drive, 1, 1))
    layout = layout_of(nb, grip, gearing, plan)
    a = obj(np.zeros((3, n), int))
    a[0, :] = gear_start
    if uniform:
        a[1, :], a[2, :] = masses
    else:
        a[1, np.ravel_multi_index((1, 1, 1), shape)] = masses[0]
        a[2, np.ravel_multi_index((4, 3, 2), shape)] = masses[1]
    r = obj(np.vstack([np.full((1, n), home(w, 0)), np.zeros((2, n), int)]))
    zero = obj(np.zeros((1, n), int))
    s = State(a, a.copy(), r, obj(np.zeros((3, n), int)), obj(np.zeros((3, n), int)), zero, zero, zero)
    notches, strides = [], []
    for _ in range(ticks):
        s, _ = step.tick(layout, s, 1)
        notches.append(s.a[0].copy())
        strides.append(w * (s.a[0] - s.b[0]) + (s.r[0] - home(w, s.go[0])))
    return np.array(notches, dtype=object), np.array(strides, dtype=object)


def miss(runs, k):
    """c_12 - c_1 - c_2 + c_0 (the k-th output of each run), its largest size over every Node-clock and tick."""
    zero, one, two, both = (run[k] for run in runs)
    return max(abs(int(v)) for v in (both - one - two + zero).ravel())


print("(2) the time gear as the count c, two held sources m m composed (runs at (0, 0), (m1, 0), (0, m2), (m1, m2)):")
for w in (1, 6):
    runs = [count_run((2, 2, 2), m, w, 1, 200, uniform=True) for m in ((0, 0), (7, 0), (0, 9), (7, 9))]
    print(f"  a uniform board (no pull), teeth {w}, the drive on the force's path, 200 ticks: the strides miss by"
          f" {miss(runs, 1)}, the counts by {miss(runs, 0)} (the deepest count {max(int(v) for v in runs[3][0].ravel())})")
SHAPE, TICKS, MASSES = (6, 6, 6), 120, ((0, 0), (300, 0), (0, 400), (300, 400))
runs = [count_run(SHAPE, m, 6, 1, TICKS) for m in MASSES]
print(f"  the {SHAPE} board, the masses at two Node-clocks, teeth 6, {TICKS} ticks: the counts miss by {miss(runs, 0)}"
      f" (the deepest count {max(int(v) for v in runs[3][0].ravel())})")
# the mutant, the head's law: the same act on the stretch X = Gamma (Gamma / p0)^4, its sources four times the count's
# (so the two laws agree to the first order), X from the vacuum's Gamma; the count read back from X in floats
BIG = 10**6
stretch = [count_run(SHAPE, m, 6, 1, TICKS, gear_start=BIG, factor=4)[0] for m in MASSES]
read = np.vectorize(lambda x: math.log(int(x) / BIG) / (-4 * math.log(1 - 1 / BIG)))
k0, k1, k2, k12 = (read(x) for x in stretch)
gap = k12 - k1 - k2 + k0
at = np.unravel_index(np.argmax(np.abs(gap)), gap.shape)
print(f"  the mutant (the act on X, Gamma = {BIG:,}): the counts miss by up to {abs(gap[at]):,.0f}"
      f" (c_1 {k1[at]:,.0f} and c_2 {k2[at]:,.0f} there)")


# (3) the rates compose by their product on the law's rate line --------------------------------------------------------
print("(3) the law's rate line, p0 = Gamma (1 - 1 / Gamma)^c to the unit (the head's core/rates.rate), Gamma = 1,000:")
worst = 0
for c1 in range(0, 400, 7):
    for c2 in range(0, 400, 11):
        worst = max(worst, abs(GAMMA * rates.rate(GAMMA, c1 + c2) - rates.rate(GAMMA, c1) * rates.rate(GAMMA, c2)))
print(f"  |Gamma rate(c1 + c2) - rate(c1) rate(c2)| at most {worst} over c1, c2 below 400 (Gamma^2 = {GAMMA * GAMMA})")
c1 = c2 = 100
x = lambda c: GAMMA * (GAMMA / rates.rate(GAMMA, c)) ** 4  # noqa: E731
p_x = GAMMA * (GAMMA / (x(c1) + x(c2) - GAMMA)) ** 0.25
print(f"  the stretch's mutant at c1 = c2 = 100: Gamma p0(X_1 + X_2 - Gamma) - p0(c1) p0(c2) ="
      f" {GAMMA * p_x - rates.rate(GAMMA, c1) * rates.rate(GAMMA, c2):.0f}")


# (4) the board's summed count: the zero mode ------------------------------------------------------------------------
def summed(w, drive, ticks, spring):
    """Random grips one per Mesh on a (4, 4, 4) board; row 0 the time gear from a random start, row 1 a held source gear
    m, row 2 a held unit gear, J_0 = 5 m 1: SUM p+ - SUM p = SUM K - D SUM a over the time gear's row at every tick."""
    nb = board((4, 4, 4))
    n = nb.shape[1]
    rng = np.random.default_rng(7)
    plan = Plan(np.array([1], np.intp), np.array([2], np.intp), obj([5]), np.array([0], np.intp))
    col = lambda v0: obj([[v0], [1], [1]])  # noqa: E731
    gearing = Gearing(col(w), col(w), 1, obj([[spring], [0], [0]]), 1, col(drive))
    grip = obj(np.vstack([rng.integers(-3, 4, (1, 3 * n)), np.zeros((2, 3 * n), int)]))
    layout = layout_of(nb, grip, gearing, plan)
    a = obj(np.vstack([rng.integers(-40, 40, (1, n)), rng.integers(0, 9, (1, n)), np.ones((1, n), int)]))
    b = a - obj(np.vstack([rng.integers(-3, 3, (1, n)), np.zeros((2, n), int)]))
    r = obj(np.vstack([rng.integers(0, w, (1, n)), np.zeros((2, n), int)]))
    rd = obj(np.vstack([rng.integers(0, drive, (1, n)), np.zeros((2, n), int)]))
    s = State(a, b, r, obj(np.zeros((3, n), int)), rd, *(obj(np.zeros((1, n), int)) for _ in range(3)))
    impulse = lambda s: w * (s.a[0] - s.b[0]) + (s.r[0] - home(w, s.go[0]))  # noqa: E731
    for _ in range(ticks):
        _, j = step.sources(layout, s)
        q, _ = step.drive(j[0], drive, s.rd[0])
        now, _ = step.tick(layout, s, 1)
        if int(impulse(now).sum() - impulse(s).sum()) != int(q.sum() - spring * s.a[0].sum()):
            return False
        s = now
    return True


print("(4) the board's summed impulse moves by SUM K - D SUM a, exactly, at every tick of 40:",
      summed(7, 3, 40, 0) and summed(7, 3, 40, 2))
w = GAMMA // 2
for spring, label in ((0, "no spring"), (1, "the clock's one notch, D / W = 2 / Gamma")):
    plan = Plan(np.array([1], np.intp), np.array([1], np.intp), obj([1]), np.array([0], np.intp))
    nb = board((2, 2, 2))
    n = nb.shape[1]
    gearing = Gearing(obj([[w], [1]]), obj([[w], [1]]), 1, obj([[spring], [0]]), 1, obj([[1], [1]]))
    layout = layout_of(nb, obj(np.zeros((2, 3 * n), int)), gearing, plan)
    a = obj(np.vstack([np.zeros((1, n), int), np.full((1, n), 30)]))  # a uniform source m m = 900 at every Node-clock
    zero = obj(np.zeros((1, n), int))
    s = State(a, a.copy(), obj(np.vstack([np.full((1, n), home(w, 0)), np.zeros((1, n), int)])),
              obj(np.zeros((2, n), int)), obj(np.zeros((2, n), int)), zero, zero, zero)
    path = []
    for _ in range(600):
        s, _ = step.tick(layout, s, 1)
        path.append(int(s.a[0, 0]))
    peak = max(path[:140])
    lows = [t + 1 for t in range(1, len(path) - 1) if path[t - 1] > path[t] <= path[t + 1]]
    print(f"  {label}: the count at 100, 300, 600: {path[99]:,}, {path[299]:,}, {path[599]:,}; its largest in the first"
          f" 140 ticks {peak:,} at tick {path.index(peak) + 1}; its lows at {lows[:4] if lows else 'none'}"
          f" (2 pi sqrt(Gamma / 2) = {2 * math.pi * math.sqrt(GAMMA / 2):.1f})")


# (5) the ruler Y in the product form, one Node-clock ------------------------------------------------------------------
def ruler(y0, y1, t0, n_m, ticks):
    ys, r = [y0, y1], 0
    for _ in range(ticks):
        num = ys[-1] * ys[-1] * (t0 + n_m) + r
        nxt, r = divmod(num, t0 * ys[-2])
        ys.append(nxt)
    return ys, r


g = 7
ys, r = ruler(g**6, g**5 * 8, 1, 0, 5)
print("(5) the ruler Y, Y+ Y- T_0 = Y^2 (T_0 + N):")
print(f"  no source, Y_0 = 7^6, Y_1 = 7^5 8: Y_t = 7^(6 - t) 8^t kept to t = 6: {ys == [g**(6 - t) * 8**t for t in range(7)]},"
      f" the last remainder {r}")
x = [y**4 for y in ys[:2]]
x.append(2 * x[1] - x[0])
print(f"  the mutant (X = Y^4 / Gamma^3 linear in the tick) at t = 2: Y_2 = {x[2] ** 0.25:.2f} for {ys[2]}")
t0, n1, n2, ticks = 10**12, 3 * 10**6, 5 * 10**6, 400
big = 10**9
y1, _ = ruler(big, big, t0, n1, ticks)
y2, _ = ruler(big, big, t0, n2, ticks)
y12, _ = ruler(big, big, t0, n1 + n2, ticks)
e1, e2 = y1[-1] / big - 1, y2[-1] / big - 1
print(f"  sources {n1 / t0:.0e} and {n2 / t0:.0e} per tick, {ticks} ticks from rest (slowdowns {e1:.4f} and {e2:.4f}):"
      f" (Y_12 Y_0 - Y_1 Y_2) / Y_0^2 = {(y12[-1] * big - y1[-1] * y2[-1]) / big**2:.2e};"
      f" the mutant's 4 e1 e2 = {4 * e1 * e2:.2e}")
