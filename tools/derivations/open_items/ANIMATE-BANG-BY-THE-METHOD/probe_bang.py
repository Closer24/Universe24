"""The bang read through Sofer's method, How to think about solutions (Animate): what the one act gives of it by itself.

usage: python -I probe_bang.py <worktree>

On tensor24's own act (engine/step.py, stage 7a, as at tensor24-review 1de239790), exact integers throughout. The time
gear is a row of the act holding the count c, the clock's load (p0 = Gamma (1 - 1 / Gamma)^c); its spring is the clock's
one notch, D / W = 2 / Gamma (ALGEBRA.md line 35); matter sources it through J, its density m m.
  (1) the swing, on a board alike everywhere under a held density: the count's tops and lows over many swings, the
      period against 2 pi sqrt(Gamma / 2) at two Gammas, the same with no spring, and the run back through every swing;
  (2) the matter moving: a hand of two rows turning on its own spring and grips, one Node-clock holding one notch more
      (the seed's one tooth), its density the count's source: the tops swing by swing, the count's spread over the
      board, the books on the board at every tick (the summed impulse moves by the summed kick less D times the summed
      count) and the run back;
  (3) the reach on a chain: the count's settled profile from one held source, at the gearing the Boss reads from
      David's B (a grip of W / 6 per Mesh, s = 1, D / W = 2 / Gamma), against sqrt(grip / D) and sqrt(Gamma / 6).
The tops and lows are read here by comparing neighbours in time: the probe is a reader, not the act.
"""

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(sys.argv[1]).resolve() / "src"))
from tensor24.algebra.carry import home  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, State  # noqa: E402


def board(shape):
    """The six neighbours (+x, -x, +y, -y, +z, -z) on the torus of the shape."""
    xyz, sides = np.indices(shape).reshape(3, -1), np.array(shape)[:, None]
    steps = [sign * axis for axis in np.eye(3, dtype=int) for sign in (1, -1)]
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % sides), shape) for s in steps])


def meshes_of(nb):
    """Each Spoke's Mesh, numbered by its axis and its - end, so a Mesh's grip is read alike from both ends."""
    axes, n = np.arange(len(nb)) // 2, nb.shape[1]
    own, theirs = axes[:, None] * n + np.arange(n)[None, :], axes[:, None] * n + nb
    return np.where((np.arange(len(nb)) % 2 == 0)[:, None], own, theirs)


def obj(x):
    return np.asarray(x, dtype=object)


def layout_of(nb, grip, gearing, plan, gamma):
    n = nb.shape[1]
    return Layout(nb, meshes_of(nb), grip, gearing, plan, obj(np.full((1, n), gamma)), gamma)


def column(*values):
    return obj([[v] for v in values])


def at_rest(a, ws):
    """A state at rest: before equal to now, each fine tooth at its home, the clocks at their start."""
    rows, n = a.shape
    r = obj(np.vstack([np.full((1, n), home(w, 0)) for w in ws]))
    zero = obj(np.zeros((1, n), int))
    return State(a, a.copy(), r, obj(np.zeros((rows, n), int)), obj(np.zeros((rows, n), int)), zero, zero, zero)


def same(s, t):
    return all(np.array_equal(x, y) for x, y in zip(s, t, strict=True))


def run(layout, s, ticks, read):
    """Tick on every Node-clock every round, reading each state; then run back to the start: (readings, exact)."""
    start, outs, seen = s, [], []
    for _ in range(ticks):
        s, out = step.tick(layout, s, 1)
        outs.append(out)
        seen.append(read(s))
    for out in reversed(outs):
        s = step.untick(layout, s, out)
    return seen, same(s, start)


def turns(path):
    """The ticks (from 1) where a path tops and where it bottoms, read by its neighbours in time."""
    tops = [t + 1 for t in range(1, len(path) - 1) if path[t - 1] < path[t] >= path[t + 1]]
    lows = [t + 1 for t in range(1, len(path) - 1) if path[t - 1] > path[t] <= path[t + 1]]
    return tops, lows


