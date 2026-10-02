"""The families from the rule (ALGEBRA.md #a-familys-declaration, every family has a dimension): a family's row holds its name, its pair and either its dimension (a family of quanta: one real line, or a plane of two) or what sources it (a held row: the form, the tensions, the Wronskian) at its level weight (the quanta of form that write one level of the row) and its rest, and the rule derives the rest from these alone with no name (who reads whom, who sources whom, the one write per held part with its walls); the amplitude bound A is derived from the integer width by the fixed point of the division act, never written and never by a root (ALGEBRA.md #the-bound)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from math import gcd

from event_universe.core.rule3 import coefficients, division_fixed_point, division_forward
from event_universe.features.currents import AXIS_PORTS, PORTS, PRODUCTS
from event_universe.features.read import edge_of
from event_universe.features.rotation import TURNED_REACH, TURNED_SLACK


@dataclass(frozen=True)
class Row:
    """A family's row as the loader reads it from the universe file: its name, its pair [num, den], its lines in all (a family of quanta's dimension, 1 or 2, times its parts; a held row's sources' count, one real line per source, and the three odd axis lines of a holder of the sign under the rotation), its parts (the records of one event never summed at a Node, 2 for the pair family, 1 otherwise), whether its lines are planes (re and im: charged matter), whether it is sourced by its readers' Wronskian (the holder of the sign; else by their form, and by their tensions where it has the axis lines), whether it acts on its readers by the rotation of the two-part record (the holder of the sign's declared act; else by the plain read into their paces), its level weight where it is held (the quanta of form that write one level of the row) and its rest."""

    name: str
    pair: tuple[int, int]
    lines: int
    parts: int
    plane: bool
    wronskian: bool
    rotation: bool
    level_weight: int | None
    rest: int
    records: int = 1  # a charged family's laid records, each owning one row of the sign; a holder of the sign's rows, 1 + the world's charged records; 1 otherwise (ALGEBRA.md, No record reads its own write of the sign)


@dataclass(frozen=True)
class Read:
    """One read of a family: the held family whose time line it reads at the weight 1 of the rule, by the plain read into its paces."""

    family: int
    weight: int


@dataclass(frozen=True)
class FamilyRule(Row):
    """A family as the rule derives it from its row (`Row`) with its reads: the held rows whose time line it reads, which by the hold's reciprocity it sources at the same weights; its rest the vacuum content of the massless row holding the content, the level at which the row rests everywhere, 0 for every other row (ALGEBRA.md #what-is-open, item 22)."""

    reads: tuple[Read, ...] = ()

    @property
    def held(self) -> bool:
        """Whether the family is held: a row with a level weight, written by the hold and read by others."""
        return self.level_weight is not None

    @property
    def quanta(self) -> bool:
        """Whether the family carries quanta, stepping at the paces of its reads with its share its count and its currents a detector's reading: every family of quanta and the holder of the sign, whose own record is light; a held row sourced by the form holds the content and steps at the pace 1."""
        return not self.held or self.wronskian

    @property
    def width(self) -> int:
        """The lines of one part of one record, the lines in all over the parts and the records: one real line, or a plane's two; a held row's time line with its axis lines (ALGEBRA.md #a-familys-declaration, the dimension's table)."""
        return self.lines // (self.parts * self.records)

    @property
    def axes(self) -> bool:
        """Whether the row carries three axis lines beside its time line: a held row sourced by the tensions (the massless row holding the content, read into the Link's paces), or the holder of the sign under the rotation (the odd lines, the phase on the Link), every row of it alike."""
        return self.held and self.width > 1

    @property
    def record(self) -> int:
        """The lines of the family's record of quanta, the ones its share, its currents, its form and its Wronskian are read from: every line of a family of quanta; the time line alone of a held row (light, the holder of the sign's own record), its axis lines being held parts."""
        return 1 if self.held else self.lines


def turns(families: tuple[FamilyRule, ...], index: int) -> bool:
    """Whether a family's record is turned: a plane that reads a holder declaring the rotation (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record); a one-part family reads no holder of the sign and is untouched, as is a plane in a universe whose holders act on the pace."""
    family = families[index]
    return family.plane and any(families[read.family].rotation for read in family.reads)


def charged(families: tuple[FamilyRule, ...], index: int) -> bool:
    """Whether a family reads a holder of the sign, plainly or by the turn: every record of such a family owns one row of the sign at every Node (ALGEBRA.md, No record reads its own write of the sign)."""
    return families[index].quanta and any(
        families[read.family].wronskian for read in families[index].reads
    )


