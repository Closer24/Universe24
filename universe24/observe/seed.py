"""AUDIT MAP R* (Study 6 link/node-centred PT reversor) on the composed system, and seed checks. Read-only: returns NEW
states; never a stage of a forward run.

R* = spatial inversion x -> c2 - x (c2 = 2 x0 for the node seed, 2 x0 + e_y for S2*; a link gear of axis k is re-based:
base x -> c2 - x - e_k) composed with the time reversal:
  matter (16 Dirac-pair gears):  (a, b)_j(c2 - x) = Gamma_ji (b, a)_i(x)  (Gamma = J'K W0 signed permutation);
                                 r_j = R'(r_i) if Gamma_ji = +1, r_i if Gamma_ji = -1
  E1 A_d (link gears):           (a, b, r) -> (-b, -a, r) at the re-based mirrored link
  E1 Phi:                        (a, b, r) -> (-Phi_next, -b, r) at the mirrored node (staggered)
  every other gear:              (a, b, r) -> (b, a, rho(r)) at the mirrored storage node, rho = rhoL0 on ref.* at
                                 l0_offset 0, R' elsewhere (the vacuum-fixing time mirror; parity signs of the other
                                 layers are NOT declared: R* is declared exact only on the matter + E1 sector).
  L0 (RC2 BATCH 1, BANG-1 / Study 8 T10d(ii)): with ``body_signs`` given and the R' vacuum (l0_offset = Q - 1), L0's
                                 SIGNED RELABELLING S = chi o P (l0_relabelling) is composed in:
                                 (a, b)_P(g)(c2 - x) = chi_P(g) (b, a)_g(x), r -> R'(r) (chi = +1) or r (chi = -1).
                                 S solves S M_opp(d) S^-1 = M_d (L0's port matrices, both classes); without it the
                                 declared R* fails at t = 1 for L0-exciting seeds.
"""
from __future__ import annotations

import numpy as np

from ..core.engine import OBJ, State
from ..core.lattice import DIRECTIONS, lattice
from ..core.reversors import remainder_map
from ..core.tensor import Tensor


def _dest(L: int, c2, link: int | None) -> np.ndarray:
    lat = lattice(L)
    xyz = lat.all_coords()
    e = (0, 0, 0) if link is None else DIRECTIONS[2 * link]
    x = (c2[0] - xyz[:, 0] - e[0]) % L
    y = (c2[1] - xyz[:, 1] - e[1]) % L
    z = (c2[2] - xyz[:, 2] - e[2]) % L
    return ((x * L + y) * L + z).astype(np.intp)


_L0_REL = {}


