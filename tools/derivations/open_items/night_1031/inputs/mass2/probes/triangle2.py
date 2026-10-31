"""MASS2 probe 2: the click world's triangle and the third click's palindrome, from the files through the engine's own
loader (node-all 9d75a4904, mass2/tree). Clock facts only.

- The triangle: which trains the live monomials join pairwise; B, C, K = C^T C; B C; B^T B + C C^T; the clocks'
  Laplacian and adjacency, their spectra by L (L - K I) = 0 and (A - degree I)(A + I) = 0.
- The palindrome L at K: trace, det, L^2 - trace L + I, the unit K + r(K^2 + 1).
- The triangle's dial K D from the file's key through the loader's edge key; its prime factorisation by trial division
  (each divisor tried while its square is at most what is left); for each prime p > 3, Euler's criterion for the
  discriminant's square-free part (its power (p - 1)/2 modulo p) says whether L's order divides p - 1 or p + 1; each
  order certified by L^n = I and L^(n/q) != I for every prime q of n; the order modulo the dial their lcm.
- The Hessian of the loader's own potential at the lay (each monomial's second derivatives, in whole numbers), at the
  file's strengths and with every chosen strength read as 1 (a reading of the files with those numbers set to 1, no
  world): the (held, giver) minor and its determinant; the tied block's own sum and difference.

No product of the structure's numbers is printed for its nearness to anything. Whole numbers only; Rule3's carry the
one division; comparisons only in the reading.
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


def mm(x, y, m):
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


def mpow(x, n, m, two):
    result = [[int(i == j) for j in range(len(x))] for i in range(len(x))]
    base = [list(r) for r in x]
    while n:
        n, bit = carry(n, two, 0)
        if bit:
            result = mm(result, base, m)
        base = mm(base, base, m)
    return result


def ppow(b, e, m, two):
    result, base = 1, carry(b, m, 0)[1]
    while e:
        e, bit = carry(e, two, 0)
        if bit:
            _, result = carry(result * base, m, 0)
        _, base = carry(base * base, m, 0)
    return result


def unit(x, m):
    return all(carry(x[i][j] - int(i == j), m, 0)[1] == 0 for i in range(len(x)) for j in range(len(x)))


def factor(n):
    """n's primes with their powers, by trial division: each divisor tried while its square is at most what is left."""
    out, d = [], 2
    while d * d <= n:
        e = 0
        while carry(n, d, 0)[1] == 0:
            n, _ = carry(n, d, 0)
            e = e + 1
        if e:
            out.append((d, e))
        d = d + 1
    if n > 1:
        out.append((n, 1))
    return out


def order(L, m, n, two):
    """L's order modulo m, given that L^n = I there: n stripped of every prime q while L^(n/q) = I stays."""
    assert unit(mpow(L, n, m, two), m)
    for q, _ in factor(n):
        while carry(n, q, 0)[1] == 0 and unit(mpow(L, carry(n, q, 0)[0], m, two), m):
            n, _ = carry(n, q, 0)
    proper = [unit(mpow(L, carry(n, q, 0)[0], m, two), m) for q, _ in factor(n)]
    return n, proper


def loaded_of(universe, setting, piece):
    spokes = files.star(len(piece["shape"]))
    turned, c, square, lifted = tmain.made(spokes)
    loaded, laid = load.load(universe, setting, files.sites_of(piece["shape"]), turned, c, square, lifted)
    assert not laid, laid
    return loaded, spokes


def hessian(loaded, at):
    """The potential's second derivatives at the counts `at` (one site): SUM over monomials f x the product of the
    other legs over every ordered pair of distinct positions on the two rows."""
    factor_, legs = loaded.potential
    rows = len(at)
    H = [[0] * rows for _ in range(rows)]
    for m in range(len(factor_)):
        f = int(factor_[m])
        if f == 0:
            continue
        ls = [int(leg[m]) for leg in legs]
        for i in range(len(ls)):
            for j in range(len(ls)):
                if i == j or ls[i] < 0 or ls[j] < 0:
                    continue
                rest = 1
                for p in range(len(ls)):
                    if p != i and p != j and ls[p] >= 0:
                        rest = rest * at[ls[p]]
                H[ls[i]][ls[j]] = H[ls[i]][ls[j]] + f * rest
    return H


