"""The striking, the clock's fourth act (ALGEBRA.md, The strike writes on the lattice): the readings at the start (every train's gearing, the unsprung hand's wind and each hand's wind at the vacuum's weight, the stopped clocks), the meshes' engagement (`engage`: every mesh once from its +a end, both ends holding a whole winding of the hand, the + fitted hand at the end the hand's lead flows into where the twist is right, the conjugate pair's selector for a sprung hand, the one-mesh read of a number at that end), the advances jammed by name (`jam`), the fittings unwound and advanced (`fittings`: the fitting's one unwind per clock from the unsprung hand, the unspringing's one unwind per end from the unwound hand, SL-S2, every unwind the one act at a list of ends, unspring.unwinds, CR-S2), the bobs' chiming (bobs.py); the advance, the exact unwind and the push they tally; the striking undone from the log at the going -1 (`strike`). The striking's one moment (CL-S2, the owner's word of 2026-10-26, 22:0x UTC by the Boss's clock, the two blind hands' cut): every reading of a hand the striking LOGS is read at the hand's notches at the tick's start (`hand_starts`, kept on the clock as `start_gears`), the sense a chime carries, the notches a chime's face shows and the push an unwind tallies at each of its ends, with the cross term of an unspringing's two moves tallied once at the engagement's own clock; the readings the striking ACTS on keep their own moment by name, the wind's fall and the exact count at an unwind and the notches an unspringing unwinds whole, read on the great clock the unwind writes, since an unwind sized on a notch the great clock no longer holds breaks the law's width; the face's notch before the turnover is the one copy of the state the turnover replaced, read at the turned-over clocks alone."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

import numpy as np

from event_universe import hands, readings
from event_universe.bobs import bobs, splits
from event_universe.core import rule3
from event_universe.core.rule3 import carries, remainder
from event_universe.core.spokes import AXES, across, spoke_of
from event_universe.draw import kept_mid, kept_pitch, vernier
from event_universe.meshes import coupling_of, train_lead, train_twists
from event_universe.phase import books, claimed, crowded, snapshot
from event_universe.run import fitting, jammed, logged
from event_universe.trains import HAND, Gear, Train
from event_universe.unspring import (
    fitted_advanced,
    fitted_notches,
    fitted_windings_of,
    read_unwinds,
    summed,
    unsprung_notches,
    unwind_ends,
)
from event_universe.unwind import advance, move, neighbour, recoil

if TYPE_CHECKING:
    from event_universe.clock import Clock


class Fitting(NamedTuple):
    """A fitting read at the meshes' engagement: the unwind's clock, the fitted hands' hand, the - fitted hand's clock, the + fitted hand's clock, the vernier's room and the unwound hand."""

    at: tuple[int, ...]
    gear_ratio: int
    minus: tuple[int, ...]
    plus: tuple[int, ...]
    room: int
    rec: int


def list_of(clock: Clock, rec: int, number: int) -> int:
    """The fitted hands' hand of an engagement of the hand `rec`, one pick for every hand (R12): the vernier's pick (the number over the winding, modulo their count) among the hands whose coupling times the unwound hand's is 0 (meshes.coupling_of): an unwound hand at the coupling 0 picks among every hand, a coupled one among the hands at the coupling 0 alone, the one hand at the spring 0, its pick modulo 1 (SL-S1: two sprung windings engaging give unsprung windings; the former branch on the unwound hand's identity, which named the unsprung hand, kept by name)."""
    all_hands = clock.hands()
    coupled = coupling_of(all_hands[rec])
    recs = [k for k, r in enumerate(all_hands) if r.size == HAND and coupled * coupling_of(r) == 0]
    return recs[int(remainder(carries(number, clock.windings[rec]), len(recs)))]


def engage(
    clock: Clock,
    rec: int,
    start: list[Gear],
    wind: Any,
    gearings: list[tuple[Gear, rule3.Gearing]],
    stopped: Any,
    other: tuple[int, Any, list[Gear]] | None = None,
) -> list[Fitting]:
    """The meshes' engagement of one hand, the same for every hand (SL-S1, the generic striking): every mesh once from its +a end; an engagement where both ends hold a whole winding of the hand at the tick's start and neither end is stopped (counted as `met`); the + fitted hand at the end the hand's own lead flows into where the twist of its transverse leads is right, at the other end where left (F = 0 and h = 0 jammed by name); a sprung hand engages as the conjugate pair alone, the two ends' sweeps of opposite sign (SL-S2's selector with no name, W_minus W_plus < 0; jammed by name `sense` where not), every sweep and the sense's refusal weighted by the hand's coupling (meshes.coupling_of, min(spring, 1): the unsprung hand's sweeps 0 and its meetings never refused by the sense, the branch on its identity a product, David's DAVID-GENERIC-ENGINE.md part B), and at rest, no lead across the mesh, as the pair at rest (MG-S1: the + fitted hand at the end whose sweep is positive, the fitting's orientation read at -1, the twist not read, its number read after the stop in `fittings`); the mesh's one number read at the lead's end names the fitted hands' hand (`list_of`; one read per clock and hand in a striking). Returns the fittings as (the unwind's clock, the fitted hands' hand, the - fitted hand's clock, the + fitted hand's clock, the vernier's room, the unwound hand)."""
    fits: list[Fitting] = []
    hand, winding = clock.hands()[rec], clock.windings[rec]
    wound = (wind >= winding) & ~stopped
    axis_leads = [clock.rim * train_lead(start, spoke_of(axis, 0)) for axis in range(AXES)]
    twists = train_twists(start)
    coupling = coupling_of(hand)
    hand_sweeps = coupling * hands.sweep(start)
    far, far_sweeps = wound, hand_sweeps
    if other is not None:
        q, q_wind, q_start = other
        far = (q_wind >= winding) & ~stopped
        axis_leads = [
            c + clock.rim * train_lead(q_start, spoke_of(axis, 0)) for axis, c in enumerate(axis_leads)
        ]
        twists = [t + u for t, u in zip(twists, train_twists(q_start), strict=True)]
        far_sweeps = hands.sweep(q_start)
    for axis in range(AXES):
        both = wound & across(far, spoke_of(axis, 0))
        for where in zip(*np.nonzero(both), strict=True):
            at = tuple(int(x) for x in where)
            j = neighbour(clock, at, spoke_of(axis, 0))
            clock.counts["met"] += 1
            if int(clock.start_factors[spoke_of(axis, 0)][at]) == 0:
                jammed(clock, at, "disengaged", link=list(j), row=rec)
                continue
            lead, h = int(axis_leads[axis][at]), int(twists[axis][at])
            w = [int(hand_sweeps[at]), int(far_sweeps[j])]
            rest = lead == 0 and w[0] * w[1] < 0
            if (lead == 0 or h == 0) and not rest:
                jammed(clock, at, "orientation" if lead == 0 else "twist", link=list(j), row=rec)
                continue
            if coupling * (w[0] * w[1] >= 0):
                jammed(clock, at, "sense", link=list(j), row=rec, charges=w)
                continue
            if rest:
                into, outof = (at, j) if w[0] > 0 else (j, at)
            else:
                into, outof = (j, at) if lead > 0 else (at, j)
            plus, minus = (into, outof) if rest or h > 0 else (outof, into)
            if other is not None:
                twins = {at: rec, j: other[0]}
                clock.twin_ends[(rec, minus, plus)] = (twins[minus], twins[plus])
            if rest:
                fits.append(Fitting(into, list_of(clock, rec, 0), minus, plus, 0, rec))
                continue
            if (into, rec) not in clock.vernier_read:
                clock.vernier_read[(into, rec)] = vernier(clock, into, gearings, winding)
            drawn = clock.vernier_read[(into, rec)]
            if drawn is None:
                continue
            number, room = drawn
            fits.append(Fitting(into, list_of(clock, rec, number), minus, plus, room, rec))
    return fits


def twin_at(
    clock: Clock, rec: int, winds: list[Any], hand_starts: list[list[Gear]]
) -> tuple[int, Any, list[Gear]] | None:
    """The hand's twin with its wind and its gears at the tick's start, where its train is twin hands."""
    twin = clock.hands()[rec].twin
    if twin is None:
        return None
    q = clock.hands().index(twin)
    return q, winds[q], hand_starts[q]


def jam(clock: Clock, fits: list[Fitting], winds: list[Any]) -> list[Fitting]:
    """The advance jammed by name: where any of the fitted hand's hand already stands at its clock, and where two fitted hands of one hand would land at one clock in one striking (the sweep made at a crowded advance); an unspringing's unsprung fitted hands (the engagement lowering the coupling: the unwound hand's coupling above the fitted hands', meshes.coupling_of; the former read of the two hands' identities kept by name, R12) pass both and read their bound on their own quantum at the unwind, the unsprung hand's winding at the end as MG-S1's wind reads it, the unsprung hand a sea the unspringing pays into (the Boss's word of 2026-10-26, 11:33 UTC, 6414995372; the standing-light bound of 4ad484eb9, which ended every merger of the record, kept by name; the fitting read at -1, MG-S1). Returns the fittings kept."""
    all_hands = clock.hands()
    inverse = [k for k in fits if coupling_of(all_hands[k.rec]) > coupling_of(all_hands[k.gear_ratio])]
    kept = []
    for at, s, minus, plus, room, rec in [k for k in fits if k not in inverse]:
        if int(winds[s][minus]) > 0 or int(winds[hands.twin_of(all_hands, s)][plus]) > 0:
            jammed(clock, at, "lay", standing=int(winds[s][minus]), unit=clock.windings[s], row=rec)
            continue
        kept.append(Fitting(at, s, minus, plus, room, rec))
    landing: dict[tuple[int, tuple[int, ...]], int] = {}
    for _at, s, minus, plus, _room, _rec in kept:
        landing[(s, minus)] = landing.get((s, minus), 0) + 1
        landing[(hands.twin_of(all_hands, s), plus)] = (
            landing.get((hands.twin_of(all_hands, s), plus), 0) + 1
        )
    crowded = [
        k
        for k in kept
        if landing[(k.gear_ratio, k.minus)] > 1
        or landing[(hands.twin_of(all_hands, k.gear_ratio), k.plus)] > 1
    ]
    for at, s, minus, plus, _room, rec in crowded:
        jammed(
            clock,
            at,
            "lay",
            children_at_one_node=max(landing[(s, minus)], landing[(hands.twin_of(all_hands, s), plus)]),
            row=rec,
        )
    return [k for k in kept if k not in crowded] + inverse


def fittings(
    clock: Clock,
    kept: list[Fitting],
    c: Any,
    factors: tuple[Any, ...],
    reads: list[tuple[Gear, rule3.Gearing]],
) -> set[tuple[int, ...]]:
    """The fittings kept, every face read before any write: every fitted hand's winding first (`fitted_windings_of`, MS-S1: what is unwound is what the advance tallies and nothing made; the gearings once per hand), then the unwinds by the case of the unwound hand's ratio, the unwound hand's gear by the fall's sign paying at its gearing (unwind.fall_of's choice, CS4-S2; the former first line kept by name): at the spring 0 one exact unwind per clock and unwound hand of its fitted hands' windings summed (the birth's case, kept by name); with a spring each fitted hand's winding paid at its own end by the hand's notches unwound whole (MG-S1: the fitting read at -1, the wind's fall read at the end's clock and its six neighbours, where alone the advance changes it, the winds read kept per striking until an unspringing writes; the mesh's number read at the unwind's clock after the stop, the vernier's jam counted there); every unwind the striking's one act at a list of ends, read whole before any write (unspring.read_ends, unwind_ends, unwinds; CR-S2, the owner's word of 2026-10-26, 06:1x UTC; the former take_at, take_line and merger_take kept by name); then each fitted hand advanced at the sweep key div 2 (`fitted`). Returns every clock an unwound fitting touched."""
    by_clock: dict[tuple[tuple[int, ...], int], list[Fitting]] = {}
    for k in kept:
        by_clock.setdefault((k.at, k.rec), []).append(k)
    all_hands = clock.hands()
    gearings = {}
    for r in {k.gear_ratio for k in kept} | {k.rec for k in kept}:
        ratio = all_hands[r].ratio
        assert ratio is not None
        gearings[r] = readings.gearing(clock, ratio, c, factors)
    own: dict[tuple[int, int, tuple[int, ...]], int] = {}
    windings = {
        k: fitted_windings_of(clock, k.gear_ratio, k.minus, k.plus, gearings[k.gear_ratio], own)
        for k in kept
    }
    start, planned = snapshot(clock), []
    winds: dict[tuple[int, tuple[int, ...]], int] = {}
    for at, rec in sorted(by_clock):
        fits = by_clock[(at, rec)]
        hand, gearing = all_hands[rec], gearings[rec]
        if hand is not clock.unsprung():
            for fit in fits:
                ends = list(zip((fit.minus, fit.plus), windings[fit], strict=True))
                twins = clock.twin_ends.get((rec, fit.minus, fit.plus))
                drawn: list[Any] = []

                def draw(at: tuple[int, ...] = at, rec: int = rec, into: list[Any] = drawn) -> Any:
                    if (at, rec) not in clock.vernier_read:  # one read per clock-node and hand
                        clock.vernier_read[(at, rec)] = vernier(clock, at, reads, clock.windings[rec])
                    into.append(clock.vernier_read[(at, rec)])
                    return into[-1]

                got = read_unwinds(clock, ends, gearing, 1, rec, draw, winds, twins)
                planned += [] if got is None else [(at, rec, [fit._replace(room=drawn[-1][1])], got, 0)]
            continue
        got = read_unwinds(
            clock, [(at, sum(sum(windings[fit]) for fit in fits))], gearing, len(fits), rec
        )
        planned += [] if got is None else [(at, rec, fits, got, 1)]
    unwound, writes, touched = [], [], set()
    for at, rec, fits, (taker, ends), light in crowded(
        clock, planned, lambda plan: claimed(clock, plan)
    ):
        clock.strikes[at] -= light
        unwound.append((at, rec, fits, summed(unwind_ends(clock, ends, taker, at))))
        writes += [(read[-1], read[0], False) for read in ends]
    for at, rec, fits, unwind in unwound:
        touched |= fitted(clock, at, fits, unwind, rec, c, factors, writes)
        clock.counts["taken"] += unwind["taken"]
        clock.counts["booked"] += unwind["booked"]
    laid = {r: readings.gearing(clock, h.ratio, c, factors) for r, h in enumerate(all_hands) if h.ratio}
    booked = books(clock, start, writes, laid)
    if booked:
        logged(clock, "books", tuple(booked[0][:-1]), booked=booked)
    return touched


def fitted(
    clock: Clock,
    at: tuple[int, ...],
    fits: list[Fitting],
    unwind: dict[str, Any],
    rec: int,
    c: Any,
    factors: tuple[Any, ...],
    writes: list[tuple[int, tuple[int, ...], bool]],
) -> set[tuple[int, ...]]:
    """One unwind's fitted hands advanced by the one advance act (unspring.fitted_advanced: the sweeping fitted hands at the sweep key div 2, an unspringing's unsprung fitted hands as the exact unwind at -1, unspring.unsprung_notches, MG-S1, each end's winding found by its clock and not by its place in the unwind's list, so the advance is order-free under the ends' naming, the comparison's bug of close.py:166-169, CL-S2), each fitting logged with its numbers, its unwind's own push among them (the Boss's 6399718139: every unwind's dP on its gear, not the striking's last), an unspringing's two ends' unwinds under `takes` and its advances under `exact_lay`. Returns the clocks touched."""
    touched = {at}
    for _at, s, minus, plus, room, _rec in fits:
        exact: list[list[int] | None] = []
        hand = clock.hands()[s]
        assert hand.ratio is not None
        if "takes" in unwind:
            windings = {
                sense: t["booked"]
                for t in unwind["takes"]
                for sense, where in ((-1, minus), (1, plus))
                if t["node"] == list(where)
            }
            notches_of = unsprung_notches(
                clock, s, windings, readings.gearing(clock, hand.ratio, c, factors), exact
            )
        else:

            def notches_of(_where: tuple[int, ...], sense: int, hand: Train = hand) -> tuple[int, ...]:
                return fitted_notches(hand, sense, clock.A, clock.B)

        advanced = fitted_advanced(clock, s, minus, plus, notches_of)
        touched |= {minus, plus}
        twin = hands.twin_of(clock.hands(), s)
        writes += [(s, minus, "takes" not in unwind), (twin, plus, "takes" not in unwind)]
        tallies = [
            recoil(clock, where, push, int(clock.start_rate[where]), 1)
            for where, push in zip((minus, plus), advanced[-1], strict=True)
        ]
        clock.counts["births"] += 1
        clock.strikes[at] += 1
        fitting(clock, at, s, (minus, plus), unwind, rec, advanced, tallies, len(fits), room, exact)
    return touched


def undo(clock: Clock, rewind_note: dict[str, Any]) -> None:
    """The strike at -1 (X2): the log since the tick's rewind note read backward, every fitting's recoils and advances and every unwind undone by the same acts at -1, the log cut back and the counters set to the rewind note's."""
    rec0 = clock.hands().index(clock.unsprung())
    untallied: set[tuple[Any, ...]] = set()
    for entry in reversed(clock.log[rewind_note["log_from"] :]):
        for *where, amount in entry.get("booked", []) if entry["event"] == "books" else []:
            clock.slack[tuple(where)] += amount
        at = tuple(entry["node"])
        if entry["event"] == "split":
            for r, moved in zip(entry["pair"], entry["moved"], strict=True):
                advance(clock, r, at, tuple(moved), -1)
            clock.slack[at] -= entry["carried"]
        if entry["event"] == "birth":
            s, (a, b) = entry["line_pair"], entry["amplitude"]
            for where, push, rate in zip(
                (entry["plus"], entry["minus"]),
                entry["dP_lay_ends"][::-1],
                entry["clock_ends"][::-1],
                strict=True,
            ):
                recoil(clock, tuple(where), push, rate, -1)
            exact = entry.get("exact_lay", [None, None])
            for where, sense, moved in zip((entry["minus"], entry["plus"]), (-1, 1), exact, strict=True):
                if moved is None:
                    p = s if sense < 0 else hands.twin_of(clock.hands(), s)
                    advance(clock, p, tuple(where), fitted_notches(clock.hands()[p], sense, a, b), -1)
                else:
                    move(clock, s, moved[0], tuple(where), -moved[1])
                    clock.slack[tuple(where)] = moved[-1]
            if "cross" in entry:
                cross = entry["cross"]
                recoil(clock, tuple(cross["node"]), cross["dP"], cross["clock"], -1)
        if entry["event"] in ("birth", "credit"):
            rec = entry.get("taken_row", rec0)
            for unwind in entry.get("takes", [entry]):
                where = tuple(unwind["node"])
                first = entry["event"] == "credit" or (where, rec, at) not in untallied
                if first:
                    untallied.add((where, rec, at))
                    recoil(clock, where, unwind["dP_take"], unwind["clock"], -1)
                if "taken_levels" in unwind:
                    advance(clock, unwind.get("hand", rec), where, tuple(unwind["taken_levels"]))
                    clock.strikes[where] += 1
                    clock.slack[where] = unwind["remainder_was"]
                    continue
                if not first:
                    continue
                toward = 1 if unwind["taker"][1] > unwind["taker"][0] else -1
                count = 0 if "laid_back" in unwind else toward * unwind["levels"]
                move(clock, rec, unwind["taken_line"], where, -count)
                clock.slack[where] = unwind["remainder_was"]
            clock.strikes[at] -= 1
    del clock.log[rewind_note["log_from"] :]
    clock.wound, clock.crossed, clock.beats, clock.reference, clock.split = rewind_note["counters"]


