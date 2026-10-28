"""Verifier's own probe for draft D (claims 1, 2 and the Bell numbers), written without the draft's code.
Integers only: a Gaussian integer is a small class over Python ints; no float, no Fraction, no root.
Random numbers from Python's getrandbits alone (integer). Run: python3 -I -B verify_closure.py [mutation]
A mutation name as the first argument changes one term (to show the probe can fail)."""

import random
import sys

MUT = sys.argv[1] if len(sys.argv) > 1 else ""


class Z:
    __slots__ = ("re", "im")

    def __init__(self, re, im=0):
        self.re, self.im = re, im

    def __add__(self, o):
        return Z(self.re + o.re, self.im + o.im)

    def __sub__(self, o):
        return Z(self.re - o.re, self.im - o.im)

    def __neg__(self):
        return Z(-self.re, -self.im)

    def __mul__(self, o):
        return Z(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)

    def __eq__(self, o):
        return self.re == o.re and self.im == o.im

    def cj(self):
        return Z(self.re, -self.im)

    def n(self):
        return self.re * self.re + self.im * self.im

    def key(self):
        return (self.re, self.im)


I = Z(0, 1)
ZERO = Z(0, 0)
R = random.Random(0xD0D0)


def rint(bits):  # a signed integer of up to `bits` bits, from getrandbits only
    v = R.getrandbits(bits)
    return -v if R.getrandbits(1) else v


def rz(bits):
    return Z(rint(bits), rint(bits))


def rspin(bits):
    while True:
        p = (rz(bits), rz(bits))
        if p[0].n() + p[1].n():
            return p


def rho_of(p):
    return p[0].n() + p[1].n()


def axis(p):  # S = (2 Re, 2 Im of conj(psi1) psi2, N(psi1) - N(psi2)), written out on the real parts
    x1, y1, x2, y2 = p[0].re, p[0].im, p[1].re, p[1].im
    sx = 2 * (x1 * x2 + y1 * y2)
    sy = 2 * (x1 * y2 - y1 * x2)
    if MUT == "axis_y_sign":
        sy = -sy
    sz = x1 * x1 + y1 * y1 - x2 * x2 - y2 * y2
    return (sx, sy, sz)


def dot(s, t):
    return s[0] * t[0] + s[1] * t[1] + s[2] * t[2]


def perp(p):  # (-conj(p2), conj(p1))
    if MUT == "perp_no_conj":
        return (-p[1], p[0])
    if MUT == "perp_no_sign":
        return (p[1].cj(), p[0].cj())
    return (-(p[1].cj()), p[0].cj())


def ovl(p, q):  # <p, q> = conj(p1) q1 + conj(p2) q2
    return p[0].cj() * q[0] + p[1].cj() * q[1]


def det2(u, v):  # u1 v2 - u2 v1
    if MUT == "det_sign":
        return u[0] * v[1] + u[1] * v[0]
    return u[0] * v[1] - u[1] * v[0]


def sense(p, a):
    return p if a == 1 else perp(p)


def eqs(p, q):
    return p[0] == q[0] and p[1] == q[1]


tally = []


def rec(name, runs, fails, note):
    tally.append((name, runs, fails, note))


def small_spinors(k):
    out = []
    rng = range(-k, k + 1)
    for a in rng:
        for b in rng:
            for c in rng:
                for d in rng:
                    if a or b or c or d:
                        out.append((Z(a, b), Z(c, d)))
    return out


SM1 = small_spinors(1)  # 80 nonzero spinors with parts in [-1, 1]
SM2 = small_spinors(2)  # 624 with parts in [-2, 2]

# ---- V1. claim 2(a): S . S = rho rho; S = 0 only at psi = 0 ------------------------------------------------
runs = fails = zero_axis_nonzero = 0
for p in small_spinors(3):
    s = axis(p)
    runs += 1
    fails += dot(s, s) != rho_of(p) ** 2
    zero_axis_nonzero += s == (0, 0, 0)
for bits in (8, 31, 62, 200):
    for _ in range(5000):
        p = rspin(bits)
        s = axis(p)
        runs += 1
        fails += dot(s, s) != rho_of(p) ** 2
for _ in range(5000):  # lopsided: one part huge, the others tiny
    p = (Z(rint(120), rint(2)), Z(rint(2), rint(3)))
    if rho_of(p):
        runs += 1
        fails += dot(axis(p), axis(p)) != rho_of(p) ** 2
