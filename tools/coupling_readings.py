"""The readings of the coupling series C under the Beam Law, on the
plane.

Reads the run folders of the worlds of `examples/events/coupling/` (the
runner's `run.json`, `initialization.json` and `events.jsonl`, the folders
told apart by the `model` of their record, `rays-coupling-<name>-plane-v1`),
replays world 5 (the source alone) through the engine's API for the ring
means and for the counts and presences at the axis Nodes, and prints a table
per item and every criterion of the entry "C, the couplings under the Beam
Law, on the plane (2026-09-19)" in docs/EXPERIMENTS.md with its verdict;
a failed criterion exits nonzero. Every identity is checked on integers and
`fractions.Fraction`; floats appear only in the ring means and the bounds.

The GameBoard is 121 x 121 x 1 with the z axis periodic: the two z headings'
rays step onto their own Node through the stub and come home, so the source
re-emits them over the six headings and the net emission into the plane is
q = 6 x 2^17 per interval at the fixed point. Under the Beam Law
(docs/BEAM_LAW.md, section 8) a free source's rays are six beams on the six
headings, a ballistic stream at 1 / sqrt 3: the items read the identities of
a stream of rays. Since 2026-09-19 the momentum label of a unit along a
heading is Q e_d with Q = `LABEL_SCALE` = 64 (the label along the unit
vector of the direction at the flight rule's scale, BEAM_LAW section 2 and
note 23), so every push, momentum and flow of the record is in label units:
where the tool compares a push or a flow with the emission q (a count of
units) or with an amount it divides the label by Q, and the registered
expectations of BEAM_LAW section 8 keep their meaning (flow x 2 pi r / q
= 1, the push -amount x m per unit); Gauss's flux is read off the Port
crossings and is untouched. 1 the equivalence (the push of a probe of
content m is m times the push of content 1, record by record; a free
probe's steps are the same for every m and its step onto the source is
refused, no merge); 2 the
third law (the pushes of A on B and of B on A equal and opposite at every
tick: each reads the other's lone beam, exact); 3 superposition (exact,
rays of different numbers never interact); 4 retardation (the first read at
r is the flight rule's first arrival at r Links, one interval after the
release, with the whole front 2^17); 5 the far field (the ring means of the
count and the presence, the flow through the ring, Gauss's flux through the
square); 6 the clock (`suspension` 1: the count owed is the presence read,
replayed); 7 the electric reading (identities against the uncharged world).
The probes read (`read`: the push taken, the rays go on), so the stream of
the source's number is the same in the worlds 5, 5P and 6: the replay of
world 5 serves the three, and the identity is checked at every tick.

    PYTHONPATH=src python tools/coupling_readings.py artifacts/coupling
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.core.integer import by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.engine import count_owed
from event_universe.events.engine import step_axis as rule_step
from event_universe.events.nature_beam import direction_flight, unit_label
from event_universe.events.world import BEAM_LAW, HEADING_OFFSET, LABEL_SCALE, NatureBeamWorld
from event_universe.events.world import Q as FLIGHT_SCALE
from event_universe.world_loading import world_of_run

# Every rule of the engine this tool needs is read off the engine's own
# functions (the architecture review of 2026-09-20, Highlights 5.4: a tool
# is a reader of the record, never a second owner of a rule): the clock
# `core.integer.by_clock` (the primitive the engine's frame, release and
# step call), the flight's constants `nature_beam.direction_flight` and its
# `manhattan_steps`, the label `nature_beam.unit_label`, the scale
# `world.LABEL_SCALE`, the world's keys through `parse_nature_beam_world` and a
# measured event's charge through `Measured.charge`.
MODEL_PREFIX = "rays-coupling-"
MODEL_SUFFIX = "-plane-v1"
CENTRE = (60, 60, 0)
SOURCE = 1 << 24
RELEASE = (1, 128)
# The source's release per heading at a self-creation: the engine's clock,
# `by_clock(age, content x n, d)` at `release` [n, d] (nature_beam, step 5),
# read at age 0; the same at every age since 128 divides 2^24.
RELEASE_PER_HEADING = by_clock(0, SOURCE * RELEASE[0], RELEASE[1])
# The net emission into the plane per interval at the fixed point: the
# release on the six headings (2^17 each), the two z headings' rays coming
# home and created again over the six.
Q = len(PORT_HEADINGS) * RELEASE_PER_HEADING
# The flight's constants of the six headings (the two rest slots first, as the
# world's table has them): the front and the mean stay are read off it.
HEADING_FLIGHT = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))
FAR_RADII = (4, 6, 8, 12, 16, 20, 24, 30, 40)
FAR_FIELD = tuple(r for r in FAR_RADII if r >= 8)
FAR_WINDOW = 50
CUBE_HALVES = (4, 8, 12, 20, 40)
ITEM1_CONTENTS = (1, 4, 16)
PROBE_RADIUS = 12
PROBE_X = (CENTRE[0] + PROBE_RADIUS, CENTRE[1], CENTRE[2])
WINDOW = 50
CHARGE = 1 << 23
PROBE_CHARGE = 2
# The mean stay of a heading ray at a Node over the flight rule's period,
# T_d / (S_1 Q) intervals per Link (the table's mean speed S_1 Q / T_d with
# T_d = isqrt(3 |v|^2 Q^2): the design's 1 / sqrt 3 rounded to the table's
# integers, 110 / 64 on a heading; until 2026-09-20 the tool printed the
# unrounded 1 / (1 / sqrt 3)).
STAY = int(HEADING_FLIGHT.resolution[HEADING_OFFSET]) / (
    int(HEADING_FLIGHT.manhattan[HEADING_OFFSET]) * FLIGHT_SCALE
)
AXES = {
    "+x": (1, 0, 0),
    "-x": (-1, 0, 0),
    "+y": (0, 1, 0),
    "-y": (0, -1, 0),
}
RETARDATION_PROBES = (("-x", 4), ("+y", 6), ("-y", 8), ("+x", PROBE_RADIUS))
Vector = tuple[int, int, int]
Record = dict[str, Any]
Reads = dict[int, tuple[int, Vector]]


def at(axis: str, radius: int) -> Vector:
    heading = AXES[axis]
    return (
        CENTRE[0] + radius * heading[0],
        CENTRE[1] + radius * heading[1],
        CENTRE[2] + radius * heading[2],
    )


def vector(values: object) -> Vector:
    assert isinstance(values, list) and len(values) == 3
    return (int(values[0]), int(values[1]), int(values[2]))


def scaled(v: Vector, m: int) -> Vector:
    return (v[0] * m, v[1] * m, v[2] * m)


def added(a: Vector, b: Vector) -> Vector:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def step_axis(event: Record) -> int:
    origin, target = vector(event["node"]), vector(event["to"])
    return next(axis for axis in range(3) if origin[axis] != target[axis])


def steps_by_rule(reads: Reads, m: int, first: int, last: int, width: int = 1) -> list[tuple[int, int]]:
    """The (tick, axis) at which a free probe of content m steps by the
    engine's step rule on the record (`NatureBeamSimulation._move`, ENGINE.md;
    since 2026-09-20 the step drive, BEAM_LAW note 17 as amended: on an
    axis whose momentum component is p the signed drive gains p at every
    self-creation and the body steps when it reaches Q x S x m + |p|, the
    engine's own `engine.step_axis` called here): its momentum is the
    cumulative push of its reads (born at rest), at tick t after that
    tick's read the first axis whose rule fires steps (the momentum in
    label units, Q = `LABEL_SCALE`, S the world's `width`); at most one per
    interval, x before y before z, wherever it lands (a refused step
    counts); the drive of every axis advances at every interval as the
    engine's does, and a fire on a later axis in the interval of an
    earlier axis's step is lost, as the frame loses it."""
    momentum = [0, 0, 0]
    drive = [0, 0, 0]
    fired: list[tuple[int, int]] = []
    for tick in range(first, last + 1):
        if tick in reads:
            momentum = list(added((momentum[0], momentum[1], momentum[2]), reads[tick][1]))
        stepped = None
        for axis in range(3):
            sign, drive[axis] = rule_step(drive[axis], momentum[axis], m, width)
            if sign is not None and stepped is None:
                stepped = axis
        if stepped is not None:
            fired.append((tick, stepped))
    return fired


