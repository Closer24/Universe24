"""For every birth, whether the born pair is taken back by a merger at a later close on its own Link (a birth whose taken_row is the children's row and whose take Node and Link are the pair's ends), by the children's row: the quartet pairs against the plane pairs. Usage: python merger_after_birth.py <record.json> [...]"""
import json
import sys

for path in sys.argv[1:]:
    rec = json.load(open(path))
    births = [e for e in rec["log"] if e["event"] == "birth"]
    out = {}
    for b in births:
        s = int(b["line_pair"])
        ends = {tuple(b["minus"]), tuple(b["plus"])}
        later = [m for m in births if int(m["i"]) > int(b["i"]) and int(m["taken_row"]) == s and "takes" in m and {tuple(t["node"]) for t in m["takes"]} == ends]
        key = str(s)
        out.setdefault(key, [0, 0, []])
        out[key][1] += 1
        if later:
            out[key][0] += 1
            out[key][2].append(int(later[0]["i"]) - int(b["i"]))
    print(json.dumps({"record": path, "pairs merged on their own Link later, by children's row: [merged, born, the delays]": out}))
