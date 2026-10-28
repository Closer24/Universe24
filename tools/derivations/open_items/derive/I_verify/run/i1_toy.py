"""I1 (drafter I): the one formula's charge on an exact rational toy of the head's step, a 3 x 3 x 3 torus.

Every number is a Fraction or an integer; no float decides anything (floats are printed only).
Run: python3 -I i1_toy.py [--mutant NAME]

The toy is the head's step without the carries (law 2 in exact rationals):
  P' = P + X F,  F = SUM_j g_j (U_j a_j - a) - D a,  g_j = 2 pinion mr(x)^2 Q_j,  a' = a + P' / w
  U_j a_j = u_tri u_off seen(a_j),  seen(z) = z where the pawl sign f = 1 and conj(z) where f = -1,
  u_off = the unit of the count n = K_x - f K_y (meshes.offsets),
  u_tri = g / conj(g), g = (4 G + i odd)(G^2 + i m)        (meshes.through_mesh and meshes.skewed)
The triple's two arguments, by variant:
  head : odd = s (o_x + o_y),          m = 3 R s (V_x + V_y)          (the head, 526a5666d)
  fixA : odd = s (o_x + f o_y),        m = 3 R s (V_x + f V_y)        (both read like the count)
  fixB : odd = e_x s (o_x + o_y),      m = e_x 3 R s (V_x + V_y)      (both carry the near end's pawl)
  fixAB: odd = s (o_x + f o_y),        m = e_x 3 R s (V_x + V_y)      (the forced form: the offset framed,
                                                                       the regulator not)
s the spoke's side, e_x = 1 - 2 b_x the pawl sign of the reading Node-clock, f = e_x e_y.
The charge: Q* = -SUM_x e_x lam_x Im(conj(a) P), lam = 1 / (X mr^2).

Checks (each prints its count and PASS or FAIL):
  C1 the Mesh current antisymmetric at every Mesh, by variant and by Mesh class
  C2 Q* kept to the last digit over 40 exact ticks (static rates, random pawls)
  C3 the pawl a pure gauge: G_x (conj the hand, flip the pawl, negate the count, and the odd gears and the flows
     where they are framed) commutes with the step
  C4 the 24: every one of the 24 rotations commutes with the step
  C5 moving rates: Q* moves by exactly the weights' change B = -SUM e (lam' - lam) Im(conj(a) P);
     with the weight read at the time-Mesh (the conserving form) Q* is kept
  C6 the turnover at a random set of Node-clocks: head, the sweep turned with the pawl (held), the same
     on the stepped state; the inflow identity
  C7 the regulator's top: the mirror about the held moment passes the top once; the mirror of the stepped
     state turns again at every tick
  C8 the global turnover and the run back: which packages retrace exactly, and the sign of Q*
  C9 the fitting: the pair's framed sweep and its Q*
"""
import random
import sys
from fractions import Fraction as Fr
from itertools import permutations, product

MUT = sys.argv[sys.argv.index('--mutant') + 1] if '--mutant' in sys.argv else ''
L = 3
SITES = list(product(range(L), repeat=3))
SPOKES = [(a, s) for a in range(3) for s in (1, -1)]       # [+X, -X, +Y, -Y, +Z, -Z]
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


def im_cb(p, q):  # Im(conj(p) q)
    return p[0] * q[1] - p[1] * q[0]


def unit_of(t):  # an exact unit from a rational: ((1 - t^2) + 2 t i) / (1 + t^2); unit_of(-t) = conj
    d = 1 + t * t
    return ((1 - t * t) / d, 2 * t / d)


def tri(odd, m, G):  # g / conj(g), g = (4 G + i odd)(G^2 + i m)
    g = mul((Fr(4 * G), Fr(odd)), (Fr(G * G), Fr(m)))
    n = g[0] * g[0] + g[1] * g[1]
    return ((g[0] * g[0] - g[1] * g[1]) / n, (2 * g[0] * g[1]) / n)


