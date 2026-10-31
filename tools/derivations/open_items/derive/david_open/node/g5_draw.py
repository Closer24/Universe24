"""G5, the split click's draw, read inside the act: one round's centred fine teeth, in and out, as the pointer.

Whole numbers alone, every division Rule3's carry. The board, the lays, term 6 and the trains are the old probe's:
6 by 6 by 6 Node-clocks, light, matter and the held count, all three trains A1, the teeth W six grips. At a drawing
Node-clock x, for the round from s_in to s_out = tick(s_in): the centred tooth c(r) = 2 r + 1 - W; P, the sum of
c(r_in) + c(r_out) over x, its six neighbours and every A1 row; u = P mod W; the pointer e = min(u, W - u), between
0 and H, where H is W div 2. The parts are read in their own order, with no rank: C_i is the sizes of parts 0 to i
summed, L their total, and part i is drawn where C_(i-1) times H is at most e times L and e times L is below C_i
times H; e = H goes to the last part of nonzero size in that order.

(a) each train's pitch: the gcd of W and every move of its fine teeth, under each plan;
(b) the pointer e under term 6: distinct values, chi-square of its tenths, same half with its odds, the star
    discrepancy and N D_N^2; again with light outside the pointer, as the theory reads it;
(c) Born at five fixed splits by four rules: e, the raw sum mod L, decision 29's digits, its digits with the dial;
    then the sizes read from the state, by e in the parts' own order; again with light outside the pointer;
(d) six lays: e's tenths, part 0 at 1:1 with its odds, each lay's D_N and largest departure, light counted and
    outside; seed 4's tenths split into its halves and the rest;
(e) the run back inside the act: 300 rounds out, then each round's tick run on the mirrored state, the same draws
    read and the books undone; the old rule read the same way, as a control, with its odds;
(f) the 24: the split between the +x and -x neighbours under every turn of the cube, by the rule and by the
    refused rank;
(g) the vacuum: light moving, matter and the held count at rest under term 6, the pointer where light alone passed;
(h) the two hardest lays of the old probe: e's tenths, its joint tenths one and two rounds apart, part 0 at 1:1, D_N;
(i) decision 29's dial on the raw sum over a full turn with the plan empty, and the raw sum with c struck there;
(j) the rows the pointer reads: (b)'s statistics with the held count alone, and with matter and the held count;
(k) the run back with a click that writes: five writes, one act for both ways of time on the mirrored state;
(l) decision 29's dial on its own digits, r div the row's pitch, with the plan empty and in the vacuum;
(m) the Fano factor of part 0 at 1:1 and 1:3 over windows of 10 to 400 rounds, on three lays, with its odds;
(n) no signal with a frozen pointer: Alice's settings given by whole sizes laid by the carry sequence, Bob's share of +
    a half at each;
(o) the frozen merges' weight: form B's deciding merges where only light crossed, on seven boards;
(p) the draw only where a Node-clock's swept area crosses the key, the first text's test;
(q) the dependence one Mesh and one round apart, the backward pass's step, on the main lay and seed 4;
(r) the rule's own checks: the edge at e = H with sizes 0, and where the refused rank would draw otherwise.

Usage: python3 -I g5_draw.py <src of main at 0df0e8385>   (the example files are read from
<src>/../examples/tensor24)
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import pushes  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402
from tensor24 import main as t24_main  # noqa: E402
from tensor24.runner import load as t24_load  # noqa: E402
from tensor24.runner.files import sites_of as t24_sites  # noqa: E402

ex_dir = Path(sys.argv[1]).parent.joinpath("examples", "tensor24")
ex_universe = json.loads(ex_dir.joinpath("universe.json").read_text())
ex_shape = json.loads(ex_dir.joinpath("piece.json").read_text())["shape"]
ex_loaded, _ = t24_load.load(ex_universe, {"version": 1, "ticks": 1, "gears": []}, t24_sites(ex_shape),
                             *t24_main.made(t24_load.star(len(ex_shape))))
GRIP = int(t24_main.layout(ex_universe, ex_shape, ex_loaded).grip[0][0])  # the example's grip, read through the loader
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


def hundredths(n):
    whole, rest = carry(n, 100, 0)
    return f"{whole}.{rest:02d}"


def nonneg(n):
    """The law's one whether: 1 where n is at least 0 and 0 below, by one carry, n div (n n + 1) being 0 or -1."""
    return carry(n, n * n + 1, 0)[0] + 1


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
SCALARS = [m_re, m_im, held]  # the theory's pointer: light is T1, outside P
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


def drawn(e, h, sizes):
    """The part drawn by the pointer e within H over whole sizes, in the parts' own order, with no rank and no if:
    part i where C_(i-1) times H is at most e times L and e times L is below C_i times H, C_i the sizes of parts 0
    to i summed and L their total; e = H goes to the last part of nonzero size, whose interval is closed there."""
    total, part, below = sum(sizes), 0, 0
    for k, size in enumerate(sizes):
        above = below + size
        closing = nonneg(above - total) * nonneg(size - 1)  # 1 at the last part of nonzero size
        part += k * nonneg(e * total - below * h) * nonneg(above * h - 1 + closing - e * total)
        below = above
    return part


def equal_sizes(sizes):
    """1 where two of the sizes are equal, for the record: the rule reads no tie."""
    return int(len(set(sizes)) < len(sizes))


def drawn_ranked(e, h, sizes):
    """The refused alternative, for the record alone (a rank is a sort, which the law refuses): the parts sorted by
    size, the larger first, equal sizes in their given order; at e = H the last of nonzero size."""
    order = sorted(range(len(sizes)), key=lambda k: -sizes[k])
    total, below = sum(sizes), 0
    for k in order:
        below += sizes[k]
        if e * total < below * h:
            return k
    return [k for k in order if sizes[k] > 0][-1]


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


def halves(rounds_e):
    """Same half as counts, each with its pairs: one Node-clock two rounds running; one Mesh apart (+x), one round."""
    hs = [[int(2 * e >= h) for e, h in row] for row in rounds_e]
    running = sum(int(hs[t][i] == hs[t + 1][i]) for t in range(len(hs) - 1) for i in range(sites))
    mesh = sum(int(row[i] == row[int(nb[0, i])]) for row in hs for i in range(sites))
    return running, (len(hs) - 1) * sites, mesh, len(hs) * sites


