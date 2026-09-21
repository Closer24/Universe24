"""The readings of series J, "the weak force" (docs/EXPERIMENTS.md, "J, the
weak force"; examples/events/weak/make_worlds.py; the model owner,
2026-09-20, "go on everything": the neutrino first, series J2; the
transformation `become`, series J1 and J3).

Reads the run folders of the worlds (the runner's `run.json`,
`initialization.json` and `events.jsonl`, told apart by the `model` of the
record, `beam-weak-<name>-v1`) and prints, per world, two kinds of number,
each line labelled (the model owner, 2026-09-20: "in reality there is no
such thing" about the host's readings of the GameBoard):

- DETECTOR readings, the only kind reality has: a reader's clicks and its
  passes (its own records: the `events` of its state, its `pass` lines),
  the far detector's clicks (J2); the shell's beta clicks per interval
  (the decay curve read behind the detector), their contents (the
  spectrum) and their ages (the flight), the nucleons' own clocks (their
  `age` and `waited`) and their `contact` records (J1, J3);
- GAMEBOARD readings, the host's view of the mechanism: the expectation
  computed from the engine's flight rule (the rays born early enough to
  reach a distance within the run) or from the engine's own presence
  reading before the run (`expectations.json`), the source's stride, each
  measured event's `become` line (the tick its clock fired, the count it
  read), the bodies' steps.

The expectations, written before the runs (README.md, docs/EXPERIMENTS.md):
J2, a window of width 1 takes exactly 1 / 64 of a stride-1 source's
arrivals and nothing behind it takes anything (a filter, not an
attenuation); a ladder of centres exhausts the beam after 64 readers; the
default width takes the half circle; a stride of 2 gives 1 / 32 at the
centre 0 and nothing at the centre 1 (the coset missed). J1, every neutron
fires at the tick its steady count gives, at + floor(at x c / 2^20), or up
to three intervals before it (the crowd's build-up), never after; the
survival curve at the shell is a step (its 10th-to-90th-percentile width
over its median far below nature's ln 9 / ln 2 = 3.17 for a memoryless
decay); every beta click carries the content 3 (a line, not nature's
continuum). J3, the bound neutron fires at the tick its count at one Link
from the proton gives (later, not never: the design's `at x (1 + k)`), the
pair then two protons at one Link, bound (no step); with the `crowd` gate
it never fires; the free neutron at its key `at` exactly. The W world, the
neutron throws one W unit (a paid family of lifetime 1) at its key and the
proton one Link away measures it one interval later, holding it: its
content a neutron's and its charge 0, nothing on the border, the momentum
exchanged. The record checks
(completed, the books balanced at every tick) fail the tool; the readings
are registered inside or outside their expectation and never moved.

    PYTHONPATH=src python tools/weak_readings.py artifacts/weak [--expectations FILE]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

import numpy as np

from event_universe.events.nature_beam import direction_flight
from event_universe.world_loading import world_of_run

MODEL_PREFIX = "beam-weak-"
MODEL_SUFFIX = "-v1"
Kind = str
GAMEBOARD: Kind = "GAMEBOARD"
DETECTOR: Kind = "DETECTOR"
ORDER = (
    "j2_filter",
    "j2_ladder",
    "j2_default",
    "j2_stride2",
    "j2_stride2_odd",
    "j1_lattice",
    "j1_source",
    "j3_deuteron",
    "j3_deuteron_crowd",
    "j3_neutron_free",
    "w_exchange",
)
ROOT = Path(__file__).resolve().parents[1]
EXPECTATIONS = ROOT / "examples" / "events" / "weak" / "expectations.json"
# Nature's memoryless decay: the 10th-to-90th-percentile width of an
# exponential survival over its median, ln 9 / ln 2.
NATURE_WIDTH_OVER_MEDIAN = math.log(9) / math.log(2)
Criterion = tuple[str, bool, Kind]


@dataclass
class Thing:
    """A measured event of the world: its number, family, position and,
    per family name, the units it clicked (its state's `events`), the rays
    that passed it (its `pass` lines), its clock (`age`, `waited`), its
    steps (the record's `step` lines) and the steps it attempted (its
    state's `steps`, a refused step counted too: the difference is what it
    handed over), its hand-overs, the key `at` of its clock trigger as
    declared (None without) and its `become` line if it transformed."""

    number: int
    family: str
    position: tuple[int, int, int]
    clicks: dict[str, int] = field(default_factory=dict)
    passes: dict[str, int] = field(default_factory=dict)
    age: int = 0
    waited: int = 0
    steps: int = 0
    attempts: int = 0
    contacts: int = 0
    at: int | None = None
    become: dict[str, object] | None = None
    # Its state at the end: the content it holds, its charge as a pair and
    # its momentum; the ticks of its clicks per family (its `click` lines).
    content: int = 0
    charge: tuple[int, int] = (0, 1)
    momentum: tuple[int, int, int] = (0, 0, 0)
    click_ticks: dict[str, list[int]] = field(default_factory=dict)

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
    # The shell's beta clicks per tick, their contents and their ages (the
    # click record's `reading` under `reads: "age"`, the age moment of one
    # unit: its age).
    shell_clicks: dict[int, int] = field(default_factory=dict)
    shell_contents: dict[int, int] = field(default_factory=dict)
    shell_ages: list[int] = field(default_factory=list)
    # The border `lifetime`'s clicks per family (the record's detector).
    border_clicks: dict[str, int] = field(default_factory=dict)

    def of_family(self, family: str) -> list[Thing]:
        return [thing for thing in self.things if thing.family == family]

    def transformed(self) -> list[Thing]:
        return [thing for thing in self.things if thing.become is not None]


def first_arrival_age(distance: int) -> int:
    """The age at which a heading ray first reaches `distance` Links, off
    the engine's flight rule (GAMEBOARD: the expectation's computation)."""
    table = direction_flight(((0, 0, 0), (0, 0, 0), (1, 0, 0)))
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
    world = world_of_run(folder)
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
        thing.age, thing.waited, thing.attempts = (
            int(state["age"]),
            int(state["waited"]),
            int(state["steps"]),
        )
        thing.contacts = sum(int(v) for v in state["contacts"])
        declared = record["numbers"][str(thing.number)].get("become")
        if declared is not None:
            thing.at = int(declared["at"])
        thing.content = int(state["content"])
        thing.charge = (int(state["charge"][0]), int(state["charge"][1]))
        momentum = [int(v) for v in state["momentum"]]
        thing.momentum = (momentum[0], momentum[1], momentum[2])
    for detector in record["detectors"]:
        if detector["name"] == "lifetime":
            reading.border_clicks = {
                str(name): int(found["clicks"]) for name, found in detector["families"].items()
            }
    shell = {str(d["name"]) for d in world.get("detectors", [])}
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for text in stream:
            if (
                '"pass"' not in text
                and '"become"' not in text
                and '"click"' not in text
                and '"step"' not in text
            ):
                continue
            event = json.loads(text)
            kind = event["event"]
            if kind == "pass" and event.get("measured") is not None:
                thing = by_number[int(event["measured"])]
                family = str(event["family"])
                thing.passes[family] = thing.passes.get(family, 0) + 1
            elif kind == "become":
                by_number[int(event["measured"])].become = event
            elif kind == "step":
                # The `step` line names the body by `number` (no world of the
                # series stepped a body until the step drive of 2026-09-20).
                by_number[int(event["number"])].steps += 1
            elif kind == "click":
                if event.get("measured") is not None:
                    thing = by_number[int(event["measured"])]
                    thing.click_ticks.setdefault(str(event["family"]), []).append(int(event["tick"]))
                if event.get("detector") in shell and event["family"] == "beta":
                    tick = int(event["tick"])
                    reading.shell_clicks[tick] = reading.shell_clicks.get(tick, 0) + int(event["amount"])
                    content = int(event["content"])
                    reading.shell_contents[content] = reading.shell_contents.get(content, 0) + 1
                    reading.shell_ages.append(int(event["reading"]))
    return reading


def find_runs(root: Path) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        model = str(record.get("model", ""))
        if model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX):
            found.append(read_run(path.parent))
    return sorted(found, key=lambda r: (ORDER.index(r.name) if r.name in ORDER else len(ORDER), r.name))


def load_expectations(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    found: dict[str, object] = json.loads(path.read_text(encoding="utf-8"))
    return found


def percentile_tick(curve: dict[int, int], fraction: float) -> int:
    """The tick by which the given fraction of the curve's clicks arrived."""
    total = sum(curve.values())
    running = 0
    for tick in sorted(curve):
        running += curve[tick]
        if running >= fraction * total:
            return tick
    return max(curve) if curve else 0


