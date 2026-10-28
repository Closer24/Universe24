"""BC verifier, part 1: Animate's 'Bell through the cone' re-derived with my own integer code.

Independent of bell_cone.py: Gaussian integers as (re, im) int pairs, Rule3 written as an integer quotient
t = (c * total) // room over every draw number c in [0, room), exact odds as Fractions of counts.
Run: python3 -I -B v1_algebra.py
"""
from fractions import Fraction as Fr
from itertools import product
import random

# ---------------- Gaussian integers and twin pairs ----------------
def gm(z, w): return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])
def ga(z, w): return (z[0] + w[0], z[1] + w[1])
def gs(z, w): return (z[0] - w[0], z[1] - w[1])
def gc(z): return (z[0], -z[1])
def gn(z): return z[0] * z[0] + z[1] * z[1]
def neg(z): return (-z[0], -z[1])
def sc(k, u): return (gm(k, u[0]), gm(k, u[1]))          # Gaussian scalar times a twin pair
def lin(n, u, m, v): return (ga(gm(n, u[0]), gm(m, v[0])), ga(gm(n, u[1]), gm(m, v[1])))

def perp(u): return (neg(gc(u[1])), gc(u[0]))
def det(u, v): return gs(gm(u[0], v[1]), gm(u[1], v[0]))
def ovl(u, v): return ga(gm(gc(u[0]), v[0]), gm(gc(u[1]), v[1]))
def rho(u): return gn(u[0]) + gn(u[1])
def axis(u):
    c = gm(gc(u[0]), u[1])
    return (2 * c[0], 2 * c[1], gn(u[0]) - gn(u[1]))
def dot(m, n): return m[0] * n[0] + m[1] * n[1] + m[2] * n[2]
def singletE(u, v): return Fr(-dot(axis(u), axis(v)), rho(u) * rho(v))

def senses(u, P=perp): return {1: u, -1: P(u)}

# ---------------- Rule3 pick over every draw number ----------------
def pick_enum(sizes, room=None):
    """sizes: list of (key, size). Every c in [0, room): t = (c * total) // room (Rule3's quotient);
    the part whose running sum first passes t takes the whole. room defaults to the parts' sum.
    (Brute force over every draw number; used to cross-check pick_counts on small rooms.)"""
    total = sum(s for _, s in sizes)
    if room is None:
        room = total
    counts = {k: 0 for k, _ in sizes}
    for c in range(room):
        t = (c * total) // room
        run = 0
        for k, s in sizes:
            run += s
            if t < run:
                counts[k] += 1
                break
    return counts, room

