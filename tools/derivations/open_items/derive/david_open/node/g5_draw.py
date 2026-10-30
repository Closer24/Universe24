"""G5, the split click's draw, read inside the act: one round's centred fine teeth, in and out, as the pointer.

Whole numbers alone, every division Rule3's carry. The board, the lays, term 6 and the trains are the old probe's:
6 by 6 by 6 Node-clocks, light, matter and the held count, all three trains A1, the teeth W six grips. At a drawing
Node-clock x, for the round from s_in to s_out = tick(s_in): the centred tooth c(r) = 2 r + 1 - W; P, the sum of
c(r_in) + c(r_out) over x, its six neighbours and every A1 row; u = P mod W; the pointer e = min(u, W - u), between
0 and H, where H is W div 2. The parts are ranked by size, the larger first, ties in their given order; the part
drawn is the first whose cumulative size C has e times L below C times H, L the sizes' total; the last one at e = H.

(a) each train's pitch: the gcd of W and every move of its fine teeth, under each plan;
(b) the pointer e under term 6: distinct values, chi-square of its tenths, same half, and its star discrepancy;
(c) Born at five fixed splits by four rules: e, the raw sum mod L, decision 29's digits, its digits with the dial;
    then the sizes read from the state, by e and the rank by size;
(d) six lays: chi-square of e's tenths and part 0 at 1:1, against the null of independent draws;
(e) the run back inside the act: 300 rounds out, then each round's tick run on the mirrored state, the same draws
    read and the books undone; the old rule read the same way, as a control;
(f) the 24: the split between the +x and -x neighbours, ranked by size, under every turn of the cube;
(g) the vacuum: light moving, matter and the held count at rest under term 6, the pointer where light alone passed;
(h) the two hardest lays of the old probe: e's tenths, its joint tenths one and two rounds apart, part 0 at 1:1;
(i) decision 29's dial over a full turn with the plan empty, and the raw sum with c struck there.

Usage: python3 -I g5_draw.py <src of main at 0df0e8385>
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
H, ODD = carry(W, 2, 0)  # W is even: H = W div 2, also every fine tooth's birth
SHAPE = (6, 6, 6)
ROWS = 5  # light re, im; matter re, im; the held count
ROUNDS, FROM = 420, 20  # the old probe's run: 420 rounds from the lay, read from round 21
N_HELD = 1000 * 1000
SEED = 20261030
SCALE = 10**12  # the whole unit for expectations summed over sizes that change from draw to draw
MILLION = 1000 * 1000


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, carry(a, b, 0)[1]
    return a


def per_mille(part, whole):
    return carry(1000 * part, whole, 0)[0]


def ppm(part, whole):
    return carry(MILLION * part, whole, 0)[0]


def shown(thousandths):
    whole, rest = carry(thousandths, 1000, 0)
    return f"{whole}.{rest:03d}"


def ceiling(a, b):
    return carry(a + b - 1, b, 0)[0]


def root(n):
    """The whole square root of n: the largest x with x x at most n, by Newton's steps in carries."""
    x, y = n, carry(n + 1, 2, 0)[0]
    while y < x:
        x, y = y, carry(y + carry(n, y, 0)[0], 2, 0)[0]
    return x


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
f2 = ceiling(g * g, 8 * kappa)  # lam = 4 f2 >= g^2 over 2 kappa, the least whole such
unit, l_re, l_im, m_re, m_im, held = -1, 0, 1, 2, 3, 4
monomials = [
    (f1, (held, m_re, m_re, unit)), (f1, (held, m_im, m_im, unit)),  # f1 k c
    (f2, (m_re, m_re, m_re, m_re)), (f2, (m_im, m_im, m_im, m_im)), (2 * f2, (m_re, m_re, m_im, m_im)),  # f2 c^2
    (f3, (held, held, unit, unit)), (-2 * f3 * N_HELD, (held, unit, unit, unit)),  # f3 (k - n)^2 less its constant
]
factor = np.array([f for f, _ in monomials], dtype=object)
legs = tuple(np.array([leg[i] for _, leg in monomials], dtype=np.intp) for i in range(4))
term6 = pushes(factor, legs)
A1 = [l_re, l_im, m_re, m_im, held]  # every row of the old probe's three A1 trains
TRAINS = (("light", (l_re, l_im)), ("matter", (m_re, m_im)), ("the held count", (held,)))


