"""G3, term 6 on the head's gear for E, for a family of two parts, and the held count's own E potential: whole numbers.

(e) an E family under four pushes, its two modes laid apart, (1, 1) and (1, -1) in the head's oblique basis
    (e1 - e2, e2 - e3), whose form is G = [[2, -1], [-1, 2]], sign changes over 4,000 rounds at a swing of 10^5:
    (i) the square's three diagonal slots s = (a, b - a, -b), c = s . s, push -g k s - lam c s;
    (ii) the oblique rows with the node page's push as written, -g k x - lam c x, c = x^T G x (the square's push
         carried back by s = B x, B^T B = G);
    (iii) the oblique rows pushed by -g k G x - lam c G x on unit teeth, the gradient with the wrong inertia;
    (iv) the push through 3 G^-1, -3 g k x - 3 lam c x;
    and the square's slots' trace s1 + s2 + s3, which the push keeps at 0 and the carries may move;
(f) the E family at a swing of 10^7 under (ii) and (iii), lam at the least whole bound and at 0;
(g) a family of two parts, c the sum of both parts' squares: the beat of each part, and the pair at 10^7 under lam;
(h) the held count's own E potential: the dimension of E's invariant forms of degree 2 to 6 under the 24 (a sum over
    the 24's matrices, ranks by fraction-free elimination); the act's three-leg table C[E, E -> E] not 0 and its
    cubic f(e) = (G e) . C(e, e) one of them; the lines where f is extreme at a fixed size, read off the Lagrange form
    det[grad f, G e]; and on each line the E part of a T1 family's spring from C[E, T1 -> T1].

Usage: python3 -I g3_kinds_and_parts.py <src of tensor24-review at 9751f91c1>
"""

import itertools
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import kinds as K  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import load as L  # noqa: E402

W = 6 * 15162856759112389 * 1000 * 1000
n, D, kappa = 10**6, W // 400, W // 16
g, _ = carry(D, n, 0)
least = carry(g * g + 2 * kappa - 1, 2 * kappa, 0)[0]
G = ((2, -1), (-1, 2))
CAP = 10**60


def times(base, m):
    """base multiplied by itself m times (1 at m = 0)."""
    out = 1
    for _ in range(m):
        out *= base
    return out


def gx(x):
    return [G[0][0] * x[0] + G[0][1] * x[1], G[1][0] * x[0] + G[1][1] * x[1]]


def run(form, laid, lam, rounds=4000, watch=0):
    """form: 'square', 'page', 'gradient' or 'three'; laid: the oblique rows (a, b). Returns sign changes of row
    `watch`, the largest trace seen (the square's form alone), and the round it ran past 10^60 (or None)."""
    a, b = laid
    rows = [a, b - a, -b] if form == "square" else [a, b]
    gears = [(v, v, 0) for v in rows]
    k = (n, n, 0)
    seen, last, trace = 0, rows[watch], 0
    for t in range(1, rounds + 1):
        x = [gear[0] for gear in gears]
        kk = k[0]
        if form == "square":
            c = sum(v * v for v in x)
            push = [-g * kk * v - lam * c * v for v in x]
        else:
            gxx = gx(x)
            c = x[0] * gxx[0] + x[1] * gxx[1]
            if form == "page":
                push = [-g * kk * v - lam * c * v for v in x]
            elif form == "gradient":
                push = [-g * kk * v - lam * c * v for v in gxx]
            else:
                push = [-3 * g * kk * v - 3 * lam * c * v for v in x]
        half, _ = carry(g * c, 2, 0)
        gears = [step.gear(*gear, W, p) for gear, p in zip(gears, push, strict=True)]
        k = step.gear(*k, W, -half - kappa * (kk - n))
        now = gears[watch][0]
        seen += int(now * last < 0)
        last = now if now else last
        if form == "square":
            trace = max(trace, abs(sum(gear[0] for gear in gears)))
        if any(abs(gear[0]) > CAP for gear in gears) or abs(k[0]) > CAP:
            return seen, trace, t
    return seen, trace, None


print("(e) sign changes over 4,000 rounds at a swing of 10^5, lam the least whole bound; spring g n gives 63.7, 3 g n 110.3")
for form, label in (("square", "(i) the square's slots"), ("page", "(ii) the page's push, c through G"),
                    ("gradient", "(iii) -g k G x on unit teeth"), ("three", "(iv) through 3 G^-1")):
    s11, t11, _ = run(form, (10**5, 10**5), least)
    s1m, t1m, _ = run(form, (10**5, -10**5), least)
    extra = f"; the slots' largest trace {max(t11, t1m)}" if form == "square" else ""
    print(f"    {label}: mode (1, 1) {s11}, mode (1, -1) {s1m}{extra}")

