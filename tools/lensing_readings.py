"""The readings of series K, "light beside a mass": a narrow beam of a
paid light family sent past a fixed mass in space at an impact distance b
toward a screen of one-Node `wave` pixels, against a control run without
the mass (docs/EXPERIMENTS.md, "K, light beside a mass";
examples/events/lensing/make_worlds.py; the model owner's go of
2026-09-20 on the law's own predictions, the physicist's entry 2: "light
is not bent by a mass, and not delayed").

Reads the run folders of the worlds (the runner's `run.json`,
`initialization.json` and `events.jsonl`, told apart by the `model` of the
record, `rays-lensing-<name>-space-v1`) and prints, per world, two kinds
of number, each line labelled (the model owner, 2026-09-20: "in reality
there is no such thing" about the host's readings of the board):

- DETECTOR readings, the only kind reality has: the screen's pixels (each
  a `DetectorSet` of one Node) over the late window: the count of clicks
  per pixel and the centroid of the arrival on the screen (in pixels, y
  and z, the deflection against the control with its sign toward the mass
  negative in y), the width of the arrival (the count-weighted rms of y
  about the centroid), the mean age of the arrivals (every click record
  carries the age moment of its group, `reads: "age"`: the flight time,
  Shapiro's reading) against the control, the tick of the first click,
  the count that reached the screen against the control (the mass's own
  clicks of light and the faces' clicks of light beside it: the
  absorption or the scattering), and the phase rate of the arrivals (the
  least-squares slope of the unwrapped phase of the pixels' `record`
  lines against the tick, count-weighted over the pixels) against the
  lamp's turn read off the engine's clock (`by_clock(0, content, K)`).
- GAMEBOARD readings, the host's view of the mechanism, which exist for
  us and not in reality (the world replayed through `NatureBeamSimulation`):
  the beam's rows in flight per interval, the rows at rest or on a
  direction outside the lamp's declared ones (a ray a collision would
  have turned) and the Nodes where they were turned, and the meetings
  (the Nodes holding a ray of the beam and a ray of the mass in the same
  interval), the crowd the beam crossed.

The expectation, written before the runs (README.md): the collision acts
per family's store and per (number, content) class, so a ray of the beam
and a ray of the mass never enter one slot state, and no other rule of
the board reads the crowd for a ray's step: the deflection is 0 within
half a pixel, the delay 0 within one interval, the count the control's,
the phase rate the lamp's turn, at every mass and impact distance; nature
bends light by 4 G M / (b c^2) toward the mass and delays it. The record
checks (completed, the books balanced at every tick) fail the tool; the
readings are registered inside or outside their bracket and never moved.

    PYTHONPATH=src python tools/lensing_readings.py artifacts/lensing
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from event_universe.core.integer import by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import flight_table
from event_universe.events.world import HEADING_OFFSET, REST_DIRECTIONS
from event_universe.json_documents import parse_json_document

MODEL_PREFIX = "rays-lensing-"
MODEL_SUFFIX = "-space-v1"
SCREEN_PREFIX = "screen_"
# The brackets of the derivation (README.md): the centroid within half a
# pixel of the control's, the mean age within one interval, the count
# within one part in a hundred, the phase rate within a twentieth of a
# step per interval of the lamp's turn.
CENTROID_BRACKET = 0.5
AGE_BRACKET = 1.0
COUNT_BRACKET = 0.01
RATE_BRACKET = 0.05
# The window of the reading begins after the slowest direction of the beam
# has reached the screen (age 90 for the declared beam; README.md).
WINDOW_START = 110
MIN_LINES = 8
GAMEBOARD = "GAMEBOARD"
DETECTOR = "DETECTOR"


@dataclass
class Pixel:
    y: int
    z: int
    record: int = 0  # the set's cumulative record (run.json)
    clicks: int = 0  # the set's cumulative clicks (run.json)
    window_count: int = 0
    window_age_moment: int = 0
    window_record: int = 0
    first_tick: int | None = None
    phases: list[tuple[int, int]] = field(default_factory=list)


@dataclass
class Replay:
    """The GameBoard view of one world: per interval the beam's rows, the
    rows a collision would have turned, and the meetings with the crowd."""

    rows: list[int] = field(default_factory=list)
    resting: list[int] = field(default_factory=list)
    turned: list[int] = field(default_factory=list)
    meetings: list[int] = field(default_factory=list)
    turned_nodes: set[tuple[int, int, int]] = field(default_factory=set)
    crowd_rows: list[int] = field(default_factory=list)


@dataclass
class Reading:
    name: str
    ticks: int
    completed: bool
    balanced: bool
    elapsed: float
    turn: int
    phase_steps: int
    K: int | tuple[int, int]
    lamp: tuple[int, int, int]
    screen_x: int
    centre: tuple[int, int, int]
    mass_content: int | None
    fan: int
    rays_per_direction: int
    beam: list[tuple[int, int, int]]
    window: tuple[int, int]
    pixels: dict[tuple[int, int], Pixel] = field(default_factory=dict)
    faces: dict[str, int] = field(default_factory=dict)
    mass_took: int = 0
    document: dict[str, object] = field(default_factory=dict)
    replay: Replay | None = None

    @property
    def impact(self) -> int:
        """The impact distance b: the lamp's y above the mass's (the
        board's centre in the control, where the mass sits otherwise)."""
        return self.lamp[1] - self.centre[1]

    @property
    def wavelength(self) -> float:
        return (self.phase_steps / self.turn) * SPEED


# The speed on a heading read off the flight table: m(T) Links per period.
HEADINGS_TABLE = flight_table(
    ((0, 0, 0), (0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
)
HEADING_PERIOD = int(HEADINGS_TABLE.period[HEADING_OFFSET])
HEADING_LINKS = int(
    HEADINGS_TABLE.manhattan_steps(np.array([HEADING_OFFSET]), np.array([HEADING_PERIOD]))[0]
)
SPEED = HEADING_LINKS / HEADING_PERIOD
DWELL = HEADING_PERIOD / HEADING_LINKS


def crowd_at(reading: Reading, impact: int) -> tuple[float, float]:
    """Series E's form of the mass's crowd at the impact distance
    (README.md, the derivation): the shell mean of the presence, q x dwell
    / (4 pi b^2) rays per Node with q the rays the fan releases per
    interval, and the age moment per Node, that presence times the age of
    a ray at b (b over the speed), the reading a clock beside the beam
    would count; both 0 without a mass."""
    if reading.mass_content is None or impact == 0:
        return 0.0, 0.0
    q = reading.fan * reading.rays_per_direction
    presence = q * DWELL / (4.0 * math.pi * impact * impact)
    return presence, presence * impact / SPEED


def read_run(folder: Path, *, replay: bool = True, window_start: int = WINDOW_START) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    document = json.loads((folder / "initialization.json").read_text(encoding="utf-8"))
    model = str(record["model"])
    name = model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)]
    world = parse_nature_beam_world(parse_json_document((folder / "initialization.json").read_bytes()))
    lamp = next(m for m in world.measured if m.lamp is not None)
    assert lamp.lamp is not None
    families = {f.name: i for i, f in enumerate(world.families)}
    masses = [m for m in world.measured if world.families[m.family].free]
    centre = masses[0].position if masses else tuple(v // 2 for v in world.shape)
    screen_x = next(
        m.position[0] for m in world.measured if m.lamp is None and not world.families[m.family].free
    )
    if masses:
        mass = masses[0]
        # The rays per direction per self-creation off the engine's clock.
        rays = by_clock(0, mass.amount * world.release[0], world.release[1])
        fan = len(mass.directions)
        mass_content: int | None = mass.amount
    else:
        rays, fan, mass_content = 0, 0, None
    ticks = int(record["completed_ticks"])
    reading = Reading(
        name=name,
        ticks=ticks,
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        elapsed=float(record["elapsed_seconds"]),
        turn=world.turn(0, lamp.amount),
        phase_steps=world.phase_steps,
        K=world.K,
        lamp=lamp.position,
        screen_x=screen_x,
        centre=tuple(centre),  # type: ignore[arg-type]
        mass_content=mass_content,
        fan=fan,
        rays_per_direction=rays,
        beam=[world.directions[i] for i in lamp.lamp.directions],
        # The window is [window_start, ticks]: the run's last tick included.
        window=(window_start, ticks + 1),
        document=document,
    )
    light = world.families[lamp.family].name
    for entry in record["detectors"]:
        detector_name = str(entry["name"])
        if detector_name.startswith(SCREEN_PREFIX):
            _, y, z = detector_name.split("_")
            pixel = Pixel(int(y), int(z))
            pixel.record = int(entry["families"][light]["record"])
            pixel.clicks = int(entry["families"][light]["clicks"])
            reading.pixels[(pixel.y, pixel.z)] = pixel
        elif detector_name.startswith("face:"):
            reading.faces[detector_name] = int(entry["families"][light]["clicks"])
    if masses:
        state = next(m for m in record["measured"] if m["number"] == 2)
        reading.mass_took = int(state["measured"][families[light]]["measure"])
    lo, hi = reading.window
    seen_groups: set[tuple[int, str, int]] = set()
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if '"screen_' not in line:
                continue
            event = json.loads(line)
            detector_name = str(event["detector"])
            if not detector_name.startswith(SCREEN_PREFIX) or event["family"] != light:
                continue
            _, y, z = detector_name.split("_")
            pixel = reading.pixels[(int(y), int(z))]
            tick = int(event["tick"])
            if event["event"] == "click":
                if pixel.first_tick is None:
                    pixel.first_tick = tick
                if lo <= tick < hi:
                    pixel.window_count += int(event["amount"])
                    # The `reading` of a click row is the age moment of its
                    # group (the rows of one number met in one interval),
                    # amount x age summed over the group: counted once.
                    group = (tick, detector_name, int(event["number"]))
                    if group not in seen_groups:
                        seen_groups.add(group)
                        pixel.window_age_moment += int(event["reading"])
            elif event["event"] == "record" and lo <= tick < hi:
                pixel.window_record += int(event["record"])
                if event["phase"] is not None:
                    pixel.phases.append((tick, int(event["phase"])))
    if replay:
        reading.replay = replay_world(reading, world, lamp.family, masses[0].family if masses else None)
    return reading


def replay_world(reading: Reading, world, light: int, crowd: int | None) -> Replay:
    """The world replayed through the API (GAMEBOARD): per interval the
    beam's rows, the rows at rest or off the lamp's directions, and the
    Nodes holding a row of the beam and a row of the crowd."""
    simulation = NatureBeamSimulation(world)
    lamp = next(m for m in simulation.measured.values() if m.lamp_rate is not None)
    allowed = np.array(sorted(lamp.lamp_directions), dtype=np.int64)
    found = Replay()
    for _ in range(reading.ticks):
        simulation.step()
        store = simulation.stores[light]
        found.rows.append(int(store.size))
        if store.size == 0:
            found.resting.append(0)
            found.turned.append(0)
            found.meetings.append(0)
            found.crowd_rows.append(0 if crowd is None else int(simulation.stores[crowd].size))
            continue
        resting = store.direction < REST_DIRECTIONS
        off = ~np.isin(store.direction, allowed)
        found.resting.append(int(resting.sum()))
        found.turned.append(int(off.sum()))
        for node in store.node[off].tolist():
            x, y, z = store.coordinates(np.array([node]))
            found.turned_nodes.add((int(x[0]), int(y[0]), int(z[0])))
        if crowd is None:
            found.meetings.append(0)
            found.crowd_rows.append(0)
        else:
            other = simulation.stores[crowd]
            found.crowd_rows.append(int(other.size))
            shared = np.intersect1d(np.unique(store.node), np.unique(other.node))
            found.meetings.append(int(shared.shape[0]))
    return found


def find_runs(root: Path, *, replay: bool = True, window_start: int = WINDOW_START) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        model = str(record.get("model", ""))
        if model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX):
            found.append(read_run(path.parent, replay=replay, window_start=window_start))
    order = {"control": 0, "mass": 1, "heavy": 2, "near": 3}
    return sorted(found, key=lambda r: (order.get(r.name, 9), r.name))


def unwrap(phases: list[int], modulus: int) -> list[int]:
    """The phases unwrapped as forward turns: every difference in [0, N)."""
    found = [0]
    for before, after in zip(phases, phases[1:], strict=False):
        found.append(found[-1] + (after - before) % modulus)
    return found


def slope(x: list[float], y: list[float]) -> float:
    xs, ys = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    dx = xs - xs.mean()
    denominator = float((dx * dx).sum())
    return float((dx * (ys - ys.mean())).sum() / denominator) if denominator > 0 else math.nan


@dataclass
class Analysis:
    count: int
    centroid_y: float
    centroid_z: float
    record_centroid_y: float
    width_y: float
    mean_age: float
    first_tick: int | None
    phase_rate: float
    escaped: int
    lit: int


def analyse(reading: Reading) -> Analysis:
    pixels = [p for p in reading.pixels.values() if p.window_count > 0]
    total = sum(p.window_count for p in pixels)
    if total == 0:
        return Analysis(0, math.nan, math.nan, math.nan, math.nan, math.nan, None, math.nan, 0, 0)
    cy = sum(p.window_count * p.y for p in pixels) / total
    cz = sum(p.window_count * p.z for p in pixels) / total
    record_total = sum(p.window_record for p in pixels)
    rcy = sum(p.window_record * p.y for p in pixels) / record_total if record_total else math.nan
    width = math.sqrt(sum(p.window_count * (p.y - cy) ** 2 for p in pixels) / total)
    mean_age = sum(p.window_age_moment for p in pixels) / total
    first = min(
        (p.first_tick for p in reading.pixels.values() if p.first_tick is not None), default=None
    )
    rates = []
    weights = []
    for p in pixels:
        if len(p.phases) < MIN_LINES:
            continue
        phi = [float(v) for v in unwrap([ph for _, ph in p.phases], reading.phase_steps)]
        rates.append(slope([float(t) for t, _ in p.phases], phi))
        weights.append(p.window_count)
    rate = (
        sum(r * w for r, w in zip(rates, weights, strict=True)) / sum(weights) if weights else math.nan
    )
    return Analysis(
        count=total,
        centroid_y=cy,
        centroid_z=cz,
        record_centroid_y=rcy,
        width_y=width,
        mean_age=mean_age,
        first_tick=first,
        phase_rate=rate,
        escaped=sum(reading.faces.values()),
        lit=len(pixels),
    )


def verdict(inside: bool) -> str:
    return "inside" if inside else "outside"


def fmt(value: float, digits: int = 3) -> str:
    return (
        "-"
        if value is None or (isinstance(value, float) and math.isnan(value))
        else f"{value:.{digits}f}"
    )


def print_readings(readings: list[Reading]) -> tuple[int, int]:
    control = next((r for r in readings if r.name == "control"), None)
    base = analyse(control) if control is not None else None
    first = readings[0]
    print(
        f"{DETECTOR} the lamp's turn {first.turn} steps of {first.phase_steps} per interval "
        f"(K {first.K}; `by_clock`), the wavelength lambda = c x period = {first.wavelength:.3f} Links "
        f"at c = {HEADING_LINKS} / {HEADING_PERIOD} = {SPEED:.4f} Links per interval (the flight table); "
        f"the beam {first.beam}; the screen at x = {first.screen_x}; the window [{first.window[0]}, {first.window[1] - 1}]"
    )
    inside = outside = 0
    print(
        f"{DETECTOR} | world | M | b | crowd at b: presence (rays per Node), age moment | clicks in the window "
        "| centroid y (the deflection off the beam's axis, against the control's) | centroid z (deflection) | width rms y (delta) | mean age (delta) | first click "
        "| count ratio | phase rate (delta vs the turn) | light on the faces | light the mass took | verdicts |"
    )
    for reading in readings:
        a = analyse(reading)
        presence, age_moment = crowd_at(reading, reading.impact)
        if base is None or reading is control or control is None:
            dy = dz = dw = dage = math.nan
            ratio = math.nan
        else:
            # The deflection: the centroid's offset from the beam's own
            # axis (the lamp's y and z) against the control's offset.
            dy = (a.centroid_y - reading.lamp[1]) - (base.centroid_y - control.lamp[1])
            dz = (a.centroid_z - reading.lamp[2]) - (base.centroid_z - control.lamp[2])
            dw, dage = a.width_y - base.width_y, a.mean_age - base.mean_age
            ratio = a.count / base.count if base.count else math.nan
        drate = a.phase_rate - reading.turn
        verdicts = []
        if reading is not control and base is not None:
            checks = [
                ("centroid y", abs(dy) <= CENTROID_BRACKET),
                ("centroid z", abs(dz) <= CENTROID_BRACKET),
                ("delay", abs(dage) <= AGE_BRACKET),
                ("count", abs(ratio - 1.0) <= COUNT_BRACKET),
                ("phase rate", abs(drate) <= RATE_BRACKET),
            ]
            for label, ok in checks:
                verdicts.append(f"{label} {verdict(ok)}")
                inside += ok
                outside += not ok
        else:
            ok = abs(drate) <= RATE_BRACKET
            verdicts.append(f"phase rate {verdict(ok)}")
            inside += ok
            outside += not ok
        mass = "-" if reading.mass_content is None else str(reading.mass_content)
        print(
            f"{DETECTOR} | `{reading.name}` | {mass} | {reading.impact} | {fmt(presence, 2)}, {fmt(age_moment, 1)} "
            f"| {a.count} | {fmt(a.centroid_y)} ({fmt(dy)}) | {fmt(a.centroid_z)} ({fmt(dz)}) "
            f"| {fmt(a.width_y)} ({fmt(dw)}) | {fmt(a.mean_age, 2)} ({fmt(dage, 2)}) | {a.first_tick} "
            f"| {fmt(ratio, 4)} | {fmt(a.phase_rate, 3)} ({fmt(drate, 3)}) | {a.escaped} | {reading.mass_took} "
            f"| {'; '.join(verdicts)} |"
        )
    for reading in readings:
        r = reading.replay
        if r is None:
            continue
        mean_meetings = float(np.mean(r.meetings[reading.window[0] :])) if r.meetings else 0.0
        turned_nodes = sorted(r.turned_nodes)
        print(
            f"{GAMEBOARD} `{reading.name}`: the beam's rows in flight {max(r.rows)} at most "
            f"({r.rows[-1]} at the end); rows at rest {sum(r.resting)} over the run; rows off the beam's "
            f"directions {sum(r.turned)} over the run at {len(turned_nodes)} Nodes"
            f"{' ' + str(turned_nodes[:10]) if turned_nodes else ''}; the crowd's rows in flight "
            f"{max(r.crowd_rows)} at most; Nodes holding a ray of the beam and a ray of the crowd in one interval "
            f"{mean_meetings:.1f} on average over the window, {max(r.meetings)} at most"
        )
    return inside, outside


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="the folder holding the run folders")
    parser.add_argument(
        "--no-replay", action="store_true", help="skip the GameBoard replay of every world"
    )
    parser.add_argument("--window-start", type=int, default=WINDOW_START)
    args = parser.parse_args(argv)
    readings = find_runs(args.root, replay=not args.no_replay, window_start=args.window_start)
    if not readings:
        print(f"no series K run under {args.root}", file=sys.stderr)
        return 2
    failed = 0
    for r in readings:
        for label, ok in (("completed", r.completed), ("balanced", r.balanced)):
            print(f"{'PASS' if ok else 'FAIL'} {r.name}: {label} ({r.ticks} ticks, {r.elapsed:.1f} s)")
            failed += not ok
    print()
    inside, outside = print_readings(readings)
    print()
    print(f"{failed} record check(s) failed; {inside} reading(s) inside, {outside} outside, none moved")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
