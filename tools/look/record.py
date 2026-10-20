"""The look's host reader, a diagnostic (docs/ENGINE.md #6-how-to-run-a-world): a world is loaded as tools/run_inputs.py loads it, stepped by the engine's own step, and every family's arrays are read after each interval into one file beside the world's files, `<world>.look.json`, labelled "lattice reading"; with `--every K` the look keeps frame 0, the frame of every K-th interval and the last frame stepped, each the full look's frame at that interval with its own lines, so that a long run's look fits a page, the intervals between the kept frames in no frame (the readings read a full look recorded locally). The frames are read from the lattice's observers (`Lattice.observers`, one callable called with the interval, the direction and the pass after every `step` and every `step_inverse`; ENGINE.md section 10, item 11): on a world whose draw declares `meeting: back` (ALGEBRA.md, The meeting's reading, root or back) the board runs to the first side's close, back to the record's birth and forward again to the partner's close, and the look holds the three passes in the look's order, every frame carrying `interval` as the board holds it (decreasing on the run back), `direction` (+1 or -1) and `pass` (1 the run to the first close, 2 the run back, 3 the run forward again), the stride within each pass with each pass's last frame kept, a frame's form the one its interval booked (on the run back the form of the interval stepped back through), the credit lines kept in their frames beside the click and parts lines, every frame carrying the board's `tick` (the loop's count of its intervals forward, which never runs back and stands at the close while the record is read back and forward) and, in the run back's reach the cone (the default), the frames of the run back and forward their `cone_radius` (the lay's Nodes within t + 1 Links at the interval t) with the look's header carrying `reach`, `cone_support` (the lay's Nodes at the file's coordinates) and `cone_volume` (the cone's Nodes per interval), the engine's own numbers; a look of one pass (every shipped world) is written as before, no `direction`, no `pass`, the click and parts lines alone, bit for bit. Per interval: a family of quanta's level now, its second level now where it is a plane, its count (the record's share in quanta, the engine's own `Lattice.quanta`), its share over the lattice in the current's units (the books' per interval, the engine's own `Lattice.total_share`), the form the interval booked (D_i over both level pairs, the engine's own `records.form`) and the least Node pace Gamma - 2 c_i its read finds at that state (the engine's own read and `node_pace`); a held family's level (its time part) and its further parts; the bodies' Nodes (where the family's share stands in quanta about the declared Nodes, `Lattice.body_nodes`), each body marked a reader where the file declares it one; the interval's `click` lines and, for a family of several parts, its `parts` lines (the NodeDetector's read, the parts' signed level sums per region, which the joint-share reader credits), each line in the frame of the pass it was written in; the lattice's shape at that interval and its offset, the layers grown before the origin on each axis (a board with a receding face grows, every array of the frame over the shape of its own frame and every Node named at the file's coordinates). At the top the world's declared numbers as the loader read them (Gamma, T, the width, the families, the shape, the boundary, the inner faces with their gaps, the receding faces, the folded axes, the bodies with their declared counts, the node_detectors), at the end the books and the end of the run where it ended at a receding face's largest size. Frame 0 is the world as laid before the first interval, its counts the record's share as the mode file laid it (the gate having admitted each body's declared count within the rounding of that share). Every number is the world's files' or the engine's arrays'; the reader writes no number of its own and touches no state of the engine. An array is nested lists [x][y][z] of integers, or, where the dense file would pass the size limit, its nonzero Nodes alone as flat x-major indexes with their values.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/look/record.py <world>.json [--intervals N] [--every K] [--out <world>.look.json]
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import growth, meeting_back, node, records
from event_universe.lattice import Lattice
from event_universe.loader.derived import FamilyRule, count_wall
from event_universe.loader.world import AXES, World
from event_universe.world_files import load_world

LABEL = "lattice reading"
DENSE, SPARSE = "dense", "sparse"
SIZE_LIMIT = 16 * 1024 * 1024  # the page's limit: beyond it every array keeps its nonzero Nodes alone
LINES = ("click", "parts")  # the lines the look keeps per frame: the clicks and the parts' reads
CONE = "cone"  # the run back's reach whose frames carry the cone's radius and whose header the cone's support and volume
PASS_LINES = ("credit",)  # kept too in a look of several passes: the clicks the passes are about
Growth = tuple[
    int, int, int, int
]  # a growth as the lattice logs it: the interval served, the axis, the side, the layers

Encoder = Callable[[np.ndarray], object]
Kept = dict[int, list[records.Record]]  # a family's lines copied at an interval's start, by its index


def dense(array: np.ndarray) -> object:
    """An array over the lattice as nested lists [x][y][z] of integers."""
    return array.tolist()


def sparse(array: np.ndarray) -> object:
    """An array over the lattice as its nonzero Nodes alone: the flat x-major indexes and the values there."""
    flat = array.reshape(-1)
    at = np.flatnonzero(flat)
    return {"at": at.tolist(), "values": flat[at].tolist()}


def nodes_of(mask: np.ndarray, offset: tuple[int, int, int] = (0, 0, 0)) -> list[list[int]]:
    """The Nodes of a mask over the lattice as [x, y, z] rows at the file's coordinates, `offset` the layers grown before the origin."""
    return [
        [int(i) - before for i, before in zip(row, offset, strict=True)] for row in np.argwhere(mask)
    ]


