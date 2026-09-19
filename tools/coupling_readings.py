"""The readings of the coupling series C under the law of events, on the
plane.

Reads the run folders of the worlds of `examples/events/coupling/` (the
runner's `run.json`, `initialization.json` and `events.jsonl`, the folders
told apart by the `model` of their record, `events-coupling-<name>-plane-v1`),
replays world 5 (the source alone) through the engine's API for the ring
means and for the counts and sizes at the axis Nodes, and prints a table per
item and every criterion of the entry "C, the couplings under the law of
events, on the plane (2026-09-19)" in docs/EXPERIMENTS.md with its verdict; a
failed criterion exits nonzero. Every identity is checked on integers and
`fractions.Fraction`; floats appear only in the ripple bounds, the ring means
and the slopes.

The board is 121 x 121 x 1 with the z axis periodic (the model owner's
decision of 2026-09-19: the series runs on two-dimensional boards): the two
z Ports of every Node return to the same Node at the next interval, so a
Node's count and the momentum it reads include what came back through its
own stub, while the radial flow (the headings projected on the radial unit
vector of the plane) does not. The items: 1 the equivalence (the push of a
probe of content m is m times the push of content 1, record by record, and a
free probe's steps are the same for every m); 2 the third law with unequal
contents (a reading, not an identity); 3 superposition (the probe's records
by number in the world of two sources equal those of each source alone); 4
retardation (the first read of each probe against the table derived by hand
from the mixing before the run, the +x Nodes past the front registered); 5
the far field (the ring means of the count, the flow, the carried radial
momentum and the size, the flux through the square, the escape; the axis
pattern at the probes of world 5P); 6 the clock (`suspension` 1: age +
waited = 200, the ages replayed from the sizes read, no probe frozen); 7 the
electric reading (identities against the uncharged world). The probes read
(`read`: the push taken, the units mix on as at an empty Node), so the stream
of the source's number is the same in the worlds 5, 5P and 6: the replay of
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

from event_universe.events import EventSimulation, parse_event_world
from event_universe.json_documents import parse_json_document

MODEL_PREFIX = "events-coupling-"
MODEL_SUFFIX = "-plane-v1"
CENTRE = (60, 60, 0)
SOURCE = 1 << 24
RELEASE = (1, 128)
# The net emission into the plane per interval at the fixed point: 2^17 per
# Port on six Ports, the two z Ports' releases coming home and created again.
Q = 6 * (SOURCE * RELEASE[0] // RELEASE[1])
SCALE = 32  # the size is in 32nds of one unit's amplitude
FAR_RADII = (4, 6, 8, 12, 16, 20, 24, 30, 40)
FAR_FIELD = tuple(r for r in FAR_RADII if r >= 8)
FAR_WINDOW = 50
CUBE_HALVES = (4, 8, 12, 20, 40)
ITEM1_CONTENTS = (1, 4, 16)
PROBE_RADIUS = 12
PROBE_X = (CENTRE[0] + PROBE_RADIUS, CENTRE[1], CENTRE[2])
MERGED_PRIOR = 2 * PROBE_RADIUS + 1
WINDOW = 50
CHARGE = 1 << 23
PROBE_CHARGE = 2
IN_PLANE_PORTS = 4
AXES = {
    "+x": (1, 0, 0),
    "-x": (-1, 0, 0),
    "+y": (0, 1, 0),
    "-y": (0, -1, 0),
}
RETARDATION_PROBES = (("-x", 4), ("+y", 6), ("-y", 8), ("+x", PROBE_RADIUS))
# The front of the stream along each axis, derived by hand before the run
# (README: the lone-arrival chain of the mixing rule, 2^17 at r = 1 on tick
# 2, then the forward share of a lone arrival at each Node, the remainders in
# the tick's Port order): the amount of the first arrival at r, at tick
# r + 1. On +x the front is exhausted at r = 6 (its three units leave on -x
# and +y at tick 7), so the first read past it is not derived and is
# registered; on -x one unit goes on whole by its momentum from r = 7, on
# +y and -y two units from r = 6.
FRONT: dict[str, dict[int, int]] = {
    "+x": {1: 131072, 2: 14563, 3: 1618, 4: 180, 5: 20, 6: 3},
    "-x": {1: 131072, 2: 14563, 3: 1618, 4: 180, 5: 20, 6: 3},
    "+y": {1: 131072, 2: 14564, 3: 1618, 4: 179, 5: 20},
    "-y": {1: 131072, 2: 14564, 3: 1619, 4: 180, 5: 20},
}
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


def by_clock(age: int, numerator: int, denominator: int) -> int:
    """The engine's rate off the clock (`engine.by_clock`), restated here so
    that the record is checked against the law's arithmetic, not the module."""
    return ((age + 1) * numerator) // denominator - (age * numerator) // denominator


