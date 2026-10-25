"""cs4: the draws per phase class at the closes that reached the lay, the first n landings of a record (the census's draws_per_class), with the births and the refusals of that interval by cause."""
import json, sys
sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1]))
n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
log = rec["log"]
light = rec["log"][0]["line_pair"]
print(sys.argv[1], "the light's index", light, "records", len(rec["planes"]))
shown = 0
for e in log:
    if e["event"] == "landing":
        i = e["i"]
        births = sum(1 for b in log if b["event"] == "birth" and b["i"] == i)
        causes = {}
        for r in log:
            if r["event"] == "refused" and r["i"] == i:
                k = r["cause"] + ("_crowd" if "children_at_one_node" in r else "_standing" if "standing" in r else "")
                causes[k] = causes.get(k, 0) + 1
        print(" i", i, "draws per class", json.dumps(e["draws_per_class"], sort_keys=True), "taken rows", e.get("taken_rows"), "births", births, "refused", json.dumps(causes, sort_keys=True))
        shown += 1
        if shown >= n:
            break
