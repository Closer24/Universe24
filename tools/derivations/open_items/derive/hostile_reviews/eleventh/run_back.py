"""The run back of stage 7a's act: exact from the after state and the out alone, every divisor away from 1, W apart from W+.

Usage: PYTHONPATH=<worktree>/src:<worktree> python -P run_back.py
(a) one round, random masks and stopped clocks, every divisor row at least 2, W != W+, s, D, T_k parted, a random plan;
(b) rounds at one layout: W+ = W, W+ < W, W+ > W (the promise r < W broken from the second round);
(c) rounds re-geared each round, the next round's W the last round's W+, every clock ticking each round;
(d) a promise broken at the start: r = W, r < 0, r_d = T_d, r_d < 0, tn > c; T_d = 0 and T_d < 0.
"""

import numpy as np

from tensor24.engine import step
from tensor24.engine.state import Gearing, Layout, Plan, State
from tests.frame import board, meshes_of, wide

SHAPE, ROWS, TERMS, PLANES, GAMMA = (3, 4, 2), 3, 25, 5, 7


def draw(rng, low, high, size):
    return rng.integers(low, high, size=size).astype(object)


def layout_of(rng, wrel="parted", stopped=True):
    nb = board(SHAPE)
    n = nb.shape[1]
    w = draw(rng, 2, 40, (ROWS, n))
    wp = {"alike": w, "parted": draw(rng, 2, 40, (ROWS, n)), "less": np.maximum(w - draw(rng, 0, 3, (ROWS, n)), 2).astype(object), "more": w + draw(rng, 1, 5, (ROWS, n))}[wrel]
    stretch = draw(rng, 2, 6, (ROWS, n)) * (1 - 2 * draw(rng, 0, 2, (ROWS, n)))
    gearing = Gearing(w, wp, stretch, draw(rng, -4, 5, (ROWS, n)), draw(rng, 2, 6, (ROWS, n)), draw(rng, 2, 30, (ROWS, n)))
    index = [rng.integers(0, h, size=TERMS).astype(np.intp) for h in (PLANES * ROWS, PLANES * ROWS, ROWS)]
    plan = Plan(index[0], index[1], draw(rng, -9, 10, TERMS), index[2])
    rate = draw(rng, 0, GAMMA + 1, (1, n))
    if stopped:
        rate[0, :3] = 0
    return Layout(nb, meshes_of(nb), draw(rng, -4, 5, (ROWS, 3 * n)), gearing, plan, rate, GAMMA)


def world(rng, layout):
    _, _, _, gearing, _, _, _ = layout
    n = layout.nb.shape[1]
    size, one = (ROWS, n), (1, n)
    c = draw(rng, 0, 3, one)
    return State(
        wide(rng, size), wide(rng, size), draw(rng, 0, 1 << 40, size) % gearing.w, draw(rng, 0, 2, size),
        draw(rng, 0, 1 << 40, size) % gearing.drive, draw(rng, 0, GAMMA, one), c, c - draw(rng, 0, 2, one),
    )


def equal(s, t):
    return all(np.array_equal(x, y) for x, y in zip(s, t, strict=True))


def masks(rng, n, rounds):
    return [draw(rng, 0, 2, (1, n)) if rng.integers(0, 2) else np.ones((1, n), dtype=object) for _ in range(rounds)]


def one_round(seeds):
    good = ticked = 0
    for seed in range(seeds):
        rng = np.random.default_rng(seed)
        layout = layout_of(rng)
        s = world(rng, layout)
        now, out = step.tick(layout, s, masks(rng, layout.nb.shape[1], 1)[0])
        ticked += int(out.k.sum())
        good += equal(step.untick(layout, now, out), s)
    return f"(a) one round, divisors >= 2, W != W+: {good} of {seeds} exact, {ticked} Node-clocks ticked"