# (1) the swing on a board alike everywhere ---------------------------------------------------------------------------
def swing(gamma, w, spring, ticks, m=30):
    """Row 0 the time gear (teeth w, spring D, the drive on the force's path), row 1 a held matter gear m at every Node-clock;
    J_0 = m m, so the count's kick is m m a tick. The count at one Node-clock (all alike), and the run back."""
    nb = board((1 + 1, 1 + 1, 1 + 1))
    n = nb.shape[1]
    plan = Plan(np.array([1], np.intp), np.array([1], np.intp), obj([1]), np.array([0], np.intp))
    gearing = Gearing(column(w, 1), column(w, 1), 1, column(spring, 0), 1, column(1, 1))
    layout = layout_of(nb, obj(np.zeros((1 + 1, 3 * n), int)), gearing, plan, gamma)
    a = obj(np.vstack([np.zeros((1, n), int), np.full((1, n), m)]))
    return run(layout, at_rest(a, (w, 1)), ticks, lambda s: int(s.a[0, 0]))


print("(1) the swing: the count on a board alike everywhere, a held density m m = 900 a tick at every Node-clock")
for gamma, ticks in ((1000, 1500), (4000, 1500)):
    w = gamma // 2
    path, exact = swing(gamma, w, 1, ticks)
    tops, lows = turns(path)
    gaps = [b - a for a, b in zip(lows, lows[1:], strict=False)]
    heights = sorted({path[t - 1] for t in tops})
    print(f"  Gamma {gamma:,}, W {w}, D 1 (D / W = 2 / Gamma), {ticks} ticks: {len(tops)} tops and {len(lows)} lows;"
          f" the lows at {lows[:5]}...; the swings {min(gaps)} to {max(gaps)} ticks against 2 pi sqrt(Gamma / 2) ="
          f" {2 * math.pi * math.sqrt(gamma / 2):.1f}")
    print(f"    the tops' heights {heights} (the count's rest at the source over D, 900, and twice it at the top);"
          f" the lows' depths {sorted({path[t - 1] for t in lows})}; the run back through every swing: {exact}")
path, exact = swing(1000, 500, 0, 600)
print(f"  no spring, Gamma 1,000, W 500: the count at 100, 300, 600: {path[99]:,}, {path[299]:,}, {path[599]:,};"
      f" tops {len(turns(path)[0])}; the run back: {exact}")
path, exact = swing(1000, 500, 1, 30000)
tops, lows = turns(path)
gaps = [b - a for a, b in zip(lows, lows[1:], strict=False)]
blocks = ", ".join(
    f"swings {lo + 1} to {min(hi, len(tops))}: tops {min(path[t - 1] for t in tops[lo:hi])} to"
    f" {max(path[t - 1] for t in tops[lo:hi])}, lows {min(path[t - 1] for t in lows[lo:hi])} to"
    f" {max(path[t - 1] for t in lows[lo:hi])}"
    for lo, hi in ((0, 30), (30, 60), (60, 120), (120, len(tops)))
)
print(f"  30,000 ticks at Gamma 1,000: {len(tops)} swings, each {min(gaps)} or {max(gaps)} ticks, their mean"
      f" {sum(gaps) / len(gaps):.3f} against the act's own 2 pi / (2 asin(sqrt(D / W) / 2)) ="
      f" {2 * math.pi / (2 * math.asin(math.sqrt(1 / 500) / 2)):.3f}; the run back: {exact}")
print(f"    {blocks}")


