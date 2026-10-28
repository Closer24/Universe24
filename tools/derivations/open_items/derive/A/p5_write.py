"""P5, the click of a whole's write as formulas (F1 to F5) in the three operations, and their property tests.

Pure integers, no engine code in the formulas: a torus of side L, every Node-clock holding one hand of each train
named here (z_now, z_before as Gaussian integers, spelt (n3, n12, b3, b12)), each Node-clock its gearing
(teeth w, hold S, six grips R_j, stretch X), the wind's carry M = 4 Gamma^3 G^2 (hands.wind's own form).
The formulas:
  sgn(n)        = n div (n n + 1) - (-n) div (n n + 1)
  [n >= 0]      = 1 + n div (n n + 1)                       (n div (n n + 1) is -1 below 0, else 0)
  [n = 0]       = 1 + (-n n) div (n^4 + 1)
  ceil(n / d)   = (n + d - 1) div d                         (d > 0)
  F1 the senses at a Mesh: sigma_e = sgn(h F_(o,e))
  F3 the take (the payer's unwind by a due D at one Node-clock): the steepest unit u, the least count by the ladder
     s -> ceil(D M / (P - a |u|^2 s)) from ceil(D M / P) to its fixed point, the zero where the integer vertex
     cannot pay; its inverse (the advance by a due) by the ladder s -> s - (R(s) - D M) div (R(s) - R(s - 1))
     from ceil(D M / P) down to its fixed point.
  F4 the charge book: the write is made only where c_T dQ_T = 0.
  F5 the unspringing at an end: the hand unwound whole, (released + r) = q w_l + r' (Rule3), the payer advanced by
     q w_l, the books per cell.
  F2 the fitting: sigma_e (A, i B) on the drawn train at each end e, each end's payer paying its own child.
Tests (each can fail): the sign lemmas; F1 against the head's meshes.train_lead and train_twists bit for bit and
under the 48 (rotations alike, reflections exchanged); F3's least count, its books and bounds, its rewind, its
covariance under the hand's units (i, -1, -i) and the conjugation and under the 48; F5's and F2's books, charge,
rewind and the 48.

argv: the head's worktree (for the bit-for-bit cross-check of the lead and the twist), the random draws.
"""
import sys
import itertools
import random
WT = sys.argv[1]
sys.path[:0] = [WT + '/src', WT]
from collections import Counter
import numpy as np

DRAWS = int(sys.argv[2]) if len(sys.argv) > 2 else 200
rng = random.Random(20261028)
stats = Counter()

# ---------------------------------------------------------------- the three operations' lemmas
def sgn(n):
    d = n * n + 1
    return n // d - (-n) // d


def ge0(n):  # [n >= 0]
    return 1 + n // (n * n + 1)


def is0(n):  # [n = 0]
    return 1 + (-n * n) // (n * n * n * n + 1)


def cdiv(n, d):  # ceil(n / d), d > 0
    return (n + d - 1) // d


# ---------------------------------------------------------------- the torus and the 48
L = 5
AXES = 3
SPOKES = [(a, s) for a in range(AXES) for s in (1, -1)]  # [+X, -X, +Y, -Y, +Z, -Z], the head's order
CLOCKS = list(itertools.product(range(L), repeat=AXES))


def nb(x, j):
    a, s = SPOKES[j]
    y = list(x)
    y[a] = (y[a] + s) % L
    return tuple(y)


IMAGES = [np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)])
          for pi in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]


def img(m, x):
    return tuple(int(v) % L for v in m @ np.array(x))


def img_spoke(m, j):
    a, s = SPOKES[j]
    v = m @ np.array([s if b == a else 0 for b in range(3)])
    a2 = next(b for b in range(3) if v[b] != 0)
    return SPOKES.index((a2, int(v[a2])))


def det(m):
    """The determinant of a 3 x 3 integer matrix in integers (products and sums alone)."""
    m = [[int(v) for v in row] for row in m]
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


