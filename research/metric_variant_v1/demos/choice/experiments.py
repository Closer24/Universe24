"""CHOICE layer experiments (B1-CHOICE): compose blocks (layers/choice.py), prepare declared initial data
(prepare/choice.py), run the core Engine, read outcomes passively (observe/choice.py), rewind exactly.

Each ``exp_*`` returns a JSON-serialisable dict; fractions are exact (``str(Fraction)``). The ensembles are laid on
the lattice: on-site constructions are independent copies at every node, fibre constructions independent copies on
every (y, z) line; every copy carries its own declared hidden data. Used by tests/test_choice.py and run_demos.py.
"""
from __future__ import annotations

import itertools
import math
from collections import Counter, defaultdict
from fractions import Fraction as Fr

import numpy as np

from ...core import Engine, check_reciprocity, compose
from ...core.reversors import reversor_check, uniform
from ...layers.choice import (build_backaction_router, build_born_router, build_clock_ring, build_common_drive,
                              build_dec_toy, build_f7, build_fibre, build_gated_pair, build_parallel_router,
                              build_sequential_router, build_spring_backaction_router, build_which_path_W)
from ...observe.choice import bit_gate, click_flags, harmonic_V, kinds, mutual_info, official, quotient, values
from ...prepare.choice import Prep, pair4_state, ring_b, ring_state, yz_lines


def _cube(n: int) -> int:
    L = 3
    while L ** 3 < n:
        L += 1
    return L


def _rewind_ok(eng, hist):
    return eng.rewind(hist[-1], len(hist) - 1).same_as(hist[0])


def _fs(x):
    return str(Fr(x))


def _arms(Q, period=6):
    a1 = build_clock_ring(Q=Q, period=period, prefix="X", name="arm1")
    a2 = build_clock_ring(Q=Q, period=period, prefix="X", name="arm2")
    n = 3 if period == 6 else 2
    return a1, a2, tuple(f"arm1.X{j}" for j in range(n)), tuple(f"arm2.X{j}" for j in range(n))


def _set_ring(pr, arm, nodes, A, phases, t=0):
    """write rings of amplitude A and per-node phases (array) at ``nodes`` (table lookup, exact ints)."""
    ph = np.asarray(phases, dtype=np.int64) % 6
    tab = [ring_state(A, p, t) for p in range(6)]
    for j in range(3):
        ta = np.array([tab[p][j][0] for p in range(6)], dtype=object)
        tb = np.array([tab[p][j][1] for p in range(6)], dtype=object)
        pr.set(arm[j], nodes, a=ta[ph], b=tb[ph])


def recip_summary(T):
    rep = check_reciprocity(T)
    return {"ok": rep.ok, "checked": rep.checked, "designated": len(rep.designated),
            "justifications": sorted({why for _, why in rep.designated}), "violations": len(rep.violations),
            "two_time_skipped": rep.skipped_two_time, "rank": T.rank, "support_violations": len(T.support_violations()),
            "a_read_monomials": [f"u[{T.names[m.target]}] += {m.coeff} * " +
                                 " * ".join(f"{f.field}[{T.names[f.gear]}]{f.offset}" for f in m.factors)
                                 for m in T.monomials if any(f.field == "a" for f in m.factors)]}


# =============================================================================================== TC.1 carriers
def exp_carriers():
    out = {"ring": [], "pair4": [], "fibre": []}
    for Q in (1, 3, 8):
        blk = build_clock_ring(Q=Q, name="ring")
        T = compose(blk)
        eng = Engine(T, Q)
        L = 3
        for A in (1, 2, 5):
            pr = Prep(T, Q, L, blk)
            nodes = np.arange(27)
            _set_ring(pr, ("ring.X0", "ring.X1", "ring.X2"), nodes, A, nodes % 6)
            hist = eng.run(pr.state(), 12, history=True)
            ok_b = all(np.array_equal(values(hist[t], T, f"ring.X{j}"), np.array([ring_b(A, int(p), t)[j]
                                                                                   for p in nodes % 6]))
                       for t in range(13) for j in range(3))
            r0 = all(int(np.max(np.abs(hist[t].r.astype(np.int64)))) == 0 for t in range(13))
            inv = all(set((sum(values(hist[t], T, f"ring.X{j}") ** 2 for j in range(3))).tolist()) == {2 * A * A}
                      for t in range(13))
            kc = set()
            for t in range(12):
                for j in range(3):
                    fl = official(T, 6 * Q, hist[t], hist[t + 1], f"ring.X{j}")
                    kc |= set(kinds(T, 6 * Q, hist[t], hist[t + 1], f"ring.X{j}")[fl].tolist())
            out["ring"].append({"Q": Q, "A": A, "exact_period6": ok_b, "remainder_0": r0, "sum_b2_2A2": inv,
                                "click_kinds": sorted(kc), "rewind": _rewind_ok(eng, hist)})
        blk4 = build_clock_ring(Q=Q, period=4, name="pair")
        T4 = compose(blk4)
        e4 = Engine(T4, Q)
        pr = Prep(T4, Q, 3, blk4)
        for j, (a, b) in enumerate(pair4_state(1, 0)):
            pr.set(f"pair.X{j}", np.arange(27), a=a, b=b)
        h4 = e4.run(pr.state(), 8, history=True)
        out["pair4"].append({"Q": Q, "period4": h4[4].same_as(h4[0]) and not h4[2].same_as(h4[0]),
                             "rewind": _rewind_ok(e4, h4)})
        out.setdefault("recip", {})[f"ring_Q{Q}"] = recip_summary(T)
    rng = np.random.default_rng(7)
    for Q in (1, 3):
        blk = build_fibre(Q=Q, axis=0, components=("F",), name="fib")
        T = compose(blk)
        eng = Engine(T, Q)
        L = 8
        pr = Prep(T, Q, L, blk)
        lines = yz_lines(L, L * L)
        g = {}
        for (y, z) in lines:
            prof = [int(v) for v in rng.integers(-9, 10, 7)] + [0]
            g[(y, z)] = prof
            for x in range(L):
                n = pr.node(x, y, z)
                pr.set("fib.F", [n], a=[prof[(x + 1) % L]], b=[prof[x % L]])
        hist = eng.run(pr.state(), 2 * L, history=True)
        exact = True
        for t in range(2 * L + 1):
            bt = values(hist[t], T, "fib.F")
            for (y, z), prof in g.items():
                for x in range(L):
                    if bt[pr.node(x, y, z)] != prof[(x - t) % L]:
                        exact = False
        r0 = all(int(np.max(np.abs(h.r.astype(np.int64)))) == 0 for h in hist)
        kc = set()
        for t in range(2 * L):
            fl = official(T, 6 * Q, hist[t], hist[t + 1], "fib.F")
            kc |= set(kinds(T, 6 * Q, hist[t], hist[t + 1], "fib.F")[fl].tolist())
        out["fibre"].append({"Q": Q, "L": L, "exact_transport_2L": exact, "remainder_0": r0, "click_kinds": sorted(kc),
                             "rewind": _rewind_ok(eng, hist)})
        out["recip"][f"fibre_Q{Q}"] = recip_summary(T)
    return out


# =============================================================================================== TC.2/3/4 router
def router_system(A, form="opposite", kappa=3, Q=None):
    Q = 8 * A * A if Q is None else Q
    a1, a2, X1, X2 = _arms(Q)
    rt = build_born_router(Q=Q, kappa=kappa, arm1=X1, arm2=X2, form=form, name="router")
    T = compose(a1, a2, rt)
    return T, (a1, a2, rt), X1, X2, Q


def _router_prep(T, blocks, Q, A, X1, X2, s_arr, lamP, lamM, n_used):
    L = _cube(n_used)
    pr = Prep(T, Q, L, *blocks)
    nodes = np.arange(n_used)
    _set_ring(pr, X1, nodes, A, np.zeros(n_used, dtype=int))
    _set_ring(pr, X2, nodes, A, s_arr)
    pr.set("router.dP", nodes, r=lamP)
    pr.set("router.dM", nodes, r=lamM)
    return pr, nodes


def _intens(hist_t, T, X1, X2, nodes):
    x = [values(hist_t, T, g, nodes=nodes) for g in X1]
    y = [values(hist_t, T, g, nodes=nodes) for g in X2]
    Ip = sum((x[j] + y[j]) ** 2 for j in range(3))
    Im = sum((x[j] - y[j]) ** 2 for j in range(3))
    return Ip, Im


