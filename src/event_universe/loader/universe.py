"""The universe file: its two keys, the four integers and the families' rows read into the loader's rows (`universe_of`, the energy line gated on the file's integers), each family's shape from its row (`shape_of`) and the key tables of the file (ENGINE.md section 4; ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from typing import Any

from event_universe.core.integer import MAX_WORK_INT
from event_universe.loader import derived
from event_universe.loader.derived import FamilyRule, Row
from event_universe.loader.keys import integer, keyed, reads_of

UNIVERSE_KEYS = ("integers", "families")
INTEGER_KEYS = ("node_clock", "quantum_action", "width", "link_unit")
FAMILY_KEYS, FAMILY_REQUIRED, HELD_KEYS, HELD_REQUIRED = (
    ("name", "pair", "dimension", "held", "reads"),
    ("name", "pair"),
    ("sources", "level_weight", "write_weight", "rest", "act"),
    ("sources", "level_weight", "write_weight"),
)
FORM, TENSIONS, WRONSKIAN = (
    "form",
    "tensions",
    "wronskian",
)  # what sources a held row: one real line each
SOURCES = ((FORM,), (FORM, TENSIONS), (WRONSKIAN,))  # the lists a held row may declare, in this order
PACE, ROTATION = (
    "pace",
    "rotation",
)  # how a held row acts on its readers: its level into their paces, or the turn of the two-part record
ACTS = (PACE, ROTATION)
PLANE = 2  # the dimension of a plane, re and im (charged matter), the one dimension with a Wronskian and a turn; every other dimension is real lines, 1 one line, 3 a vector under the cube's 48


def shape_of(row: dict[str, Any], label: str) -> tuple[int, int, bool, bool, bool]:
    """A family's shape from its row, (lines, parts, plane, wronskian, rotation): a family of quanta declares its `dimension`, any integer from 1, the lines of its record, each stepped by Rule3 as every line is, the form and the share the sum over them (1 one real line; 2 a plane, re and im, the one dimension with a Wronskian and a turn, `PLANE`; 3 three real lines, a vector under the cube's 48, no turn and no row of the sign; a dimension below 1 refused by name and no other refused by number), or its shape [parts, dimension], parts records of that dimension laid as one event and never summed at a Node (the pair family [2, 1], two real lines; ALGEBRA.md #a-familys-declaration, the dimension's table), and nothing of what sources it; a held row declares its `sources`, the form alone, the form and the tensions, or the Wronskian (one real line per source: 1, 1 + 3 or 1 lines), no dimension, a held row never being a plane, and optionally its `act` on its readers (`ACTS`): the plain read into their paces, every holder's without the key, or the rotation of the two-part record, the holder of the sign's alone (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record), under which the holder carries three odd axis lines beside its time line (1 + 3 lines); a holder of the content asking the rotation, and an act by another word, are refused by name."""
    if "held" in row:
        if "dimension" in row:
            raise ValueError(
                f"{label} is a held row and declares no dimension: its shape is its sources' count"
            )
        held = keyed(row["held"], f"{label}.held", HELD_KEYS, HELD_REQUIRED)
        sources, act = held["sources"], held.get("act", PACE)
        if not isinstance(sources, list) or tuple(sources) not in SOURCES:
            raise ValueError(
                f"{label}.held.sources is one of {[list(s) for s in SOURCES]}, got {sources!r}"
            )
        if act not in ACTS:
            raise ValueError(f"{label}.held.act is one of {list(ACTS)}, got {act!r}")
        rotation = act == ROTATION
        if rotation and WRONSKIAN not in sources:
            raise ValueError(
                f"{label}.held.act {act!r}: a holder of the content, sourced by the form, acts on its readers' "
                "paces; the rotation of the two-part record is the act of the holder of the sign, sourced by "
                "the Wronskian (ALGEBRA.md #the-hypotheses-under-their-own-names)"
            )
        return 1 + 3 * (TENSIONS in sources or rotation), 1, False, WRONSKIAN in sources, rotation
    if "dimension" not in row:
        raise ValueError(
            f"{label} lacks the key 'dimension': a family of quanta declares an integer from 1 or [parts, dimension]"
        )
    shape = row["dimension"]
    if isinstance(shape, list) and len(shape) != 2:
        raise ValueError(f"{label}.dimension as a shape is [parts, dimension], got {shape!r}")
    parts, lines = shape if isinstance(shape, list) else [1, shape]
    parts = integer(parts, f"{label}.dimension's parts", 1)
    lines = integer(lines, f"{label}.dimension", 1)
    return parts * lines, parts, lines == PLANE, False, False


def universe_of(document: object) -> tuple[dict[str, int], tuple[FamilyRule, ...]]:
    """The universe file: its integers and its families, each row its name, its pair, its reads (`reads_of`: the holders it reads by name at their weights, required, empty where it reads none) and its dimension (a family of quanta) or its sources with its level weight, its write weight, its rest and its act (a held row; the level weight `level_weight`, the quanta of form that write one level of the row; the write weight `write_weight`, the signed multiplier of its one write per line, the sign holder's k_w; the vacuum content `rest`, the level at which the massless row holding the content rests everywhere, an integer from 0 within the width; refused by name on the holder of the sign and on a row with a gap, which has no constant rest, ALGEBRA.md #what-is-open, item 22; the act `act`, `shape_of`), everything else derived by the rule from the pair and the shape, no read and no weight among it; the energy line gated on the file's integers (`derived.energy_line`)."""
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
        pair = row["pair"]
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError(f"{label}.pair must be [num, den]")
        den = integer(pair[1], f"{label}.pair's den", 1)
        num = integer(pair[0], f"{label}.pair's num", -den, den)
        if abs(num) == den and num != den:
            raise ValueError(
                f"{label}.pair [{num}, {den}]: a massive pair has den above |num| (ALGEBRA.md)"
            )
        lines, parts, plane, wronskian, rotation = shape_of(row, label)
        weight, writes, rest = None, None, 0
        if "held" in row:
            holds = row["held"]
            weight = integer(holds["level_weight"], f"{label}.held.level_weight", 1)
            writes = integer(holds["write_weight"], f"{label}.held.write_weight", -MAX_WORK_INT)
            if "rest" in holds:
                if wronskian or num != den:
                    raise ValueError(
                        f"{label}.held.rest: only the massless row of the content rests at a level"
                    )
                rest = integer(
                    holds["rest"], f"{label}.held.rest", 0, derived.largest_of(integers["width"])
                )
        rows.append(
            Row(name, (num, den), lines, parts, plane, wronskian, rotation, weight, writes, rest, reads)
        )
    families = derived.family_rules(rows)
    derived.energy_line(families, integers["node_clock"], integers["quantum_action"])
    return integers, families
