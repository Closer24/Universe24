"""The keys of the world's files as the loader reads them: an object with its allowed and required keys, an integer within its bounds, a Node inside the shape and on the board, and the document a world names by a repository path; every defect refused by name, no default written (ALGEBRA.md #a-familys-declaration). A family's declared reads by name and weight (`reads_of`, the key `reads`) were read here to 2026-10-24 and are derived since (`derived.with_reads`), kept by name."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

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


def integer(value: object, label: str, least: int, most: int | None = None) -> int:
    """An integer of the files from `least`, and through `most` where the caller names one (a Node's coordinate inside the shape), refused by name otherwise: Python's integers need no bound of the tool's, and the width the loader derives bounds every level (the bound 2^512 of 2026-10-24 and the host's 63 bits before it, both the tool's choices, gone 2026-10-24)."""
    if type(value) is not int or value < least or (most is not None and value > most):
        through = "" if most is None else f" through {most}"
        raise ValueError(f"{label} must be an integer from {least}{through}, got {value!r}")
    return value


def node_of(value: object, label: str, shape: Node) -> Node:
    """A Node's address on the lattice, three integers inside the shape, refused by name otherwise."""
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{label} must be a Node [x, y, z]")
    found = tuple(integer(value[axis], f"{label}[{axis}]", 0, shape[axis] - 1) for axis in range(3))
    return found[0], found[1], found[2]


def document_at(files: Mapping[str, object], path: object, label: str) -> object:
    """The document the world names by its repository path, refused by name where the host read no file there."""
    if not isinstance(path, str) or path not in files:
        raise ValueError(f"{label} names {path!r}, and no file stands at that repository path")
    return files[path]
