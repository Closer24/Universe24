"""The conversion, a click's act outside the step (ALGEBRA.md, The conversion; Only a click moves a quantum between families; The declarations by name 5; the owner's word of 2026-10-21, the table's declaration deleted): a record of one family credited at a declared instrument region is taken whole at the drawn Node by the region's credit and given back as whole quanta of other families laid at that Node, the rotations adding exactly in the integers. No table and no key names the records out: given the pairs, every family of quanta with a gap and a Pythagorean pair converts wherever exactly one list of the universe's other gapped families keeps the law's conservations, which are fixed and never declared, the count by whole quanta, the rotation (a rotation whose cosine is num / den has a rational sine iff den^2 - num^2 is a square, the point num + i s a Gaussian integer of norm den, `gaussian`, angle addition the Gaussian product, so a list of whole quanta at their rest rotations carries the parents' rotations exactly iff the two Gaussian products agree once each is scaled by the other's dens, `rotation`, `exact`), the charge (the Wronskian's sum, the plane records out at their senses summing to the parents' senses) and the baryon (as many records of three lines out as in, `kept`); a family with no such list never converts, its stability derived (`listed`, `declared`), and one with several is refused by name, the law having no share among them. The one residual declaration is the senses of a real-line parent's plane records out, the row's key `senses` (`senses_of`): a parent of real lines has the Wronskian 0, which (+, -) and (-, +) keep alike, so which record out is the particle is not in the pairs; one plane record out named and the rest the sum's; refused on a plane parent, whose own sense as read at the click turns its list (`sense_at`). The same rule for N credited quanta (the collision, `listed` with the parents' rotations' product and their senses summed; the null list, the parents themselves, the identity of the group and the no-conversion outcome, never a second list); the search bounded at N + BEYOND records out, a bound named and no law. The when is the region's, the window's close of the arriving record's passage, the Node the credit's own draw by the digits (`lists.region`, `lists.credited_node`); the act is the credit's hole over every line of the record and one lay by the count per record out at that Node at its family's massless pair (`emission.laid_by_count`), the identity asserted in the integers at the write and the conversion line written beside the credit's (`converted`, `line`). The Node knows no conversion; Rule3 steps the records out as it steps every record."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from event_universe.core.rule3 import largest_below
from event_universe.loader.derived import FamilyRule

if TYPE_CHECKING:
    pass

BARYON_LINES = 3  # the baryon's shape in the law's families: a record of three lines, real or planes
Pair = tuple[int, int]
Gauss = tuple[int, int]  # a Gaussian integer a + i b
Table = tuple[tuple[int, int], ...]  # the records out, each its family by position and its sense
Parents = tuple[
    tuple[int, int], ...
]  # the records in, each its family and its sense as read, 0 for real lines


def sine_of(pair: Pair) -> int | None:
    """The integer sine of a pair, s with s^2 = den^2 - num^2 (sin omega times den), None where the pair is not Pythagorean: the rotation's cosine and sine are both rational iff den^2 - num^2 is a square."""
    num, den = pair
    gap = den * den - num * num
    sine = largest_below(gap)
    return sine if sine * sine == gap else None


def gaussian(pair: Pair) -> Gauss | None:
    """The pair's point on the circle as a Gaussian integer, num + i s of norm den, None where the pair is not Pythagorean (`sine_of`)."""
    sine = sine_of(pair)
    return None if sine is None else (pair[0], sine)


def candidates(families: tuple[FamilyRule, ...]) -> list[int]:
    """The families a record out may be: the families of quanta with a gap (num below den), each at its rest rotation; a massless family rests at the rotation 0 and a one-Node lay carries no wave number, so it is no record out, and a held row holds no quantum."""
    return [
        k for k, family in enumerate(families) if not family.held and family.pair[0] != family.pair[1]
    ]


def baryons(families: tuple[FamilyRule, ...], rows: Sequence[tuple[int, int]]) -> int:
    """The records of three lines among the rows, the baryon's count, the law's shape for it (`BARYON_LINES`)."""
    return sum(1 for k, _sense in rows if families[k].laid == BARYON_LINES)


def kept(families: tuple[FamilyRule, ...], parents: Parents, table: Table) -> bool:
    """Whether a list keeps the law's two conservations beyond the count's and the rotation's, fixed and never declared: the charge, the Wronskian's sum, the plane records out at their senses (a record of real lines at 0) summing to the parents' senses summed (each parent's as read at the Node, `sense_at`, 1 at rest for a plane and 0 for real lines); the baryon, as many records of three lines out as in (`baryons`)."""
    senses = sum(sense for out, sense in table if families[out].plane)
    if senses != sum(sense for _parent, sense in parents):
        return False
    return baryons(families, table) == baryons(families, parents)


