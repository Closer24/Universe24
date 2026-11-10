"""INTEGRATOR read-only observables and AUDIT maps for the composed default system (layers/system.py).

Nothing here changes a state in place or feeds back into a run. The joint mirror is an audit map built from the
layers' DECLARED reversors (data), never a stage of the forward evolution.
"""
from __future__ import annotations

from collections import Counter

import numpy as np

from ..core.engine import OBJ, State
from ..core.reciprocity import check_reciprocity
from ..core.reversors import FunctionMap, GearwiseMap, remainder_map
from ..core.tensor import Tensor

MATTER_NS, EM_NS, OD2_NS = "matter", "em", "od2"


def joint_mirror(system, tensor: Tensor, dirac: str = "KMp"):
    """The declared JOINT reversor X and its central element N (X F^n X F^n = N):
    ref.*: rhoL0 (l0_offset 0) or M' (l0_offset Q-1); Dirac matter: K o M' (dirac="KMp", Kramers) with E1's staggered
    Phi map when em = "e1"; od2: the OD2 staggered map (hij M', h0i (a,b) -> (-h0i_next, -b), h00 (a,b) ->
    (h00(t+2), h00(t+1)), r kept); every other (b-only) gear: M'. N = Jp on the matter gears (K^2 = -1), identity
    elsewhere. dirac="Mp": plain M' on the matter too (a control; E1 needs K)."""
    from ..prepare.em import x_reversor_core
    Q = system.Q
    D = 6 * Q
    names = tensor.names
    em = system.info.get("em")
    off = system.info.get("l0_offset", 0)
    has_matter = any(n.startswith(MATTER_NS + ".") for n in names)
    has_od2 = any(n.startswith(OD2_NS + ".") for n in names)
    choices = {}
    for n in names:
        ns = n.split(".", 1)[0]
        if ns == "ref":
            choices[n] = "rhoL0" if off == 0 else "Mp"
        elif ns == MATTER_NS and has_matter and dirac == "KMp":
            continue
        elif ns == EM_NS and em in ("e1", "e1d") and dirac == "KMp":
            continue
        elif ns == OD2_NS:
            continue
        else:
            choices[n] = "Mp"
    X = GearwiseMap(tensor, Q, choices)
    N = GearwiseMap(tensor, Q, {})
    if has_matter and dirac == "KMp":
        if em in ("e1", "e1d"):
            Xem, KM, N = x_reversor_core(tensor, Q, MATTER_NS, EM_NS, "Mp")
        else:
            KM, _, N = x_reversor_core(tensor, Q, MATTER_NS, None, "Mp")
            Xem = KM
        X = Xem @ X
    if has_od2:
        from .gravity import od2_staggered_reversor
        Xs = od2_staggered_reversor(tensor, Q, OD2_NS, {})
        hij = [tensor.gear_index(n) for n in names if n.startswith(OD2_NS + ".h") and not n.startswith(OD2_NS + ".h0")]

        def od2_map(state: State) -> State:
            out = Xs(state)
            r = out.r.astype(OBJ)
            for k in hij:                      # hij: M' (R') instead of the plain M, so the joint vacuum is fixed
                r[k] = remainder_map("Mp", state.r[k].astype(OBJ), D)
            return State(state.L, out.a, out.b, r)
        X = FunctionMap(od2_map, "OD2 staggered (hij M')") @ X
    return X, N


def mirror_check(engine, X, N, s0: State, n: int) -> bool:
    """X F^n X F^n (s0) == N(s0)."""
    return X(engine.run(X(engine.run(s0, n)), n)).same_as(N(s0))


def designation_report(tensor: Tensor) -> dict:
    rep = check_reciprocity(tensor)
    counts = Counter(why for _, why in rep.designated)
    return {"ok": rep.ok, "checked": rep.checked, "skipped_constants": rep.skipped_constants,
            "skipped_two_time": rep.skipped_two_time, "n_designated": len(rep.designated),
            "designations": dict(counts), "violations": rep.violations[:20],
            "missing_partners": rep.missing_partners[:20]}


