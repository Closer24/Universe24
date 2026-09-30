"""The inner faces of a world (ALGEBRA.md #the-objects, the face rule inside the board): a declaration of the file, like the wraps and the detector Nodes, of a plane of Nodes across an axis that lies beyond the board except for its gaps; every Node beyond the board reads 0 through every Port and is read as 0 (core/ports.py), and nothing is laid, sourced or declared there."""

from __future__ import annotations

from event_universe.loader.keys import AXES, Node, integer, keyed, span_of

FACE_KEYS = ("axis", "at", "gaps")  # an inner face: the axis it stands across, its coordinate, its gaps


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
