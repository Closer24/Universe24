"""vf12: a record's laws read: the births' charge (W_children summed), taken at or above booked, the integers' count per row (the fixed count) and the max bits per row (within 128), the run back, the lines taken. Usage: python read_records.py record.json ..."""
import json, sys
sys.set_int_max_str_digits(0)
for p in sys.argv[1:]:
    r = json.load(open(p))
    births = [e for e in r["log"] if e["event"] == "birth"]
    ints = sorted({row.get("integers") for row in r["rows"]})
    bits = max(row.get("max bits", 0) for row in r["rows"])
    tbits = max(row.get("max transient bits", 0) for row in r["rows"])
    lines = {}
    for e in r["log"]:
        if e["event"] in ("birth", "credit"):
            for t in e.get("takes", [e]):
                lines[t["taken_line"]] = lines.get(t["taken_line"], 0) + 1
    print(p.split("/")[-1], "| births", len(births), "| charge 0 at every birth", all(sum(int(x) for x in e["W_children"]) == 0 for e in births) if births else "no birth", "| taken >= booked", sum(1 for e in births if int(e["taken"]) >= int(e["booked"])), "of", len(births), "| integers per row", ints, "| max bits", bits, "| transient", tbits, "| run back", r["run_back"], "| lines taken", lines, "| counts births/credits/laid back/turns", r["counts"]["births"], r["counts"]["body_clicks"], r["counts"]["laid_back"], r["counts"]["turns"])
