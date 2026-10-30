"""Term 7, the drive: one carry of the source at the drive's teeth, on the act the night builds (node-live f72067cdf).

Whole numbers alone, every division Rule3's carry: no float, root, logarithm, exponential or search, no function of
the turn's arc, and no state laid by one. The act's drive and kick (engine/step.py): q_d, r_d+ = carry(J, T_d, r_d);
K = s T_k q_d; the push s F + K; the momentum P = 2 D_in (a - b) + tooth, which the round carries to P+ = P + 4 push
(the edge's split, the 2 the senses of an axis, both read from the star).

(a) the drive's books, read from outside at every gear and round: q_d = (J + r_d - r_d+) / T_d whole; the kick read
    off the momentum, K = (P+ - P - 4 s F) / 4, equal to s T_k q_d; and over the run T_d SUM K = s T_k (SUM J + r_d(0)
    - r_d(end)) exactly, so the drive keeps every push to within one of its teeth;
(b) the drive's tooth moving: the rounds in which r_d changes, per row, at T_d = 2 and 7;
(c) the run back: rounds out and the same number back by untick (the mirror, the act, the mirror), bit for bit, on
    even rows and an odd row, at T_d = 1, 2 and 7;
(d) the mirror by parity against its mutants: the odd row's drive tooth flipped, and the even rows' kept;
(e) the drive as the books' dial: at T_k = 1 and T_d = 2 the push over the run is half the source's, to within one
    tooth, the remainder kept;
(f) the dial in the beat: Mesh-less Node-clocks, each its own oscillator, the drive at T_d 7 against the same equation
    carried by teeth seven times larger at T_d 1 and by the linear recurrence at the scale 10^30, between the springs
    on each side; (f2) the two acts count for count, the teeth act's edge tooth T_d s + 4 r_d, with the edge tooth laid
    a multiple of 4 (the act keeps its residue modulo 4 at standing teeth, every push entering the momentum four times)
    and, for the no, at 3 modulo 4, where the finer dial splits a count earlier at the dial's top;
(g) the drive inside the act's two passes: the metric's push J5 (the books' form) reads a row's momenta after a first
    drive on J1 alone; the run back holds at every T_d when J5 reads no row it pushes (the mirror theorem's hypothesis
    (d)), and fails at every T_d, T_d 1 included, when it does: the condition is the act's, not the drive's.

Usage: python3 -I term7_drive.py <src of node-live at f72067cdf> (about 50 s)
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry, flip  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import pushes  # noqa: E402
from tensor24.engine.state import Click, Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402

W = 6 * 10**6
GRIP = 10**6
UNIT = -1
NONE_I = np.zeros(0, dtype=np.intp)
NONE_O = np.zeros(0, dtype=object)
UNREAD = Read(NONE_I, NONE_O, NONE_I)
NOPLAN = Plan(NONE_I, NONE_I, NONE_I, NONE_O, NONE_I)
ROWS = 3  # two even rows (parity 1) and one odd row (parity 0), as the metric's 0i slots are
PARITY = (1, 1, 0)


def generator(seed):
    state = seed

    def pick(span):
        nonlocal state
        _, state = carry(1103515245 * state + 12345, 2147483648, 0)
        return carry(state, 2 * span + 1, 0)[1] - span

    return pick


def plan_of(terms):
    factor = np.array([f for f, _ in terms], dtype=object)
    legs = tuple(np.array([leg[i] for _, leg in terms], dtype=np.intp) for i in range(4))
    return pushes(factor, legs)


# J's potential: each row's own spring and a tie of odd factor between the two even rows (a spring alone pushes by an even
# count); the odd row's spring is even in it, so the
# potential is kept under time's reversal and the odd row's source turns with it
TERMS = [(3 * 10**4, (0, 0, UNIT, UNIT)), (2 * 10**4, (1, 1, UNIT, UNIT)), (7 * 10**3 + 1, (0, 1, UNIT, UNIT)),
         (5 * 10**4, (2, 2, UNIT, UNIT))]


def layout(shape, t_d, t_k=None):
    """The act's layout on a board of the shape: three rows at the teeth W, every Mesh at GRIP, the drive's teeth t_d on
    every row and the kick's t_k (t_d unless given), the stretch 1, the parities PARITY; no clock read, no grip read, no
    click term, no metric push, no Mesh term."""
    nb = board(shape)
    sites = nb.shape[1]
    spokes, meshes = geometry(nb, 3)
    grip = np.full((ROWS, 3 * sites), GRIP, dtype=object)
    ones = np.ones((ROWS, 1), dtype=object)
    t_k = t_d if t_k is None else t_k
    parity = np.array([[p] for p in PARITY], dtype=object)
    gearing = Gearing(W * ones, ones.copy(), t_k * ones, t_d * ones, parity)
    click = Click(NONE_I, NONE_I, NONE_O, NONE_I, np.ones((1, 1), dtype=object))
    parts = [nb, spokes, meshes, grip, gearing, plan_of(TERMS), UNREAD, UNREAD, click, NOPLAN]
    parts += [NOPLAN] * (len(Layout._fields) - len(parts))
    return Layout(*parts), sites


def lay(sites, t_d, seed):
    pick = generator(seed)
    a = np.array([[pick(5000) for _ in range(sites)] for _ in range(ROWS)], dtype=object)
    b = np.array([[a[r, i] - pick(40) for i in range(sites)] for r in range(ROWS)], dtype=object)
    tooth = np.array([[pick(W) for _ in range(sites)] for _ in range(ROWS)], dtype=object)  # within [-2 W, 2 W)
    rd = np.array([[carry(pick(10**6), t_d, 0)[1] for _ in range(sites)] for _ in range(ROWS)], dtype=object)
    return State(a, b, tooth, rd, np.zeros((1, sites), dtype=object))


def momentum(lay_, s):
    wa, wb = step.dials(lay_, s)
    return 2 * (wa + wb) * (s.a - s.b) + s.r


def books(shape, t_d, t_k, rounds, seed):
    lay_, sites = layout(shape, t_d, t_k)
    s = lay(sites, t_d, seed)
    r0 = s.rd.copy()
    sum_j = np.zeros((ROWS, sites), dtype=object)
    sum_k = np.zeros((ROWS, sites), dtype=object)
    k_ok = q_ok = moved = 0
    moved_rows = [0] * ROWS
    for _ in range(rounds):
        force, j = step.sources(lay_, s.a)
        p_in = momentum(lay_, s)
        s1 = step.tick(lay_, s)
        p_out = momentum(lay_, s1)
        q_num = j + s.rd - s1.rd
        q_d = np.array([[carry(x, t_d, 0)[0] for x in row] for row in q_num.tolist()], dtype=object)
        q_whole = all(carry(x, t_d, 0)[1] == 0 for x in q_num.ravel().tolist())
        kick = p_out - p_in - 4 * force
        k_whole = all(carry(x, 4, 0)[1] == 0 for x in kick.ravel().tolist())
        kick = np.array([[carry(x, 4, 0)[0] for x in row] for row in kick.tolist()], dtype=object)
        q_ok += int(q_whole)
        k_ok += int(k_whole and bool((kick == t_k * q_d).all()))
        for r in range(ROWS):
            moved_rows[r] += int(bool((s1.rd[r] != s.rd[r]).any()))
        moved += int(bool((s1.rd != s.rd).any()))
        sum_j += j
        sum_k += kick
        s = s1
    total = bool((t_d * sum_k == t_k * (sum_j + r0 - s.rd)).all())
    return q_ok, k_ok, total, moved_rows, sum_j, sum_k, s, r0


print(f"the act's layout: three rows at the teeth W = {W}, every Mesh at {GRIP}, rows 0 and 1 even and row 2 odd; J's"
      " potential each row's spring and a tie between the even rows, the odd row's spring even in it")
print("(a) the drive's books at every gear and round, read from outside, on a cube of 3:")
for t_d, t_k in ((1, 1), (2, 2), (7, 7), (2, 1), (7, 1)):
    q_ok, k_ok, total, moved_rows, _, _, _, _ = books((3, 3, 3), t_d, t_k, 200, 5 + t_d)
    print(f"  T_d {t_d}, T_k {t_k}: q_d = (J + r_d - r_d+) / T_d whole in {q_ok} of 200 rounds; the kick read off the"
          f" momentum, (P+ - P - 4 s F) / 4, equal to s T_k q_d in {k_ok} of 200; T_d SUM K = s T_k (SUM J + r_d(0) -"
          f" r_d(end)) at every gear: {total}")
print("(b) the drive's tooth moving, rounds of 200 in which some gear's r_d changes, per row (even, even, odd):")
for t_d in (1, 2, 7):
    _, _, _, moved_rows, _, _, _, _ = books((3, 3, 3), t_d, t_d, 200, 11 + t_d)
    print(f"  T_d {t_d}: {moved_rows}")


def run_back(t_d, rounds, seed, mutant=None):
    lay_, sites = layout((3, 3, 3), t_d)
    start = lay(sites, t_d, seed)
    s = start
    for _ in range(rounds):
        s = step.tick(lay_, s)
    if mutant is None:
        for _ in range(rounds):
            s = step.untick(lay_, s)
    else:
        for _ in range(rounds):
            s = mutant(lay_, step.tick(lay_, mutant(lay_, s)))
    return all(bool((x == y).all()) for x, y in zip(s, start))


def mirror_with(odd_flips, even_keeps):
    def mirrored(lay_, s):
        m = step.mirror(lay_, s)
        rd = m.rd.copy()
        for r, p in enumerate(PARITY):
            if p == 0 and odd_flips:
                rd[r] = flip(s.rd[r], lay_.gearing.drive[r])
            if p == 1 and even_keeps:
                rd[r] = s.rd[r]
        return State(m.a, m.b, m.r, rd, m.k)
    return mirrored


print("(c) the run back, 400 rounds out and 400 back by untick, cube of 3, the lay drawn with every tooth moving:")
for t_d in (1, 2, 7):
    print(f"  T_d {t_d}: the start returned bit for bit: {run_back(t_d, 400, 21 + t_d)}")
print("(d) the mirror by parity against its mutants, T_d 7, 400 rounds out and back:")
print(f"  the law's mirror (even rows' drive tooth flipped, the odd row's kept): {run_back(7, 400, 31)}")
print(f"  the odd row's drive tooth flipped too: {run_back(7, 400, 31, mirror_with(True, False))}")
print(f"  the even rows' drive tooth kept: {run_back(7, 400, 31, mirror_with(False, True))}")
print("(e) the drive as the books' dial: T_k 1 against T_k = T_d, the kicks summed over 200 rounds at every gear of row 0:")
for t_d in (2, 7):
    _, _, _, _, sum_j, sum_k, s, r0 = books((3, 3, 3), t_d, 1, 200, 41)
    gap = [int(t_d * k - j) for k, j in zip(sum_k[0].tolist(), sum_j[0].tolist())]
    print(f"  T_d {t_d}, T_k 1: T_d SUM K - SUM J at row 0's gears within {min(gap)} to {max(gap)}, against the bound"
          f" -(T_d - 1) to T_d - 1; the push carried is SUM J / T_d to within one tooth of the drive")


def sign(x):
    return int(x > 0) - int(x < 0)


def lone(shape, teeth, t_d, f):
    """One even row on a Mesh-less board (every grip 0), so every Node-clock is its own oscillator: the teeth, the drive's
    teeth t_d, the kick's 1, the stretch 1, the row's own spring f."""
    nb = board(shape)
    sites = nb.shape[1]
    spokes, meshes = geometry(nb, 3)
    one = np.ones((1, 1), dtype=object)
    gearing = Gearing(teeth * one, one.copy(), one.copy(), t_d * one, one.copy())
    click = Click(NONE_I, NONE_I, NONE_O, NONE_I, np.ones((1, 1), dtype=object))
    parts = [nb, spokes, meshes, np.zeros((1, 3 * sites), dtype=object), gearing, plan_of([(f, (0, 0, UNIT, UNIT))]),
             UNREAD, UNREAD, click, NOPLAN]
    parts += [NOPLAN] * (len(Layout._fields) - len(parts))
    return Layout(*parts), sites


def lone_lay(sites, seed):
    pick = generator(seed)
    a = np.array([[pick(5000) for _ in range(sites)]], dtype=object)
    b = np.array([[a[0, i] - pick(300) for i in range(sites)]], dtype=object)
    zero = np.zeros((1, sites), dtype=object)
    return State(a, b, zero, zero.copy(), zero.copy())


def count_turns(rows_of_counts):
    """The sign changes of every Node-clock's count over the run, summed: a zero keeps the last sign."""
    last = [sign(x) for x in rows_of_counts[0]]
    turns = 0
    for counts in rows_of_counts[1:]:
        for i, x in enumerate(counts):
            g = sign(x)
            if g != 0 and g != last[i]:
                turns += int(last[i] != 0)
                last[i] = g
    return turns


