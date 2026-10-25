"""The integers one Node holds, a host tool and a reading of the lattice's arrays (ENGINE.md section 2, the NodeState; the owner's principle of 2026-10-25 that a Node always holds the same count of integers, always does the same acts, every integer within a fixed width): the world is loaded as tools/run_inputs.py loads it and stepped by the engine's own step, and at the start and after every interval at which the count or the largest bit length changes (and every `--every` K) one JSON line is printed with, per family, its lines, its write remainders, its phase lines and the integers they make at one Node (one per level now, one per level before and one per remainder of every line, `len(fields(Record))`, one per write remainder), the total, the board's shape, whether every array of every state is one array over the lattice of that shape (so the same count at every Node, stated by construction and read from the shapes), the largest bit length of any element of any state array with the array that holds it, the loader's derived width in bits and the host's integer bits; a last line the summary (the distinct counts the run held with the interval each was first read at, whether one count stood throughout, the largest bit length over the run with its array and interval, and with `--bits` B the verdict whether every integer stood within B: the width the principle names is the caller's and no number of this tool). The tool reads the board and sums over it (a reading, no act) and computes nothing of the law; the test tests/test_the_node_holds_the_same_count_of_integers.py reads the board through this tool's functions by its path.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/node_integers.py <world>.json [--intervals N] [--every K] [--bits B] [--out <file>.jsonl]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import fields
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.lattice import Lattice
from event_universe.records import Record
from event_universe.world_files import load_world

LEVELS = len(
    fields(Record)
)  # the integers one line holds at a Node: the level now, the level before, the remainder


def arrays_of(board: Lattice) -> list[tuple[str, Any]]:
    """Every array of every family's NodeState with its label: per line its levels and its remainder, per held line its write remainder, per phase line its levels and its remainder (records.NodeState); each one integer per Node."""
    found: list[tuple[str, Any]] = []
    for family, state in zip(board.families, board.states, strict=True):
        for number, line in enumerate(state.lines):
            for name in (field.name for field in fields(Record)):
                found.append((f"{family.name} line {number} {name}", getattr(line, name)))
        for number, remainder in enumerate(state.write_remainders):
            found.append((f"{family.name} write {number}", remainder))
        for row, lines in enumerate(state.phases):
            for number, line in enumerate(lines):
                for name in (field.name for field in fields(Record)):
                    found.append((f"{family.name} row {row} phase {number} {name}", getattr(line, name)))
    return found


def integers_of(board: Lattice) -> dict[str, dict[str, int]]:
    """Per family its lines, its write remainders, its phase lines and the integers they make at one Node: three per line, one per write remainder, three per phase line."""
    found = {}
    for family, state in zip(board.families, board.states, strict=True):
        lines, writes = len(state.lines), len(state.write_remainders)
        phase_lines = sum(len(row) for row in state.phases)
        found[family.name] = {
            "lines": lines,
            "write_remainders": writes,
            "phase_lines": phase_lines,
            "integers": LEVELS * lines + writes + LEVELS * phase_lines,
        }
    return found


def total_of(board: Lattice) -> int:
    """The integers one Node holds in all, the arrays' count."""
    return len(arrays_of(board))


def same_shape(board: Lattice) -> bool:
    """Whether every array of every state is one array over the lattice of the board's shape, so that every Node holds the same count (the count at a Node is the arrays' count and no Node differs)."""
    return all(np.asarray(array).shape == tuple(board.shape) for _label, array in arrays_of(board))


def largest_bits(board: Lattice) -> tuple[int, str]:
    """The largest bit length of any element of any state array, the sign aside, with the label of the array that holds it; (0, "") on a board with no array."""
    found: tuple[int, str] = (0, "")
    for label, array in arrays_of(board):
        flat = np.asarray(array, dtype=object).reshape(-1).tolist()
        bits = max((abs(int(x)).bit_length() for x in flat), default=0)
        if bits > found[0]:
            found = (bits, label)
    return found


def line_of(board: Lattice) -> dict[str, Any]:
    """The reading at the board's interval as one line: the interval, the integers one Node holds, per family its counts, the board's shape, whether every array is of that shape, the largest bit length with its array, the loader's derived width in bits, the host's integer bits and the arrays' kind."""
    bits, label = largest_bits(board)
    return {
        "interval": board.interval,
        "integers": total_of(board),
        "per_family": integers_of(board),
        "shape": list(board.shape),
        "same_at_every_node": same_shape(board),
        "largest_bit_length": bits,
        "largest_at": label,
        "width_bits": board.world.width.bit_length(),
        "host_bits": MAX_WORK_INT.bit_length(),
        "kind": board.kind.__name__,
    }


def run(
    path: Path, intervals: int | None, every: int | None, bits: int | None, out: Any
) -> dict[str, Any]:
    """The world loaded and stepped `intervals` intervals (the world's own where None), the reading written to `out` as one JSON line at the start and after every interval at which the count or the largest bit length changed (and every `every` intervals where given); the summary returned: the distinct counts with the interval each was first read at, whether one count stood throughout, the largest bit length over the run with its array and interval, the seconds, and with `bits` whether every integer stood within that width."""
    began = time.perf_counter()
    board = Lattice(load_world(path))
    counts: dict[int, int] = {}
    largest: tuple[int, str, int] = (0, "", 0)
    held: tuple[int, int] | None = None

    def read() -> None:
        nonlocal largest, held
        line = line_of(board)
        line["seconds"] = round(time.perf_counter() - began, 3)
        counts.setdefault(line["integers"], board.interval)
        if line["largest_bit_length"] > largest[0]:
            largest = (line["largest_bit_length"], line["largest_at"], board.interval)
        changed = held != (line["integers"], line["largest_bit_length"])
        held = (line["integers"], line["largest_bit_length"])
        if changed or (every is not None and board.interval % every == 0):
            out.write(json.dumps(line) + "\n")

    read()
    for _ in range(board.world.intervals if intervals is None else intervals):
        board.step()
        read()
    summary: dict[str, Any] = {
        "world": path.name,
        "intervals": board.interval,
        "shape": list(board.shape),
        "width_bits": board.world.width.bit_length(),
        "host_bits": MAX_WORK_INT.bit_length(),
        "counts": {str(count): first for count, first in sorted(counts.items())},
        "same_count_throughout": len(counts) == 1,
        "largest_bit_length": largest[0],
        "largest_at": largest[1],
        "largest_interval": largest[2],
        "seconds": round(time.perf_counter() - began, 3),
    }
    if bits is not None:
        summary.update(bits=bits, within=largest[0] <= bits)
    return summary


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("world", type=Path, help="the world file, its universe file beside it")
    parser.add_argument(
        "--intervals", type=int, default=None, help="the intervals to step (the world's own)"
    )
    parser.add_argument(
        "--every",
        type=int,
        default=None,
        help="a line every so many intervals beside the lines at a change of the count or the bit length",
    )
    parser.add_argument(
        "--bits",
        type=int,
        default=None,
        help="the width the principle names: the verdict within it or beyond",
    )
    parser.add_argument("--out", type=Path, default=None, help="the lines' file (the standard output)")
    args = parser.parse_args(argv)
    if args.every is not None and args.every < 1:
        raise ValueError(f"--every takes an integer from 1, got {args.every}")
    if args.out is None:
        summary = run(args.world, args.intervals, args.every, args.bits, sys.stdout)
        print(json.dumps(summary))
        return
    with args.out.open("w", encoding="utf-8") as out:
        summary = run(args.world, args.intervals, args.every, args.bits, out)
        out.write(json.dumps(summary) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
