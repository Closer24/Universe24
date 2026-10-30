"""G5, the split click's draw: which tooth stands where decision 29's c stood (Sofer, #2187 6518975579 item 3).

Whole numbers alone. The board: 6 by 6 by 6 Node-clocks with three A1 trains, light (two parts), matter (two parts) and
the held count (one part), at the example's teeth W = 6 grip. Two plans: none (the act as built, the pull alone,
as in Animate's draw.py) and term 6's potential V6 = f1 k c + f2 c^2 + f3 (k - n)^2, c = m_re^2 + m_im^2, laid through
the head's own pushes, so the spring on matter is g = 2 f1, the four-leg term lam = 4 f2 at the least whole bound of
G3, kappa = 2 f3. Lays from an integer carry sequence; every fine tooth born at W div 2. V at a Node-clock is the sum
over it and its six neighbours of the A1 rows' fine teeth (all five rows here).

(a) each train's pitch: the gcd of W and every fine tooth's move from its birth, read after the run, under each plan;
(b) the fold at the Node-clock's own teeth, d = V mod W: distinct values, chi-square of the tenths on 9, and how often
    two draws fall in one half, two rounds in a row and one Mesh apart (500 per mille for independent draws);
(c) Born: part 0 of two parts with sizes S1, S2 (L = S1 + S2), at small and at very large L, two ways: the law's
    d = V mod L with c struck, and the fold d = V mod W with the rank by cross products, part 0 where d L < S1 W;
(c2) the sizes read from the same state as V, S1 = m_re^2 + 1 and S2 = m_im^2 + 1 at the drawing Node-clock;
(c3) the draw taken only at the rounds where a Node-clock's swept area crosses a key;
(d) decision 29's dial, c one count a round, d = (c + V) mod L: same-half per mille and the partition noise (the count
    of part 0 in blocks of 40 rounds against the binomial, 1000 per mille where draws are independent);
(e) the run back: 300 rounds out and back by the act's own untick, the draw recomputed at every round back;
(f) the 24: the state turned by each of the cube's 24 turns, both ticked, V read at the image site;
(g) the two hardest lays: the smallest swing (matter laid to 10 counts, the held count at n), and a cold board
    (everything at rest but one packet of 27 Node-clocks near 100 counts): spread, halves, and a part of 1 in 100
    drawn in two rounds running against chance.

Usage: python3 -I g5_draw.py <src of tensor24-review at a7f40fc16>
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import pushes  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402

GRIP = 15162856759112389 * 1000 * 1000
W = 6 * GRIP
SHAPE = (6, 6, 6)
ROWS = 5  # light re, im; matter re, im; the held count
ROUNDS, FROM = 420, 20
N_HELD = 1000 * 1000


def gcd(a, b):
    while b:
        a, b = b, carry(a, b, 0)[1]
    return abs(a)


def per_mille(part, whole):
    return carry(1000 * part, whole, 0)[0]


def shown(thousandths):
    whole, rest = carry(thousandths, 1000, 0)
    return f"{whole}.{rest:03d}"


def ceiling(a, b):
    return carry(a + b - 1, b, 0)[0]


nb = board(SHAPE)
sites = nb.shape[1]
spokes, meshes = geometry(nb, 3)
ones = np.ones((ROWS, 1), dtype=object)
empty_read = Read(np.zeros(0, dtype=np.intp), np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))
empty_plan = Plan(*(np.zeros(0, dtype=np.intp),) * 3, np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))

# term 6's strengths, G3's probe numbers: the spring g n = W div 400, kappa = W div 16, lam the least whole 4 f2
f1 = carry(carry(W, 400, 0)[0], 2 * N_HELD, 0)[0]
f3 = carry(carry(W, 16, 0)[0], 2, 0)[0]
g, kappa = 2 * f1, 2 * f3
f2 = ceiling(g * g, 8 * kappa)  # lam = 4 f2 >= g^2 / (2 kappa), the least whole such
unit, l_re, l_im, m_re, m_im, held = -1, 0, 1, 2, 3, 4
monomials = [
    (f1, (held, m_re, m_re, unit)), (f1, (held, m_im, m_im, unit)),  # f1 k c
    (f2, (m_re, m_re, m_re, m_re)), (f2, (m_im, m_im, m_im, m_im)), (2 * f2, (m_re, m_re, m_im, m_im)),  # f2 c^2
    (f3, (held, held, unit, unit)), (-2 * f3 * N_HELD, (held, unit, unit, unit)),  # f3 (k - n)^2 less its constant
]
factor = np.array([f for f, _ in monomials], dtype=object)
legs = tuple(np.array([leg[i] for _, leg in monomials], dtype=np.intp) for i in range(4))
term6 = pushes(factor, legs)


def layout(plan):
    return Layout(nb, spokes, meshes, np.full((1, 3 * sites), GRIP, dtype=object),
                  Gearing(W * ones, ones, ones.copy(), ones.copy()), plan, empty_read, empty_read)


def lays():
    """The lay from an integer carry sequence: light as Animate's, matter at swings up to 10^5, the held count at n."""
    state = 20261030
    a, b = np.zeros((ROWS, sites), dtype=object), np.zeros((ROWS, sites), dtype=object)

    def draw(span):
        nonlocal state
        _, state = carry(1103515245 * state + 12345, 2147483648, 0)
        return carry(state, 2 * span + 1, 0)[1] - span

    for i in range(sites):
        for row, (top, stride) in enumerate(((1000, 5), (1000, 5), (100000, 5000), (100000, 5000), (1000, 50))):
            a[row, i] = draw(top) + (N_HELD if row == held else 0)
            b[row, i] = a[row, i] - draw(stride)
    return State(a, b, np.full((ROWS, sites), carry(W, 2, 0)[0], dtype=object), np.zeros((ROWS, sites), dtype=object))