def strike(
    clock: Clock,
    hand_starts: list[list[Gear]],
    held: list[list[Gear]],
    going: int = 1,
    rewind_note: dict[str, Any] | None = None,
) -> None:
    """The strike in the going (X2: the undo is the strike at -1): forward the readings at the start (each hand's wind at its unscaled gearing in the regulator's winding, PM-S1), the meshes' engagement of every hand alike (SL-S1), the advances jammed by name, the fittings unwound and advanced, the bobs' chiming; backward the striking undone from the log's rewind note in the reverse order of its lines: the advances removed, an unspringing's cross term untallied at the engagement's clock, the unwound gear moved back by the unwind's own count at every unwind's clock (`taken_line`, CS4-S2; the former restore to the notch that was, which read a gear another advance of the same striking had moved and undid that advance twice, struck 2026-10-26 under CL-S2's rewind on the fed horizon piece; an unspringing's two ends under `takes`, their notches returned whole, MG-S1, and its exact advances removed), the slack, the strikes at every end and the readings' counters restored (an unspringing's ends count their strike back, left uncounted by the former undo and met by the rewind once the state's counters are compared, 2026-10-26) (RW-S1: one function with the going, the former `unclick` kept by name). `hand_starts` the hands' gears at the tick's start, `held` every train's."""
    if going == -1:
        assert rewind_note is not None
        undo(clock, rewind_note)
        return
    c = clock.start_load
    clock.start_gears = hand_starts
    clock.pitches, clock.vernier_read, clock.twin_ends = {}, {}, {}
    kept_pitch.cache_clear()
    kept_mid.cache_clear()
    stopped = readings.stopped_of(clock, c)
    read = clock.start_factors
    r_unsprung = readings.gearing_of(clock, clock.unsprung(), c, read)
    gearings = clock.read_gears(held, c, read)
    winds, hand_gearings = [], []
    for rec, r in enumerate(clock.hands()):
        assert r.ratio is not None
        hand_gearings.append(readings.gearing(clock, r.ratio, c, read))
        winds.append(hands.wind(clock, hand_starts[rec], hand_gearings[rec]))
    fits = [
        b
        for rec in range(len(clock.hands()))
        for b in engage(
            clock,
            rec,
            hand_starts[rec],
            winds[rec],
            gearings,
            stopped,
            twin_at(clock, rec, winds, hand_starts),
        )
    ]
    fitted_clocks = fittings(clock, jam(clock, fits, winds), c, read, gearings)
    splits(clock, hand_starts, (winds, hand_gearings, gearings), fitted_clocks, stopped, r_unsprung)
    bobs(clock, hand_starts, winds, fitted_clocks, stopped, r_unsprung)
