"""The ladder on 7a's own act: an A1 train alone at the start drives a T2 train, which with the gradient drives an A2 train.

usage: python -I l2_ladder_on_the_act.py <tensor24 src>
The universe: a (A1, one gear), t (T2, three gears), p (A2, one gear), and two coupling rows through 7a's own load.plan
and tables: J_t = g1 C[T2; T1, T1](grad a, grad a), and J_p = g2 C[A2; T1, T2](grad a, t). Board 5 x 5 x 5, grips one per
Mesh, W = W+ = 6, s = 1, the drive's teeth 4 on t and p. Measured: the tick at which each kind first stands; the step
turned by each of the 24 equal to the turned step (every slot, fine tooth, going and drive's tooth, the negated rows by the
flip); and the run back to the start, bit for bit.
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import home  # noqa: E402
from tensor24.engine import kinds as K  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, State  # noqa: E402
from tensor24.runner import board as B  # noqa: E402
from tensor24.runner import load as L  # noqa: E402

GAMMA, SHAPE, W, TD, TICKS = 1000, (5, 5, 5), 6, 4, 12
obj = lambda x: np.asarray(x, dtype=object)  # noqa: E731
kinds, tables = main.made(SHAPE)
labels, dims = tuple(n.upper() for n in kinds._fields), tuple(k.shape[-1] for k in kinds)
universe_trains = [
    {"name": "a", "kinds": ["A1"], "part": 1},
    {"name": "t", "kinds": ["T2"], "part": 1},
    {"name": "p", "kinds": ["A2"], "part": 1},
]
trains, found = L.trains_of(universe_trains, labels, dims)
assert not found, found
VALUE, GRAD = 0, 1
couplings = [
    [0, 0, 0, GRAD, 0, 0, 0, GRAD, 1, 0, 0, 1],  # J_t = C[T2; T1, T1](grad a, grad a)
    [0, 0, 0, GRAD, 1, 0, 0, VALUE, 2, 0, 0, 1],  # J_p = C[A2; T1, T2](grad a, t)
]
plan, refused = L.plan(couplings, trains, tables, labels, 3)
assert not refused, refused
rows = sum(t.rows() for t in trains)
nb, meshes = B.board(SHAPE)
n = nb.shape[1]
col = lambda *v: obj(np.array(v).reshape(-1, 1))  # noqa: E731
gearing = Gearing(col(*[W] * rows), col(*[W] * rows), 1, col(0, 1, 1, 1, 1), 1, col(1, TD, TD, TD, TD))
layout = Layout(nb, meshes, obj(np.ones((rows, 3 * n), int)), gearing, plan, obj(np.full((1, n), GAMMA)), GAMMA)
teeth_w = np.array([W] * rows).reshape(-1, 1)
teeth_d = np.array([1, TD, TD, TD, TD]).reshape(-1, 1)
print(f"the plan: {len(plan[0])} terms (T1 x T1 -> T2 and T1 x T2 -> A2 through 7a's tables), refused: {refused}")


def start():
    a = obj(np.zeros((rows, n), int))
    x0 = B.site(2, 2, 2, SHAPE[1], SHAPE[2])
    a[0, x0] = 40
    for j in range(6):
        a[0, nb[j, x0]] = 20 + 3 * j  # a bump with no symmetry of its own, so every turn moves it
    zero = obj(np.zeros((rows, n), int))
    one = obj(np.zeros((1, n), int))
    return State(a, a.copy(), obj(np.full((rows, n), home(W, 0))), zero.copy(), zero.copy(), one, one.copy(), one.copy())


def run(s, ticks):
    states, outs = [s], []
    for _ in range(ticks):
        s, o = step.tick(layout, s, 1)
        states.append(s)
        outs.append(o)
    return states, outs


states, outs = run(start(), TICKS)
first = {}
for t, s in enumerate(states):
    for name, rr in (("A1 (a)", [0]), ("T2 (t)", [1, 2, 3]), ("A2 (p)", [4])):
        if name not in first and any(int(v) != 0 for v in np.asarray(s.a[rr]).ravel()):
            first[name] = t
print(f"the tick at which each train first stands off 0: {first}")
for t in (1, 2, 3, TICKS):
    s = states[t]
    print(f"  tick {t:>2}: the largest |a| {max(abs(int(v)) for v in s.a[0])}, |t| {max(abs(int(v)) for v in s.a[1:4].ravel())},"
          f" |p| {max(abs(int(v)) for v in s.a[4])}")

# the 24 on the state: sites by the turn about the board's origin, rows by each train's kind, negated rows flipped
matrix, weight = K.turns(K.axes(3))
held = K.kinds(matrix)
turn = [g for g in range(len(weight)) if weight[g] == 1]
coords = np.array(np.unravel_index(np.arange(n), SHAPE)).T


def turned(s, g):
    R = np.asarray(held.t1[g], dtype=int)
    sign = int(held.a2[g][0, 0])
    rho_rows = np.zeros((rows, rows), dtype=int)
    rho_rows[0, 0] = 1
    rho_rows[1:4, 1:4] = sign * R
    rho_rows[4, 4] = sign
    to = np.ravel_multi_index(tuple(((coords @ R.T) % np.array(SHAPE)).T), SHAPE)  # site x -> site R x
    out = [obj(np.zeros_like(np.asarray(f))) for f in s]
    for new in range(rows):
        old = int(np.flatnonzero(rho_rows[new])[0])
        sg = int(rho_rows[new, old])
        a, b, r, go, rd = (np.asarray(f)[old] for f in s[:5])
        if sg < 0:
            a, b, r, go, rd = -a, -b, teeth_w[old, 0] - 1 - r, 1 - go, teeth_d[old, 0] - 1 - rd
        for f, v in zip(out[:5], (a, b, r, go, rd), strict=True):
            f[new, to] = v
    for f, v in zip(out[5:], s[5:], strict=True):
        f[0, to] = np.asarray(v)[0]
    return State(*out)


def same(s, t):
    return all(np.array_equal(np.asarray(x), np.asarray(y)) for x, y in zip(s, t, strict=True))


alike = 0
for g in turn:
    other, _ = run(turned(start(), g), TICKS)
    alike += all(same(turned(states[t], g), other[t]) for t in range(TICKS + 1))
print(f"the 24: the run of the turned start equals the turned run at every tick and every slot, for {alike} of {len(turn)} turns")

s = states[-1]
for o in reversed(outs):
    s = step.untick(layout, s, o)
print(f"the run back over {TICKS} ticks returns the start bit for bit: {same(s, start())}")

# where the source first stands, against where the notch first moves (the drive's and the gear's carries keep the rest)
for t in range(4):
    _, j = step.sources(layout, states[t])
    jt = max(abs(int(v)) for v in np.asarray(j[1:4]).ravel())
    jp = max(abs(int(v)) for v in np.asarray(j[4]).ravel())
    print(f"  the sources read at the start of tick {t + 1}: the largest |J_t| {jt}, |J_p| {jp}")