def census(tensor: Tensor) -> dict:
    """Per namespace: monomials by degree, designated degree-3, undesignated degree-3, a-read monomials, constants,
    support violations."""
    out = {}
    supp = {id(m) for m in tensor.support_violations()}
    for m in tensor.monomials:
        ns = tensor.names[m.target].split(".", 1)[0]
        c = out.setdefault(ns, {"by_degree": [0, 0, 0, 0], "deg3_designated": 0, "deg3_force": 0, "a_reads": 0,
                                "constants": 0, "support_wider_than_link": 0, "deg3_force_targets": set()})
        c["by_degree"][m.degree] += 1
        if m.degree == 3:
            if tensor.is_designated(m):
                c["deg3_designated"] += 1
            else:
                c["deg3_force"] += 1
                c["deg3_force_targets"].add(tensor.names[m.target].split(".", 1)[1].split("_")[0])
        if any(f.field == "a" for f in m.factors):
            c["a_reads"] += 1
        if m.degree == 0:
            c["constants"] += 1
        if id(m) in supp:
            c["support_wider_than_link"] += 1
    for v in out.values():
        v["deg3_force_targets"] = sorted(v["deg3_force_targets"])
    return out


def collisions(system, tensor: Tensor) -> dict:
    """(i) canonical monomials that are BOTH designated and undesignated (a designated read coinciding with a force
    monomial); (ii) canonical monomials written by two different blocks (coefficients merged)."""
    seen: dict = {}
    for blk in system.blocks:
        for t in blk.terms:
            target, coeff, factors = t[0], t[1], t[2]
            q = (blk.qualify(target), coeff, tuple((blk.qualify(f[0]), f[1], f[2]) for f in factors))
            m = tensor._parse(q)
            key = (m.target, m.factors)
            des = len(t) > 3 and bool(t[3])
            seen.setdefault(key, set()).add((blk.name, des))
    both = [k for k, v in seen.items() if {d for _, d in v} == {True, False}]
    multi = [k for k, v in seen.items() if len({b for b, _ in v}) > 1]
    names = tensor.names

    def txt(k):
        return f"u[{names[k[0]]}] <- " + " * ".join(f"{f.field}[{names[f.gear]}]{f.offset}" for f in k[1])
    return {"designated_and_force": len(both), "designated_and_force_examples": [txt(k) for k in both[:10]],
            "written_by_several_blocks": len(multi),
            "written_by_several_blocks_examples": [(txt(k), sorted(seen[k])) for k in multi[:10]]}


def dressed_continuity_residual(before: State, after: State, tensor: Tensor, D: int, matter_params: dict, P: int,
                                lapse: str = "metric.h00", beta: str | None = "beta.G", ns: str = "matter"):
    """rho(after) - rho(before) + div(f_d j_d)(before) - R with the lapse/beta link factor
    f_d = 1 - (F_x + F_y)/(2P) + (9/16)(G_x + G_y)/P (exact Fractions; 0 at every node iff exact)."""
    from fractions import Fraction
    from . import em as oem
    from .gravity import arr
    js = oem.link_currents(before, tensor, matter_params, ns)
    F = arr(before, tensor, lapse, "b").astype(object)
    G = arr(before, tensor, beta, "b").astype(object) if beta else 0 * F
    fj = []
    for d in range(3):
        Fn, Gn = np.roll(F, -1, axis=d), np.roll(G, -1, axis=d)
        f = 1 - (F + Fn) * Fraction(1, 2 * P) + (G + Gn) * Fraction(9, 16 * P)
        fj.append(f * np.asarray(js[d], dtype=object))
    div = sum(fj[d] - np.roll(fj[d], 1, axis=d) for d in range(3))
    sp = matter_params.get("species", "pair")
    return (np.asarray(oem.density(after, tensor, D, ns, "Jp", sp), dtype=object)
            - np.asarray(oem.density(before, tensor, D, ns, "Jp", sp), dtype=object) + div
            - np.asarray(oem.remainder_term(before, after, tensor, ns, "Jp", sp), dtype=object))


__all__ = ["joint_mirror", "mirror_check", "designation_report", "census", "collisions",
           "dressed_continuity_residual"]


