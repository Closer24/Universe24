"""The horizon under 7b's gearing (6488192915): the ruler from one table, a hill read at 0, past the stopped load the last entry.

usage: python3 -I q2_horizon.py <tensor24 src> <engine-5.0 src>
  (1) the table at Gamma 1,000 and 1,200: the stopped load (where the mesh rate rounds to 0), the clock's last rate, the
      ruler's last entry, and the read by two whethers of the closed list (nonneg, choose) at counts from a hill to 10^6;
  (2) on a ring of 32 Node-clocks (Gamma 1,200), stage 7a's act in two passes per tick, the time gear first:
      - pass A: the time gear (W = 600, D = 1, the grip 100 per Mesh) under a held source at one Node-clock, released at a
        set tick, so that its count goes past the stopped load and returns;
      - pass B: a light gear at every Node-clock (massless, the grip T / 6 per Mesh, s = 2) whose W and W+ read the ruler at
        the time gear's before, now and after counts: W = Z_b + Z_n, W+ = Z_n + Z_+, Z(c) = T Y(c)^4 div Gamma^4 (T = 6,000);
      read: the ticks past the stopped load, the time gear's impulse there, the light's summed impulse at every tick, the
      light gear at the deep Node-clock (its W, its stride, its impulse), the hand-over W = last W+, and the run back.
"""
import sys

sys.path.insert(0, sys.argv[1])
sys.path.insert(1, sys.argv[2])
import numpy as np  # noqa: E402

from event_universe.core import rates  # noqa: E402
from tensor24.algebra.carry import choose, home, nonneg  # noqa: E402
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


def zeros(rows, n):
    return obj(np.zeros((rows, n), int))


def layout_of(nb, grip, gearing, plan, gamma):
    n = nb.shape[1]
    return Layout(nb, meshes_of(nb), grip, gearing, plan, obj(np.full((1, n), gamma)), gamma)


# (1) the table and its read ---------------------------------------------------------------------------------------
def table(gamma):
    stop = rates.stopped_load(gamma)
    return [rates.rate(gamma, -c) for c in range(stop)], stop


def read(tab, c):
    """Y at the count c: a hill read at 0, past the table's end its last entry; two whethers and two choices."""
    last = len(tab) - 1
    held = choose(nonneg(c), c, 0)
    index = choose(nonneg(last - held), held, last)
    return tab[index]


print("(1) the ruler's table, Y(c) = rate(-c) on the hills' side, to the stopped load:")
for gamma in (1000, 1200):
    tab, stop = table(gamma)
    print(f"  Gamma {gamma:,}: the stopped load {stop:,} (the mesh rate there {rates.mesh_rate(gamma, stop)}, one load before"
          f" {rates.mesh_rate(gamma, stop - 1)}; the rate there {rates.rate(gamma, stop)}, the clock's last rate"
          f" {rates.rate(gamma, stop - 1)}); the table's last entry Y({stop - 1:,}) = {tab[-1]:,}")
    counts = (-7, -1, 0, 1, 2, stop - 2, stop - 1, stop, stop + 1, 10_000, 10**6)
    print("    read at " + ", ".join(f"{c:,}: {read(tab, c):,}" for c in counts))

