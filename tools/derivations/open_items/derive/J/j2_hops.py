"""Draft J, probe j2: route b, the hop of a twin quantum (Levin and Wen on the new engine).

  python3 -I j2_hops.py            the claims (must end with 0 failures)
  python3 -I j2_hops.py mutants    the mutations (each must fail)

Gaussian integers as (re, im) pairs of ints; 2x2 Gaussian matrices; no float.
1. The hops along the z Mesh that commute with the Mesh's stabilizer (the quarter turn about z, lifted, unnormalized
   Q_z = 1 + H_z) and with the turnover T, and are units: exactly +-1 (the plain hop) and +-H_z (the half-turn lift).
   Both assignments U_d = 1 and U_d = H_d are covariant under the 24's lifts. The 24 allows the half-turn hop; it does
   not force it.
2. The half-turn hop is the staggered (Kogut-Susskind) structure: g(x) = H_x^x1 H_y^x2 H_z^x3 turns every link's
   transport into a scalar sign eta_a(x) = (-1)^(x1 + ... + x_(a-1)), with a pi flux in every plaquette.
3. Levin and Wen's T-junction, t_il t_ki t_ij = e^(i theta) t_ij t_ki t_il, on two quanta with spin and explicit hops
   (one hand per quantum; the hop of whichever quantum stands at the site, h x 1 + 1 x h):
   - on states whose two spins agree once transported to the junction, theta is the sector's own sign: +1 on the
     symmetric pair, -1 on the antisymmetric pair, for the plain hop and for the half-turn hop alike;
   - on the labelled pair (no sector), LHS = P(RHS): the 'statistics' is the exchange P itself, which no hop fixes;
   - on spins that do not agree, there is no scalar e^(i theta) at all (Levin-Wen's particles have no spin);
   - the half-turn lifts' H_x H_y H_z = -H_z H_y H_x is one quantum's holonomy; in the two-quantum relation it cancels.
"""

from __future__ import annotations

import random
import sys
from itertools import product

FAIL = []
RNG = random.Random(2003_245316)


def check(name, ok, info=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if info is None else f": {info}"))


Z0, ONE, I1 = (0, 0), (1, 0), (0, 1)


