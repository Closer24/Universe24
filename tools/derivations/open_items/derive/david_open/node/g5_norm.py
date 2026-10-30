"""G5, the split click's draw, read by Big Pic's norm pointer: each round's centred fine teeth, in and out, squared.

Whole numbers alone, every division Rule3's carry: no float, root, logarithm, exponential or search, no function
of the turn's arc, and no state laid by one. The board, the lays, term 6, the statistics and the draw's machinery are
g5_draw.py's (the third text's probe, read and not written): 6 by 6 by 6 Node-clocks; light, matter and the held
count, all three trains A1 on this board; the teeth W six grips. Big Pic's candidate (#2187 6528531569, item 3), not
derived: at a drawing Node-clock x, for the round from s_in to s_out = tick(s_in), with T_row the teeth the round's
carry used at each row, c(r) = 2 r + 1 - T_row and

    Q = the sum, over x, its six neighbours and every row of every train, of c(r_in)^2 + c(r_out)^2;
    u = Q mod T_f by one carry, T_f = W on this board.

The mirror sends each c to -c, so Q needs no fold. Every odd square is 1 more than a multiple of 8, so Q is its count
of terms more than a multiple of 8, and W is a multiple of 128: u stands on one class mod 8 at every draw. One halving
leaves a step of 4; one carry by 8 reaches every residue of T8 = W div 8. The draw reads v = u div 8 against T8, the
parts' half-open cells in their own order: part i where C_(i-1) T8 <= v L < C_i T8, C_i the sizes of parts 0 to i
summed and L their total. Beside it, as the control, the third text's pointer e: P, the sum of c(r_in) + c(r_out)
over x, its six neighbours and the A1 rows, folded to a half turn, drawn by its own rule.

(a) the residue check: Q mod T over one, two and three rows, each row's c over its whole range, at the primes 97, 101
    and 103 and at small even dials; and at W, each row's tooth on the probe's lattices of 6, 16, 25 and 48 points;
(b) the run back inside the act: 300 rounds out from the old lay and back, against a control at chance;
(c) the 24: Q at the image under every turn of the cube, the draw's covariance in the parts' own order; and the
    trains' own signed permutations, under which Q stands and P moves;
(d) the third text's battery on the old lay and on six lays;
(e) the hot board and the cold packet, the held count's row alone, and the Fano factors in windows of 10 to 400 rounds;
(f) the vacuum: term 6, light laid moving at every Node-clock, matter and the held count at rest, 400 rounds;
(g) the readers' single rotations on G3's ring of 128, the merge at one Node-clock and its two neighbours: every lay
    whole, one Pythagorean hand (a = 7, b = 1), turned by the act itself for its 64 start phases;
(h) the conditional draw and the backward pass's step, the third text's (p) and (q);
(i) one row's square up to a quarter turn and its sign, at small dials and at W on the lattices of W/6, W/16 and
    W/48 (the fourth text's mathematician's NB1, his g5v4_algebra ported);
(j) the held count displaced off n, matter at rest, every row read (his g5v4_held_vacuum, ported);
(k) the cells where 8 does not divide T_f: T8 as T_f div 8 and as the ceiling (T_f + 7) div 8 (his NB2, the
    physicist's D3).

Usage: python3 -I g5_norm.py <src of main at 0df0e8385>
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import pushes  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402

GRIP = 15162856759112389 * 1000 * 1000
W = 6 * GRIP
H, ODD = carry(W, 2, 0)  # W is even: H = W div 2, also every fine tooth's birth
T8, ODD8 = carry(W, 8, 0)  # the halved form's teeth: W is a multiple of 128
SHAPE = (6, 6, 6)
ROWS = 5  # light re, im; matter re, im; the held count
ROUNDS, FROM = 420, 20  # the old probe's run: 420 rounds from the lay, read from round 21
N_HELD = 1000 * 1000
SEED = 20261030
SCALE = 10**12  # the whole unit for expectations summed over sizes that change from draw to draw
MILLION = 1000 * 1000
Z5, Z1 = 3841, 6635  # a z^2 on 1: the 5 and the 1 per cent points, in thousandths
CHI9 = (16919, 21666, 27877)  # the tenths on 9: the 5, the 1 and the one-tenth per cent points, in thousandths
KS_MEAN, KS_5 = 822, 1844  # N times D_N squared, the Kolmogorov law: its mean and its 5 per cent point, thousandths


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


def nonneg(n):
    """The law's one whether: 1 where n is at least 0 and 0 below, by one carry, n div (n n + 1) being 0 or -1."""
    return carry(n, n * n + 1, 0)[0] + 1


def odds(num, den):
    """A z^2 on 1, num over den, in its odds class: below Z5, up to Z1, or above, each in thousandths."""
    labels = (f"below {shown(Z5)}", f"{shown(Z5)} to {shown(Z1)}", f"above {shown(Z1)}")
    return labels[nonneg(1000 * num - Z5 * den) + nonneg(1000 * num - Z1 * den - 1)]


nb = board(SHAPE)
sites = nb.shape[1]
spokes, meshes = geometry(nb, 3)
ones = np.ones((ROWS, 1), dtype=object)
empty_read = Read(np.zeros(0, dtype=np.intp), np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))
empty_plan = Plan(*(np.zeros(0, dtype=np.intp),) * 3, np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))

# term 6's strengths, G3's probe numbers as g5_draw.py lays them: the spring g n = W div 400, kappa = W div 16, lam
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
ALL = [l_re, l_im, m_re, m_im, held]  # every row of every train: the norm pointer's, and the third text's A1 rows here
TERMS = 2 * 7 * len(ALL)  # c(r_in)^2 and c(r_out)^2 at seven Node-clocks on five rows
CLASS = carry(TERMS, 8, 0)[1]
lay6 = Layout(nb, spokes, meshes, np.full((1, 3 * sites), GRIP, dtype=object),
              Gearing(W * ones, ones, ones.copy(), ones.copy()), term6, empty_read, empty_read)


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


# ---- the two pointers, read inside the act: the same functions serve the forward round and its run back
def teeth_read(lay_out, s_in, rows):
    """The teeth the round's carry used, read at s_in's now slot; one W at every row read on this board."""
    w = step.teeth(lay_out, s_in)
    for row in rows:
        assert all(x == W for x in w[row].tolist())
    return w


def norm_reads(lay_out, s_in, s_out, rows=ALL):
    """Big Pic's norm pointer at every Node-clock: (Q, u, v), u = Q mod W by one carry and v = u div 8 by another."""
    w = teeth_read(lay_out, s_in, rows)
    c_in, c_out = 2 * s_in.r + 1 - w, 2 * s_out.r + 1 - w
    squares = c_in * c_in + c_out * c_out
    reads = []
    for total in star(squares[rows].sum(axis=0)):
        _, u = carry(total, W, 0)
        v, _ = carry(u, 8, 0)
        reads.append((total, u, v))
    return reads


def one_sided(lay_out, s_in, s_out, rows=ALL):
    """The control: the norm of the teeth after the tick alone, c(r_out)^2 summed, its v at every Node-clock."""
    w = teeth_read(lay_out, s_in, rows)
    c_out = 2 * s_out.r + 1 - w
    return [carry(carry(total, W, 0)[1], 8, 0)[0] for total in star((c_out * c_out)[rows].sum(axis=0))]