rec("V1 S.S=rho^2", runs, fails + zero_axis_nonzero, "exhaustive [-3,3]^4 (S=0 met only at 0), random to 200 bits, lopsided")


# ---- V2. claim 2(b): David's two-time reading, S . S - W W = 4 N(det[now, before]) ---------------------------
def two_time(now, bef):
    def d(a, c):  # D_ac = i (conj(b_a) n_c - conj(n_a) b_c)
        return I * (bef[a].cj() * now[c] - now[a].cj() * bef[c])

    duu, ddd, dud, ddu = d(0, 0), d(1, 1), d(0, 1), d(1, 0)
    herm = duu.im == 0 and ddd.im == 0 and ddu == dud.cj()
    w = duu.re + ddd.re
    sy = -(dud.im + dud.im)
    if MUT == "twotime_y_sign":
        sy = -sy
    return herm, w, (dud.re + dud.re, sy, duu.re - ddd.re)


runs = fails = s0 = s0_bad = s0_par_bad = 0
for un in range(-1, 2):
    for ui in range(-1, 2):
        for dn in range(-1, 2):
            for di in range(-1, 2):
                for ub in range(-1, 2):
                    for vb in range(-1, 2):
                        for db in range(-1, 2):
                            for eb in range(-1, 2):
                                now, bef = (Z(un, ui), Z(dn, di)), (Z(ub, vb), Z(db, eb))
                                herm, w, s = two_time(now, bef)
                                runs += 1
                                fails += (not herm) + (dot(s, s) - w * w != 4 * det2(now, bef).n())
                                if s == (0, 0, 0):
                                    s0 += 1
                                    s0_bad += w != 0
                                    # S = 0 also forces the two slots parallel: det[now, before] = 0
                                    s0_par_bad += det2(now, bef).n() != 0
for bits in (16, 62, 150):
    for _ in range(5000):
        now, bef = rspin(bits), rspin(bits)
        herm, w, s = two_time(now, bef)
        runs += 1
        fails += (not herm) + (dot(s, s) - w * w != 4 * det2(now, bef).n())
        # the hand form: 4 (rho_now rho_before - N(<now, before>))
        fails += dot(s, s) - w * w != 4 * (rho_of(now) * rho_of(bef) - ovl(now, bef).n())
rec("V2 two-time", runs, fails, "D Hermitian; S.S - W^2 = 4 N(det[now,before]) = 4 (rho rho' - N<now,before>); exhaustive [-1,1]^8 + to 150 bits")
rec("V2 open", s0, s0_bad + s0_par_bad, f"{s0} two-time readings with S = 0 met: every one has W = 0 and det = 0")

# ---- V3. the perp, Fierz, det = <u_perp, v> ----------------------------------------------------------------
runs = fails = 0
for bits in (8, 62, 160):
    for _ in range(4000):
        u, v = rspin(bits), rspin(bits)
        pu = perp(u)
        runs += 1
        fails += rho_of(pu) != rho_of(u)
        fails += axis(pu) != tuple(-x for x in axis(u))
        fails += not eqs(perp(pu), (-u[0], -u[1]))
        fails += ovl(pu, u) != ZERO
        fails += det2(u, v) != ovl(pu, v)
        fails += 2 * ovl(u, v).n() != rho_of(u) * rho_of(v) + dot(axis(u), axis(v))  # Fierz
        fails += 2 * det2(u, v).n() != rho_of(u) * rho_of(v) - dot(axis(u), axis(v))
        fails += ovl(u, v).n() + ovl(pu, v).n() != rho_of(u) * rho_of(v)  # Lagrange
rec("V3 perp/Fierz", runs, fails, "N and -S under perp, perp^2 = -1, <perp u,u> = 0, det = <perp u, v>, Fierz, Lagrange")


# ---- V4. claim 1: the four parts sigma_ab = N(det[phi1^a, phi2^b]) -------------------------------------------
def parts(p1, p2):
    return {(a, b): det2(sense(p1, a), sense(p2, b)).n() for a in (1, -1) for b in (1, -1)}


def check_parts(p1, p2):
    r1, r2, m1, m2 = rho_of(p1), rho_of(p2), axis(p1), axis(p2)
    sg = parts(p1, p2)
    bad = 0
    for (a, b), x in sg.items():
        bad += 2 * x != r1 * r2 - a * b * dot(m1, m2)
    for a in (1, -1):
        bad += sg[(a, 1)] + sg[(a, -1)] != r1 * r2  # each row: the first click half and half
        bad += sg[(1, a)] + sg[(-1, a)] != r1 * r2  # each column too: the partner's marginal one half
    bad += sum(sg.values()) != 2 * r1 * r2
    bad += sum(a * b * x for (a, b), x in sg.items()) != -2 * dot(m1, m2)
    return bad


