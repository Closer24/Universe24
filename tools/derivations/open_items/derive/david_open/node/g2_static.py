"""G2, the static weak field on the slot form: what the clocks and light read, and the post-Newtonian beta and gamma.

Whole numbers alone, on the act (engine/step.py and engine/mesh.py at main 0df0e8385), with the loader's reads laid by
hand: every row's teeth W = rest + the metric family's 00 slot (term 2), every Spoke's grip = the grip + its axis's ii
slot at both ends of its Mesh (term 3). The rows: matter (one), light (one), and the metric family in the square's
basis (00; 0x 0y 0z; xx yy zz; yz zx xy). In (a), (a2) and (b) the metric's slots are laid uniform and still.

(a) the clock: matter on a spring s at one Node-clock, the 00 slot laid at 0, 3 and 8 times the rest (W = rest, 4 rest
    and 9 rest): sign changes over 4,000 rounds, 1, 1/2 and 1/3 at a small beat; the run back bit for bit;
(a2) the reading holds at zero beat: two clocks at one depth (W = 4 rest against rest, 40,000 rounds), the slow one
     (s = rest div 400) and a fast one (s = rest div 4): N from their counts against root(rest / W) = 1/2, and the
     exact reading arcsin(root(s / 4 W)) / arcsin(root(s / 4 rest)) for each, computed in whole numbers;
(b) light: a ring of 4 Node-clocks, light laid on the mode (1, 0, -1, 0), 4 sin^2 (w / 2) = 2 grip / W: the sign
    changes at (W, grip) = (rest, g), (4 rest, g), (rest, 4 g) and (4 rest, 4 g); the same grip / W, the same count;
(c) the second order on the act's own pull (mesh.pull, the grips read at both ends): on a board of 6 by 6 by 6 the 00
    slot laid at 4 S^2 (U / S + (c2 / 2) (U / S)^2) and every ii slot at -(gamma / 2) U g0 with the grip 2 S g0, U a
    whole field: the pull less its first-order part, 8 S^2 g0 Lap U, is exactly the third-order
    -2 gamma^2 g0 SUM (U_i + U_j)^2 (U_j - U_i) at every Node-clock when c2 = gamma, for gamma 0, 1, 2 and S = 10^6,
    10^9; with c2 = gamma + 1 (a mutant) the residual is second order, growing with S; and an ii slot pulled through the
    grips that read it: F = g Lap c + Lap c^2 exactly;
(d) the series, arithmetic alone: N^2 = 1 / (1 + u) with u = -2 Phi + 2 gamma Phi^2 is 1 + 2 Phi + (4 - 2 gamma)
    Phi^2 to third order, at Phi = -1 / 10^k for k = 3, 4, 5 and gamma = 0, 1, 2;
(d2) the exponential clock (Postulate 6's product of slowdowns), arithmetic alone: N^2 = e^(-u) with the same u is
     1 + 2 Phi + (2 - 2 gamma) Phi^2 to third order (beta = 1 - gamma), its series in whole numbers; the guess beta = 1
     at gamma = 1 fails at second order;
(e) the wrapped board: the 00 row's pull summed over every Node-clock of the board is 0 for any fields and grips; a
    source pinned at one Node-clock of a board of 4 by 4 by 4 moves the 00 row's summed momentum by exactly rounds x J,
    so the 00 slot's sum and its least grow, and no static field stands without a notch on the board's mean (term 9);
(f) the source's time terms: one gear on its spring at a fixed swing, N2's 00 source per round, st (sb^2 + sa^2) -
    kv a^2, against its ii source kv a^2: the ratio of their means, and how far each runs per round;
(g) general relativity's static field in isotropic radius (the lattice's own), exact ratios: the lapse N, the scale A,
    light's coordinate speed N / A and the areal radius A r at r = G M / (2 c^2), 2 G M / c^2 and 4 G M / c^2;
(g2) the shadows, exact ratios: the one reading (an ii slot pulled through grips that read it, gamma = 1, section 5)
     has 1 + 2 v = x with x^2 = 1 - 4 G M / (c^2 r), the 00 slot pulled through those grips u = 1 - x, so
     N^2 = 1 / (2 - x) and A^2 = 1 / x; light's impact parameter squared, b^2 = r^2 A^2 / N^2 = r^2 (2 - x) / x, over
     x = 1/100 to 99/100, against general relativity's b^2 = R^3 / (R - 2) over the areal radius R = 201/100 to 10.

Usage: python3 -I g2_static.py <src of main at 0df0e8385>
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import mesh, step  # noqa: E402
from tensor24.engine.contract import pushes  # noqa: E402
from tensor24.engine.state import Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402

GRIP = 15162856759112389 * 1000 * 1000
REST = 6 * GRIP
matter_row, light_row, slot00, slot_xx = 0, 1, 2, 6  # rows: matter, light, the metric's 00 slot, its xx slot (yy, zz follow)
ROWS = 12


def layout(shape, spring):
    nb = board(shape)
    sites = nb.shape[1]
    spokes, meshes = geometry(nb, 3)
    ones = np.ones((ROWS, 1), dtype=object)
    clock = Read(np.full(ROWS, slot00, dtype=np.intp), np.ones(ROWS, dtype=object), np.arange(ROWS, dtype=np.intp))
    stretch = Read(np.array([slot_xx, slot_xx, slot_xx + 1, slot_xx + 1, slot_xx + 2, slot_xx + 2], dtype=np.intp),
                   np.ones(6, dtype=object), np.arange(6, dtype=np.intp))  # each Spoke reads its axis's ii slot
    if spring:
        plan = pushes(np.array([carry(spring, 2, 0)[0]], dtype=object),
                      tuple(np.array([leg], dtype=np.intp) for leg in (matter_row, matter_row, -1, -1)))
    else:
        plan = Plan(*(np.zeros(0, dtype=np.intp),) * 3, np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))
    lay = Layout(nb, spokes, meshes, np.full((1, 3 * sites), GRIP, dtype=object),
                 Gearing(REST * ones, ones, ones.copy(), ones.copy()), plan, clock, stretch)
    return lay, sites


def state(sites, rows_laid):
    a = np.zeros((ROWS, sites), dtype=object)
    for row, values in rows_laid.items():
        a[row, :] = values
    teeth_r = carry(REST, 2, 0)[0]
    return State(a, a.copy(), np.full((ROWS, sites), teeth_r, dtype=object), np.zeros((ROWS, sites), dtype=object))


def sign_changes(lay, s, row, site, rounds=4000):
    changes, last = 0, int(s.a[row, site])
    for _ in range(rounds):
        s = step.tick(lay, s)
        now = int(s.a[row, site])
        changes += int(now * last < 0)
        last = now if now else last
    return changes, s


# (a) the clock
spring = carry(REST, 400, 0)[0]
lay_a, sites_a = layout((1, 1, 1), spring)
counts = []
home_all = True
for times in (1, 4, 9):
    s0 = state(sites_a, {matter_row: 10**6, slot00: (times - 1) * REST})
    n, s_end = sign_changes(lay_a, s0, matter_row, 0)
    back = s_end
    for _ in range(4000):
        back = step.untick(lay_a, back)
    home_all = home_all and all(np.array_equal(x, y) for x, y in zip(back, s0, strict=True))
    counts.append(n)
print(f"(a) the clock, spring s = rest div 400, sign changes in 4,000 rounds at W = rest, 4 rest and 9 rest: {counts}"
      f" (times 1, 2 and 3: {[counts[0], 2 * counts[1], 3 * counts[2]]}); the run back bit for bit: {home_all}")

# (a2) the reading holds at zero beat: a slow clock and a fast one at one depth
SCALE = 10**40


def arctan_inverse(m):
    total, power, j, sign = 0, carry(SCALE, m, 0)[0], 0, 1
    while power:
        total += sign * carry(power, 2 * j + 1, 0)[0]
        power = carry(power, m * m, 0)[0]
        j, sign = j + 1, -sign
    return total


PI = 16 * arctan_inverse(5) - 4 * arctan_inverse(239)


def sine(x):
    total, term, j, sign = 0, x, 0, 1
    while term:
        total += sign * term
        j, sign = j + 1, -sign
        term = carry(carry(term * x, SCALE, 0)[0] * x, SCALE * (2 * j) * (2 * j + 1), 0)[0]
    return total


def half_beat(spring, teeth):
    """The angle w / 2 (times SCALE) with 4 sin^2 (w / 2) = spring / teeth: the largest one in [0, pi / 2] with
    4 teeth sin^2 <= spring, by bisection on the sine's series."""
    lo, hi = 0, carry(PI, 2, 0)[0]
    while hi - lo > 1:
        mid = carry(lo + hi, 2, 0)[0]
        s_mid = sine(mid)
        if 4 * teeth * s_mid * s_mid <= spring * SCALE * SCALE:
            lo = mid
        else:
            hi = mid
    return lo