def row_of(families: tuple[FamilyRule, ...], index: int, record: int) -> int | None:
    """The row of every holder of the sign that the record `record` of the family `index` owns, the one its Wronskian is written into and the one its read leaves out: the row 0 is owned by no record (the free row, the laid light's), and the charged families' records take the rows after it in the file's order; None where the family reads no holder of the sign."""
    if not charged(families, index):
        return None
    return (
        1 + sum(families[other].records for other in range(index) if charged(families, other)) + record
    )


def with_records(families: tuple[FamilyRule, ...], laid: Sequence[int]) -> tuple[FamilyRule, ...]:
    """The families with the world's records: a charged family's records are its bodies (`laid`, per family its bodies in the world's order; a message of such a family, a packet and no standing record, adds into its first record), one at least, each its own lines and its own row of the sign; every holder of the sign carries one row per charged record beside the row no record owns, its lines that many times its row's lines (the time line, with its three odd lines under the rotation); every other family as the universe declares it."""
    rows = 1 + sum(max(1, laid[index]) for index in range(len(families)) if charged(families, index))
    found = []
    for index, family in enumerate(families):
        if charged(families, index):
            records = max(1, laid[index])
            found.append(replace(family, lines=family.width * family.parts * records, records=records))
        elif family.wronskian:
            found.append(replace(family, lines=family.width * rows, records=rows))
        else:
            found.append(family)
    return tuple(found)


def quanta_records(families: tuple[FamilyRule, ...], index: int) -> range:
    """The records of quanta of a family, each read, stepped and booked at its own paces: every record of a family that reads a holder of the sign (each its own lines and its own row of the sign), the one record of every other family of quanta, a holder of the sign's one record, light, among them (its rows are rows of the sign and no records of light)."""
    return range(1 if families[index].wronskian else families[index].records)


def row_sources(families: tuple[FamilyRule, ...], held: int, row: int) -> list[tuple[int, int]]:
    """The records that source one row of a held family, (reader, record) pairs (ALGEBRA.md #the-primitives, the hold's reciprocity; No record reads its own write of the sign): every record of every reader for a holder of the content, whose one row is the sum of its readers' forms; for a holder of the sign the one record that owns the row, and none for the row 0, which no record writes."""
    sources = [
        (reader, record)
        for reader in readers_of(families, held)
        for record in quanta_records(families, reader)
    ]
    if not families[held].wronskian:
        return sources
    return [(reader, record) for reader, record in sources if row_of(families, reader, record) == row]


@dataclass(frozen=True)
class HeldWrite:
    """A held family's one write per line as the rule derives it from the rows (ALGEBRA.md #the-primitives, a family's write is one act): the walls, one per line, the time line's E_s T and each axis line's E_s times one measure of a current of the families that source it, the quantum's W_c = 3 den T for a tension line and one axis's den T for an odd line (ALGEBRA.md #the-rows-against-nature (b2), the wall den T; one den among the sources; with several, the least common multiple of their den in den's place), and per sourcing family the factor with which its tension or its momentum density enters the axis parts' numerator, the multiple over its own den (1 where one den serves every source), so that the sum of the sources' fractions is one fraction over one wall, exact."""

    walls: tuple[int, ...]
    factors: dict[int, int]


def family_rules(rows: list[Row]) -> tuple[FamilyRule, ...]:
    """Every family from its row by the pair and the dimension alone (ALGEBRA.md #a-familys-declaration, the dimension's table): a family of quanta reads every held row sourced by the form (the content) at the weight 1 and, where it is a plane, every held row sourced by the Wronskian (the sign); a held row sourced by the form reads nothing, and a row never reads its own level (light, the sign row's own real record, reads no holder of the sign); by the hold's reciprocity a family sources what it reads at the same weight, a plane with its Wronskian and real lines with their form and their tensions; no family gives another anything."""
    found = []
    for index, row in enumerate(rows):
        reads: list[Read] = []
        for other, held in enumerate(rows):
            if held.level_weight is not None and other != index and row.plane and held.wronskian:
                reads.append(Read(other, 1))  # a plane reads every holder of the sign
            elif held.level_weight is not None and not held.wronskian:
                reads.append(
                    Read(other, 1)
                )  # every row reads every holder of the content, itself among them
        found.append(
            FamilyRule(
                row.name,
                row.pair,
                row.lines,
                row.parts,
                row.plane,
                row.wronskian,
                row.rotation,
                row.level_weight,
                row.rest,
                reads=tuple(reads),
            )
        )
    return with_records(
        tuple(found), [0] * len(found)
    )  # one record per charged family until a world lays its bodies


def weight_of(held: int, reader: FamilyRule) -> int:
    """The weight with which a family reads a held family, and so sources it, the one weight of the pair (ALGEBRA.md #the-primitives, a family's write: whoever reads with w sources with w), 0 where it does not read it."""
    return sum(read.weight for read in reader.reads if read.family == held)


