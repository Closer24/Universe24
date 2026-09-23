"""The readings of series G, the Hubble diagram behind the detector, under
the Beam Law, in space.

Reads the run folders of the worlds of `examples/events/hubble/` (the
runner's `run.json`, `initialization.json` and `events.jsonl`, the folders
told apart by the `model` of their record, `rays-hubble-<crowd>-<clock>-
space-v1`) and prints, per run and per window of the record, the Hubble
diagram the detector at the centre reads: per source (a family of its own)
the redshift z from the rate at which the pointer of the detector's record
turns, 1 + z = rho / (Delta Phi / Delta t), rho the emitter's declared
turn per self-creation (content / K) and Delta Phi the unwrapped phase of
the `record` lines over Delta t detector intervals (a least-squares slope),
and the distance from the ages of the arriving rows on the click records
(`reading` = the age moment, amount x age, under `reads: "age"`): the
light-travel time tau = the age and the distance d = m(tau) Links, m the
Manhattan steps of the flight table read through the engine's own
`direction_flight`, whose period also gives c (README.md there).

The pinned reading is in the detector's own clock (the model owner,
2026-09-22, records 678 and 707 of docs/LOG_2026-09-20.md: a detector's
time is the clock of the Node it sits on, the interval count less what
the crowd at that Node owes through the age wall; the detector at the
centre sits in its six masses' crowd). Its clock counts r_w
self-creations per interval over a window, so a phase step that takes
Delta t intervals takes r_w Delta t of its counts and every reading of
the lattice's clock is restated by the one closed form

    1 + z_d = r_w (1 + z),   H_d = r_w H,   z_d(0) = r_w - 1,

the near fit's linear law through the detector's own zero z_d(0) (the
crowd's blue shift at the centre: a source with v / c below 1 / r_w - 1
reads blue), the three exact forms as 1 + z_d = r_w (1 + form(H tau))
(the rms of the far part times r_w, the nearest form unchanged), the
reading's formula (1 + z_d) = (1 + k)(1 + v / c) r_w (the same ratio, both
sides in one clock) and the free quadratic's q_eff on z_d - z_d(0). The
window's rate r_w is the detector's age from its state at the window's
edges over the intervals between them, a step of the replay (GAMEBOARD,
until the strict run with the reader's own lamp, examples/events/
reader_clock's form); this r_w is the detector's own count of intervals
stretched by what arrives at it, the age wall's member at the coefficient
1 (the owner's record 709); without the replay the detector's own record over
the run, age / (age + waited) of its state in `run.json`, stands for
every window (DETECTOR). The reading in the lattice's clock (the tick
count of the `record` lines, every number as the register read it until
2026-09-22) is printed beside it as [GAMEBOARD, the lattice's clock] and
counted in no criterion.

Every number is labelled by its kind (the model owner, 2026-09-20): a
DETECTOR reading is the record of the detector's set or of a measured event
in the world (clicks, the pointer, phases, the ages of arrivals, an owed
count; the only kind reality has); a GAMEBOARD reading is the host's view
of the GameBoard (a source's position and steps from the run's record, the
books, the replay's clocks; exists for us, not in reality). The Hubble
diagram and its fits are made of detector readings only; a source's speed
from its `step` records and the replay's counts are the check columns.

The fits, per window (in the lattice's clock first, then restated as
above): the linear law z = H tau through the origin on the
near part (z <= 0.2) and H t_0, t_0 the window's centre; the three exact
forms in the light-travel time at that H, q = +0.5 (Einstein-de Sitter),
q = 0 (Milne, the coasting form) and q = -0.55 (flat Omega_m = 0.3, the
accelerating form observed today), with their rms over the far part
(z > 0.2), the best H of each form over every point, and the effective q
of a free quadratic fit. The record checks (completed, the books balanced
at every tick) fail the tool; the readings are registered inside or
outside their expectation (docs/EXPERIMENTS.md, "G, the Hubble diagram
behind the detector (2026-09-20)") and never moved.

With `--from-one-point` (the physicist's review of the series, 2026-09-20;
printed after the pinned readings, not a pinned reading) every window is
fitted again with every source's light-travel time reduced by (r_0 / c) /
(1 + z), r_0 the source's declared initial distance (a GameBoard quantity):
a coasting source thrown from r_0 at the speed v is the source thrown from
the centre at the time -r_0 / v, and at t_0 its light-travel time is tau -
r_0 / (c + v) = tau - (r_0 / c) / (1 + z), so the correction is exact for
the coasting throw and first order for the pushing one. The block also
prints what the near fit itself does to an exact coasting form at the
window's own taus (its H t_0 for z = H tau / (1 - H tau) with H = 1 / t_0):
the near fit through the origin on z <= 0.2 reads the Milne curvature
(z = H tau + (H tau)^2 + ...) as a larger H, so the far part of an exact
coasting throw from one point lies below the coasting form at that H.

    PYTHONPATH=src python tools/hubble_readings.py artifacts/hubble [--png DIR] [--no-replay] [--from-one-point]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.nature_beam import direction_flight
from event_universe.events.world import HEADING_OFFSET, Q
from event_universe.world_loading import world_of_run
from event_universe.trimmed_record import refuse_trimmed_record

MODEL_PREFIX = "rays-hubble-"
MODEL_SUFFIX = "-space-v1"
DETECTOR = "centre"
WINDOWS = ((100, 200), (200, 300), (300, 400))
# Printed after the runs (not a pinned reading): the late half as one
# window, for the grain of the step rule under a changing momentum.
LONG_WINDOW = (200, 400)
# The near part of the diagram, fitted by the linear law; the far part is
# compared with the three forms.
NEAR = 0.2
MIN_LINES = 10
# The criteria pinned before the runs (README.md): the reading's formula
# within 2 %, H t_0 = 1 within 10 % in the coasting worlds, the coasting
# form's rms below 0.02 there.
FORMULA_TOLERANCE = 0.02
HUBBLE_TIME_TOLERANCE = 0.10
COASTING_RMS = 0.02
OMEGA_M = 0.3
OMEGA_L = 1.0 - OMEGA_M
LCDM_A = math.asinh(math.sqrt(OMEGA_L / OMEGA_M))
Form = Callable[[float], float]
KIND_DETECTOR = "[DETECTOR]"
KIND_BOARD = "[GAMEBOARD]"
# The reading in the lattice's clock, as the register read it until
# 2026-09-22: printed beside the detector's clock, counted in no criterion.
KIND_LATTICE = "[GAMEBOARD, the lattice's clock]"
DETECTOR_NUMBER = 1
# The flight table of the six headings (the two rest vectors first): m(age)
# and c are the same on every heading.
HEADINGS_FLIGHT = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))


def milne(x: float) -> float:
    """q = 0: 1 + z = 1 / (1 - H tau)."""
    return 1.0 / (1.0 - x) - 1.0 if x < 1.0 else math.inf


def einstein_de_sitter(x: float) -> float:
    """q = +0.5: 1 + z = (1 - 1.5 H tau)^(-2/3)."""
    return (1.0 - 1.5 * x) ** (-2.0 / 3.0) - 1.0 if 1.5 * x < 1.0 else math.inf


def accelerating(x: float) -> float:
    """q = -0.55: flat Omega_m = 0.3, 1 + z = [sinh A / sinh(A - 1.5 sqrt(Omega_L) H tau)]^(2/3)."""
    inner = LCDM_A - 1.5 * math.sqrt(OMEGA_L) * x
    return (math.sinh(LCDM_A) / math.sinh(inner)) ** (2.0 / 3.0) - 1.0 if inner > 0 else math.inf


# The forms in the order of the deceleration parameter, with the H tau at
# which each has its pole (the search bound of the best-H fit).
FORMS: tuple[tuple[str, float, Form, float], ...] = (
    ("q = +0.5", 0.5, einstein_de_sitter, 2.0 / 3.0),
    ("q = 0", 0.0, milne, 1.0),
    ("q = -0.55", -0.55, accelerating, LCDM_A / (1.5 * math.sqrt(OMEGA_L))),
)


@dataclass
class Source:
    """One thrown source: its family, its number, its declared speed and
    its record at the detector."""

    name: str
    number: int
    content: int
    momentum: int
    declared_speed: float
    initial_distance: int
    turns: list[tuple[int, int]] = field(default_factory=list)  # record lines (tick, phase)
    # The click lines per interval: tick -> the rows' (amount, reading, phase);
    # the `reading` of a row is the age moment of its group (the rows of
    # one number met in one interval), amount x age summed over the group.
    clicks: dict[int, list[tuple[int, int, int]]] = field(default_factory=dict)
    steps: list[int] = field(default_factory=list)  # step ticks (GameBoard)
    left: int | None = None  # the tick it stepped off the GameBoard, if it did

    def arrivals(self) -> list[tuple[int, int, float, int]]:
        """The arrivals per interval: (tick, the amount clicked, the mean
        age of the group = its age moment over its amount, the phase of the
        group's last row)."""
        found = []
        for tick in sorted(self.clicks):
            rows = self.clicks[tick]
            total = sum(amount for amount, _, _ in rows)
            found.append((tick, total, rows[0][1] / total, rows[-1][2]))
        return found


@dataclass
class Point:
    """One source in one window: the detector's readings and the checks."""

    name: str
    lines: int
    z: float
    k: float
    v_record: float
    tau: float
    d: float
    v_steps: float | None
    k_replay: float | None
    v_replay: float | None
    momentum_ratio: float | None
    declared: float
    own_tau: float
    # The source's declared initial distance r_0 in Links (a GameBoard
    # quantity), for the throw from one point.
    initial_distance: float = 0.0
    # The clock the point is read in: 1 the lattice's interval count, r_w
    # the detector's own self-creations per interval; z is in this clock.
    clock_rate: float = 1.0
    # The same point's z in the lattice's clock (nan when z already is).
    z_lattice: float = math.nan

    @property
    def predicted(self) -> float:
        """The reading's formula from the record's own k and v in the
        point's clock: (1 + k)(1 + v / c) r - 1, r the clock's rate (1 in
        the lattice's clock)."""
        return (1.0 + self.k) * (1.0 + self.v_record) * self.clock_rate - 1.0


@dataclass
class Fit:
    """The fits of one window's diagram."""

    t0: float
    hubble: float
    hubble_intercept: tuple[float, float]
    rms_far: dict[str, float]
    best: dict[str, tuple[float, float]]
    q_effective: float | None
    points: list[Point]
    # The clock's rate the fit is read in (1 the lattice's) and where the
    # rate came from (the replay's edges or the run's own state).
    clock_rate: float = 1.0
    clock_kind: str = KIND_LATTICE


@dataclass
class Run:
    crowd: str
    clock: str
    ticks: int
    completed: bool
    balanced: bool
    elapsed: float
    c: float
    modulus: int
    rho: float
    detector_rate: float
    sources: dict[str, Source]
    document: dict[str, object]
    replay: dict[int, dict[int, tuple[int, int, tuple[int, int, int], list[int]]]] = field(
        default_factory=dict
    )
    # The fits per window in the detector's own clock (the pinned reading)
    # and in the lattice's clock (printed, not counted).
    fits: dict[tuple[int, int], Fit] = field(default_factory=dict)
    lattice_fits: dict[tuple[int, int], Fit] = field(default_factory=dict)
    rates: dict[tuple[int, int], float] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return f"{self.crowd}_{self.clock}"

    def window_rate(self, window: tuple[int, int]) -> tuple[float, str]:
        """The detector's own clock over the window, self-creations per
        interval: its age from its state at the window's edges over the
        intervals between them (a step of the replay: GAMEBOARD until the
        strict run), else its own record over the whole run, age / (age +
        waited) of its state (DETECTOR)."""
        lo, hi = window
        if lo in self.replay and hi in self.replay and DETECTOR_NUMBER in self.replay[hi]:
            age0 = self.replay[lo][DETECTOR_NUMBER][0]
            age1 = self.replay[hi][DETECTOR_NUMBER][0]
            return (age1 - age0) / (hi - lo), (
                f"{KIND_BOARD} the detector's age at the window's edges, from the replay's "
                "state (until the strict run with the reader's own lamp)"
            )
        return self.detector_rate, (
            f"{KIND_DETECTOR} the detector's own record over the run, age / (age + waited) of its state"
        )


def read_run(folder: Path) -> Run:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    document = world_of_run(folder)
    model = str(record["model"])
    crowd, clock = model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)].split("-")
    table = direction_flight(tuple(tuple(v) for v in record["directions"]))
    heading = np.array([HEADING_OFFSET])
    period = int(table.period[HEADING_OFFSET])
    c = int(table.manhattan_steps(heading, np.array([period]))[0]) / period
    width = int(record["width"])
    numbers = {int(k): v for k, v in record["numbers"].items()}
    sources: dict[str, Source] = {}
    # A thrown source is a measured event declared with a momentum (the
    # detector and the masses inside are fixed and declare none).
    for number, entry in sorted(numbers.items()):
        family = str(entry["family"])
        declared = document["measured"][number - 1]
        if "momentum" not in declared:
            continue
        content = int(declared["amount"])
        p = max(abs(int(v)) for v in declared["momentum"])
        centre = document["measured"][0]["position"]
        distance = sum(abs(int(a) - int(b)) for a, b in zip(declared["position"], centre, strict=True))
        sources[family] = Source(family, number, content, p, p / (Q * width * content + p), distance)
    by_number = {source.number: source for source in sources.values()}
    refuse_trimmed_record(folder)
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            event = json.loads(line)
            kind = event["event"]
            if kind == "record" and event["detector"] == DETECTOR:
                if event["phase"] is not None:
                    sources[event["family"]].turns.append((int(event["tick"]), int(event["phase"])))
            elif kind == "click" and event["detector"] == DETECTOR:
                sources[event["family"]].clicks.setdefault(int(event["tick"]), []).append(
                    (int(event["amount"]), int(event["reading"]), int(event["phase"]))
                )
            elif kind == "step":
                by_number[int(event["number"])].steps.append(int(event["tick"]))
            elif (
                kind == "click"
                and event["measured"] in by_number
                and event["detector"].startswith("face:")
            ):
                by_number[int(event["measured"])].left = int(event["tick"])
    centre = next(m for m in record["measured"] if m["number"] == 1)
    source_content = next(iter(sources.values())).content
    # The clock's rate [n, d] off the engine's own parser (an integer K
    # is [1, K]): rho is the content's phase steps per self-creation.
    turn_rate = parse_nature_beam_world(document).turn_rate
    return Run(
        crowd=crowd,
        clock=clock,
        ticks=int(record["completed_ticks"]),
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        elapsed=float(record["elapsed_seconds"]),
        c=c,
        modulus=int(record["N"]),
        rho=source_content * turn_rate[0] / turn_rate[1],
        detector_rate=int(centre["age"]) / (int(centre["age"]) + int(centre["waited"])),
        sources=sources,
        document=document,
    )


