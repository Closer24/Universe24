"""The one world's helpers shared by the Universe24 tests: the shipped files' paths (the folded world of 2026-10-24, the universe at nature's den, the board and the run's length alone; `FOLDER`, `WORLD`, `UNIVERSE`, `LOG`), the eras tool loaded (`ERAS`), the one universe's clock and the small torus's side (`GAMMA`, `CUBE`), the tests' small universe and the bare torus of it (`SMALL`, `small_universe`, `bare_torus`), the former uniform sea laid by name (`uniform_sea`) and `flat`. The declared seed's universe and its small structured board (`DECLARED`, `small_world`) left 2026-10-24 with the tests of the cancelled worlds."""

import json
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.lattice import Lattice
from tests.laws import ROOT, load_file

FOLDER = ROOT / "examples" / "events" / "universe24"
WORLD, UNIVERSE = FOLDER / "universe24.json", FOLDER / "universe_universe24.json"
LOG = FOLDER / "universe24.eras.jsonl"
ERAS = load_file("eras", ROOT / "tools" / "eras.py")
GAMMA, CUBE = 1000, 3  # the one universe's clock and the small torus's side
SMALL = {  # the tests' small universe for the runs (2026-10-24, the family-less file): the one universe's clock, unit, width and Link unit at the den 1,021, a prime 1 mod 4 (30^2 + 11^2), whose circle has two points; the bare 3-cube bangs from the light seed and births its pairs at the first meeting; the shipped file's 26 points run at the record's pace and are the record's business
    "integers": {
        "den": 1021,
        "node_clock": GAMMA,
        "quantum_action": 36000,
    }  # the width derived and G the engine's, 2026-10-24
}


def bare_torus(folder: Path, cube: int = CUBE, intervals: int = 60) -> Path:
    """The folded world's three keys on a bare torus of `cube` Nodes a side with the tests' small universe written beside it (`small_universe`; the folded loader, 2026-10-24: nothing declared, the light seeded on every Node); `world_files.REPOSITORY_ROOT` is `folder`."""
    small_universe(folder)
    world = {"universe": "u.json", "shape": [cube] * 3, "intervals": intervals}
    (path := folder / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    return path


def uniform_sea(board: Any, index: int) -> None:
    """The uniform sea, the law's seed to 2026-10-24, laid by a test in the seed's place (monkeypatch seed.uniform_seed): the massless point at the drift on every Node of the torus, the origin included; the law's seed since that day leaves the origin empty (seed.uniform_seed, ORIGIN), so a sentence posed on the uniform content lays the sea itself, by name."""
    from event_universe import records, seed
    from event_universe.emission import emitted_lines
    from event_universe.lay import laid

    family, drift = board.families[index], seed.drift_of(board.world.quantum_action)
    now, before = records.full(board.shape, drift, board.kind), records.zeros(board.shape, board.kind)
    first = records.record_slice(family, 0).start
    for line in emitted_lines(family):
        laid(board, index, first + line, (now, before), None, None)


def small_universe(folder: Path) -> Path:
    """The tests' small universe (`SMALL`) written as u.json in `folder`."""
    (path := folder / "u.json").write_text(json.dumps(SMALL), encoding="utf-8")
    return path


def flat(array: Any) -> list[int]:
    return [int(x) for x in np.asarray(array, dtype=object).reshape(-1)]


def sea_plus_one(at: tuple[int, int, int]) -> Any:
    """The seed hand's S1: the law's uniform sea of light and one more quantum of it at the Node `at` (a test's seed, laid through the lay act as the law's own is)."""

    def laid_seed(board: Lattice, index: int) -> None:
        from event_universe import records, seed
        from event_universe.emission import emitted_lines
        from event_universe.lay import laid

        family, drift = board.families[index], seed.drift_of(board.world.quantum_action)
        first, zeros = records.record_slice(family, 0).start, records.zeros(board.shape, board.kind)
        mask = board.mask((at,))
        for level, nodes in (
            (records.full(board.shape, drift, board.kind), None),
            (np.where(mask, drift, 0), mask),
        ):
            for line in emitted_lines(family):
                laid(board, index, first + line, (level, zeros), None, None, nodes)

    return laid_seed
