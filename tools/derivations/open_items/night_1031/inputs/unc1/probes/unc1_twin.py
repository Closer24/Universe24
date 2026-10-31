"""UNC1's two-record reading: two lays alike on the board, one click tooth apart, read for the count on every window.

Usage: python -I unc1_twin.py <tree> <world dir> <rounds> <shift: "half" or "unit">

The world's three files are loaded as the run tool loads them (tensor24.main.ENGINE, runner.run's load); the busiest
side and site of round 1 (largest |P| where the key is above 1, MATH1's S5b rule) has its click tooth moved by half the
key or by one unit, by Rule3's carry on the dial; both lays run the act for the rounds. Read: (a) the board (a, b, r,
rd) alike at every round, a board check; (b) the clicks of the two runs, per side and site, at every round: which
differ; (c) on the moved side, every window [m, n) of rounds, 0 <= m < n <= rounds: the two counts Q_W and Q'_W, the
largest |Q_W - Q'_W| (derived: at most 1, by |K Q_W - S_W| <= K - 1 on both and S_W alike), and the windows where they
differ by one; (d) from the birth, Q_n - Q'_n at every round. Whole numbers only; Rule3's carry the one division.
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


def board_of(s):
    """The board's four fields as one text: the counts now and before, the edge tooth, the drive's fine tooth."""
    return json.dumps([np.asarray(f).tolist() for f in (s.a, s.b, s.r, s.rd)])


t1 = step.tick(layout, s0)
p1 = np.concatenate((step.passing(click, layout.plan, s0.b, s0.a, t1.a),
                     step.crossing(click, layout.nb, s0.b, s0.a, t1.a)))
busy = np.abs(p1) * (key > 1)
side, site = (int(v) for v in np.unravel_index(int(np.argmax(busy)), busy.shape))
kv = int(key.reshape(-1)[side])
half, _ = carry(kv, 2, 0)
by = half if SHIFT == "half" else 1
k1 = np.array(s0.k, dtype=object)
_, k1[side, site] = carry(k1[side, site] + by, kv, 0)
twin = engine.state(s0.a, s0.b, s0.r, s0.rd, k1)
print(f"world {WORLD.name}, {N} rounds; side {side}, site {site}, key {kv}, round 1's passing there {int(p1[side, site])}; "
      f"tooth {int(s0.k[side, site])} moved by {by} to {int(k1[side, site])}")
s, w = s0, twin
alike, where = 0, set()
qa, qb = [], []
strip = []  # the first lay's tooth after each round in the moved-into strip [K - by, K - 1]: 1, else 0
for n in range(N):
    s, cs = step.act(layout, s)
    w, cw = step.act(layout, w)
    alike += int(board_of(s) == board_of(w))
    d = np.argwhere(np.asarray(cs) != np.asarray(cw))
    where.update((int(a), int(b)) for a, b in d)
    qa.append(int(cs[side, site]))
    qb.append(int(cw[side, site]))
    strip.append(int(int(s.k[side, site]) >= kv - by))
print(f"(a) the board alike at {alike} of {N} rounds (a board check)")
print(f"(b) the (side, site) whose clicks differ: {sorted(where)}; rounds where the moved side's q differ: "
      f"{sum(1 for x, y in zip(qa, qb, strict=True) if x != y)} of {N}")
# (c) every window
pa, pb = [0], [0]
for x, y in zip(qa, qb, strict=True):
    pa.append(pa[-1] + x)
    pb.append(pb[-1] + y)
most, ones, windows = 0, 0, 0
for m in range(N):
    for n in range(m + 1, N + 1):
        diff = (pa[n] - pa[m]) - (pb[n] - pb[m])
        most = max(most, abs(diff))
        ones += int(diff != 0)
        windows += 1
print(f"(c) windows [m, n) on the moved side: {windows}; largest |Q_W - Q'_W| = {most}; windows that differ: {ones}")
# (d) from the birth
d_n = sorted({pa[n] - pb[n] for n in range(N + 1)})
print(f"(d) Q_n - Q'_n from the birth over the rounds 0 to {N}: the values {d_n}; the whole run's counts {pa[-1]} and "
      f"{pb[-1]}")
print(f"(e) the moved side's tooth at the end: {int(s.k[side, site])} and {int(w.k[side, site])}; their difference "
      f"mod K {carry(int(s.k[side, site]) - int(w.k[side, site]), kv, 0)[1]}, the move {kv - by} or {by} mod K")
# (f) the two-record law, derived: Q'_n - Q_n = [k_n >= K - u], k_n the first lay's tooth after round n, u the move
held = sum(1 for n in range(N) if pb[n + 1] - pa[n + 1] == strip[n])
print(f"(f) Q'_n - Q_n = [k_n >= K - u] at {held} of {N} rounds; rounds with the first lay's tooth in the strip "
      f"[{kv - by}, {kv - 1}]: {sum(strip)}")
_, r0 = carry(int(s0.k[side, site]), 3, 0)
_, rtop = carry(kv - 1, 3, 0)
print(f"(g) the birth mod 3: {r0}; K - 1 mod 3: {rtop}; K mod 3: {carry(kv, 3, 0)[1]}")
