"""Integer chiral test data and finite audit maps. jpure_seed is explicitly retired. Fourier splitting is a read-only diagnostic, not an initial-data or runtime update."""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, State
from ..core.lattice import DIRECTIONS, lattice
from ..core.reversors import Composite, FunctionMap, GearwiseMap, GroupLinearMap, SpatialMap
from ..core.tensor import compose
from ..layers.chiral import (HIGGS, chiral_algebra, chiral_blocks)
from ..layers.matter import algebra as pair_algebra
from ..layers.matter import bloch_matrix, matter_names
from . import vacuum_state

AXES = ("x", "y", "z")


def chiral_system(**kw):
    """(tensor, blocks) of the stand-alone chiral system: matter, matter2, wsu2, chiral."""
    blocks = chiral_blocks(include_matter=True, **kw)
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


def random_chiral_state(tensor, L: int, rng, *, matter_amp: int = 40, field_amp: int = 2,
                        groups: dict | None = None, vacuum_r: bool = False) -> State:
    """Random integer data: matter gears in [-matter_amp, matter_amp], field deviations in [-field_amp, field_amp],
    remainders uniform in 0..D-1 (or the vacuum 2 with vacuum_r=True)."""
    D = 6
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
        r = np.full((G, N), 2, dtype=OBJ)
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


def jpure_seed(tensor, blocks, L: int, *, A: int = 1 << 10, width: float = 6.0, rng=None,
               matter_block: int = 0) -> tuple[State, dict]:
    """Retired initial-data formula; no fixed-divisor replacement is established."""
    raise NotImplementedError("This preparation depended on the removed divisor scale; supply explicit integer initial data instead")


def j_minus_fraction(state: State, tensor, blocks, matter_block: int = 0) -> float:
    """Diagnostic (floats): J- fraction of the matter pair's current (a, b) data (free-pair split)."""
    mb = blocks[matter_block]
    L = state.L
    rows = [tensor.gear_index(mb.qualify(g)) for g in matter_names("pair")]
    a = np.stack([np.array(state.a[g], dtype=float).reshape(L, L, L) for g in rows], -1)
    b = np.stack([np.array(state.b[g], dtype=float).reshape(L, L, L) for g in rows], -1)
    vp, vm, _ = _jsplit(a, b, mb.params, L, 6)
    return float(np.sum(np.abs(vm) ** 2) / (np.sum(np.abs(vp) ** 2) + np.sum(np.abs(vm) ** 2)))


# ======================================================================================== discrete maps
def _sigma(Gam32: np.ndarray) -> np.ndarray:
    """4x4 signed matrix sig with Gam rho(q) Gam^-1 = rho(sig q) on the weak generators (sig fixes e0)."""
    t = chiral_algebra()["t"]
    Gi = Gam32.T.copy()
    if not np.array_equal(Gam32 @ Gi, np.eye(Gam32.shape[0], dtype=np.int64)):
        raise ValueError("the audit map must be an exact orthogonal integer matrix")
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


def discrete_map(tensor, blocks, L: int, *, matter16: np.ndarray, inversion: bool, time_flip: bool,
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
        maps.append(GearwiseMap(tensor, default="Mp"))
    mg = groups["matter"] + groups["partner"]
    maps.append(GroupLinearMap(tensor, mg, [[int(v) for v in row] for row in Gam32], neg_r="Mp", name="matter"))
    maps.append(GroupLinearMap(tensor, groups["higgs"], [[int(v) for v in row] for row in sig], neg_r="Mp",
                               name="higgs"))
    for k in range(3):
        maps.append(GroupLinearMap(tensor, groups["links"][k], [[int(v) for v in row] for row in sigL],
                                   neg_r="Mp", name=f"link{k}"))
    for key, gl in groups["paths"].items():
        maps.append(GroupLinearMap(tensor, gl, [[int(v) for v in row] for row in sigL], neg_r="Mp",
                                   name=f"path{key}"))
    if inversion:
        maps.append(SpatialMap(tensor, (0, 0, 0), "P_node(0)"))
        if groups["paths"]:
            maps.append(_two_path_shift(tensor, groups, L))
    X = Composite(maps)
    X.name = name
    return X


def standard_maps(tensor, blocks, L: int) -> dict:
    """The declared discrete maps of REVERSOR_CHIRAL (layers/chiral.py)."""
    alg = pair_algebra("pair")
    W0, Jp, K, C = (alg[k].astype(np.int64) for k in ("W0", "Jp", "K", "C"))
    return {"R*": discrete_map(tensor, blocks, L, matter16=W0 @ Jp @ K, inversion=True, time_flip=True, name="R*"),
            "T_phys": discrete_map(tensor, blocks, L, matter16=C @ K, inversion=False, time_flip=True,
                                   name="T_phys=CK.Mp"),
            "boardT": discrete_map(tensor, blocks, L, matter16=Jp @ K, inversion=False, time_flip=True,
                                   name="boardT=J'K.Mp"),
            "CP": discrete_map(tensor, blocks, L, matter16=C @ W0, inversion=True, time_flip=False, name="CP"),
            "P": discrete_map(tensor, blocks, L, matter16=W0, inversion=True, time_flip=False, name="P"),
            "C": discrete_map(tensor, blocks, L, matter16=C, inversion=False, time_flip=False, name="C")}


__all__ = ["chiral_system", "gear_groups", "random_chiral_state", "jpure_seed", "j_minus_fraction", "discrete_map",
           "standard_maps"]
