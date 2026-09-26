"""Commit 1 of the one stroke (ALGEBRA.md 9.91 (10) 1; 9.86 (2), (3); 9.85 (3)): the loader."""

from pathlib import Path

p = Path("wt_ec/src/event_universe/events/world.py")
s = p.read_text()


def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:90])
    s = s.replace(old, new)


# ---- 1. the family keys admitted on an inline entry
rep(
    """    "pair",
    "faces",
    # THE FAMILY GENERICITY (record 2066; BUILD.md section 26 item 51): what
""",
    """    "pair",
    "faces",
    # THE REPRESENTATION AS A LIST OF PARTS and the rest of the complete
    # attribute set (ALGEBRA.md 9.86 (3), 9.91 (7); the one stroke, commit 1):
    # `parts`, `levels`, `self_unit`, `clicks`, and the held source's
    # `held_factors`, `held_dipole`, `held_dipole_div`; the families file's
    # entries translate to these, an inline list may declare them
    "parts",
    "levels",
    "self_unit",
    "clicks",
    "held_factors",
    "held_dipole",
    "held_dipole_div",
    # THE FAMILY GENERICITY (record 2066; BUILD.md section 26 item 51): what
""",
)

# ---- 2. the file's constants
rep(
    """FAMILIES_INTEGERS = {"node_clock", "amplitude_bound"}
FAMILY_ENTRY_KEYS = {
    "name",
    "quantum",
    "charge",
    "pair",
    "reads",
    "representation",
    "phase",
    "self_unit",
    "booked",
    "held",
    "clicks",
}
FAMILY_ENTRY_REQUIRED = {
    "name",
    "quantum",
    "charge",
    "pair",
    "reads",
    "representation",
    "phase",
    "self_unit",
    "booked",
}
REPRESENTATIONS = ("scalar",)
HELD_COUNTS = ("content", "sign")
""",
    """# THE UNIVERSE'S INTEGERS (ALGEBRA.md 9.83 (2) (a), 9.91 (7)): Gamma, A, and Lambda
# (the charge's read weight, the word "Lambda" on a read); the energy unit
# P_0, the twist Lambda_v, the accumulator wall W and the twist table enter
# with the operations that read them (9.91 (10) commits 4 to 6)
FAMILIES_INTEGERS = {"node_clock", "amplitude_bound", "charge_weight"}
# THE ENTRY, the complete attribute set (ALGEBRA.md 9.79 (1), 9.86 (3), 9.91
# (7)): name; parts (the representation as a list of parts, [1] a scalar, [1,
# 3] a vector with its time part, [1, 3, 6] the symmetric tensor over the
# four directions); phase (1 or 2, the levels at a Node); pair ([num, den], or
# "body" for the family whose pair every body and record declares); held
# {count, factors, dipole, dipole_div} (a field family: the body's writes);
# reads [{family, weight, twist, by}]; self_source {unit}; clicks {gives,
# takes, quantum} (a family of records). `booked` is derived: true exactly
# for a family with clicks (item 53).
FAMILY_ENTRY_KEYS = {"name", "parts", "phase", "pair", "held", "reads", "self_source", "clicks"}
FAMILY_ENTRY_REQUIRED = {"name", "parts", "phase", "pair", "reads", "self_source"}
PARTS_FORMS = ((1,), (1, 3), (1, 3, 6))
HELD_COUNTS = ("content", "sign")
HELD_DIPOLES = ("spin", "moment")
# a read's weight may be the universe's word (the file's integer by name)
READ_WEIGHT_WORDS = {"Lambda": "charge_weight"}
# a read's twist (ALGEBRA.md 9.81 (2), 9.91 (6)): an integer, "own" (the
# reading record's own rotation) or "Lambda_v" (the charge's twist, the
# universe's integer once the transport reads it; commit 4)
READ_TWIST_WORDS = ("own", "Lambda_v")
READ_BY_WORDS = {1: "plain", "q": "sign", "plain": "plain", "sign": "sign"}
""",
)