def layout(plan):
    return Layout(nb, spokes, meshes, np.full((1, 3 * sites), GRIP, dtype=object),
                  Gearing(W * ones, ones, ones.copy(), ones.copy()), plan, empty_read, empty_read)


lay0, lay6 = layout(empty_plan), layout(term6)


def generator(seed):
    """The old probe's integer carry sequence: each call gives a whole number within span of 0."""
    state = seed

    def pick(span):
        nonlocal state
        _, state = carry(1103515245 * state + 12345, 2147483648, 0)
        return carry(state, 2 * span + 1, 0)[1] - span

    return pick


def blank():
    return np.zeros((ROWS, sites), dtype=object), np.zeros((ROWS, sites), dtype=object)


def laid(a, b):
    """The state from its two slots, every fine tooth born at H and every drive's at 0."""
    return State(a, b, np.full((ROWS, sites), H, dtype=object), np.zeros((ROWS, sites), dtype=object))


def lays(seed=SEED):
    """The old lay: light as Animate's, matter at swings up to 10^5, the held count at n."""
    pick, (a, b) = generator(seed), blank()
    for i in range(sites):
        for row, (top, stride) in enumerate(((1000, 5), (1000, 5), (100000, 5000), (100000, 5000), (1000, 50))):
            a[row, i] = pick(top) + (N_HELD if row == held else 0)
            b[row, i] = a[row, i] - pick(stride)
    return laid(a, b)


def swing_lay(m_top, m_stride, packet):
    """The old (g)'s lays: a hot board (light as Animate's, matter to m_top) or a cold one (everything at rest, light
    at 0 and the held count at n, but one matter packet on the 3 by 3 by 3 Node-clocks at the centre, near m_top)."""
    pick, (a, b) = generator(7 if packet else SEED), blank()
    a[held, :], b[held, :] = N_HELD, N_HELD
    for i in range(sites):
        rest, z = carry(i, 6, 0)
        x, y = carry(rest, 6, 0)
        inside = x in (2, 3, 4) and y in (2, 3, 4) and z in (2, 3, 4)
        if packet and not inside:
            continue
        for row in (l_re, l_im, m_re, m_im):
            if packet and row in (l_re, l_im):
                continue
            light = row in (l_re, l_im)
            top, stride = (1000, 5) if light else (m_top, m_stride)
            base = m_top if packet else 0
            a[row, i] = base + pick(carry(top, 10, 0)[0] if packet else top)
            b[row, i] = a[row, i] - pick(carry(top, 20, 0)[0] if packet else stride)
    return laid(a, b)


def vacuum_lay():
    """The vacuum, as the hostile reader's g5_vacuum.py lays it: light moving at every Node-clock as Animate's,
    matter at rest at 0, the held count at rest at n."""
    pick, (a, b) = generator(7), blank()
    for i in range(sites):
        for row in (l_re, l_im):
            a[row, i] = pick(1000)
            b[row, i] = a[row, i] - pick(5)
    a[held, :], b[held, :] = N_HELD, N_HELD
    return laid(a, b)


def star(own):
    """A row of the board summed over each Node-clock and its six neighbours, as Python integers."""
    return (own + own[nb].sum(axis=0)).tolist()


def run(lay_out, s, rounds, read=None):
    """The act from s for the given rounds, s_t = tick(s_(t-1)), with read(t, s_(t-1), s_t) at each t from 1."""
    for t in range(1, rounds + 1):
        s_out = step.tick(lay_out, s)
        if read is not None:
            read(t, s, s_out)
        s = s_out
    return s


# ---- the draw, read inside the act: the same function serves the forward round and its run back
def pointers(lay_out, s_in, s_out, rows=A1):
    """The pointer e and its H at every Node-clock, for the round from s_in to s_out = tick(s_in)."""
    w = step.teeth(lay_out, s_in)  # the teeth the round used
    teeth = w[rows[0]]
    assert all(np.array_equal(w[row], teeth) for row in rows)  # one W at every row the pointer reads
    centred = (2 * s_in.r + 1 - w) + (2 * s_out.r + 1 - w)  # c(r_in) + c(r_out), each at its own teeth
    e, h = [], []
    for total, wx in zip(star(centred[rows].sum(axis=0)), teeth.tolist(), strict=True):
        _, u = carry(total, wx, 0)
        half, odd = carry(wx, 2, 0)
        assert odd == 0
        e.append(min(u, wx - u))
        h.append(half)
    return e, h


