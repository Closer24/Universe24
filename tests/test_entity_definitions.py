"""Literal placement, dependency provenance and refusal before physical execution."""

import hashlib
import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe.configuration_validation import validate_configuration
from event_universe.events import NatureBeamSimulation
from event_universe.events.world import parse_nature_beam_world
from event_universe.world_loading import BUNDLE_FORMAT, DocumentSyntaxError, load_world, main


def authored():
    return {
        "law": "beam",
        "model_id": "entity-placement-test",
        "shape": [9, 9, 1],
        "ticks": 1,
        "K": 32,
        "N": 32,
        "release": 0,
        "suspension": 0,
        "families": [{"name": "carrier", "quantum": 1}],
        "entity_definitions": "entities/apparatus.json",
        "entities": [{"name": "alice", "definition": "three", "position": [3, 4, 0]}],
    }


def definitions():
    positions = [[0, 0, 0], [1, 0, 0], [2, 0, 0]]
    return {
        "format": "event-entities-v1",
        "entities": [
            {
                "name": "three",
                "measured": [
                    {
                        "position": position,
                        "family": "carrier",
                        "amount": 1,
                        "fixed": True,
                        "table": {"carrier": "measure"},
                    }
                    for position in positions
                ],
                "detectors": [{"name": "readout", "positions": positions, "threshold": 2}],
            }
        ],
    }


def bundle(world=None, entities=None):
    world = authored() if world is None else world
    return json.dumps(
        {
            "format": BUNDLE_FORMAT,
            "world": world,
            "definitions": {
                world["entity_definitions"]: json.dumps(definitions() if entities is None else entities)
            },
        }
    )


def test_positions_order_outputs_and_names_are_literal():
    world = authored()
    world["entities"].append({"name": "bob", "definition": "three", "position": [3, 6, 0]})
    loaded = load_world(bundle(world))
    assert [event.position for event in loaded.world.measured] == [
        (3, 4, 0),
        (4, 4, 0),
        (5, 4, 0),
        (3, 6, 0),
        (4, 6, 0),
        (5, 6, 0),
    ]
    assert [detector.name for detector in loaded.world.detectors] == ["/alice/readout", "/bob/readout"]
    assert [detector.threshold for detector in loaded.world.detectors] == [2, 2]
    expanded = json.loads(loaded.expanded_source)
    assert "entities" not in expanded and "entity_definitions" not in expanded
    assert loaded.world == parse_nature_beam_world(expanded)


@pytest.mark.parametrize(
    "name,escaped", [("a/b~c", "a~1b~0c"), ("__proto__", "__proto__"), ("pass", "pass")]
)
def test_names_only_change_labels(name, escaped):
    original = load_world(bundle()).world
    world = authored()
    world["entities"][0]["name"] = name
    renamed = load_world(bundle(world)).world
    assert renamed.measured == original.measured and renamed.in_transit == original.in_transit
    assert renamed.detectors[0].name == f"/{escaped}/readout"
    assert renamed.detectors[0].positions == original.detectors[0].positions


def test_inline_entries_precede_instances_and_negative_offsets_are_translated_once():
    world, entities = authored(), definitions()
    world["measured"] = [
        {
            "position": [0, 0, 0],
            "family": "carrier",
            "amount": 1,
            "fixed": True,
            "table": {"carrier": "pass"},
        }
    ]
    for event in entities["entities"][0]["measured"]:
        event["position"][0] -= 1
    loaded = load_world(bundle(world, entities)).world
    assert [event.position for event in loaded.measured] == [(0, 0, 0), (2, 4, 0), (3, 4, 0), (4, 4, 0)]


def test_dependency_bytes_and_bundle_survive_relocation_without_file_reads(tmp_path, monkeypatch):
    path = tmp_path / "entities" / "apparatus.json"
    path.parent.mkdir()
    raw = (json.dumps(definitions(), indent=3) + "\n\n").encode()
    path.write_bytes(raw)
    loaded = load_world(json.dumps(authored()), base_dir=tmp_path)
    assert loaded.dependencies[0].source == raw
    assert loaded.dependencies[0].sha256 == hashlib.sha256(raw).hexdigest()
    assert loaded.dependencies[0].path == "entities/apparatus.json"
    path.unlink()

    def no_files(*args, **kwargs):
        raise AssertionError("portable input must not read files")

    monkeypatch.setattr(Path, "read_bytes", no_files)
    relocated = load_world(loaded.portable_source, base_dir=tmp_path / "elsewhere")
    assert relocated == loaded
    assert relocated.portable_source.endswith(b"\n")


@pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig", "utf-16", "utf-32"])
def test_plain_world_keeps_decoder_behavior_and_exact_source(encoding):
    plain = json.loads(load_world(bundle()).expanded_source)
    raw = json.dumps(plain, indent=2).encode(encoding)
    loaded = load_world(raw)
    assert loaded.world == parse_nature_beam_world(plain)
    assert loaded.portable_source == raw and loaded.dependencies == ()


@pytest.mark.parametrize(
    "reference", ["/absolute.json", "../escape.json", "a/../b", "a//b", "./a", "a\\b", "https:x", ""]
)
def test_reference_paths_are_confined(reference, tmp_path):
    world = authored()
    world["entity_definitions"] = reference
    with pytest.raises(ValueError, match="entity_definitions"):
        load_world(json.dumps(world), base_dir=tmp_path)


def test_missing_context_io_and_symlink_escape_are_distinct(tmp_path):
    source = json.dumps(authored())
    with pytest.raises(ValueError, match="explicit base_dir"):
        load_world(source)
    with pytest.raises(OSError):
        load_world(source, base_dir=tmp_path)
    assert validate_configuration(source, base_dir=tmp_path).issues[0].code == "io"
    outside = tmp_path / "outside.json"
    outside.write_text(json.dumps(definitions()))
    base = tmp_path / "base"
    (base / "entities").mkdir(parents=True)
    (base / "entities" / "apparatus.json").symlink_to(outside)
    with pytest.raises(ValueError, match="outside base_dir"):
        load_world(source, base_dir=base)


@pytest.mark.parametrize(
    "change,expected",
    [
        (lambda world: world.pop("entities"), "together"),
        (lambda world: world.update(entities=[]), "at least one placement"),
        (lambda world: world["entities"][0].update(position=[True, 0, 0]), "three-integer"),
        (lambda world: world["entities"][0].update(position=[7, 4, 0]), "outside the GameBoard"),
        (lambda world: world["entities"][0].update(definition="missing"), "unknown definition"),
        (lambda world: world["entities"].append(deepcopy(world["entities"][0])), "duplicate instance"),
        (
            lambda world: world["entities"].append(
                {"name": "bob", "definition": "three", "position": [3, 4, 0]}
            ),
            "measured",
        ),
    ],
)
def test_invalid_placements_are_refused_without_clipping(change, expected):
    world = authored()
    world["boundary"] = {"x": "periodic"}
    change(world)
    with pytest.raises(ValueError, match=expected):
        load_world(bundle(world))


@pytest.mark.parametrize(
    "change,expected",
    [
        (lambda entity: entity.update(callback="run()"), "unsupported keys"),
        (lambda entity: entity["measured"][0].update(expression="x+1"), "unsupported keys"),
        (lambda entity: entity["measured"][0].update(position=[4096, 0, 0]), "-4095..4095"),
        (
            lambda entity: entity["measured"].append(deepcopy(entity["measured"][0])),
            "duplicate relative",
        ),
        (
            lambda entity: entity["detectors"][0].update(positions=[[3, 0, 0]]),
            "measured geometry",
        ),
        (lambda entity: entity["measured"][0].update(lamp={"formula": "x"}), "unsupported keys"),
        (
            lambda entity: entity["measured"][0].update(
                table={"carrier": {"rule": "pass", "formula": "x"}}
            ),
            "unsupported keys",
        ),
    ],
)
def test_unused_definitions_still_receive_structural_validation(change, expected):
    entities = definitions()
    unused = deepcopy(entities["entities"][0])
    unused["name"] = "unused"
    change(unused)
    entities["entities"].append(unused)
    with pytest.raises(ValueError, match=expected):
        load_world(bundle(entities=entities))


