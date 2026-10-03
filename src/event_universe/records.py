"""The records' lines and the sign's rows (ALGEBRA.md #the-count-is-the-records-share; No record reads its own write of the sign): a line of dimension one over the GameBoard, the lines of one record of a family (its bodies each a record where the family reads a holder of the sign), light as the sum of a holder of the sign's rows, the sum of every row but the reader's own, and the readings of the lines kept nowhere, the form, the Wronskian, the well, the write's factor, the turn's factor and the one write's numerators row by row; every one a pure function of arrays, no state of its own."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.rule3 import NO_READ, rule3
from event_universe.features import currents
from event_universe.features.write import carried
from event_universe.loader.derived import FamilyRule, HeldWrite, row_sources, weight_of

Rulers = tuple[Any, tuple[Any, Any, Any]]  # a read's paces at every Node: the clock p_0, each axis's p_a
Families = tuple[FamilyRule, ...]  # the families as the loader derived them, in the file's order


@dataclass
class NodeState:
    """A family's NodeState at every Node, the law's numbers and nothing else (ALGEBRA.md #the-postulates): its lines, each a record of dimension one (two levels and Rule3's remainder), one shape for every family, and per held line the one remainder of its write. A family of quanta's lines are its record, one line (dimension 1) or two (a plane, re and im); a held row's lines are its sources' count, the time line and, where the tensions source it, the three axis lines; the holder of the sign's one line is its record, light. Its count, currents, tension, form and Wronskian are readings of the lines (share.py, features/currents, `form`, `wronskian`) and stand nowhere."""

    lines: list[Record]
    write_remainders: list[np.ndarray]


States = list[NodeState]  # every family's NodeState, in the families' order


@dataclass(frozen=True)
class Record:
    """One line of dimension one over the GameBoard: the level now, the level before and the remainder r at every Node."""

    now: np.ndarray
    before: np.ndarray
    remainder: np.ndarray


Booking = tuple[list[Record], list[Record]]  # the lines the form and the Wronskian are read from


def level_at(record: Record, direction: int) -> np.ndarray:
    """The level a step in `direction` starts from: the level now forward (+1), the level before backward (-1), the one the state after the interval still holds (ALGEBRA.md #the-direction)."""
    return record.now if direction == 1 else record.before


def record_slice(family: FamilyRule, record: int) -> slice:
    """The lines of one record of a family, laid as records in the world's order: the record's parts, each of the family's width (a plane's two lines, a real line); for a holder of the sign the lines of one row, its time line with its odd lines under the rotation (ALGEBRA.md, No record reads its own write of the sign)."""
    span = family.parts * family.width
    return slice(record * span, (record + 1) * span)


def light_record(family: FamilyRule, lines: Sequence[Record], direction: int = 1) -> Record:
    """A holder of the sign's record, light: the sum of its rows' time lines at every Node, both levels (a detector or a body reads the sum of all rows, ALGEBRA.md, No record reads its own write of the sign), the remainder the free row's; the row's own line where it has one row, bit for bit."""
    rows = [lines[row * family.width] for row in range(family.records)]
    if len(rows) == 1:
        return rows[0]
    now: Any = sum(row.now for row in rows)
    before: Any = sum(row.before for row in rows)
    return Record(np.asarray(now), np.asarray(before), rows[0].remainder)


def row_levels(
    family: FamilyRule, lines: Sequence[Record], line: int, direction: int, skip: int | None
) -> Any:
    """The level of a holder of the sign's line `line` (0 its time line, 1 + a its odd line a) summed over every row but `skip`, the reader's own (ALGEBRA.md, No record reads its own write of the sign: a record's read and its turn take the sum of every sign row but its own), at the level the step in `direction` starts from; every row where the reader owns none; a holder of the content, one row, its one line."""
    total: Any = 0
    for row in range(family.records):
        if row != skip:
            total = total + level_at(lines[row * family.width + line], direction)
    return total


def form(begun: Sequence[Record], stepped: Sequence[Record]) -> Any:
    """The record's form at every Node over one interval, D_i = now^2 - next x before from the three levels around the step summed over its lines (`begun` holds (now, before) at the interval's start, `stepped` holds next as its `now`): the source of the rows that hold the content."""
    total: Any = 0
    for before, after in zip(begun, stepped, strict=True):
        total = total + (before.now * before.now - after.now * before.before)
    return total


def wronskian(lines: Sequence[Record], plane: bool) -> Any:
    """The Wronskian of a plane's two lines at every Node, W_i = re_now im_before - im_now re_before, the booking of the rotation sense, the charge density, summed over the record's planes: the source of the row that holds the sign; the integer 0 for a record of real lines (one line, or the pair family's two never summed at a Node), which has no plane (ALGEBRA.md #a-familys-declaration)."""
    if not plane:
        return 0
    total: Any = 0
    for re, im in zip(lines[0::2], lines[1::2], strict=True):
        total = total + (re.now * im.before - im.now * re.before)
    return total


def well(booking: Any, action: int) -> np.ndarray:
    """A reading, the well of one interval (ALGEBRA.md #the-primitives, the rows "the hold" and "the source"; row (u), a body's well is gravity's source as a number): a booking of the record at every Node (its form D_i, or its Wronskian W_i) in quanta, booking div T by the division act, no remainder kept; the run writes the booking itself through the one wall of the held line."""
    return np.asarray(carried(booking, action, 0)[0])


def written(count: Any, rulers: Rulers, gamma: int, intervals: int) -> Any:
    """The write's factor, one place (ALGEBRA.md, The write per proper volume and per proper interval): a source's booking scaled per proper volume and per proper interval at the source family's paces, N^intervals p_x p_y p_z / p_0^3 with N = p_0 / Gamma, one rounding over the one wall (`paces.write_factor`), `intervals` the proper-interval powers of the held row's source, 2 on a count (the form) and 1 on the Wronskian, which carries one N of its own; the booking itself at the vacuum's paces."""
    clock, (p_x, p_y, p_z) = rulers
    return paces.write_factor(count, p_x, p_y, p_z, clock, gamma, intervals)


def turned_by(angle: Any, clock: Any, gamma: int) -> Any:
    """The turn's factor, one place (ALGEBRA.md, The turn per proper interval): the holder's level read into a plane's phase is the angle per proper interval, the numerator times the turned family's clock over Gamma, rounded once (`paces.turn_factor`); the angle itself at the vacuum's clock."""
    return paces.turn_factor(angle, clock, gamma)


Sourcing = tuple[int, int]  # a source of a write: a family of quanta's index and the record of it


def write_sources(
    held: int,
    families: Families,
    bookings: dict[Sourcing, Any],
    stresses: dict[Sourcing, currents.Vector],
    write: HeldWrite,
    rulers: dict[Sourcing, Rulers],
    gamma: int,
) -> list[Any]:
    """The numerators of a held family's one write per line at every Node, row by row (ALGEBRA.md #the-primitives, the row "the hold"; The write per proper volume and per proper interval, the factor by the source's kind; No record reads its own write of the sign; the integer 0 where nothing sources a line): the records that source a row are `derived.row_sources` (every reader's every record for a holder of the content; for a holder of the sign the one record that owns the row, and none for the free row 0); for the row's time line SUM over them of w x the booking of each that the row's sources name scaled by the write's factor at that record's paces (`written`, `rulers` per source record), the form D for a row sourced by the form, a count source, two proper-interval powers, and the Wronskian W for the holder of the sign, one time difference carrying one N of its own, one (`bookings`); for each axis line SUM over them of w x factor x the axis booking of each scaled by the count's factor, two powers (the mathematician's 70, #1572 comment 5935615659: the odd line's source J_a is one space difference, a covector's phase, its write the count's factor and its Link angle plain), its tension's part for a row of the content and its sign current, the mean of its two a-Links' Wronskian currents J_a / 2, for the holder of the sign under the rotation (`stresses`, the records' vectors), times its factor of the common wall (`HeldWrite`, one wall per line)."""
    family = families[held]
    intervals = 1 if family.wronskian else 2
    found: list[Any] = []
    for row in range(family.records):
        sources = row_sources(families, held, row)
        time: Any = 0
        for source in sources:
            scaled = written(bookings.get(source, 0), rulers[source], gamma, intervals)
            time = time + weight_of(held, families[source[0]]) * scaled
        found.append(time)
        for axis in range(family.width - 1):
            total: Any = 0
            for source in sources:
                if source in stresses:
                    scaled = written(stresses[source][axis], rulers[source], gamma, 2)
                    total = (
                        total
                        + weight_of(held, families[source[0]]) * write.factors.get(source[0], 0) * scaled
                    )
            found.append(total)
    return [family.write * numerator for numerator in found]  # the row's write weight k_w


def largest(record: Record) -> int:
    """The largest size of a line's newest level, read against the amplitude bound A."""
    return int(np.abs(record.now).max())


def zeros(shape: tuple[int, int, int], kind: type) -> np.ndarray:
    """An array of zeros over the GameBoard, of the run's kind of integers (the loader's choice by the file's width, `World.kind`)."""
    return np.zeros(shape, dtype=kind)


def full(shape: tuple[int, int, int], value: Any, kind: type) -> np.ndarray:
    """An array over the GameBoard at one value, of the run's kind of integers."""
    return np.full(shape, value, dtype=kind)


def empty_record(shape: tuple[int, int, int], kind: type, origin: Any = 0) -> Record:
    """A line at 0 with its remainder at `origin` at every Node, the half wall of the rule the line steps by where the caller gives it: every Node's remainder is born at the half wall, the vacuum (0, 0, w div 2) at every Node, the lay's origin and the start's alike, so that the one rounding of Rule3 is half up at every Node and no neighbour reads a floor (ALGEBRA.md, the start; the owner's word of 2026-10-03, #1572 comment 5968627499 (255); the mathematician's 254 with the advisor's 5968491596, two hands: under the floor a lone massless quantum laid at one Node of an even periodic box grew as t^2 on the uniform mode's double root); 0 where no wall is given (a line read for its levels alone)."""
    return Record(zeros(shape, kind), zeros(shape, kind), full(shape, origin, kind))


def complement(remainder: Any, wall: Any) -> Any:
    """The ones' complement of a carried remainder under its wall, wall - 1 - r: the remainder a signed component carries at its image under a symmetry that negates it (the odd axis lines of a holder under the rotation across their axis's mirror), since (wall - 1 - u) div wall = -(u div wall) and (wall - 1 - u) mod wall = wall - 1 - (u mod wall) for every integer u, so a lay symmetric with its remainders complemented at the image is symmetric to the bit under every act of the step (HIGHLIGHTS.md, the mathematician's 166 with the advisor's second hand); the division's origin wall div 2 has the complement wall - 1 - wall div 2, one below it at an even wall."""
    return wall - 1 - remainder


def write_origins(
    walls: Sequence[int], shape: tuple[int, int, int], kind: type, images: Sequence[Any] = ()
) -> list[np.ndarray]:
    """A held family's write remainders at a Node with no level, one per held line at half its wall, the division's origin (ALGEBRA.md #the-primitives, a family's write is one act; the start's origin, features/start); a signed line carries the origin's complement at the Nodes its image mask names (`images`, per line the mask of the Nodes on the image side of the line's mirror, None or absent for a scalar line), so that a symmetric lay is symmetric to the bit (`complement`)."""
    found = []
    for line, wall in enumerate(walls):
        origin = rule3(NO_READ, NO_READ, 1, 2, wall, 0, 0)[0]
        image = images[line] if line < len(images) else None
        plain = full(shape, origin, kind)
        found.append(plain if image is None else np.where(image, complement(plain, wall), plain))
    return found


def empty_state(
    family: FamilyRule,
    shape: tuple[int, int, int],
    walls: Sequence[int],
    kind: type,
    images: Sequence[Any] = (),
    origin: Any = 0,
) -> NodeState:
    """A family's NodeState before its start, the state of a Node with no level: its lines at 0, as many as the loader derives for it (`FamilyRule.lines`), and where it is held one write remainder per line at the origin (`walls` the write's wall per line), complemented at a signed line's image Nodes (`images`, `write_origins`)."""
    lines = [
        empty_record(shape, kind, origin) for _ in range(family.lines)
    ]  # every line born at the half wall
    return NodeState(lines, write_origins(walls, shape, kind, images) if family.held else [])
