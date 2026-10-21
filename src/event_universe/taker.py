"""The lawful taker inside the engine, generic and opt-in (the sprint of 2026-10-21, builder L; ALGEBRA.md, The emission of a bound record is the click's act of the taker; The click's unit; A detector is the future having met the past; The click's read of the board; The digits' budget; builder A's region taker and builder B's self-clicking body, the run-script relays of the night, made the engine's own act beside the declared bodies'): under the world's key `takers: "bodies"` (loader/world.py, refused by name at any other value; absent, the engine as before bit for bit) every body laid in a holder's well, a turned record standing at the lay, is a taker, and every declared region NodeDetector with it where the world's bodies carry one transition. A body's instrument is read once at the lay and typed nowhere (`takers_of`): its frame's modes and the transition it carries (frame.py: the upper level the one of its largest share, the lower the lowest), its unit W_rec = W_c sin Omega of that transition, its window the transition's own period, and its standing region, the Nodes of its largest shares holding half its record's share (the count's own rounding as the floor), its front the region's boundary Ports on the declared board (reports.front). Each interval it books the LIGHT it reads, the holder of the sign's record whole but its own row (the free row and every other body's row, `light_lines`; No record reads its own write of the sign) through its front, the plain bilinear of those real lines (readings.currents_of, the covector's weights under the Lorentz form; the covariant form of a turned record stands in board_readings.record_currents for the records a region books), per Node and summed, into the window's inflow and the running books. At the window's close (`closed`) the body draws WHETHER on its own digits (`read_of`: the holder's rows' remainders at its Nodes on the lattice gcd(w, D_i, R_ij), three values a digit for light at the vacuum paces, and its own record's on the fine lattice gcd(w, D_i, p_i^2) of a turned plane, Hand 1's D1; the origin's digits skipped, each Node's distinct digits once, the read refused by name where the region's capacity in bits is below the draw's total, never per digit: The digits' budget) against the weights [the window's inflow floored at 0 and capped at W_rec, W_rec less it], the law's geometric draw for a steady beat (the per-window hazard the share, the mean W_rec / P windows, no count-up: Hand 1's item 8), the window's inflow beginning again (its excess above W_rec carried) and the books carried on; on a take the WHERE by one division act of the number left on the window's inflow per Node, the WHO the giver drawn among the world's bodies standing in an upper level by their upper shares (`giver_of`), the credit line as the engine's own (reports.credit: the family, the reader, the count, no Node named), and the WRITE through the one lay act (frame.relaid): the taker body's record in its upper level at the count whole with the arriving phase, the giver's record in its lower level at the count whole (the re-lay at the click's interval, the shortcut; the run back to the birth the law's path, open), and the light's hole at the drawn Node where the light stands in a quanta record, the free row, and no hole where it stands in a held row, the giver's own write (the energy question the owner decides, the books of energy printed before and after). Every line of it a LATTICE `taker` line or the NODEDETECTOR credit line (reports.taker, reports.credit); nothing of it at the Node, which steps Rule3 and knows no taker."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import gcd
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import covector, digits, node, readings, reports, share
from event_universe import frame as frames
from event_universe.core.rule3 import division_forward
from event_universe.features.click import drawn_from, read_number
from event_universe.lay import laid
from event_universe.loader.derived import row_of, turns
from event_universe.loader.world import BodyRow
from event_universe.records import Record, row_levels

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


@dataclass
class Taker:
    """One taker's instrument and books: its name in the lines (a body by its number, a region by its name), the body's number (None for a region), its frame (None for a region), its Nodes and its front per Port, the holder it reads and its own row of it (None for a region), its unit W_rec and its window, the window's inflow and the inflow per Node, the running books (the light booked less the quanta taken, in the unit's current), the intervals elapsed, the windows closed, the count taken and the fractions per level at the window's start."""

    name: str
    body: int | None
    frame: frames.Frame | None
    region: np.ndarray
    front: list[np.ndarray]
    holder: int
    skip: int | None
    unit: int
    period: int
    window: int = 0
    books: int = 0
    elapsed: int = 0
    windows: int = 0
    count: int = 0
    per_node: Any = None
    opened: list[float] = field(default_factory=list)


