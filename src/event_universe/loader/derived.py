"""The families from the rule (ALGEBRA.md #a-familys-declaration, every family has a dimension): a family's row holds its name, its pair and either its dimension (a family of quanta: one real line, or a plane of two) or what sources it (a held row: the form, the tensions, the Wronskian) at its divisor and its rest, and the rule derives the rest from these alone with no name (who reads whom, who sources whom, the one write per held part with its walls); the amplitude bound A is derived from the integer width by the fixed point of the division act, never written and never by a root (ALGEBRA.md #the-bound)."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from event_universe.core.rule3 import ISOTROPIC, coefficients, division_fixed_point, division_forward
from event_universe.features.currents import DIFFERENCE, PORTS, PRODUCTS


@dataclass(frozen=True)
class Row:
    """A family's row as the loader reads it from the universe file: its name, its pair [num, den], its lines in all (a family of quanta's dimension, 1 or 2, times its parts; a held row's sources' count, one real line per source), its parts (the records of one event never summed at a Node, 2 for the pair family, 1 otherwise), whether its lines are planes (re and im: charged matter), whether it is sourced by its readers' Wronskian (the holder of the sign; else by their form, and by their tensions where it has the axis lines), its divisor where it is held and its rest."""

    name: str
    pair: tuple[int, int]
    lines: int
    parts: int
    plane: bool
    wronskian: bool
    divisor: int | None
    rest: int


@dataclass(frozen=True)
class Read:
    """One read of a family: the held family whose time line it reads at the weight 1 of the rule, by the plain read into its paces."""

    family: int
    weight: int


@dataclass(frozen=True)
class FamilyRule(Row):
    """A family as the rule derives it from its row (`Row`) with its reads: the held rows whose time line it reads, which by the hold's reciprocity it sources at the same weights; its rest the vacuum content of the massless row holding the content, the level at which the row rests everywhere, 0 for every other row (ALGEBRA.md #what-is-open, item 22)."""

    reads: tuple[Read, ...]

    @property
    def held(self) -> bool:
        """Whether the family is held: a row with a divisor, written by the hold and read by others."""
        return self.divisor is not None

    @property
    def quanta(self) -> bool:
        """Whether the family carries quanta, stepping at the paces of its reads with its share its count and its currents a detector's reading: every family of quanta and the holder of the sign, whose own record is light; a held row sourced by the form holds the content and steps at the pace 1."""
        return not self.held or self.wronskian

    @property
    def width(self) -> int:
        """The lines of one part, the lines in all over the parts: one real line, or a plane's two (ALGEBRA.md #a-familys-declaration, the dimension's table)."""
        return self.lines // self.parts

    @property
    def axes(self) -> bool:
        """Whether the row carries the three axis lines beside its time line: a held row sourced by the tensions (the massless row holding the content)."""
        return self.held and self.lines > 1


@dataclass(frozen=True)
class HeldWrite:
    """A held family's one write per line as the rule derives it from the rows (ALGEBRA.md #the-primitives, a family's write is one act): the walls, one per line, the time line's E_s T and each axis line's E_s W_c with W_c = 3 den T of the families that source it (one den among them; with several, the least common multiple of their den in den's place), and per sourcing family the factor with which its tension enters the axis parts' numerator, the multiple over its own den (1 where one den serves every source), so that the sum of the sources' fractions is one fraction over one wall, exact."""

    walls: tuple[int, ...]
    factors: dict[int, int]


def family_rules(rows: list[Row]) -> tuple[FamilyRule, ...]:
    """Every family from its row by the pair and the dimension alone (ALGEBRA.md #a-familys-declaration, the dimension's table): a family of quanta reads every held row sourced by the form (the content) at the weight 1 and, where it is a plane, every held row sourced by the Wronskian (the sign); a held row sourced by the form reads nothing, and a row never reads its own level (light, the sign row's own real record, reads no holder of the sign); by the hold's reciprocity a family sources what it reads at the same weight, a plane with its Wronskian and real lines with their form and their tensions; no family gives another anything."""
    found = []
    for index, row in enumerate(rows):
        reads: list[Read] = []
        if row.divisor is None or row.wronskian:
            for other, held in enumerate(rows):
                if held.divisor is not None and other != index and (row.plane or not held.wronskian):
                    reads.append(Read(other, 1))
        found.append(
            FamilyRule(
                row.name,
                row.pair,
                row.lines,
                row.parts,
                row.plane,
                row.wronskian,
                row.divisor,
                row.rest,
                tuple(reads),
            )
        )
    return tuple(found)


def weight_of(held: int, reader: FamilyRule) -> int:
    """The weight with which a family reads a held family, and so sources it, the one weight of the pair (ALGEBRA.md #the-primitives, a family's write: whoever reads with w sources with w), 0 where it does not read it."""
    return sum(read.weight for read in reader.reads if read.family == held)


