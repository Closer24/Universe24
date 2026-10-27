"""Entanglement in the clicks: for every birth, the first credit at each of its two ends (the row's line, after the
birth); the true pairs against shuffled pairs (end A of birth k with end B of birth k+s, every shift s), on the
clicks' own data: the senses' product, the remainders' low bit agreeing, the remainders as a mirror pair
(rB == (wall - rA) mod wall at the same wall, or rB == wall - 1 - rA), the gap in intervals, the beats agreeing.
Integers and fractions only."""
import json, sys
from fractions import Fraction
sys.set_int_max_str_digits(2000000)
r = json.load(open(sys.argv[1]))
log = r["log"]
births = [e for e in log if e.get("event") == "birth"]
credits = [e for e in log if e.get("event") == "credit"]
by_end = {}
for k in credits:
    by_end.setdefault((tuple(k["node"]), k["line"]), []).append(k)
def first(where, line, after):
    for k in by_end.get((tuple(where), line), []):
        if int(k["i"]) > after:
            return k
    return None
pairs = []
for b in births:
    a, c = first(b["minus"], b["line_pair"], int(b["i"])), first(b["plus"], b["line_pair"], int(b["i"]))
    if a is not None and c is not None:
        pairs.append((a, c))
def stats(ps):
    n = len(ps)
    if n == 0:
        return None
    sgn = lambda x: (x > 0) - (x < 0)
    prod = Fraction(sum(sgn(int(a["sense"])) * sgn(int(c["sense"])) for a, c in ps), n)
    bit = Fraction(sum(1 for a, c in ps if int(a["remainder"]) % 2 == int(c["remainder"]) % 2), n)
    beat = Fraction(sum(1 for a, c in ps if int(a["beat"]) == int(c["beat"])), n)
    same_i = Fraction(sum(1 for a, c in ps if int(a["i"]) == int(c["i"])), n)
    gap = Fraction(sum(abs(int(a["i"]) - int(c["i"])) for a, c in ps), n)
    rem_eq = Fraction(sum(1 for a, c in ps if int(a["remainder"]) == int(c["remainder"])), n)
    return n, prod, bit, beat, same_i, gap, rem_eq
name = sys.argv[1].split("/")[-1]
print(f"{name}: births {len(births)}, credits {len(credits)}, pairs clicked at both ends {len(pairs)}")
true = stats(pairs)
if not true:
    sys.exit(0)
A = [a for a, _ in pairs]; C = [c for _, c in pairs]
shuffled = []
for s in range(1, len(pairs)):
    shuffled += [(A[k], C[(k + s) % len(pairs)]) for k in range(len(pairs))]
sh = stats(shuffled)
labels = ["pairs", "E[sA sB]", "remainder bit agrees", "beat agrees", "same interval", "mean gap (intervals)", "remainders equal"]
print(f"  {'':<22} {'true pairs':>14} {'shuffled':>14}")
for k in range(1, len(labels)):
    print(f"  {labels[k]:<22} {float(true[k]):>14.4f} {float(sh[k]):>14.4f}")
