"""Draft H's engine probe: the head's worlds under the bounds' replacements, in lockstep with the head.

Run: /home/user/Universe24/venv314/bin/python -I h_engine.py <variant> <world> <ticks>
Every change is a function installed at run time on the head's modules; no file of the repository is edited.
One JSON line per run.

Variants (each a set of switches):
  HEAD      the head unchanged (the counts of its own bounds and ties)
  WMIN      law 4's floor X_f struck; the bottom the time gear's weak minimum (X0 >= X1 <= X2, one strict)
  SMIN      the bottom the strict minimum (X0 > X1 < X2)
  FULL      the bottom at the full rate: X0 < Gamma or X2 < Gamma (the rate's dial at its whole turn)
  NOF5      F5 struck: the load read as it is (a hill read as a hill)
  FULLNOF5  FULL with F5 struck
  NOLOW     F2's lower side struck (a tension below 0 read as it is; the upper side kept)
  NORM      NOLOW with the light cone kept by the A1 normalisation of the six grips (section 4.6)
  NORMALL   NORM with F2's upper side struck too
  NOF1      F1 struck: the time gear's drive lands whole
  FULLNOF1  FULL and F1 struck, the driven carries gated by the turnover (no carry at a turned clock)
  FULLNORM  FULL with F5 struck and F2's lower side struck under the A1 normalisation (the two constructions together)
Counted per run: the ticks whose state differs from the head's and the first; turnovers; Node-clocks turned at
two ticks running (pinned); tick-start loads below 0; outputs X+ <= 0; end teeth at or below 0 at a clock not
turned; the light-cone edge D + 2 SUM R > 4 w (clock-trains past it); the widest transient (bits); fittings and
bob clicks; the fine teeth at 0 (ties: at an even teeth count, the head's mirror misses there); the rewind of 20.
"""

import hashlib
import inspect
import json
import sys
import textwrap

S = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad"
sys.path[:0] = [S + "/t24/src", S + "/t24"]

import numpy as np  # noqa: E402

from event_universe import clock as C  # noqa: E402
from event_universe import meshes, readings, run  # noqa: E402
from event_universe import tick as T  # noqa: E402
from event_universe.core import rates, rule3  # noqa: E402
from event_universe.core.rule3 import carries, mesh_factor  # noqa: E402
from event_universe.core.spokes import SIDES, SPOKE_SIDES, SPOKES, across  # noqa: E402
from event_universe.meshes import even  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
from tests.laws import run_back_exact, world_of  # noqa: E402

HEAD = {
    "turnover": C.Clock.turnover,
    "factors": T.factors,
    "rates_of": readings.rates_of,
    "gearing": rule3.gearing,
    "carry": T.Tick.carry,
    "end_teeth": T.Tick.end_teeth,
}
SWITCH = {
    "HEAD": set(),
    "WMIN": {"wmin"},
    "SMIN": {"smin"},
    "FULL": {"full"},
    "NOF5": {"nof5"},
    "FULLNOF5": {"full", "nof5"},
    "NOLOW": {"nolow"},
    "NORM": {"nolow", "norm"},
    "NORMALL": {"nolow", "noup", "norm"},
    "NOF1": {"nof1"},
    "FULLNOF1": {"full", "nof1", "gate"},
    "FULLNORM": {"full", "nolow", "norm", "nof5"},
}
COUNTS = {"head": {}, "variant": {}}
CUR = ["variant"]
ON = set()


def bump(key, value=1):
    count = COUNTS[CUR[0]]
    count[key] = count.get(key, 0) + int(value)


def n(mask):
    return int(np.asarray(mask, dtype=bool).sum())


# --- the turnover's trigger -----------------------------------------------------------------------------


def turnover(self, held, going=1, top=None):
    if going == -1 or not (ON & {"wmin", "smin", "full"}):
        found = HEAD["turnover"](self, held, going, top)
    else:
        k = self.trains_.index(self.train(REGULATOR))
        x0, x1, x2 = held[k][0].before, held[k][0].now, self.train(REGULATOR).gears[0].now
        top = (x0 <= x1) & (x2 <= x1) & ((x0 < x1) | (x2 < x1))
        if "wmin" in ON:
            top = top | ((x0 >= x1) & (x2 >= x1) & ((x0 > x1) | (x2 > x1)))
        if "smin" in ON:
            top = top | ((x0 > x1) & (x2 > x1))
        if "full" in ON:
            top = top | (x0 < self.full_rate) | (x2 < self.full_rate)
        self.turned_over = top
        if top.any():
            self.counts["turns"] += int(top.sum())
            self.turnovers.append((self.ticks, int(top.sum())))
            self.reverse(top, held)
        found = top
    if going == 1:
        prev = getattr(self, "_h_prev_top", None)
        if prev is not None:
            bump("pinned (turned two ticks running)", n(np.asarray(prev) & np.asarray(found)))
        self._h_prev_top = np.asarray(found).copy()
        x2 = self.train(REGULATOR).gears[0].now
        bump("outputs X+ <= 0 at a clock not turned", n((np.asarray(x2) <= 0) & ~np.asarray(found)))
        # the ties the head's mirror misses: the held fine teeth at 0 at an even teeth count, at the turned clocks
        if np.asarray(found).any():
            for r, train in zip(self.trains_, held):
                if r.teeth is not None:
                    continue  # a train of its own teeth (the ratchet) is flipped by the head, not mirrored
                for gear in train:
                    tooth, teeth = np.asarray(gear.fine), np.asarray(gear.teeth)
                    bump(f"ties met by the turnover (fine 0 at even teeth, turned clocks), size {r.size}",
                         n((tooth == 0) & (teeth % 2 == 0) & np.asarray(found)))
                    if gear.dfine is not None:
                        d, dt = np.asarray(gear.dfine), np.asarray(gear.dteeth)
                        bump("ties met by the turnover (drive fine 0 at even drive teeth)",
                             n((d == 0) & (dt % 2 == 0) & np.asarray(found)))
    return found


