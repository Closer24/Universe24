"""The GameBoard layer of the algebra visualizer in 3-D: the Inside, a
diagnostic (docs/designs/algebra_visualizer/DESIGN_3D.md section 3).

One model of the board is read from a run's record and nothing else: the
Nodes' extents as a box, a layer or a chain (DECLARATION); the records'
presence over the intervals where the record shows it, the marks of every
event line at its Node at its tick (GAMEBOARD; a click's mark DETECTOR);
the blocks or bodies as cubes or boxes at the positions their own lines
give per interval (GAMEBOARD, never interpolated); the detectors as faces
or cells (DECLARATION) with the count of clicks each has received up to
the interval (DETECTOR); the probes' values per interval where declared;
the books per interval; the snapshot at the last interval under a cap.
The model is one JSON object on the page; the inline script draws the
board at the interval the slider selects and rotates it; without the
script the page shows the pre-rendered picture at the last interval.

Neither engine records the board's state per Node per interval (DESIGN_3D.md,
Finding 1); the panel says so and names what the run keeps. Nothing is
computed here beyond a sum of recorded integers (a Node's rows, a plane's
cells under the cap) and the placing of a mark at its recorded Node; the
projection's floats live in drawing coordinates alone.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any

from panels import Number, Panel
from record import RunRecord, chosen_of, node_of

# The cap on the snapshot's cells and on the marks written into the page
# (DESIGN_3D.md 3.5): beyond it, the planes' sums stand in for the cells and
# the caption names the cap.
CAP = 20_000

AXES = ("x", "y", "z")
FACE_NAMES = ("face:+x", "face:-x", "face:+y", "face:-y", "face:+z", "face:-z")
DETECTOR_EVENTS = {"gather", "click", "record"}


def board_form(shape: tuple[int, int, int]) -> str:
    ones = sum(1 for v in shape if v == 1)
    if ones >= 2:
        return "a chain"
    if ones == 1:
        return "a layer"
    return "a 3-D box"


# --- the model --------------------------------------------------------------


def cells_of(run: RunRecord) -> list[dict[str, Any]]:
    """The detectors as cells: every declared set's Nodes (DECLARATION), and
    every measured event as a cell of its own Nodes, named as the engine names
    it in a gather's `chosen` (`measured:<n>`, 1-based on the old engine, 0-based
    on the new)."""
    cells: list[dict[str, Any]] = []
    in_sets: set[tuple[int, int, int]] = set()
    for entry in run.declared_detectors():
        nodes = [tuple(int(v) for v in p) for p in entry.get("positions", []) if isinstance(p, list)]
        cells.append({"name": str(entry.get("name")), "nodes": nodes, "role": "detector"})
        in_sets.update(nodes)
    base = 0 if run.is_new else 1
    for index, entry in enumerate(run.declared_measured()):
        position = entry.get("position")
        if not isinstance(position, list) or len(position) != 3:
            continue
        node = (int(position[0]), int(position[1]), int(position[2]))
        role = "body"
        if "lamp" in entry:
            role = "emitter"
        elif "side" in entry:
            role = "block"
        cells.append(
            {
                "name": f"measured:{index + base}",
                "nodes": [node],
                "role": role,
                "in_set": node in in_sets,
                "family": str(entry.get("family", "")),
            }
        )
    return cells


def faces_of(run: RunRecord) -> list[dict[str, Any]]:
    """The open faces of light's board, from `boundary` (DECLARATION)."""
    faces = []
    for axis in AXES:
        if run.periodic(axis):
            continue
        faces.append({"name": f"face:+{axis}", "axis": axis, "positive": True})
        faces.append({"name": f"face:-{axis}", "axis": axis, "positive": False})
    return faces


def family_faces_of(run: RunRecord) -> list[dict[str, Any]]:
    """Under the massive key, each family's own faces (`families[].faces`,
    periodic where absent)."""
    if not run.massive:
        return []
    found = []
    families = run.meta.get("families")
    if not isinstance(families, list):
        return []
    for family in families:
        faces = family.get("faces") if isinstance(family, dict) else None
        if isinstance(faces, dict):
            found.append(
                {
                    "family": str(family.get("name")),
                    "faces": {a: str(faces.get(a, "periodic")) for a in AXES},
                }
            )
    return found