def l0_relabelling(body_signs=(1, -1, 1)) -> dict:
    """L0's signed relabelling S = chi o P with S M_opp(d) S^-1 = M_d for all six directions (M_d[ports_d(g), g] =
    weights_d(g), universe24's coupling of these body signs, read-only). All solutions are found (BFS on P(0), parity
    2-colouring for chi); RULE: minimal order among the solutions with a +1 eigenspace, tie -> smallest P(0).
    Returns {"P": [...], "chi": [...] (chi indexed by the IMAGE label), "order", "fixed_dim", "n_solutions"}."""
    key = tuple(body_signs)
    if key in _L0_REL:
        return _L0_REL[key]
    from universe24.algebra.coupling import coupling
    C = coupling(key)
    pi = [list(C.ports[d]) for d in range(6)]
    w = [list(C.weights[d]) for d in range(6)]
    opp = {d: [k for k, f in enumerate(DIRECTIONS) if tuple(-x for x in e) == tuple(f)][0]
           for d, e in enumerate(DIRECTIONS)}
    sols = []
    for k in range(48):
        P = [-1] * 48
        P[0] = k
        stack, ok = [0], True
        while stack and ok:
            g = stack.pop()
            for d in range(6):
                h, val = pi[opp[d]][g], pi[d][P[g]]
                if P[h] == -1:
                    P[h] = val
                    stack.append(h)
                elif P[h] != val:
                    ok = False
                    break
        if not ok or -1 in P or len(set(P)) != 48:
            continue
        cons = {}
        for d in range(6):
            for g in range(48):
                a_, b_ = P[pi[opp[d]][g]], P[g]
                sgn = w[opp[d]][g] * w[d][P[g]]
                cons.setdefault(a_, []).append((b_, sgn))
                cons.setdefault(b_, []).append((a_, sgn))
        chi = [0] * 48
        chi[P[0]] = 1
        q, good = [P[0]], True
        while q:
            x = q.pop()
            for y, sgn in cons.get(x, []):
                want = chi[x] * sgn
                if chi[y] == 0:
                    chi[y] = want
                    q.append(y)
                elif chi[y] != want:
                    good = False
        if not good or 0 in chi:
            continue
        S = np.zeros((48, 48), dtype=np.int64)
        for g in range(48):
            S[P[g], g] = chi[P[g]]
        order = next(n for n in range(1, 49) if np.array_equal(np.linalg.matrix_power(S, n), np.eye(48, dtype=np.int64)))
        fixed = int(np.sum(np.abs(np.linalg.eigvals(S.astype(float)) - 1) < 1e-9))
        sols.append({"P": P, "chi": chi, "order": order, "fixed_dim": fixed, "S": S})
    good = [x for x in sols if x["fixed_dim"] > 0]
    best = min(good, key=lambda x: (x["order"], x["P"][0]))
    best = {**best, "n_solutions": len(sols)}
    _L0_REL[key] = best
    return best


def r_star(state: State, tensor: Tensor, Q: int, c2, l0_offset: int = 0, matter_ns: str = "matter",
           em_ns: str | None = "em", body_signs=None) -> State:
    from ..layers.matter import matter_names
    from ..prepare.seed import gamma_matrix
    D = 6 * Q
    L = state.L
    a, b, r = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
    na, nb, nr = a.copy(), b.copy(), r.copy()
    names = tensor.names
    rel = (l0_relabelling(body_signs) if (body_signs is not None and l0_offset != 0
                                          and any(n.startswith("ref.") for n in names)) else None)
    mrows = [tensor.gear_index(f"{matter_ns}.{n}") for n in matter_names("pair")] if any(
        n.startswith(matter_ns + ".") for n in names) else []
    mset = set(mrows)
    em_rows = {}
    if em_ns and any(n.startswith(em_ns + ".") for n in names):
        for nm in ("A_x", "A_y", "A_z", "Phi"):
            em_rows[tensor.gear_index(f"{em_ns}.{nm}")] = nm
    if em_rows:
        from .em import phi_next
        pn = np.asarray(phi_next(state, tensor, em_ns), dtype=object).reshape(-1)
    for g, gt in enumerate(tensor.gears):
        if g in mset:
            continue
        dst = _dest(L, c2, gt.link)
        if g in em_rows:
            if em_rows[g] == "Phi":
                va, vb, vr = -pn, -b[g], r[g]
            else:
                va, vb, vr = -b[g], -a[g], r[g]
        else:
            ns = gt.name.split(".", 1)[0]
            if ns == "ref" and rel is not None:
                continue                                  # L0 with its signed relabelling (below)
            rm = "rhoL0" if (ns == "ref" and l0_offset == 0) else "Mp"
            va, vb, vr = b[g], a[g], remainder_map(rm, r[g], D)
        na[g, dst], nb[g, dst], nr[g, dst] = va, vb, vr
    if rel is not None:
        dst = _dest(L, c2, None)
        for h in range(48):
            g = tensor.gear_index(f"ref.R{h:02d}")
            gp = tensor.gear_index(f"ref.R{rel['P'][h]:02d}")
            if rel["chi"][rel["P"][h]] > 0:
                na[gp, dst], nb[gp, dst], nr[gp, dst] = b[g], a[g], remainder_map("Mp", r[g], D)
            else:
                na[gp, dst], nb[gp, dst], nr[gp, dst] = -b[g], -a[g], r[g]
    if mrows:
        G = gamma_matrix()
        dst = _dest(L, c2, None)
        for j in range(16):
            (i,) = np.flatnonzero(G[j])
            s = int(G[j, i])
            na[mrows[j], dst] = s * b[mrows[i]]
            nb[mrows[j], dst] = s * a[mrows[i]]
            nr[mrows[j], dst] = remainder_map("Mp", r[mrows[i]], D) if s > 0 else r[mrows[i]]
    return State(L, na, nb, nr)


