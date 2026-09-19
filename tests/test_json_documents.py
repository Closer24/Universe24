"""Strict decoding is shared by world files and the workspace's editor fragments."""

import json
from pathlib import Path

import pytest

from event_universe.events import parse_event_world
from event_universe.json_documents import parse_json_document

WORLDS = Path(__file__).resolve().parents[1] / "examples" / "events"


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
        r'{"name": 1, "name": 2}',
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


@pytest.mark.parametrize("name", ["one_content.json", "two_slits.json"])
def test_shipped_worlds_decode_to_their_independent_values(name):
    source = (WORLDS / name).read_bytes()
    independent_document = json.loads(source)
    assert parse_json_document(source) == independent_document
    assert parse_event_world(parse_json_document(source)) == parse_event_world(independent_document)


@pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig", "utf-16", "utf-32"])
def test_world_files_decode_from_every_unicode_encoding(encoding):
    raw = json.loads((WORLDS / "one_content.json").read_text(encoding="utf-8"))
    source = json.dumps(raw).encode(encoding)
    assert parse_json_document(source) == raw