zero_beat = []
for name, clock_spring in (("slow, s = rest div 400", carry(REST, 400, 0)[0]), ("fast, s = rest div 4", carry(REST, 4, 0)[0])):
    lay_c, sites_c = layout((1, 1, 1), clock_spring)
    shallow, _ = sign_changes(lay_c, state(sites_c, {matter_row: 10**6, slot00: 0}), matter_row, 0, 40000)
    deep, _ = sign_changes(lay_c, state(sites_c, {matter_row: 10**6, slot00: 3 * REST}), matter_row, 0, 40000)
    exact = carry(10**6 * half_beat(clock_spring, 4 * REST), half_beat(clock_spring, REST), 0)[0]
    zero_beat.append(f"{name}: {shallow} and {deep} sign changes at W = rest and 4 rest, N x 10^6 ="
                     f" {carry(10**6 * deep, shallow, 0)[0]}, the exact reading {exact}")
print("(a2) two clocks at one depth over 40,000 rounds, against root(rest / W) = 500000 x 10^-6: " + "; ".join(zero_beat))

# (b) light on a ring of 4
lay_b, sites_b = layout((4, 1, 1), 0)
mode = [10**6, 0, -(10**6), 0]
light = []
for w_times, g_times in ((1, 1), (4, 1), (1, 4), (4, 4)):
    ii_each_end = carry((g_times - 1) * GRIP, 2, 0)[0]
    laid = {light_row: mode, slot00: (w_times - 1) * REST, slot_xx: ii_each_end, slot_xx + 1: ii_each_end, slot_xx + 2: ii_each_end}
    n, _ = sign_changes(lay_b, state(sites_b, laid), light_row, 0)
    light.append((w_times, g_times, n))
