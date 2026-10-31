"""The clocks' frames on the square form, in whole numbers: the per-clock sign and its quaternion kin on the 24 whole
units, the loops' parities and holonomies as the frame-free content, the free swing's kernel, and a band's sign written
on a loop as a write the rest read.

Clock: every clock x carries a sign frame. A band between clocks i and j is the cell x_i - e x_j squared, at weight w:
e = -1 is the plain band, w (x_i + x_j)^2, and e = +1 the reversed band and every Mesh grip, w (x_i - x_j)^2. Turning
clock v's frame (x_v -> -x_v) with the sign of every band at v (e -> -e) leaves every square as it was. With quaternion
hands the frame is a whole unit w (x_v -> w x_v), a band carries a link k (the cell x_i - k x_j), and the links at v
move with the frame (k_vj -> w k_vj, k_iv -> k_iv w*).
Algebra: the square form as a polynomial with whole coefficients, compared exactly before and after every frame turn;
its matrix's determinant by Bareiss's elimination, every division the carry's with its remainder checked 0 and no pivot
sought: the form is a sum of squares, so a zero pivot already shows a kernel (x^T M x = 0 forces M x = 0); the 24 whole
units in doubled coordinates, every sign on every axis and every sign on all four, no table typed; Hamilton's product of
doubled units halved by the carry, its remainder checked 0.
Board: a stand-alone ring of N Node-clocks, each with a giver and a taker on one band under the square form, every clock
gripped to its two Mesh neighbours at the grip den Gamma^2, the inertia W = 6 grips, the band at the cell's 2 f with
f = W div Gamma (so the square form's weight f); the step W (x+ - 2 x + x-) = F by the carry, each dial's fine tooth
born at W div 2 and kept; laid (a test's lay) with the uniform opposite swing, g = -u = -4,000 units at every
Node-clock, moving one unit a round, so through 0 at round 4,000; the counts are the units times lam, the grain, which
the forms' two legs scale homogeneously (F(lam x) = lam F(x)), so a finer grain is the same run with a finer carry. Not
node-all's act: no held hand, no click, no key.
Clicks: none read. The test lays one write: the band's sign at Node-clock 0 turned at the first round its pair stands at
0, where 1 - lit(g u) = 1 by one carry; the turn is its own inverse. What the other Node-clocks read of it is their
dials against the unwritten run.

Usage: python3 -I frames.py <src of node-all 9d75a4904> <Gamma> <den> <sites> <rounds> <lam> [<lam> ...]
"""

import sys
from itertools import product

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry, lit  # noqa: E402

gamma, den, sites, rounds = (int(x) for x in sys.argv[2:6])
grains = [int(x) for x in sys.argv[6:]]


def exact(a, b):
    """a / b by the carry, its remainder checked 0."""
    q, r = carry(a, b, 0)
    assert r == 0
    return q


def onward(x, size):
    """The next Node-clock around a ring of size, by the carry's remainder."""
    return carry(x + 1, size, 0)[1]


def dial(size, i):
    return {tuple(1 if j == i else 0 for j in range(size)): 1}


def add(p, q):
    out = dict(p)
    for m, c in q.items():
        out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c}


def times(p, q):
    out = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            m = tuple(a + b for a, b in zip(m1, m2, strict=True))
            out[m] = out.get(m, 0) + c1 * c2
    return {m: c for m, c in out.items() if c}


def scale(p, k):
    return {m: c * k for m, c in p.items() if c * k}


def form(size, cells):
    """SUM w (x_i - e x_j)^2 over the cells (i, j, e, w), a polynomial in size dials."""
    p = {}
    for i, j, e, w in cells:
        c = add(dial(size, i), scale(dial(size, j), -e))
        p = add(p, scale(times(c, c), w))
    return p


def turned(size, cells, v):
    """The form in clock v's turned frame: every band at v takes the other sign, and x_v -> -x_v."""
    p = form(size, [(i, j, -e if v in (i, j) else e, w) for i, j, e, w in cells])
    return {m: c * (1 - 2 * carry(m[v], 2, 0)[1]) for m, c in p.items()}


def matrix(size, cells):
    """The form's matrix M, x^T M x = SUM w (x_i - e x_j)^2."""
    m = [[0] * size for _ in range(size)]
    for i, j, e, w in cells:
        m[i][i] += w
        m[j][j] += w
        m[i][j] -= e * w
        m[j][i] -= e * w
    return m


def det(m):
    """Bareiss on a sum-of-squares form: 0 at the first zero pivot (a kernel), else the determinant."""
    a = [row[:] for row in m]
    n = len(a)
    prev = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = exact(a[i][j] * a[k][k] - a[i][k] * a[k][j], prev)
        prev = a[k][k]
    return a[n - 1][n - 1]


