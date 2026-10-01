"""The families from the rule (ALGEBRA.md #a-familys-declaration, the families from the rule): a family's row holds its name, its pair and what it holds, and the rule derives the rest from its rank and its pair (the parts, the reads, the one write per held part with its walls); the amplitude bound A is derived from the integer width by the fixed point of the division act, never written and never by a root (ALGEBRA.md #the-bound)."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from event_universe.core.rule3 import ISOTROPIC, coefficients, division_fixed_point, division_forward
from event_universe.features.currents import DIFFERENCE, LEVELS, PORTS, PRODUCTS

VACUUM_PAIR = (1, 1)  # the rule's own massless band, the band of the real field of the highest rank
BY_PLAIN, BY_SIGN = "plain", "sign"  # a read of the level as it is, or by the reader's own sign q
CONTENT, SIGN = "content", "sign"  # what a held family holds: the forms' row, or the Wronskians' row
NO_SIGN = 0  # the sign q of every family: the files declare none (the sign left the files)
RANKS = ((1,), (1, 3))  # the parts Rule3 reads: the time part alone, or with the three axis tensions


@dataclass(frozen=True)
class Read:
    """One read of a family: the read family's index, the weight 1 of the rule and the word by which it reads (plain, or by the reader's sign)."""

    family: int
    weight: int
    by: str


@dataclass(frozen=True)
class FamilyRule:
    """A family as the rule derives it from its row: its name, its pair [num, den], what it holds (content, sign or nothing) at the divisor E_s, its parts, its reads (the rows it sources, at the same weights), its sign q and its rest (the vacuum content c_vac of the massless row holding the content, the level at which the row rests everywhere, up to every face and beyond it; 0 for every other row, ALGEBRA.md #what-is-open, item 22)."""

    name: str
    pair: tuple[int, int]
    held: str | None
    divisor: int | None
    parts: tuple[int, ...]
    reads: tuple[Read, ...]
    sign: int
    rest: int

    @property
    def quanta(self) -> bool:
        """Whether the family carries quanta: two level pairs whose share is its count and whose currents a detector reads (every family but the holders of the content)."""
        return self.held != CONTENT


@dataclass(frozen=True)
class HeldWrite:
    """A held family's one write per part as the rule derives it from the rows (ALGEBRA.md #the-primitives, a family's write is one act): the walls, one per part, the time part's E_s T and each axis part's E_s W_c with W_c = 3 den T of the families that source it (one den among them; with several, the least common multiple of their den in den's place), and per sourcing family the factor with which its tension enters the axis parts' numerator, the multiple over its own den (1 where one den serves every source), so that the sum of the sources' fractions is one fraction over one wall, exact."""

    walls: tuple[int, ...]
    factors: dict[int, int]


def reduced(pair: tuple[int, int]) -> tuple[int, int]:
    """The pair in lowest terms, the band it names; the coefficients stay on the pair as written."""
    divisor = gcd(pair[0], pair[1]) or 1
    return pair[0] // divisor, pair[1] // divisor


def rank_of(held: str | None, pair: tuple[int, int]) -> tuple[int, ...]:
    """The parts Rule3 reads of what the family holds: the time part and the three axis tensions for the real field of the vacuum's band holding the content; the time part alone otherwise (the parts Rule3 never reads left, the owner, 2026-09-30)."""
    if held == CONTENT and reduced(pair) == VACUUM_PAIR:
        return RANKS[1]
    return RANKS[0]


def family_rules(
    rows: list[tuple[str, tuple[int, int], str | None, int | None, int]],
) -> tuple[FamilyRule, ...]:
    """Every family from its row (name, pair, held word, divisor, rest): the reads of a family of quanta are every holder of the content by plain and every other holder of the sign by its own sign, at the weight 1, in the file's order, and it sources what it reads at the same weight, a holder of the content with its form and the holder of the sign with its Wronskian; a held family of the content reads nothing; no family gives another anything (ALGEBRA.md #the-count-is-the-records-share, light is born by the write)."""
    ranks = [rank_of(held, pair) for _name, pair, held, _divisor, _rest in rows]
    found = []
    for index, (name, pair, held, divisor, rest) in enumerate(rows):
        reads: list[Read] = []
        if held != CONTENT:
            for other, (_n, _p, other_held, _d, _r) in enumerate(rows):
                if other_held == CONTENT:
                    reads.append(Read(other, 1, BY_PLAIN))
                elif other_held == SIGN and other != index:
                    reads.append(Read(other, 1, BY_SIGN))
        found.append(FamilyRule(name, pair, held, divisor, ranks[index], tuple(reads), NO_SIGN, rest))
    return tuple(found)


def weight_of(held: int, reader: FamilyRule, by: str = BY_PLAIN) -> int:
    """The weight with which a family reads a held family by `by`, and so sources it, the one weight of the pair (ALGEBRA.md #the-primitives, a family's write: whoever reads with w sources with w), 0 where it does not read it so."""
    return sum(read.weight for read in reader.reads if read.family == held and read.by == by)


def count_wall(family: FamilyRule, action: int) -> int:
    """The count's wall W_c = 3 den T, the family's plain wall times the universe's quantum action: the unit in which a share is read as quanta (ALGEBRA.md #the-count-is-the-records-share)."""
    return 3 * family.pair[1] * action


def held_write(families: tuple[FamilyRule, ...], index: int, action: int) -> HeldWrite:
    """The one write per part of the held family `index` (`HeldWrite`): its walls from the row's divisor, the quantum action and the den of the families that source its axis parts (the readers by plain, whose tension it takes; a reader by sign sources the time part alone), the multiple of their den by the division act on the greatest common divisor, and each source's factor, the multiple over its den."""
    family = families[index]
    assert family.divisor is not None
    sources = [other for other in range(len(families)) if weight_of(index, families[other])]
    multiple = 1
    for other in sources:
        den = families[other].pair[1]
        multiple = int(division_forward(multiple * den, gcd(multiple, den), 0)[0])
    walls = [family.divisor * action]
    walls += [family.divisor * 3 * multiple * action] * sum(family.parts[1:])
    factors = {
        other: int(division_forward(multiple, families[other].pair[1], 0)[0]) for other in sources
    }
    return HeldWrite(tuple(walls), factors)


def largest_of(width: int) -> int:
    """The largest integer of the file's width in bits, 2^width - 1, the bound every total of the law stays inside (ALGEBRA.md #the-bound)."""
    return int(2**width - 1)


def write_rooms(families: tuple[FamilyRule, ...], index: int, write: HeldWrite) -> list[int]:
    """The room of a held family's one write per part at the amplitude A, the numerator's size over A^2 at the largest level: for the time part SUM over the sourcing families of w x 2 x 2 by plain (the form over two level pairs, two products each) and w x 2 by sign (the Wronskian, two products), for each axis part SUM over the readers by plain of w x factor x 2 x 2 x 2 |num| (the tension over two level pairs, two products of a level and a difference of two levels, |num| on each)."""
    sources = [other for other in range(len(families)) if weight_of(index, families[other])]
    time = sum(abs(weight_of(index, families[other])) * LEVELS * PRODUCTS for other in sources)
    time += sum(abs(weight_of(index, other, BY_SIGN)) * PRODUCTS for other in families)
    axis = sum(
        abs(weight_of(index, families[other]))
        * write.factors[other]
        * LEVELS
        * PRODUCTS
        * DIFFERENCE
        * abs(families[other].pair[0])
        for other in sources
    )
    return [time] + [axis] * sum(families[index].parts[1:])


def amplitude_bound(families: tuple[FamilyRule, ...], gamma: int, action: int, width: int) -> int:
    """The amplitude bound A, derived and never written: the largest level at which Rule3's total 6 A R + A |S| + w (A + 1) stays inside the file's width for every pair at the levels 0, Gamma div 2 and Gamma - 1 (ALGEBRA.md #the-bound), at which the currents' reading at a Node, 6 x 2 x 2 |num| A^2 for every family of quanta (the two products of each of the record's two level pairs through the six Ports; the largest A whose square fits, the fixed point of the division act), does too (features/currents), and at which every held family's one write per part, its numerator at the sources' room (`write_rooms`) plus its remainder under the wall, does too; refused by name where no level fits."""
    largest = largest_of(width)
    found = largest
    for index, family in enumerate(families):
        num, den = family.pair
        for level in (0, int(division_forward(gamma, 2, 0)[0]), gamma - 1):
            reads, self_coefficient, wall = coefficients(num, den, gamma, level, ISOTROPIC, True)
            room = 6 * abs(reads[0]) + abs(self_coefficient) + wall
            found = min(found, int(division_forward(largest - wall, room, 0)[0]))
        if family.quanta and num:
            room = PORTS * PRODUCTS * LEVELS * abs(num)
            found = min(found, division_fixed_point(int(division_forward(largest, room, 0)[0])))
        if family.held is not None:
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
