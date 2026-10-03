"""The families from the rule (ALGEBRA.md #a-familys-declaration, every family has a dimension): a family's row holds its name, its pair, either its dimension (a family of quanta: any integer from 1, the lines of its record, one real line, a plane of two, or three or more real lines, each stepped as a line of dimension one) or what sources it (a held row: the form, the tensions, the Wronskian) at its level weight (the quanta of form that write one level of the row), its write weight (the multiplier of its one write) and its rest, and the holders it reads with their weights, as its declaration names them; the rule derives the rest from these alone with no name and no default (the lines, who sources whom by the hold's reciprocity, the one write per held part with its walls); the amplitude bound A is derived from the integer width by the fixed point of the division act, never written and never by a root (ALGEBRA.md #the-bound)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from math import gcd

from event_universe.core.rule3 import coefficients, division_fixed_point, division_forward
from event_universe.features.currents import AXIS_PORTS, PORTS, PRODUCTS
from event_universe.features.read import edge_of
from event_universe.features.rotation import TURNED_REACH, TURNED_SLACK

PLANE = 2  # the lines of a plane, re and im: the one shape with a Wronskian and a turn (charged matter)
REAL_LINE, PLANE_LINE = (
    "real",
    "plane",
)  # the kinds of a record's lines, the shape by name (the two hands of 2026-10-03)
KINDS = (REAL_LINE, PLANE_LINE)


@dataclass(frozen=True)
class Row:
    """A family's row as the loader reads it from the universe file: its name, its pair [num, den], its lines in all (a family of quanta's dimension, any integer from 1, times its parts; a held row's sources' count, one real line per source, and the three odd axis lines of a holder of the sign under the rotation), its parts (the records of one event never summed at a Node, 2 for the pair family, 1 otherwise), whether its lines are planes (the dimension 2, re and im: charged matter, the one dimension with a Wronskian and a turn; every other dimension real lines, which read none of the sign), whether it is sourced by its readers' Wronskian (the holder of the sign; else by their form, and by their tensions where it has the axis lines), whether it acts on its readers by the rotation of the two-part record (the holder of the sign's declared act; else by the plain read into their paces), its level weight where it is held (the quanta of form that write one level of the row), its write weight where it is held (the signed multiplier of its one write per line, the files' key `write_weight`: the sign holder's k_w, a nuclear holder's W_1 or -W_2), its rest, and the holders its declaration names with the weight it reads each with (`declared`, the files' key `reads`, by name; empty where it reads none)."""

    name: str
    pair: tuple[int, int]
    lines: int
    parts: int
    plane: bool
    wronskian: bool
    rotation: bool
    level_weight: int | None
    write_weight: int | None
    rest: int
    declared: tuple[tuple[str, int], ...]
    records: int = 1  # a charged family's laid records, each owning one row of the sign; a holder of the sign's rows, 1 + the world's charged records; 1 otherwise (ALGEBRA.md, No record reads its own write of the sign)


@dataclass(frozen=True)
class Read:
    """One read of a family as its declaration names it: the held family whose time line it reads and the weight it reads with, by the plain read into its paces or, where the holder declares the rotation, as the turn of its record; by the hold's reciprocity the weight it sources that holder with."""

    family: int
    weight: int


