"""G3's eighth text: the coupling family's held hand still at the bottom of a hat, on the act the night builds.

Whole numbers alone, every division Rule3's carry: no float, root, logarithm, exponential or search, no function of
the turn's arc, and no state laid by one. The act is node-live's (939fa65a7): each gear's momentum carried on the edge
between its two slots and split at the next edge's dial, W (a+ - 2 a + b) = push at constant teeth.

The law (the frame's hostile mathematician's direction, "a whole-number quartic on k with the unit"; Big Pic's
quaternion lead, #2187 6530683608 item 11): the held train's rows k_a, their norm |k|^2 = SUM_a k_a^2, and

    V = hat (|k|^2 - n)^2,   n = key^2: the hand's rest at one key,

laid as monomials of J's potential by contract.pushes, every leg pushed by minus the factor times the other three:
(hat; a, a, a, a) on every held row, (2 hat; a, a, b, b) for a < b, and (-2 hat n; a, a, unit, unit) on every held row.
The push on row a is -4 hat (|k|^2 - n) k_a, 0 exactly wherever |k|^2 = n. A tied train x ties to the hand by
(tie; x, x, a, a) over the held rows, its spring 2 tie |k|^2 read from the hand. The strengths are the probe's,
CHOSEN: key 3125 = 5^5, hat 1, W = 2,000 n (the size's beat, 8 hat n / W = 1/250), tie 3 (the tied spring
2 tie n / W = 3/1,000), the held hand's grip W/6 on each Mesh and the tied train's W/100.

(a) the law's pushes against -4 hat (|k|^2 - n) k_a at whole points, and 0 at the rests;
(b) the rest: the hand laid still at whole rests of |k|^2 = n, alike and scattered, with and without its Meshes;
(c) the norm the law picks: laid off its rest the hand swings about it at the size's beat (counted against the exact
    linear recurrence); laid near the top it swings about n too; with no hat it stands where the seed laid it;
(d) the weight: the still hand's energy, kinetic and potential, at every Node-clock;
(e) the angle: a small turn laid along a ring travels as a massless wave with the Meshes, and stands without them;
(f) the tie: the tied train's beat from the hand's rest; the hand answers it; against the unit spring with no hand;
(g) a push across k: the hand laid turning; the tied beat beside (f)'s;
(h) the run back: 500 rounds out and back with the hat, the tie, light and every Mesh, bit for bit;
(i) the 24's A2 sign: the act and the odd turn's flip of the A2 row, every round, the twisted and the plain tooth;
(j) the same law on four rows, the quaternion: rests by products of whole quaternions, the size, three angles;
(k) the frame's unit key: n = 1, the hand at (1, 0) under the same tied wave at the same beats.

Usage: python3 -I g3_hat.py <src of node-live at 939fa65a7>
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import pushes  # noqa: E402
from tensor24.engine.state import Click, Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402

KEY = 5**5
N = KEY * KEY
HAT = 1
W = 2000 * N
TIE = 3
UNIT = -1
SCALE = 10**40
MODE = (2, 1, -1, -2, -1, 1)  # the ring's whole mode of period 6: its second difference is minus itself
NONE_I = np.zeros(0, dtype=np.intp)
NONE_O = np.zeros(0, dtype=object)
UNREAD = Read(NONE_I, NONE_O, NONE_I)
NOPLAN = Plan(NONE_I, NONE_I, NONE_I, NONE_O, NONE_I)


def generator(seed):
    """An integer carry sequence: each call gives a whole number within span of 0."""
    state = seed

    def pick(span):
        nonlocal state
        _, state = carry(1103515245 * state + 12345, 2147483648, 0)
        return carry(state, 2 * span + 1, 0)[1] - span

    return pick


def ppm(part, whole):
    return carry(1000000 * part, whole, 0)[0]


def hat_terms(rows, hat, n):
    terms = []
    for i, a in enumerate(rows):
        terms.append((hat, (a, a, a, a)))
        for b in rows[i + 1:]:
            terms.append((2 * hat, (a, a, b, b)))
        terms.append((-2 * hat * n, (a, a, UNIT, UNIT)))
    return terms


def tie_terms(x_rows, held_rows, tie):
    return [(tie, (x, x, a, a)) for x in x_rows for a in held_rows]


def plan_of(terms):
    if not terms:
        return NOPLAN
    factor = np.array([f for f, _ in terms], dtype=object)
    legs = tuple(np.array([leg[i] for _, leg in terms], dtype=np.intp) for i in range(4))
    return pushes(factor, legs)


def layout(shape, grips, terms, teeth=W):
    """The act's layout: one gear row per entry of grips (its grip on every Mesh), every row's teeth at rest, no
    clock read, no grip read, no click term, no metric push and no Mesh term; J's potential the terms given."""
    nb = board(shape)
    sites = nb.shape[1]
    spokes, meshes = geometry(nb, 3)
    rows = len(grips)
    grip = np.zeros((rows, 3 * sites), dtype=object)
    for row, g in enumerate(grips):
        grip[row, :] = g
    ones = np.ones((rows, 1), dtype=object)
    gearing = Gearing(teeth * ones, ones, ones.copy(), ones.copy(), ones.copy())
    click = Click(NONE_I, NONE_I, NONE_O, NONE_I, np.ones((1, 1), dtype=object))
    parts = [nb, spokes, meshes, grip, gearing, plan_of(terms), UNREAD, UNREAD, click, NOPLAN]
    parts += [NOPLAN] * (len(Layout._fields) - len(parts))  # the Mesh plan, where the act has one: no term
    return Layout(*parts), sites


