"""I2 (drafter I): the charge of the twin hands under the turnover T = i sigma_y K (draft E), exact rationals.

A twin hand is psi = (z1, z2), two Gaussian rationals, with its momentum P = (P1, P2). Its phase reversal is
T (z1, z2) = (-conj z2, conj z1), antilinear, T T = -1 (Kramers; draft E, P4 and P5).
Each Node-clock holds its turnover count c (mod 4): the stored twin is read in the frame Z = T^c psi.
The physical hop h_xy is a unit with h_yx = conj(h_xy). In the stored frame the neighbour is read as
    U psi_y = T^(-c_x) (h_xy T^(c_y) psi_y) = K^(c_x)(h_xy) T^(c_y - c_x) psi_y      (K^c(h) = h or conj h)
and the step is the toy's: P' = P + X F, F = SUM_j g_j (U psi_j - psi) - D psi + (an on-site Hermitian spin term),
psi' = psi + P' / w. The framed charge Q = -SUM_x (-1)^(c_x) lam_x Im<psi, P>, Im<Ta, Tb> = -Im<a, b>.
Run: python3 -I i2_twins.py [--mutant NAME]
Checks:
  D1 the twins' Mesh current antisymmetric, the frame count read modulo 4
  D2 Q kept to the last digit over 30 exact ticks with turnovers at random Node-clocks, the turnover applying
     T once (the count carries it, the slots exchanged with no T)
  D3 the three ways to apply T at the turnover: once in the count (kept), once in the gears with the count
     not advanced (kept), in both (reversed)
  D4 the stored dynamics equals the physical dynamics Z = T^c psi tick by tick (the frames read modulo 4)
Mutants: z2_frames (the count read modulo 2, T^-1 read as T), twice (T in the gears and in the count),
         no_frame_advance_fix (the slots exchanged with no T and the count not advanced).
"""
import random
import sys
from fractions import Fraction as Fr
from itertools import product

MUT = sys.argv[sys.argv.index('--mutant') + 1] if '--mutant' in sys.argv else ''
L = 3
SITES = list(product(range(L), repeat=3))
SPOKES = [(a, s) for a in range(3) for s in (1, -1)]
RES = []


def report(name, ok, detail):
    RES.append((name, ok))
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")


def nb(x, j):
    a, s = SPOKES[j]
    y = list(x)
    y[a] = (y[a] + s) % L
    return tuple(y)


def back(j):
    a, s = SPOKES[j]
    return SPOKES.index((a, -s))


def mul(p, q):
    return (p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0])


def conj(p):
    return (p[0], -p[1])


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def scl(c, p):
    return (c * p[0], c * p[1])


def neg(p):
    return (-p[0], -p[1])


def im_cb(p, q):
    return p[0] * q[1] - p[1] * q[0]


def T(v):                          # T (z1, z2) = (-conj z2, conj z1)
    return (neg(conj(v[1])), conj(v[0]))


def Tpow(n, v):
    n = n % 4
    for _ in range(n):
        v = T(v)
    return v


def vadd(u, v):
    return (add(u[0], v[0]), add(u[1], v[1]))


def vsub(u, v):
    return (sub(u[0], v[0]), sub(u[1], v[1]))


def vscl(c, v):
    return (scl(c, v[0]), scl(c, v[1]))


def vmul(h, v):                    # a complex scalar on both components
    return (mul(h, v[0]), mul(h, v[1]))


def vim(u, v):                     # Im <u, v>
    return im_cb(u[0], v[0]) + im_cb(u[1], v[1])


def unit_of(t):
    d = 1 + t * t
    return ((1 - t * t) / d, 2 * t / d)


def world(rng):
    W = {'T': Fr(10 ** 6)}
    W['X'] = {x: Fr(rng.randint(500, 1500)) for x in SITES}
    W['mr'] = {x: Fr(rng.randint(300, 1000)) for x in SITES}
    W['D'] = {x: Fr(rng.randint(0, 5)) for x in SITES}
    W['c'] = {x: rng.randint(0, 3) for x in SITES}
    W['B'] = {x: [Fr(rng.randint(-5, 5), 10 ** 9) for _ in range(3)] for x in SITES}
    Q, h = {}, {}
    for x in SITES:
        for j in range(6):
            y = nb(x, j)
            if (x, j) not in Q:
                Q[(x, j)] = Q[(y, back(j))] = Fr(rng.randint(1, 9), 10 ** 6)
                u = unit_of(Fr(rng.randint(-20, 20), 17))
                h[(x, j)], h[(y, back(j))] = u, conj(u)
    W['Q'], W['h'] = Q, h
    return W


