"""Decode JSON documents once, before format-specific validation or execution."""

import json
import math


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _finite_number(source: str) -> float:
    value = float(source)
    if not math.isfinite(value):
        raise ValueError(f"non-finite JSON number {source!r}")
    return value


def parse_json_document(source: str | bytes) -> object:
    """Reject duplicate keys and non-finite numbers while retaining finite JSON values."""
    document: object = json.loads(
        source,
        object_pairs_hook=_unique_object,
        parse_float=_finite_number,
        parse_constant=_finite_number,
    )
    return document
