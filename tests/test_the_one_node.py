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
    """The loader's key lists, enumerated, hold content keys alone (the owner's rule of 2026-10-23: no more keys in the code, one single Node in the whole universe): a file naming a former act key meets the loader's ordinary refusal of an unknown key, the same as any misspelling; and no module under src/event_universe/loader or the generator tools/pixel_mode.py names a retired key or its words in its code (an ast check over the string constants outside the docstrings, as tests/test_the_acts_table.py walks the divisions)."""
    from event_universe.loader import draw, node_detector_declaration, universe
    from event_universe.loader import world as loader_world

    assert set(loader_world.WORLD_KEYS) == {
        "shape",
        "boundary",
        "face_depth",
        "faces",
        "intervals",
        "universe",
        "bodies",
        "packets",
        "node_detectors",
        "receding",
        "draw",
        "lay",
    }
    assert set(universe.HELD_KEYS) == {"sources", "level_weight", "write_weight", "rest"}
    assert set(universe.FAMILY_KEYS) == {
        "name",
        "pair",
        "dimension",
        "held",
        "reads",
        "exchange",
        "senses",
    }
    assert [list(s) for s in universe.SOURCES] == [
        ["form"],
        ["form", "tensions"],
        ["wronskian"],
        ["form", "tensions", "flux"],
    ]
    assert draw.WORLD_DRAW_KEYS == draw.DRAW_KEYS == ("window",)
    assert set(node_detector_declaration.TRANSITION_KEYS) == {
        "from",
        "to",
        "drive",
        "weight",
        "resonance",
    }
    with pytest.raises(ValueError, match="unknown key"):
        universe.universe_of(
            {
                "integers": {"node_clock": 6000, "quantum_action": 32768, "width": 63, "link_unit": 16},
                "families": [
                    {
                        "name": "g",
                        "pair": [6000, 6000],
                        "reads": {"g": 1},
                        "held": {
                            "sources": ["form", "tensions"],
                            "level_weight": 1,
                            "write_weight": 1,
                            "act": "pace",
                        },
                    }
                ],
            }
        )
    named = []
    for path in sorted(SRC.joinpath("loader").glob("*.py")) + [
        SRC.parents[1] / "tools" / "pixel_mode.py"
    ]:
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


PLACES = (  # the former keys and the place each stood at: the loader's ordinary refusal of an unknown key at each
    ("interval", "world"),
    ("uniform", "world"),
    ("erasure", "world"),
    ("meeting", "draw"),
    ("reach", "draw"),
    ("act", "held"),
    ("booking", "held"),
    ("factor", "held"),
    ("pressure", "held"),
    ("form", "held"),
    ("converts", "family"),
    ("dipole", "transition"),
)
STEPS = {  # the step's one list: every function of src/event_universe whose name is a step, by module (the acts table lists every division)
    "flux.py": [
        "step_line",
        "step_traceless",
        "step_momentum",
        "step_plane",
        "step_family",
        "step_records",
    ],
    "cone.py": ["stepped_alone"],
    "shear.py": ["stepped"],
    "meeting.py": ["stepped"],
    "lattice.py": ["stepped", "step", "step_inverse"],
}
LOADER_FILES = (  # the loader's files under examples/ and tests/, found by the keys that name each kind
    (("shape", "universe"), "a world"),
    (("families", "integers"), "a universe"),
    (("world_digest",), "a mode file"),
)