def family_row(family: FamilyRule, families: tuple[FamilyRule, ...], action: int) -> dict[str, object]:
    """A family's row as the rule derived it: its name, pair, its lines (a family of quanta's dimension, a held row's sources' count), whether they are a plane, whether it is held and at which level weight, whether its readers' Wronskian sources it (the holder of the sign), its parts, whether it carries quanta, the rows it reads and its count's wall W_c."""
    return {
        "name": family.name,
        "pair": list(family.pair),
        "lines": family.lines,
        "plane": family.plane,
        "held": family.held,
        "sign": family.wronskian,
        "level_weight": family.level_weight,
        "parts": [1, 3] if family.axes else [1],
        "quanta": family.quanta,
        "reads": [families[read.family].name for read in family.reads],
        "wall": count_wall(family, action) if family.quanta else None,
    }


def declared(world: World, path: Path, board: Lattice) -> dict[str, object]:
    """The world's declared numbers as the loader read them (the inner faces as the world file declares them, each its axis, its coordinate and its gaps, the loader having admitted them), and the node_detectors as the lattice holds them (the open faces' layer among them)."""
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
        "declared_intervals": world.intervals,
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
                "reader": row.detector is not None,
            }
            for number, row in enumerate(world.bodies)
        ],
        "node_detectors": [
            {
                "name": node_detector.name,
                "nodes": nodes_of(node_detector.nodes) if node_detector.nodes is not None else [],
                "body": node_detector.body,
            }
            for node_detector in board.node_detectors
        ],
    }


def frame(
    board: Lattice,
    kept: Kept | None,
    direction: int = 1,
    pass_number: int = 1,
    tick: int | None = None,
    cone_radius: int | None = None,
) -> dict[str, object]:
    """One interval's reading of every family's arrays (`kept` the lines the interval started from, None at frame 0): the level now of the record's line, its second where it is a plane, the count as the record's share in quanta (a reading of the record, kept nowhere), the share over the lattice in the current's units (the books' share at this interval, None over a frozen Node), the form the interval booked (forward from the kept lines to the lines now; on the run back, `direction` -1, the booking of the interval stepped back through, from the lines now to the kept ones, the same numbers the forward step booked) and the pace; the bodies' standing Nodes as a report derives them (`Lattice.body_nodes`), the frame's direction and pass, the board's tick where given (the loop's count of its intervals forward, standing at the close while the record is read back and forward) and the cone's radius where given (the run back's reach the cone: the lay's Nodes within that many Links, t + 1 at the interval t), the lattice's shape and offset at the interval and the output lines to come."""
    world, families = board.world, {}
    for index, (family, state) in enumerate(zip(board.families, board.states, strict=True)):
        row: dict[str, object]
        if family.quanta:
            lines = board.record(index)  # light the sum of the sign holder's rows, a record its lines
            row = {
                "now": lines[0].now,
                "count": board.quanta(index)[0],
                "share": board.total_share(index)[0],
            }
            if family.plane:
                row["second"] = lines[1].now
            if kept is not None:
                began = [records.rows_total(family, kept[index])] if family.wronskian else kept[index]
                row["form"] = records.form(began, lines) if direction > 0 else records.form(lines, began)
            row["pace"] = node.least_pace(
                index, board.families, board.states, world.node_clock, board.wrap, world.link_unit
            )
        else:
            row = {"level": state.lines[0].now, "parts": [line.now for line in state.lines[1:]]}
        families[family.name] = row
    bodies = [nodes_of(board.body_nodes(number), board.offset) for number in range(len(world.bodies))]
    found: dict[str, object] = {"interval": board.interval, "direction": direction, "pass": pass_number}
    if tick is not None:
        found["tick"] = tick
    if cone_radius is not None:
        found["cone_radius"] = cone_radius
    found.update(families=families, bodies=bodies)
    return {**found, "shape": list(board.shape), "offset": list(board.offset), "lines": []}


def copied(record: records.Record) -> records.Record:
    """A line's two levels copied, so the form is read from the interval's start after the step."""
    return records.Record(record.now.copy(), record.before.copy(), record.remainder)


