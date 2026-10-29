"""Stage 7a read independently (Animate): the one act against a model written from the plan's words, and its run back.

usage: python -I probe_7a.py <worktree at the head>   (run here at 9e5233d7f: probe_7a.txt)

The board, its six neighbours and its Meshes are made here (a Mesh numbered by its axis and its - end), not taken from
runner/board.py; the model is written site by site from the plan's 7a lines (#2187, 6484263257) and David's B
(6483927829): the due beat, the read as of the reader's count, F = the pull less D a, the readings (the value, the
centred difference along each axis as seen, F), J by the plan's terms, (q, r_d+) = carry(J + r_d at T_d), the push
s (F + T_k q), the impulse at W and the carry at W+ from their homes. Every coefficient is parted per gear and site.
"""

import sys
from pathlib import Path

import numpy as np

WT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(WT / "src"))
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Out, Plan, State  # noqa: E402

SHAPE = (3, 4, 5)
N = SHAPE[0] * SHAPE[1] * SHAPE[2]
ROWS, TERMS, PLANES, GAMMA = 4, 30, 5, 9
WIDE = 1 << 256


def board():
    """The six neighbours (+x, -x, +y, -y, +z, -z) on the torus, and each Spoke's Mesh: axis N + the - end's site."""
    nb = np.zeros((6, N), dtype=np.intp)
    for i in range(N):
        x = list(np.unravel_index(i, SHAPE))
        for axis in range(3):
            for d, sign in ((axis + axis, 1), (axis + axis + 1, -1)):
                y = list(x)
                y[axis] = (y[axis] + sign) % SHAPE[axis]
                nb[d, i] = np.ravel_multi_index(tuple(y), SHAPE)
    meshes = np.zeros((6, N), dtype=np.intp)
    for i in range(N):
        for axis in range(3):
            meshes[axis + axis, i] = axis * N + i
            meshes[axis + axis + 1, i] = axis * N + nb[axis + axis + 1, i]
    return nb, meshes


NB, MESHES = board()


def obj(x):
    return np.array(x, dtype=object)


def draw(rng, low, high, size):
    return obj(rng.integers(low, high, size=size).tolist())


def layout(rng, alike=False, fed=False):
    """A layout parted at every gear and site; fed: J read on rows 0 and 1 and landing on rows 2 and 3, no feedback."""
    w = draw(rng, 1, 20, (ROWS, N))
    gearing = Gearing(
        w,
        w if alike else draw(rng, 1, 20, (ROWS, N)),
        draw(rng, -3, 4, (ROWS, N)),  # s
        draw(rng, -3, 4, (ROWS, N)),  # D
        draw(rng, -5, 6, (ROWS, N)),  # T_k
        draw(rng, 1, 10, (ROWS, N)),  # T_d
    )
    if fed:
        read = [plane * ROWS + row for plane in range(PLANES) for row in (0, 1)]
        pick = lambda: np.array(rng.choice(read, TERMS), dtype=np.intp)  # noqa: E731
        plan = Plan(
            pick(), pick(), draw(rng, -9, 10, TERMS), rng.integers(2, ROWS, TERMS).astype(np.intp)
        )
    else:
        plan = Plan(
            rng.integers(0, PLANES * ROWS, TERMS).astype(np.intp),
            rng.integers(0, PLANES * ROWS, TERMS).astype(np.intp),
            draw(rng, -9, 10, TERMS),
            rng.integers(0, ROWS, TERMS).astype(np.intp),
        )
    grip = draw(rng, -3, 4, (ROWS, 3 * N))
    rate = draw(rng, 0, GAMMA + 1, (1, N))
    return Layout(NB, MESHES, grip, gearing, plan, rate, GAMMA)


def wide(rng, size):
    return obj(
        [
            [
                int(rng.integers(0, 1 << 62)) * int(rng.integers(0, 1 << 62)) ** 4 % WIDE - WIDE // 2
                for _ in range(size[1])
            ]
            for _ in range(size[0])
        ]
    )


def state(rng, lay):
    c = draw(rng, 0, 2, (1, N))
    w, td = lay.gearing.w, lay.gearing.drive
    r = obj([[int(rng.integers(0, 1 << 20)) % int(w[g, i]) for i in range(N)] for g in range(ROWS)])
    rd = obj([[int(rng.integers(0, 1 << 20)) % int(td[g, i]) for i in range(N)] for g in range(ROWS)])
    return State(
        wide(rng, (ROWS, N)),
        wide(rng, (ROWS, N)),
        r,
        draw(rng, 0, 2, (ROWS, N)),
        rd,
        draw(rng, 0, GAMMA, (1, N)),
        c,
        c - draw(rng, 0, 2, (1, N)),
    )


