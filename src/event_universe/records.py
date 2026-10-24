"""The records' lines and the sign's rows (ALGEBRA.md #the-count-is-the-records-share; No record reads its own write of the sign): a line of dimension one over the lattice, the lines of one record of a family (its bodies each a record where the family reads a holder of the sign), a holder of the sign's record as the board reads it whole, the sum of its rows, the light's record the free row 0 among them (light its own family, 2026-10-19), the sum of every row but the reader's own, and the readings of the lines kept nowhere, the form, the Wronskian, the well, the write's factor, the turn's factor and the one write's numerators row by row; every one a pure function of arrays, no state of its own."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from event_universe.core import paces
from event_universe.core.ports import AXES, SIDES
from event_universe.core.rule3 import division_forward
from event_universe.features import currents, phase, volume
from event_universe.loader.derived import FamilyRule, HeldWrite, row_sources, weight_of

Rulers = tuple[Any, tuple[Any, Any, Any]]  # a read's paces at every Node: the clock p_0, each axis's p_a
Families = tuple[FamilyRule, ...]  # the families as the loader derived them, in the file's order


@dataclass
class NodeState:
    """A family's NodeState at every Node, the law's numbers and nothing else (ALGEBRA.md #the-postulates): its lines, each a record of dimension one (two levels and Rule3's remainder), one shape for every family, and per held line the one remainder of its write. A family of quanta's lines are its record, one line (dimension 1) or two (a plane, re and im); a held row's lines are its sources' count, the time line and, where the tensions source it, the three axis lines, then the flux's three odd lines and the three shear lines xy, yz, zx where its declaration names them; the holder of the sign's time line is its record, the light's record on the free row 0, the row no body owns (light its own family, 2026-10-19). The holder of the sign under the rotation carries beside its rows the phase lines (`phases`, the line kind "phase" after the odd lines; features/phase, the mathematician's repaired form of item (g)): per row of the sign beyond the free row six lines of the same shape, the cosine and the sine line of each axis's Link at the Node that owns it (the +a Link of i), the Link's phase as the record owning the row reads it, every row but its own (ALGEBRA.md, No record reads its own write of the sign), then the three count lines, each axis's Link's count K_ij in its level now, the two ends' difference of the Node's K the step reads, the cache node.phase_counts sets (the level before and the remainder 0: a count is divided by nothing), by which the pair stands at the count's size on the one orbit from the seed and is read with the count's sign, the pair at -K the conjugate of the pair at +K (2026-10-21), and last the Node's phase row Phi, a Rule3 record whose write is the row's clocked potential (the centred count, 2026-10-23, node.phased), 30 integers per Node per record; empty on every other family and on the free row. Its count, currents, tension, form and Wronskian are readings of the lines (share.py, features/currents, `form`, `wronskian`) and stand nowhere."""

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
    return np.asarray(division_forward(booking, action, 0)[0])


def rulers_write_factor(
    count: Any, rulers: Rulers, gamma: int, intervals: int, carried: bool = False, parts: int = 1
) -> Any:
    """The write's factor at a record's rulers (ALGEBRA.md, The write per proper volume and per proper interval): a source's booking scaled per proper volume and per proper interval at the rulers handed in, the held row's own where the row reads the content and the source family's otherwise (`wall_rulers`, the owner's word of 2026-10-23), N^intervals p_x p_y p_z / p_0^3 with N = p_0 / Gamma, one rounding over the one wall (`paces.write_factor`), `intervals` the proper-interval powers of the held row's source, 2 on a count (the form) and 1 on the Wronskian, which carries one N of its own; the booking itself at the vacuum's paces; under `carried` the two terms unrounded, the product and the wall (the carried factor, `paces.write_factor_terms`)."""
    clock, (p_x, p_y, p_z) = rulers
    return paces.write_factor(count, p_x, p_y, p_z, clock, gamma, intervals, carried, parts)


def reads_content(families: Families, index: int) -> bool:
    """Whether a family reads the content, a holder of the content among its reads (ALGEBRA.md, Every row reads the content): the holders of the sign turn their readers and enter no pace, so a row whose reads are the sign's alone, or none, reads no content and has no paces of its own but the vacuum's."""
    return any(not families[r.family].rotation for r in families[index].reads)


def wall_rulers(
    held: int, families: Families, rulers: dict[Sourcing, Rulers], row: int, source: Sourcing
) -> Rulers:
    """The paces a held row's write is scaled at for one source (ALGEBRA.md, The one Node, the clause of 2026-10-23, the wall at the held row's own paces): the row's own, keyed (held, row) among the rulers, where the row reads the content (every act of the interval sees the Node's own clock and ruler, the held rows' write among them, and the Node's clock for the row's act is the row's own read of the content), so that its sources at differing read weights share the row's one wall per line; the source's own where the row reads no content (a holder of the sign reading none, whose Wronskian source is written per the Node's proper volume as the content gives it, which the row does not read: there the sources' shared paces stay the wall and the loader's gate `shared_clock` keeps them alike)."""
    own = rulers.get((held, row)) if reads_content(families, held) else None
    return rulers[source] if own is None else own


def scaled_sum(
    held: int,
    families: Families,
    values: dict[Sourcing, Any],
    rulers: dict[Sourcing, Rulers],
    gamma: int,
    intervals: int,
    factors: dict[int, int] | None = None,
    parts: int = 1,
    row: int = 0,
) -> tuple[Any, Any, list[tuple[Any, int]]]:
    """One line's numerator from its sources' values (a booking or an axis reading per source record): SUM over them of w x the value scaled by the write's factor at the row's own paces where the row reads the content, the source's otherwise (`wall_rulers`) (`rulers_write_factor`; w the read weight, times the line's factor per source family where `factors` names them, the tension lines' multiples), under the carried factor the unrounded product in its place, the line's divisor then the wall E_s T times the row's one factor wall per Node, the row's own paces' where it reads the content and its sources' shared paces' where it reads none (`wall_rulers`; the loader refuses differing sources on a row reading none alone, derived.shared_clock); returns the sum, the factor's wall (1 under the rounding) and each source's weighed term with its pair's exponent under the booking (the readings' mix, board_readings.eras)."""
    total: Any = 0
    scale: Any = 1
    terms: list[tuple[Any, int]] = []
    for source, value in values.items():
        weight = weight_of(held, families[source[0]]) * (factors.get(source[0], 0) if factors else 1)
        scaled, scale = rulers_write_factor(
            value, wall_rulers(held, families, rulers, row, source), gamma, intervals, True, parts
        )
        term = (
            weight * exact(scaled)
        )  # Python's integers before the sum: two carried terms of object arrays summed through an int64 scalar passed 2^63 at the chain's interval 208 (2026-10-24)
        total = total + term
        terms.append((term, families[source[0]].exponent(intervals)))
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
    fixed: Sequence[Any] | None = None,
) -> tuple[list[Any], list[Any], list[tuple[Any, int]]]:
    """The numerators of a held family's one write per line at every Node, row by row (ALGEBRA.md #the-primitives, the row "the held write"; The write per proper volume and per proper interval, the factor by the source's kind; No record reads its own write of the sign; the integer 0 where nothing sources a line): the records that source a row are `derived.row_sources` (every reader's every record for a holder of the content; for a holder of the sign the one record that owns the row, and none for the free row 0); for the row's time line SUM over them of w x the booking of each that the row's sources name scaled by the write's factor at that record's paces (`written`, `rulers` per source record), the form D for a row sourced by the form, a count source, two proper-interval powers, one under the row's key the form's own clock (`FamilyRule.power`; ALGEBRA.md, The form's own clock, a hypothesis under its own name, 2026-10-22: the form carrying one N of its own as the Wronskian does), and the Wronskian W for the holder of the sign, one time difference carrying one N of its own, one (`bookings`); for each axis line SUM over them of w x factor x the axis booking of each scaled by the count's factor, two powers (the mathematician's hand: the odd line's source J_a is one space difference, a covector's phase, its write the count's factor and its Link angle plain), its tension's part for a row of the content and its sign current, the mean of its two a-Links' Wronskian currents J_a / 2, for the holder of the sign under the rotation (`stresses`, the records' vectors), and for each shear line xy, yz, zx, where the row declares the shear, SUM over them of w x factor x the shear's part of each, the product of the Node's two axis differences D_a D_b (`readings.off_diagonals_of`), scaled by the count's factor, two powers, over its doubled wall 2 E_s W_c, each line's reading by its position among the record's axis readings (`axis_positions`), times its factor of the common wall (`HeldWrite`, one wall per line). Where `motion` is given, the row's own two levels as the direction finds them (forward the interval's start and backward the post-state; `Lattice.held_write`) and the row carries its volume (the volume form (every board's interval unobservable), features/volume; the momentum hand's derivation M12a read cold by the reader), the time line's numerator is the volume's write, (d + 1) X_now c with c the row's write as formed here (the write weight times the sources' forms less the trace), and its divisor Gamma E_s T, the one fixed wall (the carried factor refused under the key by the loader): X'' = (d + 1) X s / Gamma is the chain rule between the level and the volume, Gamma U'' = s - (d + 1) Gamma U'^2 with no hill as an act; the numerators returned with the walls, one divisor per line, the row's own where no carry changes them (`node.held_write_at`), and the first row's sources' terms with their pairs' exponents (the readings' mix); under the row's key the stress's trace (ALGEBRA.md, The stress's trace is the time line's, 2026-10-22) the time line's numerator is less the pressure term, the trace over three of each source's own stress parts in the energy's units at the weight -1 (`pressure_term`, one rounding per source per Node, scaled to the carried wall), and each tension line's numerator takes the traceless part of each source, 3 T_aa - SUM_b T_bb over the trace's three inside the factor's one rounding (`paces.write_factor`'s `parts`), so that no isotropic stress stretches the rulers (the clock's level does alone by h N = 1) and the tension lines' uniform mode on the closed board gets no source from a lay's mean stress (the smoke's finding of 2026-10-22: the tension lines' k = 0 mode, fed by the laid waves' mean stress and drained by nothing, froze every Link), the mean fed by the one write and the Node knowing nothing of the board (ALGEBRA.md, The uniform mode carried by Rule3's own k = 0 line, the clause of 2026-10-22; Every row reads the content, the hypothesis's one exception; The write per proper volume and per proper interval, the undimmed booking; The board's interval is no observable; the owner's locality decision of 2026-10-22). Where `fixed` is given, the row's walls per line as `Lattice.start` kept them at the rest's paces (the carried factor's one form under either key, the Boss's decision of 2026-10-22 on the text hand's model: under a rounded factor a family's write below half a level is 0 for ever, and under a carried factor at a wall that moves with the clock the remainder's range moves and the run back folds, so the moving wall is no form), every line's numerator carries the factor's ratio to the rest's paces, the carried numerator times the fixed wall over the interval's own wall rounded once as a coefficient (kind D, a number of order one on the carried product), and divides at the fixed wall, so the remainder's range never moves and division_back is exact (the reversibility hand's Theorem 1); without `fixed` the terms come out at the interval's own wall, the host's and the tests' reading of the sources."""
    family = families[held]
    intervals = family.power  # the booking's powers
    found: list[Any] = []
    scales: list[Any] = []  # per line, the carried factor's wall
    terms: list[tuple[Any, int]] = []  # the first row's sources' terms and exponents, the hill's weight
    trace = (
        not family.wronskian
    )  # a holder of the content: the stress's trace the time line's, the axis lines traceless
    for row in range(family.records):
        sources = row_sources(families, held, row)
        forms = {source: bookings.get(source, 0) for source in sources}
        time, scale, weighed = scaled_sum(
            held,
            families,
            forms,
            rulers,
            gamma,
            intervals,
            write.factors if family.wronskian else None,
            row=row,
        )  # the sign holder's charge factors: the Wronskian per quantum (The constants, 2026-10-24)
        if trace:
            time = time - pressure_term(held, families, stresses, rulers, gamma, intervals, row) * scale
        found.append(time)
        scales.append(scale)
        terms = weighed if row == 0 else terms
        for position in axis_positions(family):
            axes = {source: stresses[source][position] for source in sources if source in stresses}
            parts = AXES if trace and position < AXES else 1
            if parts > 1:
                axes = {s: AXES * axes[s] - sum(stresses[s][a] for a in range(AXES)) for s in axes}
            total, scale, _ = scaled_sum(
                held, families, axes, rulers, gamma, 2, write.factors, parts, row
            )
            found.append(total)
            scales.append(scale)
    found = [family.write * numerator for numerator in found]  # the row's write weight k_w
    walls = [wall * scale for wall, scale in zip(write.walls, scales, strict=True)]  # one per line
    if (
        fixed is not None
    ):  # the wall fixed per Node: the ratio of the walls inside the numerator, rounded once, in Python's integers (the fixed wall E_s T Gamma^power p_0^(3 - power) passes 63 bits at the shipped level weights, 7 x 10^21 at E_s 10^6 and T 2^15, so the one product is exact beyond the width as the write factor's numerator is, `exact`)
        ratios = zip(found, fixed, walls, strict=True)
        found = [paces.rounded(exact(n) * exact(f), exact(w)) for n, f, w in ratios]
        walls = [exact(f) for f in fixed]
    if (
        motion is not None and family.motion_volume
    ):  # the volume's write: (d + 1) X_now c over Gamma E_s T
        now = np.asarray(motion[0] if direction == 1 else motion[1], dtype=object)
        found[0] = volume.EXPONENT * now * np.asarray(found[0], dtype=object)
        walls = divided_walls(family, walls, gamma)
    return found, walls, terms