def replay(run: Run) -> None:
    """The world replayed through the API: every measured event's (age,
    waited, position, momentum) at every window edge, the host's view of
    the clocks' counts and the steps (GameBoard readings, the check)."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(run.document))
    edges = sorted({edge for window in WINDOWS for edge in window})
    for tick in range(1, min(max(edges), run.ticks) + 1):
        simulation.step()
        if tick in edges:
            run.replay[tick] = {
                n: (m.age, m.waited, m.position, list(m.momentum))
                for n, m in simulation.measured.items()
            }


def unwrap(phases: list[int], modulus: int) -> list[int]:
    """The phases unwrapped as forward turns: every difference taken in
    [0, N)."""
    found = [0]
    for before, after in zip(phases, phases[1:], strict=False):
        found.append(found[-1] + (after - before) % modulus)
    return found


def slope(x: list[float], y: list[float]) -> float:
    """The least-squares slope of y on x."""
    xs, ys = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    dx = xs - xs.mean()
    denominator = float((dx * dx).sum())
    return float((dx * (ys - ys.mean())).sum() / denominator) if denominator > 0 else math.nan


def links(ages: list[float]) -> np.ndarray:
    """The Links a row crossed by its age on a heading, m(age) of the flight
    table (the same on every heading; a group's mean age to the nearest
    interval)."""
    direction = np.full(len(ages), HEADING_OFFSET, dtype=np.int64)
    whole = np.asarray([round(age) for age in ages], dtype=np.int64)
    return HEADINGS_FLIGHT.manhattan_steps(direction, whole)


def window_point(run: Run, source: Source, window: tuple[int, int]) -> Point | None:
    lo, hi = window
    turns = [(t, p) for t, p in source.turns if lo <= t < hi]
    arrivals = [(t, a, age, p) for t, a, age, p in source.arrivals() if lo <= t < hi]
    if len(turns) < MIN_LINES or len(arrivals) < MIN_LINES:
        return None
    phi = unwrap([p for _, p in turns], run.modulus)
    ticks = [float(t) for t, _ in turns]
    # 1 + z = rho x (detector intervals per phase step).
    z = run.rho * slope([float(v) for v in phi], ticks) - 1.0
    # The emitter's own rate from the same record: the emission ticks are
    # tick - age, the emissions between two arrivals Delta Phi / rho.
    click_phi = [float(v) for v in unwrap([p for _, _, _, p in arrivals], run.modulus)]
    emitted = [float(t - age) for t, _, age, _ in arrivals]
    distances = links([age for _, _, age, _ in arrivals]).astype(float).tolist()
    k = run.rho * slope(click_phi, emitted) - 1.0
    v_record = slope(emitted, distances) / run.c
    first, last = int(min(emitted)), int(max(emitted))
    v_steps = (
        sum(1 for t in source.steps if first <= t <= last) / (last - first) / run.c
        if last > first
        else None
    )
    k_replay = v_replay = momentum_ratio = None
    if lo in run.replay and hi in run.replay and source.number in run.replay[hi]:
        age0, waited0, at0, _ = run.replay[lo][source.number]
        age1, waited1, at1, p1 = run.replay[hi][source.number]
        k_replay = (waited1 - waited0) / (age1 - age0) if age1 > age0 else math.nan
        v_replay = sum(abs(a - b) for a, b in zip(at1, at0, strict=True)) / (hi - lo) / run.c
        momentum_ratio = max(abs(v) for v in p1) / source.momentum
    # The throw's own coasting form (the declared world): a source of speed
    # v from r_0 is at r_0 + v t_e when its light leaves and observed at
    # t_0 = t_e + tau with tau = d / c: tau = (r_0 + v t_0) / (c + v), and
    # z = v / c, the acoustic Doppler.
    t0 = (lo + hi) / 2.0
    own_tau = (source.initial_distance + source.declared_speed * t0) / (run.c + source.declared_speed)
    return Point(
        name=source.name,
        lines=len(turns),
        z=z,
        k=k,
        v_record=v_record,
        tau=float(np.mean([age for _, _, age, _ in arrivals])),
        d=float(np.mean(distances)),
        v_steps=v_steps,
        k_replay=k_replay,
        v_replay=v_replay,
        momentum_ratio=momentum_ratio,
        declared=source.declared_speed / run.c,
        own_tau=own_tau,
        initial_distance=float(source.initial_distance),
    )


def rms(points: list[Point], form: Form, hubble: float) -> float:
    if not points:
        return math.nan
    return math.sqrt(sum((p.z - form(hubble * p.tau)) ** 2 for p in points) / len(points))


def best_hubble(points: list[Point], form: Form, pole: float) -> tuple[float, float]:
    """The H of the least rms of a form over the points, by a golden
    search below the form's pole."""
    top = 0.999 * pole / max(p.tau for p in points)
    lo, hi = 0.0, top
    golden = (math.sqrt(5.0) - 1.0) / 2.0
    a = hi - golden * (hi - lo)
    b = lo + golden * (hi - lo)
    fa, fb = rms(points, form, a), rms(points, form, b)
    for _ in range(80):
        if fa < fb:
            hi, b, fb = b, a, fa
            a = hi - golden * (hi - lo)
            fa = rms(points, form, a)
        else:
            lo, a, fa = a, b, fb
            b = lo + golden * (hi - lo)
            fb = rms(points, form, b)
    h = (lo + hi) / 2.0
    return h, rms(points, form, h)


