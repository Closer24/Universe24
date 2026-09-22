"""The readings of series K, "light beside a mass": a narrow beam of a
paid light family sent past a fixed mass in space at an impact distance b
toward a screen of one-Node `wave` pixels, against a control run without
the mass (docs/EXPERIMENTS.md, "K, light beside a mass";
examples/events/lensing/make_worlds.py; the model owner's go of
2026-09-20 on the law's own predictions, the physicist's entry 2: "light
is not bent by a mass, and not delayed"), and, since the meeting
(2026-09-20, docs/BEAM_LAW.md note 34), the same worlds under the world
key `meeting: true` and the lens world of two beams at +-b.

Reads the run folders of the worlds (the runner's `run.json`,
`initialization.json` and `events.jsonl`, told apart by the `model` of the
record, `rays-lensing-<name>-space-v1` or `beam-lensing-<name>-meeting-v1`)
and prints, per world, two kinds of number, each line labelled (the model
owner, 2026-09-20: "in reality there is no such thing" about the host's
readings of the board):

- DETECTOR readings, the only kind reality has (the phase rate per
  interval and the first click's tick count the pixels' own clock: fixed
  detectors in no crowd at suspension 0, whose tick is their age, record
  569; the strict form reads the rate against the lamp's counted births;
  the clock audit of 2026-09-22): the screen's pixels (each
  a `DetectorSet` of one Node) over the late window: the count of clicks
  per pixel and the centroid of the arrival on the screen (in pixels, y
  and z, the deflection against the control with its sign toward the mass
  negative in y), the width of the arrival (the count-weighted rms of y
  about the centroid), the mean age of the arrivals (every click record
  carries the age moment of its group, `reads: "age"`: the flight time,
  Shapiro's reading) against the control, the tick of the first click,
  the count that reached the screen against the control (the mass's own
  clicks of light and the faces' clicks of light beside it: the
  absorption or the scattering), the phase rate of the arrivals (the
  least-squares slope of the unwrapped phase of the pixels' `record`
  lines against the tick, count-weighted over the pixels) against the
  lamp's turn read off the engine's clock (`by_clock(0, content, K)`),
  and, under the meeting, the phase offset of the arrivals: per click of
  one row the phase on the click record less the lamp's phase at the
  ray's birth (the turn times the birth tick, the tick less the age on
  the record less one), taken modulo N and averaged on the circle per
  pixel and over the screen (the crowd met along the path modulo N, the
  interferometric Shapiro reading; 0 in every control, a check the tool
  prints); in a world of two lamps the centroid per lamp (per number)
  and the crossing they imply.
- GAMEBOARD readings, the host's view of the mechanism, which exist for
  us and not in reality (the world replayed through `NatureBeamSimulation`):
  the beam's rows in flight per interval, the rows at rest or on a
  direction outside the lamp's declared ones (a ray a collision or a
  meeting turned) and the Nodes where they were turned, the meetings (the
  Nodes holding a ray of the beam and a ray of the mass in the same
  interval), the crowd the beam crossed, the crowd at the impact b (the
  presence and the age moment per Node by series E's form: a host
  computation, out of the DETECTOR table since the audit of record 567,
  F16), the books' `turned` line of the light family at the end of the
  run (`run.json`, the audit) and, for two lamps, the x at which the two
  beams' mean lines are closest.

The expectation, written before the runs (README.md): without the key the
collision acts per family's store and per (number, content) class, so a
ray of the beam and a ray of the mass never enter one slot state, and no
other rule of the board reads the crowd for a ray's step: the deflection
is 0 within half a pixel, the delay 0 within one interval, the count the
control's, the phase rate the lamp's turn, at every mass and impact
distance; nature bends light by 4 G M / (b c^2) toward the mass and
delays it. Under the meeting, from the design's offline flight
(scratchpad/meeting/MEETING.md, section 3.1, the register N = 64):
`mass` the centroid -3.0 +- 0.5 pixels in y toward the mass and 0 in z,
the width about 6.0, the mean age about 90.4, about 1547 of 1553 rays
landing (a count ratio of 0.996), no ray on the faces; `heavy` -4.3 with
209 rays wrapped to the faces (0.865); `near` -2.6 with 136 (0.912); the
phase offset about 55 steps (`mass`, `near`: 119 and 183 crowd units met
modulo 64) and 24 (`heavy`: 216 modulo 64); the control unchanged; the
lens world's crossing about 70 Links past the mass, a grain of the fan
and not a focal law. The brackets under the meeting, fixed here before
the runs: the centroid within 0.5 pixel of the expected shift in y and
of 0 in z; the count ratio within 0.05 of the expected; the mean age
within 1 interval of the expected; the faces' clicks of light within a
quarter of the expected (at most 5 where 0 is expected); the phase offset
within 8 steps of the expected on the circle; the phase rate within 0.05
of the turn. The record checks (completed, the books balanced at every
tick) fail the tool; the readings are registered inside or outside their
bracket and never moved.

    PYTHONPATH=src python tools/lensing_readings.py artifacts/lensing
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from event_universe.core.integer import by_clock
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import direction_flight
from event_universe.events.world import HEADING_OFFSET, REST_DIRECTIONS
from event_universe.world_loading import world_of_run

MODEL_PREFIX = "rays-lensing-"
MODEL_SUFFIX = "-space-v1"
MODEL_PATTERN = re.compile(r"^(rays|beam)-lensing-(?P<name>.+)-(?P<kind>space|meeting)-v1$")
SCREEN_PREFIX = "screen_"
# The brackets of the derivation (README.md): the centroid within half a
# pixel of the control's, the mean age within one interval, the count
# within one part in a hundred, the phase rate within a twentieth of a
# step per interval of the lamp's turn.
CENTROID_BRACKET = 0.5
AGE_BRACKET = 1.0
COUNT_BRACKET = 0.01
RATE_BRACKET = 0.05
# The brackets under the meeting (the module docstring), fixed before the runs.
MEETING_COUNT_BRACKET = 0.05
MEETING_FACES_FRACTION = 0.25
MEETING_FACES_LEAST = 5
OFFSET_BRACKET = 8.0
# The expectation under the meeting per world (the design's offline flight):
# the centroid shift in y, the mean age, the count ratio, the faces'
# clicks of light and the phase offset in steps.
MEETING_EXPECTED: dict[str, dict[str, float]] = {
    "control": {"shift": 0.0, "age": 89.40, "ratio": 1.0, "faces": 0, "offset": 0.0},
    "mass": {"shift": -3.0, "age": 90.43, "ratio": 1547 / 1553, "faces": 0, "offset": 119 % 64},
    "heavy": {"shift": -4.3, "age": 90.64, "ratio": 1332 / 1553, "faces": 209, "offset": 216 % 64},
    "near": {"shift": -2.6, "age": 89.72, "ratio": 1399 / 1553, "faces": 136, "offset": 183 % 64},
}
# The lens world's expected crossing past the mass, in Links (a grain, not
# a focal law: registered, no bracket).
LENS_CROSSING = 70.0
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
    # Per lamp number, the count in the window (a world of two lamps).
    by_number: dict[int, int] = field(default_factory=dict)
    # The phase offsets of the clicks of one row: the sum of their unit
    # vectors on the circle and their count.
    offset_cos: float = 0.0
    offset_sin: float = 0.0
    offset_count: int = 0


@dataclass
class Replay:
    """The GameBoard view of one world: per interval the beam's rows, the
    rows a collision or a meeting turned, the meetings with the crowd and,
    for two lamps, the x where the beams' mean lines are closest."""

    rows: list[int] = field(default_factory=list)
    resting: list[int] = field(default_factory=list)
    turned: list[int] = field(default_factory=list)
    meetings: list[int] = field(default_factory=list)
    turned_nodes: set[tuple[int, int, int]] = field(default_factory=set)
    crowd_rows: list[int] = field(default_factory=list)
    crossing_x: list[float] = field(default_factory=list)


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
    meeting: bool = False
    # The lamps by number (position), one in the four worlds, two in the lens world.
    lamps: dict[int, tuple[int, int, int]] = field(default_factory=dict)
    # The `turned` line of the light family and of the world at the end.
    turned: list[int] = field(default_factory=lambda: [0, 0, 0])
    turned_total: list[int] = field(default_factory=lambda: [0, 0, 0])
    mixed_groups: int = 0
    # The register's pins of a deciding world of every family under one
    # wall (the matter block of examples/events/optical/expectations.json,
    # by the run folder's name): the shift and the arrival with their
    # brackets; None for the light worlds, whose verdicts are the
    # derivation's brackets about the control.
    pins: dict[str, float] | None = None

    @property
    def impact(self) -> int:
        """The impact distance b: the lamp's y above the mass's (the
        board's centre in the control, where the mass sits otherwise)."""
        return self.lamp[1] - self.centre[1]

    @property
    def wavelength(self) -> float:
        return (self.phase_steps / self.turn) * SPEED