@dataclass(frozen=True)
class FamilyRule(Row):
    """A family as the rule resolves it from its row (`Row`) with its reads by position: the held rows whose time line it reads at the weights its declaration names, which by the hold's reciprocity it sources at the same weights; its rest the vacuum content of the massless row holding the content, the level at which the row rests everywhere, 0 for every other row (ALGEBRA.md #what-is-open, item 22)."""

    reads: tuple[Read, ...] = ()

    @property
    def held(self) -> bool:
        """Whether the family is held: a row with a level weight, written by the hold and read by others."""
        return self.level_weight is not None

    @property
    def write(self) -> int:
        """The held row's write weight, the signed multiplier of its one write per line (the files' key `write_weight`, read as the row's level weight is); a family that holds nothing has no write."""
        assert self.write_weight is not None, f"{self.name!r} holds nothing and has no write"
        return self.write_weight

    @property
    def quanta(self) -> bool:
        """Whether the family carries quanta, stepping at the paces of its reads with its share its count and its currents a detector's reading: every family of quanta and the holder of the sign, whose own record is light; a held row sourced by the form holds the content and steps at the pace 1."""
        return not self.held or self.wronskian

    @property
    def width(self) -> int:
        """The lines of one part of one record, the lines in all over the parts and the records: a family of quanta's dimension, one real line, a plane's two or the three of a record of three real lines; a held row's time line with its axis lines (ALGEBRA.md #a-familys-declaration, the dimension's table)."""
        return self.lines // (self.parts * self.records)

    @property
    def planes(self) -> int:
        """The planes of one part of one record, half its lines where its lines are planes (re and im, `PLANE`), 0 for real lines: one for charged matter, three for a record declared as three planes."""
        return self.width // PLANE if self.plane else 0

    @property
    def laid(self) -> int:
        """The lines of one part the laid pair goes to, one per real line and one per plane (its first line, the second line its sense): the count of a body's or a message's `weights` (`keys.weights_of`, `GameBoard.lay`)."""
        return self.planes if self.plane else self.width

    @property
    def several(self) -> bool:
        """Whether the record's lines are reported line by line in the parts line (`reports.parts`, `GameBoard.report`): a record of several parts (the pair family, the GHZ family, the nuclide's two planes) or of several real lines (a record of dimension 3), each line's signed level sums over a region; a plane's two lines, re and im, are one line and its sense, and one real line is one line, neither reported."""
        return self.parts > 1 or (self.width > 1 and not self.plane)

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
    """Whether a family reads a holder of the sign, plainly or by the turn: every record of such a family, a plane (`read_of` admits no family of real lines naming one), owns one row of the sign at every Node (ALGEBRA.md, No record reads its own write of the sign)."""
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
    """A held family's one write per line as the rule derives it from the rows (ALGEBRA.md #the-primitives, a family's write is one act): the walls, one per line, the time line's E_s T and each axis line's E_s times one measure of a current of the families that source it: the quantum's W_c = 3 den T for a tension line (one den among the sources; with several, the least common multiple of their den in den's place) and the time line's own T for an odd line, the same wall as the time level's W, so that the odd level over the time level is (J_a / 2) / W = 3 (den_s / num_s) v = v / c_s^2 as the law's (b2) computes it (ALGEBRA.md #the-rows-against-nature (b2); the mathematician's 122 D, #1572 comment 5946560198, and the advisor's #1563 comments 5946186214 and 5946604467, two hands: over den T the engine's magnetic sector was 1 / den of the law's and the odd levels of the files' bodies rounded to 0), and per sourcing family the factor with which its tension enters the axis parts' numerator, the multiple over its own den (1 where one den serves every source, and 1 for every source of an odd line, whose wall carries no den), so that the sum of the sources' fractions is one fraction over one wall, exact."""

    walls: tuple[int, ...]
    factors: dict[int, int]


def read_of(rows: Sequence[Row], index: int, name: str, weight: int) -> Read:
    """One declared read resolved to the held row's position (ALGEBRA.md, every family reads the holders its declaration names, at the weights it names), refused by name where the name is no held row of the universe file, where the holder of the sign names its own level (light reads none of the sign) and where a family of real lines, one or three, names a holder of the sign: a plane reads the holder of the sign, plainly into its pace or as the turn of its two lines, and writes it by its Wronskian, and a real line does not, neutral by itself (ALGEBRA.md #a-familys-declaration, Every family has a dimension; the advisor's second hand, #1572 comment 5963681796)."""
    names = [row.name for row in rows]
    row = rows[index]
    if name not in names or rows[names.index(name)].level_weight is None:
        raise ValueError(
            f"{row.name!r} reads {name!r}, and no held row of that name stands in the universe file: a "
            "family reads the holders its declaration names (ALGEBRA.md #a-familys-declaration)"
        )
    other = names.index(name)
    if other == index and row.wronskian:
        raise ValueError(
            f"{row.name!r} reads its own level: the holder of the sign never reads its own level, light "
            "reads none of the sign (ALGEBRA.md #a-familys-declaration)"
        )
    if rows[other].wronskian and not row.plane:
        raise ValueError(
            f"{row.name!r} reads {name!r}, a holder of the sign, with lines that are no plane: a plane reads the "
            "holder of the sign, plainly or as the turn of its two lines, and a real line does not (ALGEBRA.md "
            "#a-familys-declaration, Every family has a dimension)"
        )
    return Read(other, weight)


