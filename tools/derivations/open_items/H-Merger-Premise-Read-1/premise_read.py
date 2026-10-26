"""The premise's two moments counted on a record written under the flag's `note` setting:
every meeting's current, twist and the two ends' charges as the birth laid them (the interval's
start, the engine's own read) beside the same four at the close's own moment (after the step),
and what each reading would decide: the rest branch (a merger at rest), the moving branch, or a
refusal by name. Integers only. Usage: premise_read.py <record.json> [out <summary.json>]"""

from __future__ import annotations

import json
import sys
from collections import Counter


def decide(flow: int, h: int, w_a: int, w_b: int, gapped: bool) -> str:
    """close.meet's own branching on the four readings of one meeting."""
    rest = flow == 0 and w_a * w_b < 0
    if (flow == 0 or h == 0) and not rest:
        return "refused orientation" if flow == 0 else "refused twist"
    if gapped and w_a * w_b >= 0:
        return "refused sense"
    return "rest" if rest else "moving"


def main(argv: list[str]) -> int:
    with open(argv[1], encoding="utf-8") as f:
        rec = json.load(f)
    log = rec["log"]
    premise = [e for e in log if e["event"] == "premise"]
    births = [e for e in log if e["event"] == "birth"]
    merged = [e for e in births if e["taken_row"] != e["line_pair"]]
    laid_at = {(e["i"], tuple(e["minus"]), tuple(e["plus"]), e["taken_row"]) for e in merged}
    counts: Counter[str] = Counter()
    pairs: Counter[str] = Counter()
    shifted_flow: Counter[str] = Counter()
    rows: list[dict[str, object]] = []
    for e in premise:
        a_flow, a_h, a_wa, a_wb = e["laid"]
        b_flow, b_h, b_wa, b_wb = e["shifted"]
        first = decide(a_flow, a_h, a_wa, a_wb, True)
        second = decide(b_flow, b_h, b_wa, b_wb, True)
        counts[first + " | " + second] += 1
        if first == "rest":
            pairs[second] += 1
            shifted_flow["zero" if b_flow == 0 else "apart"] += 1
            if len(rows) < 12:
                rows.append({"i": e["i"], "node": e["node"], "laid": e["laid"], "shifted": e["shifted"]})
    print(json.dumps({"meetings read": len(premise), "births": len(births), "merger births": len(merged)}))
    print(json.dumps({"laid reading | close reading": dict(counts)}))
    print(json.dumps({"the rest branch at the laid state, under the close's": dict(pairs)}))
    print(json.dumps({"the stepped current at a pair met at rest": dict(shifted_flow)}))
    print(json.dumps({"first twelve pairs at rest": rows}))
    out = argv[argv.index("out") + 1] if "out" in argv else None
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "meetings": len(premise),
                    "births": len(births),
                    "merger_births": len(merged),
                    "by_reading": dict(counts),
                    "rest_under_close": dict(pairs),
                    "stepped_current": dict(shifted_flow),
                    "sample": rows,
                    "merger_keys": len(laid_at),
                },
                f,
                indent=1,
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