def apply(m, v):
    return [sum(a * b for a, b in zip(row, v, strict=True)) for row in m]


grip = den * gamma * gamma
W = 6 * grip
f = exact(W, gamma)
print(f"grain: Gamma {gamma}, den {den}; grip {grip}, W = 6 grips {W}, f = W div Gamma {f}; a band at the cell's 2 f is"
      f" the square form's weight f on its cell")


def ring(n, signs, band, mesh):
    """n Node-clocks, the giver x and the taker n + x at each, a band (x, n + x) of sign signs[x], Mesh grips around."""
    cells = [(x, n + x, signs[x], band) for x in range(n)]
    cells += [(x, onward(x, n), 1, mesh) for x in range(n)]
    cells += [(n + x, n + onward(x, n), 1, mesh) for x in range(n)]
    return 2 * n, cells


# 1. The frame turn leaves the form as it was, clock by clock.
nets = {"the pair": (2, [(0, 1, -1, f)]), "the triangle of plain bands": (3, [(0, 1, -1, f), (1, 2, -1, f),
                                                                           (2, 0, -1, f)])}
nets["the meshed ring of 3"] = ring(3, [-1, -1, -1], f, grip)
for name, (size, cells) in nets.items():
    kept = [turned(size, cells, v) == form(size, cells) for v in range(size)]
    print(f"1. {name}: the form in each clock's turned frame equals the form: {sum(kept)} of {len(kept)} clocks")

# 2. The kernel: a free swing exactly when every loop is balanced.
plain, reversed_ = -1, 1
size, cells = nets["the pair"]
print(f"2. the pair: det at the plain band {det(matrix(size, cells))}, at the reversed band"
      f" {det(matrix(size, [(0, 1, reversed_, f)]))} (a loopless group sits at the edge in either frame)")
size, cells = nets["the triangle of plain bands"]
one_turned = cells[:2] + [(2, 0, reversed_, f)]
print(f"   the triangle: det with three plain bands {det(matrix(size, cells))} = 4 f^3 = {4 * f ** 3} (an odd loop of"
      f" plain bands, frustrated, holds); with one reversed {det(matrix(size, one_turned))} (balanced, the edge)")
for n in range(3, sites + 1):
    row = []
    for label, signs in (("all plain", [plain] * n), ("one reversed", [reversed_] + [plain] * (n - 1)),
                         ("two reversed", [reversed_] * 2 + [plain] * (n - 2)), ("all reversed", [reversed_] * n)):
        size, cells = ring(n, signs, f, grip)
        d = det(matrix(size, cells))
        row.append(f"{label} {'0' if d == 0 else 'positive (' + str(d.bit_length()) + ' bits)'}")
    size, cells = ring(n, [plain] * n, f, grip)
    free = apply(matrix(size, cells), [1] * n + [-1] * n)
    lent = [r[:] for r in matrix(size, cells)]
    for x in range(size):
        lent[x][x] += f  # an own spring f laid on every clock beyond the square form, as a lend that stays
    print(f"   the meshed ring of {n}: det {', '.join(row)}; the uniform opposite swing (1, -1 at every Node-clock)"
          f" under all plain bands: M v = 0 at {sum(1 for c in free if c == 0)} of {size} rows; with an own spring f"
          f" laid on every clock: det {'positive' if det(lent) else '0'}")

# 3. Quaternion hands: the 24 whole units, the link, the holonomy.
units = [tuple(2 * s if a == m else 0 for a in range(4)) for m in range(4) for s in (1, -1)]
units += [tuple(signs) for signs in product((1, -1), repeat=4)]
one = (2, 0, 0, 0)


def hamilton(a, b):
    return (a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3], a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2],
            a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1], a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0])


def mul(a, b):
    """The product of two doubled units, doubled: (2a)(2b) = 4ab, halved by the carry."""
    return tuple(exact(c, 2) for c in hamilton(a, b))


def conj(a):
    return (a[0], -a[1], -a[2], -a[3])


def left(k):
    """2k's left product as a 4 x 4 whole matrix: column c is (2k) e_c."""
    cols = [hamilton(k, tuple(1 if a == c else 0 for a in range(4))) for c in range(4)]
    return [[cols[c][r] for c in range(4)] for r in range(4)]


closed = all(mul(a, b) in units for a in units for b in units)
re2 = {}
for k in units:
    re2[k[0]] = re2.get(k[0], 0) + 1
gaps = [sum((a - b) ** 2 for a, b in zip(k, one, strict=True)) for k in units if k != one]
print(f"3. the 24 whole units (doubled coordinates): {len(units)}, closed under the product: {closed}; 2 Re k:"
      f" {dict(sorted(re2.items()))}; 4 |k - 1|^2 over the 23 units other than 1: least {min(gaps)}, so left"
      f" multiplication by any of them fixes no quaternion but 0")