def first_arrivals(links: int) -> dict[int, int]:
    """The flight rule's first arrival at m Links of a heading ray, by m:
    the least age at which the table's Manhattan steps m(tau) reach m
    (`Flight.manhattan_steps`, the position accumulator's count off the
    age), counted from the ray's first walk (a ray at age 0 walks at its
    first interval)."""
    ages = np.arange(1, 4 * links + 1, dtype=np.int64)
    heading = np.full(ages.shape, HEADING_OFFSET, dtype=np.int64)
    reached = HEADING_FLIGHT.manhattan_steps(heading, ages)
    found: dict[int, int] = {}
    for age, steps in zip(ages.tolist(), reached.tolist(), strict=True):
        found.setdefault(int(steps), int(age))
    return found


ARRIVALS = first_arrivals(64)


def front(radius: int) -> tuple[int, int]:
    """The first read (tick, amount) of a probe at `radius` on an axis: the
    source's first release at tick 1 walks from tick 2, so the front of 2^17
    whole arrives at tick 1 + the flight rule's first arrival at r Links."""
    return (1 + ARRIVALS[radius], RELEASE_PER_HEADING)


def label_push(heading: Vector, amount: int, content: int) -> Vector:
    """The push the engine takes on a free reader of content m from `amount`
    units of an uncharged free family's ray arriving on `heading`: minus m
    times the label flow (BEAM_LAW section 3, step 4), the label of one
    unit being u_d, the unit vector of the direction at the scale Q
    (`unit_label`, exactly Q e_d on a heading): -amount x m x Q along it."""
    return scaled(unit_label(heading), -amount * content)


def declared_charges(world: NatureBeamWorld) -> list[int | Fraction]:
    """The charge of every measured event of the parsed world in declaration
    order, as the engine computes it (`Measured.charge`: the family's charge
    per unit of content, rho = [n, d], times the event's content, a reduced
    pair; the model owner, 2026-09-20): an integer where the pair is whole,
    a `Fraction` otherwise."""
    simulation = NatureBeamSimulation(world)
    found: list[int | Fraction] = []
    for number in sorted(simulation.measured):
        numerator, denominator = simulation.measured[number].charge
        found.append(numerator if denominator == 1 else Fraction(numerator, denominator))
    return found


def slope(radii: tuple[int, ...], values: list[float]) -> float:
    x = np.log(np.array(radii, dtype=float))
    y = np.log(np.array(values, dtype=float))
    return float(np.polyfit(x, y, 1)[0])


def ripple(values: list[float]) -> float:
    """max / min - 1 over positive readings."""
    return max(values) / min(values) - 1


@dataclass
class Checks:
    """The criteria, each with its verdict and what was found."""

    rows: list[tuple[str, bool, str]] = field(default_factory=list)
    readings: list[tuple[str, bool, str]] = field(default_factory=list)

    def add(self, name: str, ok: bool, detail: str) -> None:
        self.rows.append((name, ok, detail))

    def reading(self, name: str, found: float, low: float, high: float) -> None:
        """A reading against the expectation of docs/BEAM_LAW.md, section 8: registered
        as measured, inside or outside the expectation, never moved and never a failure."""
        self.readings.append(
            (
                name,
                low <= round(found, 6) <= high,
                f"measured {found:.4f}, expected [{low}, {high}]",
            )
        )

    @property
    def outside(self) -> int:
        return sum(1 for _, ok, _ in self.readings if not ok)

    def equal(self, name: str, found: object, expected: object) -> None:
        self.add(name, found == expected, f"found {found}, expected {expected}")

    def within(self, name: str, found: float, low: float, high: float) -> None:
        self.add(name, low <= found <= high, f"found {found:.4f}, expected [{low}, {high}]")

    @property
    def failed(self) -> int:
        return sum(1 for _, ok, _ in self.rows if not ok)