def fit_points(points: list[Point], t0: float) -> Fit:
    """The fits of one window's points: the linear law through the origin
    on the near part, the three forms at that H over the far part, the
    best H of each form over every point and the free quadratic."""
    near = [p for p in points if p.z <= NEAR] or points
    far = [p for p in points if p.z > NEAR]
    hubble = sum(p.z * p.tau for p in near) / sum(p.tau * p.tau for p in near)
    intercept_slope = slope([p.tau for p in near], [p.z for p in near])
    intercept = float(np.mean([p.z for p in near]) - intercept_slope * np.mean([p.tau for p in near]))
    rms_far = {label: rms(far, form, hubble) for label, _, form, _ in FORMS}
    best = {label: best_hubble(points, form, pole) for label, _, form, pole in FORMS}
    taus = np.array([p.tau for p in points])
    zs = np.array([p.z for p in points])
    design = np.stack([taus, taus * taus], axis=1)
    coefficients, *_ = np.linalg.lstsq(design, zs, rcond=None)
    a, b = float(coefficients[0]), float(coefficients[1])
    q_effective = 2.0 * (b / (a * a) - 1.0) if a > 0 else None
    return Fit(
        t0=t0,
        hubble=hubble,
        hubble_intercept=(intercept_slope, intercept),
        rms_far=rms_far,
        best=best,
        q_effective=q_effective,
        points=sorted(points, key=lambda p: p.tau),
    )


