"""V5 (verifier A): what the head's clicks do to the charge, read at the state the click acts on; and F3 at a due <= 0.

(a) Every unspringing: the unwound hand's sweeps at its two ends on the board the click unwinds (after the step
    and the turnover), against the same ends at the tick's start (the draft's reading), and the hand's total
    plain charge before and after the click.
(b) Every fitting: the fitted hands' sweeps at the two ends before and after, the charge moved.
(c) Every take the head reads at going 1 with windings <= 0 (the remainder holds the due): the head writes 0;
    F3's ladder as written, from ceil(D M / P), with my own window numerator (hands.wind's form, before its carry).
argv: world file, ticks.
"""
import sys
from collections import Counter
from pathlib import Path

S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
sys.path[:0] = [S + '/t24/src']
import numpy as np  # noqa: E402
from event_universe.assembly.piece import read_piece  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe import tick as T, unspring as U, bobs as B  # noqa: E402
from event_universe.core.spokes import SPOKE_SIDES, SPOKES  # noqa: E402
from event_universe.core.rule3 import wind_weight  # noqa: E402
from event_universe.meshes import coupling_of  # noqa: E402

world, ticks = sys.argv[1], int(sys.argv[2])
calibre, piece = read_piece(Path(S + '/t24/tests/worlds/' + world))
clock = Clock(calibre, piece)
size = clock.size
stats = Counter()
events = []


def Wat(gears, x):
    return int(gears[0].now[x]) * int(gears[1].before[x]) - int(gears[1].now[x]) * int(gears[0].before[x])


def plainq(gears):
    return int(sum(int(v) for v in (gears[0].now * gears[1].before - gears[1].now * gears[0].before).flat))


def nb(c, j):
    a, s = SPOKE_SIDES[j]
    y = list(c)
    y[a] = (y[a] + s) % size[a]
    return tuple(y)


def val(a, c):
    return int(a[c]) if np.ndim(a) else int(a)


def numer(clk, nows, befores, r, c, k):
    n, b = nows[k][c], befores[k][c]
    gripped = shared = 0
    for j in range(SPOKES):
        y = nb(c, j)
        g = val(r.grips[j], c)
        gripped += g * befores[k][y]
        shared += g * (b - befores[k][y]) * (n + nows[k][y])
    own = val(r.teeth, c) * (n * n + b * b) - val(r.hold, c) * n * b - n * gripped
    return (own + own - shared) * val(clk.start_stretch, c)


def slope(clk, hand, at, r):
    nows = [{c: int(g.now[c]) for c in np.ndindex(size)} for g in hand.gears]
    befores = [{c: int(g.before[c]) for c in np.ndindex(size)} for g in hand.gears]
    window = [at] + [nb(at, j) for j in range(SPOKES)]
    G = []
    for k in range(2):
        def N(d):
            nows[k][at] += d
            v = sum(numer(clk, nows, befores, r, c, k) for c in window)
            nows[k][at] -= d
            return v
        G.append((N(1) - N(-1)) // 2)
        A = (N(1) + N(-1) - 2 * N(0)) // 2
    return G, A


def sgn(n):
    d = n * n + 1
    return n // d - (-n) // d


orig_fall = U.fall_of


def fall_of(clk, at, windings, r, hand, going=1):
    got = orig_fall(clk, at, windings, r, hand, going)
    if going == 1 and windings <= 0:
        stats["takes at going 1 with a due <= 0 (the head writes 0)"] += 1
        G, a = slope(clk, hand, at, r)
        u = [-sgn(G[k]) * (1 + (G[k] * G[k] - G[1 - k] * G[1 - k]) // (1 + (G[k] * G[k] - G[1 - k] * G[1 - k]) ** 2))
             for k in range(2)]
        P = -(u[0] * G[0] + u[1] * G[1])
        a2 = a * (u[0] * u[0] + u[1] * u[1])
        M = 2 * wind_weight(clk.full_rate, clk.G)
        DM = windings * M
        if P <= 0:
            stats["  of them with no slope (P = 0)"] += 1
            return got
        s, steps, seen = (DM + P - 1) // P, 0, set()
        while steps < 10 ** 5:
            nxt = (DM + (P - a2 * s) - 1) // (P - a2 * s)
            if nxt == s:
                break
            if nxt in seen:
                s = None
                break
            seen.add(s)
            s, steps = nxt, steps + 1
        if s is None:
            stats["  of them F3's ladder cycles and never stops"] += 1
        elif s < 0:
            stats["  of them F3's ladder writes a negative count (the payer wound up its slope)"] += 1
            stats["    the largest |count|"] = max(stats["    the largest |count|"], -s)
        else:
            stats["  of them F3's ladder writes 0"] += int(s == 0)
    return got


U.fall_of = fall_of
B.fall_of = fall_of
orig_click = T.Tick.click


def click(self):
    clk = self.clock
    pre = [[g.copy() for g in h.gears] for h in clk.hands()]
    starts = self.hand_starts
    q0 = [plainq(g) for g in pre]
    log_from = len(clk.log)
    orig_click(self)
    q1 = [plainq(h.gears) for h in clk.hands()]
    for e in clk.log[log_from:]:
        if e.get("event") != "birth":
            continue
        mi, pl = tuple(e["minus"]), tuple(e["plus"])
        if "takes" in e:
            rec = e["taken_row"]
            w_act = (Wat(pre[rec], mi), Wat(pre[rec], pl))
            w_start = (Wat(starts[rec], mi), Wat(starts[rec], pl))
            events.append(("unspringing", clk.ticks, rec, w_start, w_act, q1[rec] - q0[rec]))
        else:
            s = e["line_pair"]
            events.append(("fitting", clk.ticks, s, (Wat(pre[s], mi), Wat(pre[s], pl)),
                           (Wat(clk.hands()[s].gears, mi), Wat(clk.hands()[s].gears, pl)), q1[s] - q0[s]))


T.Tick.click = click
for _ in range(ticks):
    clock.tick()
print(f"{world}, {ticks} ticks")
for k, v in stats.items():
    print(f"  {k}: {v}")
uns = [ev for ev in events if ev[0] == "unspringing"]
fit = [ev for ev in events if ev[0] == "fitting"]
print(f"  unspringings: {len(uns)}")
for kind, tk, rec, ws, wa, dq in uns:
    print(f"    tick {tk}, hand {rec}: the ends' sweeps at the start {ws} (sum {sum(ws)}); on the board unwound {wa}"
          f" (sum {sum(wa)}); the hand's charge moved by the click {dq}")
print(f"  unspringings removing net charge (the board unwound): {sum(1 for ev in uns if sum(ev[4]) != 0)} of {len(uns)};"
      f" by the start's sums: {sum(1 for ev in uns if sum(ev[3]) != 0)}")
print(f"  fittings: {len(fit)}; the ends' sweeps summing to 0 after: {sum(1 for ev in fit if sum(ev[4]) == 0)};"
      f" laid on ends already standing (a sweep there before): {sum(1 for ev in fit if ev[3] != (0, 0))}")
moved = Counter()
for ev in events:
    moved[(ev[1], ev[2])] += 0
print("  per tick and hand, the click's charge change:", sorted({(ev[1], ev[2], ev[5]) for ev in events if ev[5]}))
