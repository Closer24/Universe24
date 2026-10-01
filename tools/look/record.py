"""The look's host reader, a diagnostic (docs/ENGINE.md #6-how-to-run-a-world): a world is loaded as tools/run_inputs.py loads it, stepped by the engine's own step, and every family's arrays are read after each interval into one file beside the world's files, `<world>.look.json`, labelled "GameBoard reading". Per interval: a family of quanta's real level now, its second level now, its count (the record's share in quanta, the engine's own `GameBoard.quanta`), its sense (the sign of the record's Wronskian, `node.sense_sign`), the form the interval booked (D_i over both level pairs, the engine's own `node.form`) and the least Link pace its read finds at that state (the engine's own read and `link_paces`); a held family's level (its time part) and its further parts; the bodies' Nodes (where the family's share stands in quanta about the declared Nodes, `GameBoard.body_nodes`); the interval's output lines; the GameBoard's shape at that interval and its offset, the layers grown before the origin on each axis (a board with a receding face grows, every array of the frame over the shape of its own frame and every Node named at the file's coordinates). At the top the world's declared numbers as the loader read them (Gamma, T, the width, the families, the shape, the boundary, the inner faces with their gaps, the receding faces, the folded axes, the bodies with their declared counts, the detectors), at the end the books and the end of the run where it ended at a receding face's largest size. Frame 0 is the world as laid before the first interval, its counts the record's share as the mode file laid it (the gate having admitted each body's declared count within the rounding of that share). Every number is the world's files' or the engine's arrays'; the reader writes no number of its own and touches no state of the engine. An array is nested lists [x][y][z] of integers, or, where the dense file would pass the size limit, its nonzero Nodes alone as flat x-major indexes with their values.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/look/record.py <world>.json [--ticks N] [--out <world>.look.json]
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import growth, node
from event_universe.core.rule3 import link_paces
from event_universe.game_board import GameBoard
from event_universe.loader.derived import FamilyRule, count_wall
from event_universe.loader.world import AXES, World
from event_universe.world_files import load_world

LABEL = "GameBoard reading"
DENSE, SPARSE = "dense", "sparse"
SIZE_LIMIT = 16 * 1024 * 1024  # the page's limit: beyond it every array keeps its nonzero Nodes alone
LINES = ("click",)

Encoder = Callable[[np.ndarray], object]


def dense(array: np.ndarray) -> object:
    """An array over the GameBoard as nested lists [x][y][z] of integers."""
    return array.tolist()


def sparse(array: np.ndarray) -> object:
    """An array over the GameBoard as its nonzero Nodes alone: the flat x-major indexes and the values there."""
    flat = array.reshape(-1)
    at = np.flatnonzero(flat)
    return {"at": at.tolist(), "values": flat[at].tolist()}


def nodes_of(mask: np.ndarray, offset: tuple[int, int, int] = (0, 0, 0)) -> list[list[int]]:
    """The Nodes of a mask over the GameBoard as [x, y, z] rows at the file's coordinates, `offset` the layers grown before the origin."""
    return [
        [int(i) - before for i, before in zip(row, offset, strict=True)] for row in np.argwhere(mask)
    ]


def family_row(family: FamilyRule, families: tuple[FamilyRule, ...], action: int) -> dict[str, object]:
    """A family's row as the rule derived it: its name, pair, what it holds at which divisor, its parts, whether it carries quanta, the rows it reads and its count's wall W_c."""
    return {
        "name": family.name,
        "pair": list(family.pair),
        "held": family.held,
        "divisor": family.divisor,
        "parts": list(family.parts),
        "quanta": family.quanta,
        "reads": [families[read.family].name for read in family.reads],
        "wall": count_wall(family, action) if family.quanta else None,
    }


def declared(world: World, path: Path, board: GameBoard) -> dict[str, object]:
    """The world's declared numbers as the loader read them (the inner faces as the world file declares them, each its axis, its coordinate and its gaps, the loader having admitted them), and the detectors as the GameBoard holds them (the open faces' layer among them)."""
    families = world.families
    faces = [
        "open" if opened else "periodic" if wraps else "closed"
        for opened, wraps in zip(world.open_axes, world.periodic, strict=True)
    ]
    document = json.loads(path.read_text(encoding="utf-8"))
    return {
        "world": path.name,
        "shape": list(world.shape),
        "boundary": dict(zip(AXES, faces, strict=True)),
        "folded": [extent == 1 for extent in world.shape],
        "face_depth": world.face_depth,
        "faces": document.get("faces", []),
        "receding": document.get("receding", {}),
        "declared_ticks": world.ticks,
        "node_clock": world.node_clock,
        "quantum_action": world.quantum_action,
        "largest_integer": str(world.width),
        "amplitude_bound": world.amplitude_bound,
        "families": [family_row(family, families, world.quantum_action) for family in families],
        "bodies": [
            {
                "number": number,
                "family": families[row.family].name,
                "nodes": [list(at) for at in row.nodes],
                "counts": list(row.counts),
                "declared": sum(row.counts),
            }
            for number, row in enumerate(world.bodies)
        ],
        "detectors": [
            {
                "name": detector.name,
                "nodes": nodes_of(detector.nodes) if detector.nodes is not None else [],
                "body": detector.body,
            }
            for detector in board.detectors
        ],
    }