def light_lines(board: Lattice, holder: int, skip: int | None) -> list[Record]:
    """The holder of the sign's record as a taker reads it (ALGEBRA.md, No record reads its own write of the sign; a reading of the lines into a Record, no level written): each of its lines summed over every row but `skip`, the reader's own (`records.row_levels`, both levels; every row for a region), the remainder the free row's."""
    family, lines = board.families[holder], board.states[holder].lines
    found = []
    for line in range(family.width):
        now, before = (row_levels(family, lines, line, side, skip) for side in (1, -1))
        found.append(Record(np.asarray(now), np.asarray(before), lines[line].remainder))
    return found


def standing_region(board: Lattice, index: int, record: int) -> np.ndarray:
    """A body's standing region at the lay: its record's share at every Node (share.family_share at the record's own read), the Nodes taken in the order of their shares until they hold half the record's share, the count's own rounding as the floor; the declared Node alone where the share is nowhere above 0."""
    family, gamma = board.families[index], board.world.node_clock
    content, factors = board.read(index, 1, record)
    shares = share.family_share(
        family, board.lines_of(index, record), board.wrap, gamma, content, factors, board.unit
    )
    flat = np.asarray(shares, dtype=object).ravel()
    order = sorted(range(flat.size), key=lambda k: -int(flat[k]))
    total, taken, found = int(sum(int(v) for v in flat)), 0, np.zeros(flat.size, dtype=bool)
    for place in order:
        if 2 * taken >= total or int(flat[place]) <= 0:
            break
        found[place], taken = True, taken + int(flat[place])
    return found.reshape(board.shape)


def takers_of(board: Lattice) -> list[Taker]:
    """The world's takers at the lay under the key `takers` (`World.takers`; none without it): every laid body of a turned family whose frame carries a transition (frame.frame_of; a frozen record, every level at one rotation, is none, said in a line), with its region, its front, its unit and its period read from the board; then every declared region NodeDetector where the bodies' transitions are one (the one unit and period the region reads in; none otherwise, said in a line)."""
    found: list[Taker] = []
    if not board.world.takers:
        return found
    declared = board.declared_board()
    for number, (record, row) in enumerate(board.laid_rows()):
        if (
            not isinstance(row, BodyRow)
            or row.detector is not None
            or not turns(board.families, row.family)
        ):
            continue
        name = f"{reports.BODY} {number}"
        if board.families[row.family].pair[0] == 0:  # the frozen pair: no hop, no frame
            said(board, row.family, name, {reports.TAKEN: reports.FROZEN})
            continue
        frame = frames.frame_of(board, row.family, record)
        if frame is None:
            said(board, row.family, name, {reports.TAKEN: reports.UNMOVED})
            continue
        region = standing_region(board, row.family, record)
        front = reports.front(region, board.wrap, region, declared)
        own = row_of(board.families, row.family, record)
        taker = Taker(name, number, frame, region, front, frame.holder, own, frame.unit, frame.period)
        taker.per_node = np.zeros(board.shape, dtype=object)
        taker.opened = frames.shares_of(board, frame)[0]
        found.append(taker)
        said(board, row.family, name, instrument(board, taker))
    units = {(t.unit, t.period, t.holder) for t in found if t.body is not None}
    for detector in board.node_detectors:
        if not detector.declared or detector.nodes is None:
            continue
        if len(units) != 1:
            said(
                board,
                0,
                detector.name,
                {reports.TAKEN: f"no unit: the bodies carry {len(units)} transitions, no taker"},
            )
            continue
        (unit, period, holder) = next(iter(units))
        front = reports.front(detector.nodes, board.wrap, detector.nodes, declared)
        taker = Taker(detector.name, None, None, detector.nodes, front, holder, None, unit, period)
        taker.per_node = np.zeros(board.shape, dtype=object)
        found.append(taker)
        said(board, holder, detector.name, instrument(board, taker))
    return found


