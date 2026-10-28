"""Verifier B: engine probes written apart from the draft's (no import from S/derive/B).

Run: /home/user/Universe24/venv314/bin/python -I v2_engine.py MODE ...
  cap N1 N2 ...              the bang's setting at N quanta: at tick 1 the drive N, the hold H = X T_d, push and brake;
                             over 40 ticks the first tick with |N| > H
  floor <world> <ticks> <shift>    readings.bottom -> Gamma - <shift> in lockstep with the head: the time gear's two slots at
                             every tick boundary against Gamma (the invariant P), the full state against the head's
  et3 <world> <ticks> <form>       Tick.end_teeth -> my own ET3 (<form>: plain, double, plus1, flip) in lockstep with the head:
                             the full state (teeth included) and the log, entry by entry
  held                       the reaction over the source from the engine's own rate table (rates.rate)
  bang500 QUANTA TICKS       the head on the bang at QUANTA: tick boundaries with a time-gear slot below Gamma (F5's reach)
Integers only. The repository is not edited: each variant is a function assigned at run time.
"""

import json
import sys

S = "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad"
sys.path[:0] = [S + "/t24/src", S + "/t24"]

import numpy as np  # noqa: E402

from event_universe import readings  # noqa: E402
from event_universe import tick as TK  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.core import rates  # noqa: E402
from event_universe.core.rule3 import half  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
from tests.laws import world_of  # noqa: E402

HEAD_BOTTOM, HEAD_END_TEETH, HEAD_HELD = readings.bottom, TK.Tick.end_teeth, TK.held_numerator


def clock_of(world, seed=None):
    calibre, piece = world_of(world)
    if seed is not None:
        piece = {**piece, "seed": seed}
    return Clock(calibre, piece)


def ints(a):
    return [int(v) for v in np.asarray(a, dtype=object).reshape(-1)]


def snapshot(clock):
    """Every integer of the state as I read it: each gear's now, before, fine, teeth and drive fine, the dial, the clicks,
    the slack, the beats' counters, references and split ticks, and the tick count."""
    out = [clock.ticks]
    for gear in clock.all_gears():
        out += ints(gear.now) + ints(gear.before) + ints(gear.fine)
        out += ints(gear.teeth) if np.ndim(gear.teeth) else [int(gear.teeth)]
        out += [] if gear.dfine is None else ints(gear.dfine)
    for arrs in (clock.wound, clock.crossed, clock.beats):
        for a in arrs:
            out += ints(a)
    for pair in clock.reference:
        for a in pair:
            out += ints(a)
    for a in clock.split.values():
        out += ints(a)
    out += ints(clock.dial) + ints(clock.clicks) + ints(clock.slack)
    return out


def slots_below(clock):
    g = clock.train(REGULATOR).gears[0]
    gamma = clock.full_rate
    return sum(1 for v in ints(g.now) + ints(g.before) if v < gamma)


# ------------------------------------------------------------------ cap
def mode_cap(ns):
    for n in ns:
        calibre, piece = world_of("world_bang.json")
        seed = [dict(piece["seed"][0], quanta=n)]
        clock = Clock(calibre, {**piece, "seed": seed})
        seen = {}

        def held(weight, stretch, forms, trace, rate, rim, full_rate, _seen=seen, _clock=clock):
            drive = HEAD_HELD(weight, stretch, forms, trace, rate, rim, full_rate)
            hold = np.asarray(stretch, dtype=object) * _clock.train(REGULATOR).gears[0].dteeth
            over = int(np.sum((np.asarray(drive, dtype=object) > hold) | (np.asarray(drive, dtype=object) < -hold)))
            if _clock.ticks == 1:
                at = (0, 0, 0)
                p0 = int(np.asarray(rate, dtype=object)[at]) if np.ndim(rate) else int(rate)
                x = int(np.asarray(stretch, dtype=object)[at])
                f, sig = int(np.asarray(forms, dtype=object)[at]), int(np.asarray(trace, dtype=object)[at])
                push = 4 * x * f * weight * rim * full_rate * full_rate * p0
                brake = 4 * x * sig * p0 ** 3
                _seen["t1"] = {"N": int(np.asarray(drive, dtype=object)[at]), "H": int(hold[at]), "push": push,
                               "brake": brake, "F": f, "3F div n": 3 * f // n, "3 key": 3 * _clock.key,
                               "brake/push in 1/1000": brake * 1000 // push, "N > H": int(np.asarray(drive, dtype=object)[at]) > int(hold[at]),
                               "clocks past the hold": over}
            if over and "first" not in _seen:
                _seen["first"] = _clock.ticks
            return drive

        TK.held_numerator = held
        x0 = int(clock.train(REGULATOR).gears[0].now[0, 0, 0])
        clock.tick()
        x1 = int(clock.train(REGULATOR).gears[0].now[0, 0, 0])
        for _ in range(39):
            clock.tick()
        TK.held_numerator = HEAD_HELD
        print(json.dumps({"mode": "cap", "quanta": n, "X0": x0, "X1": x1, **seen["t1"],
                          "first tick past the hold (of 40)": seen.get("first")}), flush=True)


