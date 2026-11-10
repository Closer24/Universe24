"""prepare/chiral.py — INITIAL DATA and AUDIT MAPS for the chiral candidate (layers/chiral.py). Data only: nothing here
runs the engine (the maps are audit maps, as prepare.em.x_reversor; they are never fed back into a run).

* chiral_system(Q, ...): the stand-alone chiral tensor (matter, matter2, wsu2, chiral) and its blocks.
* random_chiral_state(...): random test data (matter amplitude, field deviations, remainders).
* jpure_seed(...): the Study-7 h13 seed: an EXACTLY R*-fixed integer matter seed whose time-doubler (J-) content is at
  the rounding level (fraction ~ 1/A^2). Construction: an R*-symmetric smooth start (b0, a0 = G b0(-x)), its exact J+
  projection in Fourier space (the projection commutes with R*), scaled by A, b rounded, and a := G b_int(-x) EXACTLY.
  G = W0 J' K (one pair), inversion about the node 0.
* discrete maps (core/reversors building blocks + one custom 2-path map): R* (CPT reversor), T_phys = C K o Mp,
  board T = J'K o Mp, and the forward maps CP = inversion o C W0, P = inversion o W0, C.
"""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, State
from ..core.lattice import DIRECTIONS, lattice
from ..core.reversors import Composite, FunctionMap, GearwiseMap, GroupLinearMap, SpatialMap
from ..core.tensor import compose
from ..layers.chiral import (HIGGS, Q_DEFAULT, chiral_algebra, chiral_blocks)
from ..layers.matter import algebra as pair_algebra
from ..layers.matter import bloch_matrix, matter_names
from . import vacuum_state

AXES = ("x", "y", "z")


def chiral_system(Q: int = Q_DEFAULT, **kw):
    """(tensor, blocks) of the stand-alone chiral system: matter, matter2, wsu2, chiral."""
    blocks = chiral_blocks(Q, include_matter=True, **kw)
    return compose(*blocks), blocks


def gear_groups(tensor, blocks) -> dict:
    """Qualified gear names by role."""
    matter, partner, links, coup = blocks[0], blocks[1], blocks[2], blocks[3]
    comps = ("1", "i", "j", "k")
    out = {"matter": [matter.qualify(g) for g in matter_names("pair")],
           "partner": [partner.qualify(g) for g in matter_names("pair")],
           "higgs": [coup.qualify(h) for h in HIGGS],
           "links": {k: [links.qualify(f"U{AXES[k]}_{c}") for c in comps] for k in range(3)},
           "paths": {}}
    if links.params.get("use_P"):
        for k1 in range(3):
            for k2 in range(3):
                if k1 != k2:
                    out["paths"][(k1, k2)] = [links.qualify(f"P{AXES[k1]}{AXES[k2]}_{c}") for c in comps]
    return out


def random_chiral_state(tensor, Q: int, L: int, rng, *, matter_amp: int = 40, field_amp: int = 2,
                        groups: dict | None = None, vacuum_r: bool = False) -> State:
    """Random integer data: matter gears in [-matter_amp, matter_amp], field deviations in [-field_amp, field_amp],
    remainders uniform in 0..D-1 (or the vacuum 3Q - 1 with vacuum_r=True)."""
    D = 6 * Q
    N = lattice(L).N
    G = tensor.G
    mset = set()
    if groups is not None:
        mset = {tensor.gear_index(g) for g in groups["matter"] + groups["partner"]}
    a = np.zeros((G, N), dtype=OBJ)
    b = np.zeros((G, N), dtype=OBJ)
    for g in range(G):
        amp = matter_amp if (g in mset or groups is None) else field_amp
        a[g] = [int(v) for v in rng.integers(-amp, amp + 1, N)]
        b[g] = [int(v) for v in rng.integers(-amp, amp + 1, N)]
    if vacuum_r:
        r = np.full((G, N), 3 * Q - 1, dtype=OBJ)
    else:
        r = np.array([[int(v) for v in rng.integers(0, D, N)] for _ in range(G)], dtype=OBJ)
    return State(L, a, b, r)


# ======================================================================================== J-pure R*-fixed seed
def _jsplit(a, b, params, L, D):
    """Fourier J+/J- split of real pair data a, b of shape (L, L, L, 16): b = v+ + v-, a = e^{-wJ} v+ + e^{+wJ} v-."""
    alg = pair_algebra("pair")
    J = alg["J"].astype(float)
    ks = 2 * np.pi * np.arange(L) / L
    ah = np.fft.fftn(a, axes=(0, 1, 2))
    bh = np.fft.fftn(b, axes=(0, 1, 2))
    vp = np.zeros_like(bh)
    cs = {}
    for i in range(L):
        for j in range(L):
            for l in range(L):
                B = bloch_matrix(params, (ks[i], ks[j], ks[l]))
                w, U = np.linalg.eigh(B)
                c = U @ np.diag(w / D) @ U.conj().T
                s = U @ np.diag(np.sqrt(np.clip(1 - (w / D) ** 2, 0, None))) @ U.conj().T
                cs[(i, j, l)] = (c, s)
                rhs = J @ (ah[i, j, l] - (c + s @ J) @ bh[i, j, l])
                vp[i, j, l] = np.linalg.solve(2 * s, rhs)
    return vp, bh - vp, cs


