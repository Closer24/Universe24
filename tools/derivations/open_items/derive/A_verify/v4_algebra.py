"""V4 (verifier A): pure-integer re-derivation probes for the draft's lemma L0, formula F1, formula F3, formula F4 and the cost of F2. No engine code.

Every test counts its failures; each can fail.  Written from the formulas in DERIVATION.md, not from the
draft's probes.  python3 -I v4_algebra.py
"""
import itertools
import random
from fractions import Fraction

rng = random.Random(4242)
out = []


def report(name, bad, total):
    out.append(f"{name}: {bad} off of {total}")


# ------------------------------------------------------------------ L0, the whethers as quotients
def sgn(n):
    d = n * n + 1
    return n // d - (-n) // d


def ge0(n):
    return 1 + n // (n * n + 1)


def is0(n):
    return 1 + (-n * n) // (n * n * n * n + 1)


def cdiv(n, d):
    return (n + d - 1) // d


def true_sgn(n):
    return (n > 0) - (n < 0)


ns = list(range(-100000, 100001))
ns += [s * (2 ** k + e) for k in (31, 32, 63, 64, 127, 128, 255, 1000, 4096) for e in (-1, 0, 1) for s in (1, -1)]
ns += [rng.randrange(-2 ** 3000, 2 ** 3000) for _ in range(2000)]
report("L0 sgn(n) = n div (n n + 1) - (-n) div (n n + 1)", sum(sgn(n) != true_sgn(n) for n in ns), len(ns))
report("L0 [n >= 0] = 1 + n div (n n + 1)", sum(ge0(n) != int(n >= 0) for n in ns), len(ns))
report("L0 [n = 0] = 1 + (-n n) div (n^4 + 1)", sum(is0(n) != int(n == 0) for n in ns), len(ns))
pairs = [(n, d) for n in range(-300, 301) for d in range(1, 60)] + \
        [(rng.randrange(-2 ** 500, 2 ** 500), rng.randrange(1, 2 ** 400)) for _ in range(3000)]
