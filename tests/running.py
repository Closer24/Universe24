"""The shared helpers that run or inspect a simulation in the tests: one copy each, imported by every test that needs them."""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.rule3 import coefficients
from event_universe.events.detector_law import DetectorLawSimulation, LiveRecord
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.worlds import ROOT, load_file

sys.path.insert(0, str(ROOT / "tools"))

from run_inputs import main as run_main  # noqa: E402

Seen = dict[int, tuple[int, list[int], list[int], int, int, int, int]]


FOLDER = ROOT / "examples" / "events" / "toward_nature"


def exchange_of(
    simulation: DetectorLawSimulation,
    family: int,
    now: np.ndarray,
    before: np.ndarray,
    old: np.ndarray,
    new: np.ndarray,
) -> Fraction:
    """The change of the form I of `form_I` when the family of clicks' levels move from `old` to `new`
    (ALGEBRA.md 9.45 (5), 9.57 (1))."""
    gamma = simulation.node_clock
    num = simulation.kind_num[family].astype(object)
    den = simulation.kind_den[family].astype(object)
    (read_old, _, _), self_old, wall = coefficients(num, den, gamma, old.astype(object))
    (read_new, _, _), self_new, _wall = coefficients(num, den, gamma, new.astype(object))
    a, b = now.astype(object), before.astype(object)
    total = Fraction(0)
    for node in zip(*np.nonzero(a | b), strict=True):
        squares = int(a[node]) ** 2 + int(b[node]) ** 2
        product = int(a[node]) * int(b[node])
        total += Fraction(
            int(wall[node]) * squares - int(self_new[node]) * product, 3 * int(read_new[node])
        )
        total -= Fraction(
            int(wall[node]) * squares - int(self_old[node]) * product, 3 * int(read_old[node])
        )
    return total


def form_I(
    simulation: DetectorLawSimulation,
    family: int,
    now: np.ndarray,
    before: np.ndarray,
    content: np.ndarray | None = None,
) -> Fraction:
    # the form from the rule's own integers (ALGEBRA.md 9.57 (1))
    # at the scale of the plain form (the engine's rational over 3 L): with (R_i, S_i, w_i) the
    # weak-field rule's coefficients at the Node, [w_i (a^2 + b^2) - S_i a b] / (3 R_i) at the
    # Nodes and 1 / 3 on every Link, plain (den / num, 0 and 1 / 3 in the vacuum, where R = 2
    # Gamma^2 num, S = 0, w = 6 den Gamma^2)
    gamma = simulation.node_clock
    if content is None:
        content = simulation.level_of("content")
    num = simulation.kind_num[family].astype(object)
    den = simulation.kind_den[family].astype(object)
    (read_coefficient, _, _), self_coefficient, wall = coefficients(
        num, den, gamma, content.astype(object)
    )
    read = reads_of(simulation, family)(before).astype(object)
    now_o, before_o = now.astype(object), before.astype(object)
    total = Fraction(0)
    for node in zip(*np.nonzero(now_o | before_o | read), strict=True):
        a, b = int(now_o[node]), int(before_o[node])
        total += Fraction(
            int(wall[node]) * (a * a + b * b) - int(self_coefficient[node]) * a * b,
            3 * int(read_coefficient[node]),
        )
        total -= Fraction(1, 3) * a * int(read[node])
    return total


def reads_of(simulation: DetectorLawSimulation, family: int):
    """The read matrix as a function: the six reads' sum of an array (the family's faces)."""
    return lambda a: simulation._neighbours(a, simulation.kind_wrap[family])


