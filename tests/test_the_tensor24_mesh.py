"""Tensor24's Mesh: the due beat, the read as of the reader's count, the order, the rewind and the frame's six properties."""

import itertools

import numpy as np
import pytest

from tensor24.engine import mesh, step
from tensor24.engine.state import State
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tests.frame import (
    PROPERTIES,
    Engine,
    board,
    flat,
    holds,
    meshes_of,
    near,
    plain,
    same,
    undone_elsewhere,
    unseeded,
    wide,
)

SHAPE, T = (5, 5, 5), 10  # the board, and the count every Node-clock is run to
W, RATE, GAMMA = 7, 5, 9  # the teeth, the rate and the full rate where every site is alike


def varied(rng, stopped=True):
    """A layout parted at every site and Mesh: teeth 1 to 19, rates 0 to the full rate, a grip of either sign per Mesh."""
    nb, n = board(SHAPE), int(np.prod(SHAPE))
    w = rng.integers(1, 20, size=(1, n)).astype(object)
    rate = rng.integers(0, GAMMA + 1, size=(1, n)).astype(object)
    rate[0, 5] = 0 if stopped else rate[0, 5]
    return plain(nb, meshes_of(nb), rng.integers(-3, 4, size=3 * n).astype(object), w, rate, GAMMA)


def world(rng, shape, trains, w=W):
    """A state the tick may meet: gears of every bit across 2**256, teeth within w, goings, dials, counts, the times."""
    size, one = (trains, int(np.prod(shape))), (1, int(np.prod(shape)))

    def draw(low, high, rows):
        return rng.integers(low, high, size=rows).astype(object)

    c = draw(0, 2, one)
    tn = c - draw(0, 2, one)
    tooth = draw(0, 1 << 20, size) % w
    zero = draw(0, 1, size)  # the drive's fine tooth, within [0, T_d) at T_d = 1
    return State(
        wide(rng, size), wide(rng, size), tooth, draw(0, 2, size), zero, draw(0, GAMMA, one), c, tn
    )


def start(rng, layout):
    """The first state on a layout: two trains, every count and the now slots' times at 0."""
    w = layout.gearing.w
    n = w.shape[1]
    a, b = (rng.integers(-99, 99, size=(2, n)).astype(object) for _ in range(2))
    r = rng.integers(0, 1 << 20, size=(2, n)).astype(object) % w
    go, ph = (
        rng.integers(0, 2, size=(2, n)).astype(object),
        rng.integers(0, GAMMA, size=(1, n)).astype(object),
    )
    zero = np.zeros((1, n), dtype=object)
    return State(a, b, r, go, 0 * a, ph, zero, zero)


def parted(seed, stopped=True):
    """A varied layout and its first state, with the rng that draws the schedules."""
    rng = np.random.default_rng(seed)
    layout = varied(rng, stopped)
    return layout, start(rng, layout), rng


def until(layout, s, rng=None, limit=60 * T):
    """Rounds to the count T, every due beat or random masks; with the rounds whose counts part and the stale reads."""
    outs, parting, stale = [], 0, 0
    for _ in range(limit):
        if not (s.c < T).any():
            break
        bits = np.ones_like(s.c) if rng is None else rng.integers(0, 2, size=s.c.shape).astype(object)
        allowed = bits * (s.c < T)
        fire = mesh.due(s.c, layout.nb) * allowed
        parting += int((s.c != s.c[0, 0]).any())
        stale += int(((s.c[:, None, :] < s.tn[:, layout.nb]) * fire[:, None, :]).sum())
        s, out = rounds(step.tick, layout, s, [allowed])
        outs += out
    return s, outs, parting, stale


def order():
    """At two layouts, forty random schedules give the synchronous pass's state at equal counts, parting, stale reads."""
    for seed in (1, 4):
        layout, s, rng = parted(seed)
        reference = until(layout, s)[0]
        runs = [until(layout, s, rng) for _ in range(40)]
        if not all(same(end, reference) and parting and stale for end, _, parting, stale in runs):
            return False
    return True


def back():
    """Under a random schedule the rounds run back to the start, bit for bit."""
    layout, s, rng = parted(2)
    end, outs, _, _ = until(layout, s, rng)
    return same(rewind(step.untick, layout, end, outs), s)