seven = [[i, *nb[:, i].tolist()] for i in range(sites)]


def fine_sum(r):
    per_site = [sum(int(r[row, i]) for row in range(ROWS)) for i in range(sites)]
    return [sum(per_site[j] for j in seven[i]) for i in range(sites)]


def run(plan):
    lay_out, s = layout(plan), lays()
    vs = []
    for t in range(ROUNDS):
        s = step.tick(lay_out, s)
        if t >= FROM:
            vs.append(fine_sum(s.r))
    birth = carry(W, 2, 0)[0]
    pitch = []
    for rows in ((l_re, l_im), (m_re, m_im), (held,)):
        p = W
        for row in rows:
            for i in range(sites):
                p = gcd(p, int(s.r[row, i]) - birth)
        pitch.append(p)
    return vs, pitch, s


def halves(ds, modulus):
    """Same-half per mille, two rounds in a row and one Mesh apart (+x)."""
    hs = [[carry(2 * d, modulus, 0)[0] for d in row] for row in ds]
    rows_same = sum(int(hs[t][i] == hs[t + 1][i]) for t in range(len(hs) - 1) for i in range(sites))
    mesh_same = sum(int(h[i] == h[int(nb[0, i])]) for h in hs for i in range(sites))
    return per_mille(rows_same, (len(hs) - 1) * sites), per_mille(mesh_same, len(hs) * sites)


def chi_tenths(ds, modulus):
    counts = [0] * 10
    for row in ds:
        for d in row:
            counts[carry(10 * d, modulus, 0)[0]] += 1
    total = sum(counts)
    return carry(1000 * sum((10 * c - total) ** 2 for c in counts), 10 * total, 0)[0]


def partition(parts, s1, s2, block=40):
    """The count of part 0 in blocks of rounds at each Node-clock, its spread over the binomial's, per mille."""
    lsum = s1 + s2
    counts = []
    for i in range(sites):
        column = [parts[t][i] for t in range(len(parts))]
        for start in range(0, len(column) - block + 1, block):
            counts.append(sum(int(p == 0) for p in column[start:start + block]))
    k = len(counts)
    spread = k * sum(c * c for c in counts) - sum(counts) ** 2
    return per_mille(spread * lsum * lsum, k * k * block * s1 * s2)