def odds(num, den):
    """A z^2 of one degree, num over den, in its odds class: below 384 hundredths, up to 663, or above."""
    labels = (f"below {hundredths(384)}", f"{hundredths(384)} to {hundredths(663)}", f"above {hundredths(663)}")
    return labels[nonneg(100 * num - 384 * den) + nonneg(100 * num - 663 * den - 1)]


def z2_halves(count, n):
    """A count against half of n: z^2 = (2 count - n)^2 over n, in thousandths, with its odds class."""
    return f"z^2 {shown(carry(1000 * (2 * count - n) ** 2, n, 0)[0])}, {odds((2 * count - n) ** 2, n)}"


def odds_fixed(zero, total, s1, s2):
    lsum = s1 + s2
    return odds((lsum * zero - total * s1) ** 2, total * s1 * s2)


def discrepancy(flat):
    """The star discrepancy's numerator over N H, draws (e, H) all within one H: the largest of j H - e_(j) N and
    e_(j) N - (j - 1) H."""
    n, top_n = len(flat), 0
    for j, (e, h) in enumerate(sorted(flat), start=1):
        assert h == H
        top_n = max(top_n, j * H - e * n, e * n - (j - 1) * H)
    return top_n


SPLITS4 = ((1, 1), (1, 2), (3, 7), (1, 3))  # (c)'s five splits as they draw: the last two of (c) draw as 1 : 3


def largest_gap(flat):
    """The largest |freq(part 0) - share| over (c)'s splits, in ppm, each split drawn by the rule."""
    n = len(flat)
    return max(ppm(abs((s1 + s2) * sum(int(drawn(e, h, [s1, s2]) == 0) for e, h in flat) - n * s1), n * (s1 + s2))
               for s1, s2 in SPLITS4)


def tenths_split(flat):
    """The tenths' chi-square on 9, its halves component on 1 (the 1:1 z^2) and the remainder on 8, in thousandths."""
    counts = [0] * 10
    for e, h in flat:
        counts[tenth(e, h)] += 1
    n, low = sum(counts), sum(counts[:5])
    whole, halves_part = sum((10 * c - n) ** 2 for c in counts), 10 * (2 * low - n) ** 2
    return tuple(carry(1000 * v, 10 * n, 0)[0] for v in (whole, halves_part, whole - halves_part))


def area(s):
    """The swept area Omega = m_re p_im - m_im p_re at every Node-clock, p = W (a - b) + r, each part's stride and
    its kept tooth (the first text's key test)."""
    p_re = W * (s.a[m_re] - s.b[m_re]) + s.r[m_re]
    p_im = W * (s.a[m_im] - s.b[m_im]) + s.r[m_im]
    return (s.a[m_re] * p_im - s.a[m_im] * p_re).tolist()


def pointer_pair(lay_out, s):
    """Each read round's pointers on all five rows and on matter and the held count alone, rounds FROM + 1 to
    ROUNDS: two lists per round of (e, H) at every Node-clock."""
    both = ([], [])

    def read(t, s_in, s_out):
        if t > FROM:
            for got, rows in zip(both, (A1, SCALARS), strict=True):
                got.append(list(zip(*pointers(lay_out, s_in, s_out, rows), strict=True)))

    run(lay_out, s, ROUNDS, read)
    return both


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
reads, reads_out, areas = [], [], []


def read_bc(t, s_in, s_out):
    if t > FROM:
        e, h = pointers(lay6, s_in, s_out)
        digits, _ = carry(s_out.r, pitch_rows, 0)
        reads.append((t, e, h, sizes_at(s_in.a), star(s_out.r.sum(axis=0)), star(digits.sum(axis=0))))
        reads_out.append(list(zip(*pointers(lay6, s_in, s_out, SCALARS), strict=True)))
        areas.append((area(s_in), area(s_out)))


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
            by_e += int(drawn(e, h, [s1, s2]) == 0)
            ties += equal_sizes([s1, s2])
            raw += int(carry(v, lsum, 0)[1] < s1)
            digit += int(carry(dsum, lsum, 0)[1] < s1)
            dial += int(carry(t + dsum, lsum, 0)[1] < s1)
    gap = abs(lsum * by_e - N * s1)  # |freq(part 0) - share| = gap over N L
    if gap * worst_den > worst_gap * N * lsum:
        worst_gap, worst_den = gap, N * lsum
    within = within and gap * H <= 2 * top * lsum
    c_lines.append(f"    sizes {label}, part 0 expected in {carry(N * s1, lsum, 0)[0]} of {N}:")
    c_lines.append(f"      (i) the new rule on e, in the parts' own order, ties {ties}: {born_fixed(by_e, N, s1, s2)}")
    c_lines.append(f"      (ii) the raw sum mod L, c struck: {born_fixed(raw, N, s1, s2)}")
    c_lines.append(f"      (iii) decision 29's digits, c struck: {born_fixed(digit, N, s1, s2)}")
    c_lines.append(f"      (iv) decision 29's digits with its dial, d = (t + D) mod L: {born_fixed(dial, N, s1, s2)}")
zero = ties = expected = variance = 0
for _, e_row, h_row, size_row, _, _ in reads:
    for e, h, (s1, s2) in zip(e_row, h_row, size_row, strict=True):
        zero += int(drawn(e, h, [s1, s2]) == 0)
        ties += equal_sizes([s1, s2])
        expected += carry(SCALE * s1, s1 + s2, 0)[0]
        variance += carry(SCALE * SCALE * s1 * s2, (s1 + s2) * (s1 + s2), 0)[0]
c_lines.append("    sizes read from the state, S1 = m_re^2 + 1 and S2 = m_im^2 + 1 at x in s_in's now slot, by e"
               " in the parts' own order:")
c_lines.append(f"      part 0 in {zero} of {N} (expected {carry(expected, SCALE, 0)[0]}), z^2"
               f" {shown(carry(1000 * (SCALE * zero - expected) ** 2, variance, 0)[0])}, ties {ties}")