def stopped():
    """A stopped clock's count keeps pace: every count reaches T, and the stopped clock's gears stand."""
    layout, s, _ = parted(3)
    end, _, _, _ = until(layout, s)
    return (end.c == T).all() and (end.a[:, 5] == s.a[:, 5]).all()


def naive(shape, s, layout, mask):
    """The tick site by site, with loops and plain integers, its neighbours and Meshes found from the coordinates."""
    _, _, (grip,), gearing, _, rate, gamma = layout
    a, b, r, go, rd, ph, c, tn = (x.tolist() for x in s)
    grip, (w,), (rate,), (mask,) = grip.tolist(), gearing.w.tolist(), rate.tolist(), mask.tolist()
    n = len(c[0])
    new = [[row[:] for row in x] for x in (a, b, r, go, rd, ph, c, tn)]
    fire, k, before = ([[0] * n] for _ in range(3))
    for x in itertools.product(*map(range, shape)):
        i, around = (
            np.ravel_multi_index(x, shape),
            [np.ravel_multi_index(y, shape) for y in near(x, shape)],
        )
        spokes = [axis * n + j for axis in range(3) for j in (i, around[axis + axis + 1])]
        fire[0][i] = mask[i] * int(all(c[0][j] >= c[0][i] for j in around))
        k[0][i], new[5][0][i] = divmod(ph[0][i] + rate[i], gamma) if fire[0][i] else (0, ph[0][i])
        new[6][0][i], before[0][i] = c[0][i] + fire[0][i], tn[0][i]
        if k[0][i]:
            for g in range(len(a)):
                seen = [a[g][j] if c[0][i] >= tn[0][j] else b[g][j] for j in around]
                pull = sum(grip[m] * (v - a[g][i]) for m, v in zip(spokes, seen, strict=True))
                home = (w[i] - go[g][i]) // 2
                q, new[2][g][i] = divmod(w[i] * (a[g][i] - b[g][i]) + r[g][i] - home + pull + home, w[i])
                new[0][g][i], new[1][g][i] = a[g][i] + q, a[g][i]
            new[7][0][i] = new[6][0][i]
    return State(*(np.array(x, dtype=object) for x in new)), tuple(
        np.array(x, dtype=object) for x in (fire, k, before)
    )


def masked():
    """At a varied layout under a random mask the tick equals the naive model at every entry, at three seeds."""
    for seed in range(3):
        rng = np.random.default_rng(10 + seed)
        layout = varied(rng, stopped=False)
        s, mask = (
            world(rng, SHAPE, 2, layout.gearing.w),
            rng.integers(0, 2, size=(1, layout.gearing.w.shape[1])).astype(object),
        )
        if not same(flat(step.tick(layout, s, mask)), flat(naive(SHAPE, s, layout, mask))):
            return False
    return True


def negated():
    """The tie rule on the tick: every gear negated, its tooth flipped and its going advanced, ticks to the negation."""
    for seed in range(3):
        rng = np.random.default_rng(20 + seed)
        layout = varied(rng, stopped=False)
        s, mask = (
            world(rng, SHAPE, 2, layout.gearing.w),
            rng.integers(0, 2, size=(1, layout.gearing.w.shape[1])).astype(object),
        )
        a, b, r, go, *rest = s
        (a1, b1, r1, go1, *rest1), out1 = step.tick(layout, s, mask)
        (a2, b2, r2, go2, *rest2), out2 = step.tick(
            layout, State(-a, -b, layout.gearing.w - 1 - r, 1 - go, *rest), mask
        )
        flipped = same([a2, b2, r2, go2], [-a1, -b1, layout.gearing.w - 1 - r1, 1 - go1])
        if not (flipped and same([*rest2, *out2], [*rest1, *out1])):
            return False
    return True


def alike(nb):
    """The layout alike at every site and Mesh, for the frame's properties."""
    ones = np.ones((1, nb.shape[1]), dtype=object)
    return plain(nb, meshes_of(nb), np.ones(3 * nb.shape[1], dtype=object), W * ones, RATE * ones, GAMMA)