def family_rules(rows: Sequence[Row]) -> tuple[FamilyRule, ...]:
    """Every family from its row with its declared reads resolved by name (`read_of`; ALGEBRA.md #a-familys-declaration): a family reads the holders its declaration names at the weights it names, nothing derived from the pair or the dimension; then the world's records (`with_records`), one record per charged family until a world lays its bodies."""
    found = tuple(
        FamilyRule(
            **vars(row), reads=tuple(read_of(rows, index, name, weight) for name, weight in row.declared)
        )
        for index, row in enumerate(rows)
    )
    return with_records(found, [0] * len(found))


def energy_line(families: tuple[FamilyRule, ...], gamma: int, action: int) -> None:
    """The loader's gate of the energy line (ALGEBRA.md, energy conservation between a body and its light; the owner's word of 2026-10-02, 07:00 Israel, the advisor's hand #1563 comment 5945592281), one function with the line written once: for every plane family (dimension 2, of any parts) whose reads name a holder under the rotation h at a weight above 0, the file's integers satisfy E_h x T x num_f = k_w,h x Gamma x den_f exactly, [num_f, den_f] the family's pair (cos omega_s = num / den), E_h the holder's level weight, k_w,h its write weight, T the quantum action and Gamma the Node clock; the family's read weight multiplies its turn and, by the hold's reciprocity, its write, and cancels in the balance (it is the family's charge in units of the unit charge), so every plane family of one universe shares num / den or the universe is refused by name with the family, the holder and the four integers; a family of real lines and light (the holder's own record) read no turn and stand outside the line, as does the plain read (the act `pace`); a frozen row, a plane family at num = 0 (cos omega_s = 0 at every wave number, R_ij = 0 on every Link: its record never moves and gives no light), stands outside the line too, the balance of a body's light against its loss having nothing to balance, so the constraint that the plane families of one universe share num / den is lifted for num = 0 by name (the two hands of 2026-10-03, the advisor's #1572 comment 5966780505 and the mathematician's 236 and 242)."""
    for family in families:
        frozen = family.pair[0] == 0  # the frozen row: its record never moves and gives no light
        for read in family.reads:
            holder = families[read.family]
            if frozen or not (family.plane and holder.rotation and read.weight > 0):
                continue
            num, den = family.pair
            assert holder.level_weight is not None  # a holder under the rotation is held
            left, right = holder.level_weight * action * num, holder.write * gamma * den
            if left != right:
                raise ValueError(
                    f"the energy line fails for {family.name!r} reading {holder.name!r}: E_h x T x num = "
                    f"{holder.level_weight} x {action} x {num} = {left} and k_w x Gamma x den = {holder.write} x "
                    f"{gamma} x {den} = {right} (ALGEBRA.md, energy conservation between a body and its light: "
                    "E_h T cos omega_s = k_w Gamma; the holder's level weight, the quantum action, the holder's "
                    "write weight and the Node clock); the universe is refused"
                )


def weight_of(held: int, reader: FamilyRule) -> int:
    """The weight with which a family reads a held family, and so sources it, the one weight of the pair (ALGEBRA.md #the-primitives, a family's write: whoever reads with w sources with w), 0 where it does not read it."""
    return sum(read.weight for read in reader.reads if read.family == held)


def readers_of(families: tuple[FamilyRule, ...], held: int) -> list[int]:
    """The families of quanta that read the held family `held`, and so source it, in the file's order (ALGEBRA.md #the-primitives, A family's write is one act: the writer's quantity is a family of quanta's form, Wronskian or tension); a held row of the content reads the content as every family does since Every row reads the content, its own level among it, and sources nothing by the write."""
    return [other for other, family in enumerate(families) if weight_of(held, family) and family.quanta]