# --- F2: the tension's two sides, and the A1 normalisation ----------------------------------------------


def factors(clock, axis_notches=None, stopped=None):
    if not (ON & {"nolow", "noup"}):
        found = HEAD["factors"](clock, axis_notches, stopped)
    else:
        notches = ([g.now for g in clock.train(REGULATOR).gears[1:4]] if axis_notches is None else axis_notches)
        found = []
        for spoke, (axis, _side) in enumerate(SPOKE_SIDES):
            t = carries(even(notches[axis], spoke) + 1, SIDES)
            if "noup" not in ON:
                t = np.minimum(t, clock.full_rate)
            if "nolow" not in ON:
                t = np.maximum(t, 0)
            factor = mesh_factor(clock.full_rate, clock.G, t)
            at_teeth = None if stopped is None else stopped | across(stopped, spoke)
            found.append(factor if at_teeth is None else np.where(at_teeth, 0, factor))
        found = tuple(found)
    if axis_notches is not None:
        for spoke, (axis, _side) in enumerate(SPOKE_SIDES):
            t = carries(even(axis_notches[axis], spoke) + 1, SIDES)
            bump("tensions read", np.asarray(t).size)
            bump("tensions below 0", n(np.asarray(t) < 0))
            bump("tensions above Gamma", n(np.asarray(t) > clock.full_rate))
    return found


