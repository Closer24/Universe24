"""The universe file: its two keys, the four integers and the families' rows read into the loader's rows (`universe_of`, the energy line gated on the file's integers), each family's shape from its row (`shape_of`) and the key tables of the file (ENGINE.md section 4; ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from event_universe import conversion
from event_universe.core.integer import MAX_WORK_INT
from event_universe.loader import derived
from event_universe.loader.derived import KINDS, PLANE, PLANE_LINE, FamilyRule, Row
from event_universe.loader.keys import integer, keyed, reads_of

UNIVERSE_KEYS = ("integers", "families")
INTEGER_KEYS = ("node_clock", "quantum_action", "width", "link_unit")
FAMILY_KEYS, FAMILY_REQUIRED, HELD_KEYS, HELD_REQUIRED = (
    ("name", "pair", "dimension", "held", "reads", "exchange", "senses"),
    ("name", "pair"),
    ("sources", "level_weight", "write_weight", "rest"),
    ("sources", "level_weight"),
)  # `write_weight` required on a holder of the content and refused by name on the holder of the sign (alpha_of)
ONE_NODE_HELD = {
    "act": "the holder of the sign acts by the rotation of the two-part record and every holder of the content "
    "by the plain read into its readers' paces",
    "form": "every held row is booked with the positive form, each line its own real line",
    "booking": "every count source is booked once, the form's own clock",
    "factor": "every write's factor is carried inside the one division at the wall fixed per Node",
    "pressure": "the stress's trace enters the time line and the tension lines take the traceless parts, in the "
    "write and in the step",
}  # the switches of a held row fixed to one value for every world (the law of one Node, 2026-10-22)


def one_node_held(held: object, label: str) -> None:
    """The law of one Node (the owner's word of 2026-10-22: in nature there is one Node, whose acts are the same in every world, and no key switches what a Node does from world to world): a held row that names one of the former switches `act`, `form`, `booking`, `factor` or `pressure`, or the word `shear` among its sources, is refused by name with the one value the engine holds for every world; the universe file declares the row's content alone, its sources, its level weight, its write weight and its rest."""
    if not isinstance(held, dict):
        return
    for key, value in ONE_NODE_HELD.items():
        if key in held:
            raise ValueError(
                f"{label}.{key} is declared ({held[key]!r}): under the law of one Node no key switches what a "
                f"Node does, and {value} in every world (ALGEBRA.md, The hypotheses under their own names; the "
                "owner's word of 2026-10-22); drop the key"
            )
    sources = held.get("sources")
    if isinstance(sources, list) and sources == [WRONSKIAN] and "write_weight" in held:
        raise ValueError(
            f"{label}.write_weight is declared ({held['write_weight']!r}) on the holder of the sign: under the "
            "law of one Node the law's alpha is the ratio of the file's E_h T num to Gamma den, carried inside the "
            "holder's one write (the numerator times E_h T num, the wall times Gamma den, the remainder keeping the "
            "fraction), and no file names the sign holder's write weight (ALGEBRA.md, The constants, the proposal "
            "of 2026-10-23); drop the key"
        )
    if isinstance(sources, list) and sources != [WRONSKIAN] and "write_weight" not in held:
        raise ValueError(
            f"{label} lacks the key 'write_weight': a holder of the content declares its write weight"
        )
    if isinstance(sources, list) and OFF_DIAGONAL in sources:
        raise ValueError(
            f"{label}.sources {sources!r} names the shear: under the law of one Node a holder of the content "
            "carries its time line and its tension lines and no off-diagonal line in every world (the law as "
            "written; the shear a hypothesis under its own name against a decision, ALGEBRA.md); drop the word"
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
)  # the lists a held row may declare, in this order (the shear's two lists refused by name, one_node_held)
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
        one_node_held(row["held"], f"{label}.held")  # the former switches refused by name
        held = keyed(row["held"], f"{label}.held", HELD_KEYS, HELD_REQUIRED)
        sources = held["sources"]
        if not isinstance(sources, list) or tuple(sources) not in SOURCES:
            raise ValueError(
                f"{label}.held.sources is one of {[list(s) for s in SOURCES]}, got {sources!r}"
            )
        rotation = WRONSKIAN in sources  # the one Node: the holder of the sign acts by the rotation
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
    """Under the law of one Node every held row is booked with the positive form (the law as written), the key `form` refused by name by `one_node_held` before this function; kept as the one place the form is named. The old reading, kept by name: a held row's form, the optional key `form` of its `held` key (ALGEBRA.md, The odd line's source is the sign's own current, the covector form declared on 2026-10-21; covector.py): `positive`, each line its own real line with a positive form, the rows as the engine books them where the key is absent, or `lorentz`, the time line with its three odd lines booked as one covector with the Lorentz form, its odd lines sourced by the Link's own flux at light's pairing and the time line's entry negative in every reading of the record; declared on the holder of the sign under the rotation, massless, and refused by name on a row without odd lines, on a holder with a gap (one massless line propagates the lattice Lorenz constraint, 3 (L_0(t) - L_0(t - 1)) + SUM_a (L_a(i) - L_a(i - a)) = 0, and a gapped line does not) and on the content's holder carrying the flux's odd lines, whose covector form is stated and not built; any other word refused by name."""
    if "held" not in row or "form" not in row["held"]:
        return False
    form = row["held"]["form"]  # unreachable through the loader (one_node_held); the old gate kept
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


BOOKINGS = (
    "count",
    "form",
)  # a held row's booking of its count sources: the law's two proper-interval powers, or one, the form's own clock


def booking_of(row: dict[str, Any], label: str, wronskian: bool) -> bool:
    """The held row's optional key `booking`, the form's own clock (ALGEBRA.md, The write per proper volume and per proper interval; The form's own clock, a hypothesis under its own name, 2026-10-22, the eras hand's derivation and the kinematics hand's measurement read cold by the reader): `count`, the law as written, a count source's form booked per proper volume and per proper interval twice, N^2 / h^3, "twice for a second-order line"; or `form`, the form D = A^2 sin^2 omega' carrying one N of its own as the Wronskian W = A^2 sin omega' does (A^2 sin omega' the adiabatic invariant of Rule3's area-preserving step, sin omega' = N sin omega_proper to first order in the gap), so that the count's write is booked once, N / h^3 = p_x p_y p_z / (p_0^2 Gamma), one rule for both sources, under which a massive record at a small gap dims as e^(-5 U) and the massless pair as e^(-6 U) in the board's interval, nature's dust and radiation; the one change is the power on the count source's factor, 2 to 1, chosen by `FamilyRule.power` and read by the write (records.write_sources), the start's rest (features/start) and the width's gate (loader/rooms.py), the inverse recomputing the same factor; refused by name on the holder of the sign, whose Wronskian carries its one power already, and at any other word; False where absent (the law's booking)."""
    if "held" not in row or "booking" not in row["held"]:
        return False
    booking = row["held"]["booking"]
    if booking not in BOOKINGS:
        raise ValueError(f"{label}.held.booking is one of {list(BOOKINGS)}, got {booking!r}")
    if booking == BOOKINGS[1] and wronskian:
        raise ValueError(
            f"{label}.held.booking {booking!r}: the holder of the sign books its Wronskian with one "
            "proper-interval power already; the form's own clock is a count source's booking (ALGEBRA.md, "
            "The form's own clock)"
        )
    return bool(booking == BOOKINGS[1])


def held_word(row: dict[str, Any], label: str, key: str, words: tuple[str, str]) -> bool:
    """A held row's optional key of two words (`factor`, `pressure`): whether the second word stands, False where the key is absent, the first word the law as written; refused by name at any other word."""
    if "held" not in row or key not in row["held"]:
        return False
    word = row["held"][key]
    if word not in words:
        raise ValueError(f"{label}.held.{key} is one of {list(words)}, got {word!r}")
    return bool(word == words[1])


FACTORS = (
    "rounded",
    "carried",
)  # a held row's write factor: rounded once at the read, the law as written, or carried inside the one division


PRESSURES = (
    "tension",
    "trace",
)  # the stress's parts whole into the tension lines, the law as written, or their trace into the time line


def pressure_of(row: dict[str, Any], label: str, wronskian: bool) -> bool:
    """The held row's optional key `pressure`, the stress's trace (ALGEBRA.md, The stress's trace is the time line's, a hypothesis under its own name, 2026-10-22; the pressure hand's derivation of the pressure's write in the time line and the reader's build line on the second smoke): `tension`, the law as written, each Node's own stress parts -num h_a into the row's tension lines whole and the time line sourced by the forms alone; or `trace`, the trace over three of each source's stress parts entering the time line's write at the weight -1 in the energy's units ((p_a / Gamma)^2 / (3 den) per part, one rounding per source per Node, records.pressure_term) and the tension lines taking the traceless parts, 3 T_aa - SUM_b T_bb over three inside the factor's one rounding, so that no isotropic stress stretches the rulers (h N = 1: an isotropic ruler change without the clock's is no act of the law) and the tension lines' uniform mode on the wrapped board gets no source from a lay's mean stress, under which the volume's exponent is one integer for every mix, d + 1 (features/volume; the loader checks Gamma divides (d + 1) E_s T, derived.trace_wall); refused by name on the holder of the sign, whose rows carry no tension line, and at any other word; False where absent, the law as written, every shipped world bit for bit."""
    trace = held_word(row, label, "pressure", PRESSURES)
    if trace and wronskian:
        raise ValueError(
            f"{label}.held.pressure {PRESSURES[1]!r}: the holder of the sign carries no tension line and reads no "
            "stress; the trace is a row of the content's (ALGEBRA.md, The stress's trace is the time line's)"
        )
    return trace


def factor_of(row: dict[str, Any], label: str) -> bool:
    """The held row's optional key `factor`, the end's booking (ALGEBRA.md, The write per proper volume and per proper interval, the clause of 2026-10-22; the remainders hand's reading of the two roundings and the reader's line on the design): `rounded`, the law as written, the write's factor one rounding half up of the count times the three paces over the one wall before the write's carried division (paces.write_factor, kind D), under which a family's write at a Node is exactly 0 from the interval its dimmed form falls below one half of a level, the stop, the integers' end under the rounding, named and unreachable on every shipped width; or `carried`, the factor a coefficient of the numerator inside the held write's one carried division, Rule3's own manner (no coefficient of the law rounded apart; a fraction kept by a carried division and nothing else), the product count p_x p_y p_z over the wall E_s T times Gamma^power p_0^(3 - power) at the Node, the write's one remainder carrying it (paces.write_factor_terms, records.write_sources, node.held_write_at's walls per Node), injective (the reversibility hand's Theorem 1: the numerator and the wall from the paces of the interval's start, recovered from the post-state's before), under which no write dies and the velocity crawls and pulses where the constraint's falls below one level per interval, the coast; the row's sources sharing the clock (derived.shared_clock); refused by name at any other word; False where absent, the rounding, so that every shipped world runs bit for bit."""
    return held_word(row, label, "factor", FACTORS)


def universe_of(document: object) -> tuple[dict[str, int], tuple[FamilyRule, ...]]:
    """The universe file: its integers and its families, each row its name, its pair, its reads (`reads_of`: the holders it reads by name at their weights, required, empty where it reads none) and its dimension (a family of quanta; a real-line family optionally the senses of its plane records out, the key `senses`, the one residual declaration of The conversion, `conversion.declared`, 2026-10-21) or its sources with its level weight, its write weight, its rest and its act (a held row; a family of several parts optionally its sign under exchange, the key `exchange`, `exchange_of`, 2026-10-19; the level weight `level_weight`, the quanta of form that write one level of the row; the write weight `write_weight`, the signed multiplier of its one write per line, the sign holder's k_w; the vacuum content `rest`, the level at which the massless row holding the content rests everywhere, an integer from 0 within the width; refused by name on the holder of the sign and on a row with a gap, which has no constant rest, ALGEBRA.md #what-is-open, item 22; the act `act`, `shape_of`; the booking of its count sources `booking`, `booking_of`, the form's own clock under `form`), everything else derived by the rule from the pair and the shape, no read and no weight among it; the energy line gated on the file's integers (`derived.energy_line`)."""
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
    declaring: dict[
        int, object
    ] = {}  # the rows' `senses`, the lists derived once every pair is read (conversion.py)
    for index, entry in enumerate(entries):
        label = f"families[{index}]"
        if isinstance(entry, dict) and "converts" in entry:
            raise ValueError(
                f"{label} holds the key 'converts', deleted 2026-10-21 by the owner's word: the conversion's list is "
                "derived from the pairs under the law's conservations, and a real-line parent's plane records out "
                "take the senses of the row's key 'senses' (ALGEBRA.md, The conversion)"
            )
        row = keyed(entry, label, FAMILY_KEYS, FAMILY_REQUIRED)
        if "senses" in row:
            declaring[index] = row["senses"]
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
        off_diagonal = (
            "held" in row and OFF_DIAGONAL in row["held"]["sources"]
        )  # the row carries the shear lines
        exchange = exchange_of(row, label, parts)  # the record's sign under exchange, 0 undeclared
        lorentz = form_of(row, label, rotation, flux, num == den)  # the Lorentz form, False undeclared
        # the one Node (2026-10-22): the form's own clock on every count source, the carried factor on
        # every held row, the stress's trace on every holder of the content; no key of the file
        form_clock = not wronskian
        factor_carried = True
        pressure_trace = not wronskian
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
                form_clock=form_clock,
                factor_carried=factor_carried,
                pressure_trace=pressure_trace,
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
    return integers, conversion.declared(
        families, declaring
    )  # the lists from the pairs under the law's conservations, refused by name
