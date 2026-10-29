"""Q3, the board near rest: the push small against W, so the fine teeth the draw reads move a few teeth a beat.
Same draw as q3_wait.py part 3 (own fine tooth + one Mesh's digit by the sum carry, sizes (3, 1), hazard 1/4 for a
fresh draw), notches in {-1, 0, 1}, D 1, grip 1, on W 64 and W 4096; 2,000 seeds, 60 beats. Exact integers."""
import sys
from collections import Counter
from fractions import Fraction

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import layout, state, tick  # noqa: E402

from tensor24.algebra.carry import carry  # noqa: E402


def go(c, sizes, room):
    t, _ = carry(c * sum(sizes), room, 0)
    return sizes[0] <= t


sizes, seeds, beats, shape = (3, 1), 2000, 60, (4, 4, 1)
for W in (64, 4096):
    lay = layout(shape, W, spring=1, grip=1)
    n, mesh = 16, int(lay.nb[0, 0])
    h = Fraction(sum(go(c, sizes, W) for c in range(W)), W)
    taus, moved = Counter(), Counter()
    for seed in range(seeds):
        rng = np.random.default_rng(seed)
        a = [int(x) for x in rng.integers(-1, 2, n)]
        b = [int(x) for x in rng.integers(-1, 2, n)]
        r = [int(x) for x in rng.integers(0, W, n)]
        s, first, last = state(a, b, r), None, int(r[0])
        for t in range(1, beats + 1):
            s, _ = tick(lay, s)
            _, step = carry(int(s.r[0, 0]) - last + W // 2, W, 0)
            moved[abs(step - W // 2)] += 1  # how far site 0's fine tooth moved this beat, the short way round
            last = int(s.r[0, 0])
            _, c = carry(s.r[0, 0] + s.r[0, mesh], W, 0)
            if go(int(c), sizes, W) and first is None:
                first = t
        taus[first] += 1
    chi, row = Fraction(0), []
    for t in range(1, 13):
        e = seeds * h * (1 - h) ** (t - 1)
        chi += (taus[t] - e) ** 2 / e
        row.append(f"{taus[t]}/{float(e):.0f}")
    e_tail, o_tail = seeds * (1 - h) ** 12, seeds - sum(taus[t] for t in range(1, 13))
    chi += (o_tail - e_tail) ** 2 / e_tail
    med = sorted(moved.elements())[len(list(moved.elements())) // 2]
    print(f"W {W}: site 0's fine tooth moves a median {med} teeth a beat (of {W});")
    print(f"   first go at beats 1..12, observed/geometric: {' '.join(row)}; after 12: {o_tail}/{float(e_tail):.0f}; "
          f"never in 60: {taus[None]}; chi-square (12 dof, 5% line 21.0) = {float(chi):.1f}")