def gearing(pinion, rim, full_rate, rate, mesh_rate, factors=None, mesh_unit=1):
    g = HEAD["gearing"](pinion, rim, full_rate, rate, mesh_rate, factors, mesh_unit)
    if "norm" in ON and factors is not None:
        cap = SPOKES * mesh_unit * mesh_unit  # the vacuum's six factors' sum, the A1 part at the full rate
        total = sum(np.asarray(f, dtype=object) for f in factors)
        safe = np.where(np.asarray(total) == 0, 1, total)
        mr2 = mesh_rate * mesh_rate
        grips = tuple(((mr2 + mr2) * pinion * cap * np.asarray(f, dtype=object)) // safe for f in factors)
        teeth, own = g.teeth, g.spring
        g = rule3.Gearing(grips, teeth + teeth - own - sum(grips), teeth, own)
    # the light cone, Rule3's own edge: D + 2 SUM R <= 4 w at every clock
    edge = np.asarray(g.spring + 2 * sum(np.asarray(x, dtype=object) for x in g.grips)) > 4 * g.teeth
    bump("clock-gearings read", np.asarray(edge).size)
    bump("clock-gearings past the light-cone edge", n(edge))
    return g


# --- F5: the load below 0 -------------------------------------------------------------------------------


def rates_of(clock, c):
    c = np.asarray(c, dtype=object)
    if "nof5" in ON:
        return rates.rate_of(clock.full_rate, c), rates.mesh_rate_of(clock.full_rate, c)
    return HEAD["rates_of"](clock, c)


# --- F1: the drive within its hold; the gate before the driven carry ------------------------------------


CLAMP = "numerators = [np.minimum(np.maximum(drive, -hold), hold)]"


def _struck_carry():
    """The head's own Tick.carry with the one line of F1 changed (the drive lands whole), compiled here."""
    src = textwrap.dedent(inspect.getsource(HEAD["carry"]))
    assert src.count(CLAMP) == 1 and src.startswith("def carry(self)")
    src = src.replace("def carry(self)", "def struck_carry(self)", 1).replace(CLAMP, "numerators = [drive]")
    space = dict(vars(T))
    exec(compile(src, "struck_carry", "exec"), space)
    return space["struck_carry"]


STRUCK_CARRY = _struck_carry()


def carry(self):
    if self.going == 1:
        bump("tick-start loads below 0", n(np.asarray(self.load) < 0))
    if "nof1" not in ON:
        return HEAD["carry"](self)
    return STRUCK_CARRY(self)


def end_teeth(self, time_gear):
    w = readings.mean_teeth(self.clock, time_gear)
    if self.going == 1 and getattr(self, "_h_et", None) != self.clock.ticks:
        self._h_et = self.clock.ticks
        held = self.held[self.where[id(self.regulator)]][0]
        x0, x1, x2 = held.before, held.now, time_gear.now
        trig = (x0 <= x1) & (x2 <= x1) & ((x0 < x1) | (x2 < x1))
        if "full" in ON:
            trig = trig | (x0 < self.clock.full_rate) | (x2 < self.clock.full_rate)
        if "wmin" in ON:
            trig = trig | ((x0 >= x1) & (x2 >= x1) & ((x0 > x1) | (x2 > x1)))
        if not (ON & {"wmin", "smin", "full"}):
            trig = trig | (x0 < readings.bottom(self.clock)) | (x2 < readings.bottom(self.clock))
        bump("end teeth at or below 0", n(np.asarray(w) <= 0))
        bump("end teeth at or below 0 at a clock not turned", n((np.asarray(w) <= 0) & ~np.asarray(trig)))
    if "gate" in ON and self.going == 1:  # forward only; backward the head's (the forward's start teeth)
        held = self.held[self.where[id(self.regulator)]][0]
        x0, x1, x2 = held.before, held.now, time_gear.now
        trig = (x0 <= x1) & (x2 <= x1) & ((x0 < x1) | (x2 < x1)) | (x0 < self.clock.full_rate) | (x2 < self.clock.full_rate)
        return np.where(trig, readings.mean_teeth(self.clock, held), w)  # no carry is kept at a turned clock
    return HEAD["end_teeth"](self, time_gear)


def install(variant):
    ON.clear()
    ON.update(SWITCH[variant])
    C.Clock.turnover = turnover
    T.factors = factors
    readings.rates_of = rates_of
    rule3.gearing = gearing
    T.Tick.carry = carry
    T.Tick.end_teeth = end_teeth


def uninstall():
    ON.clear()


def digest(clock):
    return hashlib.sha256((run.state_text(clock) + f" {clock.ticks}").encode()).hexdigest()


def ties_in_state(clock, key):
    """Fine teeth at 0 at an even teeth count in the tick's end state (a carry that landed on a tie)."""
    for r in clock.trains_:
        for gear in r.gears:
            if gear.dfine is not None:
                bump(key + ", drive", n((np.asarray(gear.dfine) == 0) & (np.asarray(gear.dteeth) % 2 == 0)))
            if r.teeth is not None:
                continue
            tooth, teeth = np.asarray(gear.fine), np.asarray(gear.teeth)
            bump(key + f", size {r.size}", n((tooth == 0) & (teeth % 2 == 0)))


def make(world):
    calibre, piece = world_of(world)
    return C.Clock(calibre, piece)


def main(variant, world, ticks):
    install("HEAD")
    CUR[0] = "head"
    head = make(world)
    install(variant)
    CUR[0] = "variant"
    var = make(world)
    first, differ, stopped_at, error = None, 0, None, None
    bits = 0
    for t in range(ticks):
        install("HEAD")
        CUR[0] = "head"
        try:
            head.tick()
        except Exception as e:  # noqa: BLE001
            error = f"the head stopped at tick {t + 1}: {type(e).__name__}: {e}"
            break
        ties_in_state(head, "ties in the end state (fine 0 at even teeth)")
        CUR[0] = "variant"
        install(variant)
        try:
            var.tick()
        except Exception as e:  # noqa: BLE001
            stopped_at = t + 1
            error = f"{type(e).__name__}: {str(e)[:160]}"
            break
        bits = max(bits, var.max_transient)
        if digest(head) != digest(var):
            differ += 1
            first = t + 1 if first is None else first
    install(variant)
    CUR[0] = "rewind"
    COUNTS["rewind"] = {}
    try:
        rewind = run_back_exact(make(world), 20)
    except Exception as e:  # noqa: BLE001
        rewind = f"{type(e).__name__}: {str(e)[:80]}"
    uninstall()
    keys = ("turns", "births", "body_clicks")
    out = {
        "variant": variant, "world": world, "ticks": ticks,
        "ticks differing from the head": differ, "first tick differing": first,
        "variant stopped at tick": stopped_at, "error": error,
        "head counts": {k: head.counts[k] for k in keys}, "variant counts": {k: var.counts[k] for k in keys},
        "variant widest transient (bits)": bits, "head widest transient (bits)": head.max_transient,
        "rewind exact of 20": rewind,
        "head counted": {k: COUNTS["head"][k] for k in sorted(COUNTS["head"])},
        "variant counted": {k: COUNTS["variant"][k] for k in sorted(COUNTS["variant"])},
    }
    print(json.dumps(out), flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
