"""The acts after the step, out of the loop's module (the ledger's place (ii), the rows the loop hooks per record): the hand's check at a click on a body's set, the lifetime's end of a record at its age L, the polariser's turn of the record's pair at a body's Nodes (its angle the one in force, the switching) and its set's share of the flux in the clicks' booking, the polariser bodies' and the crystal bodies' terms for the register's check, the crystal's click and its stage (the pair record's giving, events/pair.py), and the giving's window (the write per interval, the windows' close); each function takes the engine (`DetectorLawSimulation` of `detector_law.py`) and is bound as its method of the same duty, so every caller, test and spy works unchanged."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from typing import TYPE_CHECKING, cast

import numpy as np

from event_universe.core.main_loop import ALIVE
from event_universe.core.rule3 import NO_READ, rule3
from event_universe.events import pair
from event_universe.events.records import Block, LiveRecord
from event_universe.features.crystal import CrystalOwn, CrystalStart, CrystalWrites
from event_universe.features.giving import THE_CLOSE, THE_WRITE, GivingStart
from event_universe.features.hand import HandStart, HandTerm, HandWrites
from event_universe.features.lifetime import LifetimeStart, LifetimeTerm, LifetimeWrites
from event_universe.features.polariser import PolariserOwn, PolariserStart, PolariserWrites, at
from event_universe.features.recoil import GIVING
from event_universe.loader.world import EmitterDefinition

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation


def hand_admits(loop: DetectorLawSimulation, live: LiveRecord, detector: int) -> bool:
    """The hand's check at a click on a set with a body (features/hand, the function the main loop looked up at (ii)): the taking body's spin and momentum now against the record's family's declared hand; a family with no hand, a set with no body and the face admit."""
    hand = loop.families[live.family].hand
    if hand is None or detector not in loop.set_block:
        return True
    block = loop.block_by_number[loop.set_block[detector]]
    spin = (int(block.spin[0]), int(block.spin[1]), int(block.spin[2]))
    momentum = (int(block.momentum[0]), int(block.momentum[1]), int(block.momentum[2]))
    with loop.main_loop.act(
        "the hand", "(ii)", loop._card_writes("the hand"), lambda: loop.fingerprints_of(live)
    ):
        check = loop.main_loop.function_of("the hand", "(ii)")
        writes = cast(HandWrites, check(HandTerm(hand), HandStart(spin, momentum)))
    return writes.admitted


def lifetime_stage(loop: DetectorLawSimulation, function: Callable[..., object]) -> None:
    """The lifetime's act (features/lifetime): every live record of a family with a lifetime L that the ladder did not click this interval ends on the border `lifetime` at age L, its content booked as escaped there, the record deleted whole at the interval's close as a clicked one."""
    for identity in list(loop.records):
        live = loop.records[identity]
        lifetime = loop.families[live.family].lifetime
        if lifetime is None or live.clicked or loop.lifetime_detector is None:
            continue
        writes = cast(
            LifetimeWrites, function(LifetimeTerm(lifetime), LifetimeStart(live.age, live.clicked))
        )
        if writes.ends:
            live.first_rung[loop.lifetime_detector] = loop.tick
            loop._gather_line(live, loop.lifetime_detector)
            live.clicked = True
            loop.dead.append(live.identity)


def polariser_stage(loop: DetectorLawSimulation, function: Callable[..., object]) -> None:
    """The polariser's act (features/polariser) writes nothing at its stage: the turn by the body's angle is read on the record's pair at the body's Nodes in the clicks' booking (`_polarised`, the body's own set's share) and, on a pair record, at the collapse of the label's click (events/pair.py), never written into the levels: a turn written at the body's Nodes every interval the record passes is a scatterer there (measured on the Bell world: the light reflected at the polariser, the crystal's set starved), not a polariser."""


def polarised(loop: DetectorLawSimulation, live: LiveRecord, detector: int, value: int) -> int:
    """The set's increment at a polariser body (the mathematician's form of the row, 2026-09-27): at the body's own set (the term's second set) the record's inward flux at the body's Ports times the sum over the body's Nodes of the second offers, div the sum of both offers, one division act on the body's totals with the remainder not kept (a body with no level of the record on its Nodes offers 0); the folder's `apply` is read on the pair as the step left it, before the stage turns it, with the angle in force at the body's count (the switching); a row of a rank-2 record at the rows' body books the mixed second row's share (events/pair.py); every other detector books the flux whole."""
    number = loop.set_block.get(detector)
    if number is None:
        return value
    declared = loop.polarisers.get(number)
    if declared is None or loop.detector_names[detector] != declared.sets[1]:
        return value
    block = loop.block_by_number[number]
    mask, term = block.mask, at(declared, loop.tick - block.definition.start)
    if live.pair_record is not None and pair.label_of(loop, number) == 0:
        return pair.mixed_share(loop, live, term, mask, value)
    if live.standing:
        return value
    im_now = np.zeros_like(live.now) if live.im_now is None else live.im_now
    apply = loop.register.at("the polariser", "(ii)")
    writes = cast(
        PolariserWrites, apply(term, PolariserStart(live.now[mask], im_now[mask]), PolariserOwn())
    )
    second = int(sum(writes.second.tolist()))
    whole = int(sum(writes.first.tolist())) + second
    return 0 if whole == 0 else int(rule3(NO_READ, NO_READ, 1, whole, 0, 0, value * second)[0])


def polariser_terms(loop: DetectorLawSimulation) -> list[tuple[str, str]]:
    """The files' terms of the polariser bodies for the register's check, the term's second set checked as a set on the body (the mathematician's form: the second set is the body's own); another name is refused at the load."""
    terms: list[tuple[str, str]] = []
    for number, polariser in loop.polarisers.items():
        second = polariser.sets[1]
        if (
            second not in loop.detector_names
            or loop.set_block.get(loop.detector_names.index(second)) != number
        ):
            raise ValueError(
                f"measured[{number}].polariser names {second!r} as its second set, which is no set on the body"
            )
        terms.append((f"measured[{number}].polariser", "the polariser"))
    return terms


