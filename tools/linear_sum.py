"""The linear sum L of every line, a lattice reading labelled so and no measurement (ALGEBRA.md, the flux form of Rule3; `readings.linear_sum`, `readings.weighted_linear_sum`, `readings.linear_exchange`): a world is run over its intervals and per interval every family's lines report L = SUM_i [w (now_i - before_i) + r_i] with w = 6 den Gamma^2 G^2, the rate-weighted L'' = scale x SUM_i [w (now_i - before_i) + r_i] / p_i^2 with scale the least common multiple of the distinct p_i^2, L's change since the last interval and, for a family of light (num = den, not held, so its mass term is 0 at every content), the change the faces' exchange predicts, -SUM R_ij times the numbers beyond the faces with the step's own reads, zero on a closed board; a change beyond the prediction on such a line is a jump not accounted for by Rule3's line (a lay, a click's write, a face's value, the board's growth, a turned plane's phase term), named with its interval; the scale of L'' is per record's read. The readings' nanoseconds stand beside the share's and the momentum's (`Lattice.total_share`, `readings.momentum_of`).

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/linear_sum.py <world>.json [--intervals N] [--rows]
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import node
from event_universe.core import paces
from event_universe.lattice import Lattice
from event_universe.readings import linear_exchange, linear_sum, momentum_of, weighted_linear_sum
from event_universe.records import record_slice
from event_universe.world_files import load_world

LABEL = "LATTICE"


def walls(board: Lattice) -> list[tuple[int, bool]]:
    """Per family its wall w and whether it is a family of light, num = den, not held (D = 0 at every content)."""
    gamma, square = board.world.node_clock, board.unit * board.unit
    return [
        (
            6 * family.pair[1] * gamma * gamma * square,
            family.pair[0] == family.pair[1] and not family.held,
        )
        for family in board.families
    ]


def exchanges(board: Lattice) -> dict[str, list[int]]:
    """Per family of light, per line, the faces' exchange the next step gives L, with the step's own reads."""
    gamma, unit, found = board.world.node_clock, board.unit, {}
    for index, (_wall, light) in enumerate(walls(board)):
        if not light:
            continue
        family, values = board.families[index], []
        for record in range(family.records):
            content, factors = board.read(index, 1, record)
            reads = node.rule_of(family, gamma, content, factors, unit)[0]
            span = record_slice(family, record)
            values += [
                linear_exchange(reads, line, board.wrap) for line in board.states[index].lines[span]
            ]
        found[family.name] = values
    return found


def reading(board: Lattice) -> dict[str, list[int]]:
    """L per family and line as the board stands."""
    found = {}
    for index, (wall, _light) in enumerate(walls(board)):
        found[board.families[index].name] = [
            linear_sum(wall, line) for line in board.states[index].lines
        ]
    return found


def scale_of(values: set[int]) -> int:
    """The least common multiple of the distinct paces squared, by Euclid's remainders on whole numbers."""
    found = 1
    for value in sorted(values):
        a, b = found, value
        while b:
            a, b = b, a % b
        found = found * value // a
    return found


def weighted(board: Lattice) -> dict[str, list[int]]:
    """L'' per family and line as the board stands: each Node's pace squared from its record's read, the scale the
    least common multiple of the distinct squares on the board (`readings.weighted_linear_sum`)."""
    gamma, found = board.world.node_clock, {}
    for index, (wall, _light) in enumerate(walls(board)):
        family, values = board.families[index], []
        for record in range(family.records):
            content, _factors = board.read(index, 1, record)
            squared = np.asarray(paces.node_paces(gamma, content)[1], dtype=object) ** 2
            scale = scale_of({int(v) for v in np.asarray(squared).ravel()})
            weights = np.vectorize(lambda v, s=scale: s // int(v), otypes=[object])(squared)
            span = record_slice(family, record)
            values += [
                weighted_linear_sum(wall, line, weights) for line in board.states[index].lines[span]
            ]
        found[family.name] = values
    return found


def run(path: Path, intervals: int | None) -> dict[str, Any]:
    board = Lattice(load_world(path))
    intervals = intervals or board.world.intervals
    nanoseconds = {
        "linear sum and exchange": 0,
        "weighted linear sum": 0,
        "total share and momentum": 0,
        "step": 0,
    }
    rows, unaccounted = [], []
    last = reading(board)
    for _ in range(intervals):
        started = time.perf_counter_ns()
        expected = exchanges(board)
        nanoseconds["linear sum and exchange"] += time.perf_counter_ns() - started
        started = time.perf_counter_ns()
        board.step()
        nanoseconds["step"] += time.perf_counter_ns() - started
        if board.ended is not None:
            break
        started = time.perf_counter_ns()
        now = reading(board)
        nanoseconds["linear sum and exchange"] += time.perf_counter_ns() - started
        started = time.perf_counter_ns()
        rate_weighted = weighted(board)
        nanoseconds["weighted linear sum"] += time.perf_counter_ns() - started
        started = time.perf_counter_ns()
        for index in board.order:
            board.total_share(index)
            momentum_of(board.families[index].pair[0], board.record(index), board.wrap)
        nanoseconds["total share and momentum"] += time.perf_counter_ns() - started
        row: dict[str, Any] = {
            "interval": board.interval,
            "label": LABEL,
            "linear": now,
            "weighted": rate_weighted,
        }
        for name, values in now.items():
            changes = [after - before for after, before in zip(values, last[name], strict=True)]
            row.setdefault("change", {})[name] = changes
            if name in expected:
                row.setdefault("expected", {})[name] = expected[name]
                for number, (change, predicted) in enumerate(zip(changes, expected[name], strict=True)):
                    if change != predicted:
                        unaccounted.append(
                            dict(
                                interval=board.interval,
                                family=name,
                                line=number,
                                change=change,
                                expected=predicted,
                            )
                        )
        rows.append(row)
        last = now
    return {
        "label": LABEL,
        "world": path.name,
        "intervals": board.interval,
        "rows": rows,
        "unaccounted": unaccounted,
        "nanoseconds": nanoseconds,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("world", type=Path, help="the world file, its mode file beside it")
    parser.add_argument("--intervals", type=int, default=None, help="the intervals run (the world's)")
    parser.add_argument(
        "--rows", action="store_true", help="print every interval's row, not the last alone"
    )
    args = parser.parse_args(argv)
    found = run(args.world, args.intervals)
    if not args.rows:
        found["rows"] = found["rows"][-1:]
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()