def rounds_at(wrel, seeds, rounds=8):
    good = 0
    for seed in range(seeds):
        rng = np.random.default_rng(100 + seed)
        layout = layout_of(rng, wrel)
        s0 = world(rng, layout)
        s, outs = s0, []
        for m in masks(rng, layout.nb.shape[1], rounds):
            s, o = step.tick(layout, s, m)
            outs.append(o)
        for o in reversed(outs):
            s = step.untick(layout, s, o)
        good += equal(s, s0)
    return f"(b) {rounds} rounds at one layout, W+ {wrel}: {good} of {seeds} run back exactly"


def regeared(seeds, rounds=6):
    good = 0
    for seed in range(seeds):
        rng = np.random.default_rng(200 + seed)
        layout = layout_of(rng, "parted", stopped=False)
        layout = layout._replace(rate=0 * layout.rate + GAMMA)  # every clock ticks every round
        s0 = world(rng, layout)
        s0 = s0._replace(c=0 * s0.c, tn=0 * s0.tn)
        s, outs, layouts = s0, [], []
        for _ in range(rounds):
            s, o = step.tick(layout, s, np.ones((1, layout.nb.shape[1]), dtype=object))
            outs.append(o)
            layouts.append(layout)
            g = layout.gearing
            layout = layout._replace(gearing=g._replace(w=g.wp, wp=draw(rng, 2, 40, g.wp.shape)))
        for lay, o in zip(reversed(layouts), reversed(outs), strict=True):
            s = step.untick(lay, s, o)
        good += equal(s, s0)
    return f"(c) {rounds} rounds re-geared, W of a round the W+ of the last: {good} of {seeds} run back exactly"


def broken(seeds):
    lines = []
    cases = {
        "r = W": lambda s, g: s._replace(r=0 * s.r + g.w),
        "r = -1": lambda s, g: s._replace(r=0 * s.r - 1),
        "r_d = T_d": lambda s, g: s._replace(rd=0 * s.rd + g.drive),
        "r_d = -1": lambda s, g: s._replace(rd=0 * s.rd - 1),
        "tn = c + 1": lambda s, g: s._replace(tn=s.c + 1),
    }
    for name, make in cases.items():
        good = raised = 0
        for seed in range(seeds):
            rng = np.random.default_rng(300 + seed)
            layout = layout_of(rng, stopped=False)
            s = make(world(rng, layout), layout.gearing)
            try:
                now, out = step.tick(layout, s, np.ones((1, layout.nb.shape[1]), dtype=object))
                good += equal(step.untick(layout, now, out), s)
            except ZeroDivisionError:
                raised += 1
        lines.append(f"(d) start with {name}: {good} of {seeds} run back exactly, {raised} raised")
    for name, teeth in (("T_d = 0", 0), ("T_d = -3", -3), ("W+ = 0", None)):
        rng = np.random.default_rng(7)
        layout = layout_of(rng, stopped=False)
        g = layout.gearing
        g = g._replace(wp=0 * g.wp) if teeth is None else g._replace(drive=0 * g.drive + teeth)
        layout = layout._replace(gearing=g)
        s = world(rng, layout._replace(gearing=g._replace(drive=0 * g.drive + 1)))
        try:
            now, out = step.tick(layout, s, np.ones((1, layout.nb.shape[1]), dtype=object))
            back = step.untick(layout, now, out)
            rd = now.rd[:, out.k[0] == 1]
            lines.append(f"(d) {name}: no raise; run back exact {equal(back, s)}; r_d+ range [{rd.min()}, {rd.max()}]")
        except ZeroDivisionError as e:
            lines.append(f"(d) {name}: raises ZeroDivisionError ({e})")
    return lines


import sys
if "broken" not in sys.argv:
    print(one_round(200))
for wrel in (() if "broken" in sys.argv else ("alike", "less", "more", "parted")):
    print(rounds_at(wrel, 60))
if "broken" not in sys.argv:
    print(regeared(60))
print("\n".join(broken(60)))
