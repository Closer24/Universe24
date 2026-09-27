"""THE PAIR RECORD in the loop (ALGEBRA.md #the-ladder, THE PAIR RECORD, THE LABELS' CLICKS and THE HALF QUANTUM; #the-primitives, the row "the crystal"): the crystal's giving as two records of one giving sharing one ledger, the rows of the 2 x 2 level (the second row the first turned by a quarter, so the level is the identity in the record's own frame), each stepped by Rule3 alone; the first polariser body of the file acts on the rows and the second on the columns, each read on the level at its own Nodes in the clicks' booking (the body's own set's share of each row's flux); each label's ladder runs over its own side's two sets on the two rows' bookings summed, with its own residue (the crystal's own for the rows' label, the arriving record's for the columns'); the first click turns the whole record by that label's angle and makes it rank 1 everywhere at once (both rows the taken row, or both levels of each row the taken column, the form kept whole) and the second click ends it; functions taking the engine, called from the hooks of after_step.py and the loop's ladder."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import numpy as np

from event_universe.core.rule3 import NO_READ, rule3
from event_universe.events.records import LiveRecord, PairRecord
from event_universe.features.polariser import PolariserTerm, at, triple_of, turned_back

if TYPE_CHECKING:
    from event_universe.events.detector_law import DetectorLawSimulation

Matrix = tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
LEVELS = (("now", "before", "remainder"), ("im_now", "im_before", "im_remainder"))


def label_of(loop: DetectorLawSimulation, number: int) -> int | None:
    """The label a polariser body acts on: the first polariser body of the file the rows' (0), the second the columns' (1), any other None."""
    numbers = list(loop.polarisers)
    return numbers.index(number) if number in numbers[:2] else None


def rows_of(loop: DetectorLawSimulation, live: LiveRecord) -> tuple[LiveRecord, LiveRecord]:
    """The two rows of a rank-2 record, the records of its ledger."""
    if live.pair_record is None:
        raise ValueError(f"the record {live.identity} is of rank 1: it has no rows")
    first, second = live.pair_record.rows
    return loop.records[first], loop.records[second]


def second_level(live: LiveRecord) -> None:
    """A record's second level and its two companions laid at 0 where it has none yet."""
    if live.im_now is None:
        live.im_now, live.im_before, live.im_remainder = (np.zeros_like(live.now) for _ in range(3))


def matrix_at(loop: DetectorLawSimulation, live: LiveRecord, mask: np.ndarray) -> Matrix:
    """The 2 x 2 level at the body's Nodes, a reading: the rows the two records' pairs (the first level, the second) there, a missing second level read as 0 and laid nowhere."""
    first, second = rows_of(loop, live)
    return tuple(
        (np.zeros_like(row.now) if row.im_now is None else row.im_now)[mask] if level else row.now[mask]
        for row in (first, second)
        for level in (0, 1)
    )


def mixed(term: PolariserTerm, matrix: Matrix) -> Matrix:
    """The rows mixed by the angle: each column's two entries turned back as one pair by the transport's exact triple (the folder's `turned_back`, the rounding the transport's)."""
    triple = triple_of(term.angle)
    first_along, second_along = turned_back(matrix[0], matrix[2], triple)
    first_across, second_across = turned_back(matrix[1], matrix[3], triple)
    return first_along, first_across, second_along, second_across


def squares(*levels: np.ndarray) -> int:
    """The sum of the squared levels over the Nodes, an exact Python integer."""
    return int(sum(int(x) * int(x) for level in levels for x in level.tolist()))


def mixed_share(
    loop: DetectorLawSimulation, live: LiveRecord, term: PolariserTerm, mask: np.ndarray, value: int
) -> int:
    """The body's own set's increment at the rows' body for a row of a rank-2 record: the row's flux times the sum over the body's Nodes of the mixed second row's squares div the sum of all four (the rows mixed by the angle first, the pair's one fraction on each row's flux, one division act, the remainder not kept)."""
    first_along, first_across, second_along, second_across = mixed(term, matrix_at(loop, live, mask))
    second = squares(second_along, second_across)
    whole = second + squares(first_along, first_across)
    return 0 if whole == 0 else int(rule3(NO_READ, NO_READ, 1, whole, 0, 0, value * second)[0])


def sides_of(loop: DetectorLawSimulation) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Each label's two sets: the first polariser body's sets the rows' label's and the second's the columns', each in its card's order (along, across); a name that is no set is left out."""
    names = loop.detector_names
    terms = list(loop.polarisers.values())[:2]
    return tuple(  # type: ignore[return-value]
        tuple(names.index(name) for name in term.sets if name in names) for term in terms
    )