def instrument(board: Lattice, taker: Taker) -> dict[str, object]:
    """A taker's instrument as its first line reads it: its Nodes, its front Ports, its unit, its window, and for a body its levels and transition."""
    found: dict[str, object] = {
        reports.NODES: int(taker.region.sum()),
        reports.FRONT: int(sum(int(mask.sum()) for mask in taker.front)),
        reports.UNIT: taker.unit,
        reports.WINDOW_WORD: taker.period,
    }
    if taker.frame is not None:
        family = board.families[taker.frame.index]
        found[reports.LEVELS] = [frames.level_kind(family, level) for level in taker.frame.levels]
        found[reports.PARTS] = [taker.frame.lower, taker.frame.upper]
        found[reports.SHARES] = [round(f, 6) for f in taker.opened]
    return found


def said(board: Lattice, index: int, name: str, reading: dict[str, object]) -> None:
    """A taker's LATTICE line (reports.taker), where the board has an output."""
    if board.output is not None:
        board.output(reports.taker(board.interval, board.families[index].name, name, reading))


def energies(board: Lattice) -> dict[str, float | None]:
    """The energy books, a lattice reading in units of T: every family of quanta's share over the board over W_c = 3 den T (a holder's under the Lorentz form over thirds too), and their sum."""
    found: dict[str, float | None] = {}
    for index in board.order:
        family = board.families[index]
        total = board.total_share(index)[0]
        wall = (
            3 * family.pair[1] * board.world.quantum_action * (covector.THIRDS if family.lorentz else 1)
        )
        found[family.name] = None if total is None else total / wall
    found[reports.SUM] = sum(v for v in found.values() if v is not None)
    return found


def read_of(board: Lattice, taker: Taker, total: int) -> tuple[int, tuple[int, int]]:
    """The taker's read of the board for a draw whose weights sum to `total` (ALGEBRA.md, The click's read of the board; The digits' budget): the digits of the holder of the sign at its Nodes (digits.digits_of: light's record, the free row, on the lattice gcd(w, D_i, R_ij), three values a digit at the vacuum paces) and of every other row of the holder standing there, the light in a body's row (`rows_read`), then for a body its own record's on the fine lattice of a turned plane (the gcd with the Link pairs the step reads, digits.lattice_of since 2026-10-21), the index r div F in the base w div F + 1, a remainder at the lay's origin skipped and a copy of an earlier line's at the same Node read once; refused by name where the digits' capacity in bits, SUM log2(w div F + 1) over the digits read, is below the total's bits, never per digit; the number with its two moduli as digits.read_of returns them."""
    digits_read: list[int] = []
    bases: list[int] = []
    reads: list[tuple[int, int | None]] = [(taker.holder, None)]
    if taker.frame is not None:
        reads.append((taker.frame.index, taker.frame.record))
    at = taker.region
    for index, record in reads:
        half = board.half_wall(index)
        earlier: dict[tuple[int, int], list[int]] = {}
        for remainder, found, wall, place in digits.digits_of(board, index, at):
            if record is not None and place[0] != record:
                continue  # a body reads its own record's digits
            standing = earlier.setdefault(place, [])
            if remainder == half or any(remainder in (kept, wall - kept) for kept in standing):
                continue
            standing.append(remainder)
            digits_read.append(int(division_forward(remainder, found, 0)[0]))
            bases.append(int(division_forward(wall, found, 0)[0]) + 1)
        if record is None:  # the holder's other rows at the region: the light a body wrote
            rows_read(board, index, at, digits_read, bases)
    capacity = sum((base - 1).bit_length() for base in bases)
    if not bases or capacity < total.bit_length():
        raise RuntimeError(
            f"the taker {taker.name!r} at the interval {board.interval} reads {len(bases)} digits of {capacity} bits "
            f"at its Nodes, below the draw's total of {total.bit_length()} bits: the board at the taker does not "
            "carry the draw (ALGEBRA.md, The digits' budget); the run is refused"
        )
    summed = gcd(*(base - 1 for base in bases[1:])) if len(bases) > 1 else 1
    return read_number(digits_read, bases), (summed, bases[-1])


