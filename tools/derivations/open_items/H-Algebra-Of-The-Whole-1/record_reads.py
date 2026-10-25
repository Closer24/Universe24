"""ag1, items (4), (6) and (7) read from a record alone (the writer's out.json; no act): the retrace theorem (CS6-S1: after a top
at which every Node turned, X(top + k) == X(top - k) at every Node for every k up to the mirror of the last click), the exact
returns (every Node's X == Gamma: gate 1's predicate), the decoder's counts against the log's, the takes against the units,
the state's bits and count. Usage: record_reads.py <out.json> [<out2.json>]: with a second record the two courses of X are
compared interval by interval (the cube's size entering nowhere on the uniform board)."""

from __future__ import annotations

import json
import sys

sys.set_int_max_str_digits(0)


def course(rec: dict) -> list[tuple[int, list[int], int]]:
    return [(int(line["i"]), [int(x) for x in line["X"]], len(line["turned"])) for line in rec["nodes"]]


def main(argv: list[str]) -> None:
    rec = json.load(open(argv[1], encoding="utf-8"))
    gamma, n = int(rec["gamma"]), int(rec["intervals"])
    lines = course(rec)
    count = len(lines[0][1])
    tops = [i for i, _x, t in lines if t == count]
    returns = [i for i, xs, _t in lines if all(x == gamma for x in xs)]
    xs_at = {i: xs for i, xs, _t in lines}
    log = rec["log"]
    clicks = sorted({int(e["i"]) for e in log if e["event"] in ("birth", "credit")})
    # the mirror: a Node turned at the interval T ends T at its pre-state exchanged, X(T) = X(T - 2), so the mirror stands at
    # T - 1: X(T - 1 + k) == X(T - 1 - k); X(0) = X(-1) = Gamma at the seed (now = before = Gamma)
    xs_at[0] = xs_at[-1] = [gamma] * count
    retrace = []
    for top in tops:
        m = top - 1
        k = 1
        while m - k >= -1 and m + k <= n and xs_at[m + k] == xs_at[m - k]:
            k += 1
        last_click_before = max((c for c in clicks if c <= top), default=0)
        retrace.append({"top": top, "mirror": m, "X(mirror + k) == X(mirror - k) for k below": k, "mirror - k reaches": m - k + 1, "last click at or before the top": last_click_before, "clicks between the mirror of the first difference and the top": sum(1 for c in clicks if m - k + 1 <= c <= top)})
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    laid_back = [e for e in credits if "laid_back" in e]
    counts = {k: int(v) for k, v in rec["counts"].items()}
    found = {
        "record": argv[1], "intervals": n, "cube": rec["cube"], "Gamma": gamma,
        "tops with every Node turned (first eight)": tops[:8],
        "exact returns to Gamma at every Node": returns[:12],
        "retrace at the tops (first six)": retrace[:6],
        "decoder's counts against the log's: births, credits, laid back": [[len(births), counts["births"]], [len(credits), counts["body_clicks"]], [len(laid_back), counts["laid_back"]]],
        "the log's taken summed at the births against the counts": [sum(e["taken"] for e in births), counts["taken"]],
        "the log's booked summed at the births against the counts": [sum(e["booked"] for e in births), counts["booked"]],
        "credits' takes: taken >= levels moved > 0, of": [sum(1 for e in credits if e["taken"] >= 0 and e["levels"] > 0), len(credits)],
        "births' W_children sums": sorted({sum(e["W_children"]) for e in births}),
        "run back": rec["run_back"],
        "state integers and bits at the last row": [rec["rows"][-1]["integers"], rec["rows"][-1]["max bits"], rec["rows"][-1]["max transient bits"]],
        "first row's X course (interval, mean)": [(r["i"], r["volume mean"]) for r in rec["rows"]][:14],
    }
    if len(argv) > 2:
        other = json.load(open(argv[2], encoding="utf-8"))
        o = course(other)
        same = sum(1 for (i, xs, _t), (j, ys, _u) in zip(lines, o, strict=False) if i == j and sorted(set(xs)) == sorted(set(ys)))
        found["X course equal to the second record's (distinct values per interval), intervals of"] = [same, min(len(lines), len(o))]
        found["second record"] = argv[2]
    print(json.dumps(found))


if __name__ == "__main__":
    main(sys.argv)
