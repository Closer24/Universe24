"""Hand Y2's shared helpers (the metric's ten lines, U24_METRIC): the bare 3-cube of the tests' small universe (den 1,021) under the engine's own hole seed, the test module tests/test_the_board_is_the_cube_48.py imported by path for its group, and the carry of the metric's ten lines as one object under the 48 (the flux lines a vector with the axis's sign, the shears a T_2g triple with the product of two signs, every negated line's remainder complemented at its wall, the lay's gauge w/2 as the test's carry has it). Integers only."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path
from types import ModuleType

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, os.environ.get("Y2_SRC", str(ROOT / "src")))  # Y2_SRC: another checkout's src, for the bit-for-bit digest

from event_universe import records, registry, world_files  # noqa: E402
from event_universe.core.ports import AXES  # noqa: E402
from event_universe.core.rule3 import wall_of  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import SMALL  # noqa: E402

OUT = Path(__file__).resolve().parent
PAIRS = ((0, 1), (1, 2), (2, 0))  # the shear lines xy, yz, zx


def load_by_path(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CUBE48 = load_by_path("cube48_test", ROOT / "tests" / "test_the_board_is_the_cube_48.py")
NODE_INTEGERS = load_by_path("node_integers_tool", ROOT / "tools" / "node_integers.py")


def scratch(label: str) -> Path:
    base = Path(os.environ.get("TMPDIR", tempfile.gettempdir())) / "y2"
    base.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=label + "_", dir=base))


def bare_board(side: int = 3, intervals: int = 20, lines: list | None = None, shape: list | None = None) -> Lattice:
    """The tests' small universe on the bare cube of `side` (or `shape`) under the engine's own hole seed, the volume holder gapped (the engine's own pair)."""
    folder = scratch(f"den{SMALL['integers']['den']}_{side}")
    world_files.REPOSITORY_ROOT = folder
    (folder / "u.json").write_text(json.dumps(SMALL), encoding="utf-8")
    world = {"universe": "u.json", "shape": shape or [side] * 3, "intervals": intervals}
    (folder / "w.json").write_text(json.dumps(world), encoding="utf-8")
    return Lattice(load_world(folder / "w.json"), output=None if lines is None else lines.append)


def snapshot(board: Lattice) -> list:
    found = []
    for state in board.states:
        lines = [tuple(np.asarray(a, dtype=object).copy() for a in (li.now, li.before, li.remainder)) for li in state.lines]
        writes = [np.asarray(w, dtype=object).copy() for w in state.write_remainders]
        phases = [[tuple(np.asarray(a, dtype=object).copy() for a in (li.now, li.before, li.remainder)) for li in row] for row in state.phases]
        found.append((lines, writes, phases))
    return found


def same(a, b) -> bool:  # type: ignore[no-untyped-def]
    if isinstance(a, list | tuple):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b, strict=True))
    return bool(np.array_equal(np.asarray(a, dtype=object), np.asarray(b, dtype=object)))


def digest(board: Lattice) -> str:
    """Every array of every state as one text digest (the arrays' integers in order), for the bit-for-bit comparison across two checkouts."""
    import hashlib

    h = hashlib.sha256()
    for lines, writes, phases in snapshot(board):
        for parts in lines:
            for a in parts:
                h.update(repr(a.tolist()).encode())
        for w in writes:
            h.update(repr(w.tolist()).encode())
        for row in phases:
            for parts in row:
                for a in parts:
                    h.update(repr(a.tolist()).encode())
    return h.hexdigest()


