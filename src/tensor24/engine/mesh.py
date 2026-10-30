"""Clock: each neighbour tugs a gear toward its own count through their Mesh.
Algebra: F is the sum over the six Spokes of grip (neighbour - own); a Mesh's grip is its rest plus the ii slots read at both its ends.
Board: a Node-clock reads its six neighbours' gears at the now slot, and each Mesh grips alike from both ends.
Clicks: waves and light travelling, as the clicks will read them.
"""

import numpy as np

from tensor24.algebra.carry import Z
from tensor24.engine.state import Layout


def seen(a: Z, nb: Z) -> Z:
    """Each neighbour's gears at the now slot: every Node-clock steps in every round, so its now slot is the round's."""
    return a[:, nb]


def gripped(layout: Layout, a: Z) -> Z:
    """What the grips' read lands on every Spoke at every site: each read row's now counts at both ends of the Spoke's Mesh, so the Mesh's grip is the same from either end."""
    nb, _, _, _, _, _, _, stretch, _, _, _ = layout
    first, factor, target = stretch
    here = a[first]
    landed = np.zeros(nb.shape, dtype=object)
    np.add.at(landed, target, factor[:, None] * (here + np.take_along_axis(here, nb[target], axis=1)))
    return landed


def held(layout: Layout, a: Z) -> Z:
    """Every Spoke's grip at every gear and site: its train's grip on the Spoke's Mesh at rest, and what the grips' read lands on it at the now slot."""
    _, _, meshes, grip, _, _, _, _, _, _, _ = layout
    return grip[:, meshes] + gripped(layout, a)


def stretches(layout: Layout, a: Z) -> Z:
    """Every gear's six stretches at the now slot, each neighbour's count less its own along the Spokes in the star's order: the read the pull makes, and the one the metric's push reads (term 5)."""
    nb, _, _, _, _, _, _, _, _, _, _ = layout
    return seen(a, nb) - a[:, None, :]


def pull(layout: Layout, a: Z) -> Z:
    """The Meshes' pull on every gear: its grip on each Spoke's Mesh times its stretch along the Spoke, summed over the Spokes."""
    return (stretches(layout, a) * held(layout, a)).sum(axis=1)