print("(f) the E family at a swing of 10^7:")
for form, label in (("page", "(ii)"), ("gradient", "(iii)")):
    for mode in ((10**7, 10**7), (10**7, -10**7)):
        out = []
        for lam, name in ((least, "the least lam"), (0, "lam 0")):
            seen, _, gone = run(form, mode, lam)
            out.append(f"{name} {'runs past 10^60 at round ' + str(gone) if gone else 'stays over 4,000 rounds'}")
        print(f"    {label} mode ({mode[0] // 10**7}, {mode[1] // 10**7}): {'; '.join(out)}")


def two_parts(laid, lam, rounds=4000):
    parts = [(laid[0], laid[0], 0), (laid[1], laid[1], 0)]
    k = (n, n, 0)
    seen = [0, 0]
    last = [laid[0], laid[1]]
    for t in range(1, rounds + 1):
        x = [p[0] for p in parts]
        kk = k[0]
        c = x[0] * x[0] + x[1] * x[1]
        half, _ = carry(g * c, 2, 0)
        parts = [step.gear(*p, W, -g * kk * v - lam * c * v) for p, v in zip(parts, x, strict=True)]
        k = step.gear(*k, W, -half - kappa * (kk - n))
        for i in range(2):
            seen[i] += int(parts[i][0] * last[i] < 0)
            last[i] = parts[i][0] if parts[i][0] else last[i]
        if any(abs(p[0]) > CAP for p in parts) or abs(k[0]) > CAP:
            return seen, t
    return seen, None


small, _ = two_parts((10**5, 3 * 10**4), least)
_, gone_least = two_parts((10**7, 10**7), least)
_, gone_zero = two_parts((10**7, 10**7), 0)
print(f"(g) two parts, c = x1^2 + x2^2: sign changes at 10^5 and 3 x 10^4, {small[0]} and {small[1]}; both parts laid at"
      f" 10^7: the least lam {'runs past 10^60 at round ' + str(gone_least) if gone_least else 'stays over 4,000 rounds'};"
      f" lam 0 {'runs past 10^60 at round ' + str(gone_zero) if gone_zero else 'stays over 4,000 rounds'}")

# (h) the held count's own E potential
matrix, weight = K.turns(L.star(3))
held = list(K.kinds(matrix))
emats = [[[int(held[2][t][i][j]) for j in range(2)] for i in range(2)] for t in range(len(weight)) if weight[t]]


def poly_mul(p, q):
    out = {}
    for (a1, b1), c1 in p.items():
        for (a2, b2), c2 in q.items():
            out[(a1 + a2, b1 + b2)] = out.get((a1 + a2, b1 + b2), 0) + c1 * c2
    return {key: v for key, v in out.items() if v}


def poly_pow(p, m):
    out = {(0, 0): 1}
    for _ in range(m):
        out = poly_mul(out, p)
    return out


def reynolds(a, b, mats):
    """The sum over the 24 of the monomial e1^a e2^b at M e."""
    total = {}
    for m in mats:
        row1 = {(1, 0): m[0][0], (0, 1): m[0][1]}
        row2 = {(1, 0): m[1][0], (0, 1): m[1][1]}
        for key, v in poly_mul(poly_pow(row1, a), poly_pow(row2, b)).items():
            total[key] = total.get(key, 0) + v
    return {key: v for key, v in total.items() if v}