def world(rng, moving=False, pawls=True, triple=True):
    W = dict(G=7, R=2, pin=Fr(1), T=Fr(10 ** 6), NC=Fr(13))
    W['X'] = {x: Fr(rng.randint(500, 1500)) for x in SITES}
    W['mr'] = {x: Fr(rng.randint(300, 1000)) for x in SITES}
    W['D'] = {x: Fr(rng.randint(0, 5)) for x in SITES}
    W['b'] = {x: (rng.randint(0, 1) if pawls else 0) for x in SITES}
    W['K'] = {x: Fr(rng.randint(-3, 3)) for x in SITES}
    W['o'] = {x: [(rng.randint(-9, 9) if triple else 0) for _ in range(3)] for x in SITES}
    W['V'] = {x: [(rng.randint(-9, 9) if triple else 0) for _ in range(3)] for x in SITES}
    Q = {}
    for x in SITES:
        for j in range(6):
            y = nb(x, j)
            if (x, j) not in Q:
                Q[(x, j)] = Q[(y, back(j))] = Fr(rng.randint(1, 9), 10 ** 6)
    W['Q'] = Q
    W['moving'] = moving
    return W


def eps(W, x):
    return 1 - 2 * W['b'][x]


def turn(W, x, j, z, variant):
    """U_j at x applied to the neighbour's hand z (the head's turn, or a variant's)."""
    y = nb(x, j)
    a, s = SPOKES[j]
    ex, ey = eps(W, x), eps(W, y)
    f = ex * ey
    if MUT == 'nopawl_seen':
        seen = z
    else:
        seen = z if f == 1 else conj(z)
    n = W['K'][x] - f * W['K'][y]
    if MUT == 'count_plain':
        n = W['K'][x] - W['K'][y]
    u_off = unit_of(n / W['NC'])
    ox, oy, vx, vy = W['o'][x][a], W['o'][y][a], W['V'][x][a], W['V'][y][a]
    if MUT == 'transverse':          # a contraction the 24 does not allow: the transverse component
        ox, oy = W['o'][x][(a + 1) % 3], W['o'][y][(a + 1) % 3]
    R = W['R']
    if variant == 'head':
        odd, m = s * (ox + oy), 3 * R * s * (vx + vy)
    elif variant == 'fixA':
        odd, m = s * (ox + f * oy), 3 * R * s * (vx + f * vy)
    elif variant == 'fixB':
        odd, m = ex * s * (ox + oy), ex * 3 * R * s * (vx + vy)
    elif variant == 'fixAB':
        odd, m = s * (ox + f * oy), ex * 3 * R * s * (vx + vy)
    else:
        raise ValueError(variant)
    if MUT == 'skew_far':            # fixAB with the skew read like the odd gear (the regulator framed)
        if variant == 'fixAB':
            m = 3 * R * s * (vx + f * vy)
    return mul(mul(tri(odd, m, W['G']), u_off), seen)


def grip(W, x, j):
    return 2 * W['pin'] * W['mr'][x] ** 2 * W['Q'][(x, j)]


def lam(W, x):
    return 1 / (W['X'][x] * W['mr'][x] ** 2)


def current(W, st, x, j, variant):
    """The weighted Mesh current out of x's charge through spoke j: e_x lam X g_j Im(conj(a) U a_j)."""
    a = st['a'][x]
    return eps(W, x) * 2 * W['pin'] * W['Q'][(x, j)] * im_cb(a, turn(W, x, j, st['a'][nb(x, j)], variant))


def force(W, st, x, variant):
    a = st['a'][x]
    F = (Fr(0), Fr(0))
    for j in range(6):
        F = add(F, scl(grip(W, x, j), sub(turn(W, x, j, st['a'][nb(x, j)], variant), a)))
    return sub(F, scl(W['D'][x], a))


def teeth(W, x):
    return W['T'] * W['X'][x]


def new_state(rng, W):
    """A state (a, P): the notch now and the stride's momentum P = w (a - a_before) (no remainder: exact)."""
    a = {x: (Fr(rng.randint(-99, 99)), Fr(rng.randint(-99, 99))) for x in SITES}
    P = {x: scl(teeth(W, x), (Fr(rng.randint(-9, 9)), Fr(rng.randint(-9, 9)))) for x in SITES}
    return {'a': a, 'P': P}