def test_physical_semantics_stay_in_the_canonical_world_parser():
    entities = definitions()
    entities["entities"][0]["measured"][0]["family"] = "unknown"
    with pytest.raises(ValueError, match="family"):
        load_world(bundle(entities=entities))
    entities = definitions()
    entities["entities"][0]["detectors"][0]["threshold"] = 0
    with pytest.raises(ValueError, match="threshold"):
        load_world(bundle(entities=entities))


@pytest.mark.parametrize(
    "change",
    [
        lambda document: document["definitions"].update(extra="{}"),
        lambda document: document.update(definitions={}),
        lambda document: document["definitions"].update({"entities/apparatus.json": {}}),
        lambda document: document.update(world={"format": BUNDLE_FORMAT}),
        lambda document: document.update(world={"law": "events"}),
    ],
)
def test_bundles_require_the_exact_literal_dependency_closure(change):
    document = json.loads(bundle())
    change(document)
    with pytest.raises(ValueError):
        load_world(json.dumps(document))


@pytest.mark.parametrize("raw", ['{"format": 1, "format": 2}', "{", '{"entities": NaN}'])
def test_dependency_decode_errors_keep_syntax_context(raw):
    document = json.loads(bundle())
    document["definitions"]["entities/apparatus.json"] = raw
    source = json.dumps(document)
    with pytest.raises(DocumentSyntaxError) as failure:
        load_world(source)
    assert failure.value.document == "entities/apparatus.json"
    report = validate_configuration(source)
    assert not report.valid and report.issues[0].code == "syntax"
    assert report.issues[0].document == "entities/apparatus.json"
    if raw == "{":
        assert report.issues[0].line == 1 and report.issues[0].column == 2


@pytest.mark.parametrize("encoding", ["utf-8-sig", "utf-16"])
def test_entity_authoring_refuses_noncanonical_encodings(encoding):
    with pytest.raises(DocumentSyntaxError, match="UTF-8"):
        load_world(bundle().encode(encoding))


def test_limits_apply_to_sources_and_projected_expansion_before_world_parsing():
    with pytest.raises(ValueError, match="1 MiB"):
        load_world(bundle() + " " * (1 << 20))
    entities, world = definitions(), authored()
    entities["entities"][0]["detectors"][0]["name"] = "r" * 100_000
    world["entities"] = [
        {"name": str(index), "definition": "three", "position": [3, 4, 0]} for index in range(200)
    ]
    with pytest.raises(ValueError, match="16 MiB"):
        load_world(bundle(world, entities))


def test_export_cli_validates_and_refuses_overwrite(tmp_path):
    source, output = tmp_path / "world.json", tmp_path / "portable.json"
    source.write_text(bundle())
    assert main(["--input", str(source), "--output", str(output)]) == 0
    original = output.read_bytes()
    assert load_world(original).portable_source == original
    with pytest.raises(SystemExit) as error:
        main(["--input", str(source), "--output", str(output)])
    assert error.value.code == 1 and output.read_bytes() == original


def test_plain_escaped_surrogate_names_keep_the_existing_parser_domain():
    plain = json.loads(load_world(bundle()).expanded_source)
    plain["model_id"] = chr(0xD800)
    source = json.dumps(plain).encode("ascii")
    loaded = load_world(source)
    assert loaded.portable_source == source
    assert loaded.world == parse_nature_beam_world(plain)
    assert json.loads(loaded.expanded_source)["model_id"] == chr(0xD800)


# -- families in definitions (event-entities-v2, 2026-09-20) -------------------------
#
# The model owner's decision of 2026-09-20 (record 113): one canonical
# definition per family, referenced by the worlds. A definition of the
# second format may carry `families`, merged into the expanded world by name:
# (v2-a) the inline families first, then each instance's in declaration
# order, a name already present kept when its keys agree; (v2-b) a differing
# key is refused naming the family and the key; (v2-c) a definition of a
# family alone (no measured Event) is admitted; (v2-d) a world whose
# families come from a definition expands to the same bytes and the same
# parsed world as the inline world, and runs the same; (v2-e) the first
# format refuses `families`; (v2-f) every shipped definition of
# `examples/events/entities/` places and parses, every family of the
# register is defined once, and the files are their generator's.

ROOT = Path(__file__).resolve().parents[1]
ENTITIES = ROOT / "examples" / "events" / "entities"
EXAMPLES = ROOT / "examples" / "events"


