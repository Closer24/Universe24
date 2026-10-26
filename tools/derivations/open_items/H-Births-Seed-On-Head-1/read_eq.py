"""cs7: EQ-S1 read on a record: the credits per interval with the count laid back, the six currents at the credited Nodes (how many of six nonzero, their sum), the births per interval with their rows and classes, the exact returns to Gamma, the tops with 64 turning, the bottoms; per bang (the cycles cut at the exact returns, or at the bottoms where none) the births, the credits, the laid back, the mergers.
Usage: python read_eq.py <record.json>"""
import json
import sys

sys.set_int_max_str_digits(0)


def main(path: str) -> None:
    r = json.load(open(path))
    cube = int(r["cube"])
    n_nodes = cube**3
    gamma = int(r["gamma"])
    log = r["log"]
    diag = [d for d in r["diag"] if d["i"] >= 1]
    lay = next((e for e in log if e["event"] == "lay_pattern"), None)
    phases = lay["phases"] if lay else None
    light = lay["line_pair"] if lay else None

    def cls(node):
        return phases[(node[0] * cube + node[1]) * cube + node[2]] if phases else None

    print("record:", path.split("/")[-1], "intervals:", len(diag), "records:", len(r["planes"]), "integers:", r.get("integers"), "run back:", r["run_back"])
    print("counts:", r["counts"])
    credits = [e for e in log if e["event"] == "credit"]
    by_i: dict[int, list] = {}
    for e in credits:
        by_i.setdefault(e["i"], []).append(e)
    print("credits:", len(credits), "laid back:", sum(1 for e in credits if "laid_back" in e))
    for i in sorted(by_i)[:40]:
        es = by_i[i]
        nz = [sum(1 for v in e.get("arrivals", []) if v != 0) for e in es]
        sums = sorted({sum(e.get("arrivals", [0])) for e in es})
        rows = sorted({e["line"] for e in es})
        print(f"  credits at {i}: {len(es)} on rows {rows}; laid back {sum(1 for e in es if 'laid_back' in e)}; nonzero of six per credit {sorted(set(nz))}; the six summed (distinct, first 4) {sums[:4]}; levels {sorted({e['levels'] for e in es})[:4]}; Nodes {len({tuple(e['node']) for e in es})}")
    births = [e for e in log if e["event"] == "birth"]
    bi: dict[int, list] = {}
    for e in births:
        bi.setdefault(e["i"], []).append(e)
    print("births:", len(births), "mergers (a gapped row taken, the light born):", sum(1 for e in births if e.get("taken_row", light) != light and e["line_pair"] == light))
    for i in sorted(bi)[:30]:
        es = bi[i]
        rows = {}
        classes = {}
        for e in es:
            rows[str(e["line_pair"])] = rows.get(str(e["line_pair"]), 0) + 1
            c = str(cls(e["node"]))
            classes[c] = classes.get(c, 0) + 1
        nodes = {tuple(e["minus"]) for e in es} | {tuple(e["plus"]) for e in es}
        print(f"  births at {i}: {len(es)} rows {json.dumps(rows, sort_keys=True)} classes {json.dumps(classes, sort_keys=True)} Nodes with a child {len(nodes)} of {n_nodes}; taken >= booked {sum(1 for e in es if e['taken'] >= e['booked'])}; W {sorted({tuple(e['W_children']) for e in es})[:2]}")
    landing = {e["i"]: e for e in log if e["event"] == "landing"}
    for i in sorted(bi)[:30]:
        e = landing.get(i)
        if e:
            print(f"  landing at {i}: links {e['links']} crowded {e['nodes_crowded']} light child {e['nodes_with_light_child']} draws per class {json.dumps({k: sorted(v) for k, v in sorted(e['draws_per_class'].items())})} taken rows {e.get('taken_rows')}")
    exact = [d["i"] for d in diag if d["X_min"] == gamma and d["X_max"] == gamma]
    print("exact returns to Gamma at every Node:", exact[:20], "count", len(exact))
    means = [d["X_mean"] for d in diag]
    tops = [(diag[k]["i"], means[k], diag[k + 1]["turned"]) for k in range(1, len(diag) - 1) if means[k] >= means[k - 1] and means[k] > means[k + 1]]
    print("tops (i, mean, turned at i + 1):", tops[:8])
    bottoms = [(diag[k]["i"], means[k], diag[k]["X_min"], diag[k]["X_max"]) for k in range(1, len(diag) - 1) if means[k] <= means[k - 1] and means[k] < means[k + 1]]
    print("bottoms (i, mean, min, max):", bottoms[:8])
    whole = [d["i"] for d in diag if d["turned"] == n_nodes]
    print("whole-board turns at:", whole[:8], "count", len(whole), "; partial turns count", sum(1 for d in diag if 0 < d["turned"] < n_nodes))
    split = next((d["i"] for d in diag if d["X_min"] != d["X_max"]), None)
    print("first interval not uniform:", split, "; e at the end:", diag[-1]["e_max"], "X at the end:", diag[-1]["X_min"], diag[-1]["X_mean"], diag[-1]["X_max"], "; bits max:", max(d["bits"] for d in diag))
    cuts = [0] + (exact[:1] if exact else []) + [e for e in exact[1:] if e - exact[exact.index(e) - 1] > 2] + [len(diag)] if exact else [0] + [b[0] for b in bottoms] + [len(diag)]
    cuts = sorted(set(cuts))
    print("per bang (cut at the exact returns where any, else at the bottoms): [from, to] births (rows) credits laid_back whole_turns e_end")
    for lo, hi in zip(cuts, cuts[1:]):
        if hi - lo < 3:
            continue
        b = [e for e in births if lo < e["i"] <= hi]
        c = [e for e in credits if lo < e["i"] <= hi]
        rows = {}
        for e in b:
            rows[str(e["line_pair"])] = rows.get(str(e["line_pair"]), 0) + 1
        inside = [d for d in diag if lo < d["i"] <= hi]
        print(f"  [{lo}, {hi}] births {len(b)} {json.dumps(rows, sort_keys=True)} at {sorted({e['i'] for e in b})[:5]} credits {len(c)} laid back {sum(1 for e in c if 'laid_back' in e)} at {sorted({e['i'] for e in c})[:6]} whole turns {sum(1 for d in inside if d['turned'] == n_nodes)} partial {sum(1 for d in inside if 0 < d['turned'] < n_nodes)} e_end {inside[-1]['e_max']} X_end {inside[-1]['X_min']}..{inside[-1]['X_max']}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
        print()
