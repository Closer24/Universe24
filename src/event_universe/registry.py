"""The records' registry (2026-10-24, the first commit of tier (ii), the architect's design read: a record the born child's own): the live count of a family's records read from its lines (`records_of`), the records of quanta of a family (`quanta_records`), the holder of the sign's rows as (family, record) pairs in the families' order with the free row first (`rows_of`), a record's own row (`row_of`) and the sources of every row of a held family (`sourcing`); counts and labels, nothing of the law. At this head every count is the loader's (a point's records, `loader/derived.with_records`; the holder of the sign one row per record beside the free row) and every row stands in the loader's order, so every number of the run is the same as before this module; the record's index is a label no act reads, every sum over records and rows an exact integer sum in any order (ALGEBRA.md, No record reads its own write of the sign; the held write's reciprocity)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from event_universe.core.rule3 import division_forward
from event_universe.loader.derived import FamilyRule, charged, readers_of

Families = tuple[FamilyRule, ...]
Row = tuple[int, int]  # a row's owner, (family, record); the free row the holder's own (holder, 0)


def records_of(family: FamilyRule, lines: Sequence[Any]) -> int:
    """The records a family's lines hold: the lines over one record's span, the parts times the width (`records.record_slice`); a holder of the sign its rows, the free row among them; one for a held row of the volume."""
    return int(
        division_forward(len(lines), family.parts * family.width, 0)[0]
    )  # a count over a count, exact


def quanta_records(families: Families, states: Sequence[Any], index: int) -> range:
    """The records of quanta of a family, each read, stepped and booked at its own paces: every record of a family that reads a holder of the sign, the one record of every other family of quanta, a holder of the sign's one record, light, among them (its rows are rows of the sign and no records of light)."""
    return range(1 if families[index].wronskian else records_of(families[index], states[index].lines))


def rows_of(families: Families, states: Sequence[Any]) -> list[Row]:
    """The holder of the sign's rows, each the (family, record) that owns it: the free row first, the row no record owns, named by the holder itself, then every charged family's records in the families' order (ALGEBRA.md, No record reads its own write of the sign: every record its own row)."""
    found = [(index, 0) for index, family in enumerate(families) if family.held and family.wronskian]
    for index, family in enumerate(families):
        if charged(families, index):
            found.extend((index, record) for record in range(records_of(family, states[index].lines)))
    return found


def row_of(families: Families, states: Sequence[Any], index: int, record: int) -> int | None:
    """A record's own row of the holder of the sign, its position among the rows (`rows_of`); None for a record that reads no holder of the sign."""
    if not charged(families, index):
        return None
    return rows_of(families, states).index((index, record))


def sourcing(families: Families, states: Sequence[Any], held: int) -> list[list[Row]]:
    """The sources of every row of a held family, per row the (reader, record) pairs whose bookings the row's write takes (the held write's reciprocity): a holder of the volume one row sourced by every record of quanta that reads it; a holder of the sign a list per row, the free row's empty and every other row's its one owner, which reads the holder."""
    readers = readers_of(families, held)
    if not families[held].wronskian:
        return [
            [
                (reader, record)
                for reader in readers
                for record in quanta_records(families, states, reader)
            ]
        ]
    return [[row] if row[0] in readers else [] for row in rows_of(families, states)]
