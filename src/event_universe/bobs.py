"""The bobs' chiming, the click's last act (ALGEBRA.md, One point and one beat): a hand wound to a whole winding of its own through one period of its beat clicks, one unwind of its winding at the clock from the unsprung hand (`bobs`), the chime logged with its face (`chime`: a hand's notches, neighbours, offsets and factors at the start, `face_of`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import rule3
from event_universe.core.rule3 import carries, largest_below
from event_universe.core.spokes import AXES, SPOKE_SIDES, SPOKES
from event_universe.draw import vernier
from event_universe.hands import dot, sweep, twin_pairs, wind
from event_universe.meshes import coupling_of, train_lead
from event_universe.phase import books, snapshot
from event_universe.run import chime, logged
from event_universe.trains import Gear
from event_universe.unspring import fall_of, read_unwinds, unwind_ends, unwinds
from event_universe.unwind import advance, recoil, window_clocks

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
    """The bobs' chiming: a hand wound to a whole winding of its own through one period of its beat clicks (one unwind of its winding at the clock, the chime logged), a clock of a fitting this tick or a stopped clock apart; EQ-S1 in cs7's letter (CS7-S1; the owner's word of 2026-10-25, 17:57 UTC, through the Boss's recommendation, 6402908585 and 6403341352): where nothing arrives at the clock, the unwound hand's lead across its six meshes summed 0 at the tick's start (meshes.train_lead as click.engage reads it; what flows in flows out), the unwind is returned to the unwound gear (the gear the unwind moved, logged as `taken_line`: CS4-S2) by the one advance act in the same click, the chime written with laid_back the notches and its push tallied 0, so a great clock alike at every clock returns to the full rate exactly with a bob chimed at every clock in every cycle, and where the unsprung windings accumulate the unwind stands (the former closing, the take alone, kept by name; eq2's reading, every one of the six currents 0, kept by name); the unsprung hand is never chimed as a bob, its winding's count weighted by its coupling 0 (meshes.coupling_of, min(spring, 1): its counters stay 0, the branch on its identity a product, David's DAVID-GENERIC-ENGINE.md part B; the unsprung hand no bob, cs4's sentence through the Boss, 6402358120: light at rest is no body in nature, its windings unwound at an engagement and by a bob's click alone; the former closing of the standing light, credited at every interval where its beat stood at 1, kept by name); the beat a hand's own (the owner's word of 2026-10-27, 15:5x UTC, through the Boss's recommendation: the beat read free of the phase; DAVID-OWN-BEAT.md): at the first tick of a winding the hand's notch now is kept at the clock as its reference (where that notch is 0, the next tick's), the crossings' timer restarted there, and the beat is read on the dot of the reference with the hand's notch, before and now, so a turn of the hand by any Gaussian g multiplies the reading by |g|^2 and keeps its sign, and a hand swinging on its twelve gear alone chimes as one on its three gear (the former reading on the three gear's notches, which a quarter turn of the hand moved and a hand on the twelve gear never crossed, kept by name), its zero crossings counted in either direction (CK-S1: the crossing read even under the negation of the gear, the two notches' product below 0 or exactly one of them 0, a touch of zero a crossing from either side alike, so the chiming is covariant under the reflection and the colour exchange alike; the beat the half period; the former upward crossing, and the form `b < 0 <= n or n < 0 <= b` odd where exactly one level is 0, kept by name)."""
    rec0, net = light_lead(clock, hand_starts)
    by_clock: dict[tuple[int, ...], list[int]] = {}
    for rec, hand in enumerate(clock.hands()):
        wound, reference = coupling_of(hand) * (winds[rec] >= clock.windings[rec]), clock.reference[rec]
        starting = wound & ((clock.wound[rec] == 0) | (dot(reference, reference) == 0))
        reference = [np.where(starting, g.now, r) for g, r in zip(hand.gears, reference, strict=True)]
        clock.reference[rec], clock.crossed[rec] = reference, np.where(starting, 0, clock.crossed[rec])
        clock.wound[rec] = np.where(wound, clock.wound[rec] + 1, 0)
        was = dot(reference, [g.before for g in hand.gears])
        read = dot(reference, [g.now for g in hand.gears])
        crossing = (was * read < 0) | ((was == 0) != (read == 0))
        timed = clock.crossed[rec] > 0
        clock.beats[rec] = np.where(crossing & timed, clock.crossed[rec], clock.beats[rec])
        clock.crossed[rec] = np.where(crossing, 1, np.where(timed, clock.crossed[rec] + 1, 0))
        chiming = (clock.beats[rec] > 0) & (clock.wound[rec] >= clock.beats[rec])
        for where in zip(*np.nonzero(chiming), strict=True):
            at = tuple(int(x) for x in where)
            if at in fitted_clocks or stopped[at]:
                continue
            clock.wound[rec][at] = 0
            if int(net[at]) == 0:
                still_chime(clock, rec, rec0, at, hand_starts, r_unsprung)
                continue
            by_clock.setdefault(at, []).append(rec)
    start, writes = snapshot(clock), []
    planned = [
        (
            at,
            recs,
            read_unwinds(clock, [(at, sum(clock.windings[r] for r in recs))], r_unsprung, len(recs)),
        )
        for at, recs in sorted(by_clock.items())
    ]
    for at, recs, got in planned:
        if got is not None:
            chimes_of(clock, at, recs, unwind_ends(clock, got[1], got[0])[0], hand_starts, rec0)
            writes.append((rec0, at, False))
    booked = books(clock, start, writes, {rec0: r_unsprung})
    if booked:
        logged(clock, "books", tuple(booked[0][:-1]), booked=booked)


def chimes_of(
    clock: Clock,
    at: tuple[int, ...],
    recs: list[int],
    take: dict[str, Any],
    hand_starts: list[list[Gear]],
    rec0: int,
) -> None:
    """The chimes of one take (David's DAVID-THE-ORDER-FREE-STRIKE.md: one take per clock-node and unwound hand, the dues summed, every read on the start board): the hands chiming at one clock-node in one click share its one take of their windings summed, each chime logged with its own winding booked, the first with the take's fall and each later one taking nothing, the remainder handing on what the fall paid for it, so every chime's book closes (taken + the remainder before - the remainder after = its winding) and the last leaves the take's remainder."""
    after, rest = take["remainder"], sum(clock.windings[r] for r in recs[1:])
    gear = clock.hands()[rec0].gears[take["taken_line"]]
    clock.counts["body_clicks"] += len(recs)
    clock.log.append(
        chime(
            clock,
            recs[0],
            at,
            take | {"remainder": after + rest},
            face_of(clock, recs[0], at, hand_starts),
            hand_starts[recs[0]],
        )
    )
    for rec in recs[1:]:
        now, was = int(gear.now[at]), after + rest
        rest -= clock.windings[rec]
        clock.last_push = [0] * AXES
        clock.last_recoil = recoil(clock, at, clock.last_push, int(clock.start_rate[at]), 1)
        clock.clicks[at] += 1
        part = {"taken": 0, "levels": 0, "taken_now_was": now, "taken_line": take["taken_line"]}
        part |= {
            "taker": [now, int(gear.before[at]), 0],
            "remainder_was": was,
            "remainder": after + rest,
        }
        clock.log.append(
            chime(clock, rec, at, part, face_of(clock, rec, at, hand_starts), hand_starts[rec])
        )


def still_chime(
    clock: Clock,
    rec: int,
    rec0: int,
    at: tuple[int, ...],
    hand_starts: list[list[Gear]],
    r_unsprung: rule3.Gearing,
) -> None:
    """A chime where nothing arrives (CS7-S1's letter, the owner's word of 2026-10-27, 18:5x UTC, through the Boss's recommendation; David's DAVID-WORLDS-EVERY-TEST.md): credited laid back with no take, nothing taken, nothing booked, the slack unwritten, the push 0 tallied on the mesh, logged on the gear a take would move (CS4-S2's choice, unspring.fall_of at no winding, so a turn of the hand moves the logged gear with it); the former take of the whole winding laid back after it, which the honest books refused as a stop on every uniform world, kept by name."""
    hand, slack = clock.hands()[rec0], int(clock.slack[at])
    _none, _fall, k = fall_of(clock, at, 0, r_unsprung, hand)
    now, before = int(hand.gears[k].now[at]), int(hand.gears[k].before[at])
    take = {"taken": 0, "levels": 0, "taken_now_was": now, "taken_line": k, "taker": [now, before, 0]}
    clock.last_push = [0] * AXES
    clock.last_recoil = recoil(clock, at, clock.last_push, int(clock.start_rate[at]), 1)
    clock.clicks[at] += 1
    clock.counts["body_clicks"] += 1
    clock.counts["laid_back"] += 1
    found = chime(
        clock,
        rec,
        at,
        take | {"remainder_was": slack, "remainder": slack},
        face_of(clock, rec, at, hand_starts),
        hand_starts[rec],
    )
    clock.log.append(found | {"laid_back": 0, "dP_take": [0] * AXES, "booked": 0, "recoil": [0] * AXES})


def splits(
    clock: Clock,
    hand_starts: list[list[Gear]],
    reads: tuple[list[Any], list[rule3.Gearing], list[tuple[Gear, rule3.Gearing]]],
    fitted_clocks: set[tuple[int, ...]],
    stopped: Any,
    r_unsprung: rule3.Gearing,
) -> None:
    """The split hand's chime, the measurement's law at one clock (the owner's word of 2026-10-27, 15:5x UTC, through the Boss's recommendation: the split hand's chime derived by David first; DAVID-SPLIT-CHIME.md, toys-5 dd8d3283b), run before the bobs' chiming for each twin pair: where neither twin's wind at the tick's start reaches the winding W and their sum does, the pair's split ticks counted (reset where not); where they reach the pair's beat (the up twin's, else the down's) at a clock neither fitted nor stopped and light arrives (the unsprung hand's lead over the six meshes not 0), the vernier's draw c in [0, room) picks the up twin where c (|W_up| + |W_down|) < room |W_up|, else the down, against the sweeps at the tick's start; the picked twin's every notch v goes to the largest n with n^2 |W_picked| <= v^2 (|W_up| + |W_down|), its sign kept, the other twin's to 0, both by the one advance act, the window's wind before less after into the slack (EX-S1, signed), and the pair clicks as one hand, one unwind of W from the unsprung hand (the bobs' chime act) credited to the picked twin; a refused unwind leaves nothing of the act standing; the split logged with its moves for the undo (a quantum shared between places, and the pair's one pick across a fitting that Bell's 2.828 needs, wait on the owner's word)."""
    winds, gearings, gears_read = reads
    hands, (_, net) = clock.hands(), light_lead(clock, hand_starts)
    for pair in twin_pairs(hands):
        u, w = pair[0], clock.windings[pair[0]]
        up, down = winds[u], winds[pair[1]]
        clock.split[u] = np.where((up < w) & (down < w) & (up + down >= w), clock.split[u] + 1, 0)
        beat = np.where(clock.beats[u] > 0, clock.beats[u], clock.beats[pair[1]])
        due = (beat > 0) & (clock.split[u] >= beat) & ~stopped & (net != 0)
        swept = [abs(sweep(hand_starts[r])) for r in pair]
        for where in zip(*np.nonzero(due), strict=True):
            at = tuple(int(x) for x in where)
            if at in fitted_clocks:
                continue
            clock.split[u][at] = 0
            sweeps, drawn = [int(s[at]) for s in swept], vernier(clock, at, gears_read, w)
            if drawn is None or sum(sweeps) == 0:
                continue
            picked = pair[0] if drawn[0] * sum(sweeps) < drawn[1] * sweeps[0] else pair[1]
            moved: list[list[int]] = []
            before, picked_sweep = window_wind(clock, pair, gearings, at), sweeps[pair.index(picked)]
            for r in pair:
                was = [int(slot[at]) for g in hands[r].gears for slot in (g.now, g.before)]
                to = [largest_below(int(carries(v * v * sum(sweeps), picked_sweep))) for v in was]
                kept = [(n if v >= 0 else -n) - v for n, v in zip(to, was, strict=True)]
                moved.append(kept if r == picked else [-v for v in was])
                advance(clock, r, at, tuple(moved[-1]))
            carried = before - window_wind(clock, pair, gearings, at)
            clock.slack[at] += carried
            got = unwinds(clock, [(at, w)], r_unsprung, 1)
            if got is None:
                for r, m in zip(pair, moved, strict=True):
                    advance(clock, r, at, tuple(m), -1)
                clock.slack[at] -= carried
                continue
            clock.counts["body_clicks"] += 1
            logged(
                clock,
                "split",
                at,
                pair=list(pair),
                sweeps=sweeps,
                draw=list(drawn),
                picked=picked,
                moved=moved,
                carried=carried,
            )
            clock.log.append(
                chime(
                    clock,
                    picked,
                    at,
                    got[0],
                    face_of(clock, picked, at, hand_starts),
                    hand_starts[picked],
                )
            )


def light_lead(clock: Clock, hand_starts: list[list[Gear]]) -> tuple[int, Any]:
    """The unsprung hand's place among the hands and its lead across its six meshes summed at the tick's start (meshes.train_lead as click.engage reads it): what arrives at each clock."""
    rec0 = clock.hands().index(clock.unsprung())
    return rec0, sum((train_lead(hand_starts[rec0], spoke) for spoke in range(SPOKES)), start=0)


def window_wind(
    clock: Clock, recs: tuple[int, ...], gearings: list[rule3.Gearing], at: tuple[int, ...]
) -> int:
    """The window's wind of the hands named, at the clock and its six neighbours, each hand at its own gearing (hands.wind)."""
    window = window_clocks(clock, at)
    return sum(int(v) for r in recs for v in wind(clock, clock.hands()[r].gears, gearings[r], window))


def face_of(
    clock: Clock, rec: int, at: tuple[int, ...], hand_starts: list[list[Gear]]
) -> dict[str, Any]:
    """A chime's face: the hand's notches at the clock now, before the turnover (the state the turnover replaced at a turned-over clock, the notches now elsewhere; CL-S2: no second moment of the click, the former `stepped` kept by name) and at the start, its neighbours' at the start, the mesh offsets, pawls, odd gears and factors the clock read at the start."""
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
