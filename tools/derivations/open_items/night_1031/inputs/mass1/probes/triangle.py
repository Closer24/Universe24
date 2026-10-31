"""MASS1 probe 2: the click world's triangle read from its files through the engine's own loader (node-all 9d75a4904,
the read-only copy in mass1/tree): which trains its live monomials join pairwise, the boundary maps B and C, K = C^T C,
the spectra of the triangle's own matrices, the third click's palindrome L at K (its trace, determinant and unit), its
order modulo the triangle's dial 3D read from the file's key, and the board's beats at the lay (the curvatures over W,
the dispersion's measure), at the file's strengths and with every chosen strength read as 1.

Whole numbers only; Rule3's carry the one division (every remainder printed); comparisons only in the reading. The
period N and its primes are THIRD7's numbers, checked here (L^N = I and L^(N/p) != I), not found by a search.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TREE = HERE.parent.joinpath("tree")
sys.path.insert(0, str(TREE.joinpath("src")))

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.runner import files, load, plans  # noqa: E402


def matmul(x, y, m):
    out = []
    for i in range(len(x)):
        row = []
        for j in range(len(y[0])):
            s = 0
            for k in range(len(y)):
                s = s + x[i][k] * y[k][j]
            if m:
                _, s = carry(s, m, 0)
            row.append(s)
        out.append(row)
    return out


def matpow(x, n, m):
    """x^n modulo m by squares: the exponent's binary digits read by Rule3's carry at the senses."""
    unit = [[int(i == j) for j in range(len(x))] for i in range(len(x))]
    result, base = unit, [[e for e in r] for r in x]
    while n:
        n, bit = carry(n, SENSES, 0)
        if bit:
            result = matmul(result, base, m)
        base = matmul(base, base, m)
    return result


def is_unit(x, m):
    return all(carry(x[i][j] - int(i == j), m, 0)[1] == 0 for i in range(len(x)) for j in range(len(x)))


def main() -> None:
    folder = TREE.joinpath("examples", "tensor24-click")
    universe = json.loads(folder.joinpath("universe.json").read_text())
    piece = json.loads(folder.joinpath("piece.json").read_text())
    setting = json.loads(folder.joinpath("setting.json").read_text())
    spokes = files.star(len(piece["shape"]))
    global SENSES
    SENSES, _ = carry(len(spokes), len(piece["shape"]), 0)
    turned, c, square, lifted = tmain.made(spokes)
    loaded, laid = load.load(universe, setting, files.sites_of(piece["shape"]), turned, c, square, lifted)
    trains = loaded.trains
    names = [t["name"] for t in universe["trains"]]
    factor, legs = loaded.potential
    row, of, _, _, _ = plans.rows_of(trains)
    trained = {int(r): int(t) for r, t in zip(row, of)}
    joined = {}
    for m in range(len(factor)):
        if factor[m] == 0:
            continue
        ts = sorted({trained[int(leg[m])] for leg in legs if int(leg[m]) >= 0})
        for i in range(len(ts)):
            for j in range(i + 1, len(ts)):
                joined.setdefault((ts[i], ts[j]), []).append(m)
    edges = sorted(joined)
    print("live monomials:", sum(1 for f in factor if f != 0), "| pairs of trains a live monomial joins:")
    for e in edges:
        print(f"  {names[e[0]]} - {names[e[1]]}: {len(joined[e])} live monomials")
    verts = sorted({t for e in edges for t in e})
    tris = [(i, j, k) for i in verts for j in verts for k in verts
            if i < j < k and (i, j) in joined and (i, k) in joined and (j, k) in joined]
    print("clocks joined:", [names[v] for v in verts], "| triangles:", [[names[v] for v in t] for t in tris])

    # B (V x E): +1 at an edge's lower end, -1 at its higher; C (E x F): [j,k] - [i,k] + [i,j]
    B = [[int(v == e[0]) - int(v == e[1]) for e in edges] for v in verts]
    C = [[int(e == (j, k)) - int(e == (i, k)) + int(e == (i, j)) for (i, j, k) in tris] for e in edges]
    BC = matmul(B, C, 0)
    K = matmul([list(col) for col in zip(*C)], C, 0)
    BtB = matmul([list(col) for col in zip(*B)], B, 0)
    CCt = matmul(C, [list(col) for col in zip(*C)], 0)
    print("B C:", BC, "| K = C^T C:", K)
    print("B^T B + C C^T:", [[BtB[i][j] + CCt[i][j] for j in range(len(edges))] for i in range(len(edges))])
    k3 = K[0][0]
    lap = matmul(B, [list(col) for col in zip(*B)], 0)  # the clocks' Laplacian B B^T
    degree = [sum(abs(x) for x in r) for r in B]
    adj = [[degree[i] * int(i == j) - lap[i][j] for j in range(len(verts))] for i in range(len(verts))]
    shifted = [[lap[i][j] - k3 * int(i == j) for j in range(len(verts))] for i in range(len(verts))]
    print("Laplacian B B^T:", lap, "| trace", sum(lap[i][i] for i in range(len(verts))),
          "| L (L - K I):", matmul(lap, shifted, 0))
    d0 = degree[0]
    a_minus = [[adj[i][j] - d0 * int(i == j) for j in range(len(verts))] for i in range(len(verts))]
    a_plus = [[adj[i][j] + int(i == j) for j in range(len(verts))] for i in range(len(verts))]
    print("adjacency:", adj, "| degree", degree, "| (A - degree I)(A + I):", matmul(a_minus, a_plus, 0))

    # the third click's palindrome at K: (i) eta += K tau, then tau += K eta; (iii) the same in reverse order
    s1 = [[1, 0], [k3, 1]]
    s2 = [[1, k3], [0, 1]]
    L = matmul(matmul(matmul(s1, s2, 0), s2, 0), s1, 0)
    tr = L[0][0] + L[1][1]
    det = L[0][0] * L[1][1] - L[0][1] * L[1][0]
    L2 = matmul(L, L, 0)
    print("\nthe palindrome L at K:", L, "| trace", tr, "| det", det,
          "| L^2 - trace L + I:", [[L2[i][j] - tr * L[i][j] + int(i == j) for j in range(2)] for i in range(2)])
    disc = tr * tr - SENSES * SENSES * det
    rad = k3 * k3 + det  # (K + r(K^2+1))^2 = (2K^2+1) + 2K r(K^2+1)
    print("discriminant trace^2 - 4:", disc, "= (4K)^2 x", rad, ":", disc == (SENSES * SENSES * k3) ** SENSES * rad)
    unit2 = (k3 * k3 + rad, SENSES * k3)
    print(f"(K + r{rad})^2 = {unit2[0]} + {unit2[1]} r{rad}: the eigenvalue (trace/2 + 2K r{rad}):",
          unit2[0] * SENSES == tr, "| norm of K + r:", k3 * k3 - rad)
    print("hyperbolic (no rotation angle, no beat): trace^2 > 4:", tr * tr > SENSES * SENSES)
    # its fourth power of the unit, and two products of the structure's counts, printed as structure numbers
    u4 = (unit2[0] * unit2[0] + rad * unit2[1] * unit2[1], SENSES * unit2[0] * unit2[1])
    print(f"(K + r{rad})^4 = {u4[0]} + {u4[1]} r{rad}; {u4[1]}^2 x {rad} = {u4[1] * u4[1] * rad} against {u4[0]}^2 ="
          f" {u4[0] * u4[0]}: so it lies between {u4[0] * SENSES - 1} and {u4[0] * SENSES}")
    lifts = len(lifted.whole.t1.reshape(-1, len(piece['shape']), len(piece['shape'])))
    print("lifts x trace:", lifts, "x", tr, "=", lifts * tr, "| lifts^2:", lifts * lifts)

    # the triangle's dial 3D from the file's key, through the loader's edge key
    _, _, key = loaded.click
    sides = sorted({int(x) for x in np.asarray(key).reshape(-1)})
    D = sides[0]
    dial = k3 * D
    print("\nthe file's key:", universe["chosen"]["key"], "| every side's key (one value):", sides,
          "| the triangle's dial K D:", dial)
    e3, rest3 = 0, dial
    while carry(rest3, k3, 0)[1] == 0:
        rest3, _ = carry(rest3, k3, 0)
        e3 = e3 + 1
    p3 = k3 ** e3
    print(f"the dial = {k3}^{e3} x {rest3}")
    print(f"L^({k3}^{e3 - 1}) = I mod {p3}:", is_unit(matpow(L, k3 ** (e3 - 1), p3), p3),
          f"| L^({k3}^{e3 - 2}) = I mod {p3}:", is_unit(matpow(L, k3 ** (e3 - 2), p3), p3))
    N, primes = 528480, (2, 3, 5, 367)  # THIRD7's period and its primes, checked here
    prod, n = 1, N
    exps = []
    for p in primes:
        e = 0
        while carry(n, p, 0)[1] == 0:
            n, _ = carry(n, p, 0)
            e = e + 1
        exps.append(e)
        prod = prod * p ** e
    print("THIRD7's N:", N, "= product of", list(zip(primes, exps)), ":", prod == N and n == 1)
    print("L^N = I mod the dial:", is_unit(matpow(L, N, dial), dial))
    for p in primes:
        q, r = carry(N, p, 0)
        print(f"  L^(N/{p}) = I mod the dial: {is_unit(matpow(L, q, dial), dial)} (remainder {r})")
    m9, r9 = carry(N, k3 ** (e3 - 1), 0)
    print(f"the cofactor {rest3}: L^(N/{k3 ** (e3 - 1)}) = L^{m9} = I mod it:", is_unit(matpow(L, m9, rest3), rest3),
          [(p, is_unit(matpow(L, carry(m9, p, 0)[0], rest3), rest3)) for p in (2, 5, 367)])

    # the board's beats at the lay: each curvature over W (the dispersion's measure), from the files' numbers
    grip, W = load.teeth(universe, spokes)
    gamma = universe["integers"]["full_rate"]
    f, fr = carry(W, gamma, 0)
    ch = universe["chosen"]
    a = loaded.state[0]
    held = [t for t in range(len(trains)) if trains.held[t]]
    tied = [t for t in range(len(trains)) if trains.tied[t]]

    def sq(t):
        lo, hi = int(trains.first[t]), int(trains.first[t] + trains.size[t])
        return sum(int(a[r][0]) * int(a[r][0]) for r in range(lo, hi))

    k2 = sum(sq(t) for t in held)
    x2 = sum(sq(t) for t in tied)
    print("\nW (rest):", W, "| Gamma:", gamma, "| f = W div Gamma:", f, "(remainder", fr, ")",
          "| hold, spring, tie:", ch["hold"], ch["spring"], ch["tie"])
    print("held trains:", [names[t] for t in held], "| tied trains:", [names[t] for t in tied],
          "| at Node-clock 0: |k|^2 =", k2, "| |x|^2 over the tied =", x2)
    c_ = ch["hold"] * f
    kh = SENSES * ch["spring"] + SENSES * c_ * x2
    kt = SENSES * c_ * k2
    plus, minus = kt + ch["tie"], kt - ch["tie"]
    print("held curvature 2 spring + 2 c |x|^2:", kh, "| per mille of the explicit window 4W:",
          carry(1000 * kh, SENSES * SENSES * W, 0))
    print("tied curvature 2 c |k|^2:", kt, "| the hands' tie splits it:", plus, "and", minus,
          "| their ratio:", carry(plus, minus, 0))
    print("held over the slow tied mode, curvatures:", carry(kh, minus, 0))
    print("the polarized step's multiplier on the held spring alone, cos = W / (W + spring):", W, "/", W + ch["spring"])
    one = 1
    kh1, kt1 = SENSES * one, SENSES * one * f * k2
    print("every chosen strength read as 1 (a reading, no world): the held spring's curvature", kh1,
          "| the tied curvature 2 f |k|^2:", kt1, "| their ratio f |k|^2:", carry(kt1, kh1, 0),
          "| = Spokes x den x Gamma x |k|^2:", len(spokes) * universe["integers"]["den"] * gamma * k2)


if __name__ == "__main__":
    SENSES = 0
    main()
