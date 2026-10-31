"""The tie's residual, weighed for ALG1 (the owner's ask of 08:0x UTC through the Boss's answer: does the coupling
complex close everything?). The split books each coupling's pair exchange on its edge; what no edge carries is the
sum of a coupling's works over its clocks, w_1 + w_2. Every booking through the cells of a complex sums to 0 over the
clocks (each edge's two ends cancel, and a higher cell's quanta reach no clock, as d d = 0), so a coupling whose works
do not sum to an exact difference cannot be booked on any cell. This reads, on the click world, per Node-clock:
  - the two-leg terms: their summed work against the staggered energy F = f (x_next y_now + x_now y_next), round by
    round, so that the sum of w_1 + w_2 over the rounds is - (F at the end - F at the start) exactly, or not;
  - the tie groups (four value legs on the held and the tied train): their summed work over the rounds, against the
    tie's own potential c p (|rho|^2 - n) at the start and the end, in the edge dial's keys.
Whole numbers and Rule3's carry alone.

Usage: python3 -I tieresid.py <src> <world> <rounds>
"""
import sys

src, world_dir, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path.insert(0, src)
sys.path.insert(0, ".")
import edgeclick as E  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402

universe, shape, held, lay, s, world = E.load_world(src, world_dir)
rows, sites = s.a.shape
import david_split as DS  # noqa: E402

value = DS.value


def prod(vs):
    out = 1
    for v in vs:
        out *= v
    return out

key = int(lay.click.key[0, 0])
dial = 3 * key


def staggered(a, a1):
    tot = 0
    for f, legs in world.two:
        vals = [h for h in legs if h != DS.UNIT]
        x, y = vals[0], vals[1]
        tot += f * (a1[x] * a[y] + a[x] * a1[y])
    return tot


def tie_energy(a, n):
    tot = 0
    for c, tied in world.groups:
        p = prod(a[h] for h in tied)
        tot += c * p * (sum(a[r] * a[r] for r in world.held_rows) - n)
    return tot


n0 = 0
two_sum, tie_sum, f_first, f_last, v_first, v_last = [0] * sites, [0] * sites, [None] * sites, [0] * sites, [None] * sites, [0] * sites
tie_max = [0] * sites
for t in range(rounds):
    s1, _ = step.act(lay, s)
    for x in range(sites):
        b = [int(s.b[r, x]) for r in range(rows)]
        a = [int(s.a[r, x]) for r in range(rows)]
        a1 = [int(s1.a[r, x]) for r in range(rows)]
        for f, legs in world.two:
            w = world.work(legs, f, b, a, a1)
            two_sum[x] += sum(w.values())
        for c, tied in world.groups:
            w_held, w_tied = world.excursion_work(c, tied, n0, b, a, a1)
            tie_sum[x] += w_held + w_tied
        tie_max[x] = max(tie_max[x], abs(tie_sum[x]))
        F_prev = staggered(b, a)
        if f_first[x] is None:
            f_first[x] = F_prev
            v_first[x] = tie_energy(a, n0)
        f_last[x] = staggered(a, a1)
        v_last[x] = tie_energy(a1, n0)
    s = s1

exact = sum(1 for x in range(sites) if two_sum[x] == -(f_last[x] - f_first[x]))
print(f"{world_dir}, {rounds} rounds, {sites} Node-clocks, {len(world.two)} two-leg terms and {len(world.groups)} tie groups"
      f" a Node-clock; the edge dial {dial}")
print(f"two-leg terms: their summed work over the rounds is - (F at the end - F at the start) exactly at {exact} of"
      f" {sites} Node-clocks")
worst = max(range(sites), key=lambda x: tie_max[x])
keys_max, _ = carry(tie_max[worst], dial, 0)
keys_end, _ = carry(abs(tie_sum[worst]), dial, 0)
dv = v_last[worst] - v_first[worst]
print(f"the tie groups: the largest summed work at any round, {tie_max[worst]} ({keys_max} edge keys), at Node-clock"
      f" {worst}; at the end {tie_sum[worst]} ({keys_end} keys) against the tie's own potential's change {dv}")