def divided_walls(family: FamilyRule, walls: Sequence[Any], gamma: int) -> list[Any]:
    """The walls a held row's write divides at, one per line, from the row's walls as `walls_at` and `Lattice.start` keep them (the fixed wall E_s T Gamma^power p_0^(3 - power) on the time line): the same walls for a row carrying its level, and for a row carrying its volume the time line's at Gamma times its fixed wall, the volume's divisor Gamma E_s T (`write_sources` under `motion`; the chain rule between the level and the volume), the other lines' unchanged. The one place that names the wall, read by the write and by the write remainders' origin alike (ALGEBRA.md, The write per proper volume and per proper interval: every write remainder is born at the half wall, w div 2, of its own wall; the builder's finding of 2026-10-24, #2187: the volume row's origin was born at the half of the fixed wall, 1 / (2 Gamma) of the wall its write divides at, so the first write of Universe24 read 2 where the half wall gives 3)."""
    if not family.motion_volume:
        return list(walls)
    return [gamma * walls[0], *walls[1:]]


def exact(values: Any) -> Any:
    """An array (or a number) as Python's integers, exact at any size: the hardware's integers inside an object array overflow at 63 bits when multiplied by a wall beyond them, so every term of a carried write at the fixed wall is made Python's first (the precedent the write factor's numerator, `paces.write_factor`, booked exact beyond the width)."""
    found = np.asarray(values)
    if found.shape == ():
        return int(found)
    return np.vectorize(int, otypes=[object])(found)


