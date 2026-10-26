"""The matter count of a record from its log alone (gate 21's clause: the + child at the take's Node against the other end), per record and per bang (board.recurring_bang's bangs, the exact returns), with the children's charges summed and the rows' W total at the first and the last mark. Usage: python count_matter.py <record.json> [...]"""
import json
import sys

from event_universe import board
from event_universe.decoder import Record

sys.set_int_max_str_digits(0)


def count(path: str) -> dict:
    run = json.load(open(path, encoding="utf-8"))
    rec = Record(run)
    births = rec.births
    right = [b for b in births if b["plus"] == b["node"]]
    left = [b for b in births if b["plus"] != b["node"]]
    exact = board.exact_of(rec)
    bangs = [1] + [i + 1 for i in exact]
    edges = bangs + [int(run["intervals"]) + 1]
    per_bang = []
    for lo, hi in zip(edges, edges[1:]):
        inside = [b for b in births if lo <= int(b["i"]) < hi]
        r = sum(1 for b in inside if b["plus"] == b["node"])
        per_bang.append({"bang_from": lo, "births": len(inside), "plus_at_take": r, "plus_other": len(inside) - r, "excess": 2 * r - len(inside)})
    w_sum = sum(int(x) for b in births for x in b["W_children"])
    rows = run["rows"]
    return {
        "record": path,
        "intervals": int(run["intervals"]),
        "births": len(births),
        "plus_at_take": len(right),
        "plus_other": len(left),
        "excess": len(right) - len(left),
        "W_children_sum": w_sum,
        "W_total_first_mark": rows[0].get("W total") if rows else None,
        "W_total_last_mark": rows[-1].get("W total") if rows else None,
        "W_abs_sum_last_mark": rows[-1].get("W abs sum") if rows else None,
        "bangs": bangs,
        "per_bang": per_bang,
        "counts": run["counts"],
        "run_back": run["run_back"],
    }


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps(count(p)))