def fit_window(run: Run, window: tuple[int, int]) -> Fit | None:
    points = [p for p in (window_point(run, s, window) for s in run.sources.values()) if p is not None]
    if len(points) < 3:
        return None
    return fit_points(points, (window[0] + window[1]) / 2.0)


def in_detector_clock(fit: Fit, rate: float, kind: str) -> Fit:
    """The same window's fit restated in the detector's own clock at the
    rate r (self-creations per interval): every point 1 + z_d = r (1 +
    z), the linear law through the detector's own zero z_d(0) = r - 1 so
    H_d = r H (with an intercept the same slope, the intercept r (1 + z(0))
    - 1), the three forms 1 + z_d = r (1 + form(H tau)) so every rms is r
    times the lattice's at the same H and the nearest form is the same,
    the free quadratic on z_d - z_d(0) = r z so q_eff,d = 2 ((q_eff / 2 +
    1) / r - 1); tau stays the row's own clock (its age at the click,
    record 707: the moving thing's clock, a separate reading). The
    product H_d t_0 is the same under either convention of tau: with tau
    and t_0 in the detector's count, tau_d = r tau and t_0,d = r t_0, the
    slope of z_d per unit of tau_d is H and H_d t_0,d = r H t_0 as well,
    so the Milne pin is convention-free."""
    points = [
        Point(
            p.name,
            p.lines,
            rate * (1.0 + p.z) - 1.0,
            p.k,
            p.v_record,
            p.tau,
            p.d,
            p.v_steps,
            p.k_replay,
            p.v_replay,
            p.momentum_ratio,
            p.declared,
            p.own_tau,
            p.initial_distance,
            clock_rate=rate,
            z_lattice=p.z,
        )
        for p in fit.points
    ]
    slope_lattice, intercept_lattice = fit.hubble_intercept
    q_effective = None if fit.q_effective is None else 2.0 * ((fit.q_effective / 2.0 + 1.0) / rate - 1.0)
    return Fit(
        t0=fit.t0,
        hubble=rate * fit.hubble,
        hubble_intercept=(rate * slope_lattice, rate * (1.0 + intercept_lattice) - 1.0),
        rms_far={label: rate * value for label, value in fit.rms_far.items()},
        best={label: (h, rate * r) for label, (h, r) in fit.best.items()},
        q_effective=q_effective,
        points=points,
        clock_rate=rate,
        clock_kind=kind,
    )