# ---- 3. the file reader
start = s.index("def families_file_entries(value: str)")
end = s.index("# THE ENGINE START FILE (record 2089;")
new_reader = '''def families_file_entries(value: str) -> tuple[list[dict[str, object]], dict[str, int]]:
    """The families file read and translated to the families list the parse
    reads (item 51's attributes and the one stroke's, ALGEBRA.md 9.91 (7)),
    with the universe's integers; every key required and refused by name.
    THE TRANSLATION: `parts` as declared; `phase` to `levels`; `pair` [num,
    den] or "body"; `held` {count, factors, dipole, dipole_div} to `held`
    (the count word), `held_factors`, `held_dipole`, `held_dipole_div`;
    `reads` with the weight word resolved to the universe's integer, `by` 1
    or "q" to the loader's words, `twist` kept; `self_source.unit` to
    `self_unit`; `clicks` to `clicks` with the quantum, `quantum` 1 on a
    family without clicks (a held family, one click one unit); `charge` 0
    on every family (a body's charge is the body's number, 9.91 (7); the
    hold writes it, commit 2)."""
    path = REPOSITORY_ROOT / value
    if not path.is_file():
        raise ValueError(f"{BEAM_LAW}: families names {value!r}, no file at the repository's root")
    document = json.loads(path.read_text(encoding="utf-8"))
    label = f"the families file {value!r}"
    if not isinstance(document, dict):
        raise ValueError(f"{BEAM_LAW}: {label} must be a JSON object")
    unknown = set(document) - FAMILIES_FILE_KEYS
    if unknown:
        raise ValueError(f"{BEAM_LAW}: {label} has unknown keys: {', '.join(sorted(unknown))}")
    missing = FAMILIES_FILE_KEYS - set(document)
    if missing:
        raise ValueError(f"{BEAM_LAW}: {label} lacks keys: {', '.join(sorted(missing))}")
    if document["law"] != DETECTOR_LAW_RULE:
        raise ValueError(
            f"{BEAM_LAW}: {label} declares law {document['law']!r}, not {DETECTOR_LAW_RULE!r}"
        )
    integers = document["integers"]
    if not isinstance(integers, dict) or set(integers) != FAMILIES_INTEGERS:
        raise ValueError(
            f"{BEAM_LAW}: {label}.integers must hold exactly {sorted(FAMILIES_INTEGERS)} (the "
            "universe's integers, ALGEBRA.md 9.83 (2) (a), 9.91 (7); no default)"
        )
    universe = {
        key: _integer(integers[key], f"{label}.integers.{key}", 1, AMOUNT_BOUND)
        for key in sorted(FAMILIES_INTEGERS)
    }
    entries = document["families"]
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{BEAM_LAW}: {label}.families must be a nonempty list")
    translated: list[dict[str, object]] = []
    for index, entry in enumerate(entries):
        where = f"{label}.families[{index}]"
        obj = _object(entry, where, FAMILY_ENTRY_KEYS, FAMILY_ENTRY_REQUIRED)
        parts = obj["parts"]
        if not isinstance(parts, list) or tuple(parts) not in PARTS_FORMS:
            raise ValueError(
                f"{BEAM_LAW}: {where}.parts must be one of {[list(form) for form in PARTS_FORMS]}: "
                "the representation as a list of parts, the time part first (ALGEBRA.md 9.86 (2), "
                "9.91 (1))"
            )
        if obj["phase"] not in (1, 2):
            raise ValueError(
                f"{BEAM_LAW}: {where}.phase must be 1 or 2, the levels at a Node (ALGEBRA.md 9.91 (1))"
            )
        self_source = _object(obj["self_source"], f"{where}.self_source", {"unit"}, {"unit"})
        if self_source["unit"] != 0:
            raise ValueError(
                f"{BEAM_LAW}: {where}.self_source.unit must be 0: the self-source (ALGEBRA.md 9.78 "
                "(3), 9.91 (5)) is not built"
            )
        pair_value = obj["pair"]
        if pair_value != "body" and not (
            isinstance(pair_value, list)
            and len(pair_value) == 2
            and all(type(item) is int and item >= 1 for item in pair_value)
        ):
            raise ValueError(
                f"{BEAM_LAW}: {where}.pair must be [num, den] or the word \\"body\\" (every body and "
                "record of the family declares its own pair; ALGEBRA.md 9.85 (3), 9.91 (7))"
            )
        if "held" not in obj and "clicks" not in obj:
            raise ValueError(
                f"{BEAM_LAW}: {where} declares neither held (a field family) nor clicks (a family "
                "of records): a family does one or both (ALGEBRA.md 9.86 (2))"
            )
        legacy: dict[str, object] = {
            "name": obj["name"],
            "charge": 0,
            "pair": pair_value,
            "parts": list(parts),
            "levels": obj["phase"],
            "self_unit": 0,
        }
        reads: list[dict[str, object]] = []
        raw_reads = obj["reads"]
        if not isinstance(raw_reads, list):
            raise ValueError(f"{BEAM_LAW}: {where}.reads must be a list of {{family, weight, twist, by}}")
        for position, item in enumerate(raw_reads):
            read = _object(
                item,
                f"{where}.reads[{position}]",
                {"family", "weight", "twist", "by"},
                {"family", "weight", "twist", "by"},
            )
            weight = read["weight"]
            if isinstance(weight, str):
                if weight not in READ_WEIGHT_WORDS:
                    raise ValueError(
                        f"{BEAM_LAW}: {where}.reads[{position}].weight {weight!r} names no integer of "
                        f"the universe (the words: {sorted(READ_WEIGHT_WORDS)})"
                    )
                weight = universe[READ_WEIGHT_WORDS[weight]]
            by = read["by"]
            if by not in (1, "q"):
                raise ValueError(
                    f"{BEAM_LAW}: {where}.reads[{position}].by must be 1 or \\"q\\" (the level enters "
                    "the pace plainly, or by the reading record's charge sign; ALGEBRA.md 9.91 (7))"
                )
            reads.append(
                {"family": read["family"], "weight": weight, "by": READ_BY_WORDS[by], "twist": read["twist"]}
            )
        legacy["reads"] = reads
        if "held" in obj:
            source = _object(
                obj["held"],
                f"{where}.held",
                {"count", "factors", "dipole", "dipole_div"},
                {"count", "factors", "dipole"},
            )
            legacy["held"] = source["count"]
            legacy["held_factors"] = source["factors"]
            legacy["held_dipole"] = source["dipole"]
            legacy["held_dipole_div"] = source.get("dipole_div", 1)
        if "clicks" in obj:
            clicks = _object(
                obj["clicks"], f"{where}.clicks", {"gives", "takes", "quantum"}, {"gives", "takes", "quantum"}
            )
            legacy["clicks"] = {"gives": clicks["gives"], "takes": clicks["takes"]}
            legacy["quantum"] = clicks["quantum"]
        else:
            legacy["quantum"] = 1
        translated.append(legacy)
    return translated, universe


'''
s = s[:start] + new_reader + s[end:]

