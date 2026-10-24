"""The families from the rule (ALGEBRA.md #a-familys-declaration, every family has a dimension; the owner's word of 2026-10-24, no declarations): a family's row holds its name, its pair and, for a family of quanta, its dimension (any integer from 1, the lines of its record, one real line, a plane of two, or three or more real lines, each stepped as a line of dimension one); a row without a dimension is a holder, and the rule derives the rest from the pair and the dimension alone with no name and no default: what a holder holds and what sources it (a held row with a gap holds the volume, sourced by the form and the tensions; a held massless row holds the sign, sourced by the Wronskian; `loader/universe.holder_of`), the level weight 1 and the write weight 1 (the write's and the read's universality), who reads whom at the weight 1 (`with_reads`: every family of quanta and every holder of the volume reads every holder of the volume, a plane every holder of the sign too, the holder of the sign none), the lines, who sources whom by the held write's reciprocity, the one write per held part with its walls; the amplitude bound A is derived from the integer width by the search on the share reading (`rule3.largest_below`), never written and never by a root (ALGEBRA.md #the-bound). The declared reads, sources, level weights, write weights and rests of the files to 2026-10-24 (the keys `reads` and `held`) kept by name."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from math import gcd

from event_universe.core.paces import WRONSKIAN_POWER, sine_den
from event_universe.core.ports import AXES, PORTS, SIDES
from event_universe.core.rule3 import coefficients, division_forward, largest_below, mass, partial_rooms
from event_universe.features.currents import PRODUCTS
from event_universe.features.read import edge_of

PLANE = 2  # the lines of a plane, re and im: the one shape with a Wronskian and a turn (charged matter)
FOLD_REACH = 2  # a folded arrival's part within twice the level: |X^c re_j - X^s im_j| <= X (|re_j| + |im_j|) at the fold's tangent at most 1 (the guard at load, plane.fold_guard; the sign's pair, whose magnitude is X to the rounding, read at its own extreme, `turned_room`), the integer total per part and no modulus


@dataclass(frozen=True)
class Row:
    """A family's row as the loader derives it from the universe file (the owner's word of 2026-10-24, no declarations): its name, its pair [num, den], its lines in all (a family of quanta's dimension, any integer from 1, times its parts; a holder's time line with its three axis lines, the tension lines of the holder of the volume or the odd lines of the holder of the sign), its parts (the records of one event never summed at a Node, 2 for the pair family, 1 otherwise), whether its lines are planes (the dimension 2, re and im: charged matter, the one dimension with a Wronskian and a turn; every other dimension real lines, which read none of the sign), whether it is sourced by its readers' Wronskian (the holder of the sign, the held massless row; else by their form and their tensions, the holder of the volume, the held row with a gap), whether it acts on its readers by the rotation of the two-part record (the holder of the sign; else by the plain read into their paces), its level weight where it is held (1, the quanta of form that write one level of the row), its write weight where it is held (1, the signed multiplier of its one write per line; the sign holder's alpha set by the loader, `alpha_of`), its rest (0: no row rests at a level) and the holders it reads by name, each at the weight 1 (`holders`, `with_reads`; empty where it reads none). The files' keys `reads` and `held` with `sources`, `level_weight`, `write_weight` and `rest` to 2026-10-24 kept by name."""

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
    holders: tuple[tuple[str, int], ...]
    records: int = 1  # a charged family's laid records, each owning one row of the sign; a holder of the sign's rows, 1 + the world's charged records; 1 otherwise (ALGEBRA.md, No record reads its own write of the sign)
    flux: bool = False  # a holder of the content sourced by the count's flux too: three odd lines after its tension lines, V_a at the Node, the Link's V_ij = V_a(i) + V_a(j) read with the direction's sign (ALGEBRA.md, The clock family on the Ports)
    motion_volume: bool = False  # the row carries its time line as the volume's level X = Gamma (Gamma / p_0)^(d + 1) (features/volume; the momentum hand's derivation M12a read cold by the reader, 2026-10-22): set by the loader from the volume form (every board's interval unobservable) alone on the held row of the content sourced by the tensions, massless or gapped (`axes`), that is not the sign's holder (loader/interval.volume_rows; the clause of 2026-10-23), no key of the row; Rule3's own line steps X with the one write (d + 1) X c over Gamma E_s T and no hill, the level a reading of the record (the paces, the readings)
    write_wall: int = 1  # the sign holder's wall multiplier Gamma under the charge's universality (2026-10-24; Gamma den under the law of one Node of 2026-10-23, kept by name): alpha carried inside the one write, the numerator times E_h T (`write_weight` set by the loader, `alpha_of`) and every wall of the row times Gamma (`held_write_of`; the charge multiple of the count units, 2026-10-24 to the same day, kept by name as the defect), the remainder keeping the fraction; 1 on every holder of the content, whose write weight is the file's
    fill: int = 0  # the time line's value beyond a face and on a grown layer, the Link to the fill (core/ports.arrival): the row's rest, or under the volume form the rest's volume X(rest), the rest beyond the face fixing the clock's unit (ALGEBRA.md, The board's interval is no observable; loader/interval.volume_rows, features/volume.fill_of); 0 for a row with no rest


