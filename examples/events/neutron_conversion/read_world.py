"""The neutron conversion's reader (the two hands' blind, #1572 comments 5963954612 (c), 5964082980 (c), 5964484844 and 5964520368): the world is loaded as the runner loads it and stepped by the engine's own step with an observer, once per seed of the design's trials (the record's generator at the trials tool's state, the seed times the records declared NodeReaders plus the record's number), and the blind's rows are read from the GameBoard, the lines and the books, every number a GameBoard reading labelled so unless it is a node_reader's line: over the first seed's run and the first converting seed's, at the start and at the conversion's interval, every family's lines at the Node (the levels now and before and Rule3's remainders), each record's rotation read from its levels (cos omega = before / now on a real line, (re re_b + im im_b) / (re^2 + im^2) on a plane), the Wronskian per family at the Node and summed, the holders of the sign's rows at the Node with the Nodes each row's level stands on (per interval over the run, the sign row written at the conversion), the reader's counts and the credit's counts, the share per family at the Node and over the board in the current's units and in quanta beside the count, the energies T sin omega in and out, the back-in-time gate before the conversion, after it and across it; over every seed the conversion's interval and the realised conversions against the design's expectation. The tool holds no number of the law and compares nothing.

PYTHONPATH=src python examples/events/neutron_conversion/read_world.py --expectation examples/events/neutron_conversion/expectation.json examples/events/neutron_conversion/neutron_conversion.json
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import node
from event_universe.game_board import GameBoard
from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[2] / "tools"


def back_in_time() -> Any:
    """The back-in-time gate's module, loaded from tools/ by its path."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("back_in_time", TOOLS / "back_in_time.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def loaded(path: Path, seed: int) -> GameBoard:
    """The world loaded with every record's generator at the trial's state (tools/meeting_trials.py), the lines kept on the board."""
    board = GameBoard(load_world(path), (lines := []).append)
    board.read_lines = lines  # type: ignore[attr-defined]
    for books in board.credit.bodies:
        books.state = seed * len(board.credit.bodies) + books.number
    return board


def rotation_of(levels: list[list[int]], plane: bool) -> float | None:
    """A record's rotation read from its lines' levels at the Node, cos omega = before / now on a real line and (re re_b + im im_b) / (re^2 + im^2) on a plane, over its first line or plane; None where the level now is 0."""
    (now, before, _r), *rest = levels
    if plane:
        im_now, im_before, _r2 = rest[0]
        norm = now * now + im_now * im_now
        if norm == 0:
            return None
        return math.acos(max(-1.0, min(1.0, (now * before + im_now * im_before) / norm)))
    if now == 0:
        return None
    return math.acos(max(-1.0, min(1.0, before / now)))


def at_node(board: GameBoard, index: int, here: tuple[int, int, int]) -> dict[str, Any]:
    """One family's reading at the Node: its lines' levels and remainders, its rotation, its Wronskian there, its share at the Node and over the board in the current's units and in quanta, the credit's count."""
    family, state = board.families[index], board.states[index]
    levels = [
        [int(r.now[here]), int(r.before[here]), int(r.remainder[here])]
        for r in state.lines[: family.lines]
    ]
    share, _frozen = board.share_of(index)
    wall = count_wall(family, board.world.quantum_action)
    rotation = rotation_of(levels, family.plane)
    return {
        "lines": levels,
        "rotation": rotation,
        "sine": None if rotation is None else math.sin(rotation),
        "wronskian": int(np.asarray(node.wronskian(state.lines, family.plane))[here])
        if family.plane
        else 0,
        "share_at_the_node": int(share[here]),
        "share_total": int(share.sum(dtype=object)),
        "quanta_at_the_node": int(share[here]) / wall,
        "quanta_total": int(share.sum(dtype=object)) / wall,
        "credit_count": board.credit.counts[index],
    }


def sign_rows(board: GameBoard, here: tuple[int, int, int]) -> dict[str, Any]:
    """The holders of the sign at the Node, a GameBoard reading: per holder its rows' levels now at the Node (the free row 0, then one row per charged record in the file's order, the proton's and the electron's) and per row the Nodes carrying a level other than 0 (the row written, and the massless row carrying it away)."""
    return {
        board.families[i].name: {
            "at_the_node": [int(line.now[here]) for line in rows],
            "nodes_carrying_a_level": [int((line.now != 0).sum()) for line in rows],
        }
        for i in board.held
        if board.families[i].wronskian
        for rows in [board.states[i].lines[: board.families[i].records]]
    }


def readings(board: GameBoard, here: tuple[int, int, int], quanta: list[int]) -> dict[str, Any]:
    """Every family of quanta's reading at the Node, the holders of the sign's rows there (`sign_rows`), the reader's counts, the rotations' sum, the sines and the energies T sin omega."""
    found = {board.families[i].name: at_node(board, i, here) for i in quanta}
    action = board.world.quantum_action
    rotations = {name: r["rotation"] for name, r in found.items()}
    return {
        "interval": board.tick,
        "families": found,
        "sign_rows": sign_rows(board, here),
        "node_reader_counts": [list(b.counts) for b in board.credit.bodies],
        "rotations": rotations,
        "energies_T_sin_omega": {
            name: None if r is None else action * math.sin(r) for name, r in rotations.items()
        },
    }


