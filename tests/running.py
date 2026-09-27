"""The shared helpers that run or inspect a simulation in the tests: one copy each, imported by every test that needs them."""

from __future__ import annotations

import ast
import json
import os
import random
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe.core.rule3 import coefficients
from event_universe.events.detector_law import DetectorLawSimulation, LiveRecord
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.worlds import ROOT, emitter_world, load_file

sys.path.insert(0, str(ROOT / "tools"))

from run_inputs import main as run_main  # noqa: E402

UNIVERSE = ROOT / "examples" / "events" / "universe.json"

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


SEEDS = tuple(range(24))


INTERVALS = 20


WORDS = (
    "amber",
    "basalt",
    "cedar",
    "delta",
    "ember",
    "fjord",
    "garnet",
    "harbor",
    "indigo",
    "jasper",
    "kelp",
    "lumen",
    "marble",
    "nectar",
    "onyx",
    "pebble",
    "quartz",
    "raven",
    "saffron",
    "tundra",
    "umber",
    "velvet",
    "willow",
    "xenon",
    "yarrow",
    "zephyr",
    "anvil",
    "birch",
    "cobalt",
    "dune",
    "echo",
    "flint",
    "gravel",
    "heron",
    "iris",
    "juniper",
    "kestrel",
    "lichen",
    "meadow",
    "nickel",
    "orchid",
    "prism",
    "quill",
    "ripple",
    "sable",
    "thistle",
    "upland",
    "vortex",
    "walnut",
    "yucca",
)


PAIRS = ([1, 1], [700, 703], [800, 809], [1000, 1019], [500, 501], [1000, 1181])


PARTS = ([1], [1, 3], [1, 3, 6])


def draw(seed: int) -> dict[str, Any]:
    """One draw: the families (the body's, the given, up to two holders, the rest clicking
    families of random shape) with random names, and the roles by name."""
    rng = random.Random(seed)
    count = rng.randint(1, 20)
    names = rng.sample(WORDS, count)
    roles: dict[str, str] = {}
    families: list[dict[str, Any]] = []
    body = names[0]
    roles["body"] = body
    given = names[1] if count >= 2 else None
    if given:
        roles["given"] = given
    holders: list[str] = []
    rest = names[2:] if given else names[1:]
    content_holder = rest[0] if rest and rng.random() < 0.8 else None
    if content_holder:
        rest = rest[1:]
        holders.append(content_holder)
    sign_holder = None
    if given and rng.random() < 0.5:
        sign_holder = given  # the given family holds the sign, as the shipped charge does
    elif rest and rng.random() < 0.5:
        sign_holder = rest[0]
        rest = rest[1:]
    if sign_holder:
        holders.append(sign_holder)

    def reads_of(exclude: str | None = None) -> list[dict[str, Any]]:
        chosen = [h for h in holders if h != exclude and rng.random() < 0.6]
        return [
            {
                "family": h,
                "weight": rng.choice([1, 2, 3, "Lambda"]),
                "twist": rng.choice(["own", "own", rng.randint(0, 200)]),
                "by": rng.choice([1, "q"]),
            }
            for h in chosen
        ]

    def held(count_word: str, parts: list[int]) -> dict[str, Any]:
        entry: dict[str, Any] = {
            "count": count_word,
            "factors": [rng.randint(1, 4) for _ in parts],
            "dipole": "spin" if count_word == "content" else "moment",
        }
        # the divisor is written on every entry (no default in the loader); the draw of the
        # random one keeps the stream of the seeds as it was
        entry["dipole_div"] = rng.randint(1, 3) if rng.random() < 0.5 else 1
        return entry

    def clicks() -> dict[str, Any]:
        return {"gives": True, "takes": True, "quantum": rng.randint(1, 4)}

    if content_holder:
        parts = rng.choice(([1, 3], [1, 3, 6]))
        families.append(
            {
                "name": content_holder,
                "parts": parts,
                "phase": 1,
                "pair": [1, 1],
                "held": held("content", parts),
                "spins_step": {"curl": [1, 4], "tidal": [3, 4]},
                "reads": [],
                "self_source": {"unit": 0},
            }
        )
    if sign_holder and sign_holder != given:
        parts = rng.choice(([1, 3], [1, 3, 6]))
        entry = {
            "name": sign_holder,
            "parts": parts,
            "phase": rng.choice([1, 2]),
            "pair": [1, 1],
            "held": held("sign", parts),
            "reads": reads_of(exclude=sign_holder),
            "self_source": {"unit": 0},
        }
        if entry["reads"] or rng.random() < 0.5:
            # a held family that reads has waves (the loader's rule, ALGEBRA.md 9.45 (2))
            entry["clicks"] = {"gives": True, "takes": True, "quantum": 1}
        families.append(entry)
    if given:
        parts = rng.choice(([1, 3], [1, 3, 6])) if sign_holder == given else rng.choice(PARTS)
        entry = {
            "name": given,
            "parts": parts,
            "phase": 2,
            "pair": [1, 1],
            "reads": [] if rng.random() < 0.5 else reads_of(exclude=given),
            "self_source": {"unit": 0},
            "clicks": {"gives": True, "takes": True, "quantum": 1},
        }
        if sign_holder == given:
            entry["held"] = held("sign", parts)
        families.append(entry)
    families.append(
        {
            "name": body,
            "parts": [1],
            "phase": 2,
            "pair": "body",
            "reads": reads_of(),
            "self_source": {"unit": 0},
            "clicks": {"gives": True, "takes": True, "quantum": 1},
        }
    )
    for name in rest:
        families.append(
            {
                "name": name,
                "parts": rng.choice(PARTS),
                "phase": rng.choice([1, 2]),
                "pair": rng.choice(PAIRS),
                "reads": reads_of(),
                "self_source": {"unit": 0 if rng.random() < 0.7 else 24 * AMPLITUDE * rng.randint(1, 3)},
                "clicks": clicks(),
            }
        )
    rng.shuffle(families)
    return {"seed": seed, "families": families, "roles": roles, "holders": holders}


TEMPLATE = emitter_world(stock=1, ticks=INTERVALS)


AMPLITUDE = int(TEMPLATE["amplitude_bound"])


def string_constants(path: Path) -> list[tuple[int, str]]:
    """Every string constant of the module with its line, docstrings left out."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docstrings: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                docstrings.add(id(body[0].value))
    return [
        (node.lineno, node.value)
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings
    ]


def written_defaults(path: Path) -> list[str]:
    """Every `<obj>.get("<key>", <default>)` of the module with a default that is not None: a
    key of the files with a default written in the code (record 2089)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "get"
            and len(node.args) == 2
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
            and not (isinstance(node.args[1], ast.Constant) and node.args[1].value is None)
        ):
            found.append(f"{path.relative_to(ROOT)}:{node.lineno} {node.args[0].value!r}")
    return found


def family_names() -> set[str]:
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    return {family["name"] for family in universe["families"]}


# the orders of ALGEBRA.md 9.117 item 3 as the step file law/step.json gives them: the writers
# of one value at one place in the file's order, a write deferred from (ii) first
ORDERS = {
    ("(iv)", "a family's level at a Node"): ("the hold", "the source"),
    ("(iv)", "a body's content M_k"): ("the clicks", "the giving", "the clicks list"),
    ("(iv)", "a body's momentum n"): ("the giving", "the recoil"),
    ("(v)", "a body's momentum n"): ("the feed", "the induction"),
    ("(i)", "the arrivals"): ("the receive", "the internal representation"),
    ("(ii)", "the record's tally"): ("the clicks", "the lifetime"),
}