def drawn(e, h, sizes, rank=True):
    """The part drawn by the pointer e within H over whole sizes, and 1 where two sizes tie. The parts are ranked by
    size, the larger first, ties in their given order (all in their given order where rank is off); the part is the
    first ranked j with e L below C_(j+1) H, by cross products, the last ranked one at e = H."""
    order = sorted(range(len(sizes)), key=lambda k: -sizes[k]) if rank else list(range(len(sizes)))
    total, below = sum(sizes), 0
    tie = int(len(set(sizes)) < len(sizes))
    for k in order:
        below += sizes[k]
        if e * total < below * h:
            return k, tie
    return order[-1], tie


def sizes_at(a):
    """S1 = m_re^2 + 1 and S2 = m_im^2 + 1 at every Node-clock, from a now slot."""
    return [[re * re + 1, im * im + 1] for re, im in zip(a[m_re].tolist(), a[m_im].tolist(), strict=True)]


def pointer_run(lay_out, s, rows=A1):
    """Each read round's pointers, rounds FROM + 1 to ROUNDS: a list per round of (e, H) at every Node-clock."""
    got = []

    def read(t, s_in, s_out):
        if t > FROM:
            e, h = pointers(lay_out, s_in, s_out, rows)
            got.append(list(zip(e, h, strict=True)))

    run(lay_out, s, ROUNDS, read)
    return got


# ---- the statistics, whole numbers in thousandths
def tenth(e, h):
    return min(carry(10 * e, h, 0)[0], 9)  # e = H falls in the last tenth


def chi_tenths(pairs):
    """Chi-square of the tenths of e within H on 9, in thousandths."""
    counts = [0] * 10
    for e, h in pairs:
        counts[tenth(e, h)] += 1
    total = sum(counts)
    return carry(1000 * sum((10 * c - total) ** 2 for c in counts), 10 * total, 0)[0]


def chi_joint(pairs):
    """Chi-square of a 10 by 10 table of tenths against the product of its margins, in thousandths, with its degrees
    of freedom, (filled rows - 1) (filled columns - 1); a cell on an empty margin is left out."""
    table = [[0] * 10 for _ in range(10)]
    for x, y in pairs:
        table[x][y] += 1
    n = len(pairs)
    rows = [sum(line) for line in table]
    cols = [sum(table[i][j] for i in range(10)) for j in range(10)]
    total = 0
    for i in range(10):
        for j in range(10):
            den = n * rows[i] * cols[j]
            if den:
                total += carry(10**9 * (n * table[i][j] - rows[i] * cols[j]) ** 2, den, 0)[0]
    filled = (sum(int(r > 0) for r in rows) - 1) * (sum(int(c > 0) for c in cols) - 1)
    return carry(total, MILLION, 0)[0], filled


def z2_fixed(zero, total, s1, s2):
    """z^2 of part 0's count over the draws at fixed sizes: the squared gap from the expected count over the
    binomial variance, (L zero - total s1)^2 over total s1 s2, in thousandths."""
    lsum = s1 + s2
    return carry(1000 * (lsum * zero - total * s1) ** 2, total * s1 * s2, 0)[0]


def born_fixed(zero, total, s1, s2):
    expected = carry(total * s1, s1 + s2, 0)[0]
    return f"part 0 in {zero} of {total} (expected {expected}), z^2 {shown(z2_fixed(zero, total, s1, s2))}"


def same_half(rounds_e):
    """Same half per mille: one Node-clock two rounds running, and one Mesh apart (+x) in one round."""
    hs = [[int(2 * e >= h) for e, h in row] for row in rounds_e]
    running = sum(int(hs[t][i] == hs[t + 1][i]) for t in range(len(hs) - 1) for i in range(sites))
    mesh = sum(int(row[i] == row[int(nb[0, i])]) for row in hs for i in range(sites))
    return per_mille(running, (len(hs) - 1) * sites), per_mille(mesh, len(hs) * sites)


# ==== (a)
def pitch_of(lay_out):
    """Each train's pitch: the gcd of W and every move of each of its fine teeth, ROUNDS rounds from the lay."""
    pitch = [W, W, W]

    def read(t, s_in, s_out):
        moved = s_out.r - s_in.r
        for k, (_, rows) in enumerate(TRAINS):
            _, rest = carry(moved[list(rows)], pitch[k], 0)
            for x in rest.ravel().tolist():
                if x:
                    pitch[k] = gcd(pitch[k], x)

    run(lay_out, lays(), ROUNDS, read)
    return pitch


