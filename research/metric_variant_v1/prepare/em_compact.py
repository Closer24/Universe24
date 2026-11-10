"""prepare/em_compact.py: INITIAL DATA ONLY for the compact-U(1) candidate (nothing here runs the engine).

* ``gauss_links``: link data consistent with the exact Gauss law for a given matter charge density rho: the links sit
  at U(t) = A (W = 0) and U(t-1) = A exp(-i dtheta), dtheta_k = -(phi(x+e_k) - phi(x)), -Lap phi = rho/(D A^2)
  (torus, k = 0 removed), so G_y = rho_y - D A^2 div sin(dtheta) ~ 0 up to rounding. In temporal gauge the link phase
  advance per update is the electric field.
* ``link_pulse``: a localized transverse link excitation (W_im on one axis over a small patch).
"""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, State
from ..core.tensor import Tensor
from .em import torus_poisson_float

AXES = ("x", "y", "z")


def gauss_links(state: State, tensor: Tensor, rho, A: int, D: int, ns: str = "u1") -> State:
    """Copy of ``state`` with Gauss-consistent link data for the charge density rho (float or int (L, L, L))."""
    phi = torus_poisson_float(np.asarray(rho, float), float(D) * A * A)
    L = state.L
    Aa, B, R = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    for k in range(3):
        dth = -(np.roll(phi, -1, axis=k) - phi)
        gre, gim = tensor.gear_index(f"{ns}.U{AXES[k]}_re"), tensor.gear_index(f"{ns}.U{AXES[k]}_im")
        are = np.rint(A * np.cos(dth)).astype(np.int64) - A
        aim = np.rint(-A * np.sin(dth)).astype(np.int64)
        Aa[gre] = are.reshape(-1).astype(object)
        Aa[gim] = aim.reshape(-1).astype(object)
        B[gre] = np.zeros(L ** 3, dtype=object)
        B[gim] = np.zeros(L ** 3, dtype=object)
    return State(L, Aa, B, R)


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
