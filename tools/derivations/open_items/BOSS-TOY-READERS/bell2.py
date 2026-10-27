"""Bell in the clicks with the outcome born at the click: the take's remainder's side of the half of its unit
(2 r >= booked: +1, else -1, the division's third output read, a reading of an act in the law) and the setting the
detector's own proper clock parity at its click. Pairs: the first credit at each end of a birth after it.
Variants: every credit; and only the credits at a Node whose time did not turn at that interval (the click in the
Node's own direction, read on the record as it is). S over the four cells as a fraction; the per-cell counts shown."""
import json, sys
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
births = [e for e in r["log"] if e.get("event") == "birth"]
credits = [e for e in r["log"] if e.get("event") == "credit"]
def outcome(k):
    return 1 if 2 * int(k["remainder"]) >= int(k["booked"]) else -1
def run(keep, label):
    by_end = {}
    for k in credits:
        if keep(k):
            by_end.setdefault((tuple(k["node"]), k["line"]), []).append(k)
    cells = {}
    for b in births:
        ends = []
        for where in (b["minus"], b["plus"]):
            ks = [k for k in by_end.get((tuple(where), b["line_pair"]), []) if int(k["i"]) > int(b["i"])]
            ends.append(ks[0] if ks else None)
        if None in ends:
            continue
        a, c = ends
        cells.setdefault((int(a["proper"]) % 2, int(c["proper"]) % 2), []).append(outcome(a) * outcome(c))
    n = sum(len(v) for v in cells.values())
    if len(cells) < 4:
        print(f"  {label}: {n} pairs, {len(cells)} of 4 cells: NOT READ  {dict((k, len(v)) for k, v in cells.items())}")
        return
    E = {c: Fraction(sum(v), len(v)) for c, v in cells.items()}
    S = E[(0, 0)] - E[(0, 1)] + E[(1, 0)] + E[(1, 1)]
    print(f"  {label}: {n} pairs; " + ", ".join(f"{c}: n={len(cells[c])} E={float(E[c]):+.3f}" for c in sorted(cells)) + f"; S = {float(S):+.3f}")
print(sys.argv[1].split("/")[-1], f"births {len(births)}, credits {len(credits)}, at turned Nodes {sum(1 for k in credits if index(k['node']) in turned.get(k['i'], set()))}")
run(lambda k: True, "every credit")
run(lambda k: index(k["node"]) not in turned.get(k["i"], set()), "the clicks in the Node's own direction")
