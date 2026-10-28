"""Probe B5 (exploration): where the head's release advances the unsprung gear, and whether that clock is still
(turned over or stopped) at the tick's end, on a chart or on a setting given inline as JSON.
Usage: python -I b5_explore.py WORLD TICKS [SEED_JSON]"""

import json
import sys

sys.path[:0] = ["/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/B"]
import bcommon as B  # noqa: E402
from bcommon import np  # noqa: E402
from event_universe import tick as T  # noqa: E402

HEAD_ADV, HEAD_TURN = T.Tick.advances, T.Tick.turnover
stats = {"advanced clock-ticks": 0, "advanced at a still clock": 0, "notches advanced": 0,
         "notches advanced at a still clock": 0, "release nonzero clock-ticks": 0}


def advances(self):
    if self.going == 1:
        gear = self.clock.unsprung().gears[0]
        before = gear.now.copy()
        stats["release nonzero clock-ticks"] += B.n(self.release != 0)
        HEAD_ADV(self)
        self._adv = gear.now - before
    else:
        HEAD_ADV(self)


def turnover(self):
    HEAD_TURN(self)
    adv = getattr(self, "_adv", None)
    if adv is not None:
        still = self.top | self.stopped
        nz = adv != 0
        stats["advanced clock-ticks"] += B.n(nz)
        stats["advanced at a still clock"] += B.n(nz & still)
        stats["notches advanced"] += int(sum(abs(int(x)) for x in adv.reshape(-1)))
        stats["notches advanced at a still clock"] += int(sum(abs(int(x)) for x in np.where(still, adv, 0).reshape(-1)))
        self._adv = None


T.Tick.advances, T.Tick.turnover = advances, turnover
world, ticks = sys.argv[1], int(sys.argv[2])
changes = {"seed": json.loads(sys.argv[3])} if len(sys.argv) > 3 else {}
clock = B.make(world, **changes)
for _ in range(ticks):
    clock.tick()
print(json.dumps({"world": world, "ticks": ticks, "seed": changes.get("seed", "file"), **stats,
                  "laid": clock.counts["laid"], "births": clock.counts["births"]}), flush=True)