def step(W, st, variant, conserving=False, W_next=None):
    """One exact tick: P' = P + X F(a), a' = a + P' / w (w the half-step teeth where the rates move);
    with conserving=True the momentum is carried into the next tick's charge unit, P'' = (lam / lam') P'."""
    out = {'a': {}, 'P': {}}
    for x in SITES:
        P1 = add(st['P'][x], scl(W['X'][x], force(W, st, x, variant)))
        w1 = teeth(W, x) if W_next is None else W['T'] * (W['X'][x] + W_next['X'][x]) / 2
        out['a'][x] = add(st['a'][x], scl(1 / w1, P1))
        out['P'][x] = scl(lam(W, x) / lam(W_next, x), P1) if conserving else P1
    return out


def qstar(W, st):
    return -sum((eps(W, x) * lam(W, x) * im_cb(st['a'][x], st['P'][x]) for x in SITES), Fr(0))


# ---------------------------------------------------------------- C1: antisymmetry
def c1():
    rng = random.Random(11)
    for variant in ('head', 'fixA', 'fixB', 'fixAB'):
        cls = {}
        for trial in range(6):
            W = world(rng)
            st = new_state(rng, W)
            for x in SITES:
                for j in range(6):
                    if SPOKES[j][1] != 1:
                        continue
                    y = nb(x, j)
                    t = current(W, st, x, j, variant) + current(W, st, y, back(j), variant)
                    f = eps(W, x) * eps(W, y)
                    a = SPOKES[j][0]
                    ident = W['o'][x][a] + W['o'][y][a] == 0 and W['V'][x][a] + W['V'][y][a] == 0
                    key = ('pawl wall' if f < 0 else 'one frame', 'identity triple' if ident else 'odd/skew')
                    c = cls.setdefault(key, [0, 0])
                    c[0] += 1
                    c[1] += int(t != 0)
        bad = sum(c[1] for c in cls.values())
        detail = '; '.join(f"{k[0]}, {k[1]}: {c[1]} of {c[0]} Meshes not antisymmetric" for k, c in sorted(cls.items()))
        expect_bad = variant == 'head'
        ok = (bad > 0) if expect_bad else (bad == 0)
        report(f"C1 Mesh current antisymmetric, {variant}" + (" (expected to fail: the head)" if expect_bad else ''),
               ok, detail)


# ---------------------------------------------------------------- C2: Q* kept over exact ticks
def c2():
    rng = random.Random(12)
    for variant in ('head', 'fixAB'):
        moved = 0
        ticks = 0
        for trial in range(2):
            W = world(rng)
            st = new_state(rng, W)
            q0 = qstar(W, st)
            for _ in range(20):
                st = step(W, st, variant)
                ticks += 1
                moved += int(qstar(W, st) != q0)
        expect_bad = variant == 'head'
        report(f"C2 Q* kept to the last digit, {variant}" + (" (expected to fail)" if expect_bad else ''),
               (moved > 0) if expect_bad else (moved == 0), f"Q* moved at {moved} of {ticks} exact ticks")


# ---------------------------------------------------------------- C3: the pawl a pure gauge
def gauge(W, st, xs, frame_o=True, frame_V=False):
    W2 = dict(W)
    W2['b'] = dict(W['b'])
    W2['K'] = dict(W['K'])
    W2['o'] = {x: list(v) for x, v in W['o'].items()}
    W2['V'] = {x: list(v) for x, v in W['V'].items()}
    st2 = {'a': dict(st['a']), 'P': dict(st['P'])}
    for x in xs:
        st2['a'][x], st2['P'][x] = conj(st['a'][x]), conj(st['P'][x])
        W2['b'][x] = 1 - W['b'][x]
        W2['K'][x] = -W['K'][x]
        if frame_o:
            W2['o'][x] = [-v for v in W['o'][x]]
        if frame_V:
            W2['V'][x] = [-v for v in W['V'][x]]
    return W2, st2


def c3():
    rng = random.Random(13)
    for variant in ('head', 'fixA', 'fixB', 'fixAB'):
        for frame_o, frame_V in ((True, False), (False, False), (True, True)):
            bad = n = 0
            for trial in range(3):
                W = world(rng)
                st = new_state(rng, W)
                xs = [x for x in SITES if rng.randint(0, 1)]
                Wg, stg = gauge(W, st, xs, frame_o, frame_V)
                lhs = step(Wg, stg, variant)                      # gauge, then step
                rhs = gauge(W, step(W, st, variant), xs, frame_o, frame_V)[1]   # step, then gauge
                for x in SITES:
                    n += 1
                    bad += int(lhs['a'][x] != rhs['a'][x])
            frames = (f"the count framed, the odd gears {'framed' if frame_o else 'not framed'}, "
                      f"the flows {'framed' if frame_V else 'not framed'}")
            expect = (variant == 'fixAB' and frame_o and not frame_V) or (variant == 'fixA' and frame_o and frame_V) \
                or (variant == 'fixB' and not frame_o and not frame_V)
            report(f"C3 the pawl a pure gauge, {variant}, {frames}" + ('' if expect else ' (expected to fail)'),
                   (bad == 0) if expect else (bad > 0), f"{bad} of {n} Node-clocks differ between G-then-step and step-then-G")


