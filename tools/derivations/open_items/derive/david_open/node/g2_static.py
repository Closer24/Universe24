"""G2, the static weak field on the slot form: what the clocks and light read, and the post-Newtonian beta and gamma.

Whole numbers alone, on the act (engine/step.py and engine/mesh.py at main 0df0e8385), with the loader's reads laid by
hand: every row's teeth W = rest + the metric family's 00 slot (term 2), every Spoke's grip = the grip + its axis's ii
slot at both ends of its Mesh (term 3). The rows: matter (one), light (one), and the metric family in the square's
basis (00; 0x 0y 0z; xx yy zz; yz zx xy). In (a), (a2) and (b) the metric's slots are laid uniform and still.

(a) the clock: matter on a spring s at one Node-clock, the 00 slot laid at 0, 3 and 8 times the rest (W = rest, 4 rest
    and 9 rest): sign changes over 4,000 rounds, 1, 1/2 and 1/3 at a small beat; the run back bit for bit;
(a2) the reading holds at zero beat: two clocks at one depth (W = 4 rest against rest, 40,000 rounds), the slow one
     (s = rest div 400) and a fast one (s = rest div 4): N from their counts, its square N^2 as a fraction against
     rest / W = 1/4 exactly and N against 1/2 exactly; the exact reading for each, the exact linear recurrence
     x+ = 2 x - x- - s x / W run in whole numbers from the act's lay at 10^40 times its swing, every division by carry,
     its sign changes counted over a hundred times the rounds and carried by a hundred into hundredths of the act's
     span; then, at u = 3, the next order N^2 = (1 / (1 + u)) (1 - (s / (12 rest)) u / (1 + u)) beside the exact
     reading's N^2 for each clock, and the depth each reads back, 1 / N^2 - 1, against u: both read the well deeper,
     the fast one more; how far a hundredth of the exact reading's count at 4 rest moves each clock's depth read
     back; and whether deeper than u is resolved, one count fewer at rest and one more at 4 rest still deeper;
(b) light: a ring of 4 Node-clocks, light laid on the mode (1, 0, -1, 0), 4 sin^2 (w / 2) = 2 grip / W: the sign
    changes at (W, grip) = (rest, g), (4 rest, g), (rest, 4 g) and (4 rest, 4 g); the same grip / W, the same count;
(c) the second order on the act's own pull (mesh.pull, the grips read at both ends): on a board of 6 by 6 by 6 the 00
    slot laid at 4 S^2 (U / S + (c2 / 2) (U / S)^2) and every ii slot at -gamma g0 U with the grip 2 S g0 (so
    v = -(gamma / 2) U / S at each end), U a whole field: the pull less its first-order part, 8 S^2 g0 Lap U, is
    exactly the third-order
    -2 gamma^2 g0 SUM (U_i + U_j)^2 (U_j - U_i) at every Node-clock when c2 = gamma, for gamma 0, 1, 2 and S = 10^6,
    10^9; with c2 = gamma + 1 (a mutant) the residual is second order, growing with S; and an ii slot pulled through the
    grips that read it: F = g Lap c + Lap c^2 exactly;
(d) the series, arithmetic alone: N^2 = 1 / (1 + u) with u = -2 Phi + 2 gamma Phi^2 is 1 + 2 Phi + (4 - 2 gamma)
    Phi^2 to third order, at Phi = -1 / 10^k for k = 3, 4, 5 and gamma = 0, 1, 2;
(d2) the exponential of the 00 count, arithmetic alone: N^2 = e^(-u) with the same u is 1 + 2 Phi + (2 - 2 gamma)
     Phi^2 to third order (beta = 1 - gamma), its series in whole numbers; the guess beta = 1 at gamma = 1 fails at
     second order;
(d3) the law's Postulate 6, two slowdowns composing by their product at first post-Newtonian order, on the act's pull
     (the hostile physicist's check, ported): on (c)'s board, grips and laying, at gamma 0, 1, 2 and S = 10^6, 10^9,
     two whole fields stand for two sources' first-order wells, Ua (the U of (c)) and Ub, and Ua + Ub for both; the
     fields of a alone, b alone and both each stand to third order as in (c); the teeth W = R + c00, R = 4 S^2, read
     N^2 = R / W, so N_ab^2 = N_a^2 N_b^2 exactly where the defect D = R W_ab - W_a W_b is 0: D against its closed form
     16 (gamma - 1) S^2 Ua Ub - 8 gamma S Ua Ub (Ua + Ub) - 4 gamma^2 Ua^2 Ub^2 at every Node-clock, its largest |D|,
     and how that grows from S = 10^6 to 10^9 (as S, third order, only at gamma = 1); then, arithmetic alone,
     6 q^3 (e^(u1) - (1 + u)) at Phi = -1 / q, u1 = -2 Phi, u = u1 + (gamma / 2) u1^2: the same 8 at every q only at
     gamma = 1, so there N^2 = e^(-u1) through second order and -ln N adds over the first-order wells;
(d4) arithmetic alone, the preferred-frame parameters with no row reading the 0i slots (the hostile physicist's
     numbers.py (C), ported): the post-Newtonian g_0i = -(1/2) B1 V_i - (1/2) B2 W_i (Will 2014) at 0 for every source,
     both brackets 0, gives alpha_2 = -1 + zeta_1 - 2 xi and alpha_1 = -4 (1 + gamma), checked at every gamma, zeta_1
     and xi of 0, 1 and 2; at gamma = 1 and zeta_1 = xi = 0, alpha_1 = -8 and alpha_2 = -1; general relativity's
     brackets beside;
(e) the wrapped board: the 00 row's pull summed over every Node-clock of the board is 0 for any fields and grips; a
    source pinned at one Node-clock of a board of 4 by 4 by 4 moves the 00 row's summed momentum by exactly rounds x J,
    so the 00 slot's sum and its least grow, and no static field stands without a notch on the board's mean (term 9);
(f) the source's time terms: one gear on its spring at a fixed swing, N2's 00 source per round, st (sb^2 + sa^2) -
    kv a^2, against its ii source kv a^2: how far each runs per round; then counted: the sign changes of the gear and
    of each term less its mean, and the ratio of the two sources' means at N2's strengths st = rest, kv = s, over the
    rounds run (cut mid beat) and over the whole half beats among them;
(f2) N2's 00 source against its ii source with the depth (the two hostile readers' check, ported): one gear on (f)'s
     spring at W = (1 + u) rest, u = 0, 1/100, 1/16, 1/10, 1/8, 1/4, 1/2, 1 and 3, 24,000 rounds, sums from the first
     sign change to the last (whole half beats): 10^6 x <J00> / <J_ii> at st = rest, kv = s against
     10^6 (1 - u) / (1 + u), which the lattice's <sb^2 + sa^2> = <a^2> 2 s / W gives; and the mutant st = W, the
     strides weighed at the gear's own teeth, near 10^6 at every u;
(f3) seven of (f2)'s runs, at u = 0, 1/16, 1/8, 1/4, 1/2, 1 and 3 (the hostile mathematician's table, his
     g2b_source.py, ported): 10^6 J00 / J_ii at N2's fixed strengths st = rest, kv = s, summed over whole half beats,
     against 2 / (1 + u) - 1, and beside it st read at the gear's own teeth, its least and most over the seven;
(f4) the beat's range (the hostile physicist's j00_beat.py, ported): N2's whole 00 source per round,
     st (sb^2 + sa^2) - kv a^2 at st = rest, kv = s, and its ii source kv a^2, least and most per mille of their means
     over 4,000 rounds at W = rest, for (f)'s one gear and for a two-part train, two rows on (f)'s spring, the second
     laid at the first's state a quarter beat on, (f)'s 4,000 rounds over twice its sign changes at W = rest by carry;
(g) general relativity's static field in isotropic radius (the lattice's own), exact ratios: the lapse N, the scale A,
    light's coordinate speed N / A and the areal radius A r at r = G M / (2 c^2), 2 G M / c^2 and 4 G M / c^2;
(g2) the shadows, exact ratios: the one reading (an ii slot pulled through grips that read it, gamma = 1, section 5)
     has 1 + 2 v = x with x^2 = 1 - 4 G M / (c^2 r), the 00 slot pulled through those grips u = 1 - x, so
     N^2 = 1 / (2 - x) and A^2 = 1 / x; light's impact parameter squared, b^2 = r^2 A^2 / N^2 = r^2 (2 - x) / x, over
     x = 1/100 to 99/100, against general relativity's b^2 = R^3 / (R - 2) over the areal radius R = 201/100 to 10;
     then the least by its derivative: d ln b^2 / dx times x (2 - x)(1 - x^2) is -2 (2 x - 1)(x^2 - 2 x - 1), checked
     at every x = p / q with 0 <= p <= q <= 60, where x^2 - 2 x - 1 < 0, so b^2 falls below x = 1/2 and rises above
     it; a finer scan over x = p / 10^4 for the least, and at it r = 4 / (1 - x^2) and the two least b^2's ratio;
     and the one least as polynomials (the hostile mathematician's H1, ported): the numerator of d b^2 / dx from
     b^2 = N / D multiplied out against 16 (1 - x^2) times -2 (2 x - 1)(x^2 - 2 x - 1), coefficient by coefficient,
     and x^2 - 2 x - 1 < 0 on [0, 1] from its value at both ends and its leading sign;
(h) the background (the hostile physicist's estimate, ported): the board's mean resting where term 9's notch holds
    it, u0 = 3 Omega_m (L H0 / c)^2 for the notch's range L, at L = c / H0 and at L = c age / (2 pi), a swing whose
    period is the universe's age; Planck 2018's Omega_m, H0 and age as whole ratios; and gamma / gamma0 at each by G2's
    formula (1 + C0 / rest) / (1 + 2 Cv / g) with C0 / rest = u0 and 2 Cv / g = -u0 (the notch's one range, term 9's
    second text; the first text's trace notch gave -(2/3) u0, printed beside), and with N2's 00 source at that depth
    ((f2)'s (1 - u0) / (1 + u0) of its ii source) also (1 + u0) / (1 - u0).

Usage: python3 -I g2_static.py <src of main at 0df0e8385>   (the example files are read from
<src>/../examples/tensor24)
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import mesh, step  # noqa: E402
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
REST = 6 * GRIP
# rows: matter, light, the metric's 00 slot, its xx slot (yy, zz follow)
matter_row, light_row, slot00, slot_xx = 0, 1, 2, 6
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
SCALE = 10**40  # the exact recurrence's swing over the act's


def exact_changes(spring, teeth, rounds):
    """Sign changes of the exact linear recurrence x+ = 2 x - x- - spring x / teeth in whole numbers, from the act's lay
    (the swing at 10^6 and still, the fine tooth born at rest div 2), the swing taken SCALE times the act's; the
    division by carry with its remainder kept; counted as sign_changes counts the act's."""
    now, before, kept = 10**6 * SCALE, 10**6 * SCALE, carry(REST, 2, 0)[0]
    changes, last = 0, now
    for _ in range(rounds):
        pull, kept = carry(spring * now, teeth, kept)
        now, before = 2 * now - before - pull, now
        changes += int(now * last < 0)
        last = now if now else last
    return changes


