"""observe/em.py: READ-ONLY observables of determined states for the matter and EM layers (AGENTS item 10).

Exact integer forms (numpy object arrays of Python ints) for every identity; floats only for derived diagnostics.
Notation: a state S_t holds a = X(t-1), b = X(t), r = r(t) for every gear; the step S_t -> S_{t+1} gives
D (b(t+1) + b(t-1)) = 2 u(t) + r(t) - r(t+1).

Exact identities (derivations: NOTES_em.md):
  continuity  rho(S_{t+1}) - rho(S_t) + div j(S_t) = R(S_t, S_{t+1})        at every node
              rho = D a^T J' b,  j_d(x) = 2 b(x+e_d)^T J' H_d b(x),  R = b(t)^T J' (r(t) - r(t+1))
  Lorenz      C(S_{t+1}) = C(S_t),  C(S) = Phi.b - Phi.a + div A(a)        (rounding-free accumulator)
  Gauss       Y_g(S_{t+1}) - Y_g(S_t) = -sigma R - 2 g (Q-1) Lap C          at every node (C = 0 for legal data)
              Y_g = g D [Phi(t+1) - 2 Phi(t) + Phi(t-1)] - 2 g (Q-1) Lap Phi(t) - sigma rho(t) - g div r_A(t)
  Noether     sum_x [rho(S_{t+1}) - rho(S_t)] = sum_x R
"""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, State
from ..core.tensor import Tensor
from ..layers.em import A_NAMES, PHI
from ..layers.matter import algebra, link_hamiltonian, matter_names


# --------------------------------------------------------------------------------------------- views
def _idx(tensor: Tensor, ns, names):
    return [tensor.gear_index(f"{ns}.{n}" if ns else n) for n in names]


def matter_view(state: State, tensor: Tensor, ns: str = "matter", species: str = "pair", exact: bool = True):
    """(a, b, r) of the matter gears as (L, L, L, n) arrays (object = exact ints, or float64 if exact=False)."""
    idx = _idx(tensor, ns, matter_names(species))
    L = state.L
    out = []
    for F in (state.a, state.b, state.r):
        arr = np.moveaxis(F[idx].reshape(len(idx), L, L, L), 0, -1)
        out.append(arr.astype(OBJ) if exact else arr.astype(float))
    return tuple(out)


def field_view(state: State, tensor: Tensor, ns: str = "em", exact: bool = True) -> dict:
    """{'A_x' | 'A_y' | 'A_z' | 'Phi': (a, b, r)} as (L, L, L) arrays."""
    L = state.L
    out = {}
    for n in A_NAMES + (PHI,):
        g = tensor.gear_index(f"{ns}.{n}")
        out[n] = tuple((F[g].reshape(L, L, L)).astype(OBJ if exact else float) for F in (state.a, state.b, state.r))
    return out


def _bil(u, M, v):
    """sum_ij u_i M_ij v_j over the last axis (exact for object arrays): u^T M v."""
    Mv = np.zeros_like(v)
    n = M.shape[0]
    for i in range(n):
        acc = 0
        for j in range(n):
            if M[i, j]:
                acc = acc + int(M[i, j]) * v[..., j]
        Mv[..., i] = acc
    return (u * Mv).sum(-1)


def _div(F):
    """Backward lattice divergence of a link field given as a list of three (L, L, L) arrays."""
    return sum(F[k] - np.roll(F[k], 1, axis=k) for k in range(3))


def _lap(f):
    return sum(np.roll(f, s, axis=k) for k in range(3) for s in (1, -1)) - 6 * f


# --------------------------------------------------------------------------------------------- matter bilinears
def density(state: State, tensor: Tensor, D: int, ns: str = "matter", X: str = "Jp", species: str = "pair"):
    """Exact two-time Noether density rho_X = D a^T X b (X = "Jp": the charge; "J": the C-even carrier number;
    species "single" (one 8-block) has only X = "J")."""
    a, b, _ = matter_view(state, tensor, ns, species)
    return D * _bil(a, algebra(species)[X], b)


def charge_density(state: State, tensor: Tensor, D: int, ns: str = "matter"):
    return density(state, tensor, D, ns, "Jp")


def link_currents(state: State, tensor: Tensor, matter_params: dict, ns: str = "matter", X: str = "Jp"):
    """Exact single-time link currents j_d(x) = 2 b(x+e_d)^T X H_d b(x), d = 0, 1, 2 (H_d = hop P_d - wilson W0)."""
    species = matter_params.get("species", "pair")
    _, b, _ = matter_view(state, tensor, ns, species)
    Xm = algebra(species)[X]
    out = []
    for d in range(3):
        H = link_hamiltonian(matter_params, d)
        bn = np.roll(b, -1, axis=d)
        out.append(2 * _bil(bn, Xm @ H, b))
    return out


def remainder_term(before: State, after: State, tensor: Tensor, ns: str = "matter", X: str = "Jp",
                   species: str = "pair"):
    """R = b(t)^T X (r(t) - r(t+1)) (the matter remainders' exact share of every identity)."""
    _, b, r0 = matter_view(before, tensor, ns, species)
    _, _, r1 = matter_view(after, tensor, ns, species)
    return _bil(b, algebra(species)[X], r0 - r1)


def continuity_residual(before: State, after: State, tensor: Tensor, D: int, matter_params: dict,
                        ns: str = "matter", X: str = "Jp"):
    """rho(after) - rho(before) + div j(before) - R  (exactly 0 at every node)."""
    sp = matter_params.get("species", "pair")
    return (density(after, tensor, D, ns, X, sp) - density(before, tensor, D, ns, X, sp)
            + _div(link_currents(before, tensor, matter_params, ns, X))
            - remainder_term(before, after, tensor, ns, X, sp))