@dataclass(frozen=True)
class Read:
    """One read of a family as the rule derives it (`with_reads`): the held family whose time line it reads and the weight it reads with, 1, by the plain read into its paces (a holder of the volume) or as the turn of its record (a holder of the sign); by the held write's reciprocity the weight it sources that holder with."""

    family: int
    weight: int


@dataclass(frozen=True)
class FamilyRule(Row):
    """A family as the rule resolves it from its row (`Row`) with its reads by position: the held rows whose time line it reads, each at the weight 1 (`with_reads`), which by the held write's reciprocity it sources at the same weight; its rest 0 (the vacuum content of the massless row holding the content, the files' key `rest` to 2026-10-24, kept by name: no row rests at a level)."""

    reads: tuple[Read, ...] = ()

    @property
    def held(self) -> bool:
        """Whether the family is held: a row with a level weight, written by the held write and read by others."""
        return self.level_weight is not None

    @property
    def write(self) -> int:
        """The held row's write weight, the signed multiplier of its one write per line (the files' key `write_weight`, read as the row's level weight is); a family that holds nothing has no write."""
        assert self.write_weight is not None, f"{self.name!r} holds nothing and has no write"
        return self.write_weight

    @property
    def quanta(self) -> bool:
        """Whether the family carries quanta, stepping at the paces of its reads with its share its count and its currents a node_detector's reading: every family of quanta and the holder of the sign, whose free row 0 is the light's record (light its own family, 2026-10-19: a click names a holder no family reads, `node_detector_declaration.lit_families`); a held row sourced by the form holds the content and steps at the pace 1."""
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
        """The lines of one part the laid pair goes to, one per real line and one per plane (its first line, the second line its sense): the count of a body's or a packet's `weights` (`keys.weights_of`, `Lattice.lay`)."""
        return self.planes if self.plane else self.width

    @property
    def several(self) -> bool:
        """Whether the record's lines are reported line by line in the parts line (`reports.parts`, `Lattice.report`): a record of several parts (the pair family, the GHZ family, the nuclide's two planes) or of several real lines (a record of dimension 3), each line's signed level sums over a region; a plane's two lines, re and im, are one line and its sense, and one real line is one line, neither reported; a held row's record is its time line alone (`record`), its axis lines held parts and no lines of the record, so the holder of the sign under the rotation, 1 + 3 lines per row, reports no parts line (the one Node, 2026-10-23: every sign holder rotates, and the two slits' output carries the clicks it carried)."""
        return self.parts > 1 or (self.width > 1 and not self.plane and not self.held)

    @property
    def power(self) -> int:
        """The proper-interval powers of the held row's one write on its sources' booking (ALGEBRA.md, The write per proper volume and per proper interval): two on a count's form, N^2 / (h_x h_y h_z) = p_x p_y p_z / (p_0 Gamma^2), the law's booking, and one on the Wronskian, which carries one N of its own, N / (h_x h_y h_z) = p_x p_y p_z / (p_0^2 Gamma), and on a count's form under the row's key the form's own clock, the form carrying one N of its own as the Wronskian does (The form's own clock, a hypothesis under its own name, 2026-10-22; `form_clock`) (`paces.COUNT_POWER`, `paces.WRONSKIAN_POWER`); the one place the booking's power is chosen, read by the write (records.write_sources), the start's rest (features/start/rests.py) and the width's gate (loader/rooms.py)."""
        return WRONSKIAN_POWER  # one power on every booking: the Wronskian's one N, the form's own clock

    def exponent(self, power: int | None = None) -> int:
        """The pair's dimming exponent in the board's interval under a held row's booking power, its own where none is given (ALGEBRA.md, The band at a pace; The write per proper volume and per proper interval; The mean's velocity is the content's, 2026-10-22): a count's write dims as N^(2 + power) / h^3 times the form's own sine, whose limit at a small gap is one N for a pair with a gap at rest and two for the massless pair, so the integer is 3 + power + 1 for a pair with a gap and 3 + power + 2 for the massless pair, 5 and 6 under the form's own clock (the form's own clock, the power 1) and 6 and 7 under the law's booking (the power 2), the pairs' integers the readings' mix takes (`exponent_of`; board_readings.eras)."""
        return exponent_of(self.pair[0] == self.pair[1], self.power if power is None else power)

    @property
    def axes(self) -> bool:
        """Whether the row carries three axis lines beside its time line: a held row sourced by the tensions (the massless row holding the content, read into the Link's paces), or the holder of the sign under the rotation (the odd lines, the phase on the Link), every row of it alike."""
        return self.held and self.width > 1

    @property
    def record(self) -> int:
        """The lines of the family's record of quanta, the ones its share, its currents, its form and its Wronskian are read from: every line of a family of quanta; the time line alone of a held row (the holder of the sign's own record, the light's on its free row 0; light its own family, 2026-10-19), its axis lines being held parts."""
        return 1 if self.held else self.lines

    @property
    def link_read(self) -> tuple[int, int]:
        """How a Link reads an odd line of this holder, two declared integers the Port consumes blindly (`plane.link_levels`): the weight of the Node owning the +a Link and the weight of its far end; (-1, -1) the two ends' sum with the sign opposite to the time line's (since 2026-10-21, the law's row (b2) read on the engine: the Link's hop carries the odd line as Peierls' p - q A under the hop's convention omega(k + theta), beside the time line's + q phi on the step, so that the strength the record is turned by is -d_a L_0 - d_t L_a, Maxwell's induction with its sign, and a co-moving reader of the source's family reads gamma_s (1 - beta_s^2) = 1 / gamma_s, 0.987, 0.958 and 0.919 at beta_s = 0.150, 0.286 and 0.395 against the law's 0.989, 0.958 and 0.919 (ALGEBRA.md, The sign holder rotates the two-part record; The rows against nature (b2)); (-2, 0) under the Lorentz form, where the odd line is the +a Link's own level, sourced by the Link's own flux, and the Link reads minus twice it from its owner alone, the same magnitude for a smooth line as the two ends' sum, the Link's own line where it varies (covector.py). History: (1, 1), the two ends' sum with the time line's own sign, the shipped read until 2026-10-21 (gravity's dragging sign, +theta along the current, The clock family on the Ports), under which the same co-moving reader read gamma_s (1 + beta_s^2), 1.031, 1.130 and 1.254 at the three beta_s, since the odd line is sourced at + v / c_s^2 of the time line (The odd line's source is the sign's own current)."""
        return (-1, -1)