def count_wall(family: FamilyRule, action: int) -> int:
    """The count's wall W_c = 3 den T, the family's plain wall times the universe's quantum action: the unit in which a share is read as quanta (ALGEBRA.md #the-count-is-the-records-share), the energy T of a quantum at the band's top."""
    return 3 * family.pair[1] * action


def held_write(families: tuple[FamilyRule, ...], index: int, action: int) -> HeldWrite:
    """The one write per line of the held family `index` (`HeldWrite`): its walls from the row's level weight, the quantum action and, for the tension lines, the den of the families that source them (its readers, whose tension it takes), the multiple of their den by the division act on the greatest common divisor, the measure of a current on each axis line (W_c's 3 den T for the tensions; the time line's T for the odd lines, the same wall as the time level's), and each source's factor, the multiple over its den for a tension line and 1 for an odd line."""
    family = families[index]
    assert family.level_weight is not None
    sources = readers_of(families, index)
    multiple = 1
    for other in sources:
        den = families[other].pair[1]
        multiple = int(division_forward(multiple * den, gcd(multiple, den), 0)[0])
    measure = action if family.rotation else 3 * multiple * action
    row = [family.level_weight * action] + [family.level_weight * measure] * (family.width - 1)
    walls = (
        row * family.records
    )  # one wall per line of every row, the rows of a holder of the sign alike
    factors = {
        other: 1 if family.rotation else int(division_forward(multiple, families[other].pair[1], 0)[0])
        for other in sources
    }
    return HeldWrite(tuple(walls), factors)


def largest_of(width: int) -> int:
    """The largest integer of the file's width in bits, 2^width - 1, the bound every total of the law stays inside (ALGEBRA.md #the-bound)."""
    return int(2**width - 1)


def booking_room(families: tuple[FamilyRule, ...], index: int, wronskian: bool) -> int:
    """The room of one source's booking at the amplitude A, its size over A^2: the Wronskian's two products per plane of the part (three planes thrice), or the form's two per line of its record (now^2 and next x before); where the source's record is turned (`turns`) the booking is read from the step's levels before the turn, each within twice A once A is read as A + 2 (features/rotation, `TURNED_REACH`, `TURNED_SLACK`; `amplitude_bound`): the Wronskian's two products of a turned level and a level, the form's now^2 and the two turned levels' product per line."""
    reach = TURNED_REACH if turns(families, index) else 1
    if wronskian:
        return (
            PRODUCTS * reach * (families[index].planes or 1)
        )  # every plane of the part its two products
    return families[index].record * (1 + reach * reach if reach > 1 else PRODUCTS)


def hill_scale(pair: tuple[int, int], gamma: int) -> int:
    """The write's factor's room at a source's hill's edge (ALGEBRA.md, The write per proper volume and per proper interval; The guard): P the edge's pace of the source's pair, the largest the guard admits (`features/read`, `edge_of`), where the factor N^k p_x p_y p_z / p_0^3, one rounding of the count times the three paces over the one wall (`paces.write_factor`, the product exact beyond the width), is at most (P / Gamma)^3 (1 at most in a hollow, every pace at or below Gamma): P^3 div Gamma^3 rounded up, which multiplies the booking's room in the write's numerator, the one place the factor meets the width."""
    edge = edge_of(pair, gamma)
    cube = gamma * gamma * gamma
    return int(division_forward(edge * edge * edge, cube, cube - 1)[0])