def _plus_data(vp, cs, L):
    alg = pair_algebra("pair")
    J = alg["J"].astype(float)
    ah = np.zeros_like(vp)
    for key, (c, s) in cs.items():
        ah[key] = (c - s @ J) @ vp[key]
    return np.real(np.fft.ifftn(ah, axes=(0, 1, 2))), np.real(np.fft.ifftn(vp, axes=(0, 1, 2)))


def jpure_seed(tensor, blocks, Q: int, L: int, *, A: int = 1 << 10, width: float = 6.0, rng=None,
               matter_block: int = 0) -> tuple[State, dict]:
    """The exactly R*-fixed, J+-pure (up to rounding) integer seed in ONE pair (default: the first doublet member);
    every other gear at its vacuum. Returns (state, report)."""
    rng = np.random.default_rng(31) if rng is None else rng
    D = 6 * Q
    mb = blocks[matter_block]
    params = mb.params
    alg = pair_algebra("pair")
    Gm = (alg["W0"] @ alg["Jp"] @ alg["K"]).astype(np.int64)
    idx = np.arange(L)
    X = np.stack(np.meshgrid(idx, idx, idx, indexing="ij"), -1)
    neg = lambda f: f[(-idx) % L][:, (-idx) % L][:, :, (-idx) % L]
    r2 = np.sum(((X + L / 2) % L - L / 2) ** 2, -1)
    b0 = np.exp(-r2 / width)[..., None] * rng.normal(size=16)[None, None, None, :]
    a0 = neg(b0) @ Gm.T
    vp, vm, cs = _jsplit(a0, b0, params, L, D)
    ap, bp = _plus_data(vp, cs, L)
    float_fix = float(np.max(np.abs(ap - neg(bp) @ Gm.T)))
    scale = A / np.max(np.abs(bp))
    b_int = np.round(bp * scale).astype(np.int64)
    a_int = neg(b_int) @ Gm.T
    vpi, vmi, _ = _jsplit(a_int.astype(float), b_int.astype(float), params, L, D)
    frac = float(np.sum(np.abs(vmi) ** 2) / (np.sum(np.abs(vpi) ** 2) + np.sum(np.abs(vmi) ** 2)))
    st = vacuum_state(tensor, Q, L, *blocks)
    a, b = st.a.astype(OBJ), st.b.astype(OBJ)
    rows = [tensor.gear_index(mb.qualify(g)) for g in matter_names("pair")]
    for ch, g in enumerate(rows):
        a[g] = [int(v) for v in a_int[..., ch].reshape(-1)]
        b[g] = [int(v) for v in b_int[..., ch].reshape(-1)]
    seed = State(L, a, b, st.r)
    exact_fixed = bool(np.array_equal(a_int, neg(b_int) @ Gm.T) and np.array_equal(b_int, neg(a_int) @ Gm.T))
    NJ = int(D * np.einsum("xyzi,ij,xyzj->", a_int.astype(object), alg["J"].astype(object), b_int.astype(object)))
    return seed, {"A": A, "L": L, "float_projection_Rstar_error": float_fix, "exact_Rstar_fixed_matter": exact_fixed,
                  "J_minus_fraction": frac, "N_J": NJ, "nonzero_integers": int(np.count_nonzero(a_int) +
                                                                                  np.count_nonzero(b_int))}


def j_minus_fraction(state: State, tensor, blocks, Q: int, matter_block: int = 0) -> float:
    """Diagnostic (floats): J- fraction of the matter pair's current (a, b) data (free-pair split)."""
    mb = blocks[matter_block]
    L = state.L
    rows = [tensor.gear_index(mb.qualify(g)) for g in matter_names("pair")]
    a = np.stack([np.array(state.a[g], dtype=float).reshape(L, L, L) for g in rows], -1)
    b = np.stack([np.array(state.b[g], dtype=float).reshape(L, L, L) for g in rows], -1)
    vp, vm, _ = _jsplit(a, b, mb.params, L, 6 * Q)
    return float(np.sum(np.abs(vm) ** 2) / (np.sum(np.abs(vp) ** 2) + np.sum(np.abs(vm) ** 2)))