def born(parts, s1, s2):
    total = sum(len(row) for row in parts)
    zero = sum(int(p == 0) for row in parts for p in row)
    lsum = s1 + s2
    z2 = per_mille((lsum * zero - total * s1) ** 2, total * s1 * s2)
    return f"part 0 in {zero} of {total} (expected {carry(total * s1, lsum, 0)[0]}), z^2 {shown(z2)}"


print(f"(a) W = {W}, the grip {GRIP}; term 6: g = {g}, kappa = {kappa}, lam = 4 f2 = {4 * f2} (2 kappa lam >= g^2:"
      f" {2 * kappa * 4 * f2 >= g * g}), n = {N_HELD}")
lays_run = {}
for name, plan in (("the plan empty", empty_plan), ("term 6", term6)):
    vs, pitch, last = run(plan)
    lays_run[name] = (vs, last)
    print(f"    {name}: the pitch of the fine teeth, light {pitch[0]}, matter {pitch[1]}, the held count {pitch[2]}"
          f" (W over the pitch: {carry(W, pitch[0], 0)[0]}, {carry(W, pitch[1], 0)[0]},"
          f" {carry(W, pitch[2], 0)[0]} values)")

print("(b) the fold d = V mod W:")
for name, (vs, _) in lays_run.items():
    ds = [[carry(v, W, 0)[1] for v in row] for row in vs]
    distinct = len({d for row in ds for d in row})
    rows_same, mesh_same = halves(ds, W)
    print(f"    {name}: {distinct} distinct values in {len(ds) * sites} draws; chi-square of the tenths on 9"
          f" {shown(chi_tenths(ds, W))}; in one half, two rounds in a row {rows_same}, one Mesh apart {mesh_same}"
          f" per mille")

print("(c) Born, part 0 of sizes S1 and S2, term 6:")
vs = lays_run["term 6"][0]
for s1, s2 in ((1, 1), (1, 2), (3, 7), (10**6, 3 * 10**6), (10**30, 3 * 10**30)):
    lsum = s1 + s2
    law = [[int(carry(v, lsum, 0)[1] >= s1) for v in row] for row in vs]
    fold = [[int(carry(v, W, 0)[1] * lsum >= s1 * W) for v in row] for row in vs]
    print(f"    S1 = {s1}, S2 = {s2}: the law's d = V mod L: {born(law, s1, s2)};")
    print(f"      the fold at W, cross products: {born(fold, s1, s2)}; its partition noise"
          f" {partition(fold, s1, s2)} per"
          f" mille of the binomial")

def millionths(parts, sizes):
    """Part 0's count against its expectation and variance summed over draws whose sizes change, in millionths."""
    zero = expected = variance = total = 0
    for row_parts, row_sizes in zip(parts, sizes, strict=True):
        for p, (s1, s2) in zip(row_parts, row_sizes, strict=True):
            lsum = s1 + s2
            zero += int(p == 0)
            expected += carry(10**6 * s1, lsum, 0)[0]
            variance += carry(10**12 * s1 * s2, lsum * lsum, 0)[0]
            total += 1
    z2 = per_mille((10**6 * zero - expected) ** 2, variance)
    return f"part 0 in {zero} of {total} (expected {carry(expected, 10**6, 0)[0]}), z^2 {shown(z2)}"


print("(c2) sizes read from the same state as V, S1 = m_re^2 + 1 and S2 = m_im^2 + 1 at the Node-clock, the fold at W:")
lay6, s = layout(term6), lays()
parts, sizes = [], []
for t in range(ROUNDS):
    s = step.tick(lay6, s)
    if t >= FROM:
        vs_now = fine_sum(s.r)
        row_sizes = [(int(s.a[m_re, i]) ** 2 + 1, int(s.a[m_im, i]) ** 2 + 1) for i in range(sites)]
        pairs = zip(vs_now, row_sizes, strict=True)
        parts.append([int(carry(v, W, 0)[1] * (s1 + s2) >= s1 * W) for v, (s1, s2) in pairs])
        sizes.append(row_sizes)