print("(b) light on the mode (1, 0, -1, 0), sign changes at site 0 in 4,000 rounds, (W over rest, grip over g): "
      + "; ".join(f"({w}, {gt}) {n}" for w, gt, n in light)
      + f"; the same grip / W gives the same count: {light[0][2] == light[3][2]}")

# (c) the second order on the act's own pull
nb6 = board((6, 6, 6))
sites6 = nb6.shape[1]
spokes6, meshes6 = geometry(nb6, 3)
seq = 20261030
U = []
for _ in range(sites6):
    _, seq = carry(1103515245 * seq + 12345, 2147483648, 0)
    U.append(carry(seq, 2001, 0)[1] - 1000)
lap_u = [sum(U[int(nb6[k, i])] - U[i] for k in range(6)) for i in range(sites6)]
third = [sum((U[int(nb6[k, i])] - U[i]) * (U[i] + U[int(nb6[k, i])]) ** 2 for k in range(6)) for i in range(sites6)]
G0 = 7
reads_ii = Read(np.array([slot_xx, slot_xx, slot_xx + 1, slot_xx + 1, slot_xx + 2, slot_xx + 2], dtype=np.intp),
                np.ones(6, dtype=object), np.arange(6, dtype=np.intp))
no_plan = Plan(*(np.zeros(0, dtype=np.intp),) * 3, np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))
no_read = Read(np.zeros(0, dtype=np.intp), np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))


