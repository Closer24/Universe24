"""Shared helpers for draft D1's probes: worlds on the 7a act, read with the engine's own functions, exact integers only."""

import numpy as np

from tensor24.engine import step
from tensor24.engine.mesh import pull
from tensor24.engine.state import Gearing, Layout, Plan, State
from tensor24.runner.board import board


def ints(rng, low, high, size):
    """Python integers in [low, high) as an object array."""
    return rng.integers(low, high, size=size).astype(object)


def empty_plan():
    none = np.zeros(0, dtype=np.intp)
    return Plan(none, none, none.astype(object), none)


def layout_of(shape, w, s, d, tk, td, grip, plan, gamma=5):
    """A synchronous layout at the full rate: every Node-clock beats every round (rate = Gamma, so k = 1)."""
    nb, meshes = board(shape)
    n = nb.shape[1]
    rate = np.full((1, n), gamma, dtype=object)
    return Layout(nb, meshes, grip, Gearing(w, w, s, d, tk, td), plan, rate, gamma)


def state_of(a, b, r, rd):
    """Counts, times and dials all 0: the reads are the now slots, the beat fires everywhere."""
    rows, n = a.shape
    zero = np.zeros((1, n), dtype=object)
    return State(a, b, r, np.zeros((rows, n), dtype=object), rd, zero.copy(), zero.copy(), zero.copy())


def stiffness(layout, x):
    """K x = D x - pull(x): the spring less the Meshes' pull, read on the field x (as the engine's pull reads a)."""
    _, _, _, gearing, _, _, _ = layout
    n = x.shape[1]
    zero = np.zeros((1, n), dtype=object)
    probe = State(x, x, x * 0, x * 0, x * 0, zero, zero, zero)
    return gearing.spring * x - pull(layout, probe)


def wind(layout, a, b):
    """The wind E(a, b) = sum W (a - b)^2 + s a . K b, per gear row (the rows' sums), exact integers."""
    w, s = layout.gearing.w, layout.gearing.stretch
    e = w * (a - b) * (a - b) + s * a * stiffness(layout, b)
    return e.sum(axis=1)


def act(layout, s):
    """One round of the engine's own tick, with the readings the identities need: q, the push and the state after."""
    force, j = step.sources(layout, s)
    q, kept = step.drive(j, layout.gearing.drive, s.rd)
    push = step.driven(layout.gearing, force, q)
    allowed = np.ones((1, s.a.shape[1]), dtype=object)
    now, out = step.tick(layout, s, allowed)
    return now, out, j, q, push
