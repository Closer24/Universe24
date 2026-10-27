"""The bobs' chiming, the striking's last act (ALGEBRA.md, One point and one beat): a hand wound to a whole winding of its own through one period of its beat strikes, one unwind of its winding at the clock from the unsprung hand (`bobs`), the chime logged with its face (`chime`: a hand's notches, neighbours, offsets and factors at the start, `face_of`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import rule3
from event_universe.core.spokes import AXES, SPOKE_SIDES, SPOKES
from event_universe.meshes import train_lead
from event_universe.run import chime
from event_universe.trains import Gear
from event_universe.unspring import unwinds
from event_universe.unwind import move, recoil, window_clocks

if TYPE_CHECKING:
    from event_universe.clock import Clock


def bobs(
    clock: Clock,
    hand_starts: list[list[Gear]],
    winds: list[Any],
    fitted_clocks: set[tuple[int, ...]],
    stopped: Any,
    r_unsprung: rule3.Gearing,
) -> None:
    """The bobs' chiming: a hand wound to a whole winding of its own through one period of its beat strikes (one unwind of its winding at the clock, the chime logged), a clock of a fitting this tick or a stopped clock apart; EQ-S1 in cs7's letter (CS7-S1; the owner's word of 2026-10-25, 17:57 UTC, through the Boss's recommendation, 6402908585 and 6403341352): where nothing arrives at the clock, the unwound hand's lead across its six meshes summed 0 at the tick's start (meshes.train_lead as striking.engage reads it; what flows in flows out), the unwind is returned to the unwound gear (the gear the unwind moved, logged as `taken_line`: CS4-S2) by the one advance act in the same striking, the chime written with laid_back the notches and its push tallied 0, so a great clock alike at every clock returns to the full rate exactly with a bob chimed at every clock in every cycle, and where the unsprung windings accumulate the unwind stands (the former closing, the take alone, kept by name; eq2's reading, every one of the six currents 0, kept by name); the unsprung hand is never chimed as a bob (the unsprung hand no bob, cs4's sentence through the Boss, 6402358120: light at rest is no body in nature, its windings unwound at an engagement and by a bob's strike alone; the former closing of the standing light, credited at every interval where its beat stood at 1, kept by name); the beat a hand's by its three gear's zero crossings counted in either direction (CK-S1: the crossing read even under the negation of the gear, the two notches' product below 0 or exactly one of them 0, a touch of zero a crossing from either side alike, so the chiming is covariant under the reflection and the colour exchange alike; the beat the half period; the former upward crossing, and the form `b < 0 <= n or n < 0 <= b` odd where exactly one level is 0, kept by name)."""
    rec0 = clock.hands().index(clock.unsprung())
    net = sum((train_lead(hand_starts[rec0], spoke) for spoke in range(SPOKES)), start=0)
    for rec, hand in enumerate(clock.hands()):
        if hand is clock.unsprung():
            continue
        clock.wound[rec] = np.where(winds[rec] >= clock.windings[rec], clock.wound[rec] + 1, 0)
        three = hand.gears[0]
        crossing = (three.before * three.now < 0) | ((three.before == 0) != (three.now == 0))
        timed = clock.crossed[rec] > 0
        clock.beats[rec] = np.where(crossing & timed, clock.crossed[rec], clock.beats[rec])
        clock.crossed[rec] = np.where(crossing, 1, np.where(timed, clock.crossed[rec] + 1, 0))
        chiming = (clock.beats[rec] > 0) & (clock.wound[rec] >= clock.beats[rec])
        for where in zip(*np.nonzero(chiming), strict=True):
            at = tuple(int(x) for x in where)
            if at in fitted_clocks or stopped[at]:
                continue
            got = unwinds(clock, [(at, clock.windings[rec])], r_unsprung, 1)
            clock.wound[rec][at] = 0
            if got is None:
                continue
            (unwind,) = got
            notches, now, k = unwind["levels"], unwind["taken_now_was"], unwind["taken_line"]
            clock.counts["body_clicks"] += 1
            face = face_of(clock, rec, at, hand_starts)
            entry = chime(clock, rec, at, unwind, face, hand_starts[rec])
            if int(net[at]) == 0:
                move(clock, rec0, k, at, now - int(clock.hands()[rec0].gears[k].now[at]))
                entry["laid_back"], entry["dP_take"] = notches, [0] * AXES
                back = recoil(clock, at, [-x for x in clock.last_push], entry["clock"], 1)
                entry["recoil"], entry["carry"] = [0] * AXES, back["carry"]
                clock.counts["laid_back"] += 1
            clock.log.append(entry)


def face_of(
    clock: Clock, rec: int, at: tuple[int, ...], hand_starts: list[list[Gear]]
) -> dict[str, Any]:
    """A chime's face: the hand's notches at the clock now, before the turnover (the state the turnover replaced at a turned-over clock, the notches now elsewhere; CL-S2: no second moment of the striking, the former `stepped` kept by name) and at the start, its neighbours' at the start, the mesh offsets, pawls, odd gears and factors the clock read at the start."""
    three, twelve = clock.hands()[rec].gears
    three0, twelve0 = hand_starts[rec]
    clocks = window_clocks(clock, at)[1:]
    three_was, twelve_was = clock.before_turnover[rec]
    return {
        "re_now": int(three.now[at]),
        "im_now": int(twelve.now[at]),
        "re_before": int(three.before[at]),
        "im_before": int(twelve.before[at]),
        "re_before_swap": int(three_was.now[at]),
        "im_before_swap": int(twelve_was.now[at]),
        "re_start_now": int(three0.now[at]),
        "re_start_before": int(three0.before[at]),
        "im_start_now": int(twelve0.now[at]),
        "im_start_before": int(twelve0.before[at]),
        "re_neighbours_start": [int(three0.now[n]) for n in clocks],
        "im_neighbours_start": [int(twelve0.now[n]) for n in clocks],
        "phases": [[int(c[at]), int(sn[at])] for c, sn in clock.start_offsets],
        "frames": [int(f[at]) for f in clock.start_pawls],
        "odd": [
            int(side * (clock.start_odd[axis][at] + clock.start_odd[axis][n]))
            for (axis, side), n in zip(SPOKE_SIDES, clocks, strict=True)
        ],
        "X": clock.standard_length,
        "factors": [int(f[at]) for f in clock.start_factors],
    }