def objects_of(run: RunRecord) -> list[dict[str, Any]]:
    """The blocks (the new engine: a measured event with `side`, its corner per
    interval from its `block` lines) or the bodies (the old engine: `numbers[n]`
    with its `span`, its position per interval from its `step` lines). Each
    object's `positions` is the list of (tick, Node) where its own line moved
    it, the declared position first at tick 0; nothing between two lines is
    interpolated."""
    objects: list[dict[str, Any]] = []
    if run.is_new:
        for index, entry in enumerate(run.declared_measured()):
            if "side" not in entry:
                continue
            position = [int(v) for v in entry.get("position", [0, 0, 0])]
            positions: list[list[Any]] = [[0, position]]
            lines = run.block_lines_of(index)
            for line in lines:
                corner = line.get("corner")
                if isinstance(corner, list) and [int(v) for v in corner] != positions[-1][1]:
                    positions.append([int(line["tick"]), [int(v) for v in corner]])
            last = lines[-1] if lines else None
            objects.append(
                {
                    "name": f"block measured:{index}",
                    "family": str(entry.get("family", "")),
                    "side": int(entry["side"]),
                    "span": None,
                    "positions": positions,
                    "lines": len(lines),
                    "steps": int(last["steps"]) if last is not None and "steps" in last else None,
                    "sum": int(last["sum"]) if last is not None and "sum" in last else None,
                    "clock": int(last["clock"]) if last is not None and "clock" in last else None,
                    "source": "events.jsonl: block.corner; initialization.json: measured[].side",
                }
            )
        return objects
    numbers = run.meta.get("numbers")
    if not isinstance(numbers, dict):
        return objects
    for key, entry in numbers.items():
        if not isinstance(entry, dict):
            continue
        number = int(key)
        position = [int(v) for v in entry.get("position", [0, 0, 0])]
        positions = [[0, position]]
        lines = run.steps_of(number)
        for line in lines:
            to = line.get("to")
            if isinstance(to, list):
                positions.append([int(line["tick"]), [int(v) for v in to]])
        span = entry.get("span")
        objects.append(
            {
                "name": f"body {number}",
                "family": str(entry.get("family", "")),
                "side": None,
                "span": [int(v) for v in span] if isinstance(span, list) else [1, 1, 1],
                "positions": positions,
                "lines": len(lines),
                "steps": len(lines),
                "sum": None,
                "clock": None,
                "source": "events.jsonl: step.to; run.json: numbers[].position, numbers[].span",
            }
        )
    return objects


def marks_of(run: RunRecord) -> tuple[list[list[Any]], int]:
    """Every line with a Node and a tick as (tick, event, x, y, z, kind), up to
    the cap; the second value is the count left out."""
    marks: list[list[Any]] = []
    left = 0
    for line in run.with_node():
        if line.get("event") in ("block",):
            continue
        kind = "DETECTOR" if line.get("event") in DETECTOR_EVENTS else "GAMEBOARD"
        for node in node_of(line) or []:
            if len(marks) >= CAP:
                left += 1
                continue
            marks.append([int(line["tick"]), str(line["event"]), node[0], node[1], node[2], kind])
    return marks, left


def probes_of(run: RunRecord) -> dict[str, Any] | None:
    """The new engine's `probe` lines: the declared probe Nodes and the values
    per interval (GAMEBOARD, light's summed amplitude at each)."""
    lines = run.of_kind("probe")
    declared = run.world.get("probes")
    if not lines or not isinstance(declared, list):
        return None
    nodes = [[int(v) for v in p] for p in declared if isinstance(p, list) and len(p) == 3]
    values = [[int(line["tick"]), [int(v) for v in line.get("values", [])]] for line in lines]
    return {"nodes": nodes, "values": values}


def books_of(run: RunRecord) -> dict[str, Any]:
    """The books' totals per interval per family: `transit_content` and
    `measured_content` of `run.json` (one row per completed tick), GAMEBOARD."""
    families = run.meta.get("families")
    names = [str(f.get("name")) for f in families] if isinstance(families, list) else []
    transit = run.meta.get("transit_content")
    measured = run.meta.get("measured_content")
    return {
        "families": names,
        "transit": [[int(v) for v in row] for row in transit] if isinstance(transit, list) else [],
        "measured": [[int(v) for v in row] for row in measured] if isinstance(measured, list) else [],
    }


