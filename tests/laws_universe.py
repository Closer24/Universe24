"""The one world's helpers shared by the Universe24 tests: the shipped files' paths (the folded world of 2026-10-24, the universe at nature's den, the board and the run's length alone; `FOLDER`, `WORLD`, `UNIVERSE`, `LOG`), the eras tool loaded (`ERAS`), the one universe's clock and the small torus's side (`GAMMA`, `CUBE`), the tests' small universe and the bare torus of it (`SMALL`, `small_universe`, `bare_torus`) and `flat`. The declared seed's universe and its small structured board (`DECLARED`, `small_world`) left 2026-10-24 with the tests of the cancelled worlds."""

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
SMALL = {  # the tests' small universe for the runs (2026-10-24, the family-less file): the one universe's clock, unit, width and Link unit at the den 1,021, a prime 1 mod 4 (30^2 + 11^2), whose circle has two points; the bare 3-cube bangs from the light seed and births its pairs at the first meeting; the shipped file's 242 points run at the record's pace and are the record's business
    "integers": {
        "den": 1021,
        "node_clock": GAMMA,
        "quantum_action": 36000,
        "width": 92,
        "link_unit": 16,
    }
}


def bare_torus(folder: Path, cube: int = CUBE, intervals: int = 60) -> Path:
    """The folded world's three keys on a bare torus of `cube` Nodes a side with the tests' small universe written beside it (`small_universe`; the folded loader, 2026-10-24: nothing declared, the light seeded on every Node); `world_files.REPOSITORY_ROOT` is `folder`."""
    small_universe(folder)
    world = {"universe": "u.json", "shape": [cube] * 3, "intervals": intervals}
    (path := folder / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    return path


def small_universe(folder: Path) -> Path:
    """The tests' small universe (`SMALL`) written as u.json in `folder`."""
    (path := folder / "u.json").write_text(json.dumps(SMALL), encoding="utf-8")
    return path


def flat(array: Any) -> list[int]:
    return [int(x) for x in np.asarray(array, dtype=object).reshape(-1)]
