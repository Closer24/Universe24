"""The floor by itself against the floor's edge (the owner's words of 10:11 to 11:10 UTC; FLOOR1's two pairs; David's
Harary rule, 6542620339): like tied hands banded pairwise, as node-all's hands' tie lays them (every two distinct tied
trains of one part), each band read as its own square (t/2)(x_i + x_j)^2, and nothing else: no own spring laid, no held
hand (its lend 0, FLOOR1's clean test of the edge). Two hands make one band, an even structure: one swing is free. Three
hands make a plain triangle of bands, a frustrated loop: every swing holds a spring. Stepped by the engine's gear form
(miracle/equil.py), whole numbers and Rule3's carry only, laid with the hands' difference moving.
Readings per structure, 20,000 rounds unless given: the widest count every 4,000 rounds; E32's change against the teeth's
share at every round (the identity); the run back from the end state alone.
Usage: python3 -I frustration.py <node-all src> <the click world's universe.json> [rounds]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

ROUNDS = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
chosen = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["chosen"]
TIE2 = int(chosen["tie"])  # the click world's hands' tie, the band
HALF_BAND, odd = carry(TIE2, 2, 0)
assert odd == 0
W = 600000000  # the click world's rest teeth (node-all's loader: gearing's rest)
GEAR = W + W


def split(n, d):
    q, r = carry(n + d, d + d, 0)
    return q, r - d


def pushes(a, bands):
    """Each band (t/2)(x_i + x_j)^2 pushes both its hands by -t (x_i + x_j)."""
    f = [0] * len(a)
    for i, j in bands:
        p = -TIE2 * (a[i] + a[j])
        f[i] += p
        f[j] += p
    return f


def energy(a, b, bands):
    """E32: the kinetic 16 W^2 (a - b)^2 per hand, and each band's square polarized at the edge (b, a):
    16 W t (a_i + a_j)(b_i + b_j)."""
    e = sum(16 * W * W * (x - y) * (x - y) for x, y in zip(a, b))
    for i, j in bands:
        e += 16 * W * TIE2 * (a[i] + a[j]) * (b[i] + b[j])
    return e


def round_(a, b, s, bands):
    f = pushes(a, bands)
    a1, s1 = [], []
    for i in range(len(a)):
        q, kept = split(GEAR * (a[i] - b[i]) + GEAR * (a[i] - b[i]) + 4 * f[i] + s[i], GEAR)
        a1.append(a[i] + q)
        s1.append(kept)
    return a1, s1


def share(a, b, a1, s, s1):
    return sum(4 * W * (z - y) * (p - r) for z, y, p, r in zip(a1, b, s, s1))


def read(name, lay_a, lay_b, bands):
    a, b, s = list(lay_a), list(lay_b), [0] * len(lay_a)
    start = (list(a), list(b), list(s))
    held, widest = 0, []
    for n in range(1, ROUNDS + 1):
        a1, s1 = round_(a, b, s, bands)
        held += energy(a1, a, bands) - energy(a, b, bands) == share(a, b, a1, s, s1)
        a, b, s = a1, a, s1
        if carry(n, 4000, 0)[1] == 0:
            widest.append((n, max(abs(x) for x in a)))
    ma, mb, ms = list(b), list(a), [-1 - v for v in s]
    for _ in range(ROUNDS):
        ma1, ms1 = round_(ma, mb, ms, bands)
        ma, mb, ms = ma1, ma, ms1
    back = (list(mb), list(ma), [-1 - v for v in ms]) == start
    print(f"== {name}: the lay {lay_a} now, {lay_b} before; {ROUNDS} rounds", flush=True)
    print(f"   the identity held in {held} of {ROUNDS} rounds; the largest count every 4,000 rounds: {widest}; the run back"
          f" exact: {back}", flush=True)


print(f"bands of the click world's hands' tie {TIE2}, each its own square (t/2 = {HALF_BAND} on each hand); W {W};"
      f" no own spring laid and no held hand", flush=True)
read("two tied hands, one band (an even structure: the floor's edge)", [40, -40], [39, -39], [(0, 1)])
read("three tied hands, a plain triangle of bands (a frustrated loop)", [40, -40, 0], [39, -39, 0],
     [(0, 1), (1, 2), (0, 2)])
print("exit", flush=True)
