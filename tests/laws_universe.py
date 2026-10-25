"""The one world's helpers shared by the Universe24 tests: the shipped files' paths (the folded world of 2026-10-24, the universe at nature's den, the board and the run's length alone; `FOLDER`, `WORLD`, `UNIVERSE`), the one universe's clock and the small torus's side (`GAMMA`, `CUBE`), the tests' small universe and the bare torus of it (`SMALL`, `small_universe`, `bare_torus`), the former uniform sea laid by name (`uniform_sea`), the seed hand's sea plus one (`sea_plus_one`) and `flat`; the generic Node's toy of 2026-10-25, one Node of the bare 3-cube fed through its six Links (`CENTRE`, `NEIGHBOURS`, `node_toy`, `node_arrays`, `impose`, `fed_interval`, `at_centre`, `course`, `shaken`, `carried`), shared by its two test files. The declared seed's universe and its small structured board (`DECLARED`, `small_world`) left 2026-10-24 with the tests of the cancelled worlds, the eras tool loaded here (`ERAS`) and the log's path (`LOG`) with the tests' audit of the same day."""

import json
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import meeting_board, records, world_files
from event_universe.core.ports import AXES, PORT_SIDES
from event_universe.core.rule3 import wall_of
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import ROOT

FOLDER = ROOT / "examples" / "events" / "universe24"
WORLD, UNIVERSE = FOLDER / "universe24.json", FOLDER / "universe_universe24.json"
GAMMA, CUBE = 1000, 3  # the one universe's clock and the small torus's side
CENTRE = (1, 1, 1)  # the generic Node's toy: the one Node, the centre of the bare 3-cube (2026-10-25)
NEIGHBOURS = tuple(
    tuple((CENTRE[a] + side) if a == axis else CENTRE[a] for a in range(AXES))
    for axis, side in PORT_SIDES
)  # its six face neighbours in Port order
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


def node_toy(tmp_path, monkeypatch, lines=None, cube=CUBE):  # type: ignore[no-untyped-def]
    """The toy: the tests' small universe on a bare torus with the board's own meetings restricted to the centre (a test-side filter on `meeting_board.meetings`, no seam in src/) and every output line kept where `lines` is given."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    real = meeting_board.meetings
    monkeypatch.setattr(
        meeting_board, "meetings", lambda b, i, s, f: [m for m in real(b, i, s, f) if m[0] == CENTRE]
    )
    return Lattice(
        load_world(bare_torus(tmp_path, cube)), output=None if lines is None else lines.append
    )


def node_arrays(board):  # type: ignore[no-untyped-def]
    """Every array of every family's state keyed by (family, kind, number[, row]) as Python's integers: the lines' three, the write remainders, the phase lines' three."""
    found = {}
    for i, s in enumerate(board.states):
        for n, line in enumerate(s.lines):
            found[(i, "line", n)] = tuple(
                np.asarray(a, dtype=object) for a in (line.now, line.before, line.remainder)
            )
        for n, w in enumerate(s.write_remainders):
            found[(i, "write", n)] = (np.asarray(w, dtype=object),)
        for r, row in enumerate(s.phases):
            for n, line in enumerate(row):
                found[(i, "phase", r, n)] = tuple(
                    np.asarray(a, dtype=object) for a in (line.now, line.before, line.remainder)
                )
    return found


def impose(board, shell):  # type: ignore[no-untyped-def]
    """Every array `shell` holds (an `arrays` dict) written at the 26 shell Nodes through a new Record, the centre kept; an array the board lacks is skipped and one the shell lacks is left as the step made it."""
    mask = np.ones(board.shape, dtype=bool)
    mask[CENTRE] = False

    def merged(key, own):  # type: ignore[no-untyped-def]
        return tuple(
            np.where(mask, p, np.asarray(o, dtype=object)) for p, o in zip(shell[key], own, strict=True)
        )

    for i, s in enumerate(board.states):
        s.lines = [
            records.Record(*merged((i, "line", n), (li.now, li.before, li.remainder)))
            if (i, "line", n) in shell
            else li
            for n, li in enumerate(s.lines)
        ]
        s.write_remainders = [
            merged((i, "write", n), (w,))[0] if (i, "write", n) in shell else w
            for n, w in enumerate(s.write_remainders)
        ]
        for r, row in enumerate(s.phases):
            s.phases[r] = [
                records.Record(*merged((i, "phase", r, n), (li.now, li.before, li.remainder)))
                if (i, "phase", r, n) in shell
                else li
                for n, li in enumerate(row)
            ]


def fed_interval(board, start, after=None):  # type: ignore[no-untyped-def]
    """One fed interval: the shell at the interval's start imposed, every act before the close, the shell as its own step left it imposed (`after`, the start where the shell stands), the close; the start state the close read returned."""
    impose(board, start)
    kept = board.advanced_to_the_close()
    impose(board, start if after is None else after)
    board.closed_after(kept)
    return kept