def walls_at(
    held: int, families: Families, write: HeldWrite, rulers: dict[Sourcing, Rulers], gamma: int
) -> list[Any]:
    """Every line's wall of a held row's write at the rulers given, the write of no source (`write_sources` on bookings and stresses of 0 at every source): one integer per line under the rounded factor and under the carried factor the wall per Node, E_s T Gamma^power p_0^(3 - power) on the time line and E_s W_c Gamma^2 p_0 on each axis and shear line, the trace's three on a tension line, at the row's own clock where it reads the content and at its sources' shared clock where it reads none (`wall_rulers`, `derived.shared_clock`); the walls `Lattice.start` keeps for the run at the rest's paces under the volume form with the carried factor, the wall fixed per Node."""
    nothing: dict[Sourcing, Any] = {source: (0,) * (AXES * AXES) for source in rulers}
    return write_sources(held, families, {}, nothing, write, rulers, gamma)[1]


def pressure_term(
    held: int,
    families: Families,
    stresses: dict[Sourcing, currents.Vector],
    rulers: dict[Sourcing, Rulers],
    gamma: int,
    power: int,
    row: int = 0,
) -> Any:
    """The pressure's write in the time line at every Node, the stress's trace (ALGEBRA.md, The stress's trace is the time line's, a hypothesis under its own name, 2026-10-22: the pressure hand's derivation and the reader's build line read cold; the two channels of the rulers, the clock's h = e^U by h N = 1 and the tension's Gamma / (Gamma - t_a), nature's one a(t) stretching nothing by its isotropic pressure, so the isotropic part of the tension lines' uniform mode is 0 and not braked): the trace over three of each source's own stress parts at the Node, -num h_a as the tension lines take them (readings.stresses_of, one Link's reach), each part turned into the energy's units by the record's own gradient speed squared, (p_a / Gamma)^2 / (3 den) (The band at a pace: the gradient part of 2 (1 - cos omega') is (num / (3 den)) (p_a / Gamma)^2 2 (1 - cos k), so the stress times it is the gradient energy, T_xx = T_00 for light's long wave), summed over the three axes and divided by three, then scaled per proper volume and per proper interval as the row books its count sources (p_x p_y p_z over Gamma^power p_0^(3 - power)): one rounding per source per Node over the one wall 9 den Gamma^(2 + power) p_0^(3 - power) (a coefficient rounded at the read, kind D), at the read weight, the sign -1 taken by the caller (alpha = -d lambda = -1 at lambda = 1 / d: the pressure enters against the energy's hollow, no number of the file and none of nature); every quantity read from the records as they stand at the interval's start, so the inverse recomputes the same term (the reversibility hand's Theorem 1); under the carried factor the caller scales it to the wall per Node (records.write_sources)."""
    total: Any = 0
    for source in row_sources(families, held, 0):
        if source not in stresses:
            continue
        family, (clock, p_axes) = families[source[0]], wall_rulers(held, families, rulers, row, source)
        paces_object = [
            exact(p) for p in p_axes
        ]  # Python's integers: the wall 9 den Gamma^(2 + power) p_0^(3 - power) passes 63 bits
        trace: Any = 0
        for axis in range(AXES):
            trace = trace + exact(stresses[source][axis]) * paces_object[axis] ** 2
        numerator = trace * paces_object[0] * paces_object[1] * paces_object[2]
        clock_object = exact(clock)
        wall = (
            SIDES * AXES * AXES * family.pair[1] * gamma ** (2 + power) * clock_object ** (3 - power)
        )  # the stress parts at the doubled wall (The stress is the Links', 2026-10-23): 18 den Gamma^(2 + power) p_0^(3 - power)
        total = total + weight_of(held, family) * paces.rounded(numerator, wall)
    return total


