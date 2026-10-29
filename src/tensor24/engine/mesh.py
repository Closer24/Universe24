"""The Mesh: what a Node-clock reads of its neighbours, and the Meshes' pull."""

from tensor24.algebra.carry import Z
from tensor24.engine.state import Layout


def seen(a: Z, nb: Z) -> Z:
    """Each neighbour's gears at the now slot: every Node-clock steps in every round, so its now slot is the round's."""
    return a[:, nb]


def pull(layout: Layout, a: Z) -> Z:
    """The Meshes' pull on every gear: its train's grip on each Spoke's Mesh times the neighbour less its own now."""
    nb, _, meshes, grip, _, _, _ = layout
    return ((seen(a, nb) - a[:, None, :]) * grip[:, meshes]).sum(axis=1)
