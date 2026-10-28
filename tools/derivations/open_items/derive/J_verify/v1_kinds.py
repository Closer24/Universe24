"""J_verify v1: Schur and Frobenius-Schur on all eight kinds of 2O, exact over the Gaussian integers.

python3 -I v1_kinds.py           (must end with 0 failures)
python3 -I v1_kinds.py mutants   (each mutant must fail)

Every kind is given by integer generators g_a (a = x, y, z), the lifts of the three quarter turns,
scaled so the entries are Gaussian integers: g_a = s U_a with s s = 2 on the spinor kinds, s = 1 otherwise.
  A1: 1      A2: -1      E: the axis permutation on the root lattice (x - y, y - z)
  T1: R_a    T2: -R_a    E1/2: Q_a = 1 + H_a    E5/2: -Q_a    G3/2: Q_a (x) P_a
Checks per kind: the projective closure's order; z = g^4 / s^4; the commutant (absolutely irreducible);
the invariant bilinear forms g^T B g = s s B (total, symmetric, antisymmetric); nu = (1/|G|) SUM chi(g g);
nu = chi(z)/dim. Then G3/2 in orthonormal coordinates inside E1/2 (x) T1 with T = T_twin (x) K.
Integers only; no float.
"""
import sys
import random
from itertools import product

RNG = random.Random(20261028)
FAIL = []


def check(name, ok, info=""):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + (f": {info}" if info != "" else ""))


Z0, ONE, I1 = (0, 0), (1, 0), (0, 1)


