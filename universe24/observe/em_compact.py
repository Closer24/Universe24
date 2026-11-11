"""observe/em_compact.py: READ-ONLY observables of the compact-U(1) EM candidate (layers/em_compact.py).

Exact Gauss/Noether law (Board Noether theorem with the LOCAL generator i at node y; physical variables X = W + X0):
  G_y(t) = rho_y + D sum_k [eps(U_k(y)) - eps(U_k(y - e_k))] + D sum_{k1 != k2} [eps(P_k1k2(y)) - eps(P_k1k2(y - e_k1 - e_k2))]
  eps(u) = X(t-1) . (i X(t)) = -re(t-1) im(t) + im(t-1) re(t)    (complex gear pair, i acting by left multiplication)
  rho_y = D a_y^T J' b_y (the matter's charge density; M(i) = J' on the pair)
  G_y(S_{t+1}) - G_y(S_t) = R_y + sum over the same link/2-path gears of +- X(t) . i (r(t) - r(t+1))   EXACTLY.
"""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, State
from ..core.tensor import Tensor
from .em import charge_density, remainder_term

AXES = ("x", "y", "z")
UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def _pairs(tensor: Tensor, ns: str):
    """[(re_index, im_index, X0_re, kind, (k1, k2))] for the link and 2-path gears of the u1 block."""
    out = []
    names = tensor.names
    for k in range(3):
        out.append((tensor.gear_index(f"{ns}.U{AXES[k]}_re"), tensor.gear_index(f"{ns}.U{AXES[k]}_im"), "U", (k,)))
    for k1 in range(3):
        for k2 in range(3):
            if k1 != k2 and f"{ns}.P{AXES[k1]}{AXES[k2]}_re" in names:
                out.append((tensor.gear_index(f"{ns}.P{AXES[k1]}{AXES[k2]}_re"),
                            tensor.gear_index(f"{ns}.P{AXES[k1]}{AXES[k2]}_im"), "P", (k1, k2)))
    return out


def _field(F, g, L):
    return F[g].astype(OBJ).reshape(L, L, L)


def _end_shift(arr, kind, ks):
    """Value of a gear based at y - (end offset), read at y: links end at +e_k, 2-paths at +e_k1 + e_k2."""
    if kind == "U":
        return np.roll(arr, 1, axis=ks[0])
    return np.roll(np.roll(arr, 1, axis=ks[0]), 1, axis=ks[1])


def gauss_G(state: State, tensor: Tensor, u1_params: dict, D: int, matter_ns: str = "matter", ns: str = "u1"):
    """Exact integer Gauss/Noether density G_y (see the module docstring)."""
    if type(D) is not int or D != 6:
        raise ValueError('this observer requires the fixed divisor six')
    L = state.L
    A, P0 = u1_params["A"], u1_params.get("P0", 0)
    G = charge_density(state, tensor, D, matter_ns)
    for gre, gim, kind, ks in _pairs(tensor, ns):
        x0 = A if kind == "U" else P0
        are, aim = _field(state.a, gre, L) + x0, _field(state.a, gim, L)
        bre, bim = _field(state.b, gre, L) + x0, _field(state.b, gim, L)
        eps = -are * bim + aim * bre
        G = G + D * (eps - _end_shift(eps, kind, ks))
    return G


def gauss_dressing(before: State, after: State, tensor: Tensor, u1_params: dict, matter_ns: str = "matter",
                   ns: str = "u1"):
    """The exact remainder term: R (matter) + sum +- X(t) . i (r(t) - r(t+1)) over links and 2-paths."""
    L = before.L
    A, P0 = u1_params["A"], u1_params.get("P0", 0)
    out = remainder_term(before, after, tensor, matter_ns)
    for gre, gim, kind, ks in _pairs(tensor, ns):
        x0 = A if kind == "U" else P0
        bre, bim = _field(before.b, gre, L) + x0, _field(before.b, gim, L)
        dre = _field(before.r, gre, L) - _field(after.r, gre, L)
        dim = _field(before.r, gim, L) - _field(after.r, gim, L)
        term = -bre * dim + bim * dre
        out = out + term - _end_shift(term, kind, ks)
    return out


def gauss_step_residual(before, after, tensor, u1_params, D, matter_ns="matter", ns="u1"):
    """G(after) - G(before) - dressing: exactly 0 at every node."""
    if type(D) is not int or D != 6:
        raise ValueError('this observer requires the fixed divisor six')
    return (gauss_G(after, tensor, u1_params, D, matter_ns, ns) - gauss_G(before, tensor, u1_params, D, matter_ns, ns)
            - gauss_dressing(before, after, tensor, u1_params, matter_ns, ns))


def link_phase_advance(state: State, tensor: Tensor, u1_params: dict, k: int, ns: str = "u1"):
    """Float angle of U(t) conj(U(t-1)) on the links of axis k (the electric field in temporal gauge)."""
    L = state.L
    A = u1_params["A"]
    gre, gim = tensor.gear_index(f"{ns}.U{AXES[k]}_re"), tensor.gear_index(f"{ns}.U{AXES[k]}_im")
    u1 = (state.b[gre].astype(float) + A) + 1j * state.b[gim].astype(float)
    u0 = (state.a[gre].astype(float) + A) + 1j * state.a[gim].astype(float)
    return np.angle(u1 * np.conj(u0)).reshape(L, L, L)


def link_norm_dev(state: State, tensor: Tensor, u1_params: dict, ns: str = "u1") -> float:
    """max | |U| / A - 1 | over every link (float)."""
    A = u1_params["A"]
    worst = 0.0
    for k in range(3):
        gre, gim = tensor.gear_index(f"{ns}.U{AXES[k]}_re"), tensor.gear_index(f"{ns}.U{AXES[k]}_im")
        nrm = np.hypot(state.b[gre].astype(float) + A, state.b[gim].astype(float)) / A
        worst = max(worst, float(np.abs(nrm - 1).max()))
    return worst