# (2) the ring, the count past the stopped load and back ------------------------------------------------------------
GAMMA = 1200
tab, stop = table(GAMMA)
T = 6000
G4 = GAMMA**4
Z = [T * y**4 // G4 for y in tab]
print(f"  Z(0) = {Z[0]:,} = T; Z at the table's end {Z[-1]:,} ({Z[-1] // Z[0]:,} times its rest)")


def zed(c):
    last = len(Z) - 1
    held = choose(nonneg(c), c, 0)
    return Z[choose(nonneg(last - held), held, last)]


shape = (32, 1, 1)
nb = board(shape)
n = nb.shape[1]
deep = 16
wt, Dt, gt = GAMMA // 2, 1, GAMMA // 12
# pass A: row 0 the time gear, row 1 the held source (its value S at the deep Node-clock), row 2 the unit
planA = Plan(np.array([1], np.intp), np.array([2], np.intp), obj([1]), np.array([0], np.intp))  # J_0 = S 1
gripA = obj(np.vstack([np.full((1, 3 * n), gt), np.zeros((2, 3 * n), int)]))
gearA = Gearing(obj([[wt], [1], [1]]), obj([[wt], [1], [1]]), 1, obj([[Dt], [0], [0]]), 1, obj([[1], [1], [1]]))
layA = layout_of(nb, gripA, gearA, planA, GAMMA)
# pass B: row 0 the light, massless, the grip T / 6 per Mesh, s = 2; every gear turning 3 notches a tick at the start
planB = Plan(np.zeros(0, np.intp), np.zeros(0, np.intp), obj(np.zeros(0, int)), np.zeros(0, np.intp))
gripB = obj(np.full((1, 3 * n), T // 6))


def with_source(st, value):
    a, b = st.a.copy(), st.b.copy()
    a[1, deep] = value
    b[1, deep] = value
    return State(a, b, *st[2:])


def ring(schedule, label):
    """schedule[t] is the held source at the deep Node-clock during tick t, set between ticks and logged."""
    ticks = len(schedule)
    aA = obj(np.vstack([np.zeros((1, n), int), np.zeros((1, n), int), np.ones((1, n), int)]))
    sA = State(aA, aA.copy(), obj(np.vstack([np.full((1, n), home(wt, 0)), np.zeros((2, n), int)])), zeros(3, n),
               zeros(3, n), zeros(1, n), zeros(1, n), zeros(1, n))
    aB = obj(np.full((1, n), 3))
    sB = State(aB, zeros(1, n), obj(np.full((1, n), home(2 * T, 0))), zeros(1, n), zeros(1, n), zeros(1, n),
               zeros(1, n), zeros(1, n))
    startA, startB = sA, sB
    logs, past, imp_moves, light_sum, deep_light, handover, last_wp = [], [], [], set(), [], True, None
    for t in range(ticks):
        sA = with_source(sA, schedule[t])
        cb, cn = sA.b[0], sA.a[0]
        sA1, outA = step.tick(layA, sA, 1)
        cp = sA1.a[0]
        w = obj([[zed(int(x)) + zed(int(y)) for x, y in zip(cb, cn)]])
        wp = obj([[zed(int(x)) + zed(int(y)) for x, y in zip(cn, cp)]])
        if last_wp is not None and not np.array_equal(w, last_wp):
            handover = False
        last_wp = wp
        layB = layout_of(nb, gripB, Gearing(w, wp, 2, zeros(1, 1), 1, obj([[1]])), planB, GAMMA)
        sB1, outB = step.tick(layB, sB, 1)
        p_after = wp * (sB1.a - sB1.b) + (sB1.r - home(wp, sB1.go))
        logs.append((outA, layB, outB))
        light_sum.add(int(p_after.sum()))
        c_deep = int(cn[deep])
        if c_deep >= stop:
            past.append(t)
            pa = lambda x: int(wt * (x.a[0, deep] - x.b[0, deep]) + (x.r[0, deep] - home(wt, x.go[0, deep])))  # noqa: E731
            imp_moves.append(pa(sA1) - pa(sA))
        deep_light.append((t, c_deep, int(w[0, deep]), int(sB1.a[0, deep] - sB1.b[0, deep]), int(p_after[0, deep])))
        sA, sB = sA1, sB1
    path = [d[1] for d in deep_light]
    print(f"  {label}:")
    print(f"    the deep count's largest {max(path):,} at tick {path.index(max(path))}, its smallest {min(path):,};"
          f" past the stopped load {stop:,} at {len(past)} ticks" + (f", from {past[0]} to {past[-1]}" if past else ""))
    if past:
        print(f"    the time gear on its own teeth (W = {wt}, never read from the ruler): its count leaves the stopped load"
              f" for the last time at tick {past[-1] + 1} and reads {path[-1]:,} at the end; its impulse moved at"
              f" {sum(1 for x in imp_moves if x != 0)} of the {len(past)} ticks past the stopped load")
    print(f"    the light's summed impulse: one value at every tick: {len(light_sum) == 1} ({sorted(light_sum)[0]:,});"
          f" the hand-over W = last W+ at every tick and Node-clock: {handover}")
    picks = sorted(set([0, past[0] if past else 0, (past[0] + past[-1]) // 2 if past else 0, past[-1] if past else 0,
                        ticks - 1]))
    print("    the light at the deep Node-clock (tick, count, W, stride, impulse):")
    for t in picks:
        r = deep_light[t]
        print(f"      {r[0]:>5}  {r[1]:>7,}  {r[2]:>15,}  {r[3]:>10,}  {r[4]:>18,}")
    deep_ticks = [d for d in deep_light if d[1] >= stop]
    stood = [d for d in deep_ticks if d[3] == 0]
    if deep_ticks:
        print(f"    past the stopped load its stride reads 0 at {len(stood)} of {len(deep_ticks)} ticks, and its impulse is"
              f" never 0 there: {all(d[4] != 0 for d in deep_ticks)} (from {min(abs(d[4]) for d in deep_ticks):,}"
              f" to {max(abs(d[4]) for d in deep_ticks):,})")
    after = [abs(d[3]) for d in deep_light if past and d[0] > past[-1]]
    if after:
        print(f"    after the last tick past the stopped load, the deep light's largest stride {max(after):,} notches a tick")
    for i in reversed(range(ticks)):
        outA, layB, outB = logs[i]
        sB = step.untick(layB, sB, outB)
        sA = step.untick(layA, sA, outA)
        sA = with_source(sA, schedule[i - 1] if i else 0)
    ok = all(np.array_equal(x, y) for x, y in zip(sA, startA)) and all(np.array_equal(x, y) for x, y in zip(sB, startB))
    print(f"    the run back through {ticks} ticks, every change of the source restored: exact {ok}")


print("(2) a ring of 32 Node-clocks at Gamma 1,200: the time gear first, then a light gear whose W and W+ read the ruler:")
S = 160_000
ring([S] * 400 + [0] * 500, f"a held source of {S:,} a tick at Node-clock 16, set at tick 0 and taken away at tick 400")
ramp = [S * t // 900 for t in range(900)] + [S] * 600 + [S * (900 - t) // 900 for t in range(900)] + [0] * 600
ring(ramp, f"the same source raised over 900 ticks, held for 600, lowered over 900, then 600 ticks free")
