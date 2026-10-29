"""The 24's images of stage 7a's full act (sources, drive, carry, beat), not of the sources alone.

Usage: PYTHONPATH=<worktree>/src:<worktree> python -P images_full_act.py
The board is the cube 3x3x3, four trains, A1 and A2, T1 and T2, coupled through the load's plan (the act test's), every
coefficient one per train (alike on its rows and sites), T_d > 1, W != W+. A turn moves the sites, turns a and b by the
kinds' signed permutation, and mirrors the fine teeth on the rows it negates: r -> W - 1 - r (W+ where it ticked, W where not),
go -> 1 - go, r_d -> T_d - 1 - r_d. Checked: tick(turned s) = turned tick(s), and the out moved; also with r_d unmirrored.
"""

import numpy as np

from tensor24.engine import step
from tensor24.engine.state import Gearing, Layout, Plan, State
from tensor24.main import made
from tensor24.runner.load import load
from tests.frame import board, meshes_of, stored, turns, wide
from tests.test_the_tensor24_act import COUPLINGS, CUBE, TRAINS

ks, c = made(CUBE)
held, found = load({"trains": TRAINS, "couplings": COUPLINGS}, {"gears": []}, int(np.prod(CUBE)), ks, c)
assert not found
plan = Plan(*held.plan)
nb = board(CUBE)
n, rows = nb.shape[1], 8
per_train = [0, 1, 2, 2, 2, 3, 3, 3]  # the train of each row: A1 and A2, then T1 (3) and T2 (3)


def per_row(values):
    return np.array([[values[t]] for t in per_train], dtype=object)


def run(seed, mirror_rd=True, gamma=5):
    rng = np.random.default_rng(seed)
    w, wp = per_row(rng.integers(2, 30, 4).tolist()), per_row(rng.integers(2, 30, 4).tolist())
    gearing = Gearing(
        w, wp, per_row(rng.integers(-4, 5, 4).tolist()), per_row(rng.integers(-3, 4, 4).tolist()),
        per_row(rng.integers(-4, 5, 4).tolist()), per_row(rng.integers(2, 12, 4).tolist()),
    )
    grip = per_row(rng.integers(-3, 4, 4).tolist()).repeat(3 * n, axis=1)
    rate = np.full((1, n), int(rng.integers(0, gamma + 1)), dtype=object)
    layout = Layout(nb, meshes_of(nb), grip, gearing, plan, rate, gamma)
    size, one = (rows, n), (1, n)
    cc = rng.integers(0, 2, one).astype(object)
    s = State(
        wide(rng, size) >> 200, wide(rng, size) >> 200,
        rng.integers(0, 1 << 30, size).astype(object) % w, rng.integers(0, 2, size).astype(object),
        rng.integers(0, 1 << 30, size).astype(object) % gearing.drive, rng.integers(0, gamma, one).astype(object),
        cc, cc - rng.integers(0, 2, one).astype(object),
    )
    mask = rng.integers(0, 2, one).astype(object)
    now, out = step.tick(layout, s, mask)
    xyz, sides = np.indices(CUBE).reshape(3, -1), np.array(CUBE)[:, None]
    good = 0
    for m in turns():
        site = np.ravel_multi_index(tuple((m @ xyz) % sides), CUBE)
        turn = stored(m)[:rows, :rows]
        neg = np.array([int(v) == -1 for v in turn.sum(axis=1)])[:, None]  # the rows it lands negated

        def turned(x, teeth=None, flip=None):
            y = np.empty_like(x)
            moved = turn @ x if x.shape[0] == rows else x
            if flip is not None:
                pos = np.abs(turn) @ x
                moved = np.where(neg, flip(np.abs(turn) @ np.broadcast_to(teeth, x.shape), pos), pos)
            y[:, site] = moved
            return y

        def state(z, teeth):
            mir = lambda t, v: t - 1 - v  # noqa: E731
            return State(
                turned(z.a), turned(z.b), turned(z.r, teeth, mir), turned(z.go, 1, lambda t, v: 1 - v),
                turned(z.rd, gearing.drive, mir) if mirror_rd else turned(z.rd, gearing.drive, lambda t, v: v),
                turned(z.ph), turned(z.c), turned(z.tn),
            )

        there, there_mask = state(s, w), turned(mask)
        now2, out2 = step.tick(layout, there, there_mask)
        want = state(now, np.where(np.broadcast_to(out.k, (rows, n)) == 1, np.broadcast_to(wp, (rows, n)), np.broadcast_to(w, (rows, n))))
        good += all(np.array_equal(x, y) for x, y in zip(now2, want, strict=True)) and all(
            np.array_equal(x, turned(y)) for x, y in zip(out2, out, strict=False)
        )
    return good, int(out.k.sum())


for mirror in (True, False):
    results = [run(seed, mirror) for seed in range(6)]
    print(f"r_d mirrored {mirror}: turns whose full act commutes, per world (of 24):", [g for g, _ in results], "ticked sites:", [k for _, k in results])