def make_pair(loop: DetectorLawSimulation, first: LiveRecord, arriving: LiveRecord) -> LiveRecord:
    """The pair at the crystal's giving: the given record is the first row; the second row is a record of the same ledger with the next identity, its levels 0 (the window writes its second level, the first row turned by a quarter), its residue and wheel the arriving record's (the columns' label's, the two residues read at the crystal's Node), its content 0 in the family's unit (the pair's one quantum is on the first row's line, each label's unit the half); both rows share one pair ledger."""
    identity, loop.next_identity = loop.next_identity, loop.next_identity + 1
    now, before, remainder, im_now, im_before, im_remainder = (
        np.zeros_like(first.now) for _ in range(6)
    )
    second = replace(
        first,
        identity=identity,
        u=arriving.u,
        wheel=arriving.wheel,
        content=0,
        now=now,
        before=before,
        remainder=remainder,
        im_now=im_now,
        im_before=im_before,
        im_remainder=im_remainder,
        pointers=[0] * len(first.pointers),
        first_rung=[None] * len(first.first_rung),
        momentum_tally={},
        carry={},
        outward_tally=[0, 0, 0],
        giving_line=None,
    )
    loop.records[identity] = second
    ledger = PairRecord((first.identity, identity), sides_of(loop), [0] * len(first.pointers))
    first.pair_record = second.pair_record = ledger
    return second


def term_of(loop: DetectorLawSimulation, label: int) -> PolariserTerm:
    """The label's polariser term in force at this interval (the switching read at the click, the body's own count)."""
    number = list(loop.polarisers)[label]
    block = loop.block_by_number[number]
    return at(loop.polarisers[number], loop.tick - block.definition.start)


def turn_whole(term: PolariserTerm, first: LiveRecord, second: LiveRecord, label: int) -> None:
    """The label's turn on the whole record at the click, everywhere at once: at the rows' label the two rows mixed by the angle (each column's pair of entries turned back), at the columns' label each row's pair turned back; on the two levels now and before alike (the leapfrog's pair), the remainders as they are (the transport's rounding, not kept)."""
    triple = triple_of(term.angle)
    for row in (first, second):
        second_level(row)
    for name, im in zip(LEVELS[0][:2], LEVELS[1][:2], strict=True):
        if label == 0:
            for level in (name, im):
                along, across = turned_back(getattr(first, level), getattr(second, level), triple)
                setattr(first, level, along)
                setattr(second, level, across)
            continue
        for row in (first, second):
            along, across = turned_back(getattr(row, name), getattr(row, im), triple)
            setattr(row, name, along)
            setattr(row, im, across)


def collapse(loop: DetectorLawSimulation, live: LiveRecord, label: int, index: int) -> None:
    """The click's one non-local act on the pair (ALGEBRA.md #the-ladder): the record turned by the label's angle and rank 1 everywhere at once; at the rows' label both rows become the taken row of the turned matrix (the other label's pair the taken row's, the form kept whole), at the columns' label both levels of each row become the taken column."""
    first, second = rows_of(loop, live)
    turn_whole(term_of(loop, label), first, second, label)
    if label == 0:
        source, target = (first, second) if index == 0 else (second, first)
        for name in (*LEVELS[0], *LEVELS[1]):
            setattr(target, name, getattr(source, name).copy())
        target.box = source.box
        return
    for row in (first, second):
        for kept, other in zip(LEVELS[index], LEVELS[1 - index], strict=True):
            setattr(row, other, getattr(row, kept).copy())


def pair_click(loop: DetectorLawSimulation, live: LiveRecord, increments: list[int]) -> None:
    """The labels' clicks (ALGEBRA.md #the-ladder, THE LABELS' CLICKS): each row's bookings join the ledger; once both rows booked this interval, each label not yet clicked runs the clicks' ladder over its own side's sets in the record's order on the summed bookings, with its row's residue, norm, wheel and total; a click takes the set's row or column (the first set along, the second across), the collapse as the polariser's act nested (its writes the levels), the first rung, the rung's count, the click line and the recoil on that label's row; after the second label's click both rows end as a clicked record does."""
    ledger = live.pair_record
    if ledger is None:
        raise ValueError(f"the record {live.identity} is of rank 1: no pair clicks")
    for detector, increment in enumerate(increments):
        ledger.pending[detector] += increment
    ledger.booked += 1
    if ledger.booked < 2:
        return
    click = loop.main_loop.function_of("the clicks", "(ii)")
    for label, row in enumerate(rows_of(loop, live)):
        if ledger.clicked[label]:
            continue
        side = ledger.sides[label]
        ladder = [detector for detector in loop._ladder_of(row) if detector in side]
        detector, row.total = click(
            row.u, row.norm, row.wheel, row.pace, row.total, ladder, ledger.pending
        )
        if detector is None:
            continue
        with loop.main_loop.act(
            "the polariser", "(ii)", loop._card_writes("the polariser"), loop.fingerprints
        ):
            collapse(loop, live, label, side.index(detector))
        row.first_rung[detector] = loop.tick
        if detector in loop.set_block:
            block = loop.block_by_number[loop.set_block[detector]]
            loop.rung_counts[(row.identity, detector)] = loop._body_count(block)
        loop._gather_line(row, detector)
        loop._recoil_at_taking(row, detector)
        ledger.clicked[label] = True
    ledger.pending = [0] * len(ledger.pending)
    ledger.booked = 0
    if all(ledger.clicked):
        for row in rows_of(loop, live):
            row.clicked = True
            loop.dead.append(row.identity)
