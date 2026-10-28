"""The Mesh: when a Node-clock's beat is due, and what it reads of its neighbours as of its own count."""

import numpy as np

from tensor24.algebra.carry import Z, choose, nonneg
from tensor24.engine.state import Layout, State


def due(c: Z, nb: Z) -> Z:
    """The beat is due where every neighbour stands at a count at least the Node-clock's own."""
    return np.prod(nonneg(c[:, nb] - c[:, None, :]), axis=1)


def seen(s: State, nb: Z) -> Z:
    """Each neighbour's gears as of the reader's count: the now slot written at or before it, else the before slot."""
    a, b, _, _, _, c, tn = s
    return choose(nonneg(c[:, None, :] - tn[:, nb]), a[:, nb], b[:, nb])


def pull(layout: Layout, s: State) -> Z:
    """The Meshes' pull on every gear: each Spoke's grip times its neighbour as seen less the gear's own now."""
    nb, meshes, grip, _, _, _ = layout
    a, _, _, _, _, _, _ = s
    return ((seen(s, nb) - a[:, None, :]) * grip[meshes]).sum(axis=1)
