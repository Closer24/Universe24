"""The receding face (ALGEBRA.md #the-objects, the unbounded board): the GameBoard grows by layers of zeros beyond a receding face whenever a level other than 0 stands on the layer before it, so no wave meets the face (a level leaves 0 only where a neighbour was not 0 the interval before), every grown Node at the NodeState of a Node with no level: every level 0 (the massless row holding the content at its rest, the vacuum content, ALGEBRA.md #what-is-open, item 22), a held row's time part at the remainder the start gave the row, every write remainder at half its wall (`node.write_origins`) and every other remainder 0; on the way back in time the layers a step grew are taken off after its inverse, the grown Nodes having returned to that state exactly; a face grown to the axis's largest size ends the run rather than reflecting, named; growth before the origin (the low face) keeps every declared coordinate the file's by the offset of the layers before it."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import node
from event_universe.loader.derived import FamilyRule
from event_universe.loader.faces import SIDES, RecedingFace
from event_universe.loader.keys import AXES, Node
from event_universe.reports import Detector

if TYPE_CHECKING:
    from event_universe.game_board import GameBoard

Growth = tuple[int, int, int, int]  # a growth: the interval it served, the axis, the side, the layers
ONE = (1, 1, 1)  # the shape of one Node, at which an act's origin is read
SCALARS = (
    "write_remainders",
)  # the arrays of a NodeState beside its records: the writes' remainders per part


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
        time = state.parts[0] if state.parts else None
        arrays = [
            getattr(record, key) - (family.rest if record is time else 0)
            for record in node.records(state)
            for key in ("now", "before")
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
) -> None:
    """Every array of a family's NodeState grown by `layers` layers beyond the face on `side` of `axis` (direction +1) at the NodeState of a Node with no level: the time part at the family's `rest` (the vacuum content of the massless row, 0 for every other) with its remainder at `origin`, the remainder the start gave the row, every write remainder at half its wall (`walls`, one per part), everything else 0; or the same layers taken off (direction -1)."""

    def grown(a: Any, value: int = 0) -> Any:
        return sized(a, axis, side, layers, direction, value)

    records = []
    for record in node.records(state):
        time = bool(state.parts) and record is state.parts[0]
        records.append(
            node.Record(
                grown(record.now, family.rest if time else 0),
                grown(record.before, family.rest if time else 0),
                grown(record.remainder, origin if time else 0),
            )
        )
    node.with_records(state, records)
    origins = [origin_of(at) for at in node.write_origins(walls, ONE)]
    for key in SCALARS:
        arrays = getattr(state, key)
        setattr(state, key, [grown(a, at) for a, at in zip(arrays, origins, strict=True)])


def resized_detector(detector: Detector, axis: int, side: int, layers: int, direction: int) -> Detector:
    """A detector's declared Nodes over the grown GameBoard (none grown: nothing is declared there), a body's derived each interval."""
    if detector.nodes is None:
        return detector
    return Detector(
        detector.name, sized(detector.nodes, axis, side, layers, direction, False), detector.body
    )


def grow(board: GameBoard) -> bool:
    """The receding faces before the interval's acts: where a level other than 0 stands on the layer before a receding face (`reached`) the GameBoard grows by the face's layers of zeros on that side (`resize`), up to the axis's largest size; there, with the front on that layer, the run ends, named (`board.ended`), and no act follows (False)."""
    for face in board.world.receding:
        if not reached(board.states, board.families, face.axis, face.side):
            continue
        layers = min(face.layers, face.largest - board.shape[face.axis])
        if layers < 1:
            board.ended = end(face, board.tick)
            return False
        resize(board, face.axis, face.side, layers, 1)
        board.growths.append((board.tick + 1, face.axis, face.side, layers))
    return True


def resize(board: GameBoard, axis: int, side: int, layers: int, direction: int) -> None:
    """The GameBoard grown by `layers` layers beyond its face on `side` of `axis` (direction +1) or the same layers taken off (-1): every NodeState (`resized`), the detectors' declared Nodes, the Nodes beyond the inner faces, the shape and the offset of the layers before the origin."""
    for index, (family, state) in enumerate(zip(board.families, board.states, strict=True)):
        resized(state, family, axis, side, layers, board.origins[index], board.walls(index), direction)
    board.detectors = [resized_detector(d, axis, side, layers, direction) for d in board.detectors]
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
    """A Node of the GameBoard as grown at the file's coordinates: its index less the layers grown before the origin on each axis."""
    return [int(index) - before for index, before in zip(list(at), offset, strict=True)]  # type: ignore[call-overload]


def end(face: RecedingFace, tick: int) -> dict[str, object]:
    """The lawful end, named: the front stands on the layer before the receding face of an axis grown to its largest size after this interval, and the next interval would reflect it."""
    side = SIDES[1] if face.side > 0 else SIDES[0]
    return {"interval": tick, "axis": AXES[face.axis], "side": side, "largest": face.largest}
