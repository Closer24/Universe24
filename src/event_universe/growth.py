"""The receding face (ALGEBRA.md #the-objects, the unbounded board): the lattice grows by layers of zeros beyond a receding face whenever a level other than 0 stands on the layer before it, so no wave meets the face (a level leaves 0 only where a neighbour was not 0 the interval before), every grown Node at the NodeState of a Node with no level: every level 0 (the massless row holding the content at its rest, the vacuum content, ALGEBRA.md #what-is-open, item 22), a held row's time line at the remainder the start gave the row, every write remainder at half its wall (`node.write_origins`) and every other remainder 0; on the way back in time the layers a step grew are taken off after its inverse, the grown Nodes having returned to that state exactly; a face grown to the axis's largest size ends the run rather than reflecting, named; growth before the origin (the low face) keeps every declared coordinate the file's by the offset of the layers before it."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import node
from event_universe.loader.derived import FamilyRule
from event_universe.loader.faces import SIDES, RecedingFace
from event_universe.loader.keys import AXES, Node
from event_universe.reports import NodeReader, end

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Growth = tuple[int, int, int, int]  # a growth: the interval it served, the axis, the side, the layers
ONE = (1, 1, 1)  # the shape of one Node, at which an act's origin is read


def padded(a: Any, axis: int, side: int, layers: int, value: int = 0) -> Any:
    """The array with `layers` layers of `value` beyond its face on `side` (+1 or -1) of `axis`, the dtype kept."""
    width = [(0, 0)] * 3
    width[axis] = (layers, 0) if side < 0 else (0, layers)
    return np.pad(a, width, constant_values=value)


def shrunk(a: Any, axis: int, side: int, layers: int) -> Any:
    """The array with `layers` layers taken off its face on `side` of `axis`, the inverse of `padded`."""
    kept = [slice(None)] * 3
    kept[axis] = slice(layers, None) if side < 0 else slice(None, -layers)
    return a[tuple(kept)]


def sized(a: Any, axis: int, side: int, layers: int, direction: int, value: int = 0) -> Any:
    """The array grown by `layers` layers of `value` (direction +1) or the same layers taken off (-1)."""
    if direction == 1:
        return padded(a, axis, side, layers, value)
    return shrunk(a, axis, side, layers)


def reached(
    states: list[node.NodeState], families: tuple[FamilyRule, ...], axis: int, side: int
) -> bool:
    """Whether a level other than 0 of any family (the massless row's time part read against its rest) stands on the layer before the face on `side` of `axis` (the last layer for +1, the first for -1): the layer from which the next interval would carry the front beyond the face."""
    layer = -1 if side > 0 else 0
    for family, state in zip(families, states, strict=True):
        arrays = [
            level - (family.rest if number % family.width == 0 else 0)
            for number, record in enumerate(state.lines)
            for level in (record.now, record.before)
        ]
        if any(bool(np.moveaxis(a, axis, 0)[layer].any()) for a in arrays):
            return True
    return False


def origin_of(values: Any) -> int:
    """An act's origin at one Node, read from the act over the shape of one Node."""
    return int(np.asarray(values).ravel()[0])


def resized(
    state: node.NodeState,
    family: FamilyRule,
    axis: int,
    side: int,
    layers: int,
    origin: int,
    walls: tuple[int, ...],
    direction: int,
    kind: type,
    half: int = 0,
) -> None:
    """Every array of a family's NodeState grown by `layers` layers beyond the face on `side` of `axis` (direction +1) at the NodeState of a Node with no level: the time line of every row, the first line of each (the massless row's one, a holder of the sign's one per row), at the family's `rest` (the vacuum content of the massless row, 0 for every other) with its remainder at `origin`, the remainder the start gave the row, every write remainder at half its wall (`walls`, one per held line), everything else 0; or the same layers taken off (direction -1)."""

    def grown(a: Any, value: int = 0) -> Any:
        return sized(a, axis, side, layers, direction, value)

    state.lines = [
        node.Record(
            grown(record.now, family.rest if number % family.width == 0 else 0),
            grown(record.before, family.rest if number % family.width == 0 else 0),
            grown(
                record.remainder, origin if number % family.width == 0 else half
            ),  # born at the half wall
        )
        for number, record in enumerate(state.lines)
    ]
    origins = [origin_of(at) for at in node.write_origins(walls, ONE, kind)]
    state.write_remainders = [
        grown(a, at) for a, at in zip(state.write_remainders, origins, strict=True)
    ]


def resized_node_reader(
    node_reader: NodeReader, axis: int, side: int, layers: int, direction: int
) -> NodeReader:
    """A node_reader's declared Nodes over the grown lattice (none grown: nothing is declared there), a body's derived each interval."""
    if node_reader.nodes is None:
        return node_reader
    return NodeReader(
        node_reader.name,
        sized(node_reader.nodes, axis, side, layers, direction, False),
        node_reader.body,
        node_reader.declared,
    )


def grow(board: Lattice) -> bool:
    """The receding faces before the interval's acts: where a level other than 0 stands on the layer before a receding face (`reached`) the lattice grows by the face's layers of zeros on that side (`resize`), up to the axis's largest size; there, with the front on that layer, the run ends, named (`board.ended`), and no act follows (False)."""
    for face in board.world.receding:
        if not reached(board.states, board.families, face.axis, face.side):
            continue
        layers = min(face.layers, face.largest - board.shape[face.axis])
        if layers < 1:
            board.ended = ended(face, board.interval)
            return False
        resize(board, face.axis, face.side, layers, 1)
        board.growths.append((board.interval + 1, face.axis, face.side, layers))
    return True


def resize(board: Lattice, axis: int, side: int, layers: int, direction: int) -> None:
    """The lattice grown by `layers` layers beyond its face on `side` of `axis` (direction +1) or the same layers taken off (-1): every NodeState (`resized`), the node_readers' declared Nodes, the Nodes beyond the inner faces, the shape and the offset of the layers before the origin."""
    for index, (family, state) in enumerate(zip(board.families, board.states, strict=True)):
        kind = board.world.kind
        resized(
            state,
            family,
            axis,
            side,
            layers,
            board.origins[index],
            board.walls(index),
            direction,
            kind,
            board.half_wall(index),
        )
    board.node_readers = [
        resized_node_reader(d, axis, side, layers, direction) for d in board.node_readers
    ]
    if board.wrap.beyond is not None:
        beyond = sized(board.wrap.beyond, axis, side, layers, direction, False)
        board.wrap = board.wrap._replace(beyond=beyond)
    grown = sized(np.zeros(board.shape, dtype=bool), axis, side, layers, direction)
    board.shape = (int(grown.shape[0]), int(grown.shape[1]), int(grown.shape[2]))
    if side < 0:
        offset = list(board.offset)
        offset[axis] += direction * layers
        board.offset = (offset[0], offset[1], offset[2])


def declared(at: object, offset: Node) -> list[int]:
    """A Node of the lattice as grown at the file's coordinates: its index less the layers grown before the origin on each axis."""
    return [int(index) - before for index, before in zip(list(at), offset, strict=True)]  # type: ignore[call-overload]


def ended(face: RecedingFace, interval: int) -> dict[str, object]:
    """The lawful end, named by the reports' words (`reports.end`): the interval, the axis and the side of the receding face grown to its largest size."""
    return end(interval, AXES[face.axis], SIDES[1] if face.side > 0 else SIDES[0], face.largest)