def model(lay, s, mask):
    """The act site by site from the plan's words, with Python integers and loops."""
    W, WP, S, D, TK, TD = (np.broadcast_to(x, (ROWS, N)).tolist() for x in lay.gearing)
    first, second, factor, target = (list(x) for x in lay.plan)
    grip = lay.grip.tolist()
    a, b, r, go, rd = (x.tolist() for x in s[:5])
    ph, c, tn = (x[0].tolist() for x in s[5:])
    rate, mask = lay.rate[0].tolist(), mask[0].tolist()
    na, nb_, nr, nrd = ([row[:] for row in x] for x in (a, b, r, rd))
    nph, nc, ntn, fire, k = ph[:], c[:], tn[:], [0] * N, [0] * N
    for i in range(N):
        around = [int(NB[d, i]) for d in range(6)]
        fire[i] = mask[i] * int(all(c[j] >= c[i] for j in around))
        if fire[i]:
            k[i], nph[i] = divmod(ph[i] + rate[i], GAMMA)
        nc[i] = c[i] + fire[i]
        seen = [[a[g][j] if c[i] >= tn[j] else b[g][j] for j in around] for g in range(ROWS)]
        force = [
            sum(grip[g][int(MESHES[d, i])] * (seen[g][d] - a[g][i]) for d in range(6))
            - D[g][i] * a[g][i]
            for g in range(ROWS)
        ]
        planes = [[a[g][i] for g in range(ROWS)]]
        planes += [
            [seen[g][axis + axis] - seen[g][axis + axis + 1] for g in range(ROWS)] for axis in range(3)
        ]
        planes += [force]
        readings = [x for plane in planes for x in plane]
        j = [0] * ROWS
        for t in range(TERMS):
            j[int(target[t])] += int(factor[t]) * readings[int(first[t])] * readings[int(second[t])]
        if k[i]:
            for g in range(ROWS):
                q, nrd[g][i] = divmod(j[g] + rd[g][i], TD[g][i])
                push = S[g][i] * (force[g] + TK[g][i] * q)
                p = W[g][i] * (a[g][i] - b[g][i]) + r[g][i] - (W[g][i] - go[g][i]) // 2
                v, nr[g][i] = divmod(p + push + (WP[g][i] - go[g][i]) // 2, WP[g][i])
                na[g][i], nb_[g][i] = a[g][i] + v, a[g][i]
            ntn[i] = nc[i]
    return State(obj(na), obj(nb_), obj(nr), s.go, obj(nrd), obj([nph]), obj([nc]), obj([ntn])), Out(
        obj([fire]), obj([k]), s.tn
    )


def same(x, y):
    return all(
        np.array_equal(np.asarray(p, dtype=object), np.asarray(q, dtype=object))
        for p, q in zip(x, y, strict=True)
    )


rng = np.random.default_rng(20261029)
agree, ticked, gears = 0, 0, 0
for _ in range(300):
    lay = layout(rng)
    s = state(rng, lay)
    mask = draw(rng, 0, 2, (1, N))
    got, out = step.tick(lay, s, mask)
    want, wout = model(lay, s, mask)
    agree += same(got, want) and same(out, wout)
    ticked += int(np.asarray(out.k, dtype=object).sum() > 0)
    gears += int(np.asarray(out.k, dtype=object).sum()) * ROWS
print(f"1. the act against the model from the plan's words: {agree} of 300 layouts equal at every entry")
print(
    f"   ({ticked} of 300 with a gear ticked, {gears} gear ticks; W and W+, s, D, T_k and T_d parted per gear and site)"
)

back, rounds_ticked = 0, 0
for seed in range(20):
    rng = np.random.default_rng(1000 + seed)
    lay = layout(rng, alike=True, fed=True)
    start = state(rng, lay)
    s, outs = start, []
    for _ in range(60):
        s, out = step.tick(lay, s, draw(rng, 0, 2, (1, N)))
        outs.append(out)
        rounds_ticked += int(np.asarray(out.k, dtype=object).sum() > 0)
    for out in reversed(outs):
        s = step.untick(lay, s, out)
    back += same(s, start)
print(
    f"2. the run back: {back} of 20 runs of 60 rounds return to their start bit for bit, gears across 2**256,"
)
print(
    f"   W = W+ per gear and site, T_d from 1 to 9, J read on two rows into the other two ({rounds_ticked} of 1200 rounds ticked)"
)
