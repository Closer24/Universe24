"""The readings of the orbit series D under the law of the ray, on the
plane, with the width of the push.

Reads the run folders of the worlds of `examples/events/orbit/` (the
runner's `run.json` and `events.jsonl`, the folders told apart by the
`model` of their record, `rays-orbit-s<S>-r<r>-plane-v1`) and prints, per
run, the probe's orbit read from its `step` records: whether it closed
(the first tick at which the angle about the source, unwrapped, reaches
2 pi, the probe then within one Link of its start on each axis and its
momentum's y component of the initial sign), its period T (that tick), the
mean radius over the orbit, the drift per orbit (the radius at the closing
tick less the radius at the previous one), the second and later orbits the
same way, the mean inward push per interval from the probe's `read`
records, in label units divided by Q = `LABEL_SCALE` = 64, against
m x q x L / (2 pi r) (the constant C of the derivation; L the mean label
magnitude of the source's fan in units of Q, the mean |u_d| / Q over its
directions with u_d the unit vector of the direction at the scale Q,
1.0000 for this fan within 1 %: since 2026-09-19 the push of a fan ray is
its label along u_d, RAY_LAW section 2 and note 23; the momentum column p
is in label units, 64 per unit of the probe's content), the
least and greatest radius, the escape or the refused step if any; and, per
width, the ratio T(24)^2 / T(12)^2 against (24 / 12)^2 = 4, the plane's
1 / r force (T proportional to r, k = 2; Kepler's k = 3 would give 8). The
record checks (completed, the books balanced at every tick) fail the tool;
the orbit readings are registered inside or outside their expectation
(docs/EXPERIMENTS.md, "D, the orbit under the law of the ray, on the plane
(2026-09-19)") and never moved.

    PYTHONPATH=src python tools/orbit_readings.py artifacts/orbit
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

from event_universe.events import parse_ray_world
from event_universe.events.engine import by_clock
from event_universe.events.nature_beam import flight_table
from event_universe.events.world import LABEL_SCALE, MeasuredDefinition, RayWorld
from event_universe.json_documents import parse_json_document

# Every rule of the engine this tool needs is read off the engine's own
# functions (the architecture review of 2026-09-20, Highlights 5.4: a tool
# is a reader of the record, never a second owner of a rule): the release
# off the clock `engine.by_clock`, the fan's labels off the flight table
# `nature_beam.flight_table`, the scale `world.LABEL_SCALE`, the world's
# keys and the source's Node through `parse_ray_world`.
MODEL_PREFIX = "rays-orbit-"
MODEL_SUFFIX = "-plane-v1"
# The numbers of the source and the probe in the world's declaration order.
SOURCE = 1
PROBE = 2
FULL_TURN = 2 * math.pi


def fan_emission(world: RayWorld, source: MeasuredDefinition) -> float:
    """The source's mean emission per interval over its fan: per declared
    direction the engine's release off the clock, `by_clock(age, content x
    n, d)` at `release` [n, d] (nature_beam, step 5; a free family's
    release costs nothing, so the content is constant), averaged over one
    period of d ages, which is content x n / d exactly, times the number of
    directions."""
    numerator, denominator = world.release
    per_direction = Fraction(
        sum(by_clock(age, source.amount * numerator, denominator) for age in range(denominator)),
        denominator,
    )
    return float(len(source.directions) * per_direction)


def fan_label(world: RayWorld, source: MeasuredDefinition) -> float:
    """The mean label magnitude of the source's fan in units of Q: the mean
    |u_d| / Q over its declared directions, u_d the label of one unit
    along d off the engine's flight table (`FlightTable.labels`, the unit
    vector of the direction at the scale Q)."""
    labels = flight_table(world.directions).labels
    return sum(
        math.hypot(*(int(v) for v in labels[direction])) / LABEL_SCALE for direction in source.directions
    ) / len(source.directions)


@dataclass
class Orbit:
    """One closing of the angle: the tick, the return distance on each
    axis, the heading sign kept, the mean radius over the orbit, the radius
    at the closing tick."""

    index: int
    tick: int
    return_x: int
    return_y: int
    heading_kept: bool
    mean_radius: float
    radius: float
    intervals: int = 0
    reads: int = 0
    units: int = 0
    inward_push: float = 0.0
    # The mean inward push per interval over this orbit divided by
    # q / (2 pi r_mean) (m = 1): the constant C measured on the orbit.
    constant: float = 0.0
    profile: list[float] = field(default_factory=list)

    @property
    def closed(self) -> bool:
        return max(abs(self.return_x), abs(self.return_y)) <= 1 and self.heading_kept


@dataclass
class Reading:
    name: str
    width: int
    radius: int
    momentum: int
    emission: float
    # The mean label magnitude of the source's fan in units of Q (the mean
    # |u_d| / Q over its directions).
    label: float
    ticks: int
    completed: bool
    balanced: bool
    elapsed: float
    orbits: list[Orbit] = field(default_factory=list)
    turns: float = 0.0
    least_radius: float = 0.0
    greatest_radius: float = 0.0
    final_radius: float = 0.0
    reads: int = 0
    units: int = 0
    inward_push: float = 0.0
    ended: str = ""

    @property
    def period(self) -> int | None:
        return self.orbits[0].tick if self.orbits else None

    @property
    def push_constant(self) -> float:
        """The mean inward push per interval over the run (in units of Q)
        divided by m q L / (2 pi r_mean): the constant C measured."""
        mean_radius = self.orbits[0].mean_radius if self.orbits else self.final_radius
        if not mean_radius or not self.ticks:
            return 0.0
        return (self.inward_push / LABEL_SCALE / self.ticks) / (
            self.emission * self.label / (FULL_TURN * mean_radius)
        )


def read_run(folder: Path) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    model = str(record["model"])
    name = model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)]
    width_part, radius_part = name.split("-")
    width, radius = int(width_part[1:]), int(radius_part[1:])
    # The world as the engine parses it: the source (number 1) and the probe
    # (number 2), the source's Node the centre of the orbit.
    world = parse_ray_world(parse_json_document((folder / "initialization.json").read_bytes()))
    source, probe = world.measured[SOURCE - 1], world.measured[PROBE - 1]
    centre = (source.position[0], source.position[1])
    ticks = int(record["completed_ticks"])
    reading = Reading(
        name=name.replace("-", "_"),
        width=width,
        radius=radius,
        momentum=probe.momentum[1],
        emission=fan_emission(world, source),
        label=fan_label(world, source),
        ticks=ticks,
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        elapsed=float(record["elapsed_seconds"]),
    )
    # The trajectory: the position at every tick from the step records.
    steps: dict[int, tuple[int, int, list[int]]] = {}
    pushes: list[tuple[int, list[int]]] = []
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            event = json.loads(line)
            if event["event"] == "step" and event["number"] == PROBE:
                steps[int(event["tick"])] = (
                    int(event["to"][0]),
                    int(event["to"][1]),
                    [int(v) for v in event["momentum"]],
                )
            elif event["event"] == "read" and event["measured"] == PROBE:
                pushes.append((int(event["tick"]), [int(v) for v in event["push"]]))
            elif event["event"] == "click" and event.get("measured") == PROBE:
                reading.ended = f"escaped through {event['detector']} at tick {event['tick']}"
    start = (probe.position[0], probe.position[1])
    position = start
    momentum = list(probe.momentum)
    positions: list[tuple[int, int]] = [start]
    momenta: list[list[int]] = [momentum]
    for tick in range(1, ticks + 1):
        if tick in steps:
            x, y, momentum = steps[tick]
            position = (x, y)
        positions.append(position)
        momenta.append(momentum)
    # The angle about the source, unwrapped, and the radius per tick.
    radii = [math.hypot(x - centre[0], y - centre[1]) for x, y in positions]
    angles = []
    unwrapped = 0.0
    previous = math.atan2(positions[0][1] - centre[1], positions[0][0] - centre[0])
    for x, y in positions:
        angle = math.atan2(y - centre[1], x - centre[0])
        delta = angle - previous
        if delta > math.pi:
            delta -= FULL_TURN
        elif delta < -math.pi:
            delta += FULL_TURN
        unwrapped += delta
        angles.append(unwrapped)
        previous = angle
    reading.turns = angles[-1] / FULL_TURN
    reading.least_radius = min(radii)
    reading.greatest_radius = max(radii)
    reading.final_radius = radii[-1]
    initial_sign = 1 if momenta[0][1] > 0 else -1
    last_close = 0
    index = 0
    for tick in range(1, ticks + 1):
        if angles[tick] >= FULL_TURN * (index + 1):
            index += 1
            window = radii[last_close : tick + 1]
            samples = [window[k * (len(window) - 1) // 8] for k in range(9)]
            reading.orbits.append(
                Orbit(
                    index,
                    tick,
                    positions[tick][0] - start[0],
                    positions[tick][1] - start[1],
                    (momenta[tick][1] > 0) == (initial_sign > 0),
                    sum(window) / len(window),
                    radii[tick],
                    intervals=tick - last_close,
                    profile=samples,
                )
            )
            last_close = tick
    # The push: the inward component per record, summed over the run and
    # over the orbit the record falls in.
    closings = [orbit.tick for orbit in reading.orbits]
    for tick, push in pushes:
        x, y = positions[tick - 1]
        dx, dy = centre[0] - x, centre[1] - y
        norm = math.hypot(dx, dy)
        inward = 0.0 if not norm else (push[0] * dx + push[1] * dy) / norm
        units = abs(push[0]) + abs(push[1])
        reading.inward_push += inward
        reading.reads += 1
        reading.units += units
        for orbit, closing in zip(reading.orbits, closings, strict=True):
            if tick <= closing:
                orbit.inward_push += inward
                orbit.reads += 1
                orbit.units += units
                break
    for orbit in reading.orbits:
        expected = reading.emission * reading.label / (FULL_TURN * orbit.mean_radius)
        if expected and orbit.intervals:
            orbit.constant = (orbit.inward_push / LABEL_SCALE / orbit.intervals) / expected
    if not reading.ended and reading.least_radius <= 1.0:
        reading.ended = "reached the Node beside the source"
    return reading


def find_runs(root: Path) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        model = str(record.get("model", ""))
        if model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX):
            found.append(read_run(path.parent))
    return sorted(found, key=lambda r: (r.width, r.radius))


def print_table(readings: list[Reading]) -> None:
    print(
        "| World | S | r | p (label units) | closed | T | mean radius | drift per orbit | turns | "
        "r min .. max | reads | units (label units) | C measured | end |"
    )
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in readings:
        first = r.orbits[0] if r.orbits else None
        closed = "-" if first is None else ("yes" if first.closed else "no")
        period = "-" if first is None else str(first.tick)
        mean_radius = "-" if first is None else f"{first.mean_radius:.2f}"
        drifts = []
        previous = float(r.radius)
        for orbit in r.orbits:
            drifts.append(orbit.radius - previous)
            previous = orbit.radius
        drift = "-" if not drifts else ", ".join(f"{d:+.2f}" for d in drifts)
        constant = r.push_constant if first is None else first.constant
        print(
            f"| `{r.name}` | {r.width} | {r.radius} | {r.momentum} | {closed} | {period} | "
            f"{mean_radius} | {drift} | {r.turns:.2f} | {r.least_radius:.1f} .. "
            f"{r.greatest_radius:.1f} | {r.reads} | {r.units} | {constant:.2f} | "
            f"{r.ended or 'on the board'} |"
        )
    print()
    for r in readings:
        for o in r.orbits:
            profile = ", ".join(f"{v:.1f}" for v in o.profile)
            print(
                f"{r.name} orbit {o.index}: T {o.tick} ({o.intervals} intervals), return "
                f"({o.return_x:+d}, {o.return_y:+d}), heading "
                f"{'kept' if o.heading_kept else 'reversed'}, mean radius {o.mean_radius:.2f}, "
                f"radius at the closing {o.radius:.2f}, reads {o.reads}, units {o.units}, "
                f"C {o.constant:.2f}; the radius at eighths: {profile}"
            )


def print_ratios(readings: list[Reading]) -> None:
    by_width: dict[int, dict[int, Reading]] = {}
    for r in readings:
        by_width.setdefault(r.width, {})[r.radius] = r
    print()
    print("| S | T(12) | T(24) | T(24)^2 / T(12)^2 | expected (24 / 12)^2, k = 2 | Kepler k = 3 |")
    print("| --- | --- | --- | --- | --- | --- |")
    for width in sorted(by_width):
        pair = by_width[width]
        inner, outer = pair.get(12), pair.get(24)
        t_inner = inner.period if inner else None
        t_outer = outer.period if outer else None
        ratio = "-" if not t_inner or not t_outer else f"{(t_outer / t_inner) ** 2:.2f}"
        print(f"| {width} | {t_inner or '-'} | {t_outer or '-'} | {ratio} | 4 | 8 |")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="the folder holding the six run folders")
    args = parser.parse_args(argv)
    readings = find_runs(args.root)
    if not readings:
        print(f"no orbit run under {args.root}", file=sys.stderr)
        return 2
    failed = 0
    for r in readings:
        for label, ok in (("completed", r.completed), ("balanced", r.balanced)):
            print(f"{'PASS' if ok else 'FAIL'} {r.name}: {label}")
            failed += not ok
    print()
    print_table(readings)
    print_ratios(readings)
    print()
    print(f"{failed} record check(s) failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
