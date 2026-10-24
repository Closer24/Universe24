"""The universe file: one object of integers and no family row (the owner's word of 2026-10-24, "declaring a family is forbidden; they must emerge by themselves at the click"; ALGEBRA.md #a-familys-declaration, The circle of den): den, the Node clock Gamma, the quantum's action T, and the width and the Link unit until the constants hand strikes them (`INTEGER_KEYS`); the rows the engine's internals carry derived at load from den (`rows_of`): the massless point (den, den) on one real line, the seed every world is laid with (`MASSLESS`), the holder of the sign and the holder of the volume, both at the massless point (den, den), each built by its role (`sign_holder`, `volume_holder`, `volume_pair`, the one place the volume's pair is fixed; the owner's word of 2026-10-24, "no declarations"), and every Pythagorean point of den's circle in the open quadrant as a plane row named by its exponent vector over den's primes (`loader/circle.circle_points`, `label_of`; every point a plane until the kind sentence lands, the engine's stand-in and no sentence of the law), then the reads, the records and the sign holder's alpha derived as before (`resolved`; `derived.with_reads`, `derived.alpha_of`); the gone key `families` refused by name with the derivation that replaced it (`GONE`, `gone_refused`) (ENGINE.md section 4)."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from event_universe.core.ports import AXES
from event_universe.loader import derived
from event_universe.loader.circle import circle_points, label_of
from event_universe.loader.derived import PLANE, FamilyRule, Row
from event_universe.loader.keys import integer, keyed

UNIVERSE_KEYS = ("integers",)
INTEGER_KEYS = ("den", "node_clock", "quantum_action", "width", "link_unit")  # den, Gamma, T; the width and the Link unit until the constants hand strikes them
MASSLESS, SIGN, VOLUME = "massless", "sign", "volume"  # the three rows every den carries, named by what they are
GONE = {  # the file's gone keys and the derivation that replaced each (the owner's word of 2026-10-24; the old kept by name)
    "families": (
        "the families are no rows of the file (2026-10-24, the owner's word: declaring a family is forbidden, they "
        "must emerge by themselves at the click): the file holds den with the clock and the unit, and the loader "
        "derives at load the massless point (den, den) on one real line, the holder of the sign and the holder "
        "of the volume, both at (den, den), and every Pythagorean point of den's circle as "
        "a plane row named by its exponent vector over den's primes (ALGEBRA.md #a-familys-declaration, The "
        "circle of den; the keys `families` with `name`, `pair` and `dimension` the former declaration, kept by "
        "name)"
    ),
}


def gone_refused(entry: object, label: str) -> None:
    """A document naming a gone key is refused by name with the derivation that replaced it (`GONE`): `families`."""
    if not isinstance(entry, dict):
        return
    for key in GONE:
        if key in entry:
            raise ValueError(
                f"{label} holds the key {key!r}, a declaration no file carries: {GONE[key]}"
            )


def sign_holder(name: str, pair: tuple[int, int]) -> Row:
    """The holder of the sign by its role (the owner's word of 2026-10-24, no declarations; ALGEBRA.md #a-familys-declaration, The holders are derived): a held row of the time line and three odd axis lines sourced by its readers' Wronskian, acting by the rotation of their two-part records, the level weight 1 and the write weight 1 (the write's and the read's universality, its alpha carried inside its write by the loader, `derived.alpha_of`), no rest and no flux; its reads derived once every row is read (`derived.with_reads`). The former declaration, the key `held` with `sources`, `level_weight`, `write_weight` and `rest`, kept by name; the role read from the pair, massless the sign and gapped the volume, the loader's rule from 2026-10-24 to the family-less file, kept by name."""
    return Row(name, pair, 1 + AXES, 1, False, True, True, 1, 1, 0, ())


def volume_holder(name: str, pair: tuple[int, int]) -> Row:
    """The holder of the volume by its role (the owner's word of 2026-10-24, no declarations): a held row of the time line and three axis lines sourced by its readers' form and tensions, no Wronskian and no rotation, the level weight 1 and the write weight 1, no rest and no flux; its pair from `volume_pair`, the one place it is read, massless or gapped alike."""
    return Row(name, pair, 1 + AXES, 1, False, False, False, 1, 1, 0, ())


def volume_pair(den: int) -> tuple[int, int]:
    """The volume holder's pair, the one place it is fixed: the massless point (den, den), derived from den beside the sign holder's (the gravity hand's trial of 2026-10-24: the volume row laid at Gamma with no rest solve, one bang and the expansion for ever); the gapped alternative, (den - gap, den) with a gap the law does not fix (the one world's former row at the gap 38,024, the cycle of bangs), stands by name for the owner's word and would return here and nowhere else (ALGEBRA.md, The circle of den)."""
    return den, den


def rows_of(integers: dict[str, int]) -> list[Row]:
    """The rows derived from den (the module's sentence): the holder of the volume and the holder of the sign, each by its role, then the massless point on one real line (`sign_holder`, `volume_holder`, `volume_pair`), and den's circle, every point of the open quadrant a plane row named by its vector (`circle_points`, `label_of`)."""
    den = integers["den"]
    rows = [  # the holders first, the volume's before the sign's, as the one world's file stood (its first held row the volume's)
        volume_holder(VOLUME, volume_pair(den)),
        sign_holder(SIGN, (den, den)),
        Row(MASSLESS, (den, den), 1, 1, False, False, False, None, None, 0, ()),
    ]
    for vector, num, _sine in circle_points(den):
        rows.append(Row(label_of(vector), (num, den), PLANE, 1, True, False, False, None, None, 0, ()))
    return rows


def resolved(integers: dict[str, int], rows: list[Row]) -> tuple[FamilyRule, ...]:
    """The families from the rows: every row's reads derived (`derived.with_reads`), the records (`derived.family_rules`), the law's alpha inside the sign holder's write, the numerator times E_h T and the walls times Gamma (`derived.alpha_of`, the owner's law of one Node, 2026-10-23), and the carried factor's gate (`derived.shared_clock`)."""
    families = derived.family_rules(derived.with_reads(rows))
    families = tuple(
        replace(family, write_weight=alpha[0], write_wall=alpha[1])
        if family.held and family.wronskian
        else family
        for family in families
        for alpha in [
            derived.alpha_of(
                families, families.index(family), integers["node_clock"], integers["quantum_action"]
            )
            if family.held and family.wronskian
            else (1, 1)
        ]
    )
    derived.shared_clock(families)
    return families


def universe_of(document: object) -> tuple[dict[str, int], tuple[FamilyRule, ...]]:
    """The universe file: its one object of integers (`INTEGER_KEYS`, every key required, den from 1, the Link unit a power of two) and the families derived from den (`rows_of`, `resolved`); the key `families` refused by name with the derivation that replaced it (`gone_refused`), every other key refused as unknown."""
    gone_refused(document, "the universe file")
    universe = keyed(document, "the universe file", UNIVERSE_KEYS, UNIVERSE_KEYS)
    raw: dict[str, Any] = keyed(universe["integers"], "integers", INTEGER_KEYS, INTEGER_KEYS)
    integers = {key: integer(value, f"integers.{key}", 1) for key, value in raw.items()}
    unit = integers["link_unit"]
    if unit & (unit - 1):
        raise ValueError(
            f"integers.link_unit must be a power of two, the Link's unit G in which each Link's factor is one "
            f"integer (ALGEBRA.md #the-paces, The clock is the Node's, the tension is the Link's), got {unit}"
        )
    return integers, resolved(integers, rows_of(integers))