def crystal_click(loop: DetectorLawSimulation, live: LiveRecord, detector: int) -> None:
    """The crystal's click hook (features/crystal): a click on a set whose body declares a crystal queues the pair's giving for the crystal's stage in the same interval: the body's number and the arriving record."""
    number = loop.set_block.get(detector)
    if number is not None and number in loop.crystals:
        loop._crystal_clicks.append((number, live))


def crystal_stage(loop: DetectorLawSimulation, function: Callable[..., object]) -> None:
    """The crystal's act: per click of the interval at a crystal body, the folder's `apply` on the arriving record's norm, label and clock gives the pair's declaration (its two identical labels, its norm over twice the denominator, its clock at half the rotation), set on the block as the pair's giving definition from the arriving record's giver (the given family, its weight, the component and the twist, no receiver), and the body gives one record through the giving's open as an emitter does, the record's second row made beside it (events/pair.py), the giving's act nested so that its writes are the giving's; the crystal itself writes nothing; the queue is emptied."""
    for number, live in loop._crystal_clicks:
        giver = loop.block_by_number.get(live.emitter) if live.emitter is not None else None
        given = emitter_of(giver) if giver is not None else None
        if given is None:
            continue  # a record with no giver (planted by a test) gives no pair
        clock = (live.period_numerator, live.period_denominator)
        start = CrystalStart(live.norm, live.pace, live.labels[0], clock)
        writes = cast(CrystalWrites, function(loop.crystals[number], start, CrystalOwn()))
        block = loop.block_by_number[number]
        block.crystal_giving = replace(
            given,
            clock=writes.clock,
            branches=writes.labels,
            norm=writes.norm,
            norm_denominator=writes.denominator,
            receiver=None,
        )
        with loop.main_loop.act(
            "the giving", "(ii)", loop._card_writes("the giving") | {ALIVE}, loop.fingerprints
        ):
            loop._emit(block)
            pair.make_pair(loop, loop.records[cast(int, block.window)], live)
    loop._crystal_clicks = []


def crystal_terms(loop: DetectorLawSimulation) -> list[tuple[str, str]]:
    """The files' terms of the crystal bodies for the register's check; a crystal body with an emitter of its own is refused by name (the row: the key declares nothing else; the pair's giving is the arriving record's family), as is a world with other than two polariser bodies (the pair's two labels, one side each)."""
    terms: list[tuple[str, str]] = []
    for number in loop.crystals:
        if loop.block_by_number[number].definition.emitter is not None:
            raise ValueError(
                f"measured[{number}].crystal declares nothing else: a crystal body carries no emitter"
            )
        if len(loop.polarisers) != 2:
            raise ValueError(
                f"measured[{number}].crystal needs two polariser bodies in the world, one per label of the pair record, got {len(loop.polarisers)}"
            )
        terms.append((f"measured[{number}].crystal", "the crystal"))
    return terms


def emitter_of(block: Block) -> EmitterDefinition | None:
    """The body's emitter for the giving's acts: its declared one, or on a crystal body the pair's giving definition set at the click (features/crystal)."""
    return block.definition.emitter if block.crystal_giving is None else block.crystal_giving


