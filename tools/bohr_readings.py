"""The readings of series H, "Bohr's lines behind the detector": an
electron that is a body on a set of three Nodes, turning its phase by its
momentum at every Link it steps, about a fixed proton in space, and the
far faces of the board as the `wave` detectors that receive what it
releases (docs/EXPERIMENTS.md, "H, Bohr's lines behind the detector";
examples/events/bohr/make_worlds.py; the model owner's decision of
2026-09-20, "On Bohr, go, and put it as parameters outside the board like
the age").

Reads the run folders of the worlds (the runner's `run.json`,
`initialization.json` and `events.jsonl`, told apart by the `model` of the
record, `rays-bohr-r<r>-space-v1`) and prints, per world, two kinds of
number, each line labelled (the model owner, 2026-09-20: "in reality there
is no such thing" about the host's readings of the board):

- GAMEBOARD readings, the host's view of the mechanism, which exist for us
  and not in reality: the electron's orbit read from its `step` records
  (the turns, the period T of each, the return to the start, the mean
  radius, the least and greatest radius, the end), the body's phase at
  each closing of the angle and the turn of the phase per orbit against
  the design's 4 p r / h, and the design's own numbers (p, the derived j).
- DETECTOR readings, the only kind reality has: the coherent record of
  the electron's rays at the four side faces of the board (the face
  detectors, `wave`: every `click` line on a face carries the ray's phase
  and amount), taken per turn and cumulatively over the turns through the
  engine's own `coherent_pointer` (the same tables, the same sum): the
  pointer of the clicks released in turn t, x_t; the cumulative pointer
  after T turns, X_T = sum of x_t, its square R_T = |X_T|^2 the cumulative
  coherent record; and the coherence ratio C(T) = R_T / sum |x_t|^2, which
  is T when the phase closes on itself every turn (the same phase at the
  same place, the pointers adding in line) and stays about 1 or below when
  it does not (the pointers turning against each other). The faces' own
  cumulative `record` of `run.json` (the per-interval squares summed, a
  count of what arrived, never coherent across intervals) is printed
  beside it; and the electron's own `read` records (the pushes it took,
  the arrivals it read) are its detector readings.

A click is assigned to the turn in which its ray was released: the click's
tick less the flight time of its heading from the centre's plane to the
face, the least age at which the flight table's Manhattan steps reach the
face (`FlightTable.manhattan_steps`, the engine's own), which is exact for
a release at the centre and within about r x sqrt 3 intervals of it
elsewhere on the orbit (a few intervals against a period of hundreds).

The expectation, written before the runs (README.md): at a radius where the
design's j = 4 p r / h is whole the coherent record grows as the square of
the turns, C(T) at least T / 2 after T turns and the log-log slope of R_T
against T near 2; between two whole j it stays bounded, C(T) below 2 and
the slope at most about 1; the closing radii in the ratio of j^2. The
record checks (completed, the books balanced at every tick) fail the tool;
the readings are registered inside or outside their expectation and never
moved; an orbit that does not close (no full turn, or a return farther
than a quarter of the radius) is registered as the finding.

    PYTHONPATH=src python tools/bohr_readings.py artifacts/bohr
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events.nature_beam import coherent_pointer, flight_table
from event_universe.events.world import FACE_NAMES

MODEL_PREFIX = "rays-bohr-"
MODEL_SUFFIX = "-space-v1"
ELECTRON = 2
FULL_TURN = 2 * math.pi
# The face of each in-plane heading the electron releases on (Port order).
HEADING_FACES = {(1, 0, 0): 0, (-1, 0, 0): 1, (0, 1, 0): 2, (0, -1, 0): 3}
# The coherence ratio a closing radius must reach after T turns (half the
# ideal T) and the bound a non-closing one must stay under.
CLOSING_SHARE = 0.5
BOUNDED_RATIO = 2.0
# A closed orbit returns within this fraction of the radius of its start.
RETURN_SHARE = 0.25
Vector = tuple[int, int, int]
Kind = str
GAMEBOARD: Kind = "GAMEBOARD"
DETECTOR: Kind = "DETECTOR"


@dataclass
class Turn:
    """One closing of the angle about the proton (GAMEBOARD)."""

    index: int
    tick: int
    intervals: int
    return_distance: float
    mean_radius: float
    phase: int
    reads: int = 0


@dataclass
class Reading:
    name: str
    radius: int
    momentum: Vector
    action: int
    phase_steps: int
    shell: int
    width: int
    ticks: int
    completed: bool
    balanced: bool
    elapsed: float
    derived_j: float
    turns: list[Turn] = field(default_factory=list)
    angle_turns: float = 0.0
    least_radius: float = 0.0
    greatest_radius: float = 0.0
    z_excursion: int = 0
    ended: str = ""
    reads: int = 0
    inward_push: float = 0.0
    # Per face: the clicks of the electron's family as (turn, amount, phase).
    clicks: dict[int, list[tuple[int, int, int]]] = field(default_factory=dict)
    face_records: dict[str, int] = field(default_factory=dict)
    proton_face_records: dict[str, int] = field(default_factory=dict)
    delays: dict[int, int] = field(default_factory=dict)

    @property
    def closed_turns(self) -> int:
        return sum(1 for turn in self.turns if turn.return_distance <= RETURN_SHARE * self.radius)


def flight_delay(heading: Vector, links: int) -> int:
    """The least age at which a ray on `heading` has made `links` Manhattan
    steps: the engine's flight table (`manhattan_steps`)."""
    table = flight_table((heading,))
    age = 0
    while int(table.manhattan_steps(np.array([0]), np.array([age]))[0]) < links:
        age += 1
    return age


