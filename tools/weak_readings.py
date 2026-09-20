"""The readings of series J, "the weak force" (docs/EXPERIMENTS.md, "J, the
weak force"; examples/events/weak/make_worlds.py; the model owner,
2026-09-20, "go on everything": the neutrino first, series J2).

Reads the run folders of the worlds (the runner's `run.json`,
`initialization.json` and `events.jsonl`, told apart by the `model` of the
record, `beam-weak-<name>-v1`) and prints, per world, two kinds of number,
each line labelled (the model owner, 2026-09-20: "in reality there is no
such thing" about the host's readings of the GameBoard):

- DETECTOR readings, the only kind reality has: a reader's clicks and its
  passes (its own records: the `events` of its state, its `pass` lines),
  the far detector's clicks;
- GAMEBOARD readings, the host's view of the mechanism: the expectation
  computed from the engine's flight table (the rays born early enough to
  reach a distance within the run), the source's stride.

J2, the neutrino's passage through a filled bar: the expectation, written
before the runs (README.md, docs/EXPERIMENTS.md): a window of width 1 takes
exactly 1 / 64 of a stride-1 source's arrivals and nothing behind it takes
anything (a filter, not an attenuation); a ladder of centres exhausts the
beam after 64 readers; the default width takes the half circle; a stride
of 2 gives 1 / 32 at the centre 0 and nothing at the centre 1 (the coset
missed). The record checks (completed, the books balanced at every tick)
fail the tool; the readings are registered inside or outside their
expectation and never moved.

    PYTHONPATH=src python tools/weak_readings.py artifacts/weak
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

import numpy as np

from event_universe.events.nature_beam import flight_table

MODEL_PREFIX = "beam-weak-"
MODEL_SUFFIX = "-v1"
Kind = str
GAMEBOARD: Kind = "GAMEBOARD"
DETECTOR: Kind = "DETECTOR"
ORDER = ("j2_filter", "j2_ladder", "j2_default", "j2_stride2", "j2_stride2_odd")


@dataclass
class Thing:
    """A measured event of the world: its number, family, position and,
    per family name, the units it clicked (its state's `events`) and the
    rays that passed it (its `pass` lines)."""

    number: int
    family: str
    position: tuple[int, int, int]
    clicks: dict[str, int] = field(default_factory=dict)
    passes: dict[str, int] = field(default_factory=dict)

    def arrivals(self, family: str) -> int:
        """The rays of a family that arrived at the thing over the run: what
        it clicked and what passed it (DETECTOR: its own records)."""
        return self.clicks.get(family, 0) + self.passes.get(family, 0)


@dataclass
class Reading:
    name: str
    ticks: int
    completed: bool
    balanced: bool
    elapsed: float
    shape: tuple[int, int, int]
    phase_steps: int
    stride: int
    things: list[Thing] = field(default_factory=list)

    def of_family(self, family: str) -> list[Thing]:
        return [thing for thing in self.things if thing.family == family]


def first_arrival_age(distance: int) -> int:
    """The age at which a heading ray first reaches `distance` Links, off
    the engine's flight table (GAMEBOARD: the expectation's computation)."""
    table = flight_table(((0, 0, 0), (0, 0, 0), (1, 0, 0)))
    ages = np.arange(1, 4 * distance + 64, dtype=np.int64)
    steps = table.manhattan_steps(np.full(ages.shape, 2, dtype=np.int64), ages)
    return int(ages[np.flatnonzero(steps >= distance)[0]])


def stride_of(world: dict[str, object], source: dict[str, object]) -> int:
    """The source's stride over the circle: its turn per self-creation, the
    whole part of content x n / d at the clock's rate [n, d] (an integer K
    is [1, K])."""
    clock = world["K"]
    if isinstance(clock, list):
        numerator, denominator = int(str(clock[0])), int(str(clock[1]))
    else:
        numerator, denominator = 1, int(str(clock))
    return int(str(source["amount"])) * numerator // denominator


def read_run(folder: Path) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    model = str(record["model"])
    world = json.loads((folder / "initialization.json").read_text(encoding="utf-8"))
    names = [str(f["name"]) for f in world["families"]]
    shape = tuple(int(v) for v in world["shape"])
    reading = Reading(
        name=model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)],
        ticks=int(record["completed_ticks"]),
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        elapsed=float(record["elapsed_seconds"]),
        shape=(shape[0], shape[1], shape[2]),
        phase_steps=int(world.get("N", 64)),
        stride=stride_of(world, world["measured"][0]),
    )
    for index, declared in enumerate(world["measured"]):
        position = tuple(int(v) for v in declared["position"])
        reading.things.append(
            Thing(index + 1, str(declared["family"]), (position[0], position[1], position[2]))
        )
    by_number = {thing.number: thing for thing in reading.things}
    for state in record["measured"]:
        thing = by_number[int(state["number"])]
        thing.clicks = {name: int(units) for name, units in zip(names, state["events"], strict=True)}
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for text in stream:
            if '"pass"' not in text:
                continue
            event = json.loads(text)
            if event["event"] != "pass" or event.get("measured") is None:
                continue
            thing = by_number[int(event["measured"])]
            family = str(event["family"])
            thing.passes[family] = thing.passes.get(family, 0) + 1
    return reading


def find_runs(root: Path) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        model = str(record.get("model", ""))
        if model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX):
            found.append(read_run(path.parent))
    return sorted(found, key=lambda r: (ORDER.index(r.name) if r.name in ORDER else len(ORDER), r.name))


def expectations(reading: Reading) -> list[tuple[str, bool, Kind]]:
    """The criteria of each world against its expectation, written before
    the runs (README.md): (label, inside, the kind of the reading). The
    expected far counts are the rays born at the ticks 1 .. ticks - a_far
    (a_far the first-arrival age off the flight table) whose phase no
    reader on the way admits (GAMEBOARD: the expectation's computation)."""
    found: list[tuple[str, bool, Kind]] = []
    if not reading.name.startswith("j2"):
        return found
    readers = [thing for thing in reading.of_family("d") if thing.position[0] < reading.shape[0] - 10]
    far = [thing for thing in reading.of_family("d") if thing.position[0] >= reading.shape[0] - 10][-1]
    first = readers[0]
    fraction = (
        Fraction(first.clicks.get("nu", 0), first.arrivals("nu")) if first.arrivals("nu") else None
    )
    behind = [thing for thing in readers[1:] if thing.clicks.get("nu", 0)]
    born_far = reading.ticks - first_arrival_age(far.position[0])
    modulus = reading.phase_steps
    stride = reading.stride
    phases = [(stride * (t - 1)) % modulus for t in range(1, born_far + 1)]
    if reading.name == "j2_filter":
        found.append(
            (
                "the first reader takes exactly 1 / 64 of its arrivals",
                fraction == Fraction(1, 64),
                DETECTOR,
            )
        )
        found.append(("the 127 readers behind it take nothing", not behind, DETECTOR))
        found.append(
            (
                f"the far detector reads the {modulus - 1} / {modulus} of the rays that reach it",
                far.clicks.get("nu", 0) == sum(1 for p in phases if p != 0),
                DETECTOR,
            )
        )
    elif reading.name == "j2_ladder":
        taking = [thing for thing in readers if thing.clicks.get("nu", 0)]
        found.append(
            (
                "the readers at x = 8 .. 71 each take their residue and the rest take nothing",
                [thing.position[0] for thing in taking] == list(range(8, 72)),
                DETECTOR,
            )
        )
        found.append(("the far detector reads 0", far.clicks.get("nu", 0) == 0, DETECTOR))
    elif reading.name == "j2_default":
        found.append(
            (
                "the first reader takes the half circle, 1 / 2 of its arrivals",
                fraction == Fraction(1, 2),
                DETECTOR,
            )
        )
        found.append(("the readers behind it take nothing", not behind, DETECTOR))
        found.append(
            (
                "the far detector reads the other half",
                far.clicks.get("nu", 0) == sum(1 for p in phases if 16 <= p < 48),
                DETECTOR,
            )
        )
    elif reading.name == "j2_stride2":
        found.append(
            (
                "the first reader takes 1 / 32 of its arrivals (the even coset)",
                fraction == Fraction(1, 32),
                DETECTOR,
            )
        )
        found.append(("the readers behind it take nothing", not behind, DETECTOR))
        found.append(
            (
                "the far detector reads 31 / 32 of the rays that reach it",
                far.clicks.get("nu", 0) == sum(1 for p in phases if p != 0),
                DETECTOR,
            )
        )
    elif reading.name == "j2_stride2_odd":
        found.append(("no reader clicks (the coset missed)", fraction == 0 and not behind, DETECTOR))
        found.append(
            (
                "the far detector reads every ray that reaches it",
                far.clicks.get("nu", 0) == born_far,
                DETECTOR,
            )
        )
    return found


def print_world(reading: Reading) -> list[tuple[str, bool, Kind]]:
    """Print the readings of one world and return its criteria."""
    print(
        f"[{GAMEBOARD}] world `{reading.name}`: the bar {reading.shape[0]} x {reading.shape[1]} x "
        f"{reading.shape[2]}, N {reading.phase_steps}, the source's stride {reading.stride}; "
        f"{reading.ticks} intervals in {reading.elapsed:.1f} s"
    )
    readers = [thing for thing in reading.of_family("d") if thing.position[0] < reading.shape[0] - 10]
    far = [thing for thing in reading.of_family("d") if thing.position[0] >= reading.shape[0] - 10]
    if readers:
        first = readers[0]
        print(
            f"[{DETECTOR}]   the first reader (x = {first.position[0]}): {first.clicks.get('nu', 0)} clicks of "
            f"{first.arrivals('nu')} arrivals"
        )
        taking = [
            (thing.position[0], thing.clicks.get("nu", 0))
            for thing in readers
            if thing.clicks.get("nu", 0)
        ]
        print(
            f"[{DETECTOR}]   readers that clicked: {len(taking)} of {len(readers)}; the first ten {taking[:10]}"
        )
    for thing in far:
        born = reading.ticks - first_arrival_age(thing.position[0])
        print(
            f"[{DETECTOR}]   the far detector (x = {thing.position[0]}): {thing.clicks.get('nu', 0)} clicks; "
            f"[{GAMEBOARD}] {born} rays reach its distance within the run (the first-arrival age "
            f"{first_arrival_age(thing.position[0])} off the flight table)"
        )
    criteria = expectations(reading)
    for label, ok, kind in criteria:
        print(f"[{kind}]   {label}: {'inside' if ok else 'outside'}")
    print()
    return criteria


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="the folder holding the run folders")
    args = parser.parse_args(argv)
    readings = find_runs(args.root)
    if not readings:
        print(f"no weak-force run under {args.root}", file=sys.stderr)
        return 2
    failed = 0
    for r in readings:
        for label, ok in (("completed", r.completed), ("balanced", r.balanced)):
            print(f"{'PASS' if ok else 'FAIL'} {r.name}: {label} ({r.elapsed:.1f} s, {r.ticks} ticks)")
            failed += not ok
    print()
    print(
        f"every line below is labelled [{GAMEBOARD}] (the host's view of the GameBoard: the expectation "
        f"from the flight table, the stride; exists for us, not in reality) or [{DETECTOR}] (a measured "
        "event's own records: the only kind reality has)"
    )
    print()
    criteria: list[tuple[str, bool, Kind]] = []
    for r in readings:
        criteria += print_world(r)
    inside = sum(1 for _, ok, _ in criteria if ok)
    print(
        f"{failed} record check(s) failed; {inside} reading(s) inside, {len(criteria) - inside} outside"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