def snapshot_of(run: RunRecord) -> dict[str, Any]:
    """The snapshot at the last interval: on the old engine every Node of
    `state.json`'s `nodes` with the sum of its rows' `amount`; on the new engine
    each block's own record over the board (`blocks[].rows`, in the board's
    order, x fastest). Under the cap the cells are written; beyond it the sums
    per plane of the longest axis stand in (a sum of recorded integers)."""
    shape = run.shape
    cells: list[list[int]] = []
    source = ""
    if run.is_new:
        for block in run.blocks_snapshot():
            rows = block.get("rows")
            if not isinstance(rows, list):
                continue
            source = "state.json: blocks[].rows"
            x_n, y_n, z_n = shape
            for index, value in enumerate(rows):
                if not isinstance(value, int) or value == 0:
                    continue
                if x_n and y_n:
                    x = index % x_n
                    y = (index // x_n) % y_n if y_n else 0
                    z = index // (x_n * y_n) if y_n else 0
                else:
                    x, y, z = index, 0, 0
                if z >= max(z_n, 1):
                    x, y, z = index, 0, 0
                cells.append([x, y, z, int(value)])
    else:
        for node in run.nodes_with_rows():
            position = node.get("position")
            if not isinstance(position, list):
                continue
            total = 0
            for family in node.get("families", []):
                for ray in family.get("rays", []):
                    total += int(ray.get("amount", 0))
            source = "state.json: nodes[].families[].rays[].amount (summed per Node)"
            cells.append([int(position[0]), int(position[1]), int(position[2]), total])
    count = len(cells)
    if count > CAP:
        axis = max(range(3), key=lambda i: shape[i])
        sums: dict[int, int] = Counter()
        for cell in cells:
            sums[cell[axis]] += cell[3]
        planes = [[k, sums[k]] for k in sorted(sums)]
        return {
            "tick": run.ticks,
            "cells": [],
            "count": count,
            "planes": {"axis": axis, "sums": planes},
            "source": source,
        }
    return {"tick": run.ticks, "cells": cells, "count": count, "planes": None, "source": source}


def counts_of(
    run: RunRecord, cells: list[dict[str, Any]], faces: list[dict[str, Any]]
) -> dict[str, list[list[int]]]:
    """The count of clicks each cell or face has received, as (tick, count)
    at every change: the `gather` lines by `chosen`, and on the old engine the
    face `click` lines by `detector`. DETECTOR."""
    names = [c["name"] for c in cells] + [f["name"] for f in faces]
    running: dict[str, int] = dict.fromkeys(names, 0)
    series: dict[str, list[list[int]]] = {name: [] for name in names}
    for line in run.events:
        event = line.get("event")
        name: str | None = None
        if event == "gather":
            name = chosen_of(line)
        elif event == "click" and not run.is_new and str(line.get("detector", "")).startswith("face:"):
            name = str(line["detector"])
        if name is None or name not in running:
            continue
        running[name] += 1
        series[name].append([int(line["tick"]), running[name]])
    return series


def build_board(run: RunRecord) -> dict[str, Any]:
    cells = cells_of(run)
    faces = faces_of(run)
    marks, marks_left = marks_of(run)
    return {
        "engine": run.engine,
        "shape": list(run.shape),
        "form": board_form(run.shape),
        "ticks": run.ticks,
        "axes": [
            {"axis": a, "extent": run.shape[i], "periodic": run.periodic(a)} for i, a in enumerate(AXES)
        ],
        "faces": faces,
        "family_faces": family_faces_of(run),
        "cells": cells,
        "objects": objects_of(run),
        "marks": marks,
        "marks_left_out": marks_left,
        "probes": probes_of(run),
        "books": books_of(run),
        "snapshot": snapshot_of(run),
        "counts": counts_of(run, cells, faces),
    }


# --- the projection (floats in drawing coordinates alone) -------------------

YAW = 0.62
PITCH = 0.42


def project(
    x: float, y: float, z: float, yaw: float = YAW, pitch: float = PITCH
) -> tuple[float, float, float]:
    """An orthographic projection: yaw about the z axis, then a tilt about the
    screen's horizontal; returns (u, v, depth), v downwards. The inline script
    carries the same lines."""
    cy, sy = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)
    x1 = x * cy - y * sy
    y1 = x * sy + y * cy
    depth = y1 * cp - z * sp
    up = y1 * sp + z * cp
    return (x1, -up, depth)


