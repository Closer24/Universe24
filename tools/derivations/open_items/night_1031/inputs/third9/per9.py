"""THIRD9: exact counts over exactly one period of the pair's orbit at a steady passing (a reading). The structure is
read from the world (tri7.load_world, tri7.edge_set); the member is tri7.Member (the twin on G D) run beside
tri9.MemberD (the twin on D) from the same lay, their landings compared every round. The orbit is stepped until the
pair returns to its start; over that one period, read cyclically: landings n1, two running n2, three running n3; the
derived third after two, n2 h / t, with h / t the exact ratio by whole lifts of the window at u0 = the window's floor
(arith8 item 6: one value across the window at these passings); z^2 = (n3 t - n2 h)^2 / (n2 h (t - h)), per mille.
argv: src, then runs "x_ga,x_gb,x_ab,lay" (in m = D div 50; lay birth or standin, per7's stand-in)."""
import sys
from pathlib import Path

SRC = sys.argv[1]
RUNS = sys.argv[2:]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tri7  # noqa: E402
import tri9  # noqa: E402

tri7.setup(SRC)
from tensor24.algebra.carry import carry  # noqa: E402

universe, shape, held, lay, s0, world, star = tri7.load_world(SRC, Path(SRC).parent.joinpath("examples", "tensor24-click"))
key = int(lay.click.key[0, 0])
pairs, triangles = tri7.edge_set(world)
D = star["half"] * key
M = tri7.Member(len(pairs), triangles, D, star["senses"])
MD = tri9.MemberD(len(pairs), triangles, D, star["senses"])
N3, b = M.tdial[0], M.tborn[0]
m50 = carry(D, 50, 0)[0]
ga, ab, gb = (e for e, _ in M.C[0])


def fl(n, d):
    return carry(n, d, 0)[0]


def between(tc, ec):
    tau, eta = b + tc, b + ec
    tau = M.shear(tau, eta, 0)
    eta = M.shear(eta, tau, 0)
    eta = M.shear(eta, tau, 0)
    tau = M.shear(tau, eta, 0)
    return M.cen(tau - b, 0), M.cen(eta - b, 0)


c1, c2 = between(1, 0), between(0, 1)
L = [[c1[0], c2[0]], [c1[1], c2[1]]]  # from the Member's own shears: [[19, 60], [6, 19]]
TR, H0 = L[0][0] + L[1][1], L[0][0] - 1  # 38 and 18


def count3(A, B, r):
    if B < A:
        return 0
    return fl(B - r, 3) - fl(A - 1 - r, 3)


def ratio(y):
    """(hits, total) for u0 at the window's floor: u1 over W in its class mod 3, u(t+2) = 38 u1 - u0 + 18 (y + 1)."""
    tr, lo = TR, N3 - y
    cst = carry(H0 * (y + 1), N3, 0)[1]
    u0 = lo
    r1 = carry(u0 + y, 3, 0)[1]
    tot = count3(lo, N3 - 1, r1)
    hits = 0
    zmin, zmax = tr * lo - u0 + cst, tr * (N3 - 1) - u0 + cst
    for k in range(fl(zmin, N3) - 1, fl(zmax, N3) + 2):
        A = -fl(-(k * N3 + lo + u0 - cst), tr)
        B = fl(k * N3 + N3 - 1 + u0 - cst, tr)
        hits += count3(max(A, lo), min(B, N3 - 1), r1)
    return hits, tot


print(f"per9: edges {pairs}, C {M.C}, G {M.G}; G D = {N3}; the twin's dial on D {MD.ddial[0]}", flush=True)
for run in RUNS:
    *xs, LAY = run.split(",")
    XM = [int(v) for v in xs]
    x = [0] * len(pairs)
    x[ga], x[gb], x[ab] = XM[0] * m50, XM[1] * m50, XM[2] * m50
    y = sum(sg * x[e] for e, sg in M.C[0])
    tau, eta = [b], [b]
    if LAY == "standin":
        r = 17
        vals = []
        for d in M.dial + M.tdial + M.tdial:
            r = carry(r * 6364136223846793005 + 1442695040888963407, 1 << 64, 0)[1]
            vals.append(carry(r * d, 1 << 64, 0)[0])
        tau, eta = vals[3:4], vals[4:5]
    tauD = list(tau)
    etaD = [MD.dborn[0] + MD.dcen(eta[0] - b, 0)]  # the same centred twin, held on D
    start = (tau[0], eta[0])
    f, fD = list(M.born), list(M.born)
    seq, apart, k = [], 0, 0
    while True:
        q, w = M.step(x, f, tau, eta)
        qD, wD = MD.step(x, fD, tauD, etaD)
        apart += int(w != wD or q != qD)
        seq.append(1 if w[0] else 0)
        k += 1
        if (tau[0], eta[0]) == start:
            break
    n1 = sum(seq)
    n2 = sum(seq[i] * seq[(i + 1) % k] for i in range(k))
    n3 = sum(seq[i] * seq[(i + 1) % k] * seq[(i + 2) % k] for i in range(k))
    h, t = ratio(y)
    num = n3 * t - n2 * h
    z2 = fl(1000 * num * num, n2 * h * (t - h))
    print(f"{list(XM)} m, {LAY}: one period {k} rounds; landings {n1} (y k / (G D) = {fl(y * k, N3)}); two running {n2};"
          f" after two a third {n3} of {n2}, derived {fl(n2 * h, t)} ({fl(1000 * h * N3, t * y)} per mille of a);"
          f" z^2 {z2} per mille; the twin on D against on G D: {apart} rounds apart", flush=True)
print("DONE", flush=True)
