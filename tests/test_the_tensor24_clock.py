"""Tensor24's one clock: a gear's tick and the rate dial's beat run back exactly, each law failing on its mutant."""

import itertools
import math
from types import SimpleNamespace

import numpy as np
import pytest

from tensor24.algebra.carry import choose, home
from tensor24.engine import step
from tests.frame import same, wide

SIZES = (40, 1 << 80)  # the teeth's bound: a few teeth, and teeth and a full rate of about 2**80


def clock(seed, size):
    """A Node-clock's gears, its going and its dial, with a run of teeth counts and pushes, below size and its powers."""
    rng = np.random.default_rng(seed)

    def draw(low, high, shape=1):
        return wide(rng, shape) % (high - low) + low

    w, gamma = draw(1, size, 21), int(draw(1, size * size)[0])
    a, b = (draw(-size * size, size * size, 3) for _ in range(2))
    r, go, push = draw(0, size, 3) % w[0], draw(0, 2, 3), draw(-(size**3), size**3, (20, 3))
    return (
        a,
        b,
        r,
        go,
        w,
        push,
        draw(0, 2, 20),
        int(draw(0, gamma)[0]),
        int(draw(0, gamma + 1)[0]),
        gamma,
    )


def run(m, a, b, r, go, w, push, fire, ph, rate, gamma):
    """Twenty beats forward and the same twenty back; the teeth count moves only where a gear ticks."""
    c, tn, i, log = 0, 0, 0, []
    start = (a, b, r, ph, c, tn)
    for t in range(20):
        k, ph = m.beat(ph, rate, gamma, fire[t])
        c, log = c + fire[t], [*log, (k, tn)]
        ticked = m.gear(a, b, r, go, w[i], w[i + 1], push[t])
        a, b, r = (choose(k, x, y) for x, y in zip(ticked, (a, b, r), strict=True))
        tn, i = choose(k, c, tn), i + k
    for t in reversed(range(20)):
        (k, tn), i = log[t], i - log[t][0]
        back = m.ungear(a, b, r, go, w[i], w[i + 1], push[t])
        a, b, r = (choose(k, x, y) for x, y in zip(back, (a, b, r), strict=True))
        c, ph = c - fire[t], m.unbeat(k, ph, rate, gamma, fire[t])
    now = (a, b, r, ph, c, tn)
    return all(
        np.array_equal(x, y) if isinstance(x, np.ndarray) else x == y
        for x, y in zip(now, start, strict=True)
    )


def rewind(m):
    """Twenty runs of twenty beats come back exactly, at random rates and fires, at every size."""
    return all(run(m, *clock(seed, size)) for size, seed in itertools.product(SIZES, range(20)))


def stopped(m):
    """A clock at rate 0 beats: its count advances, it never ticks, and its dial stands, at every size."""
    return all(
        m.beat(ph, 0, gamma, 1) == (0, ph) for *_, ph, _, gamma in (clock(7, size) for size in SIZES)
    )


def negated(m):
    """The tie rule at the tick: a gear negated, its tooth flipped and its going advanced, ticks to the negation."""
    for size, seed in itertools.product(SIZES, range(20)):
        a, b, r, go, w, push, *_ = clock(seed, size)
        a1, b1, r1 = m.gear(a, b, r, go, w[0], w[1], push[0])
        a2, b2, r2 = m.gear(-a, -b, w[0] - 1 - r, 1 - go, w[0], w[1], -push[0])
        if not same([a2, b2, r2], [-a1, -b1, w[1] - 1 - r1]):
            return False
    return True


def both_ways(m):
    """The run back undone: every now, its tooth within the teeth it was carried at, is the tick of its run back."""
    for size, seed in itertools.product(SIZES, range(20)):
        a, b, r, go, w, push, *_ = clock(seed, size)
        if not same(
            m.gear(*m.ungear(a, b, r, go, w[1], w[0], push[0]), go, w[1], w[0], push[0]), [a, b, r]
        ):
            return False
    return True


def mutants():
    """Broken copies of the step, each with the law that must catch it: what it replaces, and with what."""

    def doubled(*x):
        a, b, r = step.gear(*x)
        return a + a, b, r

    def floated(a, b, r, go, w, wp, push):
        n = w * (a - b) + (r - home(w, go)) + push + home(wp, go)
        q = np.array([math.floor(x / wp) for x in n], dtype=object)
        return a + q, a, n - q * wp

    return {
        "the run back blind to the push": (
            "rewind",
            {"ungear": lambda a, b, r, go, w, wp, push: step.ungear(a, b, r, go, w, wp, 0 * push)},
        ),
        "a stopped beat that ticks": ("stopped", {"beat": lambda ph, rate, gamma, fire: (fire, ph)}),
        "the going ignored": (
            "negated",
            {"gear": lambda a, b, r, go, w, wp, push: step.gear(a, b, r, 0 * go, w, wp, push)},
        ),
        "the now slot doubled, and halved by the run back": (
            "both ways",
            {"gear": doubled, "ungear": lambda a, *rest: step.ungear(a // 2, *rest)},
        ),
        "the quotient through a float": ("both ways", {"gear": floated}),
    }


@pytest.mark.parametrize("mutant", list(mutants()))
def test_each_law_of_one_clock_holds_and_fails_on_its_mutant(mutant):
    name, broken = mutants()[mutant]
    law = {"rewind": rewind, "stopped": stopped, "negated": negated, "both ways": both_ways}[name]
    assert law(step)
    assert not law(SimpleNamespace(**{**vars(step), **broken}))