zero_beat, exact_counts = [], []
clocks = (("slow, s = rest div 400", carry(REST, 400, 0)[0]), ("fast, s = rest div 4", carry(REST, 4, 0)[0]))
for name, clock_spring in clocks:
    lay_c, sites_c = layout((1, 1, 1), clock_spring)
    shallow, _ = sign_changes(lay_c, state(sites_c, {matter_row: 10**6, slot00: 0}), matter_row, 0, 40000)
    deep, _ = sign_changes(lay_c, state(sites_c, {matter_row: 10**6, slot00: 3 * REST}), matter_row, 0, 40000)
    # the exact reading: the exact recurrence over a hundred times the rounds, its counts carried into hundredths
    rest_count = exact_changes(clock_spring, REST, 4000000)
    deep_count = exact_changes(clock_spring, 4 * REST, 4000000)
    exact_counts.append((name[:4], clock_spring, deep_count, rest_count))
    exact = carry(10**6 * deep_count, rest_count, 0)[0]
    in_parts = (carry(rest_count, 100, 0), carry(deep_count, 100, 0))  # the act's 40,000 rounds' count, in hundredths
    hundredths = " and ".join(f"{whole} {part}/100" for whole, part in in_parts)
    zero_beat.append(f"{name}: {shallow} and {deep} sign changes at W = rest and 4 rest, N x 10^6 ="
                     f" {carry(10**6 * deep, shallow, 0)[0]}, N^2 = {deep * deep}/{shallow * shallow}, the exact"
                     f" reading {exact} (the exact recurrence's {hundredths}, counted over 4,000,000 rounds)")