# ---- 4. FamilyDefinition: the new attributes, booked derived, components a property
rep(
    '''    held: str | None = None
    reads: tuple[tuple[int, int, str], ...] = ()
    components: int = 1

    @property
    def booked(self) -> bool:
        """The detectors book the family's records at their Ports: every
        family but a held one (derived from `held`, item 53)."""
        return self.held is None

    @property
    def massive_kind(self) -> bool:
        """A family of the massive record kind: its pair has den > num (a
        gap); light's kind reads den = num."""
        return self.pair[1] > self.pair[0]
''',
    '''    held: str | None = None
    reads: tuple[tuple[int, int, str, int | str], ...] = ()
    # THE REPRESENTATION AS A LIST OF PARTS (ALGEBRA.md 9.86 (2), (3); 9.91
    # (1); the one stroke, commit 1): (1,) a scalar, (1, 3) the time part and
    # the vector, (1, 3, 6) the symmetric tensor over the four directions; the
    # component order fixed once, (t), (x, y, z), (xx, yy, zz, xy, xz, yz)
    parts: tuple[int, ...] = (1,)
    # the levels at a Node (9.91 (1)): 1 the pair (a_now, a_before, r); 2 the
    # two levels with their remainders (the second level not yet allocated:
    # it enters with the transport, commit 4)
    levels: int = 2
    # THE HELD SOURCE'S WRITES (9.91 (3), (7)): the factor per part (gravity
    # (1, 4, 2): s, 4 s n div W, 2 s n n div W^2; the charge (1, 1)), the
    # body's dipole number written on the six neighbours ("spin", "moment")
    # and its divisor; read by the hold once the vector parts are written
    # (commit 2); one factor per part, (1,) on a scalar
    held_factors: tuple[int, ...] = (1,)
    held_dipole: str | None = None
    held_dipole_div: int = 1
    # the self-source's unit P_2 (9.78 (3), 9.91 (5)): 0, off
    self_unit: int = 0
    # THE CLICKS (9.79 (1), 9.91 (7)): (gives, takes) for a family of records,
    # None for a field family that is never given or taken
    clicks: tuple[bool, bool] | None = None
    # THE PAIR ON THE BODY (9.85 (3), 9.91 (7)): the family declares no pair
    # of its own; every body and every given record of it declares its own
    # (`kind` on the body, `pair` on the emitter); `pair` then a placeholder
    pair_on_body: bool = False

    @property
    def booked(self) -> bool:
        """The detectors book the family's records at their Ports: exactly a
        family with clicks (derived, item 53; ALGEBRA.md 9.91 (7))."""
        return self.clicks is not None

    @property
    def components(self) -> int:
        """The count of components, the parts summed (9.91 (1))."""
        return sum(self.parts)

    @property
    def massive_kind(self) -> bool:
        """A family of the massive record kind: its pair has den > num (a
        gap), or its bodies declare their pairs; light's kind reads den =
        num."""
        return self.pair_on_body or self.pair[1] > self.pair[0]
''',
)