def engine():
    """The tick on every due beat at a layout alike everywhere: its run back, its worlds and its naive model."""

    def model(shape, s):
        nb = board(shape)
        return naive(shape, s, alike(nb), np.ones((1, nb.shape[1]), dtype=object))

    return Engine(
        lambda nb, s: step.tick(alike(nb), s, 1),
        lambda nb, s, out: step.untick(alike(nb), s, out),
        world,
        model,
    )


def teeth(gearing, w):
    """The gearing with other teeth, W and W+ alike."""
    return gearing._replace(w=w, wp=w)


def mutants():
    """Broken copies of the engine, each with the law that must catch it: what it replaces in the step, and with what."""
    tick, untick, pull, gear = step.tick, step.untick, mesh.pull, step.gear
    calls = itertools.count()

    def now_only(layout, s):
        return ((s.a[:, layout.nb] - s.a[:, None, :]) * layout.grip[:, layout.meshes]).sum(axis=1)

    def counting(layout, s, allowed):
        return tick(layout, s, allowed * step.beat(s.ph, layout.rate, layout.gamma, 1)[0])

    def keep_b(layout, s, o):
        return untick(layout, s, o)._replace(b=s.b)

    first = lambda a: (np.arange(len(a)) == 0).astype(object)[:, None]  # noqa: E731
    return {
        "the read of the now slot alone": ("order", "pull", now_only),
        "the before slot kept by the run back": ("back", "untick", keep_b),
        "the beat that counts only its ticks": ("stopped", "tick", counting),
        "the mask ignored": ("masked", "tick", lambda layout, s, allowed: tick(layout, s, 1)),
        "the grip ignored": (
            "masked",
            "pull",
            lambda layout, s: pull(layout._replace(grip=0 * layout.grip + 1), s),
        ),
        "the grip squared": (
            "masked",
            "pull",
            lambda layout, s: pull(layout._replace(grip=layout.grip * layout.grip), s),
        ),
        "the +x neighbour's rate": (
            "masked",
            "tick",
            lambda layout, s, allowed: tick(
                layout._replace(rate=layout.rate[:, layout.nb[0]]), s, allowed
            ),
        ),
        "a far site's teeth": (
            "masked",
            "tick",
            lambda layout, s, allowed: tick(
                layout._replace(gearing=teeth(layout.gearing, layout.gearing.w[:, layout.nb[0]])),
                s,
                allowed,
            ),
        ),
        "a pull that is not odd": ("negated", "pull", lambda layout, s: pull(layout, s) + 1),
        "a pull two Meshes away": (
            "locality",
            "pull",
            lambda layout, s: pull(layout._replace(nb=layout.nb[:, layout.nb[0]]), s),
        ),
        "a counter": (
            "purity",
            "tick",
            lambda layout, s, allowed: tick(layout, s._replace(c=s.c + next(calls)), allowed),
        ),
        "train 0 singled out": ("rename", "gear", lambda a, *rest: gear(a + first(a), *rest)),
        "the +x Spoke weighted twice": (
            "images",
            "pull",
            lambda layout, s: pull(layout, s) + mesh.seen(s, layout.nb)[:, 0] - s[0],
        ),
        "the before slot dropped from the stride": (
            "formula",
            "gear",
            lambda a, b, *rest: gear(a, 0 * b, *rest),
        ),
        "the run back keeping the before slot": ("bijectivity", "untick", keep_b),
    }


def law(name):
    """The Mesh's own laws, and the frame's six properties on the tick at three seeds."""
    own = {"order": order, "back": back, "stopped": stopped, "masked": masked, "negated": negated}
    return own[name]() if name in own else all(holds(name, engine, SHAPE, seed) for seed in range(3))


@pytest.mark.parametrize("mutant", list(mutants()))
def test_each_law_of_the_mesh_holds_and_fails_on_its_mutant(mutant, monkeypatch):
    name, attribute, broken = mutants()[mutant]
    assert name in [*PROPERTIES, "order", "back", "stopped", "masked", "negated"]
    assert law(name)
    monkeypatch.setattr(step, attribute, broken)
    assert not law(name)


def test_a_world_is_answered_alike_in_fresh_interpreters_at_other_hash_seeds():
    assert unseeded(__name__, "engine", SHAPE)


def test_a_world_is_run_back_in_a_fresh_interpreter_that_never_stepped():
    assert undone_elsewhere(__name__, "engine", SHAPE, 0)