runs = fails = 0
for p1 in SM1:
    for p2 in SM1:
        runs += 1
        fails += check_parts(p1, p2)
for bits in (10, 62, 128):
    for _ in range(4000):
        runs += 1
        fails += check_parts(rspin(bits), rspin(bits))
rec("V4 four parts", runs, fails, "2 sigma_ab = rho1 rho2 - ab m1.m2, rows and columns rho1 rho2, E = -m1.m2/(rho1 rho2); all 6,400 pairs in [-1,1]^4 + random")


# ---- V5. claim 1: the two-step form (first click, then law 6 on (rho1, -a m1)) gives the same joint odds --------
def law6_up(c, room, rho, s, rd, m):  # up where c (rho + rho) rho_d < room (rho rho_d + S . m)
    lhs = c * (rho + rho) * rd
    if MUT == "law6_factor":
        lhs = c * rho * rd
    return lhs < room * (rho * rd + dot(s, m))


def pick4(c, room, sg):  # Rule3: c total = t room + r; the part whose running sum first passes t
    order = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    total = sum(sg[k] for k in order)
    t = (c * total) // room
    acc = 0
    for k in order:
        acc += sg[k]
        if t < acc:
            return k
    raise AssertionError


runs = fails = within_bad = 0
for _ in range(300):
    p1, p2 = rspin(2), rspin(2)
    r1, r2, m1, m2 = rho_of(p1), rho_of(p2), axis(p1), axis(p2)
    sg = parts(p1, p2)
    total = 2 * r1 * r2
    room = total * 2  # divisible: exact
    if sum(sg.values()) != total:  # the parts must sum to the pair's whole (else no pick is defined)
        runs += 4
        fails += 4
        continue
    joint = {k: 0 for k in sg}
    for c in range(room):
        joint[pick4(c, room, sg)] += 1
    # the two steps with two independent draws, every pair of draws counted
    room_a, room_b = 2, 2 * r1 * r2
    two = {k: 0 for k in sg}
    for ca in range(room_a):
        a = 1 if law6_up(ca, room_a, r1 * r2, (0, 0, 0), 1, (0, 0, 0)) else -1  # the first parts r1 r2 each: half
        partner = (r1, tuple(-a * x for x in m1))
        if MUT == "partner_plus":
            partner = (r1, tuple(a * x for x in m1))
        for cb in range(room_b):
            b = 1 if law6_up(cb, room_b, partner[0], partner[1], r2, m2) else -1
            two[(a, b)] += 1
    for k in sg:
        runs += 1
        fails += joint[k] * room_a * room_b != two[k] * room  # same odds
        fails += joint[k] * total != sg[k] * room  # Born's exact where the room divides
    # a room the sum does not divide: within one count (section 27's claim)
    room2 = total + 1 + R.getrandbits(5)
    cnt = {k: 0 for k in sg}
    for c in range(room2):
        cnt[pick4(c, room2, sg)] += 1
    for k in sg:
        within_bad += abs(cnt[k] * total - sg[k] * room2) >= total
rec("V5 two steps", runs, fails, "one draw over four parts = first click half and half, then law 6 on (rho1, -a m1): 300 detector pairs, every draw")
rec("V5 within one", 1200, within_bad, "a room the parts' sum does not divide: each count within one of Born's")

# ---- V6. the open axis under law 6: (rho, S) = (0, 0) is always down ----------------------------------------
runs = fails = 0
for p2 in SM1:
    r2, m2 = rho_of(p2), axis(p2)
    for room in (2, 7, 58):
        for c in range(room):
            runs += 1
            fails += law6_up(c, room, 0, (0, 0, 0), r2, m2)  # up never
rec("V6 open is down", runs, fails, "law 6 on the only reading with S = 0 (rho = 0): never up, so not half and half")

# ---- V7. CHSH: the settings, the singlet, the local value, every local deterministic rule ---------------------
SET = {"a": (Z(1), Z(0)), "a'": (Z(1), Z(1)), "b": (Z(5), Z(2)), "b'": (Z(5), Z(-2))}
TERMS = (("a", "b", 1), ("a", "b'", 1), ("a'", "b", 1), ("a'", "b'", -1))


