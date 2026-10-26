"""H-Torque-Of-The-Step-2: where in the step's letter the torque is born (a reader, no act).
The board's L2 (MV-S1's density p_b(i) = 2 num SUM_lines (now_(i+b) before_i - now_i before_(i+b)) on the Link i -> i+b,
the moment about the doubled cube centre, the arm 2 r - (c - 1)) read at five phases of every interval: S0 the start,
S1 after the riding lines' one division (node.stepped, before the lays), S2 after the lays (the write), S3 after the swap,
S4 after the close. The step S0 -> S1 is split exactly, Node by Node, by the division's own identity
    ws(i) delta_l(i) = X(i) F_l(i) + (W(i) - ws(i)) (a_l(i) - a'_l(i)) + rho_l(i),
delta = a_next - 2 a + a' the line's second difference (an integer), ws the mean wall at the division, W the mean wall at the kick,
F the force the engine reads (the arrivals turned by the Links + the Node's own term + the curl's term), rho the dropped remainder
(r_start - half(W) + half(ws) - r_end), so the density's change on a Link is 2 num SUM_l (delta_l(i+b) a_l(i) - delta_l(i) a_l(i+b))
and each part of delta gives one term of L's change, as exact quotients of integers (fractions.Fraction; no float):
  LINKS_SYM  the arrivals at the Links' reach read alike from both ends, (e_ij + e_ji) / 2 with e_ij = R_ij X_i / ws_i
  LINKS_ASYM the one-end pace's part, (e_ij - e_ji) / 2 (the clock is the Node's: R_ij = 2 num p_i^2 Q_ij)
  TURN       the Links' turn of the arrivals (the records' coupling to the potential) less the plain arrivals
  OWN        the Node's own weight -(D_i + SUM_j R_ij) a_i, its gradient across the Link
  CURL       the curl's term (gram.term) of the planes with a coupling
  RIDE       the carrier's mean wall moving between the kick and the division, (W - ws)(a - a')
  ROUND      the dropped remainders rho
  REST       what the identity leaves (0 but at a frozen Node, whose lines are restored)
Usage: python tq2_torque.py <world.json> <out.json> [intervals]"""
from __future__ import annotations
import json, sys, time
from fractions import Fraction as Fr
import numpy as np
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.interval import Interval
from event_universe.core.ports import AXES, PORTS, across
from event_universe.core.rule3 import half
from event_universe.links import coupling_of

EPS = {0: (1, 2), 1: (2, 0), 2: (0, 1)}
TERMS = ["LINKS_SYM", "LINKS_ASYM", "TURN", "OWN", "CURL", "RIDE", "ROUND", "REST"]
frac = np.frompyfunc(lambda n, d: Fr(int(n), int(d)), 2, 1)

def density(lines, num):
    out = []
    for b in range(AXES):
        s = 0
        for line in lines:
            s = s + across(line.now, 2 * b) * line.before - line.now * across(line.before, 2 * b)
        out.append(2 * num * s)
    return out

def dp_of(Z, A, num):
    """The density's change on every Link from a per-Node, per-line part Z of delta and the start levels A."""
    out = []
    for b in range(AXES):
        s = 0
        for z, a in zip(Z, A):
            s = s + across(z, 2 * b) * a - z * across(a, 2 * b)
        out.append(2 * num * s)
    return out

def L2_of(p, X, c):
    L = []
    for cc in range(AXES):
        a, b = EPS[cc]
        L.append(sum(((2 * X[a] - (c - 1)) * p[b] - (2 * X[b] - (c - 1)) * p[a]).reshape(-1), Fr(0)))
    return L

def P_of(p):
    return [sum(p[b].reshape(-1), Fr(0)) for b in range(AXES)]

def L2P(recs_lines, nums, X, c):
    L = [0, 0, 0]; P = [0, 0, 0]
    for lines, num in zip(recs_lines, nums):
        p = density(lines, num)
        L = [int(x) + int(y) for x, y in zip(L, L2_of(p, X, c))]
        P = [int(x) + int(y) for x, y in zip(P, P_of(p))]
    return L, P

def s(q):
    return f"{q.numerator}/{q.denominator}" if q.denominator != 1 else str(q.numerator)

def add(u, v):
    return [x + y for x, y in zip(u, v)]