@dataclass
class Run:
    """One run folder: its record (`run.json`), its world as declared
    (`initialization.json`, the JSON object) and as the engine parses it
    (`parsed`, the world's keys with their defaults), and its events."""

    name: str
    folder: Path
    record: Record
    world: Record
    parsed: NatureBeamWorld
    events: list[Record]

    @property
    def ticks(self) -> int:
        return self.parsed.ticks

    def measured(self, number: int) -> Record | None:
        for entry in self.record["measured"]:
            if int(entry["number"]) == number:
                return dict(entry)
        return None

    def reads(self, reader: int, emitter: int) -> Reads:
        """The `read` records of one reader of one emitter's rays, by tick:
        the amount and the push (one record per tick and number)."""
        found: Reads = {}
        for event in self.events:
            if (
                event["event"] == "read"
                and int(event["measured"]) == reader
                and int(event["number"]) == emitter
            ):
                tick = int(event["tick"])
                assert tick not in found, (self.name, reader, emitter, tick)
                found[tick] = (int(event["amount"]), vector(event["push"]))
        return found

    def window_push(self, reads: Reads, first: int, last: int) -> Vector:
        total: Vector = (0, 0, 0)
        for tick, (_, push) in reads.items():
            if first <= tick <= last:
                total = added(total, push)
        return total

    def escaped_by_tick(self, family: str) -> list[int]:
        return [int(entry["families"][family]["transit"]["escaped"]) for entry in self.record["audit"]]


def load(folder: Path) -> Run:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    world = world_of_run(folder)
    parsed = parse_nature_beam_world(world)
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        events = [json.loads(line) for line in stream if line.strip()]
    model = str(record["model"])
    if not (model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX)):
        raise ValueError(f"{folder}: not a world of the coupling series on the plane ({model})")
    name = model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)].replace("-", "_")
    return Run(name, folder, record, world, parsed, events)


def find_runs(root: Path) -> list[Path]:
    """The run folders under `root`: a folder with `run.json`, or one holding
    `run/run.json` (the layout of `tools/run_series.py`)."""
    found = []
    for path in sorted(root.iterdir()):
        if (path / "run.json").exists():
            found.append(path)
        elif (path / "run" / "run.json").exists():
            found.append(path / "run")
    return found


# -- the identities of every world ----------------------------------------------


def common_checks(run: Run, checks: Checks) -> None:
    label = run.name
    record = run.record
    checks.equal(f"{label}: status", record["status"], "completed")
    checks.equal(f"{label}: the law", record["law"], BEAM_LAW)
    checks.equal(f"{label}: completed ticks", record["completed_ticks"], run.ticks)
    checks.equal(
        f"{label}: the GameBoard 121 x 121 x 1 with z periodic", record["boundary"], {"z": "periodic"}
    )
    checks.equal(f"{label}: the shape", record["shape"], [121, 121, 1])
    checks.equal(
        f"{label}: the books at every completed tick", record["conserved_at_every_completed_tick"], True
    )
    checks.equal(f"{label}: audit entries", len(record["audit"]), run.ticks)
    content = record["measured_content"]
    checks.equal(
        f"{label}: measured content constant (read absorbs nothing)",
        all(entry == content[0] for entry in content),
        True,
    )
    checks.equal(
        f"{label}: age + waited = completed intervals for every surviving measured event",
        [(int(m["number"]), int(m["age"]) + int(m["waited"])) for m in record["measured"]],
        [(int(m["number"]), run.ticks) for m in record["measured"]],
    )
    checks.equal(
        f"{label}: no merged record (a step onto a measured event is refused)",
        sum(1 for e in run.events if e["event"] == "merged"),
        0,
    )


# -- item 1: the equivalence ---------------------------------------------------


def item_1(runs: dict[str, Run], checks: Checks) -> list[str]:
    lines = [f"item 1, the equivalence (the probe at {PROBE_X}, r = {PROBE_RADIUS} on +x)", ""]
    lines.append(
        "world | m | reads | first read (tick, amount, push) | pushed | push = m x push_1 at every tick and axis"
    )
    lines.append(" | ".join("---" for _ in range(6)))
    base = runs["1a_m1"].reads(2, 1)
    base_tick = min(base)
    for m in ITEM1_CONTENTS:
        run = runs[f"1a_m{m}"]
        reads = run.reads(2, 1)
        first_tick = min(reads)
        first = (first_tick, reads[first_tick][0], reads[first_tick][1])
        checks.equal(
            f"1a_m{m}: the first read is (tick, amount, -amount x m x Q on +x) with 1a_m1's tick and amount",
            first,
            (base_tick, base[base_tick][0], label_push(AXES["+x"], base[base_tick][0], m)),
        )
        checks.equal(
            f"1a_m{m}: the same ticks and amounts as 1a_m1",
            {t: a for t, (a, _) in reads.items()},
            {t: a for t, (a, _) in base.items()},
        )
        identity = set(reads) == set(base) and all(reads[t][1] == scaled(base[t][1], m) for t in base)
        checks.equal(f"1a_m{m}: push_m(t) = m x push_1(t) at every tick and axis", identity, True)
        probe = run.measured(2)
        assert probe is not None
        pushed = vector(probe["pushed"])
        base_probe = runs["1a_m1"].measured(2)
        assert base_probe is not None
        checks.equal(f"1a_m{m}: pushed = m x pushed_1", pushed, scaled(vector(base_probe["pushed"]), m))
        axial = sum(1 for a, p in reads.values() if p == label_push(AXES["+x"], a, m))
        lines.append(
            f"1a_m{m} | {m} | {len(reads)} | {first} | {pushed} | {'yes' if identity else 'NO'} "
            f"(push = (-amount x m x Q, 0, 0) exactly at {axial} of {len(reads)} records)"
        )
    lines.append("")
    lines.append(
        "world | m | steps (ticks) | x from -> to | final Node | momentum = m x momentum_1 at every step | reads (push = m x push_1)"
    )
    lines.append(" | ".join("---" for _ in range(7)))
    base_steps = [e for e in runs["1b_m1"].events if e["event"] == "step"]
    base_reads = runs["1b_m1"].reads(2, 1)
    for m in ITEM1_CONTENTS:
        run = runs[f"1b_m{m}"]
        steps = [e for e in run.events if e["event"] == "step"]
        ticks = [int(e["tick"]) for e in steps]
        checks.equal(
            f"1b_m{m}: the step records (tick, node, to) identical to 1b_m1",
            [(e["tick"], e["node"], e["to"]) for e in steps],
            [(e["tick"], e["node"], e["to"]) for e in base_steps],
        )
        reads = run.reads(2, 1)
        probe = run.measured(2)
        assert probe is not None
        checks.equal(
            f"1b_m{m}: the probe ends beside the source, its steps onto it refused (no merge)",
            (vector(probe["position"]), [int(e["number"]) for e in run.record["measured"]]),
            ((CENTRE[0] + 1, CENTRE[1], CENTRE[2]), [1, 2]),
        )
        walked = [(int(e["tick"]), step_axis(e)) for e in steps]
        by_rule = steps_by_rule(reads, m, min(reads), run.ticks, run.parsed.width)
        checks.equal(
            f"1b_m{m}: the steps walked are the first {len(walked)} steps of the rule off the clock on the reads' cumulative push",
            walked,
            by_rule[: len(walked)],
        )
        checks.equal(
            f"1b_m{m}: one x-step per interval from the first step to the source, x {PROBE_X[0]} down to {CENTRE[0] + 1}",
            [(int(e["tick"]), vector(e["node"])[0], vector(e["to"])[0]) for e in steps],
            [(ticks[0] + k, PROBE_X[0] - k, PROBE_X[0] - k - 1) for k in range(PROBE_RADIUS - 1)]
            if ticks
            else [],
        )
        checks.equal(
            f"1b_m{m}: the momentum at every step m times 1b_m1's",
            [vector(e["momentum"]) for e in steps],
            [scaled(vector(e["momentum"]), m) for e in base_steps],
        )
        checks.equal(
            f"1b_m{m}: push_m(t) = m x push_1(t) at every read of the free probe",
            {t: p for t, (_, p) in reads.items()},
            {t: scaled(p, m) for t, (_, p) in base_reads.items()},
        )
        source = run.measured(1)
        assert source is not None
        checks.equal(
            f"1b_m{m}: the source's content 2^24, the probe's m",
            (int(source["content"]), int(probe["content"])),
            (SOURCE, m),
        )
        same_momentum = [vector(e["momentum"]) for e in steps] == [
            scaled(vector(e["momentum"]), m) for e in base_steps
        ]
        lines.append(
            f"1b_m{m} | {m} | {len(steps)} ({ticks[0] if ticks else None}..{ticks[-1] if ticks else None}) "
            f"| {vector(steps[0]['node'])[0] if steps else None} -> {vector(steps[-1]['to'])[0] if steps else None} "
            f"| {vector(probe['position'])} | {'yes' if same_momentum else 'NO'} | {len(reads)}"
        )
    first_step = min(int(e["tick"]) for e in base_steps) if base_steps else None
    lines.append("")
    lines.append(
        f"the first read at tick {base_tick} with amount {base[base_tick][0]} (the front of the flight); the "
        f"first step at tick {first_step} (the rule off the clock: by_clock(t - 1, |p|, Q m + |p|) on the cumulative push in label units); "
        "the steps onto the source refused, the probe beside it (no merge since 2026-09-19)"
    )
    return lines