# the theory's pointer, light outside it: (b)'s and (c)'s statistics again on the same run
flat_o = [p for row in reads_out for p in row]
es_o = [e for e, _ in flat_o]
lattice_o = 0
for e in es_o:
    lattice_o = gcd(lattice_o, e - es_o[0])
top_o = discrepancy(flat_o)
c_lines_o, worst_o = [], 0
for s1, s2, label in SPLITS:
    zero_o = sum(int(drawn(e, h, [s1, s2]) == 0) for e, h in flat_o)
    worst_o = max(worst_o, ppm(abs((s1 + s2) * zero_o - N * s1), N * (s1 + s2)))
    c_lines_o.append(f"      sizes {label}: {born_fixed(zero_o, N, s1, s2)}, {odds_fixed(zero_o, N, s1, s2)}")
zero_o = ties_o = 0
for (_, _, _, size_row, _, _), row_o in zip(reads, reads_out, strict=True):
    for (e, h), (s1, s2) in zip(row_o, size_row, strict=True):
        zero_o += int(drawn(e, h, [s1, s2]) == 0)
        ties_o += equal_sizes([s1, s2])
z2_o = shown(carry(1000 * (SCALE * zero_o - expected) ** 2, variance, 0)[0])
c_lines_o.append(f"      sizes read from the state: part 0 in {zero_o} of {N} (expected"
                 f" {carry(expected, SCALE, 0)[0]}), z^2 {z2_o}, ties {ties_o}")

rows_same, mesh_same = same_half(rounds_b)
print(f"(b) the pointer e under term 6, rounds {FROM + 1} to {ROUNDS} at all {sites} Node-clocks, {N} draws:")
print(f"    {len(set(es))} distinct values; every e even: {all(carry(e, 2, 0)[1] == 0 for e in es)}; the gcd of all"
      f" differences of e {lattice}, every e {carry(es[0], lattice, 0)[1]} more than a multiple of it")
print(f"    e at 0 in {es.count(0)} draws and at H in {es.count(H)}")
print(f"    chi-square of the tenths of H on 9: {shown(chi_tenths(flat_b))}")
print(f"    in one half, two rounds running {rows_same}, one Mesh apart {mesh_same} per mille (500 for independent"
      f" draws)")
run_same, run_pairs, mesh_count, mesh_pairs = halves(rounds_b)
print(f"      two rounds running {run_same} of {run_pairs}, {z2_halves(run_same, run_pairs)}; one Mesh apart"
      f" {mesh_count} of {mesh_pairs}, {z2_halves(mesh_count, mesh_pairs)}")
print(f"    the star discrepancy D_N of e over H: {ppm(top, N * H)} ppm; the bound 2 D_N: {ppm(2 * top, N * H)} ppm")
# the Kolmogorov law of N D_N^2 for independent uniform draws, in thousandths: its mean of the square pi^2 over 12,
# 822, the alternating sum of 1 over k^2; its 5 per cent point 1844, 1358 squared; the square of its mean 869, 755
print(f"    N times D_N squared: {carry(1000 * top * top, N * H * H, 0)[0]} thousandths, against pi^2 over 12, 822"
      f" thousandths, and the 5 per cent point 1,844 thousandths")
print(f"      (the Kolmogorov law's mean of the square and the point it passes one time in 20, for independent uniform"
      f" draws; the square of the mean {shown(869)} is 755 thousandths)")
print(f"    the largest |freq(part) - share| over (c)'s five Born tests by e: {ppm(worst_gap, worst_den)} ppm; each"
      f" within 2 D_N: {within}")
run_o, pairs_o, mesh_o, mesh_pairs_o = halves(reads_out)
print("    the theory's pointer, light outside it, P over matter and the held count alone:")
print(f"      {len(set(es_o))} distinct values; every e even: {all(carry(e, 2, 0)[1] == 0 for e in es_o)}; the gcd of"
      f" all differences of e {lattice_o}, every e {carry(es_o[0], lattice_o, 0)[1]} more than a multiple of it")
print(f"      e at 0 in {es_o.count(0)} draws and at H in {es_o.count(H)}; chi-square of the tenths of H on 9:"
      f" {shown(chi_tenths(flat_o))}")
print(f"      in one half, two rounds running {run_o} of {pairs_o}, {z2_halves(run_o, pairs_o)}; one Mesh apart"
      f" {mesh_o} of {mesh_pairs_o}, {z2_halves(mesh_o, mesh_pairs_o)}")
print(f"      D_N {ppm(top_o, N * H)} ppm; N times D_N squared {carry(1000 * top_o * top_o, N * H * H, 0)[0]}"
      f" thousandths; the largest |freq(part) - share| over (c)'s five Born tests by e: {worst_o} ppm")

p6 = pitches["term 6"]
print(f"(c) Born, part 0 of sizes S1 and S2, term 6, the draws of (b); t the round, s_t = tick(s_(t-1)), {FROM + 1} to"
      f" {ROUNDS};")
print("    V the raw sum of the fine teeth over x and its six neighbours in s_t; D the sum there of their digits,")
print(f"    r div the row's pitch at load from (a): light {named(p6[0])}, matter {named(p6[1])}, the held count"
      f" {named(p6[2])};")
print("    (ii) to (iv) draw part 0 where d < S1:")
for line in c_lines:
    print(line)
print("    the theory's pointer, light outside it, by e in the parts' own order:")
for line in c_lines_o:
    print(line)