def read_run(folder: Path) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    model = str(record["model"])
    radius = int(model[len(MODEL_PREFIX) + 1 : -len(MODEL_SUFFIX)])
    world = json.loads((folder / "initialization.json").read_text(encoding="utf-8"))
    proton, electron = world["measured"]
    centre = tuple(int(v) for v in proton["position"])
    side = int(world["shape"][0])
    momentum = tuple(int(v) for v in electron["momentum"])
    action = int(world["action"])
    reading = Reading(
        name=model[len(MODEL_PREFIX) : -len(MODEL_SUFFIX)],
        radius=radius,
        momentum=(momentum[0], momentum[1], momentum[2]),
        action=action,
        phase_steps=int(world["N"]),
        shell=int(world["release"][1]) // int(proton["amount"]),
        width=int(world.get("width", 1)),
        ticks=int(record["completed_ticks"]),
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        elapsed=float(record["elapsed_seconds"]),
        derived_j=4 * max(abs(v) for v in momentum) * radius / action,
    )
    families = {f["name"]: f for f in world["families"]}
    electron_family = str(electron["family"])
    proton_family = str(proton["family"])
    for detector in record["detectors"]:
        if str(detector["name"]).startswith("face:"):
            reading.face_records[str(detector["name"])] = int(
                detector["families"][electron_family]["record"]
            )
            reading.proton_face_records[str(detector["name"])] = int(
                detector["families"][proton_family]["record"]
            )
    # The flight time from the centre's plane to each face the electron's
    # headings reach: the face's coordinate less the centre's, in Links.
    for heading, face in HEADING_FACES.items():
        axis = face >> 1
        links = (side - 1 - centre[axis]) if face % 2 == 0 else centre[axis]
        reading.delays[face] = flight_delay(heading, links)
    steps: dict[int, tuple[Vector, list[int], int]] = {}
    clicks: list[tuple[int, int, int, int]] = []  # (face, tick, amount, phase)
    pushes: list[tuple[int, list[int]]] = []
    electron_family_key = f'"family": "{electron_family}"'
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if '"step"' not in line and electron_family_key not in line and '"read"' not in line:
                continue
            event = json.loads(line)
            kind = event["event"]
            if kind == "step" and event["number"] == ELECTRON:
                to = event["to"]
                steps[int(event["tick"])] = (
                    (int(to[0]), int(to[1]), int(to[2])),
                    [int(v) for v in event["momentum"]],
                    int(event["phase"]),
                )
            elif kind == "click" and event["family"] == electron_family and event["measured"] is None:
                face = FACE_NAMES.index(str(event["detector"]))
                clicks.append((face, int(event["tick"]), int(event["amount"]), int(event["phase"])))
            elif kind == "click" and event.get("measured") == ELECTRON:
                reading.ended = f"escaped through {event['detector']} at tick {event['tick']}"
            elif kind == "read" and event["measured"] == ELECTRON:
                pushes.append((int(event["tick"]), [int(v) for v in event["push"]]))
    assert families  # the world's families were read
    # The orbit from the steps (GAMEBOARD).
    start: Vector = tuple(int(v) for v in electron["position"])  # type: ignore[assignment]
    position, phase = start, int(electron.get("phase", 0))
    positions: list[Vector] = [start]
    phases: list[int] = [phase]
    for tick in range(1, reading.ticks + 1):
        if tick in steps:
            position, _, phase = steps[tick]
        positions.append(position)
        phases.append(phase)
    radii = [math.dist(p, centre) for p in positions]
    reading.least_radius, reading.greatest_radius = min(radii), max(radii)
    reading.z_excursion = max(abs(p[2] - centre[2]) for p in positions)
    unwrapped = 0.0
    previous = math.atan2(start[1] - centre[1], start[0] - centre[0])
    angles = []
    for x, y, _ in positions:
        angle = math.atan2(y - centre[1], x - centre[0])
        delta = angle - previous
        if delta > math.pi:
            delta -= FULL_TURN
        elif delta < -math.pi:
            delta += FULL_TURN
        unwrapped += delta
        angles.append(unwrapped)
        previous = angle
    reading.angle_turns = angles[-1] / FULL_TURN
    last_close, index = 0, 0
    for tick in range(1, reading.ticks + 1):
        if angles[tick] >= FULL_TURN * (index + 1):
            index += 1
            window = radii[last_close : tick + 1]
            reading.turns.append(
                Turn(
                    index,
                    tick,
                    tick - last_close,
                    math.dist(positions[tick], start),
                    sum(window) / len(window),
                    phases[tick],
                )
            )
            last_close = tick
    if not reading.ended and reading.least_radius <= 1.0:
        reading.ended = "reached the Node beside the proton"
    closings = [turn.tick for turn in reading.turns]

    def turn_of(tick: int) -> int:
        """The turn (from 1) a tick falls in; the unfinished turn after the
        last closing counts as the next index."""
        for k, closing in enumerate(closings):
            if tick <= closing:
                return k + 1
        return len(closings) + 1

    for tick, push in pushes:
        x, y, z = positions[tick - 1]
        dx, dy, dz = centre[0] - x, centre[1] - y, centre[2] - z
        norm = math.sqrt(dx * dx + dy * dy + dz * dz)
        inward = 0.0 if not norm else (push[0] * dx + push[1] * dy + push[2] * dz) / norm
        reading.inward_push += inward
        reading.reads += 1
        turn = turn_of(tick)
        if turn <= len(reading.turns):
            reading.turns[turn - 1].reads += 1
    for face, tick, amount, click_phase in clicks:
        released = max(1, tick - reading.delays[face])
        reading.clicks.setdefault(face, []).append((turn_of(released), amount, click_phase))
    return reading


