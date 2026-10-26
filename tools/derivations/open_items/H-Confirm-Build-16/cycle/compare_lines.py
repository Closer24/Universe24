import json, sys, hashlib
a, b = (json.load(open(p)) for p in sys.argv[1:3])
def h(n): return hashlib.sha256(json.dumps({k: n[k] for k in sorted(n) if k != "i"}, sort_keys=True).encode()).hexdigest()[:16]
ha, hb = [h(n) for n in a["nodes"]], [h(n) for n in b["nodes"]]
print(sys.argv[3], "intervals", len(ha), len(hb), "equal lines", sum(x == y for x, y in zip(ha, hb)), "of", min(len(ha), len(hb)), "first apart", next((i + 1 for i, (x, y) in enumerate(zip(ha, hb)) if x != y), None))
print(" hashes", ha[:3], "...", ha[-1])
la, lb = a["log"][0], b["log"][0]
print(" lay logs", {k: la[k] for k in la if k in lb and la[k] == lb[k]} and "common equal keys " + str(sorted(k for k in la if k in lb and la[k] == lb[k])), "a-only", sorted(set(la) - set(lb)), "b-only", sorted(set(lb) - set(la)), "apart", sorted(k for k in la if k in lb and la[k] != lb[k]))
print(" counts equal", a["counts"] == b["counts"], a["counts"]["births"], b["counts"]["births"], "log len", len(a["log"]), len(b["log"]))
