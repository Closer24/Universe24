"""cs5 (cs3's reader rebuilt from cs4's text, integers only): the course of a record written by cs5_run.py (the tops with the turns, the bottoms, the exact returns to Gamma at every Node, the first split, e at marks), the passing graph at marks, the landing census and the gates PER BANG (the cycles cut at the bottoms of the mean): births, credits, refusals by cause, the children's senses summed, the planes born, taken against booked, the least e and the e at the end.
Usage: python read_cs5.py <out.json> [marks i1 i2 ...]"""

from __future__ import annotations

import json
import sys
from typing import Any


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    with open(argv[1], encoding="utf-8") as f:
        record = json.load(f)
    marks = [int(x) for x in argv[argv.index("marks") + 1 :]] if "marks" in argv else [1, 10, 50, 100, 150, 200, 300, 400]
    gamma = int(record["gamma"])
    nodes_count = int(record["cube"]) ** 3
    diag = [d for d in record["diag"] if d["i"] >= 1]
    means = [d["X_mean"] for d in diag]
    n = len(diag)
    log = record.get("log", [])
    print("record:", argv[1], "intervals:", n, "records:", len(record["planes"]), "integers:", record.get("integers"), "counts:", record["counts"], "run back:", record["run_back"])
    lays = [e for e in log if e["event"] == "lay_pattern"]
    print("lay:", [{k: v for k, v in e.items() if k != "phases"} for e in lays])
    tops = [(diag[k]["i"], means[k], diag[k]["turned"], diag[k + 1]["turned"]) for k in range(1, n - 1) if means[k] >= means[k - 1] and means[k] > means[k + 1]]
    print("tops of the mean (i, mean, turned at i, turned at i + 1), first 10:", tops[:10])
    bottoms = [(diag[k]["i"], means[k], diag[k]["X_min"], diag[k]["X_max"]) for k in range(1, n - 1) if means[k] <= means[k - 1] and means[k] < means[k + 1]]
    print("bottoms of the mean (i, mean, min, max), first 10:", bottoms[:10])
    exact = [d["i"] for d in diag if d["X_min"] == gamma and d["X_max"] == gamma]
    print("exact returns (every Node at Gamma):", exact[:16], "count", len(exact))
    split = next((d["i"] for d in diag if d["X_min"] != d["X_max"]), None)
    print("first interval not uniform (min != max):", split)
    print("e_max, distinct X at marks:", [(m, diag[m - 1]["e_max"], diag[m - 1]["X_distinct"]) for m in marks if m <= n])
    print("X min/mean/max at marks:", [(m, diag[m - 1]["X_min"], diag[m - 1]["X_mean"], diag[m - 1]["X_max"]) for m in marks if m <= n])
    whole = [(d["i"], d["turned"]) for d in diag if d["turned"] == nodes_count]
    partial = [(d["i"], d["turned"]) for d in diag if 0 < d["turned"] < nodes_count]
    print("whole-board turns (i, count):", whole[:12], "count", len(whole))
    print("partial turns (i, count), first 10:", partial[:10], "count", len(partial), "Nodes summed", sum(t for _i, t in partial))
    print("F / twist / both per axis; degree hist; in-degree hist at marks:")
    for m in marks:
        if m <= n:
            d = diag[m - 1]
            print("  ", m, d["F_links_nonzero_per_axis"], d["twist_links_nonzero_per_axis"], d["F_and_twist_nonzero_per_axis"], d["pass_degree_hist"], d["pass_indegree_hist"], "share", d["light_share_min_max_hundredths"], "whole", d["light_share_whole_nodes"], "gapped whole", d["gapped_whole_nodes"])
    print("bits max over the run:", max(d["bits"] for d in diag), "frozen max:", max(d["frozen"] for d in diag), "energy min/max at 1 and at the end:", diag[0]["light_energy_min_max"], diag[-1]["light_energy_min_max"])
    cuts = [0] + [b[0] for b in bottoms] + [n]
    print("per bang (the cycle from bottom to bottom): [from, to], top (i, mean), whole / partial turns, births, credits, refused by cause, landing census summed, e_min, e_end, X_end")
    bang = 0
    for k in range(len(cuts) - 1):
        lo, hi = cuts[k], cuts[k + 1]
        if hi - lo < 3:
            continue
        bang += 1
        inside = [d for d in diag if lo < d["i"] <= hi]
        top = max(inside, key=lambda d: d["X_mean"])
        births = [e for e in log if e["event"] == "birth" and lo < e["i"] <= hi]
        credits = [e for e in log if e["event"] == "credit" and lo < e["i"] <= hi]
        refused: dict[str, int] = {}
        for e in log:
            if e["event"] == "refused" and lo < e["i"] <= hi:
                cause = e["cause"] + ("_crowd" if "children_at_one_node" in e else "_standing" if "standing" in e else "")
                refused[cause] = refused.get(cause, 0) + 1
        landing = [e for e in log if e["event"] == "landing" and lo < e["i"] <= hi]
        census = {
            "closes": len(landing),
            "links": sum(e["links"] for e in landing),
            "into_nodes": sum(e["into_nodes"] for e in landing),
            "indegree": {},
            "children_per_node": {},
            "crowded": sum(e["nodes_crowded"] for e in landing),
            "clean": sum(e["nodes_clean"] for e in landing),
            "light_child": sum(e["nodes_with_light_child"] for e in landing),
            "distinct_draws_max": max((e["distinct_draws"] for e in landing), default=0),
        }
        for e in landing:
            for kk, v in e["indegree_hist"].items():
                census["indegree"][kk] = census["indegree"].get(kk, 0) + v
            for kk, v in e["children_per_node_hist"].items():
                census["children_per_node"][kk] = census["children_per_node"].get(kk, 0) + v
        senses = sum(1 if w > 0 else -1 if w < 0 else 0 for e in births for w in e["W_children"])
        planes: dict[str, int] = {}
        for e in births:
            planes[str(e["line_pair"])] = planes.get(str(e["line_pair"]), 0) + 1
        whole_c = sum(1 for d in inside if d["turned"] == nodes_count)
        partial_c = sum(1 for d in inside if 0 < d["turned"] < nodes_count)
        births_i = sorted({e["i"] for e in births})
        credit_lines: dict[str, int] = {}
        for e in credits:
            credit_lines[str(e["line"])] = credit_lines.get(str(e["line"]), 0) + 1
        print(
            f"  bang {bang}: [{lo}, {hi}] top ({top['i']}, {top['X_mean']}) whole {whole_c} partial {partial_c} births {len(births)} at {births_i[:8]} planes {json.dumps(planes, sort_keys=True)} senses {senses} taken {sum(e['taken'] for e in births)} booked {sum(e['booked'] for e in births)} credits {len(credits)} lines {json.dumps(credit_lines, sort_keys=True)} refused {json.dumps(refused, sort_keys=True)} census {json.dumps(census, sort_keys=True)} e_min {min(d['e_max'] for d in inside)} e_end {inside[-1]['e_max']} X_end ({inside[-1]['X_min']}, {inside[-1]['X_max']})"
        )
    births = [e for e in log if e["event"] == "birth"]
    if births:
        print("births:", len(births), "first 4 (i, node, plane, W_children, amplitude, children_at_node):", [(e["i"], e["node"], e["line_pair"], e["W_children"], e["amplitude"], e["children_at_node"]) for e in births[:4]])
        by_i: dict[int, int] = {}
        for e in births:
            by_i[e["i"]] = by_i.get(e["i"], 0) + 1
        print("births per interval:", sorted(by_i.items())[:30])
        nodes_born = {tuple(e["minus"]) for e in births} | {tuple(e["plus"]) for e in births}
        print("Nodes with a child over the run:", len(nodes_born), "of", nodes_count)
    e_first = next((d["i"] for d in diag if d["e_max"] > 0), None)
    print("first interval with e above 0:", e_first, "e at the following marks:", [(d["i"], d["e_max"]) for d in diag if e_first is not None and d["i"] in (e_first, e_first + 1, e_first + 5, e_first + 10, e_first + 20, e_first + 50)])


if __name__ == "__main__":
    main(sys.argv)