def named(p):
    return "the grip" if p == GRIP else str(p)


assert ODD == 0
print(f"(a) W = {W}, the grip {GRIP}, H = W div 2 = {H}")
print(f"    term 6: g = {g}, kappa = {kappa}, lam = 4 f2 = {4 * f2}, n = {N_HELD}")
print(f"    2 kappa lam >= g^2: {2 * kappa * 4 * f2 >= g * g}")
print(f"    each train's pitch, the gcd of W and every move of each of its fine teeth, {ROUNDS} rounds from the lay:")
pitches = {}
for name, lay_out in (("the plan empty", lay0), ("term 6", lay6)):
    pitch = pitch_of(lay_out)
    pitches[name] = pitch
    print(f"    {name}: light {named(pitch[0])}, matter {named(pitch[1])}, the held count {named(pitch[2])}")
    print(f"      W over the pitch: {', '.join(str(carry(W, p, 0)[0]) for p in pitch)} values")

# ==== (b) and (c): one run of term 6 from the old lay, read in rounds FROM + 1 to ROUNDS
pitch_rows = np.zeros((ROWS, 1), dtype=object)  # each row's pitch at load, from (a)'s gcds under term 6
for k, (_, rows) in enumerate(TRAINS):
    for row in rows:
        pitch_rows[row, 0] = pitches["term 6"][k]
reads = []


def read_bc(t, s_in, s_out):
    if t > FROM:
        e, h = pointers(lay6, s_in, s_out)
        digits, _ = carry(s_out.r, pitch_rows, 0)
        reads.append((t, e, h, sizes_at(s_in.a), star(s_out.r.sum(axis=0)), star(digits.sum(axis=0))))


run(lay6, lays(), ROUNDS, read_bc)
rounds_b = [list(zip(e, h, strict=True)) for _, e, h, _, _, _ in reads]
flat_b = [p for row in rounds_b for p in row]
N = len(flat_b)
assert all(h == H for _, h in flat_b)
es = [e for e, _ in flat_b]
lattice = 0
for e in es:
    lattice = gcd(lattice, e - es[0])
ordered = sorted(es)
top = 0  # the star discrepancy's numerator over N H: the largest of j H - e_(j) N and e_(j) N - (j - 1) H
for j, e in enumerate(ordered, start=1):
    top = max(top, j * H - e * N, e * N - (j - 1) * H)

SPLITS = ((1, 1, "1 : 1"), (1, 2, "1 : 2"), (3, 7, "3 : 7"), (10**6, 3 * 10**6, "10^6 : 3 x 10^6"),
          (10**30, 3 * 10**30, "10^30 : 3 x 10^30"))
c_lines = []
worst_gap, worst_den, within = 0, 1, True
for s1, s2, label in SPLITS:
    lsum = s1 + s2
    by_e = ties = raw = digit = dial = 0
    for t, e_row, h_row, _, v_row, d_row in reads:
        for e, h, v, dsum in zip(e_row, h_row, v_row, d_row, strict=True):
            part, tie = drawn(e, h, [s1, s2])
            by_e += int(part == 0)
            ties += tie
            raw += int(carry(v, lsum, 0)[1] < s1)
            digit += int(carry(dsum, lsum, 0)[1] < s1)
            dial += int(carry(t + dsum, lsum, 0)[1] < s1)
    gap = abs(lsum * by_e - N * s1)  # |freq(part 0) - share| = gap over N L
    if gap * worst_den > worst_gap * N * lsum:
        worst_gap, worst_den = gap, N * lsum
    within = within and gap * H <= 2 * top * lsum
    c_lines.append(f"    sizes {label}, part 0 expected in {carry(N * s1, lsum, 0)[0]} of {N}:")
    c_lines.append(f"      (i) the new rule on e, ranked by size, ties {ties}: {born_fixed(by_e, N, s1, s2)}")
    c_lines.append(f"      (ii) the raw sum mod L, c struck: {born_fixed(raw, N, s1, s2)}")
    c_lines.append(f"      (iii) decision 29's digits, c struck: {born_fixed(digit, N, s1, s2)}")
    c_lines.append(f"      (iv) decision 29's digits with its dial, d = (t + D) mod L: {born_fixed(dial, N, s1, s2)}")
