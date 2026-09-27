"""THE REGRESSION RECORD OF EVERY SHIPPED WORLD (the model owner's short procedure, record 2214
point 7: "with the new feature off, all the old runs come out identical to the bit"; the Boss's
records 2216 (2) and 2230; issue #1155): one digest per shipped world over the engine's whole
state after a recorded number of intervals, written once here into `tests/shipped_worlds.json`
and compared by `tests/test_shipped_worlds.py` on every pull request, whatever it changes.

THE DIGEST is SHA-256 over what the run is, never over how the code holds it (the Boss's word on
PR #1172): the output lines the run wrote; the engine's own state stream (`snapshot_stream`: the
interval, the bodies' contents, momenta and spins, the held families' levels and the live
records' integers, each under the world file's family names, record identities and body
numbers); every live record's levels now and before and its remainder; every held family's
levels before and its remainder; every read's remainder (by the reading and the read family's
names and the axis); the clicks; and the books. Every key is a name of the world's files or a
word of the ledger, never a Python attribute name, so a cut that renames or moves the engine's
attributes while every run stays bit for bit leaves the digest where it is (its test). Nothing
physical is read: the digest is a HOST reading of the state, bit for bit, never a measurement.

THE INTERVALS per world: the world's own `ticks` when the whole run fits the budget of
`FULL_RUN_SECONDS` (estimated from `SAMPLE_STEPS` timed steps), else `PREFIX_INTERVALS`; the
count is recorded beside the digest and the test replays exactly it. A world whose file changes
(its stamp) or whose digest moves is re-recorded here on purpose, in the same commit as the
change that moved it, with the reason in that commit's message; the test never writes.

    PYTHONPATH=src python tools/record_shipped_worlds.py [world.json ...]

CI RECORDS THE REGRESSION (the model owner's word of 2026-09-27): no agent runs the 22 worlds
for a record again. The replay test hands `run` a folder, and every world's entry is written
there as `<world path with '/' as '__'>.record.json` beside the digest it compares; the
world jobs upload the folder, and one job merges every entry into the record with

    PYTHONPATH=src python tools/record_shipped_worlds.py --merge <folder> --recorded-at <sha>

the recorded count of intervals kept, a refusing world at its refusal, every world the folder
does not name kept as recorded; where the record then differs from the head's, the job commits
it to the pull request's branch and the new head replays it bit for bit.
"""

from __future__ import annotations

