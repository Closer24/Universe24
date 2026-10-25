"""Hand q1 (2026-10-25): (c) the self-read and (d) two species on one row, on the branch's engine at den 1,105 = 5 x 13 x 17 (three lifts, three plane lines) on the bare 3-cube torus, no change to src/.

Two Link births of different lines at one Node: the + child of the lift A on A's record 1 at i = (1, 1, 1) and its - child on A's record 0 at j = (2, 1, 1) (the Link along x); the + child of the lift B at the same i on B's record 1 and its - child at k = (1, 2, 1) (the Link along y); each laid by the engine's own lay by the count (`act.born_items`, `act.click`) after the first interval, the light's hole not taken (the lay alone is measured, named). Then 12 intervals; at every interval, at i: the holder of the sign's rows (the free row 0, A's two rows, B's two rows): the time level and the write remainder less its origin over the write's wall, integers; the one row (every row summed) against the engine's read (every row but the reader's own) for each + child, integers; each born record's Wronskian at i; and the decoder's point of each child's lines at i (`reports.point_of` from the three levels around the step, the reduced pair (num, den)), so whether the clicks name the species where the row cannot.

Usage: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/open_items/H-Sign-Under-One-Row-1/two_species_self_read.py ; writes two_species_self_read.json beside it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from event_universe import meeting_board, records, registry, world_files  # noqa: E402
from event_universe.act import click  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.reports import point_of  # noqa: E402
from event_universe.take import Item  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import SMALL, small_universe  # noqa: E402

OUT = Path(__file__).resolve().parent
TMP = Path("/dev/shm/tmp/q1_two_species")
DEN = 1105
I, J, K = (1, 1, 1), (2, 1, 1), (1, 2, 1)


def board_at(den: int, intervals: int) -> Lattice:
    TMP.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = TMP
    small_universe(TMP)
    (TMP / "u.json").write_text(json.dumps({"integers": {**SMALL["integers"], "den": den}}), "utf-8")
    world = {"universe": "u.json", "shape": [3, 3, 3], "intervals": intervals}
    (TMP / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    return Lattice(load_world(TMP / "bare.json"))


def rows_at(board: Lattice, at: tuple[int, int, int]) -> dict[str, Any]:
    sign = next(k for k, f in enumerate(board.families) if f.held and f.wronskian)
    family, state = board.families[sign], board.states[sign]
    width = family.width
    rows = registry.records_of(family, state.lines)
    divided = records.divided_walls(family, board.fixed_walls[sign], board.world.node_clock)
    found = []
    for r in range(rows):
        level = int(state.lines[r * width].now[at])
        rem = int(np.asarray(state.write_remainders[r * width], dtype=object)[at])
        wall_arr = np.asarray(divided[r * width], dtype=object)
        wall = int(wall_arr[at]) if wall_arr.ndim else int(wall_arr)
        found.append({"row": r, "level": level, "remainder_less_origin": rem - wall // 2, "wall": wall})
    return {"rows": found, "wall_bits": max(x["wall"].bit_length() for x in found)}


def main() -> None:
    board = board_at(DEN, 20)
    meeting_board.closed = lambda b, begun: None  # the board's own Node close off: the lays alone are measured
    names = [f.name for f in board.families]
    lifts = sorted(
        (k for k, f in enumerate(board.families) if f.records == 2), key=lambda k: board.families[k].pair[0]
    )  # the three lifts, the heavier first by num: (425, 1020), (663, 884), (975, 520)
    a, b = lifts[1], lifts[2]
    board.step()
    items = []
    for family, minus_at in ((a, J), (b, K)):
        den = board.families[family].pair[1]
        items.append(Item(family, 1, (minus_at,), (den, den), sense=-1, record=0))
        items.append(Item(family, 1, (I,), (den, den), sense=1, record=1))
    click(board, items)
    sign = next(k for k, f in enumerate(board.families) if f.held and f.wronskian)
    own_rows = {
        (family, record): registry.row_of(board.families, board.states, family, record)
        for family in (a, b)
        for record in (0, 1)
    }
    course = []
    for _ in range(12):
        board.step()
        reading = {"interval": board.interval, "at_i": rows_at(board, I), "at_j": rows_at(board, J), "at_k": rows_at(board, K)}
        rows_i = reading["at_i"]["rows"]
        wall = rows_i[0]["wall"]
        fine = [x["level"] * x["wall"] + x["remainder_less_origin"] for x in rows_i]  # the row in units of 1 / wall, integers
        reading["one_row_at_i_over_wall"] = (sum(fine), wall)
        reading["rows_but_own_at_i_over_wall"] = {
            f"{names[family]} record {record} (row {row})": (sum(fine) - fine[row], wall)
            for (family, record), row in own_rows.items()
        }
        reading["wronskian_at_i"] = {
            f"{names[family]} record {record}": int(np.asarray(records.wronskian(board.lines_of(family, record), True), dtype=object)[I])
            for family in (a, b)
            for record in (0, 1)
        }
        reading["points_at_i"] = {}
        for family in (a, b):
            for record in (0, 1):
                lines = board.lines_of(family, record)
                reading["points_at_i"][f"{names[family]} record {record}"] = [
                    None
                ]  # filled below from the three levels around the step
        course.append(reading)
    # the decoder's point: three levels around one step at i, read by stepping one more interval on copies of the levels
    begun = {(f, r): [(int(l.now[I]), int(l.before[I])) for l in board.lines_of(f, r)] for f in (a, b) for r in (0, 1)}
    board.step()
    points = {}
    for (f, r), levels in begun.items():
        after = [int(l.now[I]) for l in board.lines_of(f, r)]
        points[f"{names[f]} record {r}"] = [point_of(before, now, nxt) for (now, before), nxt in zip(levels, after, strict=True)]
    found = {
        "den": DEN,
        "lifts": {names[k]: list(board.families[k].pair) for k in lifts},
        "species_laid": {"A": names[a], "B": names[b]},
        "pairs": {"A": list(board.families[a].pair), "B": list(board.families[b].pair)},
        "sign_rows_count": registry.records_of(board.families[sign], board.states[sign].lines),
        "own_rows": {f"{names[f]} record {r}": row for (f, r), row in own_rows.items()},
        "course": course,
        "decoder_points_at_i_after_the_run": points,
        "largest_bits_state": max(
            int(np.asarray(x, dtype=object).reshape(-1)[0]).bit_length() if np.asarray(x, dtype=object).size else 0
            for s in board.states
            for line in s.lines
            for x in (np.abs(np.asarray(line.now, dtype=object)).max(), np.abs(np.asarray(line.remainder, dtype=object)).max())
        ),
    }
    (OUT / "two_species_self_read.json").write_text(json.dumps(found, indent=1, default=str))
    print("species", found["species_laid"], found["pairs"], "rows", found["sign_rows_count"], "own rows", found["own_rows"])
    for c in course:
        print(
            c["interval"],
            "one row at i:",
            c["one_row_at_i_over_wall"],
            "| rows but own:",
            c["rows_but_own_at_i_over_wall"],
            "| W:",
            c["wronskian_at_i"],
        )
    print("decoder points at i:", points)
    print("largest bits", found["largest_bits_state"])


if __name__ == "__main__":
    main()
