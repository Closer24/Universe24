"""lc1: which Node digs: at chosen intervals, the Node of the largest X, its X, the board's mean X and the least X, from the engine's record (its Node lines). Usage: deepest.py <rec.json> <intervals, comma-separated>"""
import json, sys
sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1]))
want = [int(x) for x in sys.argv[2].split(",")]
cube = rec["cube"]
for line in rec["nodes"]:
    if line["i"] in want:
        xs = line["X"]
        k = max(range(len(xs)), key=lambda j: xs[j])
        at = (k // (cube * cube), (k // cube) % cube, k % cube)
        print(json.dumps({"i": line["i"], "deepest node": k, "xyz": at, "X there": xs[k], "mean X": sum(xs) // len(xs), "X min": min(xs), "content there": line["content"][k], "frozen": len(line["frozen"]), "turned": line["turned"][:6]}))