BEYOND = 2  # the search's bound, named and no law (the conversion's own to the sweep of 2026-10-24): a meeting of q quanta births a list of at most q + BEYOND children


def conjugate_exact(families: tuple[FamilyRule, ...], table: Table) -> bool:
    """Whether a list of children completes the identity of massless parents (ALGEBRA.md, Matter's birth from light: their points (den, 0) multiply to the identity, and the children at their senses complete it, (num + i s)(num - i s) = den^2): the product over the children of (num_k + i sense_k s_k), each the family's point at the child's sense, equal to (the product of their dens, 0), exact in the Gaussian integers; the birth's own exactness, the conjugate point at the sense -1 (the conversion's exactness reads the same point at both senses, L188)."""
    point: Gauss = (1, 0)
    scale = 1
    for out, sense in table:
        found = gaussian(families[out].pair)
        if found is None:
            return False
        point = times(point, (found[0], sense * found[1]))
        scale *= families[out].pair[1]
    return point == (scale, 0)


def times(a: Gauss, b: Gauss) -> Gauss:
    """The product of two Gaussian integers, the rotations composed."""
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def lists_of(families: tuple[FamilyRule, ...], quanta: int) -> list[Table]:
    """The exact lists `quanta` whole quanta of a massless family make at one Node (ALGEBRA.md, Matter's birth from light, the clause of 2026-10-24 on the owner's word, several can be born): every multiset of at most quanta + BEYOND children of the plane families with a Pythagorean pair, each child at a sense, that completes the parents' identity (`conjugate_exact`) and keeps the two conservations (`kept`, the senses summing to the parents' 0 and the baryons to 0), the irreducible ones alone (`meeting_reducible`: a list that is the union of two parts' own lists over a partition of the quanta into two meetings is the quanta's separate clicks and no meeting of all; a part of one quantum has the null list alone, a meeting being two quanta), each list its (family, sense) rows in the families' order, the lightest first by the sum of its children's walls (`derived.count_wall`); the bound BEYOND is the search's and no law."""
    from itertools import combinations_with_replacement, product

    outs_at = [
        k for k in candidates(families) if families[k].plane and gaussian(families[k].pair) is not None
    ]
    parents: Parents = tuple((0, 0) for _ in range(quanta))
    found: set[Table] = set()
    for size in range(1, quanta + BEYOND + 1):
        for outs in combinations_with_replacement(outs_at, size):
            for senses in product((-1, 1), repeat=size):
                table: Table = tuple(sorted(zip(outs, senses, strict=True)))
                if (
                    table not in found
                    and kept(families, parents, table)
                    and conjugate_exact(families, table)
                    and not meeting_reducible(families, quanta, table)
                ):
                    found.add(table)
    return sorted(found, key=lambda table: (walls_of(families, table), table))


def walls_of(families: tuple[FamilyRule, ...], table: Table) -> int:
    """The sum of a list's children's walls, the energy the list needs, each child one quantum of its family at its own wall (`derived.count_wall` at the quantum action; the families' pairs alone, so the sum stands at every T up to the one factor: here at T = 1, the ordering of the lists)."""
    from event_universe.loader.derived import count_wall  # derived reads this module: imported here

    return sum(count_wall(families[out], 1) for out, _sense in table)


def meeting_reducible(families: tuple[FamilyRule, ...], quanta: int, table: Table) -> bool:
    """Whether a list of a meeting of `quanta` massless quanta is the union of two lists each a meeting's own: over every split of the quanta into two parts of at least two each, a split of the table into two sub-multisets each kept and exact for its part (the identity, so for any part), the quanta's separate clicks and no meeting of all; a part of one quantum has the null list alone (two quanta meet, L188), so a list of two quanta is never reducible."""
    if quanta < 4:
        return False
    for take in range(1, 2 ** len(table) - 1):
        one = tuple(row for at, row in enumerate(table) if take >> at & 1)
        other = tuple(row for at, row in enumerate(table) if not take >> at & 1)
        if all(
            kept(families, ((0, 0), (0, 0)), part) and conjugate_exact(families, part)
            for part in (one, other)
        ):
            return True
    return False


def birth_of(families: tuple[FamilyRule, ...], parent: int, quanta: int = 2) -> list[Table]:
    """Matter's birth from light, the gapless meeting's own clause (the law's sentence on the owner's word of 2026-10-23; N children on his word of 2026-10-24, several can be born): the exact lists `quanta` whole quanta of the gapless family `parent` make at one Node (`lists_of`), the lightest first by their summed walls; [] for a parent with a gap, whose quanta convert and are not born from (The conversion). To 2026-10-24 the one list per plane family, its conjugate pair ((k, -1), (k, 1)), the two kept by name as the lists at the bound 0."""
    if families[parent].pair[0] != families[parent].pair[1]:
        return []
    return lists_of(families, quanta)
