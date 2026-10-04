"""The universe file: its two keys, the four integers and the families' rows read into the loader's rows (`universe_of`, the energy line gated on the file's integers), each family's shape from its row (`shape_of`) and the key tables of the file (ENGINE.md section 4; ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import division_fixed_point, division_forward
from event_universe.loader import derived
from event_universe.loader.derived import KINDS, PLANE, PLANE_LINE, FamilyRule, Row
from event_universe.loader.keys import integer, keyed, reads_of

UNIVERSE_KEYS = ("integers", "families")
INTEGER_KEYS = ("node_clock", "quantum_action", "width", "link_unit")
FAMILY_KEYS, FAMILY_REQUIRED, HELD_KEYS, HELD_REQUIRED = (
    ("name", "pair", "dimension", "held", "reads"),
    ("name", "pair"),
    ("sources", "level_weight", "write_weight", "rest", "act"),
    ("sources", "level_weight", "write_weight", "act"),
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


def shape_of(row: dict[str, Any], label: str) -> tuple[int, int, bool, bool, bool]:
    """A family's shape from its row, (lines, parts, plane, wronskian, rotation): a family of quanta declares its `dimension`, any integer from 1, the lines of its record, each stepped by Rule3 as every line is, the form and the share the sum over them (1 one real line; 2 a plane, re and im, the one dimension with a Wronskian and a turn, `PLANE`; 3 three real lines, each stepped as a line of dimension one, no turn and no row of the sign; a dimension below 1 refused by name and no other refused by number), or its shape [parts, dimension], parts records of that dimension laid as one event and never summed at a Node (the pair family [2, 1], two real lines; ALGEBRA.md #a-familys-declaration, the dimension's table), or the shape by name, a list of its lines' kinds, `real` or `plane` (`KINDS`; the two hands: 1 and 2 kept as spellings, ["plane", "plane", "plane"] a record of three planes, one Wronskian per plane summed into its row, the proton's row; a record of real lines and planes together refused by name, not built), and nothing of what sources it; a held row declares its `sources`, the form alone, the form and the tensions, or the Wronskian (one real line per source: 1, 1 + 3 or 1 lines), no dimension, a held row never being a plane, and optionally its `act` on its readers (`ACTS`): the plain read into their paces, every holder's without the key, or the rotation of the two-part record, the holder of the sign's alone (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record), under which the holder carries three odd axis lines beside its time line (1 + 3 lines); a holder of the content asking the rotation, and an act by another word, are refused by name."""
    if "held" in row:
        if "dimension" in row:
            raise ValueError(
                f"{label} is a held row and declares no dimension: its shape is its sources' count"
            )
        held = keyed(row["held"], f"{label}.held", HELD_KEYS, HELD_REQUIRED)
        sources, act = held["sources"], held["act"]  # required: the file states the row's act
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


def composed_pair(
    first: tuple[int, int], second: tuple[int, int], den: int, relative: bool
) -> tuple[int, int]:
    """The pair of the relative part or of the centre's part of two bound records (ALGEBRA.md, the pair of two bound records, a hypothesis under its own name; the two hands): a bound record's inertia is m* = 3 tan omega_0, the band's curvature at rest, so the centre's part has tan omega_M = tan omega_1 + tan omega_2 and the relative part tan omega_mu = tan omega_1 tan omega_2 / (tan omega_1 + tan omega_2), the slow limit's own separation of the two-body problem; in the files' integers at the scale K = (den den_1 den_2)^2: s_i = isqrt(K^2 (den_i^2 - num_i^2)) div den_i is K sin omega_i and c_i = K num_i div den_i is K cos omega_i, Q = s_1 c_2 + s_2 c_1, so the relative part's cosine is Q / sqrt(Q^2 + (s_1 s_2)^2) and the centre's c_1 c_2 / sqrt((c_1 c_2)^2 + Q^2), and the pair's num is the nearest integer to den times that cosine by the division act, (2 den a + r) div (2 r) with r the fixed point of a^2 + b^2; the declared den is the family's own integer (The matter pair's den is the family's own integer). Two [2, 3] records at den 6,000 give the relative part [5237, 6000] and the centre [2449, 6000] (tools/derivations/two_body.py, the floats' 5,237.2 and 2,449.5 the second method)."""
    (num_1, den_1), (num_2, den_2) = first, second
    scale = (den * den_1 * den_2) ** 2
    sine_1 = int(
        division_forward(
            division_fixed_point(scale * scale * (den_1 * den_1 - num_1 * num_1)), den_1, 0
        )[0]
    )
    sine_2 = int(
        division_forward(
            division_fixed_point(scale * scale * (den_2 * den_2 - num_2 * num_2)), den_2, 0
        )[0]
    )
    cosine_1 = int(division_forward(scale * num_1, den_1, 0)[0])
    cosine_2 = int(division_forward(scale * num_2, den_2, 0)[0])
    summed = sine_1 * cosine_2 + sine_2 * cosine_1  # the tangents' sum at the scale squared
    along, across = (summed, sine_1 * sine_2) if relative else (cosine_1 * cosine_2, summed)
    root = division_fixed_point(along * along + across * across)
    return int(division_forward(2 * den * along + root, 2 * root, 0)[0]), den


PAIR_KEYS = ("relative_of", "centre_of", "den")  # a pair derived from two bound records' pairs


def pair_of(value: object, label: str, rows: Sequence[Row]) -> tuple[int, int]:
    """A family's pair: [num, den] as the file writes it (den from 1, num from -den through den, |num| = den only as den itself, the massless pair; ALGEBRA.md), or a pair derived from two bound records' pairs, {`relative_of`: [a, b], `den`} the relative part's and {`centre_of`: [a, b], `den`} the centre's part's, by `derived.composed_pair` at the declared den (ALGEBRA.md, the pair of two bound records, a hypothesis under its own name); the two named families are rows declared before this one with a massive pair of positive num (0 < num < den: a record with an inertia; a massless family or a family of no positive rest has none), refused by name otherwise, as is a pair naming both parts or neither."""
    if isinstance(value, dict):
        given = keyed(value, label, PAIR_KEYS, ("den",))
        parts = [key for key in ("relative_of", "centre_of") if key in given]
        if len(parts) != 1:
            raise ValueError(f"{label} names relative_of or centre_of, one of the two parts")
        names = given[parts[0]]
        if not isinstance(names, list) or len(names) != 2 or not all(isinstance(n, str) for n in names):
            raise ValueError(f"{label}.{parts[0]} must name two families, [a, b]")
        den = integer(given["den"], f"{label}.den", 1)
        found = []
        for name in names:
            row = next((r for r in rows if r.name == name), None)
            if row is None:
                raise ValueError(f"{label}.{parts[0]} names {name!r}, no family declared before it")
            if not 0 < row.pair[0] < row.pair[1]:
                raise ValueError(
                    f"{label}.{parts[0]} names {name!r} with the pair {list(row.pair)}: a bound record has a "
                    "massive pair of positive num, the inertia 3 tan omega_0; a massless family has none"
                )
            found.append(row.pair)
        return composed_pair(found[0], found[1], den, parts[0] == "relative_of")
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{label} must be [num, den], or {{relative_of | centre_of: [a, b], den}}")
    den = integer(value[1], f"{label}'s den", 1)
    num = integer(value[0], f"{label}'s num", -den, den)
    if abs(num) == den and num != den:
        raise ValueError(f"{label} [{num}, {den}]: a massive pair has den above |num| (ALGEBRA.md)")
    return num, den


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
        num, den = pair_of(row["pair"], f"{label}.pair", rows)
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