def window_write(loop: DetectorLawSimulation, live: LiveRecord) -> None:
    """One interval of an open window right after the record's own step (out of the loop's module, the loop's method of the same duty): the body's rotation written into the given row at the body's Nodes at both levels, now from the body's now and before from its before (a rotation is two levels, ALGEBRA.md #the-generator (d); one level alone is a kick the two-level rule doubles; the second row of a pair record at its second level, the quarter turn, the window's count and norm the first row's), the norm that left the body read as the outward flux through its outer Ports, the window's count grown and the box taking the body in; the emitter the crystal's giving definition on a crystal body."""
    block = loop.block_by_number.get(live.emitter) if live.emitter is not None else None
    ledger = live.pair_record
    if block is None or block.window != (live.identity if ledger is None else ledger.rows[0]):
        return
    emitter = emitter_of(block)
    if emitter is None or emitter.weight is None:
        return
    written = loop._giving_act(
        block, GivingStart(THE_WRITE, 0, (0, 0, 0), loop._body_levels(block), 0, (0, 0, 0)), live
    )
    if ledger is not None and live.identity == ledger.rows[1]:
        # the second row of a pair record: the first row turned by a quarter, its second level written; the outward norm and the window's count are the first row's
        if written.level is not None:
            cast(np.ndarray, live.im_now)[block.mask] += written.level
        return
    if written.level is not None:
        live.now[block.mask] += written.level
        live.before[block.mask] += emitter.weight * loop._body_levels(block, before=True)
    flux_tally = [0, 0, 0]
    flux = loop.body_outward_flux(live, block, flux_tally)
    closing = loop._giving_act(
        block,
        GivingStart(THE_CLOSE, 0, (0, 0, 0), None, flux, (flux_tally[0], flux_tally[1], flux_tally[2])),
        live,
    )
    live.outward = closing.own.outward
    live.outward_tally = list(closing.own.tally)
    live.window += 1
    if live.box is not None:
        live.box = tuple(
            (min(lo, low), max(hi, high))
            for (lo, hi), (low, high) in zip(live.box, loop.mask_box(block.mask), strict=True)
        )


def point_windows(loop: DetectorLawSimulation) -> None:
    """The point emitters' windows closed after the interval's bookings: the given record's norm, residue and wheel fixed from what left the body, the window's count and the record's box settled, the giving line written."""
    for block in loop.blocks:
        if block.window is None:
            continue
        live = loop.records.get(block.window)
        emitter = emitter_of(block)
        if live is None or emitter is None or emitter.weight is None or emitter.norm is None:
            block.window = None
            continue
        if live.clicked:
            # taken while its window was open (its own body's Node's set reading the returning light, the light clock): the window closes at the click, the record named
            loop._close_window(block, live)
            continue
        # (d) the close: the folder's close act on the outward norm summed over the window
        if loop._giving_act(
            block, GivingStart(THE_CLOSE, 0, (0, 0, 0), None, 0, (0, 0, 0)), live
        ).closed:
            loop._close_window(block, live)


def close_window(loop: DetectorLawSimulation, block: Block, live: LiveRecord) -> None:
    """The window's close (ALGEBRA.md; item 50): the writing ends, the record is named on its giving line with the window's length and the open's interval, the next excitation's count starts (the quantum moved at the open: the stock, the content and the ledger's rows as the train emitter's; the norm T from the open)."""
    emitter = emitter_of(block)
    if emitter is None:
        raise ValueError(f"the body {block.number} closes a window with no emitter declared")
    live.window_open = False
    for identity in live.pair_record.rows if live.pair_record is not None else ():
        loop.records[identity].window_open = False
    block.window = None
    if live.giving_line is not None and loop.record is not None:
        line = dict(live.giving_line)
        line["tick"] = loop.tick
        line["norm"] = live.norm
        line["pace"] = live.pace
        line["window"] = live.window
        line["outward"] = live.outward
        line["opened"] = loop.tick - live.window  # the open's interval (HOST)
        # THE GIVEN QUANTUM'S FOUR-VECTOR (ALGEBRA.md #the-primitives, #the-interval): the count 1, the space part the sign per axis of the outward flux over the window (DETECTOR)
        line["momentum"] = loop.direction_of(live.outward_tally)
        loop.record(line)
    outward = live.outward_tally
    loop._recoils.append(
        (
            block.number,
            GIVING,
            (int(outward[0]), int(outward[1]), int(outward[2])),
            (live.period_numerator, live.period_denominator),
        )
    )
    live.giving_line = None
    block.wait = 0
    if block.definition.emitter is not None and loop.stock_of(block) > 0:
        block.excitations += 1  # a crystal has no excitation of its own: it gives at a click alone