def pointers(lay_out, s_in, s_out, rows=ALL):
    """The third text's pointer e at every Node-clock: P mod W folded to [0, H]."""
    w = teeth_read(lay_out, s_in, rows)
    centred = (2 * s_in.r + 1 - w) + (2 * s_out.r + 1 - w)
    e = []
    for total in star(centred[rows].sum(axis=0)):
        _, u = carry(total, W, 0)
        e.append(min(u, W - u))
    return e


def cell(x, teeth, sizes):
    """The part whose half-open cell holds x within [0, teeth): part i where C_(i-1) teeth <= x L < C_i teeth, the
    parts in their own order, C_i the sizes of parts 0 to i summed and L their total; no rank, and no edge, since x
    stands below teeth and the cells cover the turn."""
    total, part, below = sum(sizes), 0, 0
    for k, size in enumerate(sizes):
        above = below + size
        part += k * nonneg(x * total - below * teeth) * nonneg(above * teeth - 1 - x * total)
        below = above
    return part


def drawn(e, h, sizes):
    """The third text's rule on e within [0, H]: part i where C_(i-1) H <= e L < C_i H; e = H to the last part of
    nonzero size, whose interval is closed there."""
    total, part, below = sum(sizes), 0, 0
    for k, size in enumerate(sizes):
        above = below + size
        closing = nonneg(above - total) * nonneg(size - 1)
        part += k * nonneg(e * total - below * h) * nonneg(above * h - 1 + closing - e * total)
        below = above
    return part


def sizes_at(a):
    """S1 = m_re^2 + 1 and S2 = m_im^2 + 1 at every Node-clock, from a now slot."""
    return [[re * re + 1, im * im + 1] for re, im in zip(a[m_re].tolist(), a[m_im].tolist(), strict=True)]


def area(s):
    """The swept area m_re p_im - m_im p_re at every Node-clock, p = W (a - b) + r (the first text's key test)."""
    p_re = W * (s.a[m_re] - s.b[m_re]) + s.r[m_re]
    p_im = W * (s.a[m_im] - s.b[m_im]) + s.r[m_im]
    return (s.a[m_re] * p_im - s.a[m_im] * p_re).tolist()


# ---- the statistics, whole numbers in thousandths; a pointer x stands within [0, scale): v with T8, e with H
def zero_count(values, scale, s1, s2):
    """Part 0's count of two parts, s1 then s2 in their own order: x (s1 + s2) < s1 scale, the cell rule's first
    cell; for e within [0, H] the same as the third text's rule, whose edge e = H goes to part 1."""
    lsum, bound = s1 + s2, s1 * scale
    return sum(int(x * lsum < bound) for x in values)


def tenth(x, scale):
    return min(carry(10 * x, scale, 0)[0], 9)  # e = H falls in the last tenth


def chi_tenths(values, scale):
    """Chi-square of the tenths on 9, in thousandths."""
    counts = [0] * 10
    for x in values:
        counts[tenth(x, scale)] += 1
    total = sum(counts)
    return carry(1000 * sum((10 * c - total) ** 2 for c in counts), 10 * total, 0)[0]


def chi_joint(pairs):
    """Chi-square of a 10 by 10 table of tenths against the product of its margins, in thousandths, with the count it
    stands on, (filled rows - 1) (filled columns - 1); a cell on an empty margin is left out."""
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


def discrepancy(values, scale):
    """The star discrepancy's numerator over N times scale: the largest of j scale - x_(j) N and x_(j) N - (j - 1)
    scale, over the sorted draws."""
    n, top = len(values), 0
    for j, x in enumerate(sorted(values), start=1):
        top = max(top, j * scale - x * n, x * n - (j - 1) * scale)
    return top


def nd2(top, n, scale):
    """N times D_N squared, in thousandths."""
    return carry(1000 * top * top, n * scale * scale, 0)[0]


def z2_fixed(zero, total, s1, s2):
    """z^2 of part 0's count at fixed sizes: (L zero - total s1)^2 over total s1 s2, in thousandths."""
    return carry(1000 * ((s1 + s2) * zero - total * s1) ** 2, total * s1 * s2, 0)[0]


def odds_fixed(zero, total, s1, s2):
    return odds(((s1 + s2) * zero - total * s1) ** 2, total * s1 * s2)


def born_fixed(zero, total, s1, s2):
    expected = carry(total * s1, s1 + s2, 0)[0]
    return (f"part 0 in {zero} of {total} (expected {expected}), z^2 {shown(z2_fixed(zero, total, s1, s2))},"
            f" {odds_fixed(zero, total, s1, s2)}")


def z2_halves(count, n):
    """A count against half of n: z^2 = (2 count - n)^2 over n, in thousandths, with its odds class."""
    return f"z^2 {shown(carry(1000 * (2 * count - n) ** 2, n, 0)[0])}, {odds((2 * count - n) ** 2, n)}"


def halves(rounds_x, scale):
    """Same half as counts, each with its pairs: one Node-clock two rounds running; one Mesh apart (+x), one round."""
    hs = [[int(2 * x >= scale) for x in row] for row in rounds_x]
    running = sum(int(hs[t][i] == hs[t + 1][i]) for t in range(len(hs) - 1) for i in range(len(hs[0])))
    mesh = sum(int(row[i] == row[int(nb[0, i])]) for row in hs for i in range(sites))
    return running, (len(hs) - 1) * len(hs[0]), mesh, len(hs) * sites


SPLITS = ((1, 1, "1 : 1"), (1, 2, "1 : 2"), (3, 7, "3 : 7"), (10**6, 3 * 10**6, "10^6 : 3 x 10^6"),
          (10**30, 3 * 10**30, "10^30 : 3 x 10^30"))


def state_born(values, sizes, scale, rule):
    """Part 0 at the state's sizes, draw by draw: its count, the expectation and the binomial variance in units of
    SCALE, and z^2 in thousandths."""
    zero = expected = variance = 0
    for x, (s1, s2) in zip(values, sizes, strict=True):
        zero += int(rule(x, scale, [s1, s2]) == 0)
        expected += carry(SCALE * s1, s1 + s2, 0)[0]
        variance += carry(SCALE * SCALE * s1 * s2, (s1 + s2) * (s1 + s2), 0)[0]
    gap2 = (SCALE * zero - expected) ** 2
    return zero, carry(expected, SCALE, 0)[0], carry(1000 * gap2, variance, 0)[0], odds(gap2, variance)


def fano(marks, sp, lsum, m):
    """A part's count in windows of m rounds at one Node-clock, pooled over the Node-clocks: F, its squared gap from
    the binomial mean over the binomial variance, in thousandths, and the windows; marks[t][k] is 1 where the part,
    sp of lsum, was drawn. Then F's z^2 against its own binomial spread, as a fraction: its variance is 2 q plus
    lsum^2 less 6 sp (lsum - sp), over the windows times q, where q is m sp (lsum - sp)."""
    windows = acc = 0
    for k in range(len(marks[0])):
        for t0 in range(0, len(marks) - m + 1, m):
            count = sum(marks[t][k] for t in range(t0, t0 + m))
            acc += (lsum * count - m * sp) ** 2
            windows += 1
    q = m * sp * (lsum - sp)
    num, den = (acc - windows * q) ** 2, windows * q * (2 * q + lsum * lsum - 6 * sp * (lsum - sp))
    return carry(1000 * acc, windows * q, 0)[0], windows, num, den


assert ODD == 0 and ODD8 == 0
print(f"W = {W}, the grip {GRIP}, H = W div 2 = {H}, T8 = W div 8 = {T8}")
print(f"term 6 at G3's probe strengths, as g5_draw.py lays it: g = {g}, kappa = {kappa}, lam = 4 f2 = {4 * f2},"
      f" n = {N_HELD}")
