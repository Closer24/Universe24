"""pl2: the records compared compactly, one row per record and reading: births, credits (laid back), turns, run back, the first interval where the X lines part from the first column's record, the max bits. Usage: compare_records.py <label=path> ..."""
import json, sys
sys.set_int_max_str_digits(0)
rows = []
base = None
for arg in sys.argv[1:]:
    label, path = arg.split("=", 1)
    r = json.load(open(path))
    credits = [e for e in r["log"] if e["event"] == "credit"]
    row = {"record": label, "births": int(r["counts"]["births"]), "credits": len(credits), "laid back": sum(1 for c in credits if "laid_back" in c),
           "turns": int(r["counts"]["turns"]), "refused stop": int(r["counts"]["refused_stop"]), "run back": r["run_back"], "max bits": max(int(x["max bits"]) for x in r["rows"]),
           "integers": r["rows"][-1]["integers"], "mean X at the end": sum(r["nodes"][-1]["X"]) // len(r["nodes"][-1]["X"])}
    if base is None:
        base = r
        row["X lines against the first"] = "the first"
    else:
        first = next((l["i"] for l, m in zip(base["nodes"], r["nodes"]) if l["X"] != m["X"]), None)
        same_log = [{k: v for k, v in e.items() if k not in ("arrivals", "laid_back")} for e in base["log"]] == [{k: v for k, v in e.items() if k not in ("arrivals", "laid_back")} for e in r["log"]]
        row["X lines against the first"] = "bit for bit" if first is None and same_log else f"apart from interval {first}" + ("" if not same_log else " (the log equal)")
    rows.append(row)
print(json.dumps(rows, indent=1))
