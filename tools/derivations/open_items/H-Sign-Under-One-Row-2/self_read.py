"""The self-read of the sign under one row (hand q2, 2026-10-25; ALGEBRA.md, No record reads its own write of the sign): the born pair's own write against the other's at the children's Nodes, measured on the branch's engine with no edit of src/.

The engine writes one row of the sign per born record and lets each record read every row but its own (records.row_levels with the reader's row skipped); the sum of the rows is the one row the generic Node would hold. On the bare 3-cube at den 1,021 one pair is laid by the birth's own path at one Node (the one-Node birth, both children at (1, 1, 1); tests/test_the_birth_is_a_list_of_records.born_here) or at the two ends of one Link (the Link birth, the + child at (1, 1, 1) and the - child at (2, 1, 1)), the board's own meetings emptied, and the board is stepped; at every interval the + child's row and the - child's row are read at the two children's Nodes: own is the level the + child's own row holds at the + child's Node, other the - child's row there, the fraction own / (|own| + |other|) the share of the potential a record reads that is its own write where nothing is excluded, and the potential read with the exclusion (the other's row) against without (the sum). Beside it the same run under the self-read (records.row_levels and node.row_levels patched to skip nothing): the + child's share at its birth Node over its share on the board, with and without the self-read, the spread the self-read adds. Every number from the engine's own functions; nothing of src/ changed.

    PYTHONPATH=src python tools/derivations/open_items/H-Sign-Under-One-Row-2/self_read.py --intervals 24 --out tools/derivations/open_items/H-Sign-Under-One-Row-2/self_read.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
for place in (str(ROOT), str(ROOT / "src")):
    if place not in sys.path:
        sys.path.insert(0, place)

import numpy as np  # noqa: E402

from event_universe import conversion, meeting_board, node, records, registry, world_files  # noqa: E402
from event_universe.act import click  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.lay import laid  # noqa: E402
from event_universe.loader.derived import count_wall  # noqa: E402
from event_universe.take import Item  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import SMALL  # noqa: E402

Node = tuple[int, int, int]
REAL_ROW_LEVELS = records.row_levels


def row_levels_unskipped(family: Any, lines: Any, line: int, direction: int, skip: int | None) -> Any:
    """Every row summed, the reader's own among them: the one row the generic Node holds."""
    return REAL_ROW_LEVELS(family, lines, line, direction, None)


def per_mille(part: int, whole: int) -> int:
    """part over whole in thousandths by the division act, the remainder dropped; 0 at a whole of 0."""
    return 0 if whole == 0 else (1000 * part) // whole


def board_of(folder: Path, den: int, lines: list[dict[str, Any]]) -> Lattice:
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    (folder / "u.json").write_text(json.dumps({"integers": {**SMALL["integers"], "den": den}}), "utf-8")
    (folder / "bare.json").write_text(json.dumps({"universe": "u.json", "shape": [3, 3, 3], "intervals": 60}), "utf-8")
    meeting_board.meetings = lambda b, i, s, f: []
    return Lattice(load_world(folder / "bare.json"), output=lines.append)


def born(board: Lattice, plus: Node, minus: Node) -> int:
    """The pair laid by the birth's own path: the light at each child's Node holed by the exact take of one child's wall (two walls at one Node for the one-Node birth), the children laid through the one click act, the + child on the record 1 at `plus` and the - child on the record 0 at `minus`."""
    light = board.world.seed
    span = records.record_slice(board.families[light], 0)
    tables = conversion.birth_of(board.families, light)
    child = min((t[0][0] for t in tables), key=lambda k: count_wall(board.families[k], board.world.quantum_action))
    den, wall = board.families[child].pair[1], count_wall(board.families[child], board.world.quantum_action)
    demand = {}
    for at in (plus, minus):
        demand[at] = demand.get(at, 0) + 1
    for at in demand:  # the hole as tests/test_the_birth_is_a_list_of_records.born_here lays it: the light at the Node to the state of a Node with no level (one quantum of the sea cannot pay the exact take of two walls at the start; named, no take here)
        here = board.mask((at,))
        for number in range(span.start, span.stop):
            line = board.states[light].lines[number]
            laid(board, light, number, (np.where(here, -line.now, 0), np.where(here, -line.before, 0)), None, None, here)
    click(board, [Item(child, 1, (plus,), (den, den), sense=1, record=1), Item(child, 1, (minus,), (den, den), sense=-1, record=0)])
    return child


