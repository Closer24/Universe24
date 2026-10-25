"""The sign's reader is Pythagorean (ALGEBRA.md, The constants, the owner's word of 2026-10-24): a reader of the holder of the sign whose sine is irrational is refused by name (`pythagorean_readers`). The charge factors that stood here the same morning (`charge_factors`, each reader's Wronskian times 3 T den over its own count unit, the units brought to one wall) left with the law's sentence The charge written is the Wronskian over T div 2 for every reader: the write reads no family's sine and no count unit, one wall 2 E_s T Gamma (`derived.held_write_of`); kept by name as the defect, the electron's factor 1,822 times the proton's on the one universe file."""

from __future__ import annotations

from event_universe.core.rule3 import largest_below
from event_universe.loader.derived import FamilyRule, readers_of


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
