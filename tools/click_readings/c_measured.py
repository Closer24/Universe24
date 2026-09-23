"""The readings of series Q, "c measured behind a detector"
(docs/EXPERIMENTS.md, "Q, c measured behind a detector (2026-09-21)";
examples/events/c_measured/make_world.py; the model owner's "go for it" of
2026-09-21, record 236).

Reads the run folder of the world (the runner's `run.json`,
`initialization.json` and `events.jsonl`) and the register written before
the run (`expectations.json` beside the world: every direction's escape
from the closed form of the flight, docs/DERIVATIONS_BEAM.md section 11.1)
and prints, row by row, the derive-and-compare: every escape click of the
faces (DETECTOR: the only kind of reading reality has; the click's tick,
the Node it left from and the face) against the derived tick, Node and
face of its direction (FORMULA: the closed form's integer, written before
the run), the click's direction read off the engine's own label table
(`nature_beam_tables(...).flight.labels`, the momentum on the click record
being the unit vector of the direction at the scale Q; the tool replays no
rule of the engine), the Euclidean pace of every escape |x_k - x_0|_2 /
tau (x_k the click's Node plus the face's unit step, tau the click's tick
less the birth's) with its minimum, maximum and mean over the fan and per
class (the axes, the face diagonals, the body diagonals, the rest), against
the derived ones and against c = 1 / sqrt 3. A differing row is printed
with its direction; the tool exits 1 on any difference or on a record that
did not complete with the books balanced. Nothing is moved.

    PYTHONPATH=src python tools/click_readings/c_measured.py artifacts/c_measured/run \\
        [--expectations examples/events/c_measured/expectations.json]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from event_universe.events import parse_nature_beam_world
from event_universe.events.nature_beam import nature_beam_tables
from event_universe.world_loading import world_of_run

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EXPECTATIONS = ROOT / "examples" / "events" / "c_measured" / "expectations.json"
FORMAT = "c-measured-expectations-v1"
DETECTOR = "DETECTOR"
FORMULA = "FORMULA"
CLASSES = ("axes", "face_diagonals", "body_diagonals", "rest")
FACE_STEPS = {
    "face:+x": (1, 0, 0),
    "face:-x": (-1, 0, 0),
    "face:+y": (0, 1, 0),
    "face:-y": (0, -1, 0),
    "face:+z": (0, 0, 1),
    "face:-z": (0, 0, -1),
}
Vector = tuple[int, int, int]
Json = dict[str, Any]


@dataclass
class Escape:
    """One escape click read off the record, beside its derived row."""

    direction: Vector
    tick: int
    node: list[int]
    face: str
    derived: Json
    birth_tick: int

    @property
    def age(self) -> int:
        return self.tick - self.birth_tick

    @property
    def pace(self) -> float:
        step = FACE_STEPS[self.face]
        centre: list[int] = self.derived["centre"]
        displacement = [n + s - c for n, s, c in zip(self.node, step, centre, strict=True)]
        return math.sqrt(sum(d * d for d in displacement)) / self.age

    @property
    def equal(self) -> bool:
        return (
            self.tick == self.derived["tick"]
            and self.age == self.derived["age"]
            and self.node == self.derived["node"]
            and self.face == self.derived["face"]
        )


@dataclass
class Reading:
    """The record of one run of the world against the register."""

    folder: Path
    status: str
    completed_ticks: int
    elapsed_seconds: float
    fingerprint: str
    balanced: bool
    births: list[int]
    gathers: int
    escapes: list[Escape] = field(default_factory=list)
    unmatched: int = 0

    @property
    def clicks(self) -> int:
        return len(self.escapes) + self.unmatched

    @property
    def differing(self) -> list[Escape]:
        return [escape for escape in self.escapes if not escape.equal]

    def directions_seen(self) -> set[Vector]:
        return {escape.direction for escape in self.escapes}


def summary(values: list[float]) -> Json:
    return {
        "min": round(min(values), 6),
        "max": round(max(values), 6),
        "mean": round(sum(values) / len(values), 6),
    }


def load_expectations(path: Path) -> Json:
    register: Json = json.loads(path.read_text(encoding="utf-8"))
    if register.get("format") != FORMAT:
        raise ValueError(f"{path}: not a {FORMAT} register")
    return register


def read_run(folder: Path, register: Json) -> Reading:
    """The escapes of a run folder against the register: every click line
    of a face matched to its direction by the engine's label table."""
    run = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    world = world_of_run(folder)
    parsed = parse_nature_beam_world(world)
    flight = nature_beam_tables(parsed).flight
    by_label: dict[Vector, Vector] = {}
    for index, vector in enumerate(parsed.directions):
        label = (
            int(flight.labels[index, 0]),
            int(flight.labels[index, 1]),
            int(flight.labels[index, 2]),
        )
        by_label.setdefault(label, (int(vector[0]), int(vector[1]), int(vector[2])))
    rows: list[Json] = register["directions"]
    derived: dict[Vector, Json] = {}
    for row in rows:
        a, b, c = (int(v) for v in row["direction"])
        derived[(a, b, c)] = {**row, "centre": register["centre"]}
    births: list[int] = []
    clicks: list[Json] = []
    gathers = 0
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for text in stream:
            line = json.loads(text)
            if line.get("event") == "birth":
                births.append(int(line["tick"]))
            elif line.get("event") == "click":
                clicks.append(line)
            elif line.get("event") == "gather":
                gathers += 1
    # The books: the runner's flag over every completed interval and the
    # per-interval `audit` lines it summarises.
    audit = run.get("audit") or []
    balanced = bool(run.get("conserved_at_every_completed_tick", False)) and all(
        bool(line.get("balanced", False)) for line in audit
    )
    reading = Reading(
        folder=folder,
        status=str(run.get("status")),
        completed_ticks=int(run.get("completed_ticks", 0)),
        elapsed_seconds=float(run.get("elapsed_seconds", 0.0)),
        fingerprint=str(run.get("source_sha256", "")),
        balanced=balanced,
        births=births,
        gathers=gathers,
    )
    birth_tick = births[0] if births else int(register["birth_tick"])
    for click in clicks:
        if not str(click["detector"]).startswith("face:"):
            reading.unmatched += 1
            continue
        px, py, pz = (int(v) for v in click["momentum"])
        direction = by_label.get((px, py, pz))
        if direction is None or direction not in derived:
            reading.unmatched += 1
            continue
        reading.escapes.append(
            Escape(
                direction=direction,
                tick=int(click["tick"]),
                node=[int(v) for v in click["node"]],
                face=str(click["detector"]),
                derived=derived[direction],
                birth_tick=birth_tick,
            )
        )
    return reading


