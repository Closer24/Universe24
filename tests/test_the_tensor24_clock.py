"""Tensor24's one clock: a gear's tick and the rate dial's beat run back exactly, each law failing on its mutant."""

from types import SimpleNamespace

import numpy as np
import pytest

from tensor24.algebra.carry import choose
from tensor24.engine import step


def clock(seed, gears=3):
    """A Node-clock's gears, its going and its dial, with a run of teeth counts and pushes, all whole numbers."""
    rng = np.random.default_rng(seed)
    w = rng.integers(1, 40, size=21).astype(object)
    a, b = (rng.integers(-500, 500, size=gears).astype(object) for _ in range(2))
    r = np.array([int(x) for x in rng.integers(0, 1 << 20, size=gears)], dtype=object) % w[0]
    go = rng.integers(0, 2, size=gears).astype(object)
    push = rng.integers(-3000, 3000, size=(20, gears)).astype(object)
    fire = rng.integers(0, 2, size=20).astype(object)
    return a, b, r, go, w, push, fire, int(rng.integers(0, 1000)), int(rng.integers(1, 1001))


def run(m, a, b, r, go, w, push, fire, ph, rate, gamma=1000):
    """Twenty beats forward and the same twenty back; the teeth count moves only where a gear ticks."""
    c, tb, tn, i, log = 0, 0, 0, 0, []
    start = (a, b, r, ph, c, tb, tn)
    for t in range(20):
        k, ph = m.beat(ph, rate, gamma, fire[t])
        c, log = c + fire[t], [*log, (k, tb)]
        ticked = m.gear(a, b, r, go, w[i], w[i + 1], push[t])
        a, b, r = (choose(k, x, y) for x, y in zip(ticked, (a, b, r), strict=True))
        tb, tn, i = *m.times(k, c, tb, tn), i + k
    for t in reversed(range(20)):
        (k, old_tb), i = log[t], i - log[t][0]
        back = m.ungear(a, b, r, go, w[i], w[i + 1], push[t])
        a, b, r = (choose(k, x, y) for x, y in zip(back, (a, b, r), strict=True))
        tb, tn = choose(k, old_tb, tb), choose(k, tb, tn)
        c, ph = c - fire[t], m.unbeat(k, ph, rate, gamma, fire[t])
    now = (a, b, r, ph, c, tb, tn)
    return all(
        np.array_equal(x, y) if isinstance(x, np.ndarray) else x == y
        for x, y in zip(now, start, strict=True)
    )


def rewind(m):
    """Twenty runs of twenty beats come back exactly, at random rates and fires."""
    return all(run(m, *clock(seed)) for seed in range(20))


def stopped(m):
    """A clock at rate 0 beats: its count advances, it never ticks, and its gears and slots stand."""
    *_, ph, _ = clock(7)
    k, ph2 = m.beat(ph, 0, 1000, 1)
    return k == 0 and ph2 == ph


def negated(m):
    """The tie rule at the tick: a gear negated, its tooth flipped and its going advanced, ticks to the negation."""
    for seed in range(20):
        a, b, r, go, w, push, *_ = clock(seed)
        a1, b1, r1 = m.gear(a, b, r, go, w[0], w[1], push[0])
        a2, b2, r2 = m.gear(-a, -b, w[0] - 1 - r, 1 - go, w[0], w[1], -push[0])
        if not (
            np.array_equal(a2, -a1) and np.array_equal(b2, -b1) and np.array_equal(r2, w[1] - 1 - r1)
        ):
            return False
    return True


def mutants():
    """One broken copy of the step per law."""
    return {
        "rewind": {"ungear": lambda a, b, r, go, w, wp, push: step.ungear(a, b, r, go, w, wp, 0 * push)},
        "stopped": {"beat": lambda ph, rate, gamma, fire: (fire, ph)},
        "negated": {"gear": lambda a, b, r, go, w, wp, push: step.gear(a, b, r, 0 * go, w, wp, push)},
    }


@pytest.mark.parametrize("name", ["rewind", "stopped", "negated"])
def test_each_law_of_one_clock_holds_and_fails_on_its_mutant(name):
    law = {"rewind": rewind, "stopped": stopped, "negated": negated}[name]
    assert law(step)
    assert not law(SimpleNamespace(**{**vars(step), **mutants()[name]}))
