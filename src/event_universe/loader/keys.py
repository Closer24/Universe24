"""The keys of the world's files as the loader reads them: an object with its allowed and required keys, an integer within its bounds, a Node inside the shape and on the board, a range of Nodes along an axis, and the document a world names by a repository path; every defect refused by name, no default written (ALGEBRA.md #a-familys-declaration)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from event_universe.core.integer import MAX_WORK_INT

Node = tuple[int, int, int]
AXES = ("x", "y", "z")


def keyed(
    value: object, label: str, allowed: tuple[str, ...], required: tuple[str, ...]
) -> dict[str, Any]:
    """An object of the files: every key it holds among `allowed` and every key of `required` present, refused by name otherwise."""
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    unknown = sorted(set(value) - set(allowed))
    if unknown:
        raise ValueError(f"{label} holds the unknown key {unknown[0]!r}: its keys are {list(allowed)}")
    lacking = [key for key in required if key not in value]
    if lacking:
        raise ValueError(f"{label} lacks the key {lacking[0]!r}")
    return value


def integer(value: object, label: str, least: int, most: int = MAX_WORK_INT) -> int:
    """An integer of the files within [least, most], refused by name otherwise."""
    if type(value) is not int or not least <= value <= most:
        raise ValueError(f"{label} must be an integer from {least} through {most}, got {value!r}")
    return value


def node_of(value: object, label: str, shape: Node, beyond: tuple[Node, ...] = ()) -> Node:
    """A Node's address on the GameBoard, three integers inside the shape and not beyond the board's inner faces, refused by name otherwise."""
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{label} must be a Node [x, y, z]")
    found = tuple(integer(value[axis], f"{label}[{axis}]", 0, shape[axis] - 1) for axis in range(3))
    node = found[0], found[1], found[2]
    if node in beyond:
        raise ValueError(
            f"{label} is the Node {list(node)}, beyond the board's inner face: nothing stands there"
        )
    return node


def span_of(value: object, label: str, extent: int) -> tuple[int, int]:
    """A range of Nodes [first, last] along one axis, inside its extent, first at most last."""
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{label} must be a range [first, last]")
    first = integer(value[0], f"{label}[0]", 0, extent - 1)
    return first, integer(value[1], f"{label}[1]", first, extent - 1)


def document_at(files: Mapping[str, object], path: object, label: str) -> object:
    """The document the world names by its repository path, refused by name where the host read no file there."""
    if not isinstance(path, str) or path not in files:
        raise ValueError(f"{label} names {path!r}, and no file stands at that repository path")
    return files[path]