# ---- 5. _kind_pair admits "body"
rep(
    """    if "pair" not in obj:
        return MASSLESS_PAIR
    if not massive_record:
        raise ValueError(
            f"{BEAM_LAW}: {label}.pair is refused without the world key `massive_record` "
            f"(the identity {MASSIVE_RECORD_RULE} beside the law, absent by default)"
        )
    value = obj["pair"]
""",
    """    if "pair" not in obj:
        return MASSLESS_PAIR
    if not massive_record:
        raise ValueError(
            f"{BEAM_LAW}: {label}.pair is refused without the world key `massive_record` "
            f"(the identity {MASSIVE_RECORD_RULE} beside the law, absent by default)"
        )
    value = obj["pair"]
    if value == "body":
        # THE PAIR ON THE BODY (ALGEBRA.md 9.85 (3), 9.91 (7)): the family
        # declares none; every body (`kind`) and every given record (the
        # emitter's `pair`) declares its own; the placeholder here, the flag
        # `pair_on_body` on the family
        return None
""",
)
rep(
    """def _kind_pair(
    obj: dict[str, object], label: str, massive_record: bool, amplitude_bound: int = AMPLITUDE_BOUND
) -> tuple[int, int]:
""",
    """def _kind_pair(
    obj: dict[str, object], label: str, massive_record: bool, amplitude_bound: int = AMPLITUDE_BOUND
) -> tuple[int, int] | None:
""",
)

# ---- 6. _families: the attributes carried into the definition
rep(
    """    generic: list[tuple[str | None, int, list[tuple[str, int, str]]]] = []
""",
    """    generic: list[FamilyAttributes] = []
""",
)
rep(
    """        pair = _kind_pair(obj, f"families[{index}]", massive_record, amplitude_bound)
        if detector_law and "phase_per_link" in obj""",
    """        declared_pair = _kind_pair(obj, f"families[{index}]", massive_record, amplitude_bound)
        pair = MASSLESS_PAIR if declared_pair is None else declared_pair
        if detector_law and "phase_per_link" in obj""",
)
rep(
    """                hand=hand,
                massive=massive,
                pair=pair,
            )
        )
        declared.append(columns)
""",
    """                hand=hand,
                massive=massive,
                pair=pair,
                pair_on_body=declared_pair is None,
            )
        )
        declared.append(columns)
""",
)
rep(
    """            pair=family.pair,
            held=held,
            reads=_resolve_reads(reads, family_names, f"families[{index}]"),
            components=components,
        )
        for index, (family, columns, (held, components, reads)) in enumerate(
            zip(found, declared, generic, strict=True)
        )
    )
    _held_family_shapes(families, detector_law)
    return families
""",
    """            pair=family.pair,
            held=attributes.held,
            reads=_resolve_reads(attributes.reads, family_names, f"families[{index}]"),
            parts=attributes.parts,
            levels=attributes.levels,
            held_factors=attributes.held_factors,
            held_dipole=attributes.held_dipole,
            held_dipole_div=attributes.held_dipole_div,
            self_unit=attributes.self_unit,
            clicks=attributes.clicks,
            pair_on_body=family.pair_on_body,
        )
        for index, (family, columns, attributes) in enumerate(
            zip(found, declared, generic, strict=True)
        )
    )
    _held_family_shapes(families, detector_law)
    return families
""",
)