# --- the panels of the layer ------------------------------------------------


def _keeps(run: RunRecord) -> str:
    if run.is_new:
        return (
            "This run keeps no row per Node per interval; it keeps the blocks' lines per interval "
            "(corner, steps, sum, clock), the probes where declared, the births and the clicks, and at "
            "the last interval each block's own record over the board and each live record's pointer "
            "per cell (DESIGN_3D.md, Finding 1)."
        )
    return (
        "This run keeps no per-Node state per interval; it keeps the events at their Nodes, the books "
        "per interval and the store's view at the last interval (DESIGN_3D.md, Finding 1)."
    )


def panel_board(run: RunRecord, board: dict[str, Any]) -> Panel:
    counts = Counter(m[1] for m in board["marks"])
    numbers = [
        Number("the GameBoard's form", board["form"], "DECLARATION", "run.json: shape"),
        Number(
            "the extents (x, y, z)",
            "(" + ", ".join(str(v) for v in board["shape"]) + ")",
            "DECLARATION",
            "run.json: shape",
        ),
        Number(
            "the faces (open axes)",
            ", ".join(f["name"] for f in board["faces"]) or "none, every axis periodic",
            "DECLARATION",
            "run.json: boundary",
        ),
        Number("the intervals", str(board["ticks"]), "GAMEBOARD", "run.json: completed_ticks"),
        Number(
            "event lines with a Node (the marks)",
            str(len(board["marks"])),
            "GAMEBOARD",
            "events.jsonl: *.node, *.tick",
        ),
    ]
    for event, count in sorted(counts.items()):
        kind = "DETECTOR" if event in DETECTOR_EVENTS else "GAMEBOARD"
        numbers.append(
            Number(f"marks of the event {event}", str(count), kind, f"events.jsonl: {event}.node")
        )
    if board["marks_left_out"]:
        numbers.append(
            Number(
                "marks beyond the cap, left out of the page",
                str(board["marks_left_out"]),
                "HOST",
                f"the cap {CAP} (DESIGN_3D.md 3.5)",
            )
        )
    for ff in board["family_faces"]:
        numbers.append(
            Number(
                f"the family {ff['family']}'s own faces",
                ", ".join(f"{a} {ff['faces'][a]}" for a in AXES),
                "DECLARATION",
                "run.json: families[].faces",
            )
        )
    if board["probes"]:
        numbers.append(
            Number(
                "probe Nodes",
                str(len(board["probes"]["nodes"])),
                "DECLARATION",
                "initialization.json: probes",
            )
        )
        numbers.append(
            Number(
                "probe lines (one per interval)",
                str(len(board["probes"]["values"])),
                "GAMEBOARD",
                "events.jsonl: probe.values",
            )
        )
    books = board["books"]
    if books["transit"]:
        numbers.append(
            Number(
                "books' rows (one per completed tick)",
                str(len(books["transit"])),
                "GAMEBOARD",
                "run.json: transit_content, measured_content",
            )
        )
    return Panel(
        key="board",
        layer=2,
        title="The board in 3-D: the box, the marks of the record over the intervals, the blocks, the cells",
        algebra=[
            (
                "Inside is the GameBoard: Nodes on the cubic lattice, integer rows on them, and the tick, the interval's count, which no detector ever reads; where no one measures.",
                "ALGEBRA.md 3.1",
            ),
            (
                "A click at a detector, a count between clicks on the detector's own record, and a ratio of such counts are what is compared with nature; nothing measured inside the board is compared; a reading of the board itself is a diagnostic.",
                "ALGEBRA.md 3.2, the reading rule",
            ),
        ],
        note=_keeps(run)
        + " The board at the interval t shows the marks of the lines up to t (the tick t's full, the earlier fading), each block where its own line puts it, each cell with the clicks it has received; drag to rotate. The tick is GAMEBOARD, the record's ordering.",
        numbers=numbers,
        figure={"kind": "board3d", "board": board},
    )