def factor_bound(families: tuple[FamilyRule, ...], index: int, gamma: int, bound: int) -> int:
    """The largest Link factor q_max the axis lines within the level `bound` admit on a Link of the family `index`'s record (ALGEBRA.md, The write per proper volume and per proper interval): the Link's factor is q = Gamma - t (`paces.axis_pace`), t the Link's tension, SUM over the held rows with axis lines the family reads of W_a times the mean of the row's axis line at the Link's two ends (`read.link_tension`), each end within the bound, so q_max = Gamma + SUM W_a x bound over those rows (the mathematician's 268 with the advisor's precision, #1572 comments 5969128707 and 5969197876: Gamma + W A on the one axis line a Link carries today, the sum where more than one held row's axis lines are read on a Link); Gamma where the family reads no axis line, the odd lines of a holder under the rotation entering no Link's factor (`node.read_lines`)."""
    weights = sum(
        abs(read.weight)
        for read in families[index].reads
        if families[read.family].axes and not families[read.family].rotation
    )
    return gamma + weights * bound


def tension_room(pair: tuple[int, int], gamma: int, q_max: int, wronskian: bool) -> int:
    """The write's factor's room at a source's hill's edge under a negative tension (ALGEBRA.md, The write per proper volume and per proper interval; the mathematician's 268 and the advisor's second, #1572 comments 5969128707 and 5969197876, two hands): the guard bounds p_i^2 Q_ij and not the Link's factor q itself, so under a negative tension q exceeds Gamma, up to q_max, the largest Link factor the axis lines within the bound admit (`factor_bound`), and in a hollow the factor reaches (P / Gamma)^3 sqrt(q_max / P) on a count and (P / Gamma)^3 q_max / P on a Wronskian, P the edge's pace of the source's pair (`edge_of`), beyond the hill's room (`hill_scale`); the room is the ceiling of P^2 (isqrt(q_max P) + 1) / Gamma^3 on a count and of P^2 q_max / Gamma^3 on a Wronskian, the ceiling by the division act with the carry Gamma^3 - 1 and the root by its fixed point plus one, so that the floor never under-bounds (at the rule's universe, Gamma 6,000 and q_max 15,266: 3 and 4 on matter's pair against the hill's 2, 2 and 3 on the massless pairs against 1)."""
    edge = edge_of(pair, gamma)
    cube = gamma * gamma * gamma
    factor = q_max if wronskian else division_fixed_point(q_max * edge) + 1
    return int(division_forward(edge * edge * factor, cube, cube - 1)[0])


def source_room(
    families: tuple[FamilyRule, ...], index: int, gamma: int, wronskian: bool, hill: int | None
) -> int:
    """The room of the write's factor of the source `index` in a row's write (ALGEBRA.md, The write per proper volume and per proper interval): the hill's room alone (`hill_scale`) where `hill` is None, the first pass of `amplitude_bound`, which finds the hill's own bound A_1; else the larger of the hill's room and the tension's room at the largest Link factor the axis lines within A_1 = `hill` admit (`tension_room`, `factor_bound`), one pass and no fixed point, since the bound found is at most A_1 and q_max(A_1) bounds q_max(A)."""
    room = hill_scale(families[index].pair, gamma)
    if hill is None:
        return room
    q_max = factor_bound(families, index, gamma, hill)
    return max(room, tension_room(families[index].pair, gamma, q_max, wronskian))