def step_axis(event: Record) -> int:
    origin, target = vector(event["node"]), vector(event["to"])
    return next(axis for axis in range(3) if origin[axis] != target[axis])


def steps_by_rule(reads: Reads, m: int, first: int, last: int) -> list[tuple[int, int]]:
    """The (tick, axis) at which a free probe of content m steps by the rule
    of the engine's step 6 on the record: its momentum is the cumulative
    push of its reads (born at rest), at tick t after that tick's read the
    first axis, x before y before z, with by_clock(t - 1, |p|, m + |p|) = 1
    steps (with `suspension` 0 its age after the self-creation of tick t is
    t, so `age - 1` is t - 1); at most one step per interval."""
    momentum = [0, 0, 0]
    fired: list[tuple[int, int]] = []
    for tick in range(first, last + 1):
        if tick in reads:
            momentum = list(added((momentum[0], momentum[1], momentum[2]), reads[tick][1]))
        for axis in range(3):
            magnitude = abs(momentum[axis])
            if magnitude and by_clock(tick - 1, magnitude, m + magnitude):
                fired.append((tick, axis))
                break
    return fired


def front(axis: str, radius: int) -> tuple[int, int] | None:
    """The first read (tick, amount) of a probe at `radius` on an axis as
    derived by hand, None where the front does not reach it."""
    if radius in FRONT[axis]:
        return (radius + 1, FRONT[axis][radius])
    if axis == "-x" and radius >= 7:
        return (radius + 1, 1)
    if axis in ("+y", "-y") and radius >= 6:
        return (radius + 1, 2)
    return None


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

    def add(self, name: str, ok: bool, detail: str) -> None:
        self.rows.append((name, ok, detail))

    def equal(self, name: str, found: object, expected: object) -> None:
        self.add(name, found == expected, f"found {found}, expected {expected}")

    def within(self, name: str, found: float, low: float, high: float) -> None:
        self.add(name, low <= found <= high, f"found {found:.4f}, expected [{low}, {high}]")

    @property
    def failed(self) -> int:
        return sum(1 for _, ok, _ in self.rows if not ok)


