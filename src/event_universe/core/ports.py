"""The six Ports of every Node: the arrival of an array through one Port, the one shift of a level across a Link in the package, under the board's face rule (0 beyond an open or closed face, the wrap on a periodic axis, the Node itself on a folded axis, and 0 through every Port of a Node the file declares beyond the board inside it, an inner face); the arrays' own methods alone, no numeric library (ALGEBRA.md #the-line)."""

from __future__ import annotations

from typing import Any, NamedTuple


class Wrap(NamedTuple):
    """The board's face rule: which of the three axes wrap (the others read 0 beyond their two faces), and the Nodes declared beyond the board inside it (`beyond`, a mask over the GameBoard, None where the file declares none): a Node beyond the board reads 0 through every Port and is read as 0 through every Port, so no level, current or source crosses its Links."""

    x: bool
    y: bool
    z: bool
    beyond: Any = None


def shifted(a: Any, axis: int, sigma: int, periodic: bool, fill: Any) -> Any:
    """The array shifted by one Link toward `sigma` on `axis`, out[i] = a[i + sigma]: the wrap on a periodic axis, `fill` beyond a face, the array itself on a folded axis of extent one."""
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
    out[tuple(face)] = fill  # the one layer beyond the face, the rest the shifted levels
    return out


def arrival(a: Any, axis: int, sigma: int, wrap: Wrap, fill: Any = 0) -> Any:
    """The level arriving through the Port toward `sigma` on `axis`, out[i] = a[i + sigma] (`shifted`), and `fill` at every Node beyond the board and through every Port whose far Node is beyond it (the inner face's rule, the same 0 as beyond an open face); the dtype the array's; the array copied once, where the folded axis returned it as it is."""
    out = shifted(a, axis, sigma, wrap[axis], fill)
    if wrap.beyond is None:
        return out
    if out is a:
        out = out.copy()
    out[wrap.beyond | shifted(wrap.beyond, axis, sigma, wrap[axis], False)] = fill
    return out
