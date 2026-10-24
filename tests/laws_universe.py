"""The one world's helpers shared by the Universe24 tests: the shipped files' paths (the folded world of 2026-10-24, the universe at nature's den, the board and the run's length alone; `FOLDER`, `WORLD`, `UNIVERSE`, `LOG`), the eras tool loaded (`ERAS`), the one universe's clock and the small torus's side (`GAMMA`, `CUBE`), the bare torus of the one universe file (`bare_torus`) and `flat`. The declared seed's universe and its small structured board (`DECLARED`, `small_world`) left 2026-10-24 with the tests of the cancelled worlds."""

import json
from pathlib import Path
from typing import Any

import numpy as np

from tests.laws import ROOT, load_file

FOLDER = ROOT / "examples" / "events" / "universe24"
WORLD, UNIVERSE = FOLDER / "universe24.json", FOLDER / "universe_universe24.json"
LOG = FOLDER / "universe24.eras.jsonl"
ERAS = load_file("eras", ROOT / "tools" / "eras.py")
GAMMA, CUBE = 1000, 3  # the one universe's clock and the small torus's side


def bare_torus(folder: Path, cube: int = CUBE, intervals: int = 60) -> Path:
    """The folded world's three keys on a bare torus of `cube` Nodes a side with the one universe file copied beside it (the folded loader, 2026-10-24: nothing declared, the light seeded on every Node); `world_files.REPOSITORY_ROOT` is `folder`."""
    (folder / "u.json").write_text(UNIVERSE.read_text(encoding="utf-8"), encoding="utf-8")
    world = {"universe": "u.json", "shape": [cube] * 3, "intervals": intervals}
    (path := folder / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    return path


def flat(array: Any) -> list[int]:
    return [int(x) for x in np.asarray(array, dtype=object).reshape(-1)]
