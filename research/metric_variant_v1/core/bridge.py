"""Read-only bridge to the reference engine universe24 (used by tests and audits only).

Converts a universe24 ``State`` (48 channels per node, divisor 6) to the dense arrays of this package and back, with
the Q-scaling of the remainders (r -> Q*r). Nothing in universe24 is modified.
"""
from __future__ import annotations

import numpy as np

from universe24.core.state import VACUUM, Channel, Cube, State as RefState

from .engine import OBJ
from .lattice import lattice as _lattice

REFERENCE_VACUUM_R = VACUUM.r          # read from universe24 (= 2); a Q-scaled reference gear rests at (0, 0, 2Q)


def reference_arrays(ref: RefState, Q: int = 1):
    """(a, b, r) object arrays of shape (48, L^3) for a universe24 state; r scaled by Q."""
    L = ref.cube.side
    lat = _lattice(L)
    a = np.empty((48, lat.N), dtype=OBJ)
    b = np.empty((48, lat.N), dtype=OBJ)
    r = np.empty((48, lat.N), dtype=OBJ)
    bg = ref.background
    a[:, :] = bg.a
    b[:, :] = bg.b
    r[:, :] = Q * bg.r
    for (x, y, z, g), ch in ref.cells.items():
        n = lat.index(x, y, z)
        a[g, n], b[g, n], r[g, n] = ch.a, ch.b, Q * ch.r
    return a, b, r


def to_reference_state(a, b, r, L: int, Q: int = 1, background: Channel = VACUUM) -> RefState:
    """universe24 State from (48, L^3) arrays; r must be a multiple of Q."""
    lat = _lattice(L)
    cells = {}
    for g in range(48):
        for n in range(lat.N):
            rr = int(r[g, n])
            if rr % Q:
                raise ValueError("remainder is not a multiple of Q: not a Q-scaled reference channel")
            ch = Channel(int(a[g, n]), int(b[g, n]), rr // Q)
            if ch != background:
                cells[(*lat.coords(n), g)] = ch
    return RefState(Cube(L), background, cells)
