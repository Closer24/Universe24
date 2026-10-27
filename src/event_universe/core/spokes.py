"""The six spokes of every clock: the pull of an array through one spoke, the one shift of a notch across a mesh in the package, on the torus (the wrap on every axis, the clock itself on a folded axis of extent one; the open and closed faces and the inner faces left 2026-10-24, the owner's word: the torus is the great clock); the arrays' own methods alone, no numeric library (ALGEBRA.md #the-line)."""

from __future__ import annotations

from typing import Any

AXES = (
    3  # the lattice's three axes (the dimension, the engine's one typed number; R3: the world's shape)
)
SIGNS = (1, -1)  # an axis's two senses, +a and -a
SIDES = len(SIGNS)  # the two spokes of one axis, one per sense
SPOKES = AXES * SIDES  # a clock's six spokes, the one definition of Rule3's 6
SPOKE_SIDES = tuple((axis, side) for axis in range(AXES) for side in SIGNS)  # [+X, -X, +Y, -Y, +Z, -Z]


def shifted(a: Any, axis: int, sigma: int) -> Any:
    """The array shifted by one mesh toward `sigma` on `axis` through the wrap, out[i] = a[i + sigma]; the array itself on a folded axis of extent one (`pull`, the notch arriving through the spoke, is this shift)."""
    extent = a.shape[axis]
    return a if extent == 1 else a.take([(index + sigma) % extent for index in range(extent)], axis=axis)


pull = shifted


def spoke_of(axis: int, side: int) -> int:
    """The spoke of an axis and a side (0 the + side, 1 the - side), SIDES * axis + side: the inverse of SPOKE_SIDES, the one spelling of a spoke's index."""
    return SIDES * axis + side


def transverse(axis: int) -> tuple[int, int]:
    """The cube's twist once (R7 of the readings' map, 2026-10-26; the Hand pair's one cross act): the two axes transverse to the axis in the cube's cyclic order, (axis + 1, axis - 1) modulo the three, the first the second's right twist about the axis; the curl, the twist and the shears read the cube's twist here and nowhere else."""
    return wrap(axis + 1, AXES), wrap(axis - 1, AXES)


def wrap(index: int, extent: int) -> int:
    """The periodic wrap of a clock's index or an axis along its extent, the torus's one index arithmetic."""
    return index % extent


def across(a: Any, spoke: int) -> Any:
    """The one read across a mesh: the array's value at the clock beyond the spoke (`pull` through the spoke's axis and side), the torus wrapped; every mesh read of the clock passes here (the owner's word of 2026-10-25: the mesh's act in one place)."""
    axis, side = SPOKE_SIDES[spoke]
    return pull(a, axis, side)