print(f"    {millionths(parts, sizes)}")

print("(c3) the draw only at the rounds where a Node-clock's swept area crosses a key (Omega = m_re p_im - m_im p_re):")
KEY = W * 10**10
lay6, s = layout(term6), lays()
before = None
at_cross, cross_sizes, cross_d = [], [], []
for t in range(ROUNDS):
    s = step.tick(lay6, s)
    p = W * (s.a - s.b) + s.r
    omega = [int(s.a[m_re, i]) * int(p[m_im, i]) - int(s.a[m_im, i]) * int(p[m_re, i]) for i in range(sites)]
    keys = [carry(o, KEY, 0)[0] for o in omega]
    if before is not None and t >= FROM:
        vs_now = fine_sum(s.r)
        for i in range(sites):
            if keys[i] != before[i]:
                d = carry(vs_now[i], W, 0)[1]
                s1, s2 = int(s.a[m_re, i]) ** 2 + 1, int(s.a[m_im, i]) ** 2 + 1
                cross_d.append(d)
                at_cross.append(int(d * (s1 + s2) >= s1 * W))
                cross_sizes.append((s1, s2))
    before = keys
print(f"    {len(cross_d)} crossings; chi-square of the tenths of d on 9 {shown(chi_tenths([cross_d], W))};"
      f" Born on the state's sizes: {millionths([at_cross], [cross_sizes])}")

print("(d) decision 29's dial, c one count a round, d = (c + V) mod L, sizes 1 and 1:")
for name, (vs, _) in lays_run.items():
    for lsum in (70, 1000, 2 * 10**6):
        ds = [[carry(t + v, lsum, 0)[1] for v in row] for t, row in enumerate(vs)]
        rows_same, mesh_same = halves(ds, lsum)
        parts = [[int(2 * d >= lsum) for d in row] for row in ds]
        bare = [[int(2 * carry(v, lsum, 0)[1] >= lsum) for v in row] for row in vs]
        print(f"    {name}, L = {lsum}: with the dial, in one half two rounds in a row {rows_same}, one Mesh apart"
              f" {mesh_same} per mille, partition noise {partition(parts, 1, 1)}; with c struck, partition noise"
              f" {partition(bare, 1, 1)} per mille")

print("(e) the run back, term 6:")
lay6, s = layout(term6), lays()
out = []
for t in range(300):
    s = step.tick(lay6, s)
    out.append([carry(v, W, 0)[1] for v in fine_sum(s.r)])
back = 0
for t in range(299, -1, -1):
    back += int([carry(v, W, 0)[1] for v in fine_sum(s.r)] == out[t])
    s = step.untick(lay6, s)
start = lays()
home = all(np.array_equal(x, y) for x, y in zip(s, start, strict=True))
print(f"    the draw recomputed equal at {back} of 300 rounds back; the lay returns bit for bit: {home}")


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


rotations = []
for order in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
    for signs in ((1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1), (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1)):
        m = [[signs[i] * int(order[i] == j) for j in range(3)] for i in range(3)]
        if det3(m) == 1:
            rotations.append(m)
s0 = step.tick(lay6, lays())
v0 = fine_sum(step.tick(lay6, s0).r)
alike = 0
for m in rotations:
    image = []
    for i in range(sites):
        rest, z = carry(i, 6, 0)
        x, y = carry(rest, 6, 0)
        xs = [carry(sum(m[a][b] * (x, y, z)[b] for b in range(3)), 6, 0)[1] for a in range(3)]
        image.append((xs[0] * 6 + xs[1]) * 6 + xs[2])
    turned = State(*(np.empty_like(part) for part in s0))
    for part, source in zip(turned, s0, strict=True):
        part[:, image] = source
    vt = fine_sum(step.tick(lay6, turned).r)
    alike += int(all(vt[image[i]] == v0[i] for i in range(sites)))