zero = ties = expected = variance = 0
for _, e_row, h_row, size_row, _, _ in reads:
    for e, h, (s1, s2) in zip(e_row, h_row, size_row, strict=True):
        part, tie = drawn(e, h, [s1, s2])
        zero += int(part == 0)
        ties += tie
        expected += carry(SCALE * s1, s1 + s2, 0)[0]
        variance += carry(SCALE * SCALE * s1 * s2, (s1 + s2) * (s1 + s2), 0)[0]
c_lines.append("    sizes read from the state, S1 = m_re^2 + 1 and S2 = m_im^2 + 1 at x in s_in's now slot, by e"
               " ranked by size:")
c_lines.append(f"      part 0 in {zero} of {N} (expected {carry(expected, SCALE, 0)[0]}), z^2"
               f" {shown(carry(1000 * (SCALE * zero - expected) ** 2, variance, 0)[0])}, ties {ties}")

rows_same, mesh_same = same_half(rounds_b)
print(f"(b) the pointer e under term 6, rounds {FROM + 1} to {ROUNDS} at all {sites} Node-clocks, {N} draws:")
print(f"    {len(set(es))} distinct values; every e even: {all(carry(e, 2, 0)[1] == 0 for e in es)}; the gcd of all"
      f" differences of e {lattice}, every e {carry(es[0], lattice, 0)[1]} more than a multiple of it")
print(f"    e at 0 in {es.count(0)} draws and at H in {es.count(H)}")
print(f"    chi-square of the tenths of H on 9: {shown(chi_tenths(flat_b))}")
print(f"    in one half, two rounds running {rows_same}, one Mesh apart {mesh_same} per mille (500 for independent"
      f" draws)")
print(f"    the star discrepancy D_N of e over H: {ppm(top, N * H)} ppm; the bound 2 D_N: {ppm(2 * top, N * H)} ppm")
# the Kolmogorov law of the root of N times D_N for independent uniform draws: its mean 869, and 1358 passed one
# time in 20, in thousandths
print(f"    the root of N times D_N: {shown(carry(MILLION * top, H * root(N * MILLION), 0)[0])} (for independent"
      f" uniform draws, mean {shown(869)}, above {shown(1358)} one time in 20)")
print(f"    the largest |freq(part) - share| over (c)'s five Born tests by e: {ppm(worst_gap, worst_den)} ppm; each"
      f" within 2 D_N: {within}")

p6 = pitches["term 6"]
print(f"(c) Born, part 0 of sizes S1 and S2, term 6, the draws of (b); t the round, s_t = tick(s_(t-1)), {FROM + 1} to"
      f" {ROUNDS};")
print("    V the raw sum of the fine teeth over x and its six neighbours in s_t; D the sum there of their digits,")
print(f"    r div the row's pitch at load from (a): light {named(p6[0])}, matter {named(p6[1])}, the held count"
      f" {named(p6[2])};")
print("    (ii) to (iv) draw part 0 where d < S1:")
for line in c_lines:
    print(line)

# ==== (d)
print(f"(d) six lays, the old lay's generator at six seeds, term 6, rounds {FROM + 1} to {ROUNDS}, {N} draws each:")
chis, z2s = [], []
for seed in (SEED, 1, 2, 3, 4, 5):
    flat = flat_b if seed == SEED else [p for row in pointer_run(lay6, lays(seed)) for p in row]
    chis.append(chi_tenths(flat))
    half = sum(int(drawn(e, h, [1, 1])[0] == 0) for e, h in flat)
    z2s.append(z2_fixed(half, len(flat), 1, 1))
    print(f"    seed {seed}: chi-square of e's tenths on 9 {shown(chis[-1])}; at 1:1"
          f" {born_fixed(half, len(flat), 1, 1)}")
mean_z2 = carry(1000 * (sum(chis) - 6 * 9000) ** 2, 108 * MILLION, 0)[0]  # (mean - 9)^2 over 18 div 6
print(f"    mean chi-square {shown(carry(sum(chis), 6, 0)[0])} over the six; the null: mean 9, sd"
      f" {shown(root(18 * MILLION))} for one lay, {shown(root(3 * MILLION))} for the mean of six;")
print(f"    the mean's z^2 {shown(mean_z2)}")
print(f"    the six z^2 at 1:1: {', '.join(shown(z) for z in z2s)}")