def resized(record: records.Record, removed: list[Growth], added: list[Growth]) -> records.Record:
    """A kept line over the lattice as the interval sized it: the layers a receding face added before this interval's acts padded on (`added`, the growths the step logged, 0 at the interval's start), and the layers the inverse took off again shrunk away (`removed`, the growths the step back unlogged), so the form is read at every Node of the frame in either direction."""
    now, before = record.now, record.before
    for _served, axis, side, layers in removed:
        now, before = (growth.shrunk(a, axis, side, layers) for a in (now, before))
    for _served, axis, side, layers in added:
        now, before = (growth.padded(a, axis, side, layers) for a in (now, before))
    return records.Record(now, before, record.remainder)


class Frames:
    """The look's frames read from the lattice's observers: one frame per call, `read(interval, direction, pass_number)` after every step and every step_inverse, frame 0 the world as laid; the stride `every` within each pass (frame 0, every K-th interval's frame and each pass's last frame kept, a repeated call at one interval of one pass, the step's end after its acts, replacing the frame read before it, the same board); every output line tagged with the pass it was written in and placed, at the end, in the kept frame of that pass at its interval, the lines of the intervals between the kept frames in no frame; a look of one pass written as before, no `direction` and no `pass` on its frames and the click and parts lines alone."""

    def __init__(self, board: Lattice, lines: list[dict[str, object]], every: int) -> None:
        self.board, self.lines, self.every = board, lines, every
        self.frames: list[dict[str, object]] = [frame(board, None, tick=getattr(board, "tick", None))]
        self.latest: dict[str, object] | None = None  # the last frame read and not kept by the stride
        self.tagged: list[tuple[int, dict[str, object]]] = []  # every output line with its pass
        self.since = 0  # the output lines from this index on take the next frame's pass
        self.last: tuple[int, int] = (
            1,
            board.interval,
        )  # the pass and the interval of the frame read last
        self.kept, self.growths = self.copies(), list(board.growths)

    def copies(self) -> Kept:
        """Every family's lines copied at this call, the start the next frame's form is read from."""
        return {
            index: [copied(line) for line in self.board.states[index].lines]
            for index in self.board.order
        }

    def read(self, interval: int, direction: int, pass_number: int) -> None:
        """The observer: one frame of the board at the call, after a step (direction +1) or a step back (-1)."""
        board = self.board
        if board.ended is not None:
            return
        self.tagged += [(pass_number, line) for line in self.lines[self.since :]]
        self.since = len(self.lines)
        removed, added = self.growths[len(board.growths) :], board.growths[len(self.growths) :]
        kept = {
            index: [resized(line, removed, added) for line in lines]
            for index, lines in self.kept.items()
        }
        coned = (
            pass_number > 1 and reach_of(board) == CONE
        )  # the run back and forward in the cone's reach
        radius = (
            meeting_back.radius(board) if coned else None
        )  # G(t): the lay's Nodes within t + 1 Links
        found = frame(board, kept, direction, pass_number, getattr(board, "tick", None), radius)
        self.kept, self.growths = self.copies(), list(board.growths)
        if self.last == (
            pass_number,
            interval,
        ):  # the step's end after its acts: the same board, the frame replaced
            if self.latest is not None:
                self.latest = found
            else:
                self.frames[-1] = found
            return
        if self.last[0] != pass_number and self.latest is not None:
            self.frames.append(self.latest)  # a pass's last frame kept whatever the stride
            self.latest = None
        self.last = (pass_number, interval)
        if interval % self.every == 0:
            self.frames.append(found)
            self.latest = None
        else:
            self.latest = found

    def closed(self) -> list[dict[str, object]]:
        """The frames at the run's end: the last frame kept whatever the stride, every output line in the kept frame of its pass at its interval (the click and parts lines; the credit lines too in a look of several passes), and a look of one pass written as before."""
        if self.latest is not None:
            self.frames.append(self.latest)
            self.latest = None
        passes = max(int(str(found["pass"])) for found in self.frames)
        at = {(int(str(found["pass"])), int(str(found["interval"]))): found for found in self.frames}
        kinds = LINES + PASS_LINES if passes > 1 else LINES
        for pass_number, line in self.tagged:
            found = at.get((pass_number, int(str(line["interval"])))) if line["event"] in kinds else None
            if found is not None:
                frame_lines = found["lines"]
                assert isinstance(frame_lines, list)
                frame_lines.append(line)
        if passes == 1:
            for found in self.frames:
                del found["direction"], found["pass"]
                found.pop("tick", None)
        return self.frames