print("(a2) two clocks at one depth over 40,000 rounds, N^2 against rest / W = 1/4 exactly and N against"
      " 1/2 = 500000 x 10^-6 exactly: " + "; ".join(zero_beat))
# at u = 3: the next order (1 / (1 + u)) (1 - (s / (12 rest)) u / (1 + u)) = (48 rest - 3 s) / (192 rest); the exact
# reading's N^2 = (deep count / rest count)^2, the exact recurrence's counts; the depth read back 1 / N^2 - 1 from each
order_rows, depths, steps, worst = [], [], [], []
for short, clock_spring, deep_count, rest_count in exact_counts:
    next_n2 = carry(10**12 * (48 * REST - 3 * clock_spring), 192 * REST, 0)[0]
    exact_n2 = carry(10**12 * deep_count * deep_count, rest_count * rest_count, 0)[0]
    depth = carry(10**6 * (rest_count * rest_count - deep_count * deep_count), deep_count * deep_count, 0)[0]
    next_depth = carry(10**6 * (144 * REST + 3 * clock_spring), 48 * REST - 3 * clock_spring, 0)[0]
    depths.append(depth)
    fewer = deep_count - 1  # the exact reading's resolution: one count fewer at 4 rest, a hundredth at the act's span
    steps.append(carry(10**6 * (rest_count * rest_count - fewer * fewer), fewer * fewer, 0)[0] - depth)
    # the shallowest reading one count at each depth allows: one count fewer at rest and one more at 4 rest
    low, more = rest_count - 1, deep_count + 1
    worst.append(carry(10**6 * (low * low - more * more), more * more, 0)[0])
    order_rows.append(f"{short}: N^2 by the next order {next_n2}, by the exact reading {exact_n2}, the depth read back"
                      f" {depth} (by the next order {next_depth})")
deeper = all(d > 3 * 10**6 for d in depths)
print("    at u = 3, N^2 x 10^12 by the next order (1 / (1 + u)) (1 - (s / (12 rest)) u / (1 + u)) beside the exact"
      " reading's, and the depth each clock reads back, (1 / N^2 - 1) x 10^6, against u = 3000000: "
      + "; ".join(order_rows) + f"; both read the well deeper than u: {deeper}, the fast clock deeper than the"
      f" slow: {depths[1] > depths[0]}, by {carry(depths[1] - 3 * 10**6, 3, 0)[0]} parts per million of u (the slow"
      f" by {carry(depths[0] - 3 * 10**6, 3, 0)[0]}); a hundredth of the exact reading's count at 4 rest moves its"
      f" depth read back by {steps[0]} (slow) and {steps[1]} (fast), the slow clock's step below its"
      f" {depths[0] - 3 * 10**6} above u: {steps[0] < depths[0] - 3 * 10**6}; one count fewer at rest and one more at"
      f" 4 rest still read {worst[0]} (slow) and {worst[1]} (fast): deeper than u resolved:"
      f" {all(w > 3 * 10**6 for w in worst)}")

# (b) light on a ring of 4
lay_b, sites_b = layout((4, 1, 1), 0)
mode = [10**6, 0, -(10**6), 0]
light = []
for w_times, g_times in ((1, 1), (4, 1), (1, 4), (4, 4)):
    ii_each_end = carry((g_times - 1) * GRIP, 2, 0)[0]
    laid = {light_row: mode, slot00: (w_times - 1) * REST, slot_xx: ii_each_end, slot_xx + 1: ii_each_end,
            slot_xx + 2: ii_each_end}
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
    for big_s, s_power in ((10**6, 6), (10**9, 9)):
        for c2, tag in ((gamma, "c2 = gamma"), (gamma + 1, "c2 = gamma + 1")):
            a_f = np.zeros((ROWS, sites6), dtype=object)
            a_f[slot00, :] = [4 * big_s * x + 2 * c2 * x * x for x in U]
            for d in range(3):
                a_f[slot_xx + d, :] = [-gamma * G0 * x for x in U]
            f00 = mesh.pull(field_layout(2 * big_s * G0), a_f)[slot00]
            left = [int(f00[i]) - 8 * big_s * big_s * G0 * lap_u[i] for i in range(sites6)]
            exact3 = all(left[i] == -2 * gamma * gamma * G0 * third[i] for i in range(sites6))
            lines.append(f"gamma {gamma}, S = 10^{s_power}, {tag}: third order exactly {exact3},"
                         f" the largest residual {max(abs(x) for x in left)}")
print("(c) the act's pull on the 00 row less its first-order part, against -2 gamma^2 g0 SUM (U_i + U_j)^2"
      " (U_j - U_i), at all 216 Node-clocks: " + "; ".join(lines))
a_f = np.zeros((ROWS, sites6), dtype=object)
for d in range(3):
    a_f[slot_xx + d, :] = [37 * x for x in U]
fxx = mesh.pull(field_layout(10**5), a_f)[slot_xx]
cc = [37 * x for x in U]
ii_exact = all(int(fxx[i]) == 10**5 * sum(cc[int(nb6[k, i])] - cc[i] for k in range(6))
               + sum(cc[int(nb6[k, i])] ** 2 - cc[i] ** 2 for k in range(6)) for i in range(sites6))
