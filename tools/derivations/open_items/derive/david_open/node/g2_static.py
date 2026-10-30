"""G2, the static weak field on the slot form: what the clocks and light read, and the post-Newtonian beta and gamma.

Whole numbers alone, on the act (engine/step.py at main 0df0e8385), with the loader's reads laid by hand: every row's
teeth W = rest + the metric family's 00 slot (term 2), every Spoke's grip = the grip + its axis's ii slot at both ends
of its Mesh (term 3). The rows: matter (one), light (one), and the metric family in the square's basis (00; 0x 0y 0z;
xx yy zz; yz zx xy). The metric's slots are laid uniform and still, so no pull and no source moves them.

(a) the clock: matter on a spring s at one Node-clock, the 00 slot laid at 0, 3 and 8 times the rest (W = rest, 4 rest
    and 9 rest): sign changes over 4,000 rounds against the rest's, 1, 1/2 and 1/3 at a small beat (4 sin^2 (w / 2) =
    s / W); the run back bit for bit;
(b) light: a ring of 4 Node-clocks, light laid on the mode (1, 0, -1, 0), the lattice's eigenmode of the pull with
    eigenvalue -2, so 4 sin^2 (w / 2) = 2 grip / W: the sign changes at (W, grip) = (rest, g), (4 rest, g), (rest, 4 g)
    and (4 rest, 4 g), the ii slot laid at 3 g / 2 at each end for 4 g; the same grip / W gives the same count;
(c) the pull's second order, exact on the lattice: with the grips read at both ends, sum over the six Meshes of
    (v_i + v_j)(u_j - u_i) = -(sum of (u_j^2 - u_i^2)) wherever v = -u, on whole fields of a board of 6 by 6 by 6;
(d) the series: N^2 = 1 / (1 + u) with u = -2 Phi + 2 gamma Phi^2 is 1 + 2 Phi + (4 - 2 gamma) Phi^2 to third order,
    read in whole numbers at Phi = -1 / 10^k for k = 3, 4 and 5 and gamma = 0, 1 and 2.

Usage: python3 -I g2_static.py <src of main at 0df0e8385>
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

# (c) the pull's second order on the lattice
nb6 = board((6, 6, 6))
state_seq = 20261030
u = []
for _ in range(nb6.shape[1]):
    _, state_seq = carry(1103515245 * state_seq + 12345, 2147483648, 0)
    u.append(carry(state_seq, 2001, 0)[1] - 1000)
v = [-x for x in u]
holds = all(
    sum((v[i] + v[int(nb6[k, i])]) * (u[int(nb6[k, i])] - u[i]) for k in range(6))
    == -sum(u[int(nb6[k, i])] * u[int(nb6[k, i])] - u[i] * u[i] for k in range(6))
    for i in range(nb6.shape[1])
)
print(f"(c) sum over the six Meshes of (v_i + v_j)(u_j - u_i) = -(sum of u_j^2 - u_i^2) wherever v = -u, at all 216"
      f" Node-clocks of a whole field: {holds}")

# (d) the series in whole numbers: Phi = -1 / q, gamma g2 / 2 (g2 = 0, 2, 4 for gamma 0, 1, 2)
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
print("(d) ((1 + u) G - 1) times q^4 at q = 10^3, 10^4 and 10^5, G = 1 + 2 Phi + (4 - 2 gamma) Phi^2, Phi = -1 / q:"
      " " + "; ".join(rows_d) + " (of order q, so the residual is third order: beta = 2 - gamma)")