# ==== (d)
print(f"(d) six lays, the old lay's generator at six seeds, term 6, rounds {FROM + 1} to {ROUNDS}, {N} draws each:")
chis, z2s, chis_o, z2s_o, seed_rounds, tenths_by_seed = [], [], [], [], {}, {}
for seed in (SEED, 1, 2, 3, 4, 5):
    seed_rounds[seed] = (rounds_b, reads_out) if seed == SEED else pointer_pair(lay6, lays(seed))
    flat = [p for row in seed_rounds[seed][0] for p in row]
    chis.append(chi_tenths(flat))
    half = sum(int(drawn(e, h, [1, 1]) == 0) for e, h in flat)
    z2s.append(z2_fixed(half, len(flat), 1, 1))
    print(f"    seed {seed}: chi-square of e's tenths on 9 {shown(chis[-1])}; at 1:1"
          f" {born_fixed(half, len(flat), 1, 1)}")
    print(f"      the 1:1 z^2 {odds_fixed(half, len(flat), 1, 1)}; D_N {ppm(discrepancy(flat), len(flat) * H)} ppm;"
          f" the largest |freq - share| over (c)'s five splits {largest_gap(flat)} ppm")
    tenths_by_seed[seed] = tenths_split(flat)
    flat = [p for row in seed_rounds[seed][1] for p in row]
    chis_o.append(chi_tenths(flat))
    half = sum(int(drawn(e, h, [1, 1]) == 0) for e, h in flat)
    z2s_o.append(z2_fixed(half, len(flat), 1, 1))
    print(f"      light outside: chi-square of the tenths on 9 {shown(chis_o[-1])}; D_N"
          f" {ppm(discrepancy(flat), len(flat) * H)} ppm; at 1:1 {born_fixed(half, len(flat), 1, 1)},"
          f" {odds_fixed(half, len(flat), 1, 1)}; the largest |freq - share| {largest_gap(flat)} ppm")
mean_z2 = carry(1000 * (sum(chis) - 6 * 9000) ** 2, 108 * MILLION, 0)[0]  # (mean - 9)^2 over 18 div 6
print(f"    mean chi-square {shown(carry(sum(chis), 6, 0)[0])} over the six; the null: mean 9, variance 18 for one lay,"
      f" 3 for the mean of six;")
print(f"    the mean's z^2 {shown(mean_z2)}")
print(f"    the six z^2 at 1:1: {', '.join(shown(z) for z in z2s)}")
whole, halves_part, rest = tenths_by_seed[4]
print(f"    seed 4's tenths chi-square {shown(whole)}: its halves component {shown(halves_part)} on 1, the 1:1 z^2, and"
      f" the remainder {shown(rest)} on 8")
mean_z2 = carry(1000 * (sum(chis_o) - 6 * 9000) ** 2, 108 * MILLION, 0)[0]
print(f"    light outside: mean chi-square {shown(carry(sum(chis_o), 6, 0)[0])} over the six, the mean's z^2"
      f" {shown(mean_z2)}; the six z^2 at 1:1: {', '.join(shown(z) for z in z2s_o)}")

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
    one = [drawn(e[x], h[x], [1, 1]) for x in range(sites)]
    by_size = [drawn(e[x], h[x], sizes[x]) for x in range(sites)]
    control = old_rule(s_out)
    for x in range(sites):
        books[0][x][one[x]] += 1
        books[1][x][by_size[x]] += 1
        books[2][x][control[x]] += 1
    forward.append((e, one, by_size, control))
    states.append(s_out)
s = states[-1]
same_e = same_one = same_size = same_control = back_ties = recovered = by_untick = 0
for t in range(BACK, 0, -1):
    m = step.mirror(lay6, s)
    m_out = step.tick(lay6, m)
    e, h = pointers(lay6, m, m_out)
    sizes = sizes_at(m.a)
    one = [drawn(e[x], h[x], [1, 1]) for x in range(sites)]
    by_size = [drawn(e[x], h[x], sizes[x]) for x in range(sites)]
    control = old_rule(m_out)
    e_f, one_f, size_f, control_f = forward[t - 1]
    for x in range(sites):
        same_e += int(e[x] == e_f[x])
        same_one += int(one[x] == one_f[x])
        same_size += int(by_size[x] == size_f[x])
        same_control += int(control[x] == control_f[x])
        back_ties += equal_sizes(sizes[x])
        books[0][x][one[x]] -= 1
        books[1][x][by_size[x]] -= 1
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
print(f"      the control's agreement against half of the draws: {z2_halves(same_control, draws)}")


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


def side(e, h, a_in, x, axis, sized=True, refused=False):
    """The site drawn at x between its + and - neighbours along an axis, the + side first in the parts' own order;
    the sizes m_re^2 + 1 at those two in the now slot a_in, or 1 and 1; by the rule, or by the refused rank; and 1
    where the two sizes are equal."""
    plus, minus = int(nb[2 * axis, x]), int(nb[2 * axis + 1, x])
    sizes = [int(a_in[m_re, plus]) ** 2 + 1, int(a_in[m_re, minus]) ** 2 + 1] if sized else [1, 1]
    part = drawn_ranked(e, h, sizes) if refused else drawn(e, h, sizes)
    return (plus, minus)[part], equal_sizes(sizes)


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
            out, tie = side(e[x], h[x], s_in.a, x, 0, refused=True)
            ranked += int(side(et[j], ht[j], t_in.a, j, new_axis, refused=True)[0] == image[out])
            ties += tie
            out = side(e[x], h[x], s_in.a, x, 0)[0]
            given += int(side(et[j], ht[j], t_in.a, j, new_axis)[0] == image[out])
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
    print(f"      the rule, the parts in their own order, + side first: covariant at {sorted({r[4] for r in sel})}")
    print(f"      the rule at sizes 1 and 1: covariant at {sorted({r[5] for r in sel})}")
    print(f"      ranked by size (refused, a sort): covariant at {sorted({r[3] for r in sel})}, ties"
          f" {sorted({r[6] for r in sel})}")

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
        vac_zero += int(drawn(e[x], h[x], [1, 1]) == 0)
        vac_zero_all += int(drawn(e_all[x], h_all[x], [1, 1]) == 0)
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
    half = sum(int(drawn(e, h, [1, 1]) == 0) for e, h in flat)
    print(f"    {name}: {len(set(e for e, _ in flat))} distinct e of {len(flat)}")
    print(f"      chi-square of e's tenths on 9: {shown(chi_tenths(flat))}; joint tenths {'; '.join(lags)}")
    print(f"      at 1:1 {born_fixed(half, len(flat), 1, 1)}")
    print(f"      D_N {ppm(discrepancy(flat), len(flat) * H)} ppm; the largest |freq - share| over (c)'s five splits"
          f" {largest_gap(flat)} ppm")

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