print("    an ii slot pulled through grips that read it: F = g Lap c + Lap c^2 at all 216, no order dropped:"
      f" {ii_exact}")

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
print("(d) arithmetic alone: ((1 + u) G - 1) times q^4 at q = 10^3, 10^4 and 10^5, G = 1 + 2 Phi + (4 - 2 gamma)"
      " Phi^2, Phi = -1 / q: " + "; ".join(rows_d) + " (of order q, so the residual is third order: beta = 2 - gamma)")

# (d2) the exponential of the 00 count: 6 q^6 (1 - u + u^2 / 2 - u^3 / 6) against 6 q^6 (1 + 2 Phi + (2 - g2) Phi^2),
# u = U / q^2
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
print("(d2) arithmetic alone, the exponential of the 00 count N^2 = e^(-u): 6 q^6 (its series to third order less"
      " 1 + 2 Phi + (2 - 2 gamma) Phi^2) at q = 10^3, 10^4 and 10^5: " + "; ".join(rows_e)
      + f" (of order q^3: beta = 1 - gamma); the guess beta = 1 at gamma = 1: {mutant} (of order q^4: second order)")

# (d3) the law's Postulate 6 on the act: two sources' first-order wells, alone and together, laid as (c) lays U
seq_b = 424242
UB = []
for _ in range(sites6):
    _, seq_b = carry(1103515245 * seq_b + 12345, 2147483648, 0)
    UB.append(carry(seq_b, 2001, 0)[1] - 1000)
UAB = [x + y for x, y in zip(U, UB, strict=True)]


def laplacian6(f):
    return [sum(f[int(nb6[k, i])] - f[i] for k in range(6)) for i in range(sites6)]


def cubic6(f):
    return [sum((f[int(nb6[k, i])] - f[i]) * (f[i] + f[int(nb6[k, i])]) ** 2 for k in range(6)) for i in range(sites6)]


wells = [(f, laplacian6(f), cubic6(f)) for f in (U, UB, UAB)]
p6_rows = []
for gamma in (0, 1, 2):
    cells, largest = [], []
    for big_s, s_power in ((10**6, 6), (10**9, 9)):
        stands, teeth_w = True, []
        for f, lap_f, cub_f in wells:
            a_f = np.zeros((ROWS, sites6), dtype=object)
            a_f[slot00, :] = [4 * big_s * x + 2 * gamma * x * x for x in f]
            for d in range(3):
                a_f[slot_xx + d, :] = [-gamma * G0 * x for x in f]
            f00 = mesh.pull(field_layout(2 * big_s * G0), a_f)[slot00]
            stands = stands and all(
                int(f00[i]) - 8 * big_s * big_s * G0 * lap_f[i] == -2 * gamma * gamma * G0 * cub_f[i]
                for i in range(sites6))
            teeth_w.append([4 * big_s * big_s + int(x) for x in a_f[slot00, :]])  # W = R + c00
        r_teeth = 4 * big_s * big_s
        w_a, w_b, w_ab = teeth_w
        defect = [r_teeth * w_ab[i] - w_a[i] * w_b[i] for i in range(sites6)]
        closed = all(defect[i] == 16 * (gamma - 1) * big_s * big_s * U[i] * UB[i]
                     - 8 * gamma * big_s * U[i] * UB[i] * (U[i] + UB[i]) - 4 * gamma * gamma * U[i] ** 2 * UB[i] ** 2
                     for i in range(sites6))
        largest.append(max(abs(x) for x in defect))
        cells.append(f"S = 10^{s_power}: a alone, b alone and both stand to third order {stands}, D its"
                     f" closed form at all 216 {closed}, the largest |D| {largest[-1]}")
    growth = carry(largest[1], largest[0], 0)[0]
    p6_rows.append(f"    gamma {gamma}: " + "; ".join(cells) + f"; the largest |D| grows by {growth} from S = 10^6 to"
                   + (" 10^9 (as S^2: second order)" if growth > 10**5 else " 10^9 (as S: third order)"))
gaps_all = []
for g2 in (0, 2, 4):
    gaps = []
    for q in (1000, 10000, 100000):
        # u1 = -2 Phi = 2 / q and u = u1 + (gamma / 2) u1^2 = 2 / q + g2 / q^2 (g2 = 2 gamma), each side times 6 q^3
        exp_u1 = 6 * q**3 + 12 * q * q + 12 * q + 8  # e^(u1) to third order: 1 + u1 + u1^2 / 2 + u1^3 / 6
        one_u = 6 * q**3 + 12 * q * q + 6 * g2 * q  # 1 + u
        gaps.append(exp_u1 - one_u)
    gaps_all.append(gaps)
print("(d3) the law's Postulate 6, two slowdowns composing by their product at first post-Newtonian order, on the act's"
      " pull: on (c)'s board, grips and laying (the 00 slot at 4 S U + 2 gamma U^2, every ii slot at -gamma g0 U, the"
      " grip 2 S g0), two sources' first-order wells Ua (the U of (c)) and Ub, and Ua + Ub for both; the teeth"
      " W = R + c00, R = 4 S^2, read N^2 = R / W, so N_ab^2 = N_a^2 N_b^2 exactly where D = R W_ab - W_a W_b is 0; D"
      " against 16 (gamma - 1) S^2 Ua Ub - 8 gamma S Ua Ub (Ua + Ub) - 4 gamma^2 Ua^2 Ub^2:")
for row in p6_rows:
    print(row)
print("    arithmetic alone, 6 q^3 (e^(u1) - (1 + u)) to third order at Phi = -1 / q, u1 = -2 Phi,"
      " u = u1 + (gamma / 2) u1^2, q = 10^3, 10^4 and 10^5: "
      + "; ".join(f"gamma {gamma}: {gaps}" for gamma, gaps in zip((0, 1, 2), gaps_all, strict=True))
      + f"; the same at every q only at gamma 1: {[len(set(g)) == 1 for g in gaps_all] == [False, True, False]}"
      f" (there 1 + u = e^(u1) through second order: N^2 = e^(-u1), and -ln N adds over the first-order wells)")


