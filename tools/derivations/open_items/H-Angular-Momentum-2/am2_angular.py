"""H-Angular-Momentum-2: a reader of the orbital angular momentum of the records' rows (no act).
p_b(i) = 2 num SUM_lines (now_(i+b) before_i - now_i before_(i+b)) on the Link i -> i+b (MV-S1's integers);
P_b = SUM_i p_b(i); L_c(z) = SUM_i eps_cab (r_i - z)_a p_b(i), r_i the Node's index in [0, c) on the torus's cut.
L2 is L about the board's centre in doubled coordinates (2 r - (c - 1)), an integer; L0 is L about the origin Node.
Phases per interval: S0 the start; S1 after the riding lines' divisions (before the writes); S2 after the writes;
S3 after the swap at the top; S4 after the close (the clicks). The remainders' part of the step S0 -> S1 is the
exact rational (a quotient of integers) 2 num eps_cab SUM_i X_a(i) [d_(i+b) a_i - d_i a_(i+b)], d_i = (half(ws_i) - rem_i) / ws_i.
Usage: python am2_angular.py <world.json> <out.json>"""
from __future__ import annotations
import json, sys, time
from fractions import Fraction
import numpy as np
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.interval import Interval
from event_universe.core.ports import AXES, across
from event_universe.core.rule3 import half
from event_universe import gram

EPS = {0: (1, 2), 1: (2, 0), 2: (0, 1)}  # eps_cab = +1 for (c, a, b) in these

def ints(a):
    return [int(x) for x in np.asarray(a, dtype=object).reshape(-1)]

def coords(shape):
    idx = np.indices(shape)
    return [idx[a].astype(object) for a in range(AXES)]

def density(lines, num):
    """p_b at every Node for a row, b = 0..2, from the lines' now and before, in the law's integers."""
    out = []
    for b in range(AXES):
        s = 0
        for line in lines:
            s = s + across(line.now, 2 * b) * line.before - line.now * across(line.before, 2 * b)
        out.append(2 * num * s)
    return out

def moments(p, X, c):
    """P_b and L about the origin (L0) and about the centre in doubled coordinates (L2)."""
    P = [int(np.sum(p[b])) for b in range(AXES)]
    L0, L2 = [], []
    for cc in range(AXES):
        a, b = EPS[cc]
        L0.append(int(np.sum(X[a] * p[b] - X[b] * p[a])))
        X2a, X2b = 2 * X[a] - (c - 1), 2 * X[b] - (c - 1)
        L2.append(int(np.sum(X2a * p[b] - X2b * p[a])))
    return P, L0, L2

def read(rows_lines, nums, X, c):
    found = {}
    tot = {"P": [0] * 3, "L0": [0] * 3, "L2": [0] * 3}
    for k, (lines, num) in enumerate(zip(rows_lines, nums)):
        P, L0, L2 = moments(density(lines, num), X, c)
        found[str(k)] = {"P": P, "L0": L0, "L2": L2}
        for key, v in (("P", P), ("L0", L0), ("L2", L2)):
            tot[key] = [x + y for x, y in zip(tot[key], v)]
    found["sum"] = tot
    return found

def rem_part(lines, num, X, c, ws):
    """The remainders' part of the step on one row's L2 (exact rationals as numerator/denominator strings) and on P."""
    sh = lines[0].now.shape
    d = []
    for line in lines:
        hw = half(ws)
        d.append(np.vectorize(lambda h, r, w: Fraction(int(h) - int(r), int(w)), otypes=[object])(hw, line.rem, ws))
    out_L, out_P = [], []
    pb = []
    for b in range(AXES):
        s = np.zeros(sh, dtype=object)
        for line, dl in zip(lines, d):
            a0 = line.before  # the start level a (the new line's before)
            s = s + across(dl, 2 * b) * a0 - dl * across(a0, 2 * b)
        pb.append(2 * num * s)
        out_P.append(sum(pb[b].reshape(-1), Fraction(0)))
    for cc in range(AXES):
        a, b = EPS[cc]
        X2a, X2b = 2 * X[a] - (c - 1), 2 * X[b] - (c - 1)
        out_L.append(sum((X2a * pb[b] - X2b * pb[a]).reshape(-1), Fraction(0)))
    return [f"{q.numerator}/{q.denominator}" for q in out_L], [f"{q.numerator}/{q.denominator}" for q in out_P], out_L, out_P

def diff(a, b):
    return [x - y for x, y in zip(a, b)]

