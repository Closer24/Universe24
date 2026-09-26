"""THE GENERIC LOADER OF THE UNIVERSE FILE (issue #1154, cut 3; the model owner's records 2220 and
2226 through the Boss: the loader replaced by one schema-driven reader, no default in the code;
ALGEBRA.md 9.91 (7), 9.110 item 1): core/schema.py is the language (a Key's kind, bounds, admitted
words; one reader refusing by name), core/loader.py reads the universe file against core's integers
block and every folder's SCHEMA (the keys of the files it reads, beside its DECLARATION), and
world.py's `universe_file_entries` is an adapter folding the checked values into the dict the
legacy reader takes. The proof of no behaviour change: (a) the hand parse of main 13623ccf copied
here verbatim as the ORACLE agrees value for value with the adapter on the shipped file, on a
file with a test's integers, on the adversarially renamed file and on a synthetic file of every
admitted form; (b) every shipped world naming the universe loads to the FamilyDefinition tuple of
main 13623ccf (a digest of its repr, recorded at the base); (c) each defect of the file is refused
by name; (d) the register refuses a folder's schema without a section, two folders reading one
key and a bound naming an integer the universe lacks; (e) no default: a Key has no default word
and the reader returns the keys present and no other. HOST; no physics, no pin on nature."""

from __future__ import annotations

import dataclasses
import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from types import SimpleNamespace

import pytest

from event_universe.core.loader import UNIVERSE_INTEGERS, family_keys, load_universe
from event_universe.core.register import Declaration, Register, declaration_of, discover
from event_universe.core.schema import AMOUNT_BOUND, Key, read_object
from event_universe.events.world import universe_file_entries
from event_universe.world_files import parse_nature_beam_world

ROOT = Path(__file__).resolve().parents[1]
FILE = "examples/events/universe.json"

# THE ORACLE: `universe_file_entries` of main 13623ccf, the hand parse, copied verbatim (its two
# helpers `_object` and `_integer` with it, the retired-key branch of `_object` aside); deleted
# with the Term-form cut, never kept as a second reader
FAMILIES_FILE_KEYS = {"integers", "families"}
FAMILIES_INTEGERS = {"node_clock", "amplitude_bound", "Lambda", "momentum_unit"}
FAMILIES_TABLES = {"twist_table"}
FAMILY_ENTRY_KEYS = {"name", "parts", "phase", "pair", "held", "reads", "self_source", "clicks"}
FAMILY_ENTRY_REQUIRED = {"name", "parts", "phase", "pair", "reads", "self_source"}
PARTS_FORMS = ((1,), (1, 3), (1, 3, 6))
READ_WEIGHT_WORDS = {"Lambda": "Lambda"}
READ_BY_WORDS = {1: "plain", "q": "sign", "plain": "plain", "sign": "sign"}


def _object(value: object, label: str, allowed: set[str], required: set[str]) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    unknown = set(value) - allowed
    if unknown:
        raise ValueError(f"{label} has unknown keys: {', '.join(sorted(unknown))}")
    missing = required - set(value)
    if missing:
        raise ValueError(f"{label} lacks keys: {', '.join(sorted(missing))}")
    return {str(key): item for key, item in value.items()}


def _integer(value: object, label: str, minimum: int, maximum: int = AMOUNT_BOUND) -> int:
    if type(value) is not int or value < minimum or value > maximum:
        raise ValueError(f"{label} must be an integer from {minimum} through {maximum}")
    return value


