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
Manhattan steps of the flight table read through the engine's own
`flight_table`, whose period also gives c), and the luminosity, the click
rate of the star's light per detector interval (expected 1 / (1 + z) of
the lamp's rate: a beam does not dilute, so the click rate carries no
distance beyond the redshift; README.md there).

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
from event_universe.events.nature_beam import flight_table
from event_universe.events.world import HEADING_OFFSET, Q

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
# The flight table of the six headings (the two rest vectors first): m(age)
# and c are the same on every heading.
HEADINGS_TABLE = flight_table(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))


def beam_speed() -> float:
    """c, the Links a ray makes on a heading in one period over the period
    (32 / 55 = 0.58182 per interval), off the flight table."""
    heading = np.array([HEADING_OFFSET])
    period = int(HEADINGS_TABLE.period[HEADING_OFFSET])
    return int(HEADINGS_TABLE.manhattan_steps(heading, np.array([period]))[0]) / period


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

    @property
    def predicted(self) -> float:
        """The reading's formula from the record's own k and v: (1 + k)(1 + v / c) - 1."""
        return (1.0 + self.k) * (1.0 + self.v_record) - 1.0


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
    under_doppler: bool
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
    fits: dict[tuple[int, int], Fit] = field(default_factory=dict)

    @property
    def prefix(self) -> str:
        """The folder of the world: `doppler/` under the key `doppler` (with
        `amplitude`), `record/` under `amplitude` alone, none otherwise."""
        return "doppler/" if self.under_doppler else "record/" if self.under_record else ""

    @property
    def name(self) -> str:
        return f"{self.prefix}{self.crowd}_{self.clock}"


def axis_of(momentum: list[int]) -> tuple[int, int]:
    """The axis and the outward sign of a momentum along one axis."""
    axis = next(k for k in range(3) if momentum[k])
    return axis, 1 if momentum[axis] > 0 else -1


