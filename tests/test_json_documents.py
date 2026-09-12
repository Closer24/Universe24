"""Strict decoding is shared by inputs, editor fragments and observer files."""

import json
from pathlib import Path

import pytest

from event_universe.initialization import (
    parse_initial_json,
    parse_initial_state,
)
from event_universe.initialization import (
    parse_json_document as public_parse_json_document,
)
from event_universe.json_documents import parse_json_document
from event_universe.observer_configuration import ObserverDefinition
from event_universe.runner import run_initialization

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity", "1e309", "-1e309", "1.0e400"])
@pytest.mark.parametrize("nested", [False, True])
@pytest.mark.parametrize("as_bytes", [False, True])
def test_nonfinite_numbers_are_rejected_at_every_document_depth(token, nested, as_bytes):
    source = '{"draft": [0, {"value": ' + token + "}]}" if nested else token
    if as_bytes:
        source = source.encode("utf-8")
    with pytest.raises(ValueError, match="non-finite JSON number"):
        parse_json_document(source)


@pytest.mark.parametrize(
    "source",
    [
        '{"name": 1, "name": 2}',
        '{"draft": [{"name": 1, "name": 2}]}',
        r'{"name": 1, "\u006eame": 2}',
    ],
)
def test_duplicate_keys_are_rejected_including_decoded_escapes(source):
    with pytest.raises(ValueError, match="duplicate JSON key 'name'"):
        parse_json_document(source)


@pytest.mark.parametrize("as_bytes", [False, True])
def test_finite_editor_data_strings_and_large_integers_keep_standard_json_values(as_bytes):
    integer = 10**400
    source = (
        '{"NaN": "Infinity", "label": "-Infinity", "nested": [null, true, false], '
        '"fractions": [1.25, -0.5, 1e308, 1e-309], "count": ' + str(integer) + "}"
    )
    if as_bytes:
        source = source.encode("utf-8")
    result = parse_json_document(source)
    assert result == {
        "NaN": "Infinity",
        "label": "-Infinity",
        "nested": [None, True, False],
        "fractions": [1.25, -0.5, 1e308, 1e-309],
        "count": integer,
    }
    assert type(result["count"]) is int
    assert all(type(value) is float for value in result["fractions"])


@pytest.mark.parametrize("source, expected", [('"NaN"', "NaN"), ("17", 17), ("-0.25", -0.25)])
def test_scalar_editor_fragments_remain_valid(source, expected):
    assert parse_json_document(source) == expected


def test_initialization_reexports_the_shared_decoder():
    assert public_parse_json_document is parse_json_document


@pytest.mark.parametrize("name", ["basic.json", "exchange.json"])
def test_complete_valid_initializations_keep_their_independent_decoded_values(name):
    source = (EXAMPLES / name).read_bytes()
    independent_document = json.loads(source)
    assert parse_json_document(source) == independent_document
    assert parse_initial_json(source) == parse_initial_state(independent_document)


@pytest.mark.parametrize(
    "observer_source, key",
    [
        ('{"position": [0, 0, 0], "position": [1, 2, 0]}', "position"),
        ('{"position": [1, 2, 0], "max_receipts": 3, "max_receipts": 4}', "max_receipts"),
    ],
)
def test_inline_and_external_observers_reject_identical_duplicate_keys(tmp_path, observer_source, key):
    observer_path = tmp_path / "observer.json"
    observer_path.write_text(observer_source, encoding="utf-8")
    source = (EXAMPLES / "basic.json").read_text(encoding="utf-8").rstrip()
    inline_source = source[:-1] + ', "observer": ' + observer_source + "}"
    with pytest.raises(ValueError, match=f"duplicate JSON key '{key}'") as inline:
        parse_initial_json(inline_source)
    with pytest.raises(ValueError, match=f"duplicate JSON key '{key}'") as external:
        ObserverDefinition.load(observer_path, (17, 17, 17))
    assert str(inline.value) == str(external.value)
    assert observer_path.read_text(encoding="utf-8") == observer_source
    assert sorted(path.name for path in tmp_path.iterdir()) == ["observer.json"]


@pytest.mark.parametrize("location", ["inline", "external"])
@pytest.mark.parametrize(
    "observer_source, message",
    [
        ('{"position": [0, 0, 0], "position": [1, 2, 0]}', "duplicate JSON key"),
        ('{"position": [0, 0, 0], "max_receipts": NaN}', "non-finite JSON number"),
        ('{"position": [0, 0, 0], "max_receipts": Infinity}', "non-finite JSON number"),
        ('{"position": [0, 0, 0], "max_receipts": -Infinity}', "non-finite JSON number"),
        ('{"position": [0, 0, 0], "max_receipts": 1e309}', "non-finite JSON number"),
    ],
)
def test_invalid_observer_input_creates_no_run_output(tmp_path, location, observer_source, message):
    source = (EXAMPLES / "basic.json").read_text(encoding="utf-8").rstrip()
    input_path = tmp_path / "input.json"
    observer_path = None
    if location == "inline":
        source = source[:-1] + ', "observer": ' + observer_source + "}"
    else:
        observer_path = tmp_path / "observer.json"
        observer_path.write_text(observer_source, encoding="utf-8")
    input_path.write_text(source, encoding="utf-8")
    before = {path.name: path.read_bytes() for path in tmp_path.iterdir()}
    with pytest.raises(ValueError, match=message):
        run_initialization(input_path, tmp_path / "output", observer=observer_path)
    assert {path.name: path.read_bytes() for path in tmp_path.iterdir()} == before


def test_valid_observer_loading_preserves_explicit_definition_without_writes(tmp_path):
    path = tmp_path / "observer.json"
    source = '{"position": [1, 2, 0], "max_receipts": 3}'
    path.write_text(source, encoding="utf-8")
    assert ObserverDefinition.load(path, (3, 3, 3)) == ObserverDefinition((1, 2, 0), 3)
    assert path.read_text(encoding="utf-8") == source
    assert list(tmp_path.iterdir()) == [path]


@pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig", "utf-16", "utf-32"])
def test_observer_file_uses_the_same_byte_decoding_as_initialization(tmp_path, encoding):
    raw = {"position": [0, 0, 0], "max_receipts": 3}
    source = json.dumps(raw).encode(encoding)
    path = tmp_path / "observer.json"
    path.write_bytes(source)
    expected = ObserverDefinition((0, 0, 0), 3)
    assert ObserverDefinition.parse(parse_json_document(source), (3, 3, 3)) == expected
    assert ObserverDefinition.load(path, (3, 3, 3)) == expected
    assert path.read_bytes() == source
