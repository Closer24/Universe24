"""lc2's course reader: the engine (David's src or the flagged copy, chosen by PYTHONPATH; the form by LC2_REACH) stepped interval by interval with the board's sums read at every interval's start from the Node's own rule (the carrier's time line): the plain Links' sum SUM_i SUM_j R_ij (X_j - X_i), the weighted sum SUM_i (1 / p_i^2) SUM_j R_ij (X_j - X_i) as an exact rational (two integers), the mass sum SUM_i D_i X_i, the mean volume, the spread e in thousandths (the range over the mean, and the root-mean-square over the mean), the turned Nodes, the births and the body credits, the Wronskian total (the charge), then the run back. Integers only (Fraction for the exact rational, printed as two integers).
Usage: python lc2_course.py <world.json> <out.json> <back N>"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction

import numpy as np

from event_universe import readings
from event_universe.core.ports import PORTS, across
from event_universe.core.rule3 import largest_below
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE
from event_universe.links import wronskian
from event_universe.core.rule3 import carried_division, held_numerator
from event_universe.rows import TRACE


def ints(a):
    return [int(x) for x in np.asarray(a, dtype=object).reshape(-1)]


def spread(xs: list[int]) -> tuple[int, int, int, int, int]:
    n = len(xs)
    mean = sum(xs) // n
    lo, hi = min(xs), max(xs)
    e_range = (hi - lo) * 1000 // mean
    ss = sum((x - mean) * (x - mean) for x in xs)
    e_rms = largest_below(ss // n) * 1000 // mean
    return mean, lo, hi, e_range, e_rms


def board_sums(node: Node) -> dict:
    carrier = node.row(CARRIER)
    x = carrier.lines[0].now
    c = node.content()
    frozen = readings.frozen_of(node, c)
    factors = node.link_factors(None, frozen)
    rule = node.rule_of(carrier, c, factors)
    p0, pi = readings.paces_of(node, c)
    links = np.zeros(node.shape, dtype=object)
    for port in range(PORTS):
        links = links + rule.reaches[port] * (across(x, port) - x)
    li = ints(links)
    pis = ints(pi)
    weighted = Fraction(0)
    frozen_n = 0
    for l, p in zip(li, pis):
        if p == 0:
            frozen_n += 1
            continue
        weighted += Fraction(l, p * p)
    mass = ints(rule.mass * x)
    arg = max(range(len(li)), key=lambda k: abs(li[k]))
    return {
        "links_plain": sum(li),
        "links_weighted_num": weighted.numerator,
        "links_weighted_den": weighted.denominator,
        "links_abs_max": li[arg],
        "links_abs_max_node": arg,
        "mass_sum": sum(mass),
        "frozen": frozen_n,
        "wall": int(rule.wall),
        "reach_min": min(ints(r) for r in rule.reaches) if np.ndim(rule.reaches[0]) else int(min(rule.reaches)),
        "reach_max": max(ints(r) for r in rule.reaches) if np.ndim(rule.reaches[0]) else int(max(rule.reaches)),
    }


def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    out_path = argv[2]
    back = int(argv[3]) if len(argv) > 3 else 10
    node = Node(universe, world)
    intervals = int(world["intervals"])
    carrier = node.row(CARRIER)
    rows = []
    hashes = []
    max_bits = 0
    first_turn = None
    prev_counts = dict(node.counts)
    for t in range(intervals):
        if back and t >= intervals - back:
            hashes.append(node.state_hash())
        before = ints(carrier.lines[0].before)
        now = ints(carrier.lines[0].now)
        sums = board_sums(node)
        node.step()
        nxt = ints(carrier.lines[0].now)
        deep = {}
        if hasattr(node, "lc2_forms"):
            # the deepest Node after the step: its X, its gap-0 level a, its lag to its six neighbours, its riding velocity, its forms, its write
            k = max(range(len(nxt)), key=lambda q: nxt[q])
            g0 = node.row(PLANE, gap=0).lines[0]
            a_now, a_before = ints(g0.now), ints(g0.before)
            nb = [int(x) for x in [np.asarray(across(g0.now, port), dtype=object).reshape(-1)[k] for port in range(PORTS)]]
            forms = ints(node.lc2_forms)
            fsum = sum(forms)
            deep = {"deep_node": k, "deep_X": nxt[k], "deep_a": a_now[k], "deep_lag": a_now[k] - sum(nb) // PORTS, "deep_v": a_now[k] - a_before[k],
                    "deep_forms": forms[k], "forms_sum": fsum, "forms_min": min(forms), "forms_max": max(forms)}
        turned = node.turned.reshape(-1).tolist()
        n_turn = sum(1 for v in turned if v)
        xpp = sum(a - 2 * b + c for a, b, c, tt in zip(nxt, now, before, turned) if not tt)
        mean, lo, hi, e_range, e_rms = spread(nxt)
        n_count, bits = node.census()
        max_bits = max(max_bits, bits)
        wt = 0
        for r in node.records():
            wt += sum(ints(wronskian(*r.lines)))
        row = {
            "i": node.interval,
            "mean": mean, "min": lo, "max": hi, "e_range": e_range, "e_rms": e_rms,
            "xpp_sum_unturned": xpp,
            "turned": n_turn,
            "turned_nodes": [k for k, v in enumerate(turned) if v][:8],
            "births": node.counts["births"] - prev_counts["births"],
            "credits": node.counts["body_clicks"] - prev_counts["body_clicks"],
            "refused_lay": node.counts["refused_lay"] - prev_counts["refused_lay"],
            "W_total": wt,
            "bits": bits,
            "integers": n_count,
        }
        row.update(sums)
        row.update(deep)
        rows.append(row)
        if n_turn and first_turn is None:
            first_turn = node.interval
        prev_counts = dict(node.counts)
    exact = 0
    for k in range(len(hashes)):
        node.step_back()
        exact += node.state_hash() == hashes[len(hashes) - 1 - k]
    summary = {
        "world": argv[1], "form": os.environ.get("LC2_REACH", "default"), "intervals": intervals,
        "run_back": {"intervals": len(hashes), "exact": exact},
        "max_bits": max_bits, "integers": rows[-1]["integers"],
        "counts": {k: int(v) for k, v in node.counts.items()},
        "first_turn": first_turn,
        "turn_intervals": node.turns[:40],
        "mean_course": [(r["i"], r["mean"]) for r in rows if r["i"] % 10 == 0 or r["i"] == 1],
        "tops": [rows[k]["i"] for k in range(1, len(rows) - 1) if rows[k]["mean"] > rows[k - 1]["mean"] and rows[k]["mean"] >= rows[k + 1]["mean"]],
        "returns_to_seed": [r["i"] for r in rows if r["min"] == r["max"] == node.gamma],
        "mean_min_after_first_top": None,
        "links_plain_abs_max": max(abs(r["links_plain"]) for r in rows),
        "links_plain_sign": [sum(1 for r in rows if r["links_plain"] > 0), sum(1 for r in rows if r["links_plain"] < 0), sum(1 for r in rows if r["links_plain"] == 0)],
        "links_weighted_abs_max_num_den": max(((abs(r["links_weighted_num"]), r["links_weighted_den"]) for r in rows), key=lambda q: Fraction(q[0], q[1])),
    }
    tops = summary["tops"]
    if tops:
        after = [r["mean"] for r in rows if r["i"] > tops[0]]
        summary["mean_min_after_first_top"] = min(after) if after else None
    if first_turn is not None:
        k = first_turn - 1
        summary["first_turn_readings"] = {
            "interval": first_turn,
            "nodes": rows[k]["turned_nodes"],
            "e_rms_before": rows[k - 1]["e_rms"] if k >= 1 else None,
            "e_rms_at": rows[k]["e_rms"],
            "e_rms_plus10": rows[min(k + 10, len(rows) - 1)]["e_rms"],
            "e_range_before": rows[k - 1]["e_range"] if k >= 1 else None,
            "e_range_plus10": rows[min(k + 10, len(rows) - 1)]["e_range"],
            "links_plain_before_at_plus1": [rows[max(k - 1, 0)]["links_plain"], rows[k]["links_plain"], rows[min(k + 1, len(rows) - 1)]["links_plain"]],
        }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "rows": rows}, f)
    print(json.dumps(summary))


if __name__ == "__main__":
    main(sys.argv)