def field_layout(grip_value):
    return Layout(nb6, spokes6, meshes6, np.full((1, 3 * sites6), grip_value, dtype=object),
                  Gearing(*(np.ones((ROWS, 1), dtype=object),) * 4), no_plan, no_read, reads_ii)


lines = []
for gamma in (0, 1, 2):
    for big_s in (10**6, 10**9):
        for c2, tag in ((gamma, "c2 = gamma"), (gamma + 1, "c2 = gamma + 1")):
            a_f = np.zeros((ROWS, sites6), dtype=object)
            a_f[slot00, :] = [4 * big_s * x + 2 * c2 * x * x for x in U]
            for d in range(3):
                a_f[slot_xx + d, :] = [-gamma * G0 * x for x in U]
            f00 = mesh.pull(field_layout(2 * big_s * G0), a_f)[slot00]
            left = [int(f00[i]) - 8 * big_s * big_s * G0 * lap_u[i] for i in range(sites6)]
            exact3 = all(left[i] == -2 * gamma * gamma * G0 * third[i] for i in range(sites6))
            lines.append(f"gamma {gamma}, S = 10^{len(str(big_s)) - 1}, {tag}: third order exactly {exact3}, the largest"
                         f" residual {max(abs(x) for x in left)}")
print("(c) the act's pull on the 00 row less its first-order part, against -2 gamma^2 g0 SUM (U_i + U_j)^2 (U_j - U_i), at"
      " all 216 Node-clocks: " + "; ".join(lines))
a_f = np.zeros((ROWS, sites6), dtype=object)
for d in range(3):
    a_f[slot_xx + d, :] = [37 * x for x in U]
fxx = mesh.pull(field_layout(10**5), a_f)[slot_xx]
cc = [37 * x for x in U]
ii_exact = all(int(fxx[i]) == 10**5 * sum(cc[int(nb6[k, i])] - cc[i] for k in range(6))
               + sum(cc[int(nb6[k, i])] ** 2 - cc[i] ** 2 for k in range(6)) for i in range(sites6))
print(f"    an ii slot pulled through grips that read it: F = g Lap c + Lap c^2 at all 216, no order dropped: {ii_exact}")

# (d) the series, arithmetic alone: Phi = -1 / q, gamma g2 / 2 (g2 = 0, 2, 4 for gamma 0, 1, 2)
rows_d = []
for g2 in (0, 2, 4):
    scale = []
    for q in (1000, 10000, 100000):
        # u = -2 Phi + 2 gamma Phi^2 = 2 / q + g2 / q^2; N^2 = 1 / (1 + u); the guess G = 1 + 2 Phi + (4 - g2) Phi^2
        # residual (1 + u) G - 1, times q^4: whole, and of order q (third order) if the guess holds
        one_u = q * q + 2 * q + g2  # (1 + u) q^2
        guess = q * q - 2 * q + (4 - g2)  # G q^2
        residual = one_u * guess - q * q * q * q  # ((1 + u) G - 1) q^4
        scale.append(residual)
    rows_d.append(f"gamma {carry(g2, 2, 0)[0]}: {scale}")
print("(d) arithmetic alone: ((1 + u) G - 1) times q^4 at q = 10^3, 10^4 and 10^5, G = 1 + 2 Phi + (4 - 2 gamma) Phi^2, Phi = -1 / q:"
      " " + "; ".join(rows_d) + " (of order q, so the residual is third order: beta = 2 - gamma)")