# ---- 7. _family_generic rewritten
start = s.index("def _family_generic(")
end = s.index("def _resolve_reads(")
new_generic = '''class FamilyAttributes(NamedTuple):
    """What a family is, as declared (items 51 and 53; ALGEBRA.md 9.86 (3), 9.91
    (7)): the reads by name, resolved after every family is read."""

    held: str | None
    parts: tuple[int, ...]
    levels: int
    held_factors: tuple[int, ...]
    held_dipole: str | None
    held_dipole_div: int
    self_unit: int
    clicks: tuple[bool, bool] | None
    reads: list[tuple[str, int, str, int | str]]


def _family_generic(obj: dict[str, object], label: str, detector_law: bool) -> FamilyAttributes:
    """THE FAMILY GENERICITY (the model owner's record 2066; BUILD.md section
    26 item 51) AND THE COMPLETE ATTRIBUTE SET (ALGEBRA.md 9.86 (3), 9.91 (7);
    the one stroke, commit 1): the family's own declaration of what it is,
    `held` (with `held_factors`, `held_dipole`, `held_dipole_div`), `parts`,
    `levels`, `self_unit`, `clicks` and `reads` (the reads by name, resolved
    after every family is read). Admitted under `detector_law` alone; under
    it every family declares `reads` (a field family with no waves the empty
    list: the plain rule), no default. The booking is derived (item 53):
    exactly a family with clicks; an inline entry without `clicks` is a
    family of records unless held (the tests' small lists)."""
    keys = [
        key
        for key in (
            "held",
            "reads",
            "parts",
            "levels",
            "self_unit",
            "clicks",
            "held_factors",
            "held_dipole",
            "held_dipole_div",
        )
        if key in obj
    ]
    if keys and not detector_law:
        raise ValueError(
            f"{BEAM_LAW}: {label} declares {', '.join(keys)}, refused without `detector_law` (a "
            "family's held source, reads and representation are the local detector law's; BUILD.md "
            "section 26 item 51)"
        )
    held: str | None = None
    if "held" in obj:
        held_value = obj["held"]
        if held_value not in HELD_SOURCES:
            raise ValueError(
                f"{BEAM_LAW}: {label}.held must be one of {list(HELD_SOURCES)}: the source a body's "
                "record writes at its Nodes, its held quanta or their signed sum (ALGEBRA.md 9.45 "
                "(2), 9.48 (1); BUILD.md section 26 item 51)"
            )
        held = str(held_value)
    if "components" in obj:
        raise ValueError(
            f"{BEAM_LAW}: {label}.components is refused: the representation is `parts`, a list "
            "([1], [1, 3] or [1, 3, 6]; ALGEBRA.md 9.86 (2), 9.91 (1))"
        )
    parts_value = obj.get("parts", [1])
    if not isinstance(parts_value, list) or tuple(parts_value) not in PARTS_FORMS:
        raise ValueError(
            f"{BEAM_LAW}: {label}.parts must be one of {[list(form) for form in PARTS_FORMS]}: the "
            "representation as a list of parts, the time part first (ALGEBRA.md 9.86 (2), 9.91 (1))"
        )
    parts = tuple(int(part) for part in parts_value)
    levels = obj.get("levels", 2)
    if levels not in (1, 2):
        raise ValueError(f"{BEAM_LAW}: {label}.levels must be 1 or 2 (ALGEBRA.md 9.91 (1))")
    self_unit = _integer(obj.get("self_unit", 0), f"{label}.self_unit", 0)
    if self_unit != 0:
        raise ValueError(
            f"{BEAM_LAW}: {label}.self_unit must be 0: the self-source (ALGEBRA.md 9.78 (3), 9.91 "
            "(5)) is not built"
        )
    held_factors: tuple[int, ...] = tuple(1 for _ in parts)
    held_dipole: str | None = None
    held_dipole_div = 1
    for key in ("held_factors", "held_dipole", "held_dipole_div"):
        if key in obj and held is None:
            raise ValueError(f"{BEAM_LAW}: {label}.{key} is refused on a family that holds nothing")
    if "held_factors" in obj:
        value = obj["held_factors"]
        if (
            not isinstance(value, list)
            or len(value) != len(parts)
            or any(type(item) is not int or item < 1 for item in value)
        ):
            raise ValueError(
                f"{BEAM_LAW}: {label}.held_factors must be {len(parts)} integers from 1, one per part "
                "(ALGEBRA.md 9.91 (3): the held factors are the families file's numbers)"
            )
        held_factors = tuple(int(item) for item in value)
    if "held_dipole" in obj:
        if obj["held_dipole"] not in HELD_DIPOLES:
            raise ValueError(
                f"{BEAM_LAW}: {label}.held_dipole must be one of {list(HELD_DIPOLES)}, the body's "
                "number written on its Node's six neighbours (ALGEBRA.md 9.91 (3))"
            )
        held_dipole = str(obj["held_dipole"])
        if len(parts) < 2:
            raise ValueError(
                f"{BEAM_LAW}: {label}.held_dipole is refused on a scalar family: the dipole is "
                "written into the vector part (ALGEBRA.md 9.91 (3))"
            )
    if "held_dipole_div" in obj:
        held_dipole_div = _integer(obj["held_dipole_div"], f"{label}.held_dipole_div", 1)
    clicks: tuple[bool, bool] | None = None
    if "clicks" in obj:
        value = _object(obj["clicks"], f"{label}.clicks", {"gives", "takes"}, {"gives", "takes"})
        if value["gives"] is not True or value["takes"] is not True:
            raise ValueError(
                f"{BEAM_LAW}: {label}.clicks.gives and .takes must be true: a family of records is "
                "given and taken at clicks (ALGEBRA.md 9.79 (1))"
            )
        clicks = (True, True)
    elif held is None:
        clicks = (True, True)
    reads: list[tuple[str, int, str, int | str]] = []
    if detector_law and "reads" not in obj:
        raise ValueError(
            f"{BEAM_LAW}: {label} declares no `reads` under {DETECTOR_LAW_RULE}: the held families "
            "whose levels enter the family's pace, with their weights (an empty list for a held "
            "family: the plain rule), no default (ALGEBRA.md 9.45 (3), 9.48 (3); BUILD.md section "
            "26 item 51)"
        )
    raw_reads = obj.get("reads", [])
    if not isinstance(raw_reads, list):
        raise ValueError(f"{BEAM_LAW}: {label}.reads must be a list of {{family, weight, by, twist}}")
    for position, item in enumerate(raw_reads):
        read = _object(
            item,
            f"{label}.reads[{position}]",
            {"family", "weight", "by", "twist"},
            {"family", "weight"},
        )
        name = read["family"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"{BEAM_LAW}: {label}.reads[{position}].family must name a family")
        weight = _integer(read["weight"], f"{label}.reads[{position}].weight", 1, AMOUNT_BOUND)
        by = read.get("by", "plain")
        if by not in READ_BY:
            raise ValueError(
                f"{BEAM_LAW}: {label}.reads[{position}].by must be one of {list(READ_BY)}: the level "
                "enters the pace as weight x level (plain) or as - q x weight x level, q the "
                "reading family's own charge sign (sign; ALGEBRA.md 9.48 (3))"
            )
        twist: int | str = read.get("twist", 0)
        if not (
            (type(twist) is int and twist >= 0) or (isinstance(twist, str) and twist in READ_TWIST_WORDS)
        ):
            raise ValueError(
                f"{BEAM_LAW}: {label}.reads[{position}].twist must be an integer from 0 or one of "
                f"{list(READ_TWIST_WORDS)} (the transport's angle per read, ALGEBRA.md 9.81 (2), "
                "9.91 (6))"
            )
        if any(other == name for other, _, _, _ in reads):
            raise ValueError(f"{BEAM_LAW}: {label}.reads names {name!r} twice")
        reads.append((name, weight, str(by), twist))
    if held is not None and reads and clicks is None:
        raise ValueError(
            f"{BEAM_LAW}: {label} is held and reads {[name for name, _, _, _ in reads]}: a field "
            "family with no waves steps by the plain rule at the pace 1 of its own and reads no "
            "level (ALGEBRA.md 9.45 (2); BUILD.md section 26 item 51)"
        )
    return FamilyAttributes(
        held, parts, levels, held_factors, held_dipole, held_dipole_div, self_unit, clicks, reads
    )


'''
s = s[:start] + new_generic + s[end:]