def pointer_by_turn(
    clicks: list[tuple[int, int, int]], turns: int, modulus: int
) -> list[tuple[int, int]]:
    """The coherent pointer of the clicks of each turn 1 .. `turns` through
    the engine's `coherent_pointer` (the 1/256 tables of the circle of
    `modulus`); (0, 0) for a turn without clicks."""
    cosines = np.array(phase_cosines(modulus), dtype=np.int64)
    sines = np.array(phase_sines(modulus), dtype=np.int64)
    found: list[tuple[int, int]] = []
    for turn in range(1, turns + 1):
        rows = [(amount, phase) for t, amount, phase in clicks if t == turn]
        if not rows:
            found.append((0, 0))
            continue
        amount = np.array([a for a, _ in rows], dtype=np.int64)
        phase = np.array([p for _, p in rows], dtype=np.int64)
        x, y = coherent_pointer(
            amount, phase, np.zeros(1, dtype=np.int64), [int(amount.sum())], cosines, sines
        )
        found.append((int(x[0]), int(y[0])))
    return found


def coherence(pointers: list[tuple[int, int]]) -> tuple[list[int], float]:
    """The cumulative coherent record R_T = |sum of the pointers|^2 after
    each turn, and the coherence ratio C = R_T / sum |x_t|^2 after the
    last turn (0 without clicks)."""
    cumulative: list[int] = []
    x = y = 0
    for px, py in pointers:
        x += px
        y += py
        cumulative.append(x * x + y * y)
    incoherent = sum(px * px + py * py for px, py in pointers)
    ratio = 0.0 if not incoherent else cumulative[-1] / incoherent
    return cumulative, ratio