def exponent_of(massless: bool, power: int) -> int:
    """A pair's dimming exponent in the board's interval at a booking's proper-interval power (`FamilyRule.exponent`): 3 for the proper volume's three rulers, the booking's power on the clock, and the form's own sine's limit at a small gap, one for a pair with a gap at rest and two for the massless pair (ALGEBRA.md, The band at a pace)."""
    return 3 + power + (2 if massless else 1)


def turns(families: tuple[FamilyRule, ...], index: int) -> bool:
    """Whether a family's record is turned: a plane that reads a holder declaring the rotation (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record); a one-part family reads no holder of the sign and is untouched, as is a plane in a universe whose holders act on the pace."""
    family = families[index]
    return family.plane and any(families[read.family].rotation for read in family.reads)


def folds(families: tuple[FamilyRule, ...], index: int) -> bool:
    """Whether a family's record is folded: a plane that reads a holder carrying the flux's odd lines, each Link's read then a pair (X^c, X^s) in the Link unit (ALGEBRA.md, The clock family on the Ports; plane.py); a record of real lines, light among them, reads the odd lines into no pace and is untouched."""
    return families[index].plane and any(families[r.family].flux for r in families[index].reads)


def charged(families: tuple[FamilyRule, ...], index: int) -> bool:
    """Whether a family reads a holder of the sign, plainly or by the turn: every record of such a family, a plane (`with_reads` gives no family of real lines one), owns one row of the sign at every Node (ALGEBRA.md, No record reads its own write of the sign)."""
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