def still(a):
    """The state at rest on the lay a: both slots alike, every tooth 0, no drive and no click carried."""
    rows, sites = a.shape
    zero = np.zeros((rows, sites), dtype=object)
    return State(a.copy(), a.copy(), zero.copy(), zero.copy(), np.zeros((1, sites), dtype=object))


def moving(a, b):
    rows, sites = a.shape
    zero = np.zeros((rows, sites), dtype=object)
    return State(a.copy(), b.copy(), zero.copy(), zero.copy(), np.zeros((1, sites), dtype=object))


def same(s, t):
    return all(bool((x == y).all()) for x, y in zip(s, t))


def norm(a, rows):
    return sum(a[r] * a[r] for r in rows)


def flips(values):
    """Sign changes of a sequence, zeros skipped."""
    count, last = 0, 0
    for v in values:
        sign = (v > 0) - (v < 0)
        if sign and last and sign != last:
            count += 1
        if sign:
            last = sign
    return count


def recurrence(x0, spring, teeth, rounds):
    """The exact linear recurrence teeth (x+ - 2 x + x-) = -spring x from a standing start, at 10^40 its size, carried
    by Rule3: its sign changes over the rounds."""
    prev, now, seen = x0 * SCALE, x0 * SCALE, []
    for _ in range(rounds):
        nxt = 2 * now - prev - carry(spring * now, teeth, 0)[0]
        prev, now = now, nxt
        seen.append(now)
    return flips(seen)


def circle_points():
    """The 44 whole points of |z|^2 = 5^10: (2 + i)^j (2 - i)^(10 - j) times the four units, by products alone."""
    points = []
    for j in range(11):
        re, im = 1, 0
        for _ in range(j):
            re, im = 2 * re - im, re + 2 * im
        for _ in range(10 - j):
            re, im = 2 * re + im, 2 * im - re
        for _ in range(4):
            points.append((re, im))
            re, im = -im, re
    return sorted(set(points))


def qmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


FIVES = ((1, 2, 0, 0), (2, 1, 0, 0), (1, 0, 2, 0), (2, 0, 1, 0), (1, 0, 0, 2), (2, 0, 0, 1),
         (1, -2, 0, 0), (1, 0, -2, 0), (1, 0, 0, -2), (0, 1, 2, 0), (0, 2, 0, 1), (0, 0, 1, 2))