def rows_at(board: Lattice, child: int) -> dict[str, Any]:
    sign = next(i for i, f in enumerate(board.families) if f.held and f.wronskian)
    width = board.families[sign].width
    found = {}
    for record in range(2):
        row = registry.row_of(board.families, board.states, child, record)
        found[record] = np.asarray(board.states[sign].lines[row * width].now, dtype=object)
    return found


def run(intervals: int, den: int, out: Any, folder: Path) -> dict[str, Any]:
    began = time.perf_counter()
    plus, minus_link, minus_node = (1, 1, 1), (2, 1, 1), (1, 1, 1)
    summary: dict[str, Any] = {"den": den, "intervals": intervals}
    for form, minus in (("node", minus_node), ("link", minus_link)):
        for self_read in (False, True):
            records.row_levels = row_levels_unskipped if self_read else REAL_ROW_LEVELS
            node.row_levels = row_levels_unskipped if self_read else REAL_ROW_LEVELS
            lines: list[dict[str, Any]] = []
            board = board_of(folder / f"{form}_{int(self_read)}", den, lines)
            child = born(board, plus, minus)
            own_fraction, read_with, read_without, spread = [], [], [], []
            for _ in range(intervals):
                board.step()
                rows = rows_at(board, child)
                own, other = int(rows[1][plus]), int(rows[0][plus])
                own_fraction.append((abs(own), abs(own) + abs(other)))  # the pair, no float: own over own plus other
                read_with.append(other)
                read_without.append(own + other)
                share = np.asarray(board.share_of(child)[0], dtype=object)
                plus_share = records.wronskian(board.lines_of(child, 1), True)
                total = int(np.abs(np.asarray(plus_share, dtype=object)).sum())
                spread.append((abs(int(np.asarray(plus_share, dtype=object)[plus])), total))  # the pair, no float
                out.write(json.dumps({"form": form, "self_read": self_read, "interval": board.interval, "own": own, "other": other, "own_over_sum": list(own_fraction[-1]), "own_per_mille": per_mille(*own_fraction[-1]), "read_with_exclusion": other, "read_without": own + other, "plus_charge_at_birth_node_over_total": list(spread[-1]), "plus_charge_per_mille": per_mille(*spread[-1]), "minus_row_at_minus_node": int(rows[0][minus]), "plus_row_at_minus_node": int(rows[1][minus]), "turned": int(np.asarray(board.turned).sum())}) + "\n")
            key = f"{form}_{'self_read' if self_read else 'excluded'}"
            summary[key] = {
                "own_over_sum_last": list(own_fraction[-1]),
                "own_per_mille_last": per_mille(*own_fraction[-1]),
                "own_per_mille_max": max(per_mille(a, b) for a, b in own_fraction),
                "own_per_mille_span_sum": [sum(a for a, _b in own_fraction), sum(b for _a, b in own_fraction)],
                "read_with_exclusion_last": read_with[-1],
                "read_without_last": read_without[-1],
                "plus_charge_at_birth_node_over_total_last": list(spread[-1]),
                "plus_charge_per_mille_last": per_mille(*spread[-1]),
                "plus_charge_per_mille_min": min(per_mille(a, b) for a, b in spread),
            }
    records.row_levels = REAL_ROW_LEVELS
    node.row_levels = REAL_ROW_LEVELS
    summary["milliseconds"] = int((time.perf_counter() - began) * 1000)  # the host's timer, an integer reading
    out.write(json.dumps(summary) + "\n")
    return summary


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--intervals", type=int, default=24)
    parser.add_argument("--den", type=int, default=SMALL["integers"]["den"])
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--folder", type=Path, default=Path("/dev/shm/tmp/q2_self_read"))
    args = parser.parse_args(argv)
    with (args.out.open("w", encoding="utf-8") if args.out else sys.stdout) as out:
        summary = run(args.intervals, args.den, out, args.folder)
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
