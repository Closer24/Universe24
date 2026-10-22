"""The records' lines and the sign's rows (ALGEBRA.md #the-count-is-the-records-share; No record reads its own write of the sign): a line of dimension one over the lattice, the lines of one record of a family (its bodies each a record where the family reads a holder of the sign), a holder of the sign's record as the board reads it whole, the sum of its rows, the light's record the free row 0 among them (light its own family, 2026-10-19), the sum of every row but the reader's own, and the readings of the lines kept nowhere, the form, the Wronskian, the well, the write's factor, the turn's factor and the one write's numerators row by row; every one a pure function of arrays, no state of its own."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import AXES
from event_universe.core.rule3 import division_forward
from event_universe.features import currents, phase
from event_universe.features.write import carried
from event_universe.loader.derived import FamilyRule, HeldWrite, exponent_of, row_sources, weight_of

Rulers = tuple[Any, tuple[Any, Any, Any]]  # a read's paces at every Node: the clock p_0, each axis's p_a
Families = tuple[FamilyRule, ...]  # the families as the loader derived them, in the file's order


@dataclass
class NodeState:
    """A family's NodeState at every Node, the law's numbers and nothing else (ALGEBRA.md #the-postulates): its lines, each a record of dimension one (two levels and Rule3's remainder), one shape for every family, and per held line the one remainder of its write. A family of quanta's lines are its record, one line (dimension 1) or two (a plane, re and im); a held row's lines are its sources' count, the time line and, where the tensions source it, the three axis lines, then the flux's three odd lines and the three shear lines xy, yz, zx where its declaration names them; the holder of the sign's time line is its record, the light's record on the free row 0, the row no body owns (light its own family, 2026-10-19). The holder of the sign under the rotation carries beside its rows the phase lines (`phases`, the line kind "phase" after the odd lines; features/phase, the mathematician's repaired form of item (g)): per row of the sign beyond the free row six lines of the same shape, the cosine and the sine line of each axis's Link at the Node that owns it (the +a Link of i), the Link's phase as the record owning the row reads it, every row but its own (ALGEBRA.md, No record reads its own write of the sign), then the three count lines, each axis's Link's count N_ij in its level now, the signed sum of the levels the phase acts added (features/phase `orbit_moves`; the level before and the remainder 0: a count is divided by nothing), by which the pair stands at the count's size on the one orbit from the seed and is read with the count's sign, the pair at -n the conjugate of the pair at +n (2026-10-21), 21 integers per Node per record; empty on every other family and on the free row. Its count, currents, tension, form and Wronskian are readings of the lines (share.py, features/currents, `form`, `wronskian`) and stand nowhere."""

    lines: list[Record]
    write_remainders: list[np.ndarray]
    phases: list[list[Record]] = field(default_factory=list)


States = list[NodeState]  # every family's NodeState, in the families' order


@dataclass(frozen=True)
class Record:
    """One line of dimension one over the lattice: the level now, the level before and the remainder r at every Node."""

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


def rows_total(family: FamilyRule, lines: Sequence[Record]) -> Record:
    """A holder of the sign's record as the board reads it whole, the sum of its rows' time lines at every Node, both levels (a node_detector or a body reads the sum of all rows, ALGEBRA.md, No record reads its own write of the sign; the light's record the free row 0 among them, light its own family, 2026-10-19), the remainder the free row's; the row's own line where it has one row, bit for bit."""
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
    """A reading, the well of one interval (ALGEBRA.md #the-primitives, the rows "the held write" and "the source"; row (u), a body's well is gravity's source as a number): a booking of the record at every Node (its form D_i, or its Wronskian W_i) in quanta, booking div T by the division act, no remainder kept; the run writes the booking itself through the one wall of the held line."""
    return np.asarray(carried(booking, action, 0)[0])


def rulers_write_factor(
    count: Any, rulers: Rulers, gamma: int, intervals: int, carried: bool = False, parts: int = 1
) -> Any:
    """The write's factor at a record's rulers (ALGEBRA.md, The write per proper volume and per proper interval): a source's booking scaled per proper volume and per proper interval at the source family's paces, N^intervals p_x p_y p_z / p_0^3 with N = p_0 / Gamma, one rounding over the one wall (`paces.write_factor`), `intervals` the proper-interval powers of the held row's source, 2 on a count (the form) and 1 on the Wronskian, which carries one N of its own; the booking itself at the vacuum's paces; under `carried` the two terms unrounded, the product and the wall (the held row's key `factor: carried`, `paces.write_factor_terms`)."""
    clock, (p_x, p_y, p_z) = rulers
    return paces.write_factor(count, p_x, p_y, p_z, clock, gamma, intervals, carried, parts)


def scaled_sum(
    held: int,
    families: Families,
    values: dict[Sourcing, Any],
    rulers: dict[Sourcing, Rulers],
    gamma: int,
    intervals: int,
    carried: bool,
    factors: dict[int, int] | None = None,
    parts: int = 1,
) -> tuple[Any, Any, list[tuple[Any, int]]]:
    """One line's numerator from its sources' values (a booking or an axis reading per source record): SUM over them of w x the value scaled by the write's factor at the source's paces (`rulers_write_factor`; w the read weight, times the line's factor per source family where `factors` names them, the tension lines' multiples), under the held row's key `factor: carried` the unrounded product in its place, the line's divisor then the wall E_s T times the sources' shared factor's wall per Node (the loader admits the carry where the row's sources share the clock, derived.shared_clock); returns the sum, the factor's wall (1 under the rounding) and each source's weighed term with its pair's exponent under the booking (the hill's weight, `hill_weight`)."""
    total: Any = 0
    scale: Any = 1
    terms: list[tuple[Any, int]] = []
    for source, value in values.items():
        weight = weight_of(held, families[source[0]]) * (factors.get(source[0], 0) if factors else 1)
        scaled = rulers_write_factor(value, rulers[source], gamma, intervals, carried, parts)
        if carried:
            scaled, scale = scaled
        total = total + weight * scaled
        terms.append((weight * scaled, families[source[0]].exponent(intervals)))
    return total, scale, terms


Sourcing = tuple[int, int]  # a source of a write: a family of quanta's index and the record of it


def write_sources(
    held: int,
    families: Families,
    bookings: dict[Sourcing, Any],
    stresses: dict[Sourcing, currents.Vector],
    write: HeldWrite,
    rulers: dict[Sourcing, Rulers],
    gamma: int,
    motion: tuple[Any, Any] | None = None,
    direction: int = 1,
) -> tuple[list[Any], list[Any], Any]:
    """The numerators of a held family's one write per line at every Node, row by row (ALGEBRA.md #the-primitives, the row "the held write"; The write per proper volume and per proper interval, the factor by the source's kind; No record reads its own write of the sign; the integer 0 where nothing sources a line): the records that source a row are `derived.row_sources` (every reader's every record for a holder of the content; for a holder of the sign the one record that owns the row, and none for the free row 0); for the row's time line SUM over them of w x the booking of each that the row's sources name scaled by the write's factor at that record's paces (`written`, `rulers` per source record), the form D for a row sourced by the form, a count source, two proper-interval powers, one under the row's key `booking: form` (`FamilyRule.power`; ALGEBRA.md, The form's own clock, a hypothesis under its own name, 2026-10-22: the form carrying one N of its own as the Wronskian does), and the Wronskian W for the holder of the sign, one time difference carrying one N of its own, one (`bookings`); for each axis line SUM over them of w x factor x the axis booking of each scaled by the count's factor, two powers (the mathematician's hand: the odd line's source J_a is one space difference, a covector's phase, its write the count's factor and its Link angle plain), its tension's part for a row of the content and its sign current, the mean of its two a-Links' Wronskian currents J_a / 2, for the holder of the sign under the rotation (`stresses`, the records' vectors), and for each shear line xy, yz, zx, where the row declares the shear, SUM over them of w x factor x the shear's part of each, the product of the Node's two axis differences D_a D_b (`readings.off_diagonals_of`), scaled by the count's factor, two powers, over its doubled wall 2 E_s W_c, each line's reading by its position among the record's axis readings (`axis_positions`), times its factor of the common wall (`HeldWrite`, one wall per line). Where `motion` is given, the row's own two levels as the direction finds them, forward the interval's start and backward the post-state (a held row of the content on a world declaring `interval: unobservable`, never the holder of the sign; `Lattice.held_write`), the time line's numerator gains the hill at the symmetry's weight after the row's write weight, -K (now - before)^2 undimmed, and its divisor the hill's, the wall plus direction x K (now - before), the symmetric hill (`paces.motion_term`, the one function of the hill's write returning the term and the divisor; `hill_weight`, `paces.motion_weight`: the weight from the Node's own sources' mix, the terms this function sums; under the carry both scaled by the factor's wall); the numerators returned with the walls, one divisor per line, the row's own where no hill and no carry changes them (`node.held_write_at`), and the hill's weight at every Node as the divisor took it (None without the hill; the forward act's reading of the run back, `paces.motion_returns`); under the row's key `pressure: trace` (ALGEBRA.md, The stress's trace is the time line's, 2026-10-22) the time line's numerator is less the pressure term, the trace over three of each source's own stress parts in the energy's units at the weight -1 (`pressure_term`, one rounding per source per Node, scaled to the carried wall), and each tension line's numerator takes the traceless part of each source, 3 T_aa - SUM_b T_bb over the trace's three inside the factor's one rounding (`paces.write_factor`'s `parts`), so that no isotropic stress stretches the rulers (the clock's level does alone by h N = 1) and the tension lines' uniform mode on the closed board gets no source from a lay's mean stress (the smoke's finding of 2026-10-22: the tension lines' k = 0 mode, fed by the laid waves' mean stress and drained by nothing, froze every Link), the mean fed by the one write less the hill and the Node knowing nothing of the board (ALGEBRA.md, The uniform mode carried by Rule3's own k = 0 line, the clause of 2026-10-22; The motion of gravity's row is a hill at the symmetry's weight; Every row reads the content, the hypothesis's one exception; The write per proper volume and per proper interval, the undimmed booking; The board's interval is no observable; the owner's locality decision of 2026-10-22)."""
    family = families[held]
    intervals, carried = (
        family.power,
        family.factor_carried,
    )  # the booking's powers; the factor's booking
    found: list[Any] = []
    scales: list[Any] = []  # per line, the factor's wall under the carry, 1 under the rounding
    terms: list[tuple[Any, int]] = []  # the first row's sources' terms and exponents, the hill's weight
    trace = family.pressure_trace  # the stress's trace the time line's, the axis lines traceless
    for row in range(family.records):
        sources = row_sources(families, held, row)
        forms = {source: bookings.get(source, 0) for source in sources}
        time, scale, weighed = scaled_sum(held, families, forms, rulers, gamma, intervals, carried)
        if trace:
            time = time - pressure_term(held, families, stresses, rulers, gamma, intervals) * scale
        found.append(time)
        scales.append(scale)
        terms = weighed if row == 0 else terms
        for position in axis_positions(family):
            axes = {source: stresses[source][position] for source in sources if source in stresses}
            parts = AXES if trace and position < AXES else 1
            if parts > 1:
                axes = {s: AXES * axes[s] - sum(stresses[s][a] for a in range(AXES)) for s in axes}
            total, scale, _ = scaled_sum(
                held, families, axes, rulers, gamma, 2, carried, write.factors, parts
            )
            found.append(total)
            scales.append(scale)
    found = [family.write * numerator for numerator in found]  # the row's write weight k_w
    walls = [wall * scale for wall, scale in zip(write.walls, scales, strict=True)]  # one per line
    if motion is None:
        return found, walls, None
    weight = hill_weight(family, [t for t, _ in terms], [n for _, n in terms], write.walls[0], gamma)
    weight = weight * scales[0]  # the hill after the write weight, at the carried wall's scale
    term, walls[0] = paces.motion_term(motion[0], motion[1], weight, walls[0], direction)
    found[0] = found[0] + term
    return found, walls, weight


def pressure_term(
    held: int,
    families: Families,
    stresses: dict[Sourcing, currents.Vector],
    rulers: dict[Sourcing, Rulers],
    gamma: int,
    power: int,
) -> Any:
    """The pressure's write in the time line at every Node, the held row's key `pressure: trace` (ALGEBRA.md, The stress's trace is the time line's, a hypothesis under its own name, 2026-10-22: the pressure hand's derivation and the reader's build line read cold; the two channels of the rulers, the clock's h = e^U by h N = 1 and the tension's Gamma / (Gamma - t_a), nature's one a(t) stretching nothing by its isotropic pressure, so the isotropic part of the tension lines' uniform mode is 0 and not braked): the trace over three of each source's own stress parts at the Node, -num h_a as the tension lines take them (readings.stresses_of, one Link's reach), each part turned into the energy's units by the record's own gradient speed squared, (p_a / Gamma)^2 / (3 den) (The band at a pace: the gradient part of 2 (1 - cos omega') is (num / (3 den)) (p_a / Gamma)^2 2 (1 - cos k), so the stress times it is the gradient energy, T_xx = T_00 for light's long wave), summed over the three axes and divided by three, then scaled per proper volume and per proper interval as the row books its count sources (p_x p_y p_z over Gamma^power p_0^(3 - power)): one rounding per source per Node over the one wall 9 den Gamma^(2 + power) p_0^(3 - power) (a coefficient rounded at the read, kind D), at the read weight, the sign -1 taken by the caller (alpha = -d lambda = -1 at lambda = 1 / d: the pressure enters against the energy's hollow, no number of the file and none of nature); every quantity read from the records as they stand at the interval's start, so the inverse recomputes the same term (the reversibility hand's Theorem 1); under the carried factor the caller scales it to the wall per Node (records.write_sources)."""
    total: Any = 0
    for source in row_sources(families, held, 0):
        if source not in stresses:
            continue
        family, (clock, p_axes) = families[source[0]], rulers[source]
        paces_object = [np.asarray(p, dtype=object) for p in p_axes]
        trace: Any = 0
        for axis in range(AXES):
            trace = trace + np.asarray(stresses[source][axis], dtype=object) * paces_object[axis] ** 2
        numerator = trace * paces_object[0] * paces_object[1] * paces_object[2]
        clock_object = np.asarray(clock, dtype=object)
        wall = AXES * AXES * family.pair[1] * gamma ** (2 + power) * clock_object ** (3 - power)
        total = total + weight_of(held, family) * paces.rounded(numerator, wall)
    return total


def hill_weight(
    family: FamilyRule, terms: Sequence[Any], exponents: Sequence[int], wall: int, gamma: int
) -> Any:
    """The hill's weight at every Node of a held row of the content from its time line's sources (`paces.motion_weight`; ALGEBRA.md, The hill's weight is the write's mix, a hypothesis under its own name, 2026-10-22): the Node's own sources' mix at the pairs' integers under the row's booking, the default, the row's own pair's exponent where nothing sources a Node (`FamilyRule.exponent`); under the row's key `weight: gap` the one-form K at the exponent of a pair with a gap at rest for every Node, no source handed (loader/universe.hill_weight_of); under the row's key `pressure: trace` one K for every mix, (d + 1) E_s T / Gamma with d the axes' three (24 at T 36,000; ALGEBRA.md, The stress's trace is the time line's: the surface (Gamma / 2) U'^2 = (1 / d) SUM s_f is invariant for every mix iff the pressure enters at -1 and c = d + 1, the pressure hand's derivation; The hill's weight is the write's mix dissolved, kept by name), the loader checking Gamma divides (d + 1) E_s T (derived.trace_wall); the write and the readings read the one weight (`write_sources`, board_readings.eras)."""
    if family.pressure_trace:  # one K for every mix, (d + 1) E_s T / Gamma, the trace's constraint
        return paces.motion_weight([], [], wall, gamma, AXES + 1)
    if family.weight_gap:
        return paces.motion_weight([], [], wall, gamma, exponent_of(False, family.power))
    return paces.motion_weight(terms, exponents, wall, gamma, family.exponent())


def axis_positions(family: FamilyRule) -> list[int]:
    """The position, among a source record's axis readings (`readings.axis_sources_of`: the three tensions, the three fluxes, the three shears, in that order; a turned record's three sign currents for the holder of the sign under the rotation), that each axis line of one row of a held family takes, in the row's order after its time line: the three tension lines or the three odd lines of the sign read the first three; the flux's odd lines the next three; the shear lines xy, yz, zx the last three (`FamilyRule.off_diagonal_lines`)."""
    positions = list(range(AXES)) if family.axes else []  # a row sourced by the form alone has none
    if family.flux:
        positions += [AXES + axis for axis in range(AXES)]
    if family.off_diagonal:
        positions += [2 * AXES + axis for axis in range(AXES)]
    assert len(positions) == family.width - 1, f"{family.name!r}: {family.width - 1} axis lines"
    return positions


def largest(record: Record) -> int:
    """The largest size of a line's newest level, read against the amplitude bound A."""
    return int(np.abs(record.now).max())


def zeros(shape: tuple[int, int, int], kind: type) -> np.ndarray:
    """An array of zeros over the lattice, of the run's kind of integers (the loader's choice by the file's width, `World.kind`)."""
    return np.zeros(shape, dtype=kind)


def full(shape: tuple[int, int, int], value: Any, kind: type) -> np.ndarray:
    """An array over the lattice at one value, of the run's kind of integers."""
    return np.full(shape, value, dtype=kind)


def empty_record(shape: tuple[int, int, int], kind: type, origin: Any = 0) -> Record:
    """A line at 0 with its remainder at `origin` at every Node, the half wall of the rule the line steps by where the caller gives it: every Node's remainder is born at the half wall, the vacuum (0, 0, w div 2) at every Node, the lay's origin and the start's alike, so that the one rounding of Rule3 is half up at every Node and no neighbour reads a floor (ALGEBRA.md, the start; the owner's word; the mathematician's hand with the advisor's hand, two hands: under the floor a lone massless quantum laid at one Node of an even periodic box grew as t^2 on the uniform mode's double root); 0 where no wall is given (a line read for its levels alone)."""
    return Record(zeros(shape, kind), zeros(shape, kind), full(shape, origin, kind))


def phase_lines(
    family: FamilyRule, shape: tuple[int, int, int], kind: type, gamma: int, width: int
) -> list[list[Record]]:
    """The phase lines of a holder of the sign under the rotation at the start (features/phase, `seed`; the two hands' item (i)): per row of the sign beyond the free row, for each axis the cosine line and the sine line of the Node's +a Link at the angle 0, (X, X cos theta_0 rounded, D div 2) and (0, -(X div Gamma), D div 2) at every Node, X the amplitude the width derives (`phase.amplitude`), the Link's phase at the fixed angle theta_0 = 1 / Gamma, and after them the three count lines at 0, each axis's Link's count N_ij (`NodeState`; features/phase `orbit_moves`, 2026-10-21); the free row's list empty (read by no record); empty for every other family."""
    if not family.rotation:
        return []
    cosine, sine = phase.seed(phase.amplitude(gamma, width), gamma)
    return [
        []
        if row == 0
        else [
            Record(full(shape, c, kind), full(shape, b, kind), full(shape, r, kind))
            for _axis in range(AXES)
            for c, b, r in (cosine, sine)
        ]
        + [
            Record(full(shape, 0, kind), full(shape, 0, kind), full(shape, 0, kind))
            for _axis in range(AXES)
        ]
        for row in range(family.records)
    ]


def complement(remainder: Any, wall: Any) -> Any:
    """The ones' complement of a carried remainder under its wall, wall - 1 - r: the remainder a signed component carries at its image under a symmetry that negates it (the odd axis lines of a holder under the rotation across their axis's mirror), since (wall - 1 - u) div wall = -(u div wall) and (wall - 1 - u) mod wall = wall - 1 - (u mod wall) for every integer u, so a lay symmetric with its remainders complemented at the image is symmetric to the bit under every act of the step (HIGHLIGHTS.md, the mathematician's hand with the advisor's second hand); the division's origin wall div 2 has the complement wall - 1 - wall div 2, one below it at an even wall."""
    return wall - 1 - remainder


def write_origins(walls: Sequence[int], shape: tuple[int, int, int], kind: type) -> list[np.ndarray]:
    """A held family's write remainders at a Node with no level, one per held line at half its wall, the division's origin (ALGEBRA.md #the-primitives, a family's write is one act; the start's origin, features/start)."""
    return [full(shape, division_forward(wall, 2, 0)[0], kind) for wall in walls]


def empty_state(
    family: FamilyRule,
    shape: tuple[int, int, int],
    walls: Sequence[int],
    kind: type,
    origin: Any = 0,
) -> NodeState:
    """A family's NodeState before its start, the state of a Node with no level: its lines at 0, as many as the loader derives for it (`FamilyRule.lines`), and where it is held one write remainder per line at the origin (`walls` the write's wall per line, `write_origins`)."""
    lines = [
        empty_record(shape, kind, origin) for _ in range(family.lines)
    ]  # every line born at the half wall
    return NodeState(lines, write_origins(walls, shape, kind) if family.held else [])
