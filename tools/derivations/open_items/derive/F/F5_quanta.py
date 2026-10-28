"""F5: one field per train and its quanta (draft F; root III items 17, 18, 19 and 24).

Exact integers and Fractions only, no float. Run: python3 -I F5_quanta.py [MUTANT]
MUTANT: none (default), centred (the centred lead read as the Mesh's flux), permanent (the boson's
two ways added with the sign -1), token (the token's hop sized by the centred lead), hold (the uniform
mode given a hold). Each mutant must make at least one check FAIL.

 A. the sweep Q = SUM Im(conj(z-) z) is the exact charge of the one formula's linear step at any hold,
    with the continuity equation per Node-clock per tick and the flux on the Mesh
    Phi(x -> x + e) = -mu Im(conj(z_x) z_(x+e)) at the middle slot (the lead of the link's bilinear);
 B. on the side-4 torus, exact one-signed waves (Pythagorean cos and sin, a train r = 3/5): the wind of a
    mode is 2 sin(w) times its sweep, so the sweep is the action per mode, the wind over the lattice's
    frequency 2 sin w: a click that reads the sweep at the key gives E = n key 2 sin w per mode; a standing
    wave has wind and no sweep;
 C. the n-quantum click of law 7 at a balanced splitter M = [[1, i], [i, 1]]: two bosons' coincidence
    amplitude per M = 0 (Hong, Ou and Mandel's dip), two twin quanta's det M = 2 (always apart), one
    quantum half and half; the odds exact;
 D. a token per quantum hopping by the sizes of the conserved flux (Bell's beables): its law of position
    is carried exactly by the sweep wherever the sizes are non-negative; the cases where they are not
    are counted;
 E. recurrence: the integer one formula on a small ring returns exactly to its setting (a bijection's
    bounded orbit is a cycle), while the massless uniform mode at the hold 0 drifts for ever.
"""

import itertools
import random
import sys
from fractions import Fraction as Fr

MUT = sys.argv[1] if len(sys.argv) > 1 else "none"
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" : " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def conj(a):
    return (a[0], -a[1])


def cadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def csc(k, a):
    return (k * a[0], k * a[1])


def im_cx(a, b):  # Im(conj(a) b)
    return a[0] * b[1] - a[1] * b[0]


def re_cx(a, b):
    return a[0] * b[0] + a[1] * b[1]


L = 4
SITES = list(itertools.product(range(L), repeat=3))
SP = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def nb(x, d):
    return ((x[0] + d[0]) % L, (x[1] + d[1]) % L, (x[2] + d[2]) % L)


def step(now, before, h, mu):
    out = {}
    for x in SITES:
        s = (Fr(0), Fr(0))
        for d in SP:
            s = cadd(s, now[nb(x, d)])
        out[x] = cadd(cadd(csc(h, now[x]), csc(mu, s)), csc(-1, before[x]))
    return out


rng = random.Random(5)
# ---------------------------------------------------------------- A. charge and continuity
for name, h, mu in (("light at the edge", Fr(0), Fr(1, 3)), ("a train below the edge", Fr(1, 2), Fr(1, 5))):
    now = {x: (Fr(rng.randint(-20, 20)), Fr(rng.randint(-20, 20))) for x in SITES}
    before = {x: (Fr(rng.randint(-20, 20)), Fr(rng.randint(-20, 20))) for x in SITES}
    Q0 = sum(im_cx(before[x], now[x]) for x in SITES)
    cons, cont = True, True
    for t in range(10):
        nxt = step(now, before, h, mu)
        for x in SITES:
            drho = im_cx(now[x], nxt[x]) - im_cx(before[x], now[x])
            if MUT == "centred":
                flux = sum(-mu * Fr(1, 2) * (im_cx(now[x], now[nb(x, d)]) - im_cx(now[x], now[nb(x, (-d[0], -d[1], -d[2]))])) for d in SP)
            else:
                flux = sum(-mu * im_cx(now[x], now[nb(x, d)]) for d in SP)
            cont = cont and drho == -flux
        before, now = now, nxt
        cons = cons and sum(im_cx(before[x], now[x]) for x in SITES) == Q0
    check(f"A1 [{name}] the sweep is the exact charge over 10 ticks", cons, f"Q = {Q0}")
    check(f"A2 [{name}] continuity at every Node-clock and tick, the flux the Mesh's lead at the middle slot", cont)

# ---------------------------------------------------------------- B. the action per mode
r = Fr(3, 5)
mu = r / 3
modes = [  # (wave function v(x), its (cos w, sin w))
    (lambda x: (Fr(1), Fr(0)), (Fr(3, 5), Fr(4, 5))),  # k = 0: cos w = r
    (lambda x: [(Fr(1), Fr(0)), (Fr(0), Fr(1)), (Fr(-1), Fr(0)), (Fr(0), Fr(-1))][(x[0] + x[1] + x[2]) % 4], (Fr(0), Fr(1))),  # k = (pi/2)^3: cos w = 0
]