# ==== (j) and (m): one run of term 6 per lay, the pointer read on three row sets at once
ROW_SETS = (("all five rows", A1), ("(j1) the held count alone", [held]),
            ("(j2) matter and the held count, light left out", [m_re, m_im, held]))
LAYS3 = (("the old lay, all 216 Node-clocks", lays(), list(range(sites))),
         ("the hot board, matter laid to 10 counts, all 216 Node-clocks", swing_lay(10, 1, False), list(range(sites))),
         ("the cold packet, one packet near 100 counts, its 27 Node-clocks", swing_lay(100, 0, True), centre))
WINDOWS = (10, 40, 100, 200, 400)


def three_runs(s, read_at):
    """Rounds FROM + 1 to ROUNDS of term 6 from s: for each row set, a list per round of (e, H) at the Node-clocks
    read."""
    got = [[] for _ in ROW_SETS]

    def read(t, s_in, s_out):
        if t > FROM:
            for k, (_, rows) in enumerate(ROW_SETS):
                e, h = pointers(lay6, s_in, s_out, rows)
                got[k].append([(e[i], h[i]) for i in read_at])

    run(lay6, s, ROUNDS, read)
    return got


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


print(f"(j) the rows the pointer reads, term 6, rounds {FROM + 1} to {ROUNDS}: (b)'s statistics with the pointer on")
print("    (j1) the held count alone and (j2) matter and the held count, light left out; parts in their own order:")
fano_lines = []
for lay_name, lay_j, read_at in LAYS3:
    runs = three_runs(lay_j, read_at)
    for (set_name, _), rounds_e in zip(ROW_SETS[1:], runs[1:], strict=True):
        flat = [p for row in rounds_e for p in row]
        n = len(flat)
        half = sum(int(drawn(e, h, [1, 1]) == 0) for e, h in flat)
        quarter = sum(int(drawn(e, h, [1, 3]) == 0) for e, h in flat)
        pairs = [(tenth(*rounds_e[t][k]), tenth(*rounds_e[t + 1][k])) for t in range(len(rounds_e) - 1)
                 for k in range(len(read_at))]
        chi, free = chi_joint(pairs)
        print(f"    {lay_name}, {set_name}:")
        print(f"      {len(set(e for e, _ in flat))} distinct e of {n}; chi-square of the tenths on 9"
              f" {shown(chi_tenths(flat))}; D_N {ppm(discrepancy(flat), n * H)} ppm")
        print(f"      at 1:1 {born_fixed(half, n, 1, 1)}")
        print(f"      at 1:3 {born_fixed(quarter, n, 1, 3)}")
        print(f"      joint tenths one round apart: {shown(chi)} on {free}")
    marks = [[[int(drawn(e, h, sizes) == 0) for e, h in row] for row in runs[0]] for sizes in ([1, 1], [1, 3])]
    fano_lines.append(f"    {lay_name}:")
    for m in WINDOWS:
        f_half, windows, num_h, den_h = fano(marks[0], 1, 2, m)
        f_quarter, _, num_q, den_q = fano(marks[1], 1, 4, m)
        fano_lines.append(f"      M = {m}, {windows} windows: {shown(f_half)} at 1:1 (z^2"
                          f" {shown(carry(1000 * num_h, den_h, 0)[0])}, {odds(num_h, den_h)}), {shown(f_quarter)} at"
                          f" 1:3 (z^2 {shown(carry(1000 * num_q, den_q, 0)[0])}, {odds(num_q, den_q)})")

# ==== (k)
KEY = MILLION  # the record tooth's teeth
TOOTH = carry(KEY - 1, 2, 0)[0]  # its birth
WRITES = (("a record tooth on the hand, one per Node-clock and part, flipped by the mirror", "tooth"),
          ("a whole count into the winner's now slot, matter's row", "now"),
          ("a whole count into the winner's now slot, light's row, the pointer without light", "light now"),
          ("both slots of light's row, the law's take, the pointer without light", "light both"),
          ("both slots of matter's row", "both"),
          ("a fine tooth moved by a grip, its quotient into the now slot, matter's row", "grip"))


def writing_act(s, hand, how):
    """One act for both ways of time: tick, the pointer from (s, tick(s)), the draw between x's matter re and im rows
    (sizes m_re^2 + 1 and m_im^2 + 1 in s's now slot, in the parts' own order), then the write; returns the state,
    the hand's record teeth, the pointers and the parts drawn."""
    s_out = step.tick(lay6, s)
    e, h = pointers(lay6, s, s_out, [m_re, m_im, held] if how.startswith("light") else A1)
    sizes = sizes_at(s.a)
    parts = [drawn(e[x], h[x], sizes[x]) for x in range(sites)]
    a, b, r, hand = s_out.a.copy(), s_out.b.copy(), s_out.r.copy(), hand.copy()
    for x, part in enumerate(parts):
        mrow, lrow = (m_re, m_im)[part], (l_re, l_im)[part]
        if how == "tooth":
            spill, hand[part, x] = carry(hand[part, x] + 1, KEY, 0)
            assert spill == 0  # the record's quotient never leaves on this run
        elif how == "now":
            a[mrow, x] += 1
        elif how == "light now":
            a[lrow, x] += 1
        elif how == "light both":
            a[lrow, x] += 1
            b[lrow, x] += 1
        elif how == "both":
            a[mrow, x] += 1
            b[mrow, x] += 1
        else:
            moved, r[mrow, x] = carry(r[mrow, x] + GRIP, W, 0)
            a[mrow, x] += moved
    return State(a, b, r, s_out.rd.copy()), hand, e, parts


def mirrored(s, hand):
    """The state mirrored by the engine, and each record tooth flipped in its teeth, KEY - 1 - k."""
    return step.mirror(lay6, s), KEY - 1 - hand


print(f"(k) the run back with a click that writes, term 6, {BACK} rounds out from the old lay and {BACK} back:")
print("    the draw at every Node-clock between its matter re and im rows, sizes m_re^2 + 1 and m_im^2 + 1 in s's now")
print("    slot, in the parts' own order, then the write; forward, s_t is the act on s_(t-1); back, s_(t-1) is the")
print(f"    same act on mirror(s_t), mirrored, with no list read; the pointer on all five rows unless said;"
      f" {BACK * sites} draws each way:")