def axis_positions(family: FamilyRule) -> list[int]:
    """The position, among a source record's axis readings (`readings.axis_sources_of`: the three tensions, the three fluxes, the three shears, in that order; a turned record's three sign currents for the holder of the sign under the rotation), that each axis line of one row of a held family takes, in the row's order after its time line: the three tension lines or the three odd lines of the sign read the first three; the flux's odd lines the next three; the shear lines xy, yz, zx the last three (`FamilyRule.off_diagonal_lines`)."""
    positions = list(range(AXES)) if family.axes else []  # a row sourced by the form alone has none
    if family.flux:
        positions += [AXES + axis for axis in range(AXES)]
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
    """The phase lines of a holder of the sign under the rotation at the start (features/phase, `seed`; the two hands' item (i); the centred count, the owner's decision of 2026-10-23): per row of the sign beyond the free row, for each axis the cosine line and the sine line of the Node's +a Link at the angle 0, (X, X cos theta rounded, D div 2) and (0, -(X div 2 Gamma), D div 2) at every Node, X the amplitude the width derives at the line's unit 2 Gamma (`phase.amplitude`, `phase.unit`), the Link's phase at the fixed half angle theta_0 / 2; after them the three count lines at 0, each axis's Link's count K_ij as the step reads it (`NodeState`, the cache of the two ends' difference node.phased carries the pair to); and last the Node's phase row Phi, a Rule3 record born at rest (0, 0, 0), whose write per interval is the clocked potential (node.phased); the free row's list empty (read by no record); empty for every other family. `node.seed_phases` then carries every pair to the count the laid state stands at."""
    if not family.rotation:
        return []
    cosine, sine = phase.seed(phase.amplitude(phase.unit(gamma), width), phase.unit(gamma))
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
        + [Record(full(shape, 0, kind), full(shape, 0, kind), full(shape, 0, kind))]
        for row in range(family.records)
    ]