import argparse
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
ENTRY_SUFFIX = ".record.json"  # one world's entry, written by the replay for CI's merge
# the folders whose worlds are ahead of the loader's words (their structure tests hold their
# load as expected failures; `generated`: the readable example of the law's form, its giving body
# refused at load until the mode file): not shipped worlds of the engine
AHEAD = ("check_mode", "generated", "source")
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
    if isinstance(value, bool) or value is None or isinstance(value, str):
        out.append(repr(value).encode())
    elif isinstance(value, int):
        # an integer by its bytes, never its decimal string: the books' conserved forms run to
        # thousands of digits (GAMEBOARD readings, ALGEBRA.md #the-direction)
        out.append(b"int " + value.to_bytes((value.bit_length() + 8) // 8, "big", signed=True))
    elif isinstance(value, float):
        out.append(value.hex().encode())
    elif isinstance(value, np.ndarray):
        out.append(f"array {value.dtype} {value.shape} ".encode())
        out.append(np.ascontiguousarray(value).tobytes())
    elif isinstance(value, np.generic):
        canonical(value.item(), out, seen)
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


def run_reading(simulation: DetectorLawSimulation, lines: list[dict[str, object]]) -> dict[str, Any]:
    """What the run is, under stable names: the output lines, the engine's state stream, the
    records' and the held families' levels and remainders, the reads' remainders, the clicks
    and the books, every family by its name. The engine's containers are read by their present names (`records`,
    `held_records`, `_pace_carry`, `layer.gathers`): a cut that renames one breaks this reader
    aloud, and the reader follows; the digest never moves on its own."""
    names = [family.name for family in simulation.families]
    records = {
        str(live.identity): {
            "family": names[live.family],
            "now": live.now,
            "before": live.before,
            "remainder": live.remainder,
        }
        for live in simulation.records.values()
    }
    held = {
        names[family]: {"before": record.before, "remainder": record.remainder}
        for family, record in simulation.held_records.items()
    }
    reads = {
        f"{names[reading]} reads {names[read]} on axis {axis}": carry
        for (reading, read, axis), carry in simulation._pace_carry.items()
    }
    state = dict(simulation.snapshot_stream())
    # the engine lists a body's held stocks and the held families by the family's position in
    # the universe file; the reading names them, so that order is not in the digest
    state["measured"] = [
        {**body, "held": dict(zip(names, body["held"], strict=True))} for body in state["measured"]
    ]
    state["held_fields"] = {
        field["family"]: {key: value for key, value in field.items() if key != "family"}
        for field in state["held_fields"]
    }
    return {
        "lines": lines,
        "state": state,
        "records": records,
        "held families": held,
        "read remainders": reads,
        "clicks": simulation.layer.gathers,
        "books": simulation.books(),
    }


def digest_of(reading: dict[str, Any]) -> str:
    parts: list[bytes] = []
    canonical(reading, parts)
    return hashlib.sha256(b"".join(parts)).hexdigest()


def run(path: Path, intervals: int | None = None, write_to: Path | None = None) -> dict[str, Any]:
    """The world stepped `intervals` times (its recorded count, or the count this tool picks) and
    its digest, with the counts that name a difference when the digest moves; a world the law
    refuses on the way keeps its count and is recorded with the refusing step and the refusal's
    words, which the digest covers, so the replay refuses the same step the same way; a recorded
    world keeps its recorded count on every re-record, a new one gets the count this tool picks.
    With `write_to`, the entry is also written there as the world's own record file for CI's merge."""
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
    refused: str | None = None
    refused_at = 0
    try:
        while simulation.tick < intervals:
            simulation.step()
    except ValueError as refusal:
        refused, refused_at = str(refusal), simulation.tick + 1
    reading = run_reading(simulation, lines)
    if refused is not None:
        reading["refused"] = [refused_at, refused]
    entry: dict[str, Any] = {
        "stamp": stamp,
        "ticks": ticks,
        "intervals": intervals,
        "digest": digest_of(reading),
        "records": len(simulation.records),
        "clicks": len(simulation.layer.gathers),
        "lines": len(lines),
        "seconds": round(time.monotonic() - started, 2),
    }
    if refused is not None:
        entry["refused_at"], entry["refused"] = refused_at, refused
    if write_to is not None:
        key = path.resolve().relative_to(ROOT).as_posix()
        write_to.mkdir(parents=True, exist_ok=True)
        (write_to / (key.replace("/", "__") + ENTRY_SUFFIX)).write_text(
            json.dumps({key: {k: v for k, v in entry.items() if k != "seconds"}}), encoding="utf-8"
        )
    return entry


def write_record(worlds: dict[str, Any], recorded_at: str) -> None:
    """The record written once, sorted by world, with the commit it was recorded at."""
    RECORD.write_text(
        json.dumps(
            {"format": FORMAT, "recorded_at": recorded_at, "worlds": dict(sorted(worlds.items()))},
            indent=1,
        )
        + "\n",
        encoding="utf-8",
    )


def merge(folder: Path, recorded_at: str, every_world: bool = False) -> list[str]:
    """Every world's record file under `folder` (the shards' uploads, any depth) merged into the
    record: a named world replaced by its entry, every other world kept as recorded; the record
    is written only where a world's entry moved, so a record that replays as it stands keeps its
    commit and is not rewritten for the sha alone; the worlds merged, sorted. With `every_world`
    a recorded world with no entry refuses the merge by name (a cancelled or lost shard), since a
    record of the worlds that finished alone is no record."""
    recorded: dict[str, Any] = (
        json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.exists() else {"worlds": {}}
    )
    worlds: dict[str, Any] = dict(recorded.get("worlds", {}))
    merged: list[str] = []
    for file in sorted(folder.rglob("*" + ENTRY_SUFFIX)):
        for key, entry in json.loads(file.read_text(encoding="utf-8")).items():
            worlds[key] = entry
            merged.append(key)
    missing = sorted(set(recorded.get("worlds", {})) - set(merged))
    if every_world and missing:
        raise ValueError(f"no entry for {len(missing)} recorded worlds under {folder}: {missing}")
    if worlds != recorded.get("worlds", {}):
        write_record(worlds, recorded_at)
    return sorted(merged)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="record or merge the shipped worlds' regression digests"
    )
    parser.add_argument(
        "worlds", nargs="*", help="the world files to record; none for every shipped world"
    )
    parser.add_argument(
        "--merge", type=Path, metavar="FOLDER", help="merge the record files under FOLDER"
    )
    parser.add_argument(
        "--recorded-at", metavar="SHA", help="the commit written into the record; HEAD's"
    )
    parser.add_argument(
        "--every-world", action="store_true", help="refuse a merge missing a recorded world's entry"
    )
    args = parser.parse_args(argv)
    recorded_at = (
        args.recorded_at
        or subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True
        ).stdout.strip()
    )
    if args.merge is not None:
        try:
            merged = merge(args.merge, recorded_at, args.every_world)
        except ValueError as refusal:
            print("the merge is refused:", refusal)
            return 1
        print("merged", len(merged), "worlds at", recorded_at, "into", RECORD.relative_to(ROOT))
        return 0
    paths = [Path(n).resolve() for n in args.worlds] if args.worlds else shipped_worlds()
    recorded: dict[str, Any] = (
        json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.exists() else {"worlds": {}}
    )
    worlds: dict[str, Any] = dict(recorded.get("worlds", {}))
    for path in paths:
        key = path.relative_to(ROOT).as_posix()
        entry = run(path, worlds.get(key, {}).get("intervals"))
        entry.pop("seconds")
        worlds[key] = entry
        print(key, json.dumps(entry))
    write_record(worlds, recorded_at)
    print("recorded", len(worlds), "worlds at", recorded_at, "into", RECORD.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