def oracle_entries(
    value: str, files: Mapping[str, object]
) -> tuple[list[dict[str, object]], dict[str, object]]:
    if value not in files:
        raise ValueError(f"universe names {value!r}, no file at the repository's root")
    document = files[value]
    label = f"the universe file {value!r}"
    if not isinstance(document, dict):
        raise ValueError(f"{label} must be a JSON object")
    unknown = set(document) - FAMILIES_FILE_KEYS
    if unknown:
        raise ValueError(f"{label} has unknown keys: {', '.join(sorted(unknown))}")
    missing = FAMILIES_FILE_KEYS - set(document)
    if missing:
        raise ValueError(f"{label} lacks keys: {', '.join(sorted(missing))}")
    integers = document["integers"]
    if not isinstance(integers, dict) or set(integers) != FAMILIES_INTEGERS | FAMILIES_TABLES:
        raise ValueError(
            f"{label}.integers must hold exactly {sorted(FAMILIES_INTEGERS | FAMILIES_TABLES)}"
        )
    universe: dict[str, object] = {
        key: _integer(integers[key], f"{label}.integers.{key}", 1, AMOUNT_BOUND)
        for key in sorted(FAMILIES_INTEGERS)
    }
    universe["twist_table"] = integers["twist_table"]
    entries = document["families"]
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{label}.families must be a nonempty list")
    translated: list[dict[str, object]] = []
    for index, entry in enumerate(entries):
        where = f"{label}.families[{index}]"
        obj = _object(entry, where, FAMILY_ENTRY_KEYS, FAMILY_ENTRY_REQUIRED)
        parts = obj["parts"]
        if not isinstance(parts, list) or tuple(parts) not in PARTS_FORMS:
            raise ValueError(f"{where}.parts must be one of {[list(form) for form in PARTS_FORMS]}")
        if obj["phase"] not in (1, 2):
            raise ValueError(f"{where}.phase must be 1 or 2")
        self_source = _object(obj["self_source"], f"{where}.self_source", {"unit"}, {"unit"})
        self_unit = _integer(self_source["unit"], f"{where}.self_source.unit", 0)
        amplitude = universe["amplitude_bound"]
        assert isinstance(amplitude, int)
        if 0 < self_unit < 24 * amplitude:
            raise ValueError(f"{where}.self_source.unit {self_unit} is below 24 A = {24 * amplitude}")
        pair_value = obj["pair"]
        if pair_value != "body" and not (
            isinstance(pair_value, list)
            and len(pair_value) == 2
            and all(type(item) is int and item >= 1 for item in pair_value)
        ):
            raise ValueError(f'{where}.pair must be [num, den] or the word "body"')
        if "held" not in obj and "clicks" not in obj:
            raise ValueError(
                f"{where} declares neither held (a field family) nor clicks (a family of records)"
            )
        legacy: dict[str, object] = {
            "name": obj["name"],
            "charge": 0,
            "pair": pair_value,
            "parts": list(parts),
            "levels": obj["phase"],
            "self_unit": self_unit,
        }
        reads: list[dict[str, object]] = []
        raw_reads = obj["reads"]
        if not isinstance(raw_reads, list):
            raise ValueError(f"{where}.reads must be a list of {{family, weight, twist, by}}")
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
                        f"{where}.reads[{position}].weight {weight!r} names no integer of the universe"
                    )
                weight = universe[READ_WEIGHT_WORDS[weight]]
            by = read["by"]
            if by not in (1, "q"):
                raise ValueError(f'{where}.reads[{position}].by must be 1 or "q"')
            reads.append(
                {
                    "family": read["family"],
                    "weight": weight,
                    "by": READ_BY_WORDS[by],
                    "twist": read["twist"],
                }
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
                obj["clicks"],
                f"{where}.clicks",
                {"gives", "takes", "quantum"},
                {"gives", "takes", "quantum"},
            )
            legacy["clicks"] = {"gives": clicks["gives"], "takes": clicks["takes"]}
            legacy["quantum"] = clicks["quantum"]
        else:
            legacy["quantum"] = 1
        translated.append(legacy)
    return translated, universe