# (d4) arithmetic alone, the preferred-frame parameters with no row reading the 0i slots (the hostile physicist's
# numbers.py (C), ported): the post-Newtonian g_0i = -(1/2) B1 V_i - (1/2) B2 W_i (Will 2014, Living Rev. Relativ. 17,
# 4), and g_0i = 0 for every source sets both brackets to 0
def brackets(gamma, alpha1, alpha2, zeta1, xi):
    """B1 and B2 of the post-Newtonian g_0i, whole numbers."""
    return 4 * gamma + 3 + alpha1 - alpha2 + zeta1 - 2 * xi, 1 + alpha2 - zeta1 + 2 * xi


def alphas(gamma, zeta1, xi):
    """alpha_1 and alpha_2 with B2 = 0 (solved for alpha_2) and then B1 = 0 (solved for alpha_1)."""
    alpha2 = zeta1 - 2 * xi - 1
    return alpha2 - zeta1 + 2 * xi - (4 * gamma + 3), alpha2


ppn_grid = [(g, z, x) for g in (0, 1, 2) for z in (0, 1, 2) for x in (0, 1, 2)]
ppn_held = all(brackets(g, *alphas(g, z, x), z, x) == (0, 0) and alphas(g, z, x) == (-4 * (1 + g), -1 + z - 2 * x)
               for g, z, x in ppn_grid)
alpha1_one, alpha2_one = alphas(1, 0, 0)
print("(d4) arithmetic alone, the preferred-frame parameters with no row reading the 0i slots: the post-Newtonian"
      " g_0i = -(1/2) B1 V_i - (1/2) B2 W_i (Will 2014), B1 = 4 gamma + 3 + alpha_1 - alpha_2 + zeta_1 - 2 xi and"
      " B2 = 1 + alpha_2 - zeta_1 + 2 xi; g_0i = 0 for every source sets both to 0, so alpha_2 = -1 + zeta_1 - 2 xi and"
      f" alpha_1 = -4 (1 + gamma), at every gamma, zeta_1 and xi of 0, 1 and 2: {ppn_held}; at gamma = 1 and"
      f" zeta_1 = xi = 0: alpha_1 = {alpha1_one}, alpha_2 = {alpha2_one}; general relativity (gamma = 1, every alpha,"
      f" zeta_1 and xi 0): B1 = {brackets(1, 0, 0, 0, 0)[0]}, B2 = {brackets(1, 0, 0, 0, 0)[1]}")

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
s4 = State(a4, a4.copy(), np.full((ROWS, sites4), carry(REST, 2, 0)[0], dtype=object),
           np.zeros((ROWS, sites4), dtype=object))


def momentum00(st):
    return sum(REST * (int(x) - int(y)) + int(r)
               for x, y, r in zip(st.a[slot00], st.b[slot00], st.r[slot00], strict=True))


p_start = momentum00(s4)
marks = []
for t in range(1, 2001):
    s4 = step.tick(lay4, s4)
    if t in (500, 1000, 2000):
        marks.append(f"round {t}: moved by rounds x J exactly {momentum00(s4) - p_start == t * J * 10**22},"
                     f" the 00 slot's sum {sum(int(x) for x in s4.a[slot00])}, its least"
                     f" {min(int(x) for x in s4.a[slot00])}")
print(f"(e) the wrapped board: the 00 row's pull summed over all 216 Node-clocks, random fields and grips: {summed};"
      " a source J = 3 x 10^22 pinned at one Node-clock of 64, the teeth held at the rest: " + "; ".join(marks))


# (f) the source's time terms
def turns(xs):
    """Sign changes along a run of whole numbers, a 0 read through (the last value not 0 carried)."""
    count, last = 0, xs[0]
    for x in xs[1:]:
        count += int(x * last < 0)
        last = x if x else last
    return count


def whole_half_beats(seq_run):
    """From the first sign change of the gear to the last, a whole number of half beats: the count of sign changes,
    and over those rounds the sums of the strides' squares sb^2 + sa^2 and of the swing's square a^2."""
    flips = [t for t in range(1, len(seq_run)) if seq_run[t] * seq_run[t - 1] < 0]
    lo, hi = flips[0], flips[-1]
    kin = sum((seq_run[t] - seq_run[t - 1]) ** 2 + (seq_run[t + 1] - seq_run[t]) ** 2 for t in range(lo, hi))
    pot = sum(seq_run[t] * seq_run[t] for t in range(lo, hi))
    return len(flips), kin, pot


spring_t = carry(REST, 400, 0)[0]
lay_t, sites_t = layout((1, 1, 1), spring_t)
f_runs = {}  # each depth's run and its gear's sign changes, read again in (f4)
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
    print(f"(f) one gear on its spring laid at 10^6, W = {times} rest, 4,000 rounds: the strides' squares sb^2 + sa^2"
          f" run from {carry(1000 * min(strides), mean_k, 0)[0]} to {carry(1000 * max(strides), mean_k, 0)[0]} per"
          f" mille of their mean, the swing's square a^2 from {carry(1000 * min(squares), mean_v, 0)[0]} to"
          f" {carry(1000 * max(squares), mean_v, 0)[0]} per mille of its mean: each source term beats at twice the"
          " gear")
    # counted over the same 3,999 rounds: each term less its mean, kept whole by the factor n
    n_t = len(squares)
    gear_turns = turns(seq_t[1:-1])
    f_runs[times] = (seq_t, gear_turns)
    square_turns = turns([n_t * v - sum(squares) for v in squares])
    stride_turns = turns([n_t * k - sum(strides) for k in strides])
    flips_t, kin_t, pot_t = whole_half_beats(seq_t)
    ratio_run = carry(10**6 * (REST * sum(strides) - spring_t * sum(squares)), spring_t * sum(squares), 0)[0]
    ratio_whole = carry(10**6 * (REST * kin_t - spring_t * pot_t), spring_t * pot_t, 0)[0]
    twice = all(x - 2 * gear_turns in (-1, 0, 1) for x in (square_turns, stride_turns))
    print(f"    counted at W = {times} rest: sign changes of the gear {gear_turns}, of a^2 less its mean"
          f" {square_turns}, of sb^2 + sa^2 less its mean {stride_turns} (twice the gear's to within one: {twice});"
          " N2's strengths"
          f" st = rest and kv = s, 10^6 x <J00> / <J_ii> = {ratio_run} over the 3,999 rounds (cut mid beat),"
          f" {ratio_whole} over the whole half beats among them ({flips_t} sign changes), against"
          f" 10^6 (1 - u) / (1 + u) = {carry(10**6 * (2 - times), times, 0)[0]}")

