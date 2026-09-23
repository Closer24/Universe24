"""The readers of the algebra visualizer: a run's record, read and never changed.

Every function here opens one of the runner's files (`run.json`,
`events.jsonl`, `state.json`, `initialization.json`) or a series' register
(`expectations.json`) and returns what it holds as the record's own integers
(or `fractions.Fraction` where a register writes a reduced pair as text).
Nothing of the law is computed: no rule is evaluated, no engine table is
loaded, no record is stepped again (docs/designs/algebra_visualizer/DESIGN.md,
"The rules the page obeys"; the display contract of SIMULATOR_DEFINITIONS.md).
The module imports nothing of `event_universe`; the record's field names are
those of docs/ENGINE.md, "The detector's readings by type".
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

RUN_FILES = ("run.json", "events.jsonl", "state.json", "initialization.json")

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
            f"make the runs first, outside the tree:\n    {MAKE_RUNS}"
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