for label, how in WRITES:
    s, hand = lays(), np.full((2, sites), TOOTH, dtype=object)
    path, record = [s], []
    for _ in range(BACK):
        s, hand, e, parts = writing_act(s, hand, how)
        path.append(s)
        record.append((e, parts))
    moved_teeth = sum(int(v != TOOTH) for v in hand.ravel().tolist())
    same_e = same_part = recovered = 0
    for t in range(BACK, 0, -1):
        m, m_hand = mirrored(s, hand)
        m_out, m_hand_out, e_back, parts_back = writing_act(m, m_hand, how)
        s, hand = mirrored(m_out, m_hand_out)
        e_f, parts_f = record[t - 1]
        same_e += sum(int(p == q) for p, q in zip(e_back, e_f, strict=True))
        same_part += sum(int(p == q) for p, q in zip(parts_back, parts_f, strict=True))
        recovered += int(all(np.array_equal(p, q) for p, q in zip(s, path[t - 1], strict=True)))
    home = all(np.array_equal(p, q) for p, q in zip(s, lays(), strict=True)) and all(
        v == TOOTH for v in hand.ravel().tolist())
    print(f"    {label}:")
    print(f"      the pointer equal at {same_e} of {BACK * sites}; the part equal at {same_part}; s_(t-1) recovered at"
          f" {recovered} of {BACK} rounds")
    print(f"      the lay and the hand return: {home}"
          + (f"; {moved_teeth} of {2 * sites} record teeth moved on the way out" if how == "tooth" else ""))


# ==== (l)
def dial_run(lay_out, s, rows, pitch, rounds, marks):
    """Decision 29's digits D, the sum over x and its six neighbours of r div the row's pitch in s_t over the given
    rows: D mod TURN's values, per Node-clock and over the board; the dial's part 0 at each Node-clock over the first
    rounds of each mark; c struck, part 0 over the same rounds."""
    over_board, at = set(), [set() for _ in range(sites)]
    dial, struck = {mk: [0] * sites for mk in marks}, dict.fromkeys(marks, 0)

    def read(t, s_in, s_out):
        digits, _ = carry(s_out.r, pitch, 0)
        for x, v in enumerate(star(digits[rows].sum(axis=0))):
            _, kept = carry(v, TURN, 0)
            over_board.add(kept)
            at[x].add(kept)
            for mk in marks:
                if t <= mk:
                    dial[mk][x] += int(carry(t + v, TURN, 0)[1] < 500)
                    struck[mk] += int(kept < 500)

    run(lay_out, s, rounds, read)
    return over_board, at, dial, struck


def pitch_column(train_pitch):
    column = np.zeros((ROWS, 1), dtype=object)
    for k, (_, rows) in enumerate(TRAINS):
        for row in rows:
            column[row, 0] = train_pitch[k]
    return column


p0 = pitches["the plan empty"]
print("(l) decision 29's dial on its own digits: D the sum over x and its six neighbours of r div the row's pitch at")
print(f"    load (from (a)), in s_t; L = {TURN}, sizes 500 and 500; the dial d = (t + D) mod {TURN}, t the round;")
print(f"    c struck, d = D mod {TURN}:")
over_board, at, dial, struck = dial_run(lay0, lays(), A1, pitch_column(p0), TURN, (TURN,))
print(f"    the plan empty, the old lay, {TURN} rounds, all five rows, light {named(p0[0])}, matter {named(p0[1])}, the"
      f" held count {named(p0[2])}:")
print(f"      D mod {TURN} takes {len(over_board)} values over the board, from {min(over_board)} to {max(over_board)};"
      f" at most {max(len(v) for v in at)} at one Node-clock;")
print(f"      frozen at every Node-clock: {all(len(v) == 1 for v in at)}")
print(f"      the dial: part 0 from {min(dial[TURN])} to {max(dial[TURN])} times of {TURN} over the Node-clocks;"
      f" exactly 500 at each: {all(c == 500 for c in dial[TURN])}")
print(f"      c struck: part 0 in {struck[TURN]} of {TURN * sites}")
over_board, at, dial, struck = dial_run(lay6, vacuum_lay(), [m_re, m_im, held], pitch_column(p6), TURN, (VACUUM, TURN))
print(f"    the vacuum of (g), term 6, matter and the held count, matter {named(p6[1])}, the held count"
      f" {named(p6[2])}:")
print(f"      D mod {TURN} takes {sorted(over_board)} over the board; frozen at every Node-clock:"
      f" {all(len(v) == 1 for v in at)}")
for mk in (VACUUM, TURN):
    print(f"      over the first {mk} rounds, the dial: part 0 from {min(dial[mk])} to {max(dial[mk])} times of {mk}"
          f" over the Node-clocks;")
    print(f"        c struck: part 0 in {struck[mk]} of {mk * sites}")

# ==== (m)
print("(m) the Fano factor of part 0's count in windows of M rounds at one Node-clock, pooled over the Node-clocks")
print(f"    read: its squared gap from the binomial mean over the binomial variance, {shown(1000)} for independent")
print("    draws, and its z^2 against its own binomial spread, one degree; term 6, the pointer on all five rows,")
print(f"    rounds {FROM + 1} to {ROUNDS}, in the parts' own order:")
for line in fano_lines:
    print(line)

# ==== (n)
FROZEN = [carry((2 * k + 1) * H, 20, 0)[0] for k in range(10)]  # e frozen at the middle of each tenth of H
SPREAD = 6240  # pointers spread evenly, each the floor of (2 k + 1) H over 2 SPREAD: a multiple of every total below
evenly = [carry((2 * k + 1) * H, 2 * SPREAD, 0)[0] for k in range(SPREAD)]
JOINT = ("++", "+-", "-+", "--")  # Alice's sign, then Bob's


def bob_plus(pointer_list, sizes):
    return sum(int(JOINT[drawn(e, H, sizes)][1] == "+") for e in pointer_list)


