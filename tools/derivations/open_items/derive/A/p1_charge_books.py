"""P1, the charge's books on the head (read-only harness, no engine change).

For every hand train T and every tick, the total sweep Q_T = SUM_x W_T(x), W = Im(conj(z_now) z_before)
= three_now twelve_before - twelve_now three_before (hands.sweep), read at three moments:
  (a) the tick's start, (b) after the step and the turnover (before the click), (c) after the click.
The step's change (b - a) and the click's change (c - b) are tallied per train, with the train's coupling
(meshes.coupling_of) beside it.  Also, at every fitting and unspringing the log writes, the sweeps the click
leaves at its two ends are read, and for every unspringing the two ends' sweeps at the tick's start
(the pair's charge W_x + W_y that the whole unwind removes).

argv: the head's worktree, the world file, the ticks.
"""
import sys
WT = sys.argv[1]
sys.path[:0] = [WT + '/src', WT]
from collections import Counter
import numpy as np
from tests.laws import world_of
from event_universe import tick as T, hands
from event_universe.clock import Clock
from event_universe.meshes import coupling_of

world, ticks = sys.argv[2], int(sys.argv[3])
calibre, piece = world_of(world)
clock = Clock(calibre, piece)
names = {id(h): k for k, h in enumerate(clock.hands())}


def charges(c):
    return [int(sum(int(v) for v in hands.sweep(h.gears).flat)) for h in c.hands()]


stats = Counter()
step_change = [Counter() for _ in clock.hands()]
click_change = [Counter() for _ in clock.hands()]
orig_click = T.Tick.click
moment = {}


def click(self):
    moment["b"] = charges(self.clock)
    starts = [[g.copy() for g in hs] for hs in self.hand_starts]
    moment["starts"] = starts
    log_from = len(self.clock.log)
    orig_click(self)
    moment["c"] = charges(self.clock)
    for e in self.clock.log[log_from:]:
        if e["event"] != "birth":
            continue
        s = e["line_pair"]
        plus_hand = e.get("plus_hand", s)
        mi, pl = tuple(e["minus"]), tuple(e["plus"])
        w_mi = int(hands.sweep(self.clock.hands()[s].gears)[mi])
        w_pl = int(hands.sweep(self.clock.hands()[plus_hand].gears)[pl])
        kind = "unspringing" if "takes" in e else "fitting"
        stats[f"{kind}s"] += 1
        stats[f"{kind}s, the two ends' sweeps after the click summing 0"] += int(w_mi + w_pl == 0)
        if kind == "unspringing":
            rec = e["taken_row"]
            w0 = int(hands.sweep(starts[rec])[mi]) if rec < len(starts) else None
            w1 = int(hands.sweep(starts[rec])[pl]) if rec < len(starts) else None
            stats["unspringings, the pair's sweeps at the start summing 0 (W_x + W_y = 0)"] += int(w0 + w1 == 0)
            stats["unspringings, the pair's sweeps at the start of opposite sign (the head's R1)"] += int(w0 * w1 < 0)
            stats.setdefault("unspringing pair sums (first 12)", [])
            if len(stats["unspringing pair sums (first 12)"]) < 12:
                stats["unspringing pair sums (first 12)"].append((w0, w1, w0 + w1))


orig_run = T.run


def run(clock_, going):
    a = charges(clock_)
    orig_run(clock_, going)
    if going == 1:
        b, c = moment["b"], moment["c"]
        for k in range(len(a)):
            d_step, d_click = b[k] - a[k], c[k] - b[k]
            step_change[k]["ticks"] += 1
            step_change[k]["ticks with the step's change 0"] += int(d_step == 0)
            step_change[k]["largest |step change|"] = max(step_change[k]["largest |step change|"], abs(d_step))
            click_change[k]["ticks with the click's change 0"] += int(d_click == 0)
            click_change[k]["largest |click change|"] = max(click_change[k]["largest |click change|"], abs(d_click))
            step_change[k]["the total sweep at the end"] = c[k]


T.run = run
T.Tick.click = click
for _ in range(ticks):
    clock.tick()
print(world, ticks, "ticks; the hands in the acts' order, with ratio and coupling:")
for k, h in enumerate(clock.hands()):
    print(f"  hand {k}: spring {h.spring}, coupling {coupling_of(h)}, twin {h.twin is not None}")
    print(f"    the step: {dict(step_change[k])}")
    print(f"    the click: {dict(click_change[k])}")
for k in sorted(stats, key=str):
    print(f"  {k}: {stats[k]}")
print("  counts:", {k: v for k, v in clock.counts.items() if v})