def lone_run(teeth, t_d, f, rounds, seed, scale_w, scale_f):
    lay_, sites = lone((3, 3, 3), teeth, t_d, f)
    s = lone_lay(sites, seed)
    seen_counts = [s.a[0].tolist()]
    energy = []
    moved = 0
    for _ in range(rounds):
        s1 = step.tick(lay_, s)
        moved += int(bool((s1.rd != s.rd).any()))
        s = s1
        seen_counts.append(s.a[0].tolist())
        energy.append(sum(scale_w * (x - y) ** 2 + scale_f * x * y for x, y in zip(s.a[0].tolist(), s.b[0].tolist())))
    return count_turns(seen_counts), min(energy), max(energy), energy[0], moved


def recurrence(rounds, seed, num, den, scale=10**30):
    """The linear recurrence x+ = 2 x - x- - (num / den) x from the act's lay, every Node-clock alone, at the scale 10^30,
    every division Rule3's carry: the equation the drive's dial and the teeth both carry, without the act's rounding."""
    _, sites = lone((3, 3, 3), 1, 1, 0)
    s = lone_lay(sites, seed)
    x = [scale * v for v in s.a[0].tolist()]
    xm = [scale * v for v in s.b[0].tolist()]
    seen_counts = [x[:]]
    for _ in range(rounds):
        nxt = [2 * u - w - carry(num * u, den, 0)[0] for u, w in zip(x, xm)]
        xm, x = x, nxt
        seen_counts.append(x[:])
    return count_turns(seen_counts)