def panel_board_objects(run: RunRecord, board: dict[str, Any]) -> Panel:
    objects = board["objects"]
    if not objects:
        return Panel(
            "board_objects",
            2,
            "The blocks as cubes, moving by their recorded steps",
            missing="no block or body declared in this run",
        )
    numbers: list[Number] = []
    table: list[list[tuple[str, str, str]]] = []
    for obj in objects:
        label = obj["name"] + (f" ({obj['family']})" if obj["family"] else "")
        if obj["side"] is not None:
            numbers.append(
                Number(
                    f"{label}: side",
                    str(obj["side"]),
                    "DECLARATION",
                    "initialization.json: measured[].side",
                )
            )
        else:
            numbers.append(
                Number(
                    f"{label}: span",
                    "(" + ", ".join(str(v) for v in obj["span"]) + ")",
                    "DECLARATION",
                    "run.json: numbers[].span",
                )
            )
        numbers.append(
            Number(
                f"{label}: declared position",
                "(" + ", ".join(str(v) for v in obj["positions"][0][1]) + ")",
                "DECLARATION",
                "run.json: numbers[].position",
            )
        )
        numbers.append(
            Number(
                f"{label}: lines that moved it",
                str(len(obj["positions"]) - 1),
                "GAMEBOARD",
                obj["source"],
            )
        )
        numbers.append(
            Number(
                f"{label}: position at the last line",
                "(" + ", ".join(str(v) for v in obj["positions"][-1][1]) + ")",
                "GAMEBOARD",
                obj["source"],
            )
        )
        if obj["steps"] is not None:
            numbers.append(
                Number(
                    f"{label}: steps",
                    str(obj["steps"]),
                    "GAMEBOARD",
                    "events.jsonl: block.steps" if obj["side"] is not None else "events.jsonl: step",
                )
            )
        if obj["sum"] is not None:
            numbers.append(
                Number(
                    f"{label}: its own record's sum over its cells at the last line",
                    str(obj["sum"]),
                    "GAMEBOARD",
                    "events.jsonl: block.sum",
                )
            )
        if obj["clock"] is not None:
            numbers.append(
                Number(
                    f"{label}: its count on its last line",
                    str(obj["clock"]),
                    "GAMEBOARD",
                    "events.jsonl: block.clock (the host's copy; the DETECTOR count is the click line's)",
                )
            )
        for tick, node in obj["positions"]:
            table.append(
                [
                    (obj["name"], "DECLARATION", obj["source"]),
                    (str(tick), "GAMEBOARD", obj["source"]),
                    ("(" + ", ".join(str(v) for v in node) + ")", "GAMEBOARD", obj["source"]),
                ]
            )
    if run.is_new:
        for block in run.blocks_snapshot():
            name = f"block measured:{block.get('measured')}"
            for key in ("corner", "steps", "drive", "momentum", "responses", "clock"):
                if key in block:
                    value = block[key]
                    text = (
                        "(" + ", ".join(str(int(v)) for v in value) + ")"
                        if isinstance(value, list)
                        else str(value)
                    )
                    numbers.append(
                        Number(
                            f"{name} at the last interval: {key}",
                            text,
                            "GAMEBOARD",
                            f"state.json: blocks[].{key}",
                        )
                    )
    else:
        for body in run.bodies():
            name = f"body {body.get('number')}"
            for key in ("position", "steps", "axis_steps", "drive", "momentum"):
                if key in body:
                    value = body[key]
                    text = (
                        "(" + ", ".join(str(int(v)) for v in value) + ")"
                        if isinstance(value, list)
                        else str(value)
                    )
                    numbers.append(
                        Number(
                            f"{name} at the last interval: {key}",
                            text,
                            "GAMEBOARD",
                            f"state.json: measured[].{key}",
                        )
                    )
    return Panel(
        key="board_objects",
        layer=2,
        title="The blocks as cubes, moving by their recorded steps",
        algebra=[
            (
                "A body's own record (its momentum, its place, its `become`) is GAMEBOARD and enters no comparison.",
                "ALGEBRA.md 3.2",
            )
        ],
        note="A block is where its own line puts it and nowhere between: its corner (the new engine's block line) or its position (the old engine's step line) changes by one Link at the line's tick and is never interpolated. The table lists every line that moved each object.",
        numbers=numbers,
        figure={"kind": "table", "head": ["object", "tick", "position"], "rows": table},
    )


