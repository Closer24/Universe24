"""Q2 on the board: the gears' fine teeth under the engine's own tick (tensor24.engine.step.tick, full rate, every
tick a beat). (1) The fine tooth is the remainder of the exact momentum: M = W (a - b) + r, M+ = M + push, every
site, every tick. (2) Over the board's states: the fine teeth of a site enumerated over all of [0, W) at a fixed coarse
state, and of all four sites jointly; is the law of the fine teeth kept uniform tick after tick? Exact integers."""
import itertools
import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import layout, state, tick  # noqa: E402

from tensor24.engine.step import driven, sources  # noqa: E402

W = 7
lay = layout((4, 1, 1), W, spring=1, grip=1)
print("(1) M = W (a - b) + r and M+ = M + push, on a ring of 4, W 7, D 1, grip 1, 40 ticks from a moving state")
s = state([30, -12, 5, 0], [21, -5, 9, 2], [3, 6, 0, 1])
ok = True
for _ in range(40):
    force, j = sources(lay, s)
    push = driven(lay.gearing, force, j * 0 + j)  # T_d = 1: q = J = 0 here, so push = s F
    m = W * (s.a - s.b) + s.r
    s, _ = tick(lay, s)
    ok = ok and bool(((W * (s.a - s.b) + s.r) == m + push).all())
print("   holds at every site and tick:", ok)

print("\n(2a) Site 0's fine tooth over all of [0, 7), the rest of the state fixed; its law at the ticks 1 to 6")
for D, g in [(1, 1), (0, 1), (7, 0), (0, 0)]:
    lay = layout((4, 1, 1), W, spring=D, grip=g)
    laws = []
    for t in range(1, 7):
        cnt = Counter()
        for r0 in range(W):
            s = state([30, -12, 5, 0], [21, -5, 9, 2], [r0, 6, 0, 1])
            for _ in range(t):
                s, _ = tick(lay, s)
            cnt[int(s.r[0, 0])] += 1
        laws.append("U" if len(cnt) == W else f"{len(cnt)}/{W}")
    print(f"   D {D}, grip {g}: residues hit at site 0 per tick (U = all 7, once each): {laws}")

print("\n(2b) All four sites' fine teeth jointly over [0, 7)^4 (2,401 states), D 1, grip 1: the images' count")
lay = layout((4, 1, 1), W, spring=1, grip=1)
starts = list(itertools.product(range(W), repeat=4))
for t in [1, 2, 3, 5, 8, 13]:
    images, marg = Counter(), Counter()
    for rs in starts:
        s = state([30, -12, 5, 0], [21, -5, 9, 2], rs)
        for _ in range(t):
            s, _ = tick(lay, s)
        images[tuple(int(x) for x in s.r[0])] += 1
        marg[int(s.r[0, 0])] += 1
    print(f"   tick {t:2d}: distinct joint fine-teeth images {len(images):4d} of 2401; site 0's law "
          f"{dict(sorted(marg.items()))}")