# Alice's settings, each given by the whole sizes of the four joint outcomes, (x, y, y, x), x and y laid by the probe's
# generic carry sequence, so no setting is picked to land at an angle or on a law of angles (law line 102, the owner's
# answer: a value is lawful by chance or from the families); in every set Bob's own share of + is a half at each
# setting, so a fair pointer signals nothing
setting_pick = generator(SEED)


def laid_setting():
    x, y = setting_pick(4) + 5, setting_pick(4) + 5
    return (x, y, y, x)


SETTING_SETS = (
    ("two settings of Alice's", (laid_setting(), laid_setting())),
    ("three settings of Alice's", (laid_setting(), laid_setting(), laid_setting())))
print("(n) no signal with a frozen pointer: the four joint outcomes in the order ++, +-, -+, -- (Alice's sign, then"
      " Bob's),")
print("    sized in whole numbers per setting of Alice's, (x, y, y, x) laid by the probe's carry sequence, and drawn by the"
      " page's rule in that order, with no rank;")
print("    Bob's analyser fixed, and in every set Bob's own share of + a half at each setting:")
act_e = [e for e, _ in flat_b]
for title, settings in SETTING_SETS:
    print(f"    {title}, sizes " + "; ".join(", ".join(str(v) for v in sizes) for sizes in settings) + ":")
    even_bob, act_bob = [], []
    for sizes in settings:
        even_bob.append(str(bob_plus(evenly, list(sizes))))
        count = bob_plus(act_e, list(sizes))
        act_bob.append(f"{count} (z^2 {shown(z2_fixed(count, N, 1, 1))})")
    per_tenth = ["".join(JOINT[drawn(e, H, list(sizes))][1] for sizes in settings) for e in FROZEN]
    moved = [k for k, bob in enumerate(per_tenth) if len(set(bob)) > 1]
    print(f"      e frozen at the middle of each tenth of H, Bob's draw at each setting: {', '.join(per_tenth)};"
          f" the far setting moves Bob's draw at {len(moved)} of 10 frozen values (tenths {moved})")
    print(f"      e spread evenly, {SPREAD} pointers: Bob + in {', '.join(even_bob)} of {SPREAD}")
    print(f"      e as the act spreads it, (b)'s {N} draws: Bob + in {', '.join(act_bob)} of {N}")

# ==== (o)
SPOKE_STEPS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def mesh_distance(p, q):
    return sum(abs(u - v) for u, v in zip(p, q, strict=True))


def tree(cells, source):
    """CLICKS-CLOSED section 13's tree: each Node-clock's parent its first neighbour, in the Spoke order +x, -x, +y, -y,
    +z, -z, one Mesh nearer the source; its children in sorted order."""
    inside = set(cells)
    arrival = {c: mesh_distance(c, source) for c in cells}
    up = {}
    for c in cells:
        if arrival[c] == 0:
            continue
        for d in SPOKE_STEPS:
            n = tuple(u + v for u, v in zip(c, d, strict=True))
            if n in inside and arrival[n] == arrival[c] - 1:
                up[c] = n
                break
    kids = {c: [] for c in cells}
    for c, p in sorted(up.items()):
        kids[p].append(c)
    return arrival, kids


def deciding(cells, source, takes):
    """Pass 2's totals, from the farthest Node-clocks to the source; a merge decides where two or more of its inputs,
    its own take and its children's totals, are not 0; for each, whether it is an absorber, and whether its seven
    Node-clocks, the pointer's, hold an absorber or the source."""
    arrival, kids = tree(cells, source)
    tot = {}
    for c in sorted(cells, key=lambda q: -arrival[q]):
        tot[c] = takes.get(c, 0) + sum(tot[k] for k in kids[c])
    inside = set(cells)
    out = []
    for c in cells:
        inputs = int(takes.get(c, 0) > 0) + sum(int(tot[k] > 0) for k in kids[c])
        if inputs >= 2:
            near = [tuple(u + v for u, v in zip(c, d, strict=True)) for d in SPOKE_STEPS] + [c]
            out.append((c, c in takes, any(q in takes or q == source for q in near if q in inside)))
    return out


def cube(side):
    return [(x, y, z) for x in range(side) for y in range(side) for z in range(side)]


def merge_line(name, cells, source, takes):
    found = deciding(cells, source, takes)
    near = sum(int(m) for _, _, m in found)
    print(f"    {name}:")
    print(f"      {len(takes)} absorbers; {len(found)} deciding merges, {sum(int(a) for _, a, _ in found)} at an"
          f" absorber, {near} with an absorber or the source among the seven, {len(found) - near} where only light"
          f" crossed")
    return found


print("(o) the frozen merges' weight: form B's deciding merges, CLICKS-CLOSED section 13's backward pass on")
print("    spread_quantum.py's tree, rebuilt in whole numbers (its probe left the tree at 1b6ca0bf9); a Node-clock's")
print("    parent its first neighbour, +x -x +y -y +z -z, one Mesh nearer the source; a merge decides where two or")
print("    more of its inputs are not 0; its pointer is frozen where none of its seven Node-clocks holds an absorber")
print("    or the source, so only light crossed there:")
c0 = 3
own = {(c0 + 3, c0, c0): 5, (c0, c0 - 3, c0): 3, (c0, c0, c0 + 2): 8, (c0 + 1, c0 + 1, c0 - 3): 6,
       (c0 - 3, c0 - 3, c0 - 3): 1, (c0 + 2, c0 - 2, c0 + 2): 7, (0, 6, 6): 2}  # sigma_f sigma_b; the full one takes 0
for c, absorber, near in merge_line("spread_quantum.py's board, side 7, the source at the centre, its absorbers' takes"
                                    " sigma_f sigma_b,\n    the full one, taking 0, left out", cube(7), (c0, c0, c0),
                                    own):
    print(f"        the merge at {c}: an absorber {absorber}; an absorber or the source among its seven {near}")
c0 = 10
merge_line("two detectors at +10 x and -10 x, side 21", cube(21), (c0, c0, c0), {(c0 + 10, c0, c0): 1,
                                                                               (c0 - 10, c0, c0): 1})
merge_line("two detectors at +10 x and +10 y, side 21", cube(21), (c0, c0, c0), {(c0 + 10, c0, c0): 1,
                                                                               (c0, c0 + 10, c0): 1})