rep(
    '''def _resolve_reads(
    reads: list[tuple[str, int, str]], names: list[str], label: str
) -> tuple[tuple[int, int, str], ...]:
    """The reads by name to the families' indices; a read names a declared
    family (the names listed)."""
    out: list[tuple[int, int, str]] = []
    for name, weight, by in reads:
        if name not in names:
            raise ValueError(
                f"{BEAM_LAW}: {label}.reads names {name!r}, which no family declares (the families: "
                f"{names})"
            )
        out.append((names.index(name), weight, by))
    return tuple(out)
''',
    '''def _resolve_reads(
    reads: list[tuple[str, int, str, int | str]], names: list[str], label: str
) -> tuple[tuple[int, int, str, int | str], ...]:
    """The reads by name to the families' indices; a read names a declared
    family (the names listed)."""
    out: list[tuple[int, int, str, int | str]] = []
    for name, weight, by, twist in reads:
        if name not in names:
            raise ValueError(
                f"{BEAM_LAW}: {label}.reads names {name!r}, which no family declares (the families: "
                f"{names})"
            )
        out.append((names.index(name), weight, by, twist))
    return tuple(out)
''',
)

# ---- 8. the held family shapes: reads name held families (4-tuples)
rep(
    """        for other, _, _ in family.reads:
            if families[other].held is None:""",
    """        for other, _, _, _ in family.reads:
            if families[other].held is None:""",
)

# ---- 9. the held bodies checks: a family with clicks has bodies and stock
rep(
    """    for index, family in enumerate(families):
        if family.held is None:
            continue
        name = family.name
        for number, entry in enumerate(measured):
            if entry.family == index:""",
    """    for index, family in enumerate(families):
        if family.held is None or family.clicks is not None:
            # a family that is held and has clicks (the charge with light as its
            # wave, ALGEBRA.md 9.86 (2) (b)) has bodies of light's kind, a stock
            # and givings; its held part is the engine's write as any held family's
            continue
        name = family.name
        for number, entry in enumerate(measured):
            if entry.family == index:""",
)

# ---- 10. the pair bound loop: reads 4-tuples; the body's kind checked in _block
rep(
    """            reach = sum(weight * source_of(families[other], entry) for other, weight, _ in family.reads)
            if family.reads and reach >= node_clock:""",
    """            reach = sum(
                weight * source_of(families[other], entry) for other, weight, _, _ in family.reads
            )
            if family.reads and reach >= node_clock:""",
)
rep(
    """        reach = 2 * sum(
            weight * source_of(families[other], entry)
            for other, weight, _ in family.reads
            for entry in measured
        )
        content = max(content, reach)
    for index, family in enumerate(families):
        _pair_bound(
            family.pair[0], family.pair[1], f"families[{index}]", amplitude_bound, node_clock, content
        )
    for number, entry in enumerate(measured):
        if entry.block is not None:
            _pair_bound(
                entry.block.pair[0],
                entry.block.pair[1],
                f"measured[{number}]",
                amplitude_bound,
                node_clock,
                content,
            )
""",
    """        reach = 2 * sum(
            weight * source_of(families[other], entry)
            for other, weight, _, _ in family.reads
            for entry in measured
        )
        content = max(content, reach)
    for index, family in enumerate(families):
        if family.pair_on_body:
            continue  # the bodies' kinds are read below (ALGEBRA.md 9.91 (7))
        _pair_bound(
            family.pair[0], family.pair[1], f"families[{index}]", amplitude_bound, node_clock, content
        )
    for number, entry in enumerate(measured):
        if entry.block is not None:
            _pair_bound(
                entry.block.pair[0],
                entry.block.pair[1],
                f"measured[{number}]",
                amplitude_bound,
                node_clock,
                content,
            )
            if families[entry.family].pair_on_body:
                _pair_bound(
                    entry.block.kind[0],
                    entry.block.kind[1],
                    f"measured[{number}].kind",
                    amplitude_bound,
                    node_clock,
                    content,
                )
""",
)