def first_trial(path: Path, seed: int, intervals: int) -> dict[str, Any]:
    """The first seed's run read in full: the start, the conversion's interval and the run's end, the lines, the books and the back-in-time gate before, after and across the conversion."""
    board = loaded(path, seed)
    index = board.world.bodies[0].family
    here = tuple(int(a) + b for a, b in zip(board.world.bodies[0].nodes[0], board.offset, strict=True))
    node_at = (here[0], here[1], here[2])
    quanta = list(board.order)
    start = readings(board, node_at, quanta)
    conversion: dict[str, Any] | None = None
    rows_by_interval: list[list[Any]] = []  # the sign holders' rows at the Node per interval
    for _ in range(intervals):
        board.step()
        lines: list[dict[str, Any]] = board.read_lines  # type: ignore[attr-defined]
        if conversion is None and any(line["event"] == "conversion" for line in lines):
            conversion = readings(board, node_at, quanta)
            conversion["line"] = next(line for line in lines if line["event"] == "conversion")
        rows_by_interval.append(
            [board.tick, {n: r["at_the_node"] for n, r in sign_rows(board, node_at).items()}]
        )
        if board.ended is not None:
            break
    lines = board.read_lines  # type: ignore[attr-defined]
    k = conversion["interval"] if conversion is not None else None
    gate = back_in_time()
    crossing: dict[str, Any] = {}
    if k is not None:
        before = loaded(path, seed)
        crossing["before_the_conversion"] = gate.verdict(before, max(k - 2, 0)) if k >= 2 else None
        after = loaded(path, seed)
        for _ in range(k):
            after.step()
        crossing["after_the_conversion"] = gate.verdict(after, max(intervals - k - 1, 0))
        across = loaded(path, seed)
        for _ in range(max(k - 2, 0)):
            across.step()
        crossing["across_the_conversion"] = gate.verdict(across, 2)
    neutron = board.families[index].name
    out = {
        "seed": seed,
        "node": list(board.world.bodies[0].nodes[0]),
        "start": start,
        "conversion": conversion,
        "end": readings(board, node_at, quanta),
        "sign_rows_at_the_node_by_interval": rows_by_interval,
        "rotations_sum": None
        if conversion is None
        else {
            "in_at_the_start": start["rotations"][neutron],
            "out_at_the_conversion": sum(
                r for name, r in conversion["rotations"].items() if name != neutron and r is not None
            ),
            "out_by_family": {n: r for n, r in conversion["rotations"].items() if n != neutron},
        },
        "sines": None
        if conversion is None
        else {
            "in": start["families"][neutron]["sine"],
            "out": sum(
                r["sine"] for name, r in conversion["families"].items() if name != neutron and r["sine"]
            ),
        },
        "wronskian_sum_at_the_conversion": None
        if conversion is None
        else sum(r["wronskian"] for r in conversion["families"].values()),
        "back_in_time": crossing,
        "lines": {
            kind: [line for line in lines if line["event"] == kind]
            for kind in ("conversion", "lay", "face", "click", "credit", "erasure")
        },
        "books": board.books(),
    }
    return out


def trials(path: Path, seeds: list[int], intervals: int) -> dict[str, Any]:
    """Every seed's run: the conversion's interval (None where none in the run) and the realised conversions."""
    when: dict[int, int | None] = {}
    several = 0
    for seed in seeds:
        board = loaded(path, seed)
        for _ in range(intervals):
            board.step()
            if board.ended is not None:
                break
        lines: list[dict[str, Any]] = board.read_lines  # type: ignore[attr-defined]
        ticks = [int(line["tick"]) for line in lines if line["event"] == "conversion"]
        when[seed] = ticks[0] if ticks else None
        several += len(ticks) > 1
    realised = [k for k in when.values() if k is not None]
    return {
        "trials": len(seeds),
        "intervals": intervals,
        "converted": len(realised),
        "conversion_intervals": when,
        "mean_conversion_interval": sum(realised) / len(realised) if realised else None,
        "runs_with_more_than_one_conversion": several,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("worlds", type=Path, nargs="+", help="the world files")
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    parser.add_argument(
        "--design", type=Path, default=HERE / "design.json", help="the design, its trials"
    )
    parser.add_argument("--first-only", action="store_true", help="the first seed's run alone")
    args = parser.parse_args(argv)
    blind = json.loads(args.expectation.read_text(encoding="utf-8"))
    design = json.loads(args.design.read_text(encoding="utf-8"))
    seeds = [int(s) for s in design["trials"]["seeds"]]
    intervals = int(design["trials"]["intervals"])
    found: dict[str, Any] = {"label": "GAMEBOARD", "blind": blind["blind"], "readings": {}}
    for path in args.worlds:
        reading = {"first_seed": first_trial(path, seeds[0], intervals)}
        if not args.first_only:
            reading["trials"] = trials(path, seeds, intervals)
            when = reading["trials"]["conversion_intervals"]
            first = next((seed for seed in seeds if when[seed] is not None), None)
            if (
                first is not None and first != seeds[0]
            ):  # the first seed whose run converts, read in full too
                reading["first_converting_seed"] = first_trial(path, first, intervals)
        found["readings"][path.stem] = reading
    print(json.dumps(found, indent=1, default=str))


if __name__ == "__main__":
    main()