def readers_of(families: tuple[FamilyRule, ...], held: int) -> list[int]:
    """The families that read the held family `held`, and so source it, in the file's order."""
    return [other for other, family in enumerate(families) if weight_of(held, family)]


def count_wall(family: FamilyRule, action: int) -> int:
    """The count's wall W_c = 3 den T, the family's plain wall times the universe's quantum action: the unit in which a share is read as quanta (ALGEBRA.md #the-count-is-the-records-share)."""
    return 3 * family.pair[1] * action


def held_write(families: tuple[FamilyRule, ...], index: int, action: int) -> HeldWrite:
    """The one write per line of the held family `index` (`HeldWrite`): its walls from the row's divisor, the quantum action and the den of the families that source its axis lines (its readers, whose tension it takes), the multiple of their den by the division act on the greatest common divisor, and each source's factor, the multiple over its den."""
    family = families[index]
    assert family.divisor is not None
    sources = readers_of(families, index)
    multiple = 1
    for other in sources:
        den = families[other].pair[1]
        multiple = int(division_forward(multiple * den, gcd(multiple, den), 0)[0])
    walls = [family.divisor * action]
    walls += [family.divisor * 3 * multiple * action] * (family.lines - 1)
    factors = {
        other: int(division_forward(multiple, families[other].pair[1], 0)[0]) for other in sources
    }
    return HeldWrite(tuple(walls), factors)


def largest_of(width: int) -> int:
    """The largest integer of the file's width in bits, 2^width - 1, the bound every total of the law stays inside (ALGEBRA.md #the-bound)."""
    return int(2**width - 1)


def write_rooms(families: tuple[FamilyRule, ...], index: int, write: HeldWrite) -> list[int]:
    """The room of a held family's one write per part at the amplitude A, the numerator's size over A^2 at the largest level: for the time part SUM over the sourcing families of w x 2 per line of a source (the form, two products per line) where the row takes the form, and w x 2 per source (the Wronskian, two products) where it takes the Wronskian; for each axis part SUM over the sources of w x factor x lines x 2 x 2 |num| (the tension per line, two products of a level and a difference of two levels, |num| on each)."""
    family = families[index]
    sources = readers_of(families, index)
    time = sum(
        abs(weight_of(index, families[other]))
        * PRODUCTS
        * (1 if family.wronskian else families[other].lines)
        for other in sources
    )
    axis = sum(
        abs(weight_of(index, families[other]))
        * write.factors[other]
        * families[other].lines
        * PRODUCTS
        * DIFFERENCE
        * abs(families[other].pair[0])
        for other in sources
    )
    return [time] + [axis] * (family.lines - 1)


def amplitude_bound(families: tuple[FamilyRule, ...], gamma: int, action: int, width: int) -> int:
    """The amplitude bound A, derived and never written: the largest level at which Rule3's total 6 A R + A |S| + w (A + 1) stays inside the file's width for every pair at the levels 0, Gamma div 2 and Gamma - 1 (ALGEBRA.md #the-bound), at which the currents' reading at a Node, 6 x 2 x lines x |num| A^2 for every family of quanta (the two products of each of the record's lines through the six Ports; the largest A whose square fits, the fixed point of the division act), does too (features/currents), and at which every held family's one write per part, its numerator at the sources' room (`write_rooms`) plus its remainder under the wall, does too; refused by name where no level fits."""
    largest = largest_of(width)
    found = largest
    for index, family in enumerate(families):
        num, den = family.pair
        for level in (0, int(division_forward(gamma, 2, 0)[0]), gamma - 1):
            reads, self_coefficient, wall = coefficients(num, den, gamma, level, ISOTROPIC, True)
            room = 6 * abs(reads[0]) + abs(self_coefficient) + wall
            found = min(found, int(division_forward(largest - wall, room, 0)[0]))
        if family.quanta and num:
            room = PORTS * PRODUCTS * family.lines * abs(num)
            found = min(found, division_fixed_point(int(division_forward(largest, room, 0)[0])))
        if family.held:
            write = held_write(families, index, action)
            for wall, room in zip(write.walls, write_rooms(families, index, write), strict=True):
                if wall > largest:
                    found = 0
                elif room:
                    fits = int(division_forward(largest - wall, room, 0)[0])
                    found = min(found, division_fixed_point(fits))
        if found < 1:
            raise ValueError(
                f"the pair [{num}, {den}] at the Node clock Gamma = {gamma} and T = {action}: the totals of "
                f"Rule3, of the currents and of the write leave no level inside the width of {width} bits "
                "(ALGEBRA.md #the-bound)"
            )
    return found
