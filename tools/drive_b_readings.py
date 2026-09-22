"""The readings of the drive-b series, the directional drive of a body
(`drive-b-v1`; `examples/events/drive_b/`), read from the runner's record and
compared with the pins of `expectations.json`, written before the runs.

Usage: `PYTHONPATH=src python tools/drive_b_readings.py <runs root>
[--register examples/events/drive_b/expectations.json]`. The root holds the
runs `tools/run_series.py` wrote (`<root>/<world>/run/`), told apart by the
model of their record (`beam-drive-b-<name>-v1`). Every line is one of two
kinds ([the register](../docs/EXPERIMENTS.md), "Two kinds of readings"):
DETECTOR, a detector's record (the body's click on a face: its tick, the
face, the Node it left from), or GAMEBOARD, the host's view (every `step`
line's Node against the line of the momentum, the `drive` accumulators
against the proved bound 3 W, `fast_steps`). The record checks (completed,
the books balanced at every tick) fail the tool; a reading outside its pin
is printed with its numbers and never moved. With `--register` the run
blocks (the source sha256, the digests of the record, the readings) are
written into the expectations file under `runs`, the pins untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTATIONS = ROOT / "examples" / "events" / "drive_b" / "expectations.json"
PREFIX = "beam-drive-b-"


@dataclass
class Reading:
    name: str
    folder: Path
    completed: bool
    balanced: bool
    ticks: int
    elapsed: float
    fingerprint: str
    hypotheses: list[str]
    fast_steps: int
    digests: dict[str, str]
    momentum: list[int]
    centre: list[int]
    clicks: list[dict[str, object]] = field(default_factory=list)
    steps: int = 0
    farthest: float = 0.0
    largest_drive: int = 0
    links: list[int] = field(default_factory=lambda: [0, 0, 0])


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_run(folder: Path) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    model = str(record["model"])
    body = record["measured"][0] if record["measured"] else None
    state = json.loads((folder / "state.json").read_text(encoding="utf-8"))
    momentum = [int(c) for c in (body["momentum"] if body else state.get("momentum", [0, 0, 0]))]
    shape = [int(c) for c in record["shape"]]
    centre = [c // 2 for c in shape]
    reading = Reading(
        name=model[len(PREFIX) : -len("-v1")],
        folder=folder,
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        ticks=int(record["completed_ticks"]),
        elapsed=float(record["elapsed_seconds"]),
        fingerprint=str(record["source_sha256"]),
        hypotheses=list(record["hypotheses"]),
        fast_steps=int(record.get("fast_steps", 0)),
        digests={
            "state_sha256": digest(folder / "state.json"),
            "audit_sha256": hashlib.sha256(
                json.dumps(record.get("audit", [])).encode("utf-8")
            ).hexdigest(),
            "events_sha256": digest(folder / "events.jsonl"),
        },
        momentum=momentum,
        centre=centre,
    )
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for text in stream:
            if '"step"' not in text and '"click"' not in text:
                continue
            event = json.loads(text)
            if event["event"] == "click" and str(event.get("detector", "")).startswith("face:"):
                reading.clicks.append(event)
                reading.momentum = [int(c) for c in event["momentum"]]
            elif event["event"] == "step":
                reading.steps += 1
                momentum = [int(c) for c in event["momentum"]]
                norm = math.sqrt(sum(c * c for c in momentum)) or 1.0
                r = [int(event["to"][a]) - centre[a] for a in range(3)]
                along = sum(r[a] * momentum[a] for a in range(3)) / norm
                reading.farthest = max(
                    reading.farthest, math.sqrt(max(0.0, sum(c * c for c in r) - along * along))
                )
                reading.largest_drive = max(
                    reading.largest_drive, max(abs(int(d)) for d in event["drive"])
                )
                port = int(event["step_port"])
                reading.links[port // 2] += 1 if port % 2 == 0 else -1
    return reading


def find_runs(root: Path) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        if path.parent.name == "resolved_view":
            continue
        record = json.loads(path.read_text(encoding="utf-8"))
        if str(record.get("model", "")).startswith(PREFIX):
            found.append(read_run(path.parent))
    return found


def lines(reading: Reading, pin: dict[str, object]) -> tuple[list[str], int, int, int]:
    """The readings of one run against its pins: the lines, the record
    checks failed, the readings inside, the readings outside."""
    out: list[str] = []
    failed = inside = outside = 0
    out.append(
        f"{reading.name}: {reading.ticks} intervals, {reading.elapsed:.2f} s, {reading.hypotheses}"
    )
    if not reading.completed or not reading.balanced:
        failed += 1
        out.append("  RECORD CHECK FAILED: not completed or the books unbalanced")
    click = dict(pin["click"])  # type: ignore[arg-type]
    if len(reading.clicks) != 1:
        outside += 1
        out.append(f"  DETECTOR the click: {len(reading.clicks)} face clicks, expected one: OUTSIDE")
    else:
        event = reading.clicks[0]
        tick, face, node = int(event["tick"]), str(event["detector"]), [int(c) for c in event["node"]]
        ok = (
            abs(tick - int(click["tick"])) <= int(click["tolerance"])
            and face == click["face"]
            and node == list(click["node"])
        )
        inside += ok
        outside += not ok
        out.append(
            f"  DETECTOR the click: tick {tick} on {face} from {node}, the momentum {event['momentum']}: "
            f"pinned {click['tick']} +- {click['tolerance']} on {click['face']} from {list(click['node'])}: "
            f"{'inside' if ok else 'OUTSIDE'}"
        )
        links_ok = reading.links == list(click["links_before"])
        inside += links_ok
        outside += not links_ok
        out.append(
            f"  GAMEBOARD the Links before the escape {reading.links} against the pinned "
            f"{list(click['links_before'])}: {'inside' if links_ok else 'OUTSIDE'}"
        )
    if "line" in pin:
        line = dict(pin["line"])  # type: ignore[arg-type]
        ok = reading.farthest <= float(line["bound"]) + 1e-9
        inside += ok
        outside += not ok
        out.append(
            f"  GAMEBOARD the line: every step's Node within {reading.farthest:.3f} Link of the line of p "
            f"(the replay's {line['farthest']}, the bound {line['bound']}): {'inside' if ok else 'OUTSIDE'}"
        )
        acc = dict(pin["accumulators"])  # type: ignore[arg-type]
        ok = reading.largest_drive < int(acc["bound_proved"])
        inside += ok
        outside += not ok
        out.append(
            f"  GAMEBOARD the accumulators: the largest |drive_a| on a step line {reading.largest_drive} "
            f"(the replay's {acc['largest_replayed']}; proved below {acc['bound_proved']}, observed below "
            f"{acc['bound_observed']}): {'inside' if ok else 'OUTSIDE'}"
        )
        fast = dict(pin["fast_steps"])  # type: ignore[arg-type]
        if fast["value"] is not None:
            ok = reading.fast_steps == int(fast["value"])
            inside += ok
            outside += not ok
            out.append(
                f"  GAMEBOARD fast_steps {reading.fast_steps} against the pinned {fast['value']}: "
                f"{'inside' if ok else 'OUTSIDE'}"
            )
        else:
            out.append(f"  GAMEBOARD fast_steps {reading.fast_steps} (reported, not pinned)")
    return out, failed, inside, outside


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="The runs' root (tools/run_series.py --out)")
    parser.add_argument("--register", type=Path, help="Write the run blocks into this expectations file")
    parser.add_argument("--expectations", type=Path, default=EXPECTATIONS)
    args = parser.parse_args()
    expected = json.loads(args.expectations.read_text(encoding="utf-8"))
    runs = find_runs(args.root)
    if not runs:
        print(f"no drive-b runs under {args.root}", file=sys.stderr)
        return 2
    failed = inside = outside = 0
    blocks: dict[str, object] = {}
    for reading in runs:
        pin = expected["worlds"].get(reading.name)
        if pin is None:
            print(f"{reading.name}: no pin in {args.expectations}", file=sys.stderr)
            return 2
        out, f, i, o = lines(reading, pin)
        failed, inside, outside = failed + f, inside + i, outside + o
        print("\n".join(out))
        blocks[reading.name] = {
            "source_sha256": reading.fingerprint,
            "completed_ticks": reading.ticks,
            "elapsed_seconds": round(reading.elapsed, 3),
            "hypotheses": reading.hypotheses,
            "fast_steps": reading.fast_steps,
            **reading.digests,
            "click": reading.clicks[0] if len(reading.clicks) == 1 else None,
            "links_before": reading.links,
            "farthest_from_the_line": round(reading.farthest, 3),
            "largest_drive": reading.largest_drive,
            "readings": {"inside": i, "outside": o, "record_checks_failed": f},
        }
    print(f"{failed} record checks failed, {inside} readings inside, {outside} outside, nothing moved")
    if args.register:
        document = json.loads(args.register.read_text(encoding="utf-8"))
        document["runs"] = blocks
        args.register.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(f"registered {len(blocks)} runs in {args.register}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