def readers_of(families: tuple[FamilyRule, ...], held: int) -> list[int]:
    """The families of quanta that read the held family `held`, and so source it, in the file's order (ALGEBRA.md #the-primitives, A family's write is one act: the writer's quantity is a family of quanta's form, Wronskian or tension); a held row of the content reads the content as every family does since Every row reads the content, its own level among it, and sources nothing by the write."""
    return [other for other, family in enumerate(families) if weight_of(held, family) and family.quanta]


def count_wall(family: FamilyRule, action: int) -> int:
    """The count's wall W_c = 3 den T, the family's plain wall times the universe's quantum action: the unit in which a share is read as quanta (ALGEBRA.md #the-count-is-the-records-share)."""
    return 3 * family.pair[1] * action


def held_write(families: tuple[FamilyRule, ...], index: int, action: int) -> HeldWrite:
    """The one write per line of the held family `index` (`HeldWrite`): its walls from the row's level weight, the quantum action and the den of the families that source its axis lines (its readers, whose tension or momentum density it takes), the multiple of their den by the division act on the greatest common divisor, the measure of a current on each axis line (W_c's 3 den T for the tensions, den T for the odd lines), and each source's factor, the multiple over its den."""
    family = families[index]
    assert family.level_weight is not None
    sources = readers_of(families, index)
    multiple = 1
    for other in sources:
        den = families[other].pair[1]
        multiple = int(division_forward(multiple * den, gcd(multiple, den), 0)[0])
    measure = multiple * action if family.rotation else 3 * multiple * action
    row = [family.level_weight * action] + [family.level_weight * measure] * (family.width - 1)
    walls = (
        row * family.records
    )  # one wall per line of every row, the rows of a holder of the sign alike
    factors = {
        other: int(division_forward(multiple, families[other].pair[1], 0)[0]) for other in sources
    }
    return HeldWrite(tuple(walls), factors)


def largest_of(width: int) -> int:
    """The largest integer of the file's width in bits, 2^width - 1, the bound every total of the law stays inside (ALGEBRA.md #the-bound)."""
    return int(2**width - 1)


def booking_room(families: tuple[FamilyRule, ...], index: int, wronskian: bool) -> int:
    """The room of one source's booking at the amplitude A, its size over A^2: the Wronskian's two products, or the form's two per line of its record (now^2 and next x before); where the source's record is turned (`turns`) the booking is read from the step's levels before the turn, each within twice A once A is read as A + 2 (features/rotation, `TURNED_REACH`, `TURNED_SLACK`; `amplitude_bound`): the Wronskian's two products of a turned level and a level, the form's now^2 and the two turned levels' product per line."""
    reach = TURNED_REACH if turns(families, index) else 1
    if wronskian:
        return PRODUCTS * reach
    return families[index].record * (1 + reach * reach if reach > 1 else PRODUCTS)


def hill_scale(pair: tuple[int, int], gamma: int) -> tuple[int, int, int]:
    """The write's factor at a source's hill's edge (ALGEBRA.md, The write per proper volume and per proper interval; The guard): P the edge's pace of the source's pair, the largest the guard admits (`features/read`, `edge_of`), where the factor N^k p_x p_y p_z / p_0^3 is at most (P / Gamma)^3 (1 at most in a hollow, every pace at or below Gamma); returns P, the factor's room P^3 div Gamma^3 rounded up, which multiplies the booking's room in the write's numerator, and the per-axis booking's room P^3 div Gamma^2 rounded up, the scaled booking times the last pace before its division, the largest intermediate of the three divisions (every earlier one smaller, P at or above Gamma)."""
    edge = edge_of(pair, gamma)
    cube, square = gamma * gamma * gamma, gamma * gamma
    factor = int(division_forward(edge * edge * edge, cube, cube - 1)[0])
    intermediate = int(division_forward(edge * edge * edge, square, square - 1)[0])
    return edge, factor, intermediate


def write_rooms(families: tuple[FamilyRule, ...], index: int, write: HeldWrite, gamma: int) -> list[int]:
    """The room of a held family's one write per part at the amplitude A, the numerator's size over A^2 at the largest level: for the time part SUM over the sourcing families of w x the room of the booking the row takes, the form or the Wronskian (`booking_room`), times the write's factor's room at the source's hill's edge (`hill_scale`, 1 in a hollow); for each axis part SUM over the sources of w x factor x lines x 2 |num| for a tension line (the tension's part per line of the source's record, two products of two levels, |num| on each) and w x factor x lines x 2 x 2 for an odd line (the sign's current across the axis's two Ports, two products each: the room of the two Links' currents, within which their mean, the source, stays)."""
    family = families[index]
    sources = readers_of(families, index)
    time = sum(
        abs(weight_of(index, families[other]))
        * booking_room(families, other, family.wronskian)
        * hill_scale(families[other].pair, gamma)[1]
        for other in sources
    )
    axis = sum(
        abs(weight_of(index, families[other]))
        * write.factors[other]
        * families[other].record
        * PRODUCTS
        * (AXIS_PORTS if family.rotation else abs(families[other].pair[0]))
        for other in sources
    )
    return ([time] + [axis] * (family.width - 1)) * family.records


