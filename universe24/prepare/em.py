"""prepare/em.py: INITIAL DATA ONLY for the matter and EM layers (AGENTS item 9). Nothing here runs the engine.

* ``dirac_packet``: a positive-energy packet of the complex Dirac pair (physical sector J = +i, charge sector
  J' = i*sigp), from the package's own Bloch matrix (layers.matter.bloch_matrix), rounded to integers. Floats are used
  ONLY to build initial data (Study 4 s4/P_em_core.packet, ported to D = 6Q).
* ``c_image``: antimatter = the C-image (Y -> -Y) of matter data.
* ``set_matter`` / ``set_field``: write (a, b[, r]) arrays into a copy of a state.
* ``torus_poisson``: rint of the torus solution of -Lap f = s (k = 0 removed), for prepared static fields.
* ``static_phi_for``: the prepared static Phi of a charge density with the E1 normalisation (static dressed Gauss:
  -2 g (Q-1) Lap Phi = sigma rho).
AUDIT MAPS (they create the initial data of a separate audit run; never applied to a running state):
* ``c_map``: the full charge conjugation C (Y -> -Y on matter with the parity-preserving remainder map R', and
  A, Phi -> -A, -Phi with R'); F C = C F exactly (tests/test_em.py).
* ``x_reversor``: the exact STAGGERED time reversor X = (K o M on matter, M on A_d, Phi -> (-Phi_next, -Phi.b, r)).
"""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, State
from ..core.tensor import Tensor
from ..layers.em import A_NAMES, PHI
from ..layers.matter import algebra, bloch_matrix, matter_names


# ------------------------------------------------------------------------------------------------- helpers
def _idx(tensor: Tensor, ns: str, names) -> list[int]:
    return [tensor.gear_index(f"{ns}.{n}" if ns else n) for n in names]


def r_parity_negation(r, D: int):
    """R'(r) = D - 2 - r (even r), D - r (odd r): the parity-preserving negation remainder map (exact for even K);
    it fixes 3Q - 1 for odd Q."""
    return np.where(r % 2 == 0, (D - 2) - r, D - r)


def to_gear_major(arr) -> np.ndarray:
    """(L, L, L, n) -> (n, L^3) in the package's flat order n = (x L + y) L + z."""
    arr = np.asarray(arr)
    L = arr.shape[0]
    return np.moveaxis(arr, -1, 0).reshape(arr.shape[-1], L ** 3)


def set_matter(state: State, tensor: Tensor, ns: str, a, b, r=None, species: str = "pair") -> State:
    """Copy of ``state`` with the matter gears of namespace ``ns`` set from (L, L, L, n) integer arrays."""
    idx = _idx(tensor, ns, matter_names(species))
    A, B, R = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    A[idx] = to_gear_major(np.asarray(a, dtype=object))
    B[idx] = to_gear_major(np.asarray(b, dtype=object))
    if r is not None:
        R[idx] = to_gear_major(np.asarray(r, dtype=object))
    return State(state.L, A, B, R)


def set_field(state: State, tensor: Tensor, ns: str, gear: str, a, b, r=None) -> State:
    """Copy of ``state`` with one field gear (e.g. 'Phi', 'A_y') set from (L, L, L) integer arrays."""
    g = tensor.gear_index(f"{ns}.{gear}" if ns else gear)
    A, B, R = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    A[g] = np.asarray(a, dtype=object).reshape(-1)
    B[g] = np.asarray(b, dtype=object).reshape(-1)
    if r is not None:
        R[g] = np.asarray(r, dtype=object).reshape(-1)
    return State(state.L, A, B, R)


def shift(arr, x):
    """Periodic shift of an (L, L, L, ...) array so that the origin moves to x."""
    return np.roll(arr, tuple(x), axis=(0, 1, 2))


# ------------------------------------------------------------------------------------------------- packets
def kgrid(L: int) -> np.ndarray:
    k1 = 2 * np.pi * np.fft.fftfreq(L)
    return np.stack(np.meshgrid(k1, k1, k1, indexing="ij"), -1)