# ---------------------------------------------------------------- C4: the 24
def rotations():
    found = []
    for p in permutations(range(3)):
        for sg in product((1, -1), repeat=3):
            M = [[(sg[r] if p[r] == c else 0) for c in range(3)] for r in range(3)]
            det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                   + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
            if det == 1:
                found.append(M)
    return found


def rot_vec(M, v):
    return [sum(M[r][c] * v[c] for c in range(3)) for r in range(3)]


def rot_site(M, x):
    return tuple(c % L for c in rot_vec(M, list(x)))


def rot_spoke(M, j):
    a, s = SPOKES[j]
    e = [0, 0, 0]
    e[a] = s
    g = rot_vec(M, e)
    for b in range(3):
        if g[b] != 0:
            return SPOKES.index((b, g[b]))


def rotate(M, W, st):
    W2 = dict(W)
    for key in ('X', 'mr', 'D', 'b', 'K'):
        W2[key] = {rot_site(M, x): v for x, v in W[key].items()}
    for key in ('o', 'V'):
        W2[key] = {rot_site(M, x): rot_vec(M, v) for x, v in W[key].items()}
    W2['Q'] = {(rot_site(M, x), rot_spoke(M, j)): v for (x, j), v in W['Q'].items()}
    st2 = {k: {rot_site(M, x): v for x, v in st[k].items()} for k in ('a', 'P')}
    return W2, st2


def c4():
    rng = random.Random(14)
    rots = rotations()
    for variant in ('head', 'fixAB'):
        bad = n = 0
        W = world(rng)
        st = new_state(rng, W)
        s1 = step(W, st, variant)
        for M in rots:
            W2, st2 = rotate(M, W, st)
            lhs = step(W2, st2, variant)
            rhs = rotate(M, W, s1)[1]
            n += 1
            bad += int(any(lhs['a'][x] != rhs['a'][x] for x in SITES))
        report(f"C4 the 24 commute with the step, {variant}", bad == 0,
               f"{len(rots)} rotations of determinant 1; {bad} of {n} do not commute")


# ---------------------------------------------------------------- C5: moving rates
def c5():
    rng = random.Random(15)
    variant = 'fixAB'
    seq = [world(rng, moving=True)]
    for t in range(12):
        Wn = dict(seq[0])
        Wn['X'] = {x: seq[-1]['X'][x] + rng.randint(-40, 40) for x in SITES}
        Wn['mr'] = {x: seq[-1]['mr'][x] + rng.randint(-20, 20) for x in SITES}
        seq.append(Wn)
    st = new_state(rng, seq[0])
    bad_id = moved = 0
    for t in range(12):
        W, Wn = seq[t], seq[t + 1]
        q0 = qstar(W, st)
        s1 = step(W, st, variant, W_next=Wn)
        q_same = qstar(W, s1)
        q1 = qstar(Wn, s1)
        B = -sum((eps(W, x) * (lam(Wn, x) - lam(W, x)) * im_cb(s1['a'][x], s1['P'][x]) for x in SITES), Fr(0))
        bad_id += int(q_same != q0) + int(q1 - q0 != B)
        moved += int(q1 != q0)
        st = s1
    report("C5a moving rates: Q* kept by the step at the tick's own weights, and Q*' - Q* = B exactly", bad_id == 0,
           f"identity failures {bad_id} of 24; Q* moved at {moved} of 12 ticks (B is not 0)")
    st = new_state(rng, seq[0])
    q0 = qstar(seq[0], st)
    moved = 0
    for t in range(12):
        W, Wn = seq[t], seq[t + 1]
        st = step(W, st, variant, conserving=MUT != 'no_rescale', W_next=Wn)
        moved += int(qstar(Wn, st) != q0)
    report("C5b the momentum carried into the next tick's charge unit keeps Q*", moved == 0,
           f"Q* moved at {moved} of 12 ticks")


