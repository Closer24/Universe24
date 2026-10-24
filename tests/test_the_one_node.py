"""The one Node (the owner's law of 2026-10-22 and his final check of 2026-10-23: every Node acts alone, on its neighbours, receiving nothing from an external file): once a world is loaded, the engine's step reads nothing outside the Nodes' own records and their six Links, no file, no key of the universe or the world, no board-wide number (ALGEBRA.md, Only local, the owner's locality decision of 2026-10-22). Two tests: the step with the file system and the loader's readers made unreachable and the board's readings made to raise, bit for bit the ordinary step; and the loader's vocabulary, the world's three keys and the universe's three integers and no declaration (the static scans of src/, the former keys' refusals, the step list and the shipped files' keys struck 2026-10-24 with the tests' audit: their claims the two tiles', the loader's and the one world's tests')."""

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
CUBE = 3  # the bare 3-cube torus of the tests' small universe: the births and their clicks from the hole seed's first intervals
INTERVALS = 30


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


def test_the_step_reads_nothing_outside_the_nodes_after_the_load(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The one world's universe on the bare 3-cube torus, loaded once; the ordinary step and the step with every reader of a file, the loader's two readers and the board's readings made to raise agree bit for bit over thirty intervals, the output lines included (the clicks' acts from outside the Node, the owner's decision of 2026-10-20, read the board as the law says and the lattice's own arrays, no file)."""
    from tests.laws_universe import small_universe

    small_universe(
        tmp_path
    )  # the tests' small universe (2026-10-24): the one world's 26 points at the enlarged den step at 0.5 s per interval on the 3-cube
    bare = {"shape": [CUBE] * 3, "intervals": INTERVALS, "universe": str(tmp_path / "u.json")}
    (tmp_path / "bare.json").write_text(json.dumps(bare), encoding="utf-8")
    world = world_files.load_world(tmp_path / "bare.json")
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


RETIRED = (
    "act",
    "booking",
    "factor",
    "pressure",
    "uniform",
    "erasure",
    "reach",
    "meeting",
    "dipole",
    "converts",
    "shear",
    "lorentz",
)  # the former act keys and their words, no module of the loader or the generator names one


def test_the_loaders_vocabulary_holds_content_keys_alone():  # type: ignore[no-untyped-def]
    """The loader's key lists, enumerated, hold content keys alone (the owner's rule of 2026-10-23: no more keys in the code, one single Node in the whole universe; his word of 2026-10-24: no declarations, a row its name, its pair and its dimension, the keys `held` and `reads` gone from the tables and refused by name, `GONE`): a file naming a former act key meets the loader's ordinary refusal of an unknown key, the same as any misspelling; and no module under src/event_universe/loader or the generator tools/pixel_mode.py names a retired key or its words in its code (an ast check over the string constants outside the docstrings, as tests/test_the_acts_table.py walks the divisions)."""
    from event_universe.loader import universe
    from event_universe.loader import world as loader_world

    assert set(loader_world.WORLD_KEYS) == {"shape", "intervals", "universe"}
    assert (
        set(universe.INTEGER_KEYS)
        == {
            "den",
            "node_clock",
            "quantum_action",
        }
    )  # no family row; the width derived and the Link unit the engine's (2026-10-24, `GONE_INTEGERS`): `families` with `name`, `pair` and `dimension` gone 2026-10-24, `held` and `reads` before them
    assert set(universe.GONE) == {"families"}
    with pytest.raises(ValueError, match="holds the key 'families', a declaration no file carries"):
        universe.universe_of(
            {
                "integers": {"den": 6000, "node_clock": 6000, "quantum_action": 32768},
                "families": [{"name": "g", "pair": [5999, 6000], "act": "pace"}],
            }
        )
    named = []
    for path in sorted(SRC.joinpath("loader").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        docs = {
            n.value.lineno
            for n in ast.walk(tree)
            if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)
        }
        named += [
            (path.name, n.value, n.lineno)
            for n in ast.walk(tree)
            if isinstance(n, ast.Constant)
            and isinstance(n.value, str)
            and n.value in RETIRED
            and n.lineno not in docs
        ]
    assert named == [], f"a module of the loader names a retired key: {named}"