# the shipped file's three families in the legacy reader's words, pinned
GRAVITY = {
    "name": "gravity",
    "charge": 0,
    "pair": [1, 1],
    "parts": [1, 3, 6],
    "levels": 1,
    "self_unit": 0,
    "reads": [],
    "quantum": 1,
    "held": "content",
    "held_factors": [1, 4, 2],
    "held_dipole": "spin",
    "held_dipole_div": 1,
}
CHARGE = {
    "name": "charge",
    "charge": 0,
    "pair": [1, 1],
    "parts": [1, 3],
    "levels": 2,
    "self_unit": 0,
    "reads": [{"family": "gravity", "weight": 1, "by": "plain", "twist": "own"}],
    "quantum": 1,
    "held": "sign",
    "held_factors": [1, 1],
    "held_dipole": "moment",
    "held_dipole_div": 2,
    "clicks": {"gives": True, "takes": True},
}
MATTER = {
    "name": "matter",
    "charge": 0,
    "pair": "body",
    "parts": [1],
    "levels": 2,
    "self_unit": 0,
    "reads": [
        {"family": "gravity", "weight": 1, "by": "plain", "twist": "own"},
        {"family": "charge", "weight": 1, "by": "sign", "twist": "own"},
    ],
    "quantum": 1,
    "clicks": {"gives": True, "takes": True},
}
# the FamilyDefinition tuple of every shipped world naming the universe, SHA-256 of its repr at
# main 13623ccf (the base of the cut); a world not here is refused on a world-file key as at
# the base, or it is a new world and its digest is added here
FAMILIES_AT_THE_BASE = {
    "dark_body/bright.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "dark_body/dark.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "massive_record/boxed_clock_side_20_at_rest.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "massive_record/boxed_clock_side_20_moving.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "massive_record/boxed_clock_side_28_at_rest.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "massive_record/boxed_clock_side_28_moving.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "massive_record/deep_well_clock_at_rest_40.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "massive_record/deep_well_clock_speed_third_40.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "massive_record/light_clock.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "massive_record/muon_moving_clock_at_rest_14.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "massive_record/muon_moving_clock_speed_third_14.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "point_emitter/point_chain.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "point_emitter/point_light_clock.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "toward_nature/bending.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "toward_nature/lorentz_moving.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "toward_nature/lorentz_moving_long.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "toward_nature/lorentz_rest.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "toward_nature/lorentz_rest_long.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "toward_nature/redshift_bottom.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "toward_nature/redshift_bottom_long.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "toward_nature/redshift_top.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
    "toward_nature/redshift_top_long.json": "d8476abdd5afa93cc33936c2256e04e0108a976ffc5df235ee776345b19459b4",
}


def shipped() -> dict:
    return json.loads((ROOT / FILE).read_text(encoding="utf-8"))


def both(document: dict, name: str = FILE) -> tuple:
    """The adapter's and the oracle's readings of one document, asserted equal."""
    files = {name: document}
    ours = universe_file_entries(name, files)
    theirs = oracle_entries(name, files)
    assert ours == theirs
    return ours


def test_the_shipped_file_reads_as_the_hand_parse_did_and_its_three_families_are_these():
    document = shipped()
    entries, integers = both(document)
    assert entries == [GRAVITY, CHARGE, MATTER]
    assert integers == document["integers"] and list(integers) == list(UNIVERSE_INTEGERS)
    # a test's integers (tests/test_families_file.py's file), the same families
    document["integers"]["node_clock"] = 512
    document["integers"]["amplitude_bound"] = 1 << 22
    entries, integers = both(document, "universe.json")
    assert entries == [GRAVITY, CHARGE, MATTER] and integers["amplitude_bound"] == 1 << 22