def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    node = Node(universe, world); c = node.cube
    n_int = int(argv[3]) if len(argv) > 3 else int(world["intervals"])
    idx = np.indices(node.shape); X = [idx[a].astype(object) for a in range(AXES)]
    recs = node.records(); nums = [r.pair[0] for r in recs]
    t0 = time.monotonic_ns(); per = []
    tot = {k: [Fr(0)] * 3 for k in TERMS}; tot_abs = {k: [Fr(0)] * 3 for k in TERMS}
    tot_phase = {k: [0, 0, 0] for k in ("step", "write", "swap", "click")}
    for t in range(n_int):
        L0, P0 = L2P([r.lines for r in recs], nums, X, c)
        iv = Interval(node, 1); iv.readings(); iv.kick()
        x_now = iv.x_now
        W_kick = iv.mean_wall(iv.carrier.lines[0])
        pre = {}
        for r in recs:
            k = iv.where[id(r)]
            rule = node.rule_of(r, iv.c, iv.factors)
            turn = iv.links_at[coupling_of(r)]
            A = iv.starts[k]
            pre[k] = dict(A=A, BF=[line.before for line in iv.rows[k]], REM=[line.rem for line in iv.rows[k]],
                          F=iv.force[k], rule=rule, W=iv.scales[k] * W_kick,
                          arr_turned=node.arrivals(A, rule, turn))
        iv.division()
        kc = iv.where[id(iv.carrier)]
        ws_end = iv.mean_wall(iv.out[kc][0])
        L1, P1 = L2P(node.stepped, nums, X, c)
        terms = {k: [Fr(0)] * 3 for k in TERMS}
        frozen = iv.frozen
        for j, r in enumerate(recs):
            k = iv.where[id(r)]; num = nums[j]; d = pre[k]
            ws = iv.scales[k] * ws_end
            W = d["W"]; rule = d["rule"]; A = d["A"]
            new = node.stepped[j]
            delta = [n.now - 2 * a + bf for n, a, bf in zip(new, A, d["BF"])]
            own_k = rule.mass + sum(rule.reaches)
            xw = frac(x_now, ws)  # X / ws at every Node
            Z = {k_: [] for k_ in TERMS[:-1]}
            for l, (a, bf, r0, F, arr_t, n) in enumerate(zip(A, d["BF"], d["REM"], d["F"], d["arr_turned"], new)):
                sym = 0; asym = 0
                for p in range(PORTS):
                    e = rule.reaches[p] * xw
                    e_back = across(rule.reaches[p ^ 1] * xw, p)
                    nb = across(a, p)
                    sym = sym + (e + e_back) * nb
                    asym = asym + (e - e_back) * nb
                Z["LINKS_SYM"].append(sym / 2)
                Z["LINKS_ASYM"].append(asym / 2)
                Z["TURN"].append(arr_t * xw - sym / 2 - asym / 2)
                own = -own_k * a
                Z["OWN"].append(own * xw)
                Z["CURL"].append((F - arr_t - own) * xw)
                Z["RIDE"].append(frac((W - ws) * (a - bf), ws))
                rho = r0 - half(W) + half(ws) - n.rem
                Z["ROUND"].append(frac(rho, ws))
            for k_ in TERMS[:-1]:
                dL = L2_of(dp_of(Z[k_], A, num), X, c)
                terms[k_] = add(terms[k_], dL)
        step = [Fr(x - y) for x, y in zip(L1, L0)]
        summed = [Fr(0)] * 3
        for k_ in TERMS[:-1]:
            summed = add(summed, terms[k_])
        terms["REST"] = [x - y for x, y in zip(step, summed)]
        L2, P2 = L2P([r.lines for r in recs], nums, X, c)
        iv.swap(); top = iv.top
        L3, P3 = L2P([r.lines for r in recs], nums, X, c)
        b0 = node.counts["births"]; cl0 = node.counts["body_clicks"]
        iv.close()
        L4, P4 = L2P([r.lines for r in recs], nums, X, c)
        row = {"i": node.interval, "turned": int(top.sum()), "frozen": int(np.sum(frozen)) if frozen is not None else 0,
               "births": node.counts["births"] - b0, "clicks": node.counts["body_clicks"] - cl0,
               "L2_start": L0, "P_start": P0,
               "dL2_step": [int(q) for q in step],
               "dL2_write": [x - y for x, y in zip(L2, L1)], "dL2_swap": [x - y for x, y in zip(L3, L2)],
               "dL2_click": [x - y for x, y in zip(L4, L3)], "dP_step": [x - y for x, y in zip(P1, P0)],
               "dP_swap": [x - y for x, y in zip(P3, P2)], "dP_click": [x - y for x, y in zip(P4, P3)],
               "L2_end": L4, "P_end": P4, "terms": {k_: [s(q) for q in v] for k_, v in terms.items()}}
        per.append(row)
        for k_ in TERMS:
            tot[k_] = add(tot[k_], terms[k_]); tot_abs[k_] = add(tot_abs[k_], [abs(q) for q in terms[k_]])
        for k_, v in (("step", row["dL2_step"]), ("write", row["dL2_write"]), ("swap", row["dL2_swap"]), ("click", row["dL2_click"])):
            tot_phase[k_] = add(tot_phase[k_], v)
        if (t + 1) % 25 == 0:
            print(json.dumps({"i": node.interval, "L2": L4, "ms": (time.monotonic_ns() - t0) // 10**6}), flush=True)
    rest_nonzero = sum(1 for r in per if any(q != "0" for q in r["terms"]["REST"]))
    out = {"world": argv[1], "cube": c, "intervals": n_int, "rows": [[r.shape, list(r.pair)] for r in recs],
           "per_interval": per, "sum_terms": {k_: [s(q) for q in v] for k_, v in tot.items()},
           "sum_abs_terms": {k_: [s(q) for q in v] for k_, v in tot_abs.items()},
           "sum_phases": tot_phase, "intervals_with_REST_not_0": rest_nonzero,
           "L2_end": per[-1]["L2_end"], "P_end": per[-1]["P_end"],
           "counts": {k: int(v) for k, v in node.counts.items()}, "ms": (time.monotonic_ns() - t0) // 10**6}
    json.dump(out, open(argv[2], "w"))
    print(json.dumps({"done": argv[1], "ms": out["ms"], "L2_end": out["L2_end"], "REST_not_0": rest_nonzero,
                      "sum_abs_terms": out["sum_abs_terms"], "sum_phases": tot_phase}))

if __name__ == "__main__":
    main(sys.argv)