# ==== (e)
BACK = 300
print(f"(e) the run back inside the act, term 6, {BACK} rounds from the old lay:")
print(f"    forward: s_t = tick(s_(t-1)) for t = 1 to {BACK}; a draw at every Node-clock from (s_(t-1), s_t),")
print("    at 1:1 and at the sizes in s_(t-1)'s now slot, each adding 1 to books[x][part]")
print(f"    backward: for t = {BACK} down to 1, m = mirror(s_t), m_out = tick(m); the same draw from (m, m_out),")
print("    taking 1 from the books; s_(t-1) recovered as mirror(m_out)")
states = [lays()]
forward = []
books = [[[0, 0] for _ in range(sites)] for _ in range(3)]  # at 1:1, at the state's sizes, the control's at 1:1


def old_rule(s_after):
    """The old rule, d = V mod W on the raw teeth of the state after the tick, its part at 1:1."""
    return [int(2 * carry(v, W, 0)[1] >= W) for v in star(s_after.r.sum(axis=0))]


for t in range(1, BACK + 1):
    s_in = states[-1]
    s_out = step.tick(lay6, s_in)
    e, h = pointers(lay6, s_in, s_out)
    sizes = sizes_at(s_in.a)
    one = [drawn(e[x], h[x], [1, 1])[0] for x in range(sites)]
    by_size = [drawn(e[x], h[x], sizes[x]) for x in range(sites)]
    control = old_rule(s_out)
    for x in range(sites):
        books[0][x][one[x]] += 1
        books[1][x][by_size[x][0]] += 1
        books[2][x][control[x]] += 1
    forward.append((e, one, [p for p, _ in by_size], control))
    states.append(s_out)
s = states[-1]
same_e = same_one = same_size = same_control = back_ties = recovered = by_untick = 0
for t in range(BACK, 0, -1):
    m = step.mirror(lay6, s)
    m_out = step.tick(lay6, m)
    e, h = pointers(lay6, m, m_out)
    sizes = sizes_at(m.a)
    one = [drawn(e[x], h[x], [1, 1])[0] for x in range(sites)]
    by_size = [drawn(e[x], h[x], sizes[x]) for x in range(sites)]
    control = old_rule(m_out)
    e_f, one_f, size_f, control_f = forward[t - 1]
    for x in range(sites):
        same_e += int(e[x] == e_f[x])
        same_one += int(one[x] == one_f[x])
        same_size += int(by_size[x][0] == size_f[x])
        same_control += int(control[x] == control_f[x])
        back_ties += by_size[x][1]
        books[0][x][one[x]] -= 1
        books[1][x][by_size[x][0]] -= 1
        books[2][x][control[x]] -= 1
    before = step.mirror(lay6, m_out)
    by_untick += int(all(np.array_equal(p, q) for p, q in zip(before, step.untick(lay6, s), strict=True)))
    recovered += int(all(np.array_equal(p, q) for p, q in zip(before, states[t - 1], strict=True)))
    s = before
draws = BACK * sites
home = all(np.array_equal(p, q) for p, q in zip(s, lays(), strict=True))
print(f"    the pointer e equal at {same_e} of {draws} draws")
print(f"    the part equal at {same_one} of {draws} (1:1) and at {same_size} of {draws} (the state's sizes, ties"
      f" {back_ties})")
print(f"    the books all 0 at the end: {all(c == 0 for c in sum(books[0], []))} (1:1),"
      f" {all(c == 0 for c in sum(books[1], []))} (the state's sizes)")
print(f"    s_(t-1) recovered bit for bit at {recovered} of {BACK} rounds; mirror(m_out) equal to the engine's untick"
      f" at {by_untick} of {BACK}")
print(f"    the lay returns bit for bit: {home}")
print("    control, the old rule d = V mod W on the raw teeth of the state after the tick, read the same way on"
      " (m, m_out):")
print(f"      the part at 1:1 equal at {same_control} of {draws}; its books end with"
      f" {sum(int(c != 0) for c in sum(books[2], []))} of {2 * sites} entries not 0")


# ==== (f)
def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


rotations = []
for order in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
    for signs in ((1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1), (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1)):
        m = [[signs[i] * int(order[i] == j) for j in range(3)] for i in range(3)]
        if det3(m) == 1:
            rotations.append(m)


def image_of(m):
    """Each Node-clock's image under the turn m, about the board's corner, wrapped."""
    image = []
    for i in range(sites):
        rest, z = carry(i, 6, 0)
        x, y = carry(rest, 6, 0)
        xs = [carry(sum(m[a][b] * (x, y, z)[b] for b in range(3)), 6, 0)[1] for a in range(3)]
        image.append((xs[0] * 6 + xs[1]) * 6 + xs[2])
    return image