def curve_shape(curve: dict[int, int]) -> tuple[int, int, int, float]:
    """The median tick, the 10th and the 90th percentile ticks of the
    shell's click curve and the 10-to-90 width over the median (0 without
    clicks)."""
    if not curve:
        return 0, 0, 0, 0.0
    median = percentile_tick(curve, 0.5)
    low, high = percentile_tick(curve, 0.1), percentile_tick(curve, 0.9)
    return median, low, high, (high - low) / median


def j2_expectations(reading: Reading) -> list[Criterion]:
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
    found: list[Criterion] = []
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


def become_expectations(reading: Reading, expected: dict[str, object]) -> list[Criterion]:
    """J1 and J3 against the expectations the generator pinned from the
    engine's own presence reading: the trigger ticks, the shell's curve, the
    spectrum, the pair's binding."""
    found: list[Criterion] = []
    neutrons = reading.of_family("n")
    fired = {thing.number: thing.become for thing in neutrons if thing.become is not None}
    if expected.get("never"):
        found.append(
            (
                f"no transformation in {reading.ticks} intervals (the count above the gate {expected['gate']})",
                not fired,
                GAMEBOARD,
            )
        )
        found.append(("no beta click at the shell", not reading.shell_clicks, DETECTOR))
        return found
    ticks = expected.get("ticks", {})
    slack = int(str(expected.get("slack", 0)))
    assert isinstance(ticks, dict)
    inside = all(
        number in fired
        and int(str(ticks[str(number)])) - slack
        <= int(str(fired[number]["triggered"]))
        <= int(str(ticks[str(number)]))
        for number in (thing.number for thing in neutrons)
    )
    found.append(
        (
            f"every neutron fires at its pinned tick or up to {slack} before it "
            f"({min(ticks.values())} .. {max(ticks.values())} pinned)",
            inside,
            GAMEBOARD,
        )
    )
    found.append(
        (
            "every beta click at the shell carries the content 3 (a line)",
            set(reading.shell_contents) == {3} and bool(reading.shell_contents),
            DETECTOR,
        )
    )
    if reading.name.startswith("j1"):
        found.append(
            (
                f"the shell's beta count is the neutrons' ({len(neutrons)})",
                sum(reading.shell_clicks.values()) == len(neutrons),
                DETECTOR,
            )
        )
        median, low, high, ratio = curve_shape(reading.shell_clicks)
        found.append(
            (
                f"the survival curve is a step: its 10-to-90 width over its median below 0.1 "
                f"(nature's memoryless decay {NATURE_WIDTH_OVER_MEDIAN:.2f})",
                bool(reading.shell_clicks) and ratio < 0.1,
                DETECTOR,
            )
        )
    if reading.name == "j3_deuteron":
        bodies = [thing for thing in reading.things if thing.family in ("p", "n")]
        found.append(
            (
                "the pair holds after the transformation (no step in the run; every "
                "attempted step refused, a hand-over)",
                all(b.steps == 0 for b in bodies),
                GAMEBOARD,
            )
        )
        found.append(("the beta reaches the shell", sum(reading.shell_clicks.values()) == 1, DETECTOR))
    if reading.name == "j3_neutron_free":
        keys = sorted({thing.at for thing in neutrons if thing.at is not None})
        found.append(
            (
                f"the free neutron fires at its key {keys} exactly (its clock counts nothing)",
                bool(keys) and [b["triggered"] for b in fired.values()] == keys,
                GAMEBOARD,
            )
        )
        found.append(("the beta reaches the shell", sum(reading.shell_clicks.values()) == 1, DETECTOR))
    return found


