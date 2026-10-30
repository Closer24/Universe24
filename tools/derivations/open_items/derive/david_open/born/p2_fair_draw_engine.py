"""The fair draw read on stage 7a's own act: the draw's number from the board's fine teeth, flat and uncorrelated?

usage: python3 -I p2_fair_draw_engine.py <tensor24 worktree>/src
A (6, 6, 6) board at the example universe's integers (den 15,162,856,759,112,389, Gamma 1,000, G 16, T = 6 den Gamma^2
G^2): the time gear (row 0, W = W+ = T, s = 1, grip T / 6, the spring of the pair (den - den div Gamma, den)) and light
(rows 1 and 2, Gaussian, W = W+ = 2 T, s = 2, grip den Gamma^2 G^2, no spring), every clock at the full rate. Each
Node-clock's draw number at each beat is d = (c + V) mod L, c its beat count and V the sum of the A1 rows' fine teeth
over it and its six neighbours, read two ways: (raw) the fine teeth as they stand; (pitch) each row's fine tooth
in units of its pitch g, the gcd of its W and its push's coefficients (s grip and s D) read once at load, the digit
r div g, as the head's vernier read it (fine div F). Read after a burn-in: the tenths, the first half, and the halves of adjacent draws
(two Node-clocks one Mesh apart at one beat; one Node-clock at two beats in a row), for several L. Two settings: every
fine tooth laid at its home (all alike at the start), and the fine teeth laid at random.
"""
import sys

sys.path.insert(0, sys.argv[1])
import numpy as np  # noqa: E402

from tensor24.algebra.carry import home  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, State  # noqa: E402

DEN, GAMMA, G = 15162856759112389, 1000, 16
T = 6 * DEN * GAMMA**2 * G**2
SHAPE = (6, 6, 6)


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


def col(values):
    return obj(np.array(values, dtype=object).reshape(-1, 1))


import math