g4 = [dial(8, i) for i in range(4)]
u4 = [dial(8, 4 + i) for i in range(4)]
held = 0
for k in units:
    lk = left(k)
    ku = [{} for _ in range(4)]
    for r in range(4):
        for c in range(4):
            ku[r] = add(ku[r], scale(u4[c], lk[r][c]))
    lhs = {}
    rhs = {}
    for r in range(4):
        cell = add(scale(g4[r], 2), scale(ku[r], -1))
        lhs = add(lhs, times(cell, cell))
        rhs = add(rhs, add(scale(times(g4[r], g4[r]), 4), scale(times(u4[r], u4[r]), 4)))
        rhs = add(rhs, scale(times(g4[r], ku[r]), -4))
    held += lhs == rhs
print(f"   the cell's square: 4 |g - k u|^2 = 4 |g|^2 + 4 |u|^2 - 4 Re(g* (2k) u) as polynomials in the eight dials, for"
      f" {held} of 24 units: the band is twice the tie's weight in the one cell, at every unit")


def qmatrix(links):
    """2M for SUM over the triangle's edges (0, 1), (1, 2), (2, 0) of |x_i - k x_j|^2, quaternion hands, 12 dials."""
    m = [[0] * 12 for _ in range(12)]
    for (i, j), k in zip(((0, 1), (1, 2), (2, 0)), links, strict=True):
        lk = left(k)
        for a in range(4):
            m[4 * i + a][4 * i + a] += 2
            m[4 * j + a][4 * j + a] += 2
            for c in range(4):
                m[4 * i + a][4 * j + c] -= lk[a][c]
                m[4 * j + c][4 * i + a] -= lk[a][c]
    return m