@dataclass
class Run:
    name: str
    folder: Path
    record: Record
    world: Record
    events: list[Record]

    @property
    def ticks(self) -> int:
        return int(self.world["ticks"])

    def measured(self, number: int) -> Record | None:
        for entry in self.record["measured"]:
            if int(entry["number"]) == number:
                return dict(entry)
        return None

    def reads(self, reader: int, emitter: int) -> Reads:
        """The `read` records of one reader of one emitter's units, by tick:
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
    world = json.loads((folder / "initialization.json").read_text(encoding="utf-8"))
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        events = [json.loads(line) for line in stream if line.strip()]
    model = str(record["model"])
    if not (model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX)):
        raise ValueError(f"{folder}: not a world of the coupling series on the plane ({model})")
    name = model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)].replace("-", "_")
    return Run(name, folder, record, world, events)


# -- the identities of every world ----------------------------------------------


def common_checks(run: Run, checks: Checks) -> None:
    label = run.name
    record = run.record
    checks.equal(f"{label}: status", record["status"], "completed")
    checks.equal(f"{label}: completed ticks", record["completed_ticks"], run.ticks)
    checks.equal(
        f"{label}: the board 121 x 121 x 1 with z periodic", record["boundary"], {"z": "periodic"}
    )
    checks.equal(f"{label}: the shape", record["shape"], [121, 121, 1])
    checks.equal(
        f"{label}: the books at every completed tick", record["conserved_at_every_completed_tick"], True
    )
    checks.equal(
        f"{label}: every audit entry balanced", all(entry["balanced"] for entry in record["audit"]), True
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
            f"1a_m{m}: the first read is (tick, amount, -amount x m on +x) with 1a_m1's tick and amount",
            first,
            (base_tick, base[base_tick][0], (-base[base_tick][0] * m, 0, 0)),
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
        axial = sum(1 for a, p in reads.values() if p == (-a * m, 0, 0))
        lines.append(
            f"1a_m{m} | {m} | {len(reads)} | {first} | {pushed} | {'yes' if identity else 'NO'} "
            f"(push = (-amount x m, 0, 0) exactly at {axial} of {len(reads)} records)"
        )
    lines.append("")
    lines.append(
        "world | m | steps (ticks) | x from -> to | merged (tick, into, amount) | source content after "
        "| momentum = m x momentum_1 at every step | reads (push = m x push_1)"
    )
    lines.append(" | ".join("---" for _ in range(8)))
    base_steps = [e for e in runs["1b_m1"].events if e["event"] == "step"]
    base_reads = runs["1b_m1"].reads(2, 1)
    merged_ticks: list[int] = []
    for m in ITEM1_CONTENTS:
        run = runs[f"1b_m{m}"]
        steps = [e for e in run.events if e["event"] == "step"]
        merged = [e for e in run.events if e["event"] == "merged"]
        ticks = [int(e["tick"]) for e in steps]
        checks.equal(
            f"1b_m{m}: the step records (tick, node, to) identical to 1b_m1",
            [(e["tick"], e["node"], e["to"]) for e in steps],
            [(e["tick"], e["node"], e["to"]) for e in base_steps],
        )
        reads = run.reads(2, 1)
        merged_at = [int(e["tick"]) for e in merged]
        last = merged_at[0] if merged_at else run.ticks
        checks.equal(
            f"1b_m{m}: the steps (tick, axis) and the merge are the rule off the clock on the reads' cumulative push",
            [(int(e["tick"]), step_axis(e)) for e in steps] + [(tick, 0) for tick in merged_at],
            steps_by_rule(reads, m, min(reads), last),
        )
        checks.equal(
            f"1b_m{m}: one x-step per interval from the first step to the merge, x {PROBE_X[0]} down to {CENTRE[0] + 1}",
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
        merged_row = [
            (int(e["tick"]), int(e["measured"]), int(e["number"]), int(e["amount"])) for e in merged
        ]
        checks.equal(
            f"1b_m{m}: one merged record into the source (number 1) with amount m",
            [(measured, number, amount) for _, measured, number, amount in merged_row],
            [(2, 1, m)],
        )
        checks.equal(
            f"1b_m{m}: the merge at the tick after the last step",
            [tick for tick, _, _, _ in merged_row],
            [ticks[-1] + 1] if ticks else [],
        )
        merged_ticks.extend(tick for tick, _, _, _ in merged_row)
        checks.equal(
            f"1b_m{m}: the probe absent afterwards, the source alone",
            [int(e["number"]) for e in run.record["measured"]],
            [1],
        )
        source = run.measured(1)
        assert source is not None
        checks.equal(f"1b_m{m}: the source's content 2^24 + m", int(source["content"]), SOURCE + m)
        checks.equal(
            f"1b_m{m}: measured content 2^24 + m at every tick",
            run.record["measured_content"][-1],
            [SOURCE + m],
        )
        same_momentum = [vector(e["momentum"]) for e in steps] == [
            scaled(vector(e["momentum"]), m) for e in base_steps
        ]
        lines.append(
            f"1b_m{m} | {m} | {len(steps)} ({ticks[0] if ticks else None}..{ticks[-1] if ticks else None}) "
            f"| {vector(steps[0]['node'])[0] if steps else None} -> {vector(steps[-1]['to'])[0] if steps else None} "
            f"| {merged_row[0] if merged_row else None} | {int(source['content'])} "
            f"| {'yes' if same_momentum else 'NO'} | {len(reads)}"
        )
    checks.equal("1b: the same merged tick for the three m", len(set(merged_ticks)), 1)
    first_step = min(int(e["tick"]) for e in base_steps) if base_steps else None
    lines.append("")
    lines.append(
        f"the first read at tick {base_tick} with amount {base[base_tick][0]} (registered, not derived: the "
        f"front on +x is exhausted at r = 6); the first step at tick {first_step} (the rule off the clock: "
        f"by_clock(t - 1, |p|, m + |p|) on the cumulative push p, 0 at the first read of one unit, p / (m + p) "
        f"= 1 / 2); the merge at tick {sorted(set(merged_ticks))} (the 3-D prior 2r + 1 = {MERGED_PRIOR})"
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
    ratios: dict[int, Fraction] = {}
    windows = [(1 + k * WINDOW, (k + 1) * WINDOW) for k in range(run.ticks // WINDOW)]
    for index, (first, last) in enumerate(windows, start=1):
        wa, wb = run.window_push(on_a, first, last), run.window_push(on_b, first, last)
        ratio = Fraction(abs(wa[0]), abs(wb[0])) if wb[0] else Fraction(0)
        ratios[index] = ratio
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
    last_two = list(ratios)[-2:]
    for index in last_two:
        checks.within(
            f"2: |P_A,x| / |P_B,x| over window {index} in [1.0, 1.5]", float(ratios[index]), 1.0, 1.5
        )
    r3, r4 = ratios[last_two[0]], ratios[last_two[1]]
    checks.within(
        "2: the ratio of the last two windows within 5 % of each other",
        abs(float(r3 / r4) - 1),
        0.0,
        0.05,
    )
    for name, p in (("A", p_a), ("B", p_b)):
        transverse = max(abs(p[1]), abs(p[2])) / abs(p[0])
        checks.within(f"2: transverse / axial of P_{name} below 5 %", transverse, 0.0, 0.05)
        lines.append(f"transverse / axial of P_{name}: {transverse:.4f}")
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
    lines.append("world | axis | r | Node | found (tick, amount, push) | derived by hand (tick, amount)")
    lines.append(" | ".join("---" for _ in range(6)))
    rows: list[tuple[str, str, int, int]] = [
        ("4", axis, r, k + 2) for k, (axis, r) in enumerate(RETARDATION_PROBES)
    ]
    rows.append(("1a_m1", "+x", PROBE_RADIUS, 2))
    rows.append(("7_00", "+x", PROBE_RADIUS, 2))
    rows += [("5p", "+x", r, k + 2) for k, r in enumerate(FAR_RADII)]
    rows += [("6", "+x", r, k + 2) for k, r in enumerate(FAR_RADII)]
    registered: dict[int, set[tuple[int, int]]] = {}
    for name, axis, r, reader in rows:
        run = runs[name]
        probe = run.measured(reader)
        assert probe is not None and vector(probe["position"]) == at(axis, r), (name, reader)
        found = first_read(run, reader)
        heading = AXES[axis]
        expected = front(axis, r)
        checks.equal(
            f"{name}: the first read of the probe at r = {r} on {axis} pushes -amount x m along the axis",
            found[2],
            scaled(heading, -found[1] * int(probe["content"])),
        )
        if expected is not None:
            checks.equal(
                f"{name}: the first read of the probe at r = {r} on {axis} is the front derived by hand",
                found[:2],
                expected,
            )
        else:
            registered.setdefault(r, set()).add(found[:2])
        lines.append(
            f"{name} | {axis} | {r} | {at(axis, r)} | {found} | {expected if expected else 'registered'}"
        )
    for r, values in sorted(registered.items()):
        checks.equal(
            f"4: the same first read (tick, amount) at r = {r} on +x in every world that holds a probe there",
            len(values),
            1,
        )
    lines.append("")
    lines.append(
        "registered on +x past the front: "
        + "; ".join(f"r = {r}: {sorted(values)}" for r, values in sorted(registered.items()))
    )
    return lines


# -- item 5: the far field, and the replay of world 5 ------------------------------


@dataclass
class Replay:
    """What the replay of world 5 through the API reads: per tick the count
    and the size at the +x axis Nodes (for 5P and 6), and over the last
    window the ring means, the flux through the square and the escape."""

    ticks: int
    nodes: dict[int, int]
    count_at: dict[int, list[int]]
    size_at: dict[int, list[int]]
    ring: dict[str, dict[int, float]]
    cube: dict[int, float]
    escape: float
    window: tuple[int, int]
    audit_matches: bool


def replay_world_5(run: Run, window: int) -> Replay:
    world = parse_event_world(parse_json_document((run.folder / "initialization.json").read_bytes()))
    simulation = EventSimulation(world)
    ticks = world.ticks
    first = ticks - window + 1
    grid = np.indices(world.shape).reshape(3, -1).T - np.array(CENTRE)
    distance = np.sqrt((grid * grid).sum(axis=1))
    rings: dict[int, tuple[Any, Any]] = {}
    nodes: dict[int, int] = {}
    for r in FAR_RADII:
        chosen = (np.abs(distance - r) < 0.5) & (distance > 0)
        positions = grid[chosen]
        radial = positions / distance[chosen][:, None]
        rings[r] = (tuple((positions + np.array(CENTRE)).T), radial)
        nodes[r] = int(chosen.sum())
    count_at: dict[int, list[int]] = {r: [] for r in FAR_RADII}
    size_at: dict[int, list[int]] = {r: [] for r in FAR_RADII}
    keys = ("count", "flow", "carried", "carried_plane", "size")
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
            count_at[r].append(int(simulation.count[0][node]))
            size_at[r].append(int(simulation.size[0][node].sum()))
        if tick >= first:
            fly_mom = simulation.transits[0].fly_mom
            departing = fly_mom.sum(axis=(3, 4))
            in_plane = fly_mom[..., :IN_PLANE_PORTS, :].sum(axis=(3, 4))
            for r in FAR_RADII:
                reading = simulation.shell_readings(0, CENTRE, r)
                sums["count"][r] += reading["count"]
                sums["flow"][r] += reading["flow"]
                sums["size"][r] += reading["size"]
                cells, radial = rings[r]
                sums["carried"][r] += float((departing[cells] * radial).sum(axis=1).mean())
                sums["carried_plane"][r] += float((in_plane[cells] * radial).sum(axis=1).mean())
            for h in CUBE_HALVES:
                cube[h] += simulation.cube_flux(0, CENTRE, h)
    ring = {key: {r: value / window for r, value in per_r.items()} for key, per_r in sums.items()}
    escaped = run.escaped_by_tick(world.families[0].name)
    escape = (escaped[ticks - 1] - escaped[first - 2]) / window / Q
    return Replay(
        ticks,
        nodes,
        count_at,
        size_at,
        ring,
        {h: v / window / Q for h, v in cube.items()},
        escape,
        (first, ticks),
        audit_matches,
    )


def item_5(
    run: Run, replay: Replay, checks: Checks, label: str = "5", pinned: bool = True
) -> tuple[list[str], dict[str, float]]:
    """The far field of one world of the source alone: the pinned world 5
    with every criterion, or the supplementary 5_long (1000 intervals, added
    after world 5 read an escape below 0.95 q) with the escape alone and the
    escape per 100-interval window off its audit."""
    checks.equal(
        f"{label}: the replay's books equal the record's audit at every tick", replay.audit_matches, True
    )
    first, last = replay.window
    lines = [
        f"item 5, the far field (world {label}, the source alone, the ring means over ticks {first}-{last}; q = {Q})"
        + ("" if pinned else " (supplementary, not pinned: the escape's approach to q)"),
        "",
    ]
    lines.append(
        "r | Nodes | count x r / q | flow x 2 pi r / q | carried x 2 pi r / q (six Ports) "
        "| carried x 2 pi r / q (the four in-plane Ports) | size x sqrt r / sqrt q"
    )
    lines.append(" | ".join("---" for _ in range(7)))
    keys = ("count", "flow", "carried", "carried_plane", "size")
    scaled_readings: dict[str, list[float]] = {key: [] for key in keys}
    for r in FAR_RADII:
        count = replay.ring["count"][r] * r / Q
        flow = replay.ring["flow"][r] * 2 * math.pi * r / Q
        carried = replay.ring["carried"][r] * 2 * math.pi * r / Q
        carried_plane = replay.ring["carried_plane"][r] * 2 * math.pi * r / Q
        size = replay.ring["size"][r] * math.sqrt(r) / math.sqrt(Q)
        for key, value in (
            ("count", count),
            ("flow", flow),
            ("carried", carried),
            ("carried_plane", carried_plane),
            ("size", size),
        ):
            scaled_readings[key].append(value)
        lines.append(
            f"{r} | {replay.nodes[r]} | {count:.4f} | {flow:.4f} | {carried:.4f} | {carried_plane:.4f} | {size:.4f}"
        )
    far = [FAR_RADII.index(r) for r in FAR_FIELD]
    slopes = {key: slope(FAR_RADII, [replay.ring[key][r] for r in FAR_RADII]) for key in keys}
    lines.append("")
    lines.append(
        f"log-log slopes over r = {FAR_RADII}: count {slopes['count']:.3f}, flow {slopes['flow']:.3f}, "
        f"carried {slopes['carried']:.3f} (in-plane Ports {slopes['carried_plane']:.3f}), size {slopes['size']:.3f}"
    )
    lines.append(
        "flux through the square (the four in-plane faces; the z faces have no outside Node) / q at h = "
        + ", ".join(f"{h}: {replay.cube[h]:.4f}" for h in CUBE_HALVES)
    )
    lines.append(f"escape per interval over the window / q: {replay.escape:.4f}")
    if pinned:
        for key, name in (("count", "count x r / q"), ("size", "size x sqrt r / sqrt q")):
            checks.within(
                f"{label}: {name} a constant over r >= {FAR_FIELD[0]} (max / min - 1 <= 0.10)",
                ripple([scaled_readings[key][i] for i in far]),
                0.0,
                0.10,
            )
        for key, name in (("flow", "flow x 2 pi r / q"), ("carried", "carried x 2 pi r / q")):
            for i in far:
                checks.within(
                    f"{label}: {name} about 1 in the far field, r = {FAR_RADII[i]} in [0.90, 1.10]",
                    scaled_readings[key][i],
                    0.90,
                    1.10,
                )
        checks.within(f"{label}: slope of the count -1.00 +- 0.10", slopes["count"], -1.10, -0.90)
        checks.within(f"{label}: slope of the flow -1.00 +- 0.15", slopes["flow"], -1.15, -0.85)
        checks.within(
            f"{label}: slope of the carried momentum -1.00 +- 0.15", slopes["carried"], -1.15, -0.85
        )
        checks.within(f"{label}: slope of the size -0.50 +- 0.10", slopes["size"], -0.60, -0.40)
        for h in CUBE_HALVES:
            checks.within(
                f"{label}: flux through the square / q at h = {h} within 2 % of 1 (Gauss)",
                replay.cube[h],
                0.98,
                1.02,
            )
    else:
        escaped = run.escaped_by_tick(str(run.world["families"][0]["name"]))
        per_window = [
            (escaped[end - 1] - (escaped[end - 101] if end > 100 else 0)) / 100 / Q
            for end in range(100, run.ticks + 1, 100)
        ]
        lines.append(
            "escape per interval / q over the 100-interval windows ending at "
            + ", ".join(
                f"{end}: {value:.4f}"
                for end, value in zip(range(100, run.ticks + 1, 100), per_window, strict=True)
            )
        )
    checks.within(
        f"{label}: escape per interval over the window in [0.95, 1.00] of q", replay.escape, 0.95, 1.00
    )
    flat = [i for i, r in enumerate(FAR_RADII) if r >= 5]
    kappa_values = [scaled_readings["carried"][i] for i in flat]
    flow_values = [scaled_readings["flow"][i] for i in flat]
    convergence = {
        "kappa": sum(kappa_values) / len(kappa_values),
        "kappa_min": min(kappa_values),
        "kappa_max": max(kappa_values),
        "kappa_plane": sum(scaled_readings["carried_plane"][i] for i in flat) / len(flat),
        "flow_mean": sum(flow_values) / len(flow_values),
        "flow_min": min(flow_values),
        "flow_max": max(flow_values),
        **{f"slope_{key}": value for key, value in slopes.items()},
    }
    return lines, convergence


def axis_probes(run: Run, replay: Replay, checks: Checks, label: str) -> list[str]:
    """The probes of 5P (and 6) on +x: the identity with the replay of world
    5 tick by tick, and the axis readings over the last window."""
    last = run.ticks
    first = last - FAR_WINDOW + 1
    lines = [
        f"{label}: the probes on +x, the axis pattern over ticks {first}-{last} (a pattern, not the law)",
        "",
    ]
    lines.append(
        "r | Node | reads | count = replay count at every tick | -push_x x 2 pi r / (m q) "
        "| count x r / q | size x sqrt r / sqrt q (replay) | push per interval"
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
        size = sum(replay.size_at[r][first - 1 : last]) / FAR_WINDOW / SCALE
        axial = -push[0] / FAR_WINDOW * 2 * math.pi * r / (m * Q)
        lines.append(
            f"{r} | {at('+x', r)} | {len(reads)} | {'yes' if same else 'NO'} | {axial:.4f} "
            f"| {count * r / Q:.4f} | {size * math.sqrt(r) / math.sqrt(Q):.4f} "
            f"| {tuple(v / FAR_WINDOW for v in push)}"
        )
    return lines


# -- item 6: the clock -----------------------------------------------------------


def item_6(runs: dict[str, Run], replay: Replay, checks: Checks) -> list[str]:
    run = runs["6"]
    width = int(run.world["suspension"])
    checks.equal("6: suspension 1", width, 1)
    source = run.measured(1)
    assert source is not None
    lines = axis_probes(run, replay, checks, "6")
    lines += [
        "",
        f"the source: age {int(source['age'])}, waited {int(source['waited'])} "
        "(its own number's returns through its stub are not read)",
        "the clock: age(200) replayed from the sizes read (k_t = size x 1 // 32 at each self-creation)",
        "",
    ]
    lines.append(
        "r | age(200) | waited | owed | replay (age, waited, owed) | last count written (tick) | age(60) "
        "| lost 1 - age/200 | k (window mean) | k / (k + 1) | (200 - first read) / (k + 1)"
    )
    lines.append(" | ".join("---" for _ in range(11)))
    lost_by_r: list[float] = []
    for k_index, r in enumerate(FAR_RADII):
        reader = k_index + 2
        probe = run.measured(reader)
        assert probe is not None
        age, waited, owed = 0, 0, 0
        age_60 = 0
        written = (0, 0)
        for tick in range(1, run.ticks + 1):
            if owed > 0:
                owed -= 1
                waited += 1
            else:
                age += 1
                owed = replay.size_at[r][tick - 1] * width // SCALE
                written = (owed, tick)
            if tick == 60:
                age_60 = age
        found = (int(probe["age"]), int(probe["waited"]), int(probe["owed"]))
        checks.equal(f"6: age + waited = 200 at r = {r}", found[0] + found[1], run.ticks)
        checks.equal(
            f"6: (age, waited, owed) at r = {r} equal the replay of the counts read",
            found,
            (age, waited, owed),
        )
        checks.equal(f"6: not frozen at r = {r}: age(200) > age(60)", found[0] > age_60, True)
        checks.equal(
            f"6: the probe at r = {r} released nothing (age below 128), so the stream is world 5's",
            found[0] < 128,
            True,
        )
        first, last = run.ticks - FAR_WINDOW + 1, run.ticks
        k_mean = sum(replay.size_at[r][first - 1 : last]) / FAR_WINDOW * width / SCALE
        lost = 1 - found[0] / run.ticks
        lost_by_r.append(lost)
        arrival = first_read(run, reader)[0]
        lines.append(
            f"{r} | {found[0]} | {found[1]} | {found[2]} | {(age, waited, owed)} | {written} | {age_60} | {lost:.4f} "
            f"| {k_mean:.2f} | {k_mean / (k_mean + 1):.4f} | {(run.ticks - arrival) / (k_mean + 1):.2f}"
        )
    checks.equal(
        "6: the lost fraction falls with r (the size is ~1/sqrt r on the plane)",
        all(a > b for a, b in zip(lost_by_r[:-1], lost_by_r[1:], strict=True)),
        True,
    )
    checks.equal(
        "6: the source's clock unslowed (no other number's size at c): age 200, waited 0",
        (int(source["age"]), int(source["waited"])),
        (run.ticks, 0),
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
        checks.equal(
            f"{name}: the declared charges (Q, q)",
            (
                int(run.world["measured"][0].get("charge", 0)),
                int(run.world["measured"][1].get("charge", 0)),
            ),
            (big, small),
        )
        reads = run.reads(2, 1)
        checks.equal(
            f"{name}: the same ticks and amounts as 7_00",
            {t: a for t, (a, _) in reads.items()},
            {t: a for t, (a, _) in base.items()},
        )
        sign = (1 if big * small > 0 else -1) if big * small else 0
        # gravity -m c, electric sign(Qq) c with c = -push_00: the total
        # (sign - m) x (-push_00) = (m - sign) x push_00.
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
            f"{name} | {big} | {small} | {m} | {len(reads)} | ({factor}) x push_00 "
            f"| {vector(probe['pushed'])} | {ratio if sign else 'no charge'}"
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
        "7: the electric part is the carried momentum (-push_00) at every record",
        all(electric_1[t] == scaled(base[t][1], -1) for t in base),
        True,
    )
    return lines


def convergence(values: dict[str, float], checks: Checks) -> list[str]:
    kappa = values["kappa"]
    lines = ["convergence", ""]
    lines.append(
        f"(a) G_push on the plane: the constant of carried x 2 pi r / q over r >= 5: {kappa:.4f} "
        f"(min {values['kappa_min']:.4f}, max {values['kappa_max']:.4f}; the four in-plane Ports alone "
        f"{values['kappa_plane']:.4f}); the flow's mean {values['flow_mean']:.4f} "
        f"(min {values['flow_min']:.4f}, max {values['flow_max']:.4f}). G from step rates is unreadable "
        "on this board: every free probe steps one Link per interval (item 1B); the equivalence identity "
        "is what is readable."
    )
    checks.within(
        "(a) carried x 2 pi r / q flat within 5 % over r >= 5",
        values["kappa_max"] / values["kappa_min"] - 1,
        0.0,
        0.05,
    )
    checks.within(
        "(a) carried x 2 pi r / q equal to the flow's within 5 %",
        abs(kappa / values["flow_mean"] - 1),
        0.0,
        0.05,
    )
    lines.append(
        "(b) see item 6: the lost fraction per r against k / (k + 1) with k = size x width // 32; the "
        "suspension reads an amplitude, the size ~ sqrt(count), so the slowing scales as sqrt(M), on "
        "the plane as sqrt(M / r), while a potential is proportional to the count."
    )
    lines.append(
        f"(c) |slope_count - slope_flow| = {abs(values['slope_count'] - values['slope_flow']):.3f}; "
        f"|2 slope_size - slope_count| = {abs(2 * values['slope_size'] - values['slope_count']):.3f}; "
        f"|slope_carried - slope_flow| = {abs(values['slope_carried'] - values['slope_flow']):.3f}"
    )
    checks.within(
        "(c) |slope_count - slope_flow| <= 0.10",
        abs(values["slope_count"] - values["slope_flow"]),
        0.0,
        0.10,
    )
    checks.within(
        "(c) |2 slope_size - slope_count| <= 0.15",
        abs(2 * values["slope_size"] - values["slope_count"]),
        0.0,
        0.15,
    )
    checks.within(
        "(c) |slope_carried - slope_flow| <= 0.15",
        abs(values["slope_carried"] - values["slope_flow"]),
        0.0,
        0.15,
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
    folders = sorted(path for path in args.root.iterdir() if (path / "run.json").exists())
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
            f"{name} ({run.ticks} ticks, {float(run.record['elapsed_seconds']):.0f} s)"
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
    print(f"{len(checks.rows) - checks.failed} criteria passed, {checks.failed} failed")
    return 1 if checks.failed else 0


if __name__ == "__main__":
    sys.exit(main())
