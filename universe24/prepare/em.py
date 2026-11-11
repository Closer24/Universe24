"""Integer initial-data setters and read-only audit maps. The former rounded packet and static-field presets are retired; floating Fourier helpers are diagnostics only. No function is applied during evolution."""
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
    it fixes 2 for divisor six."""
    if type(D) is not int or D != 6:
        raise ValueError("remainder maps use the fixed divisor six")
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
    """Retired rounded or scale-dependent preset; use explicit integer initial data."""
    raise NotImplementedError("This initial-data preset is retired; supply explicit integer initial data")


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
    """Retired rounded or scale-dependent preset; use explicit integer initial data."""
    raise NotImplementedError("This initial-data preset is retired; supply explicit integer initial data")


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
    """Retired initial-data formula; no fixed-divisor replacement is established."""
    raise NotImplementedError("This preparation depended on the removed divisor scale; supply explicit integer initial data instead")


# ------------------------------------------------------------------------------------------------- audit maps
def c_map(state: State, tensor: Tensor, D: int, matter_ns: str = "matter", em_ns: str | None = "em") -> State:
    """AUDIT MAP. Charge conjugation C: Y -> -Y on the matter pair, A_d -> -A_d and Phi -> -Phi; every negated gear
    takes the parity-preserving remainder map R' (exact for even K; fixes the vacuum 2 for divisor six)."""
    if type(D) is not int or D != 6:
        raise ValueError("audit maps use the fixed divisor six")
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
    mirror = "Mp" (default; fixes the joint vacuum 2 for divisor six) or "M" (S4-P's convention D-1-r; exact too, but it
    maps the vacuum 2 to 3). """
    if type(D) is not int or D != 6:
        raise ValueError("audit maps use the fixed divisor six")
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
    if type(D) is not int or D != 6:
        raise ValueError("audit maps use the fixed divisor six")
    A, B, R = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    mi = _idx(tensor, matter_ns, matter_names(species))
    A[mi], B[mi] = -A[mi], -B[mi]
    R[mi] = r_parity_negation(R[mi], D) if mirror == "Mp" else (D - 1) - R[mi]
    return State(state.L, A, B, R)


def x_reversor_core(tensor: Tensor, matter_ns: str = "matter", em_ns: str | None = "em",
                    mirror: str = "Mp"):
    """The same staggered reversor X, BUILT FROM core/reversors.py (stage 0.2 building blocks, manager 09:28):
    X = GroupLinearMap(K on the 16 matter gears, neg_r = mirror) o GearwiseMap(mirror on matter and A_d) o PhiMap,
    PhiMap: Phi (a, b, r) -> (-Phi_next, -Phi.b, r) (a FunctionMap; it reads A before the mirror acts). Also returns
    KM = Kramers K o mirror on the matter alone (A, Phi untouched) and the central element N (global matter negation:
    "Jp" for mirror "Mp", "J" for "M"; X^2 = N on the matter: K^2 = -1)."""
    from ..core.reversors import FunctionMap, GearwiseMap, GroupLinearMap
    mnames = [f"{matter_ns}.{n}" for n in matter_names("pair")]
    Kmat = [[int(v) for v in row] for row in algebra("pair")["K"]]
    Kmap = GroupLinearMap(tensor, mnames, Kmat, neg_r=mirror, name="K")
    Mm = GearwiseMap(tensor, {g: mirror for g in mnames})
    KM = Kmap @ Mm
    N = GearwiseMap(tensor, {g: ("Jp" if mirror == "Mp" else "J") for g in mnames})
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
    Mall = GearwiseMap(tensor, {g: mirror for g in mnames + anames})
    X = Kmap @ Mall @ PhiMap
    X.name = f"X_EM = (K o {mirror} on matter, {mirror} on A, Phi -> (-Phi_next, -b, r))"
    return X, KM, N