# ---- 11. BlockDefinition.kind
rep(
    """    side: int
    pair: tuple[int, int]
    # the well's own record's amplitude on its Nodes at interval 0 (0
    # silent), or its profile's; declared in the file, no default (the
""",
    """    side: int
    pair: tuple[int, int]
    # THE BODY'S KIND (ALGEBRA.md 9.85 (3), 9.91 (7); the one stroke, commit
    # 1): the rest pair of the body's own record, its family's declared pair
    # or, on a family whose pair is the body's, the body's own `kind`
    kind: tuple[int, int]
    # the well's own record's amplitude on its Nodes at interval 0 (0
    # silent), or its profile's; declared in the file, no default (the
""",
)
rep(
    """    pair = (
        _integer(value[0], f"{label}.pair numerator", 1, MAX_VALUE),
        _integer(value[1], f"{label}.pair denominator", 1, MAX_VALUE),
    )
    kind = family.pair
    if family.massive_kind:""",
    """    pair = (
        _integer(value[0], f"{label}.pair numerator", 1, MAX_VALUE),
        _integer(value[1], f"{label}.pair denominator", 1, MAX_VALUE),
    )
    # THE BODY'S KIND (ALGEBRA.md 9.85 (3), 9.91 (7)): the family's pair, or the
    # body's own `kind` [num, den] on a family whose pair is the body's,
    # required there and refused elsewhere (one copy)
    if family.pair_on_body:
        if "kind" not in obj:
            raise ValueError(
                f"{BEAM_LAW}: {label}.kind is required: the family {family.name!r} declares no pair, "
                "so every body of it declares its own rest pair [num, den] (ALGEBRA.md 9.85 (3), "
                "9.91 (7))"
            )
        kind_value = obj["kind"]
        if not isinstance(kind_value, list) or len(kind_value) != 2:
            raise ValueError(f"{BEAM_LAW}: {label}.kind must be [num, den], the body's rest pair")
        kind = (
            _integer(kind_value[0], f"{label}.kind numerator", 1, MAX_VALUE),
            _integer(kind_value[1], f"{label}.kind denominator", 1, MAX_VALUE),
        )
        if kind[1] <= kind[0]:
            raise ValueError(
                f"{BEAM_LAW}: {label}.kind [{kind[0]}, {kind[1]}] is no massive kind: den > num, "
                "the gap cos omega_0 = num / den (ALGEBRA.md 9.22)"
            )
    elif "kind" in obj:
        raise ValueError(
            f"{BEAM_LAW}: {label}.kind is refused: the family {family.name!r} declares its pair "
            f"{list(family.pair)}; one copy (ALGEBRA.md 9.85 (3))"
        )
    else:
        kind = family.pair
    if family.massive_kind:""",
)
rep(
    """    return BlockDefinition(
        side,
        pair,
        seed,
        extents=extents,""",
    """    return BlockDefinition(
        side,
        pair,
        kind,
        seed,
        extents=extents,""",
)

