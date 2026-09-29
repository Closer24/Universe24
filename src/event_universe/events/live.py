"""The records' making and release, out of the loop's module: the ledger's stamps for the main loop's audit, the held families' records and levels, a body's own record, a planted record for the generator's checks and the tests, a detector added by name, and a record's rows' release; each function takes the engine (`DetectorLawSimulation` of `detector_law.py`) and is bound as its method of the same duty, so every caller, test and spy works unchanged."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from event_universe.events.records import LiveRecord

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation


def fingerprints_of(
    loop: DetectorLawSimulation, *records: LiveRecord
) -> dict[str, dict[object, object]]:
    """The ledger's words of the named records and the bodies' counts, stamped for the audit: a rebound array by its identity, an integer by its value."""
    return {
        "a body's content M_k": {number: tuple(row) for number, row in enumerate(loop.held)},
        "the record's tally": {live.identity: (live.content, live.reported) for live in records},
        "the level next, the remainder": {
            live.identity: (id(live.now), id(live.before), id(live.remainder)) for live in records
        },
        "the second level": {
            live.identity: (id(live.im_now), id(live.im_before), id(live.im_remainder))
            for live in records
        },
    }


def fingerprints(loop: DetectorLawSimulation) -> dict[str, dict[object, object]]:
    """Every ledger word the main loop audits after an act, stamped: the bodies' counts, spins, positions and remainders, the records' and the held families' arrays by identity, the tallies, the paces' carries and the records alive; the momentum is a reading of the record's current (the recoil's row) and no ledger word."""
    stamps = fingerprints_of(loop, *loop.records.values(), *loop.held_component_records())
    stamps["a body's spin S"] = {b.number: (tuple(b.spin), tuple(b.spin_before)) for b in loop.blocks}
    stamps["a body's position"] = {b.number: (tuple(b.corner), id(b.mask)) for b in loop.blocks}
    stamps["the count at a Node"] = {b.number: id(b.counts) for b in loop.blocks} | {
        ("record", live.identity): id(live.counts) for live in loop.records.values()
    }
    stamps["the count's remainder"] = {b.number: id(b.count_remainder) for b in loop.blocks} | {
        ("record", live.identity): id(live.count_remainder) for live in loop.records.values()
    }
    stamps["a body's remainders"] = {
        b.number: (id(b.hold_value), b.hold_value.version, id(b.hold_carry), b.hold_carry.version)
        for b in loop.blocks
    }
    stamps["the records alive"] = dict.fromkeys(loop.records, True)
    return stamps


def held_record(loop: DetectorLawSimulation, source: str) -> LiveRecord | None:
    """The held record of the family holding `source` ("content" or "sign"), None where no family holds it; a GAMEBOARD reading by the declared attribute, never by a name."""
    for family, record in loop.held_records.items():
        if loop.families[family].held == source:
            return record
    return None


def level_of(loop: DetectorLawSimulation, source: str) -> np.ndarray:
    """The level over the board of the family holding `source` (the Node clock's c for "content", 9.45; the charge field d for "sign", 9.48), zeros where no family holds it; a GAMEBOARD reading."""
    for family in loop.held_records:
        if loop.families[family].held == source:
            return loop.node_level[family]
    return np.zeros(loop.shape, dtype=np.int64)


def massive_record(
    loop: DetectorLawSimulation,
    identity: int,
    number: int,
    family: int,
    pair: tuple[int, int],
    twist: int,
) -> LiveRecord:
    """A record of the massive kind on the board: a block's own record at the body's kind (its rest pair) with its twist "own" (ALGEBRA.md #the-primitives); no train, no clock, no Ports."""
    return LiveRecord(
        identity,
        family,
        0,
        loop.tick,
        0,
        np.zeros(loop.shape, dtype=np.int64),
        np.zeros(loop.shape, dtype=np.int64),
        np.zeros(loop.shape, dtype=np.int64),
        pair=(int(pair[0]), int(pair[1])),
        twist=twist,
    )


def planted_record(
    loop: DetectorLawSimulation,
    family: int,
    now: np.ndarray,
    before: np.ndarray,
    pair: tuple[int, int] | None = None,
    part: int = 0,
    twist: int = 0,
) -> LiveRecord:
    """A record of the family given to the rule directly, its two levels as given and its remainder 0 (the tests' device): registered in no ledger, advanced by `_advance` and read by `conserved_form` alone; `part` its component and `twist` its own rotation (commit 4)."""
    return LiveRecord(
        0,
        family,
        0,
        loop.tick,
        0,
        np.array(now, dtype=np.int64).reshape(loop.shape),
        np.array(before, dtype=np.int64).reshape(loop.shape),
        np.zeros(loop.shape, dtype=np.int64),
        pair=loop.families[family].pair if pair is None else (int(pair[0]), int(pair[1])),
        part=part,
        twist=twist,
    )


def add_detector(
    loop: DetectorLawSimulation,
    name: str,
    measured: int | None,
    face: bool,
    set_name: str | None = None,
    channel: int = 0,
) -> int:
    """One more detector of the engine, by name: its measured event, whether it is a face, its set and its channel appended to the detectors' lists; its index."""
    loop.detector_names.append(name)
    loop.detector_measured.append(measured)
    loop.detector_face.append(face)
    loop.detector_set.append(name if set_name is None else set_name)
    loop.detector_channel.append(channel)
    return len(loop.detector_names) - 1


def release(loop: DetectorLawSimulation, live: LiveRecord) -> None:
    """The record's rows leave the board: the emitters' lists drop the record."""
    for block in loop.blocks:
        if live.identity in block.emitted:
            block.emitted.remove(live.identity)
