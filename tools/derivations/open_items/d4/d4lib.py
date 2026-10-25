"""Hand d4 (2026-10-25): the decoder receives the clicks as they are. Shared helpers: the hole seed on the bare 3-cube of the tests' small universe (den 1,021), run with the output writer on or off; the board's whole state as Python integers for a bit-for-bit comparison; integer readings only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))  # tests.laws_universe
from event_universe import world_files  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import bare_torus  # noqa: E402


def hole_board(folder: Path, intervals: int, writer_on: bool, cube: int = 3) -> tuple[Lattice, list]:
    """The hole seed (the loader's own: light at one quantum on every Node but the origin) on the bare torus at den 1,021; `writer_on` gives the board an output (every line kept) else None."""
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    lines: list = []
    board = Lattice(load_world(bare_torus(folder, cube, intervals)), output=lines.append if writer_on else None)
    return board, lines


def ints(array) -> list:
    return [int(x) for x in np.asarray(array, dtype=object).reshape(-1)]


def state_of(board: Lattice) -> dict[str, list]:
    """Every integer the board holds, keyed: each family's lines (now, before, remainder), write remainders, phase lines, the counters (proper_count, closes, standing, crossed, beats) and the interval."""
    found: dict[str, list] = {}
    for k, st in enumerate(board.states):
        for n, line in enumerate(st.lines):
            found[f"f{k}.line{n}.now"] = ints(line.now)
            found[f"f{k}.line{n}.before"] = ints(line.before)
            found[f"f{k}.line{n}.remainder"] = ints(line.remainder)
        for n, r in enumerate(st.write_remainders):
            found[f"f{k}.write{n}"] = ints(r)
        for row, phase_row in enumerate(getattr(st, "phases", []) or []):
            for n, ph in enumerate(phase_row):
                found[f"f{k}.phase{row}.{n}.now"] = ints(ph.now)
                found[f"f{k}.phase{row}.{n}.before"] = ints(ph.before)
                found[f"f{k}.phase{row}.{n}.remainder"] = ints(ph.remainder)
    found["proper_count"] = ints(board.proper_count)
    found["closes"] = ints(board.closes)
    for name in ("standing", "crossed", "beats"):
        for key, arr in sorted(getattr(board, name).items()):
            found[f"{name}{list(key)}"] = ints(arr)
    found["interval"] = [int(board.interval)]
    return found


def compare(a: dict[str, list], b: dict[str, list]) -> tuple[int, int, list[str]]:
    """(arrays compared, arrays equal, the names of the unequal ones)."""
    names = sorted(set(a) | set(b))
    unequal = [n for n in names if a.get(n) != b.get(n)]
    return len(names), len(names) - len(unequal), unequal


def dump(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=1, default=str) + "\n", encoding="utf-8")
