"""The bookings of the records (ALGEBRA.md #the-primitives, the hold; #what-a-body-is, the four lines (a) and (c); No record reads its own write of the sign): the lines of one record of a family of quanta, light the sum of a holder of the sign's rows; a family's form D and Wronskian W per record about the step, light's form from its rows' sum (the advisor's cost); and the sources of the start row by row, the one act the engine's start and the generator share (`Lattice.start`, tools/pixel_mode.py)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from typing import Any

import numpy as np

from event_universe import node
from event_universe.core.ports import Wrap
from event_universe.features.start import Sourced
from event_universe.loader.derived import quanta_records, row_sources, weight_of

Bookings = dict[node.Sourcing, Any]  # per record of quanta its form or its Wronskian
Row = tuple[int, int]  # a held family's index and one row of it, the rows the start rests


def sources_of(families: node.Families, order: Sequence[int]) -> list[node.Sourcing]:
    """Every record of quanta of the families of quanta `order`, (family, record): the sources of the writes and the readers of the rows (`derived.quanta_records`)."""
    return [(index, record) for index in order for record in quanta_records(families, index)]


def record_lines(
    families: node.Families, index: int, record: int, lines: Sequence[node.Record]
) -> list[node.Record]:
    """The lines of one record of a family of quanta among the family's `lines`: the record's own lines (`node.record_slice`), and for a holder of the sign its one record, light, the sum of its rows (`node.rows_total`)."""
    family = families[index]
    return (
        [node.rows_total(family, lines)]
        if family.wronskian
        else list(lines[node.record_slice(family, record)])
    )


def booked_of(
    families: node.Families, index: int, bookings: list[node.Booking]
) -> tuple[Bookings, Bookings]:
    """A family of quanta's form D and Wronskian W per record from its bookings about the step (`node.form`, `node.wronskian`): one per record, keyed by the record, for the writes of the rows it sources; a holder of the sign's one form, light's, read from the sum of its rows (the advisor's cost: the holders' form is booked from the rows' sum, so the Wronskian write's balance stays exact, ALGEBRA.md, No record reads its own write of the sign), and no Wronskian."""
    family = families[index]
    forms, turns = Bookings(), Bookings()
    if family.wronskian:
        first = [node.rows_total(family, [b for first, _second in bookings for b in first])]
        second = [node.rows_total(family, [b for _first, second in bookings for b in second])]
        forms[(index, 0)], turns[(index, 0)] = node.form(first, second), 0
        return forms, turns
    for record, (first, second) in enumerate(bookings):
        forms[(index, record)] = node.form(first, second)
        turns[(index, record)] = node.wronskian(second, family.plane)
    return forms, turns


def booked_sources(
    families: node.Families,
    states: node.States,
    rows: Sequence[Row],
    holders: Sequence[Row],
    walls: dict[Row, int],
    packets: dict[Row, node.Record],
    levels: Sequence[np.ndarray],
    wrap: Wrap,
    gamma: int,
    unit: int,
) -> tuple[list[Sourced], list[Sourced]]:
    """The sources of the start at the held rows' levels given, as the hold's write books them (ALGEBRA.md #what-a-body-is, the four lines (a) and (c); the engine's start and the generator call this one act, `Lattice.start` and tools/pixel_mode.py): the levels laid into the time lines of `rows`, each a held family and one row of it (the holders of the content then every row of the holders of the sign, each added to the row's laid record `packets`, read once before the loop and never from the pass before, with its vacuum content, both levels alike), every record of quanta stepped once at the paces its read gives it there (`node.step_records`, every sign row but the record's own) and its form D = now^2 - next x before and its Wronskian read from the step's booking (`node.form`, `node.wronskian`), each row's source the sum over the records that source it (`row_sources`: every reader's records for a holder of the content, the one record that owns the row for a holder of the sign, none for its free row) of their bookings at the weight they read it with (the hold's reciprocity, `weight_of`), the form for a row sourced by the form and the Wronskian for the holder of the sign, over the write's wall E_s T (`walls`), with its pair, its rest and its reads of the content holders by position; the holders' sources then the sign rows'."""
    for (index, row), level in zip(rows, levels, strict=True):
        packet, laid = packets[(index, row)], level + families[index].rest
        line = node.record_slice(families[index], row).start
        states[index].lines[line] = replace(packet, now=packet.now + laid, before=packet.before + laid)
    forms, turns = Bookings(), Bookings()
    for index, family in enumerate(families):
        if not family.quanta:
            continue
        booked_forms, booked_turns = booked_of(
            families, index, node.step_records(index, families, states, wrap, gamma, unit)[1]
        )
        forms.update(booked_forms)
        turns.update(booked_turns)
    found: list[Sourced] = []
    content = [held for held, _row in holders]
    for index, row in rows:
        family, source = families[index], np.zeros_like(states[index].lines[0].now)
        bookings = turns if family.wronskian else forms
        for reader, record in row_sources(families, index, row):
            source = source + weight_of(index, families[reader]) * bookings[(reader, record)]
        reads = tuple((content.index(r.family), r.weight) for r in family.reads if r.family in content)
        found.append((family.write * source, family.pair, walls[(index, row)], family.rest, reads))
    return found[: len(holders)], found[len(holders) :]