# The speed on a heading read off the flight table: m(T) Links per period.
HEADINGS_FLIGHT = direction_flight(
    ((0, 0, 0), (0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
)
HEADING_PERIOD = int(HEADINGS_FLIGHT.period[HEADING_OFFSET])
HEADING_LINKS = int(
    HEADINGS_FLIGHT.manhattan_steps(np.array([HEADING_OFFSET]), np.array([HEADING_PERIOD]))[0]
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
    presence = q * DWELL / (4.0 * math.pi * abs(impact) * abs(impact))
    return presence, presence * abs(impact) / SPEED


def world_name(model: str) -> tuple[str, bool] | None:
    """The world's name and whether it is a meeting world, from the model id."""
    found = MODEL_PATTERN.match(model)
    if found is None:
        return None
    return found.group("name"), found.group("kind") == "meeting"


def read_run(folder: Path, *, replay: bool = True, window_start: int = WINDOW_START) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    document = world_of_run(folder)
    named = world_name(str(record["model"]))
    assert named is not None
    name, meeting = named
    world = parse_nature_beam_world(document)
    lamps = [(i + 1, m) for i, m in enumerate(world.measured) if m.lamp is not None]
    number, lamp = lamps[0]
    assert lamp.lamp is not None
    families = {f.name: i for i, f in enumerate(world.families)}
    masses = [(i + 1, m) for i, m in enumerate(world.measured) if world.families[m.family].free]
    centre = masses[0][1].position if masses else tuple(v // 2 for v in world.shape)
    screen_x = next(
        m.position[0] for m in world.measured if m.lamp is None and not world.families[m.family].free
    )
    if masses:
        mass = masses[0][1]
        # The rays per direction per self-creation off the engine's clock.
        rays = by_clock(0, mass.amount * world.release[0], world.release[1])
        fan = len(mass.directions)
        mass_content: int | None = mass.amount
    else:
        rays, fan, mass_content = 0, 0, None
    ticks = int(record["completed_ticks"])
    light = world.families[lamp.family].name
    audit = record.get("audit") or []
    last = audit[-1] if audit else {}
    turned = list(last.get("families", {}).get(light, {}).get("turned", [0, 0, 0]))
    turned_total = list(last.get("momentum", {}).get("turned", [0, 0, 0]))
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
        meeting=meeting or bool(world.meeting),
        lamps={n: m.position for n, m in lamps},
        turned=turned,
        turned_total=turned_total,
    )
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
        state = next(m for m in record["measured"] if m["number"] == masses[0][0])
        reading.mass_took = int(state["measured"][families[light]]["measure"])
    lo, hi = reading.window
    # The click groups (tick, detector, number): the rows of each, for the
    # age moment (counted once per group) and the phase offset (read only
    # off a group of one row, whose age is its reading over its amount).
    groups: dict[tuple[int, str, int], list[tuple[int, int, int]]] = {}
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if '"screen_' not in line:
                continue
            event = json.loads(line)
            if "detector" not in event:
                # The layer's lines (a gather names the chosen set) are not
                # the crowd's clicks, passes and records.
                continue
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
                    amount = int(event["amount"])
                    pixel.window_count += amount
                    other = int(event["number"])
                    pixel.by_number[other] = pixel.by_number.get(other, 0) + amount
                    group = (tick, detector_name, other)
                    if group not in groups:
                        groups[group] = []
                        pixel.window_age_moment += int(event["reading"])
                    groups[group].append((amount, int(event["phase"]), int(event["reading"])))
            elif event["event"] == "record" and lo <= tick < hi:
                pixel.window_record += int(event["record"])
                if event["phase"] is not None:
                    pixel.phases.append((tick, int(event["phase"])))
    modulus = reading.phase_steps
    for (tick, detector_name, _), rows in groups.items():
        if len(rows) != 1:
            reading.mixed_groups += 1
            continue
        amount, phase, moment = rows[0]
        if moment % amount:
            reading.mixed_groups += 1
            continue
        age = moment // amount
        # The lamp's phase at the birth: the release of the tick t0 = tick -
        # age carries the phase turn x (t0 - 1) (the lamp turns after it releases).
        birth = (reading.turn * (tick - age - 1)) % modulus
        offset = (phase - birth) % modulus
        _, y, z = detector_name.split("_")
        pixel = reading.pixels[(int(y), int(z))]
        angle = 2.0 * math.pi * offset / modulus
        pixel.offset_cos += amount * math.cos(angle)
        pixel.offset_sin += amount * math.sin(angle)
        pixel.offset_count += amount
    if replay:
        reading.replay = replay_world(
            reading, world, lamp.family, masses[0][1].family if masses else None
        )
    return reading


def replay_world(reading: Reading, world, light: int, crowd: int | None) -> Replay:
    """The world replayed through the API (GAMEBOARD): per interval the
    beam's rows, the rows at rest or off the lamp's directions, the Nodes
    holding a row of the beam and a row of the crowd and, with two lamps,
    the x at which the two beams' mean y lines are closest."""
    simulation = NatureBeamSimulation(world)
    lamps = [m for m in simulation.measured.values() if m.lamp_rate is not None]
    allowed = np.array(sorted(lamps[0].lamp_directions), dtype=np.int64)
    numbers = [m.number for m in lamps]
    found = Replay()
    lo = reading.window[0]
    for tick in range(1, reading.ticks + 1):
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
        if len(numbers) == 2 and tick >= lo:
            x, y, _ = store.coordinates(store.node)
            means = []
            for number in numbers:
                mine = store.number == number
                columns = np.unique(x[mine])
                means.append({int(c): float(y[mine & (x == c)].mean()) for c in columns})
            shared_x = sorted(set(means[0]) & set(means[1]))
            past = [c for c in shared_x if c > reading.centre[0]]
            if past:
                gaps = [abs(means[0][c] - means[1][c]) for c in past]
                found.crossing_x.append(float(past[int(np.argmin(gaps))]))
    return found


def matter_pins(register: Path | None) -> dict[str, dict[str, float]]:
    """The register's matter block by world name: the pinned shift and
    arrival with their brackets (the tool's verdict on a deciding world of
    every family under one wall; the physics-rule reviewer's S5)."""
    if register is None or not register.is_file():
        return {}
    block = json.loads(register.read_text(encoding="utf-8")).get("matter", {})
    return {
        name: {
            "shift": float(entry["shift"]),
            "shift_bracket": float(entry["shift_bracket"]),
            "arrival": float(entry["arrival"]),
            "arrival_bracket": float(entry["arrival_bracket"]),
        }
        for name, entry in block.get("worlds", {}).items()
    }


def find_runs(
    root: Path,
    *,
    replay: bool = True,
    window_start: int = WINDOW_START,
    register: Path | None = None,
) -> list[Reading]:
    found = []
    pins = matter_pins(register)
    for path in sorted(root.rglob("run.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if world_name(str(record.get("model", ""))) is not None:
            reading = read_run(path.parent, replay=replay, window_start=window_start)
            # The run folder is named after the world (tools/run_series.py).
            reading.pins = pins.get(path.parent.parent.name)
            found.append(reading)
    order = {"control": 0, "mass": 1, "heavy": 2, "near": 3, "lens": 4}
    return sorted(found, key=lambda r: (r.meeting, order.get(r.name, 9), r.name))


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


def circular_mean(cos_sum: float, sin_sum: float, count: int, modulus: int) -> tuple[float, float]:
    """The mean offset on the circle in steps and the resultant length (1 a
    sharp offset, 0 a uniform one); NaN without clicks."""
    if count == 0:
        return math.nan, math.nan
    angle = math.atan2(sin_sum, cos_sum) % (2.0 * math.pi)
    return angle * modulus / (2.0 * math.pi), math.hypot(cos_sum, sin_sum) / count


def circular_distance(a: float, b: float, modulus: int) -> float:
    return abs((a - b + modulus / 2.0) % modulus - modulus / 2.0)


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
    offset: float = math.nan
    offset_length: float = math.nan
    offset_clicks: int = 0
    centroids: dict[int, float] = field(default_factory=dict)


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
    offset, length = circular_mean(
        sum(p.offset_cos for p in pixels),
        sum(p.offset_sin for p in pixels),
        sum(p.offset_count for p in pixels),
        reading.phase_steps,
    )
    centroids = {}
    for number in sorted({n for p in pixels for n in p.by_number}):
        weight = sum(p.by_number.get(number, 0) for p in pixels)
        if weight:
            centroids[number] = sum(p.by_number.get(number, 0) * p.y for p in pixels) / weight
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
        offset=offset,
        offset_length=length,
        offset_clicks=sum(p.offset_count for p in pixels),
        centroids=centroids,
    )


def verdict(inside: bool) -> str:
    return "inside" if inside else "outside"


def fmt(value: float, digits: int = 3) -> str:
    return (
        "-"
        if value is None or (isinstance(value, float) and math.isnan(value))
        else f"{value:.{digits}f}"
    )


def pixel_offsets(reading: Reading, top: int = 9) -> list[tuple[int, int, int, float, float]]:
    """The phase offset per pixel (y, z, clicks, the mean offset in steps,
    the resultant length) for the `top` pixels by count."""
    pixels = sorted(reading.pixels.values(), key=lambda p: -p.offset_count)[:top]
    found = []
    for p in pixels:
        if p.offset_count == 0:
            continue
        mean, length = circular_mean(p.offset_cos, p.offset_sin, p.offset_count, reading.phase_steps)
        found.append((p.y, p.z, p.offset_count, mean, length))
    return found


def print_space_readings(readings: list[Reading]) -> tuple[int, int]:
    """The four worlds without the key: the readings against the derivation."""
    control = next((r for r in readings if r.name == "control"), None)
    base = analyse(control) if control is not None else None
    inside = outside = 0
    print(
        f"{DETECTOR} | world | M | b | clicks in the window "
        "| centroid y (the deflection off the beam's axis, against the control's) | centroid z (deflection) | width rms y (delta) | mean age (delta) | first click "
        "| count ratio | phase rate (delta vs the turn) | light on the faces | light the mass took | verdicts |"
    )
    for reading in readings:
        a = analyse(reading)
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
        if reading is not control and base is not None and reading.pins is not None:
            # A deciding world of every family under one wall: the register's
            # pins (the shift and the arrival against the control) with
            # their brackets; the count within the derivation's bracket.
            pins = reading.pins
            checks = [
                (
                    f"shift {fmt(dy)} against the pin {pins['shift']:+.2f} +- {pins['shift_bracket']:.1f}",
                    abs(dy - pins["shift"]) <= pins["shift_bracket"],
                ),
                ("centroid z", abs(dz) <= CENTROID_BRACKET),
                (
                    f"arrival {fmt(dage, 2)} against the pin {pins['arrival']:+.2f} +- {pins['arrival_bracket']:.0f}",
                    abs(dage - pins["arrival"]) <= pins["arrival_bracket"],
                ),
                ("count", abs(ratio - 1.0) <= COUNT_BRACKET),
            ]
        elif reading is not control and base is not None:
            checks = [
                ("centroid y", abs(dy) <= CENTROID_BRACKET),
                ("centroid z", abs(dz) <= CENTROID_BRACKET),
                ("delay", abs(dage) <= AGE_BRACKET),
                ("count", abs(ratio - 1.0) <= COUNT_BRACKET),
                ("phase rate", abs(drate) <= RATE_BRACKET),
            ]
        if reading is not control and base is not None:
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
            f"{DETECTOR} | `{reading.name}` | {mass} | {reading.impact} "
            f"| {a.count} | {fmt(a.centroid_y)} ({fmt(dy)}) | {fmt(a.centroid_z)} ({fmt(dz)}) "
            f"| {fmt(a.width_y)} ({fmt(dw)}) | {fmt(a.mean_age, 2)} ({fmt(dage, 2)}) | {a.first_tick} "
            f"| {fmt(ratio, 4)} | {fmt(a.phase_rate, 3)} ({fmt(drate, 3)}) | {a.escaped} | {reading.mass_took} "
            f"| {'; '.join(verdicts)} |"
        )
    return inside, outside


def print_meeting_readings(readings: list[Reading]) -> tuple[int, int]:
    """The worlds under `meeting: true`: the readings against the design's
    offline flight (the brackets of the module docstring)."""
    control = next((r for r in readings if r.name == "control"), None)
    base = analyse(control) if control is not None else None
    inside = outside = 0
    print(
        f"{DETECTOR} under `meeting: true` | world | M | b | clicks in the window | centroid y (the shift off the "
        "beam's axis against the control's; expected) | centroid z (shift; expected 0) | width rms y (delta) "
        "| mean age (delta; expected) | count ratio (expected) | light on the faces (expected) | light the mass took "
        "| phase rate (delta vs the turn) | phase offset, steps of N (expected), resultant, clicks read | verdicts |"
    )
    for reading in readings:
        a = analyse(reading)
        expected = MEETING_EXPECTED.get(reading.name)
        if reading.name == "lens":
            continue
        if base is None or reading is control or control is None:
            dy = dz = dw = dage = math.nan
            ratio = math.nan
        else:
            dy = (a.centroid_y - reading.lamp[1]) - (base.centroid_y - control.lamp[1])
            dz = (a.centroid_z - reading.lamp[2]) - (base.centroid_z - control.lamp[2])
            dw, dage = a.width_y - base.width_y, a.mean_age - base.mean_age
            ratio = a.count / base.count if base.count else math.nan
        drate = a.phase_rate - reading.turn
        verdicts = []
        if expected is not None and reading is not control and base is not None:
            faces_bracket = max(MEETING_FACES_LEAST, MEETING_FACES_FRACTION * expected["faces"])
            checks = [
                ("centroid y", abs(dy - expected["shift"]) <= CENTROID_BRACKET),
                ("centroid z", abs(dz) <= CENTROID_BRACKET),
                ("delay", abs(a.mean_age - expected["age"]) <= AGE_BRACKET),
                ("count", abs(ratio - expected["ratio"]) <= MEETING_COUNT_BRACKET),
                ("faces", abs(a.escaped - expected["faces"]) <= faces_bracket),
                (
                    "phase offset",
                    circular_distance(a.offset, expected["offset"], reading.phase_steps)
                    <= OFFSET_BRACKET,
                ),
                ("phase rate", abs(drate) <= RATE_BRACKET),
            ]
        else:
            checks = [
                ("phase rate", abs(drate) <= RATE_BRACKET),
                (
                    "phase offset",
                    (not math.isnan(a.offset))
                    and circular_distance(a.offset, 0.0, reading.phase_steps) <= OFFSET_BRACKET,
                ),
            ]
        for label, ok in checks:
            verdicts.append(f"{label} {verdict(ok)}")
            inside += ok
            outside += not ok
        mass = "-" if reading.mass_content is None else str(reading.mass_content)
        exp_shift = "-" if expected is None else fmt(expected["shift"], 1)
        exp_age = "-" if expected is None else fmt(expected["age"], 2)
        exp_ratio = "-" if expected is None else fmt(expected["ratio"], 3)
        exp_faces = "-" if expected is None else str(int(expected["faces"]))
        exp_offset = "-" if expected is None else fmt(expected["offset"], 0)
        print(
            f"{DETECTOR} | `{reading.name}` | {mass} | {reading.impact} | {a.count} "
            f"| {fmt(a.centroid_y)} ({fmt(dy)}; {exp_shift}) | {fmt(a.centroid_z)} ({fmt(dz)}; 0) "
            f"| {fmt(a.width_y)} ({fmt(dw)}) | {fmt(a.mean_age, 2)} ({fmt(dage, 2)}; {exp_age}) "
            f"| {fmt(ratio, 4)} ({exp_ratio}) | {a.escaped} ({exp_faces}) | {reading.mass_took} "
            f"| {fmt(a.phase_rate, 3)} ({fmt(drate, 3)}) | {fmt(a.offset, 1)} ({exp_offset}), {fmt(a.offset_length, 2)}, {a.offset_clicks} "
            f"| {'; '.join(verdicts)} |"
        )
        for y, z, count, mean, length in pixel_offsets(reading):
            print(
                f"{DETECTOR} `{reading.name}` pixel ({y}, {z}): {count} clicks read, the phase offset "
                f"{mean:.1f} steps, resultant {length:.2f}"
            )
        if reading.mixed_groups:
            print(
                f"{DETECTOR} `{reading.name}`: {reading.mixed_groups} click groups of several rows "
                "left out of the phase offset (their ages cannot be told apart)"
            )
    lens = next((r for r in readings if r.name == "lens"), None)
    if lens is not None:
        a = analyse(lens)
        length = lens.screen_x - lens.centre[0]
        print(
            f"{DETECTOR} `lens` | two lamps at {sorted(lens.lamps.values())} | the screen at x = {lens.screen_x}, "
            f"{length} Links past the mass | clicks in the window {a.count} | mean age {fmt(a.mean_age, 2)} "
            f"| light on the faces {a.escaped} | light the mass took {lens.mass_took} | phase rate {fmt(a.phase_rate, 3)} "
            f"| phase offset {fmt(a.offset, 1)} steps, resultant {fmt(a.offset_length, 2)}"
        )
        crossings = []
        for number, position in sorted(lens.lamps.items()):
            centroid = a.centroids.get(number, math.nan)
            b = position[1] - lens.centre[1]
            shift = centroid - position[1]
            # A beam straight after the mass turned toward its line crosses
            # it f = L x b / shift Links past the mass.
            crossing = abs(length * b / shift) if shift and not math.isnan(shift) else math.nan
            crossings.append(crossing)
            print(
                f"{DETECTOR} `lens` lamp {number} at y = {position[1]} (b = {b}): the centroid y {fmt(centroid)} "
                f"(the shift {fmt(shift)} toward the mass's line), the crossing it implies {fmt(crossing, 1)} Links "
                f"past the mass (expected about {LENS_CROSSING:.0f}: a grain, not a bracket)"
            )
        if len(crossings) == 2 and not any(math.isnan(c) for c in crossings):
            print(
                f"{DETECTOR} `lens`: the crossing {fmt(sum(crossings) / 2, 1)} Links past the mass on average; "
                f"the two centroids {fmt(abs(a.centroids.get(1, math.nan) - a.centroids.get(2, math.nan)))} pixels apart at the screen"
            )
    return inside, outside


def print_gameboard(readings: list[Reading]) -> None:
    for reading in readings:
        r = reading.replay
        turned = f"; the books' `turned` line of the light family {reading.turned} (the world {reading.turned_total})"
        presence, age_moment = crowd_at(reading, reading.impact)
        print(
            f"{GAMEBOARD} `{reading.name}`: the crowd at b = {reading.impact}: presence {fmt(presence, 2)} rays "
            f"per Node, age moment {fmt(age_moment, 1)} (series E's form, a host computation: a diagnostic, "
            "never pinned; the detector reading behind it, a clock's rate at b, not yet read)"
        )
        if r is None:
            print(f"{GAMEBOARD} `{reading.name}`{'' if not reading.meeting else turned}")
            continue
        mean_meetings = float(np.mean(r.meetings[reading.window[0] :])) if r.meetings else 0.0
        turned_nodes = sorted(r.turned_nodes)
        crossing = ""
        if r.crossing_x:
            crossing = (
                f"; the two beams' mean lines closest at x = {np.mean(r.crossing_x):.1f} on average over the window "
                f"({np.mean(r.crossing_x) - reading.centre[0]:.1f} Links past the mass; {min(r.crossing_x):.0f} to {max(r.crossing_x):.0f})"
            )
        print(
            f"{GAMEBOARD} `{reading.name}`{' (meeting)' if reading.meeting else ''}: the beam's rows in flight {max(r.rows)} at most "
            f"({r.rows[-1]} at the end); rows at rest {sum(r.resting)} over the run; rows off the beam's "
            f"directions {sum(r.turned)} over the run at {len(turned_nodes)} Nodes"
            f"{' ' + str(turned_nodes[:10]) if turned_nodes else ''}; the crowd's rows in flight "
            f"{max(r.crowd_rows)} at most; Nodes holding a ray of the beam and a ray of the crowd in one interval "
            f"{mean_meetings:.1f} on average over the window, {max(r.meetings)} at most"
            f"{turned if reading.meeting else ''}{crossing}"
        )


def print_readings(readings: list[Reading]) -> tuple[int, int]:
    first = readings[0]
    print(
        f"{DETECTOR} the lamp's turn {first.turn} steps of {first.phase_steps} per interval "
        f"(K {first.K}; `by_clock`), the wavelength lambda = c x period = {first.wavelength:.3f} Links "
        f"at c = {HEADING_LINKS} / {HEADING_PERIOD} = {SPEED:.4f} Links per interval (the flight table); "
        f"the beam {first.beam}; the screen at x = {first.screen_x}; the window [{first.window[0]}, {first.window[1] - 1}]"
    )
    inside = outside = 0
    space = [r for r in readings if not r.meeting]
    meeting = [r for r in readings if r.meeting]
    if space:
        found = print_space_readings(space)
        inside, outside = inside + found[0], outside + found[1]
    if meeting:
        found = print_meeting_readings(meeting)
        inside, outside = inside + found[0], outside + found[1]
    print_gameboard(readings)
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
    parser.add_argument(
        "--register",
        type=Path,
        default=None,
        help="the optical register (expectations.json) whose matter block pins a deciding world by the run folder's name",
    )
    args = parser.parse_args(argv)
    readings = find_runs(
        args.root, replay=not args.no_replay, window_start=args.window_start, register=args.register
    )
    if not readings:
        print(f"no series K run under {args.root}", file=sys.stderr)
        return 2
    failed = 0
    for r in readings:
        for label, ok in (("completed", r.completed), ("balanced", r.balanced)):
            print(
                f"{'PASS' if ok else 'FAIL'} {r.name}{' (meeting)' if r.meeting else ''}: {label} ({r.ticks} ticks, {r.elapsed:.1f} s)"
            )
            failed += not ok
    print()
    inside, outside = print_readings(readings)
    print()
    print(f"{failed} record check(s) failed; {inside} reading(s) inside, {outside} outside, none moved")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