ROUNDS_F = 10000
print("(f) the dial in the beat: 27 Mesh-less Node-clocks, one even row, each its own oscillator, 10,000 rounds, the sign")
print("    changes of the counts summed; the drive at T_d 7 and the teeth 6,000, against the same equation carried by the")
print("    teeth 42,000 at T_d 1, the recurrence at the scale 10^30, and the drive at the springs 70 and 77 on each side:")
for label, teeth, t_d, f in (("the drive, teeth 6,000, T_d 7, spring 73", 6000, 7, 73),
                             ("the teeth 42,000, T_d 1, spring 73", 42000, 1, 73),
                             ("the drive, teeth 6,000, T_d 7, spring 70", 6000, 7, 70),
                             ("the drive, teeth 6,000, T_d 7, spring 77", 6000, 7, 77)):
    turns, lo, hi, e0, moved = lone_run(teeth, t_d, f, ROUNDS_F, 51, 42000, 2 * f)
    spread = carry(10**6 * (hi - lo) + carry(e0, 2, 0)[0], e0, 0)[0]
    print(f"  {label}: {turns} sign changes; the drive's tooth moved in {moved} of {ROUNDS_F} rounds; the invariant"
          f" 42000 SUM (a - b)^2 + {2 * f} SUM a b spread over the run {spread} ppm of its first value")