merge_line("two detectors at +10 z and +6 x +4 z, side 21", cube(21), (c0, c0, c0), {(c0, c0, c0 + 10): 1,
                                                                                   (c0 + 6, c0, c0 + 4): 1})
merge_line("a full screen, the face z = 20 of side 21, the source at (10, 10, 0)", cube(21), (10, 10, 0),
           {(x, y, 20): 1 for x in range(21) for y in range(21)})
pick_state, sparse = SEED, {}
for c in cube(21):
    _, pick_state = carry(1103515245 * pick_state + 12345, 2147483648, 0)
    if carry(pick_state, 100, 0)[1] == 0 and c != (10, 10, 10):
        sparse[c] = 1
merge_line("sparse absorbers, about one Node-clock in 100 by the old lay's generator, side 21, the source at the\n"
           "    centre",
           cube(21), (10, 10, 10), sparse)
merge_line("one pixel in four of the face z = 20, the source at (10, 10, 0)", cube(21), (10, 10, 0),
           {(x, y, 20): 1 for x in range(21) for y in range(21) if carry(x + 3 * y, 4, 0)[1] == 0})

# ==== (p)
KEY_AREA = 10**10 * W  # the first text's key


def crossing_draws(rounds_e):
    """(b)'s run read only at the rounds where a Node-clock's swept area crosses a multiple of the key, from s_in to
    s_out: the pointers (e, H) there, and the sizes in s_in's now slot."""
    picked, sizes = [], []
    for t, (before, after) in enumerate(areas):
        for x in range(sites):
            if carry(before[x], KEY_AREA, 0)[0] != carry(after[x], KEY_AREA, 0)[0]:
                picked.append(rounds_e[t][x])
                sizes.append(reads[t][3][x])
    return picked, sizes


print("(p) the draw only at the rounds where a Node-clock's swept area Omega = m_re p_im - m_im p_re crosses a")
print("    multiple of the key 10^10 W, p = W (a - b) + r, from s_in to s_out (the first text's test), on (b)'s run:")
for label, rounds_e in (("light counted", rounds_b), ("light outside", reads_out)):
    picked, sizes = crossing_draws(rounds_e)
    n = len(picked)
    half = sum(int(drawn(e, h, [1, 1]) == 0) for e, h in picked)
    zero = expected_p = variance_p = 0
    for (e, h), (s1, s2) in zip(picked, sizes, strict=True):
        zero += int(drawn(e, h, [s1, s2]) == 0)
        expected_p += carry(SCALE * s1, s1 + s2, 0)[0]
        variance_p += carry(SCALE * SCALE * s1 * s2, (s1 + s2) * (s1 + s2), 0)[0]
    gap2 = (SCALE * zero - expected_p) ** 2
    print(f"    {label}: {n} crossings; chi-square of e's tenths on 9 {shown(chi_tenths(picked))}; D_N"
          f" {ppm(discrepancy(picked), n * H)} ppm")
    print(f"      at 1:1 {born_fixed(half, n, 1, 1)}, {odds_fixed(half, n, 1, 1)}; the largest |freq - share| over"
          f" (c)'s five splits {largest_gap(picked)} ppm")
    print(f"      the state's sizes there: part 0 in {zero} of {n} (expected {carry(expected_p, SCALE, 0)[0]}), z^2"
          f" {shown(carry(1000 * gap2, variance_p, 0)[0])}, {odds(gap2, variance_p)}")

# ==== (q)
print("(q) the dependence one Mesh and one round apart, the backward pass's step: e at (x, t) against e at x's")
print("    neighbour at t + 1, along +x and along all six Spokes; joint tenths on 81, and the same half with its odds:")
for seed in (SEED, 4):
    for label, rounds_e in zip(("light counted", "light outside"), seed_rounds[seed], strict=True):
        tens = [[tenth(e, h) for e, h in row] for row in rounds_e]
        sides = [[int(2 * e >= h) for e, h in row] for row in rounds_e]
        for spokes_used, along in (((0,), "+x"), (tuple(range(6)), "all six Spokes")):
            index = [(t, x, int(nb[k, x])) for t in range(len(rounds_e) - 1) for x in range(sites)
                     for k in spokes_used]
            chi, free = chi_joint([(tens[t][x], tens[t + 1][y]) for t, x, y in index])
            same = sum(int(sides[t][x] == sides[t + 1][y]) for t, x, y in index)
            print(f"    seed {seed}, {label}, along {along}: joint tenths {shown(chi)} on {free}; same half {same} of"
                  f" {len(index)}, {z2_halves(same, len(index))}")

# ==== (r)
EDGE_LISTS = ([1, 0], [0, 1], [3, 2, 0], [0, 5], [0, 0, 3], [2, 0, 2], [1, 1, 0, 0])
print("(r) the rule's own checks: the edge, e = H to the last part of nonzero size in the parts' own order, on size")
print("    lists with zeros; each list drawn on an evenly spread grid of pointers, twelve times its total, and at")
print("    e = 0 and at e = H:")
for sizes in EDGE_LISTS:
    total, counts = sum(sizes), [0] * len(sizes)
    grid_n = 12 * total
    for k in range(grid_n):
        counts[drawn(carry((2 * k + 1) * H, 2 * grid_n, 0)[0], H, sizes)] += 1
    exact = all(counts[k] * total == grid_n * size for k, size in enumerate(sizes))
    at_zero, at_h = drawn(0, H, sizes), drawn(H, H, sizes)
    print(f"    sizes {sizes}: {grid_n} pointers drawn {counts}, each part its share exactly: {exact}; at e = 0 part"
          f" {at_zero}; at e = H part {at_h}, size {sizes[at_h]} (the last part in that order: part {len(sizes) - 1},"
          f" size {sizes[-1]})")
differ = [f"{s1}:{s2} at {sum(int(drawn(e, h, [s1, s2]) != drawn_ranked(e, h, [s1, s2])) for e, h in flat_b)}"
          for s1, s2 in ((1, 2), (3, 7), (1, 3))]
print(f"    for the record, (b)'s {N} draws where the refused rank and the parts' own order pick different parts:"
      f" {'; '.join(differ)}")