def amplitude_bound(
    families: tuple[FamilyRule, ...], gamma: int, action: int, width: int, unit: int = 1
) -> int:
    """The amplitude bound A, derived and never written: the largest level at which Rule3's total 6 A R + A |S| + w (A + 1) stays inside the file's width for every pair at the vacuum's paces, at a frozen clock (the paces 0, the bound the deepest hollow approaches: |S| grows to 12 den Gamma^2 G^2 as the paces fall) and at the hill's edge P on the clock and the pace alike (`features/read`, `edge_of`; the three the extremes of the guard, ALGEBRA.md #the-bound, #the-paces, The guard; for a turned record the six arrivals within twice A, `TURNED_REACH`, and the three shears' largest product, 2 n w x1 at the tangent half-angle 1 on a Link with x1 within twice A and one, features/rotation), at which the currents' reading at a Node, 6 x 2 x lines x |num| A^2 for every family of quanta (the two products of each of the record's lines through the six Ports; the largest A whose square fits, the fixed point of the division act), does too (features/currents), at which every held family's one write per part, its numerator at the sources' room with the write's factor at the hill's edge (`write_rooms`) plus its remainder under the wall, does too, and at which the write's factor's per-axis booking, the scaled booking times one pace before its division rounded half up, 2 x the booking's room x P^3 div Gamma^2 x A^2 + 2 P per source (`hill_scale`; ALGEBRA.md, The write per proper volume and per proper interval, the engine's booking), does too; refused by name where no level fits. Where a holder turns a record (features/rotation) every room of the universe is read at the level A + 2 and the level found is 2 less (`TURNED_SLACK`: a turned level stays below 2^(1 / 2) A + 3, within twice A + 2, and not within twice A, the audit's witness (-1, -1) turning to (-3, -1) at A = 1), the turned record's total 6 R x twice the level + |S| A + w x twice the level + w (its six arrivals and the level before it is stepped against both turned, `TURNED_REACH`), the three shears' largest product 2 n w x1 at the tangent half-angle 1 on a Link with x1 within twice the level and one, and its bookings' products of turned levels (`booking_room`)."""
    largest = largest_of(width)
    found = largest
    slack = TURNED_SLACK if any(turns(families, index) for index in range(len(families))) else 0
    for index, family in enumerate(families):
        num, den = family.pair
        reach = TURNED_REACH if turns(families, index) else 1
        edge = edge_of(family.pair, gamma)
        for clock, pace in ((gamma, gamma), (0, 0), (edge, edge)):
            reads, self_coefficient, wall = coefficients(num, den, gamma, clock, pace, None, unit)
            room = (sum(abs(read) for read in reads) + wall) * reach + abs(self_coefficient)
            found = min(found, int(division_forward(largest - wall, room, 0)[0]) - slack)
        if reach > 1:
            link = 2 * 2 * gamma  # the Link's wall, tan(theta_a / 2) = (L_a(i) + L_a(j)) / (4 Gamma)
            product = int(division_forward(largest, 2 * link * link, 0)[0])  # 2 n w x1 at n = w
            found = min(found, int(division_forward(product - 1, reach, 0)[0]) - slack)
        if family.quanta and num:
            room = PORTS * PRODUCTS * family.record * abs(num)
            found = min(found, division_fixed_point(int(division_forward(largest, room, 0)[0])) - slack)
        if family.held:
            write = held_write(families, index, action)
            for wall, room in zip(write.walls, write_rooms(families, index, write, gamma), strict=True):
                if wall > largest:
                    found = 0
                elif room:
                    fits = int(division_forward(largest - wall, room, 0)[0])
                    found = min(found, division_fixed_point(fits) - slack)
            for other in readers_of(families, index):
                edge, _factor, intermediate = hill_scale(families[other].pair, gamma)
                room = 2 * booking_room(families, other, family.wronskian) * intermediate
                fits = int(division_forward(largest - 2 * edge, room, 0)[0])
                found = min(found, division_fixed_point(fits) - slack)
        if found < 1:
            raise ValueError(
                f"the pair [{num}, {den}] at the Node clock Gamma = {gamma} and T = {action}: the totals of "
                f"Rule3, of the currents and of the write leave no level inside the width of {width} bits "
                "(ALGEBRA.md #the-bound)"
            )
    return found
