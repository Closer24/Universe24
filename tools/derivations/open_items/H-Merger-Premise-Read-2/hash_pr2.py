"""pr2: two records hashed and compared with the rows' milliseconds and the reading's own log lines
struck (the premise lines the flag adds for the measure), so that the two premises' records are
compared on the board, the births, the takes, the counts and the run back alone.
Usage: python hash_pr2.py <one.json> <other.json>"""
import hashlib
import json
import sys

sys.set_int_max_str_digits(0)


def struck(rec):
    out = {k: v for k, v in rec.items() if k != "rows"}
    out["log"] = [e for e in rec["log"] if e.get("event") != "premise"]
    out["rows"] = [{k: v for k, v in r.items() if k != "milliseconds"} for r in rec.get("rows", [])]
    return out


def digest(path):
    return hashlib.sha256(
        json.dumps(struck(json.load(open(path))), sort_keys=True).encode()
    ).hexdigest()


def main(one, other):
    a, b = digest(one), digest(other)
    first = None
    ra, rb = json.load(open(one)), json.load(open(other))
    la = [e for e in ra["log"] if e.get("event") != "premise"]
    lb = [e for e in rb["log"] if e.get("event") != "premise"]
    for k, (x, y) in enumerate(zip(la, lb)):
        if x != y:
            first = {"log_line": k, "interval": x.get("i"), "one": x.get("event"), "other": y.get("event")}
            break
    print(
        json.dumps(
            {
                "one": a,
                "other": b,
                "verdict": "EQUAL" if a == b else "APART",
                "log_lines": [len(la), len(lb)],
                "first_log_line_apart": first,
                "counts_equal": ra["counts"] == rb["counts"],
                "nodes_equal": ra.get("nodes") == rb.get("nodes"),
                "run_back": [ra.get("run_back"), rb.get("run_back")],
            }
        )
    )


if __name__ == "__main__":
    main(*sys.argv[1:])