def chosen_by_the_rule(
    simulation: DetectorLawSimulation,
    total: int,
    increments: list[int],
    ladder: list[int],
    u: int,
    norm: int,
    wheel: int,
    pace: int,
) -> str:
    """The increment ladder of ALGEBRA.md 9.25 (2) on the click's own numbers: the first detector k
    at which 2 W p (C + f_1 + ... + f_k) >= (2 u + 1) T."""
    threshold = (2 * u + 1) * norm
    running = 2 * wheel * pace * total
    assert running < threshold
    for detector in ladder:
        running += 2 * wheel * pace * increments[detector]
        if running >= threshold:
            return simulation.detector_set[detector]
    raise AssertionError("no detector crossed")


def spy_on(simulation: DetectorLawSimulation, seen: Seen) -> None:
    original = simulation._ladder_click

    def spy(live, increments):
        total = live.total
        original(live, increments)
        if live.clicked and live.identity not in seen:
            seen[live.identity] = (
                total,
                list(increments),
                simulation._ladder_of(live),
                live.u,
                live.norm,
                live.wheel,
                live.pace,
            )

    simulation._ladder_click = spy  # type: ignore[method-assign]


def run(document: dict) -> tuple[list[dict], DetectorLawSimulation, list[dict]]:
    """The world stepped over its ticks, the books balanced at every interval; the lines,
    the simulation, and per interval the emitter body's own record before the interval's
    emission (its identity, residue, wheel and norm) and its count of intervals after it."""
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    block = simulation.block_by_number[0]
    trace: list[dict] = []
    for _ in range(document["ticks"]):
        before = (
            None
            if block.own is None
            else (block.own.identity, block.own.u, block.own.wheel, block.own.norm)
        )
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        trace.append(
            {
                "tick": simulation.tick,
                "excited_before": before,
                "excited_after": None if block.own is None else block.own.identity,
                "wait": block.wait,
            }
        )
    return lines, simulation, trace


def refused(document: dict, match: str) -> None:
    document["stamp"] = input_stamp(document)
    with pytest.raises(ValueError, match=match):
        parse_nature_beam_world(document)


def planted(simulation: DetectorLawSimulation, family: int, now, before, remainder) -> LiveRecord:
    """A record's rows given to the rule directly (no Ports: the flux reads the rows, not a take)."""
    return LiveRecord(
        1,
        0,
        family,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        now.astype(np.int64),
        before.astype(np.int64),
        remainder.astype(np.int64),
        pointers=[0] * len(simulation.detector_names),
        first_rung=[None] * len(simulation.detector_names),
        age=10,
    )


def run_world(document: dict, tmp_path: Path, start: dict | None = None) -> dict:
    """The one command on one world file, headless; the output file read back."""
    if start is not None:
        (tmp_path / "start.json").write_text(json.dumps(start) + "\n", encoding="utf-8")
        document["engine"] = str(tmp_path / "start.json")
        stamped(document)
    source = tmp_path / "world.json"
    source.write_text(json.dumps(document) + "\n", encoding="utf-8")
    assert run_main(["--out", str(tmp_path / "out"), "--jobs", "1", str(source)]) == 0
    return json.loads((tmp_path / "out" / "world.output.json").read_text(encoding="utf-8"))


def stamped(document: dict) -> dict:
    document["stamp"] = input_stamp(document)
    return document


def run_point_world(document: dict, ticks: int) -> tuple[DetectorLawSimulation, list[dict]]:
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    for _ in range(ticks):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    return simulation, lines


def document(name: str) -> dict:
    return json.loads((FOLDER / f"{name}.json").read_text(encoding="utf-8"))


def load_module(name: str):
    return load_file(f"toward_nature_{name}", FOLDER / f"{name}.py")


GENERATED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "artifacts",
    "build",
    "dist",
    "node_modules",
    "worktrees",  # agents' git worktrees under .claude/, checkouts and not repository content
}


def repository_files(root):
    """Visit source files once; generated output is not repository authority."""
    for directory, folders, files in os.walk(root):
        folders[:] = [
            name
            for name in folders
            if name not in GENERATED_DIRECTORIES and not name.endswith(".egg-info")
        ]
        for name in files:
            path = Path(directory) / name
            yield path