def carried_ten(board: Lattice, m: np.ndarray, turns, control: str = "") -> list:  # type: ignore[no-untyped-def]
    """The test module's carry (`CUBE48.carried`) with the metric's ten lines carried as one object: the time line a scalar, the tensions permuted with no sign (the test's own), the flux lines permuted with the axis's sign s_a (the level negated and the remainder complemented about the lay's gauge, the write remainder alike) and the shears carried to the pair pi(a) pi(b) with the sign s_a s_b; `control` "flux" or "shear" carries that triple with no sign (the negative control)."""
    found = CUBE48.carried(board, m, turns)
    pi, s = CUBE48.axis_map(m)
    volume = next(i for i, f in enumerate(board.families) if f.held and not f.wronskian)
    family, state = board.families[volume], board.states[volume]
    if family.width - 1 < AXES * AXES:
        return found
    lines, writes, phases = found[volume]
    wall = wall_of(family.pair[1], board.world.node_clock, board.unit)
    divided = records.divided_walls(family, board.fixed_walls[volume], board.world.node_clock)
    shape, side = board.shape, board.shape[0]
    nodes = np.array(list(np.ndindex(*shape)))
    images = np.mod(nodes @ m.T, side)

    def moved(array):  # type: ignore[no-untyped-def]
        a = np.asarray(array, dtype=object)
        out = np.empty_like(a)
        out[tuple(images.T)] = a[tuple(nodes.T)]
        return out

    odd = turns[volume][0] if turns else np.zeros(shape, dtype=bool)

    def complemented(remainder, w):  # type: ignore[no-untyped-def]
        # the test's gauge (tests/test_the_board_is_the_cube_48.py): the lay at the half wall, the reflection (w - r) mod w where the row's count of the Node's turns is even and (w - 2 - r) mod w where odd, the swap's conjugate of the lay's gauge
        r, w = np.asarray(remainder, dtype=object), np.asarray(w, dtype=object)
        return np.asarray(np.mod(w - 2 * np.asarray(odd, dtype=object) - r, w), dtype=object)

    time = state.lines[0]
    volume_wall = wall * (np.asarray(time.now, dtype=object) + np.asarray(time.before, dtype=object))
    # the flux lines, positions 1 + AXES + a
    for a in range(AXES):
        k, target = 1 + AXES + a, 1 + AXES + pi[a]
        now, before, remainder = (moved(v) for v in (state.lines[k].now, state.lines[k].before, state.lines[k].remainder))
        write = moved(state.write_remainders[k])
        if s[a] < 0 and control != "flux":
            now, before = -now, -before
            remainder = moved(complemented(state.lines[k].remainder, volume_wall))
            write = moved(complemented(state.write_remainders[k], divided[k]))
        lines[target], writes[target] = (now, before, remainder), write
    # the shears, positions 1 + 2 AXES + p, the pair (a, b) carried to {pi(a), pi(b)}
    index_of = {frozenset(p): n for n, p in enumerate(PAIRS)}
    for n, (a, b) in enumerate(PAIRS):
        k, target = 1 + 2 * AXES + n, 1 + 2 * AXES + index_of[frozenset((pi[a], pi[b]))]
        now, before, remainder = (moved(v) for v in (state.lines[k].now, state.lines[k].before, state.lines[k].remainder))
        write = moved(state.write_remainders[k])
        if s[a] * s[b] < 0 and control != "shear":
            now, before = -now, -before
            remainder = moved(complemented(state.lines[k].remainder, volume_wall))
            write = moved(complemented(state.write_remainders[k], divided[k]))
        lines[target], writes[target] = (now, before, remainder), write
    found[volume] = (lines, writes, phases)
    return found


def write(name: str, text: str) -> None:
    (OUT / name).write_text(text, encoding="utf-8")
    print(text)


def rows_table(board: Lattice) -> list:
    found = []
    for index, family in enumerate(board.families):
        state = board.states[index]
        found.append(
            {
                "index": index,
                "name": family.name,
                "pair": list(family.pair),
                "held": family.held,
                "flux": family.flux,
                "width": family.width,
                "records_live": registry.records_of(family, state.lines),
                "lines_live": len(state.lines),
                "write_remainders": len(state.write_remainders),
                "walls": [int(w) for w in board.writes[index].walls] if family.held else [],
            }
        )
    return found