def frame(
    board: GameBoard, kept: dict[int, tuple[node.Record, node.Record]] | None
) -> dict[str, object]:
    """One interval's reading of every family's arrays (`kept` the level pairs the interval started from, None at frame 0): the two levels now, the count as the record's share in quanta and the sense as the Wronskian's sign (readings of the record, kept nowhere), the form and the pace; the bodies' standing Nodes as a report derives them (`GameBoard.body_nodes`), the GameBoard's shape and offset at the interval and the output lines to come."""
    world, families = board.world, {}
    for index, (family, state) in enumerate(zip(board.families, board.states, strict=True)):
        row: dict[str, object]
        if family.quanta:
            assert state.levels is not None and state.second is not None
            row = {"now": state.levels.now, "second": state.second.now}
            row.update(count=board.quanta(index), sense=node.sense_sign(state, board.shape))
            if kept is not None:
                real, second = kept[index]
                row["form"] = node.form(real, state.levels) + node.form(second, state.second)
            content, axis = node.signed_read(
                index, board.families, board.states, world.node_clock, "now", board.shape
            )
            row["pace"] = min(int(np.min(pace)) for pace in link_paces(world.node_clock, content, axis))
        else:
            row = {"level": state.parts[0].now, "parts": [part.now for part in state.parts[1:]]}
        families[family.name] = row
    bodies = [nodes_of(board.body_nodes(number), board.offset) for number in range(len(world.bodies))]
    found: dict[str, object] = {"tick": board.tick, "families": families, "bodies": bodies}
    return {**found, "shape": list(board.shape), "offset": list(board.offset), "lines": []}


def copied(record: node.Record) -> node.Record:
    """A level pair's two levels copied, so the form is read from the interval's start after the step."""
    return node.Record(record.now.copy(), record.before.copy(), record.remainder)


def grown(record: node.Record, board: GameBoard) -> node.Record:
    """A kept level pair over the GameBoard as the interval grew it (the layers a receding face added before this interval's acts, 0 at the interval's start), so the form is read at every Node of the frame."""
    for served, axis, side, layers in board.growths:
        if served == board.tick:
            now, before = (growth.padded(a, axis, side, layers) for a in (record.now, record.before))
            record = node.Record(now, before, record.remainder)
    return record


def record(path: Path, ticks: int | None) -> dict[str, object]:
    """The look of one world: loaded, stepped `ticks` intervals (the world's own where None) by the engine's own step, every frame read after its interval; a refusal is written with its reason and the frames before it."""
    lines: list[dict[str, object]] = []
    world = load_world(path)
    board = GameBoard(world, lines.append)
    document: dict[str, object] = {"label": LABEL, "verdict": "LAWFUL", "reason": None}
    document.update(declared(world, path, board))
    frames: list[dict[str, object]] = []
    try:
        frames.append(frame(board, None))
        for _ in range(world.ticks if ticks is None else ticks):
            kept = {}
            for index in board.order:
                state = board.states[index]
                assert state.levels is not None and state.second is not None
                kept[index] = (copied(state.levels), copied(state.second))
            board.step()
            if board.ended is not None:
                break
            kept = {
                index: (grown(real, board), grown(second, board))
                for index, (real, second) in kept.items()
            }
            frames.append(frame(board, kept))
    except (ValueError, RuntimeError) as refusal:
        document.update(verdict="REFUSED", reason=str(refusal))
    document["ended"] = board.ended
    for line in lines:
        if line["event"] in LINES:
            tick = int(str(line["tick"]))
            if tick < len(frames):
                frame_lines = frames[tick]["lines"]
                assert isinstance(frame_lines, list)
                frame_lines.append(line)
    document.update(ticks=board.tick, frames=frames, books=board.books() if board.tick else {})
    return document


def rendered(document: dict[str, object], encoder: Encoder) -> str:
    """The document as compact JSON text, every array by `encoder`."""

    def default(value: object) -> object:
        if isinstance(value, np.ndarray):
            return encoder(value)
        if isinstance(value, np.integer):
            return int(value)
        raise TypeError(f"the look holds a {type(value).__name__}, not written")

    return json.dumps(document, separators=(",", ":"), default=default)


def written(document: dict[str, object], target: Path) -> tuple[str, int]:
    """The look written to `target`, its arrays dense, or the nonzero Nodes alone where the dense text passes the size limit; the encoding's name and the text's length returned."""
    document["arrays"] = DENSE
    text = rendered(document, dense)
    if len(text) > SIZE_LIMIT:
        document["arrays"] = SPARSE
        text = rendered(document, sparse)
    target.write_text(text + "\n", encoding="utf-8")
    return str(document["arrays"]), len(text)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("world", type=Path, help="the world file, its mode file beside it")
    parser.add_argument("--ticks", type=int, default=None, help="the intervals (the world's own)")
    parser.add_argument("--out", type=Path, default=None, help="the look's file (<world>.look.json)")
    args = parser.parse_args(argv)
    target: Path = args.out or args.world.with_suffix(".look.json")
    document = record(args.world, args.ticks)
    arrays, length = written(document, target)
    summary: dict[str, Any] = {
        "world": args.world.name,
        "verdict": document["verdict"],
        "ticks": document["ticks"],
        "arrays": arrays,
        "bytes": length,
        "look": str(target),
    }
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