# ------------------------------------------------------------------ RC2 BATCH 4: mirrors with HANDS ON (chiral + EW)
def _chiral_groups(system, tensor):
    from ..prepare.chiral import gear_groups
    return gear_groups(tensor, [system.by_name("matter"), system.by_name("matter2"), system.by_name("wsu2"),
                                system.by_name("chiral")])


def _chiral_linear(system, tensor, Q: int, matter16, inversion: bool) -> list:
    """The chiral layer's linear maps (prepare/chiral.discrete_map, read-only building blocks): both pairs matter16,
    Higgs sig, W links / 2-paths sig (o conj under inversion); neg_r = Mp (applied after the time flip)."""
    from ..core.reversors import GroupLinearMap
    from ..prepare.chiral import _sigma
    groups = _chiral_groups(system, tensor)
    Gam32 = np.kron(np.eye(2, dtype=np.int64), np.asarray(matter16, dtype=np.int64))
    sig = _sigma(Gam32)
    sigL = sig @ np.diag([1, -1, -1, -1]).astype(np.int64) if inversion else sig
    tolist = lambda M: [[int(v) for v in row] for row in M]
    maps = [GroupLinearMap(tensor, Q, groups["matter"] + groups["partner"], tolist(Gam32), neg_r="Mp", name="pairs"),
            GroupLinearMap(tensor, Q, groups["higgs"], tolist(sig), neg_r="Mp", name="higgs")]
    for k in range(3):
        maps.append(GroupLinearMap(tensor, Q, groups["links"][k], tolist(sigL), neg_r="Mp", name=f"W{k}"))
    for key, gl in groups["paths"].items():
        maps.append(GroupLinearMap(tensor, Q, gl, tolist(sigL), neg_r="Mp", name=f"P{key}"))
    return maps, groups


def joint_mirror_hands_on(system, tensor: Tensor):
    """The full-system time mirror with HANDS ON (chiral + electroweak): T_phys = C K o M' of the chiral layer extended by
    E1 composed with the C-flip of its fields: Phi (a, b, r) -> (+Phi_next, +b, R'(r)) (read on the ORIGINAL state),
    M' on every other gear, A_d negated after M' (net (-b, -a, r)), then the chiral linear maps (both pairs C K; Higgs,
    W links, 2-paths sig). Returns (X, N) with N = X o X (the Kramers central element)."""
    from ..core.reversors import Composite, FunctionMap, GearwiseMap, GroupLinearMap
    from ..layers.matter import algebra as pair_algebra
    from .em import phi_next
    Q = system.Q
    alg = pair_algebra("pair")
    CK = alg["C"].astype(np.int64) @ alg["K"].astype(np.int64)
    has_e1 = system.info.get("em") in ("e1", "e1d")
    p = tensor.gear_index(f"{EM_NS}.Phi") if has_e1 else None

    def phi_c(state: State) -> State:
        a, b, r = state.a.astype(OBJ), state.b.astype(OBJ), state.r.astype(OBJ)
        nxt = np.asarray(phi_next(state, tensor, EM_NS), dtype=object).reshape(-1)
        a[p], b[p], r[p] = nxt, b[p].copy(), remainder_map("Mp", r[p], 6 * Q)
        return State(state.L, a, b, r)
    lin, _ = _chiral_linear(system, tensor, Q, CK, inversion=False)
    choices = {f"{EM_NS}.Phi": "id"} if has_e1 else {}
    if system.info.get("l0_offset", 0) == 0:
        choices.update({n: "rhoL0" for n in tensor.names if n.startswith("ref.")})
    maps = [FunctionMap(phi_c, "Phi->(+Phi_next,+b,R')")] if has_e1 else []
    maps.append(GearwiseMap(tensor, Q, choices, default="Mp"))
    if has_e1:
        anames = [f"{EM_NS}.A_{c}" for c in "xyz"]
        maps.append(GroupLinearMap(tensor, Q, anames, [[-1, 0, 0], [0, -1, 0], [0, 0, -1]], neg_r="Mp", name="-A"))
    X = Composite(maps + lin)
    X.name = "X_on = T_phys(C K o M') + E1 (C-flipped staggered) + M' elsewhere"
    return X, Composite([X, X])