def lam(W, x):
    return 1 / (W['X'][x] * W['mr'][x] ** 2)


def sign(W, x):
    return 1 - 2 * (W['c'][x] % 2)


def read(W, x, j, v):
    """The neighbour's twin read in x's frame: K^(c_x)(h) T^(c_y - c_x) v."""
    y = nb(x, j)
    h = W['h'][(x, j)]
    hx = h if W['c'][x] % 2 == 0 else conj(h)
    d = W['c'][y] - W['c'][x]
    if MUT == 'z2_frames':
        d = d % 2                  # the pawl alone: T^-1 read as T
    return vmul(hx, Tpow(d, v))


def spin(W, x, v):
    """An on-site Hermitian term B . sigma on the twin (the Pauli gearing's form), in the stored frame:
    T^-c (B.sigma) T^c = (-1)^c B.sigma."""
    bx, by, bz = W['B'][x]
    z1, z2 = v
    s = sign(W, x)
    # sigma_x (z1, z2) = (z2, z1); sigma_y = (-i z2, i z1); sigma_z = (z1, -z2)
    sx = (z2, z1)
    sy = (mul((Fr(0), Fr(-1)), z2), mul((Fr(0), Fr(1)), z1))
    sz = (z1, neg(z2))
    out = vadd(vadd(vscl(bx, sx), vscl(by, sy)), vscl(bz, sz))
    return vscl(s, out)


def force(W, st, x):
    psi = st['psi'][x]
    F = ((Fr(0), Fr(0)), (Fr(0), Fr(0)))
    for j in range(6):
        g = 2 * W['mr'][x] ** 2 * W['Q'][(x, j)]
        F = vadd(F, vscl(g, vsub(read(W, x, j, st['psi'][nb(x, j)]), psi)))
    F = vsub(F, vscl(W['D'][x], psi))
    return vadd(F, vscl(W['mr'][x] ** 2, spin(W, x, psi)))


def step(W, st):
    out = {'psi': {}, 'P': {}}
    for x in SITES:
        P1 = vadd(st['P'][x], vscl(W['X'][x], force(W, st, x)))
        out['psi'][x] = vadd(st['psi'][x], vscl(1 / (W['T'] * W['X'][x]), P1))
        out['P'][x] = P1
    return out


def charge(W, st):
    return -sum((sign(W, x) * lam(W, x) * vim(st['psi'][x], st['P'][x]) for x in SITES), Fr(0))


def cur(W, st, x, j):
    g = 2 * W['Q'][(x, j)]
    return sign(W, x) * g * vim(st['psi'][x], read(W, x, j, st['psi'][nb(x, j)]))


def rnd_vec(rng):
    return ((Fr(rng.randint(-99, 99)), Fr(rng.randint(-99, 99))), (Fr(rng.randint(-99, 99)), Fr(rng.randint(-99, 99))))


def new_state(rng, W):
    return {'psi': {x: rnd_vec(rng) for x in SITES},
            'P': {x: vscl(W['T'] * W['X'][x], ((Fr(rng.randint(-9, 9)), Fr(rng.randint(-9, 9))),
                                                (Fr(rng.randint(-9, 9)), Fr(rng.randint(-9, 9))))) for x in SITES}}


def turnover(W, st, xs, how):
    """The turnover at the Node-clocks xs on the stepped state, the slots exchanged:
    'count': the count advanced, the slots exchanged with no T (T once, in the count);
    'gears': T on both slots, the count kept (T once, in the gears);
    'twice': T on both slots and the count advanced (E's T with the head's pawl flip)."""
    W2 = dict(W)
    W2['c'] = dict(W['c'])
    out = {'psi': dict(st['psi']), 'P': dict(st['P'])}
    for x in xs:
        psi, P = st['psi'][x], st['P'][x]
        before = vsub(psi, vscl(1 / (W['T'] * W['X'][x]), P))
        if how == 'gears' or how == 'twice':
            out['psi'][x], out['P'][x] = T(before), vscl(-1, T(P))
        else:
            out['psi'][x], out['P'][x] = before, vscl(-1, P)
        if how == 'count' or how == 'twice':
            if MUT != 'no_frame_advance_fix':
                W2['c'][x] = (W['c'][x] + 1) % 4
    return W2, out


