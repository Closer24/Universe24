"""The six Ports of every Node: the arrival of an array through one Port, the one shift of a level across a Link in the package; the arrays' own methods alone, no numeric library (ALGEBRA.md #the-line)."""

from __future__ import annotations

from typing import Any

Wrap = tuple[bool, bool, bool]


def arrival(a: Any, axis: int, sigma: int, wrap: bool, fill: Any = 0) -> Any:
    """The level arriving through the Port toward `sigma` on `axis`, out[i] = a[i + sigma]: the wrap on a periodic axis (the neighbours' addresses, adjacent_node's), `fill` beyond an open or closed face, the array itself on a folded axis of extent one (the self-Link); the dtype the array's."""
    extent = a.shape[axis]
    if extent == 1:
        return a
    if wrap:
        return a.take([(index + sigma) % extent for index in range(extent)], axis=axis)
    out = a.copy()
    out[...] = fill
    lower = [slice(None)] * 3
    upper = [slice(None)] * 3
    if sigma > 0:
        lower[axis], upper[axis] = slice(None, -1), slice(1, None)
    else:
        lower[axis], upper[axis] = slice(1, None), slice(None, -1)
    out[tuple(lower)] = a[tuple(upper)]
    return out