def children_of(families: tuple[FamilyRule, ...], index: int) -> int:
    """The records a charged family needs for its births: the largest count of its children in any list a meeting selects (`conversion.birth_of` over every gapless parent, the exact lists; 2 at every list of the one universe, (k, -1), (k, 1)), 0 where no list births it (ALGEBRA.md, Matter's birth from light, the clause of 2026-10-24: N records of the write step, one per child of the list, each at its own sense; the owner's word, several can be born). Nothing here counts two: the list's own length."""
    from event_universe.conversion import (
        birth_of,  # conversion reads this module: imported here
    )

    return max(
        (
            sum(1 for out, _sense in table if out == index)
            for parent in range(len(families))
            if families[parent].quanta and families[parent].pair[0] == families[parent].pair[1]
            for table in birth_of(families, parent)
        ),
        default=0,
    )


def with_records(families: tuple[FamilyRule, ...], laid: Sequence[int]) -> tuple[FamilyRule, ...]:
    """The families with the world's records: a charged family's records are its bodies (`laid`, per family its bodies in the world's order, 0 since no file declares one) or the children a meeting's list births of it (`children_of`; ALGEBRA.md, Matter's birth from light, the clause of 2026-10-24: N records of the write step, one per child of the list, each at its own sense, so that each born child carries its Wronskian and sources its own row, where one record carrying both children of a pair read W = 0 and sourced nothing, the defect found on 1b670aaf2), one at least, each its own lines and its own row of the sign; every holder of the sign carries one row per charged record beside the row no record owns, its lines that many times its row's lines (the time line, with its three odd lines under the rotation); every other family as the universe declares it."""
    rows = 1 + sum(
        max(1, laid[index], children_of(families, index))
        for index in range(len(families))
        if charged(families, index)
    )
    found = []
    for index, family in enumerate(families):
        if charged(families, index):
            records = max(
                1, laid[index], children_of(families, index)
            )  # one per child of the list (2026-10-24)
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
    """The records that source one row of a held family, (reader, record) pairs (ALGEBRA.md #the-primitives, the held write's reciprocity; No record reads its own write of the sign): every record of every reader for a holder of the content, whose one row is the sum of its readers' forms; for a holder of the sign the one record that owns the row, and none for the row 0, which no record writes."""
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
    """A held family's one write per line as the rule derives it from the rows (ALGEBRA.md #the-primitives, a family's write is one act): the walls, one per line, the time line's E_s T and each axis line's E_s times one measure of a current of the families that source it: the quantum's W_c = 3 den T for a tension line (one den among the sources; with several, the least common multiple of their den in den's place) and the time line's own T for an odd line, the same wall as the time level's W, so that the odd level over the time level is (J_a / 2) / W = 3 (den_s / num_s) v = v / c_s^2 as the law's (b2) computes it (ALGEBRA.md #the-rows-against-nature (b2); the two hands: over den T the engine's magnetic sector was 1 / den of the law's and the odd levels of the files' bodies rounded to 0), and per sourcing family the factor with which its tension enters the axis parts' numerator, the multiple over its own den (1 where one den serves every source, and 1 for every source of an odd line, whose wall carries no den), so that the sum of the sources' fractions is one fraction over one wall, exact."""

    walls: tuple[int, ...]
    factors: dict[int, int]


