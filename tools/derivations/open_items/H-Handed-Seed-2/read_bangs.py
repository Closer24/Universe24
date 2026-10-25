"""cs2's per-bang reader (integers only): from a record's diag lines, the bangs numbered by the bottoms of the board's mean X (a local minimum below the mean of the run, or the exact return X_min = X_max = Gamma), and per bang window (bottom to the next bottom): the top (interval, mean, Nodes turned at the top), the births, the body credits, the refusals by cause, e_max, the light's F and twist Links at the bottom, the light's share at the bottom, the uniformity of the orbits (X_min, X_max at the bottom); the run back, the bits, the counts.

Usage: python read_bangs.py <out.json>"""

from __future__ import annotations

import json
import sys


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    with open(argv[1], encoding="utf-8") as f:
        d = json.load(f)
    diag = d["diag"]
    gamma = int(d["gamma"])
    means = [int(g["X_mean"]) for g in diag]
    n = len(means)
    # bottoms: local minima of the mean with the mean at or below 3 Gamma, after a top above the seed
    bottoms = [0]
    for i in range(1, n - 1):
        if means[i] <= means[i - 1] and means[i] < means[i + 1] and means[i] <= 3 * gamma:
            # the bottom follows a rise above 3 Gamma since the last bottom
            if max(means[bottoms[-1]:i]) > 3 * gamma:
                bottoms.append(i)
    bottoms.append(n - 1)
    counters = ("births", "body_clicks", "refused_orientation", "refused_twist", "refused_lay", "refused_stop", "refused_origin")
    print("bang | bottom i, X mean/min/max, share light min/max, F links !=0, twist links !=0 | top i, mean, turned | births | credits | refused o/t/l/s/origin | e_max in window | turns in window (intervals x Nodes)")
    for k in range(len(bottoms) - 1):
        a, b = bottoms[k], bottoms[k + 1]
        g = diag[a]
        window = diag[a:b]
        top = max(range(a, b), key=lambda i: means[i])
        turned_top = max(int(diag[i]["turned"]) for i in range(a, b)) if b > a else 0
        deltas = [int(diag[b]["births" if c == "births" else c]) - int(diag[a][c]) for c in counters]
        e = max(int(x["e_max"]) for x in window)
        turns = [(int(x["i"]), int(x["turned"])) for x in window if int(x["turned"]) > 0]
        fz = 192 if "F_links_zero" not in g else 3 * len(d["nodes"][0]["X"]) - int(g["F_links_zero"])
        print(
            f"{k} | {int(g['i'])}, {means[a]}/{int(g['X_min'])}/{int(g['X_max'])}, {g['light_share_min_max_hundredths']}, {fz}, {g['twist_links_nonzero']} | {int(diag[top]['i'])}, {means[top]}, {turned_top} | {deltas[0]} | {deltas[1]} | {deltas[2]}/{deltas[3]}/{deltas[4]}/{deltas[5]}/{deltas[6]} | {e} | {len(turns)} turns, {turns[:6]}"
        )
    last = diag[-1]
    print("end", int(last["i"]), "X mean/min/max", means[-1], int(last["X_min"]), int(last["X_max"]), "e_max", last["e_max"], "bits", last["bits"], "max bits over run", max(int(x["bits"]) for x in diag))
    print("counts", d["counts"], "run back", d["run_back"])
    # the group's invariance: the distinct X values per interval at the bottoms and tops
    for i in bottoms[1:-1]:
        xs = d["nodes"][i - 1]["X"] if i - 1 < len(d["nodes"]) else []
        print("bottom", i, "distinct X values", len(set(xs)), sorted(set(xs))[:8])
    births = [e for e in d["log"] if e["event"] == "birth"]
    senses = {}
    for e in births:
        key = (e["line_pair"], tuple(1 if w > 0 else -1 if w < 0 else 0 for w in e["W_children"]))
        senses[key] = senses.get(key, 0) + 1
    print("births by (plane, children senses)", {str(k): v for k, v in senses.items()})
    by_i = {}
    for e in births:
        by_i[e["i"]] = by_i.get(e["i"], 0) + 1
    print("births per interval", sorted(by_i.items())[:40])


if __name__ == "__main__":
    main(sys.argv)