def test_the_renamed_file_and_a_file_of_every_admitted_form_read_as_the_hand_parse_did():
    rename = {"gravity": "matter", "charge": "gravity", "matter": "charge"}
    document = shipped()
    for entry in document["families"]:
        entry["name"] = rename[entry["name"]]
        for read in entry["reads"]:
            read["family"] = rename[read["family"]]
    entries, _ = both(document)
    assert [entry["name"] for entry in entries] == ["matter", "gravity", "charge"]
    assert entries[2]["reads"][1] == {"family": "gravity", "weight": 1, "by": "sign", "twist": "own"}
    amplitude = 1 << 20
    every = {
        "integers": {**shipped()["integers"], "Lambda": 7, "momentum_unit": 3},
        "families": [
            {
                "name": "field",
                "parts": [1, 3, 6],
                "phase": 1,
                "pair": [700, 703],
                "held": {"count": "content", "factors": [2, 5, 1], "dipole": "spin", "dipole_div": 2},
                "reads": [],
                "self_source": {"unit": 24 * amplitude},
            },
            {
                "name": "wave",
                "parts": [1, 3],
                "phase": 2,
                "pair": [1, 1],
                "held": {"count": "sign", "factors": [1, 1], "dipole": "moment", "dipole_div": 1},
                "reads": [{"family": "field", "weight": "Lambda", "twist": 200, "by": "q"}],
                "self_source": {"unit": 0},
                "clicks": {"gives": True, "takes": False, "quantum": 3},
            },
            {
                "name": "stuff",
                "parts": [1],
                "phase": 2,
                "pair": "body",
                "reads": [
                    {"family": "field", "weight": "momentum_unit", "twist": "own", "by": 1},
                    {"family": "wave", "weight": 2, "twist": 0, "by": "q"},
                ],
                "self_source": {"unit": 0},
                "clicks": {"gives": True, "takes": True, "quantum": 1},
            },
        ],
    }
    # the hand parse resolved "Lambda" alone; the reader resolves every integer of the universe by
    # its key (a widening, no shipped or test universe touched): the oracle sees the integer
    plain = json.loads(json.dumps(every))
    plain["families"][2]["reads"][0]["weight"] = 3
    entries, integers = universe_file_entries("every.json", {"every.json": every})
    assert (entries, integers) == oracle_entries("every.json", {"every.json": plain})
    assert entries[0]["self_unit"] == 24 * amplitude and entries[0]["held_dipole_div"] == 2
    assert entries[1]["reads"] == [{"family": "field", "weight": 7, "by": "sign", "twist": 200}]
    assert entries[1]["clicks"] == {"gives": True, "takes": False} and entries[1]["quantum"] == 3
    assert entries[2]["reads"][0]["weight"] == 3 and entries[2]["quantum"] == 1


def test_every_shipped_world_naming_the_universe_loads_to_the_families_of_the_base():
    found = {}
    for path in sorted((ROOT / "examples/events").glob("*/*.json")):
        text = json.loads(path.read_text(encoding="utf-8"))
        if not (isinstance(text, dict) and isinstance(text.get("universe"), str)):
            continue
        name = path.relative_to(ROOT / "examples/events").as_posix()
        try:
            world = parse_nature_beam_world(text)
        except ValueError as refusal:
            # a world-file key ahead of the loader (the check-mode and source worlds), never the universe file's
            assert "the universe file" not in str(refusal), (name, refusal)
            continue
        found[name] = hashlib.sha256(repr(world.families).encode("utf-8")).hexdigest()
    assert {name: found[name] for name in FAMILIES_AT_THE_BASE} == FAMILIES_AT_THE_BASE
    assert len(found) >= 22


def refused(document: object, match: str, name: str = FILE) -> None:
    with pytest.raises(ValueError, match=match):
        load_universe(name, {name: document}, discover())