def versioned(families=None, measured=None, detectors=None, name="three"):
    """A second-format definitions document with one definition."""
    return {
        "format": "event-entities-v2",
        "entities": [
            {
                "name": name,
                "families": [] if families is None else families,
                "measured": [] if measured is None else measured,
                "detectors": [] if detectors is None else detectors,
            }
        ],
    }


def placed(world, entities):
    return load_world(bundle(world, entities))


def test_families_of_a_definition_merge_into_the_world_by_name():
    """(v2-a): inline first, then the instances' in order; an agreeing repeat kept once."""
    world = authored()
    world["families"] = [{"name": "carrier", "quantum": 1}]
    world["entities"] = [
        {"name": "a", "definition": "three", "position": [1, 1, 0]},
        {"name": "b", "definition": "three", "position": [5, 5, 0]},
    ]
    entities = versioned(
        families=[{"name": "carrier", "quantum": 1}, {"name": "dust", "quantum": 0, "phase": False}],
        measured=[{"position": [0, 0, 0], "family": "dust", "amount": 2, "fixed": True}],
    )
    loaded = placed(world, entities)
    assert [family.name for family in loaded.world.families] == ["carrier", "dust"]
    assert json.loads(loaded.expanded_source)["families"] == [
        {"name": "carrier", "quantum": 1},
        {"name": "dust", "quantum": 0, "phase": False},
    ]
    assert [event.position for event in loaded.world.measured] == [(1, 1, 0), (5, 5, 0)]


@pytest.mark.parametrize(
    "inline,declared,key",
    [
        ({"name": "carrier", "quantum": 1}, {"name": "carrier", "quantum": 2}, "quantum"),
        ({"name": "carrier", "quantum": 1}, {"name": "carrier", "quantum": 1, "phase": True}, "phase"),
        ({"name": "carrier", "quantum": 1, "charge": 0}, {"name": "carrier", "quantum": 1}, "charge"),
    ],
)
def test_a_differing_key_is_refused_naming_the_family_and_the_key(inline, declared, key):
    """(v2-b)."""
    world = authored()
    world["families"] = [inline]
    entities = versioned(families=[declared])
    with pytest.raises(ValueError, match=f"family 'carrier'.*different key '{key}'"):
        placed(world, entities)
    # Two instances of two definitions that disagree are refused the same way.
    world["families"] = []
    world["entities"] = [
        {"name": "a", "definition": "three", "position": [1, 1, 0]},
        {"name": "b", "definition": "other", "position": [5, 5, 0]},
    ]
    entities["entities"].append({**versioned(families=[inline], name="other")["entities"][0]})
    with pytest.raises(ValueError, match=f"family 'carrier'.*different key '{key}'"):
        placed(world, entities)


def test_a_definition_of_a_family_alone_is_admitted():
    """(v2-c): no measured Event, no detector; the family reaches the world."""
    world = authored()
    del world["families"]
    world["measured"] = [
        {
            "position": [0, 0, 0],
            "family": "carrier",
            "amount": 1,
            "fixed": True,
            "table": {"carrier": "pass"},
        }
    ]
    loaded = placed(world, versioned(families=[{"name": "carrier", "quantum": 1}]))
    assert [family.name for family in loaded.world.families] == ["carrier"]
    assert len(loaded.world.measured) == 1
    # Without a family the empty definition is still refused, as in the first format.
    with pytest.raises(ValueError, match="at least one Event"):
        placed(authored(), versioned())


def test_a_world_from_a_definition_expands_to_the_inline_bytes_and_runs_the_same():
    """(v2-d): the same expanded document, the same parsed world, the same records."""
    event = {
        "position": [4, 4, 0],
        "family": "carrier",
        "amount": 1,
        "fixed": True,
        "table": {"carrier": "measure"},
    }
    inline = authored()
    del inline["entity_definitions"], inline["entities"]
    inline["measured"] = [event]
    world = authored()
    del world["families"]
    world["entities"] = [{"name": "the", "definition": "three", "position": [4, 4, 0]}]
    entities = versioned(
        families=[{"name": "carrier", "quantum": 1}],
        measured=[{**event, "position": [0, 0, 0]}],
    )
    defined = placed(world, entities)
    plain = load_world(json.dumps(inline).encode("utf-8"))
    assert json.loads(defined.expanded_source) == {**inline, "detectors": []}
    assert defined.world == plain.world == parse_nature_beam_world(inline)
    records = []
    for loaded in (plain, defined):
        lines = []
        simulation = NatureBeamSimulation(loaded.world, lines.append)
        for _ in range(3):
            simulation.step()
        records.append((lines, simulation.books(), simulation.snapshot()))
    assert records[0] == records[1]


