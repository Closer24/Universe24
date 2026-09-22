"""The readings of series G2, the Hubble diagram with stars behind the
detector, under the Beam Law, in space (the model owner's question of
2026-09-20: "can you run a test of whether dark energy is needed? what
comes out of an experiment in our model? a star has to be placed there").

Reads the run folders of the worlds of `examples/events/hubble_stars/` (the
runner's `run.json`, `initialization.json` and `events.jsonl`, the folders
told apart by the `model` of their record, `rays-hubble-stars-<crowd>-
<clock>-space-v1`) and prints, per run and per window of the record, the
Hubble diagram the detector at the centre reads of the stars: per star (a
family of its own, a lamp holding a mass) the redshift z from the rate at
which the pointer of the detector's record turns, 1 + z = rho / (Delta Phi
/ Delta t), rho the star's declared turn per self-creation (its content
over K, 1 by design) and Delta Phi the unwrapped phase of the `record`
lines over Delta t detector intervals (a least-squares slope), the
distance from the ages of the arriving light on the click records
(`reading` = the age moment, amount x age, under `reads: "age"`; the
light-travel time tau = the age and the distance d = m(tau) Links, m the
Manhattan steps of the flight rule read through the engine's own
`direction_flight`, whose period also gives c), and the luminosity, the click
rate of the star's light per detector interval (expected 1 / (1 + z) of
the lamp's rate: a beam does not dilute, so the click rate carries no
distance beyond the redshift; README.md there).

The pinned reading is in the detector's own clock (the model owner,
2026-09-22, records 678 and 707 of docs/LOG_2026-09-20.md: a detector's
time is the clock of the Node it sits on, the interval count less what
the crowd at that Node owes through the age wall; series G's rule,
tools/hubble_readings.py). The detector's clock counts r self-creations
per interval, its own count of intervals stretched by what arrives at it,
the age wall's member at the coefficient 1 (the owner's record 709), read
off its own record over the run (age / (age + waited)
of its state in `run.json`, DETECTOR; the per-window step of series G,
the replay's edges, is not made here), and every reading of the lattice's
clock is restated by the one closed form 1 + z_d = r (1 + z): the near
fit's H_d = r H through the clock's own zero z_d(0) = r - 1, the forms
1 + z_d = r (1 + form(H tau)) with every rms r times the lattice's (the
nearest and the farthest unchanged, q of the free fit unchanged, its H
r times), the reading's formula (1 + z_d) = (1 + k)(1 + v / c) r (the
same ratio), the luminosity as the clicks per the detector's own count,
L_d = L / r, so L_d (1 + z_d) = L (1 + z) (the pin 1 / (1 + z) is
clock-free). The reading in the lattice's clock is printed beside it as
[GAMEBOARD, the lattice's clock] and counted in no criterion; the step
rule's longest burst (a `step` record) is printed as a GameBoard
diagnostic and counted in no criterion (2026-09-22).

Every number is labelled by its kind (the model owner, 2026-09-20): a
DETECTOR reading is the record of the detector's set or of a measured event
in the world (clicks, the pointer, phases, the ages of arrivals, an owed
count; the only kind reality has); a GAMEBOARD reading is the host's view
of the GameBoard (a star's position, steps and momentum from the run's
record, its `read` lines, the homes, the books; exists for us, not in
reality). The Hubble diagram and its fits are made of detector readings
only; a star's speed from its `step` records, the push it took and the
momentum it has left are the check columns.

The fits, per window (the lesson of series G: a near fit through the
origin reads the coasting form's own curvature as a larger H, so every
form is fitted with H free over every point, and the criterion is
validated on the exact expected points before the run):

- the three exact forms in the light-travel time, each with its best H
  over every point and its rms: q = +0.5 (Einstein-de Sitter), q = 0
  (Milne, the coasting form) and q = -0.55 (flat Omega_m = 0.3, the
  accelerating form observed today);
- the power-law family a ~ t^n, 1 + z = (1 - (1 + q) H tau)^(-1 / (1 +
  q)), with H and q both free (`fit_q`): the deceleration parameter the
  diagram reads by itself, q = 0 coasting, q > 0 decelerating, q < 0
  accelerating;
- the linear law through the origin on the near part (z <= 0.2) and the
  free quadratic's q_eff, printed for continuity with series G, not
  pinned.

The record checks (completed, the books balanced at every tick) fail the
tool; the readings are registered inside or outside their expectation
(`expectations.json` beside the worlds, written by the generator before
the runs) and never moved.

    PYTHONPATH=src python tools/hubble_stars_readings.py artifacts/hubble_stars [--png DIR] [--expectations FILE] [--json FILE]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np

from event_universe.core.game_board import PORT_HEADINGS
from event_universe.events import parse_nature_beam_world
from event_universe.events.nature_beam import direction_flight
from event_universe.events.world import HEADING_OFFSET, Q
from event_universe.world_loading import world_of_run

ROOT = Path(__file__).resolve().parents[1]
MODEL_PREFIX = "rays-hubble-stars-"
MODEL_SUFFIX = "-space-v1"
DETECTOR = "centre"
MASS_FAMILY = "mass"
WINDOWS = ((100, 200), (200, 300), (300, 400))
REGISTERED_WINDOW = (300, 400)
NEAR = 0.2
MIN_LINES = 10
EXPECTATIONS = ROOT / "examples" / "events" / "hubble_stars" / "expectations.json"
# The reading's formula within 2 % (series G's pin, kept), the luminosity
# within 5 % of 1 / (1 + z) (the grain of a rate over a hundred intervals).
FORMULA_TOLERANCE = 0.02
LUMINOSITY_TOLERANCE = 0.05
OMEGA_M = 0.3
OMEGA_L = 1.0 - OMEGA_M
LCDM_A = math.asinh(math.sqrt(OMEGA_L / OMEGA_M))
Form = Callable[[float], float]
KIND_DETECTOR = "[DETECTOR]"
KIND_BOARD = "[GAMEBOARD]"
# The reading in the lattice's clock, as the register read it until
# 2026-09-22: printed beside the detector's clock, counted in no criterion.
KIND_LATTICE = "[GAMEBOARD, the lattice's clock]"
# The flight's constants of the six headings (the two rest vectors first): m(age)
# and c are the same on every heading.
HEADINGS_FLIGHT = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))


def beam_speed() -> float:
    """c, the Links a ray makes on a heading in one period over the period
    (32 / 55 = 0.58182 per interval), off the flight rule."""
    heading = np.array([HEADING_OFFSET])
    period = int(HEADINGS_FLIGHT.period[HEADING_OFFSET])
    return int(HEADINGS_FLIGHT.manhattan_steps(heading, np.array([period]))[0]) / period


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


def power_law(x: float, q: float) -> float:
    """The family a ~ t^n with q = (1 - n) / n: 1 + z = (1 - (1 + q) H
    tau)^(-1 / (1 + q)); q = 0 is the coasting form, q = +0.5 Einstein-de
    Sitter, q -> -1 the exponential (de Sitter) form."""
    if q <= -1.0:
        return math.exp(x) - 1.0
    inner = 1.0 - (1.0 + q) * x
    return inner ** (-1.0 / (1.0 + q)) - 1.0 if inner > 0 else math.inf


# The three forms in the order of the deceleration parameter, with the H tau
# at which each has its pole (the search bound of the best-H fit).
FORMS: tuple[tuple[str, float, Form, float], ...] = (
    ("q = +0.5", 0.5, einstein_de_sitter, 2.0 / 3.0),
    ("q = 0", 0.0, milne, 1.0),
    ("q = -0.55", -0.55, accelerating, LCDM_A / (1.5 * math.sqrt(OMEGA_L))),
)
Q_GRID = np.linspace(-0.95, 1.5, 246)


@dataclass
class Star:
    """One thrown star: its family, its number, its declared speed and
    initial distance, and its record at the detector."""

    name: str
    number: int
    content: int
    momentum: int
    declared_speed: float
    initial_distance: int
    turns: list[tuple[int, int]] = field(default_factory=list)  # record lines (tick, phase)
    # The click lines per interval: tick -> the rows' (amount, reading, phase).
    clicks: dict[int, list[tuple[int, int, int]]] = field(default_factory=dict)
    steps: list[int] = field(default_factory=list)  # step ticks (GameBoard)
    # The pushes the star took, (tick, the push component along its axis,
    # signed outward positive), from its `read` lines (GameBoard).
    pushes: list[tuple[int, int]] = field(default_factory=list)
    homes: int = 0  # the rows of its own that came home (GameBoard)
    left: int | None = None  # the tick it stepped off the GameBoard, if it did
    final_momentum: int | None = None  # |p| at the end of the run (GameBoard)

    def arrivals(self) -> list[tuple[int, int, float, int]]:
        """The arrivals per interval: (tick, the amount clicked, the mean
        age of the group, the phase of the group's last row)."""
        found = []
        for tick in sorted(self.clicks):
            rows = self.clicks[tick]
            total = sum(amount for amount, _, _ in rows)
            found.append((tick, total, rows[0][1] / total, rows[-1][2]))
        return found


@dataclass
class Point:
    """One star in one window: the detector's readings and the checks."""

    name: str
    lines: int
    z: float
    k: float
    v_record: float
    tau: float
    d: float
    rate: float  # the click rate per detector interval (the luminosity)
    declared: float  # v / c declared (GameBoard)
    v_steps: float | None = None  # v / c from the step lines (GameBoard)
    push_fraction: float | None = None  # the window's pushes over p(0) (GameBoard)
    momentum_ratio: float | None = None  # |p(end)| / p(0) (GameBoard)
    # The step rule under a changing momentum (GameBoard): the longest stall
    # (intervals between two steps) and the longest burst (steps on
    # consecutive intervals) over the window's emission span.
    stall: int | None = None
    burst: int | None = None
    # The clock the point is read in: 1 the lattice's interval count, r the
    # detector's own self-creations per interval; z and rate are in it.
    clock_rate: float = 1.0
    # The same point's z in the lattice's clock (nan when z already is).
    z_lattice: float = math.nan

    @property
    def predicted(self) -> float:
        """The reading's formula from the record's own k and v in the
        point's clock: (1 + k)(1 + v / c) r - 1, r the clock's rate."""
        return (1.0 + self.k) * (1.0 + self.v_record) * self.clock_rate - 1.0


@dataclass
class Fit:
    """The fits of one window's diagram: the best H and rms of the three
    forms, the free (H, q) of the power-law family with its rms, the near
    fit's H and the free quadratic's q_eff."""

    t0: float
    best: dict[str, tuple[float, float]]
    q_fit: float
    h_fit: float
    rms_fit: float
    hubble_near: float
    q_effective: float | None
    points: list[Point]
    # The clock's rate the fit is read in (1 the lattice's) and its source.
    clock_rate: float = 1.0
    clock_kind: str = KIND_LATTICE

    @property
    def nearest(self) -> str:
        finite = {k: v for k, (_, v) in self.best.items() if math.isfinite(v)}
        return min(finite, key=lambda k: finite[k]) if finite else "-"

    @property
    def farthest(self) -> str:
        finite = {k: v for k, (_, v) in self.best.items() if math.isfinite(v)}
        return max(finite, key=lambda k: finite[k]) if finite else "-"


@dataclass
class Run:
    crowd: str
    clock: str
    under_record: bool
    ticks: int
    completed: bool
    balanced: bool
    elapsed: float
    c: float
    modulus: int
    rho: float
    detector_rate: float
    stars: dict[str, Star]
    document: dict[str, object]
    fingerprint: str
    # The fits per window in the detector's own clock (the pinned reading)
    # and in the lattice's clock (printed, not counted).
    fits: dict[tuple[int, int], Fit] = field(default_factory=dict)
    lattice_fits: dict[tuple[int, int], Fit] = field(default_factory=dict)

    def own_clock(self) -> tuple[float, str]:
        """The detector's own clock, self-creations per interval, off its
        own record over the run (DETECTOR); the per-window step (the
        replay's edges, series G) is not made here."""
        return self.detector_rate, (
            f"{KIND_DETECTOR} the detector's own record over the run, age / (age + waited) of its "
            "state (the per-window step of series G not made here)"
        )

    @property
    def prefix(self) -> str:
        """The folder of the world: `record/` under the record click, none
        otherwise (the `doppler/` folder of the third run left with the key
        `doppler` on 2026-09-21, MIGRATION)."""
        return "record/" if self.under_record else ""

    @property
    def name(self) -> str:
        return f"{self.prefix}{self.crowd}_{self.clock}"


def axis_of(momentum: list[int]) -> tuple[int, int]:
    """The axis and the outward sign of a momentum along one axis."""
    axis = next(k for k in range(3) if momentum[k])
    return axis, 1 if momentum[axis] > 0 else -1


def read_run(folder: Path) -> Run:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    # The world as the engine read it (`resolved_initialization.json` where
    # the run resolved entity definitions, since the shipped worlds take
    # their families from `entities/families.json`).
    document = world_of_run(folder)
    model = str(record["model"])
    parts = model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)].split("-")
    # Under the record click (the world key `amplitude`, the model id
    # `rays-hubble-stars-record-<crowd>-<clock>-space-v1`) the `record`
    # lines are per record and the reading comes from the gather lines.
    under_record = parts[0] == "record"
    crowd, clock = parts[-2], parts[-1]
    table = direction_flight(tuple(tuple(v) for v in record["directions"]))
    heading = np.array([HEADING_OFFSET])
    period = int(table.period[HEADING_OFFSET])
    c = int(table.manhattan_steps(heading, np.array([period]))[0]) / period
    width = int(record["width"])
    numbers = {int(k): v for k, v in record["numbers"].items()}
    centre = document["measured"][0]["position"]
    stars: dict[str, Star] = {}
    # A star is a measured event declared with a momentum (the detector is
    # fixed and declares none); its content is its light plus the mass it
    # holds (the frame's M_A, the step rule's M).
    for number, entry in sorted(numbers.items()):
        family = str(entry["family"])
        declared = document["measured"][number - 1]
        if "momentum" not in declared:
            continue
        content = int(declared["amount"]) + sum(int(v) for v in declared.get("held", {}).values())
        p = max(abs(int(v)) for v in declared["momentum"])
        distance = sum(abs(int(a) - int(b)) for a, b in zip(declared["position"], centre, strict=True))
        stars[family] = Star(family, number, content, p, p / (Q * width * content + p), distance)
    by_number = {star.number: star for star in stars.values()}
    signs = {
        star.number: axis_of(document["measured"][star.number - 1]["momentum"])
        for star in stars.values()
    }
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            event = json.loads(line)
            kind = event["event"]
            if kind == "gather" and under_record and event["family"] in stars:
                # One gather per record, the world's row: the record's birth
                # phase u (the star's clock at the birth) and the interval
                # it arrived, the pointer's turn read off the world's list.
                stars[event["family"]].turns.append((int(event["arrived"]), int(event["u"])))
            elif kind == "record" and not under_record and event["detector"] == DETECTOR:
                if event["phase"] is not None and event["family"] in stars:
                    stars[event["family"]].turns.append((int(event["tick"]), int(event["phase"])))
            elif kind == "click" and event["detector"] == DETECTOR and event["family"] in stars:
                stars[event["family"]].clicks.setdefault(int(event["tick"]), []).append(
                    (int(event["amount"]), int(event["reading"]), int(event["phase"]))
                )
            elif kind == "step" and int(event["number"]) in by_number:
                by_number[int(event["number"])].steps.append(int(event["tick"]))
            elif kind == "read" and event["measured"] in by_number and event["family"] == MASS_FAMILY:
                axis, sign = signs[int(event["measured"])]
                by_number[int(event["measured"])].pushes.append(
                    (int(event["tick"]), sign * int(event["push"][axis]))
                )
            elif kind == "home" and event["measured"] in by_number:
                by_number[int(event["measured"])].homes += 1
            elif (
                kind == "click"
                and event.get("measured") in by_number
                and str(event["detector"]).startswith("face:")
            ):
                by_number[int(event["measured"])].left = int(event["tick"])
    for state in record["measured"]:
        if int(state["number"]) in by_number:
            by_number[int(state["number"])].final_momentum = max(abs(int(v)) for v in state["momentum"])
    detector_state = next(m for m in record["measured"] if m["number"] == 1)
    star_content = next(iter(stars.values())).content
    turn_rate = parse_nature_beam_world(document).turn_rate
    return Run(
        crowd=crowd,
        clock=clock,
        under_record=under_record,
        ticks=int(record["completed_ticks"]),
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        elapsed=float(record["elapsed_seconds"]),
        c=c,
        modulus=int(record["N"]),
        rho=star_content * turn_rate[0] / turn_rate[1],
        detector_rate=int(detector_state["age"])
        / max(1, int(detector_state["age"]) + int(detector_state["waited"])),
        stars=stars,
        document=document,
        fingerprint=str(record.get("source_sha256", "")),
    )


