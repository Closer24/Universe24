"""Periodic cube (Z/LZ)^3: node indexing, the six face directions, the Yee link convention.

Pure geometry. Nothing here knows what a gear means.

* Node (x, y, z), 0 <= x, y, z < L, has the flat index n = (x*L + y)*L + z, so an array of shape (G, L**3) reshapes
  to (G, L, L, L) indexed [gear, x, y, z].
* The six face directions use the order of universe24.algebra.group_2o.DIRECTIONS: +x, -x, +y, -y, +z, -z (index d;
  the opposite direction of d is d ^ 1).
* Legal storage offsets of a tensor factor: OFFSETS = (0, +-e_x, +-e_y, +-e_z).
* Yee convention: the link (x, x + e_k), k = 0, 1, 2 for +x, +y, +z, is stored at its BASE node x. A link gear is an
  ordinary gear type of the unit cell carrying the metadata ``link = k``; the engine treats it like any other gear.
"""
from __future__ import annotations

from functools import lru_cache

import numpy as np

DIRECTIONS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
ZERO = (0, 0, 0)
OFFSETS = (ZERO,) + DIRECTIONS
DIRECTION_NAMES = ("+x", "-x", "+y", "-y", "+z", "-z")
LINK_AXES = ("x", "y", "z")          # link axis k is stored at the base node; its direction index is 2k


def link_direction(axis: int) -> tuple[int, int, int]:
    """Unit vector e_k of the Yee link axis k in {0, 1, 2}."""
    if type(axis) is not int or not 0 <= axis < 3:
        raise ValueError("link axis must be 0, 1 or 2 (+x, +y, +z)")
    return DIRECTIONS[2 * axis]


def offset_tuple(value) -> tuple[int, int, int]:
    off = tuple(value)
    if len(off) != 3 or any(type(v) is not int for v in off):
        raise TypeError(f"offset must be three Python ints, got {value!r}")
    return off


class Lattice:
    """Periodic L^3 cube with precomputed gather maps for the seven legal offsets."""

    __slots__ = ("L", "N", "_shift")

    def __init__(self, L: int):
        if type(L) is not int or L < 3:
            raise ValueError("side length L must be an integer >= 3")
        self.L = L
        self.N = L ** 3
        self._shift = {}

    def __eq__(self, other):
        return isinstance(other, Lattice) and other.L == self.L

    def __hash__(self):
        return hash(("Lattice", self.L))

    def __repr__(self):
        return f"Lattice(L={self.L})"

    def index(self, x: int, y: int, z: int) -> int:
        L = self.L
        return ((x % L) * L + (y % L)) * L + (z % L)

    def coords(self, n: int) -> tuple[int, int, int]:
        L = self.L
        if not 0 <= n < self.N:
            raise ValueError("node index outside the cube")
        return (n // (L * L), (n // L) % L, n % L)

    def all_coords(self) -> np.ndarray:
        """(N, 3) array of (x, y, z) in flat-index order."""
        n = np.arange(self.N)
        L = self.L
        return np.stack([n // (L * L), (n // L) % L, n % L], axis=1)

    def shift_index(self, offset) -> np.ndarray:
        """Gather map: field[..., shift_index(o)][n] is the value at node n + o (periodic)."""
        off = offset_tuple(offset)
        cached = self._shift.get(off)
        if cached is None:
            L = self.L
            xyz = self.all_coords()
            x = (xyz[:, 0] + off[0]) % L
            y = (xyz[:, 1] + off[1]) % L
            z = (xyz[:, 2] + off[2]) % L
            cached = ((x * L + y) * L + z).astype(np.intp)
            cached.setflags(write=False)
            self._shift[off] = cached
        return cached

    def neighbour(self, n: int, d: int) -> int:
        """Flat index of the face neighbour of node n in direction d (0..5)."""
        x, y, z = self.coords(n)
        dx, dy, dz = DIRECTIONS[d]
        return self.index(x + dx, y + dy, z + dz)

    def link_endpoints(self, n: int, axis: int) -> tuple[int, int]:
        """Yee: the link gear of axis k stored at node n joins n and n + e_k."""
        return (n, self.neighbour(n, link_direction_index(axis)))


def link_direction_index(axis: int) -> int:
    link_direction(axis)
    return 2 * axis


@lru_cache(maxsize=32)
def lattice(L: int) -> Lattice:
    return Lattice(L)