def quaternion_points(count, seed):
    """Whole quaternions of norm 5^10, each a product of ten of norm 5 picked by the carry sequence."""
    pick, points = generator(seed), []
    for _ in range(count):
        q = (1, 0, 0, 0)
        for _ in range(10):
            q = qmul(q, FIVES[pick(5) + 6])
        points.append(q)
    return points


print(f"the probe's strengths, CHOSEN: key {KEY}, n = key^2 = {N}, hat {HAT}, W = 2,000 n = {W}, tie {TIE};")
print(f"  the size's beat 8 hat n / W = 1/{carry(W, 8 * HAT * N, 0)[0]}; the tied spring 2 tie n / W = 3/1000")

# ---- (a) the law's pushes
print("(a) the hat's monomials by contract.pushes, J against -4 hat (|k|^2 - n) k_a:")
for held in ((0, 1), (0, 1, 2, 3)):
    lay_a, sites = layout((6, 6, 6), [0] * len(held), hat_terms(held, HAT, N))
    pick = generator(7 + len(held))
    a = np.array([[pick(2 * KEY) for _ in range(sites)] for _ in held], dtype=object)
    _, j1 = step.sources(lay_a, a)
    want = [-4 * HAT * (norm(a, held) - N) * a[r] for r in held]
    agree = sum(int((j1[r] == want[r]).all()) for r in held)
    pts = circle_points() if len(held) == 2 else quaternion_points(sites, 11)
    rest = np.array([[pts[carry(i, len(pts), 0)[1]][r] for i in range(sites)] for r in range(len(held))], dtype=object)
    _, j0 = step.sources(lay_a, rest)
    zero_at_rest = sum(int((j0[r] == 0).all()) for r in held)
    print(f"  {len(held)} rows: J equals the formula on {agree} of {len(held)} rows at {sites} whole points; at {sites}"
          f" whole rests of |k|^2 = n, J is 0 on {zero_at_rest} of {len(held)} rows")
print(f"  the circle's whole points: {len(circle_points())} (r_2(5^10) = 4 (10 + 1) = 44), each |z|^2 = n:"
      f" {all(x * x + y * y == N for x, y in circle_points())}")

# ---- (b) the rest
print("(b) the rest: the held hand (rows 0, 1) laid still at whole rests, a tied train (row 2) and light (row 3) at 0,"
      " 6 by 6 by 6, 2,000 rounds:")
GH, GX, GL = carry(W, 6, 0)[0], carry(W, 100, 0)[0], carry(W, 6, 0)[0]
terms = hat_terms((0, 1), HAT, N) + tie_terms((2,), (0, 1), TIE)
for label, gh, scatter, hat in (("alike, with Meshes", GH, False, HAT), ("scattered, Mesh-less", 0, True, HAT),
                                ("scattered, with Meshes", GH, True, HAT),
                                ("scattered, with Meshes, a stiffer hat 40", GH, True, 40)):
    lay_b, sites = layout((6, 6, 6), [gh, gh, GX, GL], hat_terms((0, 1), hat, N) + tie_terms((2,), (0, 1), TIE))
    pts = circle_points()
    pick = generator(21)
    a = np.zeros((4, sites), dtype=object)
    for i in range(sites):
        p = pts[pick(21) + 22] if scatter else (KEY, 0)
        a[0, i], a[1, i] = p
    s0 = still(a)
    s, moved, worst, biggest = s0, 0, 0, 0
    for _ in range(2000):
        s1 = step.tick(lay_b, s)
        moved += int(not same(s1, s))
        dev = norm(s1.a, (0, 1)) - N
        worst = max(worst, int(max(abs(x) for x in dev.tolist())))
        biggest = max(biggest, int(max(abs(x) for x in s1.a[:2].ravel().tolist())))
        s = s1
    print(f"  {label}: rounds in which any count or tooth moved {moved} of 2000; |k|^2 - n at most {worst}"
          f" ({ppm(worst, N)} ppm of n); the largest held count {biggest}; the tied train and light stayed at 0:"
          f" {bool((s.a[2:] == 0).all())}")