# (2) the matter moving: a hand turning, the seed's one tooth -----------------------------------------------------------
def moving(ticks, gamma=1000, w=500, wm=50, m=30):
    """Rows 0 the time gear (W 500, D 1, grip W / 6 per Mesh), 1 and 2 the hand's real and imaginary rows (W 50, D 1,
    grip W / 6 per Mesh), on a (4, 4, 4) board. The hand turns: re m at rest, im 0 with a stride of m sqrt(D / W) a
    tick, so its density re re + im im is nearly alike in time; the Node-clock (0, 0, 0) holds re m + 1, the seed's one
    tooth. J_0 = re re + im im. Per tick: the count's mean and spread, the books' identity; then the run back."""
    shape = (4, 4, 4)
    nb = board(shape)
    n = nb.shape[1]
    plan = Plan(np.array([1, 1 + 1], np.intp), np.array([1, 1 + 1], np.intp), obj([1, 1]), np.array([0, 0], np.intp))
    gearing = Gearing(column(w, wm, wm), column(w, wm, wm), 1, column(1, 1, 1), 1, column(1, 1, 1))
    grip = obj(np.vstack([np.full((1, 3 * n), w // 6), np.full((1 + 1, 3 * n), wm // 6)]))
    layout = layout_of(nb, grip, gearing, plan, gamma)
    a = obj(np.vstack([np.zeros((1, n), int), np.full((1, n), m), np.zeros((1, n), int)]))
    a[1, 0] = m + 1
    s = at_rest(a, (w, wm, wm))
    stride = round(m * math.sqrt(1 / wm))
    s = s._replace(b=s.b - obj(np.vstack([np.zeros((1 + 1, n), int), np.full((1, n), stride)])))
    impulse = lambda s: w * (s.a[0] - s.b[0]) + (s.r[0] - home(w, s.go[0]))  # noqa: E731
    held = []

    def read(now):
        held.append(now)
        return (sum(now.a[0]), max(now.a[0]) - min(now.a[0]))

    seen, exact = run(layout, s, ticks, read)
    books, before = 0, s
    for now in held:
        _, j = step.sources(layout, before)
        books += int(impulse(now).sum() - impulse(before).sum()) == int(j[0].sum() - before.a[0].sum())
        before = now
    return seen, exact, books, n


print("(2) the matter moving: a hand turning on its own spring and grips, the seed's one tooth at one Node-clock,"
      " its density the count's source ((4, 4, 4), Gamma 1,000)")
seen, exact, books, n = moving(1000)
means = [total / n for total, _ in seen]
tops, lows = turns(means)
print(f"  {len(tops)} tops of the count's mean, at {tops[:7]}; their heights {[round(means[t - 1], 1) for t in tops]}")
print(f"  the count's spread over the board (largest less smallest) at each top: {[seen[t - 1][1] for t in tops]}")
print(f"  the books on the board (the summed impulse moved by the summed kick less D times the summed count): exact at"
      f" {books} of {len(seen)} ticks; the run back through every swing: {exact}")


# (3) the reach on a chain ---------------------------------------------------------------------------------------------
def reach(gamma, length, ticks, m=100):
    """A chain (length, 1, 1): row 0 the time gear (W = Gamma / 2, s 1, D 1, a grip of W / 6 per Mesh), row 1 a held
    source m at the chain's first Node-clock. The count's mean over the ticks at each Node-clock, its decay per Mesh read
    between the 5th and the 30th, and the run back."""
    nb = board((length, 1, 1))
    n = nb.shape[1]
    w = gamma // 2
    plan = Plan(np.array([1], np.intp), np.array([1], np.intp), obj([1]), np.array([0], np.intp))
    gearing = Gearing(column(w, 1), column(w, 1), 1, column(1, 0), 1, column(1, 1))
    grip = obj(np.vstack([np.full((1, 3 * n), w // 6), np.zeros((1, 3 * n), int)]))
    layout = layout_of(nb, grip, gearing, plan, gamma)
    a = obj(np.zeros((1 + 1, n), int))
    a[1, 0] = m
    seen, exact = run(layout, at_rest(a, (w, 1)), ticks, lambda s: s.a[0].copy())
    mean = np.array([sum(int(v[x]) for v in seen) for x in range(n)], dtype=float) / ticks
    near, far = 5, 30
    kappa = (math.log(mean[near]) - math.log(mean[far])) / (far - near)
    return 1 / kappa, w // 6, exact, [int(v[0]) for v in seen]


gamma = 1200
lam, grip, exact, local = reach(gamma, 200, 3000)
tops, lows = turns(local)
print(f"(3) the reach on a chain (Gamma {gamma:,}, W {gamma // 2}, grip {grip} per Mesh, D 1; the count's mean over 3,000"
      f" ticks, about 19 swings):")
print(f"  the decay length {lam:.2f} Meshes; sqrt(grip / D) = {math.sqrt(grip):.2f} (the lattice's, from"
      f" 2 cosh(1 / L) - 2 = D / grip: {1 / math.acosh(1 + 1 / (2 * grip)):.2f}); sqrt(Gamma / 12) ="
      f" {math.sqrt(gamma / 12):.2f}; David's sqrt(Gamma / 6) = {math.sqrt(gamma / 6):.2f}; the run back: {exact}")
print(f"  the count's own wave speed sqrt(s grip / W) = {math.sqrt(grip / (gamma // 2)):.3f} Mesh per tick"
      f" (1 / sqrt 6 = {1 / math.sqrt(6):.3f}; light's 1 / sqrt 3 = {1 / math.sqrt(3):.3f}, Postulate 3); the swing's"
      f" period 2 pi sqrt(W / D) = {2 * math.pi * math.sqrt(gamma // 2):.1f} ticks reads D / W alone")
print(f"  a local bang: the count at the source's own Node-clock tops at {tops[:5]} ({[local[t - 1] for t in tops[:5]]})"
      f" and returns at {lows[:5]} ({[local[t - 1] for t in lows[:5]]}), its settled level {round(sum(local) / len(local))}")