def _sector_basis(sig: int, sigp: int) -> np.ndarray:
    alg = algebra("pair")
    n = 16
    PJ = (np.eye(n) - 1j * sig * alg["J"]) / 2
    PJp = (np.eye(n) - 1j * sigp * alg["Jp"]) / 2
    U, _s, _ = np.linalg.svd(PJ @ PJp)
    return U[:, :4]


def dirac_packet(params: dict, L: int, sigp: int, width: float, amp: int, kc=(0.0, 0.0, 0.0), spin: int = 0,
                 center=(0, 0, 0)):
    """Positive-energy packet of the pair (J = +i, J' = i*sigp), Gaussian of k-width 1/width around kc, centred at
    ``center``. Returns integer arrays (a, b) of shape (L, L, L, 16) with b = b(0), a = b(-1) (exact Bloch phases,
    rounded; peak |b| = amp) and the Bloch angles w (L, L, L). Initial data only."""
    D = 6 * params["Q"]
    K = kgrid(L)
    B = np.zeros((L, L, L, 16, 16), complex)
    alg = algebra("pair")
    for d in range(3):
        ph = np.exp(-1j * K[..., d])[..., None, None]
        B += params["hop"] * (ph * alg["P"][d] + np.conj(ph) * alg["P"][d].T)
        if params["wilson"]:
            B += params["wilson"] * (2 - 2 * np.cos(K[..., d]))[..., None, None] * alg["W0"]
    B += params["mass"] * alg["W0"]
    Bs = _sector_basis(+1, sigp)
    Bk = np.einsum("ia,...ij,jb->...ab", Bs.conj(), B, Bs)
    lam, Vv = np.linalg.eigh(Bk)                        # ascending: [0, 1] are beta < 0 (the positive-energy pair)
    u0 = Vv[0, 0, 0][:, spin]
    Pk = np.einsum("...ia,...ja->...ij", Vv[..., :2], Vv[..., :2].conj())
    vk = np.einsum("...ij,j->...i", Pk, u0)
    vk16 = np.einsum("ia,...a->...i", Bs, vk)
    beta = lam[..., 0]
    w = np.arccos(np.clip(beta / D, -1, 1))
    kc = np.asarray(kc, float)
    kk = ((K - kc + np.pi) % (2 * np.pi)) - np.pi
    Z = np.exp(-0.5 * width ** 2 * (kk ** 2).sum(-1))
    zb = np.fft.ifftn(Z[..., None] * vk16, axes=(0, 1, 2))
    za = np.fft.ifftn((Z * np.exp(1j * w))[..., None] * vk16, axes=(0, 1, 2))
    sc = amp / np.abs(zb.real).max()
    b = np.rint(zb.real * sc).astype(np.int64)
    a = np.rint(za.real * sc).astype(np.int64)
    return shift(a, center), shift(b, center), w


def c_image(arr):
    """Antimatter = the C-image: (X, Y) -> (X, -Y) on (L, L, L, 16) matter data (flips J', keeps J and the Dirac
    matrices)."""
    out = np.array(arr, copy=True)
    out[..., 8:] *= -1
    return out


def spin_spinors(params: dict, sigp: int = +1):
    """The two k = 0 spinors (16-vectors, complex) of the (J = +i, J' = i*sigp) positive-energy pair."""
    Bs = _sector_basis(+1, sigp)
    B0 = bloch_matrix(params, np.zeros(3))
    lam, Vv = np.linalg.eigh(Bs.conj().T @ B0 @ Bs)
    return [Bs @ Vv[:, 0], Bs @ Vv[:, 1]]


# ------------------------------------------------------------------------------------------------- fields
def torus_poisson(src, scale: float = 1.0):
    """rint of the torus solution f of -Lap f = src / scale (k = 0 mode removed). Initial data only."""
    src = np.asarray(src, float)
    L = src.shape[0]
    K = kgrid(L)
    lam = (2 - 2 * np.cos(K)).sum(-1)
    lam[0, 0, 0] = 1.0
    F = np.fft.fftn(src) / (scale * lam)
    F[0, 0, 0] = 0
    return np.rint(np.fft.ifftn(F).real).astype(np.int64)


