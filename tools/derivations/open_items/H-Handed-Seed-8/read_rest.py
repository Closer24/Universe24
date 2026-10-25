"""cs8: the merger at rest read on a record: per interval the rest meetings (the candidates: F 0 and the two ends' charges opposite) by row with the charge sums, the mergers landed (a birth whose taken row has a gap and whose children are the light), their charge summed (the two ends' charges at the rest meeting of the same Link), the refusals of the heavy rows by cause, the light children laid per Node (the crowd); the exact returns to Gamma, the tops; per bang the births, the credits, the mergers.
Usage: python read_rest.py <record.json>"""
import json
import sys
from collections import Counter

sys.set_int_max_str_digits(0)


def main(path: str) -> None:
    r = json.load(open(path))
    cube = int(r["cube"])
    n_nodes = cube**3
    gamma = int(r["gamma"])
    log = r["log"]
    diag = [d for d in r["diag"] if d["i"] >= 1]
    lay = next((e for e in log if e["event"] == "lay_pattern"), None)
    light = lay["line_pair"] if lay else [str(p) for p in r["planes"]].index(str(r["den"]))
    print("record:", path.split("/")[-1], "intervals:", len(diag), "integers:", r.get("integers"), "run back:", r["run_back"], "bits max:", max(d["bits"] for d in diag))
    print("counts:", r["counts"])
    rest = [e for e in log if e["event"] == "rest_meet"]
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    mergers = [e for e in births if e.get("taken_row", light) != light and e["line_pair"] == light]
    plain = [e for e in births if e.get("taken_row", light) == light]
    print("rest meetings:", len(rest), "at intervals:", sorted({e["i"] for e in rest})[:30])
    print("births from light:", len(plain), "at:", sorted({e["i"] for e in plain})[:20])
    print("mergers (a gapped row taken, the light born):", len(mergers), "at:", sorted({e["i"] for e in mergers})[:30])
    # the charge at every merger: the rest meeting of the same interval, row and Link
    by_key = {}
    for e in rest:
        a, b = tuple(e["node"]), tuple(e["link"])
        by_key[(e["i"], e["row"], frozenset((a, b)))] = e["charges"]
    sums = Counter()
    for e in mergers:
        k = (e["i"], e["taken_row"], frozenset((tuple(e["minus"]), tuple(e["plus"]))))
        w = by_key.get(k)
        sums[None if w is None else w[0] + w[1]] += 1
    print("the heavy charge summed over the two ends at every merger (sum: count):", dict(sums))
    print("the light children's senses at the mergers (W_children):", Counter(tuple(e["W_children"]) for e in mergers).most_common(4))
    print("merger takes: taken >= booked at", sum(1 for e in mergers if e["taken"] >= e["booked"]), "of", len(mergers), "; levels (distinct, first 6):", sorted({e["levels"] for e in mergers})[:6], "; the ends' lines taken (taken_line per end):", Counter(tuple(t.get("taken_line") for t in e.get("takes", [])) for e in mergers).most_common(4))
    for i in sorted({e["i"] for e in rest})[:24]:
        rs = [e for e in rest if e["i"] == i]
        ms = [e for e in mergers if e["i"] == i]
        rows = Counter(e["row"] for e in rs)
        csum = Counter(e["charges"][0] + e["charges"][1] for e in rs)
        ends = Counter()
        for e in rs:
            ends[(e["row"], tuple(e["node"]))] += 1
            ends[(e["row"], tuple(e["link"]))] += 1
        per_node = Counter(ends.values())
        light_landing = Counter()
        for e in ms:
            light_landing[tuple(e["minus"])] += 1
            light_landing[tuple(e["plus"])] += 1
        ref = Counter((e["row"], e["cause"] + ("_crowd" if "children_at_one_node" in e else "_standing" if "standing" in e else "")) for e in log if e["event"] == "refused" and e["i"] == i and e.get("row", light) != light)
        print(f"  i {i}: rest meetings {len(rs)} by row {dict(rows)}; charge sums {dict(csum)}; candidate Links per (row, Node) histogram {dict(per_node)}; mergers landed {len(ms)} by taken row {dict(Counter(e['taken_row'] for e in ms))}; Nodes receiving light children {len(light_landing)} (max per Node {max(light_landing.values()) if light_landing else 0}); heavy refusals {dict(ref)}")
    exact = [d["i"] for d in diag if d["X_min"] == gamma and d["X_max"] == gamma]
    print("exact returns to Gamma at every Node:", exact[:20], "count", len(exact))
    means = [d["X_mean"] for d in diag]
    tops = [(diag[k]["i"], means[k], diag[k + 1]["turned"]) for k in range(1, len(diag) - 1) if means[k] >= means[k - 1] and means[k] > means[k + 1]]
    print("tops (i, mean, turned at i + 1):", tops[:8])
    split = next((d["i"] for d in diag if d["X_min"] != d["X_max"]), None)
    print("first interval not uniform:", split, "; e at the end:", diag[-1]["e_max"], "; X at the end:", diag[-1]["X_min"], diag[-1]["X_mean"], diag[-1]["X_max"], "; whole-board turns:", sum(1 for d in diag if d["turned"] == n_nodes), "partial:", sum(1 for d in diag if 0 < d["turned"] < n_nodes))
    gw = [(d["i"], d["gapped_whole_nodes"]) for d in diag if d["gapped_whole_nodes"] != [0, 0]]
    print("intervals with gapped children whole (first 30):", gw[:30], "count", len(gw))
    cuts = sorted(set([0] + exact + [len(diag)]))
    cuts = [c for k, c in enumerate(cuts) if k == 0 or c - cuts[k - 1] > 2]
    print("per bang (cut at the exact returns): [from, to] births credits (laid back) mergers")
    for lo, hi in zip(cuts, cuts[1:]):
        b = [e for e in plain if lo < e["i"] <= hi]
        c = [e for e in credits if lo < e["i"] <= hi]
        m = [e for e in mergers if lo < e["i"] <= hi]
        inside = [d for d in diag if lo < d["i"] <= hi]
        print(f"  [{lo}, {hi}] births {len(b)} at {sorted({e['i'] for e in b})[:4]} (Nodes with a child {len({tuple(e['minus']) for e in b} | {tuple(e['plus']) for e in b})}) credits {len(c)} laid back {sum(1 for e in c if 'laid_back' in e)} at {sorted({e['i'] for e in c})[:5]} mergers {len(m)} at {sorted({e['i'] for e in m})[:4]} whole turns {sum(1 for d in inside if d['turned'] == n_nodes)} X_end {inside[-1]['X_min']}..{inside[-1]['X_max']}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
        print()