def report(reading: Reading, register: Json) -> list[str]:
    """The lines of the comparison, every number labelled by its kind."""
    lines = [
        f"{reading.folder}: {reading.status}, {reading.completed_ticks} intervals, "
        f"{reading.elapsed_seconds:.2f} s, the source fingerprint {reading.fingerprint[:12]}, "
        f"the books {'balanced' if reading.balanced else 'NOT balanced'}",
        f"FORMULA: Q {register['Q']}, the fan {register['fan']} directions, the half-width "
        f"{register['half_width']}, the birth at tick {register['birth_tick']}, "
        f"{register['clicks']} escapes derived, the last at tick {register['last_tick']}",
        f"DETECTOR: births {reading.births} (the record's), gathers {reading.gathers}, "
        f"clicks {reading.clicks} on the faces, {len(reading.escapes)} matched to a direction of "
        f"the fan, {len(reading.directions_seen())} directions seen, "
        f"{len(reading.escapes) - len(reading.differing)} of {len(reading.escapes)} at the "
        f"derived tick, Node and face",
    ]
    for escape in reading.differing:
        lines.append(
            f"  DIFFERS {escape.direction}: the click at tick {escape.tick} (age {escape.age}) "
            f"at {escape.node} on {escape.face}; derived tick {escape.derived['tick']} "
            f"(age {escape.derived['age']}) at {escape.derived['node']} on {escape.derived['face']}"
        )
    classes: Json = register["classes"]
    lines.append(
        "class | count | ages (DETECTOR) | ages (FORMULA) | pace min / max / mean (DETECTOR) | "
        "pace min / max / mean (FORMULA)"
    )
    for name in CLASSES:
        members = [escape for escape in reading.escapes if escape.derived["class"] == name]
        pinned: Json = classes[name]
        pinned_pace: Json = pinned["pace"]
        if members:
            measured = summary([escape.pace for escape in members])
            ages = sorted({escape.age for escape in members})
            lines.append(
                f"{name} | {len(members)} of {pinned['count']} | {ages} | {pinned['ages']} | "
                f"{measured['min']} / {measured['max']} / {measured['mean']} | "
                f"{pinned_pace['min']} / {pinned_pace['max']} / {pinned_pace['mean']}"
            )
        else:
            lines.append(f"{name} | 0 of {pinned['count']} | [] | {pinned['ages']} | none | none")
    pinned_total: Json = register["pace"]
    asymptotic: Json = register["asymptotic_pace"]
    if reading.escapes:
        measured_total = summary([escape.pace for escape in reading.escapes])
        lines.append(
            f"DETECTOR: the pace over the fan min {measured_total['min']} max "
            f"{measured_total['max']} mean {measured_total['mean']} Links per interval; FORMULA "
            f"min {pinned_total['min']} max {pinned_total['max']} mean {pinned_total['mean']}; "
            f"the asymptotic pace Q |D| / T_D over the fan min {asymptotic['min']} max "
            f"{asymptotic['max']} mean {asymptotic['mean']}; c = 1 / sqrt 3 = {register['c']}"
        )
    return lines


def verdict(reading: Reading, register: Json) -> bool:
    """Inside: the record completed and balanced, the births and the clicks
    as registered, every direction seen, every click at its derived tick,
    Node and face, none unmatched."""
    return (
        reading.status == "completed"
        and reading.balanced
        and len(reading.births) == register["births"]
        and reading.births[0] == register["birth_tick"]
        and reading.clicks == register["clicks"]
        and reading.unmatched == 0
        and len(reading.directions_seen()) == register["fan"]
        and not reading.differing
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("run", type=Path, help="the run folder (run.json, events.jsonl)")
    parser.add_argument("--expectations", type=Path, default=DEFAULT_EXPECTATIONS)
    args = parser.parse_args(argv)
    register = load_expectations(args.expectations)
    reading = read_run(args.run, register)
    for line in report(reading, register):
        print(line)
    inside = verdict(reading, register)
    print("VERDICT:", "inside (every click at its derived tick)" if inside else "OUTSIDE")
    return 0 if inside else 1


if __name__ == "__main__":
    sys.exit(main())
