"""Probe B6 (spread): the fed stopped centre under Z (no stopped mask anywhere): its neighbours' loads, its own stretch,
its tensions and factors over the first ticks (the stop spreading through the one-ended Mesh). Usage: python -I b6_spread.py TICKS"""
import json
import sys

sys.path[:0] = ["/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/B"]
import b6_stopped as S6  # noqa: E402
from event_universe import readings  # noqa: E402
from event_universe.core import rates  # noqa: E402
from event_universe.core.spokes import AXES  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
from event_universe.unwind import window_clocks  # noqa: E402

for variant in ("head", "Z"):
    S6.install(variant)
    c = S6.fed_clock()
    stopped_load = rates.stopped_load(c.full_rate)
    for t in range(int(sys.argv[1])):
        load = readings.load(c)
        reg = c.train(REGULATOR).gears
        print(json.dumps({"variant": variant, "tick": t, "the stopped load": stopped_load,
                          "centre X": int(reg[0].now[S6.CENTRE]),
                          "centre tensions": [int(g.now[S6.CENTRE]) for g in reg[1:1 + AXES]],
                          "neighbours' loads": [int(load[n]) for n in window_clocks(c, S6.CENTRE)[1:]]}))
        c.tick()
S6.install("head")