def rank(rows):
    """Fraction-free (Bareiss) elimination on whole numbers."""
    m = [list(r) for r in rows]
    r, prev = 0, 1
    cols = len(m[0]) if m else 0
    for col in range(cols):
        pivot = next((i for i in range(r, len(m)) if m[i][col]), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        for i in range(r + 1, len(m)):
            for j in range(col + 1, cols):
                m[i][j] = carry(m[r][col] * m[i][j] - m[i][col] * m[r][j], prev, 0)[0]
            m[i][col] = 0
        prev = m[r][col]
        r += 1
    return r


dims = []
for deg in range(2, 7):
    images = [reynolds(a, deg - a, emats) for a in range(deg + 1)]
    dims.append(rank([[img.get((a, deg - a), 0) for a in range(deg + 1)] for img in images]))
print(f"(h) E's invariant forms under the 24, degrees 2 to 6: {dims} (the form x^T G x, the cubic, its square's"
      f" companion only at six legs)")

inv = list(K.kinds(K.inverse(matrix)))
tables = L.tables(held, inv, weight, K.projector)  # keyed (input, input, output), each (output, input, input)
at = {lab: i for i, lab in enumerate(("A1", "A2", "E", "T1", "T2"))}
cube = [[[int(tables[(at["E"], at["E"], at["E"])][c][a][b]) for b in range(2)] for a in range(2)] for c in range(2)]


def f_act(e):
    ge = gx(e)
    return sum(ge[c] * cube[c][a][bb] * e[a] * e[bb] for c in range(2) for a in range(2) for bb in range(2))


points = [(p, q) for p in range(-4, 5) for q in range(-4, 5)]
invariant = all(f_act([m[0][0] * p + m[0][1] * q, m[1][0] * p + m[1][1] * q]) == f_act([p, q]) for m in emats for p, q in points)

# the cubic's coefficients from four values: f(e1, e2) = sum_a c_a e1^a e2^(3 - a)
values = {t: f_act([t, 1]) for t in range(4)}
c3 = carry(values[3] - 3 * values[2] + 3 * values[1] - values[0], 6, 0)[0]
c0 = values[0]
c2 = carry(values[2] - 2 * values[1] + values[0] - 6 * c3, 2, 0)[0]
c1 = values[1] - c0 - c2 - c3
coef = {3: c3, 2: c2, 1: c1, 0: c0}
check = all(f_act([p, q]) == sum(coef[a] * times(p, a) * times(q, 3 - a) for a in range(4)) for p, q in points)
r3 = next(img for img in (reynolds(a, 3 - a, emats) for a in range(4)) if img)
r3c = {a: r3.get((a, 3 - a), 0) for a in range(4)}
pivot = next(a for a in range(4) if r3c[a])
one_cubic = all(coef[a] * r3c[pivot] == r3c[a] * coef[pivot] for a in range(4)) and coef[pivot] != 0
print(f"    C[E, E -> E] not 0: {any(v for plane in cube for row in plane for v in row)}; f = (G e) . C(e, e) kept by the"
      f" 24 on 81 whole points: {invariant}; a multiple of the 24's one invariant cubic: {one_cubic}")
# Lagrange form det[grad f, G e] = df/de1 (G e)_2 - df/de2 (G e)_1, a binary cubic
d1 = {(a - 1, 3 - a): a * coef[a] for a in range(1, 4)}
d2 = {(a, 2 - a): (3 - a) * coef[a] for a in range(0, 3)}
ge1 = {(1, 0): 2, (0, 1): -1}
ge2 = {(1, 0): -1, (0, 1): 2}
lag = poly_mul(d1, ge2)
for key, v in poly_mul(d2, ge1).items():
    lag[key] = lag.get(key, 0) - v
lines = poly_mul(poly_mul({(1, 0): 1, (0, 1): 1}, {(1, 0): 2, (0, 1): -1}), {(1, 0): 1, (0, 1): -2})
ratio = next(v for v in lines.values() if v)
lead = lag.get(next(key for key, v in lines.items() if v), 0)
proportional = all(lag.get(key, 0) * ratio == v * lead for key, v in lines.items()) and set(lag) <= set(lines)
print(f"    f = {coef[3]} e1^3 + {coef[2]} e1^2 e2 + {coef[1]} e1 e2^2 + {coef[0]} e2^3 on every whole point: {check};"
      f" the Lagrange form det[grad f, G e] = {lag}, a multiple of (e1 + e2)(2 e1 - e2)(e1 - 2 e2): {proportional and lead != 0}")

spring_e = [[[int(tables[(at["E"], at["T1"], at["T1"])][x][comp][z]) for z in range(3)] for x in range(3)] for comp in range(2)]
for e in ((1, -1), (1, 2), (2, 1), (-1, 1), (-1, -2), (-2, -1)):
    m = [[spring_e[0][x][z] * e[0] + spring_e[1][x][z] * e[1] for z in range(3)] for x in range(3)]
    diagonal = all(m[x][z] == 0 for x in range(3) for z in range(3) if x != z)
    d = [m[i][i] for i in range(3)]
    pair = len({d[0], d[1], d[2]}) == 2
    print(f"    on the line through e = {e}: f = {f_act(list(e))}; the T1 family's E part diagonal {diagonal}, {d},"
          f" two alike {pair}")
off = [(p, q) for p, q in itertools.product(range(-6, 7), repeat=2) if (p, q) != (0, 0)]
three = sum(1 for p, q in off if len({spring_e[0][i][i] * p + spring_e[1][i][i] * q for i in range(3)}) == 3)
on_lines = sum(1 for p, q in off if (p + q) * (2 * p - q) * (p - 2 * q) == 0)
print(f"    on the 168 whole points off 0 with |e| up to 6: three different springs exactly off the three lines: {three}"
      f" off, {on_lines} on, {three + on_lines == len(off)}")