# ---------------------------------------------------------------- C6: the turnover
def turned(W, st, x, kind):
    """The turnover's mirror of one Node-clock's hand in (a, P): (now, before) -> (K before, K now) on the head,
    (before, now) with the sweep turned with the pawl; P -> -conj(P) or -P."""
    a, P = st['a'][x], st['P'][x]
    ab = sub(a, scl(1 / teeth(W, x), P))
    if kind == 'head' or MUT == 'sweep_not_turned':
        return conj(ab), scl(-1, conj(P))   # acts.reverse with hands.signs [1, -1]
    return ab, scl(-1, P)                   # the sweep turned with the pawl: the slots exchanged, no K


def c6():
    rng = random.Random(16)
    variant = 'fixAB'
    for kind, where in (('head', 'held'), ('fix', 'held'), ('fix', 'stepped')):
        bad = n = 0
        flips = 0
        for trial in range(4):
            W = world(rng)
            st = new_state(rng, W)
            q0 = qstar(W, st)
            xs = [x for x in SITES if rng.randint(0, 3) == 0]
            s1 = step(W, st, variant)
            inflow = sum((-sum((current(W, st, x, j, variant) for j in range(6)), Fr(0)) for x in xs), Fr(0))
            src = st if where == 'held' else s1
            out = {'a': dict(s1['a']), 'P': dict(s1['P'])}
            for x in xs:
                out['a'][x], out['P'][x] = turned(W, src, x, kind)
            Wt = dict(W)
            Wt['b'] = {x: (1 - W['b'][x] if x in xs else W['b'][x]) for x in SITES}
            q1 = qstar(Wt, out)
            n += 1
            if where == 'held':
                bad += int(q1 - q0 != -inflow)
            else:
                bad += int(q1 != q0)
            flips += int(q1 != q0)
        if kind == 'head':
            report("C6a the head's turnover (K on the hand, the pawl flipped): Q* not kept (expected)", bad > 0,
                   f"the inflow identity fails at {bad} of {n} turnovers")
        elif where == 'held':
            report("C6b the sweep turned with the pawl, mirrored about the held moment: Q*' - Q* = -(the turned clocks' inflow)",
                   bad == 0, f"identity failures {bad} of {n}; Q* moved at {flips} of {n} (the inflow is not 0)")
        else:
            report("C6c the sweep turned with the pawl, mirrored on the stepped state: Q* kept", bad == 0,
                   f"Q* moved at {bad} of {n} turnovers")


# ---------------------------------------------------------------- C7: the regulator's top
def c7():
    found = {}
    for where in ('held', 'stepped'):
        X_b, X, d = 0, 10, -1           # a time gear rising and braked: X_(t+1) = 2 X_t - X_(t-1) + d
        turns = []
        for t in range(20):
            X2 = 2 * X - X_b + d
            top = X_b <= X >= X2 and (X_b < X or X2 < X)
            if top:
                turns.append(t)
                if where == 'held':
                    X_b, X = X, X_b     # the held pre-state exchanged: (now, before) = (X_b, X)
                else:
                    X_b, X = X2, X      # the stepped state exchanged: (now, before) = (X, X2)
            else:
                X_b, X = X, X2
        found[where] = turns
    ok = len(found['held']) == 1 and found['stepped'] == list(range(found['stepped'][0], 20))
    report("C7 the top: the mirror about the held moment turns once; the stepped mirror turns at every tick after",
           ok, f"held: turnovers at ticks {found['held']}; stepped: at ticks {found['stepped']}")