def d1():
    rng = random.Random(21)
    bad = n = 0
    for trial in range(6):
        W = world(rng)
        st = new_state(rng, W)
        for x in SITES:
            for j in range(6):
                if SPOKES[j][1] != 1:
                    continue
                y = nb(x, j)
                n += 1
                bad += int(cur(W, st, x, j) + cur(W, st, y, back(j)) != 0)
    report("D1 the twins' Mesh current antisymmetric, the frame count modulo 4", bad == 0,
           f"{bad} of {n} Meshes not antisymmetric")


def d2():
    rng = random.Random(22)
    how = 'twice' if MUT == 'twice' else 'count'
    W = world(rng)
    st = new_state(rng, W)
    q0 = charge(W, st)
    moved = turns = 0
    for t in range(30):
        st = step(W, st)
        if t % 3 == 2:
            xs = [x for x in SITES if rng.randint(0, 2) == 0]
            turns += len(xs)
            W, st = turnover(W, st, xs, how)
        moved += int(charge(W, st) != q0)
    report("D2 Q kept to the last digit, 30 exact ticks, turnovers on the stepped state, T once in the count",
           moved == 0, f"Q moved at {moved} of 30 ticks; {turns} Node-clock turnovers")


def d3():
    rng = random.Random(23)
    out = {}
    for how in ('count', 'gears', 'twice'):
        kept = rev = n = 0
        for trial in range(8):
            W = world(rng)
            st = new_state(rng, W)
            xs = [x for x in SITES if rng.randint(0, 1)]
            q0 = charge(W, st)
            W2, s2 = turnover(W, st, xs, how)
            q1 = charge(W2, s2)
            # the framed charge of the turned Node-clocks alone
            qa = -sum((sign(W, x) * lam(W, x) * vim(st['psi'][x], st['P'][x]) for x in xs), Fr(0))
            n += 1
            kept += int(q1 == q0)
            rev += int(q1 == q0 - 2 * qa)
        out[how] = (kept, rev, n)
    ok = out['count'][0] == out['count'][2] and out['gears'][0] == out['gears'][2] and out['twice'][1] == out['twice'][2]
    report("D3 T applied once keeps Q (in the count, or in the gears); T in both reverses the turned clocks' charge", ok,
           '; '.join(f"{h}: kept {k} of {n}, reversed {r} of {n}" for h, (k, r, n) in out.items()))


def d4():
    """The stored dynamics against the physical one: Z = T^c psi, the physical step with the bare hop h."""
    rng = random.Random(24)
    W = world(rng)
    st = new_state(rng, W)
    Wp = dict(W)
    Wp['c'] = {x: 0 for x in SITES}

    def phys(W, st):
        return {'psi': {x: Tpow(W['c'][x], st['psi'][x]) for x in SITES},
                'P': {x: Tpow(W['c'][x], st['P'][x]) for x in SITES}}

    def spin_phys_fix(Wp, W):
        # the physical spin field is the stored one turned by the frame: B_phys = (-1)^c B under T^c (B . sigma) T^-c
        Wq = dict(Wp)
        Wq['B'] = W['B']
        return Wq

    zs = phys(W, st)
    Wq = spin_phys_fix(Wp, W)
    bad = 0
    for t in range(12):
        st = step(W, st)
        zs = step(Wq, zs)
        p = phys(W, st)
        bad += int(any(p['psi'][x] != zs['psi'][x] for x in SITES))
    report("D4 the stored twins read through T^c (c modulo 4) move exactly as the physical twins", bad == 0,
           f"{bad} of 12 ticks differ")


if __name__ == '__main__':
    print(f"I2 the twin hands, a {L}^3 torus; mutant: {MUT or 'none'}")
    for c in (d1, d2, d3, d4):
        c()
    fails = [n for n, ok in RES if not ok]
    print(f"{len(RES) - len(fails)} of {len(RES)} checks PASS" + (f"; FAIL: {fails}" if fails else ''))