def with_reads(rows: Sequence[Row]) -> list[Row]:
    """Every row's reads derived from the rows (the owner's word of 2026-10-24, no declarations; ALGEBRA.md #the-paces, The reads are derived): every family of quanta and every holder of the volume reads every holder of the volume (the held rows with a gap) at the weight 1, a holder of the volume its own level among them (Every row reads the content); every plane family (the dimension 2) reads every holder of the sign (the held massless rows) at 1 too, as the turn of its two lines, and writes it by its Wronskian; a family of real lines, one or three, reads none of the sign, neutral by itself; the holder of the sign reads none, its rows a phase on its readers' Links, entering no pace and no clock (the one world's file as the owner wrote it). The declared reads (the key `reads`, a family naming the holders it reads at the weights it names, 2026-10-02 to 2026-10-24) kept by name."""
    volume = tuple((row.name, 1) for row in rows if row.level_weight is not None and not row.wronskian)
    sign = tuple((row.name, 1) for row in rows if row.wronskian)
    found = []
    for row in rows:
        reads: tuple[tuple[str, int], ...] = ()
        if row.level_weight is None:
            reads = volume + (sign if row.plane else ())
        elif not row.wronskian:
            reads = volume
        found.append(replace(row, holders=reads))
    return found


def family_rules(rows: Sequence[Row]) -> tuple[FamilyRule, ...]:
    """Every family from its row with its reads resolved by name to the held rows' positions (`with_reads`, each at the weight 1; ALGEBRA.md #a-familys-declaration), then the world's records (`with_records`), one record per charged family."""
    names = [row.name for row in rows]
    found = tuple(
        FamilyRule(
            **vars(row), reads=tuple(Read(names.index(name), weight) for name, weight in row.holders)
        )
        for row in rows
    )
    return with_records(found, [0] * len(found))


def alpha_of(families: tuple[FamilyRule, ...], index: int, gamma: int, action: int) -> tuple[int, int]:
    """The law's alpha of a holder of the sign carried inside its one write (the owner's word of 2026-10-24, nature's charge universality, "nature is the main thing"; ALGEBRA.md, The constants: the law's alpha is the ratio of the file's E_h T to Gamma, one per holder with any pairs under it; the old kept by name: "the ratio of the file's E_h T num to Gamma den, [num, den] the pair the moving planes reading the holder share, two moving planes of different num / den asking one holder for two alphas refused by name: one holder, one alpha", the law of one Node, 2026-10-23): the pair (E_h T, Gamma) reduced by their greatest common divisor, the numerator's multiplier and the walls' multiplier of every line of the holder's rows; no reader's pair enters it, the charge the Wronskian over T div 2 for every reader at the write (`held_write_of`, The constants, the sentence of 2026-10-24; the charge factors of that morning, 3 T den over each count unit, kept by name as the defect); (1, 1) where no plane of quanta reads the holder (light's own row on the gate worlds), the write of no source."""
    holder = families[index]
    assert holder.level_weight is not None
    if not any(family.plane and weight_of(index, family) > 0 for family in families):
        return 1, 1
    from event_universe.loader.charge import (
        pythagorean_readers,  # charge reads this module: imported here
    )

    pythagorean_readers(families, index)
    above, below = holder.level_weight * action, gamma
    common = gcd(above, below)
    return int(division_forward(above, common, 0)[0]), int(division_forward(below, common, 0)[0])


def shared_clock(families: tuple[FamilyRule, ...]) -> None:
    """The loader's gate of the carried factor, the carried factor (ALGEBRA.md, The write per proper volume and per proper interval, the clause of 2026-10-22; loader/universe.factor_of): the sources of a row carrying its factor share the row's one wall per Node, E_s T times the factor's wall at the Node's clock, where they read the content alike, the same holders at the same weights (`FamilyRule.reads`; the clock from the content a family reads, node.rulers), so that the one remainder per held line carries every source's fraction and no second carried integer stands (the reader's form; the two-stage form, one remainder per source, named and not built); a row whose sources read the content at differing weights is refused by name with the readers and their reads, the rounded factor standing on every row; the reads compared are the reads of holders of the content alone, since the holder of the sign acts by the rotation, a phase on the Links, and enters no pace and no clock (the law of one Node, 2026-10-22: the hydrogen universes' proton and electron read the sign holder at 1 and 3 and no content, one clock, the vacuum's)."""
    for index, family in enumerate(families):
        readers = readers_of(families, index)
        reads = {
            tuple(
                sorted(
                    (r.family, r.weight)
                    for r in families[other].reads
                    if not families[r.family].wronskian
                )
            )
            for other in readers
        }  # the reads of the content alone: the holder of the sign turns its readers and enters no pace
        if len(reads) > 1 and not any(not families[r.family].rotation for r in family.reads):
            raise ValueError(
                f"{family.name!r} reads no content and its sources read the content at differing weights, "
                f"{[(families[o].name, families[o].holders) for o in readers]}: a held row's write is scaled at "
                "the row's own paces where the row reads the content (ALGEBRA.md, The one Node, the clause of "
                "2026-10-23), and a row that reads none, a holder of the sign, writes its sources per the Node's "
                "proper volume as the content gives it, one wall per line at its sources' shared paces (The write "
                "per proper volume and per proper interval, the clause of 2026-10-22); let the row read the "
                "content, or let its sources read alike"
            )


