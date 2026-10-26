"""H-Torque-Of-The-Step-1: where in the step's letter the torque on the board's L is born (a reader, no act).

The board's L (am1/am2's reading of MV-S1 about the doubled cube centre): 2 L_c = SUM over Links (i, i+a) of
eps_cba d_b(i) p_a(i), p_a(i) = 2 num SUM_lines (now_(i+a) before_i - now_i before_(i+a)), d the doubled offset of
the Node from the centre, 2 x - (c - 1).

The riding line's division as built (interval.division): W v + rem' = W (now - before) + rem + X F, next = now + v,
so exactly  next_i = 2 now_i - before_i + g_i,  g_i = (X_i F_i + rem_i - rem'_i) / W_i,  W_i the mean wall at the Node.
Then for every Link  delta p_a(i) = 2 num SUM_lines (g_(i+a) now_i - g_i now_(i+a))  (the Wronskian's own identity:
the 2 now - before part conserves p_a(i) line by line).  So the step's change of L is a sum over Links of local
terms, one per term of g, each a function of the Link's two ends and their six Links:
  rounding   g^r_i = (rem_i - rem'_i) / W_i                      (the dropped remainder of the Node's division)
  mass       g^m_i = -(X_i / W_i) D_i now_i                     (the Node's own clock in the record's mass)
  link sym   g^s_i = SUM_j Ks_ij (now_j - now_i)                 Ks_ij = (K_ij + K_ji) / 2,  K_ij = X_i R_ij / W_i
  link asym  g^a_i = SUM_j Ka_ij (now_j - now_i)                 Ka_ij = (K_ij - K_ji) / 2  (the pace not shared by the ends)
  curl       g^c_i = (X_i / W_i) term_i                          (the potential's odd lines rotating the row)
  turn       g^t_i = (X_i / W_i) (arrivals turned - arrivals plain)   (the Link's record turning the arrival)
  ride       g^w_i = (Wb_i - W_i) (now_i - before_i - 1/2) / W_i       (the kick read at the carrier's mean wall before its
             act, Wb, the division at the mean wall after it, W: the content's own motion within the interval)
The identity checked at every interval: the integer change of 2 L across the divisions equals the sum of the six
rational torques, exactly (Fractions of integers; no float).  Then the lays' write, the swap and the close, each the
integer difference of the reading before and after the act.
Usage: python tq1_torque.py <record_cache.json> <out.json>"""
from __future__ import annotations

import json
import sys
import time
from fractions import Fraction

import numpy as np

from event_universe import gram
from event_universe.core.ports import AXES, PORTS, across
from event_universe.core.rule3 import quotient
from event_universe.interval import Interval
from event_universe.links import coupling_of
from event_universe.node import Node

EPS = {0: (1, 2), 1: (2, 0), 2: (0, 1)}  # eps_cab = +1 for (c, a, b)
TERMS = ("ride", "rounding", "mass", "link_sym", "link_asym", "curl", "turn")


def ints(a):
    return [int(x) for x in np.asarray(a, dtype=object).reshape(-1)]


def frac(a):
    """An object array of Fractions from an integer array."""
    return np.vectorize(lambda v: Fraction(int(v)), otypes=[object])(np.asarray(a, dtype=object))


def read_L(recs, D):
    """2 L about the doubled centre and P, integers, summed over the record rows."""
    L = [0, 0, 0]
    P = [0, 0, 0]
    for r in recs:
        num = int(r.pair[0])
        p = []
        for b in range(AXES):
            s = 0
            for line in r.lines:
                s = s + across(line.now, 2 * b) * line.before - line.now * across(line.before, 2 * b)
            p.append(2 * num * s)
        for b in range(AXES):
            P[b] += int(np.sum(p[b]))
        for cc in range(AXES):
            a, b = EPS[cc]
            L[cc] += int(np.sum(D[a] * p[b] - D[b] * p[a]))
    return L, P


def torque_of(g_lines, now_lines, num, D):
    """The torque of a per-Node term g (a list of Fraction arrays, one per line) on 2 L: SUM over Links of
    eps d x e_a 2 num SUM_lines (g_(i+a) now_i - g_i now_(i+a)), and its push on P."""
    dp = []
    for a in range(AXES):
        s = 0
        for g, n in zip(g_lines, now_lines):
            s = s + across(g, 2 * a) * n - g * across(n, 2 * a)
        dp.append(2 * num * s)
    L = []
    for cc in range(AXES):
        a, b = EPS[cc]
        L.append(sum((D[a] * dp[b] - D[b] * dp[a]).reshape(-1), Fraction(0)))
    P = [sum(dp[a].reshape(-1), Fraction(0)) for a in range(AXES)]
    return L, P


def fstr(q):
    return f"{q.numerator}/{q.denominator}"


