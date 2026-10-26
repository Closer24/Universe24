"""rl2: two records compared on the course alone: the counts, the log's events on their common keys (event, i, node, cause, row, pair, children, sense, line), the turned Nodes per interval, the run back; the reader's own extra keys ignored. Usage: compare_records.py <found.json> <cached.json>"""
import json
import sys

sys.set_int_max_str_digits(0)
KEYS = ("event", "i", "node", "cause", "row", "pair", "children", "sense", "line", "beat", "at", "to")
a, b = (json.load(open(p)) for p in sys.argv[1:3])


def events(rec):
    return [{k: str(e.get(k)) for k in KEYS if k in e} for e in rec.get("log", [])]


ea, eb = events(a), events(b)
first = next((k for k, (x, y) in enumerate(zip(ea, eb)) if x != y), None)
out = {
    "counts_equal": a.get("counts") == b.get("counts"),
    "counts": a.get("counts"), "cached_counts": b.get("counts"),
    "log_lengths": [len(ea), len(eb)],
    "log_equal_on_common_keys": first is None and len(ea) == len(eb),
    "first_apart": None if first is None else {"index": first, "found": ea[first], "cached": eb[first]},
    "turns_equal": a.get("turns") == b.get("turns"),
    "nodes_equal": a.get("nodes") == b.get("nodes"),
    "run_back": a.get("run_back"), "cached_run_back": b.get("run_back"),
}
print(json.dumps(out, default=str))