def doppler_part(fit: Fit) -> Fit:
    """The same fits on the Doppler part of the reading alone, z_D = v / c
    from the record's emission ticks and distances (the emitter's clock
    removed): printed after the runs, not a pinned reading."""
    points = [
        Point(
            p.name,
            p.lines,
            p.v_record,
            0.0,
            p.v_record,
            p.tau,
            p.d,
            p.v_steps,
            p.k_replay,
            p.v_replay,
            p.momentum_ratio,
            p.declared,
            p.own_tau,
            p.initial_distance,
        )
        for p in fit.points
    ]
    return fit_points(points, fit.t0)


def from_one_point(fit: Fit, c: float) -> Fit:
    """The same fits with every source's light-travel time reduced by
    (r_0 / c) / (1 + z): the throw from one point. A coasting source thrown
    from r_0 at the speed v is the source thrown from the centre at the
    time -r_0 / v; at t_0 it is read at tau = (r_0 + v t_0) / (c + v), the
    source from the centre at v t_0 / (c + v), so the difference is r_0 /
    (c + v) = (r_0 / c) / (1 + z) with z = v / c. Exact for the coasting
    throw, first order for the pushing one; r_0 is the declared initial
    distance (a GameBoard quantity). Printed after the runs, not pinned."""
    points = [
        Point(
            p.name,
            p.lines,
            p.z,
            p.k,
            p.v_record,
            p.tau - (p.initial_distance / c) / (1.0 + p.z),
            p.d,
            p.v_steps,
            p.k_replay,
            p.v_replay,
            p.momentum_ratio,
            p.declared,
            p.own_tau,
            0.0,
        )
        for p in fit.points
    ]
    return fit_points(points, fit.t0)


def near_fit_of_the_coasting_form(fit: Fit) -> float:
    """What the near fit reads off an exact coasting throw from one point
    at this window's own taus: H t_0 of the linear law through the origin
    on z <= NEAR for z = H tau / (1 - H tau) with H = 1 / t_0 (the Milne
    curvature (H tau)^2 read as a larger H; 1 would be an unbiased fit)."""
    exact = [
        Point(
            p.name,
            p.lines,
            milne(p.tau / fit.t0),
            0.0,
            0.0,
            p.tau,
            p.d,
            None,
            None,
            None,
            None,
            0.0,
            p.tau,
        )
        for p in fit.points
    ]
    return fit_points(exact, fit.t0).hubble * fit.t0