# (d2) the exponential clock: 6 q^6 (1 - u + u^2 / 2 - u^3 / 6) against 6 q^6 (1 + 2 Phi + (2 - g2) Phi^2), u = U / q^2
rows_e = []
for g2 in (0, 2, 4):
    scale = []
    for q in (1000, 10000, 100000):
        big_u = 2 * q + g2
        series = 6 * q**6 - 6 * q**4 * big_u + 3 * q * q * big_u * big_u - big_u**3
        guess = 6 * q**6 - 12 * q**5 + 6 * (2 - g2) * q**4
        scale.append(series - guess)
    rows_e.append(f"gamma {carry(g2, 2, 0)[0]}: {scale}")
mutant = []
for q in (1000, 10000, 100000):
    big_u = 2 * q + 2
    series = 6 * q**6 - 6 * q**4 * big_u + 3 * q * q * big_u * big_u - big_u**3
    mutant.append(series - (6 * q**6 - 12 * q**5 + 6 * 2 * q**4))
print("(d2) arithmetic alone, the exponential clock N^2 = e^(-u): 6 q^6 (its series to third order less 1 + 2 Phi + (2 - 2"
      " gamma) Phi^2) at q = 10^3, 10^4 and 10^5: " + "; ".join(rows_e) + f" (of order q^3: beta = 1 - gamma); the guess"
      f" beta = 1 at gamma = 1: {mutant} (of order q^4: second order)")

# (e) the wrapped board
gen_seq = 77
a_w = np.zeros((ROWS, sites6), dtype=object)
a_w[slot00, :] = [x * 10**9 + 3 for x in U]
for d in range(3):
    row = []
    for _ in range(sites6):
        _, gen_seq = carry(1103515245 * gen_seq + 12345, 2147483648, 0)
        row.append(carry(gen_seq, 1000, 0)[1])
    a_w[slot_xx + d, :] = row
summed = sum(int(x) for x in mesh.pull(field_layout(10**4), a_w)[slot00])
nb4 = board((4, 4, 4))
sites4 = nb4.shape[1]
spokes4, meshes4 = geometry(nb4, 3)
grips4 = np.full((ROWS, 3 * sites4), GRIP, dtype=object)
grips4[matter_row, :] = 0  # the matter row held still: no grip
J = 3
source = Plan(np.array([matter_row], dtype=np.intp), np.array([5 * ROWS], dtype=np.intp),
              np.array([5 * ROWS], dtype=np.intp), np.array([J], dtype=object), np.array([slot00], dtype=np.intp))
lay4 = Layout(nb4, spokes4, meshes4, grips4, Gearing(REST * np.ones((ROWS, 1), dtype=object),
              *(np.ones((ROWS, 1), dtype=object),) * 3), source, no_read,
              Read(np.array([slot_xx, slot_xx, slot_xx + 1, slot_xx + 1, slot_xx + 2, slot_xx + 2], dtype=np.intp),
                   np.ones(6, dtype=object), np.arange(6, dtype=np.intp)))
a4 = np.zeros((ROWS, sites4), dtype=object)
a4[matter_row, 0] = 10**22
s4 = State(a4, a4.copy(), np.full((ROWS, sites4), carry(REST, 2, 0)[0], dtype=object), np.zeros((ROWS, sites4), dtype=object))


def momentum00(st):
    return sum(REST * (int(x) - int(y)) + int(r) for x, y, r in zip(st.a[slot00], st.b[slot00], st.r[slot00], strict=True))


p_start = momentum00(s4)
marks = []
for t in range(1, 2001):
    s4 = step.tick(lay4, s4)
    if t in (500, 1000, 2000):
        marks.append(f"round {t}: moved by rounds x J exactly {momentum00(s4) - p_start == t * J * 10**22}, the 00 slot's sum"
                     f" {sum(int(x) for x in s4.a[slot00])}, its least {min(int(x) for x in s4.a[slot00])}")
print(f"(e) the wrapped board: the 00 row's pull summed over all 216 Node-clocks, random fields and grips: {summed}; a source"
      f" J = 3 x 10^22 pinned at one Node-clock of 64, the teeth held at the rest: " + "; ".join(marks))

