"""The universe file: its two keys, the four integers and the families' rows read into the loader's rows (`universe_of`, the energy line gated on the file's integers), each family's shape from its row (`shape_of`) and the key tables of the file (ENGINE.md section 4; ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from typing import Any

from event_universe.core.integer import MAX_WORK_INT
from event_universe.loader import derived
from event_universe.loader.derived import KINDS, PLANE, PLANE_LINE, FamilyRule, Row
from event_universe.loader.keys import integer, keyed, reads_of

UNIVERSE_KEYS = ("integers", "families")
INTEGER_KEYS = ("node_clock", "quantum_action", "width", "link_unit")
FAMILY_KEYS, FAMILY_REQUIRED, HELD_KEYS, HELD_REQUIRED = (
    ("name", "pair", "dimension", "held", "reads", "exchange"),
    ("name", "pair"),
    ("sources", "level_weight", "write_weight", "rest", "act", "form"),
    ("sources", "level_weight", "write_weight", "act"),
)
POSITIVE, LORENTZ = (
    "positive",
    "lorentz",
)  # a held row's form: each line its own real line with a positive form, or the time line with its three odd lines one covector with the Lorentz form (covector.py)
FORMS = (POSITIVE, LORENTZ)
FORM, TENSIONS, WRONSKIAN, FLUX, OFF_DIAGONAL = (
    "form",
    "tensions",
    "wronskian",
    "flux",
    "shear",
)  # what sources a held row: one real line each, the flux three odd lines, the shear three off-diagonal lines
SOURCES = (
    (FORM,),
    (FORM, TENSIONS),
    (WRONSKIAN,),
    (FORM, TENSIONS, FLUX),
    (FORM, TENSIONS, OFF_DIAGONAL),
    (FORM, TENSIONS, FLUX, OFF_DIAGONAL),
)  # the lists a held row may declare, in this order
PACE, ROTATION = (
    "pace",
    "rotation",
)  # how a held row acts on its readers: its level into their paces, or the turn of the two-part record
ACTS = (PACE, ROTATION)
EXCHANGE = {
    "antisymmetric": -1,
    "symmetric": 1,
}  # a family's sign under the exchange of two of its parts, the key `exchange` and its two words


def exchange_of(row: dict[str, Any], label: str, parts: int) -> int:
    """A family's sign under the exchange of two of its parts, the key `exchange` (ALGEBRA.md, Spin, closed for the paper as a route, The family's sign under exchange, 2026-10-19): `antisymmetric` -1 or `symmetric` 1, the family's declaration read by the first side's coefficients (`meeting_back.coefficients_of`, `credit.terms_of`) and the lists' factor (`lists.exchange_factor`) and by nothing at the Node; 0 where the key is absent, the lists and the credit as they stand, so that no world without the key changes; refused by name at any other value and on a family of one part, which has no second label to exchange."""
    if "exchange" not in row:
        return 0
    value = row["exchange"]
    if not isinstance(value, str) or value not in EXCHANGE:
        raise ValueError(f"{label}.exchange is one of {list(EXCHANGE)}, got {value!r}")
    if parts < 2:
        raise ValueError(
            f"{label}.exchange names a sign under the exchange of parts on a family of one part: no second "
            "label to exchange"
        )
    return EXCHANGE[value]