def rows_read(
    board: Lattice, holder: int, at: np.ndarray, digits_read: list[int], bases: list[int]
) -> None:
    """The holder's rows beyond the free row at the Nodes `at`, each line's remainder as a digit on the holder's own lattice (digits.lattice_of on the holder's rule, the free row's read), the origin skipped and each row's copies read once: the light a body's write carries."""
    family, gamma = board.families[holder], board.world.node_clock
    content, factors = board.read(holder, 1, 0)
    rule = node.rule_of(family, gamma, content, factors, board.unit)
    lattice, wall, half = digits.lattice_of(rule, at), int(rule.wall), board.half_wall(holder)
    lines = board.states[holder].lines
    for row in range(1, family.records):
        earlier: dict[int, list[int]] = {}
        for line in lines[row * family.width : (row + 1) * family.width]:
            kept = [int(r) for r in np.asarray(line.remainder)[at]]
            for place, (remainder, found) in enumerate(zip(kept, lattice, strict=True)):
                standing = earlier.setdefault(place, [])
                if remainder == half or any(remainder in (k, wall - k) for k in standing):
                    continue
                standing.append(remainder)
                digits_read.append(int(division_forward(remainder, found, 0)[0]))
                bases.append(int(division_forward(wall, found, 0)[0]) + 1)


def booked(board: Lattice, taker: Taker) -> int:
    """One interval's booking: the light the taker reads (`light_lines`) through its front, the plain current of the holder's lines at the covector's weights (readings.currents_of), per Node (reports.entering) into the window's inflow per Node, their sum into the window and the books; returns the interval's inflow."""
    holder = board.families[taker.holder]
    through = readings.currents_of(
        holder.pair[0],
        light_lines(board, taker.holder, taker.skip),
        board.wrap,
        covector.weights(holder),
    )
    came = reports.entering(taker.front, through)
    taker.per_node = taker.per_node + np.asarray(came, dtype=object)
    total = int(np.asarray(came, dtype=object).sum())
    taker.window, taker.books = taker.window + total, taker.books + total
    return total


def giver_of(board: Lattice, taker: Taker, number: int) -> tuple[Taker | None, int]:
    """The WHO: the body whose light the taker took, drawn among the world's body takers but the taker itself by their shares in their upper levels (one above 0 a certain draw, the number consumed by nothing), with the number left; None where no body stands in an upper level (the light the lay's)."""
    candidates = [
        t for t in board.credit.takers if t.body is not None and t is not taker and t.frame is not None
    ]
    weights = []
    for candidate in candidates:
        assert candidate.frame is not None
        fractions = frames.shares_of(board, candidate.frame)[0]
        weights.append(int(round(fractions[candidate.frame.upper] * candidate.unit)))
    if not candidates or sum(weights) <= 0:
        return None, number
    pick, left = drawn_from(
        number, weights, f"the giver of {taker.name!r} at the interval {board.interval}"
    )
    return candidates[pick], left


def hole(board: Lattice, taker: Taker, at: tuple[int, ...]) -> str:
    """The light's hole at the drawn Node where the light stands in a quanta record, the holder's free row 0 (every line of the row to 0 through the one lay act), and none where the free row is 0 there, the light standing in a held row, a body's own write; the word for the line."""
    family, lines = board.families[taker.holder], board.states[taker.holder].lines
    free = lines[: family.width]
    if not any(int(line.now[at]) or int(line.before[at]) for line in free):
        return reports.HELD_LIGHT
    origin = board.half_wall(taker.holder)
    mask = np.zeros(board.shape, dtype=bool)
    mask[at] = True
    for number, line in enumerate(free):
        changes = (np.where(mask, -np.asarray(line.now), 0), np.where(mask, -np.asarray(line.before), 0))
        laid(board, taker.holder, number, changes, None, origin, mask)
    return reports.HOLE


