"""UNC2's lawful twin: two lays alike on the board, the edge's one tooth moved on both its sides, read on the clicks.

Usage: python -I unc2_twin.py <tree> <world dir> <rounds> <shift: "half" or "unit">

The world's three files are loaded as the run tool loads them; the busiest own side and site of round 1 (largest |P|
where the key is above 1, at a Node-clock) is the edge side (t, u); its mirror is (u, t). The edge's one tooth is moved
by d (half the key, or one unit): k(t, u) + d and k(u, t) - d, both by Rule3's carry on the dial, so the two teeth still
sum to K - 1 (the 08:5x ruling: a one-side twin is an off-lay state the sides' guard refuses). Both lays run the act.
Read: (a) the board (a, b, r, rd) alike at every round (a board check); (b) the (side, site) whose clicks differ, and at
how many rounds each; (c) the edge's books in the moved lay, q(t, u) + q(u, t) = 0 at every round, and its teeth
summing to K - 1 at every round; (d) on each of the two sides, every window [m, n) of rounds: the largest
|Q_W - Q'_W| and the windows that differ; (e) U1f on each side: Q'_n - Q_n = [k_n >= K - v] - [k_0 >= K - v] with v
the side's own move (d on (t, u), K - d on (u, t)), k_n the first lay's tooth after round n; (f) the rounds with the
first lay's tooth in each side's strip. Whole numbers only; Rule3's carry the one division.
"""

import json
import sys
from pathlib import Path

TREE, WORLD, N, SHIFT = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import run as trun  # noqa: E402

paths = [WORLD.joinpath(n + ".json") for n in ("universe", "piece", "setting")]
universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
shape = piece["shape"]
engine = tmain.ENGINE
kinds, tables, square, lifted = engine.made(trun.star(len(shape)))
loaded, found = trun.load(universe, setting, trun.sites_of(shape), kinds, tables, square, lifted)
assert not found, found
layout = engine.layout(universe, shape, loaded)
s0 = engine.state(*loaded.state)
click = layout.click
key = np.asarray(click.key)
trains = click.weight.shape[-1]
own = trains * trains


def board_of(s):
    """The board's four fields as one text: the counts now and before, the edge tooth, the drive's fine tooth."""
    return json.dumps([np.asarray(f).tolist() for f in (s.a, s.b, s.r, s.rd)])


t1 = step.tick(layout, s0)
p1 = step.passing(click, layout.plan, s0.b, s0.a, t1.a)  # the own sides at every Node-clock
busy = np.abs(p1) * (key[:own] > 1)
side, site = (int(v) for v in np.unravel_index(int(np.argmax(busy)), busy.shape))
t, u = carry(side, trains, 0)
mirror = u * trains + t
kv = int(key.reshape(-1)[side])
half, _ = carry(kv, 2, 0)
d = half if SHIFT == "half" else 1
k1 = np.array(s0.k, dtype=object)
_, k1[side, site] = carry(k1[side, site] + d, kv, 0)
_, k1[mirror, site] = carry(k1[mirror, site] - d, kv, 0)
twin = engine.state(s0.a, s0.b, s0.r, s0.rd, k1)
print(f"world {WORLD.name}, {N} rounds; the edge ({t}, {u}) at site {site}: side {side} and its mirror {mirror}, key "
      f"{kv}, round 1's passing {int(p1[side, site])}; teeth {int(s0.k[side, site])} and {int(s0.k[mirror, site])} "
      f"moved by +{d} and -{d} to {int(k1[side, site])} and {int(k1[mirror, site])}, summing to "
      f"{int(k1[side, site]) + int(k1[mirror, site])} (K - 1 = {kv - 1})")
s, w = s0, twin
alike, books, teeth = 0, 0, 0
where: dict[tuple[int, int], int] = {}
qa = {side: [], mirror: []}
qb = {side: [], mirror: []}
strip = {side: [], mirror: []}
moves = {side: d, mirror: kv - d}
for n in range(N):
    s, cs = step.act(layout, s)
    w, cw = step.act(layout, w)
    alike += int(board_of(s) == board_of(w))
    for a, b in np.argwhere(np.asarray(cs) != np.asarray(cw)):
        where[(int(a), int(b))] = where.get((int(a), int(b)), 0) + 1
    books += int(int(cw[side, site]) + int(cw[mirror, site]) == 0)
    teeth += int(int(w.k[side, site]) + int(w.k[mirror, site]) == kv - 1)
    for x in (side, mirror):
        qa[x].append(int(cs[x, site]))
        qb[x].append(int(cw[x, site]))
        strip[x].append(int(int(s.k[x, site]) >= kv - moves[x]))
print(f"(a) the board alike at {alike} of {N} rounds (a board check)")
print(f"(b) the (side, site) whose clicks differ, with the rounds each: {sorted(where.items())}")
print(f"(c) the moved lay's edge books q(t, u) + q(u, t) = 0 at {books} of {N} rounds; its two teeth summing to K - 1 "
      f"at {teeth} of {N} rounds")
for x in (side, mirror):
    pa, pb = [0], [0]
    for y, z in zip(qa[x], qb[x], strict=True):
        pa.append(pa[-1] + y)
        pb.append(pb[-1] + z)
    diffs = [pb[n] - pa[n] for n in range(N + 1)]
    most = max(diffs) - min(diffs)  # the largest |Q_W - Q'_W| over every window [m, n) is max - min of the differences
    differ = sum(1 for m in range(N) for n in range(m + 1, N + 1) if diffs[n] != diffs[m])
    wrap = int(int(s0.k[x, site]) >= kv - moves[x])
    held = sum(1 for n in range(N) if diffs[n + 1] == strip[x][n] - wrap)
    rounds_apart = sum(1 for y, z in zip(qa[x], qb[x], strict=True) if y != z)
    print(f"(d) side {x}: rounds whose q differ {rounds_apart} of {N}; windows {carry(N * (N + 1), 2, 0)[0]}; the largest "
          f"|Q_W - Q'_W| = {most}; windows that differ: {differ}")
    print(f"(e) side {x}, its move v = {moves[x]}: Q'_n - Q_n = [k_n >= K - v] - [k_0 >= K - v] at {held} of {N} "
          f"rounds (the wrap bracket [k_0 >= K - v] = {wrap})")
    print(f"(f) side {x}: rounds with the first lay's tooth in the strip [{kv - moves[x]}, {kv - 1}]: {sum(strip[x])}")