def read_run(folder: Path) -> Run:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    document = json.loads((folder / "initialization.json").read_text(encoding="utf-8"))
    model = str(record["model"])
    parts = model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)].split("-")
    # Under the record click (the world key `amplitude`, the model id
    # `rays-hubble-stars-record-<crowd>-<clock>-space-v1`) the `record`
    # lines are per record and the reading comes from the gather lines.
    under_record = parts[0] == "record"
    # Under the key `doppler` as well (doppler-v1, the model id
    # `rays-hubble-stars-record-doppler-<crowd>-<clock>-space-v1`) the
    # reading is the same; the stars' pushes are weighted on the GameBoard.
    under_doppler = "doppler" in parts[:-2]
    crowd, clock = parts[-2], parts[-1]
    table = flight_table(tuple(tuple(v) for v in record["directions"]))
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
        under_doppler=under_doppler,
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
    return HEADINGS_TABLE.manhattan_steps(direction, whole)


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
        key=lambda r: (r.under_record, r.under_doppler, order.get(r.crowd, 9), clocks.get(r.clock, 9)),
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
    criteria: list[tuple[str, bool]] = []
    print(
        f"{KIND_DETECTOR} `{run.name}`, the window [{window[0]}, {window[1]}), t_0 = {fit.t0:.0f}: per "
        "star, 1 + z from the pointer's turn, tau the mean age of the arrivals, d = m(tau), the "
        "luminosity the click rate per interval; k and v from the record's emission ticks (tick - "
        f"age) and distances; the checks {KIND_BOARD}: v / c declared, v / c from the `step` lines, "
        "the push taken in the window over p(0) (outward positive), the momentum left at the "
        "end, |p(end)| / p(0), and the step rule's longest stall (intervals between two steps) and "
        "burst (steps on consecutive intervals) over the window's emission span"
    )
    print(
        "| star | v / c declared | lines | z read | k (record) | v / c (record) | (1 + k)(1 + v / c) - 1 "
        "| ratio (1 + z) | tau | d (Links) | clicks per interval | rate x (1 + z) | v / c (steps) | "
        "push / p(0) | p(end) / p(0) | stall | burst |"
    )
    print(
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    )
    for p in fit.points:
        ratio = (1.0 + p.z) / (1.0 + p.predicted)
        formula_ok = abs(ratio - 1.0) <= FORMULA_TOLERANCE
        luminosity = p.rate * (1.0 + p.z)
        luminosity_ok = abs(luminosity - 1.0) <= LUMINOSITY_TOLERANCE
        tag = f"{run.name} [{window[0]}, {window[1]}) {p.name}"
        criteria.append((f"{tag}: the reading's formula", formula_ok))
        criteria.append((f"{tag}: the luminosity 1 / (1 + z)", luminosity_ok))
        print(
            f"| {p.name} | {p.declared:.4f} | {p.lines} | {p.z:.4f} | {p.k:.4f} | {p.v_record:.4f} | "
            f"{p.predicted:.4f} | {ratio:.4f} {verdict(formula_ok)} | {p.tau:.1f} | {p.d:.1f} | "
            f"{p.rate:.4f} | {luminosity:.4f} {verdict(luminosity_ok)} | {fmt(p.v_steps)} | "
            f"{fmt(p.push_fraction, 5)} | {fmt(p.momentum_ratio)} | {'-' if p.stall is None else p.stall} | "
            f"{'-' if p.burst is None else p.burst} |"
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
    print(
        f"{label}: the power-law family with H and q free: q = {fit.q_fit:+.3f}, H = {fit.h_fit:.5f} "
        f"per interval{ht}, rms {fit.rms_fit:.4f} in z; the near fit through the origin on z <= {NEAR}: "
        f"H = {fit.hubble_near:.5f}; the free quadratic's q_eff = {fmt(fit.q_effective, 3)}"
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
    for prefix in ("", "record/", "doppler/"):
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
            f"{KIND_DETECTOR} {run.name}: c = {run.c:.5f} Links per interval (the flight table), rho = "
            f"{run.rho:g} step per self-creation; the detector's own clock over the run {run.detector_rate:.4f} "
            f"self-creations per interval; stars that left the GameBoard: {', '.join(left) if left else 'none'}; "
            f"{KIND_BOARD} rows taken home over the run: {homes}; source fingerprint {run.fingerprint}"
        )
    print()
    criteria: list[tuple[str, bool]] = []
    for run in runs:
        for window in WINDOWS:
            fit = fit_window(run, window)
            if fit is not None:
                run.fits[window] = fit
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
            criteria += print_points(run, window, fit)
            print_fit(
                f"{KIND_DETECTOR} `{run.name}`, the window [{window[0]}, {window[1]})", fit, throw_age
            )
            if window == REGISTERED_WINDOW:
                criteria += judge_fit(run, window, fit, expected)
            doppler = doppler_part(fit)
            print(
                f"{KIND_DETECTOR} `{run.name}`: the Doppler part alone, z_D = v / c from the record's emission "
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
                    # The step drive (2026-09-20): one Link per interval at most.
                    ok = max(bursts) <= burst_max
                    criteria.append(
                        (
                            f"{run.name}: the step rule's longest burst at most {burst_max} Link per "
                            f"interval {KIND_BOARD}",
                            ok,
                        )
                    )
                    print(
                        f"{KIND_BOARD} `{run.name}`: the longest burst {max(bursts)} (expected at most "
                        f"{burst_max}): {verdict(ok)}"
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
        for prefix, clock in [
            (p, c) for p in ("", "record/", "doppler/") for c in ("none", "scalar", "age")
        ]:
            by_crowd = {
                run.crowd: run.fits[REGISTERED_WINDOW].q_fit
                for run in runs
                if run.clock == clock and run.prefix == prefix and REGISTERED_WINDOW in run.fits
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
                    "under_doppler": run.under_doppler,
                    "completed": run.completed,
                    "balanced": run.balanced,
                    "elapsed": run.elapsed,
                    "fingerprint": run.fingerprint,
                    "homes": sum(s.homes for s in run.stars.values()),
                    "windows": {
                        f"{lo}-{hi}": {
                            "t0": fit.t0,
                            "q_fit": fit.q_fit,
                            "h_fit": fit.h_fit,
                            "rms_fit": fit.rms_fit,
                            "hubble_near": fit.hubble_near,
                            "q_effective": fit.q_effective,
                            "best": fit.best,
                            "doppler_q": doppler_part(fit).q_fit,
                            "points": [asdict(p) for p in fit.points],
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
        f"{failed} record check(s) failed; {inside_count} reading(s) inside, {len(criteria) - inside_count} outside"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