def complement(remainder: Any, wall: Any) -> Any:
    """The ones' complement of a carried remainder under its wall, wall - 1 - r: the remainder a signed component carries at its image under a symmetry that negates it (the odd axis lines of a holder under the rotation across their axis's mirror), since (wall - 1 - u) div wall = -(u div wall) and (wall - 1 - u) mod wall = wall - 1 - (u mod wall) for every integer u, so a lay symmetric with its remainders complemented at the image is symmetric to the bit under every act of the step (HIGHLIGHTS.md, the mathematician's hand with the advisor's second hand); the division's origin wall div 2 has the complement wall - 1 - wall div 2, one below it at an even wall."""
    return wall - 1 - remainder


def write_origins(walls: Sequence[Any], shape: tuple[int, int, int], kind: type) -> list[np.ndarray]:
    """A held family's write remainders at a Node with no level, one per held line at half its wall, the division's origin (ALGEBRA.md #the-primitives, a family's write is one act; the start's origin, features/start): `walls` are the walls the write divides at (`divided_walls`), the volume's time line's Gamma E_s T and not its fixed wall alone (the finding of 2026-10-24)."""
    return [full(shape, division_forward(wall, 2, 0)[0], kind) for wall in walls]


def empty_state(
    family: FamilyRule,
    shape: tuple[int, int, int],
    walls: Sequence[int],
    kind: type,
    origin: Any = 0,
) -> NodeState:
    """A family's NodeState before its start, the state of a Node with no level: its lines at 0, as many as the loader derives for it (`FamilyRule.lines`), the three tension lines of a row under the stress's trace born at the half of the wall 3 w they step by (flux.step_traceless, the one rounding half up there too), and where it is held one write remainder per line at the origin (`walls` the write's wall per line, `write_origins`)."""
    lines = [
        empty_record(shape, kind, origin) for _ in range(family.lines)
    ]  # every line born at the half wall
    if family.axes and not family.wronskian:  # the tension lines step at the wall 3 w: born at its half
        lines[1 : 1 + AXES] = [empty_record(shape, kind, AXES * origin) for _ in range(AXES)]
    return NodeState(lines, write_origins(walls, shape, kind) if family.held else [])
