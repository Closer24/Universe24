"""Resolve literal entity definitions into one ordinary, portable event world.

This host adapter owns files and placement, never physical rules or runtime state.
See docs/ENTITY_DEFINITIONS.md for the versioned authoring and bundle contracts.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from event_universe.events.world import (
    DETECTOR_GROUP_KEYS,
    DETECTOR_KEYS,
    LAMP_KEYS,
    MEASURED_KEYS,
    TABLE_ENTRY_KEYS,
    EventWorld,
    parse_event_world,
)
from event_universe.json_documents import parse_json_document

ENTITIES_FORMAT = "event-entities-v1"
BUNDLE_FORMAT = "event-world-bundle-v1"
SOURCE_LIMIT = 1 << 20
EXPANDED_LIMIT = 16 << 20
_AUTHOR_KEYS = {"entity_definitions", "entities"}


@dataclass(frozen=True)
class DefinitionSource:
    path: str
    source: bytes
    sha256: str


@dataclass(frozen=True)
class LoadedWorld:
    world: EventWorld
    portable_source: bytes
    expanded_source: bytes
    dependencies: tuple[DefinitionSource, ...]


class DocumentSyntaxError(ValueError):
    """A strict decoding failure, preserving the source and JSON coordinates."""

    def __init__(
        self, document: str, message: str, line: int | None = None, column: int | None = None
    ) -> None:
        super().__init__(message)
        self.document = document
        self.line = line
        self.column = column


def _decode(source: str | bytes, document: str) -> object:
    try:
        if not isinstance(source, (str, bytes)):
            raise ValueError("configuration source must be JSON text or bytes")
        return parse_json_document(source)
    except json.JSONDecodeError as error:
        raise DocumentSyntaxError(document, error.msg, error.lineno, error.colno) from error
    except RecursionError as error:
        raise DocumentSyntaxError(document, "JSON nesting exceeds the supported depth") from error
    except ValueError as error:
        raise DocumentSyntaxError(document, str(error)) from error


def _encode(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode(
        "utf-8", errors="backslashreplace"
    )


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _array(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return cast(list[object], value)


def _name(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _keys(value: dict[str, object], allowed: set[str], required: set[str], label: str) -> None:
    extra, missing = value.keys() - allowed, required - value.keys()
    if extra:
        raise ValueError(f"{label}: unsupported keys {sorted(extra)}")
    if missing:
        raise ValueError(f"{label}: missing keys {sorted(missing)}")


def _triple(value: object, label: str) -> tuple[int, int, int]:
    items = _array(value, label)
    if len(items) != 3 or any(type(item) is not int for item in items):
        raise ValueError(f"{label} must be an exact three-integer position")
    return cast(tuple[int, int, int], tuple(items))


def _relative(value: object, label: str) -> tuple[int, int, int]:
    result = _triple(value, label)
    if any(abs(item) > 4095 for item in result):
        raise ValueError(f"{label} must be within -4095..4095")
    return result


def _utf8(source: bytes, label: str) -> str:
    if len(source) > SOURCE_LIMIT:
        raise ValueError(f"{label} exceeds the 1 MiB source limit")
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as error:
        raise DocumentSyntaxError(label, "document must be UTF-8 without a byte-order mark") from error
    if text.startswith("\ufeff"):
        raise DocumentSyntaxError(label, "document must be UTF-8 without a byte-order mark")
    return text


def _reference(value: object) -> str:
    path = _name(value, "entity_definitions")
    if "\\" in path or ":" in path or any(part in ("", ".", "..") for part in path.split("/")):
        raise ValueError("entity_definitions must be a relative POSIX path without traversal")
    return path


def _definition_geometry(definition: dict[str, object], label: str) -> None:
    measured = _array(definition["measured"], f"{label}.measured")
    if not measured:
        raise ValueError(f"{label}.measured must contain at least one Event")
    geometry: set[tuple[int, int, int]] = set()
    for index, raw in enumerate(measured):
        entry_label = f"{label}.measured[{index}]"
        entry = _object(raw, entry_label)
        _keys(entry, MEASURED_KEYS | {"port_map"}, {"position"}, entry_label)
        position = _relative(entry["position"], f"{entry_label}.position")
        if position in geometry:
            raise ValueError(f"{entry_label}: duplicate relative measured position {position}")
        geometry.add(position)
        if "family" in entry:
            _name(entry["family"], f"{entry_label}.family")
        for key in ("momentum", "port_map"):
            if key in entry:
                _array(entry[key], f"{entry_label}.{key}")
        if "lamp" in entry:
            lamp_label = f"{entry_label}.lamp"
            lamp = _object(entry["lamp"], lamp_label)
            _keys(lamp, LAMP_KEYS, set(), lamp_label)
            for key in ("rate", "headings"):
                if key in lamp:
                    _array(lamp[key], f"{lamp_label}.{key}")
        if "table" in entry:
            table = _object(entry["table"], f"{entry_label}.table")
            for family, rule in table.items():
                _name(family, f"{entry_label}.table family")
                if isinstance(rule, dict):
                    _keys(rule, TABLE_ENTRY_KEYS, {"rule"}, f"{entry_label}.table.{family}")
                    _name(rule["rule"], f"{entry_label}.table.{family}.rule")
                else:
                    _name(rule, f"{entry_label}.table.{family}")
    names: set[str] = set()
    for index, raw in enumerate(_array(definition["detectors"], f"{label}.detectors")):
        detector_label = f"{label}.detectors[{index}]"
        detector = _object(raw, detector_label)
        _keys(detector, DETECTOR_KEYS | {"groups"}, {"name", "positions"}, detector_label)
        name = _name(detector["name"], f"{detector_label}.name")
        if name in names:
            raise ValueError(f"{detector_label}: duplicate detector name {name!r}")
        names.add(name)
        _check_geometry(detector["positions"], geometry, f"{detector_label}.positions")
        if "groups" in detector:
            group_names: set[str] = set()
            for group_raw in _array(detector["groups"], f"{detector_label}.groups"):
                group = _object(group_raw, f"{detector_label}.groups")
                _keys(group, DETECTOR_GROUP_KEYS, {"name", "positions", "output"}, detector_label)
                group_name = _name(group["name"], f"{detector_label}.group.name")
                if group_name in group_names:
                    raise ValueError(f"{detector_label}: duplicate group name {group_name!r}")
                group_names.add(group_name)
                _check_geometry(group["positions"], geometry, f"{detector_label}.group.positions")
                _check_geometry([group["output"]], geometry, f"{detector_label}.group.output")


def _check_geometry(value: object, geometry: set[tuple[int, int, int]], label: str) -> None:
    for raw in _array(value, label):
        position = _relative(raw, label)
        if position not in geometry:
            raise ValueError(
                f"{label}: {position} does not refer to this definition's measured geometry"
            )


def _definitions(source: bytes, path: str) -> dict[str, dict[str, object]]:
    text = _utf8(source, path)
    document = _object(_decode(text, path), path)
    _keys(document, {"format", "entities"}, {"format", "entities"}, path)
    if document["format"] != ENTITIES_FORMAT:
        raise ValueError(f"{path}.format must be {ENTITIES_FORMAT!r}")
    result: dict[str, dict[str, object]] = {}
    for index, raw in enumerate(_array(document["entities"], f"{path}.entities")):
        label = f"{path}.entities[{index}]"
        definition = _object(raw, label)
        _keys(definition, {"name", "measured", "detectors"}, {"name", "measured", "detectors"}, label)
        name = _name(definition["name"], f"{label}.name")
        if name in result:
            raise ValueError(f"{label}: duplicate definition name {name!r}")
        _definition_geometry(definition, label)
        result[name] = definition
    return result


def _placements(
    document: dict[str, object], definitions: dict[str, dict[str, object]]
) -> list[tuple[str, tuple[int, int, int], dict[str, object]]]:
    shape = _triple(document.get("shape"), "world.shape")
    instances = _array(document["entities"], "world.entities")
    if not instances:
        raise ValueError("world.entities must contain at least one placement")
    names: set[str] = set()
    result: list[tuple[str, tuple[int, int, int], dict[str, object]]] = []
    for index, raw in enumerate(instances):
        label = f"world.entities[{index}]"
        instance = _object(raw, label)
        _keys(instance, {"name", "definition", "position"}, {"name", "definition", "position"}, label)
        name = _name(instance["name"], f"{label}.name")
        if name in names:
            raise ValueError(f"{label}: duplicate instance name {name!r}")
        names.add(name)
        definition_name = _name(instance["definition"], f"{label}.definition")
        if definition_name not in definitions:
            raise ValueError(f"{label}: unknown definition {definition_name!r}")
        origin = _triple(instance["position"], f"{label}.position")
        if any(not 0 <= value < extent for value, extent in zip(origin, shape, strict=True)):
            raise ValueError(f"{label}.position is outside the board")
        result.append((name, origin, definitions[definition_name]))
    return result


def _translated(
    value: object, origin: tuple[int, int, int], shape: tuple[int, int, int], label: str
) -> list[int]:
    relative = _relative(value, label)
    result = [a + b for a, b in zip(relative, origin, strict=True)]
    if any(not 0 <= value < extent for value, extent in zip(result, shape, strict=True)):
        raise ValueError(f"instance {label}: translated position {result} is outside the board")
    return result


def _escape(name: str) -> str:
    return name.replace("~", "~0").replace("/", "~1")


def _entries(
    document: dict[str, object],
    placements: list[tuple[str, tuple[int, int, int], dict[str, object]]],
    kind: str,
) -> Iterator[object]:
    yield from _array(document.get(kind, []), f"world.{kind}")
    shape = _triple(document["shape"], "world.shape")
    for name, origin, definition in placements:
        for raw in _array(definition[kind], kind):
            entry = copy.deepcopy(_object(raw, kind))
            if kind == "measured":
                entry["position"] = _translated(entry["position"], origin, shape, name)
            else:
                entry["name"] = f"/{_escape(name)}/{_escape(cast(str, entry['name']))}"
                entry["positions"] = [
                    _translated(position, origin, shape, name)
                    for position in _array(entry["positions"], name)
                ]
                for raw_group in _array(entry.get("groups", []), name):
                    group = _object(raw_group, name)
                    group["positions"] = [
                        _translated(position, origin, shape, name)
                        for position in _array(group["positions"], name)
                    ]
                    group["output"] = _translated(group["output"], origin, shape, name)
            yield entry


def _expand(document: dict[str, object], definitions: dict[str, dict[str, object]]) -> dict[str, object]:
    placements = _placements(document, definitions)
    expanded = {key: value for key, value in document.items() if key not in _AUTHOR_KEYS}
    expanded.update(measured=[], detectors=[])
    # Count exactly, one translated entry at a time, before allocating multiplied arrays.
    size = len(_encode(expanded))
    for kind in ("measured", "detectors"):
        for index, entry in enumerate(_entries(document, placements, kind)):
            size += len(_encode(entry)) - 1 + int(index > 0)
            if size > EXPANDED_LIMIT:
                raise ValueError("world.entities expansion exceeds the 16 MiB generated JSON limit")
    for kind in ("measured", "detectors"):
        expanded[kind] = list(_entries(document, placements, kind))
    return expanded


def load_world(source: str | bytes, *, base_dir: Path | None = None) -> LoadedWorld:
    """Load one world with explicit file context or a self-contained bundle."""
    decoded = _decode(source, "input")
    raw = source.encode("utf-8") if isinstance(source, str) else source
    document = _object(decoded, "input")
    bundled = document.get("format") == BUNDLE_FORMAT
    if not bundled and not (_AUTHOR_KEYS & document.keys()):
        world = parse_event_world(document)
        return LoadedWorld(world, raw, _encode(document), ())
    _utf8(raw, "input")
    supplied: dict[str, object] | None = None
    if bundled:
        _keys(document, {"format", "world", "definitions"}, {"format", "world", "definitions"}, "bundle")
        supplied = _object(document["definitions"], "bundle.definitions")
        document = _object(document["world"], "bundle.world")
        if "format" in document:
            raise ValueError("bundle.world must be an authored world, not a nested bundle")
    if not _AUTHOR_KEYS <= document.keys():
        raise ValueError("world requires entity_definitions and entities together")
    reference = _reference(document["entity_definitions"])
    if supplied is not None:
        if set(supplied) != {reference}:
            raise ValueError("bundle.definitions must contain exactly the referenced dependency")
        text = supplied[reference]
        if not isinstance(text, str):
            raise ValueError("bundle.definitions dependency must be its original UTF-8 JSON text")
        dependency = text.encode("utf-8")
    else:
        if base_dir is None:
            raise ValueError("entity_definitions requires an explicit base_dir or a portable bundle")
        base = base_dir.resolve()
        path = (base / reference).resolve()
        if not path.is_relative_to(base):
            raise ValueError("entity_definitions resolves outside base_dir")
        dependency = path.read_bytes()
    definitions = _definitions(dependency, reference)
    expanded_document = _expand(document, definitions)
    world = parse_event_world(expanded_document)
    expanded = _encode(expanded_document)
    portable = _encode(
        {
            "format": BUNDLE_FORMAT,
            "world": document,
            "definitions": {reference: dependency.decode("utf-8")},
        }
    )
    if len(portable) > SOURCE_LIMIT:
        raise ValueError("portable bundle exceeds the 1 MiB source limit")
    definition_source = DefinitionSource(reference, dependency, hashlib.sha256(dependency).hexdigest())
    return LoadedWorld(world, portable, expanded, (definition_source,))


def main(argv: list[str] | None = None) -> int:
    """Validate and export portable input without executing a world."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        loaded = load_world(args.input.read_bytes(), base_dir=args.input.parent)
        with args.output.open("xb") as output:
            output.write(loaded.portable_source)
    except (ValueError, OSError) as error:
        parser.exit(1, f"{error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