print(f"  the recurrence x+ = 2 x - x- - (146 / 42000) x at the scale 10^30: {recurrence(ROUNDS_F, 51, 146, 42000)} sign"
      " changes")


def twin_run(rounds, seed, residue):
    """The drive act (teeth 6,000, T_d 7, spring 73) and the teeth act (teeth 42,000, T_d 1, spring 73) from one lay, the
    edge tooth laid at `residue` modulo 4 (0 at rest) and the drive's tooth drawn within [0, 7), the teeth act's tooth
    laid 7 s + 4 r_d: the rounds in which some count differs, the first, and the rounds in which the teeth act's tooth is
    7 s + 4 r_d of the drive act's at every Node-clock."""
    la, sites = lone((3, 3, 3), 6000, 7, 73)
    lb, _ = lone((3, 3, 3), 42000, 1, 73)
    pick = generator(seed)
    sa = lone_lay(sites, seed)
    tooth = np.array([[4 * carry(pick(1000), 1000, 0)[1] + residue for _ in range(sites)]], dtype=object)
    rd = np.array([[carry(pick(10**6), 7, 0)[1] for _ in range(sites)]], dtype=object)
    sa = State(sa.a, sa.b, tooth, rd, sa.k)
    sb = State(sa.a.copy(), sa.b.copy(), 7 * tooth + 4 * rd, np.zeros((1, sites), dtype=object), sa.k.copy())
    differ = mapped = 0
    first = None
    for n in range(rounds):
        sa, sb = step.tick(la, sa), step.tick(lb, sb)
        if bool((sa.a != sb.a).any()):
            differ += 1
            first = n + 1 if first is None else first
        mapped += int(bool((7 * sa.r + 4 * sa.rd == sb.r).all()))
    return differ, first, mapped


