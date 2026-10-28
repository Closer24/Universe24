"""V1 (head, read-only): does the head's one big bang close a circle of its gears, and do its books grow?

Verifier of draft F, law 10 (every bang shows more; time on the board is a circle). Integers only.
The t24 worktree's src is imported read-only, as F7_dark_head.py does; nothing in it is changed.
Per tick it keeps the board's gear state (every train's gears: now, before, fine, dfine) and, apart,
the books (the click counts and the per-Node-clock click record). It reports the least period p and
start t0 with gears(t) == gears(t - p) for every t from t0 to the end, the bangs, and the books at the bangs.
Pass criterion of the run: printed, not asserted; the claims in the report quote these lines.

Usage: python -I V1_head_circle.py QUANTA TICKS
"""

import sys

T24 = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/t24"
sys.path[:0] = [T24 + "/src", T24]

import json  # noqa: E402

from tests.laws import world_of  # noqa: E402
from event_universe.clock import Clock  # noqa: E402

quanta, ticks = int(sys.argv[1]), int(sys.argv[2])
calibre, piece = world_of("world_bang.json")
piece = json.loads(json.dumps(piece))
piece["seed"][0]["quanta"] = quanta


def flat(a):
    return None if a is None else tuple(int(v) for v in a.ravel().tolist())


def gears_of(clock):
    out = []
    for r in clock.trains_:
        for g in r.gears:
            out.append((flat(g.now), flat(g.before), flat(g.fine), flat(g.dfine)))
    return tuple(out)


def books_of(clock):
    return (int(clock.counts.get("births", 0)), int(clock.counts.get("body_clicks", 0)), len(clock.log),
            int(clock.clicks.sum()))


clock = Clock(calibre, piece)
size = 1
for n in clock.size:
    size *= n
G, B, bangs = [gears_of(clock)], [books_of(clock)], []
for _ in range(ticks):
    clock.tick()
    G.append(gears_of(clock))
    B.append(books_of(clock))
    if int(clock.turned_over.sum()) == size:
        bangs.append(clock.ticks)

best = None
for p in range(1, ticks // 2 + 1):
    t0 = None
    for t in range(ticks, p - 1, -1):
        if G[t] == G[t - p]:
            t0 = t
        else:
            break
    if t0 is not None and t0 <= ticks - p:
        best = (p, t0)
        break
print(f"head, {quanta} quanta, {ticks} ticks; whole-board turnovers at {bangs}")
if best:
    p, t0 = best
    print(f"gears(t) == gears(t - {p}) for every t from {t0} to {ticks}: the gears close a circle of {p} ticks")
else:
    print("no exact repeat of the gears with a period up to half the run")
print("books at each bang (births, chimes, log entries, the click record's sum):")
for b in bangs:
    print(f"  tick {b}: {B[b]}")
distinct = len(set(G))
print(f"distinct gear states among the {ticks + 1} read: {distinct}")