def torus_poisson_float(src, scale: float = 1.0):
    src = np.asarray(src, float)
    L = src.shape[0]
    K = kgrid(L)
    lam = (2 - 2 * np.cos(K)).sum(-1)
    lam[0, 0, 0] = 1.0
    F = np.fft.fftn(src) / (scale * lam)
    F[0, 0, 0] = 0
    return np.fft.ifftn(F).real


def static_phi_for(rho, em_params: dict):
    """Prepared static Phi of a charge density rho (rho = D a^T J' b, as observe.em.charge_density) in the E1
    normalisation: the static dressed Gauss law -2 g (Q - 1) Lap Phi = sigma rho (torus, k = 0 removed)."""
    Q, g, sigma = em_params["Q"], em_params["g"], em_params["sigma"]
    return torus_poisson(np.asarray(rho, float) * sigma, 2.0 * g * (Q - 1))


# ------------------------------------------------------------------------------------------------- audit maps
def c_map(state: State, tensor: Tensor, D: int, matter_ns: str = "matter", em_ns: str | None = "em") -> State:
    """AUDIT MAP. Charge conjugation C: Y -> -Y on the matter pair, A_d -> -A_d and Phi -> -Phi; every negated gear
    takes the parity-preserving remainder map R' (exact for even K; fixes the vacuum 3Q - 1 for odd Q)."""
    A, B, R = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    neg = _idx(tensor, matter_ns, matter_names("pair")[8:])
    if em_ns is not None:
        neg += _idx(tensor, em_ns, A_NAMES + (PHI,))
    A[neg], B[neg] = -A[neg], -B[neg]
    R[neg] = r_parity_negation(R[neg], D)
    return State(state.L, A, B, R)


def phi_next_flat(state: State, tensor: Tensor, em_ns: str = "em"):
    """Phi(t+1) of a state (exact; the accumulator never rounds): 2 Phi.b - Phi.a - div A.b + div A.a (flat)."""
    L = state.L
    p = tensor.gear_index(f"{em_ns}.{PHI}")
    ia = _idx(tensor, em_ns, A_NAMES)
    a = state.a.astype(OBJ)
    b = state.b.astype(OBJ)

    def div(F):
        out = 0
        for k, g in enumerate(ia):
            f = F[g].reshape(L, L, L)
            out = out + (f - np.roll(f, 1, axis=k))
        return out.reshape(-1)
    return 2 * b[p] - a[p] - div(b) + div(a)


def x_reversor(state: State, tensor: Tensor, D: int, matter_ns: str = "matter", em_ns: str | None = "em",
               mirror: str = "Mp", species: str = "pair") -> State:
    """AUDIT MAP. The staggered reversor X (s4 A7/P-iv, S4-P PR-17), declared as data in build_em's params:
    matter: K o M'  (M': (a, b, r) -> (b, a, R'(r)); then the signed permutation K = 1_2 (x) R_j (x) 1_2, a negated
            channel taking the negation map R' again, i.e. r unchanged overall);
    A_d   : M';
    Phi   : (a, b, r) -> (-Phi_next, -Phi.b, r)  (Phi never rounds, so its remainder is inert).
    mirror = "Mp" (default; fixes the joint vacuum 3Q - 1 for ODD Q) or "M" (S4-P's convention D-1-r; exact too, but it
    maps the vacuum 3Q - 1 to 3Q). Even Q has no mirror-fixed vacuum remainder."""
    if mirror not in ("Mp", "M"):
        raise ValueError("mirror must be 'Mp' or 'M'")
    rmap = (lambda r: r_parity_negation(r, D)) if mirror == "Mp" else (lambda r: (D - 1) - r)
    alg = algebra(species)
    K = alg["K"]
    n = alg["n"]
    perm = np.abs(K).argmax(1)
    sgn = K[np.arange(n), perm]
    A, B, R = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    nA, nB, nR = A.copy(), B.copy(), R.copy()
    mi = _idx(tensor, matter_ns, matter_names(species))
    for i in range(n):
        src = mi[perm[i]]
        s = int(sgn[i])
        nA[mi[i]] = s * B[src]
        nB[mi[i]] = s * A[src]
        nR[mi[i]] = rmap(R[src]) if s > 0 else R[src].copy()
    if em_ns is not None:
        for g in _idx(tensor, em_ns, A_NAMES):
            nA[g], nB[g], nR[g] = B[g].copy(), A[g].copy(), rmap(R[g])
        p = tensor.gear_index(f"{em_ns}.{PHI}")
        nA[p] = -phi_next_flat(state, tensor, em_ns)
        nB[p] = -B[p]
        nR[p] = R[p].copy()
    return State(state.L, nA, nB, nR)