def test_each_defect_of_the_file_is_refused_by_name():
    good = shipped()
    with pytest.raises(
        ValueError, match="universe names 'nowhere.json', no file at the repository's root"
    ):
        load_universe("nowhere.json", {}, discover())
    refused([], r"the universe file 'examples/events/universe.json' must be a JSON object with the keys")
    cases = (
        (lambda d: d.__setitem__("law", "beam-v1"), "the universe file .* has unknown keys: law"),
        (lambda d: d.pop("families"), "lacks keys: families"),
        (
            lambda d: d["integers"].pop("node_clock"),
            r"integers lacks keys: node_clock \(the keys: \['node_clock'",
        ),
        (
            lambda d: d["integers"].__setitem__("Lambda", 0),
            "integers.Lambda must be an integer from 1 through 4611686018427387903, not 0",
        ),
        (
            lambda d: d["integers"].__setitem__("Lambda", True),
            "integers.Lambda must be an integer from 1 through 4611686018427387903, not True",
        ),
        (lambda d: d["integers"]["twist_table"].pop("coarse"), "twist_table lacks keys: coarse"),
        (
            lambda d: d.__setitem__("families", []),
            r"families must be a list of at least 1 items, not \[\]",
        ),
        (lambda d: d["families"][0].pop("parts"), r"families\[0\] lacks keys: parts"),
        (
            lambda d: d["families"][0].__setitem__("name", ""),
            "families\\[0\\].name must be a name, a nonempty string, not ''",
        ),
        (
            lambda d: d["families"][0].__setitem__("parts", [3]),
            r"parts must be one of \[\[1\], \[1, 3\], \[1, 3, 6\]\], not \[3\] \(ALGEBRA.md 9.86 \(2\); 9.91 \(1\)\)",
        ),
        (lambda d: d["families"][0].__setitem__("parts", [1, True]), r"parts must be one of"),
        (lambda d: d["families"][0].__setitem__("phase", 3), r"phase must be one of \[1, 2\], not 3"),
        (
            lambda d: d["families"][0].__setitem__("phase", True),
            r"phase must be one of \[1, 2\], not True",
        ),
        (
            lambda d: d["families"][0]["self_source"].__setitem__("unit", 24),
            r"self_source\.unit must be an integer from 24 x amplitude_bound = 25165824 through 4611686018427387903 or one of \[0\], not 24",
        ),
        (
            lambda d: d["families"][0]["self_source"].__setitem__("unit", -1),
            r"self_source\.unit must be an integer from 24 x amplitude_bound",
        ),
        (
            lambda d: d["families"][0].pop("held"),
            r"families\[0\] declares neither clicks \(a family of records\) nor held \(a field family\): a family does at least one",
        ),
        (
            lambda d: d["families"][2].__setitem__("pair", "mine"),
            r"pair must be \[num, den\] or the word 'body' \(two integers from 1\), not 'mine'",
        ),
        (
            lambda d: d["families"][2].__setitem__("pair", [0, 1]),
            r"pair must be \[num, den\] or the word 'body'",
        ),
        (
            lambda d: d["families"][2]["reads"][1].__setitem__("weight", "Mu"),
            r"reads\[1\].weight 'Mu' names no integer of the universe \(the integers: \['Lambda', 'amplitude_bound', 'momentum_unit', 'node_clock'\]\)",
        ),
        (
            lambda d: d["families"][2]["reads"][1].__setitem__("weight", 0),
            r"reads\[1\].weight must be an integer from 1 through 4611686018427387903 or a universe integer's key, not 0",
        ),
        (
            lambda d: d["families"][2]["reads"][1].__setitem__("twist", -1),
            r"reads\[1\].twist must be an integer from 0 through 4611686018427387903 or the word 'own', not -1",
        ),
        (
            lambda d: d["families"][2]["reads"][1].__setitem__("by", 2),
            r"by must be one of \[1, 'q'\], not 2",
        ),
        (
            lambda d: d["families"][2]["reads"][1].__setitem__("by", True),
            r"by must be one of \[1, 'q'\], not True",
        ),
        (lambda d: d["families"][2]["reads"][1].pop("twist"), r"reads\[1\] lacks keys: twist"),
        (lambda d: d["families"][2].__setitem__("reads", {}), r"reads must be a list, not \{\}"),
        (lambda d: d["families"][0]["held"].pop("dipole_div"), "held lacks keys: dipole_div"),
        (
            lambda d: d["families"][0]["held"].__setitem__("count", "mass"),
            r"held.count must be one of \['content', 'sign'\], not 'mass'",
        ),
        (
            lambda d: d["families"][0]["held"].__setitem__("factors", [1, 0, 1]),
            r"held.factors\[1\] must be an integer from 1 through",
        ),
        (
            lambda d: d["families"][0]["held"].__setitem__("factors", []),
            r"held.factors must be a list of 1 to 3 items, not \[\]",
        ),
        (
            lambda d: d["families"][0]["held"].__setitem__("dipole", "twist"),
            r"held.dipole must be one of \['spin', 'moment'\], not 'twist'",
        ),
        (
            lambda d: d["families"][1]["clicks"].__setitem__("quantum", 0),
            r"clicks.quantum must be an integer from 1 through 4611686018427387903, not 0",
        ),
        (
            lambda d: d["families"][1]["clicks"].__setitem__("gives", 1),
            r"clicks.gives must be true or false, not 1",
        ),
        (
            lambda d: d["families"][1]["clicks"].__setitem__("given", True),
            r"clicks has unknown keys: given",
        ),
    )
    for change, match in cases:
        broken = json.loads(json.dumps(good))
        change(broken)
        refused(broken, match)