PINION = DEN - DEN // GAMMA
PITCH = [math.gcd(math.gcd(T // 6, 12 * (DEN - PINION) * G**2 * GAMMA**2), T),
         math.gcd(2 * DEN * GAMMA**2 * G**2, 2 * T), math.gcd(2 * DEN * GAMMA**2 * G**2, 2 * T)]


def run(seed, laid_at_home, ticks=400, pitch=False):
    rng = np.random.default_rng(seed)
    nb = board(SHAPE)
    n = nb.shape[1]
    pinion = DEN - DEN // GAMMA
    w = col([T, 2 * T, 2 * T])
    s = col([1, 2, 2])
    spring = col([12 * (DEN - pinion) * G**2 * GAMMA**2, 0, 0])
    grip = obj(np.array([[T // 6] * 3 * n, [DEN * GAMMA**2 * G**2] * 3 * n, [DEN * GAMMA**2 * G**2] * 3 * n], dtype=object))
    none = np.zeros(0, dtype=np.intp)
    plan = Plan(none, none, none.astype(object), none)
    layout = Layout(nb, meshes_of(nb), grip, Gearing(w, w, s, spring, col([1, 1, 1]), col([1, 1, 1])), plan,
                    obj(np.full((1, n), GAMMA)), GAMMA)
    a = obj(rng.integers(-40, 41, (3, n)))
    b = a - obj(rng.integers(-3, 4, (3, n)))
    go = obj(np.zeros((3, n), int))
    if laid_at_home:
        r = home(w, go) + 0 * a
    else:
        r = obj(np.array([[int(rng.integers(0, 2**62)) * int(rng.integers(0, 2**62)) % int(wr) for _ in range(n)]
                          for wr in (T, 2 * T, 2 * T)], dtype=object))
    zero = obj(np.zeros((1, n), int))
    st = State(a, b, r, go, obj(np.zeros((3, n), int)), zero, zero, zero)
    allowed = obj(np.ones((1, n), int))
    records = []
    for _ in range(ticks):
        c = st.c[0]
        if pitch:
            fine = sum(st.r[i] // PITCH[i] for i in range(3))  # each row's digit on its own pitch
        else:
            fine = st.r.sum(axis=0)  # the A1 rows' fine teeth at each Node-clock
        v = fine + fine[nb].sum(axis=0)  # with its six neighbours': the multiset's sum, the 24's invariant
        records.append((c.copy(), v.copy()))
        st, _ = step.tick(layout, st, allowed)
    return nb, records


def read(nb, records, L, burn=50):
    tenths = [0] * 10
    first = total = 0
    space_same = space_n = 0
    time_same = time_n = 0
    xs, ys, ts, nx = [], [], [], []
    prev = None
    for t, (c, v) in enumerate(records):
        d = [int((int(ci) + int(vi)) % L) for ci, vi in zip(c, v)]
        if t >= burn:
            for x in d:
                tenths[10 * x // L] += 1
                first += 2 * x < L
                total += 1
            for x in range(len(d)):
                y = int(nb[0, x])  # the +x neighbour, one Mesh apart
                space_same += (2 * d[x] < L) == (2 * d[y] < L)
                space_n += 1
                xs.append(d[x] / L)
                ys.append(d[y] / L)
            if prev is not None:
                for x in range(len(d)):
                    time_same += (2 * d[x] < L) == (2 * prev[x] < L)
                    time_n += 1
                    ts.append(prev[x] / L)
                    nx.append(d[x] / L)
        prev = d
    corr_s = float(np.corrcoef(xs, ys)[0, 1])
    corr_t = float(np.corrcoef(ts, nx)[0, 1])
    per = [sum(1 for x in range(L) if 10 * x // L == j) for j in range(10)]  # the values each tenth holds
    chi = sum((k - total * q / L) ** 2 / (total * q / L) for k, q in zip(tenths, per)) if L >= 10 else float("nan")
    return tenths, first, total, space_same, space_n, corr_s, time_same, time_n, corr_t, chi


print(f"the pitches: the time gear {PITCH[0]} (2^14 5^6), light {PITCH[1]} (T / 3, a base of 6)")
for pitch in (False, True):
  for laid, name in ((True, "every fine tooth laid at its home"), (False, "the fine teeth laid at random")):
    nb, records = run(7, laid, pitch=pitch)
    print(f"{'pitch' if pitch else 'raw'}, {name}: (6, 6, 6), 400 beats, read from beat 50 on, 216 Node-clocks:")
    for L in (2, 3, 10, 97, 1000, 4060, 16384, 1048583):
        tenths, first, total, ss, sn, cs, ts, tn, ct, chi = read(nb, records, L)
        tline = f" tenths {tenths}, chi-square {chi:.1f} on 9," if L >= 10 else ""
        print(f"  L {L}:{tline} first half {first} of {total}; one Mesh apart in one half {ss} of {sn} "
              f"(corr {cs:+.3f}); one Node-clock at two beats in one half {ts} of {tn} (corr {ct:+.3f})")


# the run back: the draws read again on the way back equal the draws of the way out, since each is a reading of the
# state at its beat and the rewind restores every state exactly
def rewind_check(seed=5, ticks=120, L=4060):
    rng = np.random.default_rng(seed)
    nb = board(SHAPE)
    n = nb.shape[1]
    w = col([T, 2 * T, 2 * T])
    s_ = col([1, 2, 2])
    spring = col([12 * (DEN - PINION) * G**2 * GAMMA**2, 0, 0])
    grip = obj(np.array([[T // 6] * 3 * n, [DEN * GAMMA**2 * G**2] * 3 * n, [DEN * GAMMA**2 * G**2] * 3 * n], dtype=object))
    none = np.zeros(0, dtype=np.intp)
    layout = Layout(nb, meshes_of(nb), grip, Gearing(w, w, s_, spring, col([1, 1, 1]), col([1, 1, 1])),
                    Plan(none, none, none.astype(object), none), obj(np.full((1, n), GAMMA)), GAMMA)
    a = obj(rng.integers(-40, 41, (3, n)))
    go = obj(np.zeros((3, n), int))
    zero = obj(np.zeros((1, n), int))
    st = State(a, a - obj(rng.integers(-3, 4, (3, n))), home(w, go) + 0 * a, go, obj(np.zeros((3, n), int)), zero, zero, zero)
    allowed = obj(np.ones((1, n), int))

    def draws(x):
        fine = sum(x.r[i] // PITCH[i] for i in range(3))
        return [int((int(c) + int(v)) % L) for c, v in zip(x.c[0], fine + fine[nb].sum(axis=0))]

    out, outs = [], []
    for _ in range(ticks):
        out.append(draws(st))
        st, o = step.tick(layout, st, allowed)
        outs.append(o)
    back = []
    for o in reversed(outs):
        st = step.untick(layout, st, o)
        back.append(draws(st))
    return out == back[::-1]


print(f"the run back: the draws read on the way back equal the way out's at every beat and Node-clock: {rewind_check()}")
