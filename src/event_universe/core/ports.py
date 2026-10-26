"""The six Ports of every Node: the arrival of an array through one Port, the one shift of a level across a Link in the package, on the torus (the wrap on every axis, the Node itself on a folded axis of extent one; the open and closed faces and the inner faces left 2026-10-24, the owner's word: the torus is the board); the arrays' own methods alone, no numeric library (ALGEBRA.md #the-line)."""

from __future__ import annotations

from typing import Any

AXES = 3  # the lattice's three axes
SIDES = 2  # the two Ports of one axis, +a and -a
PORTS = AXES * SIDES  # a Node's six Ports, the one definition of Rule3's 6
PORT_SIDES = tuple((axis, side) for axis in range(AXES) for side in (1, -1))  # [+X, -X, +Y, -Y, +Z, -Z]


def shifted(a: Any, axis: int, sigma: int) -> Any:
    """The array shifted by one Link toward `sigma` on `axis` through the wrap, out[i] = a[i + sigma]; the array itself on a folded axis of extent one (`arrival`, the level arriving through the Port, is this shift)."""
    extent = a.shape[axis]
    return a if extent == 1 else a.take([(index + sigma) % extent for index in range(extent)], axis=axis)


arrival = shifted


def port_of(axis: int, side: int) -> int:
    """The Port of an axis and a side (0 the + side, 1 the - side), SIDES * axis + side: the inverse of PORT_SIDES, the one spelling of a Port's index."""
    return SIDES * axis + side


def transverse(axis: int) -> tuple[int, int]:
    """The cube's hand once (R7 of the readings' map, 2026-10-26; the Hand pair's one cross act): the two axes transverse to the axis in the cube's cyclic order, (axis + 1, axis - 1) modulo the three, the first the second's right hand about the axis; the curl, the twist and the shears read the hand here and nowhere else."""
    return wrap(axis + 1, AXES), wrap(axis - 1, AXES)


def wrap(index: int, extent: int) -> int:
    """The periodic wrap of a Node's index or an axis along its extent, the torus's one index arithmetic."""
    return index % extent


def across(a: Any, port: int) -> Any:
    """The one read across a Link: the array's value at the Node beyond the Port (`arrival` through the Port's axis and side), the torus wrapped; every Link read of the Node passes here (the owner's word of 2026-10-25: the Link's act in one place)."""
    axis, side = PORT_SIDES[port]
    return arrival(a, axis, side)