def main() -> None:
    folder = TREE.joinpath("examples", "tensor24-click")
    universe = json.loads(folder.joinpath("universe.json").read_text())
    piece = json.loads(folder.joinpath("piece.json").read_text())
    setting = json.loads(folder.joinpath("setting.json").read_text())
    loaded, spokes = loaded_of(universe, setting, piece)
    two, _ = carry(len(spokes), len(piece["shape"]), 0)  # the senses of an axis, from the star
    trains = loaded.trains
    names = [t["name"] for t in universe["trains"]]
    factor_, legs = loaded.potential
    row, of, _, _, _ = plans.rows_of(trains)
    trained = {int(r): int(t) for r, t in zip(row, of)}
    joined = {}
    for m in range(len(factor_)):
        if factor_[m] == 0:
            continue
        ts = sorted({trained[int(leg[m])] for leg in legs if int(leg[m]) >= 0})
        for i in range(len(ts)):
            for j in range(i + 1, len(ts)):
                joined.setdefault((ts[i], ts[j]), []).append(m)
    edges = sorted(joined)
    print("live monomials:", sum(1 for f in factor_ if f != 0), "| pairs joined:",
          [(names[a], names[b], len(joined[(a, b)])) for a, b in edges])
    verts = sorted({t for e in edges for t in e})
    tris = [(i, j, k) for i in verts for j in verts for k in verts
            if i < j < k and (i, j) in joined and (i, k) in joined and (j, k) in joined]
    print("clocks joined:", [names[v] for v in verts], "| triangles:", [[names[v] for v in t] for t in tris])
    B = [[int(v == e[0]) - int(v == e[1]) for e in edges] for v in verts]
    C = [[int(e == (j, k)) - int(e == (i, k)) + int(e == (i, j)) for (i, j, k) in tris] for e in edges]
    tB, tC = [list(x) for x in zip(*B)], [list(x) for x in zip(*C)]
    K = mm(tC, C, 0)
    BtB, CCt = mm(tB, B, 0), mm(C, tC, 0)
    print("B C:", mm(B, C, 0), "| K:", K, "| B^T B + C C^T:",
          [[BtB[i][j] + CCt[i][j] for j in range(len(edges))] for i in range(len(edges))])
    k3 = K[0][0]
    lap = mm(B, tB, 0)
    degree = [sum(x * x for x in r) for r in B]
    adj = [[degree[i] * int(i == j) - lap[i][j] for j in range(len(verts))] for i in range(len(verts))]
    nv = len(verts)
    print("Laplacian:", lap, "trace", sum(lap[i][i] for i in range(nv)), "| L (L - K I):",
          mm(lap, [[lap[i][j] - k3 * int(i == j) for j in range(nv)] for i in range(nv)], 0))
    print("adjacency:", adj, "trace", sum(adj[i][i] for i in range(nv)), "| (A - degree I)(A + I):",
          mm([[adj[i][j] - degree[0] * int(i == j) for j in range(nv)] for i in range(nv)],
             [[adj[i][j] + int(i == j) for j in range(nv)] for i in range(nv)], 0))

    s1, s2 = [[1, 0], [k3, 1]], [[1, k3], [0, 1]]
    L = mm(mm(mm(s1, s2, 0), s2, 0), s1, 0)
    tr, det = L[0][0] + L[1][1], L[0][0] * L[1][1] - L[0][1] * L[1][0]
    L2 = mm(L, L, 0)
    rad = k3 * k3 + det
    print("\nL:", L, "| trace", tr, "| det", det, "| L^2 - trace L + I:",
          [[L2[i][j] - tr * L[i][j] + int(i == j) for j in range(2)] for i in range(2)])
    print(f"trace^2 - 4 det = {tr * tr - two * two * det} = (4K)^2 x {rad}: "
          f"{tr * tr - two * two * det == (two * two * k3) * (two * two * k3) * rad}"
          f" | (K + r{rad})^2 = {k3 * k3 + rad} + {two * k3} r{rad}, the larger eigenvalue: {(k3 * k3 + rad) * two == tr}"
          f" | the unit's norm K^2 - {rad} = {k3 * k3 - rad} | trace^2 > 4: hyperbolic, no rotation angle: {tr * tr > two * two}")

    _, _, key = loaded.click
    sides = sorted({int(x) for x in np.asarray(key).reshape(-1)})
    dial = k3 * sides[0]
    print("\nthe file's key:", universe["chosen"]["key"], "= ", factor(universe["chosen"]["key"]),
          "| every side's key:", sides, "| the dial K D:", dial, "=", factor(dial))
    orders = []
    for p, e in factor(dial):
        pe = p ** e
        if unit(L, p):
            # L = I mod p: its order modulo p^e is a power of p, at most p^(e - 1); tried power by power, e at most
            n = 1
            for _ in range(e):
                if unit(mpow(L, n, pe, two), pe):
                    break
                n = n * p
            o, proper = n, [unit(mpow(L, carry(n, q, 0)[0], pe, two), pe) for q, _ in factor(n)]
            print(f"  mod {p}^{e} = {pe}: L = I mod {p}: {unit(L, p)}; order {o} = {factor(o)}; L^(order/q) = I for its"
                  f" primes q: {proper}")
        else:
            half, _ = carry(p - 1, two, 0)
            leg = ppow(rad, half, p, two)
            split = leg == 1
            n = p - 1 if split else p + 1
            o, proper = order(L, pe, n, two)
            print(f"  mod {p}: {rad}^((p-1)/2) = {'+1' if split else ('-1' if leg == p - 1 else leg)} mod p, so "
                  f"{'split' if split else 'inert'}: L^({'p - 1' if split else 'p + 1'}) = I, {n} = {factor(n)};"
                  f" order {o} = {factor(o)}; L^(order/q) = I for its primes q: {proper}")
        orders.append(o)
    total = 1
    for o in orders:
        g, x = total, o
        while x:
            g, x = x, carry(g, x, 0)[1]
        total = carry(total * o, g, 0)[0]
    print(f"the order modulo the dial, the lcm: {total} = {factor(total)} | L^{total} = I mod the dial:"
          f" {unit(mpow(L, total, dial, two), dial)}")

    # the Hessian at the lay, site 0, at the file's strengths and with every chosen strength read as 1
    a0 = [int(x) for x in np.asarray(loaded.state[0])[:, 0]]
    W = load.teeth(universe, spokes)[1]
    held = [t for t in range(len(trains)) if trains.held[t]][0]
    tied = [t for t in range(len(trains)) if trains.tied[t]]
    hr, gr, tr_ = int(trains.first[held]), int(trains.first[tied[0]]), int(trains.first[tied[1]])
    print(f"\nthe lay at site 0: held row {hr} at {a0[hr]}, {names[tied[0]]} row {gr} at {a0[gr]},"
          f" {names[tied[1]]} row {tr_} at {a0[tr_]} | W {W} | 4W {two * two * W}")
    ones = {**universe, "chosen": {**universe["chosen"],
                                   **{k: 1 for k in ("hold", "spring", "tie") if universe["chosen"][k]}}}
    for label, uni in (("the file's strengths", universe), ("every chosen strength read as 1", ones)):
        ld, _ = loaded_of(uni, setting, piece)
        H = hessian(ld, a0)
        hh, hg, gg, gt = H[hr][hr], H[hr][gr], H[gr][gr], H[gr][tr_]
        detm = hh * gg - hg * hg
        print(f"{label}: d2V/dk2 {hh} ({carry(1000 * hh, two * two * W, 0)[0]} per mille of 4W) | d2V/dk dx {hg} |"
              f" d2V/dx2 {gg} | d2V/dx_g dx_t {gt}")
        print(f"  the (held, giver) minor's determinant {detm}: {'indefinite' if detm < 0 else 'definite or flat'}"
              f" | the tied block's sum {gg + gt} and difference {gg - gt}, their carry {carry(gg + gt, gg - gt, 0)}"
              f" | held over tied diagonal {carry(hh, gg, 0)}")
    ld1, _ = loaded_of(ones, setting, piece)
    H1 = hessian(ld1, [0 if i in range(gr, gr + int(trains.size[tied[0]])) else v for i, v in enumerate(a0)])
    print(f"every chosen strength read as 1, the tied counts read at 0 (the held spring's own curvature):"
          f" d2V/dk2 {H1[hr][hr]} | the tied over it at the lay's |k|: {carry(H[gr][gr], H1[hr][hr], 0)}")


if __name__ == "__main__":
    main()
