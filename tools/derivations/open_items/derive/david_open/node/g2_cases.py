"""G2's third text, cases built to pass its own words (David's self-check, the owner's word of 16:2x UTC).

(case 1) Postulate 6's own mutant, the head's law (linear in the stretch): N^2 = 1 - c00 / R, on (d3)'s lay (the same two
      wells Ua, Ub from seeds 20261030 and 424242 over 216 Node-clocks, the 00 slot at 4 S U + 2 gamma U^2). Two
      slowdowns compose by their product where H = R (c_a + c_b - c_ab) - c_a c_b is 0 (H / R^2 is N_ab^2 - N_a^2 N_b^2).
      H against -16 (gamma + 1) S^2 Ua Ub - 8 gamma S Ua Ub (Ua + Ub) - 4 gamma^2 Ua^2 Ub^2, at gamma 1 and -1.
(case 2) N2's source ratio with the fast clock: one gear on s = rest div 4, W = (1 + u) rest, sums over whole half beats,
      10^6 x <J00> / <J_ii> at st = rest, kv = s, against 10^6 (1 - u) / (1 + u).
(case 3) A two-part train laid in phase: (f4)'s train with the second row laid at the first's own state (no quarter beat).
(case 4) Frame dragging on the act as built: the 0i slots laid with a turning field, every other row run with and without
      it for 400 rounds; a row that reads the 0i slots would differ.

Whole numbers alone, Rule3's carry for every division; no float, root, log, circular function or search.
Usage: python3 -I g2_cases.py <src of main at 0df0e8385>   (the example files are read from
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
REST = 6 * GRIP
matter_row, light_row, slot00, slot_xx = 0, 1, 2, 6
slot_0x = 3  # the 0i slots: 0x, 0y, 0z
ROWS = 12


def layout(shape, spring):
    nb = board(shape)
    sites = nb.shape[1]
    spokes, meshes = geometry(nb, 3)
    ones = np.ones((ROWS, 1), dtype=object)
    clock = Read(np.full(ROWS, slot00, dtype=np.intp), np.ones(ROWS, dtype=object), np.arange(ROWS, dtype=np.intp))
    stretch = Read(np.array([slot_xx, slot_xx, slot_xx + 1, slot_xx + 1, slot_xx + 2, slot_xx + 2], dtype=np.intp),
                   np.ones(6, dtype=object), np.arange(6, dtype=np.intp))
    if spring:
        plan = pushes(np.array([carry(spring, 2, 0)[0]], dtype=object),
                      tuple(np.array([leg], dtype=np.intp) for leg in (matter_row, matter_row, -1, -1)))
    else:
        plan = Plan(*(np.zeros(0, dtype=np.intp),) * 3, np.zeros(0, dtype=object), np.zeros(0, dtype=np.intp))
    lay = Layout(nb, spokes, meshes, np.full((1, 3 * sites), GRIP, dtype=object),
                 Gearing(REST * ones, ones, ones.copy(), ones.copy()), plan, clock, stretch)
    return lay, sites, nb


def state(sites, rows_laid):
    a = np.zeros((ROWS, sites), dtype=object)
    for row, values in rows_laid.items():
        a[row, :] = values
    teeth_r = carry(REST, 2, 0)[0]
    return State(a, a.copy(), np.full((ROWS, sites), teeth_r, dtype=object), np.zeros((ROWS, sites), dtype=object))


# (case 1) the head's law on (d3)'s lay
def wells(seed, sites):
    out, seq = [], seed
    for _ in range(sites):
        _, seq = carry(1103515245 * seq + 12345, 2147483648, 0)
        out.append(carry(seq, 2001, 0)[1] - 1000)
    return out


UA, UB = wells(20261030, 216), wells(424242, 216)
UAB = [x + y for x, y in zip(UA, UB, strict=True)]
rows12 = []
for gamma in (1, -1):
    cells, largest = [], []
    for big_s, power in ((10**6, 6), (10**9, 9)):
        r_teeth = 4 * big_s * big_s
        c_a, c_b, c_ab = ([4 * big_s * x + 2 * gamma * x * x for x in f] for f in (UA, UB, UAB))
        head = [r_teeth * (c_a[i] + c_b[i] - c_ab[i]) - c_a[i] * c_b[i] for i in range(216)]
        closed = all(head[i] == -16 * (gamma + 1) * big_s * big_s * UA[i] * UB[i]
                     - 8 * gamma * big_s * UA[i] * UB[i] * (UA[i] + UB[i]) - 4 * gamma * gamma * UA[i] ** 2 * UB[i] ** 2
                     for i in range(216))
        largest.append(max(abs(x) for x in head))
        cells.append(f"S = 10^{power}: H its closed form at all 216 {closed}, the largest |H| {largest[-1]}")
    growth = carry(largest[1], largest[0], 0)[0]
    rows12.append(f"gamma {gamma}: " + "; ".join(cells) + f"; the largest |H| grows by {growth} from S = 10^6 to 10^9"
                  + (" (as S^2: second order)" if growth > 10**5 else " (as S: third order)"))
print("(case 1) Postulate 6's mutant, the head's law N^2 = 1 - c00 / R, on (d3)'s lay: " + "; ".join(rows12))


# (case 2) the fast clock's source ratio
def whole_half_beats(seq_run):
    flips = [t for t in range(1, len(seq_run)) if seq_run[t] * seq_run[t - 1] < 0]
    first, last = flips[0], flips[-1]
    kin = sum((seq_run[t] - seq_run[t - 1]) ** 2 + (seq_run[t + 1] - seq_run[t]) ** 2 for t in range(first, last))
    pot = sum(seq_run[t] * seq_run[t] for t in range(first, last))
    return len(flips), kin, pot


rows14 = []
for spring_div in (4, 400):
    spring = carry(REST, spring_div, 0)[0]
    lay_f, sites_f, _ = layout((1, 1, 1), spring)
    for u_num, u_den in ((0, 1), (1, 4), (3, 1)):
        w_teeth = carry(REST * (u_den + u_num), u_den, 0)[0]
        st = state(sites_f, {matter_row: 10**6, slot00: w_teeth - REST})
        run = [int(st.a[matter_row, 0])]
        for _ in range(4000):
            st = step.tick(lay_f, st)
            run.append(int(st.a[matter_row, 0]))
        flips, kin, pot = whole_half_beats(run)
        ratio = carry(10**6 * (REST * kin - spring * pot), spring * pot, 0)[0]
        model = carry(10**6 * (u_den - u_num), u_den + u_num, 0)[0]
        u_text = f"{u_num}" if u_den == 1 else f"{u_num}/{u_den}"
        rows14.append(f"s = rest div {spring_div}, u = {u_text} ({flips} sign changes): {ratio} against {model}")
print("(case 2) N2's 00 source against its ii source, 10^6 x <J00> / <J_ii> over whole half beats in 4,000 rounds, the"
      " fast clock beside the slow: " + "; ".join(rows14))

# (case 3) a two-part train laid in phase, and (f4)'s quarter beat beside it
spring_t = carry(REST, 400, 0)[0]
lay_t, sites_t, _ = layout((1, 1, 1), spring_t)


def beat_range(seqs):
    j00 = []
    for t in range(1, len(seqs[0]) - 1):
        kin = sum((x[t] - x[t - 1]) ** 2 + (x[t + 1] - x[t]) ** 2 for x in seqs)
        pot = sum(x[t] * x[t] for x in seqs)
        j00.append(REST * kin - spring_t * pot)
    mean = carry(sum(j00), len(j00), 0)[0]
    return f"J00 from {carry(1000 * min(j00), mean, 0)[0]} to {carry(1000 * max(j00), mean, 0)[0]} per mille of its mean"


st_one = state(sites_t, {matter_row: 10**6})
seq_one = [int(st_one.a[matter_row, 0])]
for _ in range(4000):
    st_one = step.tick(lay_t, st_one)
    seq_one.append(int(st_one.a[matter_row, 0]))
turns_one = sum(int(seq_one[t] * seq_one[t - 1] < 0) for t in range(2, len(seq_one)))
quarter = carry(4000, 2 * turns_one, 0)[0]
pair_rows = (matter_row, light_row)
pair_plans = [pushes(np.array([carry(spring_t, 2, 0)[0]], dtype=object),
                     tuple(np.array([leg], dtype=np.intp) for leg in (row, row, -1, -1))) for row in pair_rows]
lay_pair = lay_t._replace(plan=Plan(*(np.concatenate(xs) for xs in zip(*pair_plans, strict=True))))
rows15 = []
for name, offset in (("in phase", 0), ("a quarter beat apart", quarter)):
    a_pair = np.zeros((ROWS, sites_t), dtype=object)
    b_pair = np.zeros((ROWS, sites_t), dtype=object)
    a_pair[matter_row, 0], b_pair[matter_row, 0] = 10**6, 10**6
    if offset:
        a_pair[light_row, 0], b_pair[light_row, 0] = seq_one[offset], seq_one[offset - 1]
    else:
        a_pair[light_row, 0], b_pair[light_row, 0] = 10**6, 10**6
    s_pair = State(a_pair, b_pair, np.full((ROWS, sites_t), carry(REST, 2, 0)[0], dtype=object),
                   np.zeros((ROWS, sites_t), dtype=object))
    seqs = [[int(s_pair.b[row, 0]), int(s_pair.a[row, 0])] for row in pair_rows]
    for _ in range(4000):
        s_pair = step.tick(lay_pair, s_pair)
        for seq_row, row in zip(seqs, pair_rows, strict=True):
            seq_row.append(int(s_pair.a[row, 0]))
    rows15.append(f"{name}: {beat_range(seqs)}")
print(f"(case 3) a two-part train on (f)'s spring at W = rest over 4,000 rounds (a quarter beat = {quarter} rounds): "
      + "; ".join(rows15) + f"; one gear alone: {beat_range([[10**6] + seq_one])}")

# (case 4) frame dragging: the 0i slots laid with a turning field on a board of 4 by 4 by 4
lay_b, sites_b, nb_b = layout((4, 4, 4), spring_t)
side = 4
coords = []
for i in range(sites_b):
    rest_i, x = carry(i, side, 0)
    z, y = carry(rest_i, side, 0)
    coords.append((x, y, z))
base = {matter_row: [10**6 * (1 + x + 2 * y + 3 * z) for x, y, z in coords],
        light_row: [10**5 * (x - y) for x, y, z in coords],
        slot00: [10**15 * (x + y + z) for x, y, z in coords]}
spun = dict(base)
spun[slot_0x] = [-10**15 * (2 * y - 3) for x, y, z in coords]  # 0x = -(y - 3/2), doubled: a turning field about z
spun[slot_0x + 1] = [10**15 * (2 * x - 3) for x, y, z in coords]  # 0y = +(x - 3/2), doubled
s_plain, s_spun = state(sites_b, base), state(sites_b, spun)
other = [r for r in range(ROWS) if r not in (slot_0x, slot_0x + 1, slot_0x + 2)]
same, moved_0i = True, False
for _ in range(400):
    s_plain, s_spun = step.tick(lay_b, s_plain), step.tick(lay_b, s_spun)
    for r in other:
        same = same and all(int(p) == int(q) for p, q in zip(s_plain.a[r], s_spun.a[r], strict=True))
        same = same and all(int(p) == int(q) for p, q in zip(s_plain.r[r], s_spun.r[r], strict=True))
moved_0i = any(int(p) != int(q) for p, q in zip(s_plain.a[slot_0x], s_spun.a[slot_0x], strict=True))
print("(case 4) frame dragging on the act as built (every row's teeth read the 00 slot, every Spoke's grip its axis's ii"
      " slot): a turning field on the 0x and 0y slots of a 4 by 4 by 4 board, 400 rounds with and without it: every"
      f" other row's swing and remainder alike at every round {same}; the 0i slots themselves differ {moved_0i}")
