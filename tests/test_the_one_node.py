"""The one Node (the owner's law of 2026-10-22 and his final check of 2026-10-23: every Node acts alone, on its neighbours, receiving nothing from an external file): once a world is loaded, the engine's step reads nothing outside the Nodes' own records and their six Links, no file, no key of the universe or the world, no board-wide number; the board part of the law stands in tests/test_the_acts_table.py (every division of src with its kind) and in ALGEBRA.md, Only local (the owner's locality decision of 2026-10-22). Two tests: the step with the file system and the loader's readers made unreachable and the board's readings made to raise, bit for bit the ordinary step; and the static check over src/event_universe that no module outside the loader reads a file and that the step's line (core/rule3.py, flux.py, the write's division) takes no reduction over the board."""

import ast
import builtins
import json
import pathlib
from pathlib import Path

import numpy as np
import pytest

from event_universe import board_readings, world_files
from event_universe.lattice import Lattice
from event_universe.loader import universe as loader_universe
from event_universe.loader import world as loader_world

SRC = Path(__file__).resolve().parents[1] / "src" / "event_universe"
WORLD = Path(
    "examples/events/bell/bell_a_b.json"
)  # a shipped world with a holder of the content, a sign holder, receding faces and a click
INTERVALS = 30
READERS = (
    "open",
    "load",
    "loads",
    "read_text",
    "read_bytes",
)  # a file's readers, allowed in the loader alone
REDUCTIONS = ("sum", "mean", "max", "min", "any", "all", "dot")  # a board-wide number
LINE = (
    "core/rule3.py",
    "flux.py",
    "features/write/__init__.py",
)  # the step's line, every act one Node's


def unreachable(what: str):  # type: ignore[no-untyped-def]
    def raiser(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError(
            f"the step read {what} after the load: the one Node receives nothing from outside"
        )

    return raiser


def frozen(board: Lattice) -> list[tuple[str, ...]]:
    """Every array of every family's NodeState as Python's integers, the comparison bit for bit."""
    found = []
    for state in board.states:
        for line in state.lines:
            found.append(
                tuple(
                    np.asarray(a, dtype=object).tolist() for a in (line.now, line.before, line.remainder)
                )
            )
        found.append(tuple(np.asarray(a, dtype=object).tolist() for a in state.write_remainders))
    return found


def test_the_step_reads_nothing_outside_the_nodes_after_the_load(monkeypatch):  # type: ignore[no-untyped-def]
    """A shipped world loaded once; the ordinary step and the step with every reader of a file, the loader's two readers and the board's readings made to raise agree bit for bit over thirty intervals, the output lines included (the clicks' acts from outside the Node, the owner's decision of 2026-10-20, read the board as the law says and the lattice's own arrays, no file)."""
    world = world_files.load_world(WORLD)
    plain, lines = [], []
    board = Lattice(world, plain.append)
    for _ in range(INTERVALS):
        board.step()
    other = Lattice(world, lines.append)  # the same loaded world, nothing read again
    monkeypatch.setattr(builtins, "open", unreachable("a file by open"))
    monkeypatch.setattr(pathlib.Path, "read_text", unreachable("a file by read_text"))
    monkeypatch.setattr(pathlib.Path, "read_bytes", unreachable("a file by read_bytes"))
    monkeypatch.setattr(json, "load", unreachable("a JSON file"))
    monkeypatch.setattr(json, "loads", unreachable("a JSON text"))
    monkeypatch.setattr(world_files, "load_world", unreachable("the world's files"))
    monkeypatch.setattr(loader_world, "parse_world", unreachable("the world's keys"))
    monkeypatch.setattr(loader_universe, "universe_of", unreachable("the universe's keys"))
    monkeypatch.setattr(board_readings, "uniform_mode", unreachable("the board's mean, a reading"))
    monkeypatch.setattr(board_readings, "eras", unreachable("the board's eras, a reading"))
    for _ in range(INTERVALS):
        other.step()
    assert other.interval == board.interval == INTERVALS
    assert frozen(other) == frozen(board)
    assert lines == plain and lines  # the output lines the same, the board's own readings among them


def calls(tree: ast.AST) -> list[tuple[str, int, bool]]:
    """Every call's name (an attribute's last word or a bare name), its line and whether it is an attribute's (an array's method or numpy's function, which reduces over the whole array; a bare name is Python's own `sum` over a Node's few terms, the six Links' reaches or the three lines' Link terms at one Node)."""
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            target = node.func
            attribute = isinstance(target, ast.Attribute)
            name = target.attr if attribute else target.id if isinstance(target, ast.Name) else ""
            found.append((name, node.lineno, attribute))
    return found


def test_every_act_of_the_step_reads_the_nodes_record_and_its_links_alone():  # type: ignore[no-untyped-def]
    """The static check: no module of src/event_universe outside loader/ and world_files.py calls a reader of a file (`open`, `json.load`, `json.loads`, `read_text`, `read_bytes`), so every number the step takes was read at the load; and the step's line, core/rule3.py (the division act), flux.py (the Links' sum gathered Link by Link, each Link's one difference) and the write's division, calls no reduction over an array (an array's `sum`, `mean`, `max`, `min`, `any`, `all`, `dot` or numpy's; Python's own `sum` over the six Links' reaches of one Node and over the three lines' Link terms at one Node is a Node's own arithmetic): every act's inputs at a Node are the Node's record and its Ports' reads (tests/test_the_acts_table.py lists every division of src with its kind; ALGEBRA.md, Only local)."""
    readers, reductions = [], []
    for path in sorted(SRC.rglob("*.py")):
        relative = path.relative_to(SRC).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"))
        if not relative.startswith("loader/") and relative != "world_files.py":
            readers += [(relative, name, line) for name, line, _ in calls(tree) if name in READERS]
        if relative in LINE:
            reductions += [
                (relative, name, line)
                for name, line, attribute in calls(tree)
                if attribute and name in REDUCTIONS
            ]
    assert readers == [], f"a module outside the loader reads a file: {readers}"
    assert reductions == [], f"the step's line takes a board-wide number: {reductions}"


if __name__ == "__main__":
    pytest.main([__file__])