def slope(values: list[int]) -> float | None:
    """The least-squares slope of log R_T against log T over the turns with
    a nonzero record (None below two points)."""
    points = [(math.log(t + 1), math.log(v)) for t, v in enumerate(values) if v > 0]
    if len(points) < 2:
        return None
    mean_x = sum(x for x, _ in points) / len(points)
    mean_y = sum(y for _, y in points) / len(points)
    var = sum((x - mean_x) ** 2 for x, _ in points)
    if not var:
        return None
    return sum((x - mean_x) * (y - mean_y) for x, y in points) / var


def find_runs(root: Path) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        model = str(record.get("model", ""))
        if model.startswith(MODEL_PREFIX) and model.endswith(MODEL_SUFFIX):
            found.append(read_run(path.parent))
    return sorted(found, key=lambda r: r.radius)


def expected_closing(j: float) -> bool:
    return abs(j - round(j)) < 0.1


def print_world(reading: Reading) -> list[tuple[str, bool]]:
    """The readings of one world, each line labelled by its kind; returns
    the criteria (label, inside)."""
    criteria: list[tuple[str, bool]] = []
    r = reading
    closing = expected_closing(r.derived_j)
    print(
        f"[{GAMEBOARD}] world `{r.name}`: r = {r.radius}, p = {max(abs(v) for v in r.momentum)} (label units), "
        f"h = {r.action}, N = {r.phase_steps}, width {r.width}; the design's j = 4 p r / h = {r.derived_j:.3f} "
        f"({'closing' if closing else 'between'}); {r.ticks} intervals in {r.elapsed:.1f} s"
    )
    completed = len(r.turns)
    print(
        f"[{GAMEBOARD}] the orbit: {r.angle_turns:.2f} turns of the angle, {completed} closings, "
        f"{r.closed_turns} of them returning within {RETURN_SHARE:.2f} r of the start; r from "
        f"{r.least_radius:.1f} to {r.greatest_radius:.1f}, z excursion {r.z_excursion}; "
        f"{r.ended or 'on the board at the end'}"
    )
    for turn in r.turns:
        print(
            f"[{GAMEBOARD}]   turn {turn.index}: T = {turn.intervals} intervals (closing at tick {turn.tick}), "
            f"return {turn.return_distance:.1f} Links, mean radius {turn.mean_radius:.2f}, "
            f"the body's phase {turn.phase} of {r.phase_steps}, {turn.reads} reads"
        )
    if len(r.turns) >= 2:
        drifts = [
            ((r.turns[k].phase - r.turns[k - 1].phase) % r.phase_steps) / r.phase_steps
            for k in range(1, len(r.turns))
        ]
        expected_fraction = r.derived_j - math.floor(r.derived_j)
        print(
            f"[{GAMEBOARD}] the phase's turn per orbit, the fraction of a circle beyond whole circles: "
            f"measured {', '.join(f'{d:.3f}' for d in drifts)} against the design's {expected_fraction:.3f} "
            f"(0 or 1 at a closing radius)"
        )
    if r.reads:
        print(
            f"[{DETECTOR}] the electron's own reads: {r.reads} `read` records, the mean inward push per "
            f"interval {r.inward_push / r.ticks / 64:.2f} (in units of Q = 64 per unit of content)"
        )
    turns = max(1, completed)
    pooled: list[tuple[int, int]] = [(0, 0)] * turns
    for face in sorted(r.clicks):
        pointers = pointer_by_turn(r.clicks[face], turns, r.phase_steps)
        pooled = [(a + c, b + d) for (a, b), (c, d) in zip(pooled, pointers, strict=True)]
        cumulative, ratio = coherence(pointers)
        clicks = sum(1 for t, _, _ in r.clicks[face] if t <= turns)
        print(
            f"[{DETECTOR}]   {FACE_NAMES[face]}: {clicks} clicks of the electron's rays over {turns} turns "
            f"(the flight {r.delays[face]} intervals), the pointer per turn "
            f"{' '.join(f'({x}, {y})' for x, y in pointers)}, the cumulative coherent record "
            f"{cumulative[-1]}, C = {ratio:.2f}, the face's own record {r.face_records.get(FACE_NAMES[face], 0)}"
        )
    cumulative, ratio = coherence(pooled)
    growth = slope(cumulative)
    print(
        f"[{DETECTOR}] the four faces pooled: the cumulative coherent record after each turn "
        f"{cumulative}, C({turns}) = {ratio:.2f}, the log-log slope of R_T against T "
        f"{'-' if growth is None else f'{growth:.2f}'}"
    )
    if completed >= 2:
        if closing:
            inside = ratio >= CLOSING_SHARE * turns
            verdict = f"C >= {CLOSING_SHARE * turns:.1f} (T / 2 after {turns} turns): {'inside' if inside else 'outside'}"
        else:
            inside = ratio < BOUNDED_RATIO
            verdict = f"C < {BOUNDED_RATIO:.0f} (bounded): {'inside' if inside else 'outside'}"
        print(f"[{DETECTOR}] expected at a {'closing' if closing else 'between'} radius: {verdict}")
        criteria.append((f"r = {r.radius} ({'closing' if closing else 'between'}): {verdict}", inside))
    else:
        print(
            f"[{GAMEBOARD}] fewer than two turns closed: no coherence reading is taken at r = {r.radius} "
            "(the finding is the orbit)"
        )
    print()
    return criteria