def panel_board_cells(run: RunRecord, board: dict[str, Any]) -> Panel:
    cells = board["cells"]
    faces = board["faces"]
    if not cells and not faces:
        return Panel(
            "board_cells",
            2,
            "The detectors as faces or cells",
            missing="no detector set, measured event or open face declared",
        )
    numbers: list[Number] = []
    table: list[list[tuple[str, str, str]]] = []
    counts = board["counts"]
    for cell in cells:
        total = counts.get(cell["name"], [])
        role = cell["role"] + (", in a declared set" if cell.get("in_set") else "")
        numbers.append(
            Number(
                f"{cell['name']} ({role}): Nodes",
                str(len(cell["nodes"])),
                "DECLARATION",
                "initialization.json: detectors[].positions, measured[].position",
            )
        )
        numbers.append(
            Number(
                f"{cell['name']}: clicks received",
                str(total[-1][1] if total else 0),
                "DETECTOR",
                "events.jsonl: gather.chosen",
            )
        )
        for tick, count in total:
            table.append(
                [
                    (cell["name"], "DECLARATION", "initialization.json: detectors[].name"),
                    (str(tick), "GAMEBOARD", "events.jsonl: gather.tick"),
                    (str(count), "DETECTOR", "events.jsonl: gather.chosen"),
                ]
            )
    for face in faces:
        total = counts.get(face["name"], [])
        numbers.append(
            Number(
                f"{face['name']} (an open face, a detector): clicks received",
                str(total[-1][1] if total else 0),
                "DETECTOR",
                "events.jsonl: click.detector, gather.chosen",
            )
        )
        for tick, count in total:
            table.append(
                [
                    (face["name"], "DECLARATION", "run.json: boundary"),
                    (str(tick), "GAMEBOARD", "events.jsonl: click.tick"),
                    (str(count), "DETECTOR", "events.jsonl: click.detector"),
                ]
            )
    for cell in cells:
        for node in cell["nodes"]:
            table.append(
                [
                    (cell["name"], "DECLARATION", "initialization.json: detectors[].name"),
                    ("Node", "DECLARATION", "initialization.json: detectors[].positions"),
                    (
                        "(" + ", ".join(str(v) for v in node) + ")",
                        "DECLARATION",
                        "initialization.json: detectors[].positions, measured[].position",
                    ),
                ]
            )
    return Panel(
        key="board_cells",
        layer=2,
        title="The detectors as faces or cells, with the clicks each has received",
        algebra=[
            (
                "A detector is a declared set of measured events with one record; a click says 'here, in one of these'; a measured event outside every declared detector is a detector of one Node; an open face of the GameBoard is a detector.",
                "TERMINOLOGY.md, Detector; Face, face detector",
            )
        ],
        note="Each cell's count of clicks up to the interval t grows on the board as the slider moves: the gather lines whose chosen cell it is, and on the old engine the face click lines. The counts are the Outside's, placed on the Inside; they keep their DETECTOR kind.",
        numbers=numbers,
        figure={"kind": "table", "head": ["cell", "tick", "clicks so far"], "rows": table},
    )