def test_every_shipped_and_test_file_holds_content_and_run_parameters_alone():  # type: ignore[no-untyped-def]
    """Every world, universe and mode file under examples/ and tests/ (found by its own key: a world by `shape`, a universe by `families`, a mode file by `world_digest`) holds keys of the loader's vocabulary alone at every level the loader reads with a key table (the world's keys, its bodies', node_detectors', draw's, lay's, receding faces' and packets', the universe's, its families' and their held rows', a body's transitions', rates' and parts'), and no former key stands anywhere in them (the owner's rule of 2026-10-23: the files hold content and run parameters alone)."""
    from event_universe.loader import faces, lay, mode, node_detector_declaration, universe
    from event_universe.loader import world as loader_world

    tables = {
        "world": set(loader_world.WORLD_KEYS),
        "bodies": set(loader_world.BODY_KEYS),
        "node_detectors": set(loader_world.NODEDETECTOR_KEYS),
        "draw": set(draw_keys := ("window",)),
        "lay": set(lay.LAY_KEYS),
        "faces": set(faces.FACE_KEYS),
        "transitions": set(node_detector_declaration.TRANSITION_KEYS),
        "rates": set(node_detector_declaration.RATE_KEYS) | set(node_detector_declaration.RATE_OPTIONAL),
        "parts": set(node_detector_declaration.PART_KEYS),
        "universe": set(universe.UNIVERSE_KEYS),
        "integers": set(universe.INTEGER_KEYS),
        "families": set(universe.FAMILY_KEYS),
        "held": set(universe.HELD_KEYS),
    }
    assert draw_keys == tuple(loader_world.draw_of({"window": 1}, "draw", True).__dataclass_fields__)
    retired, found = set(RETIRED) | {"interval", "write_weight"}, []
    for folder in ("examples", "tests"):
        for path in sorted((SRC.parents[1] / folder).rglob("*.json")):
            try:
                document = json.loads(path.read_text(encoding="utf-8"))
            except ValueError:
                continue
            if not isinstance(document, dict):
                continue
            kind = next(
                (kind for keys, kind in LOADER_FILES if all(key in document for key in keys)), None
            )
            if path.name.endswith(("design.json", "expectation.json")) or ".blind" in path.name:
                continue  # the generator's design, the blind and the expectation: no file the loader reads
            if kind is None:
                continue
            table = "world" if kind == "a world" else "universe" if kind == "a universe" else None
            if table:
                found += [(path.name, key) for key in document if key not in tables[table]]
            for key, value in document.items():
                rows = value if isinstance(value, list) else [value] if isinstance(value, dict) else []
                if kind == "a mode file":  # the generator's entries: a body's or a packet's levels laid
                    found += [
                        (path.name, key, k)
                        for row in rows
                        if isinstance(row, dict)
                        for k in row
                        if k not in mode.MODE_BODY_KEYS
                    ]
                    continue
                for row in rows:
                    if key in tables and isinstance(row, dict):
                        found += [(path.name, key, k) for k in row if k not in tables[key]]
                    for inner in ("held", "transitions", "rates", "parts"):
                        for entry in [row.get(inner)] if isinstance(row, dict) else []:
                            for item in (
                                entry
                                if isinstance(entry, list)
                                else [entry]
                                if isinstance(entry, dict)
                                else []
                            ):
                                found += [
                                    (path.name, key, inner, k) for k in item if k not in tables[inner]
                                ]
                                if inner == "held":
                                    found += [
                                        (path.name, key, "held.write_weight")
                                        for k in item
                                        if k == "write_weight" and "wronskian" in item.get("sources", [])
                                    ]
            words = {key for key in document} | {
                k for v in document.values() if isinstance(v, dict) for k in v
            }
            assert not words & (retired - {"interval"}), (path.name, words & retired)
    assert found == [], found


@pytest.mark.parametrize(("key", "place"), PLACES)
def test_the_loader_refuses_every_former_key_by_name(key, place):  # type: ignore[no-untyped-def]
    """Every former key of the universe and world files meets the loader's ordinary refusal of an unknown key at the place it stood (the owner's rule of 2026-10-23: no more keys in the code, one Node): the world's `interval`, `uniform` and `erasure`, the draw's `meeting` and `reach`, a held row's `act`, `booking`, `factor`, `pressure` and `form`, a family's `converts`, a transition's `dipole`."""
    from event_universe.loader import draw, node_detector_declaration, universe
    from event_universe.loader import world as loader_world
    from event_universe.loader.keys import keyed

    held = {"sources": ["form"], "level_weight": 1, "write_weight": 1}
    family = {"name": "g", "pair": [6000, 6000], "reads": {"g": 1}, "held": held}
    integers = {"node_clock": 6000, "quantum_action": 32768, "width": 63, "link_unit": 16}
    with pytest.raises(ValueError, match=f"unknown key '{key}'"):
        if place == "world":
            world = {"shape": [3, 1, 1], "boundary": {}, "intervals": 1, "universe": "u.json", key: 1}
            keyed(
                {**world, "bodies": [], "node_detectors": []},
                "the world",
                loader_world.WORLD_KEYS,
                loader_world.WORLD_REQUIRED,
            )
        elif place == "draw":
            draw.draw_of({"window": 4, key: "cone"}, "draw", True)
        elif place == "held":
            universe.universe_of(
                {"integers": integers, "families": [{**family, "held": {**held, key: "pace"}}]}
            )
        elif place == "family":
            universe.universe_of({"integers": integers, "families": [{**family, key: {}}]})
        else:
            row = {
                "from": "g",
                "to": "e",
                "drive": "photon",
                "weight": 1,
                "resonance": [5, 6],
                key: [[0, 0, 1], 1],
            }
            node_detector_declaration.transitions_of([row], "t", ("g", "e"), {"photon": 1}, 2)


def test_the_steps_act_list_is_the_one_list():  # type: ignore[no-untyped-def]
    """The step's act list is the one list: every function of src/event_universe whose name is a step (`step*`, `stepped*`) stands in STEPS by module, so no alternative step is reachable from the engine's public surface (Lattice.step and Lattice.step_inverse, which call meeting.stepped and flux.step_records, the shear's momentum and the cone stepped alone), and the Lattice has the two public acts of an interval alone, `step` and `step_inverse`."""
    found: dict[str, list[str]] = {}
    for path in sorted(SRC.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        names = [
            n.name
            for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name.startswith(("step", "stepped"))
        ]
        if names:
            found[path.relative_to(SRC).as_posix()] = names
    assert found == STEPS, found