report("L0 ceil(n / d) = (n + d - 1) div d, d > 0", sum(cdiv(n, d) != -((-n) // d) for n, d in pairs), len(pairs))
# the floor division of Python is Rule3's quotient (0 <= r' < d) for d > 0: checked, and the lemma needs d = n n + 1 > |n|
report("Rule3: n = q d + r', 0 <= r' < d for d = n n + 1",
       sum(not (0 <= n - (n // (n * n + 1)) * (n * n + 1) < n * n + 1) for n in ns), len(ns))

# ------------------------------------------------------------------ F1 on a torus: my own lead, twist, 48
L = 4
CL = list(itertools.product(range(L), repeat=3))


def add(x, a, s):
    y = list(x)
    y[a] = (y[a] + s) % L
    return tuple(y)


def lead(f, x, y):  # SUM over the gears (now_x before_y - before_x now_y); f[x] = (n3, n12, b3, b12)
    return f[x][0] * f[y][2] + f[x][1] * f[y][3] - f[x][2] * f[y][0] - f[x][3] * f[y][1]


def u_vec(f, k):  # u_b(k) = F(k, k - e_b) - F(k, k + e_b)
    return [lead(f, k, add(k, b, -1)) - lead(f, k, add(k, b, 1)) for b in range(3)]


def twist(f, x, a):  # e_a . (u(x) x u(x + e_a))
    ux, uy = u_vec(f, x), u_vec(f, add(x, a, 1))
    b, c = (a + 1) % 3, (a + 2) % 3
    return ux[b] * uy[c] - ux[c] * uy[b]


def senses(f, x, a):
    y = add(x, a, 1)
    F, h = lead(f, x, y), twist(f, x, a)
    return sgn(h * lead(f, y, x)), sgn(h * F), F, h   # sigma_x = sgn(h F_(y,x)), sigma_y = sgn(h F_(x,y))


def field(amp, real=False):
    f = {}
    for x in CL:
        n3, b3 = rng.randint(-amp, amp), rng.randint(-amp, amp)
        n12, b12 = (0, 0) if real else (rng.randint(-amp, amp), rng.randint(-amp, amp))
        f[x] = (n3, n12, b3, b12)
    return f


MATS = []
for perm in itertools.permutations(range(3)):
    for signs in itertools.product((1, -1), repeat=3):
        m = [[0] * 3 for _ in range(3)]
        for i in range(3):
            m[i][perm[i]] = signs[i]
        MATS.append(m)
assert len(MATS) == 48


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def act(m, x):
    return tuple(sum(m[i][j] * x[j] for j in range(3)) % L for i in range(3))


anti = zero_ok = n_mesh = 0
rot_ok = rot_n = ref_ok = ref_n = 0
for trial in range(40):
    f = field(rng.choice((3, 30, 3000)), real=(trial % 4 == 0))
    if trial % 5 == 1:   # plant zeros of the lead and of the twist
        for x in rng.sample(CL, 10):
            f[x] = (0, 0, 0, 0)
    base = {}
    for x in CL:
        for a in range(3):
            sx, sy, F, h = senses(f, x, a)
            n_mesh += 1
            anti += (sx + sy) != 0
            zero_ok += ((sx == 0 and sy == 0) != (h * F == 0))
            base[(x, a)] = (sx, sy)
    for m in rng.sample(MATS, 6):
        dm = det3(m)
        fm = {act(m, x): v for x, v in f.items()}
        for (x, a), (sx, sy) in base.items():
            y = add(x, a, 1)
            xm, ym = act(m, x), act(m, y)
            am = next(i for i in range(3) if m[i][a] != 0)
            lo, hi = (xm, ym) if m[am][a] == 1 else (ym, xm)
            s_lo, s_hi, _F, _h = senses(fm, lo, am)
            got = {lo: s_lo, hi: s_hi}
            ok = got[xm] == dm * sx and got[ym] == dm * sy
            if dm == 1:
                rot_n += 1
                rot_ok += ok
            else:
                ref_n += 1
                ref_ok += ok
report("F1 sigma_x + sigma_y = 0", anti, n_mesh)
report("F1 sigma = 0 exactly where h F = 0", zero_ok, n_mesh)
report("F1 rotations: the image Mesh's senses equal", rot_n - rot_ok, rot_n)
report("F1 reflections: the image Mesh's senses exchanged", ref_n - ref_ok, ref_n)
# J = Im(conj(z_x) z_y) on a real field is 0 at every Mesh
fr = field(500, real=True)
report("L1 J = Im(conj(z_x) z_y) = 0 on a real hand (no twelve gear)",
       sum((fr[x][0] * fr[add(x, a, 1)][1] - fr[x][1] * fr[add(x, a, 1)][0]) != 0 for x in CL for a in range(3)),
       3 * len(CL))
# the uniqueness: functions of (sgn h, sgn F) into {-1, 0, 1}
S3 = (-1, 0, 1)
dom = list(itertools.product(S3, S3))
odd_odd = odd_even = 0
for vals in itertools.product(S3, repeat=9):
    g = dict(zip(dom, vals))
    oddF = all(g[(h, -F)] == -g[(h, F)] for h, F in dom)
    oddh = all(g[(-h, F)] == -g[(h, F)] for h, F in dom)
    evenh = all(g[(-h, F)] == g[(h, F)] for h, F in dom)
    odd_odd += oddF and oddh
    odd_even += oddF and evenh
out.append(f"F1 uniqueness: rules g(sgn h, sgn F) odd in F and odd in h: {odd_odd} (kappa s_h s_F); "
           f"odd in F and even in h (a mirror-symmetric lay): {odd_even}")

# ------------------------------------------------------------------ F3: the ladder against brute force
def least_brute(P, a2, DM):
    """The least count s >= 0 with s P - a2 s s >= DM, or None (scanning to the vertex)."""
    top = (P + a2) // (2 * a2)
    if top * P - a2 * top * top < DM:
        return None
    lo, hi = -1, top    # the predicate is monotone on [0, top]: bisection over integers
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid >= 0 and mid * P - a2 * mid * mid >= DM:
            hi = mid
        else:
            lo = mid
    return hi


def ladder(P, a2, DM, cap=10 ** 6):
    s = cdiv(DM, P)
    steps = 0
    while steps < cap:
        nxt = cdiv(DM, P - a2 * s)
        if nxt == s:
            return s, steps
        s, steps = nxt, steps + 1
    return None, steps


bad = n = 0
worst = 0
neg = neg_n = 0
for t in range(60000):
    P = rng.choice((rng.randint(1, 10 ** 6), rng.randint(1, 10 ** 30), rng.randint(10 ** 40, 10 ** 60)))
    a2 = rng.choice((rng.randint(1, 10 ** 3), rng.randint(1, max(1, P // 7)), rng.randint(1, max(1, P // 5000))))
    top = (P + a2) // (2 * a2)
    fmax = top * P - a2 * top * top
    if fmax <= 0:
        continue
    kind = t % 3
    DM = rng.randint(1, fmax) if kind == 0 else (fmax - rng.randint(0, max(0, fmax // 10 ** 6)) if kind == 1 else rng.randint(1, max(1, fmax // 100)))
    want = least_brute(P, a2, DM)
    got, steps = ladder(P, a2, DM)
    n += 1
    bad += got != want
    worst = max(worst, steps)
report("F3 the ladder's fixed point = the least count (D > 0, payable)", bad, n)
out.append(f"F3 the ladder's longest run on these draws: {worst} carries past the first")
# the length grows without bound as the due nears the top: a family
fam = []
for k in (10, 20, 40, 80, 160):
    a2 = 1
    P = 2 * 10 ** k + 1
    top = (P + a2) // 2
    fmax = top * P - top * top
    _s, steps = ladder(P, a2, fmax)
    fam.append((k, steps))
out.append(f"F3 the ladder's carries at the top's own due, P = 2 10^k + 1, a' = 1: {fam}")
# the due at or below 0 (the remainder holds more than the windings booked): the formula as written
cases = []
for P, a2, DM in ((10 ** 6, 10, 0), (10 ** 6, 10, -1), (10 ** 6, 10, -10 ** 6), (10 ** 6, 10, -5 * 10 ** 6),
                  (10 ** 20, 10 ** 5, -3 * 10 ** 21)):
    top = (P + a2) // (2 * a2)
    zero = top * P - a2 * top * top < DM   # the draft's zero
    s, _ = ladder(P, a2, DM)
    cases.append((DM, 'zero' if zero else s))
out.append(f"F3 at a due D M <= 0, (D M, the count the formula writes): {cases}")

# ------------------------------------------------------------------ F3 on a real wind: my own numerator
RIM, GAM, KEY, GU = 15162856759112389, 1000, 36000, 16
M = 4 * GAM ** 3 * GU * GU
SP = [(a, s) for a in range(3) for s in (1, -1)]


def gear_at(pinion, x, rand):
    X = rand.randint(GAM // 2, 2 * GAM) if rand else GAM
    w = 6 * RIM * GAM ** 2 * GU * GU
    D = 12 * (RIM - pinion) * GAM ** 2 * GU * GU
    R = [2 * GAM ** 2 * GU * GU * pinion if not rand else 2 * GAM ** 2 * rand.randint(GU * GU // 2, GU * GU) * pinion
         for _ in range(6)]
    return w, w + w - D - sum(R), R, X


def numer(f, g, c, k):
    w, Sh, R, X = g[c]
    n, b = f[c][k], f[c][2 + k]
    nbs = [add(c, a, s) for a, s in SP]
    gripped = sum(R[j] * f[y][2 + k] for j, y in enumerate(nbs))
    shared = sum(R[j] * (b - f[y][2 + k]) * (n + f[y][k]) for j, y in enumerate(nbs))
    own = w * (n * n + b * b) - Sh * n * b - n * gripped
    return (own + own - shared) * X


def win(x):
    return [x] + [add(x, a, s) for a, s in SP]


def wnum(f, g, x, k):
    return sum(numer(f, g, c, k) for c in win(x))


def wwind(f, g, x):
    return sum(numer(f, g, c, k) // M for c in win(x) for k in range(2))


def moved(f, x, d):
    f2 = dict(f)
    n3, n12, b3, b12 = f[x]
    f2[x] = (n3 + d[0], n12 + d[1], b3, b12)
    return f2


def take(f, g, x, D):
    G, A = [], []
    for k in range(2):
        e = [1 if j == k else 0 for j in range(2)]
        N0, Np, Nm = wnum(f, g, x, k), wnum(moved(f, x, e), g, x, k), wnum(moved(f, x, [-v for v in e]), g, x, k)
        G.append((Np - Nm) // 2)
        A.append((Np + Nm - N0 - N0) // 2)
    u = [-sgn(G[k]) * ge0(G[k] * G[k] - G[1 - k] * G[1 - k]) for k in range(2)]
    P = -(u[0] * G[0] + u[1] * G[1])
    a2 = A[0] * (u[0] * u[0] + u[1] * u[1])
    return G, A, u, P, a2


bad_quad = bad_curv = bad_least = bad_bound = bad_cov = n_take = 0
for t in range(120):
    rand = rng if t % 2 else None
    g = {x: gear_at(RIM, x, rand) for x in CL}
    f = field(4000)
    x = rng.choice(CL)
    G, A, u, P, a2 = take(f, g, x, 0)
    bad_curv += A[0] != A[1] or A[0] != 2 * g[x][0] * g[x][3]
    # the fall along u is exactly s P - a2 s s on the numerator (separable in gears, quadratic)
    for s in (1, 2, 7, 33):
        d = [s * u[0], s * u[1]]
        fall = sum(wnum(f, g, x, k) - wnum(moved(f, x, d), g, x, k) for k in range(2))
        bad_quad += fall != s * P - a2 * s * s
    top = (P + a2) // (2 * a2) if a2 else 0
    fmax = top * P - a2 * top * top
    if fmax // M < 3:
        continue
    D = rng.randint(1, fmax // M)
    s, _ = ladder(P, a2, D * M)
    n_take += 1
    bad_least += not (s * P - a2 * s * s >= D * M and (s - 1) * P - a2 * (s - 1) ** 2 < D * M)
    Fc = wwind(f, g, x) - wwind(moved(f, x, [s * u[0], s * u[1]]), g, x)
    bad_bound += not (D - 14 < Fc < D + P // M + 15)
    # covariance under the hand's units and the conjugation
    for mapz, mapu in ((lambda z: (-z[1], z[0], -z[3], z[2]), lambda v: [-v[1], v[0]]),
                       (lambda z: (-z[0], -z[1], -z[2], -z[3]), lambda v: [-v[0], -v[1]]),
                       (lambda z: (z[0], -z[1], z[2], -z[3]), lambda v: [v[0], -v[1]])):
        fz = {c: mapz(v) for c, v in f.items()}
        Gz, Az, uz, Pz, a2z = take(fz, g, x, D)
        sz, _ = ladder(Pz, a2z, D * M)
        Fz = wwind(fz, g, x) - wwind(moved(fz, x, [sz * uz[0], sz * uz[1]]), g, x)
        bad_cov += not (uz == mapu(u) and sz == s and Fz == Fc)
report("F3 the bend a = 2 w X, the same on both gears", bad_curv, 120)
report("F3 the numerator's fall along u is exactly s P - a' s s (s = 1, 2, 7, 33)", bad_quad, 480)
report("F3 the ladder's count is the least on the numerator", bad_least, n_take)
report("F3 the carried window's fall in (D - 14, D + P div M + 15)", bad_bound, n_take)
report("F3 covariant under z -> i z, -z, conj z (unit turned, count and fall kept)", bad_cov, 3 * n_take)

# ------------------------------------------------------------------ F4: the sweep's algebra
def Wz(z):
    return z[0] * z[3] - z[1] * z[2]


def cross_term(z, d):   # Im(conj(z_now) d_before) + Im(conj(d_now) z_before)
    return (z[0] * d[3] - z[1] * d[2]) + (d[0] * z[3] - d[1] * z[2])


bad = 0
for _ in range(20000):
    z = tuple(rng.randint(-10 ** 9, 10 ** 9) for _ in range(4))
    d = tuple(rng.randint(-10 ** 9, 10 ** 9) for _ in range(4))
    zd = tuple(p + q for p, q in zip(z, d))
    bad += Wz(zd) - Wz(z) != Wz(d) + cross_term(z, d)
report("F4 W(z + d) - W(z) = W(d) + X(z, d)", bad, 20000)
A_, B_ = 125, 144
e = A_ * B_
bad = 0
for q in range(1, 30):
    for sig in (1, -1):
        bad += Wz((q * sig * A_, 0, 0, q * B_)) != q * q * sig * e
report("F4 q fitted hands as one hand carry q q sigma e", bad, 58)
bad = n_ = 0
for k in range(1, 7):
    for sig in itertools.product((1, -1), repeat=k):
        z = (sum(sig) * A_, 0, 0, k * B_)
        n_ += 1
        bad += Wz(z) - sum(sig) * e != (k - 1) * sum(sig) * e
report("F4 k fitted hands at one Node-clock: excess (k - 1)(SUM sigma) e", bad, n_)

# ------------------------------------------------------------------ F2's cost: the fitted hand on zero gears
def lone_wind(pinion, X, sign):
    """The fitted hand (sign A, i B) alone on zero gears at x, the window's carried wind, by my numerator."""
    g = {x: (6 * RIM * GAM ** 2 * GU * GU, None, None, X) for x in CL}
    for x in CL:
        w = g[x][0]
        D = 12 * (RIM - pinion) * GAM ** 2 * GU * GU
        R = [2 * GAM ** 2 * GU * GU * pinion] * 6
        g[x] = (w, w + w - D - sum(R), R, X)
    f = {x: (0, 0, 0, 0) for x in CL}
    x = (1, 2, 3)
    f[x] = (sign * A_, 0, 0, B_)
    return wwind(f, g, x)


W_L = 3 * KEY * RIM
costs = {p: lone_wind(p, GAM, s) for p in (15162854575528411, 2458210083751875, 2580388913625285, RIM) for s in (1, -1)}
out.append(f"F2 the fitted hand's wind on zero gears at the vacuum, per pinion and sense: {sorted(set(costs.values()))}")
out.append(f"   3 rim (A^2 + B^2) = {3 * RIM * (A_ * A_ + B_ * B_)}; over the light winding 3 key rim:"
           f" {Fraction(A_ * A_ + B_ * B_, KEY)} = {float(Fraction(A_ * A_ + B_ * B_, KEY)) * 1e6:.1f} millionths")
print("\n".join(out))
