"""The six Ports of every Node: the arrival of an array through one Port, the six arrivals in Port order taken once per array per interval, and the outward Ports of a set of Nodes; the arrays' own methods alone, no numeric library (ALGEBRA.md #the-primitives, SEND and RECEIVE)."""

from __future__ import annotations

from typing import Any

from event_universe.core.game_board import PORT_HEADINGS

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


def port_of(axis: int, side: int) -> int:
    """The Port toward `side` on `axis` in Port order [+X, -X, +Y, -Y, +Z, -Z]."""
    return 2 * axis + (0 if side > 0 else 1)


class Ports:
    """The GameBoard's Ports for one loop: `arrivals` once per (array, offset, shape, strides, wrap, fill) per interval, the cache cleared by `begin` (the interval's start, and the in-place writers of exchanged arrays); `outward` the Nodes of a mask whose Link through a Port leaves it."""

    def __init__(self, wrap: Wrap) -> None:
        self.wrap = wrap
        self.taken: dict[tuple[Any, ...], tuple[Any, tuple[Any, ...]]] = {}
        self.exchanged = 0

    def begin(self) -> None:
        """The cache emptied: every array's arrivals are taken again at their next request."""
        self.taken.clear()

    def key(self, a: Any, wrap: Wrap, fill: Any) -> tuple[Any, ...]:
        """The identity of one array as exchanged: its base kept alive in the entry so the id is not reused within the interval."""
        base = a if a.base is None else a.base
        interface = a.__array_interface__
        return (id(base), interface["data"][0], a.shape, interface["strides"], wrap, fill, a.dtype.str)

    def arrivals(self, a: Any, wrap: Wrap | None = None, fill: Any = 0) -> tuple[Any, ...]:
        """The six arrivals of `a` in Port order, one exchange per array per interval (ALGEBRA.md #the-primitives: one send out, one arrival in)."""
        faces = self.wrap if wrap is None else wrap
        key = self.key(a, faces, fill)
        base = a if a.base is None else a.base
        found = self.taken.get(key)
        if found is not None and found[0] is base:
            return found[1]
        taken = tuple(
            arrival(a, port // 2, heading[port // 2], faces[port // 2], fill)
            for port, heading in enumerate(PORT_HEADINGS)
        )
        self.taken[key] = (base, taken)
        self.exchanged += 1
        return taken

    def outward(self, mask: Any, wrap: Wrap | None = None) -> tuple[Any, ...]:
        """Per Port the Nodes of `mask` whose Link through it leads to a Node outside `mask`: beyond an open face there is no Node and no Port (the fill True), a folded axis carries none (the mask arrives as itself)."""
        inside = self.arrivals(mask, wrap, True)
        return tuple(mask & ~inside[port] for port in range(6))
