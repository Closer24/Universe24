"""Probe B1: where each bound of the head acts, counted at every forward tick of every chart (the head's code unchanged).

Usage: python -I b1_counts.py WORLD TICKS   (one chart, one JSON line)
       python -I b1_counts.py --all         (every chart of bcommon.CHARTS, one after the other)
The bounds: F1 the drive at plus or minus the hold (tick.py:255), F2 the tension in [0, Gamma] (meshes.py:74),
F5 the load below 0 read at 0 (readings.py:21), ET the end teeth kept above 0 (tick.end_teeth), R10 the stopped mask.
It can fail: the ET line 'neither turned nor stopped' must read 0 (the claim that every fallback value is discarded)."""

import json
import sys

sys.path[:0] = ["/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/B"]
from collections import Counter  # noqa: E402

import bcommon as B  # noqa: E402


def one(world, ticks):
    stats = Counter()
    B.install_counters(stats)
    clock = B.make(world)
    for _ in range(ticks):
        clock.tick()
    # the end state's load too (a hill left by the last tick is read by no tick start)
    from event_universe import readings

    stats["F5 load below 0 in the end state"] = B.n(readings.load(clock) < 0)
    B.uninstall()
    return {"world": world, "ticks": ticks, **dict(stats)}


if __name__ == "__main__":
    runs = B.CHARTS if sys.argv[1] == "--all" else [(sys.argv[1], int(sys.argv[2]))]
    for world, ticks in runs:
        print(json.dumps(one(world, ticks)), flush=True)