def unwrap(phases: list[int], modulus: int) -> list[int]:
    """The phases unwrapped as forward turns: every difference taken in [0, N)."""
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
    table (a group's mean age to the nearest interval)."""
    direction = np.full(len(ages), HEADING_OFFSET, dtype=np.int64)
    whole = np.asarray([round(age) for age in ages], dtype=np.int64)
    return HEADINGS_FLIGHT.manhattan_steps(direction, whole)


def window_point(run: Run, star: Star, window: tuple[int, int]) -> Point | None:
    lo, hi = window
    turns = [(t, p) for t, p in star.turns if lo <= t < hi]
    arrivals = [(t, a, age, p) for t, a, age, p in star.arrivals() if lo <= t < hi]
    if len(turns) < MIN_LINES or len(arrivals) < MIN_LINES:
        return None
    phi = unwrap([p for _, p in turns], run.modulus)
    ticks = [float(t) for t, _ in turns]
    # 1 + z = rho x (detector intervals per phase step).
    z = run.rho * slope([float(v) for v in phi], ticks) - 1.0
    # The star's own rate from the same record: the emission ticks are
    # tick - age, the emissions between two arrivals Delta Phi / rho.
    click_phi = [float(v) for v in unwrap([p for _, _, _, p in arrivals], run.modulus)]
    emitted = [float(t - age) for t, _, age, _ in arrivals]
    distances = links([age for _, _, age, _ in arrivals]).astype(float).tolist()
    k = run.rho * slope(click_phi, emitted) - 1.0
    v_record = slope(emitted, distances) / run.c
    first, last = int(min(emitted)), int(max(emitted))
    v_steps = (
        sum(1 for t in star.steps if first <= t <= last) / (last - first) / run.c
        if last > first
        else None
    )
    pushed = sum(push for t, push in star.pushes if first <= t <= last)
    span_steps = [t for t in star.steps if first <= t <= last]
    stall = max((b - a for a, b in zip(span_steps, span_steps[1:], strict=False)), default=None)
    burst = None
    if span_steps:
        burst, run_length = 1, 1
        for a, b in zip(span_steps, span_steps[1:], strict=False):
            run_length = run_length + 1 if b == a + 1 else 1
            burst = max(burst, run_length)
    return Point(
        name=star.name,
        lines=len(turns),
        z=z,
        k=k,
        v_record=v_record,
        tau=float(np.mean([age for _, _, age, _ in arrivals])),
        d=float(np.mean(distances)),
        rate=sum(a for _, a, _, _ in arrivals) / (hi - lo),
        declared=star.declared_speed / run.c,
        v_steps=v_steps,
        push_fraction=pushed / star.momentum if star.momentum else None,
        momentum_ratio=(
            star.final_momentum / star.momentum
            if star.final_momentum is not None and star.momentum
            else None
        ),
        stall=stall,
        burst=burst,
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


def fit_q(points: list[Point]) -> tuple[float, float, float]:
    """The power-law family with H and q free: the q of the least best-H
    rms on a grid, refined by a golden search between its neighbours;
    returns (q, H, rms)."""

    def best_at(q: float) -> tuple[float, float]:
        pole = math.inf if q <= -1.0 else 1.0 / (1.0 + q)
        return best_hubble(points, lambda x, q=q: power_law(x, q), min(pole, 4.0))

    grid = [(float(q), *best_at(float(q))) for q in Q_GRID]
    index = min(range(len(grid)), key=lambda i: grid[i][2])
    lo = grid[max(0, index - 1)][0]
    hi = grid[min(len(grid) - 1, index + 1)][0]
    golden = (math.sqrt(5.0) - 1.0) / 2.0
    a = hi - golden * (hi - lo)
    b = lo + golden * (hi - lo)
    fa, fb = best_at(a)[1], best_at(b)[1]
    for _ in range(40):
        if fa < fb:
            hi, b, fb = b, a, fa
            a = hi - golden * (hi - lo)
            fa = best_at(a)[1]
        else:
            lo, a, fa = a, b, fb
            b = lo + golden * (hi - lo)
            fb = best_at(b)[1]
    q = (lo + hi) / 2.0
    h, r = best_at(q)
    return q, h, r


def fit_points(points: list[Point], t0: float) -> Fit:
    """The fits of one window's points."""
    best = {label: best_hubble(points, form, pole) for label, _, form, pole in FORMS}
    q, h, r = fit_q(points)
    near = [p for p in points if p.z <= NEAR] or points
    hubble_near = sum(p.z * p.tau for p in near) / sum(p.tau * p.tau for p in near)
    taus = np.array([p.tau for p in points])
    zs = np.array([p.z for p in points])
    design = np.stack([taus, taus * taus], axis=1)
    coefficients, *_ = np.linalg.lstsq(design, zs, rcond=None)
    a, b = float(coefficients[0]), float(coefficients[1])
    q_effective = 2.0 * (b / (a * a) - 1.0) if a > 0 else None
    return Fit(
        t0=t0,
        best=best,
        q_fit=q,
        h_fit=h,
        rms_fit=r,
        hubble_near=hubble_near,
        q_effective=q_effective,
        points=sorted(points, key=lambda p: p.tau),
    )


def fit_window(run: Run, window: tuple[int, int]) -> Fit | None:
    points = [p for p in (window_point(run, s, window) for s in run.stars.values()) if p is not None]
    if len(points) < 3:
        return None
    return fit_points(points, (window[0] + window[1]) / 2.0)


def in_detector_clock(fit: Fit, rate: float, kind: str) -> Fit:
    """The same window's fit restated in the detector's own clock at the
    rate r (self-creations per interval): every point 1 + z_d = r (1 + z)
    and its luminosity L_d = L / r (clicks per the detector's own count),
    the forms 1 + z_d = r (1 + form(H tau)) so every best-H rms is r times
    the lattice's at the same H (the nearest and the farthest the same),
    the free fit's q unchanged and its H_d = r H (the slope of z_d in tau),
    the near fit's H_d = r H through the clock's own zero z_d(0) = r - 1,
    the free quadratic on z_d - z_d(0) = r z so q_eff,d = 2 ((q_eff / 2 +
    1) / r - 1); tau stays the row's own clock (its age at the click,
    record 707)."""
    points = [
        Point(
            p.name,
            p.lines,
            rate * (1.0 + p.z) - 1.0,
            p.k,
            p.v_record,
            p.tau,
            p.d,
            p.rate / rate,
            p.declared,
            p.v_steps,
            p.push_fraction,
            p.momentum_ratio,
            p.stall,
            p.burst,
            clock_rate=rate,
            z_lattice=p.z,
        )
        for p in fit.points
    ]
    q_effective = None if fit.q_effective is None else 2.0 * ((fit.q_effective / 2.0 + 1.0) / rate - 1.0)
    return Fit(
        t0=fit.t0,
        best={label: (h, rate * r) for label, (h, r) in fit.best.items()},
        q_fit=fit.q_fit,
        h_fit=rate * fit.h_fit,
        rms_fit=rate * fit.rms_fit,
        hubble_near=rate * fit.hubble_near,
        q_effective=q_effective,
        points=points,
        clock_rate=rate,
        clock_kind=kind,
    )


def doppler_part(fit: Fit) -> Fit:
    """The same fits on the Doppler part of the reading alone, z_D = v / c
    from the record's emission ticks and distances (the star's clock
    removed): printed beside the reading, not pinned."""
    points = [
        Point(p.name, p.lines, p.v_record, 0.0, p.v_record, p.tau, p.d, p.rate, p.declared)
        for p in fit.points
    ]
    return fit_points(points, fit.t0)


def exact_points(
    stars: list[tuple[str, float, float]], t0: float, c: float, throw_age: float
) -> list[Point]:
    """The exact coasting throw from one point at the window's centre: a
    star of speed v (Links per interval) thrown from the centre `throw_age`
    intervals before the run reads z = v / c at tau = (v / c)(t_0 +
    throw_age) / (1 + v / c), the Milne form with H = 1 / (t_0 +
    throw_age) exactly. `stars` is (name, v, r_0) per star; the design's
    points the criterion is validated on before the run."""
    found = []
    for name, v, _ in stars:
        z = v / c
        tau = z * (t0 + throw_age) / (1.0 + z)
        found.append(Point(name, 0, z, 0.0, z, tau, tau * c, 1.0 / (1.0 + z), z))
    return found


def find_runs(root: Path) -> list[Run]:
    found = []
    for path in sorted(root.rglob("run.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        model = str(record.get("model", ""))
        if model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX):
            found.append(read_run(path.parent))
    order = {"coasting": 0, "gravity": 1, "double": 2}
    clocks = {"none": 0, "scalar": 1, "age": 2}
    return sorted(
        found,
        key=lambda r: (r.under_record, order.get(r.crowd, 9), clocks.get(r.clock, 9)),
    )


def load_expectations(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    found: dict[str, object] = json.loads(path.read_text(encoding="utf-8"))
    return found


def fmt(value: float | None, digits: int = 4) -> str:
    return (
        "-"
        if value is None or (isinstance(value, float) and math.isnan(value))
        else f"{value:.{digits}f}"
    )


def inside(value: float, bracket: list[float] | tuple[float, float]) -> bool:
    return bracket[0] <= value <= bracket[1]


def verdict(ok: bool) -> str:
    return "inside" if ok else "outside"


def print_points(run: Run, window: tuple[int, int], fit: Fit) -> list[tuple[str, bool]]:
    """The points of one window in the detector's own clock (the pinned
    reading), the lattice's z beside each as [GAMEBOARD, the lattice's
    clock]; the formula and the luminosity criteria per star."""
    criteria: list[tuple[str, bool]] = []
    rate = fit.clock_rate
    print(
        f"{KIND_DETECTOR} `{run.name}`, the window [{window[0]}, {window[1]}), t_0 = {fit.t0:.0f}, in "
        f"the detector's own clock (its rate r = {rate:.4f} self-creations per interval: "
        f"{fit.clock_kind}): per star, 1 + z_d = r (1 + z), z from the pointer's turn per interval, "
        "tau the mean age of the arrivals (the row's own clock), d = m(tau), the luminosity the "
        "clicks per the detector's own count, L_d = L / r; k and v from the record's emission ticks "
        f"(tick - age) and distances; z and L {KIND_LATTICE}; the checks {KIND_BOARD}: v / c declared, "
        "v / c from the `step` lines, the push taken in the window over p(0) (outward positive), the "
        "momentum left at the end, |p(end)| / p(0), and the step rule's longest stall (intervals "
        "between two steps) and burst (steps on consecutive intervals) over the window's emission span"
    )
    print(
        "| star | v / c declared | lines | z_d read | z (lattice) | k (record) | v / c (record) | "
        "(1 + k)(1 + v / c) r - 1 | ratio (1 + z_d) | tau | d (Links) | L_d, clicks per own count | "
        "L, clicks per interval (lattice) | L_d x (1 + z_d) | v / c (steps) | push / p(0) | "
        "p(end) / p(0) | stall | burst |"
    )
    print(
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | "
        "--- | --- | --- |"
    )
    for p in fit.points:
        ratio = (1.0 + p.z) / (1.0 + p.predicted)
        formula_ok = abs(ratio - 1.0) <= FORMULA_TOLERANCE
        luminosity = p.rate * (1.0 + p.z)
        luminosity_ok = abs(luminosity - 1.0) <= LUMINOSITY_TOLERANCE
        tag = f"{run.name} [{window[0]}, {window[1]}) {p.name}"
        criteria.append((f"{tag}: the reading's formula (the detector's clock)", formula_ok))
        criteria.append((f"{tag}: the luminosity 1 / (1 + z) (the detector's clock)", luminosity_ok))
        print(
            f"| {p.name} | {p.declared:.4f} | {p.lines} | {p.z:+.4f} | {fmt(p.z_lattice)} | {p.k:.4f} | "
            f"{p.v_record:.4f} | {p.predicted:+.4f} | {ratio:.4f} {verdict(formula_ok)} | {p.tau:.1f} | "
            f"{p.d:.1f} | {p.rate:.4f} | {p.rate * rate:.4f} | {luminosity:.4f} {verdict(luminosity_ok)} | "
            f"{fmt(p.v_steps)} | {fmt(p.push_fraction, 5)} | {fmt(p.momentum_ratio)} | "
            f"{'-' if p.stall is None else p.stall} | {'-' if p.burst is None else p.burst} |"
        )
    missing = [s.name for s in run.stars.values() if all(p.name != s.name for p in fit.points)]
    if missing:
        print(f"(not read in this window, fewer than {MIN_LINES} lines: {', '.join(missing)})")
    stalls = [p.stall for p in fit.points if p.stall is not None]
    bursts = [p.burst for p in fit.points if p.burst is not None]
    if stalls and bursts:
        print(
            f"{KIND_BOARD} the step rule over the window's emission span: the longest stall {max(stalls)} "
            f"intervals, the longest burst {max(bursts)} Links on consecutive intervals; stars with a burst "
            f"of 3 or more: {sum(1 for b in bursts if b >= 3)} of {len(bursts)}"
        )
    print()
    return criteria


def print_fit(label: str, fit: Fit, throw_age: float | None) -> None:
    ht = f", H (t_0 + T_0) = {fit.h_fit * (fit.t0 + throw_age):.4f}" if throw_age is not None else ""
    clock = (
        f"in the detector's own clock (r = {fit.clock_rate:.4f}; H_d = r H, z_d(0) = r - 1 = "
        f"{fit.clock_rate - 1.0:+.4f})"
        if fit.clock_kind != KIND_LATTICE
        else "in the lattice's clock, as the register read it until 2026-09-22 (not counted)"
    )
    print(
        f"{label} {clock}: the power-law family with H and q free: q = {fit.q_fit:+.3f}, H = "
        f"{fit.h_fit:.5f} per interval{ht}, rms {fit.rms_fit:.4f} in z; the near fit through the "
        f"clock's own zero on z <= {NEAR} (the lattice's z): H = {fit.hubble_near:.5f}; the free "
        f"quadratic's q_eff = {fmt(fit.q_effective, 3)}"
    )
    print("| form | best H over every point | its H (t_0 + T_0) | its rms |")
    print("| --- | --- | --- | --- |")
    for form_label, _, _, _ in FORMS:
        h, r = fit.best[form_label]
        ht_form = f"{h * (fit.t0 + throw_age):.4f}" if throw_age is not None else "-"
        print(f"| {form_label} | {h:.5f} | {ht_form} | {r:.4f} |")
    print(
        f"the far part resembles {fit.nearest} (the least best-H rms) and least {fit.farthest}; what is "
        f"observed today (q = -0.55) is {'the nearest' if fit.nearest == 'q = -0.55' else 'not the nearest'}"
    )


def judge_fit(
    run: Run, window: tuple[int, int], fit: Fit, expected: dict[str, object]
) -> list[tuple[str, bool]]:
    """The pinned criteria of a window's fit against the expectations file
    (the brackets written before the runs)."""
    criteria: list[tuple[str, bool]] = []
    tag = f"{run.name} [{window[0]}, {window[1]})"
    crowd = (
        expected.get("crowds", {}).get(run.crowd) if isinstance(expected.get("crowds"), dict) else None
    )
    if not isinstance(crowd, dict):
        return criteria
    throw_age = float(expected["throw_age"])
    q_bracket = crowd.get("q_bracket")
    if isinstance(q_bracket, list):
        criteria.append(
            (
                f"{tag}: q of the free fit within {q_bracket[0]:+.2f} .. {q_bracket[1]:+.2f}",
                inside(fit.q_fit, q_bracket),
            )
        )
    hubble_bracket = crowd.get("hubble_bracket")
    if isinstance(hubble_bracket, list):
        ht = fit.h_fit * (fit.t0 + throw_age)
        criteria.append(
            (
                f"{tag}: H (t_0 + T_0) of the free fit within {hubble_bracket[0]:.2f} .. {hubble_bracket[1]:.2f}",
                inside(ht, hubble_bracket),
            )
        )
    nearest = crowd.get("nearest_forms")
    if isinstance(nearest, list):
        criteria.append(
            (
                f"{tag}: the nearest of the three forms one of {', '.join(nearest)}",
                fit.nearest in nearest,
            )
        )
    farthest = crowd.get("farthest_form")
    if isinstance(farthest, str):
        criteria.append((f"{tag}: the farthest of the three forms {farthest}", fit.farthest == farthest))
    # The expectation (README, "the criteria, pinned before the runs"): q =
    # -0.55 NOT the nearest of the three forms in any world; inside when it
    # is not (the label read the fact and not the pass until the second run
    # of 2026-09-20; the first registration's README counted it as here).
    criteria.append(
        (f"{tag}: what is observed today (q = -0.55) not the nearest", fit.nearest != "q = -0.55")
    )
    return criteria


def print_bends(runs: list[Run], window: tuple[int, int]) -> None:
    by_name = {r.name: r for r in runs}
    for prefix in ("", "record/"):
        for crowd in ("coasting", "gravity", "double"):
            scalar, age = by_name.get(f"{prefix}{crowd}_scalar"), by_name.get(f"{prefix}{crowd}_age")
            if scalar is None or age is None:
                continue
            fs, fa = scalar.fits.get(window), age.fits.get(window)
            if fs is None or fa is None:
                continue
            print(
                f"{KIND_DETECTOR} the bend of the age clock, `{prefix}{crowd}`, the window "
                f"[{window[0]}, {window[1]}): z_age - z_scalar per star (reported, no bracket); "
                f"q of the free fit {fs.q_fit:+.3f} (scalar) against {fa.q_fit:+.3f} (age)"
            )
            print("| star | tau (scalar) | z scalar | z age | z age - z scalar | k scalar | k age |")
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


def write_png(runs: list[Run], directory: Path, throw_age: float | None) -> None:
    """The diagrams with matplotlib, in the given directory (the repository
    gets the numbers, not the pictures)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    directory.mkdir(parents=True, exist_ok=True)
    columns = 3 if len(runs) > 4 else len(runs)
    rows = math.ceil(len(runs) / columns)
    for window in WINDOWS:
        figure, axes = plt.subplots(rows, columns, figsize=(4.2 * columns, 3.8 * rows), squeeze=False)
        for axis in axes.flat:
            axis.set_visible(False)
        for axis, run in zip(axes.flat, runs, strict=False):
            axis.set_visible(True)
            fit = run.fits.get(window)
            if fit is None:
                continue
            taus = np.linspace(0.0, max(p.tau for p in fit.points) * 1.05, 200)
            for (label, _, form, _), style in zip(FORMS, ("--", "-", ":"), strict=True):
                h, _ = fit.best[label]
                axis.plot(taus, [form(h * t) for t in taus], style, label=f"{label} (best H)")
            axis.plot(
                taus,
                [power_law(fit.h_fit * t, fit.q_fit) for t in taus],
                "-",
                color="black",
                linewidth=0.8,
                label=f"free fit q = {fit.q_fit:+.2f}",
            )
            axis.plot([p.tau for p in fit.points], [p.z for p in fit.points], "o", label="the detector")
            axis.set_title(f"{run.name}, t_0 = {fit.t0:.0f}, q = {fit.q_fit:+.2f}")
            axis.set_xlabel("light-travel time tau (intervals)")
            axis.set_ylabel("z")
            axis.set_ylim(0, 0.7)
            axis.legend(fontsize=7)
        figure.tight_layout()
        figure.savefig(directory / f"hubble_stars_{window[0]}_{window[1]}.png", dpi=110)
        plt.close(figure)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="the folder holding the run folders")
    parser.add_argument("--png", type=Path, help="write the diagrams with matplotlib into this folder")
    parser.add_argument(
        "--expectations",
        type=Path,
        default=EXPECTATIONS,
        help="the expectations written before the runs",
    )
    parser.add_argument(
        "--json", type=Path, help="write every reading and fit to this JSON file (for the page)"
    )
    args = parser.parse_args(argv)
    runs = find_runs(args.root)
    if not runs:
        print(f"no Hubble-stars run under {args.root}", file=sys.stderr)
        return 2
    expected = load_expectations(args.expectations)
    throw_age = float(expected["throw_age"]) if "throw_age" in expected else None
    failed = 0
    for run in runs:
        for label, ok in (("completed", run.completed), ("balanced", run.balanced)):
            print(
                f"{'PASS' if ok else 'FAIL'} {run.name}: {label} ({run.ticks} ticks, {run.elapsed:.1f} s)"
            )
            failed += not ok
        left = [f"{s.name} at {s.left}" for s in run.stars.values() if s.left is not None]
        homes = sum(s.homes for s in run.stars.values())
        print(
            f"{KIND_DETECTOR} {run.name}: c = {run.c:.5f} Links per interval (the flight rule), rho = "
            f"{run.rho:g} step per self-creation; the detector's own clock over the run {run.detector_rate:.4f} "
            f"self-creations per interval; stars that left the GameBoard: {', '.join(left) if left else 'none'}; "
            f"{KIND_BOARD} rows taken home over the run: {homes}; source fingerprint {run.fingerprint}"
        )
    print()
    criteria: list[tuple[str, bool]] = []
    for run in runs:
        rate, kind = run.own_clock()
        for window in WINDOWS:
            fit = fit_window(run, window)
            if fit is not None:
                run.lattice_fits[window] = fit
                run.fits[window] = in_detector_clock(fit, rate, kind)
    if throw_age is not None:
        stars_design = [
            (str(s["name"]), float(s["speed"]), float(s["initial_distance"])) for s in expected["stars"]
        ]
        c = beam_speed()
        for window in WINDOWS:
            t0 = (window[0] + window[1]) / 2.0
            exact = fit_points(exact_points(stars_design, t0, c, throw_age), t0)
            print_fit(
                f"{KIND_BOARD} the criterion validated on the exact coasting throw from one point at t_0 = "
                f"{t0:.0f} (the design's speeds, no grain; written before the runs)",
                exact,
                throw_age,
            )
            print()
    for window in WINDOWS:
        for run in runs:
            fit = run.fits.get(window)
            if fit is None:
                print(f"`{run.name}`: no reading in the window [{window[0]}, {window[1]})")
                continue
            if math.isnan(fit.rms_fit):
                # The register's statement (docs/EXPERIMENTS.md, series G2, the
                # re-run under the one click; tests/test_hubble_stars_readings.py
                # (b)): in a world whose stars birth records the `wave` set's
                # phase never turns, so the acoustic rule's z (the slope of the
                # record's phase) is undefined; the reading is the `source`
                # rule of the record worlds. An undefined reading is neither
                # inside nor outside: the criteria of this window are not
                # counted (2026-09-21, the Replicator, record 463 (iii)).
                print(
                    f"{KIND_DETECTOR} `{run.name}`, the window [{window[0]}, {window[1]}): NOT READABLE "
                    "under the acoustic rule: the stars birth records, the set's phase never turns and "
                    "the slope of the record's phase is undefined (the register's statement, "
                    "docs/EXPERIMENTS.md series G2, the re-run under the one click); the reading of "
                    "these worlds is the record worlds' `source` rule (examples/events/hubble_stars/record); "
                    "no criterion of this window is counted inside or outside"
                )
                continue
            lattice = run.lattice_fits[window]
            criteria += print_points(run, window, fit)
            print_fit(
                f"{KIND_DETECTOR} `{run.name}`, the window [{window[0]}, {window[1]})", fit, throw_age
            )
            if window == REGISTERED_WINDOW:
                criteria += judge_fit(run, window, fit, expected)
            print_fit(
                f"{KIND_LATTICE} `{run.name}`, the window [{window[0]}, {window[1]})", lattice, throw_age
            )
            doppler = doppler_part(lattice)
            print(
                f"{KIND_LATTICE} `{run.name}`: the Doppler part alone, z_D = v / c from the record's emission "
                f"ticks and distances (the star's clock removed; not pinned): q = {doppler.q_fit:+.3f}, "
                f"H (t_0 + T_0) = {fmt(doppler.h_fit * (fit.t0 + throw_age) if throw_age is not None else None)}, "
                f"the nearest form {doppler.nearest}"
            )
            if window == REGISTERED_WINDOW and isinstance(expected.get("crowds"), dict):
                crowd = expected["crowds"].get(run.crowd, {})
                momentum_bracket = (
                    crowd.get("momentum_ratio_bracket") if isinstance(crowd, dict) else None
                )
                ratios = [p.momentum_ratio for p in fit.points if p.momentum_ratio is not None]
                if isinstance(momentum_bracket, list) and ratios:
                    ok = all(inside(r, momentum_bracket) for r in ratios)
                    criteria.append(
                        (
                            f"{run.name}: |p(end)| / p(0) of every star within {momentum_bracket[0]:.3f} .. "
                            f"{momentum_bracket[1]:.3f} {KIND_BOARD}",
                            ok,
                        )
                    )
                    print(
                        f"{KIND_BOARD} `{run.name}`: |p(end)| / p(0) from {min(ratios):.4f} to {max(ratios):.4f} "
                        f"(expected {momentum_bracket[0]:.3f} .. {momentum_bracket[1]:.3f}): {verdict(ok)}"
                    )
                burst_max = expected.get("step_burst_max")
                bursts = [p.burst for p in fit.points if p.burst is not None]
                if isinstance(burst_max, int) and bursts:
                    # The step drive (2026-09-20): one Link per interval at
                    # most. The burst is counted on the `step` lines' ticks,
                    # the record's ordering, a `step` record the host's view
                    # of the body (ENGINE.md's table): a GameBoard diagnostic,
                    # printed with its expectation and out of the counted
                    # criteria (records 562 and 564; the clock audit of
                    # 2026-09-22, findings 5 and 10); the detector reading
                    # behind it, the stars' arrivals at the centre, is read above.
                    ok = max(bursts) <= burst_max
                    print(
                        f"{KIND_BOARD} (a diagnostic, not counted) `{run.name}`: the step rule's longest "
                        f"burst {max(bursts)} Link per interval (expected at most {burst_max}): "
                        f"{'agrees' if ok else 'differs'}"
                    )
                k_bracket = crowd.get("k_bracket") if isinstance(crowd, dict) else None
                if isinstance(k_bracket, list):
                    ks = [p.k for p in fit.points]
                    ok = all(inside(k, k_bracket) for k in ks)
                    criteria.append(
                        (
                            f"{run.name}: the stars' clocks k within {k_bracket[0]:.3f} .. {k_bracket[1]:.3f}",
                            ok,
                        )
                    )
                    print(
                        f"{KIND_DETECTOR} `{run.name}`: k from {min(ks):.4f} to {max(ks):.4f} (expected "
                        f"{k_bracket[0]:.3f} .. {k_bracket[1]:.3f}): {verdict(ok)}"
                    )
            print()
        print_bends(runs, window)
    ordering = expected.get("ordering")
    if isinstance(ordering, dict):
        for prefix, clock in [(p, c) for p in ("", "record/") for c in ("none", "scalar", "age")]:
            by_crowd = {
                run.crowd: run.fits[REGISTERED_WINDOW].q_fit
                for run in runs
                if run.clock == clock
                and run.prefix == prefix
                and REGISTERED_WINDOW in run.fits
                # an undefined reading (the acoustic rule on a record world,
                # rms nan) orders nothing
                and not math.isnan(run.fits[REGISTERED_WINDOW].rms_fit)
            }
            crowds = [c for c in ordering["crowds"] if c in by_crowd]
            if len(crowds) < 2:
                continue
            gaps = [by_crowd[b] - by_crowd[a] for a, b in zip(crowds, crowds[1:], strict=False)]
            ok = all(gap > float(ordering["minimum_gap"]) for gap in gaps)
            tag = f"{prefix}{clock} clocks"
            criteria.append(
                (
                    f"{tag}: q in the order {' < '.join(crowds)} with every gap above "
                    f"{float(ordering['minimum_gap']):.2f}",
                    ok,
                )
            )
            print(
                f"{KIND_DETECTOR} the {tag}, the window [{REGISTERED_WINDOW[0]}, {REGISTERED_WINDOW[1]}): "
                + ", ".join(f"q_{c} = {by_crowd[c]:+.3f}" for c in crowds)
                + f"; the gaps {', '.join(f'{g:+.3f}' for g in gaps)}: {verdict(ok)}"
            )
        print()
    if args.png is not None:
        write_png(runs, args.png, throw_age)
    if args.json is not None:
        payload = {
            "runs": [
                {
                    "name": run.name,
                    "crowd": run.crowd,
                    "clock": run.clock,
                    "under_record": run.under_record,
                    "completed": run.completed,
                    "balanced": run.balanced,
                    "elapsed": run.elapsed,
                    "fingerprint": run.fingerprint,
                    "homes": sum(s.homes for s in run.stars.values()),
                    "clock_rate": run.detector_rate,
                    "windows": {
                        f"{lo}-{hi}": {
                            "t0": fit.t0,
                            "clock": "the detector's own clock, 1 + z_d = r (1 + z)",
                            "clock_rate": fit.clock_rate,
                            "q_fit": fit.q_fit,
                            "h_fit": fit.h_fit,
                            "rms_fit": fit.rms_fit,
                            "hubble_near": fit.hubble_near,
                            "q_effective": fit.q_effective,
                            "best": fit.best,
                            "doppler_q": doppler_part(run.lattice_fits[(lo, hi)]).q_fit,
                            "points": [asdict(p) for p in fit.points],
                            "lattice": {
                                "kind": "GAMEBOARD, the lattice's clock",
                                "q_fit": run.lattice_fits[(lo, hi)].q_fit,
                                "h_fit": run.lattice_fits[(lo, hi)].h_fit,
                                "rms_fit": run.lattice_fits[(lo, hi)].rms_fit,
                                "hubble_near": run.lattice_fits[(lo, hi)].hubble_near,
                                "q_effective": run.lattice_fits[(lo, hi)].q_effective,
                                "best": run.lattice_fits[(lo, hi)].best,
                            },
                        }
                        for (lo, hi), fit in run.fits.items()
                    },
                }
                for run in runs
            ],
            "criteria": [{"label": label, "inside": ok} for label, ok in criteria],
        }
        args.json.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    inside_count = 0
    for label, ok in criteria:
        if "formula" not in label and "luminosity" not in label:
            print(f"{verdict(ok)}: {label}")
        inside_count += ok
    formula = [ok for label, ok in criteria if "formula" in label]
    luminosity = [ok for label, ok in criteria if "luminosity" in label]
    print(
        f"the reading's formula: {sum(formula)} of {len(formula)} inside {FORMULA_TOLERANCE:.0%}; the "
        f"luminosity 1 / (1 + z): {sum(luminosity)} of {len(luminosity)} inside {LUMINOSITY_TOLERANCE:.0%}; "
        f"{failed} record check(s) failed; {inside_count} reading(s) inside, {len(criteria) - inside_count} outside "
        "(every criterion in the detector's own clock; the lattice's clock and the step rule's burst "
        "printed, not counted)"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