print("(f2) count for count: the drive act at the teeth 6,000 and T_d 7 against the teeth act at 42,000 and T_d 1, spring")
print("     73 on both, one lay, the teeth act's edge tooth laid 7 s + 4 r_d, 10,000 rounds:")
for label, residue in (("the edge tooth laid a multiple of 4", 0), ("the edge tooth laid at 3 modulo 4", 3)):
    differ, first, mapped = twin_run(ROUNDS_F, 71, residue)
    print(f"  {label}: some count differs in {differ} of {ROUNDS_F} rounds (first: {first}); the teeth act's tooth is 7 s +"
          f" 4 r_d at every Node-clock in {mapped} rounds")

def pushed_layout(t_d, reads):
    """Two even rows at the teeth W, every Mesh at GRIP, each row's own spring, the drive's teeth t_d per row, the kick's 1;
    the metric's push in the books' form on row 0, the momenta in whole turns of the rest dial (step.stress), so the act's
    first drive (on J1 alone) feeds the push it reads: at reads = 1, J5 = 11 sigma_in(1) sigma_out(1), reading a row it
    does not push; at reads = 0, J5 = 11 (sigma_in(0) sigma_out(1) + sigma_out(0) sigma_in(1)), reading the row it
    pushes (the mirror theorem's hypothesis (d) broken), each kept under the mirror's swap of the two momenta."""
    nb = board((3, 3, 3))
    sites = nb.shape[1]
    spokes, meshes = geometry(nb, 3)
    rows = 2
    grip = np.full((rows, 3 * sites), GRIP, dtype=object)
    ones = np.ones((rows, 1), dtype=object)
    drive_teeth = np.array([[t] for t in t_d], dtype=object)
    gearing = Gearing(W * ones, ones.copy(), ones.copy(), drive_teeth, ones.copy())
    click = Click(NONE_I, NONE_I, NONE_O, NONE_I, np.ones((1, 1), dtype=object))
    spokes_n = nb.shape[0]
    sigma_in, sigma_out, unit = spokes_n * rows, (spokes_n + 1) * rows, (spokes_n + 2) * rows
    if reads == 1:  # row 1's two momenta, a row J5 does not push
        legs = ([sigma_in + 1], [sigma_out + 1])
    else:  # row 0's momenta too, the row J5 pushes: in 0 x out 1 + out 0 x in 1, kept under the mirror's swap
        legs = ([sigma_in, sigma_out], [sigma_out + 1, sigma_in + 1])
    terms = len(legs[0])
    push = Plan(np.array(legs[0], dtype=np.intp), np.array(legs[1], dtype=np.intp),
                np.array([unit] * terms, dtype=np.intp), np.array([11] * terms, dtype=object),
                np.zeros(terms, dtype=np.intp))
    springs = plan_of([(3 * 10**4, (0, 0, UNIT, UNIT)), (2 * 10**4, (1, 1, UNIT, UNIT))])
    parts = [nb, spokes, meshes, grip, gearing, springs, UNREAD, UNREAD, click, push]
    parts += [NOPLAN] * (len(Layout._fields) - len(parts))
    return Layout(*parts), sites