print(f"the norm pointer: Q over x, its six neighbours and all {len(ALL)} rows, {TERMS} odd squares; W mod 128 ="
      f" {carry(W, 128, 0)[1]}, so u = Q mod W is {CLASS} more than a multiple of 8 at every draw; one halving")
print("leaves u div 2 on a step of 4; one carry by 8, v = u div 8 within [0, T8), can reach every residue there, and")
print("the draw reads v against T8 in the parts' half-open cells")

# ==== (a)
print("(a) the residue check: Q mod T over one, two and three rows, one c per row, each over its whole range")
print("    c = 2 r + 1 - T for r = 0 to T - 1:")
LIMITS = []


def residue_counts(teeth, values, rows):
    """The counts of the sum of c^2 mod teeth over every choice of one c per row from values, as a dict."""
    one = {}
    for c in values:
        _, k = carry(c * c, teeth, 0)
        one[k] = one.get(k, 0) + 1
    counts = {0: 1}
    for _ in range(rows):
        grown = {}
        for i, m in counts.items():
            for j, m2 in one.items():
                _, k = carry(i + j, teeth, 0)
                grown[k] = grown.get(k, 0) + m * m2
        counts = grown
    return counts


def regrouped(counts, step_by):
    """The counts of residue div step_by."""
    out = {}
    for k, m in counts.items():
        q, _ = carry(k, step_by, 0)
        out[q] = out.get(q, 0) + m
    return out


for teeth in (97, 101, 103):
    whole = [2 * r + 1 - teeth for r in range(teeth)]
    cells = []
    for rows, named in ((1, "one row"), (2, "two rows"), (3, "three rows")):
        counts = residue_counts(teeth, whole, rows)
        nonzero = [m for k, m in counts.items() if k]
        cells.append(f"{named}: {len(counts)} of {teeth} residues, each nonzero one reached {min(nonzero)} to"
                     f" {max(nonzero)} times, 0 {counts.get(0, 0)} times")
    print(f"    the prime {teeth}: " + "; ".join(cells))
print("    small even dials: c is odd, every c^2 is 1 more than a multiple of 8, so Q is its count of rows more than a")
print("    multiple of gcd(T, 8); u div gcd(T, 8) read against T div gcd(T, 8), the halved form:")
for teeth in (6, 16, 48, 96, 384):
    whole = [2 * r + 1 - teeth for r in range(teeth)]
    step_by = gcd(teeth, 8)
    span = carry(teeth, step_by, 0)[0]
    cells = []
    for rows in (1, 2, 3):
        counts = residue_counts(teeth, whole, rows)
        classes = {carry(k, step_by, 0)[1] for k in counts}
        halved = regrouped(counts, step_by)
        cells.append(f"{rows}: u {len(counts)} of {teeth}, classes mod {step_by} {sorted(classes)}, u div {step_by}"
                     f" {len(halved)} of {span} ({min(halved.values())} to {max(halved.values())} times)")
    print(f"    T = {teeth}: " + "; ".join(cells))
print("    at W, each row's tooth on one of the probe's lattices of q points, r = H + j (W div q), j = 0 to q - 1:")
print("    q = 6 is the grip's (light on every lay; every row with the plan empty), 16 the plan's kappa = W div 16,")
print("    25 the Pythagorean kappa = 2 W div 25 of (g), 48 the joint lattice of kappa and the grip:")
for q in (6, 16, 25, 48):
    stride, rest = carry(W, q, 0)
    assert rest == 0
    lattice = [2 * carry(H + j * stride, W, 0)[1] + 1 - W for j in range(q)]
    cells = []
    for rows in (1, 2, 3):
        counts = residue_counts(W, lattice, rows)
        keys = sorted(counts)
        spread = 0
        for k in keys:
            spread = gcd(spread, k - keys[0])
        halved = regrouped(counts, 8)
        cells.append(f"{rows}: {len(counts)} residues of u, {len(halved)} of v, on a lattice of W over"
                     f" {carry(W, spread, 0)[0] if spread else 1}")
    print(f"    q = {q}: " + "; ".join(cells))

# ==== (b)
BACK = 300
print(f"(b) the run back inside the act, term 6, {BACK} rounds from the old lay:")
print(f"    forward: s_t = tick(s_(t-1)) for t = 1 to {BACK}; the norm pointer and the draw at every Node-clock from")
print(f"    (s_(t-1), s_t), at 1:1 and at the sizes in s_(t-1)'s now slot; backward: for t = {BACK} down to 1,")
print("    m = mirror(s_t), m_out = tick(m), the same reading from (m, m_out); s_(t-1) recovered as mirror(m_out)")
states, forward = [lays()], []
classes_b = set()
for t in range(1, BACK + 1):
    s_in = states[-1]
    s_out = step.tick(lay6, s_in)
    reads = norm_reads(lay6, s_in, s_out)
    sizes = sizes_at(s_in.a)
    classes_b.update(carry(u, 8, 0)[1] for _, u, _ in reads)
    forward.append(([q for q, _, _ in reads], [cell(v, T8, [1, 1]) for _, _, v in reads],
                    [cell(v, T8, sizes[x]) for x, (_, _, v) in enumerate(reads)],
                    [cell(v, T8, [1, 1]) for v in one_sided(lay6, s_in, s_out)]))
    states.append(s_out)
s = states[-1]
same_q = same_one = same_size = same_control = recovered = 0
for t in range(BACK, 0, -1):
    m = step.mirror(lay6, s)
    m_out = step.tick(lay6, m)
    reads = norm_reads(lay6, m, m_out)
    sizes = sizes_at(m.a)
    q_f, one_f, size_f, control_f = forward[t - 1]
    control = [cell(v, T8, [1, 1]) for v in one_sided(lay6, m, m_out)]
    for x, (q, _, v) in enumerate(reads):
        same_q += int(q == q_f[x])
        same_one += int(cell(v, T8, [1, 1]) == one_f[x])
        same_size += int(cell(v, T8, sizes[x]) == size_f[x])
        same_control += int(control[x] == control_f[x])
    before = step.mirror(lay6, m_out)
    recovered += int(all(np.array_equal(p, r) for p, r in zip(before, states[t - 1], strict=True)))
    s = before
draws = BACK * sites
home = all(np.array_equal(p, r) for p, r in zip(s, lays(), strict=True))
print(f"    u mod 8 over the forward draws: {sorted(classes_b)}")
print(f"    Q itself, unfolded, equal at {same_q} of {draws} draws: the mirror leaves it unchanged, no fold needed")
print(f"    the part equal at {same_one} of {draws} (1:1) and at {same_size} of {draws} (the state's sizes)")
print(f"    control, the norm of the teeth after the tick alone, c(r_out)^2 summed, read the same way on (m, m_out):")
print(f"      the part at 1:1 equal at {same_control} of {draws}, {z2_halves(same_control, draws)}")
print(f"    what cannot fail, named so: s_(t-1) recovered at {recovered} of {BACK} rounds and the lay returned"
      f" ({home}): the engine's own bijection, since the draw writes nothing")


# ==== (c)
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


def side(v, a_in, x, axis, sized=True):
    """The site drawn at x between its + and - neighbours along an axis, the + side first in the parts' own order;
    the sizes m_re^2 + 1 at those two in the now slot a_in, or 1 and 1; by the half-open cells on v."""
    plus, minus = int(nb[2 * axis, x]), int(nb[2 * axis + 1, x])
    sizes = [int(a_in[m_re, plus]) ** 2 + 1, int(a_in[m_re, minus]) ** 2 + 1] if sized else [1, 1]
    return (plus, minus)[cell(v, T8, sizes)]


