"""The six Ports of every Node: the arrival of an array through one Port, the one shift of a level across a Link in the package, under the board's face rule (the fill beyond an open or closed face, 0 for a record of a family of quanta, the vacuum, and the face Node's own level for a held row of the content, `OWN_LEVEL`, its rest continued through the face with no reflection; the wrap on a periodic axis; the Node itself on a folded axis; and the same fill through every Port of a Node the file declares beyond the board inside it, an inner face); the arrays' own methods alone, no numeric library (ALGEBRA.md #the-line, the arrival)."""

from __future__ import annotations

from typing import Any, NamedTuple

AXES = 3  # the lattice's three axes
SIDES = 2  # the two Ports of one axis, +a and -a
PORTS = AXES * SIDES  # a Node's six Ports, the one definition of Rule3's 6
PORT_SIDES = tuple((axis, side) for axis in range(AXES) for side in (1, -1))  # [+X, -X, +Y, -Y, +Z, -Z]


class Wrap(NamedTuple):
    """The board's face rule: which of the three axes wrap (the others read the row's fill beyond their two faces), and the Nodes declared beyond the board inside it (`beyond`, a mask over the GameBoard, None where the file declares none): a Node beyond the board reads the fill through every Port and is read as the fill through every Port, 0 for a record of a family of quanta, so no level, current or source crosses its Links."""

    x: bool
    y: bool
    z: bool
    beyond: Any = None


class OwnLevel:
    """The fill that reads the face Node's own level through a Port whose far Node is beyond the board, the held rows of the content's rule (ALGEBRA.md #the-line, the arrival; #what-is-open, item 22): the face layer kept from the array itself, as the folded axis keeps the Node, so a holder's tail meets itself beyond the face and no reflection with the sign flipped is made; a record of a family of quanta reads 0 there, the vacuum."""


OWN_LEVEL = OwnLevel()


def shifted(a: Any, axis: int, sigma: int, periodic: bool, fill: Any) -> Any:
    """The array shifted by one Link toward `sigma` on `axis`, out[i] = a[i + sigma]: the wrap on a periodic axis, `fill` beyond a face (the face layer's own level kept where `fill` is `OWN_LEVEL`), the array itself on a folded axis of extent one."""
    extent = a.shape[axis]
    if extent == 1:
        return a
    if periodic:
        return a.take([(index + sigma) % extent for index in range(extent)], axis=axis)
    out = a.copy()
    lower = [slice(None)] * 3
    upper = [slice(None)] * 3
    face = [slice(None)] * 3
    if sigma > 0:
        lower[axis], upper[axis], face[axis] = slice(None, -1), slice(1, None), slice(-1, None)
    else:
        lower[axis], upper[axis], face[axis] = slice(1, None), slice(None, -1), slice(None, 1)
    out[tuple(lower)] = a[tuple(upper)]
    if fill is not OWN_LEVEL:  # the face layer keeps its own level under OWN_LEVEL, the copy's
        out[tuple(face)] = fill  # the one layer beyond the face, the rest the shifted levels
    return out


def arrival(a: Any, axis: int, sigma: int, wrap: Wrap, fill: Any = 0) -> Any:
    """The level arriving through the Port toward `sigma` on `axis`, out[i] = a[i + sigma] (`shifted`), and `fill` at every Node beyond the board and through every Port whose far Node is beyond it (the inner face's rule, the same fill as beyond an open face: 0 for a record of a family of quanta, the Node's own level under `OWN_LEVEL`); the dtype the array's; the array copied once, where the folded axis returned it as it is."""
    out = shifted(a, axis, sigma, wrap[axis], fill)
    if wrap.beyond is None:
        return out
    if out is a:
        out = out.copy()
    beyond = wrap.beyond | shifted(wrap.beyond, axis, sigma, wrap[axis], False)
    out[beyond] = a[beyond] if fill is OWN_LEVEL else fill
    return out
