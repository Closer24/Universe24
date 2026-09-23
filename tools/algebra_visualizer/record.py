"""The readers of the algebra visualizer: a run's record, read and never changed.

Every function here opens one of the runner's files (`run.json`,
`events.jsonl`, `state.json`, `initialization.json`) or a series' register
(`expectations.json`) and returns what it holds as the record's own integers
(or `fractions.Fraction` where a register writes a reduced pair as text).
Nothing of the law is computed: no rule is evaluated, no engine table is
loaded, no record is stepped again (docs/designs/algebra_visualizer/DESIGN.md,
"The rules the page obeys"; the display contract of SIMULATOR_DEFINITIONS.md).
The module imports nothing of `event_universe`; the record's field names are
those of docs/ENGINE.md, "The detector's readings by type", and, for the
detector-law engine, of docs/designs/detector_law/BUILD.md section 3 on the
branch detector-law-build (read from its runs at 2f44797c; DESIGN_3D.md
section 5). The engine a run came from is told from `run.json`'s
`hypotheses` alone (`engine_of`); a key an engine does not write is "not
recorded", never a crash.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

RUN_FILES = ("run.json", "events.jsonl", "state.json", "initialization.json")

# The two engines, told from `run.json`'s `hypotheses` (DESIGN_3D.md 5.1).
ENGINE_OLD = "the Beam Law (beam-v1 with amplitude-v1)"
ENGINE_NEW = "the detector law (detector-law-v1)"
NEW_IDENTITY = "detector-law-v1"
MASSIVE_IDENTITY = "massive-record-v1"

# The line that makes one run folder (the runner, outside the tree).
MAKE_RUN = "PYTHONPATH=src python -m event_universe --init WORLD.json --output FOLDER"

# The line that makes a runs directory (the register's runner, outside the tree).
MAKE_RUNS = (
    "PYTHONPATH=src python tools/run_series.py --out RUNS_DIR "
    "examples/events/c_measured/c_measured.json examples/events/amplitude/slits_low.json"
)


class MissingRun(SystemExit):
    """A run folder without the runner's files: refused plainly, never made here."""