def test_the_register_refuses_a_schema_without_a_section_two_readers_of_one_key_and_a_bound_the_universe_lacks():
    module = SimpleNamespace(
        DECLARATION=Declaration(
            "the hold", "(iv)", (), ("a family's level at a Node",), 1, None, "9.91 (3)"
        ),
        SCHEMA={"family": (Key("held", "int"),)},
    )
    with pytest.raises(ValueError, match="the key 'held' of family names no ALGEBRA.md section"):
        declaration_of("hold", module)
    module.SCHEMA = {"family": [Key("held", "int", section="9.91 (3)")]}
    with pytest.raises(ValueError, match="SCHEMA must map a word of the files to a tuple of Keys"):
        declaration_of("hold", module)
    module.SCHEMA = {"family": (Key("held", "int", section="9.91 (3)"),)}
    declaration = declaration_of("hold", module)
    assert declaration.schema == module.SCHEMA
    register = Register()
    register.add(declaration)
    other = Declaration(
        "the well",
        "(iv)",
        (),
        (),
        None,
        None,
        "9.1",
        schema={"family": (Key("held", "int", section="9.1"),)},
    )
    with pytest.raises(
        ValueError,
        match="the primitives 'the hold' and 'the well' both read the key 'held' of family: one key, one reader",
    ):
        register.add(other)
    lacking = Register()
    lacking.add(
        Declaration(
            "the well",
            "(iv)",
            (),
            (),
            None,
            None,
            "9.1",
            schema={"family": (Key("depth", "int", low="Mu", section="9.1"),)},
        )
    )
    document = {"integers": shipped()["integers"], "families": [{"name": "a", "depth": 3}]}
    with pytest.raises(
        ValueError,
        match=r"families\[0\].depth: its schema names the bound 'Mu', which the universe's integers lack",
    ):
        load_universe("u.json", {"u.json": document}, lacking)
    assert [key.name for key in family_keys(lacking)] == ["name", "depth"]


def test_no_default_the_reader_returns_the_keys_present_and_the_folders_keys_are_these():
    assert not any("default" in field.name for field in dataclasses.fields(Key))
    keys = (Key("a", "int", required=False), Key("b", "bool", role="a role"), Key("c", "int", low=1))
    assert read_object(keys, {"c": 4}, "x", {}) == {"c": 4}
    assert read_object(keys, {"c": 4, "b": True, "a": -2}, "x", {}) == {"a": -2, "b": True, "c": 4}
    with pytest.raises(ValueError, match=r"x lacks keys: c \(the keys: \['a', 'b', 'c'\]\)"):
        read_object(keys, {}, "x", {})
    with pytest.raises(ValueError, match=r"x has unknown keys: d, e \(the keys"):
        read_object(keys, {"c": 1, "e": 1, "d": 1}, "x", {})
    with pytest.raises(ValueError, match="the schema's key 'z' has the kind 'float', none of"):
        read_object((Key("z", "float"),), {"z": 1}, "x", {})
    # the folders' keys of a family in the folders' order, the name core's; the integers block core's
    assert [key.name for key in family_keys(discover())] == [
        "name",
        "clicks",
        "parts",
        "held",
        "pair",
        "phase",
        "self_source",
        "reads",
    ]
    assert UNIVERSE_INTEGERS == (
        "node_clock",
        "amplitude_bound",
        "Lambda",
        "momentum_unit",
        "twist_table",
    )