def find_runs(root: Path) -> list[Run]:
    found = []
    for path in sorted(root.rglob("run.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        model = str(record.get("model", ""))
        if model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX):
            found.append(read_run(path.parent))
    order = {"coasting": 0, "pushing": 1}
    return sorted(found, key=lambda r: (order.get(r.crowd, 9), r.clock != "scalar"))


def fmt(value: float | None, digits: int = 4) -> str:
    return (
        "-"
        if value is None or (isinstance(value, float) and math.isnan(value))
        else f"{value:.{digits}f}"
    )


def print_points(run: Run, window: tuple[int, int], fit: Fit) -> list[tuple[str, bool]]:
    """The points of one window in the detector's own clock (the pinned
    reading), the lattice's z beside each as [GAMEBOARD, the lattice's
    clock]; the formula criterion per source."""
    criteria: list[tuple[str, bool]] = []
    rate = fit.clock_rate
    print(
        f"{KIND_DETECTOR} `{run.name}`, the window [{window[0]}, {window[1]}), t_0 = {fit.t0:.0f}, in "
        f"the detector's own clock (its rate r_w = {rate:.4f} self-creations per interval over the "
        f"window: {fit.clock_kind}): per source, 1 + z_d = r_w (1 + z), z from the pointer's turn "
        "per interval, tau the mean age of the arrivals (the row's own clock), d = m(tau); k and v "
        f"from the record's emission ticks (tick - age) and distances; z {KIND_LATTICE}; the checks "
        f"{KIND_BOARD}: v / c declared and the throw's own coasting form tau_own = (r_0 + v t_0) / "
        "(c + v) with z_own = (1 + v / c) r_w - 1, v / c from the `step` lines, the replay's k, v and "
        "the momentum left, p(t) / p(0)"
    )
    print(
        "| source | v / c declared | z_own | tau_own | lines | z_d read | z (lattice) | k (record) | "
        "v / c (record) | (1 + k)(1 + v / c) r_w - 1 | ratio (1 + z_d) | tau | d (Links) | "
        "v / c (steps) | k (replay) | v / c (replay) | p(t) / p(0) |"
    )
    print(
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | "
        "--- | --- |"
    )
    for p in fit.points:
        ratio = (1.0 + p.z) / (1.0 + p.predicted)
        inside = abs(ratio - 1.0) <= FORMULA_TOLERANCE
        criteria.append(
            (
                f"{run.name} [{window[0]}, {window[1]}) {p.name}: the reading's formula "
                "(the detector's clock)",
                inside,
            )
        )
        z_own = (1.0 + p.declared) * rate - 1.0
        print(
            f"| {p.name} | {p.declared:.4f} | {z_own:+.4f} | {p.own_tau:.1f} | {p.lines} | {p.z:+.4f} | "
            f"{fmt(p.z_lattice)} | {p.k:.4f} | {p.v_record:.4f} | {p.predicted:+.4f} | "
            f"{ratio:.4f} {'inside' if inside else 'outside'} | {p.tau:.1f} | {p.d:.1f} | "
            f"{fmt(p.v_steps)} | {fmt(p.k_replay)} | {fmt(p.v_replay)} | {fmt(p.momentum_ratio)} |"
        )
    missing = [s.name for s in run.sources.values() if all(p.name != s.name for p in fit.points)]
    if missing:
        print(f"(not read in this window, fewer than {MIN_LINES} lines: {', '.join(missing)})")
    own_z = math.sqrt(
        sum((p.z - ((1.0 + p.declared) * rate - 1.0)) ** 2 for p in fit.points) / len(fit.points)
    )
    own_tau = math.sqrt(sum((p.tau - p.own_tau) ** 2 for p in fit.points) / len(fit.points))
    blue = sum(1 for p in fit.points if p.z < 0.0)
    print(
        f"{KIND_BOARD} the throw's own coasting form against the reading in the detector's clock: rms "
        f"of z_d - ((1 + v / c) r_w - 1) {own_z:.4f}, rms of tau - tau_own {own_tau:.1f} intervals; "
        f"sources read blue (z_d < 0, v / c below 1 / r_w - 1 = {1.0 / rate - 1.0:.4f}): {blue} of "
        f"{len(fit.points)}"
    )
    print()
    return criteria


def print_fit(
    run: Run, window: tuple[int, int], fit: Fit, kind: str = KIND_DETECTOR
) -> list[tuple[str, bool]]:
    """The fits of one window: in the detector's own clock (`kind`
    DETECTOR, the pinned reading, its criteria returned) or in the
    lattice's clock (`kind` the lattice's, printed and counted in no
    criterion: the criteria returned are the lattice's, for the record)."""
    criteria: list[tuple[str, bool]] = []
    coasting = run.crowd == "coasting"
    ht = fit.hubble * fit.t0
    h_links = fit.hubble / run.c
    clock = (
        f"in the detector's own clock (r_w = {fit.clock_rate:.4f})"
        if kind == KIND_DETECTOR
        else "in the lattice's clock, as the register read it until 2026-09-22 (not counted)"
    )
    print(
        f"{kind} `{run.name}`, the window [{window[0]}, {window[1]}) {clock}: the linear law on the "
        f"near part (z <= {NEAR} in the lattice's clock) through the clock's own zero z_d(0) = r_w - 1: "
        f"H = {fit.hubble:.5f} per interval ({h_links:.5f} per Link), "
        f"H t_0 = {ht:.4f} (Milne: 1); with an intercept: H = {fit.hubble_intercept[0]:.5f}, "
        f"z(0) = {fit.hubble_intercept[1]:+.4f}; the free quadratic's q_eff = {fmt(fit.q_effective, 3)}"
    )
    print(
        "| form | rms over the far part at the near fit's H | best H over every point | its H t_0 | its rms |"
    )
    print("| --- | --- | --- | --- | --- |")
    for label, _, _, _ in FORMS:
        h, r = fit.best[label]
        print(f"| {label} | {fmt(fit.rms_far[label])} | {h:.5f} | {h * fit.t0:.4f} | {r:.4f} |")
    finite = {k: v for k, v in fit.rms_far.items() if math.isfinite(v)}
    nearest = min(finite, key=lambda k: finite[k]) if finite else "-"
    farthest = max(finite, key=lambda k: finite[k]) if finite else "-"
    print(
        f"the far part resembles {nearest} (the least rms) and least {farthest}; "
        f"what is observed today (q = -0.55) is {'the nearest' if nearest == 'q = -0.55' else 'not the nearest'}"
    )
    clock_tag = "the detector's clock" if kind == KIND_DETECTOR else "the lattice's clock"
    tag = f"{run.name} [{window[0]}, {window[1]}) ({clock_tag})"
    if coasting:
        criteria.append((f"{tag}: H t_0 = 1 within 10 %", abs(ht - 1.0) <= HUBBLE_TIME_TOLERANCE))
        criteria.append((f"{tag}: the coasting form q = 0 the nearest of the three", nearest == "q = 0"))
        criteria.append(
            (f"{tag}: the coasting form's rms below {COASTING_RMS}", fit.rms_far["q = 0"] < COASTING_RMS)
        )
    else:
        criteria.append((f"{tag}: H t_0 < 1", ht < 1.0))
        criteria.append((f"{tag}: q_eff > 0", fit.q_effective is not None and fit.q_effective > 0))
        criteria.append(
            (f"{tag}: the accelerating form the farthest of the three", farthest == "q = -0.55")
        )
    criteria.append((f"{tag}: what is observed today (q = -0.55) the nearest", nearest == "q = -0.55"))
    if kind != KIND_DETECTOR:
        for label, ok in criteria:
            print(f"{kind} {'inside' if ok else 'outside'}, not counted: {label}")
    print()
    return criteria


def print_bends(runs: list[Run], window: tuple[int, int]) -> None:
    by_name = {r.name: r for r in runs}
    for crowd in ("coasting", "pushing"):
        scalar, age = by_name.get(f"{crowd}_scalar"), by_name.get(f"{crowd}_age")
        if scalar is None or age is None:
            continue
        fs, fa = scalar.fits.get(window), age.fits.get(window)
        if fs is None or fa is None:
            continue
        print(
            f"{KIND_DETECTOR} the bend of the age clock, the {crowd} crowd, the window "
            f"[{window[0]}, {window[1]}): z_age - z_scalar per source in each detector's own clock "
            f"(r_w {fs.clock_rate:.4f} and {fa.clock_rate:.4f}; reported, no bracket)"
        )
        print("| source | tau (scalar) | z scalar | z age | z age - z scalar | k scalar | k age |")
        print("| --- | --- | --- | --- | --- | --- | --- |")
        age_points = {p.name: p for p in fa.points}
        for p in fs.points:
            a = age_points.get(p.name)
            if a is None:
                continue
            print(
                f"| {p.name} | {p.tau:.1f} | {p.z:.4f} | {a.z:.4f} | {a.z - p.z:+.4f} | {p.k:.4f} | {a.k:.4f} |"
            )
        print()


def print_from_one_point(run: Run, fit: Fit) -> None:
    """The `--from-one-point` block of one window: the reading and its
    Doppler part with every tau reduced by (r_0 / c) / (1 + z), and the
    near fit's own reading of an exact coasting form at these taus."""
    bias = near_fit_of_the_coasting_form(fit)
    print(
        f"{KIND_LATTICE} `{run.name}`: the near fit's own reading of an exact coasting throw from one "
        f"point at this window's taus (z = H tau / (1 - H tau), H = 1 / t_0): H t_0 = {bias:.4f} "
        "(1 would be unbiased; the far part of that exact form lies below the coasting form at this H)"
    )
    for label, shifted in (
        ("the throw from one point", from_one_point(fit, run.c)),
        ("the Doppler part alone from one point", from_one_point(doppler_part(fit), run.c)),
    ):
        finite = {k: v for k, v in shifted.rms_far.items() if math.isfinite(v)}
        nearest = min(finite, key=lambda k: finite[k]) if finite else "-"
        best = min(shifted.best, key=lambda k: shifted.best[k][1])
        print(
            f"{KIND_LATTICE} `{run.name}`: {label}, every tau reduced by (r_0 / c) / (1 + z) "
            f"(r_0 the declared initial distance {KIND_BOARD}; printed after the runs, not a pinned "
            f"reading): the near fit's H t_0 = {shifted.hubble * shifted.t0:.4f}; the far part's rms at "
            "that H "
            + ", ".join(f"{k} {fmt(v)}" for k, v in shifted.rms_far.items())
            + f", the nearest {nearest}; the best-H rms "
            + ", ".join(
                f"{k} {fmt(r)} (H t_0 {h * shifted.t0:.3f})" for k, (h, r) in shifted.best.items()
            )
            + f", the best {best}; q_eff = {fmt(shifted.q_effective, 3)}"
        )


def write_png(runs: list[Run], directory: Path) -> None:
    """The diagrams with matplotlib, in the given directory (the repository
    gets the numbers, not the pictures)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    directory.mkdir(parents=True, exist_ok=True)
    for window in WINDOWS:
        figure, axes = plt.subplots(1, len(runs), figsize=(4.2 * len(runs), 4.0), squeeze=False)
        for axis, run in zip(axes[0], runs, strict=True):
            fit = run.fits.get(window)
            if fit is None:
                continue
            taus = np.linspace(0.0, max(p.tau for p in fit.points) * 1.05, 200)
            for (label, _, form, _), style in zip(FORMS, ("--", "-", ":"), strict=True):
                axis.plot(taus, [form(fit.hubble * t) for t in taus], style, label=label)
            axis.plot([p.tau for p in fit.points], [p.z for p in fit.points], "o", label="the detector")
            axis.set_title(f"{run.name}, t_0 = {fit.t0:.0f}, H t_0 = {fit.hubble * fit.t0:.2f}")
            axis.set_xlabel("light-travel time tau (intervals) = the age of the arriving ray")
            axis.set_ylabel("z")
            axis.set_ylim(0, 1.0)
            axis.legend(fontsize=8)
        figure.tight_layout()
        figure.savefig(directory / f"hubble_{window[0]}_{window[1]}.png", dpi=110)
        plt.close(figure)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="the folder holding the run folders")
    parser.add_argument("--png", type=Path, help="write the diagrams with matplotlib into this folder")
    parser.add_argument("--no-replay", action="store_true", help="skip the replay (the check columns)")
    parser.add_argument(
        "--from-one-point",
        action="store_true",
        help="also fit every window with each tau reduced by (r_0 / c) / (1 + z), the throw from one point",
    )
    args = parser.parse_args(argv)
    runs = find_runs(args.root)
    if not runs:
        print(f"no Hubble run under {args.root}", file=sys.stderr)
        return 2
    failed = 0
    for run in runs:
        for label, ok in (("completed", run.completed), ("balanced", run.balanced)):
            print(
                f"{'PASS' if ok else 'FAIL'} {run.name}: {label} ({run.ticks} ticks, {run.elapsed:.1f} s)"
            )
            failed += not ok
        left = [f"{s.name} at {s.left}" for s in run.sources.values() if s.left is not None]
        print(
            f"{KIND_DETECTOR} {run.name}: c = {run.c:.5f} Links per interval (the flight table), "
            f"rho = {run.rho:g} step per self-creation; the detector's own clock over the run "
            f"{run.detector_rate:.4f} self-creations per interval; sources that left the GameBoard: "
            f"{', '.join(left) if left else 'none'}"
        )
    print()
    criteria: list[tuple[str, bool]] = []
    for run in runs:
        if not args.no_replay:
            replay(run)
        for window in (*WINDOWS, LONG_WINDOW):
            fit = fit_window(run, window)
            if fit is not None:
                rate, kind = run.window_rate(window)
                run.rates[window] = rate
                run.lattice_fits[window] = fit
                run.fits[window] = in_detector_clock(fit, rate, kind)
    for window in (*WINDOWS, LONG_WINDOW):
        if window == LONG_WINDOW:
            print(
                f"The late half [{window[0]}, {window[1]}) as one window, printed after the runs for "
                "the grain of the step rule (not a pinned reading; its verdict lines are not counted):"
            )
            print()
        for run in runs:
            fit = run.fits.get(window)
            lattice = run.lattice_fits.get(window)
            if fit is None or lattice is None:
                print(f"`{run.name}`: no reading in the window [{window[0]}, {window[1]})")
                continue
            print(
                f"{KIND_DETECTOR} `{run.name}`, the window [{window[0]}, {window[1]}): the detector's "
                f"own clock over the window r_w = {fit.clock_rate:.4f} self-creations per interval "
                f"({fit.clock_kind}); the pinned reading below is in this clock, 1 + z_d = r_w (1 + z), "
                f"H_d = r_w H, z_d(0) = r_w - 1 = {fit.clock_rate - 1.0:+.4f}"
            )
            found = print_points(run, window, fit) + print_fit(run, window, fit)
            if window != LONG_WINDOW:
                criteria += found
            print_fit(run, window, lattice, KIND_LATTICE)
            doppler = doppler_part(lattice)
            finite = {k: v for k, v in doppler.rms_far.items() if math.isfinite(v)}
            nearest = min(finite, key=lambda k: finite[k]) if finite else "-"
            print(
                f"{KIND_LATTICE} `{run.name}`: the Doppler part alone, z_D = v / c from the record's "
                "emission ticks and distances (the emitter's clock removed; printed after the runs, not "
                f"a pinned reading): the near fit's H = {doppler.hubble:.5f}, H t_0 = "
                f"{doppler.hubble * doppler.t0:.4f}; the far part's rms at that H "
                + ", ".join(f"{label} {fmt(value)}" for label, value in doppler.rms_far.items())
                + f", the nearest {nearest}; q_eff = {fmt(doppler.q_effective, 3)}"
            )
            if args.from_one_point:
                print_from_one_point(run, lattice)
            print()
        print_bends(runs, window)
    if args.png is not None:
        write_png(runs, args.png)
    inside = sum(1 for _, ok in criteria if ok)
    for label, ok in criteria:
        if "formula" not in label:
            print(f"{'inside' if ok else 'outside'}: {label}")
    formula = [ok for label, ok in criteria if "formula" in label]
    print(
        f"the reading's formula: {sum(formula)} of {len(formula)} inside 2 %; "
        f"{failed} record check(s) failed; {inside} reading(s) inside, {len(criteria) - inside} outside "
        "(every criterion in the detector's own clock; the lattice's clock printed, not counted)"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