@dataclass
class RunRecord:
    """One run's record as the runner wrote it: the folder, `run.json` (the
    metadata), `events.jsonl` (every line, in the record's order), `state.json`
    (the snapshot at the last interval) and the world file the run was made
    from (`initialization.json`, a copy of the world file)."""

    folder: Path
    meta: dict[str, Any]
    events: list[dict[str, Any]]
    state: dict[str, Any]
    world: dict[str, Any]
    register: dict[str, Any] | None = None
    counts: dict[str, int] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.folder.parent.name if self.folder.name == "run" else self.folder.name

    @property
    def engine(self) -> str:
        """The engine the run came from, from `hypotheses` alone."""
        return engine_of(self.meta)

    @property
    def is_new(self) -> bool:
        return self.engine == ENGINE_NEW

    @property
    def massive(self) -> bool:
        """The massive record kind's key, written by the new engine when true."""
        return bool(self.meta.get("massive_record")) or MASSIVE_IDENTITY in hypotheses_of(self.meta)

    @property
    def exploratory(self) -> bool:
        """An EXPLORATORY run: the word in its folder's path or its model identity
        (the Boss's rule of 2026-09-23: such a page carries EXPLORATORY in its
        title and on every panel, never a result)."""
        return (
            "EXPLORATORY" in str(self.folder).upper()
            or "EXPLORATORY" in str(self.meta.get("model", "")).upper()
        )

    @property
    def ticks(self) -> int:
        value = self.meta.get("completed_ticks", self.meta.get("tick", 0))
        return int(value) if isinstance(value, int) else 0

    @property
    def shape(self) -> tuple[int, int, int]:
        found = self.meta.get("shape")
        if isinstance(found, list) and len(found) == 3:
            return (int(found[0]), int(found[1]), int(found[2]))
        return (0, 0, 0)

    def periodic(self, axis: str) -> bool:
        """Whether light's axis is periodic (`boundary`: "open", or per axis)."""
        boundary = self.meta.get("boundary")
        if isinstance(boundary, dict):
            return boundary.get(axis) == "periodic"
        return boundary == "periodic"

    def with_node(self) -> list[dict[str, Any]]:
        """Every line with a `tick` and a `node` (one Node or a list of Nodes),
        in the record's order: the marks of the board (DESIGN_3D.md 3.2)."""
        return [line for line in self.events if "tick" in line and node_of(line) is not None]

    def steps_of(self, number: int) -> list[dict[str, Any]]:
        """The old engine's `step` lines of one body, by its `number`."""
        return [
            line for line in self.events if line.get("event") == "step" and line.get("number") == number
        ]

    def block_lines_of(self, index: int) -> list[dict[str, Any]]:
        """The new engine's `block` lines of one block, by its `measured` index."""
        return [
            line
            for line in self.events
            if line.get("event") == "block" and line.get("measured") == index
        ]

    def blocks_snapshot(self) -> list[dict[str, Any]]:
        """The new engine's `blocks` of the snapshot (under the massive key)."""
        found = self.state.get("blocks", [])
        return list(found) if isinstance(found, list) else []

    def records_snapshot(self) -> list[dict[str, Any]]:
        """The new engine's live `records` of the snapshot."""
        found = self.state.get("records", [])
        return list(found) if isinstance(found, list) else []

    def declared_measured(self) -> list[dict[str, Any]]:
        """The world file's measured events (`initialization.json`, `measured`)."""
        found = self.world.get("measured", [])
        return list(found) if isinstance(found, list) else []

    def declared_detectors(self) -> list[dict[str, Any]]:
        """The world file's detector sets (`initialization.json`, `detectors`)."""
        found = self.world.get("detectors", [])
        return list(found) if isinstance(found, list) else []

    def meta_detectors(self) -> list[dict[str, Any]]:
        """The per-detector counts of `run.json` (`detectors`)."""
        found = self.meta.get("detectors", [])
        return list(found) if isinstance(found, list) else []

    def of_kind(self, *kinds: str) -> list[dict[str, Any]]:
        """The lines whose `event` is one of `kinds`, in the record's order."""
        wanted = set(kinds)
        return [line for line in self.events if line.get("event") in wanted]

    def of_record(self, identity: int) -> list[dict[str, Any]]:
        """Every line of one record (its `record` identity, or `of` on a
        `record` line under the reading `sum`), in the record's order."""
        return [
            line for line in self.events if line.get("record") == identity or line.get("of") == identity
        ]

    def bodies(self) -> list[dict[str, Any]]:
        """The measured events (the bodies) of the snapshot."""
        found = self.state.get("measured", [])
        return list(found) if isinstance(found, list) else []

    def detector_sets(self) -> list[dict[str, Any]]:
        """The detector sets of the snapshot (the faces among them)."""
        found = self.state.get("detectors", [])
        return list(found) if isinstance(found, list) else []

    def nodes_with_rows(self) -> list[dict[str, Any]]:
        """The Nodes that still hold rows at the last interval (the store's view)."""
        found = self.state.get("nodes", [])
        return list(found) if isinstance(found, list) else []

    def last_audit(self) -> dict[str, Any] | None:
        """The books at the last completed tick (`audit` of `run.json`)."""
        audit = self.meta.get("audit")
        if isinstance(audit, list) and audit:
            last = audit[-1]
            return dict(last) if isinstance(last, dict) else None
        return None


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _load_lines(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def load_run(folder: Path, register: Path | None = None, block: str | None = None) -> RunRecord:
    """Read one run folder (the runner's output directory) and, when given,
    the series' register beside its world (`block` names the register's entry
    of this world, the whole register when None). A folder without the four
    files is refused with the line that makes it."""
    missing = [name for name in RUN_FILES if not (folder / name).exists()]
    if missing:
        raise MissingRun(
            f"no run record under {folder} (missing {', '.join(missing)}); "
            f"make the runs first, outside the tree:\n    {MAKE_RUNS}\n"
            f"or one run:\n    {MAKE_RUN}"
        )
    events = list(_load_lines(folder / "events.jsonl"))
    counts: dict[str, int] = {}
    for line in events:
        kind = str(line.get("event"))
        counts[kind] = counts.get(kind, 0) + 1
    pins: dict[str, Any] | None = None
    if register is not None and register.exists():
        loaded = _load_json(register)
        if block is not None:
            loaded = loaded.get(block) if isinstance(loaded, dict) else None
        pins = loaded if isinstance(loaded, dict) else None
    found = RunRecord(
        folder=folder,
        meta=_load_json(folder / "run.json"),
        events=events,
        state=_load_json(folder / "state.json"),
        world=_load_json(folder / "initialization.json"),
        register=pins,
        counts=counts,
    )
    return found


def hypotheses_of(meta: dict[str, Any]) -> list[str]:
    found = meta.get("hypotheses")
    return [str(v) for v in found] if isinstance(found, list) else []


def engine_of(meta: dict[str, Any]) -> str:
    """The engine a `run.json` came from: the new one when `detector-law-v1`
    is among its `hypotheses`, else the old. A `run.json` without the key
    is refused, naming it (DESIGN_3D.md 5.1)."""
    if "hypotheses" not in meta:
        raise MissingRun("run.json without the key hypotheses: the engine cannot be told; refused")
    return ENGINE_NEW if NEW_IDENTITY in hypotheses_of(meta) else ENGINE_OLD


def node_of(line: dict[str, Any]) -> list[tuple[int, int, int]] | None:
    """The Node or Nodes a line names (`node`: one triple or a list of them;
    on a `step` line the Node it moved to), or None when it names none."""
    raw = line.get("to") if line.get("event") == "step" else line.get("node")
    if not isinstance(raw, list) or not raw:
        return None
    if all(isinstance(v, int) for v in raw) and len(raw) == 3:
        return [(int(raw[0]), int(raw[1]), int(raw[2]))]
    found = []
    for entry in raw:
        if isinstance(entry, list) and len(entry) == 3 and all(isinstance(v, int) for v in entry):
            found.append((int(entry[0]), int(entry[1]), int(entry[2])))
    return found or None


def chosen_of(line: dict[str, Any]) -> str | None:
    """The cell a `gather` line's click chose (`chosen[0][0]`), or None."""
    chosen = line.get("chosen")
    if isinstance(chosen, list) and chosen and isinstance(chosen[0], list) and chosen[0]:
        return str(chosen[0][0])
    return None


def fraction(value: Any) -> Fraction:
    """A register's number as an exact fraction: an integer, a `[n, d]` pair or
    the text `n/d` (the registers write reduced pairs as text)."""
    if isinstance(value, bool):
        raise TypeError("a boolean is not a number of the record")
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return Fraction(int(value[0]), int(value[1]))
    raise TypeError(f"not a number of the record: {value!r}")


def manhattan(a: Iterable[int], b: Iterable[int]) -> int:
    """The Manhattan distance of two Nodes: a difference of recorded integers."""
    return sum(abs(int(x) - int(y)) for x, y in zip(a, b, strict=True))


def squared_distance(a: Iterable[int], b: Iterable[int]) -> int:
    """The squared Euclidean distance of two Nodes: exact on integers."""
    return sum((int(x) - int(y)) ** 2 for x, y in zip(a, b, strict=True))


FACE_STEPS: dict[str, tuple[int, int, int]] = {
    "face:+x": (1, 0, 0),
    "face:-x": (-1, 0, 0),
    "face:+y": (0, 1, 0),
    "face:-y": (0, -1, 0),
    "face:+z": (0, 0, 1),
    "face:-z": (0, 0, -1),
}


def face_node(click: dict[str, Any]) -> tuple[int, int, int]:
    """The Node just outside the face a click left through: the click's Node
    plus the face's unit step (the face's name is on the click line)."""
    node = [int(v) for v in click["node"]]
    step = FACE_STEPS[str(click["detector"])]
    return (node[0] + step[0], node[1] + step[1], node[2] + step[2])


def label_class(label: Iterable[int]) -> str:
    """The class of a direction read off its recorded label (the unit vector
    of the direction at the scale Q, on the click line as `momentum`): an
    axis (one component), a face diagonal (two of equal size), a body diagonal
    (three of equal size), else the rest of the fan. A reading of the label,
    not a table of the engine."""
    sizes = sorted(abs(int(v)) for v in label if int(v) != 0)
    if len(sizes) == 1:
        return "axes"
    if len(sizes) == 2 and sizes[0] == sizes[1]:
        return "face_diagonals"
    if len(sizes) == 3 and sizes[0] == sizes[1] == sizes[2]:
        return "body_diagonals"
    return "rest"
