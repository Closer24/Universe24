"""The keys of the world's files as the loader reads them: an object with its allowed and required keys, an integer within its bounds, a Node inside the shape and on the board, a range of Nodes along an axis, a family's declared reads by name and weight, a laid record's weight per real line, and the document a world names by a repository path; every defect refused by name, no default written (ALGEBRA.md #a-familys-declaration)."""

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
    """A Node's address on the lattice, three integers inside the shape and not beyond the board's inner faces, refused by name otherwise."""
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


def weights_of(value: object, label: str, lines: int, plane: bool) -> tuple[int, ...]:
    """A laid record's weight on each laid line of its part (the world file's key `weights` on a body or a packet, `Lattice.lay`: the laid pair times the line's weight on that line, so a record of three real lines is laid at the weights (a, b, c) over its three lines): a list of one integer per real line, not all 0, refused by name on planes, whose second line is its sense and no weighted copy of the first; 1 on every laid line without the key (`FamilyRule.laid`, one per real line, one per plane), the pair laid alike."""
    if value is None:
        return (1,) * lines
    if plane:
        raise ValueError(
            f"{label} weights the lines of a plane: a plane's second line is its sense (the second level pair), "
            "and no weight is laid on it; the key is a record of real lines' (ALGEBRA.md #a-familys-declaration)"
        )
    if not isinstance(value, list) or len(value) != lines:
        raise ValueError(f"{label} must list one integer weight per line of the record, {lines} here")
    found = tuple(integer(weight, f"{label}[{at}]", -MAX_WORK_INT) for at, weight in enumerate(value))
    if not any(found):
        raise ValueError(f"{label} weights every line of the record at 0: nothing is laid")
    return found


def reads_of(value: object, label: str) -> tuple[tuple[str, int], ...]:
    """A family's declared reads (the universe file's key `reads`, `label` the row's): an object naming each holder it reads with the integer weight it reads with (and, by the hold's reciprocity, sources it with), a weight of 0 refused by name (a holder read at 0 is left out), an empty object where it reads none; the names resolved against the held rows once every row is read (`derived.read_of`)."""
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object, each holder's name to the weight it is read with")
    found = []
    for name, weight in value.items():
        at = f"{label}[{name!r}]"
        if integer(weight, at, -MAX_WORK_INT) == 0:
            raise ValueError(f"{at} is 0: a holder read at the weight 0 is no read, leave it out")
        found.append((name, int(weight)))
    return tuple(found)