def reach_of(board: Lattice) -> str | None:
    """The run back's reach of the world's draw as the credit's books hold it (`board.credit.reach`): board, cone or books on a world whose draw declares `meeting: back` (cone where the file declares no `reach`, the owner's word), None on a root world."""
    books = getattr(board, "credit", None)
    found = getattr(books, "reach", None)
    return str(found) if found is not None else None


def reached(board: Lattice) -> dict[str, object]:
    """The header's words of the run back's reach after the run, the engine's own numbers (ENGINE.md section 10, item 11): `reach` on a back world, and in the cone's reach `cone_support`, the lay's Nodes S_0 at the file's coordinates (`board.credit.support`), and `cone_volume`, the cone's Nodes |G(t)| per interval from 0 to the close (`board.credit.cone`), and `cone_stepped`, the Node-steps per interval of the cone stepped alone, the box with its ring, where the books count them; nothing on a root world, whose look is as before bit for bit."""
    reach = reach_of(board)
    if reach is None:
        return {}
    found: dict[str, object] = {"reach": reach}
    if reach == CONE:
        found["cone_support"] = [[int(c) for c in at] for at in board.credit.support]
        cone = {int(t): int(v) for t, v in dict(board.credit.cone).items()}
        found["cone_volume"] = [cone[t] for t in range(max(cone) + 1)] if cone else []
        stepped = {int(t): int(v) for t, v in dict(getattr(board.credit, "stepped", {})).items()}
        if stepped:  # the cone stepped alone: the Node-steps per interval, the box with its ring, the engine's count
            found["cone_stepped"] = [stepped.get(t, 0) for t in range(max(stepped) + 1)]
    return found


def passes_of(frames: list[dict[str, object]]) -> list[int]:
    """The frames' count per pass, in the passes' order: one entry for a look of one pass (no `pass` key), three for the click that runs back."""
    numbers = [int(str(found.get("pass", 1))) for found in frames]
    return [numbers.count(number) for number in range(1, max(numbers, default=1) + 1)]


def record(path: Path, intervals: int | None, every: int = 1) -> dict[str, object]:
    """The look of one world: loaded, stepped `intervals` intervals (the world's own where None) by the engine's own step, every frame read from the lattice's observers after its interval (and, on a world whose draw runs back, after every step back and every step of the run forward again, the passes in the look's order), and the frames kept at the stride `every` within each pass: frame 0, the frames at the intervals K, 2 K, 3 K, ... and the last interval stepped of each pass (1, the default, every frame), each kept frame the full look's frame at that interval bit for bit with its own `click` and `parts` lines (and, in a look of several passes, its `credit` lines), the lines of the intervals between the kept frames in no frame (the readings read a full look recorded locally; a page of a strided look takes its measurement from the run's output file, `--output`); a refusal is written with its reason and the frames before it; the look returned with the frames' count per pass (one count for a look of one pass), the summary's."""
    if every < 1:
        raise ValueError(f"--every takes an integer from 1, got {every}")
    lines: list[dict[str, object]] = []
    world = load_world(path)
    board = Lattice(world, lines.append)
    document: dict[str, object] = {"label": LABEL, "verdict": "LAWFUL", "reason": None}
    document.update(declared(world, path, board))
    reader = Frames(board, lines, every)
    board.observers.append(reader.read)
    try:
        for _ in range(world.intervals if intervals is None else intervals):
            board.step()
            if board.ended is not None:
                break
    except (ValueError, RuntimeError) as refusal:
        document.update(verdict="REFUSED", reason=str(refusal))
    document["ended"] = board.ended
    document.update(reached(board))
    frames = reader.closed()
    document.update(
        intervals=board.interval,
        every=every,
        frames=frames,
        books=board.books() if board.interval else {},
    )
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
    parser.add_argument("--intervals", type=int, default=None, help="the intervals (the world's own)")
    parser.add_argument(
        "--every", type=int, default=1, help="keep every K-th frame and the last (1, every frame)"
    )
    parser.add_argument("--out", type=Path, default=None, help="the look's file (<world>.look.json)")
    args = parser.parse_args(argv)
    target: Path = args.out or args.world.with_suffix(".look.json")
    document = record(args.world, args.intervals, args.every)
    arrays, length = written(document, target)
    summary: dict[str, Any] = {
        "world": args.world.name,
        "verdict": document["verdict"],
        "intervals": document["intervals"],
        "every": document["every"],
        "frames": len(document["frames"]),  # type: ignore[arg-type]
        "passes": passes_of(document["frames"]),  # type: ignore[arg-type]
        **({"reach": document["reach"]} if "reach" in document else {}),
        "arrays": arrays,
        "bytes": length,
        "look": str(target),
    }
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
