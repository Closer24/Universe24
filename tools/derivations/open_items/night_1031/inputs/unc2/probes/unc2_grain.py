"""UNC2's grain: every edge passing of a world is a whole multiple of G, read from the plan as the loader lays it.

Usage: python -I unc2_grain.py <tree> <world dir>

step.passing books on the side (t, u), for each term i of J's plan on the value legs, weight[i, u] x work_i, with
work_i = factor_i x (the product of its legs' readings) x (its target's a+ - b), all whole; so P(t, u) = given[t, u] -
given[u, t] is a whole multiple of every common divisor of the nonzero weight[i, u] x factor_i. step.crossing books
across[s, r, p] x (a whole number) on the Mesh sides. G is the gcd of all those nonzero whole numbers: every passing of
every state is a multiple of G (DERIVED from the two functions' lines). Printed: the distinct nonzero weight x factor
values and Mesh couplings, G, the edge key K, gcd(G, K), the birth h and h, K - 1 and K - 2 modulo gcd(G, K).
Whole numbers only; Rule3's carry the one division (Euclid's gcd by repeated carry, a reading outside the act).
"""

import json
import sys
from pathlib import Path

TREE, WORLD = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(TREE.joinpath("src")))

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.runner import run as trun  # noqa: E402


def gcd(x: int, y: int) -> int:
    """Euclid's gcd of two whole numbers by Rule3's carry, both taken from 0 up."""
    x, y = abs(x), abs(y)
    while y:
        _, r = carry(x, y, 0)
        x, y = y, r
    return x


paths = [WORLD.joinpath(n + ".json") for n in ("universe", "piece", "setting")]
universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
shape = piece["shape"]
engine = tmain.ENGINE
kinds, tables, square, lifted = engine.made(trun.star(len(shape)))
loaded, found = trun.load(universe, setting, trun.sites_of(shape), kinds, tables, square, lifted)
assert not found, found
layout = engine.layout(universe, shape, loaded)
weight, _, key, across, _ = layout.click
factor = layout.plan.factor
values = sorted({abs(int(weight[i, u]) * int(factor[i])) for i in range(weight.shape[0]) for u in range(weight.shape[1])
                 if int(weight[i, u]) * int(factor[i]) != 0})
couplings = sorted({abs(int(c)) for c in np.asarray(across).reshape(-1) if int(c) != 0})
G = 0
for v in values + couplings:
    G = gcd(G, v)
K = int(np.asarray(key).reshape(-1)[0])
keys = sorted({int(k) for k in np.asarray(key).reshape(-1)})
c = gcd(G, K)
h, _ = carry(K - 1, 2, 0)
print(f"world {WORLD.name}: the file's key {universe['chosen']['key']}, the edge keys {keys}")
print(f"  nonzero |weight x factor| on the edges: {values}")
print(f"  nonzero |Mesh couplings|: {couplings}")
print(f"  G = {G}; K = {K}; gcd(G, K) = {c}; the tooth's coset size K / gcd(G, K) = {carry(K, c, 0)[0] if c else K}")
if c:
    print(f"  the birth h = {h}; h mod {c} = {carry(h, c, 0)[1]}; (K - 1) mod {c} = {carry(K - 1, c, 0)[1]}; "
          f"(K - 2) mod {c} = {carry(K - 2, c, 0)[1] if K >= 2 else 0}; 0 mod {c} = 0")