def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    node = Node(universe, world)
    c = node.cube
    X = coords(node.shape)
    recs = node.records()
    nums = [r.pair[0] for r in recs]
    rec_idx = [node.rows_.index(r) for r in recs]
    t0 = time.monotonic_ns()
    per = []
    start = read([r.lines for r in recs], nums, X, c)
    out = {"world": argv[1], "cube": c, "intervals": int(world["intervals"]), "rows": [[r.shape, list(r.pair)] for r in recs],
           "start": start, "per_interval": per}
    for t in range(int(world["intervals"])):
        s0 = read([r.lines for r in recs], nums, X, c)
        iv = Interval(node, 1)
        iv.walled_act(); iv.forces(); iv.kicks(); iv.carrier_act(); iv.divisions()
        s1 = read([iv.out[k] for k in rec_idx], nums, X, c)
        # the remainders' part of the step per row (exact rationals)
        rem_rows = {}
        rem_sum_L = [Fraction(0)] * 3
        rem_sum_P = [Fraction(0)] * 3
        for j, k in enumerate(rec_idx):
            ws = iv.scales[k] * iv.w_div
            sL, sP, fL, fP = rem_part(iv.out[k], nums[j], X, c, ws)
            rem_rows[str(j)] = {"L2": sL, "P": sP}
            rem_sum_L = [x + y for x, y in zip(rem_sum_L, fL)]
            rem_sum_P = [x + y for x, y in zip(rem_sum_P, fP)]
        iv.writes()
        node.set_rows(iv.out)
        iv.rest()
        s2 = read([r.lines for r in recs], nums, X, c)
        counters = ([a.copy() for a in node.standing], [a.copy() for a in node.crossed], [a.copy() for a in node.beats])
        top = node.swap(iv.held, iv.frozen)
        s3 = read([r.lines for r in recs], nums, X, c)
        log_from = len(node.log)
        births0 = node.counts["births"]; clicks0 = node.counts["body_clicks"]
        node.click(iv.plane_starts, iv.held)
        node.stack.append({"turned": top, "counters": counters, "log_from": log_from, "frozen": iv.frozen})
        s4 = read([r.lines for r in recs], nums, X, c)
        step_L2 = diff(s1["sum"]["L2"], s0["sum"]["L2"])
        rat_L2 = [Fraction(x) - y for x, y in zip(step_L2, rem_sum_L)]
        per.append({
            "i": node.interval,
            "turned": int(top.sum()),
            "births": node.counts["births"] - births0,
            "clicks": node.counts["body_clicks"] - clicks0,
            "L2_start": s0["sum"]["L2"], "P_start": s0["sum"]["P"],
            "dL2_step": step_L2, "dP_step": diff(s1["sum"]["P"], s0["sum"]["P"]),
            "dL2_step_remainders": [f"{q.numerator}/{q.denominator}" for q in rem_sum_L],
            "dP_step_remainders": [f"{q.numerator}/{q.denominator}" for q in rem_sum_P],
            "dL2_step_rational": [f"{q.numerator}/{q.denominator}" for q in rat_L2],
            "dL2_write": diff(s2["sum"]["L2"], s1["sum"]["L2"]), "dP_write": diff(s2["sum"]["P"], s1["sum"]["P"]),
            "dL2_swap": diff(s3["sum"]["L2"], s2["sum"]["L2"]), "dP_swap": diff(s3["sum"]["P"], s2["sum"]["P"]),
            "dL2_click": diff(s4["sum"]["L2"], s3["sum"]["L2"]), "dP_click": diff(s4["sum"]["P"], s3["sum"]["P"]),
            "L2_end": s4["sum"]["L2"], "P_end": s4["sum"]["P"],
            "rows_end": {k: v for k, v in s4.items() if k != "sum"},
            "rows_step_remainders": rem_rows,
        })
        if (t + 1) % 20 == 0:
            print(json.dumps({"i": node.interval, "L2": s4["sum"]["L2"], "P": s4["sum"]["P"], "ms": (time.monotonic_ns() - t0) // 10**6}), flush=True)
    # the packet's L about its own centroid: W L_cent = W L0 - (SUM w r) x P, per row, at the end (weight = the row's form)
    cent = {}
    for j, r in enumerate(recs):
        nows = [line.now for line in r.lines]
        w = gram.form(gram.gram(r.shape), nows, nows)
        W = int(np.sum(w))
        if W == 0:
            continue
        m = [int(np.sum(w * X[a])) for a in range(AXES)]
        P, L0, _ = moments(density(r.lines, r.pair[0]), X, c)
        WL = []
        for cc in range(AXES):
            a, b = EPS[cc]
            WL.append(W * L0[cc] - (m[a] * P[b] - m[b] * P[a]))
        cent[str(j)] = {"W": W, "moment": m, "P": P, "L0": L0, "W_L_about_centroid": WL}
    out["end_about_centroid"] = cent
    out["counts"] = {k: int(v) for k, v in node.counts.items()}
    out["ms"] = (time.monotonic_ns() - t0) // 10**6
    with open(argv[2], "w", encoding="utf-8") as f:
        json.dump(out, f)
    print(json.dumps({"done": argv[1], "ms": out["ms"], "L2_end": per[-1]["L2_end"], "P_end": per[-1]["P_end"]}))

if __name__ == "__main__":
    main(sys.argv)
