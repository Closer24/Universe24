"""The faces a world declares beside its boundary (ALGEBRA.md #the-objects): the inner faces (the face rule inside the board), a declaration of the file, like the wraps and the detector Nodes, of a plane of Nodes across an axis that lies beyond the board except for its gaps, every Node beyond the board reading 0 through every Port and read as 0 (core/ports.py), nothing laid, sourced or declared there; and the receding faces (the unbounded board), a face of an open or closed axis beyond which the GameBoard grows by layers of zeros as the front reaches it (growth.py), with the axis's largest size and the layers per growth, the file's numbers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from event_universe.loader.keys import AXES, Node, integer, keyed, span_of

FACE_KEYS = ("axis", "at", "gaps")  # an inner face: the axis it stands across, its coordinate, its gaps
RECEDING_KEYS = (
    "sides",
    "largest",
    "layers",
)  # a receding face: its sides, the axis's largest size, the layers per growth
SIDES = ("low", "high")  # an axis's two faces: before the coordinate 0 and beyond the last Node
PERIODIC = "periodic"  # the boundary word of an axis without faces


@dataclass(frozen=True)
class RecedingFace:
    """A receding face as declared: its axis, its side (-1 the low face, +1 the high), the axis's largest extent in Nodes and the layers of zeros the GameBoard grows by at a time."""

    axis: int
    side: int
    largest: int
    layers: int


def receding_of(value: object, shape: Node, boundary: Mapping[str, object]) -> tuple[RecedingFace, ...]:
    """The receding faces from the world's `receding` key: per axis (`x`, `y` or `z`) its `sides`, a list of `low` and/or `high` (no side twice), `largest`, the axis's largest extent in Nodes, above the shape's, and `layers`, the layers of zeros per growth, from 1; an axis with a receding face is open or closed (a periodic axis has no face) and of more than one Node (an axis of one Node folds); every other key, word or number is refused by name."""
    found: list[RecedingFace] = []
    for name, entry in keyed(value, "receding", AXES, ()).items():
        axis, label = AXES.index(name), f"receding.{name}"
        face = keyed(entry, label, RECEDING_KEYS, RECEDING_KEYS)
        if boundary[name] == PERIODIC or shape[axis] < 2:
            raise ValueError(
                f"{label}: a receding face stands on an open or closed axis of two Nodes or more, and the "
                f"{name} axis is {boundary[name]} with {shape[axis]} Node(s)"
            )
        sides = face["sides"]
        if not isinstance(sides, list) or not sides or len(set(sides)) != len(sides):
            raise ValueError(f"{label}.sides lists {list(SIDES)}, each once, got {sides!r}")
        largest = integer(face["largest"], f"{label}.largest", shape[axis] + 1)
        layers = integer(face["layers"], f"{label}.layers", 1)
        for side in sides:
            if side not in SIDES:
                raise ValueError(f"{label}.sides holds {side!r}: a side is one of {list(SIDES)}")
            found.append(RecedingFace(axis, 1 if side == SIDES[1] else -1, largest, layers))
    return tuple(found)


def faces_of(value: object, shape: Node) -> tuple[Node, ...]:
    """The Nodes beyond the board, sorted, from the inner faces: each across an axis at a coordinate, the plane's Nodes beyond the board except its gaps, each gap a range on each of the other two axes; faces that leave no Node on the board are refused by name."""
    if not isinstance(value, list):
        raise ValueError("faces must be a list of the inner faces")
    beyond: set[Node] = set()
    for index, entry in enumerate(value):
        label = f"faces[{index}]"
        face = keyed(entry, label, FACE_KEYS, FACE_KEYS)
        if face["axis"] not in AXES:
            raise ValueError(f"{label}.axis is one of {list(AXES)}, got {face['axis']!r}")
        axis = AXES.index(face["axis"])
        at = integer(face["at"], f"{label}.at", 0, shape[axis] - 1)
        others = tuple(other for other in range(3) if other != axis)
        names = tuple(AXES[other] for other in others)
        if not isinstance(face["gaps"], list):
            raise ValueError(f"{label}.gaps must be a list of its gaps, each a range on {list(names)}")
        gaps = []
        for number, gap in enumerate(face["gaps"]):
            ranges = keyed(gap, f"{label}.gaps[{number}]", names, names)
            gaps.append(
                tuple(
                    span_of(ranges[name], f"{label}.gaps[{number}].{name}", shape[other])
                    for name, other in zip(names, others, strict=True)
                )
            )
        for first in range(shape[others[0]]):
            for second in range(shape[others[1]]):
                if any(a <= first <= b and c <= second <= d for (a, b), (c, d) in gaps):
                    continue
                node = [0, 0, 0]
                node[axis], node[others[0]], node[others[1]] = at, first, second
                beyond.add((node[0], node[1], node[2]))
    if beyond and len(beyond) >= shape[0] * shape[1] * shape[2]:
        raise ValueError("faces leave no Node on the board")
    return tuple(sorted(beyond))
