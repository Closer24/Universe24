"""THE REGRESSION RECORD OF EVERY SHIPPED WORLD (the model owner's short procedure, record 2214
point 7: "with the new feature off, all the old runs come out identical to the bit"; the Boss's
records 2216 (2) and 2230; issue #1155): one digest per shipped world over the engine's whole
state after a recorded number of intervals, written once here into `tests/shipped_worlds.json`
and compared by `tests/test_shipped_worlds.py` on every pull request, whatever it changes.

THE DIGEST is SHA-256 over a canonical dump of the simulation object after the intervals: every
attribute, every dataclass field, every integer array (its dtype, shape and bytes), every list
and dict in a fixed order; the parsed world included, so a change of the loader, of the rule, of
a hold, of a click or of a world file moves it. Nothing physical is read: the digest is a HOST
reading of the state, bit for bit, never a measurement.

THE INTERVALS per world: the world's own `ticks` when the whole run fits the budget of
`FULL_RUN_SECONDS` (estimated from `SAMPLE_STEPS` timed steps), else `PREFIX_INTERVALS`; the
count is recorded beside the digest and the test replays exactly it. A world whose file changes
(its stamp) or whose digest moves is re-recorded here on purpose, in the same commit as the
change that moved it, with the reason in that commit's message; the test never writes.

    PYTHONPATH=src python tools/record_shipped_worlds.py [world.json ...]
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "examples" / "events"
RECORD = ROOT / "tests" / "shipped_worlds.json"
FORMAT = "shipped-worlds-digest"
# the folders whose worlds are ahead of the loader's words (their structure tests hold their
# load as expected failures): not shipped worlds of the engine
AHEAD = ("check_mode", "source")
FULL_RUN_SECONDS = 12.0
PREFIX_INTERVALS = 200
SAMPLE_STEPS = 5
# THE CLICK PATH: no shipped world clicks within the prefix, so three cheap worlds are recorded
# further, past their first clicks (the light clock 42 clicks, the point light clock 11, the
# Lorentz clock at rest 39; each under ten seconds, HOST), so the ladder, the taking, the giving
# and the recoil are compared bit for bit as well as the step, the hold and the reads
LONGER = {
    "examples/events/massive_record/light_clock.json": 1500,
    "examples/events/point_emitter/point_light_clock.json": 3000,
    "examples/events/toward_nature/lorentz_rest.json": 1500,
}


def shipped_worlds() -> list[Path]:
    """Every world file under examples/events/: a JSON object with `shape`, `ticks` and a
    `universe`, outside the folders ahead of the loader; sorted by path."""
    worlds = []
    for path in sorted(EVENTS.rglob("*.json")):
        if any(part in AHEAD for part in path.relative_to(EVENTS).parts):
            continue
        document = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(document, dict) and {"shape", "ticks", "universe"} <= set(document):
            worlds.append(path)
    return worlds


def canonical(value: Any, out: list[bytes], seen: dict[int, int] | None = None) -> None:
    """The canonical dump: a fixed byte form for every kind of state the engine holds. A
    container met a second time (the engine's objects point at each other) is written as the
    order number of its first visit, so the dump is finite and the same for the same state."""
    if seen is None:
        seen = {}
    if (
        isinstance(value, (list, tuple, dict, set, frozenset))
        or (dataclasses.is_dataclass(value) and not isinstance(value, type))
        or (hasattr(value, "__dict__") and not callable(value) and not isinstance(value, np.ndarray))
    ):
        if id(value) in seen:
            out.append(f"<again {seen[id(value)]}>".encode())
            return
        seen[id(value)] = len(seen)
    if value is None or isinstance(value, (bool, int, str)):
        out.append(repr(value).encode())
    elif isinstance(value, float):
        out.append(value.hex().encode())
    elif isinstance(value, np.ndarray):
        out.append(f"array {value.dtype} {value.shape} ".encode())
        out.append(np.ascontiguousarray(value).tobytes())
    elif isinstance(value, np.generic):
        out.append(repr(value.item()).encode())
    elif isinstance(value, (list, tuple)):
        out.append(b"[")
        for item in value:
            canonical(item, out, seen)
            out.append(b",")
        out.append(b"]")
    elif isinstance(value, dict):
        out.append(b"{")
        for key in sorted(value, key=repr):
            out.append(repr(key).encode())
            out.append(b":")
            canonical(value[key], out, seen)
            out.append(b",")
        out.append(b"}")
    elif isinstance(value, (set, frozenset)):
        canonical(sorted(value, key=repr), out, seen)
    elif dataclasses.is_dataclass(value) and not isinstance(value, type):
        out.append(type(value).__name__.encode())
        canonical({f.name: getattr(value, f.name) for f in dataclasses.fields(value)}, out, seen)
    elif callable(value):
        out.append(b"<callable>")
    elif hasattr(value, "__dict__"):
        out.append(type(value).__name__.encode())
        canonical(vars(value), out, seen)
    else:
        raise TypeError(f"no canonical form for {type(value).__name__}")


def state_digest(simulation: DetectorLawSimulation) -> str:
    parts: list[bytes] = []
    canonical(vars(simulation), parts)
    return hashlib.sha256(b"".join(parts)).hexdigest()


def run(path: Path, intervals: int | None = None) -> dict[str, Any]:
    """The world stepped `intervals` times (its recorded count, or the count this tool picks) and
    its digest, with the counts that name a difference when the digest moves."""
    document = json.loads(path.read_text(encoding="utf-8"))
    stamp = input_stamp(document)
    started = time.monotonic()
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    lines: list[dict[str, object]] = []
    simulation.record = lines.append
    ticks = int(document["ticks"])
    if intervals is None:
        for _ in range(min(SAMPLE_STEPS, ticks)):
            simulation.step()
        per_step = (time.monotonic() - started) / max(1, min(SAMPLE_STEPS, ticks))
        intervals = ticks if per_step * ticks <= FULL_RUN_SECONDS else min(ticks, PREFIX_INTERVALS)
        intervals = min(ticks, LONGER.get(path.resolve().relative_to(ROOT).as_posix(), intervals))
    while simulation.tick < intervals:
        simulation.step()
    return {
        "stamp": stamp,
        "ticks": ticks,
        "intervals": intervals,
        "digest": state_digest(simulation),
        "records": len(simulation.records),
        "clicks": len(simulation.layer.gathers),
        "lines": len(lines),
        "seconds": round(time.monotonic() - started, 2),
    }


def main(argv: list[str] | None = None) -> int:
    names = argv if argv is not None else sys.argv[1:]
    paths = [Path(n).resolve() for n in names] if names else shipped_worlds()
    recorded: dict[str, Any] = (
        json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.exists() else {"worlds": {}}
    )
    worlds: dict[str, Any] = dict(recorded.get("worlds", {}))
    for path in paths:
        key = path.relative_to(ROOT).as_posix()
        entry = run(path)
        entry.pop("seconds")
        worlds[key] = entry
        print(key, json.dumps(entry))
    commit = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True
    ).stdout.strip()
    RECORD.write_text(
        json.dumps(
            {"format": FORMAT, "recorded_at": commit, "worlds": dict(sorted(worlds.items()))}, indent=1
        )
        + "\n",
        encoding="utf-8",
    )
    print("recorded", len(worlds), "worlds at", commit, "into", RECORD.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
