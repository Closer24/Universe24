"""The universe file: its two keys, its integers (the Node clock Gamma, the quantum's action T and, to 2026-10-24, the Link unit G and the width, the width derived since, `loader/rooms.width_of`, `GONE_INTEGERS`) and the families' rows read into the loader's rows (`universe_of`), each family of quanta's shape from its row (`shape_of`), each holder's kind, lines, sources, weights and reads derived from its pair and the absence of a dimension (`holder_of`, `derived.with_reads`; the owner's word of 2026-10-24, "no declarations": a row is its name, its pair and, for a family of quanta, its dimension, nothing else), the key tables of the file and the gone keys refused by name with the derivation that replaced each (`GONE`, `gone_refused`) (ENGINE.md section 4; ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from event_universe.core.ports import AXES
from event_universe.loader import derived
from event_universe.loader.derived import KINDS, PLANE, PLANE_LINE, FamilyRule, Row
from event_universe.loader.keys import integer, keyed

UNIVERSE_KEYS = ("integers", "families")
INTEGER_KEYS = ("node_clock", "quantum_action", "link_unit")  # the width derived, 2026-10-24
GONE_INTEGERS = {  # the file's integers to 2026-10-24 that are the engine's and not the universe's (the owner's word of that day: only the universe's constants; the old kept by name)
    "width": (
        "the width is derived (2026-10-24): the least width at which the amplitude bound holds the volume's level "
        "at the deepest content the guard admits, the Link's last pace (loader/rooms.width_of; ALGEBRA.md #the-bound, "
        "The width is derived; the key `width`, the integers' bits, the former declaration, 92 in the one universe "
        "file, kept by name)"
    ),
}
FAMILY_KEYS, FAMILY_REQUIRED = (
    ("name", "pair", "dimension"),
    ("name", "pair"),
)  # a family of quanta declares its dimension; a row without one is a holder (2026-10-24)
GONE = {  # the rows' declared keys to 2026-10-24 and the derivation that replaced each (the owner's word of that day: no declarations; the old kept by name)
    "reads": (
        "the reads are derived (2026-10-24): every family of quanta and every holder of the volume reads every "
        "holder of the volume at the weight 1, a holder of the volume its own level among them, and every plane "
        "family (dimension 2) reads every holder of the sign at 1 too, a family of real lines none of the sign "
        "and the holder of the sign none at all (ALGEBRA.md #the-paces, The reads are derived; the key `reads` "
        "with its weights the former declaration, kept by name)"
    ),
    "held": (
        "a holder is derived (2026-10-24): a row with no `dimension` is held, a held row with a gap (num below "
        "den) holds the volume and is sourced by its readers' form and tensions, a held massless row (num = den) "
        "holds the sign and is sourced by their Wronskian, every level weight and every write weight is 1 and no "
        "row rests at a level (ALGEBRA.md #a-familys-declaration, The holders are derived; the key `held` with "
        "`sources`, `level_weight`, `write_weight` and `rest` the former declaration, kept by name)"
    ),
}


def gone_refused(entry: object, label: str) -> None:
    """A row naming a gone key is refused by name with the derivation that replaced it (`GONE`): `reads`, and `held` with its `sources`, `level_weight`, `write_weight` and `rest`."""
    if not isinstance(entry, dict):
        return
    for key in GONE:
        if key in entry:
            raise ValueError(
                f"{label} holds the key {key!r}, a declaration no file carries: {GONE[key]}"
            )


def shape_of(row: dict[str, Any], label: str) -> tuple[int, int, bool]:
    """A family of quanta's shape from its row, (lines, parts, plane): the family declares its `dimension`, any integer from 1, the lines of its record, each stepped by Rule3 as every line is, the form and the share the sum over them (1 one real line; 2 a plane, re and im, the one dimension with a Wronskian and a turn, `PLANE`; 3 three real lines, each stepped as a line of dimension one, no turn and no row of the sign; a dimension below 1 refused by name and no other refused by number), or its shape [parts, dimension], parts records of that dimension laid as one event and never summed at a Node (the pair family [2, 1], two real lines; ALGEBRA.md #a-familys-declaration, the dimension's table), or the shape by name, a list of its lines' kinds, `real` or `plane` (`KINDS`; the two hands: 1 and 2 kept as spellings, ["plane", "plane", "plane"] a record of three planes, one Wronskian per plane summed into its row, the proton's row; a record of real lines and planes together refused by name, not built); a held row declares no dimension, its lines its sources' count (`holder_of`)."""
    shape = row["dimension"]
    if isinstance(shape, list) and shape and all(isinstance(kind, str) for kind in shape):
        kinds = sorted(set(shape))
        if any(kind not in KINDS for kind in kinds):
            raise ValueError(
                f"{label}.dimension lists its lines' kinds, each one of {list(KINDS)}, got {shape!r}"
            )
        if len(kinds) > 1:
            raise ValueError(
                f"{label}.dimension {shape!r} mixes real lines and planes in one record: every line of a record is "
                "real or every line a plane (a mixed record is not built)"
            )
        plane = kinds[0] == PLANE_LINE
        return len(shape) * (PLANE if plane else 1), 1, plane
    if isinstance(shape, list) and len(shape) != 2:
        raise ValueError(
            f"{label}.dimension as a shape is [parts, dimension] or a list of its lines' kinds, got {shape!r}"
        )
    parts, lines = shape if isinstance(shape, list) else [1, shape]
    parts = integer(parts, f"{label}.dimension's parts", 1)
    lines = integer(lines, f"{label}.dimension", 1)
    return parts * lines, parts, lines == PLANE