def turned(s, image):
    out = State(*(np.empty_like(part) for part in s))
    for part, source in zip(out, s, strict=True):
        part[:, image] = source
    return out


def side(e, h, a_in, x, axis, sized=True, rank=True):
    """The site drawn at x between its + and - neighbours along an axis, + first in the given order; the sizes
    m_re^2 + 1 at those two in the now slot a_in, or 1 and 1; and 1 where the sizes tie."""
    plus, minus = int(nb[2 * axis, x]), int(nb[2 * axis + 1, x])
    sizes = [int(a_in[m_re, plus]) ** 2 + 1, int(a_in[m_re, minus]) ** 2 + 1] if sized else [1, 1]
    part, tie = drawn(e, h, sizes, rank)
    return (plus, minus)[part], tie


TURN_ROUNDS = 5
path = [lays()]
for _ in range(TURN_ROUNDS):
    path.append(step.tick(lay6, path[-1]))
rows_f = []
for m in rotations:
    image = image_of(m)
    axis_to = [m[a][0] for a in range(3)]  # the image of +x: the turn's first column
    new_axis = [a for a in range(3) if axis_to[a] != 0][0]
    act = e_same = ranked = given = equal = ties = 0
    for t in range(1, TURN_ROUNDS + 1):
        s_in, s_out = path[t - 1], path[t]
        e, h = pointers(lay6, s_in, s_out)
        t_in = turned(s_in, image)
        t_out = step.tick(lay6, t_in)
        act += int(all(np.array_equal(p, q) for p, q in zip(t_out, turned(s_out, image), strict=True)))
        et, ht = pointers(lay6, t_in, t_out)
        for x in range(sites):
            j = image[x]
            e_same += int(et[j] == e[x])
            out, tie = side(e[x], h[x], s_in.a, x, 0)
            ranked += int(side(et[j], ht[j], t_in.a, j, new_axis)[0] == image[out])
            ties += tie
            out = side(e[x], h[x], s_in.a, x, 0, rank=False)[0]
            given += int(side(et[j], ht[j], t_in.a, j, new_axis, rank=False)[0] == image[out])
            out = side(e[x], h[x], s_in.a, x, 0, sized=False)[0]
            equal += int(side(et[j], ht[j], t_in.a, j, new_axis, sized=False)[0] == image[out])
    rows_f.append((axis_to[new_axis], act, e_same, ranked, given, equal, ties))
print(f"(f) the 24: {len(rotations)} turns; rounds 1 to {TURN_ROUNDS} from the old lay, each input state turned and"
      f" ticked;")
print("    at x the split between its +x and -x neighbours, sizes m_re^2 + 1 at those two in s_in's now slot;")
print("    covariant where the turned board's draw at x's image is the image of the original's;")
print(f"    {TURN_ROUNDS * sites} draws a turn, each count listed once:")
for sign in (1, -1):
    sel = [r for r in rows_f if r[0] == sign]
    print(f"    {len(sel)} turns taking +x to a {'+' if sign == 1 else '-'} direction:")
    print(f"      the act turned with the board in {sorted({r[1] for r in sel})} of {TURN_ROUNDS} rounds;"
          f" e equal at the image at {sorted({r[2] for r in sel})}")
    print(f"      ranked by size: covariant at {sorted({r[3] for r in sel})}, ties {sorted({r[6] for r in sel})}")
    print(f"      the parts in their given order, + side first, not ranked: covariant at {sorted({r[4] for r in sel})}")
    print(f"      sizes 1 and 1, all ties, broken in the given order: covariant at {sorted({r[5] for r in sel})}")

# ==== (g)
VACUUM = 400
print(f"(g) the vacuum: term 6; light laid moving at every Node-clock (seed 7, as the hostile reader's g5_vacuum.py);"
      f" matter")
print(f"    laid at rest at 0 and the held count at rest at n; {VACUUM} rounds. Light taken as T1, as in the theory, so"
      f" P runs")
print("    over matter and the held count; light passed every Node-clock and nothing else moved")
seen = [set() for _ in range(sites)]
seen_all = [set() for _ in range(sites)]
light_teeth = set()
vac_zero = vac_zero_all = 0