# (f2) N2's 00 source against its ii source with the depth, on (f)'s gear
f2_rows, fixed_gaps, mutants, f2_by_u = [], [], [], {}
for u_num, u_den in ((0, 1), (1, 100), (1, 16), (1, 10), (1, 8), (1, 4), (1, 2), (1, 1), (3, 1)):
    w_teeth = carry(REST * (u_den + u_num), u_den, 0)[0]
    st_u = state(sites_t, {matter_row: 10**6, slot00: w_teeth - REST})
    seq_u = [int(st_u.a[matter_row, 0])]
    for _ in range(24000):
        st_u = step.tick(lay_t, st_u)
        seq_u.append(int(st_u.a[matter_row, 0]))
    flips_u, kin_u, pot_u = whole_half_beats(seq_u)
    fixed = carry(10**6 * (REST * kin_u - spring_t * pot_u), spring_t * pot_u, 0)[0]  # st = rest
    own = carry(10**6 * (w_teeth * kin_u - spring_t * pot_u), spring_t * pot_u, 0)[0]  # st = W, the gear's own teeth
    model = carry(10**6 * (u_den - u_num), u_den + u_num, 0)[0]  # (1 - u) / (1 + u) = 2 rest / W - 1
    fixed_gaps.append(fixed - model)
    mutants.append(own)
    f2_by_u[(u_num, u_den)] = (fixed, own)  # read again in (f3)
    u_text = f"{u_num}" if u_den == 1 else f"{u_num}/{u_den}"
    f2_rows.append(f"    u = {u_text} ({flips_u} sign changes): st = rest {fixed} against {model}; st = W {own}")
print("(f2) N2's 00 source against its ii source with the depth: one gear on (f)'s spring s = rest div 400, laid at"
      " 10^6, W = (1 + u) rest, 24,000 rounds, sums from the first sign change to the last (whole half beats);"
      " 10^6 x <J00> / <J_ii> at N2's strengths st = rest and kv = s against 10^6 (1 - u) / (1 + u), and the mutant"
      " st = W (the strides weighed at the gear's own teeth):")
for row in f2_rows:
    print(row)
print(f"    st = rest: within {min(fixed_gaps)} to {max(fixed_gaps)} x 10^-6 of (1 - u) / (1 + u) at every u, so J00"
      f" falls as J_ii (1 - 2 u) at first order in the depth; st = W: from {min(mutants)} to {max(mutants)} at every u")

# (f3) seven of (f2)'s runs, at the depths of the hostile mathematician's table (his g2b_source.py, ported): N2's fixed
# strengths against 2 / (1 + u) - 1, and beside it st read at the gear's own teeth
f3_depths = ((0, 1), (1, 16), (1, 8), (1, 4), (1, 2), (1, 1), (3, 1))
f3_rows = []
for u_num, u_den in f3_depths:
    u_text = f"{u_num}" if u_den == 1 else f"{u_num}/{u_den}"
    beside = carry(10**6 * (2 * u_den - (u_den + u_num)), u_den + u_num, 0)[0]  # 2 / (1 + u) - 1
    f3_rows.append(f"u = {u_text} {f2_by_u[(u_num, u_den)][0]} against {beside}")
f3_own = [f2_by_u[depth][1] for depth in f3_depths]
print("(f3) N2's 00 source against its ii source with the depth, seven of (f2)'s runs: one gear at s = rest div 400,"
      " N2's fixed strengths st = rest and kv = s, summed over whole half beats; 10^6 J00 / J_ii against"
      " 2 / (1 + u) - 1: " + "; ".join(f3_rows) + f"; with st read at the gear's own teeth, from {min(f3_own)} to"
      f" {max(f3_own)}")


# (f4) the beat's range (the hostile physicist's j00_beat.py, ported): N2's whole 00 source per round,
# st (sb^2 + sa^2) - kv a^2 at st = rest and kv = s, and its ii source kv a^2, least and most per mille of their means
# over 4,000 rounds at W = rest, for (f)'s one gear and for a two-part train, two rows on (f)'s spring (the second in
# row 1, the light row's place, as j00_beat.py lays it), the second laid at the first's state a quarter beat on
def beat_range(seqs):
    """J00 and J_ii per round, each round with a stride in and a stride out, summed over a train's parts: the least
    and the most of each, per mille of its mean."""
    j00, jii = [], []
    for t in range(1, len(seqs[0]) - 1):
        kin = sum((x[t] - x[t - 1]) ** 2 + (x[t + 1] - x[t]) ** 2 for x in seqs)
        pot = sum(x[t] * x[t] for x in seqs)
        j00.append(REST * kin - spring_t * pot)
        jii.append(spring_t * pot)
    ranges = []
    for xs in (j00, jii):
        mean = carry(sum(xs), len(xs), 0)[0]
        ranges.append(f"from {carry(1000 * min(xs), mean, 0)[0]} to {carry(1000 * max(xs), mean, 0)[0]}")
    return ranges


seq_one, turns_one = f_runs[1]
quarter = carry(4000, 2 * turns_one, 0)[0]  # a quarter beat: (f)'s 4,000 rounds over twice its sign changes
one_part = beat_range([[10**6] + seq_one])  # the lay's before slot, then (f)'s run at W = rest
pair_rows = (matter_row, light_row)
pair_plans = [pushes(np.array([carry(spring_t, 2, 0)[0]], dtype=object),
                     tuple(np.array([leg], dtype=np.intp) for leg in (row, row, -1, -1))) for row in pair_rows]
