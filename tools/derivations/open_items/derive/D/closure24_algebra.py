"""Draft D, the closure of the split: the algebra's checks (DERIVATION.md, part 2). Integers only: Gaussian
integers are pairs of ints, every ratio is compared by cross-multiplication, no float, no Fraction, no root.
Run: python3 -I closure24_algebra.py. Every check prints its runs and its failures; a failure above 0 refutes
the claim the check names (the two existence checks, 'open' and 'local bound', print what they found)."""

# ---- the integer generator: Knuth's 64-bit MMIX LCG, the probe's own (the probe is no engine) ----------
MASK = (1 << 64) - 1


class Lcg:
    def __init__(self, seed):
        self.x = seed & MASK

    def next(self):
        self.x = (self.x * 6364136223846793005 + 1442695040888963407) & MASK
        return self.x >> 33

    def int_in(self, lo, hi):  # an integer in [lo, hi]
        return lo + self.next() % (hi - lo + 1)


# ---- Gaussian integers and twin pairs -------------------------------------------------------------------
def gc(z):
    return (z[0], -z[1])


def gm(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def ga(z, w):
    return (z[0] + w[0], z[1] + w[1])


def gs(z, w):
    return (z[0] - w[0], z[1] - w[1])


def gn(z):
    return (-z[0], -z[1])


def nrm(z):
    return z[0] * z[0] + z[1] * z[1]


I_UNIT = (0, 1)


def reading(psi):
    """The one-time reading of a twin pair: rho = N(psi1) + N(psi2), S = (2 Re, 2 Im of conj(psi1) psi2, N(psi1) - N(psi2))."""
    a, b = psi
    ab = gm(gc(a), b)
    return nrm(a) + nrm(b), (ab[0] + ab[0], ab[1] + ab[1], nrm(a) - nrm(b))


def two_time(now, before):
    """David's reading from the slots (DAVID-TENSOR24-THE-CLICK_CHECKS.txt): D_ac = i (conj(b_a) n_c - conj(n_a) b_c),
    W = D_uu + D_dd, S = (2 Re D_ud, -2 Im D_ud, D_uu - D_dd)."""

    def d(x, y):
        return gm(I_UNIT, gs(gm(gc(before[x]), now[y]), gm(gc(now[x]), before[y])))

    duu, ddd, dud = d(0, 0), d(1, 1), d(0, 1)
    assert duu[1] == 0 and ddd[1] == 0
    return duu[0] + ddd[0], (dud[0] + dud[0], -(dud[1] + dud[1]), duu[0] - ddd[0])


def perp(phi):
    """phi_perp = (-conj(phi2), conj(phi1))."""
    return (gn(gc(phi[1])), gc(phi[0]))


def inner(phi, psi):
    """<phi, psi> = conj(phi1) psi1 + conj(phi2) psi2."""
    return ga(gm(gc(phi[0]), psi[0]), gm(gc(phi[1]), psi[1]))


def det(u, v):
    """The A1 part of two twin pairs: u1 v2 - u2 v1, one Gaussian integer."""
    return gs(gm(u[0], v[1]), gm(u[1], v[0]))


def dot3(s, t):
    return s[0] * t[0] + s[1] * t[1] + s[2] * t[2]


def scal(c, psi):
    return (gm(c, psi[0]), gm(c, psi[1]))


def sp_add(p, q):
    return (ga(p[0], q[0]), ga(p[1], q[1]))


def sp_neg(p):
    return (gn(p[0]), gn(p[1]))


def sense(phi, a):
    """phi^a: the detector's own spinor for a = +1, its perp for a = -1."""
    return phi if a > 0 else perp(phi)


rng = Lcg(20261028)


def gauss(k):
    return (rng.int_in(-k, k), rng.int_in(-k, k))


def spinor(k):
    while True:
        p = (gauss(k), gauss(k))
        if p[0] != (0, 0) or p[1] != (0, 0):
            return p


results = []


def report(name, runs, fails, claim):
    results.append((name, runs, fails, claim))


BIG = 10**6
RANDOM = 20000

# ---- 1. Lagrange: S . S = rho^2 for one twin pair (so S = 0 only at rho = 0) -----------------------------
runs = fails = 0
rng_small = range(-2, 3)
for a0 in rng_small:
    for a1 in rng_small:
        for b0 in rng_small:
            for b1 in rng_small:
                rho, s = reading(((a0, a1), (b0, b1)))
                runs += 1
                fails += dot3(s, s) != rho * rho
for _ in range(RANDOM):
    rho, s = reading(spinor(BIG))
    runs += 1
    fails += dot3(s, s) != rho * rho
report("lagrange", runs, fails, "S . S = rho rho for every twin pair (exhaustive in [-2, 2]^4, then 20,000 random up to 10^6)")

# ---- 2. the two-time reading: S . S - W W = 4 N(det[now, before]) >= 0, so S = 0 forces W = 0 -----------
runs = fails = zero_s = zero_s_bad = 0
for n0 in range(-1, 2):
    for n1 in range(-1, 2):
        for n2 in range(-1, 2):
            for n3 in range(-1, 2):
                for b0 in range(-1, 2):
                    for b1 in range(-1, 2):
                        for b2 in range(-1, 2):
                            for b3 in range(-1, 2):
                                now, before = ((n0, n1), (n2, n3)), ((b0, b1), (b2, b3))
                                w, s = two_time(now, before)
                                runs += 1
                                fails += dot3(s, s) - w * w != 4 * nrm(det(now, before))
                                if s == (0, 0, 0):
                                    zero_s += 1
                                    zero_s_bad += w != 0
for _ in range(RANDOM):
    now, before = spinor(BIG), spinor(BIG)
    w, s = two_time(now, before)
    runs += 1
    fails += dot3(s, s) - w * w != 4 * nrm(det(now, before))
report("two-time", runs, fails, "S . S - W W = 4 N(det[now, before]) on David's reading (exhaustive in [-1, 1]^8, then 20,000 random)")
report("open", zero_s, zero_s_bad, "every two-time reading with S = 0 has W = 0: no twin pair holds the open reading (W > 0, S = 0)")

# ---- 3. the perp: S(phi_perp) = -S(phi), N kept, perp(perp(phi)) = -phi, <phi_perp, phi> = 0 -------------
runs = fails = 0
for _ in range(RANDOM):
    phi = spinor(BIG)
    rho, s = reading(phi)
    rho_p, s_p = reading(perp(phi))
    runs += 1
    fails += (rho_p != rho) + (s_p != tuple(-x for x in s)) + (perp(perp(phi)) != sp_neg(phi)) + (inner(perp(phi), phi) != (0, 0))
report("perp", runs, fails, "phi_perp has the same rho and the opposite axis; its perp is -phi (the half-spin sign); it is orthogonal to phi")

# ---- 4. the A1 part: det[u, v] = <u_perp, v>, and 2 N(det[u, v]) = rho_u rho_v - S_u . S_v (Fierz) --------
runs = fails = 0
for _ in range(RANDOM):
    u, v = spinor(BIG), spinor(BIG)
    (ru, su), (rv, sv) = reading(u), reading(v)
    runs += 1
    fails += (det(u, v) != inner(perp(u), v)) + (2 * nrm(det(u, v)) != ru * rv - dot3(su, sv))
report("det-fierz", runs, fails, "det[u, v] = <u_perp, v> exactly, and 2 N(det[u, v]) = rho_u rho_v - S_u . S_v")

# ---- 5. the split's decomposition and its remainder's axis --------------------------------------------------
runs = fails = 0
for _ in range(RANDOM):
    phi, psi = spinor(1000), spinor(1000)
    rd, m = reading(phi)
    whole = sp_add(scal(inner(phi, psi), phi), scal(inner(perp(phi), psi), perp(phi)))
    runs += 1
    fails += whole != scal((rd, 0), psi)
    for a in (1, -1):
        eta = sense(phi, -a)  # the part not taken when the answer is a
        c = inner(eta, psi)
        rem_rho, rem_s = reading(scal(c, eta))
        want = tuple(-a * nrm(c) * x for x in m)  # N(<eta, psi>) times the axis -a m
        runs += 1
        fails += (rem_s != want) + (rem_rho != nrm(c) * rd)
report("remainder", runs, fails, "N(phi) psi = <phi,psi> phi + <phi_perp,psi> phi_perp; the part not taken has the axis -a m exactly")

# ---- 6. the pair's joint split on its A1 part --------------------------------------------------------------
runs = fails = 0
for _ in range(RANDOM):
    p1, p2 = spinor(1000), spinor(1000)
    (r1, m1), (r2, m2) = reading(p1), reading(p2)
    sig = {(a, b): nrm(det(sense(p1, a), sense(p2, b))) for a in (1, -1) for b in (1, -1)}
    bad = 0
    for (a, b), s_ab in sig.items():
        bad += s_ab + s_ab != r1 * r2 - a * b * dot3(m1, m2)
    for a in (1, -1):
        bad += sig[(a, 1)] + sig[(a, -1)] != r1 * r2  # the first click's two parts: half and half
    bad += sum(a * b * s for (a, b), s in sig.items()) != -2 * dot3(m1, m2)
    bad += sum(sig.values()) != 2 * r1 * r2
    runs += 1
    fails += bad
report("joint", runs, fails, "sigma_ab = N(det[phi1^a, phi2^b]) = (rho1 rho2 - a b m1 . m2) / 2; each first part rho1 rho2; E = -m1.m2/(rho1 rho2)")

# ---- 7. the joint split by one draw equals the first click then the partner's law 6 on (rho1, -a m1) --------
runs = fails = 0
for _ in range(400):
    p1, p2 = spinor(3), spinor(3)
    (r1, m1), (r2, m2) = reading(p1), reading(p2)
    total = 2 * r1 * r2
    sig = {(a, b): nrm(det(sense(p1, a), sense(p2, b))) for a in (1, -1) for b in (1, -1)}
    order = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    room = total * 3  # a room the sizes' sum divides
    joint = dict.fromkeys(order, 0)
    for c in range(room):  # one draw over four parts: Rule3 c total = t room + r, the part where t falls
        t = (c * total) // room
        acc = 0
        for k in order:
            acc += sig[k]
            if t < acc:
                joint[k] += 1
                break
    room_a, room_b = 2, total * 3
    seq = dict.fromkeys(order, 0)
    for ca in range(room_a):
        a = 1 if ca * (r1 * r2 + r1 * r2) < room_a * (r1 * r2) else -1  # law 6 on the A1 part's first parts
        for cb in range(room_b):
            partner_s = tuple(-a * x for x in m1)  # the partner's reading (rho1, -a m1)
            b = 1 if cb * (r1 + r1) * r2 < room_b * (r1 * r2 + dot3(partner_s, m2)) else -1
            seq[(a, b)] += 1
    for k in order:
        runs += 1
        fails += joint[k] * room_a * room_b != seq[k] * room  # the same odds, cross-multiplied
        fails += joint[k] * total != sig[k] * room  # exact Born odds where the sum divides the room
report("factor", runs, fails, "the joint split's odds equal the first click (half and half) then the partner's law 6 on (rho1, -a m1)")

# ---- 8. the antisymmetric product of two twin pairs is det times epsilon --------------------------------------
runs = fails = 0
for _ in range(RANDOM):
    u, v = spinor(BIG), spinor(BIG)
    d = det(u, v)
    for i in range(2):
        for j in range(2):
            anti = gs(gm(u[i], v[j]), gm(v[i], u[j]))
            eps = 0 if i == j else (1 if i < j else -1)
            runs += 1
            fails += anti != (d[0] * eps, d[1] * eps)
report("antisym", runs, fails, "u (x) v - v (x) u = det[u, v] epsilon: the antisymmetric part of two twin pairs is the singlet alone")


# ---- 9. the double cover 2O as Gaussian-integer matrices with a scale; epsilon its one A1 two-spinor -----------
def mm(p, q):
    return (
        (ga(gm(p[0][0], q[0][0]), gm(p[0][1], q[1][0])), ga(gm(p[0][0], q[0][1]), gm(p[0][1], q[1][1]))),
        (ga(gm(p[1][0], q[0][0]), gm(p[1][1], q[1][0])), ga(gm(p[1][0], q[0][1]), gm(p[1][1], q[1][1]))),
    )


def norm_el(m, e):
    while e >= 2 and all(z[0] % 2 == 0 and z[1] % 2 == 0 for row in m for z in row):
        m = tuple(tuple((z[0] // 2, z[1] // 2) for z in row) for row in m)
        e -= 2
    return m, e


def mdet(m):
    return gs(gm(m[0][0], m[1][1]), gm(m[0][1], m[1][0]))


def mt(m):
    return ((m[0][0], m[1][0]), (m[0][1], m[1][1]))


def mapply(m, psi):
    return (ga(gm(m[0][0], psi[0]), gm(m[0][1], psi[1])), ga(gm(m[1][0], psi[0]), gm(m[1][1], psi[1])))


ONE, ZERO = (1, 0), (0, 0)
ident = ((ONE, ZERO), (ZERO, ONE))
gens = [(((1, -1), ZERO), (ZERO, (1, 1))), ((ONE, (0, -1)), ((0, -1), ONE))]  # quarter turns about z and x, scale root 2
group = {(ident, 0)}
frontier = [(ident, 0)]
while frontier:
    new = []
    for m, e in frontier:
        for g in gens:
            el = norm_el(mm(m, g), e + 1)
            if el not in group:
                group.add(el)
                new.append(el)
    frontier = new
minus_one = (((-1, 0), ZERO), (ZERO, (-1, 0)))
runs = 1
fails = (len(group) != 48) + ((minus_one, 0) not in group)
for m, e in group:  # det M = 2^e (the turn has det 1), so U eps U^T = eps: epsilon is A1
    runs += 1
    fails += mdet(m) != (1 << e, 0)
basis_sym = [((ONE, ZERO), (ZERO, ZERO)), ((ZERO, ONE), (ONE, ZERO)), ((ZERO, ZERO), (ZERO, ONE))]
for t in basis_sym:  # the Reynolds sum of each symmetric two-spinor, scaled to the common 4: zero (no A1 in T1)
    acc = [[ZERO, ZERO], [ZERO, ZERO]]
    for m, e in group:
        mtm = mm(mm(m, t), mt(m))
        scale = (1 << (2 - e), 0)
        for i in range(2):
            for j in range(2):
                acc[i][j] = ga(acc[i][j], gm(scale, mtm[i][j]))
    runs += 1
    fails += any(acc[i][j] != ZERO for i in range(2) for j in range(2))
rotations = set()
for m, e in group:  # the axis S is T1: S(M psi) = 2^e R S(psi), R one of the 24 signed permutations of det 1
    cols = []
    for probe, half in (((ONE, ZERO), 1), (((1, 0), (1, 0)), 2), (((1, 0), (0, 1)), 2)):
        s = reading(mapply(m, probe))[1]
        cols.append(tuple(x // (half << e) for x in s))
    rz, rx, ry = cols
    r = ((rx[0], ry[0], rz[0]), (rx[1], ry[1], rz[1]), (rx[2], ry[2], rz[2]))
    signed_perm = all(sorted(abs(x) for x in row) == [0, 0, 1] for row in r)
    d3 = (r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1]) - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
          + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0]))
    runs += 1
    fails += (not signed_perm) + (d3 != 1)
    rotations.add(r)
    for _ in range(20):
        psi = spinor(50)
        s0, s1 = reading(psi)[1], reading(mapply(m, psi))[1]
        rs = tuple(dot3(row, s0) << e for row in r)
        runs += 1
        fails += s1 != rs
runs += 1
fails += len(rotations) != 24
report("2O", runs, fails, "the 48 of 2O close; det M = 2^e; epsilon is the one A1 two-spinor; the axis S moves by the 24, each twice")

# ---- 10. the six Spokes' directions: sum of n n^T = 2 I (rank-2 isotropy of the 24's orbit of an axis) --------
SIX = {  # the six Spoke directions and a twin pair along each (Gaussian integers, no root)
    (0, 0, 1): ((1, 0), (0, 0)), (0, 0, -1): ((0, 0), (1, 0)),
    (1, 0, 0): ((1, 0), (1, 0)), (-1, 0, 0): ((1, 0), (-1, 0)),
    (0, 1, 0): ((1, 0), (0, 1)), (0, -1, 0): ((1, 0), (0, -1)),
}
runs = fails = 0
for i in range(3):
    for j in range(3):
        runs += 1
        fails += sum(n[i] * n[j] for n in SIX) != (2 if i == j else 0)
for n, chi in SIX.items():
    rho, s = reading(chi)
    runs += 1
    fails += s != tuple(rho * x for x in n)
report("isotropy", runs, fails, "the six Spoke directions sum n n^T to 2 I, and each has a Gaussian twin pair along it")

# ---- 11. the CHSH values: the singlet, the local model, every deterministic local strategy ---------------------
SETTINGS = {"a": ((1, 0), (0, 0)), "a'": ((1, 0), (1, 0)), "b": ((5, 0), (2, 0)), "b'": ((5, 0), (-2, 0))}
PAIRS = [("a", "b", 1), ("a", "b'", 1), ("a'", "b", 1), ("a'", "b'", -1)]  # S = E(a,b) + E(a,b') + E(a',b) - E(a',b')


def singlet_e(p1, p2):  # (numerator, denominator)
    (r1, m1), (r2, m2) = reading(p1), reading(p2)
    return -dot3(m1, m2), r1 * r2


def local_e(p1, p2):  # opposite senses chi(n), chi(-n), Born at each end, n over the six directions
    (r1, m1), (r2, m2) = reading(p1), reading(p2)
    num, den = 0, 0
    for n, chi in SIX.items():
        ra, sa = reading(chi)
        rb, sb = reading(SIX[tuple(-x for x in n)])
        num_n, den_n = dot3(sa, m1) * dot3(sb, m2), ra * r1 * rb * r2
        num, den = (num * den_n + num_n * den, den * den_n) if den else (num_n, den_n)
    return num, den * len(SIX)


def chsh(efun):
    num, den = 0, 1
    for x, y, sgn in PAIRS:
        n, d = efun(SETTINGS[x], SETTINGS[y])
        num, den = num * d + sgn * n * den, den * d
    return num, den


def reduce(n, d):
    a, b = abs(n), abs(d)
    while b:
        a, b = b, a % b
    return n // a, d // a


s_singlet = reduce(*chsh(singlet_e))
s_local = reduce(*chsh(local_e))
best = 0
for xa in (1, -1):
    for xa2 in (1, -1):
        for yb in (1, -1):
            for yb2 in (1, -1):
                out = {"a": xa, "a'": xa2, "b": yb, "b'": yb2}
                best = max(best, abs(sum(sgn * out[x] * out[y] for x, y, sgn in PAIRS)))
runs = 1
fails = (s_singlet != (-82, 29)) + (s_local != (-82, 87)) + (best != 2)
n_, d_ = s_singlet
fails += not (4 * d_ * d_ < n_ * n_ <= 8 * d_ * d_)
report("chsh", runs, fails, "S singlet = -82/29 (4 < S^2 <= 8), local isotropic = -82/87, max over the 16 deterministic strategies = 2")
for x, y, _sgn in PAIRS:
    report(f"E({x},{y})", 0, 0, f"singlet {reduce(*singlet_e(SETTINGS[x], SETTINGS[y]))}, local {reduce(*local_e(SETTINGS[x], SETTINGS[y]))}")
report("local bound", 16, 0, f"the largest |S| of the 16 deterministic local strategies: {best}")

# ---- negative controls: the same checks with one sign turned must fail (the probe can fail) ------------------------
controls = []
bad = 0
for _ in range(400):  # the partner's reading (rho1, +a m1) instead of (rho1, -a m1)
    p1, p2 = spinor(3), spinor(3)
    (r1, m1), (r2, m2) = reading(p1), reading(p2)
    for a in (1, -1):
        wrong = tuple(a * x for x in m1)
        up = r1 * r2 + dot3(wrong, m2)
        bad += up != nrm(det(sense(p1, a), p2)) + nrm(det(sense(p1, a), p2))
controls.append(("partner +a m1", bad))
bad = 0
for _ in range(400):  # the joint split without the perp (phi^- = phi) loses the half and half
    p1, p2 = spinor(3), spinor(3)
    r1, r2 = reading(p1)[0], reading(p2)[0]
    bad += nrm(det(p1, p2)) + nrm(det(p1, p2)) != r1 * r2
controls.append(("half without perp", bad))

# ---- the record ---------------------------------------------------------------------------------------------------
total_fail = sum(f for name, r, f, c in results)
print("closure24_algebra.py: draft D's algebra, integers only")
for name, r, f, c in results:
    print(f"  {name:12s} runs {r:7d} failures {f:3d}  {c}")
print(f"total failures over the checks: {total_fail}")
for name, count in controls:
    print(f"  control (a wrong form; a count above 0 shows the check can fail): {name:20s} mismatches {count}")


def tenk(n, d):  # n / d times 10^4, truncated toward 0, integers only
    q = (abs(n) * 10000) // d
    return -q if n < 0 else q


print(f"S singlet {s_singlet[0]}/{s_singlet[1]} (x 10^4: {tenk(*s_singlet)}), local isotropic {s_local[0]}/{s_local[1]} (x 10^4: {tenk(*s_local)})")