def shape_of(row: dict[str, Any], label: str) -> tuple[int, int, bool, bool, bool]:
    """A family's shape from its row, (lines, parts, plane, wronskian, rotation): a family of quanta declares its `dimension`, any integer from 1, the lines of its record, each stepped by Rule3 as every line is, the form and the share the sum over them (1 one real line; 2 a plane, re and im, the one dimension with a Wronskian and a turn, `PLANE`; 3 three real lines, each stepped as a line of dimension one, no turn and no row of the sign; a dimension below 1 refused by name and no other refused by number), or its shape [parts, dimension], parts records of that dimension laid as one event and never summed at a Node (the pair family [2, 1], two real lines; ALGEBRA.md #a-familys-declaration, the dimension's table), or the shape by name, a list of its lines' kinds, `real` or `plane` (`KINDS`; the two hands: 1 and 2 kept as spellings, ["plane", "plane", "plane"] a record of three planes, one Wronskian per plane summed into its row, the proton's row; a record of real lines and planes together refused by name, not built), and nothing of what sources it; a held row declares its `sources`, the form alone, the form and the tensions, or the Wronskian (one real line per source: 1, 1 + 3 or 1 lines), no dimension, a held row never being a plane, and optionally its `act` on its readers (`ACTS`): the plain read into their paces, every holder's without the key, or the rotation of the two-part record, the holder of the sign's alone (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record), under which the holder carries three odd axis lines beside its time line (1 + 3 lines); a holder of the content sourced by the form, the tensions and the flux carries three odd lines after its tension lines (1 + 3 + 3 lines), the count's flux through the axis's two Links written into them and read by every plane reading it as the odd part of the Link's read (ALGEBRA.md, The clock family on the Ports; plane.py); a holder of the content sourced by the form, the tensions and the shear (with or without the flux) carries three off-diagonal lines xy, yz, zx last in its row (1 + 3 + 3 or 1 + 3 + 3 + 3 lines), the product of the Node's two axis differences of its sources' records written into them over the doubled wall 2 E_s W_c and read by no record (the held rows' own wave sector, 2026-10-20), the shear without the tensions refused by name; a holder of the content asking the rotation, and an act by another word, are refused by name."""
    if "held" in row:
        if "dimension" in row:
            raise ValueError(
                f"{label} is a held row and declares no dimension: its shape is its sources' count"
            )
        held = keyed(row["held"], f"{label}.held", HELD_KEYS, HELD_REQUIRED)
        sources, act = held["sources"], held["act"]  # required: the file states the row's act
        if isinstance(sources, list) and OFF_DIAGONAL in sources and TENSIONS not in sources:
            raise ValueError(
                f"{label}.held.sources {sources!r} declares the shear without the tensions: the three "
                "off-diagonal parts xy, yz, zx stand beside the three diagonal parts xx, yy, zz of one stress, "
                "sourced by the same records' axis differences at the same wall, and a row without the "
                "tensions (a holder sourced by the form alone, or the holder of the sign) carries no shear"
            )
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
        odd = 3 * (FLUX in sources)  # the three odd lines of the count's flux after the tensions
        off = 3 * (OFF_DIAGONAL in sources)  # the three shear lines xy, yz, zx, the last of the row
        return (
            1 + 3 * (TENSIONS in sources or rotation) + odd + off,
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


def form_of(row: dict[str, Any], label: str, rotation: bool, flux: bool, massless: bool) -> bool:
    """A held row's form, the optional key `form` of its `held` key (ALGEBRA.md, The odd line's source is the sign's own current, the covector form declared on 2026-10-21; covector.py): `positive`, each line its own real line with a positive form, the rows as the engine books them where the key is absent, or `lorentz`, the time line with its three odd lines booked as one covector with the Lorentz form, its odd lines sourced by the Link's own flux at light's pairing and the time line's entry negative in every reading of the record; declared on the holder of the sign under the rotation, massless, and refused by name on a row without odd lines, on a holder with a gap (one massless line propagates the lattice Lorenz constraint, 3 (L_0(t) - L_0(t - 1)) + SUM_a (L_a(i) - L_a(i - a)) = 0, and a gapped line does not) and on the content's holder carrying the flux's odd lines, whose covector form is stated and not built; any other word refused by name."""
    if "held" not in row or "form" not in row["held"]:
        return False
    form = row["held"]["form"]
    if form not in FORMS:
        raise ValueError(f"{label}.held.form is one of {list(FORMS)}, got {form!r}")
    if form == POSITIVE:
        return False
    if not rotation:
        raise ValueError(
            f"{label}.held.form {form!r}: the Lorentz form books a time line with its three odd lines as one "
            "covector, the holder of the sign under the act 'rotation'"
            + (
                "; the content's holder carrying the flux's odd lines takes it in form only, stated and not built"
                if flux
                else ""
            )
        )
    if not massless:
        raise ValueError(
            f"{label}.held.form {form!r}: the four lines are one covector over one massless line, whose R / w = "
            "1 / 3 propagates the lattice Lorenz constraint; a holder with a gap is refused"
        )
    return True


def universe_of(document: object) -> tuple[dict[str, int], tuple[FamilyRule, ...]]:
    """The universe file: its integers and its families, each row its name, its pair, its reads (`reads_of`: the holders it reads by name at their weights, required, empty where it reads none) and its dimension (a family of quanta) or its sources with its level weight, its write weight, its rest and its act (a held row; a family of several parts optionally its sign under exchange, the key `exchange`, `exchange_of`, 2026-10-19; the level weight `level_weight`, the quanta of form that write one level of the row; the write weight `write_weight`, the signed multiplier of its one write per line, the sign holder's k_w; the vacuum content `rest`, the level at which the massless row holding the content rests everywhere, an integer from 0 within the width; refused by name on the holder of the sign and on a row with a gap, which has no constant rest, ALGEBRA.md #what-is-open, item 22; the act `act`, `shape_of`), everything else derived by the rule from the pair and the shape, no read and no weight among it; the energy line gated on the file's integers (`derived.energy_line`)."""
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
            writes = integer(holds["write_weight"], f"{label}.held.write_weight", -MAX_WORK_INT)
            if "rest" in holds:
                if wronskian or num != den:
                    raise ValueError(
                        f"{label}.held.rest: only the massless row of the content rests at a level"
                    )
                rest = integer(
                    holds["rest"], f"{label}.held.rest", 0, derived.largest_of(integers["width"])
                )
        flux = "held" in row and FLUX in row["held"]["sources"]  # the row carries the odd lines
        off_diagonal = (
            "held" in row and OFF_DIAGONAL in row["held"]["sources"]
        )  # the row carries the shear lines
        exchange = exchange_of(row, label, parts)  # the record's sign under exchange, 0 undeclared
        lorentz = form_of(row, label, rotation, flux, num == den)  # the Lorentz form, False undeclared
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
                exchange,
                off_diagonal,
                lorentz,
            )
        )
    families = derived.family_rules(rows)
    derived.energy_line(families, integers["node_clock"], integers["quantum_action"])
    return integers, families
