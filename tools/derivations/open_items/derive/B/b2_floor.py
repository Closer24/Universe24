"""Probe B2: the floor and the end teeth replaced by the turnover, run in lockstep with the head on every chart.

Variants (installed at run time, no file edited):
  ET    the end teeth W+ = the mean teeth of the time gear as the act leaves it: (T/2)(X- + X) at a still clock
        (turned over or stopped, where the turnover or the stop leaves the time gear at its start's two notches),
        (T/2)(X + X+) elsewhere; no fallback (the head's np.where(w > 0, w, start)).
  FLOOR the turnover's floor at the full rate, X_f = Gamma (the stretch of the load 0), in place of X(-Gamma);
        with it no clock starts a tick on a hill, so the hill's clamp (readings.rates_of, F5) is never reached
        through the load.
  ET3   the end teeth W+ = the start's mean teeth only where the act discards its output by the floor's trigger
        (X- < X_f or the raw X+ < X_f) or by the stop, (T/2)(X + X+) elsewhere (the top-turned clocks as the head).
  BOTH  ET and FLOOR together.  BOTH3  ET3 and FLOOR together.
Each chart: the state (every integer, run.state_text) compared with the head's after every tick; the log compared
entry by entry; F5 counted under the variant (tick-start loads below 0, and held loads below 0 separately);
the variant's rewind (tests.laws.run_back_exact over 20 ticks from the setting).
It can fail: ET must leave the state bit for bit on every chart (PROVED in DERIVATION.md section 4); FLOOR must leave
every chart where F5 never acts bit for bit, and must read 0 tick-start loads below 0 everywhere.
Usage: python -I b2_floor.py <variant> <world> <ticks>"""

import json
import sys

sys.path[:0] = ["/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/B"]
import hashlib  # noqa: E402

import bcommon as B  # noqa: E402
from bcommon import np  # noqa: E402
from event_universe import readings  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
from tests.laws import run_back_exact  # noqa: E402

HEAD = {"end_teeth": T.Tick.end_teeth, "bottom": readings.bottom, "rate_readings": T.Tick.rate_readings}
COUNT = {"load<0": 0, "held<0": 0, "head fallback sites": 0}


def end_teeth(self, time_gear):
    """W+ read from the time gear as the act leaves it (forward); backward the head's (the forward's start teeth)."""
    if self.going == -1:
        return HEAD["end_teeth"](self, time_gear)
    clock = self.clock
    held = self.held[self.where[id(self.regulator)]][0]
    x0, x1, x2 = held.before, held.now, time_gear.now
    x2 = np.where(self.stopped, x1, x2)  # the stop's restore, as the turnover's trigger reads it (R10 kept here)
    xf = readings.bottom(clock)
    top = (x0 <= x1) & (x2 <= x1) & ((x0 < x1) | (x2 < x1)) | (x0 < xf) | (x2 < xf)
    still = top | self.stopped
    start, end = readings.mean_teeth(clock, held), readings.mean_teeth(clock, time_gear)
    if getattr(self, "_b2_tick", None) != clock.ticks:  # once per tick: the carry's call, not the advances'
        self._b2_tick = clock.ticks
        COUNT["head fallback sites"] += B.n(end <= 0)
    return np.where(still, start, end)


def end_teeth3(self, time_gear):
    """W+ at the start's teeth where the floor (on the raw output) or the stop discards the output; backward the head's."""
    if self.going == -1:
        return HEAD["end_teeth"](self, time_gear)
    clock = self.clock
    held = self.held[self.where[id(self.regulator)]][0]
    x0, x2 = held.before, time_gear.now
    xf = readings.bottom(clock)
    discarded = (x0 < xf) | (x2 < xf) | self.stopped
    start, end = readings.mean_teeth(clock, held), readings.mean_teeth(clock, time_gear)
    if getattr(self, "_b2_tick", None) != clock.ticks:
        self._b2_tick = clock.ticks
        COUNT["head fallback sites"] += B.n(end <= 0)
        COUNT["floor-discarded sites"] = COUNT.get("floor-discarded sites", 0) + B.n(discarded)
    return np.where(discarded, start, end)


def bottom(clock):
    return clock.full_rate


def rate_readings(self):
    HEAD["rate_readings"](self)
    if self.going == 1:
        COUNT["load<0"] += B.n(self.load < 0)
        COUNT["held<0"] += B.n(np.asarray(self.held_load) < 0)


def install(variant):
    T.Tick.rate_readings = rate_readings
    if variant in ("ET", "BOTH"):
        T.Tick.end_teeth = end_teeth
    if variant in ("ET3", "BOTH3"):
        T.Tick.end_teeth = end_teeth3
    if variant in ("FLOOR", "BOTH", "BOTH3"):
        readings.bottom = bottom


def uninstall():
    T.Tick.end_teeth, readings.bottom, T.Tick.rate_readings = HEAD["end_teeth"], HEAD["bottom"], HEAD["rate_readings"]


def digest(clock):
    return hashlib.sha256(B.state(clock).encode()).hexdigest()


def log_keys(a, b):
    """The keys whose values differ between two log entries."""
    return sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))


def main(variant, world, ticks):
    head, var = B.make(world), B.make(world)
    first, differ, stats = None, 0, {}
    for t in range(ticks):
        uninstall()
        head.tick()
        install(variant)
        var.tick()
        uninstall()
        if digest(head) != digest(var):
            differ += 1
            first = t + 1 if first is None else first
    install(variant)
    load_end = B.n(readings.load(var) < 0)
    uninstall()
    # the logs, entry by entry
    hl, vl = head.log, var.log
    same_len = len(hl) == len(vl)
    diff_entries, keys = 0, {}
    for a, b in zip(hl, vl):
        if json.dumps(a, sort_keys=True, default=str) != json.dumps(b, sort_keys=True, default=str):
            diff_entries += 1
            for k in log_keys(a, b):
                keys[k] = keys.get(k, 0) + 1
    counted = dict(COUNT)
    # the variant's rewind from the setting
    install(variant)
    rewind = run_back_exact(B.make(world), 20)
    uninstall()
    stats = {
        "variant": variant, "world": world, "ticks": ticks,
        "ticks whose state differs from the head's": differ, "first tick differing": first,
        "log entries head/variant": [len(hl), len(vl)], "log entries differing (same length)": diff_entries if same_len else None,
        "keys differing": keys,
        "variant: tick-start loads below 0": counted["load<0"], "variant: tick-start held loads below 0": counted["held<0"],
        "variant: end-state loads below 0": load_end,
        "variant: sites where the head's end teeth would be at or below 0": counted["head fallback sites"],
        "variant ET3: sites whose output the floor or the stop discards": counted.get("floor-discarded sites"),
        "counts head": {k: head.counts[k] for k in ("turns", "births", "body_clicks", "laid", "laid_nodes")},
        "counts variant": {k: var.counts[k] for k in ("turns", "births", "body_clicks", "laid", "laid_nodes")},
        "variant rewind exact of 20": rewind,
    }
    print(json.dumps(stats), flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