def mat(a, b):
    return [[sum(a[i][t] * b[t][j] for t in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def frame(w):
    """Q2 = 2Q for the frame w at clock 0: 2w's left product on clock 0, 2 on the others."""
    q = [[0] * 12 for _ in range(12)]
    lw = left(w)
    for a in range(4):
        for c in range(4):
            q[a][c] = lw[a][c]
        q[4 + a][4 + a] = 2
        q[8 + a][8 + a] = 2
    return q


kept = 0
for w in units:
    q2 = frame(w)
    q2t = [list(r) for r in zip(*q2, strict=True)]
    for k in units:
        before = qmatrix([k, one, one])
        after = qmatrix([mul(w, k), one, conj(w)])
        kept += mat(mat(q2t, after), q2) == [[4 * x for x in r] for r in before]
print(f"   the frame w at clock 0 with its links moved (k_01 -> w k_01, k_20 -> k_20 w*): the form kept for {kept} of"
      f" {24 * 24} (frame, link) pairs on the triangle")
zero = [k for k in units if det(qmatrix([k, one, one])) == 0]
pair_zero = 0
for k in units:
    m = [r[:8] for r in qmatrix([k, one, one])[:8]]
    for a in range(8):  # the pair alone: only the edge (0, 1); drop the two edges at clock 2
        m[a][a] -= 2
    pair_zero += det(m) == 0
print(f"   the triangle's holonomy k_01 k_12 k_20 = k: det 0 at {len(zero)} of 24 units, namely k = 1 only:"
      f" {zero == [one]}; the pair alone (a loopless edge) with link k: det 0 at {pair_zero} of 24")

# The click world's scalar dials with a unit link k on their band: the cell g - k u with g and u on the real axis, its
# square w (g^2 + u^2 - 2 Re(k) g u); doubled, 2M = w [[2, -2 Re k], [-2 Re k, 2]], det w^2 (4 - (2 Re k)^2).
edge_units = [k for k in units if (2 * f) ** 2 - (f * k[0]) ** 2 == 0]
classes = {}
for k in units:
    key = ((2 * f, -f * k[0]), (-f * k[0], 2 * f))
    classes[key] = classes.get(key, 0) + 1
print(f"   scalar dials (the click world's) with a unit link k on their band: the pair's form is"
      f" f (g^2 + u^2 - 2 Re(k) g u), det 0 at {len(edge_units)} of 24 units (2 Re k = {sorted(k[0] for k in edge_units)}),"
      f" positive at the other {24 - len(edge_units)}: the band reaches the dials through Re k alone, so the 24 give"
      f" {len(classes)} pair forms on scalar dials (one per value of 2 Re k)")

# 4. The ring run: the free swing drifts; a reversed band holds it; the write at a zero is read by the rest.
n = sites
A = 4000  # a test's lay, in units: the uniform opposite swing at -A, one unit a round, so through 0 at round A


def forces(g, u, signs):
    fg, fu = [], []
    for x in range(n):
        cell = g[x] - signs[x] * u[x]
        fg.append(-2 * f * cell - 2 * grip * (2 * g[x] - g[x - 1] - g[onward(x, n)]))
        fu.append(2 * f * signs[x] * cell - 2 * grip * (2 * u[x] - u[x - 1] - u[onward(x, n)]))
    return fg, fu


def potential(g, u, signs):
    total = sum(f * (g[x] - signs[x] * u[x]) ** 2 for x in range(n))
    return total + sum(grip * ((g[x] - g[onward(x, n)]) ** 2 + (u[x] - u[onward(x, n)]) ** 2) for x in range(n))


def polarized(g1, u1, g0, u0, signs):
    """E = W |x+ - x|^2 + x+^T K x with K = 2M: the step's own invariant where the carry leaves nothing; with the carry
    it moves by the teeth's share, (x+ - x-) . (t - t+) a round."""
    kin = W * sum((g1[x] - g0[x]) ** 2 + (u1[x] - u0[x]) ** 2 for x in range(n))
    pot = sum(f * (g1[x] - signs[x] * u1[x]) * (g0[x] - signs[x] * u0[x]) for x in range(n))
    pot += sum(grip * ((g1[x] - g1[onward(x, n)]) * (g0[x] - g0[onward(x, n)])
                       + (u1[x] - u1[onward(x, n)]) * (u0[x] - u0[onward(x, n)])) for x in range(n))
    return kin + 2 * pot


def run(signs, write, lam):
    signs = list(signs)
    g, u = [-A * lam] * n, [A * lam] * n
    gb, ub = [-A * lam - lam] * n, [A * lam + lam] * n
    tg, tu = [carry(W, 2, 0)[0]] * n, [carry(W, 2, 0)[0]] * n
    path, wrote, energy = [], None, []
    for r in range(rounds + 1):
        path.append((tuple(g), tuple(u)))
        if write and wrote is None and 1 - lit(g[0] * u[0]) == 1:
            before = potential(g, u, signs)
            e_old = polarized(g, u, gb, ub, signs)
            signs[0] = -signs[0]
            wrote = (r, potential(g, u, signs) - before, polarized(g, u, gb, ub, signs) - e_old)
        fg, fu = forces(g, u, signs)
        ng, nu = [], []
        for x in range(n):
            q, tg[x] = carry(fg[x], W, tg[x])
            ng.append(2 * g[x] - gb[x] + q)
            q, tu[x] = carry(fu[x], W, tu[x])
            nu.append(2 * u[x] - ub[x] + q)
        energy.append(polarized(ng, nu, g, u, signs))
        gb, ub, g, u = g, u, ng, nu
    return path, wrote, energy


def widest(path):
    return max(abs(a - b) for gs, us in path for a, b in zip(gs, us, strict=True))


def ppm(spread, base):
    return carry(spread * 1000000, base, 0)[0]


for lam in grains:
    free_path, _, free_e = run([plain] * n, False, lam)
    held_path, _, held_e = run([reversed_] + [plain] * (n - 1), False, lam)
    written, wrote, written_e = run([plain] * n, True, lam)
    end = free_path[-1]
    print(f"4. the ring of {n} at lam {lam} (counts = units x lam), {rounds} rounds, the uniform opposite swing laid at"
          f" -{A} units moving one unit a round:")
    print(f"   all plain: every push 0, the drift exact: at the end g = {end[0][0]} counts, |g - u| ="
          f" {abs(end[0][0] - end[1][0])} at every Node-clock ({len(set(end[0]))} value); E {free_e[0]} at the start and"
          f" {free_e[-1]} at the end")
    print(f"   one band reversed from the start (Node-clock 0): the widest |g - u| over the run {widest(held_path)}; E"
          f" spread {ppm(max(held_e) - min(held_e), held_e[0])} parts per million of its start")
    r_w, dv, de = wrote
    first = []
    for x in range(n):
        parted = [r for r in range(rounds + 1)
                  if (written[r][0][x], written[r][1][x]) != (free_path[r][0][x], free_path[r][1][x])]
        first.append(parted[0] if parted else None)
    print(f"   the write: Node-clock 0's band turned at round {r_w}, where its pair stands at 0: the potential moved by"
          f" {dv} and E by {de} at the write; after it the widest |g - u| {widest(written[r_w:])} against the free"
          f" drift's {widest(free_path)}; E after the write spread {ppm(max(written_e[r_w:]) - min(written_e[r_w:]),
          written_e[0])} parts per million of its start")
    print(f"   the first round each Node-clock's dials part from the unwritten run, Node-clocks 0 to {n - 1}: {first}")
early = A - 1000
print(f"   the same turn at round {early}, the pair at {early - A} and {A - early} units, would move the potential by"
      f" 4 f g^2 = {4 * f * (A - early) ** 2} at lam 1: the write moves no energy only where g u = 0")
