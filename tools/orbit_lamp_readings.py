"""The readings of series D3, Newton after a detector: series D's circular
orbit on the plane read by a lamp on the probe and a line of one-Node
detectors (docs/EXPERIMENTS.md, "D3, Newton after a detector";
examples/events/orbit_lamp/make_worlds.py, the pins in its
`expectations.json`, written before the runs).

Reads the run folders of the five worlds (the runner's `run.json` for the
record checks and `events.jsonl` for the reading, told apart by the
`model` of the record, `rays-orbit-lamp-<name>-plane-v1`) and prints two
kinds of number, each line labelled (the model owner, 2026-09-21, record
281: only a detector's reading is a measurement; a GameBoard reading is a
diagnostic, never pinned):

- DETECTOR readings, from the `click` lines of the detector line alone
  (`line_<x>`, the rows of the lamp's family): each click's x (the
  detector's column, the probe's x at the row's birth, the row keeping its
  x on the heading -y), its tick and its age (the flight; the wall's entry
  reads `age`), so the birth tick is the tick less the age and the clicks
  give x(t), one sample per birth. From them: the count, the range of x
  and its amplitude (max - min) / 2 (the orbit's radius) and its middle,
  the period T as the recurrence of x(t) (the mean spacing of successive
  crossings of the centre column in one direction, each crossing's tick
  interpolated between the two births that bracket it), the angular rate
  squared omega^2 from the lagged second difference (x(t + h) - 2 x(t) +
  x(t - h) = -4 sin^2(omega h / 2) (x(t) - c_x): the slope of the second
  difference against x - c_x over every sample with both neighbours at the
  lag h, then omega = (2 / h) asin(sqrt(-slope) / 2)), the acceleration a
  = omega^2 r with r the clicks' amplitude, the ages' range, and, in a
  control, the escape of the probe through a face (the face's `click`
  line naming the probe's number under `measured`). Across the worlds: the
  ratio T(24) / T(12) and the equivalence (the 4 M_held world's period
  against `r24`'s, and its x on every common birth tick against `r24`'s).
  Nothing of the probe's own record (its steps, its momentum, its store)
  enters a reading.
- GAMEBOARD diagnostics, printed apart and never pinned: the probe's
  position and momentum at the end of the run off `run.json`'s `measured`
  block, and the count of the record's `home` lines (a row of the probe's
  own number taken home and created again on the lamp's pair: the reason
  a birth may be read late or not at all).

The pins (`expectations.json`): T = 343 at r = 12 and 687 at r = 24 within
9 percent (the re-run of 2026-09-22 at n = 9, the per-axis drive's circle;
the first run's 371 and 742 at n = 10 stay in the register as history);
T(24) / T(12) = 2.00 +- 0.18; omega^2 = (2 pi / T)^2 within T's bracket;
the amplitude r - 1 to r + 2; the equivalence within one birth interval on
T and one Node on x; the controls' x = c_x + r on every click and the
escape near (SIDE - c_y) / v, the 61st step. The record checks (completed,
the books balanced at every tick) fail the tool; the readings are
registered inside or outside their bracket and never moved.

    PYTHONPATH=src python tools/orbit_lamp_readings.py artifacts/orbit_lamp
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from event_universe.events import parse_nature_beam_world
from event_universe.world_loading import world_of_run

ROOT = Path(__file__).resolve().parents[1]
EXPECTATIONS = ROOT / "examples" / "events" / "orbit_lamp" / "expectations.json"
MODEL_PATTERN = re.compile(r"^rays-orbit-lamp-(?P<name>.+)-plane-v1$")
DETECTOR_PREFIX = "line_"
FACE_PREFIX = "face:"
DETECTOR = "DETECTOR"
GAMEBOARD = "GAMEBOARD"
# The half-Node level the crossings are read at (never a column's own x).
LEVEL_OFFSET = 0.5

Sample = tuple[int, int]  # (the birth tick, the x)


@dataclass
class Click:
    tick: int
    x: int
    age: int

    @property
    def birth(self) -> int:
        return self.tick - self.age


@dataclass
class Crossings:
    """The crossings of the centre column by x(t) in one direction: the
    interpolated ticks and the spacings between successive ones."""

    ticks: list[float] = field(default_factory=list)

    @property
    def spacings(self) -> list[float]:
        return [b - a for a, b in zip(self.ticks, self.ticks[1:], strict=False)]


@dataclass
class Period:
    value: float | None
    down: Crossings
    up: Crossings

    @property
    def crossings(self) -> int:
        return len(self.down.ticks) + len(self.up.ticks)

    @property
    def spacings(self) -> list[float]:
        return self.down.spacings + self.up.spacings


@dataclass
class SecondDifference:
    lag: int  # in intervals
    slope: float | None
    omega_squared: float | None
    samples: int


@dataclass
class Reading:
    name: str
    folder: Path
    ticks: int
    completed: bool
    balanced: bool
    elapsed: float
    centre_x: int
    radius: int
    source: bool
    lamp_family: str
    probe_number: int
    clicks: list[Click]
    escape: tuple[str, int] | None
    homes: int
    final_position: list[int] | None
    final_momentum: list[int] | None
    initial_momentum: list[int]

    @property
    def samples(self) -> list[Sample]:
        return sorted((c.birth, c.x) for c in self.clicks)

    @property
    def xs(self) -> list[int]:
        return [c.x for c in self.clicks]

    @property
    def amplitude(self) -> float | None:
        if not self.clicks:
            return None
        return (max(self.xs) - min(self.xs)) / 2

    @property
    def middle(self) -> float | None:
        if not self.clicks:
            return None
        return (max(self.xs) + min(self.xs)) / 2


# -- The readings off a sample list (the tool's own functions, tested on a
# hand-made click list) ---------------------------------------------------


def clicks_of(lines, lamp_family: str, prefix: str = DETECTOR_PREFIX) -> list[Click]:
    """The clicks of the detector line off the record's lines: `click`
    events at a detector named `<prefix><x>` of the lamp's family, each
    with its tick, its x (the detector's column) and its age."""
    found: list[Click] = []
    for line in lines:
        if isinstance(line, str):
            if '"click"' not in line or prefix not in line:
                continue
            event = json.loads(line)
        else:
            event = line
        if event.get("event") != "click" or event.get("family") != lamp_family:
            continue
        detector = str(event.get("detector"))
        if not detector.startswith(prefix):
            continue
        found.append(Click(int(event["tick"]), int(detector[len(prefix) :]), int(event["age"])))
    return found


def crossings_of(samples: list[Sample], level: float) -> tuple[Crossings, Crossings]:
    """The downward and upward crossings of `level` by x(t) over the
    samples in order of t, each crossing's tick interpolated linearly
    between the two samples that bracket it."""
    down, up = Crossings(), Crossings()
    for (t0, x0), (t1, x1) in zip(samples, samples[1:], strict=False):
        if x0 == x1:
            continue
        if x0 > level > x1 or x0 < level < x1:
            tick = t0 + (x0 - level) / (x0 - x1) * (t1 - t0)
            (down if x0 > x1 else up).ticks.append(tick)
    return down, up


def period_of(samples: list[Sample], centre_x: int) -> Period:
    """The period as the recurrence of x(t): the mean spacing of successive
    crossings of the centre column in one direction (the down and the up
    crossings pooled, each kind weighted by its count of spacings); None
    with fewer than two crossings of one kind."""
    down, up = crossings_of(samples, centre_x + LEVEL_OFFSET)
    span = sum(c.ticks[-1] - c.ticks[0] for c in (down, up) if len(c.ticks) >= 2)
    count = sum(len(c.ticks) - 1 for c in (down, up) if len(c.ticks) >= 2)
    return Period(span / count if count else None, down, up)


def second_difference_of(samples: list[Sample], centre_x: int, lag: int) -> SecondDifference:
    """The slope of the lagged second difference of x(t) against x(t) -
    c_x over every sample with both neighbours at the lag (in intervals),
    and omega^2 from it: -4 sin^2(omega h / 2) = slope."""
    by_tick = dict(samples)
    numerator = denominator = 0.0
    count = 0
    for t, x in samples:
        before, after = by_tick.get(t - lag), by_tick.get(t + lag)
        if before is None or after is None:
            continue
        difference = after - 2 * x + before
        offset = x - centre_x
        numerator += difference * offset
        denominator += offset * offset
        count += 1
    if not count or denominator == 0:
        return SecondDifference(lag, None, None, count)
    slope = numerator / denominator
    if not 0 < -slope < 4:
        return SecondDifference(lag, slope, None, count)
    omega = 2 / lag * math.asin(math.sqrt(-slope) / 2)
    return SecondDifference(lag, slope, omega * omega, count)


def common_x_difference(a: list[Sample], b: list[Sample]) -> tuple[int, int, int]:
    """Over the birth ticks two worlds share: the count, the count with
    equal x, and the largest |x_a - x_b|."""
    by_tick = dict(a)
    shared = [(x, by_tick[t]) for t, x in b if t in by_tick]
    if not shared:
        return 0, 0, 0
    return len(shared), sum(1 for x, y in shared if x == y), max(abs(x - y) for x, y in shared)


# -- The run folders ---------------------------------------------------------


def world_name(model: str) -> str | None:
    found = MODEL_PATTERN.match(model)
    return found.group("name").replace("-", "_") if found else None


def read_run(folder: Path) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    name = world_name(str(record["model"]))
    assert name is not None
    document = world_of_run(folder)
    world = parse_nature_beam_world(document)
    probe_number, probe = next((i + 1, m) for i, m in enumerate(world.measured) if m.lamp is not None)
    lamp_family = world.families[probe.family].name
    sources = [m for m in world.measured if world.families[m.family].free and m.fixed]
    centre_x = sources[0].position[0] if sources else world.shape[0] // 2
    radius = abs(probe.position[0] - centre_x)
    clicks: list[Click] = []
    escape = None
    homes = 0
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if '"home"' in line and '"event": "home"' in line:
                homes += 1
                continue
            if '"click"' not in line:
                continue
            event = json.loads(line)
            if event.get("event") != "click":
                continue
            detector = str(event.get("detector"))
            if detector.startswith(DETECTOR_PREFIX):
                if event.get("family") == lamp_family:
                    clicks.append(
                        Click(
                            int(event["tick"]), int(detector[len(DETECTOR_PREFIX) :]), int(event["age"])
                        )
                    )
            elif detector.startswith(FACE_PREFIX) and event.get("measured") == probe_number:
                escape = (detector, int(event["tick"]))
    audit = record.get("audit")
    if isinstance(audit, list):
        balanced = all(bool(entry.get("balanced", False)) for entry in audit)
    else:
        balanced = bool(audit.get("balanced", False)) if isinstance(audit, dict) else False
    ticks = int(record["completed_ticks"])
    final_position = final_momentum = None
    for entry in record.get("measured", []):
        if int(entry.get("number", 0)) == probe_number:
            final_position = list(entry.get("position", []))
            final_momentum = list(entry.get("momentum", []))
    return Reading(
        name,
        folder,
        ticks,
        ticks == int(document["ticks"]),
        balanced,
        float(record.get("elapsed_seconds", record.get("elapsed", 0.0)) or 0.0),
        centre_x,
        radius,
        bool(sources),
        lamp_family,
        probe_number,
        clicks,
        escape,
        homes,
        final_position,
        final_momentum,
        list(probe.momentum),
    )


def find_runs(root: Path) -> list[Reading]:
    found = []
    for run_file in sorted(root.glob("**/run.json")):
        record = json.loads(run_file.read_text(encoding="utf-8"))
        if world_name(str(record.get("model", ""))) is None:
            continue
        found.append(read_run(run_file.parent))
    return found


# -- The verdicts against the pins -------------------------------------------


class Verdicts:
    def __init__(self) -> None:
        self.inside = 0
        self.outside = 0
        self.failed_checks = 0

    def check(self, label: str, ok: bool) -> None:
        print(f"  record check {'passed' if ok else 'FAILED'}: {label}")
        if not ok:
            self.failed_checks += 1

    def bracket(self, label: str, value: float | None, bracket: list[float]) -> None:
        lo, hi = bracket
        if value is None:
            self.outside += 1
            print(f"  {DETECTOR} {label}: none (expected {lo:.4g} .. {hi:.4g}): outside")
            return
        ok = lo <= value <= hi
        self.inside += ok
        self.outside += not ok
        print(
            f"  {DETECTOR} {label}: {value:.4g} (expected {lo:.4g} .. {hi:.4g}): {'inside' if ok else 'outside'}"
        )

    def exact(self, label: str, ok: bool, detail: str) -> None:
        self.inside += ok
        self.outside += not ok
        print(f"  {DETECTOR} {label}: {detail}: {'inside' if ok else 'outside'}")


def report(readings: list[Reading], pins: dict[str, object]) -> int:
    worlds = pins["worlds"]
    assert isinstance(worlds, dict)
    verdicts = Verdicts()
    periods: dict[str, float | None] = {}
    samples: dict[str, list[Sample]] = {}
    for reading in readings:
        pin = worlds.get(reading.name)
        print(f"{reading.name} ({reading.folder}): {reading.ticks} intervals, {reading.elapsed:.1f} s")
        verdicts.check("completed", reading.completed)
        verdicts.check("the books balanced at every tick", reading.balanced)
        if pin is None:
            print("  no pin for this world")
            continue
        assert isinstance(pin, dict)
        sample = reading.samples
        samples[reading.name] = sample
        birth_interval = int(pins["birth_interval"])
        off_grid = sum(1 for t, _ in sample if t % birth_interval)
        ages = [c.age for c in reading.clicks]
        print(
            f"  {DETECTOR} clicks on the line: {len(reading.clicks)} (birth ticks off the {birth_interval}-interval "
            f"grid: {off_grid}); x from {min(reading.xs) if reading.xs else '-'} to "
            f"{max(reading.xs) if reading.xs else '-'}, the middle {reading.middle}, the amplitude "
            f"{reading.amplitude}; the ages {min(ages) if ages else '-'} .. {max(ages) if ages else '-'}"
        )
        if pin.get("source"):
            period = period_of(sample, reading.centre_x)
            periods[reading.name] = period.value
            spacings = period.spacings
            print(
                f"  {DETECTOR} crossings of the centre column: {len(period.down.ticks)} down, {len(period.up.ticks)} up; "
                f"the spacings {min(spacings):.0f} .. {max(spacings):.0f}"
                if spacings
                else f"  {DETECTOR} crossings of the centre column: {period.crossings}, no spacing"
            )
            verdicts.bracket(
                "the period T (the recurrence of x)", period.value, pin["period"]["bracket"]
            )
            lag = int(pin["second_difference_lag"]) * birth_interval
            second = second_difference_of(sample, reading.centre_x, lag)
            print(
                f"  {DETECTOR} the second difference at the lag {lag} over {second.samples} samples: the slope "
                f"{second.slope if second.slope is None else round(second.slope, 4)}"
            )
            verdicts.bracket(
                "omega^2 (per interval^2)", second.omega_squared, pin["omega_squared"]["bracket"]
            )
            if second.omega_squared is not None and reading.amplitude:
                acceleration = second.omega_squared * reading.amplitude
                print(
                    f"  {DETECTOR} the acceleration omega^2 x amplitude: {acceleration:.4g} Links per interval^2 "
                    f"(the pin v^2 / r {pin['acceleration']['pin']:.4g}; 3.3's small-n limit "
                    f"{pin['acceleration']['small_n_limit']:.4g})"
                )
            verdicts.bracket(
                "the amplitude (the radius)", reading.amplitude, pin["amplitude"]["bracket"]
            )
        else:
            expected_x = int(pin["x"])
            xs = set(reading.xs)
            verdicts.exact(
                "every click at x = c_x + r",
                xs == {expected_x},
                f"x in {sorted(xs)} (expected {{{expected_x}}})",
            )
            if reading.escape is None:
                verdicts.bracket("the escape tick", None, pin["escape_tick"]["bracket"])
            else:
                print(f"  {DETECTOR} the probe left through {reading.escape[0]}")
                verdicts.bracket(
                    "the escape tick", float(reading.escape[1]), pin["escape_tick"]["bracket"]
                )
        print(
            f"  {GAMEBOARD} (a diagnostic, not pinned): homes {reading.homes}; the probe at the end "
            f"{reading.final_position}, |p| / |p_0| = "
            f"{math.hypot(*reading.final_momentum) / math.hypot(*reading.initial_momentum):.4f}"
            if reading.final_momentum and any(reading.initial_momentum)
            else f"  {GAMEBOARD} (a diagnostic, not pinned): homes {reading.homes}"
        )
    print("across the worlds:")
    ratio_pin = pins["ratio"]
    assert isinstance(ratio_pin, dict)
    t12, t24 = periods.get("r12"), periods.get("r24")
    ratio = t24 / t12 if t12 and t24 else None
    verdicts.bracket("the ratio T(24) / T(12)", ratio, ratio_pin["bracket"])
    equivalence = pins["equivalence"]
    assert isinstance(equivalence, dict)
    first, second = equivalence["worlds"]
    if (
        first in periods
        and second in periods
        and periods[first] is not None
        and periods[second] is not None
    ):
        difference = abs(periods[second] - periods[first])
        verdicts.bracket(
            f"the equivalence: |T({second}) - T({first})|",
            difference,
            [0.0, float(equivalence["period_difference_bracket"])],
        )
    else:
        verdicts.bracket(
            f"the equivalence: |T({second}) - T({first})|",
            None,
            [0.0, float(equivalence["period_difference_bracket"])],
        )
    if first in samples and second in samples:
        shared, equal, largest = common_x_difference(samples[first], samples[second])
        verdicts.exact(
            f"the equivalence: x({second}) against x({first}) on the common birth ticks",
            shared > 0 and largest <= int(equivalence["x_difference_bracket"]),
            f"{shared} common ticks, {equal} equal, the largest difference {largest} Node(s)",
        )
    print(
        f"{verdicts.failed_checks} record checks failed, {verdicts.inside} readings inside, "
        f"{verdicts.outside} outside, none moved"
    )
    return 1 if verdicts.failed_checks else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("root", type=Path, help="the folder holding the run folders")
    parser.add_argument("--expectations", type=Path, default=EXPECTATIONS)
    args = parser.parse_args(argv)
    pins = json.loads(args.expectations.read_text(encoding="utf-8"))
    readings = find_runs(args.root)
    if not readings:
        print(f"no run of the series under {args.root}")
        return 1
    return report(readings, pins)


if __name__ == "__main__":
    sys.exit(main())