# ------------------------------------------------------------------ floor
def mode_floor(world, ticks, shift):
    head, var = clock_of(world), clock_of(world)
    gamma = head.full_rate

    def bottom(clock, _shift=shift):
        return clock.full_rate - _shift

    p_var = p_head = differ = 0
    first = None
    prev_h = prev_v = None
    pinned_h = pinned_v = 0
    for t in range(ticks):
        readings.bottom = HEAD_BOTTOM
        head.tick()
        readings.bottom = bottom
        var.tick()
        readings.bottom = HEAD_BOTTOM
        p_head += slots_below(head)
        p_var += slots_below(var)
        th, tv = np.asarray(head.turned_over, dtype=bool).copy(), np.asarray(var.turned_over, dtype=bool).copy()
        if prev_h is not None:
            pinned_h += int((th & prev_h).sum())
            pinned_v += int((tv & prev_v).sum())
        prev_h, prev_v = th, tv
        if snapshot(head) != snapshot(var):
            differ += 1
            first = first if first is not None else t + 1
    print(json.dumps({"mode": "floor", "world": world, "ticks": ticks, "X_f": gamma - shift,
                      "head: time-gear slots below Gamma at tick ends": p_head,
                      "variant: time-gear slots below Gamma at tick ends": p_var,
                      "ticks whose state differs": differ, "first tick differing": first,
                      "turns head/variant": [head.counts["turns"], var.counts["turns"]],
                      "clocks turned at two ticks in a row head/variant": [pinned_h, pinned_v],
                      "births head/variant": [head.counts["births"], var.counts["births"]]}), flush=True)


# ------------------------------------------------------------------ et3
def make_et3(form):
    def end_teeth(self, time_gear):
        if self.going == -1:
            return HEAD_END_TEETH(self, time_gear)
        clock = self.clock
        held = self.held[self.where[id(self.regulator)]][0]
        xm, x, xp = held.before, held.now, time_gear.now
        xf = readings.bottom(clock)
        f = ((xm < xf) | (xp < xf) | np.asarray(self.stopped, dtype=bool)).astype(object)
        h = half(clock.teeth)
        if form == "flip":
            return h * (x + xp + f * (xp - xm))
        w = h * (x + xp + f * (xm - xp))
        if form == "double":
            return w + f * w
        if form == "plus1":
            return w + f
        return w

    return end_teeth


def mode_et3(world, ticks, form):
    head, var = clock_of(world), clock_of(world)
    et = make_et3(form)
    differ, first, refused = 0, None, None
    for t in range(ticks):
        TK.Tick.end_teeth = HEAD_END_TEETH
        head.tick()
        TK.Tick.end_teeth = et
        try:
            var.tick()
        except Exception as e:  # noqa: BLE001
            refused = f"tick {t + 1}: {type(e).__name__}: {str(e)[:80]}"
            TK.Tick.end_teeth = HEAD_END_TEETH
            break
        TK.Tick.end_teeth = HEAD_END_TEETH
        if snapshot(head) != snapshot(var):
            differ += 1
            first = first if first is not None else t + 1
    logs = [json.dumps(e, sort_keys=True, default=str) for e in head.log], [json.dumps(e, sort_keys=True, default=str) for e in var.log]
    log_diff = sum(1 for a, b in zip(*logs) if a != b) + abs(len(logs[0]) - len(logs[1]))
    print(json.dumps({"mode": "et3", "form": form, "world": world, "ticks": ticks, "refused": refused,
                      "ticks whose state differs": differ, "first tick differing": first,
                      "log entries head/variant": [len(logs[0]), len(logs[1])], "log entries differing": log_diff,
                      "laid head/variant": [head.counts["laid"], var.counts["laid"]]}), flush=True)