def exp_router(A, form, steps=12, mirror=False):
    T, blocks, X1, X2, Q = router_system(A, form)
    D = 6 * Q
    eng = Engine(T, Q)
    n = 6 * D
    s_arr = np.repeat(np.arange(6), D)
    lam = np.tile(np.arange(D), 6)
    lamM = lam if form == "opposite" else D - 1 - lam
    pr, nodes = _router_prep(T, blocks, Q, A, X1, X2, s_arr, lam, lamM, n)
    hist = eng.run(pr.state(), steps, history=True)
    rows = []
    static = True
    for t in range(steps + 1):
        Ip, Im = _intens(hist[t], T, X1, X2, nodes)
        for s in range(6):
            sel = s_arr == s
            if len(set(Ip[sel].tolist())) != 1 or len(set(Im[sel].tolist())) != 1:
                static = False
    Ip0, Im0 = _intens(hist[0], T, X1, X2, nodes)
    one_per_update = True
    equal_r = True
    for t in range(steps):
        cp = official(T, D, hist[t], hist[t + 1], "router.dP", nodes)
        cm = official(T, D, hist[t], hist[t + 1], "router.dM", nodes)
        qp = quotient(T, hist[t], hist[t + 1], "router.dP", nodes)
        qm = quotient(T, hist[t], hist[t + 1], "router.dM", nodes)
        if not np.all(cp ^ cm):
            one_per_update = False
        if form == "opposite":
            rp = values(hist[t + 1], T, "router.dP", "r", nodes)
            rm = values(hist[t + 1], T, "router.dM", "r", nodes)
            equal_r &= bool(np.array_equal(rp, rm))
            if not (set(qp[cp].tolist()) <= {1} and set(qm[cm].tolist()) <= {-1}):
                one_per_update = False
        if t == 0:
            for s in range(6):
                sel = s_arr == s
                rows.append({"s": s, "I+": int(Ip0[sel][0]), "I-": int(Im0[sel][0]),
                             "P(d+)": _fs(Fr(int(cp[sel].sum()), D)), "P(d-)": _fs(Fr(int(cm[sel].sum()), D)),
                             "both": int((cp & cm)[sel].sum()), "none": int((~cp & ~cm)[sel].sum()),
                             "kinds_d+": sorted(set(kinds(T, D, hist[0], hist[1], "router.dP", nodes)[sel & cp]
                                                    .tolist())),
                             "kinds_d-": sorted(set(kinds(T, D, hist[0], hist[1], "router.dM", nodes)[sel & cm]
                                                    .tolist()))})
    res = {"A": A, "form": form, "Q": Q, "D": D, "rows": rows, "I_static": static, "one_click_per_update": one_per_update,
           "rewind": _rewind_ok(eng, hist), "recip": recip_summary(T)}
    if form == "opposite":
        res["r_plus_eq_r_minus_every_update"] = equal_r
    if mirror:
        M = uniform(T, Q, "M")
        n7 = 7
        hb = hist[:n7 + 1]
        m = eng.run(M(hb[-1]), n7, history=True)
        same = True
        for k in range(n7):
            for gname in ("router.dP", "router.dM"):
                f_fl = official(T, D, hb[n7 - 1 - k], hb[n7 - k], gname, nodes)
                m_fl = official(T, D, m[k], m[k + 1], gname, nodes)
                f_k = kinds(T, D, hb[n7 - 1 - k], hb[n7 - k], gname, nodes)
                m_k = kinds(T, D, m[k], m[k + 1], gname, nodes)
                f_q = quotient(T, hb[n7 - 1 - k], hb[n7 - k], gname, nodes)
                m_q = quotient(T, m[k], m[k + 1], gname, nodes)
                same &= bool(np.array_equal(f_fl, m_fl) and np.array_equal(f_k[f_fl], m_k[m_fl])
                             and np.array_equal(f_q[f_fl], m_q[m_fl]))
        res["mirror_M_F7_M_F7_id"] = M(m[-1]).same_as(hb[0])
        res["mirror_log_reversed_same_kinds"] = same
    return res


def exp_grangier(A):
    out = {"A": A, "rows": []}
    for form in ("mirror", "opposite"):
        T, blocks, X1, X2, Q = router_system(A, form)
        D = 6 * Q
        eng = Engine(T, Q)
        n = 6 * D * D
        s_arr = np.repeat(np.arange(6), D * D)
        lp = np.tile(np.repeat(np.arange(D), D), 6)
        lm = np.tile(np.tile(np.arange(D), D), 6)
        pr, nodes = _router_prep(T, blocks, Q, A, X1, X2, s_arr, lp, lm, n)
        s0 = pr.state()
        s1 = eng.step(s0)
        cp = official(T, D, s0, s1, "router.dP", nodes)
        cm = official(T, D, s0, s1, "router.dM", nodes)
        for s in range(6):
            sel = s_arr == s
            N = D * D
            Pp, Pm, Pb = Fr(int(cp[sel].sum()), N), Fr(int(cm[sel].sum()), N), Fr(int((cp & cm)[sel].sum()), N)
            Pn = Fr(int((~cp & ~cm)[sel].sum()), N)
            out["rows"].append({"form": form, "tokens": "independent", "s": s, "P+": _fs(Pp), "P-": _fs(Pm),
                                "P(both)": _fs(Pb), "P(none)": _fs(Pn),
                                "alpha": _fs(Pb / (Pp * Pm)) if Pp * Pm else None})
        out[f"rewind_{form}"] = eng.inverse_step(s1).same_as(s0)
    return out


def exp_mismatch():
    A, Q = 1, 8
    D = 6 * Q
    rows = []
    for kappa in (1, 2, 3, 4):
        T, blocks, X1, X2, _ = router_system(A, "opposite", kappa=kappa, Q=Q)
        eng = Engine(T, Q)
        n = 6 * D
        s_arr = np.repeat(np.arange(6), D)
        lam = np.tile(np.arange(D), 6)
        pr, nodes = _router_prep(T, blocks, Q, A, X1, X2, s_arr, lam, lam, n)
        s0 = pr.state()
        s1 = eng.step(s0)
        cp = official(T, D, s0, s1, "router.dP", nodes)
        cm = official(T, D, s0, s1, "router.dM", nodes)
        Ip, Im = _intens(s0, T, X1, X2, nodes)
        for s in range(6):
            sel = s_arr == s
            ip, im = int(Ip[sel][0]), int(Im[sel][0])
            Kp, Km = 2 * kappa * ip, 2 * kappa * im
            if max(Kp, Km) > D:
                continue
            S = Kp + Km
            both, none = int((cp & cm)[sel].sum()), int((~cp & ~cm)[sel].sum())
            one = int((cp ^ cm)[sel].sum())
            cond = Fr(int((cp & ~cm)[sel].sum()), one) if one else None
            rows.append({"kappa": kappa, "s": s, "S": S, "D": D, "P(both)": _fs(Fr(both, D)),
                         "pred_both": _fs(Fr(max(0, S - D), D)), "P(none)": _fs(Fr(none, D)),
                         "pred_none": _fs(Fr(max(0, D - S), D)), "P(+|one)": _fs(cond) if cond is not None else None,
                         "I+/(I++I-)": _fs(Fr(ip, ip + im)), "rewind": eng.inverse_step(s1).same_as(s0)})
    return {"rows": rows}


