"""What a giant clock like the universe needs (the owner's words to Big Pic of 13:5x UTC: "Look for the one solution of
the system, through the algebra, the clocks, the quaternion... with no degrees of freedom"; "Think about what a giant
clock like the universe needs..."; "Look for a mathematical miracle"; the Boss's 6544107938, 6544115974 and
6544159731). A stand-alone reading of exact clocks, not the engine's board. Whole numbers only, and no tooth anywhere:
every step is exact.
A clock with no tooth steps exactly: a_(n+1) = 2 a_n - a_(n-1) - K a_n, with K its springs and ties, whole, in the
gear's own unit. Its energy (a_n - a_(n-1)) . (a_n - a_(n-1)) + a_n . K a_(n-1) is kept exactly (DERIVED: the step is
the leapfrog of a whole quadratic form). A whole step that keeps a positive whole energy permutes the finitely many
states below any energy, so it has a finite order: the clock returns, every start with one great period (DERIVED).
A swing with no spring (an eigenvalue 0 of K) drifts for ever and never returns; an eigenvalue 4 sits at the step's
own edge and grows; so a returning clock holds every swing, with no free play.
Readings:
  - one clock, K = k for k = 0 to 5: the energy kept over 120 rounds from every start on a grid, and the powers up to 12
    at which the step is the identity;
  - the 24 units of the whole (Hurwitz) quaternions, in doubled coordinates: each class's powers up to 12 at which it is
    1; left multiplication by every unit keeping every norm (Euler's four squares) on a grid of whole quaternions; and
    the order-3 unit w = (-1 + i + j + k) / 2 turning i to j to k;
  - two clocks, K = [[k1, c], [c, k2]] with whole k1, k2 from 0 to 4 and c from -4 to 4: those that return
    (M^120 = I, 120 the least common multiple of every order a step of two clocks can have), each one's great period
    and its characteristic polynomial;
  - three like hands, K = [[s, b, b], [b, s, b], [b, b, s]] with b not 0: those that return (M^2520 = I, 2520 the least
    common multiple of every order a step of three clocks can have);
  - the click world's triangle with the coupling family inside: the giver and the taker alike (spring s), the held
    hand (spring h), the band b between the giver and the taker and the tie t from the held hand to each, so
    K = [[s, b, t], [b, s, t], [t, t, h]], every whole s, h from 0 to 4 and b, t from -4 to 4 with b and t not 0: those
    that return, each one's great period and its characteristic polynomial.
Usage: python3 -I giant.py <node-all src>
"""
import itertools
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402


def mat_mul(p, r):
    return [[sum(p[i][k] * r[k][j] for k in range(len(r))) for j in range(len(r[0]))] for i in range(len(p))]


