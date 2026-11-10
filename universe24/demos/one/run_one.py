"""ONE bang run (Study 22, ONE-A): T3 / T4 of s22/ONE-A_NOTES.md (pre-registered 14:49:43 UTC).

THE RUN LOOP (``forward``) does nothing but call Engine.step (Rule3) on the composed ONE tensor: no f(t), no hold, no
intervention, no branch (OWNER rule, manager 14:47 UTC). Every measurement reads the yielded snapshots (read-only); the
driver may only STOP iterating (horizon / wall budget). Outputs go to --out (never to the package's results/).

usage: python -m universe24.demos.one.run_one --L 6 --bang jpure --rng 13 --tmax 1200 --budget 1500
                                                              --tag T3_main --out DIR [--rewind] [--compare OTHER.json]
       [--uncoupled (ONE v1: the default, as run for T3/T4) | --couple (C1, OPT-IN ONLY: NEW LAW candidate, REJECTED
        by the owner; runaway measured in Study 30; kept for the record)] [--theta0 N] [--mass_m M]
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import sys
import time
import zlib
from pathlib import Path

import numpy as np

from ...core.engine import Engine, OBJ
from ...core.tensor import compose
from ...layers.one import COSMIC_NS, COUPLING_STATUS, one_system
from ...observe.one import (CosmicLedger, CosmicView, flat, flat_ab, knz, namespace_bits, rel_distance,
                            state_hash)
from ...prepare.one import one_seed

sys.set_int_max_str_digits(0)


def utc() -> str:
    return time.strftime("%a %b %d %H:%M:%S UTC %Y", time.gmtime())


def forward(engine: Engine, state, n: int):
    """THE run loop: n Rule3 steps of the composed tensor, nothing else. Yields (t, state_t)."""
    for t in range(1, n + 1):
        state = engine.step(state)
        yield t, state


def build(L: int, bang: str, rng_seed: int, system_kw: dict | None = None):
    S = one_system(**(system_kw or {}))
    T = compose(*S.blocks)
    E = Engine(T, S.Q)
    s0, rep = one_seed(S, T, L, bang=bang, rng_seed=rng_seed)
    return S, T, E, s0, rep


def theorem_o_a_structural(T) -> dict:
    """THEOREM O (a)/(Theta) rows on the TENSOR: pair inputs read only the Theta readers (M1, M2) and loads; every
    reader input carries exactly one hand factor; every hand term is odd (degree 1) in the hand."""
    names = T.names
    idx = {n: i for i, n in enumerate(names)}
    th, m1, m2 = idx[f"{COSMIC_NS}.Th"], idx[f"{COSMIC_NS}.M1"], idx[f"{COSMIC_NS}.M2"]
    lp, lm = idx[f"{COSMIC_NS}.Lp"], idx[f"{COSMIC_NS}.Lm"]
    dp, dm = idx[f"{COSMIC_NS}.dp"], idx[f"{COSMIC_NS}.dm"]
    bad_pair = bad_reader = bad_hand = 0
    n_pair = n_reader = n_hand = 0
    for m in T.monomials:
        gs = [f.gear for f in m.factors]
        if m.target in (dp, dm):
            n_pair += 1
            bad_pair += int(not all(g in (m1, m2, lp, lm) for g in gs) or sum(g in (m1, m2) for g in gs) != 2)
        elif m.target in (m1, m2):
            n_reader += 1
            bad_reader += int(gs.count(th) != 1 or sum(g in (m1, m2) for g in gs) != 1)
        elif m.target == th:
            n_hand += 1
            bad_hand += int(gs.count(th) != 1 or any(g in (m1, m2) for g in gs))
    return {"pair_terms": n_pair, "pair_terms_not_from_readers": bad_pair, "reader_terms": n_reader,
            "reader_terms_not_theta_x_odd": bad_reader, "hand_terms": n_hand, "hand_terms_not_odd_or_sourced": bad_hand,
            "holds": bad_pair == 0 and bad_reader == 0 and bad_hand == 0}


def run(args) -> dict:
    t_wall = time.time()
    skw = {}
    if args.couple:
        skw["couple_doublet"] = True
    if args.uncoupled:
        skw["couple_doublet"] = False
    if args.theta0:
        skw["theta0"] = args.theta0
    if args.mass_m:
        skw["package_kw"] = {"mass": args.mass_m << 22}
    S, T, E, s0, rep = build(args.L, args.bang, args.rng, skw)
    Q, D = S.Q, 6 * S.Q
    cp = S.info["one"]["cosmic_params"]
    h, theta0 = cp["h"], cp["theta0"]
    L, N = args.L, args.L ** 3
    v = CosmicView(T)
    led = CosmicLedger(v, s0, h, cp["c_pair"])
    names = T.names
    ns_of = [n.split(".", 1)[0] for n in names]
    ns_rows = {k: np.array([i for i, x in enumerate(ns_of) if x == k], dtype=np.intp) for k in sorted(set(ns_of))}
    pkg_ns = [k for k in ns_rows if k != COSMIC_NS]
    mrows = [v.rows["M1"], v.rows["M2"]]
    pm_rows = list(ns_rows["matter"]) + list(ns_rows.get("matter2", []))
    b0_c, ab0_c, k0_c = flat(s0, mrows), flat_ab(s0, mrows), knz(s0, mrows, N)
    b0_p = flat(s0, pm_rows)
    lapse = T.gear_index(S.info["lapse_field"])
    P = S.info["P"]
    from ...observe.em import lorenz_C
    from ...observe.system import dressed_continuity_residual
    C0 = np.asarray(lorenz_C(s0, T), dtype=OBJ)
    mparams = S.by_name("matter").params
    meta = {"tag": args.tag, "start": utc(), "L": L, "bang": args.bang, "rng": args.rng, "tmax": args.tmax,
            "budget_s": args.budget, "Q": Q, "G": T.G, "monomials": len(T), "rank": T.rank,
            "designations": len(T.designations), "dynamics_fingerprint": T.dynamics_fingerprint,
            "fingerprint": T.fingerprint, "cosmic_params": {k: cp[k] for k in ("theta0", "h", "k_theta", "g_w", "c_pair", "load_sum")},
            "seed": rep, "theorem_o_a_structural": theorem_o_a_structural(T), "system_kw": {k: str(v) for k, v in skw.items()},
            "coupling": S.info["one"].get("coupling")}
    print(json.dumps({k: meta[k] for k in ("tag", "start", "G", "monomials", "dynamics_fingerprint")}), flush=True)
    rows, dist_c, dist_cab, dist_k, dist_p, hashes, outc, bits_log = [], [], [], [], [], [], [], []
    Dhist = {0: v.delta(s0)}
    win, windows = None, []
    def new_win():
        return {"t0": None, "matter_clicks": 0, "pair_event_nodes": 0, "pair_events": 0, "pkg_official": 0,
                "pkg_official_by_ns": {}}
    win = new_win()
    sampled = {"click_ledger_checks": 0, "click_ledger_fail": 0, "lorenz_fail_updates": 0,
               "dressed_continuity_checks": 0, "dressed_continuity_nonzero_nodes": 0}
    prev = s0
    t_end = 0
    maxbits_seen = 0
    for t, s in forward(E, s0, args.tmax):
        t_end = t
        led.update(prev, s)
        hd = v.hand(s)
        I_sum = int(np.sum(v.intensity(prev)))
        rows.append((t, hd["mean"], hd["split"], hd["min"], hd["max"], I_sum))
        Dhist[t] = v.delta(s)
        dist_c.append((t,) + rel_distance(flat(s, mrows), b0_c))
        dist_cab.append((t,) + rel_distance(flat_ab(s, mrows), ab0_c))
        dist_k.append((t,) + rel_distance(knz(s, mrows, N), k0_c))
        dist_p.append((t,) + rel_distance(flat(s, pm_rows), b0_p))
        lp = v.quotients(prev, s, "dp")
        lm = v.quotients(prev, s, "dm")
        outc.append(tuple(int(x) for x in lp.ravel()))
        m1q, m2q = v.quotients(prev, s, "M1"), v.quotients(prev, s, "M2")
        win["matter_clicks"] += int(np.sum(m1q != 0) + np.sum(m2q != 0))
        win["pair_event_nodes"] += int(np.sum((lp != 0) | (lm != 0)))
        win["pair_events"] += int(np.sum(lp - lm))
        cl = E.clicks(prev, s)
        offi = [g for g, lab in zip(cl.gear, cl.label) if lab == "official" and ns_of[g] != COSMIC_NS]
        win["pkg_official"] += len(offi)
        for g in offi:
            k = ns_of[g]
            win["pkg_official_by_ns"][k] = win["pkg_official_by_ns"].get(k, 0) + 1
        C = np.asarray(lorenz_C(s, T), dtype=OBJ)
        sampled["lorenz_fail_updates"] += int(np.any(C != C0))
        if t % 20 == 1:
            K = 2 * np.asarray(E.inputs(prev)).astype(OBJ)
            ell = np.asarray(s.b).astype(OBJ) + np.asarray(prev.a).astype(OBJ)
            ok = D * ell == K + np.asarray(prev.r).astype(OBJ) - np.asarray(s.r).astype(OBJ)
            sampled["click_ledger_checks"] += int(ok.size)
            sampled["click_ledger_fail"] += int(ok.size - np.sum(ok))
            res = np.asarray(dressed_continuity_residual(prev, s, T, D, mparams, P), dtype=OBJ)
            sampled["dressed_continuity_checks"] += int(res.size)
            sampled["dressed_continuity_nonzero_nodes"] += int(np.sum(res != 0))
        nb = namespace_bits(s, ns_rows)
        mb = max(nb[k] for k in pkg_ns)
        maxbits_seen = max(maxbits_seen, mb)
        F = np.asarray(s.b[lapse]).astype(OBJ)
        Um = int(np.sum(F)) / F.size / (2 * P)
        if t % 10 == 0:
            bits_log.append({"t": t, "pkg_maxbits": mb, "top": sorted(nb.items(), key=lambda kv: -kv[1])[:4],
                             "U_mean": Um, "hand_mean_over_theta0": hd["mean"] / theta0,
                             "split_over_theta0": hd["split"] / theta0, "dist_cosmic": dist_c[-1][1],
                             "dist_pkg_matter": dist_p[-1][1]})
        if t % 50 == 0:
            print(json.dumps(bits_log[-1]), flush=True)
        hashes.append((t, state_hash(s, np.array([v.rows["Th"], v.rows["M1"], v.rows["M2"]], dtype=np.intp)),
                       state_hash(s, v.package_rows),
                       hashlib.sha256(",".join(str(int(x)) for x in Dhist[t].ravel()).encode()).hexdigest(),
                       state_hash(s, np.array([v.rows["dp"], v.rows["dm"], v.rows["Lp"], v.rows["Lm"]], dtype=np.intp))))
        if t % 50 == 0:
            win["t_end"] = t
            windows.append(win)
            win = new_win()
        prev = s
        if mb > 200 or time.time() - t_wall > args.budget:
            break
    s_final = prev
    wall_fwd = time.time() - t_wall
    # ------------------------------------------------------------ zeros of the board-mean hand + THEOREM O defects
    zeros = []
    for i in range(1, len(rows)):
        t1, m1_ = rows[i][0], rows[i][1]
        t0_, m0_ = rows[i - 1][0], rows[i - 1][1]
        if m1_ == 0 or (m0_ != 0 and (m0_ > 0) != (m1_ > 0)):
            tz = t1 if m1_ == 0 else t0_ + m0_ / (m0_ - m1_)
            ti = int(round(tz))
            r = rows[ti - 1] if 1 <= ti <= len(rows) else None
            dsym = None
            if (ti + 1) in Dhist and (ti - 1) in Dhist:
                dd = Dhist[ti + 1] - Dhist[ti - 1]
                dsym = {"max_abs": int(max(abs(int(x)) for x in dd.ravel())), "nodes_nonzero": int(np.sum(dd != 0))}
            zeros.append({"t_cross": round(tz, 4), "nearest_int": ti,
                          "(b) Delta(t+1)-Delta(t-1)": dsym,
                          "(c) mean_at_int_over_theta0": (r[1] / theta0) if r else None,
                          "(d) split_at_int_over_theta0": (r[2] / theta0) if r else None,
                          "min_max_at_int": [r[3], r[4]] if r else None})
    # ------------------------------------------------------------ echoes (local minima of the seed distances)
    def minima(dist, thr):
        out = []
        for i in range(1, len(dist) - 1):
            if dist[i][1] < dist[i - 1][1] and dist[i][1] <= dist[i + 1][1] and dist[i][1] < thr:
                out.append((dist[i][0], round(dist[i][1], 6), dist[i][2]))
        return out
    mins_c, mins_cab, mins_k = minima(dist_c, 0.5), minima(dist_cab, 0.5), minima(dist_k, 0.6)
    mins_p = minima(dist_p, 0.5)
    bangs = [m for m in mins_c if m[1] < 0.05]
    bt = [0]
    for m in bangs:
        if m[0] - bt[-1] > 20:
            bt.append(m[0])
    pkg_at_bangs = [{"t": b, "dist_pkg_matter": dist_p[b - 1][1]} for b in bt[1:]]
    # ------------------------------------------------------------ per-aeon records
    aeon_stats = []
    for i in range(len(bt) - 1):
        seg = outc[bt[i]:bt[i + 1]]
        raw = ";".join(",".join(map(str, o)) for o in seg).encode()
        wsel = [w for w in windows if bt[i] < w["t_end"] <= bt[i + 1]]
        aeon_stats.append({"aeon": i + 1, "t0": bt[i], "t1": bt[i + 1], "updates": bt[i + 1] - bt[i],
                           "pair_outcomes_plus": sum(sum(o) for o in seg), "zlib_outcomes": len(zlib.compress(raw, 9)),
                           "matter_clicks_windows": sum(w["matter_clicks"] for w in wsel),
                           "pkg_official_clicks_windows": sum(w["pkg_official"] for w in wsel)})
    for i in range(1, len(aeon_stats)):
        A0, A1 = outc[bt[i - 1]:bt[i]], outc[bt[i]:bt[i + 1]]
        n = min(len(A0), len(A1))
        diff = sum(1 for j in range(n) for x, y in zip(A0[j], A1[j]) if x != y)
        aeon_stats[i]["outcome_entries_differing_vs_prev"] = diff
        aeon_stats[i]["entries_compared"] = n * N
        joint = len(zlib.compress(";".join(",".join(map(str, o)) for o in A0 + A1).encode(), 9))
        aeon_stats[i]["zlib_joint_minus_prev"] = joint - aeon_stats[i - 1]["zlib_outcomes"]
    born = led.born_frequencies(s0, cp["load_sum"])
    # ------------------------------------------------------------ rewind (audit map; never part of the run)
    rewind = None
    if args.rewind:
        t1 = time.time()
        rewind = {"exact": bool(E.rewind(s_final, t_end).same_as(s0)), "updates": t_end, "wall_s": round(time.time() - t1, 1)}
    out = {"meta": meta, "end": utc(), "t_end": t_end, "wall_forward_s": round(wall_fwd, 1), "engine_stats": dict(E.stats),
           "max_pkg_bits": maxbits_seen, "rewind": rewind, "cosmic_ledger_failures": led.fail,
           "cosmic_ledger_checks": led.checks, "events_total": led.events_total, "born": born,
           "sampled_ledgers": sampled, "zeros": zeros, "echo_minima_cosmic_b": mins_c[:40],
           "echo_minima_cosmic_ab": mins_cab[:40], "echo_minima_pkg_matter": mins_p[:60], "echo_minima_cosmic_knz": mins_k[:40], "bangs_lt_0.05": bangs,
           "bang_times": bt, "pkg_matter_distance_at_bangs": pkg_at_bangs,
           "pkg_matter_min_distance_after_t20": min((d for d in dist_p if d[0] > 20), key=lambda d: d[1], default=None),
           "aeon_stats": aeon_stats, "windows": windows, "bits_log": bits_log, "hand_rows_every5": rows[::5],
           "hashes": hashes, "_outcomes": outc}
    return out


def compare(a: dict, b: dict) -> dict:
    """T4: bit-identical history (hand+matter, package, Delta) vs differing outcomes (pairs, loads)."""
    ha, hb = a["hashes"], b["hashes"]
    n = min(len(ha), len(hb))
    same = {"hand_matter": 0, "package": 0, "delta": 0, "pairs_loads": 0}
    for i in range(n):
        for k, j in (("hand_matter", 1), ("package", 2), ("delta", 3), ("pairs_loads", 4)):
            same[k] += int(ha[i][j] == hb[i][j])
    return {"updates_compared": n, "identical_updates": same}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=int, default=6)
    ap.add_argument("--bang", default="jpure")
    ap.add_argument("--rng", type=int, default=13)
    ap.add_argument("--tmax", type=int, default=1200)
    ap.add_argument("--budget", type=float, default=1500.0)
    ap.add_argument("--tag", default="T3_main")
    ap.add_argument("--out", required=True)
    ap.add_argument("--rewind", action="store_true")
    ap.add_argument("--compare", default=None)
    ap.add_argument("--couple", action="store_true",
                    help=f"C1, opt-in only: couple_doublet=True ({COUPLING_STATUS})")
    ap.add_argument("--uncoupled", action="store_true",
                    help="ONE v1: block-diagonal (couple_doublet=False); the default of one_system, same as no flag")
    ap.add_argument("--theta0", type=int, default=0)
    ap.add_argument("--mass_m", type=int, default=0, help="package matter mass = m * 2^22 (default: the package's 4915)")
    args = ap.parse_args(argv)
    out = run(args)
    od = Path(args.out)
    od.mkdir(parents=True, exist_ok=True)
    if args.compare:
        other = json.loads(Path(args.compare).read_text())
        out["compare_with"] = {"file": args.compare, "result": compare(other, out)}
    outc = out.pop("_outcomes")
    with gzip.open(od / f"{args.tag}_outcomes.json.gz", "wt") as fh:
        json.dump(outc, fh)
    if args.compare:
        oc = Path(args.compare).with_name(Path(args.compare).stem + "_outcomes.json.gz")
        if oc.exists():
            with gzip.open(oc, "rt") as fh:
                other_o = json.load(fh)
            n = min(len(other_o), len(outc))
            diff = sum(1 for i in range(n) for x, y in zip(other_o[i], outc[i]) if x != y)
            lit = sum(1 for i in range(n) for x, y in zip(other_o[i], outc[i]) if x != 0 or y != 0)
            out["compare_with"]["outcomes"] = {"updates": n, "entries": n * len(outc[0]), "differing": diff,
                                               "lit_entries": lit, "differing_over_lit": diff / lit if lit else None}
    (od / f"{args.tag}.json").write_text(json.dumps(out, default=str))
    summ = {k: out[k] for k in ("t_end", "wall_forward_s", "max_pkg_bits", "rewind", "cosmic_ledger_failures",
                                "born", "sampled_ledgers", "bang_times", "zeros")}
    summ["echo_minima_cosmic_b"] = out["echo_minima_cosmic_b"][:12]
    summ["pkg_matter_distance_at_bangs"] = out["pkg_matter_distance_at_bangs"]
    summ["echo_minima_pkg_matter"] = out["echo_minima_pkg_matter"][:20]
    summ["aeon_stats"] = out["aeon_stats"]
    if "compare_with" in out:
        summ["compare_with"] = out["compare_with"]
    print("SUMMARY", json.dumps(summ, default=str), flush=True)


if __name__ == "__main__":
    main()
