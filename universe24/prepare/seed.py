"""Explicit integer initial-data templates and finite matrix orbit sums.

Names such as dark, matter, and lapse identify experimental register groups;
they are not a physical identification. No preparation runs the update.
Rounded eigenvector and calibrated background presets are retired.
"""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, State
from ..core.lattice import lattice
from ..core.tensor import Tensor


def gamma_matrix() -> np.ndarray:
    """Gamma = J' K W0 (16 x 16 signed permutation), read from layers.matter (read-only)."""
    from ..layers.matter import JP16, K16, W016
    return JP16 @ K16 @ W016


def _matter_rows(tensor: Tensor, ns: str = "matter") -> list[int]:
    from ..layers.matter import matter_names
    return [tensor.gear_index(f"{ns}.{n}") for n in matter_names("pair")]


def s2_star(state: State, tensor: Tensor, x0, A: int, i: int = 0, axis: int = 1, ns: str = "matter") -> State:
    """S2* on the link (x0, x0 + e_axis) (axis 1 = y for Gamma = J'R_j W0). Returns a NEW state."""
    G = gamma_matrix()
    rows = _matter_rows(tensor, ns)
    lat = lattice(state.L)
    a, b, r = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    n0 = lat.index(*x0)
    x1 = list(x0)
    x1[axis] += 1
    n1 = lat.index(*x1)
    e = np.zeros(16, dtype=np.int64)
    e[i] = 1
    ge = G @ e
    b[rows[i], n0] = A
    for j in range(16):
        if ge[j]:
            a[rows[j], n1] = A * int(ge[j])
    return State(state.L, a, b, r)


def node_rstar(state: State, tensor: Tensor, x0, A: int, i: int = 0, ns: str = "matter") -> State:
    """node R*: b(x0) = A e_i, a(x0) = A Gamma e_i (two integers on one node)."""
    G = gamma_matrix()
    rows = _matter_rows(tensor, ns)
    lat = lattice(state.L)
    a, b, r = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    n0 = lat.index(*x0)
    e = np.zeros(16, dtype=np.int64)
    e[i] = 1
    ge = G @ e
    b[rows[i], n0] = A
    for j in range(16):
        if ge[j]:
            a[rows[j], n0] = A * int(ge[j])
    return State(state.L, a, b, r)


def ra_background(state: State, tensor: Tensor, value: int, gear: str = "bgk.B") -> State:
    """R-a datum: the background gear held at (value, value) at every node (static: u_B = 6 b)."""
    g = tensor.gear_index(gear)
    a, b, r = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    a[g] = value
    b[g] = value
    return State(state.L, a, b, r)


def k0_offset(state: State, tensor: Tensor, c0: int, field: str = "metric.h00") -> State:
    """The k = 0 lapse offset: c0 added to the lapse field's a and b at every node (prepared data)."""
    g = tensor.gear_index(field)
    a, b, r = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    a[g] = a[g] + c0
    b[g] = b[g] + c0
    return State(state.L, a, b, r)


def l0_dark_seed(state: State, tensor: Tensor, x0, A: int, v=None, ns: str = "ref") -> State:
    """L0 (dark) seed: a(x0) = b(x0) = A v on the 48 L0 gears (v integer, default e_0). Returns a NEW state."""
    lat = lattice(state.L)
    n0 = lat.index(*x0)
    vv = [0] * 48 if v is None else list(v)
    if any(type(x) is bool or not isinstance(x, (int, np.integer)) for x in vv):
        raise TypeError("v needs exact integer entries")
    vv = [int(x) for x in vv]
    if v is None:
        vv[0] = 1
    if len(vv) != 48:
        raise ValueError("v needs 48 integer entries")
    a, b, r = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    for h in range(48):
        if vv[h]:
            g = tensor.gear_index(f"{ns}.R{h:02d}")
            a[g, n0] = a[g, n0] + A * vv[h]
            b[g, n0] = b[g, n0] + A * vv[h]
    return State(state.L, a, b, r)


def m0_band_vector(body_signs=(1, -1, 1), band: int = 0, scale: int = 64) -> list[int]:
    """Retired rounded or scale-dependent preset; use explicit integer initial data."""
    raise NotImplementedError("This initial-data preset is retired; supply explicit integer initial data")


def l0_rstar_vector(body_signs=(1, -1, 1), base=None) -> list[int]:
    """An L0 vector fixed by L0's signed relabelling S (observe.seed.l0_relabelling): v = Sum_j S^j v0 over one period of
    S (v0 = e_0 by default, or an integer 48-vector), so S v = v and the node seed a = b = A v is R*-fixed. Data only."""
    from ..observe.seed import l0_relabelling
    rel = l0_relabelling(body_signs)
    S = rel["S"]
    v0 = np.zeros(48, dtype=object)
    if base is None:
        v0[0] = 1
    else:
        if len(base) != 48 or any(type(x) is bool or not isinstance(x, (int, np.integer)) for x in base):
            raise TypeError("base needs 48 exact integer entries")
        v0[:] = [int(x) for x in base]
    v, cur = np.zeros(48, dtype=object), v0.copy()
    for _ in range(rel["order"]):
        v += cur
        cur = S @ cur
    if not np.any(v):
        raise ValueError("the orbit sum vanishes for this base vector; choose another")
    return [int(x) for x in v]


def ra_free_mean(engine, state, field: str = "metric.h00", bg: str = "bgk.B", t_avg: int = 4000):
    """Compatibility entry point that explicitly rejects the retired background calibration."""
    from .gravity_ra import ra_free_mean as _ra
    return _ra(engine, state, field=field, bg=bg, t_avg=t_avg)


def pplus_seed_hook(*args, **kwargs):
    """TODO (documented): the positive-energy P+ seed (Study 6 S12/T14; s6/M1_work/M1_t29_S12_legal_Pplus.py).
    Steps to port: (1) the P+ projector P+(k) = (1 + h(k)/lambda(k))/2 of the system's Dirac matter (with Wilson) applied
    to A e_i at x0 (float FFT, then exact integer rounding on a declared support), (2) a = Gamma b(sigma x),
    (3) an R*-symmetric integer flux w with div w = -rho' routed through x0 along mirror-symmetric paths, split into
    b_A, a_A with a_A = -b_A o mirror, b_Phi = 0, a_Phi = div a_A (Lorenz C = 0), in the E1 normalisation of the system
    (sigma, g, hs, ws), (4) checks C = 0, Gauss = 0, R*(s0) = s0. Not ported in stage 3 (1818 integers in M1's run)."""
    raise NotImplementedError(pplus_seed_hook.__doc__)


__all__ = ["gamma_matrix", "s2_star", "node_rstar", "l0_dark_seed", "m0_band_vector", "l0_rstar_vector",
           "ra_background", "ra_free_mean", "k0_offset", "pplus_seed_hook"]
