"""Tensor24's Mesh: the due beat, the read as of the reader's count, the order, the rewind and the frame's six properties."""

import itertools

import numpy as np
import pytest

from tensor24.engine import mesh, step
from tensor24.engine.state import Layout, State
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tests.frame import PROPERTIES, Engine, board, holds, near, same, unseeded, wide

SHAPE, T = (5, 5, 5), 10  # the board, and the count every Node-clock is run to
W, RATE, GAMMA = 7, 5, 9  # the teeth, the rate and the full rate where every site is alike


def parted(seed, stopped=True):
    """Two trains on the board, the teeth and the rates parted and one clock stopped, every integer whole."""
    rng, n = np.random.default_rng(seed), int(np.prod(SHAPE))
    w, rate = (rng.integers(1, high, size=(1, n)).astype(object) for high in (20, GAMMA))
    rate[0, 5] = 0 if stopped else rate[0, 5]
    layout = Layout(board(SHAPE), np.ones((6, n), dtype=object), w, rate, GAMMA)
    a, b = (rng.integers(-99, 99, size=(2, n)).astype(object) for _ in range(2))
    r = rng.integers(0, 1 << 20, size=(2, n)).astype(object) % w
    go, ph = (
        rng.integers(0, 2, size=(2, n)).astype(object),
        rng.integers(0, GAMMA, size=(1, n)).astype(object),
    )
    zero = np.zeros((1, n), dtype=object)
    return layout, State(a, b, r, go, ph, zero, zero - 1, zero), rng


def until(layout, s, rng=None, limit=60 * T):
    """Rounds until every count stands at T, or the limit: every due beat (rng None), or random masks."""
    outs = []
    for _ in range(limit):
        if not (s.c < T).any():
            break
        bits = np.ones_like(s.c) if rng is None else rng.integers(0, 2, size=s.c.shape).astype(object)
        s, out = rounds(step.tick, layout, s, [bits * (s.c < T)])
        outs += out
    return s, outs


def order():
    """Forty random schedules give the synchronous pass's state at equal counts, rates parted, one clock stopped."""
    layout, s, rng = parted(1)
    reference, _ = until(layout, s)
    return all(same(until(layout, s, rng)[0], reference) for _ in range(40))


def back():
    """Under a random schedule the rounds run back to the start, bit for bit."""
    layout, s, rng = parted(2)
    end, outs = until(layout, s, rng)
    return same(rewind(step.untick, layout, end, outs), s)


def stopped():
    """A stopped clock's count keeps pace: every count reaches T, and the stopped clock's gears stand."""
    layout, s, _ = parted(3)
    end, _ = until(layout, s)
    return (end.c == T).all() and (end.a[:, 5] == s.a[:, 5]).all()


def world(rng, shape, trains):
    """A state the tick may meet: gears of every bit across 2**256, teeth within W, goings, dials, counts, times."""
    size, one = (trains, int(np.prod(shape))), (1, int(np.prod(shape)))

    def draw(low, high, rows):
        return rng.integers(low, high, size=rows).astype(object)

    a, b = wide(rng, size), wide(rng, size)
    c = draw(0, 2, one)
    tn = c - draw(0, 2, one)
    return State(
        a, b, draw(0, W, size), draw(0, 2, size), draw(0, GAMMA, one), c, tn - 1 - draw(0, 2, one), tn
    )


def naive(shape, s):
    """The tick site by site, with loops and plain integers, its neighbours found from the coordinates."""
    a, b, r, go, ph, c, tb, tn = (x.tolist() for x in s)
    new = [[row[:] for row in x] for x in (a, b, r, go, ph, c, tb, tn)]
    fire, k, before = ([[0] * len(c[0])] for _ in range(3))
    for x in itertools.product(*map(range, shape)):
        i, around = (
            np.ravel_multi_index(x, shape),
            [np.ravel_multi_index(y, shape) for y in near(x, shape)],
        )
        fire[0][i] = int(all(c[0][j] >= c[0][i] for j in around))
        k[0][i], new[4][0][i] = divmod(ph[0][i] + RATE, GAMMA) if fire[0][i] else (0, ph[0][i])
        new[5][0][i], before[0][i] = c[0][i] + fire[0][i], tb[0][i]
        if k[0][i]:
            for g in range(len(a)):
                pull = sum((a[g][j] if c[0][i] >= tn[0][j] else b[g][j]) - a[g][i] for j in around)
                p = W * (a[g][i] - b[g][i]) + r[g][i] - (W - go[g][i]) // 2
                q, new[2][g][i] = divmod(p + pull + (W - go[g][i]) // 2, W)
                new[0][g][i], new[1][g][i] = a[g][i] + q, a[g][i]
            new[6][0][i], new[7][0][i] = tn[0][i], new[5][0][i]
    return State(*(np.array(x, dtype=object) for x in new)), tuple(
        np.array(x, dtype=object) for x in (fire, k, before)
    )


def engine():
    """The tick on every due beat, at one layout alike at every site: its run back, its worlds and its naive model."""

    def layout(nb):
        return Layout(nb, np.ones(nb.shape, dtype=object), W, RATE, GAMMA)

    return Engine(
        lambda nb, s: step.tick(layout(nb), s, 1),
        lambda nb, s, out: step.untick(layout(nb), s, out),
        world,
        naive,
    )


def mutants():
    """One broken copy of the engine per law: what it replaces in the step, and with what."""
    tick, untick, pull, gear = step.tick, step.untick, mesh.pull, step.gear
    calls = itertools.count()

    def now_only(layout, s):
        return ((s.a[:, layout.nb] - s.a[:, None, :]) * layout.grip).sum(axis=1)

    def counting(layout, s, allowed):
        return tick(layout, s, allowed * step.beat(s.ph, layout.rate, layout.gamma, 1)[0])

    return {
        "order": ("pull", now_only),
        "back": ("untick", lambda layout, s, o: untick(layout, s, o)._replace(b=s.b)),
        "stopped": ("tick", counting),
        "locality": ("pull", lambda layout, s: pull(layout._replace(nb=layout.nb[:, layout.nb[0]]), s)),
        "purity": (
            "tick",
            lambda layout, s, allowed: tick(layout, s._replace(c=s.c + next(calls)), allowed),
        ),
        "rename": (
            "gear",
            lambda a, *rest: gear(a + (np.arange(len(a)) == 0).astype(object)[:, None], *rest),
        ),
        "images": ("pull", lambda layout, s: pull(layout, s) + mesh.seen(s, layout.nb)[:, 0] - s[0]),
        "formula": ("gear", lambda a, b, *rest: gear(a, 0 * b, *rest)),
        "bijectivity": ("untick", lambda layout, s, o: untick(layout, s, o)._replace(b=s.b)),
    }


def law(name):
    """The Mesh's own laws, and the frame's six properties on the tick at three seeds."""
    own = {"order": order, "back": back, "stopped": stopped}
    return own[name]() if name in own else all(holds(name, engine, SHAPE, seed) for seed in range(3))


@pytest.mark.parametrize("name", ["order", "back", "stopped", *PROPERTIES])
def test_each_law_of_the_mesh_holds_and_fails_on_its_mutant(name, monkeypatch):
    attribute, broken = mutants()[name]
    assert law(name)
    monkeypatch.setattr(step, attribute, broken)
    assert not law(name)


def test_a_world_is_answered_alike_in_fresh_interpreters_at_other_hash_seeds():
    assert unseeded(__name__, "engine", SHAPE)
