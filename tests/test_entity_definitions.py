"""Literal placement, dependency provenance and refusal before physical execution."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe.configuration_validation import validate_configuration
from event_universe.events.world import parse_ray_world
from event_universe.world_loading import BUNDLE_FORMAT, DocumentSyntaxError, load_world, main


def authored():
    return {
        "law": "rays",
        "model_id": "entity-placement-test",
        "shape": [9, 9, 1],
        "ticks": 1,
        "K": 32,
        "N": 32,
        "release": 0,
        "suspension": 0,
        "families": [{"name": "carrier", "kind": "paid"}],
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
    assert loaded.world == parse_ray_world(expanded)


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
    assert loaded.world == parse_ray_world(plain)
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
        (lambda world: world["entities"][0].update(position=[7, 4, 0]), "outside the board"),
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
    assert loaded.world == parse_ray_world(plain)
    assert json.loads(loaded.expanded_source)["model_id"] == chr(0xD800)