# ---- 12. the emitter's pair
rep(
    """    # THE GIVEN CLOCK (ALGEBRA.md 9.85 (3); item 59): the given record's clock
    # [p, q], the family's own or the emitter's `clock`
    clock: tuple[int, int]
    period: int | None = None
    norm: int | None = None
    train: TrainDefinition | None = None
""",
    """    # THE GIVEN CLOCK (ALGEBRA.md 9.85 (3); item 59): the given record's clock
    # [p, q], the family's own or the emitter's `clock`
    clock: tuple[int, int]
    # THE GIVEN RECORD'S PAIR (ALGEBRA.md 9.85 (3), 9.91 (7); commit 1): the
    # given family's declared pair, or the emitter's own `pair` on a family
    # whose pair is the body's
    pair: tuple[int, int] = MASSLESS_PAIR
    period: int | None = None
    norm: int | None = None
    train: TrainDefinition | None = None
""",
)
rep(
    """            "norm_denominator",
            "window_read",
            "clock",
        },
        {"family"},
    )
    name = obj["family"]
    if not isinstance(name, str) or name not in names:
        raise ValueError(f"{BEAM_LAW}: {label}.family names an unknown family")
""",
    """            "norm_denominator",
            "window_read",
            "clock",
            "pair",
        },
        {"family"},
    )
    name = obj["family"]
    if not isinstance(name, str) or name not in names:
        raise ValueError(f"{BEAM_LAW}: {label}.family names an unknown family")
""",
)
rep(
    """    if given_family.free:
        raise ValueError(
            f"{BEAM_LAW}: {label}.family {name!r}: the given family is a paid family (light's kind, "
            "or a massive kind)"
        )
    if given_family.held is not None:
""",
    """    if given_family.free:
        raise ValueError(
            f"{BEAM_LAW}: {label}.family {name!r}: the given family is a paid family (light's kind, "
            "or a massive kind)"
        )
    # THE GIVEN RECORD'S PAIR (ALGEBRA.md 9.85 (3), 9.91 (7)): the emitter's
    # `pair` [num, den], required when the given family's pair is the body's
    # and refused when the family declares one (one copy)
    given_pair: tuple[int, int]
    if given_family.pair_on_body:
        if "pair" not in obj:
            raise ValueError(
                f"{BEAM_LAW}: {label}.pair is required: the given family {name!r} declares no pair, "
                "so the emitter declares the given record's pair [num, den] (ALGEBRA.md 9.85 (3), "
                "9.91 (7))"
            )
        given_pair = _ratio(obj["pair"], f"{label}.pair", zero=False)
        if given_pair[1] <= given_pair[0]:
            raise ValueError(
                f"{BEAM_LAW}: {label}.pair [{given_pair[0]}, {given_pair[1]}] is no massive kind: den "
                "> num (ALGEBRA.md 9.22)"
            )
    elif "pair" in obj:
        raise ValueError(
            f"{BEAM_LAW}: {label}.pair is refused: the given family {name!r} declares its pair "
            f"{list(given_family.pair)}; one copy (ALGEBRA.md 9.85 (3))"
        )
    else:
        given_pair = given_family.pair
    if given_family.held is not None and given_family.clicks is None:
""",
)
rep(
    """        wrap = periodic
        given = _given_train(value, f"{label}.given", given_family, shape, extents, wrap, train)
    return EmitterDefinition(
        names[name],
        branches,
        label_hands,
        receiver,
        clock,
        period,
        norm,
        train,
        given,
        weight=weight,
        norm_denominator=norm_denominator,
    )
""",
    """        wrap = periodic
        given = _given_train(value, f"{label}.given", given_pair, shape, extents, wrap, train)
    return EmitterDefinition(
        names[name],
        branches,
        label_hands,
        receiver,
        clock,
        given_pair,
        period,
        norm,
        train,
        given,
        weight=weight,
        norm_denominator=norm_denominator,
    )
""",
)
rep(
    """def _given_train(
    value: object,
    label: str,
    given_family: FamilyDefinition,
    shape: Address3,
""",
    """def _given_train(
    value: object,
    label: str,
    given_pair: tuple[int, int],
    shape: Address3,
""",
)
rep(
    """    expected = given_train_norm(now, before, board, (0, 0, 0), extents, given_family.pair, wrap)
""",
    """    expected = given_train_norm(now, before, board, (0, 0, 0), extents, given_pair, wrap)
""",
)

# ---- 13. the profile check reads the body's kind
rep(
    """        family = families[entry.family]
        wrap = periodic
        a, b = block.clock
        # (iii) the band: a / b above the family's band top 2 num / den and below 2
        if a * family.pair[1] <= 2 * family.pair[0] * b:
            raise ValueError(
                f"{BEAM_LAW}: measured[{number}].clock [{a}, {b}] is not above the band's top "
                f"2 x {family.pair[0]} / {family.pair[1]} of the family {family.name!r}: the "
""",
    """        family = families[entry.family]
        kind = block.kind  # the body's rest pair (ALGEBRA.md 9.91 (7); commit 1)
        wrap = periodic
        a, b = block.clock
        # (iii) the band: a / b above the kind's band top 2 num / den and below 2
        if a * kind[1] <= 2 * kind[0] * b:
            raise ValueError(
                f"{BEAM_LAW}: measured[{number}].clock [{a}, {b}] is not above the band's top "
                f"2 x {kind[0]} / {kind[1]} of the kind of the family {family.name!r}: the "
""",
)
rep(
    """        num = [family.pair[0]] * count
        den = [family.pair[1]] * count
        where = [True] * count
        for other_number, other, other_block, other_nodes in blocks:
            if other.family != entry.family:
                continue
""",
    """        num = [kind[0]] * count
        den = [kind[1]] * count
        where = [True] * count
        for other_number, other, other_block, other_nodes in blocks:
            if other.family != entry.family or other_block.kind != kind:
                continue
""",
)

# ---- 14. NamedTuple import
rep("from typing import", "from typing import NamedTuple,", 1) if "NamedTuple" not in s else None
p.write_text(s)
print("world.py edited")