TURN_ROUNDS = 5
path = [lays()]
for _ in range(TURN_ROUNDS):
    path.append(step.tick(lay6, path[-1]))
path_reads = [norm_reads(lay6, path[t - 1], path[t]) for t in range(1, TURN_ROUNDS + 1)]
rows_c = []
for m in rotations:
    image = image_of(m)
    axis_to = [m[a][0] for a in range(3)]  # the image of +x: the turn's first column
    new_axis = [a for a in range(3) if axis_to[a] != 0][0]
    act = q_same = given = equal = 0
    for t in range(1, TURN_ROUNDS + 1):
        s_in, s_out = path[t - 1], path[t]
        reads = path_reads[t - 1]
        t_in = turned(s_in, image)
        t_out = step.tick(lay6, t_in)
        act += int(all(np.array_equal(p, r) for p, r in zip(t_out, turned(s_out, image), strict=True)))
        reads_t = norm_reads(lay6, t_in, t_out)
        for x in range(sites):
            j = image[x]
            q_same += int(reads_t[j][0] == reads[x][0])
            given += int(side(reads_t[j][2], t_in.a, j, new_axis) == image[side(reads[x][2], s_in.a, x, 0)])
            equal += int(side(reads_t[j][2], t_in.a, j, new_axis, False) == image[side(reads[x][2], s_in.a, x, 0,
                                                                                        False)])
    rows_c.append((axis_to[new_axis], act, q_same, given, equal))
print(f"(c) the 24: {len(rotations)} turns; rounds 1 to {TURN_ROUNDS} from the old lay, each input state turned and"
      f" ticked;")
print("    at x the split between its +x and -x neighbours, sizes m_re^2 + 1 at those two in s_in's now slot, + side")
print("    first; covariant where the turned board's draw at x's image is the image of the original's;")
print(f"    {TURN_ROUNDS * sites} draws a turn, each count listed once:")
for sign in (1, -1):
    sel = [r for r in rows_c if r[0] == sign]
    print(f"    {len(sel)} turns taking +x to a {'+' if sign == 1 else '-'} direction:")
    print(f"      the act turned with the board in {sorted({r[1] for r in sel})} of {TURN_ROUNDS} rounds; Q equal at"
          f" the image at {sorted({r[2] for r in sel})}")
    print(f"      the draw, the parts in their own order: covariant at {sorted({r[3] for r in sel})}; at sizes 1 and 1:"
          f" {sorted({r[4] for r in sel})}")


def geared(s, negate=(), swap=()):
    """A train's own signed permutation on the state: a row negated, its fine tooth flipped in its teeth W (and its
    drive's in its teeth 1); two rows of one train swapped."""
    a, b, r, rd = (part.copy() for part in s)
    for row in negate:
        a[row], b[row], r[row], rd[row] = -a[row], -b[row], flip(r[row], W), flip(rd[row], 1)
    for i, j in swap:
        for part in (a, b, r, rd):
            part[[i, j]] = part[[j, i]]
    return State(a, b, r, rd)


GEARS = (("light's re row negated", (l_re,), ()), ("matter's re and im rows swapped", (), ((m_re, m_im),)),
         ("matter's two rows negated and light's two rows swapped", (m_re, m_im), ((l_re, l_im),)))
print("    the trains' own signed permutations (Big Pic's claim 1), the same rounds, every Node-clock in place:")
for label, negate, swap in GEARS:
    act = q_same = e_same = 0
    for t in range(1, TURN_ROUNDS + 1):
        s_in, s_out = path[t - 1], path[t]
        g_in = geared(s_in, negate, swap)
        g_out = step.tick(lay6, g_in)
        act += int(all(np.array_equal(p, r) for p, r in zip(g_out, geared(s_out, negate, swap), strict=True)))
        reads_g = norm_reads(lay6, g_in, g_out)
        e_f, e_g = pointers(lay6, s_in, s_out), pointers(lay6, g_in, g_out)
        q_same += sum(int(reads_g[x][0] == path_reads[t - 1][x][0]) for x in range(sites))
        e_same += sum(int(e_g[x] == e_f[x]) for x in range(sites))
    print(f"      {label}: the act commutes in {act} of {TURN_ROUNDS} rounds; Q equal at {q_same} of"
          f" {TURN_ROUNDS * sites}; the third text's e equal at {e_same}")


# ==== (d)
def lay_run(s, row_sets, read_at=None, keep=False):
    """Rounds FROM + 1 to ROUNDS of term 6 from s: per row set, a list per round of v at the Node-clocks read, and the
    classes of u mod 8; with keep, each round's sizes in s_in's now slot and its swept areas before and after."""
    at = list(range(sites)) if read_at is None else read_at
    got = [[] for _ in row_sets]
    classes = [set() for _ in row_sets]
    kept = {"sizes": [], "areas": []}

    def read(t, s_in, s_out):
        if t > FROM:
            for k, rows in enumerate(row_sets):
                reads = norm_reads(lay6, s_in, s_out, rows)
                got[k].append([reads[i][2] for i in at])
                classes[k].update(carry(reads[i][1], 8, 0)[1] for i in at)
            if keep:
                kept["sizes"].append(sizes_at(s_in.a))
                kept["areas"].append((area(s_in), area(s_out)))

    run(lay6, s, ROUNDS, read)
    return got, classes, kept


SPLITS4 = ((1, 1), (1, 2), (3, 7), (1, 3))  # the five splits as they draw: the last two of SPLITS draw as 1 : 3


def largest_gap(flat):
    """The largest |freq(part 0) - share| over the splits, in ppm, by the half-open cells on v."""
    n = len(flat)
    return max(ppm(abs((s1 + s2) * zero_count(flat, T8, s1, s2) - n * s1), n * (s1 + s2)) for s1, s2 in SPLITS4)


def battery(label, rounds_v, sizes_rounds, classes, full):
    """The third text's battery on one lay's v, printed."""
    flat = [v for row in rounds_v for v in row]
    n = len(flat)
    chi, top = chi_tenths(flat, T8), discrepancy(flat, T8)
    run_same, run_pairs, mesh_same, mesh_pairs = halves(rounds_v, T8)
    print(f"    {label}: {len(set(flat))} distinct v of {n}; u mod 8 {sorted(classes)}; the tenths {shown(chi)} on 9")
    print(f"      the same half two rounds running {run_same} of {run_pairs}, {z2_halves(run_same, run_pairs)}; one"
          f" Mesh apart {mesh_same} of {mesh_pairs}, {z2_halves(mesh_same, mesh_pairs)}")
    print(f"      D_N {ppm(top, n * T8)} ppm; N times D_N squared {nd2(top, n, T8)} thousandths (the Kolmogorov law's"
          f" mean {KS_MEAN}, its 5 per cent point {KS_5:,})")
    cells, differ, agree = [], 0, True
    for s1, s2, name in SPLITS:
        zero = zero_count(flat, T8, s1, s2)
        if full:
            agree = agree and zero == sum(int(cell(v, T8, [s1, s2]) == 0) for v in flat)
            differ += sum(int(cell(v, T8, [s1, s2]) != cell(8 * v + CLASS, W, [s1, s2])) for v in flat)
            print(f"      Born at {name}: {born_fixed(zero, n, s1, s2)}")
        else:
            cells.append(f"{name} {shown(z2_fixed(zero, n, s1, s2))}")
    if not full:
        print("      Born, z^2 at the five splits: " + "; ".join(cells))
    sizes_flat = [sz for row in sizes_rounds for sz in row]
    zero, expected, z2, cls = state_born(flat, sizes_flat, T8, cell)
    print(f"      at the state's sizes, S1 = m_re^2 + 1 and S2 = m_im^2 + 1 in s_in's now slot: part 0 in {zero} of {n}"
          f" (expected {expected}), z^2 {shown(z2)}, {cls}")
    print(f"      the largest |freq - share| over the five splits {largest_gap(flat)} ppm, within 2 D_N by the theorem")
    if full:
        print(f"      the cell rule drawn part by part equal to the first cell's count at the five splits: {agree};")
        print(f"      the raw form, u against W, and the halved form, v against T8, part at {differ} of {5 * n} draws")
    return chi, z2_fixed(zero_count(flat, T8, 1, 1), n, 1, 1)


