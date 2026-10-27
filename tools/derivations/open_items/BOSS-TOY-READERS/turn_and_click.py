"""Does a detector fail to click where its time turned? On a record: for every credit and every refusal, whether its
Node was turned at that interval (the Node lines' turned set, C order over the board's shape), against the base rate
of turned Node-intervals. Integers only; counts and fractions as quotients."""
import json, sys, collections
from fractions import Fraction
sys.set_int_max_str_digits(2000000)
r = json.load(open(sys.argv[1]))
shape = r["world"]["shape"]
def index(node):
    k = 0
    for c, n in zip(node, shape):
        k = k * n + c
    return k
turned = {f["i"]: set(f["turned"]) for f in r["nodes"]}
cells = len(r["nodes"][0]["X"])
base = Fraction(sum(len(v) for v in turned.values()), cells * len(turned))
print(f"{sys.argv[1].split('/')[-1]}: base rate of turned Node-intervals {float(base):.4f}")
kinds = collections.defaultdict(lambda: [0, 0])
for e in r["log"]:
    ev = e.get("event")
    if ev not in ("credit", "refused") or "node" not in e or e.get("i") not in turned:
        continue
    key = "credit" if ev == "credit" else f"refused:{e.get('cause')}"
    kinds[key][0] += 1
    kinds[key][1] += index(e["node"]) in turned[e["i"]]
for key, (n, t) in sorted(kinds.items(), key=lambda kv: -kv[1][0]):
    print(f"  {key:<24} {n:>6} events, at a turned Node {t:>6} = {t/n:.4f}  (x{(Fraction(t, n)/base) if base else 0:.2f} the base)" if n else "")
# turned the interval BEFORE the event (the time reversed just before)
prev = collections.defaultdict(lambda: [0, 0])
for e in r["log"]:
    ev = e.get("event")
    if ev not in ("credit", "refused") or "node" not in e or (e.get("i", 0) - 1) not in turned:
        continue
    key = "credit" if ev == "credit" else f"refused:{e.get('cause')}"
    prev[key][0] += 1
    prev[key][1] += index(e["node"]) in turned[e["i"] - 1]
print("  turned at the interval before:")
for key, (n, t) in sorted(prev.items(), key=lambda kv: -kv[1][0]):
    print(f"    {key:<22} {n:>6} events, turned the interval before {t:>6} = {t/n:.4f}")
