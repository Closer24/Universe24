"""Draft B's shared harness: the head's clock from a test world, its state as text, and the counters of the five bounds.

Nothing here edits a file of the repository: every change is a wrapper installed on the head's functions at run time.
Integers only; run with python -I and the path set by `setup`."""

import sys

S = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad"
sys.path[:0] = [S + "/t24/src", S + "/t24", S + "/derive/B"]

from collections import Counter  # noqa: E402

import numpy as np  # noqa: E402

from event_universe import meshes, readings, run  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.core.rule3 import carries, held_numerator  # noqa: E402
from event_universe.core.spokes import AXES, SIDES, SPOKE_SIDES, across  # noqa: E402
from event_universe.meshes import even  # noqa: E402
from event_universe.regulation import tensor_parts  # noqa: E402
from tests.laws import world_of  # noqa: E402

# every chart of tests/worlds at its own intervals, the one big bang at the plan's 250
CHARTS = [
    ("world_hole.json", 60), ("world_nature.json", 60), ("world_bodies.json", 120), ("world_bang.json", 250),
    ("world_node.json", 20), ("world_ga2.json", 230), ("world_polarization.json", 12), ("world_packet.json", 150),
    ("world_emission.json", 300), ("world_emission_none.json", 300), ("world_emission_one.json", 300),
    ("world_sea.json", 400), ("world_sea_3.json", 240), ("world_plasma.json", 400), ("world_plasma_3.json", 400),
    ("world_universe.json", 400), ("world_universe_3.json", 400), ("world_pair_3.json", 400),
    ("world_collapse_500.json", 600), ("world_collapse_800.json", 600), ("world_collapse_1200.json", 600),
]


def make(world, **changes):
    calibre, piece = world_of(world)
    return Clock(calibre, {**piece, **changes})


def state(clock):
    return run.state_text(clock) + f" {clock.ticks}"


def n(mask):
    return int(np.asarray(mask, dtype=bool).sum())


ORIG = {
    "rate_readings": T.Tick.rate_readings,
    "carry": T.Tick.carry,
    "end_teeth": T.Tick.end_teeth,
    "turnover": T.Tick.turnover,
    "factors": T.factors,
}


def install_counters(stats: Counter):
    """Count, at every forward tick, where each bound of the head acts (the head's code runs unchanged)."""

    def factors(clock, axis_notches=None, stopped=None):
        if axis_notches is not None:
            for spoke, (axis, _side) in enumerate(SPOKE_SIDES):
                t = carries(even(axis_notches[axis], spoke) + 1, SIDES)
                stats["F2 tensions read"] += t.size
                stats["F2 tension below 0"] += n(t < 0)
                stats["F2 tension above Gamma"] += n(t > clock.full_rate)
                stats["F2 tension at or above Gamma (factor 0)"] += n(t >= clock.full_rate)
        return ORIG["factors"](clock, axis_notches, stopped)

    def rate_readings(self):
        ORIG["rate_readings"](self)
        stats["clock-ticks"] += self.load.size
        stats["F5 load below 0 at the tick's start"] += n(self.load < 0)
        stats["R10 stopped clock-ticks"] += n(self.stopped)
        stats["R10 dial held where the rate is not 0"] += n(self.stopped & (np.asarray(self.rate) != 0))

    def carry(self):
        clk, k = self.clock, self.where[id(self.regulator)]
        trace, _ = tensor_parts(self.stress[:AXES])
        drive = held_numerator(clk.trace, self.stretch_now, self.forms, trace, self.rate, clk.rim, clk.full_rate)
        hold = self.stretch_now * self.trains[k][0].dteeth
        stats["F1 drive above the hold"] += n(drive > hold)
        stats["F1 drive below minus the hold"] += n(drive < -hold)
        over = np.where(np.abs(drive) > hold, np.abs(drive) // hold, 0)
        stats["F1 largest |drive| div hold"] = max(stats["F1 largest |drive| div hold"], int(over.max()))
        self._et_first = True
        ORIG["carry"](self)

    def end_teeth(self, time_gear):
        if getattr(self, "_et_first", False):
            self._et_first = False
            w = readings.mean_teeth(self.clock, time_gear)
            self._fallback = np.asarray(w <= 0)
            stats["ET end teeth at or below 0 (the fallback)"] += n(self._fallback)
        return ORIG["end_teeth"](self, time_gear)

    def turnover(self):
        ORIG["turnover"](self)
        fb = getattr(self, "_fallback", None)
        stats["turned clock-ticks"] += n(self.top)
        if fb is not None:
            stats["ET fallback at a turned clock"] += n(fb & self.top)
            stats["ET fallback at a stopped clock"] += n(fb & self.stopped)
            stats["ET fallback at a clock neither turned nor stopped"] += n(fb & ~self.top & ~self.stopped)
            self._fallback = None

    T.Tick.rate_readings, T.Tick.carry, T.Tick.end_teeth, T.Tick.turnover = rate_readings, carry, end_teeth, turnover
    T.factors = factors


def uninstall():
    T.Tick.rate_readings, T.Tick.carry = ORIG["rate_readings"], ORIG["carry"]
    T.Tick.end_teeth, T.Tick.turnover = ORIG["end_teeth"], ORIG["turnover"]
    T.factors = ORIG["factors"]


def across_any(mask, spokes):
    return [mask | across(mask, s) for s in range(spokes)]


__all__ = ["S", "CHARTS", "make", "state", "n", "install_counters", "uninstall", "meshes", "np"]
