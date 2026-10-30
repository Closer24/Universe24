"""The Mesh: what a Node-clock reads of its neighbours, and the Meshes' pull."""

import numpy as np

from tensor24.algebra.carry import Z
from tensor24.engine.state import Layout


def seen(a: Z, nb: Z) -> Z:
    """Each neighbour's gears at the now slot: every Node-clock steps in every round, so its now slot is the round's."""
    return a[:, nb]


def gripped(layout: Layout, a: Z) -> Z:
    """What the grips' read lands on every Spoke at every site: each read row's now counts at both ends of the Spoke's Mesh, so the Mesh's grip is the same from either end."""
    nb, _, _, _, _, _, _, stretch = layout
    first, factor, target = stretch
    here = a[first]
    landed = np.zeros(nb.shape, dtype=object)
    np.add.at(landed, target, factor[:, None] * (here + np.take_along_axis(here, nb[target], axis=1)))
    return landed


def pull(layout: Layout, a: Z) -> Z:
    """The Meshes' pull on every gear: its train's grip on each Spoke's Mesh, at rest and as the grips' read lands it, times the neighbour less its own now."""
    nb, _, meshes, grip, _, _, _, _ = layout
    return ((seen(a, nb) - a[:, None, :]) * (grip[:, meshes] + gripped(layout, a))).sum(axis=1)