lay_pair = lay_t._replace(plan=Plan(*(np.concatenate(xs) for xs in zip(*pair_plans, strict=True))))
a_pair = np.zeros((ROWS, sites_t), dtype=object)
b_pair = np.zeros((ROWS, sites_t), dtype=object)
a_pair[matter_row, 0], b_pair[matter_row, 0] = 10**6, 10**6
a_pair[light_row, 0], b_pair[light_row, 0] = seq_one[quarter], seq_one[quarter - 1]
s_pair = State(a_pair, b_pair, np.full((ROWS, sites_t), carry(REST, 2, 0)[0], dtype=object),
               np.zeros((ROWS, sites_t), dtype=object))
pair_seqs = [[int(s_pair.b[row, 0]), int(s_pair.a[row, 0])] for row in pair_rows]
for _ in range(4000):
    s_pair = step.tick(lay_pair, s_pair)
    for seq_row, row in zip(pair_seqs, pair_rows, strict=True):
        seq_row.append(int(s_pair.a[row, 0]))
two_part = beat_range(pair_seqs)
print("(f4) the beat's range at W = rest over 4,000 rounds: N2's whole 00 source per round, st (sb^2 + sa^2) - kv a^2"
      " at st = rest and kv = s, and its ii source kv a^2, least and most per mille of their means: (f)'s one gear,"
      f" J00 {one_part[0]}, J_ii {one_part[1]}; a two-part train, two rows on (f)'s spring, the second laid at the"
      f" first's state a quarter beat on ({quarter} rounds: 4,000 over twice (f)'s {turns_one} sign changes, by carry),"
      f" J00 {two_part[0]}, J_ii {two_part[1]}")

# (g) general relativity's static field in isotropic radius r = q G M / c^2, q = 1/2, 2, 4, as whole ratios
rows_g = []
for q_num, q_den in ((1, 2), (2, 1), (4, 1)):
    n_num, n_den = 2 * q_num - q_den, 2 * q_num + q_den  # N = (2 q - 1) / (2 q + 1)
    a_num, a_den = n_den * n_den, 4 * q_num * q_num  # A = ((2 q + 1) / (2 q))^2
    rows_g.append(f"r = {q_num}/{q_den}: N = {n_num}/{n_den}, A = {a_num}/{a_den},"
                  f" N / A = {n_num * a_den}/{n_den * a_num}, A r = {a_num * q_num}/{a_den * q_den} G M / c^2")
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
      f" b^2 = 256/3 (G M / c^2)^2 exactly: {one_num * 3 == 256 * one_den}; general relativity's least b^2 ="
      f" R^3 / (R - 2) over R = 201/100 to 10 at R = {m0}/100, b^2 = 27 exactly: {gr_num == 27 * gr_den}; the ratio"
      " (256/3) / 27 = 256/81 = (16/9)^2: the one reading's shadow 16/9 of general relativity's")
# the least by its derivative: d ln b^2 / dx = -1 / (2 - x) - 1 / x + 4 x / (1 - x^2); times x (2 - x)(1 - x^2), which
# is above 0 on (0, 1), its numerator -x (1 - x^2) - (2 - x)(1 - x^2) + 4 x^2 (2 - x); at x = p / q both sides times q^3
pairs, factored, below0, signed = 0, True, True, True
for q in range(1, 61):
    for p in range(q + 1):
        numer = -p * (q * q - p * p) - (2 * q - p) * (q * q - p * p) + 4 * p * p * (2 * q - p)
        factored = factored and numer == -2 * (2 * p - q) * (p * p - 2 * p * q - q * q)
        below0 = below0 and p * p - 2 * p * q - q * q < 0
        signed = signed and (numer < 0) == (2 * p < q) and (numer > 0) == (2 * p > q)
        pairs += 1
least_fine = None
for p in range(1, 10000):  # x = p / 10^4: b^2 = 16 (2 10^4 - p) 10^16 / (p (10^8 - p^2)^2)
    b_num, b_den = 16 * (20000 - p) * 10**16, p * (10**8 - p * p) ** 2
    if least_fine is None or b_num * least_fine[2] < least_fine[1] * b_den:
        least_fine = (p, b_num, b_den)
p_fine, fine_num, fine_den = least_fine
two_least = 81 * one_num * gr_den == 256 * one_den * gr_num
print("    the least by its derivative: d ln b^2 / dx times x (2 - x)(1 - x^2) equals -2 (2 x - 1)(x^2 - 2 x - 1) at"
      f" every x = p / q, 0 <= p <= q <= 60 ({pairs} pairs): {factored}; x^2 - 2 x - 1 < 0 at all of them: {below0};"
      f" the numerator below 0 where x < 1/2, 0 at 1/2 and above 0 where x > 1/2: {signed} (with"
      " x (2 - x)(1 - x^2) > 0 on (0, 1), b^2 falls, then rises); the scan over"
      f" x = p / 10^4, p = 1 to 9999: the least at p = {p_fine}, b^2 = 256/3 there: {3 * fine_num == 256 * fine_den},"
      f" r = 4 / (1 - x^2) = 16/3 there: {3 * 4 * 10**8 == 16 * (10**8 - p_fine * p_fine)}; the two least b^2,"
      f" (256/3) / 27 = 256/81 = (16 x 16) / (9 x 9), cross-multiplied: {two_least}")


# the one least as polynomials (the hostile mathematician's H1, ported): b^2 = N / D, the numerator of its derivative
# N' D - N D' multiplied out coefficient by coefficient, and x^2 - 2 x - 1 below 0 on [0, 1] from its two ends and its
# leading sign (a parabola that opens upward is largest at an end of an interval)
def poly_mul(f, g):
    """The product of two polynomials, coefficients from x^0 up, whole numbers."""
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            out[i + j] += a * b
    return out