# ------------------------------------------------------------------ held
def mode_held():
    gamma, key, w = 1000, 36000, 2
    out = {}
    for c in (0, 10, 100, 1000, 3000):
        p, pw = rates.rate(gamma, c), rates.rate(gamma, c + w)
        num, den = key * (p * p - pw * pw), 2 * w * p * p
        out[str(c)] = [p, pw, num // den, num % den, den]
    print(json.dumps({"mode": "held", "Gamma": gamma, "key": key, "w": w, "load: [p0, p0(c+w), q, r, den]": out}), flush=True)


# ------------------------------------------------------------------ the bang below the cap: does F5 act on the head?
def mode_bang(quanta, ticks):
    calibre, piece = world_of("world_bang.json")
    seed = [dict(piece["seed"][0], quanta=quanta)]
    clock = Clock(calibre, {**piece, "seed": seed})
    below, first, least = 0, None, None
    for t in range(ticks):
        clock.tick()
        b = slots_below(clock)
        g = clock.train(REGULATOR).gears[0]
        m = min(ints(g.now) + ints(g.before))
        least = m if least is None else min(least, m)
        if b and first is None:
            first = t + 1
        below += b
    print(json.dumps({"mode": "bang", "quanta": quanta, "ticks": ticks, "time-gear slots below Gamma at tick ends": below,
                      "first tick": first, "least slot": least, "turns": clock.counts["turns"],
                      "births": clock.counts["births"]}), flush=True)


def mode_et3pair(world, ticks, form):
    """plain ET3 against a mutated ET3, in lockstep: the state and the log entry by entry."""
    a, b = clock_of(world), clock_of(world)
    plain, mut = make_et3("plain"), make_et3(form)
    differ = 0
    for _ in range(ticks):
        TK.Tick.end_teeth = plain
        a.tick()
        TK.Tick.end_teeth = mut
        b.tick()
        TK.Tick.end_teeth = HEAD_END_TEETH
        differ += snapshot(a) != snapshot(b)
    la = [json.dumps(e, sort_keys=True, default=str) for e in a.log]
    lb = [json.dumps(e, sort_keys=True, default=str) for e in b.log]
    keys = {}
    for x, y in zip(a.log, b.log):
        for k in set(x) | set(y):
            if json.dumps(x.get(k), default=str) != json.dumps(y.get(k), default=str):
                keys[k] = keys.get(k, 0) + 1
    print(json.dumps({"mode": "et3pair", "form": form, "world": world, "ticks": ticks,
                      "ticks whose state differs (plain vs mutated)": differ,
                      "log entries differing (plain vs mutated)": sum(1 for x, y in zip(la, lb) if x != y) + abs(len(la) - len(lb)),
                      "keys": keys, "laid plain/mutated": [a.counts["laid"], b.counts["laid"]]}), flush=True)


def mode_chart(world, ticks, variant):
    """One run, the head or the floor at Gamma: stopped clock-ticks (the mesh rate 0 read at each tick's start),
    the first stopped tick, the turns, the births, and the stopped clocks' turns at their release (FR-S1)."""
    clock = clock_of(world)
    if variant == "floor":
        readings.bottom = lambda c: c.full_rate
    stopped_ticks, first, released = 0, None, 0
    prev = None
    for t in range(ticks):
        st = np.asarray(readings.stopped_of(clock, readings.load(clock)), dtype=bool)
        clock.tick()
        n = int(st.sum())
        stopped_ticks += n
        if n and first is None:
            first = t + 1
        released += int((st & np.asarray(clock.turned_over, dtype=bool)).sum())
    readings.bottom = HEAD_BOTTOM
    g = clock.train(REGULATOR).gears[0]
    print(json.dumps({"mode": "chart", "variant": variant, "world": world, "ticks": ticks,
                      "stopped clock-ticks": stopped_ticks, "first tick with a stopped clock": first,
                      "stopped clock-ticks turned at that tick": released, "turns": clock.counts["turns"],
                      "births": clock.counts["births"], "X bits": max(abs(v).bit_length() for v in ints(g.now))}), flush=True)


def mode_rewind(world, ticks, variant):
    """The variant forward TICKS ticks from the setting, my snapshot kept at every tick, then TICKS ticks back:
    the count of ticks whose state returns exactly (my snapshot, teeth and drive fines included); also the count of
    floor turns crossed (clock-ticks turned with a time-gear slot of the held start below Gamma + 1 or a raw fall)."""
    clock = clock_of(world)
    if variant in ("floor", "both"):
        readings.bottom = lambda c: c.full_rate
    if variant in ("et3", "both"):
        TK.Tick.end_teeth = make_et3("plain")
    kept, turned = [], 0
    for _ in range(ticks):
        kept.append(snapshot(clock))
        clock.tick()
        turned += int(np.asarray(clock.turned_over, dtype=bool).sum())
    back = 0
    for k in range(ticks):
        clock.tick(-1)
        back += snapshot(clock) == kept[ticks - 1 - k]
    readings.bottom, TK.Tick.end_teeth = HEAD_BOTTOM, HEAD_END_TEETH
    print(json.dumps({"mode": "rewind", "variant": variant, "world": world, "ticks": ticks,
                      "states returned exactly": back, "turned clock-ticks crossed": turned}), flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "cap":
        mode_cap([int(x) for x in sys.argv[2:]])
    elif mode == "floor":
        mode_floor(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    elif mode == "et3":
        mode_et3(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    elif mode == "held":
        mode_held()
    elif mode == "et3pair":
        mode_et3pair(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    elif mode == "chart":
        mode_chart(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    elif mode == "rewind":
        mode_rewind(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    elif mode == "bang500":
        mode_bang(int(sys.argv[2]), int(sys.argv[3]))