# ---- (c) the norm the law picks
print("(c) the norm the law picks: the hand laid alike at every Node-clock, off its rest, 2,000 rounds:")
for label, k0, with_hat in (("at key + 31, the hat on", KEY + 31, True), ("at key + 31, no hat", KEY + 31, False),
                            ("near the top, at key / 25, the hat on", carry(KEY, 25, 0)[0], True)):
    lay_c, sites = layout((6, 1, 1), [0, 0], hat_terms((0, 1), HAT, N) if with_hat else [])
    a = np.zeros((2, sites), dtype=object)
    a[0, :] = k0
    s, trace, low, high = still(a), [], None, None
    for _ in range(2000):
        s = step.tick(lay_c, s)
        r2 = int(norm(s.a, (0, 1))[0])
        trace.append(int(s.a[0, 0]) - KEY)
        low = r2 if low is None else min(low, r2)
        high = r2 if high is None else max(high, r2)
    print(f"  {label}: |k|^2 / n within {ppm(low, N)} to {ppm(high, N)} ppm; sign changes of k_0 - key {flips(trace)}")
expected = recurrence(31, 8 * HAT * N, W, 2000)
print(f"  the exact linear recurrence W (d+ - 2 d + d-) = -8 hat n d from d = 31: {expected} sign changes in 2,000"
      f" rounds")

# ---- (d) the weight
print("(d) the weight of the still hand, (b)'s lays at round 2,000 of the Mesh-less run and of the alike run:")
for label, gh, scatter in (("alike", GH, False), ("scattered, Mesh-less", 0, True)):
    lay_d, sites = layout((6, 6, 6), [gh, gh, GX, GL], terms)
    pts, pick = circle_points(), generator(21)
    a = np.zeros((4, sites), dtype=object)
    for i in range(sites):
        a[0, i], a[1, i] = pts[pick(21) + 22] if scatter else (KEY, 0)
    s = still(a)
    for _ in range(2000):
        s = step.tick(lay_d, s)
    kinetic = sum(int(x) for x in (W * (s.a - s.b) * (s.a - s.b)).ravel().tolist())
    potential = sum(int(x) for x in (HAT * (norm(s.a, (0, 1)) - N) ** 2).tolist())
    momenta = sum(abs(int(x)) for x in s.r.ravel().tolist())
    print(f"  {label}: the kinetic sum W (a - b)^2 {kinetic}, the potential sum hat (|k|^2 - n)^2 {potential}, the"
          f" teeth's momenta summed {momenta}")

# ---- (e) the angle
print("(e) the angle: on a ring of 48, k_0 = key everywhere and k_1 = 50 times the period-6 mode, standing, 600 rounds:")
for label, gh in (("with Meshes, grip W/6", GH), ("Mesh-less", 0)):
    lay_e, sites = layout((48, 1, 1), [gh, gh], hat_terms((0, 1), HAT, N))
    a = np.zeros((2, sites), dtype=object)
    a[0, :] = KEY
    for i in range(sites):
        a[1, i] = 50 * MODE[carry(i, 6, 0)[1]]
    s, trace, size = still(a), [], 0
    for _ in range(600):
        s = step.tick(lay_e, s)
        trace.append(int(s.a[1, 0]))
        size = max(size, int(max(abs(x) for x in (norm(s.a, (0, 1)) - N).tolist())))
    print(f"  {label}: sign changes of k_1 at Node-clock 0: {flips(trace)}; k_1 there within {min(trace)} to"
          f" {max(trace)}; |k|^2 - n at most {size} ({ppm(size, N)} ppm)")
print(f"  the massless recurrence W (p+ - 2 p + p-) = -(W/6) p from 100: {recurrence(100, GH, W, 600)} sign changes in"
      f" 600 rounds")

# ---- (f) the tie
print("(f) the tie: on the ring, the hand at (key, 0) with Meshes, the tied train x = 50 times the mode, grip W/100,"
      " 2,000 rounds:")