print(f"(f) the 24: {len(rotations)} turns; V at the image site equal at every site after a round: {alike} of"
      f" {len(rotations)}")


def swing_lay(m_top, m_stride, packet):
    """(g)'s lays: a hot board (light as Animate's, matter to m_top) or a cold one (everything at rest, light at 0 and
    the held count at n, but one matter packet on a cube of 3 by 3 by 3 Node-clocks at the centre, near m_top)."""
    state = 7 if packet else 20261030
    a, b = np.zeros((ROWS, sites), dtype=object), np.zeros((ROWS, sites), dtype=object)

    def draw(span):
        nonlocal state
        _, state = carry(1103515245 * state + 12345, 2147483648, 0)
        return carry(state, 2 * span + 1, 0)[1] - span

    a[held, :], b[held, :] = N_HELD, N_HELD
    for i in range(sites):
        rest, z = carry(i, 6, 0)
        x, y = carry(rest, 6, 0)
        inside = int(x in (2, 3, 4) and y in (2, 3, 4) and z in (2, 3, 4))
        if packet and not inside:
            continue
        for row in (l_re, l_im, m_re, m_im):
            if packet and row in (l_re, l_im):
                continue
            light = row in (l_re, l_im)
            top, stride = (1000, 5) if light else (m_top, m_stride)
            base = m_top if packet else 0
            a[row, i] = base + draw(carry(top, 10, 0)[0] if packet else top)
            b[row, i] = a[row, i] - draw(carry(top, 20, 0)[0] if packet else stride)
    return State(a, b, np.full((ROWS, sites), carry(W, 2, 0)[0], dtype=object), np.zeros((ROWS, sites), dtype=object))


def rare_part(name, s, read):
    """d = V mod W at the read Node-clocks: spread, halves, and a part of size 1 in 100 drawn by cross products."""
    ds = []
    for t in range(ROUNDS):
        s = step.tick(lay6, s)
        if t >= FROM:
            v = fine_sum(s.r)
            ds.append([carry(v[i], W, 0)[1] for i in read])
    flat = [d for row in ds for d in row]
    rare = [[int(d * 100 < W) for d in row] for row in ds]
    pairs = (len(rare) - 1) * len(read)
    both = sum(int(rare[t][i] and rare[t + 1][i]) for t in range(len(rare) - 1) for i in range(len(read)))
    hs = [[carry(2 * d, W, 0)[0] for d in row] for row in ds]
    same = sum(int(hs[t][i] == hs[t + 1][i]) for t in range(len(hs) - 1) for i in range(len(read)))
    counts = []
    for i in range(len(read)):
        column = [rare[t][i] for t in range(len(rare))]
        for start in range(0, len(column) - 39, 40):
            counts.append(sum(column[start:start + 40]))
    k = len(counts)
    noise = per_mille((k * sum(c * c for c in counts) - sum(counts) ** 2) * 100 * 100, k * k * 40 * 99)
    print(f"    {name}: {len(set(flat))} distinct of {len(flat)}; chi-square {shown(chi_tenths(ds, W))}; one half"
          f" two rounds in a row {per_mille(same, pairs)}; the part of 1 in 100 in {sum(map(sum, rare))} (expected"
          f" {carry(len(flat), 100, 0)[0]}), in two rounds running {both} (independent {carry(pairs, 10000, 0)[0]}),"
          f" partition noise {noise}")


print("(g) the two hardest lays, term 6, the held count laid at n, d = V mod W:")
rare_part("a hot board, matter laid to 10 counts", swing_lay(10, 1, False), list(range(sites)))
centre = [(x * 6 + y) * 6 + z for x in (2, 3, 4) for y in (2, 3, 4) for z in (2, 3, 4)]
rare_part("a cold board, one packet near 100 counts, read on its 27 Node-clocks", swing_lay(100, 0, True), centre)