def weight_of(held: int, reader: FamilyRule) -> int:
    """The weight with which a family reads a held family, and so sources it: one for every reader (the owner's word of 2026-10-24, 'like nature', the read's universality beside the write's; ALGEBRA.md, The constants), 0 where it does not read it; the declared weights (ALGEBRA.md #the-primitives, a family's write: whoever reads with w sources with w, the former rule) kept by name, every read derived at the weight 1 (`with_reads`)."""
    return 1 if any(read.family == held for read in reader.reads) else 0


def readers_of(families: tuple[FamilyRule, ...], held: int) -> list[int]:
    """The families of quanta that read the held family `held`, and so source it, in the file's order (ALGEBRA.md #the-primitives, A family's write is one act: the writer's quantity is a family of quanta's form, Wronskian or tension); a held row of the content reads the content as every family does since Every row reads the content, its own level among it, and sources nothing by the write."""
    return [other for other, family in enumerate(families) if weight_of(held, family) and family.quanta]


def count_wall(family: FamilyRule, action: int) -> int:
    """The wall of one quantum of the family, the unit in which its share is read as quanta (ALGEBRA.md #the-count-is-the-records-share; the two hands' word of 2026-10-03 on R8, #1793, the Boss's 5972724842: a count is one quantum of the invariant, the form T sin omega_0 of the family's gap): (the largest x with x^2 <= 9 T^2 (den^2 - num^2)) for a family with a gap, W_c sin omega_0 to the unit by one search on the whole product (`paces.sine_den`, the engine's one integer sine, `rule3.largest_below`), the share per quantum of a record standing at its rest; 3 den T, the bolometer's W_c, for a massless family, whose quantum is read at its wave's own frequency by the books (`credit.record_unit`) and whose inflow a region reads in units of T."""
    num, den = family.pair
    if abs(num) == den:
        return 3 * den * action
    # Rule3's 3 den over the den of sin omega_0: one search on the whole product
    return sine_den(num, den, 3 * action)


