"""The acts after the step, out of the loop's module (the ledger's place (ii), the rows the loop hooks per record): the hand's check at a click on a body's set, the lifetime's end of a record at its age L, the polariser's turn of the record's pair at a body's Nodes and its set's share of the flux in the clicks' booking, and the polariser bodies' terms for the register's check; each function takes the engine (`DetectorLawSimulation` of `detector_law.py`) and is bound as its method of the same duty, so every caller, test and spy works unchanged."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from typing import TYPE_CHECKING, cast

import numpy as np

from event_universe.core.main_loop import ALIVE
from event_universe.core.rule3 import NO_READ, rule3
from event_universe.events.records import LiveRecord
from event_universe.features.crystal import CrystalOwn, CrystalStart, CrystalWrites
from event_universe.features.hand import HandStart, HandTerm, HandWrites
from event_universe.features.lifetime import LifetimeStart, LifetimeTerm, LifetimeWrites
from event_universe.features.polariser import PolariserOwn, PolariserStart, PolariserWrites
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
    """The polariser's act (features/polariser): per polariser body and per live record with a level on its Nodes, the folder's `apply` on the record's pair there (a record with one level has its second at 0), the turned pair rebound whole at those Nodes (the record continues to the far set with it); the body's own set took its share of the flux in the clicks' booking before (`_polarised`); a record with nothing on the body's Nodes is untouched, and the body's own standing record is no record of the ladder."""
    for number, term in loop.polarisers.items():
        mask = loop.block_by_number[number].mask
        for live in loop.records.values():
            im_now = np.zeros_like(live.now) if live.im_now is None else live.im_now
            if not (np.any(live.now[mask]) or np.any(im_now[mask])):
                continue
            writes = cast(
                PolariserWrites,
                function(term, PolariserStart(live.now[mask], im_now[mask]), PolariserOwn()),
            )
            now, im = live.now.copy(), im_now.copy()
            now[mask], im[mask] = writes.re, writes.im
            if live.im_now is None:
                live.im_before, live.im_remainder = np.zeros_like(im), np.zeros_like(im)
            live.now, live.im_now = now, im


def polarised(loop: DetectorLawSimulation, live: LiveRecord, detector: int, value: int) -> int:
    """The set's increment at a polariser body (the mathematician's form of the row, 2026-09-27): at the body's own set (the term's second set) the record's inward flux at the body's Ports times the sum over the body's Nodes of the second offers, div the sum of both offers, one division act on the body's totals with the remainder not kept (a body with no level of the record on its Nodes offers 0); the folder's `apply` is read on the pair as the step left it, before the stage turns it; every other detector books the flux whole."""
    number = loop.set_block.get(detector)
    if number is None:
        return value
    term = loop.polarisers.get(number)
    if term is None or loop.detector_names[detector] != term.sets[1]:
        return value
    mask = loop.block_by_number[number].mask
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
    """The crystal's act: per click of the interval at a crystal body, the folder's `apply` on the arriving record's norm and label gives the pair's declaration (its two identical labels, its norm the taken one, the crystal's clock), set on the block as the pair's giving definition from the arriving record's giver (the given family, its weight, the component and the twist, no receiver), and the body gives one record through the giving's open as an emitter does, the giving's act nested so that its writes are the giving's; the crystal itself writes nothing; the queue is emptied."""
    for number, live in loop._crystal_clicks:
        writes = cast(
            CrystalWrites,
            function(
                loop.crystals[number], CrystalStart(live.norm, live.pace, live.labels[0]), CrystalOwn()
            ),
        )
        block, giver = loop.block_by_number[number], loop.block_by_number[cast(int, live.emitter)]
        block.crystal_giving = replace(
            cast(EmitterDefinition, giver.definition.emitter),
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
    loop._crystal_clicks = []


def crystal_terms(loop: DetectorLawSimulation) -> list[tuple[str, str]]:
    """The files' terms of the crystal bodies for the register's check; a crystal body with an emitter of its own is refused by name (the row: the key declares nothing else; the pair's giving is the arriving record's family)."""
    terms: list[tuple[str, str]] = []
    for number in loop.crystals:
        if loop.block_by_number[number].definition.emitter is not None:
            raise ValueError(
                f"measured[{number}].crystal declares nothing else: a crystal body carries no emitter"
            )
        terms.append((f"measured[{number}].crystal", "the crystal"))
    return terms