def frac_add(x, y):
    return (x[0] * y[1] + y[0] * x[1], x[1] * y[1])


def frac_red(x):
    a, b = abs(x[0]), abs(x[1])
    while b:
        a, b = b, a % b
    g = a if a else 1
    s = -1 if x[1] < 0 else 1
    return (s * x[0] // g, s * x[1] // g)


fails = 0
fails += [(rho_of(SET[k]), axis(SET[k])) for k in ("a", "a'", "b", "b'")] != [
    (1, (0, 0, 1)), (2, (2, 0, 0)), (29, (20, 0, 21)), (29, (-20, 0, 21))]
s_sing = (0, 1)
for x, y, sgn in TERMS:
    s_sing = frac_add(s_sing, (-sgn * dot(axis(SET[x]), axis(SET[y])), rho_of(SET[x]) * rho_of(SET[y])))
s_sing = frac_red(s_sing)
fails += s_sing != (-82, 29)
fails += not (4 * 29 * 29 < 82 * 82 <= 8 * 29 * 29)
# the singlet's E from the four parts (a different route): sum ab sigma / sum sigma
s_parts = (0, 1)
for x, y, sgn in TERMS:
    sg = parts(SET[x], SET[y])
    s_parts = frac_add(s_parts, (sgn * sum(a * b * v for (a, b), v in sg.items()), sum(sg.values())))
fails += frac_red(s_parts) != (-82, 29)
# the local value: opposite senses along n, n over the six Spoke directions, Born at each end
SIX = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
s_loc = (0, 1)
for x, y, sgn in TERMS:
    m1, m2, r1, r2 = axis(SET[x]), axis(SET[y]), rho_of(SET[x]), rho_of(SET[y])
    num = sum(dot(n, m1) * (-dot(n, m2)) for n in SIX)  # <a>_n <b>_n = (n.m1/r1) (-n.m2/r2)
    s_loc = frac_add(s_loc, (sgn * num, 6 * r1 * r2))
fails += frac_red(s_loc) != (-82, 87)
# every local deterministic rule: answers in {-1, +1}, then also in {-1, 0, +1} (a pair whose click did not fire counted as 0)
vals2 = [(p, q, r, t) for p in (1, -1) for q in (1, -1) for r in (1, -1) for t in (1, -1)]
best2 = max(abs(p * r + p * t + q * r - q * t) for p, q, r, t in vals2)
all_two = all(abs(p * r + p * t + q * r - q * t) == 2 for p, q, r, t in vals2)
vals3 = [(p, q, r, t) for p in (1, 0, -1) for q in (1, 0, -1) for r in (1, 0, -1) for t in (1, 0, -1)]
best3 = max(abs(p * r + p * t + q * r - q * t) for p, q, r, t in vals3)
fails += (best2 != 2) + (not all_two) + (best3 != 2)
rec("V7 CHSH", 1, fails, f"settings' axes; S singlet {s_sing[0]}/{s_sing[1]} two ways; local {frac_red(s_loc)}; 16 rules all |S| = 2; 81 rules with 0, max {best3}")

# the detection loophole: a local deterministic rule, each pair counted only where both clicks fired
# hidden k in 0..3 names one of the four terms; A fires only at that term's A setting, B only at its B setting
cnt = {t: [0, 0] for t in range(4)}  # (sum of a b over fired pairs, fired pairs)
allp = {t: [0, 0] for t in range(4)}  # every pair counted, a missing click as 0
for k in range(4):
    xk, yk, sk = TERMS[k]
    for t, (x, y, sgn) in enumerate(TERMS):
        fa = x == xk
        fb = y == yk
        a = 1 if fa else 0
        b = (sk if fb else 0)
        allp[t][0] += a * b
        allp[t][1] += 1
        if fa and fb:
            cnt[t][0] += a * b
            cnt[t][1] += 1
s_post = (0, 1)
s_all = (0, 1)
for t, (x, y, sgn) in enumerate(TERMS):
    s_post = frac_add(s_post, (sgn * cnt[t][0], cnt[t][1]))
    s_all = frac_add(s_all, (sgn * allp[t][0], allp[t][1]))
rec("V7 loophole", 1, int(frac_red(s_post) != (4, 1)) + int(frac_red(s_all) != (1, 1)),
    f"a local rule: S = {frac_red(s_post)} over pairs clicked at both ends, S = {frac_red(s_all)} with every pair counted")

# ---- V8. the k <= 1/3 claim: for any state of two twin pairs, the trace of its correlation is at most its norm ----
# sum_i <Psi| sigma_i (x) sigma_i |Psi> = <Psi| (2 SWAP - 1) |Psi>, eigenvalues 1 (T1) and -3 (A1)
runs = fails = 0
for _ in range(20000):
    psi = [rz(20) for _ in range(4)]  # amplitudes of uu, ud, du, dd
    nrm = sum(z.n() for z in psi)
    if not nrm:
        continue
    uu, ud, du, dd = psi
    swap_exp = uu.n() + dd.n() + 2 * (ud.cj() * du).re  # <Psi| SWAP |Psi>
    tr_t = 2 * swap_exp - nrm
    a1 = (ud - du).n()  # 2 <Psi|singlet><singlet|Psi>
    runs += 1
    fails += (tr_t > nrm) + (tr_t < -3 * nrm) + (nrm - tr_t != 2 * a1)
rec("V8 k<=1/3", runs, fails, "Tr T in [-3, 1] times the norm, and 1 - Tr T = 4 x the A1 weight: E = +k m1^.m2^ for all axes needs k <= 1/3")

# ---- V9. claim 3 attacked: the L = 1 act's parts do not read the pair --------------------------------------------
# M3's sizes N(det[phi1^a, phi2^b]) hold no hand of the pair. Its E is the singlet's for ANY two fitted hands, even
# parallel ones. The A1 part of the pair's product, read literally, multiplies every size by N(det[psiA, psiB]):
# zero for parallel hands (no click), and half the product's weight for opposite ones (the T1 half discarded).
runs = singlet_any = zero_par = 0
half_opp_bad = 0
for _ in range(2000):
    pa = rspin(6)
    pb_par = (pa[0] * Z(3, 1), pa[1] * Z(3, 1))  # parallel to pa
    pb_opp = perp(pa)
    for x, y, sgn in TERMS:
        sg = parts(SET[x], SET[y])  # what M3 reads: the detectors alone
        e_num, e_den = sum(a * b * v for (a, b), v in sg.items()), sum(sg.values())
        runs += 1
        singlet_any += e_num * rho_of(SET[x]) * rho_of(SET[y]) == -dot(axis(SET[x]), axis(SET[y])) * e_den
        # literal A1 premise: sizes N(det[psiA, psiB]) sigma_ab
        zero_par += det2(pa, pb_par).n() == 0
    # the A1 weight of the product psiA (x) psiB: N(det)/(2 rhoA rhoB) = (rhoA rhoB - SA.SB)/(4 rhoA rhoB)
    ra, rb = rho_of(pa), rho_of(pb_opp)
    half_opp_bad += det2(pa, pb_opp).n() != ra * rb  # opposite senses: N(det) / (2 rhoA rhoB) = 1/2 exactly
rec("V9 M3 reads no pair", runs, runs - singlet_any, f"the singlet's E from the settings alone in {singlet_any} of {runs}; parallel hands' A1 factor 0 in {zero_par} of {runs}")
rec("V9 A1 half", 2000, half_opp_bad, "for opposite fitted hands the A1 part holds exactly half the product's weight")

# ---- V10. the two-time axis against the one-time axis: for now = g before (a pair turning whole by the Gaussian g),
# (W, S_two) = lam (rho, (S_x, -S_y, S_z)) with lam = -2 Im g: the two forms differ by the sign of S_y (a mirror)
runs = fails = 0
for _ in range(5000):
    bef = rspin(30)
    g = rz(8)
    if g.im == 0:
        continue
    now = (g * bef[0], g * bef[1])
    herm, w, s2 = two_time(now, bef)
    s1, r = axis(bef), rho_of(bef)
    lam = -2 * g.im
    runs += 1
    fails += (w != lam * r) + (s2 != (lam * s1[0], -lam * s1[1], lam * s1[2]))
rec("V10 two vs one", runs, fails, "for a pair turning whole: two-time (W, S) = -2 Im g (rho, (Sx, -Sy, Sz)) of the one-time reading")

# ---- the record -------------------------------------------------------------------------------------------------
print(f"verify_closure.py (the verifier's own probe), mutation: {MUT or 'none'}")
tot = 0
for name, r, f, note in tally:
    tot += f
    print(f"  {name:18s} runs {r:8d} failures {f:6d}  {note}")
print(f"total failures: {tot}")