def held_write_of(families: tuple[FamilyRule, ...], index: int, action: int, unit: int = 1) -> HeldWrite:
    """The one write per line of the held family `index` (`HeldWrite`): its walls from the row's level weight, the quantum action and, for the tension lines, the den of the families that source them (its readers, whose tension it takes), the multiple of their den by the division act on the greatest common divisor, the measure of a current on each axis line (W_c's 3 den T for the tensions; the time line's T for the odd lines, the same wall as the time level's), and each source's factor, the multiple over its den for a tension line and 1 for the sign's odd line; the odd lines of either holder at twice their measure's wall, the two Links' currents summed unhalved over the doubled wall (the two hands' lines of 2026-10-09, the mathematician's (L2) and the advisor's (c)): the sign holder's time line at 2 E_s T as well, the Wronskian centred on the triple, W(now, before) + W(next, now) summed unhalved (bookings.booked_of; the owner's decision of 2026-10-23, the centred count), and its three odd lines at 2 E_s T, the Node's two a-Links' Wronskian currents summed (`readings.sense_current_of`, unhalved), and a flux holder's three odd lines at 2 E_s W_c, the count's flux through the axis's two Links summed unhalved over twice the count's wall (the joint line, the T of their "2 E_s T W_c" read as W_c's own: the flux F is in the share's units, one quantum W_c, as the form D over E_s T is one quantum T, so that a rigidly moving source's static solution is V = U v, ALGEBRA.md, The clock family on the Ports), the same factor per source as the tensions'; and a holder's three shear lines, where it declares the shear, at the same doubled wall 2 E_s W_c, the Node's product of its two axis differences D_a D_b being the two ends' halves of the Link's off-diagonal booking -num G_ab (ALGEBRA.md, The tension: G_ab(i) the stress booking on the b-Link, -2 b^2 sin k_a sin k_b on a plane record, met in the mean by -(D_a D_b) / 2 at each end as G_aa is met by h_a at each end exactly), the same factor per source as the tensions'. Under the Lorentz form (`Row.lorentz`, the key `form`: `lorentz`) the sign holder's odd line a is sourced by the +a Link's own flux of the record's step in the Link unit, Phi_a(i) = Im(conj(z_i) (X^c + i X^s) z_(i+a)) with (X^c, X^s) the Link's pair the step reads, X = 2 num_s Q_ij (`covector.link_fluxes`), over the wall 2 den_s G^2 E_s T, `unit` the run's Link unit G and den_s the source's den (the multiple of the sources' den where they differ, each source's factor the multiple over its own den, as the tensions'), so that the odd level over the time level is Phi / (2 den_s G^2 W) = (num_s / den_s) (g / W) = v / c^2 at light's c^2 = 1 / 3, the pairing at the holder's own light speed under which the massless line propagates the lattice Lorenz constraint exactly (covector.py; the pairing at c_s of ALGEBRA.md, The odd line's source is the sign's own current, is this times den_s / num_s, 1 - 2 x 10^-28 in nature)."""
    family = families[index]
    assert family.level_weight is not None
    sources, multiple = readers_of(families, index), 1
    for other in sources:
        den = families[other].pair[1]
        multiple = int(division_forward(multiple * den, gcd(multiple, den), 0)[0])
    measure = action if family.rotation else 3 * multiple * action
    doubled = SIDES if family.wronskian else 1
    row = [doubled * family.level_weight * action] + [family.level_weight * measure] * (family.width - 1)
    if family.axes:  # the tension lines: the centred difference squared over the doubled wall 2 E_s W_c (The stress is the Links', 2026-10-23)
        row[1 : 1 + AXES] = [SIDES * family.level_weight * measure] * AXES
    if family.flux:  # the odd lines: the two Links' flux summed unhalved over twice the count's wall
        row[1 + AXES :] = [SIDES * family.level_weight * measure] * AXES
    if family.rotation:  # the sign's odd lines: the two Links' currents summed unhalved over 2 E_s T
        row[1:] = [SIDES * family.level_weight * measure] * AXES
    row = [
        wall * family.write_wall for wall in row
    ]  # the sign holder's Gamma (alpha inside the write); the charge the Wronskian over T div 2 for every reader, no count unit in any wall (The constants, 2026-10-24)
    walls = (
        row * family.records
    )  # one wall per line of every row, the rows of a holder of the sign alike
    factors = {
        other: 1 if family.rotation else int(division_forward(multiple, families[other].pair[1], 0)[0])
        for other in sources
    }  # the sign's sources at 1, the Wronskian whole (the holder of the sign rotates)
    return HeldWrite(tuple(walls), factors)


def largest_of(width: int) -> int:
    """The largest integer of the file's width in bits, 2^width - 1, the bound every total of the law stays inside (ALGEBRA.md #the-bound)."""
    return int(2**width - 1)