def read_g(t, s_in, s_out):
    global vac_zero, vac_zero_all
    e, h = pointers(lay6, s_in, s_out, [m_re, m_im, held])
    e_all, h_all = pointers(lay6, s_in, s_out)
    for x in range(sites):
        seen[x].add(e[x])
        seen_all[x].add(e_all[x])
        vac_zero += int(drawn(e[x], h[x], [1, 1])[0] == 0)
        vac_zero_all += int(drawn(e_all[x], h_all[x], [1, 1])[0] == 0)
    light_teeth.update(s_out.r[l_re].tolist() + s_out.r[l_im].tolist())


last = run(lay6, vacuum_lay(), VACUUM, read_g)
values = set().union(*seen)
at_rest = all(v == 0 for v in last.a[m_re].tolist() + last.a[m_im].tolist()) and all(
    v == N_HELD for v in last.a[held].tolist())
on_grip = all(carry(r - H, GRIP, 0)[1] == 0 for r in light_teeth)
print(f"    matter and the held count still at rest after {VACUUM} rounds: {at_rest}")
print(f"    e: at most {max(len(v) for v in seen)} distinct value at any Node-clock, {len(values)} over the board, e ="
      f" {sorted(values)}; frozen in every round: {all(len(v) == 1 for v in seen)}")
print(f"    light's own fine teeth: {len(light_teeth)} distinct values, each on the grip's lattice about H: {on_grip}")
print(f"    a 1:1 split there: part 0 in {vac_zero} of {VACUUM * sites} draws")
print(f"    with light's rows counted in P (the probe's A1 trains, as in (b)): at most {max(len(v) for v in seen_all)}"
      f" distinct e")
print(f"    at a Node-clock, {len(set().union(*seen_all))} over the board; a 1:1 split, part 0 in {vac_zero_all} of"
      f" {VACUUM * sites}")

# ==== (h)
print(f"(h) the two hardest lays of the old probe, term 6, the held count laid at n, e read in rounds {FROM + 1} to"
      f" {ROUNDS};")
print("    the lags pool one Node-clock's pairs over the Node-clocks read:")
centre = [(x * 6 + y) * 6 + z for x in (2, 3, 4) for y in (2, 3, 4) for z in (2, 3, 4)]
for name, lay_h, read_at in (("a hot board, matter laid to 10 counts, all 216 Node-clocks", swing_lay(10, 1, False),
                              list(range(sites))),
                             ("a cold board, one packet near 100 counts, its 27 Node-clocks", swing_lay(100, 0, True),
                              centre)):
    picked = [[row[i] for i in read_at] for row in pointer_run(lay6, lay_h)]
    flat = [p for row in picked for p in row]
    lags = []
    for lag in (1, 2):
        pairs = [(tenth(*picked[t][k]), tenth(*picked[t + lag][k])) for t in range(len(picked) - lag)
                 for k in range(len(read_at))]
        chi, free = chi_joint(pairs)
        lags.append(f"at t and t + {lag}: {shown(chi)} on {free}")
    half = sum(int(drawn(e, h, [1, 1])[0] == 0) for e, h in flat)
    print(f"    {name}: {len(set(e for e, _ in flat))} distinct e of {len(flat)}")
    print(f"      chi-square of e's tenths on 9: {shown(chi_tenths(flat))}; joint tenths {'; '.join(lags)}")
    print(f"      at 1:1 {born_fixed(half, len(flat), 1, 1)}")

# ==== (i)
TURN = 1000
mods = set()
dial_zero = [0] * sites
struck_zero = 0


def read_i(t, s_in, s_out):
    global struck_zero
    for x, v in enumerate(star(s_out.r.sum(axis=0))):
        _, kept = carry(v, TURN, 0)
        mods.add(kept)
        dial_zero[x] += int(carry(t + v, TURN, 0)[1] < 500)
        struck_zero += int(kept < 500)


run(lay0, lays(), TURN, read_i)
print(f"(i) decision 29's dial with the plan empty, the old lay, {TURN} rounds; L = {TURN}, sizes 500 and 500;")
print("    V the raw sum of the fine teeth over x and its six neighbours in s_t:")
print(f"    V mod {TURN} takes {sorted(mods)} at every Node-clock in every round; frozen: {len(mods) == 1}")
print(f"    the dial, d = (t + V) mod {TURN}, t the round: part 0 exactly 500 times at each of the {sites} Node-clocks:"
      f" {all(c == 500 for c in dial_zero)}")
print(f"    c struck, d = V mod {TURN}: part 0 in {struck_zero} of {TURN * sites} draws")
