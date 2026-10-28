"""The click's phase, read whole before any write (the order-free click, David's DAVID-THE-STRIKES-ORDER.md and DAVID-THE-ORDER-FREE-STRIKE.md): the one board every read of a phase reads (`snapshot`), the one jam of two clicks writing one gear at one node-clock (`crowded`, `claimed`) and the books that close the phase node-clock by node-clock (`books`)."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import hands
from event_universe.core import rule3
from event_universe.trains import Gear, zeros
from event_universe.unwind import window_clocks

if TYPE_CHECKING:
    from event_universe.clock import Clock

Claim = tuple[int, tuple[int, ...]]


def snapshot(clock: Clock) -> list[list[Gear]]:
    """Every hand's gears copied where a click's phase starts: the one board every read of the phase reads, and the books' ground."""
    return [[gear.copy() for gear in hand.gears] for hand in clock.hands()]


def crowded(clock: Clock, planned: list[Any], claims: Callable[[Any], set[Claim]]) -> list[Any]:
    """The phase's one jam beside the lay's (DAVID-THE-ORDER-FREE-STRIKE.md: any two writes of one gear at one node-clock but the takes summed jam whole): two clicks of one phase writing one hand at one node-clock (an end's take, or a hand laid there; `claims` names each click's) are jammed by name `lay`, both, so no write reads another's and no order chooses between them. Returns the clicks kept."""
    seen: dict[Claim, int] = {}
    for plan in planned:
        for claim in claims(plan):
            seen[claim] = seen.get(claim, 0) + 1
    kept = []
    for plan in planned:
        shared = sorted(claim for claim in claims(plan) if seen[claim] > 1)
        if not shared:
            kept.append(plan)
            continue
        clock.counts["refused_lay"] += 1
        jam = {"event": "refused", "i": clock.ticks, "node": list(shared[0][1]), "cause": "lay"}
        clock.log.append(jam | {"crowded": len(shared)})
    return kept


def claimed(clock: Clock, plan: Any) -> set[Claim]:
    """A fitting click's writes, hand and node-clock: its unwind's ends and its fitted hands' two ends (the hand at the - end, its twin at the + end)."""
    _at, _rec, fits, (_taker, ends), _light = plan
    laid = {
        (p, end)
        for fit in fits
        for p, end in (
            (fit.gear_ratio, fit.minus),
            (hands.twin_of(clock.hands(), fit.gear_ratio), fit.plus),
        )
    }
    return {(read[-1], read[0]) for read in ends} | laid


def books(
    clock: Clock,
    start: list[list[Gear]],
    writes: list[tuple[int, tuple[int, ...], bool]],
    gearings: dict[int, rule3.Gearing],
) -> list[list[int]]:
    """A click phase's books (DAVID-THE-STRIKES-ORDER.md point 2, DAVID-THE-ORDER-FREE-STRIKE.md point 3): at every node-clock the hands' wind after the phase less at its start, less each write's own (a write the hand's notches at one node-clock: an unwind's end read alone on the start board, or a fitted hand's own quantum on zero gears, the windings booked; `writes` holds (hand, node-clock, on zero gears)), booked into the node-clock's remainder, signed: the cross terms of adjacent writes and of a lay with the field it lands in, so the book closes node-clock by node-clock whatever order the writes took, every write's own book its own, a remainder below 0 the light's debt the next due there pays first. Returns the node-clocks booked as [x, y, z, the amount] for the log."""
    left = zeros(clock.size)
    for r in sorted({w[0] for w in writes}):
        hand, gearing = clock.hands()[r], gearings[r]
        base = hands.wind(clock, start[r], gearing)
        left = left + hands.wind(clock, hand.gears, gearing) - base
        for _r, where, zero in (w for w in writes if w[0] == r):
            at = zeros(clock.size) != 0
            at[where] = True
            trial = [
                Gear(
                    np.where(at, gear.now - zero * s.now, (1 - zero) * s.now),
                    np.where(at, gear.before - zero * s.before, (1 - zero) * s.before),
                    s.fine,
                    s.teeth,
                )
                for gear, s in zip(hand.gears, start[r], strict=True)
            ]
            window = sorted(set(window_clocks(clock, where)))
            for c, v in zip(window, hands.wind(clock, trial, gearing, window), strict=True):
                left[c] -= int(v) - (1 - zero) * int(base[c])
    booked = [[*c, int(v)] for c, v in np.ndenumerate(left) if int(v) != 0]
    for *node, v in booked:
        clock.slack[tuple(node)] -= v
    return booked