def write_rooms(
    families: tuple[FamilyRule, ...], index: int, write: HeldWrite, gamma: int, hill: int | None
) -> list[int]:
    """The room of a held family's one write per part at the amplitude A, the numerator's size over A^2 at the largest level, each part's times the size of the row's write weight: for the time part SUM over the sourcing families of w x the room of the booking the row takes, the form or the Wronskian (`booking_room`), times the write's factor's room at the source's hill's edge (`source_room`: the hill's, `hill_scale`, 1 in a hollow under tensions at or above 0, where `hill` is None, and the larger of it and the tension's room at the hill's own bound `hill`, `tension_room`, where it is given); for each axis part SUM over the sources of w x factor x lines x 2 |num| for a tension line (the tension's part per line of the source's record, two products of two levels, |num| on each) and w x factor x lines x 2 x 2 for an odd line (the sign's current across the axis's two Ports, two products each: the room of the two Links' currents, within which their mean, the source, stays)."""
    family = families[index]
    sources = readers_of(families, index)
    time = sum(
        abs(weight_of(index, families[other]))
        * booking_room(families, other, family.wronskian)
        * source_room(families, other, gamma, family.wronskian, hill)
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
    return [abs(family.write) * room for room in ([time] + [axis] * (family.width - 1)) * family.records]


def amplitude_bound(
    families: tuple[FamilyRule, ...], gamma: int, action: int, width: int, unit: int = 1
) -> int:
    """The amplitude bound A, derived and never written: the largest level at which Rule3's total 6 A R + A |S| + w (A + 1) stays inside the file's width for every pair at the vacuum's paces, at a frozen clock (the paces 0, the bound the deepest hollow approaches: |S| grows to 12 den Gamma^2 G^2 as the paces fall) and at the hill's edge P on the clock and the pace alike (`features/read`, `edge_of`; the three the extremes of the guard, ALGEBRA.md #the-bound, #the-paces, The guard; for a turned record the six arrivals within twice A, `TURNED_REACH`, and the three shears' largest product, 2 n w x1 at the tangent half-angle 1 on a Link with x1 within twice A and one, features/rotation), at which the currents' reading at a Node, 6 x 2 x lines x |num| A^2 for every family of quanta (the two products of each of the record's lines through the six Ports; the largest A whose square fits, the fixed point of the division act), does too (features/currents), at which every held family's one write per part, its numerator at the sources' room with the write's factor at the hill's edge (`write_rooms`: the booking's room times the factor's room at the source's hill's edge, `hill_scale`, the one rounding's value; its numerator, the count times the three paces, is exact in Python's integers and meets no width, `paces.write_factor`) plus its remainder under the wall, does too, in two passes: the first with every source's room the hill's (`hill_scale`) finds the hill's own bound A_1, the second with every source's room the larger of the hill's and the tension's at q_max = Gamma + SUM W_a A_1, the largest Link factor the axis lines within A_1 admit (`source_room`, `tension_room`, `factor_bound`; `bound_under_rooms`, the one pass), the bound at most A_1 and no fixed point, since q_max(A_1) bounds q_max(A) (the mathematician's 268 and the advisor's second, two hands; the four shipped universes' bound 9,266 unmoved, the write's total not their binding term); refused by name where no level fits. Where a holder turns a record (features/rotation) every room of the universe is read at the level A + 2 and the level found is 2 less (`TURNED_SLACK`: a turned level stays below 2^(1 / 2) A + 3, within twice A + 2, and not within twice A, the audit's witness (-1, -1) turning to (-3, -1) at A = 1), the turned record's total 6 R x twice the level + |S| A + w x twice the level + w (its six arrivals and the level before it is stepped against both turned, `TURNED_REACH`), the three shears' largest product 2 n w x1 at the tangent half-angle 1 on a Link with x1 within twice the level and one, and its bookings' products of turned levels (`booking_room`)."""
    hill = bound_under_rooms(families, gamma, action, width, unit, None)
    return bound_under_rooms(families, gamma, action, width, unit, hill)


def bound_under_rooms(
    families: tuple[FamilyRule, ...], gamma: int, action: int, width: int, unit: int, hill: int | None
) -> int:
    """One pass of `amplitude_bound`: the largest level inside the width under Rule3's totals, the currents' reading and every held family's one write per part, its rooms read by `write_rooms` at `hill`, None every source's room the hill's (the first pass, whose level is the hill's own bound A_1) and A_1 the larger of the hill's and the tension's room per source (the second pass, the bound); refused by name where no level fits."""
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
            rooms = write_rooms(families, index, write, gamma, hill)
            for wall, room in zip(write.walls, rooms, strict=True):
                if wall > largest:
                    found = 0
                elif room:
                    fits = int(division_forward(largest - wall, room, 0)[0])
                    found = min(found, division_fixed_point(fits) - slack)
        if found < 1:
            raise ValueError(
                f"the pair [{num}, {den}] at the Node clock Gamma = {gamma} and T = {action}: the totals of "
                f"Rule3, of the currents and of the write leave no level inside the width of {width} bits "
                "(ALGEBRA.md #the-bound)"
            )
    return found
