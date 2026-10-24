"""The charge per quantum of the sign holder's readers (ALGEBRA.md, The constants: the charge written is the Wronskian over T div 2 for every reader, the law's sentence of 2026-10-24, the owner's word of that morning, the charge universal like nature; the sign's reader is Pythagorean, the owner's word of the same day): each reader's Wronskian enters the holder's one write as it stands, the factor 1 and the one wall 2 E_s T Gamma for every family, a quantum of every plane family carrying W = T div 2 and writing the same charge (`charge_factors`); a reader whose sine is irrational is refused by name (`pythagorean_readers`); the former factor, 3 T den over each reader's count unit, kept by name as the defect (one born electron written as 1,822 proton charges on the one universe file)."""

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


def charge_factors(
    families: tuple[FamilyRule, ...], index: int, action: int
) -> tuple[dict[int, int], int]:
    """The sign holder's readers' charge factors and the walls' charge multiple (ALGEBRA.md, The constants, The charge written is the Wronskian over T div 2 for every reader, the law's sentence of 2026-10-24 on the owner's word of that morning, the charge universal like nature): the factor 1 for every reader and the multiple 1, so that each reader's Wronskian enters the holder's one write as it stands over the one wall 2 E_s T Gamma, a quantum of every plane family carrying W = T div 2 (the birth's quarter-turn lay at the massless pair, `act.born_pair`, `emission.laid_by_count`: A^2 = 17,956 at T 36,000 for the proton and the electron alike) and writing T / (2 Gamma) per interval, one quantum of charge in the books (`share.count_read`, the charge over T div 2) and in the holder alike; the readers Pythagorean first (`pythagorean_readers`). The former clause (3 T den over each reader's count unit W_c sin omega_0, the units brought to one wall by their least common multiple, 2026-10-24 to the same day) kept by name as the defect it was on the one universe file: the electron's factor 25,873,230,495 against the proton's 14,198,860, 1,822 times, so one born electron wrote 16,427 levels per interval into its row where the proton wrote 9, and the sign holder's row ran away threefold per interval on every structured board (the runaway hand's derivation, 2026-10-24)."""
    pythagorean_readers(families, index)
    return {other: 1 for other in readers_of(families, index)}, 1
