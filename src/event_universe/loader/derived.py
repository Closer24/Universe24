"""The families from the rule (ALGEBRA.md #a-familys-declaration, the families from the rule): a family's row holds its name, its pair and what it holds, and the rule derives the rest from its rank and its pair (the parts, the reads, the family it gives); the amplitude bound A is derived from the integer width, never written (ALGEBRA.md #the-bound)."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, isqrt

from event_universe.core.rule3 import ISOTROPIC, coefficients, division_forward
from event_universe.features.counts_line import PORTS, PRODUCTS

VACUUM_PAIR = (1, 1)  # the rule's own massless band, the band of the real field of the highest rank
BY_PLAIN, BY_SIGN = "plain", "sign"  # a read of the level as it is, or by the reader's sign q
CONTENT, SIGN = "content", "sign"  # what a held family holds
NO_SIGN = 0  # the sign q of every family: the files declare none (the sign left the files)
RANKS = ((1,), (1, 3), (1, 3, 6))  # the parts of a rank: the count, its current, the current's tensor


@dataclass(frozen=True)
class Read:
    """One read of a family: the read family's index, the weight 1 of the rule and the word by which it reads (plain, or by the reader's sign)."""

    family: int
    weight: int
    by: str


@dataclass(frozen=True)
class FamilyRule:
    """A family as the rule derives it from its row: its name, its pair [num, den], what it holds (content, sign or nothing) at the divisor E_s, its parts, its reads, the family it gives at a click (None: it gives nothing) and its sign q."""

    name: str
    pair: tuple[int, int]
    held: str | None
    divisor: int | None
    parts: tuple[int, ...]
    reads: tuple[Read, ...]
    gives: int | None
    sign: int

    @property
    def quanta(self) -> bool:
        """Whether the family carries quanta: two levels, a count and its current (every family but the holders of the content)."""
        return self.held != CONTENT


def reduced(pair: tuple[int, int]) -> tuple[int, int]:
    """The pair in lowest terms, the band it names; the coefficients stay on the pair as written."""
    divisor = gcd(pair[0], pair[1]) or 1
    return pair[0] // divisor, pair[1] // divisor


def rank_of(held: str | None, pair: tuple[int, int]) -> tuple[int, ...]:
    """The parts from what writes the family: the count, the current and the current's tensor for the real field of the vacuum's band holding the content; the count and the current for the holder of the sign; the count alone otherwise."""
    if held == SIGN:
        return RANKS[1]
    if held == CONTENT and reduced(pair) == VACUUM_PAIR:
        return RANKS[2]
    return RANKS[0]


def family_rules(
    rows: list[tuple[str, tuple[int, int], str | None, int | None]],
) -> tuple[FamilyRule, ...]:
    """Every family from its row (name, pair, held word, divisor): the reads of a family of quanta are every holder of the content by plain and every holder of the sign of a higher rank by its sign, at the weight 1, in the file's order; a held family of the content reads nothing; the family it gives is the one holder of the sign it reads, none where it reads none, and two are refused by name."""
    ranks = [rank_of(held, pair) for _name, pair, held, _divisor in rows]
    found = []
    for index, (name, pair, held, divisor) in enumerate(rows):
        reads: list[Read] = []
        if held != CONTENT:
            for other, (_n, _p, other_held, _d) in enumerate(rows):
                if other_held == CONTENT:
                    reads.append(Read(other, 1, BY_PLAIN))
                elif other_held == SIGN and len(ranks[other]) > len(ranks[index]):
                    reads.append(Read(other, 1, BY_SIGN))
        signs = [read.family for read in reads if read.by == BY_SIGN]
        if len(signs) > 1:
            raise ValueError(
                f"the family {name!r} reads {len(signs)} holders of the sign: the family a body gives at its "
                "click is the one holder of the sign its family reads (ALGEBRA.md #the-counts-line)"
            )
        gives = signs[0] if signs else None
        found.append(FamilyRule(name, pair, held, divisor, ranks[index], tuple(reads), gives, NO_SIGN))
    return tuple(found)


def largest_of(width: int) -> int:
    """The largest integer of the file's width in bits, 2^width - 1, the bound every total of the law stays inside (ALGEBRA.md #the-bound)."""
    return int(2**width - 1)


def amplitude_bound(
    families: tuple[FamilyRule, ...], gamma: int, action: int, most: int, width: int
) -> int:
    """THE AMPLITUDE BOUND A, DERIVED AND NEVER WRITTEN: the largest level at which Rule3's total 6 A R + A |S| + w (A + 1) stays inside the file's width for every pair at the levels 0, Gamma div 2 and Gamma - 1 (ALGEBRA.md #the-bound), and at which the count's line's total 6 x 2 |num| A^2 + W_c (most + 2) of every family of quanta does too (ALGEBRA.md #the-counts-line, the bound), W_c = 3 den T and most the largest count a body declares at a Node; refused by name where no level fits."""
    largest = largest_of(width)
    found = largest
    for family in families:
        num, den = family.pair
        for level in (0, int(division_forward(gamma, 2, 0)[0]), gamma - 1):
            reads, self_coefficient, wall = coefficients(num, den, gamma, level, ISOTROPIC, True)
            room = 6 * abs(reads[0]) + abs(self_coefficient) + wall
            found = min(found, int(division_forward(largest - wall, room, 0)[0]))
        if family.quanta and num:
            spare = max(largest - 3 * den * action * (most + 2), 0)
            found = min(found, isqrt(int(division_forward(spare, PORTS * PRODUCTS * abs(num), 0)[0])))
        if found < 1:
            raise ValueError(
                f"the pair [{num}, {den}] at the Node clock Gamma = {gamma} and T = {action}: the totals of "
                f"Rule3 and of the count's line leave no level inside the width of {width} bits "
                "(ALGEBRA.md #the-bound)"
            )
    return found