def panel_board_snapshot(run: RunRecord, board: dict[str, Any]) -> Panel:
    snap = board["snapshot"]
    if snap["count"] == 0 and not board["probes"] and not board["books"]["transit"]:
        return Panel(
            "board_snapshot",
            2,
            "The snapshot at the last interval, and what the run keeps per Node",
            note=_keeps(run),
            missing="no per-Node value at the last interval (no rows in the store, no block record, no probe) and no books per interval",
        )
    numbers = [
        Number("the snapshot's interval", str(snap["tick"]), "GAMEBOARD", "state.json: tick"),
        Number(
            "Nodes with a value at the last interval",
            str(snap["count"]),
            "GAMEBOARD",
            snap["source"] or "state.json",
        ),
    ]
    table: list[list[tuple[str, str, str]]] = []
    if snap["planes"]:
        axis = AXES[snap["planes"]["axis"]]
        numbers.append(
            Number(
                f"the cap; the sums per plane of the axis {axis} stand in for the cells",
                str(CAP),
                "HOST",
                "DESIGN_3D.md 3.5",
            )
        )
        for k, total in snap["planes"]["sums"]:
            table.append(
                [
                    (f"{axis} = {k}", "GAMEBOARD", snap["source"]),
                    (str(total), "GAMEBOARD", snap["source"] + " (summed per plane)"),
                ]
            )
        head = ["plane", "sum of the cells"]
    else:
        values = [c[3] for c in snap["cells"]]
        if values:
            numbers.append(Number("the least value", str(min(values)), "GAMEBOARD", snap["source"]))
            numbers.append(Number("the greatest value", str(max(values)), "GAMEBOARD", snap["source"]))
            numbers.append(
                Number(
                    "the sum over the Nodes", str(sum(values)), "GAMEBOARD", snap["source"] + " (summed)"
                )
            )
        for x, y, z, value in snap["cells"]:
            table.append(
                [
                    (f"({x}, {y}, {z})", "GAMEBOARD", snap["source"]),
                    (str(value), "GAMEBOARD", snap["source"]),
                ]
            )
        head = ["Node", "value"]
    probes = board["probes"]
    if probes:
        for index, node in enumerate(probes["nodes"]):
            last = probes["values"][-1]
            value = last[1][index] if index < len(last[1]) else 0
            numbers.append(
                Number(
                    f"probe at ({node[0]}, {node[1]}, {node[2]}): light's summed amplitude at the last interval",
                    str(value),
                    "GAMEBOARD",
                    "events.jsonl: probe.values",
                )
            )
        for tick, values in probes["values"]:
            for index, value in enumerate(values):
                node = probes["nodes"][index] if index < len(probes["nodes"]) else [0, 0, 0]
                table.append(
                    [
                        (
                            f"probe ({node[0]}, {node[1]}, {node[2]}) at t = {tick}",
                            "GAMEBOARD",
                            "events.jsonl: probe.tick",
                        ),
                        (str(value), "GAMEBOARD", "events.jsonl: probe.values"),
                    ]
                )
    if run.is_new:
        for record in run.records_snapshot():
            pointers = record.get("pointers")
            if isinstance(pointers, dict):
                for cell, pointer in pointers.items():
                    table.append(
                        [
                            (
                                f"record {record.get('record')}: pointer at {cell}",
                                "GAMEBOARD",
                                "state.json: records[].pointers",
                            ),
                            (str(pointer), "GAMEBOARD", "state.json: records[].pointers"),
                        ]
                    )
    books = board["books"]
    for t_index, row in enumerate(books["transit"]):
        for f_index, value in enumerate(row):
            name = books["families"][f_index] if f_index < len(books["families"]) else str(f_index)
            table.append(
                [
                    (
                        f"{name} in transit at t = {t_index + 1}",
                        "GAMEBOARD",
                        "run.json: transit_content",
                    ),
                    (str(value), "GAMEBOARD", "run.json: transit_content"),
                ]
            )
    for t_index, row in enumerate(books["measured"]):
        for f_index, value in enumerate(row):
            name = books["families"][f_index] if f_index < len(books["families"]) else str(f_index)
            table.append(
                [
                    (f"{name} measured at t = {t_index + 1}", "GAMEBOARD", "run.json: measured_content"),
                    (str(value), "GAMEBOARD", "run.json: measured_content"),
                ]
            )
    return Panel(
        key="board_snapshot",
        layer=2,
        title="The snapshot at the last interval, the probes, the books per interval, and what the run keeps per Node",
        algebra=[
            (
                "The store is a report of the host, not a thing of the law; the books are a GameBoard reading.",
                "TERMINOLOGY.md, The store; Books",
            )
        ],
        note=_keeps(run)
        + " The cells drawn on the board at the last interval are these values; the books' totals per family per interval are the strip under the board.",
        numbers=numbers,
        figure={"kind": "table", "head": head, "rows": table},
    )


def build_layer(run: RunRecord) -> tuple[dict[str, Any], list[Panel]]:
    board = build_board(run)
    return board, [
        panel_board(run, board),
        panel_board_objects(run, board),
        panel_board_cells(run, board),
        panel_board_snapshot(run, board),
    ]
