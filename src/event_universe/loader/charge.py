"""The charge per quantum of the sign holder's readers (ALGEBRA.md, The constants: the charge is the Wronskian per quantum and the sign's reader is Pythagorean, the owner's words of 2026-10-24): each reader's Wronskian enters the holder's one write times 3 T den over its own count unit W_c sin omega_0 = 3 T den sin omega_0 (`derived.count_wall`), one over the sine, so that every quantum of every family writes T / 2 per count (`charge_factors`: the readers' units brought to one wall by their least common multiple as the tension lines' dens are, the factors and the multiple reduced once by their common divisor, a massless reader's factor the multiple itself); a reader whose sine is irrational is refused by name (`pythagorean_readers`), as the conversion refuses it from every exact list (ALGEBRA.md 180); the former behaviour of 236e74ed0 (the count unit rounded once, the lcm of units sharing no structure) kept by name as its defect."""

from __future__ import annotations

from math import gcd

from event_universe.core.rule3 import division_forward, largest_below
from event_universe.loader.derived import FamilyRule, count_wall, readers_of


def pythagorean_readers(families: tuple[FamilyRule, ...], index: int) -> None:
    """The sign's reader is Pythagorean (the owner's word of 2026-10-24, (ii), "closed"; ALGEBRA.md, The constants): a reader of the holder of the sign `index` writes its charge per quantum by its count unit, exact for a Pythagorean pair alone; a reader with an irrational sine is refused by name, as the conversion refuses it from every exact list (ALGEBRA.md, The conversion, 180), the sentence naming the reader, its pair and its den^2 - num^2; a massless reader (num = den) carries its Wronskian as before. The former behaviour of 236e74ed0, the count unit rounded once and the readers' units brought to one wall by their lcm, kept by name as its defect."""
    holder = families[index]
    for other in readers_of(families, index):
        num, den = families[other].pair
        gap = den * den - num * num
        if (
            families[other].plane and abs(num) != den and largest_below(gap) ** 2 != gap
        ):  # a real-line reader is refused as no plane (loader/universe)
            raise ValueError(
                f"{families[other].name!r} reads the holder of the sign {holder.name!r} with the pair "
                f"[{num}, {den}], whose sine is irrational (den^2 - num^2 = {gap}, no square): a reader of "
                "the sign writes its charge per quantum by its count unit, exact for a Pythagorean pair "
                "alone; a reader with an irrational sine is refused, as the conversion refuses it from every "
                "exact list (ALGEBRA.md, The conversion, 180; The constants, the owner's word of 2026-10-24; "
                "the rounded count unit and the lcm of 236e74ed0 the former behaviour, kept by name as its defect)"
            )


def charge_factors(
    families: tuple[FamilyRule, ...], index: int, action: int
) -> tuple[dict[int, int], int]:
    """The sign holder's readers' charge factors and the walls' charge multiple (ALGEBRA.md, The constants, 2026-10-24): per reader with a gap 3 T den over its count unit, the units brought to their least common multiple by the division act on the greatest common divisor, the factors and the multiple reduced once by their common divisor; a massless reader's factor the multiple itself; the readers Pythagorean first (`pythagorean_readers`), so that every unit is 3 T times an integer sine and the multiple stays within the den."""
    pythagorean_readers(families, index)
    sources = readers_of(families, index)
    units = {
        other: count_wall(families[other], action)
        for other in sources
        if abs(families[other].pair[0]) != families[other].pair[1]
    }
    charge = 1
    for unit_of_one in units.values():
        charge = int(division_forward(charge * unit_of_one, gcd(charge, unit_of_one), 0)[0])
    factors = {
        other: 3 * action * families[other].pair[1] * int(division_forward(charge, units[other], 0)[0])
        if other in units
        else charge
        for other in sources
    }
    common = charge
    for factor in factors.values():
        common = gcd(common, factor)
    charge = int(division_forward(charge, common, 0)[0])
    return {
        other: int(division_forward(factor, common, 0)[0]) for other, factor in factors.items()
    }, charge