def identity(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def mat_pow(m, e):
    out, base = identity(len(m)), m
    for bit in bin(e)[2:][::-1]:
        if bit == "1":
            out = mat_mul(out, base)
        base = mat_mul(base, base)
    return out


def step_matrix(k):
    """The exact step on the state (a_n, a_(n-1)): [[2 I - K, -I], [I, 0]]."""
    n = len(k)
    top = [[(2 if i == j else 0) - k[i][j] for j in range(n)] + [-1 if i == j else 0 for j in range(n)]
           for i in range(n)]
    low = [[1 if i == j else 0 for j in range(n)] + [0] * n for i in range(n)]
    return top + low


def divisors(n):
    return [d for d in range(1, n + 1) if carry(n, d, 0)[1] == 0]


def great_period(m, bound):
    one = identity(len(m))
    if mat_pow(m, bound) != one:
        return None
    return min(d for d in divisors(bound) if mat_pow(m, d) == one)


def char_poly(k):
    """The characteristic polynomial of K, det(x I - K), its whole coefficients from the top."""
    n = len(k)
    if n == 1:
        return [1, -k[0][0]]
    if n == 2:
        return [1, -(k[0][0] + k[1][1]), k[0][0] * k[1][1] - k[0][1] * k[1][0]]
    tr = k[0][0] + k[1][1] + k[2][2]
    minors = sum(k[i][i] * k[j][j] - k[i][j] * k[j][i] for i, j in ((0, 1), (0, 2), (1, 2)))
    det = (k[0][0] * (k[1][1] * k[2][2] - k[1][2] * k[2][1]) - k[0][1] * (k[1][0] * k[2][2] - k[1][2] * k[2][0])
           + k[0][2] * (k[1][0] * k[2][1] - k[1][1] * k[2][0]))
    return [1, -tr, minors, -det]


def qmul(p, r):
    """The quaternion product, components (1, i, j, k)."""
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = r
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def dmul(p2, r2):
    """The product in doubled coordinates: (2p)(2r) = 4 pr, halved exactly back to 2 pr."""
    out = []
    for v in qmul(p2, r2):
        h, rest = carry(v, 2, 0)
        assert rest == 0
        out.append(h)
    return tuple(out)


def norm(q):
    return sum(v * v for v in q)


print("== one clock with no tooth: a_(n+1) = (2 - k) a_n - a_(n-1)", flush=True)
for k in range(6):
    m = step_matrix([[k]])
    kept = True
    for a0, a1 in itertools.product(range(-3, 4), repeat=2):
        p, q = a0, a1
        e0 = (q - p) * (q - p) + k * q * p
        for _ in range(120):
            p, q = q, (2 - k) * q - p
            kept = kept and (q - p) * (q - p) + k * q * p == e0
    powers = [e for e in range(1, 13) if mat_pow(m, e) == identity(2)]
    print(f"   k {k}: the energy kept at every round from every start: {kept}; the powers up to 12 at which the step is"
          f" the identity: {powers}", flush=True)

print("== the 24 units of the whole quaternions, doubled coordinates", flush=True)
ONE2 = (2, 0, 0, 0)
units = [u for u in itertools.product(range(-2, 3), repeat=4)
         if norm(u) == 4 and len({carry(v, 2, 0)[1] for v in u}) == 1]
classes = {}
for u in units:
    pw, back = u, []
    for e in range(1, 13):
        if pw == ONE2:
            back.append(e)
        pw = dmul(pw, u)
    classes.setdefault(u[0], set()).add(tuple(back))
print(f"   units: {len(units)}", flush=True)
for real in sorted(classes):
    count = sum(1 for u in units if u[0] == real)
    print(f"   doubled real part {real}: {count} units; the powers up to 12 at which each is 1:"
          f" {sorted(classes[real])}",
          flush=True)
grid = [q for q in itertools.product(range(-3, 4), repeat=4) if len({carry(v, 2, 0)[1] for v in q}) == 1]
held = sum(1 for u in units for q in grid if norm(dmul(u, q)) == norm(q))
print(f"   left multiplication by every unit keeps the norm of every whole quaternion on the grid: {held} of"
      f" {len(units) * len(grid)}", flush=True)
W2 = (-1, 1, 1, 1)
W2_INV = (-1, -1, -1, -1)
turned = [dmul(dmul(W2, x), W2_INV) for x in ((0, 2, 0, 0), (0, 0, 2, 0), (0, 0, 0, 2))]
print(f"   the order-3 unit w = (-1 + i + j + k) / 2 turns i, j, k to {turned} (doubled): i to j, j to k, k to i",
      flush=True)

print("== two clocks with no tooth, K = [[k1, c], [c, k2]]", flush=True)
for k1, k2, c in itertools.product(range(5), range(5), range(-4, 5)):
    if k1 > k2 or c == 0:
        continue
    period = great_period(step_matrix([[k1, c], [c, k2]]), 120)
    if period:
        print(f"   k1 {k1}, k2 {k2}, c {c}: returns with the great period {period}; the polynomial"
              f" {char_poly([[k1, c], [c, k2]])}", flush=True)

print("== three like hands with no tooth, K = [[s, b, b], [b, s, b], [b, b, s]], b not 0", flush=True)
like = [(s, b) for s in range(5) for b in range(-4, 5)
        if b and great_period(step_matrix([[s, b, b], [b, s, b], [b, b, s]]), 2520)]
print(f"   those that return: {like}", flush=True)

print("== the click world's triangle with the coupling family inside, K = [[s, b, t], [b, s, t], [t, t, h]],"
      " b and t not 0", flush=True)
found = []
for s, h, b, t in itertools.product(range(5), range(5), range(-4, 5), range(-4, 5)):
    if b == 0 or t == 0:
        continue
    k = [[s, b, t], [b, s, t], [t, t, h]]
    period = great_period(step_matrix(k), 2520)
    if period:
        found.append((s, h, b, t, period, char_poly(k)))
keys = {(s, h, b, t) for s, h, b, t, _, _ in found}
for s, h, b, t, period, poly in found:
    opposite = s - b  # K (1, -1, 0) = (s - b) (1, -1, 0): the giver's and the taker's opposite swing
    rest_t, rest_d = -poly[1] - opposite, carry(-poly[3], opposite, 0)[0]
    rest = great_period(step_matrix([[0, -rest_d], [1, rest_t]]), 120)
    own = great_period(step_matrix([[opposite]]), 12)
    # the step with K and the step with 4 I - K are one clock read through a_n -> (-1)^n a_n
    partner = (4 - s, 4 - h, -b, -t) in keys
    print(f"   the giver's and the taker's spring {s}, the held hand's {h}, the band {b}, the tie {t}: the great period"
          f" {period}; the polynomial {poly}; the opposite swing held at {opposite}, returning every {own} rounds; the"
          f" other two swings x^2 - {rest_t} x + {rest_d}, returning every {rest} rounds; 4 I - K with the tie's sign"
          f" turned among the solutions: {partner}", flush=True)
print(f"   solutions: {len(found)} of {5 * 5 * 8 * 8}", flush=True)
print("   the search holds every candidate: a returning step has every eigenvalue of K inside (0, 4), so each diagonal"
      " entry is 1, 2 or 3 and, by the interlacing of every 2 x 2 block, each off-diagonal entry is -1, 0 or 1"
      " (DERIVED)", flush=True)
print("exit", flush=True)
