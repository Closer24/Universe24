"""Read the runner's records of series R, the quarks (`examples/events/quarks/`),
and compare them with the register's pins (`expectations.json`, derived by
`docs/designs/quarks/quark_numbers.py`; the design QUARKS.md section 4.7).

Every line is labelled DETECTOR (the bodies' own `read` and `contact`
records, the border's clicks, the content the bodies hold: the only kind
reality has) or GAMEBOARD (the bodies' steps, positions and separations:
the host's view of the mechanism). A pin outside is reported with its
numbers and never moved.

    PYTHONPATH=src python tools/quarks_readings.py artifacts/quarks
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples" / "events" / "quarks"
Vector = tuple[int, int, int]
DETECTOR = "DETECTOR"
GAMEBOARD = "GAMEBOARD"
GLUE = "glue"
LIFETIME_BORDER = "lifetime"
# The tick at which the border's rows per interval are read: the glue rows
# click at the age 3, from tick 4 on, and every line of the fan within the
# reach has arrived by tick 20 (series I's reference tick).
BORDER_TICK = 20


def add(a: Vector, b: Vector) -> Vector:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vector(v: Vector) -> str:
    return "(" + ", ".join(f"{c:,}" for c in v) + ")"


@dataclass
class Body:
    number: int
    family: str
    start: Vector
    push: Vector = (0, 0, 0)
    steps: int = 0
    first_step: int | None = None
    final: Vector = (0, 0, 0)
    contacts: int = 0
    first_contact: int | None = None
    largest_handed: int = 0
    left_through: str | None = None


@dataclass
class Reading:
    world: str
    ticks: int
    bodies: dict[int, Body]
    border_rows_at_border_tick: int = 0
    border_families: set[str] = field(default_factory=set)
    read_mass: int = 0
    conserved: bool = True
    largest_spread: float = 0.0
    final_spread: float = 0.0


def read_run(folder: Path, push_tick: int) -> Reading:
    """The record of one world: the pushes at `push_tick` per body, the
    hand-overs, the steps, the border's rows at that tick, the bodies'
    content at the end and the largest separation over the run."""
    run = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    state = json.loads((folder / "state.json").read_text(encoding="utf-8"))
    world = json.loads((folder / "initialization.json").read_text(encoding="utf-8"))
    bodies: dict[int, Body] = {}
    for number, m in enumerate(world["measured"], start=1):
        pos = tuple(int(c) for c in m["position"])
        bodies[number] = Body(
            number, str(m["family"]), (pos[0], pos[1], pos[2]), final=(pos[0], pos[1], pos[2])
        )
    reading = Reading(str(run.get("model_id", folder.name)), int(run.get("completed_ticks", 0)), bodies)
    positions = {n: b.start for n, b in bodies.items()}
    spread = spread_of(positions)
    reading.largest_spread = spread
    border_rows = 0
    with (folder / "events.jsonl").open(encoding="utf-8") as events:
        for line in events:
            event = json.loads(line)
            kind = event["event"]
            tick = int(event["tick"])
            if kind == "read":
                body = bodies.get(int(event["measured"]))
                if body is not None and tick == push_tick:
                    body.push = add(body.push, tuple(event["push"]))  # type: ignore[arg-type]
            elif kind == "contact":
                occupant = int(event["occupant"])
                body = bodies.get(occupant)
                if body is not None:
                    body.contacts += 1
                    if body.first_contact is None:
                        body.first_contact = tick
                    body.largest_handed = max(body.largest_handed, abs(int(event["component"])))
            elif kind == "step":
                body = bodies[int(event["number"])]
                to = tuple(int(c) for c in event["to"])
                body.steps += 1
                if body.first_step is None:
                    body.first_step = tick
                body.final = (to[0], to[1], to[2])
                positions[body.number] = body.final
                reading.largest_spread = max(reading.largest_spread, spread_of(positions))
            elif kind == "click" and event.get("measured") is None:
                if str(event.get("detector")) == LIFETIME_BORDER:
                    reading.border_families.add(str(event.get("family")))
                    if tick == BORDER_TICK:
                        border_rows += 1
    reading.border_rows_at_border_tick = border_rows
    reading.final_spread = spread_of(positions)
    for body in bodies.values():
        edge = [c for c in body.final if c <= 0 or c >= 20]
        if body.steps and edge:
            body.left_through = "the face at " + str(body.final)
    # The content a detector reads of the set: what the bodies on the
    # GameBoard hold at the end, plus what left with a body through a face
    # (booked on that face's `measured_content` per family; the state drops
    # a body that left).
    for entry in state["measured"]:
        held = entry.get("held", [])
        reading.read_mass += (
            sum(int(h) for h in held) if isinstance(held, list) else int(entry.get("amount", 0))
        )
    for detector in run.get("detectors", []):
        if str(detector.get("name", "")).startswith("face:"):
            for family in detector.get("families", {}).values():
                reading.read_mass += int(family.get("measured_content", 0))
    reading.conserved = bool(run.get("conserved_at_every_completed_tick", False))
    return reading


def spread_of(positions: dict[int, Vector]) -> float:
    numbers = list(positions)
    if len(numbers) < 2:
        return 0.0
    return max(
        math.dist(positions[a], positions[b]) for i, a in enumerate(numbers) for b in numbers[i + 1 :]
    )


def expectations(reading: Reading, pinned: dict[str, object]) -> list[tuple[str, bool, str]]:
    """Each pin of the register against the reading: (what, inside, the numbers)."""
    out: list[tuple[str, bool, str]] = []
    pushes = pinned["pushes"]
    assert isinstance(pushes, dict)
    push_tick = int(pinned["push_tick"])  # type: ignore[arg-type]
    for number, body in reading.bodies.items():
        expected = tuple(pushes[str(number)])
        measured = body.push
        gap = max(abs(a - b) for a, b in zip(expected, measured, strict=True))
        inside = gap <= 1
        out.append(
            (
                f"[{DETECTOR}] body {number} ({body.family}): the push per interval at tick {push_tick}",
                inside,
                f"expected {vector(expected)}, measured {vector(measured)}"
                + ("" if gap == 0 else f" (the accumulator's unit: {gap})"),
            )
        )
    rows = int(pinned["border_rows_per_interval"])  # type: ignore[arg-type]
    out.append(
        (
            f"[{DETECTOR}] the border `{LIFETIME_BORDER}` at tick {BORDER_TICK}",
            reading.border_rows_at_border_tick == rows and reading.border_families <= {GLUE},
            f"expected {rows} glue rows and no other family, measured {reading.border_rows_at_border_tick} "
            f"of {sorted(reading.border_families)}",
        )
    )
    mass = int(pinned["read_mass"])  # type: ignore[arg-type]
    out.append(
        (
            f"[{DETECTOR}] the read mass (the content the bodies hold at {reading.ticks}, with what left through a face)",
            reading.read_mass == mass,
            f"expected {mass}, measured {reading.read_mass}",
        )
    )
    fate = pinned["fate"]
    assert isinstance(fate, dict)
    holds = bool(fate["holds"])
    steps = sum(b.steps for b in reading.bodies.values())
    first = min(
        (b.first_step for b in reading.bodies.values() if b.first_step is not None), default=None
    )
    if holds:
        out.append(
            (
                f"[{GAMEBOARD}] the set holds: no step in {reading.ticks} intervals",
                steps == 0,
                f"steps {steps}, the first at {first}, the largest separation {reading.largest_spread:.2f}, "
                f"the final {reading.final_spread:.2f}",
            )
        )
    else:
        out.append(
            (
                f"[{GAMEBOARD}] the set does not hold: a step, the bodies beyond three Links",
                steps > 0 and reading.largest_spread > 3,
                f"steps {steps}, the first at {first}, the largest separation {reading.largest_spread:.2f}, "
                f"the final {reading.final_spread:.2f}; the toy's first step {fate.get('toy_first_step', fate.get('engine_first_step'))}",
            )
        )
    out.append(
        (
            f"[{DETECTOR}] the books",
            reading.conserved,
            "balanced at every tick" if reading.conserved else "NOT balanced",
        )
    )
    return out


def report(out_dir: Path) -> int:
    register = json.loads((WORLDS / "expectations.json").read_text(encoding="utf-8"))
    failed = 0
    inside = outside = 0
    for name, pinned in register["worlds"].items():
        folder = out_dir / name / "run"
        if not ((folder / "events.jsonl").exists() and (folder / "run.json").exists()):
            print(f"== {name}: no record under {folder}")
            failed += 1
            continue
        reading = read_run(folder, int(pinned["push_tick"]))
        print(f"== {name} ({reading.ticks} intervals)")
        for body in reading.bodies.values():
            print(
                f"   [{DETECTOR}] body {body.number} ({body.family} at {body.start}): {body.contacts} hand-overs"
                f" from tick {body.first_contact}, the largest {body.largest_handed:,}"
            )
            print(
                f"   [{GAMEBOARD}] body {body.number}: {body.steps} steps, the first at {body.first_step}, "
                f"final {body.final}"
            )
        for what, ok, numbers in expectations(reading, pinned):
            verdict = "inside" if ok else "OUTSIDE"
            inside += ok
            outside += not ok
            print(f"   {what}: {numbers} -> {verdict}")
    print(f"{failed} record checks failed, {inside} readings inside, {outside} outside, nothing moved")
    return 1 if failed else 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("out_dir", type=Path)
    args = parser.parse_args()
    sys.exit(report(args.out_dir))


if __name__ == "__main__":
    main()