def mode_field(coeffs, t, signs):
    f = {x: (Fr(0), Fr(0)) for x in SITES}
    for (v, (c, s)), A, sg in zip(modes, coeffs, signs):
        U = (c, -sg * s)  # e^(-i sg w)
        Ut = (Fr(1), Fr(0))
        for _ in range(t) if t >= 0 else []:
            Ut = cmul(Ut, U)
        if t < 0:
            Ui = conj(U)  # |U| = 1
            for _ in range(-t):
                Ut = cmul(Ut, Ui)
        for x in SITES:
            f[x] = cadd(f[x], cmul(cmul(A, Ut), v(x)))
    return f


def wind(now, before, h, mu_):
    tot = Fr(0)
    for x in SITES:
        a, b = now[x], before[x]
        s = csc(h, b)
        for d in SP:
            s = cadd(s, csc(mu_, before[nb(x, d)]))
        tot += a[0] ** 2 + a[1] ** 2 + b[0] ** 2 + b[1] ** 2 - re_cx(a, s)
    return tot


A1, A2 = (Fr(3), Fr(-2)), (Fr(1), Fr(4))
ok_sol = True
z_b, z_n = mode_field([A1, A2], -1, [1, 1]), mode_field([A1, A2], 0, [1, 1])
for t in range(1, 6):
    nxt = step(z_n, z_b, Fr(0), mu)
    ok_sol = ok_sol and nxt == mode_field([A1, A2], t, [1, 1])
    z_b, z_n = z_n, nxt
check("B1 the two waves (k = 0, cos 3/5; k = (pi/2)^3, cos 0) solve the one formula exactly for the train r = 3/5", ok_sol)
E_tot = wind(mode_field([A1, A2], 0, [1, 1]), mode_field([A1, A2], -1, [1, 1]), Fr(0), mu)
parts = []
for i, ((v, (c, s)), A) in enumerate(zip(modes, [A1, A2])):
    coeffs = [A if j == i else (Fr(0), Fr(0)) for j in range(2)]
    n0, b0 = mode_field(coeffs, 0, [1, 1]), mode_field(coeffs, -1, [1, 1])
    Em = wind(n0, b0, Fr(0), mu)
    Qm = sum(im_cx(n0[x], b0[x]) for x in SITES)  # Im(conj(z) z-): positive for e^(-i w t)
    parts.append((Em, Qm, s))
    print(f"   mode {i}: wind {Em}, sweep {Qm}, sin w {s}; wind / (2 sin w) = {Em / (2 * s)}")
Q_tot = sum(im_cx(mode_field([A1, A2], 0, [1, 1])[x], mode_field([A1, A2], -1, [1, 1])[x]) for x in SITES)
check("B2 for each one-signed mode the wind is 2 sin(w) times its sweep: the sweep is the action per mode",
      all(Em == 2 * s * Qm for Em, Qm, s in parts))
check("B3 the waves' winds and sweeps add (no cross terms over the torus): E = SUM 2 sin(w_m) Q_m, Q = SUM Q_m",
      E_tot == sum(2 * s * Qm for _, Qm, s in parts) and Q_tot == sum(Qm for _, Qm, _ in parts),
      f"E = {E_tot}, Q = {Q_tot}")
check("B4 no single frequency reads the sum: E != 2 sin(w) Q for either sin w", all(E_tot != 2 * s * Q_tot for _, _, s in parts))
st_n, st_b = mode_field([A1, A1], 0, [1, -1]), mode_field([A1, A1], -1, [1, -1])
# a standing wave of the k = 0 mode: both senses
sw_n = {x: cadd(mode_field([A1, (Fr(0), Fr(0))], 0, [1, 1])[x], mode_field([A1, (Fr(0), Fr(0))], 0, [-1, 1])[x]) for x in SITES}
sw_b = {x: cadd(mode_field([A1, (Fr(0), Fr(0))], -1, [1, 1])[x], mode_field([A1, (Fr(0), Fr(0))], -1, [-1, 1])[x]) for x in SITES}
check("B5 a standing wave of one mode (both senses) has wind and no sweep: the sweep counts the senses' difference",
      sum(im_cx(sw_n[x], sw_b[x]) for x in SITES) == 0 and wind(sw_n, sw_b, Fr(0), mu) > 0)

# ---------------------------------------------------------------- C. the n-quantum click at a splitter
M = [[(1, 0), (0, 1)], [(0, 1), (1, 0)]]  # [[1, i], [i, 1]]: each column's norm 2


def two_ways(m, sign):
    return cadd(cmul(m[0][0], m[1][1]), csc(sign, cmul(m[0][1], m[1][0])))


bos = two_ways(M, -1 if MUT == "permanent" else 1)
fer = two_ways(M, -1)
N = lambda a: a[0] * a[0] + a[1] * a[1]  # noqa: E731
# odds with the columns' norms (2 x 2 = 4) and the bosons' 1 / n! for two in one output
p_bos_11 = Fr(N(bos), 4)
p_bos_20 = Fr(N(csc(2, cmul(M[0][0], M[0][1]))), 4 * 2)
p_bos_02 = Fr(N(csc(2, cmul(M[1][0], M[1][1]))), 4 * 2)
p_fer_11 = Fr(N(fer), 4)
check("C1 two bosons, one per input: the two ways cancel (per M = 0), odds (1/2, 0, 1/2): Hong, Ou and Mandel's dip",
      bos == (0, 0) and (p_bos_20, p_bos_11, p_bos_02) == (Fr(1, 2), 0, Fr(1, 2)), f"per M = {bos}")