# --------------------------------------------------------------------------------------------- field
def phi_next(state: State, tensor: Tensor, ns: str = "em"):
    f = field_view(state, tensor, ns)
    pa, pb, _ = f[PHI]
    return 2 * pb - pa - _div([f[n][1] for n in A_NAMES]) + _div([f[n][0] for n in A_NAMES])


def phi_centred(state: State, tensor: Tensor, ns: str = "em"):
    """phi_c = Phi(t) + Phi(t+1): what the matter reads."""
    return field_view(state, tensor, ns)[PHI][1] + phi_next(state, tensor, ns)


def lorenz_C(state: State, tensor: Tensor, ns: str = "em"):
    """C = Phi.b - Phi.a + div A(a) = Phi(t) - Phi(t-1) + div A(t-1): exactly constant in time (rounding-free Phi)."""
    f = field_view(state, tensor, ns)
    return f[PHI][1] - f[PHI][0] + _div([f[n][0] for n in A_NAMES])


def gauss_Y(state: State, tensor: Tensor, em_params: dict, matter_ns: str = "matter", em_ns: str = "em"):
    """Y_g = g D (Phi(t+1) - 2 Phi(t) + Phi(t-1)) - 2 g (Q-1) Lap Phi(t) - sigma rho(t) - g div r_A(t) (exact)."""
    Q, g, sigma = em_params["Q"], em_params["g"], em_params["sigma"]
    D = 6 * Q
    f = field_view(state, tensor, em_ns)
    pa, pb, _ = f[PHI]
    pn = phi_next(state, tensor, em_ns)
    rho = charge_density(state, tensor, D, matter_ns)
    rA = [f[n][2] for n in A_NAMES]
    return g * D * (pn - 2 * pb + pa) - 2 * g * (Q - 1) * _lap(pb) - sigma * rho - g * _div(rA)


def gauss_step_residual(before: State, after: State, tensor: Tensor, em_params: dict, matter_ns: str = "matter",
                        em_ns: str = "em"):
    """Y_g(after) - Y_g(before) + sigma R + 2 g (Q-1) Lap C  (exactly 0 at every node, for ANY data)."""
    Q, g, sigma = em_params["Q"], em_params["g"], em_params["sigma"]
    return (gauss_Y(after, tensor, em_params, matter_ns, em_ns) - gauss_Y(before, tensor, em_params, matter_ns, em_ns)
            + sigma * remainder_term(before, after, tensor, matter_ns)
            + 2 * g * (Q - 1) * _lap(lorenz_C(before, tensor, em_ns)))


def electric_field(state: State, tensor: Tensor, ns: str = "em", phi_norm: float = 1.0 / 3.0):
    """E_d(t) on the links (x, x+e_d) (float): -(phi(x+e) - phi(x)) - (A_d(t) - A_d(t-1)), phi = phi_norm * Phi
    (documented normalisation phi = Phi / 3; the Gauss law reads 6Q div E + 2 Lap Phi = (sigma/g) rho + div r_A + ...)."""
    f = field_view(state, tensor, ns, exact=False)
    phi = phi_norm * f[PHI][1]
    return [-(np.roll(phi, -1, axis=d) - phi) - (f[A_NAMES[d]][1] - f[A_NAMES[d]][0]) for d in range(3)]


# --------------------------------------------------------------------------------------------- readouts (float)
def species_projector(sp: int) -> np.ndarray:
    """2 Pi_sp = 1 - sp V (V = J J' = -s s'): keeps the charge sector J' = i*sp of the physical sector J = +i."""
    return np.eye(16, dtype=np.int64) - sp * algebra("pair")["V"]


def species_density(state: State, tensor: Tensor, sp: int, ns: str = "matter"):
    """Float density of one species: (2 Pi a)^T J' (2 Pi b) (event view)."""
    a, b, _ = matter_view(state, tensor, ns, exact=False)
    P = species_projector(sp).astype(float)
    Jp = algebra("pair")["Jp"].astype(float)
    pa, pb = a @ P.T, b @ P.T
    return (pa * (pb @ Jp.T)).sum(-1)


def projected_density(state: State, tensor: Tensor, P: np.ndarray, ns: str = "matter"):
    a, b, _ = matter_view(state, tensor, ns, exact=False)
    Jp = algebra("pair")["Jp"].astype(float)
    pa, pb = a @ P.T, b @ P.T
    return (pa * (pb @ Jp.T)).sum(-1)


def centroid(w, axis: int, origin: int):
    """Minimum-image centroid of a weight field along one axis, relative to ``origin``."""
    L = w.shape[0]
    X = np.arange(L)
    dx = ((X - origin + L // 2) % L) - L // 2
    shape = [1, 1, 1]
    shape[axis] = L
    return float((w * dx.reshape(shape)).sum() / w.sum())


def click_sizes(before: State, after: State, tensor: Tensor, ns: str = "matter"):
    """ell = b(t+1) + b(t-1) of every matter gear (L, L, L, 16), float (the click sizes, read-only)."""
    _, b1, _ = matter_view(after, tensor, ns, exact=False)
    a0, _, _ = matter_view(before, tensor, ns, exact=False)
    return b1 + a0


def click_charge(ell0, ell1, P: np.ndarray | None = None):
    """Click-space charge density ell(t)^T J' ell(t+1) (float), optionally species-projected."""
    Jp = algebra("pair")["Jp"].astype(float)
    if P is not None:
        ell0, ell1 = ell0 @ P.T, ell1 @ P.T
    return (ell0 * (ell1 @ Jp.T)).sum(-1)


def max_abs(state: State) -> int:
    return state.max_abs()
