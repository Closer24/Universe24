"""cs2: a record above 1.5 MB kept slim: the Node lines kept at every fifth interval and at the turns (X and the turned Nodes alone), every credit's frame dropped (its i, node, line, sense, beat, taken, levels kept), the births kept whole, the diag's mergers dropped; everything else kept. Usage: python slim.py <in.json> <out.json>"""
import json
import sys

sys.set_int_max_str_digits(0)
with open(sys.argv[1], encoding="utf-8") as f:
    d = json.load(f)
d["nodes"] = [
    {"i": n["i"], "X": n["X"], "turned": n["turned"]}
    for n in d["nodes"]
    if int(n["i"]) % 5 == 0 or n["turned"] or 155 <= int(n["i"]) <= 195
]
log = []
for e in d["log"]:
    if e["event"] == "credit":
        log.append({k: e[k] for k in ("event", "i", "node", "line", "sense", "beat", "taken", "levels", "turned")})
    else:
        log.append(e)
d["log"] = log
for g in d["diag"]:
    g.pop("mergers", None)
with open(sys.argv[2], "w", encoding="utf-8") as f:
    json.dump(d, f)
