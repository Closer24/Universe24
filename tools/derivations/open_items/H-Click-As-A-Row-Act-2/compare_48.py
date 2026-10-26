"""The 48's verdicts image for image, the copy against the head: run_48.py's summary lines (one JSON per image). Usage: compare_48.py copy.summary head.summary"""
import json, sys
a, b = ([json.loads(l) for l in open(p) if l.startswith("{") and "det" in l] for p in sys.argv[1:3])
same = sum(1 for x, y in zip(a, b) if x == y)
tally = lambda rows: {k: sum(1 for r in rows if r["verdict"] == k) for k in ("EQUAL", "CONJUGATE", "APART")}
rot = lambda rows: tally([r for r in rows if r["det"] == 1]); ref = lambda rows: tally([r for r in rows if r["det"] == -1])
print(json.dumps({"images": [len(a), len(b)], "equal_image_for_image": same, "copy_rotations": rot(a), "copy_reflections": ref(a), "head_rotations": rot(b), "head_reflections": ref(b), "base": {k: a[0][k] for k in ("births", "credits")} if a else None, "first_apart": sorted({r["first_apart_equal"] for r in a if r["verdict"] == "APART"})}))
