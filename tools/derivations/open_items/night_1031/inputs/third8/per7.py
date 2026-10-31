"""THIRD7: the period of the triangle's pair at a steady passing (a reading): from a lay, the member's pair (tau, eta)
is stepped with the steady circulating passing y until it returns to its start; the rounds taken, and the landings in
one period against y times the period over the dial. Whole numbers only; tri7.Member's own arithmetic.
argv: src, x_ga, x_gb, x_ab (in m = D div 50), lay (birth or standin), cap."""
import json
import sys
from pathlib import Path

SRC = sys.argv[1]
XM = [int(v) for v in sys.argv[2:5]]
LAY, CAP = sys.argv[5], int(sys.argv[6])
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tri7  # noqa: E402

tri7.setup(SRC)
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402

world = Path(SRC).parent.joinpath("examples", "tensor24-click")
key = json.loads(world.joinpath("universe.json").read_text())["chosen"]["key"]
axes = len(json.loads(world.joinpath("piece.json").read_text())["shape"])
spokes = len(loading.star(axes))
senses = carry(spokes, axes, 0)[0]
D = carry(spokes, senses, 0)[0] * key
m50 = carry(D, 50, 0)[0]
M = tri7.Member(3, [(0, 2, 1)], D, senses)
x = [XM[0] * m50, XM[1] * m50, XM[2] * m50]  # edges (0, 1), (0, 2), (1, 2): ga, gb, ab
y = sum(sg * x[e] for e, sg in M.C[0])
tau, eta = [M.tborn[0]], [M.tborn[0]]
if LAY == "standin":
    r = 17
    vals = []
    for d in M.dial + M.tdial + M.tdial:
        r = carry(r * 6364136223846793005 + 1442695040888963407, 1 << 64, 0)[1]
        vals.append(carry(r * d, 1 << 64, 0)[0])
    tau, eta = vals[3:4], vals[4:5]
start = (tau[0], eta[0])
f = list(M.born)
landings, k = 0, 0
while True:
    q, w = M.step(x, f, tau, eta)
    landings += w[0]
    k += 1
    if (tau[0], eta[0]) == start or k >= CAP:
        break
print(f"y = {y} ({XM} m), the {LAY} lay: the pair returns to its start after {k} rounds"
      f"{' (the cap)' if k >= CAP else ''}; landings in that span {landings}, against y k / (G D) = "
      f"{carry(y * k, M.tdial[0], 0)[0]}")
