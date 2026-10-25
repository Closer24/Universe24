"""Hand u2's shared helpers: the bare 3-cube of the tests' small universe (den 1,021) loaded under the engine's own hole seed, with the test module tests/test_the_board_is_the_cube_48.py's `carried`, `apart`, `cube_48`, `turns_of` and `axis_map` imported by path; integer readings only (ALGEBRA.md, The Node; the owner's Addition 3)."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))  # tests.laws_universe and tests.laws by their package path
sys.path.insert(0, str(ROOT / "src"))

from event_universe import world_files  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.loader import universe  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import SMALL  # noqa: E402

OUT = Path(__file__).resolve().parent


def load_by_path(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


CUBE48 = load_by_path("cube48_test", ROOT / "tests" / "test_the_board_is_the_cube_48.py")
NODE_INTEGERS = load_by_path("node_integers_tool", ROOT / "tools" / "node_integers.py")


class Patch:
    """A stand-in for pytest's monkeypatch: setattr with the originals kept, undone by `undo`."""

    def __init__(self) -> None:
        self.kept: list[tuple[object, str, object]] = []

    def setattr(self, target: object, name: str, value: object) -> None:
        self.kept.append((target, name, getattr(target, name)))
        setattr(target, name, value)

    def undo(self) -> None:
        for target, name, value in reversed(self.kept):
            setattr(target, name, value)
        self.kept = []


def scratch(label: str) -> Path:
    base = Path(os.environ.get("TMPDIR", tempfile.gettempdir())) / "u2"
    base.mkdir(parents=True, exist_ok=True)
    found = Path(tempfile.mkdtemp(prefix=label + "_", dir=base))
    return found


def bare_board(
    den: int = SMALL["integers"]["den"],
    side: int = 3,
    intervals: int = 20,
    gapped: bool = True,
    lines: list | None = None,
) -> tuple[Lattice, Patch]:
    """The tests' small universe at `den` on the bare cube of `side` under the engine's own hole seed, the volume holder gapped (the engine's own pair) or massless by name as the 48 test's `board_of` has it; the patch returned for its `undo`."""
    folder = scratch(f"den{den}_{side}")
    patch = Patch()
    patch.setattr(world_files, "REPOSITORY_ROOT", folder)
    if not gapped:
        patch.setattr(universe, "volume_pair", lambda den, gamma: (den, den))
    integers = {**SMALL["integers"], "den": den}
    (folder / "u.json").write_text(json.dumps({"integers": integers}), encoding="utf-8")
    world = {"universe": "u.json", "shape": [side] * 3, "intervals": intervals}
    (folder / "w.json").write_text(json.dumps(world), encoding="utf-8")
    board = Lattice(load_world(folder / "w.json"), output=None if lines is None else lines.append)
    return board, patch


def write(name: str, text: str) -> None:
    (OUT / name).write_text(text, encoding="utf-8")
    print(text)