def w_expectations(reading: Reading, expected: dict[str, object]) -> list[Criterion]:
    """The W world against the generator's integers: the neutron's `become`
    at its key with one W unit on +x, the proton's click one Link and one
    interval later, its charge and content after (a neutron's in the
    detector's terms), nothing on the border, the momentum exchanged."""
    at = int(str(expected["at"]))
    click_tick = int(str(expected["click_tick"]))
    label = int(str(expected["label"]))
    content = int(str(expected["content"]))
    charge = expected["charge"]
    assert isinstance(charge, list)
    pair = (int(str(charge[0])), int(str(charge[1])))
    neutron, proton = reading.things[0], reading.things[1]
    become = neutron.become
    return [
        (
            f"the neutron becomes a proton at its key {at} and throws one W unit of content 3 on +x",
            become is not None
            and int(str(become["triggered"])) == at
            and become["products"] == [["w", 1, 3, [1, 0, 0]]],
            GAMEBOARD,
        ),
        (
            f"the proton takes the W at tick {click_tick} (one Link, the lifetime 1, one interval)",
            proton.click_ticks.get("w") == [click_tick] and proton.clicks.get("w") == 1,
            DETECTOR,
        ),
        (
            f"the proton's charge {list(pair)} and content {content} after: a neutron's",
            proton.charge == pair and proton.content == content,
            DETECTOR,
        ),
        ("no W on the border lifetime", reading.border_clicks.get("w", 0) == 0, DETECTOR),
        (
            f"the momentum exchanged: -{label} on the neutron become proton, +{label} on the proton",
            neutron.momentum == (-label, 0, 0) and proton.momentum == (label, 0, 0),
            GAMEBOARD,
        ),
    ]