# ---------------------------------------------------------------- C8: the global turnover and the run back
def c8():
    rng = random.Random(18)
    W0 = world(rng)
    st0 = new_state(rng, W0)
    N = 5
    packages = [
        # (name, transport, hand turnover, K sign, o sign, V sign, expected to retrace)
        ("the head's turnover (K, count negated) with the head's triple", 'head', 'head', -1, 1, 1, False),
        ("the head's turnover with fixB (both T1 gears carry the near pawl)", 'fixB', 'head', -1, 1, 1, True),
        ("the head's turnover with fixAB", 'fixAB', 'head', -1, 1, 1, False),
        ("the sweep turned with the pawl, fixAB, count kept, flows negated", 'fixAB', 'fix', 1, 1, -1, True),
        ("the sweep turned with the pawl, fixAB, the head's signs (count negated, flows kept)", 'fixAB', 'fix', -1, 1, 1, False),
    ]
    for name, variant, hand, sK, so, sV, expect in packages:
        W = dict(W0)
        st = {'a': dict(st0['a']), 'P': dict(st0['P'])}
        s1 = step(W, st, variant)
        q_start = qstar(W, s1)
        for _ in range(N - 1):
            st = step(W, st, variant)
        st = step(W, st, variant)
        # the global turnover: every Node-clock, every pawl flipped (f unchanged), the background by its signs
        Wt = dict(W)
        Wt['b'] = {x: 1 - W['b'][x] for x in SITES}
        Wt['K'] = {x: sK * W['K'][x] for x in SITES}
        Wt['o'] = {x: [so * v for v in W['o'][x]] for x in SITES}
        Wt['V'] = {x: [sV * v for v in W['V'][x]] for x in SITES}
        tt = {'a': {}, 'P': {}}
        for x in SITES:
            tt['a'][x], tt['P'][x] = turned(W, st, x, hand)
        q_turned = qstar(Wt, tt)
        for _ in range(N - 1):
            tt = step(Wt, tt, variant)
        target = {'a': {}, 'P': {}}
        for x in SITES:
            target['a'][x], target['P'][x] = turned(W, s1, x, hand)
        retr = all(tt['a'][x] == target['a'][x] and tt['P'][x] == target['P'][x] for x in SITES)
        sign = 'kept' if q_turned == q_start else ('reversed' if q_turned == -q_start else 'other')
        report(f"C8 run back, {name}" + ('' if expect else ' (expected not to retrace)'),
               retr == expect, f"retraces exactly: {retr}; Q* through the turnover: {sign}")


# ---------------------------------------------------------------- C9: the fitting
def c9():
    rng = random.Random(19)
    A, B = 125, 144
    e = A * B
    n = wall = framed0 = unframed0 = weighted0 = same_units = 0
    for trial in range(400):
        W = world(rng)
        x = rng.choice(SITES)
        j = rng.randrange(6)
        y = nb(x, j)
        sx = rng.choice((1, -1))
        sy = -sx
        n += 1
        f = eps(W, x) * eps(W, y)
        wall += int(f < 0)
        # the head lays (sigma A, 0 | 0, B) on zero hands: W = sigma A B in the stored frame at both ends
        unframed = eps(W, x) * sx * e + eps(W, y) * sy * e
        # laid in the end's frame (the twelve gear read through the pawl): the stored sweep eps sigma A B
        framed = eps(W, x) * (eps(W, x) * sx * e) + eps(W, y) * (eps(W, y) * sy * e)
        # its Q*: the stored sweep's momentum D = -w W (zero hands, the fine tooth at mid)
        qx = eps(W, x) * lam(W, x) * teeth(W, x) * (eps(W, x) * sx * e)
        qy = eps(W, y) * lam(W, y) * teeth(W, y) * (eps(W, y) * sy * e)
        unframed0 += int(unframed == 0)
        framed0 += int(framed == 0)
        weighted0 += int(qx + qy == 0)
        same_units += int(lam(W, x) * teeth(W, x) == lam(W, y) * teeth(W, y))
    ok = framed0 == n and unframed0 == n - wall
    report("C9 the fitting's pair: the framed sweep 0 when laid in the end's frame; the head's frame-blind lay is "
           "not 0 across a pawl wall", ok,
           f"{n} pairs, {wall} across a pawl wall: framed sweep 0 at {framed0} laid in the frame, at {unframed0} laid "
           f"as the head lays; Q* 0 at {weighted0} (the two ends' charge units equal at {same_units})")


if __name__ == '__main__':
    print(f"I1 the exact toy, a {L}^3 torus; mutant: {MUT or 'none'}")
    for c in (c1, c2, c3, c4, c5, c6, c7, c8, c9):
        c()
    fails = [n for n, ok in RES if not ok]
    print(f"{len(RES) - len(fails)} of {len(RES)} checks PASS" + (f"; FAIL: {fails}" if fails else ''))