def matter_negation(state: State, tensor: Tensor, D: int, matter_ns: str = "matter", mirror: str = "Mp",
                    species: str = "pair") -> State:
    """AUDIT MAP. Global matter sign N: (a, b, r) -> (-a, -b, R'(r)) (mirror "Mp") or (-a, -b, D-1-r) ("M") on every
    matter gear: the central element X^2 (K^2 = -1, the Kramers sign)."""
    A, B, R = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    mi = _idx(tensor, matter_ns, matter_names(species))
    A[mi], B[mi] = -A[mi], -B[mi]
    R[mi] = r_parity_negation(R[mi], D) if mirror == "Mp" else (D - 1) - R[mi]
    return State(state.L, A, B, R)


def x_reversor_core(tensor: Tensor, Q: int, matter_ns: str = "matter", em_ns: str | None = "em",
                    mirror: str = "Mp"):
    """The same staggered reversor X, BUILT FROM core/reversors.py (stage 0.2 building blocks, manager 09:28):
    X = GroupLinearMap(K on the 16 matter gears, neg_r = mirror) o GearwiseMap(mirror on matter and A_d) o PhiMap,
    PhiMap: Phi (a, b, r) -> (-Phi_next, -Phi.b, r) (a FunctionMap; it reads A before the mirror acts). Also returns
    KM = Kramers K o mirror on the matter alone (A, Phi untouched) and the central element N (global matter negation:
    "Jp" for mirror "Mp", "J" for "M"; X^2 = N on the matter: K^2 = -1)."""
    from ..core.reversors import FunctionMap, GearwiseMap, GroupLinearMap
    mnames = [f"{matter_ns}.{n}" for n in matter_names("pair")]
    Kmat = [[int(v) for v in row] for row in algebra("pair")["K"]]
    Kmap = GroupLinearMap(tensor, Q, mnames, Kmat, neg_r=mirror, name="K")
    Mm = GearwiseMap(tensor, Q, {g: mirror for g in mnames})
    KM = Kmap @ Mm
    N = GearwiseMap(tensor, Q, {g: ("Jp" if mirror == "Mp" else "J") for g in mnames})
    if em_ns is None:
        return KM, KM, N
    anames = [f"{em_ns}.{n}" for n in A_NAMES]
    p = tensor.gear_index(f"{em_ns}.{PHI}")

    def phi_fn(state: State) -> State:
        a, b, r = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
        nxt = phi_next_flat(state, tensor, em_ns)
        a[p], b[p] = -nxt, -b[p]
        return State(state.L, a, b, r)
    PhiMap = FunctionMap(phi_fn, "Phi->(-Phi_next,-b,r)")
    Mall = GearwiseMap(tensor, Q, {g: mirror for g in mnames + anames})
    X = Kmap @ Mall @ PhiMap
    X.name = f"X_EM = (K o {mirror} on matter, {mirror} on A, Phi -> (-Phi_next, -b, r))"
    return X, KM, N