def main(argv):
    sys.set_int_max_str_digits(0)
    cache = json.load(open(argv[1]))
    universe, world = cache["universe"], cache["world"]
    node = Node(universe, world)
    c = node.cube
    idx = np.indices(node.shape)
    D = [2 * idx[a].astype(object) - (c - 1) for a in range(AXES)]
    recs = node.records()
    t0 = time.monotonic_ns()
    per = []
    identity_misses = 0
    line_misses = 0
    totals = {t: [Fraction(0)] * 3 for t in TERMS}
    tot_abs = {t: [Fraction(0)] * 3 for t in TERMS}
    tot_int = {"lays": [0] * 3, "swap": [0] * 3, "click": [0] * 3, "step": [0] * 3}
    tot_absint = {"lays": [0] * 3, "swap": [0] * 3, "click": [0] * 3, "step": [0] * 3}
    bound_total = [0, 0, 0]
    L_start, _ = read_L(recs, D)
    for step_k in range(int(world["intervals"])):
        L0, P0 = read_L(recs, D)
        iv = Interval(node, 1)
        iv.readings()
        iv.kick()
        # the division, by hand so that the rows after the divisions and before the lays can be read
        carrier = iv.carrier
        k_c = iv.where[id(carrier)]
        from event_universe.core.rule3 import held_numerator, division_forward, half
        p02 = iv.p0 * iv.p0
        numerators = [held_numerator(node.trace, iv.x_now, iv.forms, iv.trace, iv.p0, node.den, node.gamma)]
        numerators += [iv.traceless[a] * p02 for a in range(AXES)] + [None] * (carrier.shape - 1 - AXES)
        iv.out[k_c] = node.carried(iv.rows[k_c], node.rule_of(carrier, iv.c, iv.factors), numerators, 1, *iv.ends(carrier))
        w_div = iv.mean_wall(iv.out[k_c][0])
        w_side = iv.mean_wall(iv.carrier.lines[0])
        from event_universe.rows import Line
        terms_L = {t: [Fraction(0)] * 3 for t in TERMS}
        terms_P = {t: [Fraction(0)] * 3 for t in TERMS}
        bound = [0, 0, 0]
        rows_out = {}
        for r in iv.riders:
            k = iv.where[id(r)]
            ws = iv.scales[k] * w_div
            new = []
            for a, p, line in zip(iv.starts[k], iv.kicked[k], iv.rows[k], strict=True):
                v, rem = division_forward(p, ws, half(ws))
                new.append(Line(a + v, a, rem, ws, line.wr, line.wwall))
            iv.out[k] = new
            if r in iv.records:
                iv.plane_starts.append(list(iv.rows[k]))
                iv.stepped.append([line.copy() for line in new])
                num = int(r.pair[0])
                rule = node.rule_of(r, iv.c, iv.factors)
                turn = iv.links_at[coupling_of(r)]
                starts = iv.starts[k]
                X = frac(iv.x_now)
                W = frac(ws)
                Wb = frac(iv.scales[k] * w_side)
                XW = X / W
                # the identity per line: W (next - 2 now + before) = X F + rem - rem'
                for a, f, line, nl in zip(starts, iv.force[k], iv.rows[k], new, strict=True):
                    lhs = 2 * ws * (nl.now - 2 * a + line.before)
                    rhs = 2 * (iv.x_now * f + line.rem - nl.rem) + (iv.scales[k] * w_side - ws) * (2 * (a - line.before) - 1)
                    if any(int(x) != 0 for x in (lhs - rhs).reshape(-1)):
                        line_misses += 1
                # the terms of g per line
                arr_turned = node.arrivals(starts, rule, turn)
                arr_plain = node.arrivals(starts, rule, None)
                coefficient = quotient(sum(rule.reaches), iv.scales[k])
                added = gram.term(r.shape, coefficient, iv.curl, starts)
                sum_R = sum(rule.reaches)
                # K_ij = X_i R_ij / W_i per Port, and its mirror from the other end
                K = [XW * frac(np.asarray(rule.reaches[port]) + 0 * iv.x_now) for port in range(PORTS)]
                K_other = [across(K[port ^ 1], port) for port in range(PORTS)]  # K_ji read at i: the neighbour's reach on the Link back
                Ks = [(x + y) / 2 for x, y in zip(K, K_other)]
                Ka = [(x - y) / 2 for x, y in zip(K, K_other)]
                g = {t: [] for t in TERMS}
                for a, f, line, nl, at, ap, ad in zip(starts, iv.force[k], iv.rows[k], new, arr_turned, arr_plain, added, strict=True):
                    af = frac(a)
                    g["rounding"].append((frac(line.rem) - frac(nl.rem)) / W)
                    g["ride"].append((Wb - W) * (af - frac(line.before) - Fraction(1, 2)) / W)
                    g["mass"].append(-XW * frac(rule.mass) * af)
                    gs = 0
                    ga = 0
                    for port in range(PORTS):
                        diff = frac(across(a, port)) - af
                        gs = gs + Ks[port] * diff
                        ga = ga + Ka[port] * diff
                    g["link_sym"].append(gs)
                    g["link_asym"].append(ga)
                    g["curl"].append(XW * frac(ad))
                    g["turn"].append(XW * (frac(at) - frac(ap)))
                    # the identity of the terms: SUM g = (X F + rem - rem') / W
                    total_g = g["ride"][-1] + g["rounding"][-1] + g["mass"][-1] + gs + ga + g["curl"][-1] + g["turn"][-1]
                    want = frac(nl.now) - 2 * af + frac(line.before)
                    if any(x != 0 for x in (total_g - want).reshape(-1)):
                        line_misses += 1
                nows = [frac(a) for a in starts]
                row_terms = {}
                for tname in TERMS:
                    Lt, Pt = torque_of(g[tname], nows, num, D)
                    row_terms[tname] = [fstr(q) for q in Lt]
                    terms_L[tname] = [x + y for x, y in zip(terms_L[tname], Lt)]
                    terms_P[tname] = [x + y for x, y in zip(terms_P[tname], Pt)]
                # the rounding's bound: |g^r| < 1 per Node, so |delta p_a(i)| <= 2 num (|now_i| + |now_(i+a)|) per line
                for a in range(AXES):
                    s = 0
                    for n in starts:
                        s = s + abs(across(n, 2 * a)) + abs(n)
                    s = 2 * num * s
                    for cc in range(AXES):
                        aa, bb = EPS[cc]
                        if bb == a:
                            bound[cc] += int(np.sum(abs(D[aa]) * s))
                        if aa == a:
                            bound[cc] += int(np.sum(abs(D[bb]) * s))
                rows_out[str(k)] = row_terms
        node.stepped = iv.stepped
        node.set_rows(iv.out)
        L1, P1 = read_L(node.records(), D)
        iv.lays()
        node.restore(node.all_lines(), [line for row in iv.held for line in row], iv.frozen)
        L2, P2 = read_L(node.records(), D)
        iv.swap()
        L3, P3 = read_L(node.records(), D)
        births0, clicks0 = node.counts["births"], node.counts["body_clicks"]
        iv.close()
        L4, P4 = read_L(node.records(), D)
        d_step = [x - y for x, y in zip(L1, L0)]
        sum_terms = [sum(terms_L[t][cc] for t in TERMS) for cc in range(3)]
        ok = all(Fraction(d_step[cc]) == sum_terms[cc] for cc in range(3))
        if not ok:
            identity_misses += 1
        d_lays = [x - y for x, y in zip(L2, L1)]
        d_swap = [x - y for x, y in zip(L3, L2)]
        d_click = [x - y for x, y in zip(L4, L3)]
        for t in TERMS:
            totals[t] = [x + y for x, y in zip(totals[t], terms_L[t])]
            tot_abs[t] = [x + abs(y) for x, y in zip(tot_abs[t], terms_L[t])]
        for name, d in (("lays", d_lays), ("swap", d_swap), ("click", d_click), ("step", d_step)):
            tot_int[name] = [x + y for x, y in zip(tot_int[name], d)]
            tot_absint[name] = [x + abs(y) for x, y in zip(tot_absint[name], d)]
        bound_total = [x + y for x, y in zip(bound_total, bound)]
        per.append({
            "i": node.interval, "turned": int(iv.top.sum()),
            "births": node.counts["births"] - births0, "clicks": node.counts["body_clicks"] - clicks0,
            "L2_start": L0, "dL2_divisions": d_step, "identity": ok,
            "terms": {t: [fstr(q) for q in terms_L[t]] for t in TERMS},
            "terms_P": {t: [fstr(q) for q in terms_P[t]] for t in TERMS},
            "rounding_bound_2L": bound,
            "dL2_lays": d_lays, "dL2_swap": d_swap, "dL2_click": d_click,
            "dP_divisions": [x - y for x, y in zip(P1, P0)], "dP_click": [x - y for x, y in zip(P4, P3)],
            "L2_end": L4, "P_end": P4, "rows": rows_out,
        })
        if (step_k + 1) % 50 == 0:
            print(json.dumps({"i": node.interval, "L2": L4, "ms": (time.monotonic_ns() - t0) // 10**6}), flush=True)
    L_end, P_end = read_L(node.records(), D)
    summary = {
        "record": argv[1], "cube": c, "intervals": int(world["intervals"]),
        "2L_start": L_start, "2L_end": L_end, "P_end": P_end,
        "identity_misses": identity_misses, "line_misses": line_misses,
        "sum_over_record": {t: [fstr(q) for q in totals[t]] for t in TERMS},
        "sum_abs_over_record": {t: [fstr(q) for q in tot_abs[t]] for t in TERMS},
        "sum_int": tot_int, "sum_abs_int": tot_absint,
        "rounding_bound_2L_total": bound_total,
        "rounding_bound_ratio_percent": [int(100 * tot_abs["rounding"][cc] / bound_total[cc]) if bound_total[cc] else None for cc in range(3)],
        "counts": {k: int(v) for k, v in node.counts.items()},
        "ms": (time.monotonic_ns() - t0) // 10**6,
    }
    json.dump({"summary": summary, "per_interval": per}, open(argv[2], "w"))
    print(json.dumps(summary))


if __name__ == "__main__":
    main(sys.argv)