def cdiv(a, b): return -((-a) // b)

def pick_counts(sizes, room=None):
    """the same counts without the loop over c: part k (running sums lo..hi) takes exactly the draw numbers
    c with lo <= (c * total) // room < hi, i.e. ceil(hi room / total) - ceil(lo room / total) of them."""
    total = sum(s for _, s in sizes)
    if room is None:
        room = total
    counts, lo = {}, 0
    for k, s in sizes:
        hi = lo + s
        counts[k] = cdiv(hi * room, total) - cdiv(lo * room, total)
        lo = hi
    return counts, room

def law6_two(frame, child, P=perp):
    """the detector's own click of a child: parts N<f+,chi>, N<f-,chi>."""
    return [(1, gn(ovl(frame, child))), (-1, gn(ovl(P(frame), child)))]

# ---------------- the route: split at the fitting, children carried, far clicks ----------------
def birth_sizes(fA, fB, P=perp, D=det, size=None):
    sA, sB = senses(fA, P), senses(fB, P)
    out = []
    for a in (1, -1):
        for b in (1, -1):
            d = D(sA[a], sB[b])
            out.append(((a, b), gn(d) if size is None else size(d)))
    return out

def run(fA_fit, fB_fit, fA_clk, fB_clk, P=perp, D=det, size=None, swap=False, flipB=False,
        room=None, k=(3, 2)):
    """returns E, A's marginal P(+), B's marginal P(+), whole-click draws, birth room."""
    sizes = birth_sizes(fA_fit, fB_fit, P, D, size)
    cnt, R = pick_counts(sizes, room)
    sA, sB = senses(fA_fit, P), senses(fB_fit, P)
    E = Fr(0); pa = Fr(0); pb = Fr(0); whole = 0
    for (a, b), n in cnt.items():
        if n == 0:
            continue
        chiA, chiB = sc(k, sA[a]), sc(k, sB[b])
        if swap:
            chiA, chiB = chiB, chiA
        cA, rA = pick_counts(law6_two(fA_clk, chiA, P))
        cB, rB = pick_counts(law6_two(fB_clk, chiB, P))
        if 0 in (cA[1], cA[-1]) and 0 in (cB[1], cB[-1]):
            whole += n
        w = Fr(n, R)
        for x, nx in cA.items():
            for y, ny in cB.items():
                if nx == 0 or ny == 0:
                    continue
                q = w * Fr(nx, rA) * Fr(ny, rB)
                yy = -y if flipB else y
                E += q * x * yy
                pa += q * (x == 1)
                pb += q * (yy == 1)
    return E, pa, pb, whole, R

def chsh(E): return E[0] + E[1] + E[2] - E[3]
PAIRS = [("a", "b"), ("a", "b'"), ("a'", "b"), ("a'", "b'")]
REAL = {"a": ((1, 0), (0, 0)), "a'": ((1, 0), (1, 0)), "b": ((5, 0), (2, 0)), "b'": ((5, 0), (-2, 0))}
CPLX = {"a": ((1, 0), (0, 0)), "a'": ((1, 0), (0, 1)), "b": ((5, 0), (0, 2)), "b'": ((5, 0), (0, -2))}
OTHER = {"a": "a'", "a'": "a", "b": "b'", "b'": "b"}

def S_of(fit, clk, **kw):
    Es, ms, wh = [], [], []
    for x, y in PAIRS:
        E, pa, pb, whole, R = run(fit(x, y)[0], fit(x, y)[1], clk[x], clk[y], **kw)
        Es.append(E); ms.append((pa, pb)); wh.append((whole, R))
    return chsh(Es), Es, ms, wh

def band(s):  # 4 < S^2 <= 8 by integer cross-multiplication
    n, d = s.numerator, s.denominator
    return 4 * d * d < n * n <= 8 * d * d

def show(label, s, Es=None):
    print(f"  {label}: S = {s} ({float(s):+.4f}); |S|>2: {abs(s) > 2}; in 4<S^2<=8: {band(s)}"
          + (f"; E = {[str(e) for e in Es]}" if Es else ""))

def main():
    print("== 0. the fast count against every draw number ==")
    rz = random.Random(5); miss = 0; n0 = 0
    for _ in range(3000):
        sizes = [(i, rz.randint(0, 40)) for i in range(rz.randint(1, 5))]
        if sum(s for _, s in sizes) == 0:
            continue
        room = rz.choice([None, rz.randint(1, 300)])
        n0 += 1
        miss += (pick_counts(sizes, room) != pick_enum(sizes, room))
    print(f"  {n0} random size lists and rooms: counts differ in {miss}")
    print("== A. reproduction (own code) ==")
    for name, ST in (("real (draft D's)", REAL), ("complex (y, z)", CPLX)):
        s, Es, ms, wh = S_of(lambda x, y, ST=ST: (ST[x], ST[y]), ST)
        sing = [singletE(ST[x], ST[y]) for x, y in PAIRS]
        print(f" settings {name}: E = {[str(e) for e in Es]}; singlet {[str(e) for e in sing]}; equal {Es == sing}")
        show("route", s)
        print(f"  S^2 = {s * s}; 8 = {Fr(8 * s.denominator ** 2, s.denominator ** 2)} (as /{s.denominator ** 2})")
        print(f"  whole far clicks (draws): {wh}")
        print(f"  marginals (A+, B+): {[(str(p), str(q)) for p, q in ms]}")
    # no signalling and singlet on random complex frames
    rnd = random.Random(20261028)
    bad_sig = bad_sing = bad_whole = 0
    N = 300
    for _ in range(N):
        fA = tuple((rnd.randint(-9, 9), rnd.randint(-9, 9)) for _ in range(2))
        fB = tuple((rnd.randint(-9, 9), rnd.randint(-9, 9)) for _ in range(2))
        if rho(fA) == 0 or rho(fB) == 0:
            continue
        E, pa, pb, whole, R = run(fA, fB, fA, fB, k=(rnd.randint(1, 5), rnd.randint(-5, 5)))
        bad_sig += (pa != Fr(1, 2)) + (pb != Fr(1, 2))
        bad_sing += (E != singletE(fA, fB))
        bad_whole += (whole != R)
    print(f" random complex frames ({N}): singlet misses {bad_sing}, marginal misses {bad_sig}, non-whole {bad_whole}")

    print("== B. controls: frames at the fitting not the click frames ==")
    s, Es, _, _ = S_of(lambda x, y: (REAL[x], REAL[OTHER[y]]), REAL)
    show("B saw the other B setting (probe's control)", s, Es)
    s, Es, _, _ = S_of(lambda x, y: (REAL[OTHER[x]], REAL[y]), REAL)
    show("A saw the other A setting", s, Es)
    s, Es, _, _ = S_of(lambda x, y: (REAL[OTHER[x]], REAL[OTHER[y]]), REAL)
    show("both saw the other", s, Es)
    # P-f counterexamples: a frame at the fitting that is not the detector's, yet |S| > 2
    s, Es, _, _ = S_of(lambda x, y: (REAL[x], perp(REAL[y])), REAL)
    show("B's frame at the fitting = perp(B's click frame)", s)
    big = {kk: sc((10, 0), v) for kk, v in REAL.items()}
    near = lambda u: (ga(u[0], (0, 1)), u[1])          # one notch off in A's first gear
    s, Es, _, _ = S_of(lambda x, y: (near(big[x]), near(big[y])), big)
    show("frames at the fitting one notch off the click frames (x10)", s)
    # frames at the fitting independent of the click settings: every fixed pair from a grid
    grid = [((p, q), (r, t)) for p, q, r, t in product(range(-1, 2), repeat=4) if (p, q, r, t) != (0, 0, 0, 0)]
    mx = Fr(0); arg = None; cnt = 0
    for gA in grid:
        for gB in grid[::3]:
            s, _, _, _ = S_of(lambda x, y: (gA, gB), REAL)
            cnt += 1
            if abs(s) > mx:
                mx, arg = abs(s), (gA, gB)
    print(f"  fixed fitting frames (independent of the settings), {cnt} pairs: max |S| = {mx} ({float(mx):.4f}) at {arg}")
    # persistence: the fitting's frame is the click frame with probability p per side, else the other setting
    def S_p(p):
        Es = []
        for x, y in PAIRS:
            E = Fr(0)
            for xs, px in ((x, p), (OTHER[x], 1 - p)):
                for ys, py in ((y, p), (OTHER[y], 1 - p)):
                    E += px * py * run(REAL[xs], REAL[ys], REAL[x], REAL[y])[0]
            Es.append(E)
        return chsh(Es)
    for p in (Fr(1), Fr(9, 10), Fr(1, 2), Fr(0)):
        print(f"  persistence p = {p}: S = {S_p(p)} ({float(S_p(p)):+.4f})")
    lo, hi = Fr(1, 2), Fr(1)
    for _ in range(30):
        mid = (lo + hi) / 2
        if abs(S_p(mid)) > 2:
            hi = mid
        else:
            lo = mid
    print(f"  threshold p* (|S| = 2), both sides: {float(lo):.5f}")

    print("== C. mutants ==")
    nosign = lambda u: (gc(u[1]), gc(u[0]))
    noconj = lambda u: (neg(u[1]), u[0])
    plus = lambda u, v: ga(gm(u[0], v[1]), gm(u[1], v[0]))
    same = lambda ST: (lambda x, y: (ST[x], ST[y]))
    for label, ST, kw in (("perp without its sign (real)", REAL, dict(P=nosign)),
                          ("perp without the conjugates (real)", REAL, dict(P=noconj)),
                          ("perp without the conjugates (complex)", CPLX, dict(P=noconj)),
                          ("det with the plus sign (real)", REAL, dict(D=plus)),
                          ("children swapped", REAL, dict(swap=True)),
                          ("B's answer label negated", REAL, dict(flipB=True))):
        s, Es, ms, _ = S_of(same(ST), ST, **kw)
        show(label, s)
        print(f"     marginals A+: {sorted(set(str(p) for p, _ in ms))}, B+: {sorted(set(str(q) for _, q in ms))}")
    for n in (2, 3, 4, 8):
        s, Es, ms, _ = S_of(same(REAL), REAL, size=lambda d, n=n: gn(d) ** n)
        show(f"sizes N(det)^{n} (no-signalling: A+ {sorted(set(str(p) for p, _ in ms))})", s)
    # law 6 on a pair state Psi (2x2 Gaussian tensor) against the product frames
    def psi_sizes(Psi):
        def size_fn(fA, fB):
            sA, sB = senses(fA), senses(fB)
            out = []
            for a in (1, -1):
                for b in (1, -1):
                    amp = (0, 0)
                    for i in range(2):
                        for j in range(2):
                            amp = ga(amp, gm(gm(gc(sA[a][i]), gc(sB[b][j])), Psi[i][j]))
                    out.append(((a, b), gn(amp)))
            return out
        return size_fn
    def S_psi(Psi):
        f = psi_sizes(Psi)
        Es = []
        for x, y in PAIRS:
            sizes = f(REAL[x], REAL[y])
            cnt, R = pick_counts(sizes)
            Es.append(sum(Fr(n, R) * a * b for (a, b), n in cnt.items()))  # far clicks whole: frames equal
        return chsh(Es), Es
    Z, O = (0, 0), (1, 0)
    for label, Psi in (("k eps, k = 1", [[Z, O], [(-1, 0), Z]]),
                       ("k eps, k = 7 - 4i", [[Z, (7, -4)], [(-7, 4), Z]]),
                       ("product up x down", [[Z, O], [Z, Z]]),
                       ("triplet ud + du", [[Z, O], [O, Z]]),
                       ("eps + uu (T1 admixed)", [[O, O], [(-1, 0), Z]]),
                       ("3 eps + uu", [[O, (3, 0)], [(-3, 0), Z]])):
        s, Es = S_psi(Psi)
        show(f"law 6 on the pair state {label}", s)
    # the engine's room is not the parts' sum (draft D's room 5,800, and a small prime)
    for R in (5800, 97):
        Es = []
        for x, y in PAIRS:
            sizes = birth_sizes(REAL[x], REAL[y])
            cnt, RR = pick_counts(sizes, R)
            Es.append(sum(Fr(n, RR) * a * b for (a, b), n in cnt.items()))
        s = chsh(Es)
        print(f"  room {R} (not the parts' sum): S = {s} ({float(s):+.5f}), off the singlet by {float(s + Fr(82, 29)):+.5f}")

    print("== C'. the 24's double cover acting on all frames (P-e) ==")
    els = []
    def qmat(a, b, c, d):  # a + b i + c j + d k, scaled to Gaussian integers
        return [[(a, b), (c, d)], [(-c, d), (a, -b)]]
    for sgn in product((1, -1), repeat=1):
        pass
    units = []
    for i in range(4):
        for s_ in (1, -1):
            v = [0, 0, 0, 0]; v[i] = s_; units.append(v)                  # +-1, +-i, +-j, +-k (scale 1)
    for sg in product((1, -1), repeat=4):
        units.append(list(sg))                                            # (+-1+-i+-j+-k)/2 times 2
    for i in range(4):
        for j in range(i + 1, 4):
            for s1 in (1, -1):
                for s2 in (1, -1):
                    v = [0, 0, 0, 0]; v[i] = s1; v[j] = s2; units.append(v)  # (+-u+-v)/sqrt2 times sqrt2
    mats = [qmat(*v) for v in units]
    def mapply(M, u): return (ga(gm(M[0][0], u[0]), gm(M[0][1], u[1])), ga(gm(M[1][0], u[0]), gm(M[1][1], u[1])))
    def mdet(M): return gs(gm(M[0][0], M[1][1]), gm(M[0][1], M[1][0]))
    badE = badP = 0
    s0 = S_of(same(REAL), REAL)[1]
    for M in mats:
        ST = {kk: mapply(M, v) for kk, v in REAL.items()}
        s, Es, _, _ = S_of(same(ST), ST)
        badE += (Es != s0)
        for v in REAL.values():
            badP += (perp(mapply(M, v)) != mapply(M, perp(v)))
    print(f"  {len(mats)} elements (dets {sorted(set(mdet(M) for M in mats))}): E changed in {badE}; perp(Mu) != M perp(u) in {badP}")

    print("== D. measurement dependence (Hall) ==")
    # the route's lambda = the drawn answer pair: P(ab|xy) = sigma_ab / room
    def Pab(x, y):
        cnt, R = pick_counts(birth_sizes(REAL[x], REAL[y]))
        return {k: Fr(n, R) for k, n in cnt.items()}
    Ms = [sum(abs(Pab(*p)[k] - Pab(*q)[k]) for k in Pab(*p)) for p in PAIRS for q in PAIRS]
    print(f"  route, lambda = answer pair: M = {max(Ms)}; lambda = children's states: supports disjoint, M = 2")
    # Hall's relaxed CHSH S <= 2 + 3M over measurement-dependent mixtures of the 16 deterministic strategies
    strat = list(product((1, -1), repeat=4))  # (a0, a1, b0, b1)
    cxy = {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): -1}
    def S_M(ps):
        S = sum(cxy[xy] * sum(ps[xy][l] * strat[l][xy[0]] * strat[l][2 + xy[1]] for l in range(16)) for xy in cxy)
        M = max(sum(abs(ps[p][l] - ps[q][l]) for l in range(16)) for p in cxy for q in cxy)
        return S, M
    viol = 0; trials = 4000; best = Fr(-9)
    r2 = random.Random(7)
    for _ in range(trials):
        base = [r2.randint(0, 6) for _ in range(16)]
        ps = {}
        for xy in cxy:
            w = [max(0, b + r2.randint(-3, 3) * (r2.random() < 0.3)) for b in base]
            if sum(w) == 0:
                w[0] = 1
            ps[xy] = [Fr(v, sum(w)) for v in w]
        S, M = S_M(ps)
        viol += (S > 2 + 3 * M)
        best = max(best, S - 2 - 3 * M)
    # the tight construction at M = 8/29
    t = Fr(12, 29)
    one_wrong = {}
    for l, (a0, a1, b0, b1) in enumerate(strat):
        terms = {(0, 0): a0 * b0, (0, 1): a0 * b1, (1, 0): a1 * b0, (1, 1): -a1 * b1}
        wrong = [xy for xy in cxy if terms[xy] == -1]
        if len(wrong) == 1:
            one_wrong.setdefault(wrong[0], l)
    q = one_wrong[(1, 1)]
    ps = {}
    for xy in cxy:
        vec = [Fr(0)] * 16
        vec[q] += 1 - t
        for w_, l in one_wrong.items():
            if w_ != xy:
                vec[l] += t / 3
        ps[xy] = vec
    S, M = S_M(ps)
    print(f"  random mixtures {trials}: S > 2 + 3M in {viol} (max S - 2 - 3M = {best})")
    print(f"  tight construction: S = {S}, M = {M}; 2 + 3M = {2 + 3 * M}: Hall's minimum for |S| = 82/29 is M = 8/29")

    print("== E. the cone: A's frame leaves at t_F - d(A,F), B clicks at t_F + d(F,B) ==")
    pts = list(product(range(-2, 3), repeat=3))
    L1 = lambda p, q: sum(abs(i - j) for i, j in zip(p, q))
    spacelike = total = 0
    for F in pts[::7]:
        for A in pts[::5]:
            for B in pts[::3]:
                total += 1
                spacelike += (L1(F, B) + L1(A, F) < L1(A, B))
    print(f"  {total} placements: A's setting event outside B's click's past cone in {spacelike}")

if __name__ == "__main__":
    main()
