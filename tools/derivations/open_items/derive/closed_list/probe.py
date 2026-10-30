"""Can the engine be written with Rule3's carry, addition and multiplication alone?

The owner's word (2026-10-28, 15:3x UTC): "the node does very simple things: Rule3,
addition and multiplication; make sure the engine can really be written with these."

A probe, not the engine. Z is a whole number that allows addition, multiplication
(and so a product by -1) and nothing else: every comparison, truth test, division,
remainder, power, shift, bit operation, abs, int, index and hash raises, and so does
any plain number but 0 and 1. carry() is the one place a division is written.
Every act of the engine is written on Z below (section A, the closed part), checked
against a plain reference on random cases (section B), with one mutant per act that
must fail, and an AST scan of section A for if, comparison, while and boolean ops.

usage: python3 -I probe.py
"""

import ast
import inspect
import itertools
import random
import sys


class OffList(TypeError):
    """An operation off the closed list."""


def _raw(o):
    if isinstance(o, Z):
        return o.v
    if type(o) is int and o in (0, 1):
        return o
    raise OffList(f"a number beyond 0 and 1: {o!r}")


class Z:
    """A whole number with addition and multiplication only."""

    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v

    def __add__(self, o):
        return Z(self.v + _raw(o))

    __radd__ = __add__

    def __mul__(self, o):
        return Z(self.v * _raw(o))

    __rmul__ = __mul__

    def __neg__(self):  # a product by -1
        return Z(-self.v)

    def __sub__(self, o):  # a sum with a product by -1
        return self + Z(-_raw(o))

    def __rsub__(self, o):
        return Z(_raw(o)) + (-self)

    def _off(self, *a):
        raise OffList("off the closed list")

    __lt__ = __le__ = __gt__ = __ge__ = __eq__ = __ne__ = _off
    __bool__ = __int__ = __index__ = __float__ = __hash__ = _off
    __floordiv__ = __rfloordiv__ = __mod__ = __rmod__ = __truediv__ = __rtruediv__ = _off
    __divmod__ = __rdivmod__ = __pow__ = __rpow__ = __abs__ = __round__ = _off
    __lshift__ = __rshift__ = __and__ = __or__ = __xor__ = __invert__ = _off
    __trunc__ = __floor__ = __ceil__ = _off


def carry(n, d):
    """Rule3, the one division: n = q d + r with 0 <= r < d, d a teeth count of at least 1."""
    q, r = divmod(n.v, d.v)
    return Z(q), Z(r)


# ===================== A. the closed part: only Z, carry, + and * =====================
ZERO, ONE = Z(0), Z(1)
TWO = ONE + ONE


def nonneg(n):
    """The one whether: 1 where n >= 0, 0 below (Sofer's bit)."""
    q, _ = carry(n, n * n + ONE)
    return ONE + q


def choose(b, x, y):
    return b * x + (ONE - b) * y


def minimum(a, b):
    return a - nonneg(a - b) * (a - b)


def maximum(a, b):
    return b + nonneg(a - b) * (a - b)


def equal(a, b):
    return nonneg(a - b) * nonneg(b - a)


def mid(w):
    q, _ = carry(w, TWO)
    return q


# the Gaussian integers: a hand z = (re, im), two gears
def gadd(z, w):
    return (z[0] + w[0], z[1] + w[1])


def gmul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def conj(z):  # K
    return (z[0], -z[1])


def norm(z):  # z conj(z): a click's size
    return z[0] * z[0] + z[1] * z[1]


def turn(z):  # i z, a quarter of the phase
    return (-z[1], z[0])


def gpair(z, w):  # conj(z) w: its real part the dot, its imaginary part the cross
    return gmul(conj(z), w)


# the twin hands: psi = (z1, z2)
def overlap(phi, psi):
    return gadd(gpair(phi[0], psi[0]), gpair(phi[1], psi[1]))


def reverse(psi):  # T = i sigma_y K on the twins
    return ((-psi[1][0], psi[1][1]), conj(psi[0]))


def rho(psi):
    return norm(psi[0]) + norm(psi[1])


