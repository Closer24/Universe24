"""The six Ports of every Node: the arrival of an array through one Port, the one shift of a level across a Link in the package, on the torus (the wrap on every axis, the Node itself on a folded axis of extent one; the open and closed faces and the inner faces left 2026-10-24, the owner's word: the torus is the board); the arrays' own methods alone, no numeric library (ALGEBRA.md #the-line)."""

from __future__ import annotations

from typing import Any, NamedTuple

AXES = 3  # the lattice's three axes
SIDES = 2  # the two Ports of one axis, +a and -a
PORTS = AXES * SIDES  # a Node's six Ports, the one definition of Rule3's 6
PORT_SIDES = tuple((axis, side) for axis in range(AXES) for side in (1, -1))  # [+X, -X, +Y, -Y, +Z, -Z]


class Wrap(NamedTuple):
    """The board's face rule, the torus: every axis wraps (ALGEBRA.md, The board is a torus; the open and closed faces and the inner faces of the record worlds left 2026-10-24), the three flags kept as the readings' word for the ring on each axis."""

    x: bool
    y: bool
    z: bool


def shifted(a: Any, axis: int, sigma: int) -> Any:
    """The array shifted by one Link toward `sigma` on `axis` through the wrap, out[i] = a[i + sigma]; the array itself on a folded axis of extent one."""
    extent = a.shape[axis]
    if extent == 1:
        return a
    return a.take([(index + sigma) % extent for index in range(extent)], axis=axis)


def arrival(a: Any, axis: int, sigma: int, wrap: Wrap) -> Any:
    """The level arriving through the Port toward `sigma` on `axis`, out[i] = a[i + sigma] (`shifted`), on the torus `wrap` names; the dtype the array's."""
    return shifted(a, axis, sigma)
