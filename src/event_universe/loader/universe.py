"""The universe file: its two keys, the four integers and the families' rows read into the loader's rows (`universe_of`, the energy line gated on the file's integers), each family's shape from its row (`shape_of`) and the key tables of the file (ENGINE.md section 4; ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from event_universe.core.integer import MAX_WORK_INT
from event_universe.loader import derived
from event_universe.loader.derived import KINDS, PLANE, PLANE_LINE, FamilyRule, Row
from event_universe.loader.keys import integer, keyed, reads_of

UNIVERSE_KEYS = ("integers", "families")
INTEGER_KEYS = ("node_clock", "quantum_action", "width", "link_unit")
FAMILY_KEYS, FAMILY_REQUIRED, HELD_KEYS, HELD_REQUIRED = (
    ("name", "pair", "dimension", "held", "reads"),
    ("name", "pair"),
    ("sources", "level_weight", "write_weight", "rest"),
    ("sources", "level_weight"),
)  # `write_weight` required on a holder of the content and refused by name on the holder of the sign (alpha_of)


def write_weight_rule(held: object, label: str) -> None:
    """The write weight's place (the owner's law of one Node, 2026-10-23): a holder of the content declares `write_weight`, the signed multiplier of its one write; the holder of the sign declares none, its alpha the ratio E_h T num / (Gamma den) carried inside its write (derived.alpha_of), and a file naming it there is refused."""
    if not isinstance(held, dict):
        return
    sources = held.get("sources")
    if isinstance(sources, list) and sources == [WRONSKIAN] and "write_weight" in held:
        raise ValueError(
            f"{label}.write_weight is declared ({held['write_weight']!r}) on the holder of the sign: the law's alpha "
            "is the ratio of the file's E_h T num to Gamma den, carried inside the holder's one write, and no file "
            "names the sign holder's write weight (ALGEBRA.md, The constants, the proposal of 2026-10-23); drop the key"
        )
    if isinstance(sources, list) and sources != [WRONSKIAN] and "write_weight" not in held:
        raise ValueError(
            f"{label} lacks the key 'write_weight': a holder of the content declares its write weight"
        )


FORM, TENSIONS, WRONSKIAN, FLUX = (
    "form",
    "tensions",
    "wronskian",
    "flux",
)  # what sources a held row: one real line each, the flux three odd lines
SOURCES = (
    (FORM,),
    (FORM, TENSIONS),
    (WRONSKIAN,),
    (FORM, TENSIONS, FLUX),
)  # the lists a held row may declare, in this order


def shape_of(row: dict[str, Any], label: str) -> tuple[int, int, bool, bool, bool]:
    """A family's shape from its row, (lines, parts, plane, wronskian, rotation): a family of quanta declares its `dimension`, any integer from 1, the lines of its record, each stepped by Rule3 as every line is, the form and the share the sum over them (1 one real line; 2 a plane, re and im, the one dimension with a Wronskian and a turn, `PLANE`; 3 three real lines, each stepped as a line of dimension one, no turn and no row of the sign; a dimension below 1 refused by name and no other refused by number), or its shape [parts, dimension], parts records of that dimension laid as one event and never summed at a Node (the pair family [2, 1], two real lines; ALGEBRA.md #a-familys-declaration, the dimension's table), or the shape by name, a list of its lines' kinds, `real` or `plane` (`KINDS`; the two hands: 1 and 2 kept as spellings, ["plane", "plane", "plane"] a record of three planes, one Wronskian per plane summed into its row, the proton's row; a record of real lines and planes together refused by name, not built), and nothing of what sources it; a held row declares its `sources`, the form alone, the form and the tensions, or the Wronskian (one real line per source: 1, 1 + 3 or 1 lines), no dimension, a held row never being a plane, and optionally its `act` on its readers (`ACTS`): the plain read into their paces, every holder's without the key, or the rotation of the two-part record, the holder of the sign's alone (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record), under which the holder carries three odd axis lines beside its time line (1 + 3 lines); a holder of the content sourced by the form, the tensions and the flux carries three odd lines after its tension lines (1 + 3 + 3 lines), the count's flux through the axis's two Links written into them and read by every plane reading it as the odd part of the Link's read (ALGEBRA.md, The clock family on the Ports; plane.py); a holder of the content sourced by the form, the tensions and the shear (with or without the flux) carries three off-diagonal lines xy, yz, zx last in its row (1 + 3 + 3 or 1 + 3 + 3 + 3 lines), the product of the Node's two axis differences of its sources' records written into them over the doubled wall 2 E_s W_c and read by no record (the held rows' own wave sector, 2026-10-20), the shear without the tensions refused by name; a holder of the content asking the rotation, and an act by another word, are refused by name."""
    if "held" in row:
        if "dimension" in row:
            raise ValueError(
                f"{label} is a held row and declares no dimension: its shape is its sources' count"
            )
        write_weight_rule(row["held"], f"{label}.held")
        held = keyed(row["held"], f"{label}.held", HELD_KEYS, HELD_REQUIRED)
        sources = held["sources"]
        if not isinstance(sources, list) or tuple(sources) not in SOURCES:
            raise ValueError(
                f"{label}.held.sources is one of {[list(s) for s in SOURCES]}, got {sources!r}"
            )
        rotation = WRONSKIAN in sources  # the one Node: the holder of the sign acts by the rotation
        odd = 3 * (FLUX in sources)  # the three odd lines of the count's flux after the tensions
        return (
            1 + 3 * (TENSIONS in sources or rotation) + odd,
            1,
            False,
            WRONSKIAN in sources,
            rotation,
        )
    if "dimension" not in row:
        raise ValueError(
            f"{label} lacks the key 'dimension': a family of quanta declares an integer from 1 or [parts, dimension]"
        )
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
        return len(shape) * (PLANE if plane else 1), 1, plane, False, False
    if isinstance(shape, list) and len(shape) != 2:
        raise ValueError(
            f"{label}.dimension as a shape is [parts, dimension] or a list of its lines' kinds, got {shape!r}"
        )
    parts, lines = shape if isinstance(shape, list) else [1, shape]
    parts = integer(parts, f"{label}.dimension's parts", 1)
    lines = integer(lines, f"{label}.dimension", 1)
    return parts * lines, parts, lines == PLANE, False, False


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
    """The universe file: its integers and its families, each row its name, its pair, its reads (`reads_of`: the holders it reads by name at their weights, required, empty where it reads none) and its dimension (a family of quanta) or its sources with its level weight, its write weight and its rest (a held row; the keys `senses`, the conversion's declared senses of 2026-10-21, and `exchange`, the sign under the exchange of parts of 2026-10-19, refused as unknown since 2026-10-24, the owner's word: no parameters; the level weight `level_weight`, the quanta of form that write one level of the row; the write weight `write_weight`, the signed multiplier of its one write per line, the sign holder's k_w; the vacuum content `rest`, the level at which the massless row holding the content rests everywhere, an integer from 0 within the width; refused by name on the holder of the sign and on a row with a gap, which has no constant rest, ALGEBRA.md #what-is-open, item 22; the act `act`, `shape_of`; the booking of its count sources `booking`, `booking_of`, the form's own clock under `form`), everything else derived by the rule from the pair and the shape, no read and no weight among it; the energy line gated on the file's integers (`derived.energy_line`)."""
    universe = keyed(document, "the universe file", UNIVERSE_KEYS, UNIVERSE_KEYS)
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
        row = keyed(entry, label, FAMILY_KEYS, FAMILY_REQUIRED)
        name = row["name"]
        if not isinstance(name, str) or not name or name in [found.name for found in rows]:
            raise ValueError(f"{label}.name must be a name of its own")
        label = f"{label} ({name!r})"
        if "reads" not in row:
            raise ValueError(
                f"{label} lacks the key 'reads': a family names the holders it reads, {{}} for none"
            )
        reads = reads_of(row["reads"], f"{label}.reads")
        num, den = pair_of(row["pair"], f"{label}.pair")
        lines, parts, plane, wronskian, rotation = shape_of(row, label)
        weight, writes, rest = None, None, 0
        if "held" in row:
            holds = row["held"]
            weight = integer(holds["level_weight"], f"{label}.held.level_weight", 1)
            writes = (
                1  # the holder of the sign: alpha set by the loader from the file's integers (derived.alpha_of)
                if wronskian
                else integer(holds["write_weight"], f"{label}.held.write_weight", -MAX_WORK_INT)
            )
            if "rest" in holds:
                if wronskian or num != den:
                    raise ValueError(
                        f"{label}.held.rest: only the massless row of the content rests at a level"
                    )
                rest = integer(
                    holds["rest"], f"{label}.held.rest", 0, derived.largest_of(integers["width"])
                )
        flux = "held" in row and FLUX in row["held"]["sources"]  # the row carries the odd lines
        rows.append(
            Row(
                name,
                (num, den),
                lines,
                parts,
                plane,
                wronskian,
                rotation,
                weight,
                writes,
                rest,
                reads,
                1,
                flux,
            )
        )
    families = derived.family_rules(rows)
    # the law's alpha inside the sign holder's write (the owner's law of one Node, 2026-10-23): the numerator times
    # E_h T num and the walls times Gamma den, in place of the file's write weight and the loader's energy line
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
    # the trace's wall Gamma | (d + 1) E_s T is no gate of the volume form: the hill's weight K was the level form's integer (the one Node, 2026-10-23; derived.trace_wall kept by name, called by nothing)
    return integers, families
