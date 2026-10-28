"""The unspringing at rest, MG-S1 (H-Merger-At-Rest-1, 2026-10-26, the Boss's order under the owner's delegation; the former CS8-S1 and CS8-S2 as one letter): a fitted hand's winding is its own quantum, the wind its notches (A, 0 | 0, +-B) hold alone at the clock under its train's gearing, the same two integers for every train (`fitted_windings_of`; the former board's increment kept by name, equal to it on an empty hand); a sprung hand whose two ends hold a whole winding each of opposite sweep with no lead across the mesh engages as the conjugate pair (striking.engage's rest branch); each fitted hand's winding is paid at its own end by the unwound hand's notches at that clock unwound whole by the one advance act at -1, the fall the wind the great clock loses, both ends read before either is written, jammed by name `stop` where an end's fall is below the winding (`merger_falls`, `merger_take`; the mesh's number read after the stop, so a stopped pair reads nothing on the vernier); the unsprung hand is advanced at each end as the exact unwind at -1, on the gear the unwind names, by the least count of notches at which the wind rises by the winding (fall_of at -1; the former rise_of kept by name), the notches of that advance `unsprung_notches`, the two fitted hands' advance one act for the unsprung and the sweeping fitted hand alike (`fitted_advanced`). The striking's one unwind act for every letter (CR-S1 and CR-S2, the owner's word of 2026-10-26, 06:1x UTC): the ends read before any is written (`read_ends`), then written (`unwind_ends`), the fitting's one end, the bob's one end and the unspringing's two alike (`unwinds`, `summed`)."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import hands
from event_universe.core import acts, rule3
from event_universe.core.spokes import AXES
from event_universe.meshes import coupling_of
from event_universe.trains import HAND, Gear, Train, zeros
from event_universe.unwind import advance, move, push_of, recoil, window_clocks

if TYPE_CHECKING:
    from event_universe.clock import Clock


def fitted_notches(hand: Any, sense: int, a: int, b: int) -> tuple[int, ...]:
    """A fitted hand's notches at one end, now and before per gear of the hand: the one advance of the law at the unit (hands.moving, MV-S1's form; the setting's rest advance the same advance at the train's own ratio), the now pair (sense A, 0) and the before pair (0, sense B) at the quarter turn along the vector (1, 0, ...), so three_now sense A and twelve_before B (GP-S1's two integers, A B = key div 2) and 0 on every other notch; the former plane-typed four and the child's own spelling kept by name (the Boss's 6414464356: the rest advance and child_at one advance)."""
    gears = hands.moving(1, (sense * a, 0), (0, sense * b), 1, sense)
    return tuple(int(x) for gear in gears for x in (gear.now, gear.before))


def fitted_advanced(
    clock: Clock,
    s: int,
    minus: tuple[int, ...],
    plus: tuple[int, ...],
    notches_of: Callable[[tuple[int, ...], int], tuple[int, ...]],
) -> tuple[list[int], list[int], list[list[int]], list[list[int]]]:
    """The two fitted hands advanced by the one advance act, the - fitted hand at the - end and the + fitted hand at the + end, each end's notches by `notches_of` at the end and its sense (the sweeping fitted hand's fitted_notches at the sweep key div 2 with the sweep's sign on the three gear, GP-S1, the owner's word of 2026-10-26, 04:3x UTC; an unspringing's unsprung windings the exact unwind at -1, `unsprung_notches`, MG-S1), each advance's push tallied over the hand's gears at its clock before it is advanced (push_of, the Boss's 6413599502 (b)), the second end read on the great clock the first advance changed (the sum exact); the former child_at, close.child_laid and light_children one function (NL-S1's stroke 4, 2026-10-26). Returns the advances' push summed and per end (dP_lay_ends, the J hands' key, AJ-S2), each fitted hand's sweep at its clock (its sense, the owner's word 3; -+(key div 2) where the hand stood at nothing) and the hand's notches at each clock before the advance (the residue)."""
    twins = (s, hands.twin_of(clock.hands(), s))
    hand = clock.hands()[s]
    assert hand.ratio is not None
    stood = [stood_at(clock.hands()[p], minus, plus)[k] for k, p in enumerate(twins)]
    ends = []
    for where, sense, p in ((minus, -1, twins[0]), (plus, 1, twins[1])):
        notches = notches_of(where, sense)
        ends.append(push_of(clock, clock.hands()[p].gears, where, notches, hand.ratio[0]))
        advance(clock, p, where, notches)
    senses = [senses_at(clock.hands()[p], minus, plus)[k] for k, p in enumerate(twins)]
    return [a + b for a, b in zip(*ends, strict=True)], senses, stood, ends


def fall_of(
    clock: Clock, at: tuple[int, ...], windings: int, r: rule3.Gearing, hand: Train, going: int = 1
) -> tuple[int | None, int, int]:
    """The exact unwind at the clock in the regulator's winding (PM-S1) on the gear the fall's sign chooses (CS4-S2: the unwound hand's gear whose notch now stands farthest from its before, the largest now^2 - before^2, the first gear where equal, covariant under the hand's quarter turn): the unwound gear's now moved toward its before by the least count of notches, by comparisons alone (rule3.least_at), at which the wind the clock and its six neighbours hold falls by the windings due (EX-S1, the owner's word of 2026-10-27, 15:5x UTC: the wind's own fall, as the sprung unwind reads it, where TC-S1's closed form carried the pull's sign reversed and booked a fall the great clock never lost; the closed form struck); 0 where nothing is due; (None, the full fall) where the full move pays less; at -1 the gear's now moved away from its before by the least count at which the wind rises by the windings, the unspringing's unsprung windings (MG-S1)."""
    gaps = [n * n - b * b for n, b in ((int(z.now[at]), int(z.before[at])) for z in hand.gears)]
    k = gaps.index(max(gaps))
    gear = hand.gears[k]
    now, before = int(gear.now[at]), int(gear.before[at])
    if windings <= 0 and going == 1:
        return 0, 0, k
    if now == before and going == 1:
        return None, 0, k
    t = (1 if before > now else -1) if going == 1 else (1 if now > before else -1)
    window = window_clocks(clock, at)
    base = sum(int(v) for v in hands.wind(clock, hand.gears, r, window))

    def fall(s: int) -> int:
        moved = gear.now.copy()
        moved[at] = now + t * s
        trial = [Gear(moved, g.before, g.fine, g.teeth) if g is gear else g for g in hand.gears]
        return going * (base - sum(int(v) for v in hands.wind(clock, trial, r, window)))

    if going == -1:
        s = rule3.least_at(lambda c: fall(c) >= windings)
        return s, fall(s), k
    dist = abs(now - before)
    if fall(dist) < windings:
        return None, fall(dist), k
    s = rule3.least_at(lambda c: c >= dist or fall(c) >= windings)
    return s, fall(s), k


def unsprung_notches(
    clock: Clock, s: int, windings: dict[int, int], gearing: rule3.Gearing, exact: list[list[int] | None]
) -> Callable[[tuple[int, ...], int], tuple[int, ...]]:
    """An unspringing's unsprung windings at an end (MG-S1), the notches its advance names: the exact unwind at -1 (fall_of at -1; the former rise_of kept by name) on the gear the unwind names, the count of notches at which the wind rises by the fitted hand's winding at that end (`windings` by the sense), advanced on that gear's now alone, at both ends (the unsprung advance is never the fitted hand's advance, which carries the sweep; the former `d == 0` branch the bug of H-Children-Charge-Bug-1, struck 2026-10-26), the exact advance [gear, count, rise] appended to `exact`; the end's sense enters no notch of the unsprung windings (H-Matter-From-The-Floor's bug (a), open: the unspringing's orientation reaching the great clock)."""
    hand = clock.hands()[s]

    def notches_of(where: tuple[int, ...], sense: int) -> tuple[int, ...]:
        count, rise, k = fall_of(clock, where, windings[sense], gearing, hand, -1)
        assert count is not None
        z, slack_was = hand.gears[k], int(clock.slack[where])
        d = count * (1 if int(z.now[where]) > int(z.before[where]) else -1)
        clock.slack[where] = slack_was - (rise - windings[sense])
        exact.append([k, d, rise, slack_was])
        return tuple(d if j == HAND * k else 0 for j in range(HAND * len(hand.gears)))

    return notches_of


def fitted_windings_of(
    clock: Clock,
    s: int,
    minus: tuple[int, ...],
    plus: tuple[int, ...],
    gearing: rule3.Gearing,
    own: dict[tuple[int, int, tuple[int, ...]], int],
) -> tuple[int, int]:
    """Each fitted hand's winding, its own quantum (MG-S1, CS8-S2): the fitted hand advanced by the one advance act at its end on the train's count of zero gears (the train's gears held and put back), the wind summed under the train's gearing at the great clock's load over the end and its six neighbours (hands.wind at that window: the zero gears' wind is 0 everywhere else), the gears discarded; the same two integers for every train and every clock of one load, read once per end and train in a striking (`own`: no gear of the great clock enters it); the former reading, the board's increment where the plane already stands, kept by name."""
    hand = clock.hands()[s]
    held, found = hand.gears, []
    for where, sense in ((minus, -1), (plus, 1)):
        if (s, sense, where) not in own:
            hand.gears = [
                Gear(zeros(clock.size), zeros(clock.size), gear.fine, gear.teeth) for gear in held
            ]
            advance(clock, s, where, fitted_notches(hand, sense, clock.A, clock.B))
            window = sorted(set(window_clocks(clock, where)))
            own[(s, sense, where)] = sum(int(v) for v in hands.wind(clock, hand.gears, gearing, window))
        found.append(own[(s, sense, where)])
    hand.gears = held
    return found[0], found[1]


def wind_fall(
    clock: Clock,
    rec: int,
    gearing: rule3.Gearing,
    where: tuple[int, ...],
    notches: tuple[int, ...],
    cache: dict[tuple[int, tuple[int, ...]], int],
) -> int:
    """The wind the great clock loses by an advance at -1 of the notches at the clock (advanced and returned): the advance changes the wind at the clock and its six neighbours alone, so the fall is their winds' difference, bit for bit the great clock's (the former read of the whole board's share, kept by name); the winds as read kept in `cache` per hand and clock for the striking until an unwind writes, read on the whole great clock at once where the window holds a clock not yet read."""
    hand, window = clock.hands()[rec], sorted(set(window_clocks(clock, where)))
    if any((rec, at) not in cache for at in window):
        whole = hands.wind(clock, hand.gears, gearing)
        cache.update({(rec, at): int(v) for at, v in np.ndenumerate(whole)})
    before = sum(cache[(rec, at)] for at in window)
    advance(clock, rec, where, notches, -1)
    after = sum(int(v) for v in hands.wind(clock, hand.gears, gearing, window))
    advance(clock, rec, where, notches, 1)
    return before - after


def notches_at(hand: Any, where: tuple[int, ...]) -> tuple[int, ...]:
    """A hand's notches at the clock as one advance names them (now, before per gear)."""
    return tuple(int(a[where]) for gear in hand.gears for a in (gear.now, gear.before))


def read_ends(
    clock: Clock,
    ends: list[tuple[tuple[int, ...], int]],
    gearing: rule3.Gearing,
    cause: int,
    rec: int,
    cache: dict[tuple[int, tuple[int, ...]], int] | None = None,
    twins: tuple[int, int] | None = None,
) -> list[Read] | None:
    """The unwind act's reads (CR-S2, the owner's word of 2026-10-26, 06:1x UTC: every end read before any is written, jammed by name `stop` at the first that cannot pay, the first end's jam sparing the second's read): every end owes the windings tallied less the slack there weighted by the hand's coupling's complement (meshes.coupling_of, a product: the slack whole at the coupling 0, EX-S1, and 0 at the coupling 1, MG-S1's end owing the whole winding; the former branch on the hand's identity kept by name, R12); at the unsprung hand its gear by the fall's sign is read for the least count paying it (`fall_of`); at a sprung hand the end's notches are read whole with the wind the great clock loses by their advance at -1 (`wind_fall`, MG-S1, the fitting read at -1), owing the winding. Returns per end (the clock, the windings tallied, the notches or the count, the fall, the gear or None, the slack before, the due), or None; the former merger_falls kept by name."""
    found = []
    for end, (where, tallied) in enumerate(ends):
        r = rec if twins is None else twins[end]
        hand = clock.hands()[r]
        slack_was = (1 - coupling_of(hand)) * int(clock.slack[where])
        due = tallied - slack_was
        if hand is not clock.unsprung():
            notches: Any = notches_at(hand, where)
            fall, k = wind_fall(clock, r, gearing, where, notches, {} if cache is None else cache), None
            short = fall < tallied
        else:
            notches, fall, k = fall_of(clock, where, due, gearing, hand)
            short = notches is None
        if short:
            clock.counts["refused_stop"] += cause
            entry = {"event": "refused", "i": clock.ticks, "node": list(where), "cause": "stop"}
            clock.log.append(entry | {"fall": fall, "walls": tallied, "owed": due, "row": rec})
            return None
        found.append((where, tallied, notches, fall, k, slack_was, due, r))
    return found


Read = tuple[tuple[int, ...], int, Any, int, int | None, int, int, int]


def unspring_end(
    clock: Clock, rec: int, read: Read, own: list[Gear]
) -> tuple[dict[str, Any], list[int]]:
    """One end of an unspringing's unwind written: its whole notches advanced at -1, the end's entry with the push the start tallies and its recoil, and the push read on the tick's start board with the unwind's own earlier ends unwound (`own`) less the start's: the cross term of its own ends alone, no other unwind's move in it, so the click's order enters nothing (David's DAVID-THE-STRIKES-ORDER.md); the remainder raised by the fall above the tally, an increment, so two writes at one clock commute."""
    where, tallied, notches, fall, _k, _slack_was, _due, r = read
    hand = clock.hands()[r]
    assert hand.ratio is not None
    live = push_of(clock, own, where, notches, hand.ratio[0], -1)
    push = push_of(clock, clock.start_gears[r], where, notches, hand.ratio[0], -1)
    at = zeros(clock.size) != 0
    at[where] = True
    own[:] = [
        Gear(
            np.where(at, acts.advance(g.now, now, -1), g.now),
            np.where(at, acts.advance(g.before, before, -1), g.before),
            g.fine,
            g.teeth,
            g.dfine,
            g.dteeth,
        )
        for g, now, before in zip(own, notches[0::HAND], notches[1::HAND], strict=True)
    ]
    advance(clock, r, where, notches, -1)
    clock.strikes[where] -= 1
    size, slack_was = sum(abs(x) for x in notches), int(clock.slack[where])
    clock.slack[where] += fall - tallied
    entry = dict(
        node=list(where),
        taken=fall,
        booked=tallied,
        levels=size,
        taken_levels=list(notches),
        remainder_was=slack_was,
        remainder=int(clock.slack[where]),
        **({} if r == rec else {"hand": r}),
        dP_take=push,
        **recoil(clock, where, push, int(clock.start_rate[where]), 1),
    )
    return entry, [a - b for a, b in zip(live, push, strict=True)]


def unsprung_end(clock: Clock, rec: int, read: Read) -> dict[str, Any]:
    """One end of the unsprung hand's unwind written: the unwound gear moved toward its before by the count (unwind.move, CR-S1), the fall above what was due its new slack (EX-S1), the push tallied at the gears of the tick's start (CL-S2, the one moment of every unwind, the owner's word of 2026-10-27, 15:5x UTC) and its recoil."""
    where, tallied, notches, fall, k, _slack_was, due, _r = read
    hand = clock.hands()[rec]
    assert hand.ratio is not None and k is not None
    z = hand.gears[k]
    now, before = int(z.now[where]), int(z.before[where])
    toward = 1 if before > now else -1
    move(clock, rec, k, where, toward * notches)
    clock.strikes[where] += 1
    slack_was = int(clock.slack[where])
    clock.slack[where] += fall - tallied
    clock.last_push = push_of(
        clock, [clock.start_gears[rec][k]], where, (toward * notches, 0), hand.ratio[0]
    )
    clock.last_recoil = recoil(clock, where, clock.last_push, int(clock.start_rate[where]), 1)
    return {
        "node": list(where),
        "taken": fall,
        "booked": tallied,
        "levels": notches,
        "taken_now_was": now,
        "taker": [now, before, notches],
        "dP_take": clock.last_push,
        "taken_line": k,
        "remainder_was": slack_was,
        "remainder": int(clock.slack[where]),
        "owed": due,
        **clock.last_recoil,
    }


def unwind_ends(
    clock: Clock,
    reads: list[Read],
    rec: int,
    at: tuple[int, ...] | None = None,
) -> list[dict[str, Any]]:
    """The unwind act's writes after its reads (CR-S2): at the unsprung hand the end's gear moved toward its before by the count (unwind.move, CR-S1), the fall above what was due its new slack (EX-S1), the push tallied; at a sprung hand the end's notches unwound whole by the advance act at -1, the push each end tallies read at the hand's notches at the tick's start (clock.start_gears, CL-S2: so the two ends of one mesh commute and the per-clock attribution does not depend on the order the engagement named them) and the cross term of the two moves, the live great clock's sum less the start's, nonzero on the mesh's own axis alone, tallied once at the engagement's own clock `at` after both ends, the two-ended unwind's alone, an unspringing's (the notches unwound whole keep their moment, the great clock the unwind writes, MG-S1; the former third read of the hand's identity, implied by the engagement's clock and the two ends, kept by name, R12). Returns each end's unwind as the log carries it, the cross under the last end's `cross` for `summed` to lift; the former take_line and merger_take kept by name."""
    hand = clock.hands()[rec]
    found: list[dict[str, Any]] = []
    cross = [0] * AXES
    own = {read[-1]: [gear.copy() for gear in clock.start_gears[read[-1]]] for read in reads}
    for read in reads:
        if hand is not clock.unsprung():
            entry, moved = unspring_end(clock, rec, read, own[read[-1]])
            cross = [c + m for c, m in zip(cross, moved, strict=True)]
            found.append(entry)
            continue
        found.append(unsprung_end(clock, rec, read))
    if at is not None and len(found) > 1:
        tally = recoil(clock, at, cross, int(clock.start_rate[at]), 1)
        found[-1]["cross"] = {"node": list(at), "dP": cross, **tally}
    return found


def read_unwinds(
    clock: Clock,
    ends: list[tuple[tuple[int, ...], int]],
    gearing: rule3.Gearing,
    cause: int,
    rec: int | None = None,
    draw: Callable[[], Any] | None = None,
    cache: dict[tuple[int, tuple[int, ...]], int] | None = None,
    twins: tuple[int, int] | None = None,
) -> tuple[int, list[Read]] | None:
    """The unwind's reads alone (CR-S2), the unwound hand (the unsprung hand's where none is named: a bob's unwind) with every end read before any is written (`read_ends`) and jammed by name at the first that cannot pay, the mesh's number read on the vernier after the reads where the letter reads one (`draw`, the unspringing's; None read jams the unwind); a click reads every unwind of its phase so before it writes any (the order-free click, David's DAVID-THE-STRIKES-ORDER.md: every take read on the one board the phase starts from). Returns the unwound hand and the reads, or None."""
    unwound = clock.hands().index(clock.unsprung()) if rec is None else rec
    reads = read_ends(clock, ends, gearing, cause, unwound, cache, twins)
    if reads is None or (draw is not None and draw() is None):
        return None
    return unwound, reads


def unwinds(
    clock: Clock,
    ends: list[tuple[tuple[int, ...], int]],
    gearing: rule3.Gearing,
    cause: int,
    rec: int | None = None,
) -> list[dict[str, Any]] | None:
    """The one unwind act read and written at once, for a click whose phase holds it alone (the split hand's chime): `read_unwinds`, then the writes (`unwind_ends`). Returns each end's unwind, or None."""
    read = read_unwinds(clock, ends, gearing, cause, rec)
    return None if read is None else unwind_ends(clock, read[1], read[0])


def summed(found: list[dict[str, Any]]) -> dict[str, Any]:
    """One unwind's numbers as the log carries them: one end's own fields; two ends' summed, each end's own under `takes` (an unspringing's whole notches as the unwound and the unwinder, no gear), the cross term's tally lifted from the last end under `cross` (CL-S2)."""
    if len(found) == 1:
        return {k: v for k, v in found[0].items() if k != "node"}
    whole = "taken_levels" in found[0]
    cross = found[-1].get("cross")
    if cross is not None:
        del found[-1]["cross"]
    return {
        **({} if cross is None else {"cross": cross}),
        "taken": sum(t["taken"] for t in found),
        "booked": sum(t["booked"] for t in found),
        "levels": sum(t["levels"] for t in found),
        "taken_now_was": [t["taken_levels" if whole else "taken_now_was"] for t in found],
        "taker": [t["taken_levels" if whole else "taker"] for t in found],
        "dP_take": [sum(x) for x in zip(*(t["dP_take"] for t in found), strict=True)],
        "taken_line": [None if whole else t["taken_line"] for t in found],
        "takes": found,
    }


def stood_at(hand: Any, minus: tuple[int, ...], plus: tuple[int, ...]) -> list[list[int]]:
    """The hand's notches as they stood at the two ends, now and before per gear in the train's order (the log's `stood`; generic in the gears)."""
    return [[int(x[w_]) for gear in hand.gears for x in (gear.now, gear.before)] for w_ in (minus, plus)]


def senses_at(hand: Any, minus: tuple[int, ...], plus: tuple[int, ...]) -> list[int]:
    """The hand's sweep at the two ends after the advance (hands.sweep, the hand's Wronskian three_now twelve_before - twelve_now three_before; generic in the gears), the fitted hands' W as the log names it."""
    sweep = hands.sweep(hand.gears)
    return [int(sweep[w_]) for w_ in (minus, plus)]
