"""ck1's per-bang reader: from a record as run.py writes it (nodes, turns, log, counts, gamma), the bangs (every Node turning at once at a top), the returns (every Node at X = Gamma), the bottoms (the mean's local minima), and per cycle (from one whole-board top to the next, the seed to the first top the cycle 0) the gates' counts: births, credits per record line, refusals by cause, the species credited (distinct lines), frozen Nodes (holes), the light's current (the largest |F| over the Links from the Node lines), the births' handedness (the + child at the +axis end against the -axis end), the colours' credits (even / odd Nodes) where the board is even.
Usage: python read_bangs.py <record.json> [<record.json> ...]; one table per record, Markdown rows. Integers only."""

from __future__ import annotations

import json
import sys
from collections import Counter
from typing import Any


def cycles_of(record: dict[str, Any]) -> list[tuple[int, int]]:
    n = record["cube"] ** 3
    tops = [i for i, k in record["turns"] if k == n]
    bounds = [0] + tops + [record["intervals"] + 1]
    return [(bounds[k], bounds[k + 1]) for k in range(len(bounds) - 1)]


def read(path: str) -> None:
    r = json.load(open(path, encoding="utf-8"))
    n = r["cube"] ** 3
    gamma = int(r["gamma"])
    nodes = r["nodes"]
    log = r["log"]
    means = {d["i"]: sum(d["X"]) // len(d["X"]) for d in nodes}
    uniform = {d["i"]: (min(d["X"]) == max(d["X"])) for d in nodes}
    returns = [d["i"] for d in nodes if min(d["X"]) == max(d["X"]) == gamma and d["i"] > 1]
    ivs = sorted(means)
    bottoms = [i for k, i in enumerate(ivs[1:-1], 1) if means[ivs[k - 1]] > means[i] <= means[ivs[k + 1]] and means[i] < gamma + gamma // 2]
    tops = [i for i, k in r["turns"] if k == n]
    partial = [(i, k) for i, k in r["turns"] if k != n]
    print(f"\n### {path}")
    print(f"Nodes {n}, intervals {r['intervals']}, Gamma {gamma}; whole-board tops (bangs) at {tops}; exact returns (every Node at Gamma) at {returns}; bottoms (the mean's local minima below 3 Gamma / 2) at {[(i, means[i]) for i in bottoms]}; partial turns {len(partial)} (first {partial[:3]}); run back {r.get('run_back')}; counts {r['counts']}")
    print("| cycle | intervals | top X (i) | bottom X (i) | X uniform at | births | credits (line: count) | credits even / odd | refusals by cause | species credited | frozen max | light F max | handedness +/- | gates shown |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for k, (a, b) in enumerate(cycles_of(r)):
        span = [i for i in ivs if a < i <= b]
        if not span:
            continue
        births = [e for e in log if e["event"] == "birth" and a < e["i"] <= b]
        credits = [e for e in log if e["event"] == "credit" and a < e["i"] <= b]
        refused = Counter(e["cause"] for e in log if e["event"] == "refused" and a < e["i"] <= b)
        by_line = Counter(e["line"] for e in credits)
        even = sum(1 for e in credits if sum(e["node"]) % 2 == 0)
        odd = len(credits) - even
        top_i = max(span, key=lambda i: means[i])
        bot_i = min(span, key=lambda i: means[i])
        uni = sum(1 for i in span if uniform[i])
        frozen = max(len(d["frozen"]) for d in nodes if a < d["i"] <= b)
        fmax = max(abs(v) for d in nodes if a < d["i"] <= b for axis in d["current"] for v in axis)
        hand = Counter()
        for e in births:
            plus, minus = e["plus"], e["minus"]
            diff = [(p - m) for p, m in zip(plus, minus, strict=True)]
            side = [x for x in diff if x != 0]
            if side:
                x = side[0]
                hand["+" if x in (1, -(r["cube"] - 1)) else "-"] += 1
        gates = []
        if births:
            gates.append("46 births at the bang" if k > 0 else "births")
        if credits:
            gates.append("8 credits")
        if len(by_line) > 1:
            gates.append("4 species > 1")
        if fmax > 0:
            gates.append("light current")
        if uni == len(span):
            gates.append("1 uniform")
        print(f"| {k} | {a + 1}..{min(b, r['intervals'])} | {means[top_i]} ({top_i}) | {means[bot_i]} ({bot_i}) | {uni} of {len(span)} | {len(births)} | {dict(sorted(by_line.items()))} | {even} / {odd} | {dict(sorted(refused.items()))} | {len(by_line)} | {frozen} | {fmax} | {hand['+']} / {hand['-']} | {', '.join(gates) or 'none'} |")


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    for path in argv[1:]:
        read(path)


if __name__ == "__main__":
    main(sys.argv)
