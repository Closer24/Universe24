"""cs1's reader of a record written by cs_run.py (or by run.py: the diag then absent, the Node lines read): the X course (the tops of the mean with the count turning, the bottoms and the returns to Gamma at every Node), the first interval where the board is not uniform, the spread's course at marks, the turns that were not the whole board's, the light's current and twist per axis at marks, the births and the refusals by cause, and the gates PER BANG: the cycles cut at the bottoms of the mean (a bang = one rise and fall), each with its births, body credits, refusals by cause, the mergers 0 (not built), the whole-board turns, the least spread. Integers only.

Usage: python read_cs.py <out.json> [marks i1 i2 ...]"""

from __future__ import annotations

import json
import sys
from typing import Any


def course(record: dict[str, Any]) -> list[dict[str, Any]]:
    """The per-interval course from the diag where present, else from the Node lines (X min, mean, max, turned)."""
    if "diag" in record:
        return [d for d in record["diag"] if d["i"] >= 1]
    found = []
    for line in record["nodes"]:
        xs = line["X"]
        found.append(
            {
                "i": line["i"],
                "X_min": min(xs),
                "X_mean": sum(xs) // len(xs),
                "X_max": max(xs),
                "turned": len(line["turned"]),
                "e_max": 0 if min(xs) == max(xs) else (max(xs) - min(xs)) * 1000 // min(xs),
            }
        )
    return found


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    with open(argv[1], encoding="utf-8") as f:
        record = json.load(f)
    marks = [int(x) for x in argv[argv.index("marks") + 1 :]] if "marks" in argv else [1, 10, 50, 100, 200, 300, 400]
    gamma = int(record["gamma"])
    nodes_count = int(record["cube"]) ** 3
    diag = course(record)
    means = [d["X_mean"] for d in diag]
    n = len(diag)
    print("record:", argv[1], "intervals:", n, "counts:", record["counts"], "run back:", record["run_back"])
    if "log" in record:
        lays = [e for e in record["log"] if e["event"] in ("lay_pattern", "lay", "lay_fourth")]
        print("lays:", lays)
    tops = []
    for k in range(1, n - 1):
        if means[k] >= means[k - 1] and means[k] > means[k + 1]:
            tops.append((diag[k]["i"], means[k], diag[k]["turned"], diag[k + 1]["turned"]))
    print("tops of the mean (i, mean, turned at i, turned at i + 1), first 12:", tops[:12])
    bottoms = []
    for k in range(1, n - 1):
        if means[k] <= means[k - 1] and means[k] < means[k + 1]:
            bottoms.append((diag[k]["i"], means[k], diag[k]["X_min"], diag[k]["X_max"]))
    print("bottoms of the mean (i, mean, min, max), first 12:", bottoms[:12])
    exact = [d["i"] for d in diag if d["X_min"] == gamma and d["X_max"] == gamma]
    print("exact returns (every Node at Gamma):", exact[:16], "count", len(exact))
    split = next((d["i"] for d in diag if d["X_min"] != d["X_max"]), None)
    print("first interval not uniform (min != max):", split)
    print("e_max at marks:", [(m, diag[m - 1]["e_max"]) for m in marks if m <= n])
    print("X min/mean/max at marks:", [(m, diag[m - 1]["X_min"], diag[m - 1]["X_mean"], diag[m - 1]["X_max"]) for m in marks if m <= n])
    whole = [(d["i"], d["turned"]) for d in diag if d["turned"] == nodes_count]
    partial = [(d["i"], d["turned"]) for d in diag if 0 < d["turned"] < nodes_count]
    print("whole-board turns (i, count):", whole[:12], "count", len(whole))
    print("partial turns (i, count), first 12:", partial[:12], "count", len(partial), "Nodes summed", sum(t for _i, t in partial))
    if "diag" in record:
        print(
            "F / twist / both nonzero per axis at marks:",
            [
                (m, diag[m - 1]["F_links_nonzero_per_axis"], diag[m - 1]["twist_links_nonzero_per_axis"], diag[m - 1]["F_and_twist_nonzero_per_axis"])
                for m in marks
                if m <= n
            ],
        )
        print("light share min/max hundredths, whole Nodes at marks:", [(m, diag[m - 1]["light_share_min_max_hundredths"], diag[m - 1]["light_share_whole_nodes"]) for m in marks if m <= n])
        print("light energy min/max at marks:", [(m, diag[m - 1]["light_energy_min_max"]) for m in marks if m <= n])
        print("bits max over the run:", max(d["bits"] for d in diag), "frozen max:", max(d["frozen"] for d in diag))
    # the gates per bang: the cycles cut at the bottoms of the mean (the seed is the first bottom)
    cuts = [0] + [b[0] for b in bottoms] + [n]
    log = record.get("log", [])
    print("per bang (cycle from bottom to bottom): [from, to], top (i, mean), whole turns, partial turns, births, credits, refused by cause, least e, e at the end")
    for k in range(len(cuts) - 1):
        lo, hi = cuts[k], cuts[k + 1]
        if hi - lo < 3:
            continue
        inside = [d for d in diag if lo < d["i"] <= hi]
        top = max(inside, key=lambda d: d["X_mean"])
        births = sum(1 for e in log if e["event"] == "birth" and lo < e["i"] <= hi)
        credits = sum(1 for e in log if e["event"] == "credit" and lo < e["i"] <= hi)
        refused: dict[str, int] = {}
        for e in log:
            if e["event"] == "refused" and lo < e["i"] <= hi:
                cause = e["cause"] + ("_crowd" if "children_at_one_node" in e else "")
                refused[cause] = refused.get(cause, 0) + 1
        whole_c = sum(1 for d in inside if d["turned"] == nodes_count)
        partial_c = sum(1 for d in inside if 0 < d["turned"] < nodes_count)
        print(
            f"  bang {k + 1}: [{lo}, {hi}] top ({top['i']}, {top['X_mean']}) whole {whole_c} partial {partial_c} births {births} credits {credits} refused {json.dumps(refused, sort_keys=True)} e_min {min(d['e_max'] for d in inside)} e_end {inside[-1]['e_max']} X_end ({inside[-1]['X_min']}, {inside[-1]['X_max']})"
        )
    births = [e for e in log if e["event"] == "birth"]
    if births:
        senses = [w for e in births for w in e["W_children"]]
        print("births:", len(births), "first 6 (i, node, plane, W_children, amplitude):", [(e["i"], e["node"], e["line_pair"], e["W_children"], e["amplitude"]) for e in births[:6]])
        print("children's senses summed (the charge in the clicks):", sum(1 if w > 0 else -1 if w < 0 else 0 for w in senses))
        planes = {}
        for e in births:
            planes[e["line_pair"]] = planes.get(e["line_pair"], 0) + 1
        print("births per plane:", planes, "taken summed", sum(e["taken"] for e in births), "booked summed", sum(e["booked"] for e in births))
    credits = [e for e in log if e["event"] == "credit"]
    if credits:
        print("credits:", len(credits), "first 4 (i, node, line, sense, beat):", [(e["i"], e["node"], e["line"], e["sense"], e["beat"]) for e in credits[:4]])


if __name__ == "__main__":
    main(sys.argv)
