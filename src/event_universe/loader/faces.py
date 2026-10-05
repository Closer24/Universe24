"""The faces a world declares beside its boundary (ALGEBRA.md #the-objects): the inner faces (the face rule inside the board), a declaration of the file, like the wraps and the node_detector Nodes, of a plane of Nodes across an axis that lies beyond the board except for its gaps, every Node beyond the board reading 0 through every Port and read as 0 (core/ports.py), nothing laid, sourced or declared there; and the receding faces (the unbounded board), a face of an open or closed axis beyond which the lattice grows by layers of zeros as the front reaches it (growth.py), with the axis's largest size and the layers per growth, the file's numbers."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from itertools import pairwise

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
    """A receding face as declared: its axis, its side (-1 the low face, +1 the high), the axis's largest extent in Nodes and the layers of zeros the lattice grows by at a time."""

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


def layer_of(
    shape: Node, open_axes: tuple[bool, bool, bool], depth: int, receding: tuple[RecedingFace, ...]
) -> tuple[Node, ...]:
    """The open faces' layer, the Nodes within `depth` of an open face that does not recede, sorted: the one region of the board's own that reports (ENGINE.md, the words), none where every open face recedes."""
    gone = {(face.axis, face.side) for face in receding}
    found: set[Node] = set()
    for axis in range(3):
        if not open_axes[axis]:
            continue
        for x in range(shape[0]):
            for y in range(shape[1]):
                for z in range(shape[2]):
                    at = (x, y, z)
                    if (at[axis] < depth and (axis, -1) not in gone) or (
                        at[axis] >= shape[axis] - depth and (axis, 1) not in gone
                    ):
                        found.add(at)
    return tuple(sorted(found))


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


def connected(nodes: tuple[Node, ...], shape: Node, periodic: tuple[bool, bool, bool]) -> bool:
    """Whether a set of Nodes is one region: every Node reached from the first along the Links, across a periodic wrap too."""
    region, seen, front = set(nodes), {nodes[0]}, [nodes[0]]
    while front:
        node = front.pop()
        for axis in range(3):
            for side in (1, -1):
                there = list(node)
                there[axis] += side
                if periodic[axis]:
                    there[axis] %= shape[axis]
                at = (there[0], there[1], there[2])
                if at in region and at not in seen:
                    seen.add(at)
                    front.append(at)
    return seen == region


def extent_across(coordinates: Iterable[int], length: int, wraps: bool) -> int:
    """The extent of a region on one axis, in Nodes, for the size rule of `loader/world.regions_of_the_law`: from its least to its greatest distinct coordinate on an open or closed axis, and across a periodic axis of `length` Nodes the smallest arc of the ring that covers its coordinates, the length less the largest gap between cyclic neighbours (the gap through the wrap included) plus 1, so that y = 0 and y = 4 of 5 are 2 Nodes across, 1, 2 and 3 of 5 are 3, the same as from the least to the greatest, the whole ring is 5 and one coordinate is 1 (the advisor's breaker over the engine at 7756546d, #1793: a region two Nodes wide through the wrap was read as 5 and admitted under a wider half wavelength)."""
    distinct = sorted(set(coordinates))
    if not wraps:
        return distinct[-1] - distinct[0] + 1
    gaps = [after - before for before, after in pairwise(distinct)]
    gaps.append(length - distinct[-1] + distinct[0])  # the wrap's gap, the whole ring at one coordinate
    return length - max(gaps) + 1
