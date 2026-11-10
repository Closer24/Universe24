"""SEED preparations as DATA ONLY (AGENTS item 9; INTEGRATOR, manager 11:0x). Nothing here is a law, a gear or a run:
every function returns a NEW State (the seed enters only as initial data on the joint vacuum).

Sources: s6/AGREE_M.md (a)/F2 (twin-agreed Study 6 seed), B1-GRAV F4d (R-a background, k = 0 offset).
  S2*      b(x0) = A e_i,  a(x0 + e_y) = A Gamma e_i,   Gamma = J' K W0 (= W0 G, G = J'K; K = 1_2 (x) R_j (x) 1_2 Kramers,
           W0 = beta = Pi the mass/parity matrix) on the 16-channel Dirac pair "matter"; every other gear at the joint
           vacuum. Two integers. Fixed by R* about the link midpoint (observe/seed.py). y-link for J'R_j (the C2
           direction rule: J'R_k needs a z-link).
  node R*  b(x0) = A e_i,  a(x0) = A Gamma e_i  (the node-centred alternative; Wilson-dependent generativity).
  R-a      the declared uniform k = 0 background: the bgk.B gear held at (v, v) (u_B = 6Q b keeps it static).
  k = 0 offset   a constant added to the lapse field's a and b (the prepared offset of F4d).
  L0 dark  (OWNER decision 2, handed class) a SEPARATE datum beside S2*: a(x0) = b(x0) = A v on the 48 L0 gears,
           v an integer vector (default: one L0 channel; or a rounded eigenvector of M0 = 6 - Sum W_d, a dark band at
           rest). a = b is the turning point of the clock; fixed by R* about the node x0 (L0 has no Gauss law).
           Its clicks are AUDIT-ONLY under the handed class (observe/readout.py).
  weak-field rule (R-P1/R-P2): when a seed is meant to feel a weak potential, amplitude x field >= D/(8 g_phi)
           (System.info["weak_field_min"]); below it a rest clock can be rounding-locked.
  P+ seed  HOOK ONLY (TODO): the positive-energy projected seed with an R*-symmetric integer flux network
           (s6/M1_work/M1_t29_S12_legal_Pplus.py) is NOT ported: it needs its own normalisation (dd = hn = PF) and a
           float FFT projector followed by an integer flux routing; see pplus_seed_hook.
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
    """R-a datum: the background gear held at (value, value) at every node (static: u_B = 6Q b)."""
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
    vv = [0] * 48 if v is None else [int(x) for x in v]
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
    """A rounded integer eigenvector of L0's mass matrix M0 (band = index of the distinct eigenvalue, ascending)."""
    from ..layers.gravity_l0c import m0_matrix
    M0 = m0_matrix(body_signs).astype(float)
    vals, vecs = np.linalg.eigh(M0)
    distinct = sorted(set(np.round(vals, 9)))
    idx = int(np.argmin(np.abs(vals - distinct[band])))
    v = vecs[:, idx]
    return [int(round(scale * x / np.max(np.abs(v)))) for x in v]


def l0_rstar_vector(body_signs=(1, -1, 1), base=None) -> list[int]:
    """An L0 vector fixed by L0's signed relabelling S (observe.seed.l0_relabelling): v = Sum_j S^j v0 over one period of
    S (v0 = e_0 by default, or an integer 48-vector), so S v = v and the node seed a = b = A v is R*-fixed. Data only."""
    from ..observe.seed import l0_relabelling
    rel = l0_relabelling(body_signs)
    S = rel["S"]
    v0 = np.zeros(48, dtype=np.int64)
    if base is None:
        v0[0] = 1
    else:
        v0[:] = [int(x) for x in base]
    v, cur = np.zeros(48, dtype=np.int64), v0.copy()
    for _ in range(rel["order"]):
        v += cur
        cur = S @ cur
    if not np.any(v):
        raise ValueError("the orbit sum vanishes for this base vector; choose another")
    return [int(x) for x in v]


def ra_free_mean(engine, state, field: str = "metric.h00", bg: str = "bgk.B", t_avg: int = 4000):
    """R-a datum from the EXACT first-order time mean of the lapse source per Fourier mode (wraps B1-GRAV's
    prepare/gravity_ra.ra_free_mean; data only: the tensor is evaluated, nothing is run). For seeds that excite L0
    (pi/2-carrier and form-C L0 sources have a nonzero first-order mean). For S2* the first-order mean is exactly 0; its
    positive mean source is NONLINEAR, so no cancellation is claimed. Returns (new state, diagnostics)."""
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