def amplitude_bound(
    families: tuple[FamilyRule, ...], gamma: int, action: int, width: int, unit: int = 1
) -> int:
    """The amplitude bound A, the engine's and no line of the law, derived and never written: the largest level at which every partial sum of Rule3's flux line in the step's order, 3 w A, D A, A (|2 w - D| + w), the Links' sum 2 A SUM |R_ij| (a turned plane's (1 + 2^(1 / 2)) A SUM |R_ij|, a folded one's 3 A SUM |R_ij|) and the total A (SUM |R_ij| + |S| + w) + w - 1 (`rule3.partial_rooms`), stays inside the file's width for every pair at the vacuum's paces, at a frozen clock (the paces 0, the bound the deepest hollow approaches: |S| grows to 12 den Gamma^2 G^2 as the paces fall) and at the hill's edge P on the clock and the pace alike (`features/read`, `edge_of`; the three the extremes of the guard, ALGEBRA.md #the-bound, #the-paces, The guard; for a turned record the six arrivals each under the sign's pair with the Link's phase at its own extreme, X 2^(1/2) to the rounding, `turned_room`, and for a folded one within twice the level, `FOLD_REACH`), at which the currents' reading at a Node, 6 x 2 x lines x |num| A^2 for every family of quanta (the two products of each of the record's lines through the six Ports; the largest A whose square fits, `rule3.largest_below`), does too (features/currents), at which every held family's one write per part, its numerator at the sources' room with the write's factor at the hill's edge (`write_rooms`: the booking's room times the factor's room at the source's hill's edge, `hill_scale`, the one rounding's value; its numerator, the count times the three paces, is exact in Python's integers and meets no width, `paces.write_factor`) plus its remainder under the wall, does too, in two passes: the first with every source's room the hill's (`hill_scale`) finds the hill's own bound A_1, the second with every source's room the larger of the hill's and the tension's at q_max = Gamma + SUM W_a A_1, the largest Link factor the axis lines within A_1 admit (`source_room`, `tension_room`, `factor_bound`; `bound_under_rooms`, the one pass), the bound at most A_1 and no fixed point, since q_max(A_1) bounds q_max(A) (the mathematician's hand and the advisor's second, two hands; the shipped universes' bound 6,949 set by light's Links' sum, the write's total not their binding term); refused by name where no level fits. A turned level is a plain level (features/phase, the temporal gauge): no shear takes a room."""
    hill = bound_under_rooms(families, gamma, action, width, unit, None)
    return bound_under_rooms(families, gamma, action, width, unit, hill)


def bound_under_rooms(
    families: tuple[FamilyRule, ...], gamma: int, action: int, width: int, unit: int, hill: int | None
) -> int:
    """One pass of `amplitude_bound`: the largest level inside the width under Rule3's totals, the currents' reading and every held family's one write per part, its rooms read by `write_rooms` at `hill`, None every source's room the hill's (the first pass, whose level is the hill's own bound A_1) and A_1 the larger of the hill's and the tension's room per source (the second pass, the bound); refused by name where no level fits."""
    largest = largest_of(width)
    found = largest
    for index, family in enumerate(families):
        num, den = family.pair
        edge = edge_of(family.pair, gamma)
        for clock, pace in ((gamma, gamma), (0, 0), (edge, edge)):
            reads, self_coefficient, wall = coefficients(num, den, gamma, clock, pace, None, unit)
            plain = sum(abs(read) for read in reads)  # the six plain reaches, R_ij = p_i^2 X_ij
            arrivals = plain  # the six arrivals' reads, under the pair's two parts where the plane turns or folds
            if folds(families, index):  # the six arrivals each under a pair's two parts, within 2 X
                arrivals *= FOLD_REACH
            elif turns(families, index):  # the sign's pair with the phase: the pair's extreme, X 2^(1/2)
                from event_universe.plane import turned_room  # plane reads this module: imported here

                arrivals = PORTS * pace * pace * turned_room(family.pair, gamma, unit)
            own = mass(num, den, clock, unit)  # the flux line's five partial sums (rule3.partial_rooms)
            *partials, total = partial_rooms(
                reads, self_coefficient, wall, own, arrivals + plain, arrivals
            )
            for room, head in (*((room, largest) for room in partials), (total, largest - wall)):
                if room:
                    found = min(found, int(division_forward(head, room, 0)[0]))
        if family.quanta and num:
            room = PORTS * PRODUCTS * family.record * abs(num)
            found = min(found, largest_below(int(division_forward(largest, room, 0)[0])))
        if family.held:
            from event_universe.loader.rooms import write_rooms  # rooms reads this module: imported here

            write = held_write_of(families, index, action, unit)
            rooms = write_rooms(families, index, write, gamma, hill, unit)
            from event_universe.loader.rooms import held_room  # rooms reads this module: imported here

            found = held_room(family, write, rooms, found, largest, gamma, action, width)
        if found < 1:
            raise ValueError(
                f"the pair [{num}, {den}] at the Node clock Gamma = {gamma} and T = {action}: the totals of "
                f"Rule3, of the currents and of the write leave no level inside the width of {width} bits "
                "(ALGEBRA.md #the-bound)"
            )
    return found
