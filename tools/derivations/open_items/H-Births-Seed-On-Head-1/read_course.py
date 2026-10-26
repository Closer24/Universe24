"""rg1: the course of a cs6_run record read per interval: the births per interval with their Nodes, phase classes (the lay's p1 digit at the Node), taken rows and taken lines; X mean / min / max / distinct, e_max, turned, the light's share, the gapped rows' whole Nodes for the first intervals and about every top and bottom; the tops with 64 turning, the bottoms, the exact returns to Gamma; the credits per interval with the laid-back count. Integers only.
Usage: python read_course.py <record.json> [first N intervals shown, default 16]"""
import json
import sys

sys.set_int_max_str_digits(0)


def main(path, first):
    r = json.load(open(path))
    cube = int(r["cube"])
    n_nodes = cube**3
    gamma = int(r["gamma"])
    log = r["log"]
    diag = {d["i"]: d for d in r["diag"]}
    n = int(r["intervals"])
    lay = next((e for e in log if e["event"] == "lay_pattern"), None)
    phases = lay.get("phases") if lay else None

    def cls(node):
        return phases[(node[0] * cube + node[1]) * cube + node[2]] if phases else None

    print("record:", path.split("/")[-1], "| intervals", n, "| run back", r["run_back"], "| integers", r.get("integers"), "| counts", r["counts"])
    births = [e for e in log if e["event"] == "birth"]
    by_i = {}
    for e in births:
        by_i.setdefault(e["i"], []).append(e)
    print("births:", len(births), "at intervals", sorted(by_i))
    for i in sorted(by_i):
        es = by_i[i]
        nodes = sorted({tuple(e["node"]) for e in es})
        classes = sorted({cls(e["node"]) for e in es}) if phases else None
        rows = sorted({(e.get("taken_row"), e["line_pair"]) for e in es})
        lines = sorted({e.get("taken_line", 0) for e in es})
        wc = sorted({tuple(e["W_children"]) for e in es})[:3]
        print(f"  i {i}: {len(es)} births at {len(nodes)} Nodes; classes {classes}; (taken_row, child row) {rows}; taken lines {lines}; W_children {wc}; taken >= booked {sum(1 for e in es if int(e['taken']) >= int(e['booked']))} of {len(es)}")
    credits = [e for e in log if e["event"] == "credit"]
    ci = {}
    for e in credits:
        ci.setdefault(e["i"], []).append(e)
    print("credits:", len(credits), "laid back", sum(1 for e in credits if "laid_back" in e), "| per interval (i: count, laid back, Nodes):", [(i, len(v), sum(1 for e in v if "laid_back" in e), len({tuple(e["node"]) for e in v})) for i, v in sorted(ci.items())][:24])
    keys = ("X_mean", "X_min", "X_max", "X_distinct", "e_max", "turned", "births", "light_share_min_max_hundredths", "gapped_whole_nodes")
    print("the first intervals (i: " + ", ".join(keys) + "):")
    for i in range(0, min(first, n) + 1):
        d = diag[i]
        print("  ", i, [d.get(k) for k in keys])
    tops = [i for i in range(2, n) if diag[i]["X_mean"] >= diag[i - 1]["X_mean"] and diag[i]["X_mean"] > diag[i + 1]["X_mean"]]
    whole = [i for i in range(1, n + 1) if diag[i]["turned"] == n_nodes]
    turned_any = [(i, diag[i]["turned"]) for i in range(1, n + 1) if diag[i]["turned"] > 0]
    print("tops of the mean X (i, X, turned at i + 1):", [(i, diag[i]["X_mean"], diag[i + 1]["turned"]) for i in tops][:12])
    print("intervals with 64 turning:", whole, "| turns in parts (first 16):", [t for t in turned_any if t[1] != n_nodes][:16], "| count of turn intervals", len(turned_any))
    bottoms = [i for i in range(2, n) if diag[i]["X_mean"] <= diag[i - 1]["X_mean"] and diag[i]["X_mean"] < diag[i + 1]["X_mean"]]
    print("bottoms of the mean X (i, mean, min, max):", [(i, diag[i]["X_mean"], diag[i]["X_min"], diag[i]["X_max"]) for i in bottoms][:12])
    exact = [i for i in range(1, n + 1) if diag[i]["X_min"] == diag[i]["X_max"] == gamma]
    print("exact returns to Gamma at every Node:", exact)
    uniform = sum(1 for i in range(1, n + 1) if diag[i]["X_distinct"] == 1)
    first_part = next((i for i in range(1, n + 1) if diag[i]["X_distinct"] > 1), None)
    print("uniform intervals (X one value):", uniform, "of", n, "| the first parted interval:", first_part, "| e_max over the run:", max(diag[i]["e_max"] for i in range(1, n + 1)))
    for t in tops[:3]:
        if diag[t + 1]["turned"] == n_nodes:
            k_first = next((k for k in range(1, min(t, n - t) + 1) if diag[t + k]["X_mean"] != diag[t - k]["X_mean"] or diag[t + k]["X_min"] != diag[t - k]["X_min"]), None)
            print(f"retrace about the top {t}: X(top + k) == X(top - k) for every k < {k_first}")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 16)