# -- item 2: the third law with unequal contents ---------------------------------


def item_2(runs: dict[str, Run], checks: Checks) -> list[str]:
    run = runs["2"]
    a, b = run.measured(1), run.measured(2)
    assert a is not None and b is not None
    d = abs(vector(a["position"])[0] - vector(b["position"])[0])
    on_a, on_b = run.reads(1, 2), run.reads(2, 1)
    p_a, p_b = vector(a["pushed"]), vector(b["pushed"])
    lines = [
        f"item 2, the third law with unequal contents (A = 2^22 at x = {vector(a['position'])[0]}, "
        f"B = 2^20 at x = {vector(b['position'])[0]}, d = {d})",
        "",
    ]
    lines.append("window | P_A (push on A) | P_B (push on B) | |P_A,x| / |P_B,x|")
    lines.append(" | ".join("---" for _ in range(4)))
    windows = [(1 + k * WINDOW, (k + 1) * WINDOW) for k in range(run.ticks // WINDOW)]
    for first, last in windows:
        wa, wb = run.window_push(on_a, first, last), run.window_push(on_b, first, last)
        ratio = Fraction(abs(wa[0]), abs(wb[0])) if wb[0] else Fraction(0)
        lines.append(f"{first}-{last} | {wa} | {wb} | {float(ratio):.4f}")
    lines.append(f"cumulative | {p_a} | {p_b} | {abs(p_a[0]) / abs(p_b[0]):.4f}")
    checks.equal(
        "2: the cumulative pushes toward each other (P_A,x > 0, P_B,x < 0)",
        (p_a[0] > 0, p_b[0] < 0),
        (True, True),
    )
    checks.equal(
        "2: the sum of the read pushes is the cumulative pushed",
        (run.window_push(on_a, 1, run.ticks), run.window_push(on_b, 1, run.ticks)),
        (p_a, p_b),
    )
    # Each source releases content / 128 per interval apportioned whole over its six
    # headings (2^15 = 6 x 5461 + 2 and 2^13 = 6 x 1365 + 2, the leftover units to the
    # directions `age mod 6` on), so the amount on the axis toward the other varies by a
    # unit from interval to interval and the reads of one tick (one or two rays) differ by
    # a few units of 2^20 against about 10^4: the cumulative pushes cancel to the grain.
    grain = int(b["content"])
    largest = max(
        (
            abs(added(on_a[t][1], on_b[t][1])[0]) / abs(on_a[t][1][0])
            for t in on_a
            if t in on_b and on_a[t][1][0]
        ),
        default=0.0,
    )
    lines.append("")
    lines.append(
        f"per tick |push_A + push_B|_x / |push_A|_x at most {largest:.4f} (the grain of the whole "
        f"apportioning: units of B's content 2^20 = {grain} against about 5461 units read); cumulative "
        f"|P_A + P_B|_x / |P_A|_x = {abs(added(p_a, p_b)[0]) / abs(p_a[0]):.2e}"
    )
    checks.equal("2: the same reading ticks on both", set(on_a) == set(on_b), True)
    checks.within(
        "2: at every tick, |push_A(t) + push_B(t)| / |push_A(t)| below 1 % (the apportioning's grain)",
        largest,
        0.0,
        0.01,
    )
    checks.within(
        "2: |P_A + P_B| / |P_A| cumulative below 1e-4 (1.0000 at four decimals)",
        abs(added(p_a, p_b)[0]) / abs(p_a[0]),
        0.0,
        1e-4,
    )
    checks.equal(
        "2: P_A + P_B = 0 over the first window (the leftovers in step)",
        added(run.window_push(on_a, 1, WINDOW), run.window_push(on_b, 1, WINDOW)),
        (0, 0, 0),
    )
    return lines


# -- item 3: superposition -------------------------------------------------------


def item_3(runs: dict[str, Run], checks: Checks) -> list[str]:
    three, alone_a, alone_b = runs["3"], runs["3a"], runs["3b"]
    by_a, by_b = three.reads(3, 1), three.reads(3, 2)
    a_alone, b_alone = alone_a.reads(2, 1), alone_b.reads(1, 2)
    checks.equal("3: the probe's records of A (number 1) equal 3a's exactly", by_a, a_alone)
    checks.equal("3: the probe's records of B (number 2) equal 3b's exactly", by_b, b_alone)
    probe, probe_a, probe_b = three.measured(3), alone_a.measured(2), alone_b.measured(1)
    assert probe is not None and probe_a is not None and probe_b is not None
    total = vector(probe["pushed"])
    checks.equal(
        "3: the probe's total push is the sum of 3a's and 3b's exactly",
        total,
        added(vector(probe_a["pushed"]), vector(probe_b["pushed"])),
    )
    checks.equal(
        "3: A's and B's mutual records unchanged by the probe (as in world 2)",
        (three.reads(1, 2), three.reads(2, 1)),
        (runs["2"].reads(1, 2), runs["2"].reads(2, 1)),
    )
    lines = [f"item 3, superposition (the probe of content 1 at {at('+y', 8)})", ""]
    lines.append("world | records of A | records of B | probe pushed")
    lines.append(" | ".join("---" for _ in range(4)))
    lines.append(f"3 | {len(by_a)} | {len(by_b)} | {total}")
    lines.append(f"3a | {len(a_alone)} | | {vector(probe_a['pushed'])}")
    lines.append(f"3b | | {len(b_alone)} | {vector(probe_b['pushed'])}")
    return lines


# -- item 4: retardation ---------------------------------------------------------


def first_read(run: Run, reader: int) -> tuple[int, int, Vector]:
    reads = run.reads(reader, 1)
    tick = min(reads)
    return (tick, reads[tick][0], reads[tick][1])


def item_4(runs: dict[str, Run], checks: Checks) -> list[str]:
    lines = ["item 4, retardation (the first read of each probe)", ""]
    lines.append("world | axis | r | Node | found (tick, amount, push) | the flight rule (tick, amount)")
    lines.append(" | ".join("---" for _ in range(6)))
    rows: list[tuple[str, str, int, int]] = [
        ("4", axis, r, k + 2) for k, (axis, r) in enumerate(RETARDATION_PROBES)
    ]
    rows.append(("1a_m1", "+x", PROBE_RADIUS, 2))
    rows.append(("7_00", "+x", PROBE_RADIUS, 2))
    rows += [("5p", "+x", r, k + 2) for k, r in enumerate(FAR_RADII)]
    rows += [("6", "+x", r, k + 2) for k, r in enumerate(FAR_RADII)]
    for name, axis, r, reader in rows:
        run = runs[name]
        probe = run.measured(reader)
        assert probe is not None and vector(probe["position"]) == at(axis, r), (name, reader)
        found = first_read(run, reader)
        heading = AXES[axis]
        expected = front(r)
        checks.equal(
            f"{name}: the first read of the probe at r = {r} on {axis} pushes -amount x m x Q along the axis",
            found[2],
            label_push(heading, found[1], int(probe["content"])),
        )
        checks.equal(
            f"{name}: the first read of the probe at r = {r} on {axis} is the flight rule's front, whole",
            found[:2],
            expected,
        )
        lines.append(f"{name} | {axis} | {r} | {at(axis, r)} | {found} | {expected}")
    lines.append("")
    lines.append(
        "the front: 2^17 whole (a ray does not spread), at tick 1 + the flight rule's first arrival at r Links"
    )
    return lines


# -- item 5: the far field, and the replay of world 5 ------------------------------


@dataclass
class Replay:
    """What the replay of world 5 through the API reads: per tick the count
    and the presence at the +x axis Nodes (for 5P and 6), and over the last
    window the ring means, the flux through the square and the escape."""

    ticks: int
    nodes: dict[int, int]
    count_at: dict[int, list[int]]
    presence_at: dict[int, list[int]]
    ring: dict[str, dict[int, float]]
    cube: dict[int, float]
    escape: float
    window: tuple[int, int]
    audit_matches: bool


def square_flux(simulation: NatureBeamSimulation, half: int) -> int:
    """Gauss's flux through the square of half-width `half` about the centre
    on the plane: the arrivals just outside each in-plane face moving
    outward less the arrivals on the face moving inward (the engine's
    `per_port` reading; the z faces have no outside Node)."""
    per_port = simulation.per_port[0]
    total = 0
    for axis in range(2):
        for sign in (1, -1):
            face = CENTRE[axis] + sign * half
            outside = face + sign
            lows = [CENTRE[a] - half for a in range(2)] + [0]
            highs = [CENTRE[a] + half + 1 for a in range(2)] + [1]
            slices = [slice(lows[a], highs[a]) for a in range(3)]
            outward = 2 * axis + (0 if sign > 0 else 1)
            inward = outward ^ 1
            slices[axis] = slice(outside, outside + 1)
            total += int(per_port[tuple(slices)][..., outward].sum())
            slices[axis] = slice(face, face + 1)
            total -= int(per_port[tuple(slices)][..., inward].sum())
    return total


def replay_world_5(run: Run, window: int) -> Replay:
    world = run.parsed
    simulation = NatureBeamSimulation(world)
    ticks = world.ticks
    first = ticks - window + 1
    # The ring's Nodes are the engine's shell (`shell_readings`: the Nodes at
    # Euclidean distance within a half Link of r from the centre).
    nodes = {r: int(simulation.shell_readings(0, CENTRE, r)["nodes"]) for r in FAR_RADII}
    count_at: dict[int, list[int]] = {r: [] for r in FAR_RADII}
    presence_at: dict[int, list[int]] = {r: [] for r in FAR_RADII}
    keys = ("count", "flow", "presence")
    sums: dict[str, dict[int, float]] = {key: dict.fromkeys(FAR_RADII, 0.0) for key in keys}
    cube: dict[int, float] = dict.fromkeys(CUBE_HALVES, 0.0)
    audit_matches = True
    audit = run.record["audit"]
    for tick in range(1, ticks + 1):
        simulation.step()
        books = json.loads(json.dumps(simulation.books()))
        audit_matches = audit_matches and books == audit[tick - 1]
        for r in FAR_RADII:
            node = at("+x", r)
            count_at[r].append(int(simulation.arrived[0][node]))
            presence_at[r].append(int(simulation.presence[0][node]))
        if tick >= first:
            for r in FAR_RADII:
                reading = simulation.shell_readings(0, CENTRE, r)
                for key in keys:
                    sums[key][r] += reading[key]
            for h in CUBE_HALVES:
                cube[h] += square_flux(simulation, h)
    ring = {key: {r: value / window for r, value in per_r.items()} for key, per_r in sums.items()}
    escaped = run.escaped_by_tick(world.families[0].name)
    escape = (escaped[ticks - 1] - escaped[first - 2]) / window / Q
    return Replay(
        ticks,
        nodes,
        count_at,
        presence_at,
        ring,
        {h: v / window / Q for h, v in cube.items()},
        escape,
        (first, ticks),
        audit_matches,
    )


def item_5(
    run: Run, replay: Replay, checks: Checks, label: str = "5", pinned: bool = True
) -> tuple[list[str], dict[str, float]]:
    checks.equal(
        f"{label}: the replay's books equal the record's audit at every tick", replay.audit_matches, True
    )
    first, last = replay.window
    lines = [
        f"GAMEBOARD (a host reading of the GameBoard: `shell_readings` and the cube flux) item 5, the far field (world {label}, the source alone, the ring means over ticks {first}-{last}; q = {Q}; the flow in label units divided by Q_label = {LABEL_SCALE})"
        + ("" if pinned else " (supplementary, not pinned)"),
        "",
    ]
    lines.append(
        "r | Nodes | count x r / q | presence x r / q | flow / Q_label x 2 pi r / q | presence / count"
    )
    lines.append(" | ".join("---" for _ in range(6)))
    scaled_readings: dict[str, list[float]] = {"count": [], "presence": [], "flow": [], "ratio": []}
    for r in FAR_RADII:
        count = replay.ring["count"][r] * r / Q
        presence = replay.ring["presence"][r] * r / Q
        flow = replay.ring["flow"][r] / LABEL_SCALE * 2 * math.pi * r / Q
        ratio = replay.ring["presence"][r] / replay.ring["count"][r] if replay.ring["count"][r] else 0.0
        for key, value in (("count", count), ("presence", presence), ("flow", flow), ("ratio", ratio)):
            scaled_readings[key].append(value)
        lines.append(
            f"{r} | {replay.nodes[r]} | {count:.4f} | {presence:.4f} | {flow:.4f} | {ratio:.4f}"
        )
    far = [FAR_RADII.index(r) for r in FAR_FIELD]
    slopes = {
        key: slope(FAR_RADII, [replay.ring[key][r] for r in FAR_RADII])
        for key in ("count", "flow", "presence")
    }
    lines.append("")
    lines.append(
        f"log-log slopes over r = {FAR_RADII}: count {slopes['count']:.3f}, flow {slopes['flow']:.3f}, presence {slopes['presence']:.3f}"
    )
    lines.append(
        "flux through the square (the four in-plane faces) / q at h = "
        + ", ".join(f"{h}: {replay.cube[h]:.4f}" for h in CUBE_HALVES)
    )
    lines.append(f"escape per interval over the window / q: {replay.escape:.4f}")
    lines.append(
        "the six beams: the ring's Nodes off the four in-plane axes are empty, so a ring mean is the axial Node's "
        f"reading over the ring (count x r / q = r / Nodes, about 1 / (2 pi) = {1 / (2 * math.pi):.4f}); presence / count "
        f"is the mean stay of a ray at a Node, 1 / c = {STAY:.4f} over the flight rule's period"
    )
    if pinned:
        for key, name in (("count", "count x r / q"), ("presence", "presence x r / q")):
            checks.reading(
                f"{label}: {name} a constant over r >= {FAR_FIELD[0]} (max / min - 1 <= 0.10)",
                ripple([scaled_readings[key][i] for i in far]),
                0.0,
                0.10,
            )
        for i in far:
            checks.reading(
                f"{label}: count x r / q on the six headings, r = {FAR_RADII[i]} in [0.15, 0.19]",
                scaled_readings["count"][i],
                0.15,
                0.19,
            )
            checks.reading(
                f"{label}: flow x 2 pi r / q about 1 in the far field, r = {FAR_RADII[i]} in [0.90, 1.10]",
                scaled_readings["flow"][i],
                0.90,
                1.10,
            )
        checks.within(f"{label}: slope of the count -1.00 +- 0.10", slopes["count"], -1.10, -0.90)
        checks.within(f"{label}: slope of the flow -1.00 +- 0.15", slopes["flow"], -1.15, -0.85)
        checks.reading(f"{label}: slope of the presence -1.00 +- 0.10", slopes["presence"], -1.10, -0.90)
        for h in CUBE_HALVES:
            checks.within(
                f"{label}: flux through the square / q at h = {h} within 2 % of 1 (Gauss)",
                replay.cube[h],
                0.98,
                1.02,
            )
        checks.within(
            f"{label}: escape per interval over the window within 2 % of q (a ballistic stream)",
            replay.escape,
            0.98,
            1.02,
        )
    flat = [i for i, r in enumerate(FAR_RADII) if r >= 5]
    flow_values = [scaled_readings["flow"][i] for i in flat]
    convergence = {
        "flow_mean": sum(flow_values) / len(flow_values),
        "flow_min": min(flow_values),
        "flow_max": max(flow_values),
        "stay_mean": sum(scaled_readings["ratio"][i] for i in flat) / len(flat),
        **{f"slope_{key}": value for key, value in slopes.items()},
    }
    return lines, convergence


def axis_probes(run: Run, replay: Replay, checks: Checks, label: str) -> list[str]:
    last = run.ticks
    first = last - FAR_WINDOW + 1
    lines = [
        f"GAMEBOARD (a host reading of the GameBoard, the probes' counts) {label}: the probes on +x, the axis readings over ticks {first}-{last} (the beam's Nodes)",
        "",
    ]
    lines.append(
        "r | Node | reads | amount read = replay count at every tick | -push_x / Q_label x 2 pi r / (m q) | count x r / q | presence (replay) | push per interval (label units)"
    )
    lines.append(" | ".join("---" for _ in range(8)))
    for k, r in enumerate(FAR_RADII):
        reader = k + 2
        probe = run.measured(reader)
        assert probe is not None
        m = int(probe["content"])
        reads = run.reads(reader, 1)
        same = all(
            reads.get(t, (0, (0, 0, 0)))[0] == replay.count_at[r][t - 1] for t in range(1, last + 1)
        )
        checks.equal(
            f"{label}: the amount read at r = {r} equals the replay's count at every tick", same, True
        )
        push = run.window_push(reads, first, last)
        count = sum(reads[t][0] for t in reads if first <= t <= last) / FAR_WINDOW
        presence = sum(replay.presence_at[r][first - 1 : last]) / FAR_WINDOW
        axial = -push[0] / LABEL_SCALE / FAR_WINDOW * 2 * math.pi * r / (m * Q)
        lines.append(
            f"{r} | {at('+x', r)} | {len(reads)} | {'yes' if same else 'NO'} | {axial:.4f} "
            f"| {count * r / Q:.4f} | {presence:.1f} | {tuple(v / FAR_WINDOW for v in push)}"
        )
    return lines


# -- item 6: the clock -----------------------------------------------------------


def item_6(runs: dict[str, Run], replay: Replay, checks: Checks) -> list[str]:
    run = runs["6"]
    # The width of the clock's count as the engine parses it, `suspension`
    # [n, d] (an integer w accepted as [w, 1]).
    numerator, denominator = run.parsed.suspension
    checks.equal("6: suspension 1", Fraction(numerator, denominator), 1)
    source = run.measured(1)
    assert source is not None
    lines = axis_probes(run, replay, checks, "6")
    lines += [
        "",
        f"the source: age {int(source['age'])}, waited {int(source['waited'])} (its own number's returns through the stub are home, not read)",
        "the clock: age(200) replayed from the presence read (k_t = the rays of the source's number at the probe's Node at each self-creation, owed = count_owed(acc, k_t, [1, 1]), the accumulator of the fraction-free law)",
        "",
    ]
    lines.append(
        "r | age(200) | waited | owed | replay (age, waited, owed) | age(60) | lost 1 - age/200 | k (window mean) | k / (k + 1)"
    )
    lines.append(" | ".join("---" for _ in range(9)))
    lost_by_r: list[float] = []
    for k_index, r in enumerate(FAR_RADII):
        reader = k_index + 2
        probe = run.measured(reader)
        assert probe is not None
        # The clock's frame as the engine keeps it (`NatureBeamSimulation._frame_all`
        # and `_suspend`, ENGINE.md): an interval owed is paid by one, else
        # the event self-creates, its age advances and it owes the count
        # its owed accumulator gains, `count_owed(acc, presence, [n, d])`
        # (the fraction-free law, BEAM_LAW note 41), on the presence the
        # replay read at its Node.
        age, waited, owed, accumulator = 0, 0, 0, 0
        age_60 = 0
        for tick in range(1, run.ticks + 1):
            if owed > 0:
                owed -= 1
                waited += 1
            else:
                owed, accumulator = count_owed(
                    accumulator, replay.presence_at[r][tick - 1], (numerator, denominator)
                )
                age += 1
            if tick == 60:
                age_60 = age
        found = (int(probe["age"]), int(probe["waited"]), int(probe["owed"]))
        checks.equal(f"6: age + waited = 200 at r = {r}", found[0] + found[1], run.ticks)
        checks.equal(
            f"6: (age, waited, owed) at r = {r} equal the replay of the presence read",
            found,
            (age, waited, owed),
        )
        checks.equal(
            f"6: the clock at r = {r} counts until the front's arrival at tick {front(r)[0]} and is "
            "then owed the beam's presence for the rest of the run (the accepted price on the axis)",
            (found[0], found[0] == age_60 or found[0] > 60),
            (front(r)[0], True),
        )
        expected_k = Q / (6 * r)
        checks.reading(
            f"6: the count's share lost at r = {r} against k / (k + 1) with k = q / (6 r) ~ 1 / r",
            1 - found[0] / run.ticks,
            0.0,
            expected_k / (expected_k + 1),
        )
        first, last = run.ticks - FAR_WINDOW + 1, run.ticks
        k_mean = sum(replay.presence_at[r][first - 1 : last]) / FAR_WINDOW * numerator / denominator
        lost = 1 - found[0] / run.ticks
        lost_by_r.append(lost)
        lines.append(
            f"{r} | {found[0]} | {found[1]} | {found[2]} | {(age, waited, owed)} | {age_60} | {lost:.4f} | {k_mean:.1f} | {k_mean / (k_mean + 1):.4f}"
        )
    checks.equal(
        "6: the source's clock unslowed (no other number at c): age 200, waited 0",
        (int(source["age"]), int(source["waited"])),
        (run.ticks, 0),
    )
    lines.append("")
    lines.append(
        "on the axis the presence is the beam's (2^17 per ray, one or two rays at the Node), the same at every r: "
        "the slowing on the axis does not fall with r; off the axis a Node reads no ray (the six-heading gas of "
        "docs/BEAM_LAW.md, section 8, item 6: granular, ~1 / r in the mean over a ring)"
    )
    return lines


# -- item 7: the electric reading --------------------------------------------------


def item_7(runs: dict[str, Run], checks: Checks) -> list[str]:
    base = runs["7_00"].reads(2, 1)
    checks.equal(
        "7_00: the uncharged world's records equal 1a_m1's (family q, charge 0)",
        base,
        runs["1a_m1"].reads(2, 1),
    )
    base_probe = runs["7_00"].measured(2)
    assert base_probe is not None
    pushed_00 = vector(base_probe["pushed"])
    lines = [f"item 7, the electric reading (Q on the source, q on the probe at {PROBE_X})", ""]
    lines.append("world | Q | q | m | records | push per record | pushed | electric / gravity per axis")
    lines.append(" | ".join("---" for _ in range(8)))
    signs = {"0": 0, "p": 1, "m": -1}
    for name in ("7_00", "7_pp", "7_pm", "7_mp", "7_mm", "7_pp_m4"):
        run = runs[name]
        probe = run.measured(2)
        assert probe is not None
        m = int(probe["content"])
        big = signs[name[2]] * CHARGE
        small = signs[name[3]] * PROBE_CHARGE
        source_charge, probe_charge = declared_charges(run.parsed)
        checks.equal(f"{name}: the declared charges (Q, q)", (source_charge, probe_charge), (big, small))
        reads = run.reads(2, 1)
        checks.equal(
            f"{name}: the same ticks and amounts as 7_00",
            {t: a for t, (a, _) in reads.items()},
            {t: a for t, (a, _) in base.items()},
        )
        sign = (1 if big * small > 0 else -1) if big * small else 0
        factor = m - sign
        checks.equal(
            f"{name}: every push = ({factor}) x the (0, 0) push (gravity -m c, electric sign(Qq) c)",
            all(reads[t][1] == scaled(base[t][1], factor) for t in base),
            True,
        )
        checks.equal(
            f"{name}: pushed = ({factor}) x pushed_00 exactly",
            vector(probe["pushed"]),
            scaled(pushed_00, factor),
        )
        ratio_ok = True
        ratio: Fraction | None = None
        if sign:
            expected = Fraction(-big * small, SOURCE * m)
            for t in base:
                gravity = scaled(base[t][1], m)
                electric = tuple(p - g for p, g in zip(reads[t][1], gravity, strict=True))
                for axis in range(3):
                    if gravity[axis]:
                        ratio = Fraction(electric[axis], gravity[axis])
                        ratio_ok = ratio_ok and ratio == expected
            checks.equal(
                f"{name}: electric / gravity = -Qq / (M m) = {expected} on every axis of every record",
                ratio_ok,
                True,
            )
        lines.append(
            f"{name} | {big} | {small} | {m} | {len(reads)} | ({factor}) x push_00 | {vector(probe['pushed'])} | {ratio if sign else 'no charge'}"
        )
    pp, pp4 = runs["7_pp"].reads(2, 1), runs["7_pp_m4"].reads(2, 1)
    electric_1 = {t: tuple(p - g for p, g in zip(pp[t][1], base[t][1], strict=True)) for t in base}
    electric_4 = {
        t: tuple(p - g for p, g in zip(pp4[t][1], scaled(base[t][1], 4), strict=True)) for t in base
    }
    checks.equal(
        "7: the electric part of the content-4 probe equals its content-1 twin's at every record",
        electric_4,
        electric_1,
    )
    checks.equal(
        "7: the electric part is the flow (-push_00) at every record",
        all(electric_1[t] == scaled(base[t][1], -1) for t in base),
        True,
    )
    return lines


def convergence(values: dict[str, float], checks: Checks) -> list[str]:
    lines = ["convergence", ""]
    lines.append(
        f"(a) the flow x 2 pi r / q over r >= 5: mean {values['flow_mean']:.4f} (min {values['flow_min']:.4f}, max "
        f"{values['flow_max']:.4f}): Gauss's constant of a ballistic stream; the mean stay of a ray at a Node "
        f"(presence / count) {values['stay_mean']:.4f} against 1 / c = {STAY:.4f}"
    )
    checks.reading(
        "(a) flow x 2 pi r / q flat within 10 % over r >= 5",
        values["flow_max"] / values["flow_min"] - 1,
        0.0,
        0.10,
    )
    lines.append(
        "(b) see item 6: the count owed is the presence read, replayed exactly; on the axis it does not fall with r."
    )
    lines.append(
        f"(c) |slope_count - slope_flow| = {abs(values['slope_count'] - values['slope_flow']):.3f}; |slope_presence - slope_count| = {abs(values['slope_presence'] - values['slope_count']):.3f}"
    )
    checks.within(
        "(c) |slope_count - slope_flow| <= 0.10",
        abs(values["slope_count"] - values["slope_flow"]),
        0.0,
        0.10,
    )
    checks.reading(
        "(c) |slope_presence - slope_count| <= 0.10",
        abs(values["slope_presence"] - values["slope_count"]),
        0.0,
        0.10,
    )
    lines.append("(d) see item 7: electric / gravity = -Qq / (M m) per arrival exactly.")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "root",
        type=Path,
        nargs="?",
        default=Path("artifacts/coupling"),
        help="the folder holding the run folders",
    )
    args = parser.parse_args(argv)
    folders = find_runs(args.root)
    if not folders:
        parser.error(f"no run folder (a folder with run.json) under {args.root}")
    checks = Checks()
    runs: dict[str, Run] = {}
    for folder in folders:
        run = load(folder)
        if run.name in runs:
            raise ValueError(f"two runs of {run.name}: {runs[run.name].folder} and {folder}")
        runs[run.name] = run
        common_checks(run, checks)
    fingerprints = {str(run.record["source_sha256"]) for run in runs.values()}
    checks.equal("one source fingerprint over the runs", len(fingerprints), 1)
    print(
        "runs:",
        ", ".join(
            f"{name} ({run.ticks} ticks, {float(run.record['elapsed_seconds']):.1f} s)"
            for name, run in runs.items()
        ),
    )
    print("source_sha256:", ", ".join(sorted(fingerprints)))
    print()
    sections: list[list[str]] = []
    sections.append(item_1(runs, checks))
    sections.append(item_2(runs, checks))
    sections.append(item_3(runs, checks))
    sections.append(item_4(runs, checks))
    replay = replay_world_5(runs["5"], FAR_WINDOW)
    lines, values = item_5(runs["5"], replay, checks)
    sections.append(lines)
    if "5_long" in runs:
        long_replay = replay_world_5(runs["5_long"], FAR_WINDOW)
        lines, _ = item_5(runs["5_long"], long_replay, checks, "5_long", pinned=False)
        sections.append(lines)
    sections.append(axis_probes(runs["5p"], replay, checks, "5p"))
    sections.append(item_6(runs, replay, checks))
    sections.append(item_7(runs, checks))
    sections.append(convergence(values, checks))
    for section in sections:
        print("\n".join(section))
        print()
    for name, ok, detail in checks.rows:
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")
    print()
    for name, ok, detail in checks.readings:
        print(f"{'INSIDE ' if ok else 'OUTSIDE'}  {name}: {detail}")
    print()
    print(
        f"{len(checks.rows) - checks.failed} criteria passed, {checks.failed} failed; "
        f"{len(checks.readings) - checks.outside} readings inside the expectation, "
        f"{checks.outside} outside (registered, not moved)"
    )
    return 1 if checks.failed else 0


if __name__ == "__main__":
    sys.exit(main())