lay_f, sites = layout((48, 1, 1), [GH, GH, GX], hat_terms((0, 1), HAT, N) + tie_terms((2,), (0, 1), TIE))
lay_u, _ = layout((48, 1, 1), [GH, GH, GX], [(TIE * N, (2, 2, UNIT, UNIT))])
a = np.zeros((3, sites), dtype=object)
a[0, :] = KEY
for i in range(sites):
    a[2, i] = 50 * MODE[carry(i, 6, 0)[1]]
s, u, trace, differ, first, low, high = still(a), still(a), [], 0, None, N, N
for t in range(1, 2001):
    s, u = step.tick(lay_f, s), step.tick(lay_u, u)
    trace.append(int(s.a[2, 0]))
    if not bool((s.a[2] == u.a[2]).all()):
        differ += 1
        first = t if first is None else first
    r2 = norm(s.a, (0, 1)).tolist()
    low, high = min(low, min(r2)), max(high, max(r2))
print(f"  the tied train's sign changes at Node-clock 0: {flips(trace)}; the recurrence with the spring W/100 + 2 tie n:"
      f" {recurrence(100, GX + 2 * TIE * N, W, 2000)}")
print(f"  the hand's |k|^2 - n within {low - N} to {high - N} ({ppm(low - N, N)} to {ppm(high - N, N)} ppm): the hand"
      f" answers the tied train")
print(f"  against the unit spring (tie n; x, x, unit, unit) with no hand: the tied train differs in {differ} of 2000"
      f" rounds, first at round {first}")

# ---- (g) a push across k
print("(g) a push across k: (f)'s lay with the hand turning, b = (key, -25) at every Node-clock, 2,000 rounds:")
b = a.copy()
b[1, :] = -25
s, trace, low, high, turns, last = moving(a, b), [], None, None, 0, 0
for _ in range(2000):
    s = step.tick(lay_f, s)
    trace.append(int(s.a[2, 0]))
    r2 = norm(s.a, (0, 1)).tolist()
    low = min(r2) if low is None else min(low, min(r2))
    high = max(r2) if high is None else max(high, max(r2))
    sign = (s.a[1, 0] > 0) - (s.a[1, 0] < 0)
    if sign and last and sign != last:
        turns += 1
    last = sign or last
print(f"  the hand's k_1 changed sign {turns} times (half turns); |k|^2 - n within {low - N} to {high - N}"
      f" ({ppm(low - N, N)} to {ppm(high - N, N)} ppm); the tied train's sign changes {flips(trace)}, against (f)'s"
      f" still hand above")

# ---- (h) the run back
print("(h) the run back: 6 by 6 by 6, the hand scattered over the circle, the tied train and light laid moving, every"
      " Mesh, 500 rounds out and 500 back:")
lay_h, sites = layout((6, 6, 6), [GH, GH, GX, GL], terms)
pick = generator(5)
pts = circle_points()
a = np.zeros((4, sites), dtype=object)
b = np.zeros((4, sites), dtype=object)
for i in range(sites):
    a[0, i], a[1, i] = pts[pick(21) + 22]
    b[0, i], b[1, i] = a[0, i] + pick(3), a[1, i] + pick(3)
    for row in (2, 3):
        a[row, i] = pick(200)
        b[row, i] = a[row, i] - pick(5)
start = moving(a, b)
s = start
for _ in range(500):
    s = step.tick(lay_h, s)
for _ in range(500):
    s = step.untick(lay_h, s)
print(f"  the start returned bit for bit: {same(s, start)}")

# ---- (i) the 24's A2 sign


def flipped(s, row, twisted):
    a, b, r, rd, k = (x.copy() for x in s)
    a[row], b[row] = -a[row], -b[row]
    r[row] = -1 - r[row] if twisted else -r[row]
    return State(a, b, r, rd, k)


print("(i) the odd turn's flip of the A2 row (row 1): tick(flip s) against flip(tick s), (h)'s lay, 300 rounds:")
for label, twisted in (("the twisted tooth, s -> -1 - s", True), ("the plain tooth, s -> -s", False)):
    s, agree = start, 0
    for _ in range(300):
        agree += int(same(step.tick(lay_h, flipped(s, 1, twisted)), flipped(step.tick(lay_h, s), 1, twisted)))
        s = step.tick(lay_h, s)
    print(f"  {label}: {agree} of 300 rounds commute")