print(f"(d) the third text's battery, term 6, rounds {FROM + 1} to {ROUNDS} at all {sites} Node-clocks, the norm"
      f" pointer v against T8,")
print("    the parts' half-open cells in their own order; the old lay in full, then the six lays (the old lay first):")
LIGHT = [l_re, l_im]
seed_runs = {}
got, classes, kept_old = lay_run(lays(), (ALL, LIGHT), keep=True)
seed_runs[SEED] = (got[0], kept_old["sizes"], classes[0])
light_alone = got[1]
battery("the old lay", got[0], kept_old["sizes"], classes[0], True)
for seed in (1, 2, 3, 4, 5):
    got, classes, kept = lay_run(lays(seed), (ALL,), keep=True)
    seed_runs[seed] = (got[0], kept["sizes"], classes[0])
chis, z2s = [], []
for seed in (SEED, 1, 2, 3, 4, 5):
    rounds_v, sizes_rounds, classes = seed_runs[seed]
    chi, z2 = battery(f"seed {seed}", rounds_v, sizes_rounds, classes, False)
    chis.append(chi)
    z2s.append(z2)
mean_z2 = carry(1000 * (sum(chis) - 6 * 9000) ** 2, 108 * MILLION, 0)[0]  # (mean - 9)^2 over 18 div 6
print(f"    mean tenths chi-square {shown(carry(sum(chis), 6, 0)[0])} over the six; the null: mean 9, variance 18 for"
      f" one lay, 3 for the mean of six; the mean's z^2 {shown(mean_z2)}")
print(f"    the six z^2 at 1:1: {', '.join(shown(z) for z in z2s)}; the six tenths:"
      f" {', '.join(shown(c) for c in chis)}; past the 5 per cent point {shown(CHI9[0])}:"
      f" {sum(int(c > CHI9[0]) for c in chis)} of 6")

# ==== (e)
print(f"(e) the two hardest lays of the old probe, term 6, the held count laid at n, rounds {FROM + 1} to {ROUNDS};")
print("    the lags pool one Node-clock's pairs over the Node-clocks read; then the held count's row alone in Q, where")
print("    the third text's pointer froze (its (j): 86,400 of 86,400 and 10,800 of 10,800 draws to part 0):")
centre = [(x * 6 + y) * 6 + z for x in (2, 3, 4) for y in (2, 3, 4) for z in (2, 3, 4)]
HARD = (("a hot board, matter laid to 10 counts, all 216 Node-clocks", swing_lay(10, 1, False), None),
        ("a cold board, one packet near 100 counts, its 27 Node-clocks", swing_lay(100, 0, True), centre))
fano_sets = [("the old lay, all 216 Node-clocks", seed_runs[SEED][0])]
for name, lay_h, read_at in HARD:
    got, classes, _ = lay_run(lay_h, (ALL, [held]), read_at)
    picked = got[0]
    fano_sets.append((name, picked))
    flat = [v for row in picked for v in row]
    n, width = len(flat), len(picked[0])
    lags = []
    for lag in (1, 2):
        pairs = [(tenth(picked[t][k], T8), tenth(picked[t + lag][k], T8)) for t in range(len(picked) - lag)
                 for k in range(width)]
        chi, free = chi_joint(pairs)
        lags.append(f"at t and t + {lag}: {shown(chi)} on {free}")
    half = sum(int(cell(v, T8, [1, 1]) == 0) for v in flat)
    quarter = sum(int(cell(v, T8, [1, 3]) == 0) for v in flat)
    print(f"    {name}: {len(set(flat))} distinct v of {n}; u mod 8 {sorted(classes[0])}")
    print(f"      the tenths {shown(chi_tenths(flat, T8))} on 9; joint tenths {'; '.join(lags)}")
    print(f"      at 1:1 {born_fixed(half, n, 1, 1)}; at 1:3 {born_fixed(quarter, n, 1, 3)}")
    top = discrepancy(flat, T8)
    print(f"      D_N {ppm(top, n * T8)} ppm, N times D_N squared {nd2(top, n, T8)} thousandths; the largest"
          f" |freq - share| over the five splits {largest_gap(flat)} ppm")
    alone = [v for row in got[1] for v in row]
    half = sum(int(cell(v, T8, [1, 1]) == 0) for v in alone)
    quarter = sum(int(cell(v, T8, [1, 3]) == 0) for v in alone)
    top = discrepancy(alone, T8)
    print(f"      the held count's row alone: {len(set(alone))} distinct v; u mod 8 {sorted(classes[1])}; the tenths"
          f" {shown(chi_tenths(alone, T8))} on 9; D_N {ppm(top, n * T8)} ppm, N times D_N squared {nd2(top, n, T8)}")
    print(f"        at 1:1 {born_fixed(half, n, 1, 1)}; at 1:3 {born_fixed(quarter, n, 1, 3)}")
print("    the Fano factor of part 0's count in windows of M rounds at one Node-clock, pooled over the Node-clocks")
print("    read: its squared gap from the binomial mean over the binomial variance (1 for independent draws), and its")
print("    z^2 on 1 against its own binomial spread; the norm pointer, the parts' half-open cells:")
WINDOWS = (10, 40, 100, 200, 400)
for name, picked in fano_sets:
    marks = [[[int(cell(v, T8, sizes) == 0) for v in row] for row in picked] for sizes in ([1, 1], [1, 3])]
    print(f"    {name}:")
    for m in WINDOWS:
        f_half, windows, num_h, den_h = fano(marks[0], 1, 2, m)
        f_quarter, _, num_q, den_q = fano(marks[1], 1, 4, m)
        z_h, z_q = shown(carry(1000 * num_h, den_h, 0)[0]), shown(carry(1000 * num_q, den_q, 0)[0])
        print(f"      M = {m}, {windows} windows: {shown(f_half)} at 1:1 (z^2 {z_h}, {odds(num_h, den_h)}),"
              f" {shown(f_quarter)} at 1:3 (z^2 {z_q}, {odds(num_q, den_q)})")

# ==== (f)
VACUUM = 400
print("(f) the vacuum: term 6; light laid moving at every Node-clock (seed 7, as the hostile reader's g5_vacuum.py);")
print(f"    matter laid at rest at 0 and the held count at rest at n; {VACUUM} rounds, every round read; Q over every")
print("    row, light's included, as Big Pic reads it (the third text's pointer, light outside, froze at e = 42 here):")
seen = [set() for _ in range(sites)]
vac_rounds, vac_sizes, vac_classes, light_terms = [], [], set(), set()