# =============================================================================================== TC.5 token
def exp_token():
    A, Q = 1, 8
    D = 6 * Q
    out = {}
    # (a) common drive, light off
    a1, a2, X1, X2 = _arms(Q)
    rt = build_born_router(Q=Q, kappa=3, arm1=X1, arm2=X2, form="opposite", name="router")
    dr = build_common_drive(Q=Q, w=5, detectors=("router.dP", "router.dM"), name="drive")
    T = compose(a1, a2, rt, dr)
    eng = Engine(T, Q)
    pr = Prep(T, Q, 3, a1, a2, rt, dr)
    pr.set("drive.S", [0], a=1, b=1)
    hist = eng.run(pr.state(), 2 * D, history=True)
    rp = [int(values(h, T, "router.dP", "r")[0]) for h in hist]
    rm = [int(values(h, T, "router.dM", "r")[0]) for h in hist]
    births = rp[:D // 2]
    out["drive"] = {"w": 5, "c": 1, "K_per_update": 10, "r+ == r- every update": rp == rm,
                    "visited_over_24_birth_times": sorted(births) == list(range(0, D, 2)),
                    "both_detectors_identical": all(values(h, T, "router.dP", "b")[0] == values(h, T, "router.dM", "b")[0]
                                                    for h in hist),
                    "rewind": _rewind_ok(eng, hist), "recip": recip_summary(T)}
    # (b) unstaged exposure, detectors born at the vacuum with equal remainder r0
    T, blocks, X1, X2, _ = router_system(A, "opposite")
    eng = Engine(T, Q)
    n = 6 * D
    s_arr = np.repeat(np.arange(6), D)
    r0 = np.tile(np.arange(D), 6)
    pr, nodes = _router_prep(T, blocks, Q, A, X1, X2, s_arr, r0, r0, n)
    steps = 2 * D
    hist = eng.run(pr.state(), steps, history=True)
    eq = True
    one = True
    plus = []
    for t in range(steps):
        cp = official(T, D, hist[t], hist[t + 1], "router.dP", nodes)
        cm = official(T, D, hist[t], hist[t + 1], "router.dM", nodes)
        one &= bool(np.all(cp ^ cm))
        eq &= bool(np.array_equal(values(hist[t + 1], T, "router.dP", "r", nodes),
                                  values(hist[t + 1], T, "router.dM", "r", nodes)))
        plus.append(cp.astype(np.int64))
    plus = np.array(plus)
    Ip, Im = _intens(hist[0], T, X1, X2, nodes)
    windows_ok = all(np.array_equal(plus[t0:t0 + D].sum(0), 6 * Ip) for t0 in range(steps - D + 1))
    rows = []
    for s in range(6):
        sel = s_arr == s
        rows.append({"s": s, "I+": int(Ip[sel][0]), "P(+) over D readout times (every r0)":
                     sorted(set(_fs(Fr(int(v), D)) for v in plus[:D].sum(0)[sel]))})
    out["unstaged"] = {"r+ == r- every update": eq, "exactly one click every update": one,
                       "N+ over any D consecutive updates == 6 I+": windows_ok, "rows": rows,
                       "rewind": _rewind_ok(eng, hist)}
    return out


# =============================================================================================== TC.6 n exits
def compositions(total, n):
    if n == 1:
        yield (total,)
        return
    for k in range(total + 1):
        for rest in compositions(total - k, n - 1):
            yield (k,) + rest


def exp_sequential(D_I, Q, kappa, n):
    D = 6 * Q
    assert 2 * kappa * D_I == D
    comps = list(compositions(D_I, n))
    # tokens on x = 0..D-1; the stream profile starts on x = L-n..L-1 (outside the token nodes), so every token node
    # sees the n visits exactly once, at snapshots x + 1 .. x + n, and nothing before
    L = max(D + n + 1, math.isqrt(len(comps) - 1) + 1)
    fib = build_fibre(Q=Q, axis=0, components=("S",), name="stream")
    seq = build_sequential_router(Q=Q, kappa=kappa, stream="stream.S", name="seq")
    T = compose(fib, seq)
    eng = Engine(T, Q)
    pr = Prep(T, Q, L, fib, seq)
    lines = yz_lines(L, len(comps))
    lat_idx = lambda x, y, z: pr.node(x, y, z)
    for (y, z), comp in zip(lines, comps):
        for k, I in enumerate(comp, start=1):
            pr.set("stream.S", [lat_idx(-k, y, z)], b=I)
            pr.set("stream.S", [lat_idx(-k - 1, y, z)], a=I)
        pr.set("seq.Lk", [lat_idx(x, y, z) for x in range(D)], r=list(range(D)))
    steps = L + n
    hist = eng.run(pr.state(), steps, history=True)
    clicks = [official(T, D, hist[t], hist[t + 1], "seq.Lk") for t in range(steps)]
    quot = [quotient(T, hist[t], hist[t + 1], "seq.Lk") for t in range(steps)]
    bad_excl = 0
    bad_born = 0
    for (y, z), comp in zip(lines, comps):
        cnt = [0] * n
        for x in range(D):
            node = lat_idx(x, y, z)
            ks = [k for k in range(1, n + 1) if clicks[x + k][node]]
            if len(ks) != 1 or quot[x + ks[0]][node] != 1:
                bad_excl += 1
                continue
            cnt[ks[0] - 1] += 1
        if [Fr(c, D) for c in cnt] != [Fr(I, D_I) for I in comp]:
            bad_born += 1
    return {"D_I": D_I, "Q": Q, "kappa": kappa, "n": n, "D": D, "L": L, "compositions": len(comps),
            "tokens": D, "non_exclusive_cases": bad_excl, "non_Born_compositions": bad_born,
            "rewind": _rewind_ok(eng, hist), "recip": recip_summary(T)}


def exp_parallel(D_I, Q, kappa, n, offsets_search=False):
    D = 6 * Q
    comps = list(compositions(D_I, n))
    L = max(D + 2, math.isqrt(len(comps) - 1) + 1)          # tokens on x = 0..D-1, the streams start at x = L-1
    comps_names = tuple(f"S{k}" for k in range(1, n + 1))
    fib = build_fibre(Q=Q, axis=0, components=comps_names, name="stream")
    par = build_parallel_router(Q=Q, kappa=kappa, streams=tuple(f"stream.{c}" for c in comps_names), name="par")
    T = compose(fib, par)
    eng = Engine(T, Q)
    pr = Prep(T, Q, L, fib, par)
    lines = yz_lines(L, len(comps))
    for (y, z), comp in zip(lines, comps):
        for k, I in enumerate(comp, start=1):
            pr.set(f"stream.S{k}", [pr.node(-1, y, z)], b=I)
            pr.set(f"stream.S{k}", [pr.node(-2, y, z)], a=I)
        for k in range(1, n + 1):
            pr.set(f"par.E{k}", [pr.node(x, y, z) for x in range(D)], r=list(range(D)))
    steps = L + 1
    hist = eng.run(pr.state(), steps, history=True)
    tab = [click_flags(T, D, hist[t], hist[t + 1]) for t in range(steps)]
    gi = [T.gear_index(f"par.E{k}") for k in range(1, n + 1)]
    fails = 0
    excl_fail = 0
    for (y, z), comp in zip(lines, comps):
        cnt = [0] * n
        bad = False
        for x in range(D):
            node = pr.node(x, y, z)
            ks = [k for k in range(1, n + 1) if tab[x + 1][gi[k - 1], node]]
            if len(ks) != 1:
                bad = True
                excl_fail += 1
                continue
            cnt[ks[0] - 1] += 1
        if bad or [Fr(c, D) for c in cnt] != [Fr(I, D_I) for I in comp]:
            fails += 1
    res = {"D_I": D_I, "Q": Q, "n": n, "compositions": len(comps), "failing_compositions": fails,
           "non_exclusive_cases": excl_fail, "rewind": _rewind_ok(eng, hist), "recip": recip_summary(T)}
    if offsets_search and n == 3:
        # ONE fixed offset o for exit 2 (a local rule: the same for every composition), searched exhaustively over the
        # remainder circle (exit 1: lam < K1; exit 3: lam >= D - K3; exit 2: (lam + o) mod D >= D - K2; the same arc
        # arithmetic as the gear run above, which is o = 0). Also reported: a per-composition offset (it uses the
        # intensities themselves, i.e. non-local information, like S5-P's c2 = I3) can always succeed.
        lam = np.arange(D)

        def nbad(comp, o):
            K = [2 * kappa * I for I in comp]
            return int(((lam < K[0]).astype(int) + (((lam + o) % D) >= D - K[1]).astype(int)
                        + (lam >= D - K[2]).astype(int) != 1).sum())
        per_o = [sum(nbad(c, o) > 0 for c in comps) for o in range(D)]
        res["fixed_offset_min_failing_compositions"] = min(per_o)
        res["per_composition_offset_failing"] = sum(min(nbad(c, o) for o in range(D)) > 0 for c in comps)
    return res


# =============================================================================================== TC.7 F7
F7_Q, F7_KAPPA, F7_D, F7_XA, F7_DIST, F7_TA = 4, 3, 24, 2, 5, 1


def f7_system():
    blk = build_f7(Q=F7_Q, kappa=F7_KAPPA, name="f7")
    return compose(blk), blk


def f7_run(T, blk, eng, phi, a, b, steps=14, L=24):
    D = F7_D
    xA, xB = F7_XA, F7_XA + F7_DIST
    lines = yz_lines(L, D * D)
    pr = Prep(T, F7_Q, L, blk)
    nA, nB = pr.nodes_x(xA, lines), pr.nodes_x(xB, lines)
    lamA = np.array([i // D for i in range(D * D)])
    lamB = np.array([i % D for i in range(D * D)])
    c = ring_b(1, phi)
    for j in range(3):                       # photon flash: left-moving, at x_A + 1 at t = 0 (reaches x_A at t_A = 1)
        pr.set(f"f7.PH{j}", pr.nodes_x(xA + 1, lines), b=c[j])
        pr.set(f"f7.PH{j}", pr.nodes_x(xA + 2, lines), a=c[j])
    pr.set("f7.PG", pr.nodes_x(xA + 1, lines), b=1)
    pr.set("f7.PG", pr.nodes_x(xA + 2, lines), a=1)
    for j, (aa, bb) in enumerate(ring_state(1, a)):
        pr.set(f"f7.C{j}", nA, a=aa, b=bb)
    for j, (aa, bb) in enumerate(ring_state(1, b)):
        pr.set(f"f7.B{j}", nB, a=aa, b=bb)
    for g in ("f7.dAp", "f7.dAm"):
        pr.set(g, nA, r=lamA)
    for g in ("f7.dBp", "f7.dBm"):
        pr.set(g, nB, r=lamB)
    s0 = pr.state()
    hist = eng.run(s0, steps, history=True)
    return hist, nA, nB


def exp_f7(settings=range(6), phis=range(6), steps=14):
    T, blk = f7_system()
    eng = Engine(T, F7_Q)
    D = F7_D
    N = D * D
    E = defaultdict(int)          # (a, b, tB) -> sum of q * oB over (phi, lamA, lamB)
    mA = defaultdict(int)
    mB = defaultdict(int)
    bitgate = defaultdict(int)
    alice_ok = True
    front_zero_before = True
    front_C0 = True
    rewind_all = True
    pair = (0, 1)
    gAp, gAm = T.gear_index("f7.dAp"), T.gear_index("f7.dAm")
    tick_info = None
    t_front_bob = None
    for a in settings:
        for b in settings:
            for phi in phis:
                hist, nA, nB = f7_run(T, blk, eng, phi, a, b, steps)
                rewind_all &= _rewind_ok(eng, hist)
                # Alice: exactly one click at update t_A, none before or after
                q = None
                tabs = [click_flags(T, D, hist[t], hist[t + 1]) for t in range(steps)]
                for t in range(steps):
                    cp = tabs[t][gAp][nA]
                    cm = tabs[t][gAm][nA]
                    if t == F7_TA:
                        qp = quotient(T, hist[t], hist[t + 1], "f7.dAp", nA)
                        qm = quotient(T, hist[t], hist[t + 1], "f7.dAm", nA)
                        alice_ok &= bool(np.all(cp ^ cm)) and set((qp + qm).tolist()) <= {1, -1}
                        q = qp + qm
                    else:
                        alice_ok &= not bool(cp.any() or cm.any())
                for t in range(F7_TA + 3):                       # front identically 0 up to snapshot t_A + 2
                    for j in range(3):
                        front_zero_before &= not bool(np.any(values(hist[t], T, f"f7.P{j}")))
                for h in hist:
                    for j in range(3):
                        front_C0 &= not bool(np.any(values(h, T, f"f7.P{j}", "r")))
                for t in range(steps):
                    p = quotient(T, hist[t], hist[t + 1], "f7.dBp", nB)
                    m = quotient(T, hist[t], hist[t + 1], "f7.dBm", nB)
                    oB = np.where(p == 1, 1, 0) - np.where(m == -1, 1, 0)
                    if not np.all(np.abs(oB) == 1):
                        alice_ok = False
                    E[(a, b, t)] += int(np.sum(q * oB))
                    mB[(a, b, t)] += int(oB.sum())
                    if t_front_bob is None and np.any(values(hist[t], T, "f7.P0", nodes=nB)):
                        t_front_bob = t
                mA[(a, b)] += int(q.sum())
                # designed bit gate (observer) at the first timelike readout with the front present
                tB = F7_TA + 3 + F7_DIST
                if a in pair and b in pair:
                    front = np.stack([values(hist[tB], T, f"f7.P{j}", nodes=nB) for j in range(3)], 1)
                    pats = {(o, aa): [o * v for v in ring_b(1, aa, tB - 1 - F7_DIST)] for o in (1, -1) for aa in pair}
                    for i in range(N):
                        o, aa = bit_gate(front[i], pair, pats)
                        bitgate[(a, b)] += int(q[i]) * o * (-1 if (aa == 1 and b == 1) else 1)
                if tick_info is None:
                    qB = [int(quotient(T, hist[t], hist[t + 1], "f7.B0", nB)[0]) for t in range(steps)]
                    tick_info = qB
    tot = N * len(list(phis))
    curves = {}
    Smax = {}
    margB = {}
    for tB in range(steps):
        Et = {(a, b): Fr(E[(a, b, tB)], tot) for a in settings for b in settings}
        byd = defaultdict(set)
        for (a, b), v in Et.items():
            byd[(a - b) % 6].add(v)
        curves[tB] = [sorted(_fs(v) for v in byd[k]) for k in range(6)]
        Smax[tB] = _fs(max(abs(Et[(a, b)] + Et[(a, b2)] + Et[(a2, b)] - Et[(a2, b2)])
                           for a, a2, b, b2 in itertools.product(settings, repeat=4)))
        margB[tB] = sorted(set(_fs(Fr(mB[(a, b, tB)], tot)) for a in settings for b in settings))
    Ebg = {k: Fr(v, tot) for k, v in bitgate.items()}
    S_bg = Ebg[(0, 0)] + Ebg[(0, 1)] + Ebg[(1, 0)] - Ebg[(1, 1)]
    # spacelike / timelike by the taxicab cone: Alice's click is the update t_A -> t_A + 1 at x_A; Bob's update
    # t_B -> t_B + 1 at x_B reads snapshot t_B, which can depend on the click iff t_B >= t_A + 1 + d
    cone = {tB: ("timelike" if tB >= F7_TA + 1 + F7_DIST else "spacelike") for tB in range(steps)}
    return {"Q": F7_Q, "D": D, "d": F7_DIST, "t_A": F7_TA, "x_A": F7_XA, "x_B": F7_XA + F7_DIST,
            "tokens": "lam_A, lam_B over all 24 remainders (576 lines); phi over Z6; all 36 setting pairs",
            "E_by_(a-b)_per_tB": {str(k): v for k, v in curves.items()}, "maxS_per_tB": {str(k): v for k, v in Smax.items()},
            "cone_per_tB": {str(k): v for k, v in cone.items()},
            "Alice_marginals": sorted(set(_fs(Fr(v, tot)) for v in mA.values())),
            "Bob_marginals_per_tB": {str(k): v for k, v in margB.items()},
            "bit_gate_E": {f"{k}": _fs(v) for k, v in Ebg.items()}, "bit_gate_S": _fs(S_bg),
            "alice_one_click_at_tA_only_and_bob_one_click_per_update": alice_ok,
            "front_zero_through_snapshot_tA+2": front_zero_before, "front_fibres_C0": front_C0,
            "first_snapshot_with_front_at_Bob": t_front_bob, "Bob_clock_B0_click_sizes": tick_info,
            "rewind_all_runs": rewind_all, "recip": recip_summary(T)}


# =============================================================================================== TC.8 all-or-nothing
def exp_all_or_nothing(tau=6):
    Q, A = 5, 1
    a1, a2, X1, X2 = _arms(Q)
    W = build_which_path_W(Q=Q, Q_W=5, arm=X1, N=1, name="W")
    T = compose(a1, a2, W)
    eng = Engine(T, Q)
    n = 180
    s_arr = np.repeat(np.arange(6), 30)
    rW = np.tile(np.arange(30), 6)
    L = _cube(n)
    pr = Prep(T, Q, L, a1, a2, W)
    nodes = np.arange(n)
    _set_ring(pr, X1, nodes, A, np.zeros(n, dtype=int))
    _set_ring(pr, X2, nodes, A, -s_arr)
    pr.set("W.W0", nodes, r=rW)
    hist = eng.run(pr.state(), tau, history=True)
    R = np.zeros(n, dtype=bool)
    for t in range(tau):
        R |= official(T, 6 * Q, hist[t], hist[t + 1], "W.W0", nodes)
    dist = np.zeros(n, dtype=np.int64)
    ident = np.ones(n, dtype=bool)
    for t in range(tau + 1):
        for arm, ph in ((X1, np.zeros(n, dtype=int)), (X2, -s_arr)):
            for j in range(3):
                fa = np.array([ring_state(A, int(p), t)[j][0] for p in ph])
                fb = np.array([ring_state(A, int(p), t)[j][1] for p in ph])
                da = np.abs(values(hist[t], T, arm[j], "a", nodes) - fa)
                db = np.abs(values(hist[t], T, arm[j], "b", nodes) - fb)
                dr = values(hist[t], T, arm[j], "r", nodes) != 0
                ident &= (da == 0) & (db == 0) & ~dr
                if t == tau:
                    dist += da + db
    return {"Q": Q, "configs": n, "clicking": int(R.sum()), "silent": int((~R).sum()),
            "silent_bit_identical": int((~R & ident).sum()), "clicking_changed": int((R & ~ident).sum()),
            "min_final_disturbance_clicking": int(dist[R].min()) if R.any() else None,
            "rewind": _rewind_ok(eng, hist), "recip": recip_summary(T)}


# =============================================================================================== TC.9 M2-2
M22_Q, M22_QW, M22_TAU = 40, 5, 6


def m22_system(N):
    Q = M22_Q
    a1, a2, X1, X2 = _arms(Q)
    W = build_which_path_W(Q=Q, Q_W=M22_QW, arm=X1, N=N, name="W")
    gate = build_fibre(Q=Q, axis=0, components=("G",), name="gate", label="audit")
    ex = build_gated_pair(Q=Q, kappa=15, arm1=X1, arm2=X2, gate="gate.G", name="exit")
    T = compose(a1, a2, W, gate, ex)
    return T, (a1, a2, W, gate, ex), X1, X2


def m22_configs(N, mode):
    DW = 6 * M22_QW
    if mode == "exhaustive":
        return [tuple(c) for c in itertools.product(range(DW), repeat=N)]
    rng = np.random.default_rng(1)                       # S5-P2R's declared seed-1 sample (P_m22_p2r.py)
    return [tuple(int(x) for x in rng.integers(0, DW, N)) for _ in range(2000)]


def exp_m22(N, mode, L=12, rewind_batches=3):
    T, blocks, X1, X2 = m22_system(N)
    Q = M22_Q
    D = 6 * Q
    eng = Engine(T, Q)
    cfgs = m22_configs(N, mode)
    members = [(c, s, lam) for c in range(len(cfgs)) for s in range(6) for lam in range(8)]
    per = L * L
    x0 = 1
    plus = np.zeros((len(cfgs), 6, 8), dtype=np.int64)
    wfinal = {}
    rew_ok = True
    for bi, start in enumerate(range(0, len(members), per)):
        batch = members[start:start + per]
        pr = Prep(T, Q, L, *blocks)
        lines = yz_lines(L, len(batch))
        nodes = pr.nodes_x(x0, lines)
        cidx = np.array([m[0] for m in batch])
        s_arr = np.array([m[1] for m in batch])
        lam = np.array([m[2] for m in batch])
        _set_ring(pr, X1, nodes, 1, np.zeros(len(batch), dtype=int))
        _set_ring(pr, X2, nodes, 1, -s_arr)
        for j in range(N):
            pr.set(f"W.W{j}", nodes, r=[(Q // M22_QW) * cfgs[c][j] for c in cidx])
        pr.set("exit.dP", nodes, r=30 * lam)
        pr.set("exit.dM", nodes, r=30 * (7 - lam))
        pr.set("gate.G", pr.nodes_x(x0 + M22_TAU, lines), b=1)
        pr.set("gate.G", pr.nodes_x(x0 + M22_TAU + 1, lines), a=1)
        hist = eng.run(pr.state(), M22_TAU + 1, history=True)
        if bi < rewind_batches:
            rew_ok &= _rewind_ok(eng, hist)
        qp = quotient(T, hist[M22_TAU], hist[M22_TAU + 1], "exit.dP", nodes)
        qm = quotient(T, hist[M22_TAU], hist[M22_TAU + 1], "exit.dM", nodes)
        for t in range(M22_TAU):                          # the exit pair must be silent before the gate
            if np.any(quotient(T, hist[t], hist[t + 1], "exit.dP", nodes)) or np.any(
                    quotient(T, hist[t], hist[t + 1], "exit.dM", nodes)):
                rew_ok = False
        pl = (qp == 1) & (qm != 1)
        plus[cidx, s_arr, lam] = pl.astype(np.int64)
        wst = np.stack([np.concatenate([values(hist[M22_TAU], T, f"W.W{j}", f, nodes) for j in range(N)])
                        .reshape(N, -1) for f in ("a", "b", "r")], 0).reshape(3 * N, -1).T
        for i, (c, s, l) in enumerate(batch):
            wfinal[(c, s, l)] = tuple(int(v) for v in wst[i])
    Pens = [plus[:, s, :].mean() for s in range(6)]
    Vs = []
    for c in range(len(cfgs)):
        Vs.append(harmonic_V([plus[c, s, :].mean() for s in range(6)]))
    Vsingle = float(np.nanmean(Vs))

    def cond(keyfun):
        g = defaultdict(lambda: [[0, 0] for _ in range(6)])
        for (c, s, l), w in wfinal.items():
            k = keyfun(w)
            g[k][s][0] += int(plus[c, s, l])
            g[k][s][1] += 1
        tot = wt = 0.0
        for k, cnts in g.items():
            if all(x[1] > 0 for x in cnts):
                v = harmonic_V([x[0] / x[1] for x in cnts])
                if v == v:
                    ww = sum(x[1] for x in cnts)
                    tot += ww * v
                    wt += ww
        return tot / wt if wt else float("nan")
    Ver = cond(lambda w: w)
    V1 = cond(lambda w: (w[0], w[N], w[2 * N]))
    return {"N": N, "mode": mode, "configs": len(cfgs), "Q": Q, "D": D, "V_ens": round(harmonic_V(Pens), 3),
            "V_single": round(Vsingle, 3), "V_eraser": round(Ver, 3), "V_1": round(V1, 3),
            "P_ens": [round(float(p), 4) for p in Pens], "rewind_checked_batches_ok": rew_ok,
            "recip": recip_summary(T)}


# =============================================================================================== TC.10 D12b toy
def exp_dec(A, c):
    Q = 4 * A * A
    D = 6 * Q
    blk = build_dec_toy(Q=Q, c=c, name="dec")
    T = compose(blk)
    eng = Engine(T, Q)
    n = 4 * D
    s_arr = np.repeat(np.arange(4), D)
    lam = np.tile(np.arange(D), 4)
    L = _cube(n)
    pr = Prep(T, Q, L, blk)
    nodes = np.arange(n)
    for j, (a, b) in enumerate(pair4_state(A, 0)):
        pr.set(f"dec.X1_{j}", nodes, a=a, b=b)
    for j in range(2):
        pr.set(f"dec.X2_{j}", nodes, a=[pair4_state(A, int(s))[j][0] for s in s_arr],
               b=[pair4_state(A, int(s))[j][1] for s in s_arr])
    pr.set("dec.W1", nodes, r=D - 1 - lam)
    pr.set("dec.W2", nodes, r=lam)
    pr.set("dec.dP", nodes, r=D - 1 - lam)
    pr.set("dec.dM", nodes, r=lam)
    s0 = pr.state()
    hist = eng.run(s0, 2, history=True)
    w1 = official(T, D, hist[0], hist[1], "dec.W1", nodes)
    w2 = official(T, D, hist[0], hist[1], "dec.W2", nodes)
    d_early = official(T, D, hist[0], hist[1], "dec.dP", nodes) | official(T, D, hist[0], hist[1], "dec.dM", nodes)
    p = official(T, D, hist[1], hist[2], "dec.dP", nodes)
    m = official(T, D, hist[1], hist[2], "dec.dM", nodes)
    excl = bool(np.all(w1 ^ w2)) and bool(np.all(p ^ m)) and not bool(d_early.any())
    rows = []
    joint_e, joint_er = Counter(), Counter()
    for s in range(4):
        sel = s_arr == s
        rows.append({"s": s, "P(+|s)": _fs(Fr(int(p[sel].sum()), D)),
                     "P(+|s,W1)": _fs(Fr(int((p & w1)[sel].sum()), int(w1[sel].sum()))),
                     "P(+|s,W2)": _fs(Fr(int((p & w2)[sel].sum()), int(w2[sel].sum())))})
    for i in range(n):
        joint_e[(int(s_arr[i]), bool(p[i]))] += 1
        joint_er[(int(s_arr[i]), (bool(p[i]), bool(w1[i])))] += 1
    M = uniform(T, Q, "M")
    mir = reversor_check(M, eng, [s0], 2)
    return {"A": A, "c": c, "Q": Q, "D": D, "rows": rows, "I(s;exit)": round(mutual_info(joint_e), 4),
            "I(s;exit,record)": round(mutual_info(joint_er), 4), "one_W_and_one_exit_click": excl,
            "rewind": _rewind_ok(eng, hist), "M_F2_M_F2_id": mir["ok"], "recip": recip_summary(T)}


# =============================================================================================== TC.11 back-action
def exp_backaction(g, steps=12, A=1, spring_lam=None, cap_bits=None):
    """g-form (rank 3 for g = 0, spring cross term only for g > 0) or, with ``spring_lam``, the COMPLETE OD4 spring.
    ``cap_bits``: stop early (and say so) once max|b| of any gear exceeds this many bits (blow-up)."""
    Q, kappa = 8 * A * A, 3
    D = 6 * Q
    a1, a2, X1, X2 = _arms(Q)
    if spring_lam is None:
        ba = build_backaction_router(Q=Q, kappa=kappa, g=g, arm1=X1, arm2=X2, name="ba")
    else:
        ba = build_spring_backaction_router(Q=Q, kappa=kappa, lam=spring_lam, arm1=X1, arm2=X2, name="ba")
    T = compose(a1, a2, ba)
    eng = Engine(T, Q)
    n = 6 * D
    s_arr = np.repeat(np.arange(6), D)
    lam = np.tile(np.arange(D), 6)
    L = _cube(n)
    pr = Prep(T, Q, L, a1, a2, ba)
    nodes = np.arange(n)
    _set_ring(pr, X1, nodes, A, np.zeros(n, dtype=int))
    _set_ring(pr, X2, nodes, A, s_arr)
    pr.set("ba.dP", nodes, r=lam)
    pr.set("ba.dM", nodes, r=lam)
    hist = [pr.state()]
    stopped = None
    for t in range(steps):
        hist.append(eng.step(hist[-1]))
        if cap_bits is not None and hist[-1].max_abs().bit_length() > cap_bits:
            stopped = t + 1
            break
    per = []
    maxb = []
    for t in range(len(hist) - 1):
        cp = official(T, D, hist[t], hist[t + 1], "ba.dP", nodes)
        cm = official(T, D, hist[t], hist[t + 1], "ba.dM", nodes)
        req = values(hist[t + 1], T, "ba.dP", "r", nodes) == values(hist[t + 1], T, "ba.dM", "r", nodes)
        per.append({"update": t, "exactly_one": int((cp ^ cm).sum()), "both": int((cp & cm).sum()),
                    "none": int((~cp & ~cm).sum()), "r+==r-": int(req.sum())})
        mb = 0
        for arm in (X1, X2):
            for gname in arm:
                row = hist[t + 1].b[T.gear_index(gname)][:n]
                mb = max(mb, max(abs(int(v)) for v in row))
        maxb.append(mb.bit_length())                     # bits of max |b| over both arms (exact Python ints)
        if t == 0:
            first = []
            for s in range(6):
                sel = s_arr == s
                first.append({"s": s, "P(d+)": _fs(Fr(int(cp[sel].sum()), D)), "both": int((cp & cm)[sel].sum()),
                              "none": int((~cp & ~cm)[sel].sum())})
    return {"g": g, "spring_lam": spring_lam, "A": A, "rank": T.rank, "members": n, "first_update": first,
            "per_update": per,
            "max_abs_arm_b_bits": maxb, "stopped_after_update_beyond_cap": stopped, "cap_bits": cap_bits,
            "engine_stats": dict(eng.stats),
            "rewind": _rewind_ok(eng, hist), "recip": recip_summary(T)}


# =============================================================================================== reversors (binding 3)
def exp_reversors():
    """Declared mirror maps as data: M' (parity-preserving) on the b-only experiment tensors, checked as
    M' F^n M' F^n = id on their actual initial data; the M'-fixed vacuum (r0 = 3Q - 1) exists only for ODD Q.
    For F7 (a-read gears) the per-gear mirrors are reported (expected NOT reversors)."""
    out = {}
    # odd-Q sequential router (Q = 3) with the vacuum at 3Q - 1 for the carriers
    for name, (T, s0, eng, Q) in _reversor_cases().items():
        Mp = uniform(T, Q, "Mp")
        rc = reversor_check(Mp, eng, [s0], 8)
        out[name] = {"Q": Q, "b_only": T.b_only, "Mp_identity": rc["identity"], "Mp_failures": rc["failures"]}
    from ...core.reversors import is_fixed, remainder_map
    for Q in (3, 5, 4, 8):
        D = 6 * Q
        r = np.arange(D)
        Rp = remainder_map("Mp", r, D)
        out[f"Mp_fixed_remainders_Q{Q}"] = [int(v) for v in r[Rp == r]]
    # the joint vacuum (every gear (0, 0, 3Q - 1)) of the odd-Q all-or-nothing system is M'-fixed
    T, s0, eng, Q = _reversor_cases()["all_or_nothing_Q5"]
    vac = Prep(T, Q, 3, default_r=0)
    for name in T.names:
        vac.set(name, np.arange(27), r=3 * Q - 1)
    out["vacuum_3Q-1_Mp_fixed_Q5"] = is_fixed(uniform(T, Q, "Mp"), vac.state())
    out["vacuum_run_Q5_stays_vacuum"] = eng.run(vac.state(), 6).same_as(vac.state())
    return out


def _reversor_cases():
    cases = {}
    T, blocks, X1, X2, Q = router_system(1, "opposite")
    eng = Engine(T, Q)
    D = 6 * Q
    s_arr = np.repeat(np.arange(6), D)
    lam = np.tile(np.arange(D), 6)
    pr, _ = _router_prep(T, blocks, Q, 1, X1, X2, s_arr, lam, lam, 6 * D)
    cases["router_Q8"] = (T, pr.state(), eng, Q)
    T, blk = f7_system()
    eng = Engine(T, F7_Q)
    hist, _, _ = f7_run(T, blk, eng, 0, 0, 1, steps=0)
    cases["f7_Q4"] = (T, hist[0], eng, F7_Q)
    Q = 5
    a1, a2, X1, X2 = _arms(Q)
    W = build_which_path_W(Q=Q, Q_W=5, arm=X1, N=1, name="W")
    T = compose(a1, a2, W)
    eng = Engine(T, Q)
    pr = Prep(T, Q, 6, a1, a2, W)
    nodes = np.arange(180)
    for name in T.names:                       # C0 carriers and W at the M'-fixed vacuum remainder 3Q - 1 (odd Q)
        pr.set(name, np.arange(216), r=3 * Q - 1)
    _set_ring(pr, X1, nodes, 1, np.zeros(180, dtype=int))
    _set_ring(pr, X2, nodes, 1, -np.repeat(np.arange(6), 30))
    pr.set("W.W0", nodes, r=np.tile(np.arange(30), 6))
    cases["all_or_nothing_Q5"] = (T, pr.state(), eng, Q)
    return cases


__all__ = [n for n in dir() if n.startswith("exp_")] + ["compositions", "router_system", "f7_system", "f7_run",
                                                         "m22_system", "recip_summary"]


# =============================================================================================== TC.13 odd Q
GAUGE_Q = 2 ** 19 + 1


def parity_obstruction(Qmax=999):
    """Matched two-exit polarization router: 16 kappa A^2 = 6Q (3-gear rings). Returns the odd Q <= Qmax that admit a
    solution (expected: none, since 8 kappa A^2 = 3Q forces Q even) and, for contrast, the even Q that do."""
    odd = [Q for Q in range(1, Qmax + 1, 2) if any(6 * Q == 16 * k * A * A for A in range(1, 40)
                                                    for k in range(1, 6 * Q // 16 + 1))]
    even = [Q for Q in range(2, 101, 2) if any(6 * Q == 16 * k * A * A for A in range(1, 40)
                                                for k in range(1, 6 * Q // 16 + 1))]
    return {"odd_Q_with_matched_router": odd, "even_Q_with_matched_router_up_to_100": even}


def exp_near_matched(Q, A=1, chunk_L=None, token_step=1):
    """Opposite-form polarization pair at (odd) Q with kappa = floor(6Q / 16A^2): S = 16 kappa A^2 <= D. Exhaustive over
    the tokens r = 0, token_step, 2 token_step, ... (token_step = 6 is the conserved class when K = 0 mod 6)."""
    D = 6 * Q
    kappa = D // (16 * A * A)
    S = 16 * kappa * A * A
    a1, a2, X1, X2 = _arms(Q)
    rt = build_born_router(Q=Q, kappa=kappa, arm1=X1, arm2=X2, form="opposite", name="router")
    T = compose(a1, a2, rt)
    eng = Engine(T, Q)
    tokens = np.arange(0, D, token_step)
    members_s = np.repeat(np.arange(6), len(tokens))
    members_l = np.tile(tokens, 6)
    n_all = len(members_s)
    per = (chunk_L ** 3) if chunk_L else n_all
    cnt = {s: Counter() for s in range(6)}
    rew = True
    for start in range(0, n_all, per):
        sl = slice(start, min(start + per, n_all))
        s_arr, lam = members_s[sl], members_l[sl]
        L = chunk_L or _cube(len(s_arr))
        pr = Prep(T, Q, L, a1, a2, rt)
        nodes = np.arange(len(s_arr))
        _set_ring(pr, X1, nodes, A, np.zeros(len(s_arr), dtype=int))
        _set_ring(pr, X2, nodes, A, s_arr)
        pr.set("router.dP", nodes, r=lam)
        pr.set("router.dM", nodes, r=lam)
        s0 = pr.state()
        s1 = eng.step(s0)
        rew &= eng.inverse_step(s1).same_as(s0)
        fl = click_flags(T, D, s0, s1)
        cp = fl[T.gear_index("router.dP")][nodes]
        cm = fl[T.gear_index("router.dM")][nodes]
        for s in range(6):
            sel = s_arr == s
            cnt[s]["+"] += int((cp & ~cm)[sel].sum())
            cnt[s]["-"] += int((cm & ~cp)[sel].sum())
            cnt[s]["both"] += int((cp & cm)[sel].sum())
            cnt[s]["none"] += int((~cp & ~cm)[sel].sum())
    N = len(tokens)
    rows = []
    for s in range(6):
        c = cnt[s]
        det = c["+"] + c["-"]
        rows.append({"s": s, "P(both)": _fs(Fr(c["both"], N)), "P(none)": _fs(Fr(c["none"], N)),
                     "P(+|detected)": _fs(Fr(c["+"], det)) if det else None})
    return {"Q": Q, "odd": Q % 2 == 1, "D": D, "A": A, "kappa": kappa, "S": S, "pred_P(none)": _fs(Fr(D - S, D)),
            "tokens": f"r = 0, {token_step}, ..., {D - token_step} ({N} values)", "rows": rows, "rewind": rew,
            "recip": recip_summary(T)}


def exp_odd_q():
    out = {"parity": parity_obstruction()}
    out["sequential_n2"] = [exp_sequential(9, 3, 1, 2), exp_sequential(15, 5, 1, 2)]
    out["near_matched"] = [exp_near_matched(3), exp_near_matched(11), exp_near_matched(11, A=2)]
    return out


def exp_gauge_q_router():
    """The near-matched pair at the gauge layer's Q = 2^19 + 1 (D = 3,145,734), exhaustive over the conserved token class
    r = 0 mod 6 (524,289 tokens x 6 phases), in chunks of 64^3 nodes."""
    return exp_near_matched(GAUGE_Q, A=1, chunk_L=64, token_step=6)


# =============================================================================================== TC.14 designation audit
def _qualified_terms(blocks):
    out = []
    for blk in blocks:
        for t in blk.terms:
            tgt = blk.qualify(t[0])
            facs = tuple(sorted((blk.qualify(f[0]), tuple(f[1]), f[2]) for f in t[2]))
            out.append((tgt, facs, len(t) > 3, (t[3]["designated_one_way"] if len(t) > 3 else None)))
    return out


def designation_audit(name, blocks):
    from ...core.lattice import DIRECTIONS
    terms = _qualified_terms(blocks)
    des = {(t, f) for t, f, d, _ in terms if d}
    force = {(t, f) for t, f, d, _ in terms if not d}
    coincide = sorted(des & force)
    T = compose(*blocks)
    names = T.names
    present = {(names[m.target], tuple(sorted((names[f.gear], f.offset, f.field) for f in m.factors))): m
               for m in T.monomials}
    partners_present = []
    rank4 = []
    for m in T.monomials:
        why = T.is_designated(m)
        if why is None:
            continue
        if m.degree == 3:
            rank4.append((f"u[{names[m.target]}] += {m.coeff} * " + " * ".join(
                f"{f.field}[{names[f.gear]}]{f.offset}" for f in m.factors), why))
        if any(f.field != "b" for f in m.factors):
            continue
        var = [(names[m.target], (0, 0, 0))] + [(names[f.gear], f.offset) for f in m.factors]
        for g, p in sorted(set(var)):
            if (g, p) == var[0]:
                continue
            rest = list(var)
            rest.remove((g, p))
            facs = []
            ok = True
            for gg, o in rest:
                off = (o[0] - p[0], o[1] - p[1], o[2] - p[2])
                if off != (0, 0, 0) and off not in DIRECTIONS:
                    ok = False
                facs.append((gg, off, "b"))
            if not ok:
                continue
            key = (g, tuple(sorted(facs)))
            if key in present:
                partners_present.append({"designated": f"u[{names[m.target]}] += {m.coeff} * ...",
                                         "partner": f"u[{g}] += {present[key].coeff} * " + " * ".join(
                                             f"b[{a}]{o}" for a, o, _ in key[1]),
                                         "partner_designated": T.is_designated(present[key]) is not None})
    return {"experiment": name, "designated_terms": len(des), "force_terms": len(force),
            "designated_coinciding_with_force": [str(c) for c in coincide], "partners_present": partners_present,
            "rank4_designated": len(rank4), "rank4_purposes": sorted({w for _, w in rank4})}


def audit_all():
    out = []
    a1, a2, X1, X2 = _arms(8)
    for form in ("opposite", "mirror"):
        out.append(designation_audit(f"router {form}", (a1, a2, build_born_router(Q=8, kappa=3, arm1=X1, arm2=X2,
                                                                                    form=form, name="router"))))
    rt = build_born_router(Q=8, kappa=3, arm1=X1, arm2=X2, name="router")
    out.append(designation_audit("token + drive", (a1, a2, rt, build_common_drive(Q=8, w=5, detectors=(
        "router.dP", "router.dM")))))
    out.append(designation_audit("sequential", (build_fibre(Q=3, components=("S",), name="stream"),
                                                build_sequential_router(Q=3, kappa=1, stream="stream.S"))))
    out.append(designation_audit("parallel", (build_fibre(Q=3, components=("S1", "S2", "S3"), name="stream"),
                                              build_parallel_router(Q=3, kappa=1, streams=(
                                                  "stream.S1", "stream.S2", "stream.S3")))))
    out.append(designation_audit("F7", (build_f7(Q=F7_Q, kappa=F7_KAPPA, name="f7"),)))
    out.append(designation_audit("F7 gated Bob (odd Q = 3)", (build_f7(Q=3, kappa=2, name="f7", bob_gate=True),)))
    b1, b2, Y1, Y2 = _arms(5)
    out.append(designation_audit("all-or-nothing", (b1, b2, build_which_path_W(Q=5, Q_W=5, arm=Y1, N=1))))
    T, blocks, _, _ = m22_system(6)
    out.append(designation_audit("M2-2 N=6", blocks))
    out.append(designation_audit("D12b c=1", (build_dec_toy(Q=4, c=1),)))
    out.append(designation_audit("back-action g=6", (a1, a2, build_backaction_router(Q=8, kappa=3, g=6, arm1=X1,
                                                                                       arm2=X2))))
    out.append(designation_audit("back-action complete spring lam=1", (a1, a2, build_spring_backaction_router(
        Q=8, kappa=3, lam=1, arm1=X1, arm2=X2))))
    return out


# =============================================================================================== TC.15 F7 at odd Q
def exp_f7_odd(Q=11, kappa=8, token_step=2, steps=14, settings=range(6), phis=range(6)):
    """F7 at an odd Q with near-matched pairs (S = 8 kappa < D): conditional (coincidence) correlations."""
    blk = build_f7(Q=Q, kappa=kappa, name="f7")
    T = compose(blk)
    eng = Engine(T, Q)
    D = 6 * Q
    toks = np.arange(0, D, token_step)
    n = len(toks)
    L = max(math.isqrt(n * n - 1) + 1, 16)
    xA, xB = F7_XA, F7_XA + F7_DIST
    lines = yz_lines(L, n * n)
    lamA = np.array([toks[i // n] for i in range(n * n)])
    lamB = np.array([toks[i % n] for i in range(n * n)])
    Ec = defaultdict(lambda: [0, 0])          # (a, b, tB) -> [sum q oB over coincidences, number of coincidences]
    Eall = defaultdict(int)
    alice_det = Counter()
    bob_none = Counter()
    rew = True
    excl = True
    gAp, gAm, gBp, gBm = (T.gear_index(f"f7.{g}") for g in ("dAp", "dAm", "dBp", "dBm"))
    for a in settings:
        for b in settings:
            for phi in phis:
                pr = Prep(T, Q, L, blk)
                nA, nB = pr.nodes_x(xA, lines), pr.nodes_x(xB, lines)
                c = ring_b(1, phi)
                for j in range(3):
                    pr.set(f"f7.PH{j}", pr.nodes_x(xA + 1, lines), b=c[j])
                    pr.set(f"f7.PH{j}", pr.nodes_x(xA + 2, lines), a=c[j])
                pr.set("f7.PG", pr.nodes_x(xA + 1, lines), b=1)
                pr.set("f7.PG", pr.nodes_x(xA + 2, lines), a=1)
                for j, (aa, bb) in enumerate(ring_state(1, a)):
                    pr.set(f"f7.C{j}", nA, a=aa, b=bb)
                for j, (aa, bb) in enumerate(ring_state(1, b)):
                    pr.set(f"f7.B{j}", nB, a=aa, b=bb)
                for g in ("f7.dAp", "f7.dAm"):
                    pr.set(g, nA, r=lamA)
                for g in ("f7.dBp", "f7.dBm"):
                    pr.set(g, nB, r=lamB)
                hist = eng.run(pr.state(), steps, history=True)
                rew &= _rewind_ok(eng, hist)
                tabs = [click_flags(T, D, hist[t], hist[t + 1]) for t in range(steps)]
                cp, cm = tabs[F7_TA][gAp][nA], tabs[F7_TA][gAm][nA]
                excl &= not bool((cp & cm).any())
                q = cp.astype(np.int64) - cm.astype(np.int64)
                alice_det[(a, b)] += int((q != 0).sum())
                for t in range(steps):
                    bp, bm = tabs[t][gBp][nB], tabs[t][gBm][nB]
                    excl &= not bool((bp & bm).any())
                    oB = bp.astype(np.int64) - bm.astype(np.int64)
                    co = (q != 0) & (oB != 0)
                    Ec[(a, b, t)][0] += int((q * oB)[co].sum())
                    Ec[(a, b, t)][1] += int(co.sum())
                    Eall[(a, b, t)] += int((q * oB).sum())
                    bob_none[t] += int((oB == 0).sum())
    runs = len(list(settings)) ** 2 * len(list(phis))
    tot = n * n * len(list(phis))
    curves, Smax, Eunc = {}, {}, {}
    for tB in range(steps):
        Et = {(a, b): Fr(*Ec[(a, b, tB)]) for a in settings for b in settings}
        byd = defaultdict(set)
        for (a, b), v in Et.items():
            byd[(a - b) % 6].add(v)
        curves[str(tB)] = [sorted(_fs(v) for v in byd[k]) for k in range(6)]
        Smax[str(tB)] = _fs(max(abs(Et[(a, b)] + Et[(a, b2)] + Et[(a2, b)] - Et[(a2, b2)])
                                for a, a2, b, b2 in itertools.product(settings, repeat=4)))
        Eunc[str(tB)] = sorted({_fs(Fr(Eall[(a, b, tB)], tot)) for a in settings for b in settings if a == b})
    return {"Q": Q, "odd": Q % 2 == 1, "D": D, "kappa": kappa, "S": 8 * kappa, "tokens": f"class step {token_step}, "
            f"{n} x {n} lines", "P_alice_detects": sorted({_fs(Fr(v, tot)) for v in alice_det.values()}),
            "P_bob_no_click_per_update": sorted({_fs(Fr(v, tot * runs)) for v in bob_none.values()}),
            "never_two_clicks": excl, "E_cond_by_(a-b)_per_tB": curves, "maxS_cond_per_tB": Smax,
            "E_uncond_at_a_eq_b_per_tB": Eunc, "rewind_all_runs": rew, "recip": recip_summary(T)}


# =============================================================================================== TC.16 spacelike R2 reader
def exp_f7_copy_reader(settings=range(6), phis=range(6)):
    """S5-M2's spacelike photon-copy reader: Bob's Alice-type router at x_B reads his own copy of the source flash
    against his setting (written into the C gears at x_B); both clicks at update 1 -> 2 (spacelike, |x|_1 = 5)."""
    T, blk = f7_system()
    eng = Engine(T, F7_Q)
    D, L, steps = F7_D, 24, 4
    xA, xB = F7_XA, F7_XA + F7_DIST
    lines = yz_lines(L, D * D)
    lamA = np.array([i // D for i in range(D * D)])
    lamB = np.array([i % D for i in range(D * D)])
    gAp, gAm = T.gear_index("f7.dAp"), T.gear_index("f7.dAm")
    E = defaultdict(int)
    mB = defaultdict(int)
    ok = True
    no_front = True
    rew = True
    for a in settings:
        for b in settings:
            for phi in phis:
                pr = Prep(T, F7_Q, L, blk)
                nA, nB = pr.nodes_x(xA, lines), pr.nodes_x(xB, lines)
                c = ring_b(1, phi)
                for j in range(3):                          # Alice's flash (left-moving) and Bob's copy (right-moving)
                    pr.set(f"f7.PH{j}", pr.nodes_x(xA + 1, lines), b=c[j])
                    pr.set(f"f7.PH{j}", pr.nodes_x(xA + 2, lines), a=c[j])
                    pr.set(f"f7.PH{j}", pr.nodes_x(xB - 1, lines), b=c[j])
                    pr.set(f"f7.PH{j}", pr.nodes_x(xB - 2, lines), a=c[j])
                for xx, sgn in ((xA + 1, "b"), (xA + 2, "a"), (xB - 1, "b"), (xB - 2, "a")):
                    pr.set("f7.PG", pr.nodes_x(xx, lines), **{sgn: 1})
                for nodes, setting in ((nA, a), (nB, b)):
                    for j, (aa, bb) in enumerate(ring_state(1, setting)):
                        pr.set(f"f7.C{j}", nodes, a=aa, b=bb)
                pr.set("f7.dAp", nA, r=lamA)
                pr.set("f7.dAm", nA, r=lamA)
                pr.set("f7.dAp", nB, r=lamB)
                pr.set("f7.dAm", nB, r=lamB)
                hist = eng.run(pr.state(), steps, history=True)
                rew &= _rewind_ok(eng, hist)
                fl = click_flags(T, D, hist[F7_TA], hist[F7_TA + 1])
                for t in range(steps):
                    if t != F7_TA:
                        f2 = click_flags(T, D, hist[t], hist[t + 1])
                        ok &= not bool(f2[gAp][nA].any() or f2[gAm][nA].any() or f2[gAp][nB].any() or f2[gAm][nB].any())
                    for j in range(3):
                        no_front &= not bool(np.any(values(hist[t + 1], T, f"f7.F{j}", nodes=nB)))
                qa = fl[gAp][nA].astype(np.int64) - fl[gAm][nA].astype(np.int64)
                qb = fl[gAp][nB].astype(np.int64) - fl[gAm][nB].astype(np.int64)
                ok &= bool(np.all(np.abs(qa) == 1) and np.all(np.abs(qb) == 1))
                E[(a, b)] += int((qa * qb).sum())
                mB[(a, b)] += int(qb.sum())
    tot = D * D * len(list(phis))
    Et = {k: Fr(v, tot) for k, v in E.items()}
    byd = defaultdict(set)
    for (a, b), v in Et.items():
        byd[(a - b) % 6].add(v)
    Smax = max(abs(Et[(a, b)] + Et[(a, b2)] + Et[(a2, b)] - Et[(a2, b2)])
               for a, a2, b, b2 in itertools.product(settings, repeat=4))
    return {"E_by_(a-b)": [sorted(_fs(v) for v in byd[k]) for k in range(6)], "maxS": _fs(Smax),
            "Bob_marginals": sorted({_fs(Fr(v, tot)) for v in mB.values()}), "one_click_each_at_update_1": ok,
            "no_front_at_Bob": no_front, "spacelike": "both clicks at update 1 -> 2, |x_B - x_A|_1 = 5",
            "rewind_all_runs": rew}


# =============================================================================================== TC.15b F7, odd Q, gated Bob
def exp_f7_gated(Q=3, kappa=2, token_step=2, tBs=(9, 6), settings=range(6), phis=range(6)):
    """F7 at odd Q with a ONE-SHOT Bob (gate flash at x_B at snapshot t_B): conditional correlations."""
    blk = build_f7(Q=Q, kappa=kappa, name="f7", bob_gate=True)
    T = compose(blk)
    eng = Engine(T, Q)
    D = 6 * Q
    toks = np.arange(0, D, token_step)
    n = len(toks)
    L = max(math.isqrt(n * n - 1) + 1, 16)
    xA, xB = F7_XA, F7_XA + F7_DIST
    lines = yz_lines(L, n * n)
    lamA = np.array([toks[i // n] for i in range(n * n)])
    lamB = np.array([toks[i % n] for i in range(n * n)])
    gAp, gAm, gBp, gBm = (T.gear_index(f"f7.{g}") for g in ("dAp", "dAm", "dBp", "dBm"))
    out = {"Q": Q, "odd": Q % 2 == 1, "D": D, "kappa": kappa, "S": 8 * kappa, "lines": n * n, "L": L, "per_tB": {}}
    rew = True
    for tB in tBs:
        steps = tB + 3
        Ec = defaultdict(lambda: [0, 0])
        a_det, b_det, b_bad, two = Counter(), Counter(), 0, False
        for a in settings:
            for b in settings:
                for phi in phis:
                    pr = Prep(T, Q, L, blk)
                    nA, nB = pr.nodes_x(xA, lines), pr.nodes_x(xB, lines)
                    c = ring_b(1, phi)
                    for j in range(3):
                        pr.set(f"f7.PH{j}", pr.nodes_x(xA + 1, lines), b=c[j])
                        pr.set(f"f7.PH{j}", pr.nodes_x(xA + 2, lines), a=c[j])
                    pr.set("f7.PG", pr.nodes_x(xA + 1, lines), b=1)
                    pr.set("f7.PG", pr.nodes_x(xA + 2, lines), a=1)
                    pr.set("f7.BG", pr.nodes_x(xB + tB, lines), b=1)          # left-moving: at x_B at snapshot t_B
                    pr.set("f7.BG", pr.nodes_x(xB + tB + 1, lines), a=1)
                    for j, (aa, bb) in enumerate(ring_state(1, a)):
                        pr.set(f"f7.C{j}", nA, a=aa, b=bb)
                    for j, (aa, bb) in enumerate(ring_state(1, b)):
                        pr.set(f"f7.B{j}", nB, a=aa, b=bb)
                    for g in ("f7.dAp", "f7.dAm"):
                        pr.set(g, nA, r=lamA)
                    for g in ("f7.dBp", "f7.dBm"):
                        pr.set(g, nB, r=lamB)
                    hist = eng.run(pr.state(), steps, history=True)
                    rew &= _rewind_ok(eng, hist)
                    tabs = [click_flags(T, D, hist[t], hist[t + 1]) for t in range(steps)]
                    cp, cm = tabs[F7_TA][gAp][nA], tabs[F7_TA][gAm][nA]
                    q = cp.astype(np.int64) - cm.astype(np.int64)
                    two |= bool((cp & cm).any())
                    a_det[(a, b)] += int((q != 0).sum())
                    for t in range(steps):
                        bp, bm = tabs[t][gBp][nB], tabs[t][gBm][nB]
                        two |= bool((bp & bm).any())
                        if t != tB:
                            b_bad += int((bp | bm).sum())
                    bp, bm = tabs[tB][gBp][nB], tabs[tB][gBm][nB]
                    oB = bp.astype(np.int64) - bm.astype(np.int64)
                    b_det[(a, b)] += int((oB != 0).sum())
                    co = (q != 0) & (oB != 0)
                    Ec[(a, b)][0] += int((q * oB)[co].sum())
                    Ec[(a, b)][1] += int(co.sum())
        tot = n * n * len(list(phis))
        Et = {k: Fr(*v) for k, v in Ec.items()}
        byd = defaultdict(set)
        for (a, b), v in Et.items():
            byd[(a - b) % 6].add(v)
        Smax = max(abs(Et[(a, b)] + Et[(a, b2)] + Et[(a2, b)] - Et[(a2, b2)])
                   for a, a2, b, b2 in itertools.product(settings, repeat=4))
        out["per_tB"][str(tB)] = {
            "cone": "timelike" if tB >= F7_TA + 1 + F7_DIST else "spacelike",
            "P_alice_detects": sorted({_fs(Fr(v, tot)) for v in a_det.values()}),
            "P_bob_detects": sorted({_fs(Fr(v, tot)) for v in b_det.values()}),
            "bob_clicks_outside_gate": b_bad, "two_clicks_in_a_pair": two,
            "E_cond_by_(a-b)": [sorted(_fs(v) for v in byd[k]) for k in range(6)], "maxS_cond": _fs(Smax)}
    out["rewind_all_runs"] = rew
    out["recip"] = recip_summary(T)
    return out


# =============================================================================================== TC.17 light-carried front (probe)
def f7_light_params(A):
    """Odd Q with near-matched readers (S = 8 A^2 <= 6Q, kappa = 1) and gamma matching the CW plane-wave amplitude of
    60-degree light at Bob to Bob's clock amplitude: |G| = gamma A / (2 (Q-1) sin k), cos k = 1 - 3Q / (2(Q-1))."""
    Q = -(-8 * A * A // 6)
    if Q % 2 == 0:
        Q += 1
    cosk = 1 - 3 * Q / (2 * (Q - 1))
    sink = math.sqrt(1 - cosk * cosk)
    gamma = round(2 * (Q - 1) * sink)
    return Q, gamma, cosk, sink


def exp_f7_light(A, d=5, steps=30, L=32, settings=range(6)):
    """STATUS PROBE (TC.17): F7 with the front on the headroom light gear, plane-wave geometry (all (y, z) identical
    except Bob's clock phase b on six lines). Alice's q is fixed per run by a representative token (lam_A = D-1 gives
    q = +1, lam_A = 0 gives q = -1 when both arcs are non-empty); the hidden phase phi and Alice's token enter through
    the exact arc weights K+/D, |K-|/D. Bob is a one-shot reader at each readout time t_B: P_B(+-) from his exact
    input K+- (the verified arc law). Conditional (coincidence) correlations E(a, b, t_B), exact Fractions."""
    Q, gamma, cosk, sink = f7_light_params(A)
    D = 6 * Q
    blk = build_f7(Q=Q, kappa=1, name="f7", carrier="light", gamma=gamma)
    T = compose(blk)
    eng = Engine(T, Q)
    xA, xB, tA = 2, 2 + d, 1
    allyz = yz_lines(L, L * L)
    rew = True
    num = defaultdict(Fr)
    den = defaultdict(Fr)
    p_by = {}
    for a in settings:
        # Alice's arc weights for every phi (exact ring values at t_A)
        Cs = ring_b(A, a, tA)
        wts = {}
        for phi in range(6):
            ph = ring_b(A, phi)
            X = sum(p * c for p, c in zip(ph, Cs))
            Kp, Km = 2 * (sum(p * p for p in ph) + X), 2 * (sum(p * p for p in ph) - X)
            wts[phi] = (Fr(min(max(Kp, 0), D), D), Fr(min(max(Km, 0), D), D))
        phi_rep = (a + tA + 1) % 6                      # both arcs non-empty for this photon phase
        for q, lamA in ((1, D - 1), (-1, 0)):
            pr = Prep(T, Q, L, blk)
            nA = pr.nodes_x(xA, allyz)
            c = ring_b(A, phi_rep)
            for j in range(3):
                pr.set(f"f7.PH{j}", pr.nodes_x(xA + 1, allyz), b=c[j])
                pr.set(f"f7.PH{j}", pr.nodes_x(xA + 2, allyz), a=c[j])
            pr.set("f7.PG", pr.nodes_x(xA + 1, allyz), b=1)
            pr.set("f7.PG", pr.nodes_x(xA + 2, allyz), a=1)
            for j, (aa, bb) in enumerate(ring_state(A, a)):
                pr.set(f"f7.C{j}", nA, a=aa, b=bb)
            pr.set("f7.dAp", nA, r=lamA)
            pr.set("f7.dAm", nA, r=lamA)
            hist = eng.run(pr.state(), steps, history=True)
            rew &= _rewind_ok(eng, hist)
            qa = quotient(T, hist[tA], hist[tA + 1], "f7.dAp", nA) + quotient(T, hist[tA], hist[tA + 1], "f7.dAm", nA)
            if set(qa.tolist()) != {q}:
                raise AssertionError(f"representative token did not give q = {q}")
            nB0 = pr.node(xB, 0, 0)
            for t in range(steps + 1):
                P = [int(values(hist[t], T, f"f7.P{j}")[nB0]) for j in range(3)]
                if q == 1:
                    p_by.setdefault((a, t), P)
                for b in settings:
                    Bv = ring_b(A, b, t)
                    X = sum(bb * pp for bb, pp in zip(Bv, P))
                    n2 = sum(bb * bb for bb in Bv)
                    Kp, Km = 2 * (n2 + X), 2 * (n2 - X)
                    Pp, Pm = Fr(min(max(Kp, 0), D), D), Fr(min(max(Km, 0), D), D)
                    for phi in range(6):
                        w = wts[phi][0] if q == 1 else wts[phi][1]
                        num[(a, b, t)] += w * q * (Pp - Pm)
                        den[(a, b, t)] += w * (Pp + Pm)
    out = {"A": A, "Q": Q, "odd": Q % 2 == 1, "D": D, "gamma": gamma, "cos_k": round(cosk, 6), "c_Q": math.sqrt((Q - 1) / (3 * Q)),
           "d": d, "taxicab_first_snapshot": tA + 1 + d, "round_first_snapshot": tA + 1 + d * math.sqrt(3 * Q / (Q - 1)),
           "per_tB": {}, "rewind_all_runs": rew}
    theta_cw = (-90 - math.degrees(math.acos(cosk)) * d) % 360
    for t in range(steps + 1):
        Et = {(a, b): (num[(a, b, t)] / den[(a, b, t)]) if den[(a, b, t)] else Fr(0) for a in settings for b in settings}
        S = max(abs(Et[(a, b)] + Et[(a, b2)] + Et[(a2, b)] - Et[(a2, b2)])
                for a, a2, b, b2 in itertools.product(settings, repeat=4))
        # best rho, theta for E ~ rho cos(60 (a - b) + theta) (least squares over the 36 settings)
        cs = sum(float(Et[(a, b)]) * math.cos(math.radians(60 * (a - b))) for a in settings for b in settings)
        sn = sum(float(Et[(a, b)]) * math.sin(math.radians(60 * (a - b))) for a in settings for b in settings)
        rho = 2 * math.hypot(cs, sn) / 36
        theta = math.degrees(math.atan2(-sn, cs)) % 360
        resid = max(abs(float(Et[(a, b)]) - rho * math.cos(math.radians(60 * (a - b) + theta)))
                    for a in settings for b in settings)
        out["per_tB"][str(t)] = {"maxS": round(float(S), 6), "max|E|": round(max(abs(float(v)) for v in Et.values()), 6),
                                 "rho": round(rho, 4), "theta_deg": round(theta, 2), "fit_resid": round(resid, 5),
                                 "front_at_Bob_a0": p_by.get((0, t))}
    out["theta_CW_pred_deg"] = round(theta_cw, 2)
    out["recip"] = recip_summary(T)
    return out