def taken(board: Lattice, taker: Taker, number: int, moduli: tuple[int, int]) -> dict[str, object]:
    """A take: the WHERE drawn by the window's inflow per Node (one division act of the number left, the Node at the file's coordinates), the WHO (`giver_of`), the credit (count +1, the books less one unit), the WRITE (the taker body's record in its upper level at the count whole with the arriving phase, the giver's in its lower level at the count whole, the light's hole at the Node where the light is the free row's), the energy books before and after, and the engine's credit line."""
    nodes = [tuple(int(v) for v in here) for here in np.argwhere(taker.region)]
    weights = [max(int(w), 0) for w in taker.per_node[taker.region]]
    label = f"the taker {taker.name!r} at the interval {board.interval}"
    if sum(weights) > 0:
        pick, number = drawn_from(number, weights, label, moduli)
    else:
        pick = 0
    where = nodes[pick]
    giver, number = giver_of(board, taker, number)
    before = energies(board)
    written: dict[str, object] = {reports.AT: list(where)}
    if taker.frame is not None:
        fractions, coefficients = frames.shares_of(board, taker.frame)
        frames.relaid(board, taker.frame, taker.frame.upper, coefficients[taker.frame.upper], 1, None)
        written[reports.REALISED] = frames.level_kind(
            board.families[taker.frame.index], taker.frame.levels[taker.frame.upper]
        )
    if giver is not None and giver.frame is not None:
        fractions, coefficients = frames.shares_of(board, giver.frame)
        frames.relaid(board, giver.frame, giver.frame.lower, coefficients[giver.frame.lower], 1, None)
        written[reports.GIVER] = {giver.name: [round(f, 6) for f in fractions]}
    written[reports.LIGHT] = hole(board, taker, where)
    taker.count, taker.books = taker.count + 1, taker.books - taker.unit
    written[reports.ENERGY] = {reports.BEFORE: before, reports.AFTER: energies(board)}
    if board.output is not None:
        family = board.families[taker.holder].name
        window = [board.interval - taker.period + 1, board.interval]
        source = reports.THE_LAY if giver is None else giver.name
        board.output(
            reports.credit(
                board.interval,
                family,
                taker.name,
                window,
                board.interval,
                taker.windows,
                None,
                None,
                1,
                None,
                absorbed=family,
                source=source,
            )
        )
    return written


def closed(board: Lattice, taker: Taker) -> None:
    """The window's close: the WHETHER drawn on the taker's own digits against [the window's inflow floored at 0 and capped at W_rec, W_rec less it] (the geometric draw, the share the hazard; nothing drawn at an inflow of 0 or below, a certain take at W_rec or above), the take where drawn (`taken`), the window begun again with its excess carried and the books carried on; one LATTICE `taker` line per close with the reader's numbers."""
    unit, window = taker.unit, taker.window
    weight = min(max(window, 0), unit)
    reading: dict[str, object] = {
        reports.WINDOW_WORD: [board.interval - taker.period + 1, board.interval],
        reports.INFLOW: window,
        reports.BOOKED: taker.books,
        reports.UNIT: unit,
        reports.WEIGHTS: [weight, unit - weight],
        reports.COUNT: taker.count,
    }
    if taker.frame is not None:
        fractions = frames.shares_of(board, taker.frame)[0]
        reading[reports.SHARES] = [round(f, 6) for f in fractions]
        taker.opened = fractions
    if weight <= 0:
        reading[reports.TAKEN] = reports.NOTHING
    else:
        number, moduli = read_of(board, taker, unit)
        reading[reports.DIGITS] = number.bit_length()
        if weight < unit:
            pick, number = drawn_from(
                number, [weight, unit - weight], f"whether, {taker.name!r} at {board.interval}", moduli
            )
        else:
            pick = 0
        reading[reports.TAKEN] = pick == 0
        if pick == 0:
            reading[reports.WRITTEN] = taken(board, taker, number, moduli)
    taker.window = max(window - unit, 0) if weight >= unit else 0
    taker.per_node = np.zeros(board.shape, dtype=object)
    taker.elapsed, taker.windows = 0, taker.windows + 1
    said(board, taker.holder, taker.name, reading)


def jumped(board: Lattice) -> None:
    """The takers' act at the end of an interval, after the declared bodies' (meeting.jumped): every taker's frame advanced by the interval's acts (frame.advanced), its booking (`booked`), and at its window's length its close (`closed`); nothing on a world without the key."""
    for taker in board.credit.takers:
        if taker.frame is not None:
            frames.advanced(board, taker.frame)
        booked(board, taker)
        taker.elapsed += 1
        if taker.elapsed >= taker.period:
            closed(board, taker)
