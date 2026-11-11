"""Integer compact-link preparations. The former rounded Gauss-law initial-data preset is explicitly retired; link_pulse accepts a chosen integer excitation."""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, State
from ..core.tensor import Tensor
from .em import torus_poisson_float

AXES = ("x", "y", "z")


def gauss_links(state: State, tensor: Tensor, rho, A: int, D: int, ns: str = "u1") -> State:
    """Retired rounded or scale-dependent preset; use explicit integer initial data."""
    raise NotImplementedError("This initial-data preset is retired; supply explicit integer initial data")


def link_pulse(state: State, tensor: Tensor, axis: int, center, half: int, amp: int, ns: str = "u1") -> State:
    """Copy of ``state`` with W_im = amp on the axis-``axis`` links of a (2 half + 1)^3 patch at ``center`` (a = b:
    the pulse starts at rest)."""
    L = state.L
    g = tensor.gear_index(f"{ns}.U{AXES[axis]}_im")
    Aa, B, R = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    f = np.zeros((L, L, L), dtype=object)
    cx, cy, cz = center
    for dx in range(-half, half + 1):
        for dy in range(-half, half + 1):
            for dz in range(-half, half + 1):
                f[(cx + dx) % L, (cy + dy) % L, (cz + dz) % L] = amp
    Aa[g] = f.reshape(-1)
    B[g] = f.reshape(-1).copy()
    return State(L, Aa, B, R)
