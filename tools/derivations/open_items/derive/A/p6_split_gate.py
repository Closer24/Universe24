"""P6, the split's gate (R6, bobs.py:160) on a world whose matter is twin hands (no committed calibre holds one).

The head fires a twin pair's split at a Node-clock where it is due (the pair's beat, its split ticks, not stopped)
AND light arrives (the unsprung hand's lead over the six Meshes not 0).  The replacement read here: the split by
the parts' sizes alone, its payment the take F3, whose own zero (the payer's integer vertex below the winding)
is the only other gate.  Counted: the due Node-clocks with and without light arriving, and of those R6 blocks,
how many the light there could pay (F3's vertex) and how many would split by the parts' sizes (the head's own
draw against the sweeps, read without writing).

argv: the head's worktree, the world file, the ticks.  The world's calibre is read with every gapped row of two
gears made a row of four (twin hands at the same pair), in memory only.
"""
import sys
WT = sys.argv[1]
sys.path[:0] = [WT + '/src', WT]
import copy
from collections import Counter
import numpy as np
from tests.laws import world_of
from event_universe import bobs as B, hands as H
from event_universe.clock import Clock
from event_universe.core.rule3 import wind_weight
from event_universe.trains import Gear
from event_universe.unwind import window_clocks
from event_universe.hands import spoke_places, products


def numerator(clock, gears, r, window):
    """hands.wind's exact numerator summed over the window, before its carry: SUM (o + o - s) X (as in P3)."""
    places = [tuple(np.array(w) for w in zip(*window))]
    places += [tuple(table[(slice(None), *places[0])]) for table in spoke_places(clock.size)]
    at = lambda a: a[places[0]] if np.ndim(a) else a
    beyond = lambda a, spoke: a[places[1 + spoke]]
    x = clock.start_stretch[places[0]]
    full_n, full_b = [g.now for g in gears], [g.before for g in gears]
    nows, befores = [at(n) for n in full_n], [at(b) for b in full_b]
    zero = np.zeros(len(window), dtype=object)
    gripped = [zero.copy() for _ in gears]
    shared = [zero.copy() for _ in gears]
    for spoke, grip in enumerate(r.grips):
        b_j = [beyond(b, spoke) for b in full_b]
        n_j = [beyond(n, spoke) for n in full_n]
        here = at(grip)
        gripped = [v + here * bj for v, bj in zip(gripped, b_j)]
        parts = products([b - bj for b, bj in zip(befores, b_j)], [n + nj for n, nj in zip(nows, n_j)])
        shared = [s + here * p for s, p in zip(shared, parts)]
    own = [at(r.teeth) * (nn + bb) - at(r.hold) * nb - nr for nn, bb, nb, nr in
           zip(products(nows, nows), products(befores, befores), products(nows, befores), products(nows, gripped))]
    return int(sum(int(v) for o, s in zip(own, shared) for v in ((o + o - s) * x)))


def moved(gears, at, d):
    out = []
    for g, dk in zip(gears, d):
        n = g.now.copy()
        n[at] = n[at] + dk
        out.append(Gear(n, g.before, g.fine, g.teeth))
    return out

stats = Counter()
orig_splits = B.splits


def sgn(n):
    d = n * n + 1
    return n // d - (-n) // d


def light_can_pay(clock, at, due, r):
    """F3's zero: the light's integer vertex along its steepest unit pays the due (in wind units)."""
    hand = clock.unsprung()
    window = window_clocks(clock, at)
    N0 = numerator(clock, hand.gears, r, window)
    G, A = [], []
    for k in range(2):
        up = [1 if j == k else 0 for j in range(2)]
        dn = [-1 if j == k else 0 for j in range(2)]
        Np, Nm = numerator(clock, moved(hand.gears, at, up), r, window), numerator(clock, moved(hand.gears, at, dn), r, window)
        G.append((Np - Nm) // 2)
        A.append((Np + Nm - 2 * N0) // 2)
    steep = [1 if G[k] * G[k] >= G[1 - k] * G[1 - k] else 0 for k in range(2)]
    u = [-sgn(G[k]) * steep[k] for k in range(2)]
    u2 = u[0] * u[0] + u[1] * u[1]
    if u2 == 0:
        return False
    P = -(u[0] * G[0] + u[1] * G[1])
    a2 = A[0] * u2
    sv = (P + a2) // (a2 + a2)
    M = 2 * wind_weight(clock.full_rate, clock.G)
    return sv * P - a2 * sv * sv >= due * M


def splits(clock, hand_starts, reads, fitted_clocks, stopped, r_unsprung):
    winds, gearings, gears_read = reads
    hands, (_, net) = clock.hands(), B.light_lead(clock, hand_starts)
    for pair in H.twin_pairs(hands):
        u, w = pair[0], clock.windings[pair[0]]
        up, down = winds[u], winds[pair[1]]
        split_next = np.where((up < w) & (down < w) & (up + down >= w), clock.split[u] + 1, 0)
        beat = np.where(clock.beats[u] > 0, clock.beats[u], clock.beats[pair[1]])
        due = (beat > 0) & (split_next >= beat) & ~stopped
        for where in zip(*np.nonzero(due)):
            at = tuple(int(x) for x in where)
            if at in fitted_clocks:
                continue
            arrives = int(net[at]) != 0
            stats["split-due Node-clocks (the pair's beat, its split ticks, not stopped, not fitted)"] += 1
            stats["  light arriving (the head's R6 lets it split)"] += int(arrives)
            if not arrives:
                owed = w - int(clock.slack[at])
                pays = owed <= 0 or light_can_pay(clock, at, owed, r_unsprung)
                stats["  no light arriving (R6 blocks it)"] += 1
                stats["    of them the light there can pay the winding (F3's vertex): the split by the sizes alone"] += int(pays)
    return orig_splits(clock, hand_starts, reads, fitted_clocks, stopped, r_unsprung)


from event_universe import click as C  # noqa: E402
B.splits = splits
C.splits = splits  # click.click calls the name it imported
calibre, piece = world_of(sys.argv[2])
calibre = copy.deepcopy(calibre)
for row in calibre["rows"]:
    if int(row["shape"]) == 2:
        row["shape"] = 4
clock = Clock(calibre, piece)
for _ in range(int(sys.argv[3])):
    clock.tick()
splits_logged = sum(1 for e in clock.log if e["event"] == "split")
print(sys.argv[2], "with twin hands,", sys.argv[3], "ticks; fittings", clock.counts["births"], "chimes",
      clock.counts["body_clicks"], "splits", splits_logged)
for k in stats:
    print(f"  {k}: {stats[k]}")