def at_centre(found):  # type: ignore[no-untyped-def]
    """Every array of an `arrays` dict read at the centre as Python's integers."""
    return {key: tuple(int(a[CENTRE]) for a in value) for key, value in found.items()}


def course(tmp_path, monkeypatch, shift, intervals):  # type: ignore[no-untyped-def]
    """The plain board's own run: per interval its arrays at the start, after the acts and at the end, every array carried by the translation `shift` of the torus (so a Node of the board stands at the centre), with the board's output lines."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    lines = []
    board = Lattice(load_world(bare_torus(tmp_path, CUBE)), output=lines.append)

    def rolled(found):  # type: ignore[no-untyped-def]
        return {k: tuple(np.roll(a, shift, axis=(0, 1, 2)) for a in v) for k, v in found.items()}

    found = []
    for _ in range(intervals):
        start = rolled(node_arrays(board))
        kept = board.advanced_to_the_close()
        after = rolled(node_arrays(board))
        board.closed_after(kept)
        found.append((start, after, rolled(node_arrays(board))))
    return found, lines, board


def shaken(board, draw, levels, volumes, remainders=False):  # type: ignore[no-untyped-def]
    """A fed shell from the board's arrays: the light line's two levels random within `levels` (the remainder random in [0, w) too where asked) and the volume's time line standing at a random volume among `volumes` at every Node, the centre's own overwritten by nothing (`impose` keeps it)."""
    found, light, held = node_arrays(board), board.world.seed, board.held[0]
    now, before = (draw.integers(-levels, levels + 1, board.shape).astype(object) for _ in range(2))
    wall = wall_of(board.families[light].pair[1], GAMMA, board.unit)
    kept = (
        draw.integers(0, wall, board.shape).astype(object)
        if remainders
        else found[(light, "line", 0)][2]
    )
    found[(light, "line", 0)] = (now, before, kept)
    volume_now = np.asarray(draw.choice(volumes, board.shape), dtype=object)
    found[(held, "line", 0)] = (volume_now, volume_now.copy(), found[(held, "line", 0)][2])
    return found


def carried(shell, element):  # type: ignore[no-untyped-def]
    """A fed shell under one of the cube's 48, (a permutation of the axes, a sign per axis): every array transposed and flipped about the centre, the three axis lines of a held row permuted among themselves, the sign holder's odd lines negated with their remainders complemented where their axis is reversed."""
    permutation, signs = element
    found = {}

    def moved(a):  # type: ignore[no-untyped-def]
        a = np.transpose(a, permutation)
        return a[tuple(slice(None, None, -1) if s < 0 else slice(None) for s in signs)]

    for key, value in shell.items():
        found[key] = tuple(moved(a) for a in value)
    for key in list(
        found
    ):  # the axis lines 1 + a of a held row: the line of the axis `a` goes where the permutation sends it
        family, kind, number = key[0], key[1], key[2]
        if kind in ("line", "write") and 1 <= number <= AXES and family in (0, 1):
            axis = number - 1
            image = permutation.index(axis)
            found[(family, kind, 1 + image)] = tuple(moved(a) for a in shell[key])
    return found