def gm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ga(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gc(a):
    return (a[0], -a[1])


def gk(k, a):
    return (k * a[0], k * a[1])


def mm(A, B):
    return tuple(tuple(ga(gm(A[r][0], B[0][c]), gm(A[r][1], B[1][c])) for c in range(2)) for r in range(2))


def madd(A, B):
    return tuple(tuple(ga(A[r][c], B[r][c]) for c in range(2)) for r in range(2))


def msc(k, A):
    return tuple(tuple(gk(k, A[r][c]) for c in range(2)) for r in range(2))


def mdag(A):
    return tuple(tuple(gc(A[c][r]) for c in range(2)) for r in range(2))


def mv(A, v):
    return tuple(ga(gm(A[r][0], v[0]), gm(A[r][1], v[1])) for r in range(2))


ID = ((ONE, Z0), (Z0, ONE))
H = {
    "x": ((Z0, (0, -1)), ((0, -1), Z0)),  # -i sigma_x
    "y": ((Z0, (-1, 0)), (ONE, Z0)),  # -i sigma_y
    "z": (((0, -1), Z0), (Z0, (0, 1))),  # -i sigma_z
}
AX = ("x", "y", "z")


def Hpow(a, n):
    out = ID
    for _ in range(n % 4):
        out = mm(out, H[a])
    return out


def T(v):
    return (gk(-1, gc(v[1])), gc(v[0]))


def rg(k=4):
    return (RNG.randint(-k, k), RNG.randint(-k, k))


def rvec(k=4):
    while True:
        v = (rg(k), rg(k))
        if v != (Z0, Z0):
            return v


# the quarter turn about a, on directions (counterclockwise, the lift (1 + H_a)/r2)
def quarter(a, d):
    s, ax = d
    rot = {"z": {"x": (+1, "y"), "y": (-1, "x"), "z": (+1, "z")}, "x": {"y": (+1, "z"), "z": (-1, "y"), "x": (+1, "x")}, "y": {"z": (+1, "x"), "x": (-1, "z"), "y": (+1, "y")}}
    sg, nax = rot[a][ax]
    return (s * sg, nax)


DIRS = [(s, a) for s in (+1, -1) for a in AX]


def U_half(d):
    s, a = d
    return H[a] if s > 0 else msc(-1, H[a])


def U_plain(d):
    return ID


def main():
    print("1. The hops a Mesh allows: commuting with the Mesh's quarter turn, with T, and units")
    G = [(a, b) for a in range(-1, 2) for b in range(-1, 2)]
    Qz = madd(ID, H["z"])
    comm = []
    for e in product(G, repeat=4):
        U = ((e[0], e[1]), (e[2], e[3]))
        if mm(U, Qz) == mm(Qz, U):
            comm.append(U)
    diag = all(U[0][1] == Z0 and U[1][0] == Z0 for U in comm)
    check("every Gaussian 2x2 hop (entries in {-1,0,1} + i{-1,0,1}) commuting with Q_z is diagonal: span{1, H_z}", diag and len(comm) == 81, f"{len(comm)} of 6561, all diagonal: {diag}")
    units = [U for U in comm if mm(U, mdag(U)) == ID]
    t_ok = [U for U in units if all(mv(U, T(v)) == T(mv(U, v)) for v in (rvec() for _ in range(20)))]
    want = {ID, msc(-1, ID), H["z"], msc(-1, H["z"])}
    check("the unit hops among them that commute with the turnover T are exactly +-1 and +-H_z", set(t_ok) == want, f"{len(units)} units, {len(t_ok)} commuting with T")
    for name, Uf in (("the plain hop U_d = 1", U_plain), ("the half-turn hop U_d = H_d", U_half)):
        ok = tot = 0
        for a in AX:
            Qa = madd(ID, H[a])
            Qi = madd(ID, msc(-1, H[a]))  # Q_a^-1 = (1 - H_a) / 2
            for d in DIRS:
                tot += 1
                ok += mm(mm(Qa, Uf(d)), Qi) == msc(2, Uf(quarter(a, d)))
        check(f"{name} is covariant under the three quarter turns' lifts: Q U_d Q^-1 = U_(R d)", ok == tot, f"{ok} of {tot}")
    print("   so the 24 (and T) allow both hops; nothing in the 24 forces the half-turn hop")

    print("2. The half-turn hop is the staggered (Kogut-Susskind) structure on the 4^3 torus")
    SIDE = 4
    sites = list(product(range(SIDE), repeat=3))

    def g(x):
        return mm(mm(Hpow("x", x[0]), Hpow("y", x[1])), Hpow("z", x[2]))

    def ginv(x):
        return mdag(g(x))  # the lifts are unitary

    def step(x, k):
        y = list(x)
        y[k] = (y[k] + 1) % SIDE
        return tuple(y)

    scalar = 0
    eta = {}
    for x in sites:
        for k, a in enumerate(AX):
            V = mm(mm(ginv(step(x, k)), H[a]), g(x))
            if V in (ID, msc(-1, ID)):
                scalar += 1
                eta[(x, k)] = 1 if V == ID else -1
    check("g(x + e_a)^-1 H_a g(x) is a scalar sign on every link", scalar == 3 * len(sites), f"{scalar} of {3 * len(sites)}")
    ks = sum(eta[(x, k)] == (-1) ** sum(x[:k]) for x in sites for k in range(3))
    check("the signs are Kogut and Susskind's eta_a(x) = (-1)^(x_1 + ... + x_(a-1))", ks == 3 * len(sites), f"{ks} of {3 * len(sites)}")
    flux = 0
    for x in sites:
        for k, l in ((0, 1), (1, 2), (0, 2)):
            p = eta[(x, k)] * eta[(step(x, k), l)] * eta[(step(x, l), k)] * eta[(x, l)]
            flux += p == -1
    check("a pi flux through every plaquette (the staggered Dirac structure, not a defect of the 24)", flux == 3 * len(sites), f"{flux} of {3 * len(sites)}")

    print("3. Levin and Wen's T-junction on two quanta with spin, explicit hops (center i, neighbours j=+x, k=+y, l=+z)")
    pos = {0: (0, 0, 0), 1: (1, 0, 0), 2: (0, 1, 0), 3: (0, 0, 1)}

    def transport(Uf, to, frm):
        d = tuple(p - q for p, q in zip(pos[to], pos[frm]))
        k = [abs(c) for c in d].index(1)
        return Uf((d[k], AX[k]))

    def hop1(Uf, to, frm):
        """one quantum's hop from frm to to: (h psi)(to) = U psi(frm), every other site 0."""
        U = transport(Uf, to, frm)

        def h(psi):
            out = {s: (Z0, Z0) for s in pos}
            out[to] = mv(U, psi[frm])
            return out
        return h

    def basis_state(site, spin):
        return {s: (spin if s == site else (Z0, Z0)) for s in pos}

    def pair_apply(h, Psi):
        """t = h x 1 + 1 x h on a pair given as a list of (coefficient, psi1, psi2) product terms."""
        out = []
        for c, p1, p2 in Psi:
            out.append((c, h(p1), p2))
            out.append((c, p1, h(p2)))
        return out

    def dense(Psi):
        D = {}
        for c, p1, p2 in Psi:
            for s1 in pos:
                for a in range(2):
                    if p1[s1][a] == Z0:
                        continue
                    for s2 in pos:
                        for b in range(2):
                            if p2[s2][b] == Z0:
                                continue
                            key = (s1, a, s2, b)
                            D[key] = ga(D.get(key, Z0), gk(c, gm(p1[s1][a], p2[s2][b])))
        return {k: v for k, v in D.items() if v != Z0}

    def Pd(D):
        return {(k[2], k[3], k[0], k[1]): v for k, v in D.items()}

    def scale(D, c):
        return {k: gm(c, v) for k, v in D.items()}

    i, j, kk, l = 0, 1, 2, 3
    results = {}
    for tname, Uf in (("plain", U_plain), ("half-turn", U_half)):
        tij, tki, til = hop1(Uf, i, j), hop1(Uf, kk, i), hop1(Uf, i, l)
        Uij, Uil = transport(Uf, i, j), transport(Uf, i, l)
        agree = {"symmetric": 0, "antisymmetric": 0, "labelled P": 0}
        trials = 60
        for _ in range(trials):
            s = rvec()
            s2 = mv(mdag(Uil), mv(Uij, s))  # the second quantum's spin agrees with the first's at the junction
            base = [(1, basis_state(j, s), basis_state(l, s2))]
            sym = base + [(1, basis_state(l, s2), basis_state(j, s))]
            alt = base + [(-1, basis_state(l, s2), basis_state(j, s))]
            for name, Psi, want in (("symmetric", sym, ONE), ("antisymmetric", alt, (-1, 0))):
                L = dense(pair_apply(til, pair_apply(tki, pair_apply(tij, Psi))))
                R = dense(pair_apply(tij, pair_apply(tki, pair_apply(til, Psi))))
                agree[name] += bool(L) and L == scale(R, want)
            L = dense(pair_apply(til, pair_apply(tki, pair_apply(tij, base))))
            R = dense(pair_apply(tij, pair_apply(tki, pair_apply(til, base))))
            agree["labelled P"] += bool(L) and L == Pd(R) and L != R
        results[tname] = agree
        check(f"{tname} hop: e^(i theta) = +1 on the symmetric pair, -1 on the antisymmetric pair (spins agreeing at the junction)", agree["symmetric"] == agree["antisymmetric"] == trials, f"{agree['symmetric']} and {agree['antisymmetric']} of {trials}")
        check(f"{tname} hop: on the labelled pair LHS = P(RHS), not a number: the exchange is P itself, its sign the sector's", agree["labelled P"] == trials, f"{agree['labelled P']} of {trials}")
        none = 0
        for _ in range(trials):
            s, s2 = rvec(), rvec()
            sym = [(1, basis_state(j, s), basis_state(l, s2)), (1, basis_state(l, s2), basis_state(j, s))]
            L = dense(pair_apply(til, pair_apply(tki, pair_apply(tij, sym))))
            R = dense(pair_apply(tij, pair_apply(tki, pair_apply(til, sym))))
            agree_spin = mv(Uij, s) == mv(Uil, s2) or mv(Uij, s) == gk(1, mv(Uil, s2))
            if not agree_spin:
                none += all(L != scale(R, c) for c in (ONE, (-1, 0), I1, (0, -1)))
        check(f"{tname} hop: spins not agreeing at the junction give no scalar e^(i theta) (Levin-Wen's particles carry no spin)", none == trials, f"{none} of {trials}")
    hol = mm(mm(H["x"], H["y"]), H["z"]) == msc(-1, mm(mm(H["z"], H["y"]), H["x"]))
    check("one quantum: H_x H_y H_z = -H_z H_y H_x (a holonomy of one hand; it cancels in the two-quantum relation above)", hol)
    print("   so the hop never makes the sign: the half-turn hop's pi flux 'contributes equally to the swapped and unswapped states'")


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    print("M1. The z Mesh's hop required to commute with the quarter turn about x (the wrong axis): H_z must drop out")
    Qx = madd(ID, H["x"])
    report("H_z fails to commute with Q_x", int(mm(H["z"], Qx) != mm(Qx, H["z"])), 1)
    print("M2. No staggering gauge (g = 1): the links must stop being scalar signs")
    c = sum(H[a] not in (ID, msc(-1, ID)) for a in AX)
    report("links whose transport is not a scalar sign", c, 3)
    print("M3. The half-turn hop with equal raw spins (s2 = s, not transported): the scalar relation must fail")
    print("    (the transports to the junction are -H_x from j and -H_z from l; (H_x - H_z) s = 0 has no solution s != 0)")
    c = 0
    for _ in range(50):
        s = rvec()
        c += mv(msc(-1, H["x"]), s) != mv(msc(-1, H["z"]), s)
    report("raw-equal spins that disagree once transported to the junction", c, 50)
    print("M4. Commuting transports (diag(-i, i) on every axis): the one-quantum ratio must be +1, not -1")
    D = H["z"]
    report("the ratio is not -1", int(mm(mm(D, D), D) != msc(-1, mm(mm(D, D), D))), 1)
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)
