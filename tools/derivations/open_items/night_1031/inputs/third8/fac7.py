"""THIRD7's dial read for the turn's period (a reading, never an act): the triangle's dial G D at the click world's key,
its factors by trial division with the carry, and the order of the pair's round L = [[19, 60], [6, 19]] modulo each
prime power factor (the least k with L^k = I there), so that the pair's turn on the dial is seen as the product of its
parts: where L is I modulo a factor, that part of the hidden pair is never turned. Whole numbers only. argv: src."""
import json
import sys
from pathlib import Path

SRC = sys.argv[1]
sys.path.insert(0, SRC)
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402

world = Path(SRC).parent.joinpath("examples", "tensor24-click")
key = json.loads(world.joinpath("universe.json").read_text())["chosen"]["key"]
axes = len(json.loads(world.joinpath("piece.json").read_text())["shape"])
spokes = len(loading.star(axes))
senses = carry(spokes, axes, 0)[0]
D = carry(spokes, senses, 0)[0] * key
G = 3  # C^T C of the click world's one triangle (mat7.txt item 2), read there from C
N = G * D
n, f, factors = N, 2, []
while f * f <= n:
    q, r = carry(n, f, 0)
    if r == 0:
        factors.append(f)
        n = q
    else:
        f += 1
if n > 1:
    factors.append(n)
powers = {}
for p in factors:
    powers[p] = powers.get(p, 0) + 1
print(f"the triangle's dial G D = {N} = " + " x ".join(f"{p}^{e}" if e > 1 else f"{p}" for p, e in sorted(powers.items())))
L = [[19, 60], [6, 19]]


def mulm(a, b, m):
    return [[carry(a[i][0] * b[0][j] + a[i][1] * b[1][j], m, 0)[1] for j in range(2)] for i in range(2)]


for p, e in sorted(powers.items()):
    m = 1
    for _ in range(e):
        m *= p
    I = [[carry(1, m, 0)[1], 0], [0, carry(1, m, 0)[1]]]
    A, k = mulm(L, I, m), 1
    while A != I:
        A = mulm(A, L, m)
        k += 1
    print(f"  modulo {m}: L to the power {k} is I (the pair's round there repeats every {k} rounds)")
