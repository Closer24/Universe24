"""vf12: two records compared field by field: nodes (the Node lines per interval), rows (apart from milliseconds), counts, turns, run_back, integers; the log entry by entry with the fields apart named and counted (taken_line expected new on every birth / credit; the refusals' fall expected apart where the sign chooses the other line); hashes of the whole file with taken_line and the refusals' fall masked. Usage: python compare_records.py a.json b.json"""
import hashlib
import json
import sys

sys.set_int_max_str_digits(0)


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def strip_ms(rows):
    return [{k: v for k, v in r.items() if k != "milliseconds"} for r in rows]


def masked(rec):
    log = []
    for e in rec["log"]:
        e = dict(e)
        e.pop("taken_line", None)
        if e.get("event") == "refused" and e.get("cause") == "stop":
            e.pop("fall", None)
        if "takes" in e:
            e["takes"] = [{k: v for k, v in t.items() if k != "taken_line"} for t in e["takes"]]
        log.append(e)
    return {k: (log if k == "log" else strip_ms(v) if k == "rows" else v) for k, v in rec.items()}


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()[:16]


a, b = load(sys.argv[1]), load(sys.argv[2])
na, nb = sys.argv[1].split("/")[-1], sys.argv[2].split("/")[-1]
print(na, "against", nb)
print("  keys equal:", sorted(a) == sorted(b), "| nodes equal:", a["nodes"] == b["nodes"], "(%d lines)" % len(a["nodes"]), "| rows equal apart from milliseconds:", strip_ms(a["rows"]) == strip_ms(b["rows"]), "| counts equal:", a["counts"] == b["counts"], "| turns equal:", a["turns"] == b["turns"], "| run_back:", a["run_back"], b["run_back"], "| integers:", a.get("integers"), b.get("integers"))
print("  counts a:", a["counts"])
if a["counts"] != b["counts"]:
    print("  counts b:", b["counts"])
la, lb = a["log"], b["log"]
print("  log lengths:", len(la), len(lb))
apart = {}
fall_apart = []
taken_line_on = {"birth": 0, "credit": 0, "takes": 0}
lines_taken = {}
for i, (x, y) in enumerate(zip(la, lb)):
    kx, ky = set(x), set(y)
    for k in kx | ky:
        if x.get(k) != y.get(k):
            apart[k] = apart.get(k, 0) + 1
            if k == "fall":
                fall_apart.append((x.get("i"), x.get("node"), x.get("row"), x.get("fall"), y.get("fall")))
for e in la + lb:
    if "taken_line" in e:
        taken_line_on[e["event"]] = taken_line_on.get(e["event"], 0) + 1
        for t in e.get("takes", [e]):
            k = t["taken_line"]
            lines_taken[k] = lines_taken.get(k, 0) + 1
print("  log fields apart (field: entries):", apart)
print("  refusals' fall apart:", len(fall_apart), "first 6:", fall_apart[:6])
print("  taken_line present on (event: entries, both files):", taken_line_on, "| lines taken (line: takes, both files):", lines_taken)
print("  masked hashes (taken_line and the stop refusals' fall masked, milliseconds dropped):", digest(masked(a)), digest(masked(b)), "equal:", masked(a) == masked(b))
print("  whole hashes (milliseconds dropped):", digest({**a, "rows": strip_ms(a["rows"])}), digest({**b, "rows": strip_ms(b["rows"])}))