def print_ladder(readings: list[Reading]) -> None:
    closing = [r for r in readings if expected_closing(r.derived_j) and len(r.turns) >= 2]
    if len(closing) < 2:
        print(
            f"[{GAMEBOARD}] the ladder: fewer than two closing radii with two turns; no ratio is taken"
        )
        return
    print(f"[{GAMEBOARD}] the ladder of the closing radii (expected in the ratio of j^2):")
    first = closing[0]
    for r in closing[1:]:
        j1, j2 = round(first.derived_j), round(r.derived_j)
        print(
            f"[{GAMEBOARD}]   r = {r.radius} / r = {first.radius} = {r.radius / first.radius:.2f} against "
            f"(j = {j2} / j = {j1})^2 = {(j2 / j1) ** 2:.2f}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="the folder holding the run folders")
    args = parser.parse_args(argv)
    readings = find_runs(args.root)
    if not readings:
        print(f"no bohr run under {args.root}", file=sys.stderr)
        return 2
    failed = 0
    for r in readings:
        for label, ok in (("completed", r.completed), ("balanced", r.balanced)):
            print(f"{'PASS' if ok else 'FAIL'} {r.name}: {label} ({r.elapsed:.1f} s, {r.ticks} ticks)")
            failed += not ok
    print()
    print(
        f"every line below is labelled [{GAMEBOARD}] (the host's view of the board: the orbit, the "
        f"design; exists for us, not in reality) or [{DETECTOR}] (a detector's record or a measured "
        "event's own: the only kind reality has)"
    )
    print()
    criteria: list[tuple[str, bool]] = []
    for r in readings:
        criteria += print_world(r)
    print_ladder(readings)
    inside = sum(1 for _, ok in criteria if ok)
    print()
    print(
        f"{failed} record check(s) failed; {inside} reading(s) inside, {len(criteria) - inside} outside"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