# (f) the source's time terms
lay_t, sites_t = layout((1, 1, 1), carry(REST, 400, 0)[0])
for times in (1, 4):
    st_t = state(sites_t, {matter_row: 10**6, slot00: (times - 1) * REST})
    seq_t = [int(st_t.a[matter_row, 0])]
    for _ in range(4000):
        st_t = step.tick(lay_t, st_t)
        seq_t.append(int(st_t.a[matter_row, 0]))
    strides = [(seq_t[t] - seq_t[t - 1]) ** 2 + (seq_t[t + 1] - seq_t[t]) ** 2 for t in range(1, len(seq_t) - 1)]
    squares = [seq_t[t] * seq_t[t] for t in range(1, len(seq_t) - 1)]
    mean_k = carry(sum(strides), len(strides), 0)[0]
    mean_v = carry(sum(squares), len(squares), 0)[0]
    print(f"(f) one gear on its spring laid at 10^6, W = {times} rest, 4,000 rounds: the strides' squares sb^2 + sa^2 run from"
          f" {carry(1000 * min(strides), mean_k, 0)[0]} to {carry(1000 * max(strides), mean_k, 0)[0]} per mille of their"
          f" mean, the swing's square a^2 from {carry(1000 * min(squares), mean_v, 0)[0]} to"
          f" {carry(1000 * max(squares), mean_v, 0)[0]} per mille of its mean: each source term beats at twice the gear")

# (g) general relativity's static field in isotropic radius r = q G M / c^2, q = 1/2, 2, 4, as whole ratios
rows_g = []
for q_num, q_den in ((1, 2), (2, 1), (4, 1)):
    n_num, n_den = 2 * q_num - q_den, 2 * q_num + q_den  # N = (2 q - 1) / (2 q + 1)
    a_num, a_den = n_den * n_den, 4 * q_num * q_num  # A = ((2 q + 1) / (2 q))^2
    rows_g.append(f"r = {q_num}/{q_den}: N = {n_num}/{n_den}, A = {a_num}/{a_den}, N / A = {n_num * a_den}/{n_den * a_num},"
                  f" A r = {a_num * q_num}/{a_den * q_den} G M / c^2")
print("(g) general relativity's static field in isotropic radius (r in G M / c^2): " + "; ".join(rows_g)
      + "; where 1 + 2 v = 0 with v = gamma Phi, Phi = -1 / (2 gamma), at gamma 1 the radius 2: N / A = 48/125 there;"
      + " at r = 1/2, N = 0 and A = 4: in the act's terms W without bound and the grip g / A^2 = g/16")

# (g2) the shadows: x = p / 100, r = 4 / (1 - x^2), b^2 = r^2 (2 - x) / x = 16 10^8 (200 - p) / (p (10^4 - p^2)^2);
# general relativity: R = m / 100, b^2 = R^3 / (R - 2) = m^3 / (10^4 (m - 200)); each least found by cross-multiplying
least_one = None
for p in range(1, 100):
    b_num, b_den = 16 * 10**8 * (200 - p), p * (10000 - p * p) ** 2
    if least_one is None or b_num * least_one[2] < least_one[1] * b_den:
        least_one = (p, b_num, b_den)
least_gr = None
for m in range(201, 1001):
    b_num, b_den = m * m * m, 10000 * (m - 200)
    if least_gr is None or b_num * least_gr[2] < least_gr[1] * b_den:
        least_gr = (m, b_num, b_den)
p0, one_num, one_den = least_one
m0, gr_num, gr_den = least_gr
print(f"(g2) the shadows: the one reading's least b^2 over x = 1/100 to 99/100 at x = {p0}/100 (r = 16/3 G M / c^2),"
      f" b^2 = 256/3 (G M / c^2)^2 exactly: {one_num * 3 == 256 * one_den}; general relativity's least b^2 = R^3 / (R - 2)"
      f" over R = 201/100 to 10 at R = {m0}/100, b^2 = 27 exactly: {gr_num == 27 * gr_den}; the ratio (256/3) / 27 ="
      f" 256/81 = (16/9)^2: the one reading's shadow 16/9 of general relativity's")