def expectations(reading: Reading, pinned: dict[str, object] | None = None) -> list[Criterion]:
    """The criteria of each world against its expectation, written before
    the runs (README.md): (label, inside, the kind of the reading). The
    expected far counts of J2 are the rays born at the ticks 1 .. ticks -
    a_far (a_far the first-arrival age off the flight rule) whose phase no
    reader on the way admits; the expected trigger ticks of J1 and J3 are
    the generator's, from the engine's own presence reading."""
    if reading.name.startswith("j2"):
        return j2_expectations(reading)
    pinned = pinned or {}
    if reading.name.startswith("w_"):
        w_pinned = pinned.get("w", {})
        assert isinstance(w_pinned, dict)
        w_expected = w_pinned.get(reading.name)
        return w_expectations(reading, w_expected) if isinstance(w_expected, dict) else []
    become = pinned.get("become", {})
    assert isinstance(become, dict)
    expected = become.get(reading.name)
    if not isinstance(expected, dict):
        return []
    return become_expectations(reading, expected)


def print_world(reading: Reading, pinned: dict[str, object]) -> list[Criterion]:
    """Print the readings of one world and return its criteria."""
    print(
        f"[{GAMEBOARD}] world `{reading.name}`: the GameBoard {reading.shape[0]} x {reading.shape[1]} x "
        f"{reading.shape[2]}, N {reading.phase_steps}; {reading.ticks} intervals in {reading.elapsed:.1f} s"
    )
    if reading.name.startswith("j2"):
        print(f"[{GAMEBOARD}]   the source's stride {reading.stride}")
        readers = [
            thing for thing in reading.of_family("d") if thing.position[0] < reading.shape[0] - 10
        ]
        far = [thing for thing in reading.of_family("d") if thing.position[0] >= reading.shape[0] - 10]
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
                f"{first_arrival_age(thing.position[0])} off the flight rule)"
            )
    elif reading.name.startswith("w_"):
        for thing in reading.things:
            become = thing.become
            print(
                f"[{GAMEBOARD}]   number {thing.number} ({thing.family} as declared) at {thing.position}: "
                + (
                    f"`become` at tick {become['triggered']} into {become['into']} with the products "
                    f"{become['products']}, the recoil {become['recoil']}; "
                    if become is not None
                    else "no transformation; "
                )
                + f"the momentum {list(thing.momentum)}"
            )
            print(
                f"[{DETECTOR}]   number {thing.number}: the clicks {thing.clicks} at the ticks "
                f"{thing.click_ticks}; the content {thing.content}, the charge {list(thing.charge)}"
            )
        print(f"[{DETECTOR}]   the border lifetime's clicks {reading.border_clicks}")
    else:
        neutrons = reading.of_family("n")
        fired = [thing for thing in neutrons if thing.become is not None]
        triggered = sorted(int(str(thing.become["triggered"])) for thing in fired if thing.become)
        counts = sorted(int(str(thing.become["counted"])) for thing in fired if thing.become)
        print(
            f"[{GAMEBOARD}]   {len(fired)} of {len(neutrons)} neutrons transformed"
            + (
                f"; the trigger ticks {triggered[0]} .. {triggered[-1]} ({len(set(triggered))} distinct), "
                f"the counts read at the trigger {counts[0]} .. {counts[-1]}"
                if fired
                else ""
            )
        )
        for thing in neutrons[:2] if len(neutrons) > 2 else neutrons:
            print(
                f"[{DETECTOR}]   the clock of number {thing.number} at {thing.position}: age {thing.age}, "
                f"waited {thing.waited} (the rate {thing.age / max(1, thing.age + thing.waited):.4f})"
            )
        bodies = [thing for thing in reading.things if thing.family in ("p", "n")]
        for thing in bodies:
            print(
                f"[{GAMEBOARD}]   number {thing.number} ({thing.family}) at {thing.position}: {thing.steps} steps "
                f"of {thing.attempts} attempted (the refused ones handed over); "
                f"[{DETECTOR}] {thing.contacts} hand-overs taken"
            )
        total = sum(reading.shell_clicks.values())
        median, low, high, ratio = curve_shape(reading.shell_clicks)
        print(
            f"[{DETECTOR}]   the shell's beta clicks: {total} in all"
            + (
                f", from tick {min(reading.shell_clicks)} to {max(reading.shell_clicks)}; the median tick {median}, "
                f"the 10th and 90th percentiles {low} and {high}, the width over the median {ratio:.4f} "
                f"(nature's memoryless decay {NATURE_WIDTH_OVER_MEDIAN:.2f})"
                if total
                else ""
            )
        )
        if total:
            ages = sorted(reading.shell_ages)
            print(
                f"[{DETECTOR}]   the clicks' contents {dict(sorted(reading.shell_contents.items()))} (the spectrum), "
                f"their ages {ages[0]} .. {ages[-1]} (the flight to the shell)"
            )
    criteria = expectations(reading, pinned)
    for label, ok, kind in criteria:
        print(f"[{kind}]   {label}: {'inside' if ok else 'outside'}")
    print()
    return criteria


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="the folder holding the run folders")
    parser.add_argument(
        "--expectations", type=Path, default=EXPECTATIONS, help="the generator's pinned expectations"
    )
    args = parser.parse_args(argv)
    readings = find_runs(args.root)
    if not readings:
        print(f"no weak-force run under {args.root}", file=sys.stderr)
        return 2
    pinned = load_expectations(args.expectations)
    failed = 0
    for r in readings:
        for label, ok in (("completed", r.completed), ("balanced", r.balanced)):
            print(f"{'PASS' if ok else 'FAIL'} {r.name}: {label} ({r.elapsed:.1f} s, {r.ticks} ticks)")
            failed += not ok
    print()
    print(
        f"every line below is labelled [{GAMEBOARD}] (the host's view of the GameBoard: the expectation "
        f"from the engine's tables, the stride, the trigger ticks, the steps; exists for us, not in "
        f"reality) or [{DETECTOR}] (a measured event's or a detector set's own records: the only kind "
        "reality has)"
    )
    print()
    criteria: list[Criterion] = []
    for r in readings:
        criteria += print_world(r, pinned)
    inside = sum(1 for _, ok, _ in criteria if ok)
    print(
        f"{failed} record check(s) failed; {inside} reading(s) inside, {len(criteria) - inside} outside"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