# ---- (j) the quaternion
print("(j) the same law on four rows (rows 0 to 3), the quaternion:")
pts4 = quaternion_points(216, 3)
print(f"  216 products of ten whole quaternions of norm 5: each of norm n: {all(sum(x * x for x in q) == N for q in pts4)};"
      f" distinct {len(set(pts4))}")
lay_j, sites = layout((6, 6, 6), [0, 0, 0, 0], hat_terms((0, 1, 2, 3), HAT, N))
a = np.array([[pts4[i][r] for i in range(sites)] for r in range(4)], dtype=object)
s0 = still(a)
s, moved = s0, 0
for _ in range(500):
    s1 = step.tick(lay_j, s)
    moved += int(not same(s1, s))
    s = s1
print(f"  scattered rests, Mesh-less: rounds in which anything moved {moved} of 500")
lay_j1, sites = layout((6, 1, 1), [0, 0, 0, 0], hat_terms((0, 1, 2, 3), HAT, N))
a = np.zeros((4, sites), dtype=object)
a[0, :] = KEY + 31
s, trace = still(a), []
for _ in range(2000):
    s = step.tick(lay_j1, s)
    trace.append(int(s.a[0, 0]) - KEY)
print(f"  the size laid at key + 31: {flips(trace)} sign changes in 2,000 rounds, (c)'s two rows {expected} by the"
      f" recurrence")
lay_j2, sites = layout((48, 1, 1), [GH] * 4, hat_terms((0, 1, 2, 3), HAT, N))
a = np.zeros((4, sites), dtype=object)
a[0, :] = KEY
for i in range(sites):
    for r in (1, 2, 3):
        a[r, i] = 50 * MODE[carry(i + 2 * r, 6, 0)[1]]
s, traces = still(a), {1: [], 2: [], 3: []}
for _ in range(600):
    s = step.tick(lay_j2, s)
    for r in (1, 2, 3):
        traces[r].append(int(s.a[r, 0]))
print(f"  three angles laid on the ring with Meshes, each the mode shifted: sign changes {flips(traces[1])},"
      f" {flips(traces[2])}, {flips(traces[3])} in 600 rounds; the massless recurrence from the lay's own value at"
      f" Node-clock 0: {recurrence(50 * MODE[2], GH, W, 600)}, {recurrence(50 * MODE[4], GH, W, 600)},"
      f" {recurrence(50 * MODE[0], GH, W, 600)}")

# ---- (k) the unit key
print("(k) the frame's unit key, n = 1: the hand at (1, 0), the same beats (hat 10^6, W = 2,000 hat, tie 3 W / 2,000),"
      " (f)'s tied wave, 2,000 rounds:")
hat1 = 10**6
w1 = 2000 * hat1
tie1 = 3 * carry(w1, 2000, 0)[0]
lay_k, sites = layout((48, 1, 1), [carry(w1, 6, 0)[0], carry(w1, 6, 0)[0], carry(w1, 100, 0)[0]],
                      hat_terms((0, 1), hat1, 1) + tie_terms((2,), (0, 1), tie1), teeth=w1)
a = np.zeros((3, sites), dtype=object)
a[0, :] = 1
for i in range(sites):
    a[2, i] = 50 * MODE[carry(i, 6, 0)[1]]
s, off, top, largest, gone = still(a), 0, 0, 0, None
for t in range(1, 2001):
    s = step.tick(lay_k, s)
    r2 = norm(s.a, (0, 1)).tolist()
    off += int(any(x != 1 for x in r2))
    top += int(any(x == 0 for x in r2))
    largest = max(largest, max(r2))
    if largest > 10**6:
        gone = t
        break
print(f"  rounds with |k|^2 off 1 somewhere {off}; with the hand at the top (k = 0) somewhere {top}; the largest |k|^2"
      f" {largest}; thrown past |k|^2 = 10^6 at round {gone} (the run stops there)")