# ======================================================================================== discrete maps
def _sigma(Gam32: np.ndarray) -> np.ndarray:
    """4x4 signed matrix sig with Gam rho(q) Gam^-1 = rho(sig q) on the weak generators (sig fixes e0)."""
    t = chiral_algebra()["t"]
    Gi = np.round(np.linalg.inv(Gam32.astype(float))).astype(np.int64)
    sig = np.zeros((4, 4), np.int64)
    sig[0, 0] = 1
    for a in range(3):
        img = Gam32 @ t[a] @ Gi
        hit = [(b, s) for b in range(3) for s in (1, -1) if np.array_equal(img, s * t[b])]
        if len(hit) != 1:
            raise ValueError("this matter map does not normalise the weak algebra: not a symmetry of the chiral block")
        b, s = hit[0]
        sig[b + 1, a + 1] = s
    return sig


def _two_path_shift(tensor, groups, L) -> FunctionMap:
    """After a SpatialMap (node gears x -> S - x): move each 2-path family (k1,k2) to the (k2,k1) rows shifted by
    -(e_k1 + e_k2) (the reversed path), values unchanged."""
    lat = lattice(L)
    fams = {key: [tensor.gear_index(g) for g in names] for key, names in groups["paths"].items()}

    def fn(state: State) -> State:
        a, b, r = state.a.copy(), state.b.copy(), state.r.copy()
        for (k1, k2), src in fams.items():
            dst = fams[(k2, k1)]
            off = tuple(-(DIRECTIONS[2 * k1][i] + DIRECTIONS[2 * k2][i]) for i in range(3))
            # new[dst](y) = moved[src](y - off)  i.e. value at y - off moves to y
            take = lat.shift_index(tuple(-o for o in off))
            for s_, d_ in zip(src, dst):
                a[d_] = state.a[s_][take]
                b[d_] = state.b[s_][take]
                r[d_] = state.r[s_][take]
        return State._raw(state.L, a, b, r)
    return FunctionMap(fn, "two_path_reverse")


def discrete_map(tensor, blocks, Q: int, L: int, *, matter16: np.ndarray, inversion: bool, time_flip: bool,
                 name: str = "map"):
    """Composite audit map: [time flip Mp on every gear] then the linear maps (matter: matter16 per pair; Higgs: sigma;
    links / 2-paths: sigma (o conj if inversion)) with neg_r = Mp, then the inversion about node 0 (links re-based,
    2-paths reversed). The same integer map on a and b; R' on negated gears (forward maps) / kept r after Mp."""
    groups = gear_groups(tensor, blocks)
    Gam32 = np.kron(np.eye(2, dtype=np.int64), matter16.astype(np.int64))
    sig = _sigma(Gam32)
    conj = np.diag([1, -1, -1, -1]).astype(np.int64)
    sigL = sig @ conj if inversion else sig
    maps = []
    if time_flip:
        maps.append(GearwiseMap(tensor, Q, default="Mp"))
    mg = groups["matter"] + groups["partner"]
    maps.append(GroupLinearMap(tensor, Q, mg, [[int(v) for v in row] for row in Gam32], neg_r="Mp", name="matter"))
    maps.append(GroupLinearMap(tensor, Q, groups["higgs"], [[int(v) for v in row] for row in sig], neg_r="Mp",
                               name="higgs"))
    for k in range(3):
        maps.append(GroupLinearMap(tensor, Q, groups["links"][k], [[int(v) for v in row] for row in sigL],
                                   neg_r="Mp", name=f"link{k}"))
    for key, gl in groups["paths"].items():
        maps.append(GroupLinearMap(tensor, Q, gl, [[int(v) for v in row] for row in sigL], neg_r="Mp",
                                   name=f"path{key}"))
    if inversion:
        maps.append(SpatialMap(tensor, (0, 0, 0), "P_node(0)"))
        if groups["paths"]:
            maps.append(_two_path_shift(tensor, groups, L))
    X = Composite(maps)
    X.name = name
    return X


def standard_maps(tensor, blocks, Q: int, L: int) -> dict:
    """The declared discrete maps of REVERSOR_CHIRAL (layers/chiral.py)."""
    alg = pair_algebra("pair")
    W0, Jp, K, C = (alg[k].astype(np.int64) for k in ("W0", "Jp", "K", "C"))
    return {"R*": discrete_map(tensor, blocks, Q, L, matter16=W0 @ Jp @ K, inversion=True, time_flip=True, name="R*"),
            "T_phys": discrete_map(tensor, blocks, Q, L, matter16=C @ K, inversion=False, time_flip=True,
                                   name="T_phys=CK.Mp"),
            "boardT": discrete_map(tensor, blocks, Q, L, matter16=Jp @ K, inversion=False, time_flip=True,
                                   name="boardT=J'K.Mp"),
            "CP": discrete_map(tensor, blocks, Q, L, matter16=C @ W0, inversion=True, time_flip=False, name="CP"),
            "P": discrete_map(tensor, blocks, Q, L, matter16=W0, inversion=True, time_flip=False, name="P"),
            "C": discrete_map(tensor, blocks, Q, L, matter16=C, inversion=False, time_flip=False, name="C")}


__all__ = ["chiral_system", "gear_groups", "random_chiral_state", "jpure_seed", "j_minus_fraction", "discrete_map",
           "standard_maps"]