def non_vacuum_count(state: State, vac: State) -> int:
    return int(np.count_nonzero(state.a.astype(OBJ) != vac.a.astype(OBJ)) +
               np.count_nonzero(state.b.astype(OBJ) != vac.b.astype(OBJ)) +
               np.count_nonzero(state.r.astype(OBJ) != vac.r.astype(OBJ)))


__all__ = ["r_star", "non_vacuum_count", "l0_relabelling"]


# ------------------------------------------------------------------ RC2 BATCH 4: R* with HANDS ON (chiral + EW)
def r_star_hands_on(system, tensor: Tensor, c2, L: int):
    """R* of the hands-ON system as ONE composite of core building blocks (the chiral layer's inversion maps about the
    SAME centre c2 composed with the integrator's maps): Phi (a, b, r) -> (-Phi_next, -b, r) (original state), M' on every
    other gear, A_d negated (net (-b, -a, r)), both pairs Gamma = W0 J' K, Higgs sig, W links / 2-paths sig o conj,
    L0's signed relabelling S, then the inversion x -> c2 - x (links re-based) and the 2-path reversal of the W links.
    Requires the chiral layer (matter2, wsu2, chiral), E1 and the R' vacuum (l0_offset = Q - 1)."""
    from ..core.reversors import Composite, FunctionMap, GearwiseMap, GroupLinearMap, SpatialMap
    from ..layers.matter import algebra as pair_algebra
    from ..observe.system import _chiral_linear
    from .em import phi_next
    Q = system.Q
    D = 6 * Q
    alg = pair_algebra("pair")
    Gam = alg["W0"].astype(np.int64) @ alg["Jp"].astype(np.int64) @ alg["K"].astype(np.int64)
    p = tensor.gear_index("em.Phi")

    def phi_r(state: State) -> State:
        a, b, r = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
        nxt = np.asarray(phi_next(state, tensor, "em"), dtype=object).reshape(-1)
        a[p], b[p] = -nxt, -b[p]
        return State(state.L, a, b, r)
    maps = [FunctionMap(phi_r, "Phi->(-Phi_next,-b,r)"),
            GearwiseMap(tensor, Q, {"em.Phi": "id"}, default="Mp"),
            GroupLinearMap(tensor, Q, [f"em.A_{c}" for c in "xyz"], [[-1, 0, 0], [0, -1, 0], [0, 0, -1]], neg_r="Mp",
                           name="-A")]
    lin, groups = _chiral_linear(system, tensor, Q, Gam, inversion=True)
    maps += lin
    rel = l0_relabelling(system.info["body_signs"])
    maps.append(GroupLinearMap(tensor, Q, [f"ref.R{h:02d}" for h in range(48)],
                               [[int(v) for v in row] for row in rel["S"]], neg_r="Mp", name="L0 S"))
    maps.append(SpatialMap(tensor, tuple(c2), f"x -> {tuple(c2)} - x"))
    if groups["paths"]:
        from ..prepare.chiral import _two_path_shift
        maps.append(_two_path_shift(tensor, groups, L))
    X = Composite(maps)
    X.name = "R*_on"
    return X


__all__ = __all__ + ["r_star_hands_on"]