def read_f(t, s_in, s_out):
    reads = norm_reads(lay6, s_in, s_out)
    vac_rounds.append([v for _, _, v in reads])
    vac_sizes.append(sizes_at(s_in.a))
    for x, (_, u, v) in enumerate(reads):
        seen[x].add(v)
        vac_classes.add(carry(u, 8, 0)[1])
    for row in LIGHT:
        for r in s_out.r[row].tolist() + s_in.r[row].tolist():
            c = 2 * r + 1 - W
            light_terms.add(carry(carry(c * c, W, 0)[1] - 1, GRIP, 0))


last = run(lay6, vacuum_lay(), VACUUM, read_f)
at_rest = all(v == 0 for v in last.a[m_re].tolist() + last.a[m_im].tolist()) and all(
    v == N_HELD for v in last.a[held].tolist())
moved_rows = [row for row in ALL if any(x != H for x in last.r[row].tolist())]
values = sorted({v for row in vac_rounds for v in row})
print(f"    matter and the held count still at rest after {VACUUM} rounds: {at_rest}; the rows whose fine teeth moved:"
      f" {moved_rows} (light's are rows 0 and 1)")
print(f"    each light term's c^2 - 1, by one carry by the grip: quotients mod 6 and rests"
      f" {sorted({(carry(qq, 6, 0)[1], rr) for qq, rr in light_terms})}: light's teeth on the grip's lattice")
print(f"    v: at most {max(len(x) for x in seen)} distinct values at a Node-clock, {len(values)} over the board, at"
      f" {', '.join(str(per_mille(x, T8)) for x in values)} thousandths of T8")
battery("the vacuum's battery, as (d)'s", vac_rounds, vac_sizes, vac_classes, True)
flat_light = [v for row in light_alone for v in row]
print(f"    light's two rows alone in Q on the old lay of (d): {len(set(flat_light))} distinct v of {len(flat_light)},"
      f" at {', '.join(str(per_mille(x, T8)) for x in sorted(set(flat_light)))} thousandths of T8")

# ==== (g)
A = N_HELD  # the hand's swing, n
PA, PB = 7, 1  # the Pythagorean pair: W = a^2 + b^2 in units of W div 50, kappa_p = 4 b^2 in the same units
HYP = PA * PA + PB * PB
NEAR, NEAR_REST = carry(A * (PA * PA - PB * PB), HYP, 0)  # A (a^2 - b^2) over (a^2 + b^2), whole
SIDE, SIDE_REST = carry(A * 2 * PA * PB, HYP, 0)  # A 2 a b over (a^2 + b^2), whole
KAPPA_P, KP_REST = carry(4 * PB * PB * W, HYP, 0)  # 2 W div 25, whole
assert NEAR_REST == 0 and SIDE_REST == 0 and KP_REST == 0
HAND = ((A, NEAR), (0, -SIDE))  # re at its now and before slots, im a quarter turn behind: one uniform rotation
KAPPA = carry(W, 16, 0)[0]  # the plan's kappa
OFFSET = carry(W, 16 * N_HELD, 0)[0] + 1  # the readers' offset: kappa + OFFSET leaves W div 16's lattice by a step
OFFSET_P = carry(W, 25 * N_HELD, 0)[0] + 1  # the same for the Pythagorean lattice of 25 points
SEVEN = carry(2 * W + 7, 14, 0)[0]  # W div 7, rounded
ELEVEN = carry(6 * W + 11, 22, 0)[0]  # 3 W div 11, rounded
ROUNDS_G = 10800
SIZE = 128
MERGE = (SIZE - 1, 0, 1)  # the ring's merge: Node-clock 0 and its two neighbours


def hand_run(lay, spring, rounds):
    """One Node-clock's held hand (re, im), each part a gear at teeth W pushed by -spring times its now count, its
    fine teeth born at H: per round the norm's sum c(re_in)^2 + c(re_out)^2 + c(im_in)^2 + c(im_out)^2, the third
    text's sum of the same four c, and re's fine-tooth move; and the end state."""
    (ra, rb), (ia, ib) = lay
    re, im = (ra, rb, H), (ia, ib, H)
    norms, sums, moves = [], [], []
    for _ in range(rounds):
        re_out = step.gear(*re, W, -spring * re[0])
        im_out = step.gear(*im, W, -spring * im[0])
        c1, c2 = 2 * re[2] + 1 - W, 2 * re_out[2] + 1 - W
        c3, c4 = 2 * im[2] + 1 - W, 2 * im_out[2] + 1 - W
        norms.append(c1 * c1 + c2 * c2 + c3 * c3 + c4 * c4)
        sums.append(c1 + c2 + c3 + c4)
        moves.append(abs(re_out[2] - re[2]))
        re, im = re_out, im_out
    return norms, sums, moves, ((re[0], re[1]), (im[0], im[1]))


def ring_run(lay, spring, rounds):
    """G3's ring of 128, every Node-clock laid alike: each part pulled by its two neighbours at the grip and pushed
    by -spring part (g3_held_hand.py's pointer_round, the hand); per round the merge's norm sum and third-text sum."""
    (ra, rb), (ia, ib) = lay
    parts = [[(ra, rb, H)] * SIZE, [(ia, ib, H)] * SIZE]
    out = []
    for _ in range(rounds):
        nows = [[gear[0] for gear in row] for row in parts]
        nxt = [[], []]
        for i in range(SIZE):
            right = carry(i + 1, SIZE, 0)[1]
            for p in range(2):
                lap = nows[p][i - 1] + nows[p][right] - 2 * nows[p][i]
                nxt[p].append(step.gear(*parts[p][i], W, GRIP * lap - spring * nows[p][i]))
        cs = [2 * gear[y][2] + 1 - W for row in (parts, nxt) for gear in row for y in MERGE]
        out.append((sum(c * c for c in cs), sum(cs)))
        parts = nxt
    return out


def norm_v(total, times):
    return carry(carry(times * total, W, 0)[1], 8, 0)[0]


def third_e(total, times):
    _, u = carry(times * total, W, 0)
    return min(u, W - u)


def scan_stats(values, scale, rule, checked):
    """The tenths, N times D_N squared and the largest z^2 over 1:1, 1:3 and 3:7, all in thousandths; part 0 counted
    by zero_count, checked against the rule itself where asked."""
    n = len(values)
    zs = []
    for s1, s2 in ((1, 1), (1, 3), (3, 7)):
        zero = zero_count(values, scale, s1, s2)
        if checked:
            assert zero == sum(int(rule(x, scale, [s1, s2]) == 0) for x in values)
        zs.append(z2_fixed(zero, n, s1, s2))
    return chi_tenths(values, scale), nd2(discrepancy(values, scale), n, scale), max(zs)


def report(values, scale, rule):
    n = len(values)
    top = discrepancy(values, scale)
    chi, free = chi_joint([(tenth(values[t], scale), tenth(values[t + 1], scale)) for t in range(n - 1)])
    zs = [shown(z2_fixed(sum(int(rule(x, scale, [s1, s2]) == 0) for x in values), n, s1, s2))
          for s1, s2 in ((1, 1), (1, 3), (3, 7))]
    return (f"{len(set(values))} distinct; the tenths {shown(chi_tenths(values, scale))} on 9; D_N"
            f" {ppm(top, n * scale)} ppm, N times D_N squared {nd2(top, n, scale)}; lag-1 joint tenths {shown(chi)} on"
            f" {free}; z^2 at 1:1, 1:3, 3:7: {', '.join(zs)}")