def gm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ga(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gneg(a):
    return (-a[0], -a[1])


def gc(a):
    return (a[0], -a[1])


def gk(k, a):
    return (k * a[0], k * a[1])


def mm(A, B):
    n, m, p = len(A), len(B), len(B[0])
    out = []
    for i in range(n):
        row = []
        for j in range(p):
            s = Z0
            for k in range(m):
                s = ga(s, gm(A[i][k], B[k][j]))
            row.append(s)
        out.append(row)
    return out


def tr(A):
    return [list(r) for r in zip(*A)]


def ident(n):
    return [[ONE if i == j else Z0 for j in range(n)] for i in range(n)]


def kron(A, B):
    return [[gm(A[i // len(B)][j // len(B)], B[i % len(B)][j % len(B)]) for j in range(len(A) * len(B))] for i in range(len(A) * len(B))]


def scal(k, A):
    return [[gk(k, x) for x in r] for r in A]


def real(M):
    return [[(x, 0) for x in r] for r in M]


# --- rank over Q(i) by fraction-free elimination over Z[i] -----------------------------------------------------
def rank(rows):
    rows = [list(r) for r in rows if any(x != Z0 for x in r)]
    if not rows:
        return 0
    ncol = len(rows[0])
    r = 0
    for c in range(ncol):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] != Z0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        p = rows[r][c]
        for i in range(len(rows)):
            if i != r and rows[i][c] != Z0:
                f = rows[i][c]
                rows[i] = [ga(gm(p, rows[i][j]), gneg(gm(f, rows[r][j]))) for j in range(ncol)]
                # keep the numbers small: divide by the common rational content
                from math import gcd
                g = 0
                for x in rows[i]:
                    g = gcd(g, gcd(abs(x[0]), abs(x[1])))
                if g > 1:
                    rows[i] = [(x[0] // g, x[1] // g) for x in rows[i]]
        r += 1
        if r == len(rows):
            break
    return r


def nullity_bilinear(gens, s2, extra=None):
    """dim of {B : g^T B g = s2 B for every generator} (with optional symmetry rows)."""
    n = len(gens[0])
    rows = []
    for g in gens:
        for i in range(n):
            for j in range(n):
                row = []
                for k in range(n):
                    for l in range(n):
                        v = gm(g[k][i], g[l][j])
                        if k == i and l == j:
                            v = ga(v, (-s2, 0))
                        row.append(v)
                rows.append(row)
    if extra == "sym" or extra == "alt":
        sg = -1 if extra == "sym" else 1
        for k in range(n):
            for l in range(n):
                row = [Z0] * (n * n)
                row[k * n + l] = ga(row[k * n + l], ONE)
                row[l * n + k] = ga(row[l * n + k], (sg, 0))
                if any(x != Z0 for x in row):
                    rows.append(row)
    return n * n - rank(rows)


def nullity_hom(gV, gW):
    """dim of {X (dim W x dim V) : X gV = gW X for every generator pair}."""
    nV, nW = len(gV[0]), len(gW[0])
    rows = []
    for A, Bm in zip(gV, gW):
        for i in range(nW):
            for j in range(nV):
                row = [Z0] * (nW * nV)
                for k in range(nV):  # (X A)_ij = SUM_k X_ik A_kj
                    row[i * nV + k] = ga(row[i * nV + k], A[k][j])
                for k in range(nW):  # (B X)_ij = SUM_k B_ik X_kj
                    row[k * nV + j] = ga(row[k * nV + j], gneg(Bm[i][k]))
                rows.append(row)
    return nW * nV - rank(rows)


# --- the canonical projective element (M, k): U = M / sqrt2^k, k minimal at its parity -------------------------
def reduce(M, k):
    while k >= 2 and all(x[0] % 2 == 0 and x[1] % 2 == 0 for r in M for x in r):
        M = [[(x[0] // 2, x[1] // 2) for x in r] for r in M]
        k -= 2
    return M, k


def key(M, k):
    return (k, tuple(x for r in M for x in r))


def closure(gens, spinor):
    n = len(gens[0])
    start = (ident(n), 0)
    seen = {key(*start): start}
    frontier = [start]
    while frontier:
        nxt = []
        for M, k in frontier:
            for g in gens:
                M2, k2 = reduce(mm(M, g), k + (1 if spinor else 0))
                kk = key(M2, k2)
                if kk not in seen:
                    seen[kk] = (M2, k2)
                    nxt.append((M2, k2))
        frontier = nxt
    return list(seen.values())


def trace(M):
    s = Z0
    for i in range(len(M)):
        s = ga(s, M[i][i])
    return s


# --- the generators --------------------------------------------------------------------------------------------
H = {"x": [[Z0, (0, -1)], [(0, -1), Z0]], "y": [[Z0, (-1, 0)], [(1, 0), Z0]], "z": [[(0, -1), Z0], [Z0, (0, 1)]]}
Q = {a: [[ga(ident(2)[i][j], H[a][i][j]) for j in range(2)] for i in range(2)] for a in "xyz"}
R = {"x": [[1, 0, 0], [0, 0, -1], [0, 1, 0]], "y": [[0, 0, 1], [0, 1, 0], [-1, 0, 0]], "z": [[0, -1, 0], [1, 0, 0], [0, 0, 1]]}


def axis_perm(Rm):
    """the unsigned permutation of the three axes, as a 3x3 0/1 matrix."""
    return [[abs(Rm[i][j]) for j in range(3)] for i in range(3)]


def on_roots(P3):
    """P3 acting on the sum-zero plane, in the basis e1 = x - y, e2 = y - z: w = w1 e1 + (w1 + w2) e2."""
    cols = []
    for e in ((1, -1, 0), (0, 1, -1)):
        w = [sum(P3[i][j] * e[j] for j in range(3)) for i in range(3)]
        cols.append((w[0], w[0] + w[1]))
    return [[cols[j][i] for j in range(2)] for i in range(2)]


P = {a: on_roots(axis_perm(R[a])) for a in "xyz"}


def kinds():
    K = {}
    K["A1"] = ([[[ONE]] for a in "xyz"], False)
    K["A2"] = ([[[(-1, 0)]] for a in "xyz"], False)
    K["E"] = ([real(P[a]) for a in "xyz"], False)
    K["T1"] = ([real(R[a]) for a in "xyz"], False)
    K["T2"] = ([scal(-1, real(R[a])) for a in "xyz"], False)
    K["E1/2"] = ([Q[a] for a in "xyz"], True)
    K["E5/2"] = ([scal(-1, Q[a]) for a in "xyz"], True)
    K["G3/2"] = ([kron(Q[a], real(P[a])) for a in "xyz"], True)
    return K


def main():
    print("0. The lifts: Q_a H_b Q_a^dagger = 2 SUM_c (R_a)_cb H_c (each Q_a lies over the quarter turn R_a)")
    ok = 0
    for a in "xyz":
        Qd = [[gc(Q[a][j][i]) for j in range(2)] for i in range(2)]
        for bi, b in enumerate("xyz"):
            lhs = mm(mm(Q[a], H[b]), Qd)
            rhs = [[Z0, Z0], [Z0, Z0]]
            for ci, c in enumerate("xyz"):
                rhs = [[ga(rhs[i][j], gk(2 * R[a][ci][bi], H[c][i][j])) for j in range(2)] for i in range(2)]
            ok += lhs == rhs
    check("covering relation", ok == 9, f"{ok} of 9")

    print("1. The eight kinds: closure, z, commutant, invariant bilinear forms, Frobenius-Schur, nu = chi(z)/dim")
    K = kinds()
    dims = {}
    expect_order = {"A1": 1, "A2": 2, "E": 6, "T1": 24, "T2": 24, "E1/2": 48, "E5/2": 48, "G3/2": 48}
    for name, (gens, spinor) in K.items():
        n = len(gens[0])
        dims[name] = n
        s2 = 2 if spinor else 1
        G = closure(gens, spinor)
        # z: g_a^4 / s^4
        M4 = mm(mm(gens[2], gens[2]), mm(gens[2], gens[2]))
        Mz, kz = reduce(M4, 4 if spinor else 0)
        zsign = None
        if kz == 0 and Mz == ident(n):
            zsign = +1
        elif kz == 0 and Mz == scal(-1, ident(n)):
            zsign = -1
        comm = nullity_hom(gens, gens)
        tot = nullity_bilinear(gens, s2)
        sym = nullity_bilinear(gens, s2, "sym")
        alt = nullity_bilinear(gens, s2, "alt")
        # Frobenius-Schur over the closure: chi(g g) = trace(M M) / 2^k
        fs_num = (0, 0)
        exact = True
        for M, k in G:
            t = trace(mm(M, M))
            d = 2 ** k
            if t[0] % d or t[1] % d:
                exact = False
            fs_num = ga(fs_num, (t[0] // d, t[1] // d))
        nu_ok = exact and fs_num[1] == 0 and fs_num[0] % len(G) == 0
        nu = fs_num[0] // len(G) if nu_ok else None
        print(f"    {name:5s} dim {n}: |image| {len(G)}, z = {zsign:+d}, commutant {comm}, invariant bilinears {tot} (sym {sym}, alt {alt}), nu = {nu}")
        check(f"{name}: image order {expect_order[name]}", len(G) == expect_order[name], len(G))
        check(f"{name}: absolutely irreducible (commutant 1)", comm == 1, comm)
        check(f"{name}: exactly one invariant bilinear form (Schur)", tot == 1, tot)
        check(f"{name}: it is symmetric iff nu = +1, antisymmetric iff nu = -1 (sym - alt = nu)", nu is not None and sym - alt == nu and sym + alt == 1, f"sym {sym}, alt {alt}, nu {nu}")
        check(f"{name}: nu = chi(z)/dim = z (E's big law on 2O)", nu == zsign, f"nu {nu}, z {zsign}")
    tot48 = sum(d * d for d in dims.values())
    check("sum of dim^2 over the eight kinds = 48 = |2O|", tot48 == 48, tot48)
    print("2. The eight kinds are pairwise distinct (Hom = 0 between kinds of one z; kinds of different z differ by z)")
    names = list(K)
    bad = 0
    pairs = 0
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            if K[a][1] != K[b][1]:
                continue
            pairs += 1
            bad += nullity_hom(K[a][0], K[b][0]) != 0
    check("Hom(V, W) = 0 for every pair of distinct kinds of one z", bad == 0, f"{pairs - bad} of {pairs} pairs")

    print("3. G3/2 in orthonormal coordinates: the kernel of psi -> SUM_a H_a psi_a inside E1/2 (x) T1, T = T_twin (x) K")
    gens6 = [kron(Q[a], real(R[a])) for a in "xyz"]  # index (s, a) -> 3 s + a
    # the contraction C : C^6 -> C^2, (C psi)_s = SUM_a SUM_t H_a[s][t] psi_(t, a)
    C = [[H["xyz"[c % 3]][s][c // 3] for c in range(6)] for s in range(2)]
    # C intertwines: C g6 = Q C
    okC = all(mm(C, gens6[i]) == mm(Q["xyz"[i]], C) for i in range(3))
    check("C is an intertwiner E1/2 (x) T1 -> E1/2 (C g = Q C)", okC)
    # kernel basis: solve C v = 0 by brute force over a small box, keep 4 independent vectors
    basis = []
    for v in product([(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)], repeat=6):
        if all(x == Z0 for x in v):
            continue
        col = [[x] for x in v]
        if mm(C, col) == [[Z0], [Z0]] and rank([list(b) for b in basis] + [list(v)]) == len(basis) + 1:
            basis.append(v)
        if len(basis) == 4:
            break
    check("the kernel (G3/2) is 4-dimensional", len(basis) == 4 and rank([list(b) for b in basis]) == 4, len(basis))

    def T6(u):
        # T_twin on each axis's twin hand: (u0, u1) -> (-conj u1, conj u0); index 3 s + a
        out = [Z0] * 6
        for a in range(3):
            out[0 * 3 + a] = gneg(gc(u[1 * 3 + a]))
            out[1 * 3 + a] = gc(u[0 * 3 + a])
        return out

    def ip(u, v):
        s = Z0
        for x, y in zip(u, v):
            s = ga(s, gm(gc(x), y))
        return s

    def B6(u, v):
        return ip(T6(u), v)

    def apply(M, u):
        return [sum_g([gm(M[i][j], u[j]) for j in range(len(u))]) for i in range(len(M))]

    def sum_g(xs):
        s = Z0
        for x in xs:
            s = ga(s, x)
        return s

    def rv(n, k=4):
        return [(RNG.randint(-k, k), RNG.randint(-k, k)) for _ in range(n)]

    def comb(cs):
        return [sum_g([gm(c, b[i]) for c, b in zip(cs, basis)]) for i in range(6)]

    inv = sym = lin = tt = 0
    N = 300
    for _ in range(N):
        u, v = comb(rv(4)), comb(rv(4))
        c = (RNG.randint(-4, 4), RNG.randint(-4, 4))
        inv += all(B6(apply(g, u), apply(g, v)) == gk(2, B6(u, v)) for g in gens6)
        sym += B6(v, u) == gneg(B6(u, v))
        lin += B6([gm(c, x) for x in u], v) == gm(c, B6(u, v)) and B6(u, [gm(c, x) for x in v]) == gm(c, B6(u, v))
        tt += T6(T6(u)) == [gneg(x) for x in u]
    check("on G3/2, B = <T u, v> is directionless (B(g u, g v) = s s B(u, v) for the three lifts)", inv == N, f"{inv} of {N}")
    check("on G3/2, B is bilinear (linear in u through T's antilinearity, linear in v)", lin == N, f"{lin} of {N}")
    check("on G3/2, B(v, u) = (T T) B(u, v) with T T = -1", sym == N and tt == N, f"{sym} of {N}, T T = -1 on {tt} of {N}")
    gram = [[B6(list(b1), list(b2)) for b2 in basis] for b1 in basis]
    check("on G3/2, B restricted to the kernel is nondegenerate (rank 4)", rank(gram) == 4, rank(gram))
    t_keeps = all(mm(C, [[x] for x in T6(list(b))]) == [[Z0], [Z0]] for b in basis)
    check("T keeps the G3/2 kernel", t_keeps)
    n6 = nullity_bilinear(gens6, 2)
    a6 = nullity_bilinear(gens6, 2, "alt")
    check("E1/2 (x) T1 = E1/2 + G3/2 holds exactly 2 invariant bilinears, both antisymmetric", n6 == 2 and a6 == 2, f"{n6} total, {a6} antisymmetric")

    print("4. The coordinate caveat: on E in the root coordinates, <K u, v> (the plain dot) is not directionless")
    gensE = [real(P[a]) for a in "xyz"]
    fails = sum(mm(tr(g), g) != ident(2) for g in gensE)
    check("plain dot on E's root coordinates fails the 24 on some lift (so <,> must be the 24's own product)", fails > 0, f"{fails} of 3 lifts break it")


def mutants():
    bad = []

    def rep(name, cond, info):
        print(f"  {name}: {info} ({'fails as it must' if cond else 'did not fail'})")
        if not cond:
            bad.append(name)

    K = kinds()
    print("M1. G3/2 built without its E factor (Q_a (x) 1, two copies of E1/2): Schur's one form must break")
    gw = [kron(Q[a], ident(2)) for a in "xyz"]
    comm = nullity_hom(gw, gw)
    tot = nullity_bilinear(gw, 2)
    rep("G3/2 without E", comm != 1 and tot != 1, f"commutant {comm}, invariant bilinears {tot}")
    print("M1b. (kept as a note) the x and y labels of E's axis map exchanged is an inner automorphism of S3: same kind, not a mutant")
    Pw = {"x": P["y"], "y": P["x"], "z": P["z"]}
    gw2 = [kron(Q[a], real(Pw[a])) for a in "xyz"]
    print(f"  relabelled G3/2: commutant {nullity_hom(gw2, gw2)}, image {len(closure(gw2, True))}, Hom to G3/2 {nullity_hom(gw2, K['G3/2'][0])} (isomorphic, as it must be)")
    print("M2. The spinor scale dropped (s s = 1 in place of 2): no invariant bilinear on E1/2")
    n = nullity_bilinear(K["E1/2"][0], 1)
    rep("scale 1 on E1/2", n == 0, f"{n} invariant bilinears")
    print("M3. The symmetric constraint on E1/2's form: none survives (the det is antisymmetric)")
    n = nullity_bilinear(K["E1/2"][0], 2, "sym")
    rep("symmetric invariant on E1/2", n == 0, f"{n} symmetric invariant bilinears")
    print("M4. G3/2 with K in place of T (no sigma_y): B'(u, v) = SUM u v is not directionless")
    gens6 = [kron(Q[a], real(R[a])) for a in "xyz"]
    fails = sum(mm(tr(g), g) != scal(2, ident(6)) for g in gens6)
    rep("plain bilinear on E1/2 (x) T1", fails > 0, f"{fails} of 3 lifts break it")
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)
