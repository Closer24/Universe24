"""Probe B6: R10 and BH-S1, the stopped clock (the mesh rate 0 at the tick's start): its dial held
(np.where(stopped, 0, rate), tick.py:108), its gears restored every tick (tick.carry's last restore), its Meshes'
factors set to 0 from both ends (meshes.factors), and the click's skips (click.engage, splits, bobs.py:51).

Variants (installed at run time, no file edited):
  head   the head unchanged.
  Z      'the rate 0 gives nothing, with no restore': readings.stopped_of reads no clock stopped, everywhere (the tick's
         mask, the restore, the dial's hold, the factors' mask and the click's skips all gone); what is left is the
         formula's own zero, the grips 2 pinion p_i^2 Q at the mesh rate p_i = 0.
Modes:
  fed VARIANT TICKS    the head's own BH-S1 test world: the 3-cube's centre fed to the stopped load's level, both
                       slots (tests/test_the_node.py), every tick: the centre's stretch, its turnovers, its gears moved,
                       its dial; the centre's own grips (must read 0 with no mask: the formula's zero) and its
                       neighbours' grips toward it (the mask's work); the rewind of the run.
  chart <variant> <world> <ticks>   a chart: stopped clock-ticks, turnovers, births, the stretch's bits; with Z in lockstep
                       with the head (the ticks whose state differs) and the rewind of 20 ticks from 5 ticks before the
                       first stop."""

import copy
import json
import sys

sys.path[:0] = ["/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/B"]
import hashlib  # noqa: E402

import bcommon as B  # noqa: E402
from bcommon import np  # noqa: E402
from event_universe import readings  # noqa: E402
from event_universe.core import rates  # noqa: E402
from event_universe.core.spokes import SPOKES  # noqa: E402
from event_universe.trains import REGULATOR  # noqa: E402
from event_universe.unwind import window_clocks  # noqa: E402
from tests.laws import level_at, run_back_exact  # noqa: E402

HEAD_STOPPED = readings.stopped_of
CENTRE = (1, 1, 1)


def no_stop(clock, c):
    return np.zeros(clock.size, dtype=bool)


def install(variant):
    readings.stopped_of = no_stop if variant == "Z" else HEAD_STOPPED


def fed_clock():
    clock = B.make("world_node.json")
    stopped = rates.stopped_load(clock.full_rate)
    reg = clock.train(REGULATOR).gears[0]
    reg.now[CENTRE] = level_at(clock, stopped)
    reg.before[CENTRE] = reg.now[CENTRE]
    clock.driven_teeth()
    return clock


def grips_at(clock, at):
    """Every train's six grips at the clock `at`, read from the load at the tick's start with no mask (factors None)."""
    from event_universe.meshes import factors

    load = readings.load(clock)
    unmasked = factors(clock, None, None)
    own, toward = 0, 0
    for r in clock.trains_:
        if r.ratio is None:
            continue
        g = readings.gearing_of(clock, r, load, unmasked)
        own += sum(1 for grip in g.grips if int(np.asarray(grip)[at]) != 0)
        for spoke, n in enumerate(window_clocks(clock, at)[1:]):
            back = spoke ^ 1  # the neighbour's spoke toward `at`
            toward += int(int(np.asarray(g.grips[back])[n]) != 0)
    return own, toward


def fed(variant, ticks):
    install(variant)
    clock = fed_clock()
    kept = copy.deepcopy(clock)
    fed_gears = [[int(a[CENTRE]) for a in (g.now, g.before, g.fine)] for g in clock.all_gears()]
    course, own_nonzero, toward_nonzero, stopped_ticks, moved_ticks = [], 0, 0, 0, 0
    dial0 = int(clock.dial[CENTRE])
    for t in range(ticks):
        load = readings.load(clock)
        stopped_now = np.asarray(rates.mesh_rate_of(clock.full_rate, load), dtype=object) == 0
        if stopped_now[CENTRE]:
            stopped_ticks += 1
            own, toward = grips_at(clock, CENTRE)
            own_nonzero += own
            toward_nonzero += toward
        clock.tick()
        gears = [[int(a[CENTRE]) for a in (g.now, g.before, g.fine)] for g in clock.all_gears()]
        moved_ticks += gears != fed_gears
        if t < 8 or (t + 1) % 10 == 0:
            reg = clock.train(REGULATOR).gears[0]  # re-read: the trains' gears are new objects every tick
            course.append({"tick": t + 1, "X now": int(reg.now[CENTRE]), "turned": bool(clock.turned_over[CENTRE]),
                           "stopped at start": bool(stopped_now[CENTRE]), "dial": int(clock.dial[CENTRE]) - dial0,
                           "light gear 0": int(clock.unsprung().gears[0].now[CENTRE])})
    rewind = run_back_exact(kept, ticks)
    install("head")
    print(json.dumps({"mode": "fed", "variant": variant, "ticks": ticks, "ticks the centre starts stopped": stopped_ticks,
                      "ticks its gears differ from the fed values": moved_ticks,
                      "the centre's own grips not 0, no mask (summed over its stopped ticks)": own_nonzero,
                      "neighbours' grips toward the centre not 0, no mask (summed)": toward_nonzero,
                      "turns": clock.counts["turns"], "rewind exact": f"{rewind} of {ticks}", "course": course}),
          flush=True)


def digest(clock):
    return hashlib.sha256(B.state(clock).encode()).hexdigest()


def chart(variant, world, ticks):
    a = B.make(world)
    b = B.make(world) if variant == "Z" else None
    stopped, first_stop, differ, first = 0, None, 0, None
    for t in range(ticks):
        install("head")
        s = readings.stopped_of(a, readings.load(a))
        if B.n(s) and first_stop is None:
            first_stop = t + 1
        stopped += B.n(s)
        a.tick()
        if b is not None:
            install("Z")
            b.tick()
            install("head")
            if digest(a) != digest(b):
                differ += 1
                first = t + 1 if first is None else first
    out = {"mode": "chart", "variant": variant, "world": world, "ticks": ticks, "stopped clock-ticks (head)": stopped,
           "first tick with a stopped clock (head)": first_stop,
           "counts head": {k: a.counts[k] for k in ("turns", "births", "body_clicks")}}
    if b is not None:
        out.update({"ticks whose state differs": differ, "first tick differing": first,
                    "counts Z": {k: b.counts[k] for k in ("turns", "births", "body_clicks")},
                    "X bits head / Z": [max(int(abs(int(v))).bit_length() for v in c.train(REGULATOR).gears[0].now.reshape(-1)) for c in (a, b)]})
        if first_stop is not None:
            install("Z")
            c = B.make(world)
            for _ in range(max(0, first_stop - 5)):
                c.tick()
            out["Z rewind of 20 from 5 ticks before the first stop"] = run_back_exact(c, 20)
            install("head")
    print(json.dumps(out), flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "fed":
        fed(sys.argv[2], int(sys.argv[3]))
    else:
        chart(sys.argv[2], sys.argv[3], int(sys.argv[4]))