# ---------------------------------------------------------------- the calibre's integers (the head's)
RIM, GAMMA, KEY = 15162856759112389, 1000, 36000
GU = 16  # the mesh unit G at Gamma 1,000 (rule3.mesh_unit_of)
M = 4 * GAMMA ** 3 * GU * GU  # the wind's carry (hands.wind: 2 wind_weight)
W_LIGHT = 3 * KEY * RIM  # the unsprung hand's winding (rule3.winding_of at s = rim)
A_CHILD, B_CHILD = 125, 144  # the fitted hand's notches, A B = KEY div 2 (the head's balanced_notches)


def gearing(pinion, rng_=None):
    """Rule3's integers at every Node-clock: at the vacuum, or with a random stretch and random mesh factors."""
    g = {}
    for x in CLOCKS:
        X = GAMMA if rng_ is None else rng_.randint(GAMMA // 2, 2 * GAMMA)
        q = [GU * GU] * 6 if rng_ is None else [rng_.randint(GU * GU // 2, GU * GU) for _ in range(6)]
        w = 6 * RIM * GAMMA ** 2 * GU * GU
        D = 12 * (RIM - pinion) * GAMMA ** 2 * GU * GU
        R = [2 * GAMMA ** 2 * qj * pinion for qj in q]
        g[x] = (w, w + w - D - sum(R), R, X)
    return g


def image_gearing(m, g):
    out = {}
    for x, (w, S, R, X) in g.items():
        R2 = [0] * 6
        for j in range(6):
            R2[img_spoke(m, j)] = R[j]
        out[img(m, x)] = (w, S, R2, X)
    return out


# ---------------------------------------------------------------- the wind (hands.wind's form, per gear)
def num_gear(f, g, c, k):
    """The wind's numerator of gear k (0 the three, 1 the twelve) at the Node-clock c: (2 own - shared) X."""
    w, S, R, X = g[c]
    n, b = f[c][k], f[c][2 + k]
    gripped = sum(R[j] * f[nb(c, j)][2 + k] for j in range(6))
    shared = sum(R[j] * (b - f[nb(c, j)][2 + k]) * (n + f[nb(c, j)][k]) for j in range(6))
    own = w * (n * n + b * b) - S * n * b - n * gripped
    return (own + own - shared) * X


def wind_at(f, g, c):
    return sum(num_gear(f, g, c, k) // M for k in range(2))


def window(x):
    return [x] + [nb(x, j) for j in range(6)]


def wwind(f, g, x):
    return sum(wind_at(f, g, c) for c in window(x))


def wnum(f, g, x, k):
    return sum(num_gear(f, g, c, k) for c in window(x))


def with_now(f, x, d):
    f2 = dict(f)
    n3, n12, b3, b12 = f[x]
    f2[x] = (n3 + d[0], n12 + d[1], b3, b12)
    return f2


def W(z):  # the sweep Im(conj(z_now) z_before)
    n3, n12, b3, b12 = z
    return n3 * b12 - n12 * b3


# ---------------------------------------------------------------- F1, the lead, the twist, the senses
def lead(f, x, y):  # F_(x, y) = SUM over the gears (now_x before_y - before_x now_y)
    return sum(f[x][k] * f[y][2 + k] - f[x][2 + k] * f[y][k] for k in range(2))


def twist(f, x, a):
    """h at the Mesh (x, x + e_a): the cross of the two ends' (u_b, u_c), u_b(k) = F(k, k - e_b) - F(k, k + e_b)."""
    b, c = (a + 1) % 3, (a - 1) % 3
    y = nb(x, SPOKES.index((a, 1)))

    def u(k, ax):
        return lead(f, k, nb(k, SPOKES.index((ax, -1)))) - lead(f, k, nb(k, SPOKES.index((ax, 1))))

    return u(x, b) * u(y, c) - u(x, c) * u(y, b)


def senses(f, x, a):
    """F1 at the Mesh (x, y = x + e_a): sigma_x = sgn(h F_(y,x)), sigma_y = sgn(h F_(x,y))."""
    y = nb(x, SPOKES.index((a, 1)))
    h, F = twist(f, x, a), lead(f, x, y)
    return {x: sgn(h * (-F)), y: sgn(h * F)}, h, F


# ---------------------------------------------------------------- F3, the take and its inverse
def pull_of(f, g, x):
    """The wind's pull on each gear at x (exact central differences of the window's numerator), its curvature."""
    G, A = [], []
    for k in range(2):
        e = [1 if j == k else 0 for j in range(2)]
        N0 = wnum(f, g, x, k)
        Np = wnum(with_now(f, x, e), g, x, k)
        Nm = wnum(with_now(f, x, [-v for v in e]), g, x, k)
        G.append((Np - Nm) // 2)
        A.append((Np + Nm - N0 - N0) // 2)
    return G, A


def unit(G, toward):
    """The steepest unit, both gears where tied: u_k = toward sgn(G_k) [G_k^2 >= G_l^2] (toward -1 falls, +1 rises)."""
    return [toward * sgn(G[k]) * ge0(G[k] * G[k] - G[1 - k] * G[1 - k]) for k in range(2)]


def take(f, g, x, D):
    """The payer at x unwound by the due D (wind units). Returns (u, s, fall) or None (the zero: cannot pay)."""
    G, A = pull_of(f, g, x)
    a = A[0]
    u = unit(G, -1)
    u2 = u[0] * u[0] + u[1] * u[1]
    P = -(u[0] * G[0] + u[1] * G[1])
    a2 = a * u2
    if u2 == 0 or P <= 0:
        return None
    sv = (P + a2) // (a2 + a2)  # the integer vertex
    Dp = D * M
    if sv * P - a2 * sv * sv < Dp:
        return None
    s, steps = cdiv(Dp, P), 0
    while True:  # the ladder of carries, monotone from below to the least count
        nxt = cdiv(Dp, P - a2 * s)
        if nxt == s:
            break
        s, steps = nxt, steps + 1
    stats["F3 takes: the ladder's carries past the first (largest)"] = max(
        stats["F3 takes: the ladder's carries past the first (largest)"], steps)
    d = [s * u[0], s * u[1]]
    fall = wwind(f, g, x) - wwind(with_now(f, x, d), g, x)
    return u, s, fall


def advance(f, g, x, D):
    """The payee at x advanced by the due D (wind units), the least count by the backward ladder."""
    G, A = pull_of(f, g, x)
    a = A[0]
    u = unit(G, 1)
    if u[0] == 0 and u[1] == 0:
        u = [1, 0]  # a payee with no pull at all: its three gear (a still hand rises the same either way)
        stats["F5 advances from a hand with no pull (the three gear by name: OPEN)"] += 1
    u2 = u[0] * u[0] + u[1] * u[1]
    P = u[0] * G[0] + u[1] * G[1]
    a2 = a * u2
    Dp = D * M
    R = lambda s: s * P + a2 * s * s
    s = cdiv(Dp, P) if P > 0 else 1
    while R(s) < Dp:  # (only where P is 0: the rise is the curvature's alone)
        s = s + s
    while True:  # the backward ladder: monotone from above to the least count
        step = (R(s) - Dp) // (R(s) - R(s - 1)) if s > 0 else 0
        if step == 0:
            break
        s = s - step
    d = [s * u[0], s * u[1]]
    rise = wwind(with_now(f, x, d), g, x) - wwind(f, g, x)
    return u, s, rise


# ---------------------------------------------------------------- random fields
def light_field(amp=6000, vel=600):
    f = {}
    for x in CLOCKS:
        n3, n12 = rng.randint(-amp, amp), rng.randint(-amp, amp)
        f[x] = (n3, n12, n3 + rng.randint(-vel, vel), n12 + rng.randint(-vel, vel))
    return f


def image_field(m, f):
    return {img(m, x): v for x, v in f.items()}


# ---------------------------------------------------------------- tests
def test_lemmas():
    bad = 0
    for n in list(range(-3000, 3001)) + [10 ** 30 + 1, -(10 ** 30 + 1), 2 ** 150, -(2 ** 150)]:
        bad += sgn(n) != (n > 0) - (n < 0)
        bad += ge0(n) != int(n >= 0)
        bad += is0(n) != int(n == 0)
    for n in range(-200, 201):
        for d in range(1, 40):
            bad += cdiv(n, d) != -((-n) // d)
    stats["lemmas (sgn, [n >= 0], [n = 0], ceil) off"] += bad


def test_f1_against_head():
    """The pure lead and twist against the head's meshes.train_lead and train_twists on one random field."""
    from event_universe.meshes import train_lead, train_twists
    from event_universe.trains import Gear
    f = light_field()
    arr = lambda k: np.array([[[f[(i, j, l)][k] for l in range(L)] for j in range(L)] for i in range(L)], dtype=object)
    gears = [Gear(arr(0), arr(2), None, None), Gear(arr(1), arr(3), None, None)]
    tw = train_twists(gears)
    bad = 0
    for x in CLOCKS:
        for a in range(3):
            y = nb(x, SPOKES.index((a, 1)))
            bad += int(train_lead(gears, SPOKES.index((a, 1)))[x]) != lead(f, x, y)
            bad += int(tw[a][x]) != twist(f, x, a)
    stats["F1: the pure lead and twist against the head's, Meshes read"] += L ** 3 * 3
    stats["F1: ... off"] += bad


def test_f1_images(draws):
    for _ in range(draws):
        f = light_field()
        base = {}
        for x in CLOCKS:
            for a in range(3):
                sig, h, F = senses(f, x, a)
                base[(x, a)] = sig
        for m in IMAGES:
            fm = image_field(m, f)
            dm = det(m)
            for (x, a), sig in base.items():
                y = nb(x, SPOKES.index((a, 1)))
                xm, ym = img(m, x), img(m, y)
                j = img_spoke(m, SPOKES.index((a, 1)))
                am, sm = SPOKES[j]
                lo = xm if sm == 1 else ym  # the image Mesh's +a end
                sigm, _, _ = senses(fm, lo, am)
                ok = sigm[xm] == dm * sig[x] and sigm[ym] == dm * sig[y]
                stats[f"F1 images: Meshes read under {'rotations' if dm == 1 else 'reflections'}"] += 1
                stats[f"F1 images: ... sigma(image) = {'+' if dm == 1 else '-'}sigma"] += int(ok)
                stats["F1: sigma_x + sigma_y = 0"] += int(sig[x] + sig[y] == 0)


def test_take(draws):
    for t in range(draws):
        f = light_field()
        g = gearing(RIM, rng if t % 2 else None)  # the unsprung hand's gearing: the vacuum, or random rates
        x = rng.choice(CLOCKS)
        G, A = pull_of(f, g, x)
        u = unit(G, -1)
        P = -(u[0] * G[0] + u[1] * G[1])
        a2 = A[0] * (u[0] ** 2 + u[1] ** 2)
        sv = (P + a2) // (a2 + a2) if a2 else 0
        fmax = (sv * P - a2 * sv * sv) // M
        if fmax < 2:
            continue
        D = rng.randint(1, fmax)
        got = take(f, g, x, D)
        stats["F3 takes made (a due at most the integer vertex's fall)"] += 1
        if got is None:
            stats["F3 takes: refused below the vertex (must be 0)"] += 1
            continue
        u, s, fall = got
        # the least count: s - 1 does not pay on the exact numerator
        pays = lambda s_: s_ * P - a2 * s_ * s_ >= D * M
        stats["F3 takes: the count is the least on the numerator"] += int(pays(s) and not pays(s - 1))
        stats["F3 takes: the window's fall (with its carries) within [D - 14, D + one unit's fall + 15)"] += int(
            D - 14 <= fall < D + P // M + 15)
        # the books: the remainder r' = r + fall - D, the wind and the remainder summed kept exactly
        r = rng.randint(-10 ** 6, 10 ** 6)
        f2 = with_now(f, x, [s * u[0], s * u[1]])
        r2 = r + fall - D
        board_fall = sum(wind_at(f, g, c) for c in CLOCKS) - sum(wind_at(f2, g, c) for c in CLOCKS)
        stats["F3 takes: the whole great clock's fall is the window's (the write is local)"] += int(board_fall == fall)
        stats["F3 takes: the books (every wind and the remainder) exact, the due booked"] += int(
            (board_fall + r) - r2 == D)
        # the rewind from the click's record (x, u, s, D): the gear moved back, the fall re-read, r restored
        f3 = with_now(f2, x, [-s * u[0], -s * u[1]])
        fall_back = wwind(f3, g, x) - wwind(f2, g, x)
        stats["F3 takes: the rewind bit for bit (the field and the remainder)"] += int(f3 == f and r2 - fall_back + D == r)
        # the hand's units and the conjugation: z -> i z, -z, -i z, conj z, at every Node-clock
        for name, mapz, mapu in (
            ("i", lambda z: (-z[1], z[0], -z[3], z[2]), lambda v: [-v[1], v[0]]),
            ("-1", lambda z: (-z[0], -z[1], -z[2], -z[3]), lambda v: [-v[0], -v[1]]),
            ("-i", lambda z: (z[1], -z[0], z[3], -z[2]), lambda v: [v[1], -v[0]]),
            ("conj", lambda z: (z[0], -z[1], z[2], -z[3]), lambda v: [v[0], -v[1]]),
        ):
            fz = {c: mapz(v) for c, v in f.items()}
            gz = take(fz, g, x, D)
            ok = gz is not None and gz[0] == mapu(u) and gz[1] == s and gz[2] == fall
            stats[f"F3 takes: covariant under z -> {name} z (the unit turned, the count and the fall kept)"] += int(ok)
        # the 48: the field and the gearing imaged, the take at the image Node-clock
        m = IMAGES[rng.randrange(48)]
        gm = take(image_field(m, f), image_gearing(m, g), img(m, x), D)
        stats["F3 takes: alike at the image under one of the 48 drawn"] += int(gm == got)
        # the inverse: the advance of the same due from the post-state returns to a state within the unit
        ua, sa, rise = advance(f2, g, x, D)
        stats["F3 inverse: the advance of the due from the post-state rises at least D - 14"] += int(D - 14 <= rise)
        Ga, Aa = pull_of(f2, g, x)
        Pa = ua[0] * Ga[0] + ua[1] * Ga[1]
        stats["F3 inverse: ... and at most D + its last unit's rise + 15"] += int(
            rise < D + (Pa + Aa[0] * (ua[0] ** 2 + ua[1] ** 2) * (2 * sa - 1)) // M + 15)


def board(fs_gs):
    return sum(wind_at(f, g, c) for f, g in fs_gs for c in CLOCKS)


def at_clock(fs_gs, c):
    return sum(wind_at(f, g, c) for f, g in fs_gs)


def books_per_end(pre, post, alone, ends):
    """The order-free book (DAVID-THE-ORDER-FREE-STRIKE.md): each end books its own write's fall over every train,
    read alone on the start board, and every Node-clock books the cross term arising there (the board's change
    there less the changes the writes make there read alone).  `alone[e]` is the state with e's write alone.
    Returns {clock: the remainder's change} (positive: wind the remainder gains)."""
    change = {}
    for e in ends:
        change[e] = change.get(e, 0) + (board(pre) - board(alone[e]))
    for c in CLOCKS:
        k = (at_clock(pre, c) - at_clock(post, c)) - sum(at_clock(pre, c) - at_clock(alone[e], c) for e in ends)
        if k:
            change[c] = change.get(c, 0) + k
    return change


def test_unspringing_and_fitting(draws):
    """F2 and F5 on a light and one coupled train at a Mesh: every take and every advance read on the start board
    (the order-free click), the moves written together, the books per end (each write's own fall read alone, the
    cross terms where they arise), the charge, the rewind, the 48."""
    pin = 2458210083751875  # a heavy pinion of the toy calibre
    for t in range(draws):
        light = light_field(4000, 400)
        T = {x: (0, 0, 0, 0) for x in CLOCKS}
        gl = gearing(RIM, rng if t % 2 else None)
        gT = gearing(pin, None)
        x = rng.choice(CLOCKS)
        a = rng.randrange(3)
        y = nb(x, SPOKES.index((a, 1)))
        sig, h, F = senses(light, x, a)
        if sig[x] == 0:
            continue
        stats["F2 fittings: read"] += 1
        child = {e: (sig[e] * A_CHILD, 0, 0, B_CHILD) for e in (x, y)}
        T2 = dict(T)
        for e in (x, y):
            T2[e] = tuple(p_ + q_ for p_, q_ in zip(T[e], child[e]))
        dQ = sum(W(T2[e]) - W(T[e]) for e in (x, y))
        stats["F2 fittings: the charge moved dQ_T = 0 on zero gears"] += int(dQ == 0)
        dues = {}
        for e in (x, y):
            alone = {c: (0, 0, 0, 0) for c in CLOCKS}
            alone[e] = child[e]
            dues[e] = sum(wind_at(alone, gT, c) for c in window(e))
        got = {e: take(light, gl, e, dues[e]) for e in (x, y)}  # both read on the start board
        if any(v is None for v in got.values()):
            stats["F2 fittings: an end's light cannot pay its own child (the zero, nothing written)"] += 1
            continue
        L2 = dict(light)
        for e in (x, y):
            u, s, _fall = got[e]
            n3, n12, b3, b12 = L2[e]
            L2[e] = (n3 + s * u[0], n12 + s * u[1], b3, b12)
        # the two takes commute: the light's joint fall is the sum of the two alone, within the carries
        joint = board([(light, gl)]) - board([(L2, gl)])
        stats["F2 fittings: the two light takes' joint fall = the sum alone, within 4 (no now-now cross term)"] += int(
            abs(joint - got[x][2] - got[y][2]) <= 4)
        pre, post = [(light, gl), (T, gT)], [(L2, gl), (T2, gT)]
        alone = {}
        for e in (x, y):
            Le = dict(light)
            u, s, _fall = got[e]
            n3, n12, b3, b12 = Le[e]
            Le[e] = (n3 + s * u[0], n12 + s * u[1], b3, b12)
            Te = dict(T)
            Te[e] = T2[e]
            alone[e] = [(Le, gl), (Te, gT)]
        r0 = {c: rng.randint(-10 ** 9, 10 ** 9) for c in CLOCKS}
        ch = books_per_end(pre, post, alone, (x, y))
        r1 = {c: r0[c] + ch.get(c, 0) for c in CLOCKS}  # the light's fall less the train's rise, per end
        stats["F2 fittings: the books close exactly (every wind and every remainder)"] += int(
            board(pre) + sum(r0.values()) == board(post) + sum(r1.values()))
        stats["F2 fittings: the cross terms arise at the two ends alone"] += int(set(ch) <= {x, y})
        for e in (x, y):
            Ge, Ae = pull_of(light, gl, e)
            ue = got[e][0]
            unit_fall = -(ue[0] * Ge[0] + ue[1] * Ge[1]) // M + 15  # one unit's fall at e (and the carries)
            kappa = (at_clock(pre, e) - at_clock(post, e)) - sum(at_clock(pre, e) - at_clock(alone[f_], e) for f_ in (x, y))
            moved_by = r1[e] - r0[e]
            stats["F2 fittings: an end's remainder moved within [kappa, kappa + one unit's fall) (the take's overpay)"] += int(
                kappa - 15 <= moved_by < kappa + unit_fall)
            stats["F2 fittings: |the cross term at an end| below a hundredth of a light winding"] += int(
                100 * abs(kappa) < W_LIGHT)
        # the rewind from the record (each end's u and s, the children's senses)
        L3 = dict(L2)
        T3 = dict(T2)
        for e in (x, y):
            u, s, _fall = got[e]
            n3, n12, b3, b12 = L3[e]
            L3[e] = (n3 - s * u[0], n12 - s * u[1], b3, b12)
            T3[e] = tuple(p_ - q_ for p_, q_ in zip(T2[e], child[e]))
        stats["F2 fittings: the rewind bit for bit (the light, the train; the remainders by the same book at -1)"] += int(
            L3 == light and T3 == T)
        # F5: the unspringing of the pair just laid (the fitting read backward as its own click)
        WTx, WTy = W(T2[x]), W(T2[y])
        stats["F5 unspringings: the pair's charge W_x + W_y = 0, the gate open"] += is0(WTx + WTy)
        T4 = dict(T2)
        T4[x], T4[y] = (0, 0, 0, 0), (0, 0, 0, 0)
        released = {}
        for e in (x, y):
            Te = dict(T2)
            Te[e] = (0, 0, 0, 0)
            released[e] = board([(T2, gT)]) - board([(Te, gT)])  # each end's release read alone
        qr = {e: divmod(released[e] + r1[e], W_LIGHT) for e in (x, y)}
        for e in (x, y):
            stats["F5 unspringings: the end's Rule3 remainder in [0, one light winding)"] += int(0 <= qr[e][1] < W_LIGHT)
            stats[f"F5 unspringings: whole light windings written at an end: {qr[e][0]}"] += 1
        adv = {e: advance(L2, gl, e, qr[e][0] * W_LIGHT) for e in (x, y) if qr[e][0] > 0}
        L4 = dict(L2)
        for e, (u, s, _rise) in adv.items():
            n3, n12, b3, b12 = L4[e]
            L4[e] = (n3 + s * u[0], n12 + s * u[1], b3, b12)
        alone = {}
        for e in (x, y):
            Le = dict(L2)
            if e in adv:
                u, s, _rise = adv[e]
                n3, n12, b3, b12 = Le[e]
                Le[e] = (n3 + s * u[0], n12 + s * u[1], b3, b12)
            Te = dict(T2)
            Te[e] = (0, 0, 0, 0)
            alone[e] = [(Le, gl), (Te, gT)]
        pre, post = [(L2, gl), (T2, gT)], [(L4, gl), (T4, gT)]
        ch = books_per_end(pre, post, alone, (x, y))
        r2 = {c: r1[c] + ch.get(c, 0) for c in CLOCKS}
        stats["F5 unspringings: the books close exactly"] += int(
            board(pre) + sum(r1.values()) == board(post) + sum(r2.values()))
        for e in (x, y):
            stats["F5 unspringings: the end's final remainder in (-(one light winding), one light winding)"] += int(
                -W_LIGHT < r2[e] - r0[e] < W_LIGHT)
        stats["F5 unspringings: the charge moved = -(W_x + W_y) exactly"] += int(
            W(T4[x]) + W(T4[y]) - WTx - WTy == -(WTx + WTy))
        m = IMAGES[rng.randrange(48)]
        lm = image_field(m, light)
        j = img_spoke(m, SPOKES.index((a, 1)))
        am, sm = SPOKES[j]
        xm, ym = img(m, x), img(m, y)
        lo = xm if sm == 1 else ym
        sigm, _, _ = senses(lm, lo, am)
        stats["F2 fittings: under one drawn image the children at the image ends, exchanged by a reflection"] += int(
            sigm[xm] == det(m) * sig[x] and sigm[ym] == det(m) * sig[y])


test_lemmas()
test_f1_against_head()
test_f1_images(max(1, DRAWS // 100))
test_take(DRAWS)
test_unspringing_and_fitting(max(1, DRAWS // 4))
print("P5 the write's formulas, random draws", DRAWS)
for k in stats:
    print(f"  {k}: {stats[k]}")