check("C2 two twin quanta: det M = 2, the coincidence certain (odds 1), never in one output", fer == (2, 0) and p_fer_11 == 1)
check("C3 one quantum: N(1) : N(i) = 1 : 1, the binomial partition", N(M[0][0]) == N(M[1][0]) == 1)

# ---------------------------------------------------------------- D. the token's hop (Bell's beables)
valid = invalid = 0
exact = True
z_b, z_n = mode_field([A1, A2], -1, [1, 1]), mode_field([A1, A2], 0, [1, 1])
for t in range(0, 8):
    z_x = step(z_n, z_b, Fr(0), mu)
    rho = {x: im_cx(z_n[x], z_b[x]) for x in SITES}  # the slab (t-1, t)
    rho_next = {x: im_cx(z_x[x], z_n[x]) for x in SITES}
    Q = sum(rho.values())
    flux = {}
    for x in SITES:
        for d in SP:
            if MUT == "token":
                back = nb(x, (-d[0], -d[1], -d[2]))
                flux[(x, d)] = mu * Fr(1, 2) * (im_cx(z_n[x], z_n[nb(x, d)]) - im_cx(z_n[x], z_n[back]))
            else:
                flux[(x, d)] = mu * im_cx(z_n[x], z_n[nb(x, d)])  # out of x toward x + d, for the density Im(conj(z) z-)
    P_next = {x: Fr(0) for x in SITES}
    ok_here = True
    for x in SITES:
        out = sum(max(Fr(0), flux[(x, d)]) for d in SP)  # the parts' sizes: the outflow on each Spoke
        stay = rho[x] - out
        if rho[x] <= 0 or stay < 0:
            ok_here = False
        P_next[x] += stay / Q
        for d in SP:
            P_next[nb(x, d)] += max(Fr(0), flux[(x, d)]) / Q
    if ok_here:
        valid += 1
        exact = exact and all(P_next[x] == rho_next[x] / Q for x in SITES)
    else:
        invalid += 1
    z_b, z_n = z_n, z_x
check("D1 where every size is non-negative the token's law of position is carried exactly as the sweep (Born for position)",
      exact and valid > 0, f"{valid} ticks with non-negative sizes, {invalid} with a negative size or density")

# ---------------------------------------------------------------- E. recurrence on a small ring
def ring_step(a, am, r, W, g, D, n):
    mid = (W - 1) // 2
    na, nr = [], []
    for i in range(n):
        F = g * (a[(i + 1) % n] - a[i]) + g * (a[(i - 1) % n] - a[i]) - D * a[i]
        pp = W * (a[i] - am[i]) + (r[i] - mid) + F
        na.append(a[i] + (pp + mid) // W)
        nr.append((pp + mid) % W)
    return na, list(a), nr


W, g, D, n = 9, 2, 3, 3  # 2 W - 2 g - D = 11 > 0 (a hold below the edge), a massive train
start = ([2, -1, 0], [1, 0, -1], [4, 4, 4])
state, period = start, None
seen_max = 0
for t in range(1, 200001):
    state = ring_step(*state, W, g, D, n)
    seen_max = max(seen_max, max(abs(v) for v in state[0]))
    if state == (list(start[0]), list(start[1]), list(start[2])):
        period = t
        break
check("E1 the integer one formula's orbit on a ring of 3 returns exactly to its setting (a bounded bijection's cycle)",
      period is not None, f"period {period}, largest notch {seen_max}")
# the massless uniform mode at the hold 0: every Node-clock alike with a velocity of one notch a tick
W2, g2 = 9, 9  # hold 2 W - 2 g = 0 on the ring (two Spokes)
a, am, r = [5, 5, 5], [4, 4, 4], [4, 4, 4]
hold = Fr(1, 1) if MUT == "hold" else 0
drift = []
for t in range(1, 41):
    if MUT == "hold":
        mid2 = (W2 - 1) // 2
        na, nr = [], []
        for i in range(3):
            F = g2 * (a[(i + 1) % 3] - a[i]) + g2 * (a[(i - 1) % 3] - a[i]) - 1 * a[i]
            pp = W2 * (a[i] - am[i]) + (r[i] - mid2) + F
            na.append(a[i] + (pp + mid2) // W2)
            nr.append((pp + mid2) % W2)
        a, am, r = na, list(a), nr
    else:
        a, am, r = ring_step(a, am, r, W2, g2, 0, 3)
    drift.append(a[0])
check("E2 the massless uniform mode at the hold 0 drifts by one notch a tick for ever (a double root: no recurrence)",
      drift == [5 + t for t in range(1, 41)], f"notch {drift[0]} .. {drift[-1]}")

print("RESULT:", "ALL PASS" if not FAILS else "FAILED " + ", ".join(FAILS))