def pushed_lay(sites, t_d, seed):
    pick = generator(seed)
    a = np.array([[pick(5000) for _ in range(sites)] for _ in range(2)], dtype=object)
    b = np.array([[a[r, i] - pick(40) for i in range(sites)] for r in range(2)], dtype=object)
    tooth = np.array([[pick(W) for _ in range(sites)] for _ in range(2)], dtype=object)
    rd = np.array([[carry(pick(10**6), t_d[r], 0)[1] for _ in range(sites)] for r in range(2)], dtype=object)
    return State(a, b, tooth, rd, np.zeros((1, sites), dtype=object))


def pushed_run(t_d, reads, rounds, seed):
    lay_, sites = pushed_layout(t_d, reads)
    start = pushed_lay(sites, t_d, seed)
    s = start
    j5_rounds = moved = 0
    for _ in range(rounds):
        force, j1 = step.sources(lay_, s.a)
        first = np.array([[carry(x, t, rd)[0] for x, rd in zip(row, rds)]
                          for row, rds, t in zip(j1.tolist(), s.rd.tolist(), t_d)], dtype=object)
        j5 = step.stress(lay_, s, step.driven(lay_.gearing, force, step.kick(lay_.gearing, first)))
        j5_rounds += int(bool((j5[0] != 0).any()))
        s1 = step.tick(lay_, s)
        moved += int(bool((s1.rd[0] != s.rd[0]).any()))
        s = s1
        if max(abs(x) for x in s.a.ravel().tolist()) > 10**12:  # a runaway, read from outside, stops the run
            return f"no, ran away by round {_ + 1}", j5_rounds, moved
    for _ in range(rounds):
        s = step.untick(lay_, s)
    back = all(bool((x == y).all()) for x, y in zip(s, start))
    return back, j5_rounds, moved


print("(g) the drive inside the act's two passes: the metric's push J5 (the books' form) reads a row's momenta after the")
print("    first drive, on J1 alone; 400 rounds out and 400 back by untick, cube of 3, two even rows, J5 on row 0:")
for label, t_d, reads in (("J5 reads row 1, which it does not push, T_d 7 and 7", (7, 7), 1),
                          ("J5 reads row 1, T_d 7 on row 0 and 1 on row 1", (7, 1), 1),
                          ("J5 reads row 1, T_d 1 and 1", (1, 1), 1),
                          ("J5 reads row 0's momenta too, the row it pushes, T_d 7 and 7", (7, 7), 0),
                          ("J5 reads row 0's momenta too, the row it pushes, T_d 1 and 1", (1, 1), 0)):
    back, j5_rounds, moved = pushed_run(t_d, reads, 400, 61)
    print(f"  {label}: J5 not 0 in {j5_rounds} of 400 rounds; row 0's drive tooth moved in {moved}; the start returned"
          f" bit for bit: {back}")

print("(h) the carry's three identities behind the mirror and the 24, at every T_d from 1 to 11, J from -60 to 60 and r_d")
print("    within [0, T_d), carry(J, T_d, r_d) = (q, r_d+):")
flips = signs = turns = cases = 0
for t in range(1, 12):
    for j in range(-60, 61):
        for r in range(t):
            q, r1 = carry(j, t, r)
            cases += 1
            flips += int(carry(j, t, t - 1 - r1) == (q, t - 1 - r))  # time's reversal on an even row
            signs += int(carry(-j, t, r1) == (-q, r))  # time's reversal on an odd row
            turns += int(carry(-j, t, t - 1 - r) == (-q, t - 1 - r1))  # a turn of the 24 that negates the row
print(f"  carry(J, T_d, T_d - 1 - r_d+) = (q, T_d - 1 - r_d) in {flips} of {cases}; carry(-J, T_d, r_d+) = (-q, r_d) in"
      f" {signs} of {cases}; carry(-J, T_d, T_d - 1 - r_d) = (-q, T_d - 1 - r_d+) in {turns} of {cases}")
