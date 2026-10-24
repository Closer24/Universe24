"""The bookings of the records (ALGEBRA.md #the-primitives, the held write; #what-a-body-is, the four lines (a) and (c); No record reads its own write of the sign): the lines of one record of a family of quanta, light the sum of a holder of the sign's rows; a family's form D and Wronskian W per record about the step, light's form from its rows' sum (the advisor's cost); and the sources of the start row by row, the one act the engine's start and the generator share (`Lattice.start`, tools/pixel_mode.py)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from typing import Any

import numpy as np

from event_universe import node, records, registry
from event_universe.features.start import Sourced
from event_universe.flux import step_records as stepped_records
from event_universe.loader.derived import weight_of

Bookings = dict[records.Sourcing, Any]  # per record of quanta its form or its Wronskian
Row = tuple[int, int]  # a held family's index and one row of it, the rows the start rests


def sources_of(
    families: records.Families, states: records.States, order: Sequence[int]
) -> list[records.Sourcing]:
    """Every record of quanta of the families of quanta `order`, (family, record): the sources of the writes and the readers of the rows (`registry.quanta_records`, the live count of each family's records)."""
    return [
        (index, record) for index in order for record in registry.quanta_records(families, states, index)
    ]


def record_lines(
    families: records.Families, index: int, record: int, lines: Sequence[records.Record]
) -> list[records.Record]:
    """The lines of one record of a family of quanta among the family's `lines`: the record's own lines (`records.record_slice`), and for a holder of the sign its one record, light, the sum of its rows (`records.rows_total`)."""
    family = families[index]
    return (
        [records.rows_total(family, lines)]
        if family.wronskian
        else list(lines[records.record_slice(family, record)])
    )


def booked_of(
    families: records.Families, index: int, bookings: list[records.Booking]
) -> tuple[Bookings, Bookings]:
    """A family of quanta's form D and Wronskian W per record from its bookings about the step (`records.form`, `records.wronskian`): one per record, keyed by the record, for the writes of the rows it sources; a holder of the sign's one form, light's, read from the sum of its rows (the advisor's cost: the holders' form is booked from the rows' sum, so the Wronskian write's balance stays exact, ALGEBRA.md, No record reads its own write of the sign), and no Wronskian."""
    family = families[index]
    forms, turns = Bookings(), Bookings()
    if family.wronskian:
        first = [records.rows_total(family, [b for first, _second in bookings for b in first])]
        second = [records.rows_total(family, [b for _first, second in bookings for b in second])]
        forms[(index, 0)], turns[(index, 0)] = records.form(first, second), 0
        return forms, turns
    for record, (first, second) in enumerate(bookings):
        forms[(index, record)] = records.form(first, second)
        turns[(index, record)] = (
            records.wronskian(first, family.plane) + records.wronskian(second, family.plane)
        )  # the Wronskian centred on the triple: the two edges' sum over the doubled wall (derived.held_write_of)
    return forms, turns


def booked_sources(
    families: records.Families,
    states: records.States,
    rows: Sequence[Row],
    holders: Sequence[Row],
    walls: dict[Row, int],
    packets: dict[Row, records.Record],
    levels: Sequence[np.ndarray],
    gamma: int,
    unit: int,
    amplitude: int,
) -> tuple[list[Sourced], list[Sourced]]:
    """The sources of the start at the held rows' levels given, as the held write's write books them (ALGEBRA.md #what-a-body-is, the four lines (a) and (c); the engine's start and the generator call this one act, `Lattice.start` and tools/pixel_mode.py; for every held holder of the sign under the rotation (`Row.rotation`, the declared act `rotation` and no form's name; `node.phase_act`, the one act `Lattice.step` takes before the lines' step) the booking is taken after the first interval's phase act at these levels, the Links' pairs the first step reads, and the phase lines are turned back to the angle 0 after it, bit for bit, so that the first write returns the rest on every turned world and, under the Lorentz form, the lattice Lorenz constraint stands from the first interval (covector.py); the booking before 2026-10-21 took the trial step at the seed angle 0 on every turned holder but the one declaring the Lorentz form, so that the first interval's turn moved the rows by the two Wronskians' difference, the bound pair's 11-cube's centre 3029 at the lay and 3596 after the first interval, ALGEBRA.md, (g) The field at rest, the start of a world, the dated clause of 2026-10-21; the numbers in CHANGELOG.md): the levels laid into the time lines of `rows`, each a held family and one row of it (the holders of the content then every row of the holders of the sign, each added to the row's laid record `packets`, read once before the loop and never from the pass before, with its vacuum content, both levels alike), every record of quanta stepped once at the paces its read gives it there (`flux.step_records`, every sign row but the record's own, the phase lines after the first interval's act with `amplitude` their X, features/phase) and its form D = now^2 - next x before and its Wronskian read from the step's booking (`records.form`, `records.wronskian`), each row's source the sum over the records that source it (`row_sources`: every reader's records for a holder of the content, the one record that owns the row for a holder of the sign, none for its free row) of their bookings at the weight they read it with (the held write's reciprocity, `weight_of`), the form for a row sourced by the form and the Wronskian for the holder of the sign, over the write's wall E_s T (`walls`), with its pair, its rest, its reads of the content holders by position and the proper-interval power of its booking (`FamilyRule.power`, the rest scaled as the write scales its source); the holders' sources then the sign rows'."""
    for (index, row), level in zip(rows, levels, strict=True):
        packet, laid = packets[(index, row)], level + families[index].rest
        line = records.record_slice(families[index], row).start
        states[index].lines[line] = replace(packet, now=packet.now + laid, before=packet.before + laid)
    forms, turns = Bookings(), Bookings()
    phased = [index for index, family in enumerate(families) if family.held and family.rotation]
    if phased:  # the first interval's phase act before its step: the booking the first write takes
        node.phase_act(phased, families, states, 1, gamma)
    for index, family in enumerate(families):
        if not family.quanta:
            continue
        booked_forms, booked_turns = booked_of(
            families,
            index,
            stepped_records(index, families, states, gamma, unit, amplitude=amplitude)[1],
        )
        forms.update(booked_forms)
        turns.update(booked_turns)
    if phased:  # the phase lines returned to the angle 0, the state the run starts from, exactly
        node.phase_act(phased, families, states, -1, gamma)
    found: list[Sourced] = []
    content = [held for held, _row in holders]
    for index, row in rows:
        family, source = families[index], np.zeros_like(states[index].lines[0].now)
        bookings = turns if family.wronskian else forms
        for reader, record in registry.sourcing(families, states, index)[row]:
            source = source + weight_of(index, families[reader]) * bookings[(reader, record)]
        reads = tuple((content.index(r.family), r.weight) for r in family.reads if r.family in content)
        found.append(
            (family.write * source, family.pair, walls[(index, row)], family.rest, reads, family.power)
        )
    return found[: len(holders)], found[len(holders) :]
