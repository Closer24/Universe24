"""A small board for the probes, built from the engine's own records and run by tensor24.engine.step.tick."""
import numpy as np

from tensor24.engine import step
from tensor24.engine.state import Gearing, Layout, Plan, State
from tensor24.runner.board import board


def layout(shape, w, spring, grip, gamma=9, rate=None):
    """One gear row per site, W = W+ = w, s = 1, D = spring, T_k = 1, T_d = 1 (the force's path), no J, every grip alike."""
    nb, meshes = board(shape)
    n = nb.shape[1]
    ones = np.ones((1, n), dtype=object)
    none = np.zeros(0, dtype=np.intp)
    plan = Plan(none, none, none.astype(object), none)
    return Layout(nb, meshes, grip * np.ones((1, 3 * n), dtype=object),
                  Gearing(w * ones, w * ones, ones, spring * ones, ones, ones), plan,
                  (gamma if rate is None else rate) * ones, gamma)


def state(a, b, r):
    n = len(a)
    z = np.zeros((1, n), dtype=object)
    row = lambda x: np.array([list(x)], dtype=object)
    return State(row(a), row(b), row(r), z.copy(), z.copy(), z.copy(), z.copy(), z.copy())


def tick(lay, s):
    return step.tick(lay, s, 1)