def holder_of(name: str, pair: tuple[int, int]) -> Row:
    """A holder's row from its name and its pair alone (the owner's word of 2026-10-24, no declarations; ALGEBRA.md #a-familys-declaration, The holders are derived): a held row with a gap (num below den) holds the volume, its time line and three axis lines sourced by its readers' form and tensions, no Wronskian and no rotation; a held massless row (num = den) holds the sign, its time line and three odd axis lines sourced by its readers' Wronskian, acting by the rotation of their two-part records; the level weight 1 and the write weight 1 on either (the write's and the read's universality, the sign holder's alpha carried inside its write by the loader, `derived.alpha_of`), no rest and no flux; the reads derived once every row is read (`derived.with_reads`). The former declaration, the key `held` with `sources` (the form alone, the form and the tensions, the Wronskian, the form, the tensions and the flux), `level_weight`, `write_weight` and `rest`, kept by name."""
    sign = pair[0] == pair[1]
    return Row(name, pair, 1 + AXES, 1, False, sign, sign, 1, 1, 0, ())


def pair_of(value: object, label: str) -> tuple[int, int]:
    """A family's pair: [num, den] as the file writes it (den from 1, num from -den through den, |num| = den only as den itself, the massless pair; ALGEBRA.md); a pair derived from two bound records' pairs, {`relative_of` | `centre_of`: [a, b], `den`} by `composed_pair`, was read here until 2026-10-21 and is deleted 2026-10-21 with no world, its loader test, its no-root assertions and its two acts-table rows gone with it (ALGEBRA.md, The pair of two bound records, a hypothesis under its own name), so a dict is refused with the list's form."""
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{label} must be [num, den]")
    den = integer(value[1], f"{label}'s den", 1)
    num = integer(value[0], f"{label}'s num", -den, den)
    if abs(num) == den and num != den:
        raise ValueError(f"{label} [{num}, {den}]: a massive pair has den above |num| (ALGEBRA.md)")
    return num, den


def universe_of(document: object) -> tuple[dict[str, int], tuple[FamilyRule, ...]]:
    """The universe file: its integers (the key `width` refused by name with the derivation that replaced it, `GONE_INTEGERS`, 2026-10-24) and its families, each row its name, its pair and, for a family of quanta, its dimension (`shape_of`); a row without a dimension is a holder, its kind, its lines, its sources and its weights derived from its pair (`holder_of`), and every row's reads derived from the rows (`derived.with_reads`): nothing declared beyond the name, the pair and the dimension (the owner's word of 2026-10-24, no declarations; the keys `reads` and `held` with `sources`, `level_weight`, `write_weight` and `rest` refused by name with the derivation that replaced each, `gone_refused`; the keys `senses` and `exchange` refused as unknown since 2026-10-24, the owner's word: no parameters); the sign holder's alpha, the ratio of the file's E_h T to Gamma, carried inside its one write (`derived.alpha_of`)."""
    universe = keyed(document, "the universe file", UNIVERSE_KEYS, UNIVERSE_KEYS)
    if isinstance(universe["integers"], dict):
        for key in GONE_INTEGERS:
            if key in universe["integers"]:
                raise ValueError(
                    f"integers holds the key {key!r}, an integer of the engine and not of the universe: "
                    f"{GONE_INTEGERS[key]}"
                )
    raw = keyed(universe["integers"], "integers", INTEGER_KEYS, INTEGER_KEYS)
    integers = {key: integer(value, f"integers.{key}", 1) for key, value in raw.items()}
    unit = integers["link_unit"]
    if unit & (unit - 1):
        raise ValueError(
            f"integers.link_unit must be a power of two, the Link's unit G in which each Link's factor is one "
            f"integer (ALGEBRA.md #the-paces, The clock is the Node's, the tension is the Link's), got {unit}"
        )
    entries = universe["families"]
    if not isinstance(entries, list) or not entries:
        raise ValueError("families must be a list of the families' rows")
    rows: list[Row] = []
    for index, entry in enumerate(entries):
        label = f"families[{index}]"
        named = isinstance(entry, dict) and isinstance(entry.get("name"), str)
        gone_refused(entry, f"{label} ({entry['name']!r})" if named else label)
        row = keyed(entry, label, FAMILY_KEYS, FAMILY_REQUIRED)
        name = row["name"]
        if not isinstance(name, str) or not name or name in [found.name for found in rows]:
            raise ValueError(f"{label}.name must be a name of its own")
        label = f"{label} ({name!r})"
        pair = pair_of(row["pair"], f"{label}.pair")
        if "dimension" not in row:
            rows.append(holder_of(name, pair))
            continue
        lines, parts, plane = shape_of(row, label)
        rows.append(Row(name, pair, lines, parts, plane, False, False, None, None, 0, ()))
    families = derived.family_rules(derived.with_reads(rows))
    # the law's alpha inside the sign holder's write (the owner's law of one Node, 2026-10-23): the numerator times
    # E_h T and the walls times Gamma, in place of a write weight of the file
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
    return integers, families
