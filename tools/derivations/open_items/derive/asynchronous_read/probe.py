"""Item (u), the asynchronous read: the order test under the past read and under lin, on the stage 3 engine.

The order test: forty random schedules, each run until every count stands at T, give the synchronous pass's state.
past: a neighbour's now slot where its tn is at most the reader's count c, else its before slot (the ruling's line 5).
lin: the same where tn <= c; else the straight line between the two slots by the local times, one carry by tn - tb.
usage: PYTHONPATH=src python3 tools/derivations/open_items/derive/asynchronous_read/probe.py
"""

import numpy as np

from tensor24.algebra.carry import carry, choose, nonneg
from tensor24.engine import step
from tensor24.engine.state import Layout, State

SIDE, T, GAMMA = 5, 10, 9


def board():
    xyz = np.indices((SIDE,) * 3).reshape(3, -1)
    steps = [sign * axis for axis in np.eye(3, dtype=int) for sign in (1, -1)]
    return np.stack([np.ravel_multi_index(tuple((xyz + s[:, None]) % SIDE), (SIDE,) * 3) for s in steps])


def parted(seed):
    rng, n = np.random.default_rng(seed), SIDE**3
    w, rate = (rng.integers(1, high, size=(1, n)).astype(object) for high in (20, GAMMA))
    rate[0, 5] = 0
    layout = Layout(board(), np.ones((6, n), dtype=object), w, rate, GAMMA)
    a, b = (rng.integers(-99, 99, size=(2, n)).astype(object) for _ in range(2))
    r = rng.integers(0, 1 << 20, size=(2, n)).astype(object) % w
    go, ph = rng.integers(0, 2, size=(2, n)).astype(object), rng.integers(0, GAMMA, size=(1, n)).astype(object)
    zero = np.zeros((1, n), dtype=object)
    return layout, State(a, b, r, go, ph, zero, zero - 1, zero), rng


def until(layout, s, rng=None):
    for _ in range(60 * T):
        if not (s.c < T).any():
            break
        bits = np.ones_like(s.c) if rng is None else rng.integers(0, 2, size=s.c.shape).astype(object)
        s, _ = step.tick(layout, s, bits * (s.c < T))
    return s


def lin_pull(layout, s):
    nb, grip, _, _, _ = layout
    a, b, _, _, _, c, tb, tn = s
    span = tn[:, nb] - tb[:, nb]
    line = b[:, nb] + carry((a[:, nb] - b[:, nb]) * (c[:, None, :] - tb[:, nb]), span, 0)[0]
    seen = choose(nonneg(c[:, None, :] - tn[:, nb]), a[:, nb], line)
    return ((seen - a[:, None, :]) * grip).sum(axis=1)


def trial():
    layout, s, rng = parted(1)
    reference = until(layout, s)
    return sum(all(np.array_equal(x, y) for x, y in zip(until(layout, s, rng), reference)) for _ in range(40))


print("past: the random schedules equal the synchronous pass in", trial(), "of 40")
step.pull = lin_pull
print("lin:  the random schedules equal the synchronous pass in", trial(), "of 40")