def third_rule(e, h, sizes):
    return drawn(e, h, sizes)


print(f"(g) the readers' single rotations: G3's held hand on G3's ring of {SIZE}, the merge at Node-clock 0 and its")
print(f"    two neighbours, re and im read, every fine tooth born at H, {ROUNDS_G} rounds. Laid alike at every")
print("    Node-clock, the Meshes pull nothing, so the merge reads 3 times one Node-clock's sum, and the board's star")
print("    of seven 7 times. Every lay is whole: G3's quarter lay, the readers' own-beat lays and their 64 start")
print("    phases came from series, so one Pythagorean hand stands for them all (Big Pic's construction), and the act")
print("    turns it:")
print(f"    a = {PA}, b = {PB}: re laid at {A} and {NEAR} (now, before), im at 0 and {-SIDE}; the beat's two whole")
near2, side2 = PA * PA - PB * PB, 2 * PA * PB
print(f"    ratios {near2} over {HYP} and {side2} over {HYP}; ({near2})^2 + ({side2})^2 ="
      f" {HYP}^2: {(PA * PA - PB * PB) ** 2 + (2 * PA * PB) ** 2 == HYP * HYP}; re^2 + im^2 the same at both slots:"
      f" {A * A == NEAR * NEAR + SIDE * SIDE}")
print(f"    the hand's own spring 4 b^2 W over (a^2 + b^2) = 2 W div 25 = {KAPPA_P}; at another spring the same lay")
print("    turns on an ellipse; the norm pointer v at the merge drawn by the half-open cells, the third text's e")
print("    beside it by its own rule, the control:")
check = ring_run(HAND, KAPPA + OFFSET, 1000)
norms0, sums0, _, _ = hand_run(HAND, KAPPA + OFFSET, 1000)
agree = sum(int(qq == 3 * a and pp == 3 * b) for (qq, pp), a, b in zip(check, norms0, sums0, strict=True))
print(f"    the whole ring's merge against 3 times one Node-clock, at kappa + W div (16 n) + 1, rounds 1 to 1000:"
      f" equal at {agree} of 1000")
CASES = (("the plan's kappa = W div 16, on its lattice of 16 points", KAPPA),
         ("kappa + 1, one count off that lattice", KAPPA + 1),
         ("kappa + W div (16 n) + 1, the readers' off-lattice spring, at the lay's own phase", KAPPA + OFFSET),
         ("the hand's own beat, 2 W div 25, on its lattice of 25 points", KAPPA_P),
         ("2 W div 25 + W div (25 n) + 1, off that lattice by a step at the swing", KAPPA_P + OFFSET_P),
         ("W div 7 rounded, the mathematician's", SEVEN),
         ("3 W div 11 rounded, the mathematician's", ELEVEN))
print(f"    W mod 7 = {carry(W, 7, 0)[1]}, W mod 11 = {carry(W, 11, 0)[1]}; gcd(W, W div 7 rounded) = {gcd(W, SEVEN)},"
      f" gcd(W, 3 W div 11 rounded) = {gcd(W, ELEVEN)}")
for label, spring in CASES:
    norms, sums, moves, _ = hand_run(HAND, spring, ROUNDS_G)
    ordered = sorted(moves)
    print(f"    {label}: the spring {spring}; re's fine-tooth move over W, median"
          f" {per_mille(ordered[carry(len(ordered), 2, 0)[0]], W)} thousandths of a turn")
    for times, where in ((3, "the ring's merge"), (7, "the board's star")):
        print(f"      {where}, Q: " + report([norm_v(x, times) for x in norms], T8, cell))
        print(f"      {where}, P: " + report([third_e(x, times) for x in sums], H, third_rule))

STARTS = 64


def octant(re, im):
    """0 to 7 counterclockwise from re's + axis: the quadrant by the signs (G3's quadrant()), then the half of it by
    the larger magnitude; the hand never stands at 0."""
    if re > 0 and im >= 0:
        quad = 0
    elif re <= 0 and im > 0:
        quad = 1
    elif re < 0 and im <= 0:
        quad = 2
    else:
        quad = 3
    first = abs(re) > abs(im) if quad in (0, 2) else abs(im) > abs(re)
    return 2 * quad + (0 if first else 1)


print(f"    the off-lattice springs at {STARTS} start phases: the hand laid as above, then turned by the act itself, d")
print("    rounds between starts at the spring, every fine tooth born again at H for each start's read; d, written")
print("    here, takes the starts once round (their octants, counterclockwise from re's + axis, listed); per start,")
print("    the tenths on 9, N times D_N squared and the largest z^2 of 1:1, 1:3 and 3:7:")
for label, spring, turn_step in (("kappa + W div (16 n) + 1, the readers' spring", KAPPA + OFFSET, 602),
                                 ("2 W div 25 + W div (25 n) + 1, the hand on its own beat", KAPPA_P + OFFSET_P, 421)):
    re, im = (HAND[0][0], HAND[0][1], H), (HAND[1][0], HAND[1][1], H)
    rows_s, octants = [], [0] * 8
    for j in range(STARTS):
        octants[octant(re[0], im[0])] += 1
        norms, sums, _, _ = hand_run(((re[0], re[1]), (im[0], im[1])), spring, ROUNDS_G)
        line = []
        for times in (3, 7):
            line.append(scan_stats([norm_v(x, times) for x in norms], T8, cell, j == 0))
            line.append(scan_stats([third_e(x, times) for x in sums], H, third_rule, j == 0))
        rows_s.append(line)
        for _ in range(turn_step):
            re, im = step.gear(*re, W, -spring * re[0]), step.gear(*im, W, -spring * im[0])
    print(f"    {label}, d = {turn_step}: the {STARTS} starts by octant {octants}")
    chance = [STARTS * p for p in (50, 10, 1)]  # thousandths of a lay: the 5, 1 and one-tenth per cent of 64
    print(f"      chance for independent uniform draws: the tenths past their three points in {shown(chance[0])},"
          f" {shown(chance[1])} and {shown(chance[2])} lays; N times D_N squared past {shown(KS_5)} in"
          f" {shown(chance[0])}; the largest of three z^2 past {shown(Z1)} in about"
          f" {shown(carry(STARTS * (100**3 - 99**3) * 1000, 100**3, 0)[0])}")
    for k, name in enumerate(("the ring's merge, Q", "the ring's merge, P", "the board's star, Q",
                              "the board's star, P")):
        col = [row[k] for row in rows_s]
        past = [sum(int(c[0] > point) for c in col) for point in CHI9]
        worst = max(range(STARTS), key=lambda i: col[i][0])
        print(f"      {name}: the tenths past {shown(CHI9[0])}, {shown(CHI9[1])} and {shown(CHI9[2])} in"
              f" {past[0]}, {past[1]} and {past[2]} of {STARTS}; N times D_N squared past {shown(KS_5)} in"
              f" {sum(int(c[1] > KS_5) for c in col)}; a split's z^2 past {shown(Z1)} in"
              f" {sum(int(c[2] > Z1) for c in col)}; the largest tenths {shown(col[worst][0])} at start {worst}")
        print(f"        the {STARTS} tenths, in start order: {', '.join(shown(c[0]) for c in col)}")