def poly_sub(f, g):
    """f less g, coefficients from x^0 up."""
    out = [0] * max(len(f), len(g))
    for i, a in enumerate(f):
        out[i] += a
    for i, b in enumerate(g):
        out[i] -= b
    return out


def poly_der(f):
    """The derivative, coefficients from x^0 up: each power times its coefficient."""
    return [i * a for i, a in enumerate(f)][1:]


def poly_at(f, x):
    """The value at a whole x, by Horner's rule."""
    value = 0
    for a in reversed(f):
        value = value * x + a
    return value


num_b2 = [32, -16]  # N = 16 (2 - x)
den_b2 = poly_mul([0, 1], poly_mul([1, 0, -1], [1, 0, -1]))  # D = x (1 - x^2)^2
slope_num = poly_sub(poly_mul(poly_der(num_b2), den_b2), poly_mul(num_b2, poly_der(den_b2)))  # N' D - N D'
quadratic = [-1, -2, 1]  # x^2 - 2 x - 1
factored_num = poly_mul([-2], poly_mul([-1, 2], quadratic))  # -2 (2 x - 1)(x^2 - 2 x - 1)
ends = (poly_at(quadratic, 0), poly_at(quadratic, 1))
below_all = ends[0] < 0 and ends[1] < 0 and quadratic[-1] > 0
print("    the one least as polynomials: b^2 = N / D with N = 16 (2 - x) and D = x (1 - x^2)^2, multiplied out in whole"
      f" numbers; the numerator of d b^2 / dx, N' D - N D', coefficients from x^0 up {slope_num}, equals 16 (1 - x^2)"
      f" times -2 (2 x - 1)(x^2 - 2 x - 1) = {factored_num}: {slope_num == poly_mul([16, 0, -16], factored_num)};"
      f" x^2 - 2 x - 1 is {ends[0]} at x = 0 and {ends[1]} at x = 1, its leading coefficient {quadratic[-1]} above 0,"
      f" so its largest on [0, 1] stands at an end: below 0 on all of [0, 1]: {below_all}; with 16 (1 - x^2) and D^2"
      " above 0 on (0, 1), d b^2 / dx has the sign of 2 x - 1 there: b^2 falls below x = 1/2 and rises above it, the"
      " one least")

# (h) the background. Term 9 rests the board's mean at J_total / (2 f9) with the range L, L^2 = grip / (2 f9) in Meshes
# squared, so u0 = J L^2 / (grip rest); the static field's own scale, grip rest Lap u = -J with u = -2 Phi, gives
# J / (grip rest) = 8 pi G rho / c^2, and rho = Omega_m 3 H0^2 / (8 pi G): u0 = 3 Omega_m (L H0 / c)^2. The trace
# on one range, (f9 over 3) tr^2 as term 9's second text lays it, holds each ii slot at Cv = J_ii over (2 f9) with
# J_ii = -(g over (2 rest)) J00 (the CHOSEN strength, gamma0 = 1), so 2 Cv over g = -u0, condition (i) kept by the rest;
# the first text's (f9 over 2) tr^2 gave -(2/3) u0. Constants and their sources:
C_LIGHT = 299792458  # m / s, exact (the SI metre)
AU = 149597870700  # m, exact (IAU 2012 Resolution B2); the parsec is 648000 / pi au (IAU 2015 Resolution B2)
YEAR = 31557600  # s, the Julian year (IAU)
H0_TENTHS = 674  # km/s per Mpc in tenths, so 674 x 100 m/s per Mpc (Planck 2018 results VI, A&A 641, A6: 674 +- 5)
OMEGA_M = 315  # in thousandths (Planck 2018 results VI: 315 +- 7)
AGE_MYR = 13787  # Myr (Planck 2018 results VI: 13787 +- 20)
# L H0 / c at L = c age / (2 pi) is H0 age / (2 pi); H0 = 67400 pi / (648000 10^6 AU) per second, so pi cancels:
# H0 age / (2 pi) = 67400 AGE_MYR 10^6 YEAR / (2 648000 10^6 AU), a whole ratio
x_num, x_den = H0_TENTHS * 100 * AGE_MYR * YEAR, 2 * 648000 * AU
background = []
for name, l_num, l_den in (("L = c / H0", 1, 1), ("L = c age / (2 pi)", x_num, x_den)):
    big_a, big_b = 3 * OMEGA_M * l_num * l_num, 1000 * l_den * l_den  # u0 = big_a / big_b
    mpc = carry(C_LIGHT * l_num, H0_TENTHS * 100 * l_den, 0)[0]  # L in Mpc: (c / H0) (L H0 / c)
    page = carry(10**6 * (big_b + big_a), big_b - big_a, 0)[0]  # (1 + u0) over (1 - u0)
    with_n2 = carry(10**6 * (big_b + big_a) * (big_b + big_a), (big_b - big_a) * (big_b - big_a), 0)[0]
    first = carry(10**6 * 3 * (big_b + big_a), 3 * big_b - 2 * big_a, 0)[0]  # the first text's trace notch
    squared = carry(10**6 * l_num * l_num, l_den * l_den, 0)[0]
    background.append(f"at {name} = {mpc} Mpc: (L H0 / c)^2 x 10^6 = {squared},"
                      f" u0 x 10^6 = {carry(10**6 * big_a, big_b, 0)[0]}, gamma / gamma0 x 10^6 by G2's formula {page},"
                      f" with N2's 00 source also {with_n2} (the first text's trace notch {first})")
print("(h) the background, the board's mean resting where term 9's notch holds it: u0 = 3 Omega_m (L H0 / c)^2 for"
      " the notch's range L, Omega_m = 315/1000, H0 = 674/10 km/s/Mpc, the age 13787 Myr (Planck 2018); gamma / gamma0"
      " by G2's formula (1 + C0 / rest) / (1 + 2 Cv / g) = (1 + u0) / (1 - u0), the ii slots held by the notch's one"
      " range, and with N2's 00 source at that depth ((f2)) times (1 + u0) / (1 - u0) again: " + "; ".join(background))