def test_a_table_entry_of_a_window_alone_is_admitted_in_a_definition():
    """A definition's table entry may omit `rule`, as a world's may: the
    family's default rule applies (the world parser's contract)."""
    entities = definitions()
    entities["entities"][0]["measured"][0]["table"] = {"carrier": {"phase_window": 0}}
    loaded = load_world(bundle(None, entities))
    assert len(loaded.world.measured) == 3
    entities["entities"][0]["measured"][0]["table"] = {"carrier": {"phase_window": 0, "formula": "x"}}
    with pytest.raises(ValueError, match="unsupported keys"):
        load_world(bundle(None, entities))


def test_the_first_format_refuses_families_and_keeps_its_rules():
    """(v2-e)."""
    entities = definitions()
    entities["entities"][0]["families"] = [{"name": "carrier", "quantum": 1}]
    with pytest.raises(ValueError, match="unsupported keys"):
        load_world(bundle(entities=entities))
    entities = versioned(families=[{"name": "carrier", "quantum": 1, "formula": "x"}])
    with pytest.raises(ValueError, match="unsupported keys"):
        load_world(bundle(entities=entities))
    entities = versioned(families=[{"name": "carrier", "quantum": 1}, {"name": "carrier", "quantum": 1}])
    with pytest.raises(ValueError, match="duplicate family name"):
        load_world(bundle(entities=entities))
    entities = versioned()
    entities["format"] = "event-entities-v3"
    with pytest.raises(ValueError, match="format must be"):
        load_world(bundle(entities=entities))


def shipped_definitions(name: str) -> dict[str, object]:
    return json.loads((ENTITIES / name).read_text(encoding="utf-8"))


def register_family_names() -> set[str]:
    names: set[str] = set()
    for path in sorted(EXAMPLES.rglob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(document, dict) and isinstance(document.get("families"), list):
            names.update(str(family["name"]) for family in document["families"])
    return names


def test_the_shipped_definitions_are_the_generators_and_define_every_family_once():
    """(v2-f): the files equal `make_definitions.py`'s documents; the 47 names once."""
    path = ENTITIES / "make_definitions.py"
    spec = importlib.util.spec_from_file_location("entities_make_definitions", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["entities_make_definitions"] = module
    spec.loader.exec_module(module)
    assert shipped_definitions("families.json") == module.families()
    assert shipped_definitions("apparatus.json") == module.apparatus()
    defined = [
        family["name"]
        for entity in shipped_definitions("families.json")["entities"]
        for family in entity["families"]
    ]
    assert len(defined) == len(set(defined))
    assert set(defined) == register_family_names()


def entity_world(reference: str, definition: str, position: list[int]) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "entities-placement-test",
        "shape": [9, 9, 3],
        "ticks": 3,
        "K": 4096,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1}],
        "entity_definitions": reference,
        "entities": [{"name": "it", "definition": definition, "position": position}],
    }


@pytest.mark.parametrize("reference", ["entities/families.json", "entities/apparatus.json"])
def test_every_shipped_definition_places_parses_and_runs(reference):
    """(v2-f): each definition placed alone in a small world of `K` 4096 parses through the canonical loader and runs three
    intervals with the books balanced."""
    for entity in shipped_definitions(Path(reference).name)["entities"]:
        world = entity_world(reference, entity["name"], [4, 4, 1])
        loaded = load_world(json.dumps(world).encode("utf-8"), base_dir=EXAMPLES)
        names = [family.name for family in loaded.world.families]
        assert names[0] == "light" and len(names) == len(set(names)), entity["name"]
        for family in entity["families"]:
            assert family["name"] in names, entity["name"]
        assert len(loaded.world.measured) == len(entity["measured"]), entity["name"]
        simulation = NatureBeamSimulation(loaded.world)
        for _ in range(3):
            simulation.step()
            assert simulation.books()["balanced"], entity["name"]