# the 24 from the six Spokes alone
SPOKES = [
    (ONE, ZERO, ZERO), (-ONE, ZERO, ZERO), (ZERO, ONE, ZERO),
    (ZERO, -ONE, ZERO), (ZERO, ZERO, ONE), (ZERO, ZERO, -ONE),
]


def dot3(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross3(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def weight(u, v, w):
    """1 on a turn of the cube (the images orthogonal, determinant +1), 0 on every other candidate."""
    ortho = equal(dot3(u, v), ZERO) * equal(dot3(u, w), ZERO) * equal(dot3(v, w), ZERO)
    return ortho * nonneg(dot3(cross3(u, v), w))


def the_24():
    return sum(weight(u, v, w) for u, v, w in itertools.product(SPOKES, repeat=3))


# the contraction T1 x T1 -> A1 + T1 + E + T2, its tables made from the Spokes
AXES = [SPOKES[0], SPOKES[2], SPOKES[4]]


def table():
    """C[kind component][i][j], every entry a sum and product of the axes' integers."""
    d = [[dot3(a, b) for b in AXES] for a in AXES]  # delta
    eps = [[[dot3(cross3(a, b), c) for c in AXES] for b in AXES] for a in AXES]  # Levi-Civita
    x, y, z = 0, 1, 2
    rows = [[[d[i][j] for j in range(3)] for i in range(3)]]  # A1: the dot
    rows += [[[eps[k][i][j] for j in range(3)] for i in range(3)] for k in range(3)]  # T1: the cross
    e1 = [[TWO * d[i][z] * d[j][z] - d[i][x] * d[j][x] - d[i][y] * d[j][y] for j in range(3)] for i in range(3)]
    e2 = [[d[i][x] * d[j][x] - d[i][y] * d[j][y] for j in range(3)] for i in range(3)]
    rows += [e1, e2]  # E
    for a, b in ((y, z), (z, x), (x, y)):  # T2
        rows.append([[d[i][a] * d[j][b] + d[i][b] * d[j][a] for j in range(3)] for i in range(3)])
    return rows


def contract(c, f, g):
    return [sum(c[k][i][j] * f[i] * g[j] for i in range(3) for j in range(3)) for k in range(len(c))]


# the step of one gear and its exact inverse
def force(a, nbs, g, d_spring, j_source):
    """F = sum_j g_j (U_j a_j - a) - D a + J on a hand, U_j a unit of Z[i]."""
    f = (ZERO, ZERO)
    for (u, aj), gj in zip(nbs, g):
        t = gadd(gmul(u, aj), (-a[0], -a[1]))
        f = gadd(f, (gj * t[0], gj * t[1]))
    return gadd(f, gadd((-d_spring * a[0], -d_spring * a[1]), j_source))


def step(a, b, r, w, wp, s, f, k):
    """p = W (a - b) + (r - mid W); p+ = p + s F + K; a+ and r+ by the carry."""
    p = w * (a - b) + (r - mid(w))
    pp = p + s * f + k
    q, rp = carry(pp + mid(wp), wp)
    return a + q, a, rp


def unstep(ap, a, rp, w, wp, s, f, k):
    pp = wp * (ap - a) + (rp - mid(wp))
    p = pp - s * f - k
    q, r = carry(p + mid(w), w)
    return a, a - q, r


# the two clicks
def click_whole(e, winding):
    """q quanta leave, the remainder stays."""
    return carry(e, winding)


def click_split(sizes, c, room):
    """t by carry(c sum sigma, room); the part by the cumulative quotients, no sort and no if."""
    total = sum(sizes)
    t, _ = carry(c * total, room)
    cum, picks = ZERO, []
    for s in sizes:
        picks.append(nonneg(t - cum) * (ONE - nonneg(t - (cum + s))))
        cum = cum + s
    return picks


# the draw's digits "in the order of their values": a fixed network of min and max
def sort4(v):
    a, b, c, d = v
    a, b = minimum(a, b), maximum(a, b)
    c, d = minimum(c, d), maximum(c, d)
    a, c = minimum(a, c), maximum(a, c)
    b, d = minimum(b, d), maximum(b, d)
    b, c = minimum(b, c), maximum(b, c)
    return [a, b, c, d]


# the turnover at the time gear's top, and the beat
def turnover(x, top, teeth, t_of):
    """q = the time gear's carry; T applied q times as a choice: q T x + (1 - q) x."""
    q, _ = carry(top, teeth)
    tx = t_of(x)
    return tuple(tuple(choose(q, tx[i][j], x[i][j]) for j in range(2)) for i in range(2))


def beat(ph, rate, gamma, stepped, old):
    """(k, ph') = carry(ph + rate, Gamma); k = 0 is no tick this tick."""
    k, ph2 = carry(ph + rate, gamma)
    return choose(k, stepped, old), ph2


# ===================== B. the checks against plain references =====================
R = random.Random(20261028)


def zi(n):
    return Z(n)


def rnd(lo, hi):
    return R.randint(lo, hi)


def gz(lo=-50, hi=50):
    return (zi(rnd(lo, hi)), zi(rnd(lo, hi)))


def v(z):
    return z.v if isinstance(z, Z) else tuple(v(x) for x in z)


def run(name, cases, fn):
    bad = sum(1 for _ in range(cases) if not fn())
    return name, cases, bad


def checks(m):
    """m: the set of mutants switched on (each must make its check fail)."""
    out = []
    nn = (lambda n: ONE + carry(n + ONE, n * n + ONE)[0]) if "nonneg" in m else nonneg
    out.append(run("nonneg, the one whether", 4000, lambda: (lambda n: v(nn(zi(n))) == (1 if n >= 0 else 0))(rnd(-10**6, 10**6) if R.randrange(10) < 9 else rnd(-3, 3))))
    mn = (lambda a, b: a - nonneg(b - a) * (a - b)) if "min" in m else minimum
    out.append(run("min, max and equality", 4000, lambda: (lambda a, b: v(mn(zi(a), zi(b))) == min(a, b) and v(maximum(zi(a), zi(b))) == max(a, b) and v(equal(zi(a), zi(b))) == (a == b))(rnd(-99, 99), rnd(-99, 99))))
    gm = (lambda z, w: (z[0] * w[0] + z[1] * w[1], z[0] * w[1] + z[1] * w[0])) if "gmul" in m else gmul

    def gauss():
        z, w = gz(), gz()
        c = complex(*v(z)) * complex(*v(w))
        dot, cross = v(z)[0] * v(w)[0] + v(z)[1] * v(w)[1], v(z)[0] * v(w)[1] - v(z)[1] * v(w)[0]
        return v(gm(z, w)) == (int(c.real), int(c.imag)) and v(gpair(z, w)) == (dot, cross) and v(norm(z)) == v(z)[0] ** 2 + v(z)[1] ** 2 and v(turn(z)) == (-v(z)[1], v(z)[0])
    out.append(run("the Gaussian product, dot and cross, norm, i z", 4000, gauss))
    rv = (lambda psi: (conj(psi[1]), conj(psi[0]))) if "reverse" in m else reverse

    def twins():
        phi, psi = (gz(), gz()), (gz(), gz())
        tt = v(rv(rv(psi))) == tuple(tuple(-x for x in z) for z in v(psi))
        lag = v(norm(overlap(phi, psi)) + norm(overlap(rv(phi), psi))) == v(rho(phi) * rho(psi))
        return tt and lag
    out.append(run("the twin hands: T T = -1, Lagrange's identity", 2000, twins))
    w24 = (lambda u, v_, w: equal(dot3(u, v_), ZERO) * equal(dot3(u, w), ZERO) * equal(dot3(v_, w), ZERO)) if "the24" in m else weight
    def parity(p):
        return (-1) ** sum(1 for i in range(3) for j in range(i + 1, 3) if p[i] > p[j])
    ref24 = sum(1 for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)
                if parity(p) * s[0] * s[1] * s[2] == 1)
    out.append(run("the 24 from the six Spokes (" + str(v(sum(w24(a, b, c) for a, b, c in itertools.product(SPOKES, repeat=3)))) + " found)", 1, lambda: v(sum(w24(a, b, c) for a, b, c in itertools.product(SPOKES, repeat=3))) == ref24 == 24))
    tab = table()
    if "table" in m:
        tab[1] = tab[2]

    def kinds():
        f = [zi(rnd(-30, 30)) for _ in range(3)]
        g = [zi(rnd(-30, 30)) for _ in range(3)]
        F, G = [x.v for x in f], [x.v for x in g]
        k = contract(tab, f, g)
        dot = sum(a * b for a, b in zip(F, G))
        cr = [F[1] * G[2] - F[2] * G[1], F[2] * G[0] - F[0] * G[2], F[0] * G[1] - F[1] * G[0]]
        a1, (t1, t2, t3), (e1, e2), (s1, s2, s3) = k[0], k[1:4], k[4:6], k[6:9]
        # the outer product back from the nine kind parts, every quotient exact (remainder 0)
        zz, r1 = carry(e1 + a1, ONE + TWO)
        xx, r2 = carry((a1 - zz) + e2, TWO)
        yz, r3 = carry(s1 + t1, TWO)
        exact = v(r1) == v(r2) == v(r3) == 0
        return v(a1) == dot and [v(t) for t in (t1, t2, t3)] == cr and v(zz) == F[2] * G[2] and v(xx) == F[0] * G[0] and v(yz) == F[1] * G[2] and exact
    out.append(run("the contraction T1 x T1 -> A1 + T1 + E + T2 (dot, cross, the stress), and back", 2000, kinds))
    un = (lambda ap, a, rp, w, wp, s, f, k: (a, a - carry(wp * (ap - a) + rp - s * f - k + mid(w), w)[0], carry(wp * (ap - a) + rp - s * f - k + mid(w), w)[1])) if "unstep" in m else unstep

    def gear():
        w, wp = zi(rnd(1, 40)), zi(rnd(1, 40))
        a, b, s = zi(rnd(-500, 500)), zi(rnd(-500, 500)), zi(rnd(-3, 3))
        r = zi(rnd(0, w.v - 1))
        units = [(ONE, ZERO), (ZERO, ONE), (-ONE, ZERO), (ZERO, -ONE)]
        hand = gz()
        nbs = [(units[rnd(0, 3)], gz()) for _ in range(6)]
        g = [zi(rnd(0, 3)) for _ in range(6)]
        spring, source = zi(rnd(0, 5)), gz(-5, 5)
        F = force(hand, nbs, g, spring, source)
        Fr = [0, 0]
        for (u, aj), gj in zip(nbs, g):
            c = complex(*v(u)) * complex(*v(aj)) - complex(*v(hand))
            Fr[0] += gj.v * int(c.real)
            Fr[1] += gj.v * int(c.imag)
        Fr = (Fr[0] - spring.v * hand[0].v + source[0].v, Fr[1] - spring.v * hand[1].v + source[1].v)
        ok_f = v(F) == Fr  # the force against the plain sum
        f, k = F[0], zi(rnd(-50, 50))
        ap, a2, rp = step(a, b, r, w, wp, s, f, k)
        pp = w.v * (a.v - b.v) + (r.v - w.v // 2) + s.v * f.v + k.v
        ref = (a.v + (pp + wp.v // 2) // wp.v, a.v, (pp + wp.v // 2) % wp.v)
        back = un(ap, a2, rp, w, wp, s, f, k)
        return ok_f and v((ap, a2, rp)) == ref and v(back) == (a.v, b.v, r.v)
    out.append(run("the step of a gear (p+ = p + s F + K and the carry) and its exact inverse", 4000, gear))
    cw = (lambda e, w: carry(e, w + ONE)) if "whole" in m else click_whole
    out.append(run("the whole click: q quanta leave, the remainder stays", 4000, lambda: (lambda e, w: v(cw(zi(e), zi(w))) == divmod(e, w))(rnd(-10**5, 10**5), rnd(1, 999))))

    def split():
        sizes = [zi(rnd(0, 40)) for _ in range(rnd(2, 5))]
        if sum(x.v for x in sizes) == 0:
            sizes[0] = zi(1)
        room = zi(rnd(1, 1000))
        c = zi(rnd(0, room.v - 1))
        picks = click_split(sizes, c, room) if "split" not in m else [nonneg(zi(0)) for _ in sizes]
        t = c.v * sum(x.v for x in sizes) // room.v
        cum, ref = 0, []
        for s in sizes:
            ref.append(1 if cum <= t < cum + s.v else 0)
            cum += s.v
        return [x.v for x in picks] == ref and sum(ref) == 1
    out.append(run("the split click: the draw picks one part by the sizes", 4000, split))
    so = (lambda q: q) if "sort" in m else sort4
    out.append(run("the draw's digits in order: a fixed network of min and max", 4000, lambda: (lambda d: [x.v for x in so([zi(x) for x in d])] == sorted(d))([rnd(-9, 9) for _ in range(4)])))

    def turn_over():
        psi = (gz(), gz())
        teeth = zi(rnd(1, 50))
        top = zi(rnd(0, teeth.v - 1)) if R.randrange(2) == 0 else teeth
        got = turnover(psi, top, teeth, reverse if "turnover" not in m else (lambda p: p))
        want = v(reverse(psi)) if top.v == teeth.v else v(psi)
        return v(got) == want
    out.append(run("the turnover at the top: T applied by the time gear's carry", 4000, turn_over))

    def beats():
        gamma = zi(rnd(1, 30))
        rate, ph = zi(rnd(0, gamma.v)), zi(rnd(0, gamma.v - 1))
        new, ph2 = beat(ph, rate, gamma, zi(1), zi(0)) if "beat" not in m else (zi(1), ph)
        k = (ph.v + rate.v) // gamma.v
        return new.v == k and ph2.v == (ph.v + rate.v) % gamma.v
    out.append(run("the beat: a tick or no tick, by the rate dial's carry", 4000, beats))
    return out


def scan():
    """Section A's code: count if, conditional expression, comparison, while, and/or, try and raise."""
    names = [nonneg, choose, minimum, maximum, equal, mid, gadd, gmul, conj, norm, turn, gpair,
             overlap, reverse, rho, dot3, cross3, weight, the_24, table, contract, force, step,
             unstep, click_whole, click_split, sort4, turnover, beat]
    bad = {}
    for fn in names:
        for node in ast.walk(ast.parse(inspect.getsource(fn))):
            kind = type(node).__name__
            if kind in ("If", "IfExp", "Compare", "While", "BoolOp", "Try", "Raise", "Assert"):
                bad[fn.__name__] = bad.get(fn.__name__, []) + [kind]
    return names, bad


def main():
    names, bad = scan()
    print(f"section A: {len(names)} acts; if, comparison, while, and/or, try, raise: {bad or 'none'}")
    fails = 0
    for name, cases, b in checks(set()):
        print(f"  {'ok  ' if b == 0 else 'FAIL'} {name}: {cases - b} of {cases}")
        fails += b
    print("the mutants (each must fail):")
    caught = 0
    mutants = ["nonneg", "min", "gmul", "reverse", "the24", "table", "unstep", "whole", "split", "sort", "turnover", "beat"]
    for mu in mutants:
        try:
            res = [f"{n}: {b} of {c} fail" for n, c, b in checks({mu}) if b]
            hit = bool(res)
            for line in res:
                print(f"    {mu}: {line}")
        except OffList as e:
            hit = False
            print(f"  {mu}: off the list ({e})")
        except ZeroDivisionError:
            hit = True
        caught += hit
        print(f"  {'caught' if hit else 'MISSED'} {mu}")
    off = 0
    for probe in (lambda: ONE < ONE, lambda: bool(ONE), lambda: ONE // ONE, lambda: ONE % ONE, lambda: Z(5) + 2, lambda: abs(ONE), lambda: [0][ONE]):
        try:
            probe()
        except OffList:
            off += 1
    print(f"the closed list refuses 7 of 7 off-list uses: {off} of 7")
    ok = fails == 0 and caught == len(mutants) and not bad and off == 7
    print("RESULT:", "the engine's acts are written with the carry, addition and multiplication alone" if ok else "NOT SHOWN")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