# ==== (h)
KEY_AREA = 10**10 * W  # the first text's key
print("(h) the third text's (p): the norm pointer only at the rounds where a Node-clock's swept area")
print("    m_re p_im - m_im p_re crosses a multiple of the key 10^10 W, p = W (a - b) + r, from s_in to s_out, on the")
print("    old lay's run of (d):")
old_v, old_sizes = seed_runs[SEED][0], seed_runs[SEED][1]
picked, picked_sizes = [], []
for t, (before, after) in enumerate(kept_old["areas"]):
    for x in range(sites):
        if carry(before[x], KEY_AREA, 0)[0] != carry(after[x], KEY_AREA, 0)[0]:
            picked.append(old_v[t][x])
            picked_sizes.append(old_sizes[t][x])
n = len(picked)
half = sum(int(cell(v, T8, [1, 1]) == 0) for v in picked)
zero, expected, z2, cls = state_born(picked, picked_sizes, T8, cell)
top = discrepancy(picked, T8)
print(f"    {n} crossings; the tenths {shown(chi_tenths(picked, T8))} on 9; D_N {ppm(top, n * T8)} ppm, N times D_N"
      f" squared {nd2(top, n, T8)} thousandths; the largest |freq - share| over the five splits {largest_gap(picked)}"
      f" ppm")
print(f"    at 1:1 {born_fixed(half, n, 1, 1)}; at the state's sizes part 0 in {zero} of {n} (expected {expected}), z^2"
      f" {shown(z2)}, {cls}")
print("    the third text's (q), the backward pass's step: v at (x, t) against v at x's neighbour at t + 1, along +x")
print("    and along all six Spokes; joint tenths on 81, and the same half with its odds:")
for seed in (SEED, 4):
    rounds_v = seed_runs[seed][0]
    tens = [[tenth(v, T8) for v in row] for row in rounds_v]
    sides = [[int(2 * v >= T8) for v in row] for row in rounds_v]
    for spokes_used, along in (((0,), "+x"), (tuple(range(6)), "all six Spokes")):
        index = [(t, x, int(nb[k, x])) for t in range(len(rounds_v) - 1) for x in range(sites) for k in spokes_used]
        chi, free = chi_joint([(tens[t][x], tens[t + 1][y]) for t, x, y in index])
        same = sum(int(sides[t][x] == sides[t + 1][y]) for t, x, y in index)
        print(f"    seed {seed}, along {along}: joint tenths {shown(chi)} on {free}; same half {same} of {len(index)},"
              f" {z2_halves(same, len(index))}")

# ---- (i) to (k): the fifth text's sections, the fourth text's readers' cases (the hostile mathematician's g5v4_algebra
# and g5v4_held_vacuum, the hostile physicist's D3), ported here and rerun on the probe's own board
print("(i) one row's square reads its tooth up to a quarter turn and its sign (the mathematician's NB1):")


def c_at(r, t):
    return 2 * r + 1 - t


def residue(x, t):
    return carry(x, t, 0)[1]


for t in (16, 32, 48, 64, 128, 1024):
    quarter, eighth, half = carry(t, 4, 0)[0], carry(t, 8, 0)[0], carry(t, 2, 0)[0]
    q_bad = sum(int(residue(c_at(residue(r + quarter, t), t) ** 2, t) != residue(c_at(r, t) ** 2, t)) for r in range(t))
    e_bad = sum(int(residue(c_at(residue(r + eighth, t), t) ** 2, t) != residue(c_at(r, t) ** 2 + half, t))
                for r in range(t))
    distinct = len({residue(c_at(r, t) ** 2, t) for r in range(t)})
    print(f"    T = {t}: c(r + T/4)^2 = c(r)^2 mod T failing at {q_bad} of {t} teeth; c(r + T/8)^2 = c(r)^2 + T/2 failing"
          f" at {e_bad}; one row's distinct squares {distinct}, T/8 = {eighth}")
grid = [residue(j * carry(W, 1009, 0)[0] + 7 * j, W) for j in range(1009)]
for m in (6, 16, 48):
    step_m = carry(W, m, 0)[0]
    counts = []
    for r in grid[:50]:
        moved = {residue(c_at(residue(r + j * step_m, W), W) ** 2 - c_at(r, W) ** 2, W) for j in range(1, m + 1)}
        counts.append(len(moved))
    print(f"    at W, a tooth moved by multiples of W/{m} (W mod {m} = {residue(W, m)}): its square takes at most"
          f" {max(counts)} residues of W over 50 teeth (m = {m}, m/4 = {carry(m, 4, 0)[0]})")


def held_lay(held_off, light_moving):
    pick, (a, b) = generator(11), blank()
    for i in range(sites):
        if light_moving:
            for row in (l_re, l_im):
                a[row, i] = pick(1000)
                b[row, i] = a[row, i] - pick(5)
        a[held, i] = N_HELD + held_off(pick)
        b[held, i] = a[held, i]
    return laid(a, b)


def held_report(label, s):
    values, per_site = [], [set() for _ in range(sites)]
    moves = off_grip = 0
    for t in range(1, ROUNDS + 1):
        s_out = step.tick(lay6, s)
        if t > FROM:
            for x, (_, _, v) in enumerate(norm_reads(lay6, s, s_out)):
                values.append(v)
                per_site[x].add(v)
        for x in range(sites):
            d = int(s_out.r[held, x]) - int(s.r[held, x])
            if d:
                moves += 1
                off_grip += int(carry(d, GRIP, 0)[1] != 0)
        s = s_out
    n = len(values)
    cells = []
    for s1, s2 in ((1, 1), (1, 3), (3, 7)):
        zero = sum(int(cell(v, T8, [s1, s2]) == 0) for v in values)
        cells.append(f"{s1}:{s2} part 0 {zero} of {n} (expected {carry(n * s1, s1 + s2, 0)[0]}) z^2"
                     f" {shown(z2_fixed(zero, n, s1, s2))}")
    print(f"    {label}: the held count's tooth moved in {moves} of {ROUNDS * sites} Node-clock rounds, {off_grip} of them"
          f" off the grip's lattice; v takes {len(set(values))} values, at most {max(len(p) for p in per_site)} at one"
          f" Node-clock; the tenths {shown(chi_tenths(values, T8))} on 9; " + "; ".join(cells))


print("(j) the held count displaced, matter at rest, every row read (the mathematician's case, on this board):")
held_report("laid 1,000 off n alike, light at rest", held_lay(lambda pick: 1000, False))
held_report("laid off n by the generator up to 1,000, light at rest", held_lay(lambda pick: pick(1000), False))
held_report("the same, light moving as (f)'s vacuum", held_lay(lambda pick: pick(1000), True))

print("(k) the cells where 8 does not divide T_f (the mathematician's NB2, the physicist's D3): T8 as the fourth text read"
      " it, T_f div 8, and as the fifth reads it, the ceiling (T_f + 7) div 8:")
for t_f in (W + 1, W + 4, W + 7, W - 3):
    floor8, ceil8 = carry(t_f, 8, 0)[0], carry(t_f + 7, 8, 0)[0]
    top_u = range(t_f - 16, t_f)
    past_floor = sum(int(carry(u, 8, 0)[0] >= floor8) for u in top_u)
    past_ceil = sum(int(carry(u, 8, 0)[0] >= ceil8) for u in top_u)
    drawn_zero = sum(int(cell(carry(u, 8, 0)[0], ceil8, [0, 1]) == 0) for u in top_u)
    print(f"    T_f = W {'+' if t_f > W else '-'} {abs(t_f - W)}: of the top 16 residues, v at or past T_f div 8 at"
          f" {past_floor}, past the ceiling at {past_ceil}; with the ceiling, a part of size 0 before one of size 1 drawn"
          f" at {drawn_zero} of 16")
