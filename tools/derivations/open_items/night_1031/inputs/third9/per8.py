"""THIRD8: the period of the triangle's pair at a steady passing (a reading), per7.py with nothing typed: the click
world's structure is loaded (tri7.load_world), the edges and the triangle read from it (tri7.edge_set), C and G = C^T C
by tri7.Member, the dial from the star and the world's key. From a lay, the member's pair (tau, eta) is stepped by the
Member's own step with the steady passing until it returns to its start; the rounds taken, and the landings in that
span against y k / (G D). The stand-in lay is per7's (the same whole-number generator, the same draws).
argv: src, cap, then one or more runs, each "x_ga,x_gb,x_ab,lay" (passings in m = D div 50; lay birth or standin)."""
import sys
from pathlib import Path

SRC, CAP = sys.argv[1], int(sys.argv[2])
RUNS = sys.argv[3:]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tri7  # noqa: E402

tri7.setup(SRC)
from tensor24.algebra.carry import carry  # noqa: E402

universe, shape, held, lay, s0, world, star = tri7.load_world(SRC, Path(SRC).parent.joinpath("examples", "tensor24-click"))
key = int(lay.click.key[0, 0])
pairs, triangles = tri7.edge_set(world)
D = star["half"] * key
M = tri7.Member(len(pairs), triangles, D, star["senses"])
m50 = carry(D, 50, 0)[0]
ga, ab, gb = (e for e, _ in M.C[0])
print(f"per8: edges {pairs}, the triangle (ga, ab, gb) = {triangles}, C {M.C}, G {M.G}; D = {D}, G D = {M.tdial[0]}",
      flush=True)
for run in RUNS:
    *xs, LAY = run.split(",")
    XM = [int(v) for v in xs]
    x = [0] * len(pairs)
    x[ga], x[gb], x[ab] = XM[0] * m50, XM[1] * m50, XM[2] * m50
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
    print(f"y = {y} ({XM} m; y mod 3 = {carry(y, 3, 0)[1]}), the {LAY} lay: the pair returns to its start after {k}"
          f" rounds{' (the cap)' if k >= CAP else ''}; landings in that span {landings}, against y k / (G D) ="
          f" {carry(y * k, M.tdial[0], 0)[0]}", flush=True)
print("DONE", flush=True)
