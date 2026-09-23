"""The readings of Side A of Newton on the side (docs/designs/newton_clicks/
NEWTON_ON_THE_SIDE.md sections 3 and 4; the chain of steps and the pins
restated in docs/designs/fail_rows/RUN_14.md; the worlds
examples/events/newton_side/): a massive row released at rest by a lamp
A, walking one Link per 19 counts past a held mass, read at a receiver
BODY on the plane x = 54 under the world key `clock_stamp`; the control
without the mass; and the light row of the same world for the lever-arm
pin.

Outside arithmetic on the click lines alone (the model owner, records
768 and 1046: Newton from the algebra of the clicks and not of the
GameBoard). A click is the line a receiver body writes when a row of the
lamp's family ends at its Node: the receiver's number and Node, the row's
ordinal (`record` mod 2^32, the lamp's count at the release) and the
receiver's own count `clock` at the arrival (the entry's reading, the
presence, beside them). From these and nothing else, per world:

- DETECTOR: the arrival count per click, `clock` less the ordinal (n_B at
  the click less the row's ordinal), its mean, least, greatest and
  spread over the window; the pace over the window, the Links from the
  lamp to the plane over that count (the one band rule, 2 / W); the
  centroid of the arrival Nodes in y and z, and its shift against the
  control's centroid in pixels toward the mass; the count ratio of
  consecutive clicks at the one receiver that clicked most (the
  receiver's counts apart over the rows' ordinals apart); the clicks of
  the lamp's family on the faces (a row that left the board); and the
  line of the arrival counts against the ordinals over the window (its
  intercept the flight's count where both clocks were 0, its slope the
  receiver's rate less the lamp's: Einstein's step in the middle, the
  count ratio in a crowd, separated from the flight's count).
- COMPUTATION: the control's arrival count derived from the world's own
  integers before it is read (the massive triple's first age at L Links;
  the flight table's for the light row), the difference of the mass
  world's count from the control's and their ratio, the pins of
  `expectations.json` beside the worlds and each verdict against them.
- GAMEBOARD, printed beside and never pinned: the tick of the first
  click and the receiver's count behind the tick (what it owes the
  crowd).

    PYTHONPATH=src python tools/newton_side_readings.py artifacts/newton_side
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

import numpy as np

from event_universe.events import parse_nature_beam_world
from event_universe.events.nature_beam import direction_flight
from event_universe.events.world import HEADING_OFFSET
from event_universe.trimmed_record import refuse_trimmed_record
from event_universe.world_loading import world_of_run

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "examples" / "events" / "newton_side" / "expectations.json"
MODEL_PATTERN = re.compile(r"^beam-newton-side-(?P<name>[a-z0-9_]+)-v1$")
ORDINAL_MASK = (1 << 32) - 1
LABEL_SCALE = 64
DETECTOR = "DETECTOR"
COMPUTATION = "COMPUTATION"
GAMEBOARD = "GAMEBOARD"
HOST = "HOST"
# The flight table on a heading (the same integers the engine walks by):
# 32 Links per 55 intervals.
HEADINGS_FLIGHT = direction_flight(
    ((0, 0, 0), (0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
)


@dataclass(frozen=True)
class Click:
    """One click line of a receiver body: DETECTOR, all of it but the tick."""

    receiver: int
    node: tuple[int, int, int]
    clock: int
    ordinal: int
    tick: int
    amount: int
    reading: int | None

    @property
    def arrival_count(self) -> int:
        """n_B at the click less the row's ordinal: the flight in the
        receiver's own counts."""
        return self.clock - self.ordinal


@dataclass
class Reading:
    name: str
    folder: Path | None
    completed: bool
    balanced: bool
    ticks: int
    elapsed: float
    lamp_position: tuple[int, int, int]
    lamp_family: str
    mass_position: tuple[int, int, int] | None
    mass_amount: int | None
    plane_x: int
    receivers: dict[int, tuple[int, int, int]]
    clicks: list[Click] = field(default_factory=list)
    face_clicks: dict[str, int] = field(default_factory=dict)
    control_count: int | None = None
    control_source: str = ""
    hypotheses: list[str] = field(default_factory=list)

    @property
    def links_line(self) -> int:
        """The Links from the lamp to the plane."""
        return self.plane_x - self.lamp_position[0]

    @property
    def toward(self) -> int:
        """The sign of y toward the mass: -1 with the lamp above the
        mass's line (series K's geometry), +1 below."""
        centre_y = self.mass_position[1] if self.mass_position is not None else self.lamp_position[1]
        return -1 if self.lamp_position[1] >= centre_y else 1


@dataclass
class Analysis:
    count: int
    mean_count: float
    first_count: int | None
    least_count: int | None
    greatest_count: int | None
    spread: float
    pace: float
    band: float
    centroid_y: float
    centroid_z: float
    ratio_receiver: int | None
    count_ratio: Fraction | None
    ratio_window: int
    consecutive_least: float | None
    consecutive_greatest: float | None
    first_tick: int | None
    owed_mean: float
    receivers_lit: int
    intercept: float = math.nan
    slope: float = math.nan


def clicks_of(lines, receivers: set[int], family: str) -> list[Click]:
    """The receivers' clicks of the lamp's family off the record's lines
    (a line a string of `events.jsonl` or a decoded object): `click`
    events written by a receiver body (`measured` its number) carrying a
    record (the row's ordinal) and the receiver's own count `clock`."""
    found: list[Click] = []
    for line in lines:
        if isinstance(line, str):
            if '"click"' not in line or '"clock"' not in line:
                continue
            event = json.loads(line)
        else:
            event = line
        if event.get("event") != "click" or event.get("family") != family:
            continue
        if event.get("measured") not in receivers or "record" not in event or "clock" not in event:
            continue
        amount = int(event.get("amount", 1))
        reading = event.get("reading")
        found.append(
            Click(
                int(event["measured"]),
                tuple(int(v) for v in event["node"]),  # type: ignore[arg-type]
                int(event["clock"]),
                int(event["record"]) & ORDINAL_MASK,
                int(event["tick"]),
                amount,
                int(reading) if isinstance(reading, int) else None,
            )
        )
    return found


def face_clicks_of(lines, family: str) -> dict[str, int]:
    """The clicks of the lamp's family on the faces (rows that left the
    board), per face: the control's FAIL if any."""
    found: dict[str, int] = {}
    for line in lines:
        if isinstance(line, str):
            if '"click"' not in line or '"face:' not in line:
                continue
            event = json.loads(line)
        else:
            event = line
        detector = str(event.get("detector", ""))
        if event.get("event") != "click" or not detector.startswith("face:"):
            continue
        if event.get("family") != family:
            continue
        found[detector] = found.get(detector, 0) + int(event.get("amount", 1))
    return found


def massive_arrival_count(links: int, quantum: int, width: int, momentum_magnitude: int) -> int:
    """The massive triple's first age at `links` Links on a heading: the
    least tau with floor((2 tau p + E'_D) / (2 E'_D)) >= links, E'_0 = Q S
    M_row, E'_D = isqrt(E'_0^2 + 3 p^2) (NEWTON_ON_THE_SIDE.md 3 (b))."""
    rest = LABEL_SCALE * width * quantum
    wall = math.isqrt(rest * rest + 3 * momentum_magnitude * momentum_magnitude)
    tau = 0
    while (2 * tau * momentum_magnitude + wall) // (2 * wall) < links:
        tau += 1
    return tau


def light_arrival_count(links: int) -> int:
    """The flight table's first age at `links` Links on a heading (the
    engine's own table; 55 for 32 Links, 89 for 52)."""
    tau = 0
    while int(HEADINGS_FLIGHT.manhattan_steps(np.array([HEADING_OFFSET]), np.array([tau]))[0]) < links:
        tau += 1
    return tau


def world_name(model: str) -> str | None:
    found = MODEL_PATTERN.match(model)
    return None if found is None else found.group("name")


def read_run(folder: Path) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    if not record.get("clock_stamp"):
        raise SystemExit(f"{folder}: the record carries no clock stamp; nothing here reads the tick")
    name = world_name(str(record["model"]))
    assert name is not None
    document = world_of_run(folder)
    world = parse_nature_beam_world(document)
    lamps = [(i + 1, m) for i, m in enumerate(world.measured) if m.lamp is not None]
    lamp_number, lamp = lamps[0]
    lamp_family = world.families[lamp.family]
    masses = [(i + 1, m) for i, m in enumerate(world.measured) if world.families[m.family].free]
    receivers = {
        i + 1: tuple(m.position)
        for i, m in enumerate(world.measured)
        if i + 1 != lamp_number and not world.families[m.family].free and m.lamp is None
    }
    plane_x = next(iter(receivers.values()))[0]
    reading = Reading(
        name=name,
        folder=folder,
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        ticks=int(record["completed_ticks"]),
        elapsed=float(record.get("elapsed_seconds", 0.0) or 0.0),
        lamp_position=tuple(lamp.position),  # type: ignore[arg-type]
        lamp_family=lamp_family.name,
        mass_position=tuple(masses[0][1].position) if masses else None,  # type: ignore[arg-type]
        mass_amount=int(masses[0][1].amount) if masses else None,
        plane_x=plane_x,
        receivers=receivers,  # type: ignore[arg-type]
        hypotheses=list(record.get("hypotheses", [])),
    )
    links = reading.links_line
    if lamp_family.massive:
        assert lamp.lamp is not None and lamp.lamp.momentum_magnitude is not None
        reading.control_count = massive_arrival_count(
            links, lamp_family.quantum, world.width, lamp.lamp.momentum_magnitude
        )
        reading.control_source = (
            f"the massive triple (M_row {lamp_family.quantum}, S {world.width}, p "
            f"{lamp.lamp.momentum_magnitude}) at {links} Links"
        )
    else:
        reading.control_count = light_arrival_count(links)
        reading.control_source = f"the flight table on the heading at {links} Links"
    refuse_trimmed_record(folder)
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        lines = [text for text in stream if '"click"' in text]
    reading.clicks = clicks_of(lines, set(receivers), lamp_family.name)
    reading.face_clicks = face_clicks_of(lines, lamp_family.name)
    return reading


def find_runs(root: Path) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        if path.parent.name == "resolved_view":
            continue
        record = json.loads(path.read_text(encoding="utf-8"))
        if world_name(str(record.get("model", ""))) is not None:
            found.append(read_run(path.parent))
    order = {"control": 0, "mass": 1, "light": 2}
    return sorted(found, key=lambda r: (order.get(r.name, 9), r.name))


def analyse(reading: Reading, window_start: int) -> Analysis:
    """The Outside arithmetic on the clicks whose receiver count is at or
    after `window_start` (the module docstring)."""
    window = [c for c in reading.clicks if c.clock >= window_start]
    if not window:
        return Analysis(
            0, math.nan, None, None, None, math.nan, math.nan, math.nan, math.nan, math.nan,
            None, None, 0, None, None, None, math.nan, 0,
        )  # fmt: skip
    # The birth's convention (RUN_14.md step 6): a lamp at the content K
    # births at its first self-creation, skips the second once (its
    # accumulator at K - M_row below the wall K) and births at every one
    # after, so the ordinal lags the lamp's count by one from the third
    # self-creation on; the first ordinal's count stands apart, the rest
    # are read for "every click alike".
    ordered = sorted(window, key=lambda c: (c.ordinal, c.clock))
    first_count = ordered[0].arrival_count
    rest = ordered[1:] or ordered
    counts = [c.arrival_count for c in rest]
    total = sum(c.amount for c in window)
    mean = sum(c.amount * c.arrival_count for c in window) / total
    spread = math.sqrt(sum(c.amount * (c.arrival_count - mean) ** 2 for c in window) / total)
    cy = sum(c.amount * c.node[1] for c in window) / total
    cz = sum(c.amount * c.node[2] for c in window) / total
    by_receiver: dict[int, list[Click]] = {}
    for c in rest:
        by_receiver.setdefault(c.receiver, []).append(c)
    best = max(by_receiver, key=lambda n: (len(by_receiver[n]), -n))
    mine = sorted(by_receiver[best], key=lambda c: (c.ordinal, c.clock))
    ratio: Fraction | None = None
    ratio_window = 0
    least = greatest = None
    if len(mine) >= 2 and mine[-1].ordinal != mine[0].ordinal:
        ratio = Fraction(mine[-1].clock - mine[0].clock, mine[-1].ordinal - mine[0].ordinal)
        ratio_window = mine[-1].clock - mine[0].clock
        pairs = [
            (b.clock - a.clock) / (b.ordinal - a.ordinal)
            for a, b in zip(mine, mine[1:], strict=False)
            if b.ordinal != a.ordinal
        ]
        if pairs:
            least, greatest = min(pairs), max(pairs)
    first = min(reading.clicks, key=lambda c: c.tick) if reading.clicks else None
    # The line of the arrival counts against the ordinals: the intercept at
    # the ordinal 0 (both clocks at 0) the flight's count, the slope the
    # receiver's rate less the lamp's (the count ratio's excess over 1).
    xs = np.array([c.ordinal for c in rest], dtype=float)
    ys = np.array([c.arrival_count for c in rest], dtype=float)
    dx = xs - xs.mean()
    slope = float((dx * (ys - ys.mean())).sum() / (dx * dx).sum()) if (dx * dx).sum() > 0 else math.nan
    intercept = float(ys.mean() - slope * xs.mean()) if not math.isnan(slope) else math.nan
    return Analysis(
        count=total,
        mean_count=mean,
        first_count=first_count,
        least_count=min(counts),
        greatest_count=max(counts),
        spread=spread,
        pace=reading.links_line / mean,
        band=2.0 / mean,
        centroid_y=cy,
        centroid_z=cz,
        ratio_receiver=best,
        count_ratio=ratio,
        ratio_window=ratio_window,
        consecutive_least=least,
        consecutive_greatest=greatest,
        first_tick=first.tick if first is not None else None,
        owed_mean=sum(c.tick - c.clock for c in window) / len(window),
        receivers_lit=len({c.receiver for c in window}),
        intercept=intercept,
        slope=slope,
    )


def fmt(value: object, digits: int = 3) -> str:
    if value is None:
        return "-"
    if isinstance(value, Fraction):
        return f"{float(value):.{digits + 1}f}"
    if isinstance(value, float):
        return "-" if math.isnan(value) else f"{value:.{digits}f}"
    return str(value)


class Verdicts:
    def __init__(self) -> None:
        self.inside = 0
        self.outside = 0
        self.failed_checks = 0

    def check(self, label: str, ok: bool) -> None:
        print(f"  record check {'passed' if ok else 'FAILED'}: {label}")
        self.failed_checks += not ok

    def pin(self, label: str, value: float | None, pin: float, bracket: float, detail: str = "") -> bool:
        ok = value is not None and not math.isnan(value) and abs(value - pin) <= bracket
        print(
            f"  {'PASS' if ok else 'FAIL'} {label}: {fmt(value)} against the pin {pin:g} +- {bracket:g}"
            f"{' ' + detail if detail else ''}"
        )
        self.inside += ok
        self.outside += not ok
        return ok

    def exact(self, label: str, ok: bool, detail: str) -> bool:
        print(f"  {'PASS' if ok else 'FAIL'} {label}: {detail}")
        self.inside += ok
        self.outside += not ok
        return ok


def report(readings: list[Reading], register: dict[str, object]) -> int:
    """Every reading by kind, the verdicts against the register's pins."""
    worlds = register["worlds"]
    assert isinstance(worlds, dict)
    windows = register.get("window", {})
    assert isinstance(windows, dict)
    verdicts = Verdicts()
    analyses: dict[str, Analysis] = {}
    control = next((r for r in readings if r.name == "control"), None)
    for reading in readings:
        window_start = int(windows["light" if reading.lamp_family == "light" else "massive"])
        a = analyse(reading, window_start)
        analyses[reading.name] = a
        pins = worlds.get(reading.name)
        print(
            f"{reading.name} ({reading.folder}): {reading.ticks} intervals, {HOST} {reading.elapsed:.1f} s; "
            f"the hypotheses {reading.hypotheses}"
        )
        verdicts.check("completed", reading.completed)
        verdicts.check("the books balanced at every tick", reading.balanced)
        print(
            f"  {COMPUTATION} the control's arrival count derived before the read: {reading.control_count} "
            f"({reading.control_source}); the window opens at the receiver count {window_start}"
        )
        print(
            f"  {DETECTOR} clicks of `{reading.lamp_family}` at the receivers in the window: {a.count} "
            f"on {a.receivers_lit} receiver(s) ({len(reading.clicks)} over the run); the arrival count "
            f"(clock less the ordinal): mean {fmt(a.mean_count, 2)}, the first ordinal's {a.first_count}, "
            f"then least {a.least_count}, greatest {a.greatest_count}, spread {fmt(a.spread, 2)}; the pace {reading.links_line} Links over that "
            f"count {fmt(a.pace, 5)} (the band 2 / W = {fmt(a.band, 5)}); the centroid y {fmt(a.centroid_y)} "
            f"z {fmt(a.centroid_z)}; the faces' clicks of the family {reading.face_clicks or 'none'}"
        )
        print(
            f"  {COMPUTATION} the line of the arrival counts against the ordinals over the window: the intercept "
            f"{fmt(a.intercept, 2)} (the flight's count where both clocks were 0), the slope {fmt(a.slope, 5)} "
            f"per ordinal (the receiver's rate less the lamp's: the count ratio in the crowd, Einstein's step)"
        )
        print(
            f"  {DETECTOR} the count ratio of consecutive clicks at receiver {a.ratio_receiver} "
            f"(counts apart over ordinals apart, {a.ratio_window} counts): {fmt(a.count_ratio)}; "
            f"the consecutive pairs from {fmt(a.consecutive_least)} to {fmt(a.consecutive_greatest)}"
        )
        print(
            f"  {GAMEBOARD} the first click's tick {a.first_tick}; the receiver's count behind the tick "
            f"{fmt(a.owed_mean, 2)} on average (what it owes the crowd; a diagnostic, never pinned)"
        )
        if pins is None:
            print("  no pin for this world")
            continue
        assert isinstance(pins, dict)
        if reading.name == "control":
            arrival = pins["arrival_count"]
            verdicts.pin(
                "the arrival count (DETECTOR)",
                a.mean_count,
                float(arrival["pin"]),
                float(arrival["bracket"]),
                "(the birth's convention, one count)",
            )
            verdicts.exact(
                "every click after the first the same count (the rung whole)",
                a.count > 0 and a.least_count == a.greatest_count,
                f"the first ordinal's {a.first_count}, then least {a.least_count}, greatest {a.greatest_count}",
            )
            rung = int(register["rung"]["k"])  # type: ignore[index]
            verdicts.pin(
                f"the pace over the window (DETECTOR) against 1 / {rung}",
                a.pace,
                1.0 / rung,
                a.band if not math.isnan(a.band) else 0.0,
                "(the one band rule)",
            )
            verdicts.exact(
                "the arrival Node the line's end (the centroid on the lamp's y and z)",
                a.count > 0
                and abs(a.centroid_y - reading.lamp_position[1]) == 0
                and abs(a.centroid_z - reading.lamp_position[2]) == 0,
                f"centroid ({fmt(a.centroid_y)}, {fmt(a.centroid_z)}) against the lamp's "
                f"({reading.lamp_position[1]}, {reading.lamp_position[2]})",
            )
            verdicts.exact(
                "no click of the family on a face",
                not reading.face_clicks,
                f"{reading.face_clicks or 'none'}",
            )
            ratio = pins["count_ratio"]
            verdicts.pin(
                "the count ratio of consecutive clicks (DETECTOR)",
                None if a.count_ratio is None else float(a.count_ratio),
                float(ratio["pin"]),
                float(ratio["bracket"]),
            )
            continue
        # The mass world and the light world: against the control's read
        # centroid where a control run is present, else against the line's
        # end (COMPUTATION, rung 1: the lamp's y and z).
        if control is not None and control.name in analyses and analyses[control.name].count > 0:
            base_y = analyses[control.name].centroid_y
            base_source = "the control's read centroid"
        else:
            base_y = float(reading.lamp_position[1])
            base_source = "the line's end, the lamp's y (COMPUTATION, rung 1; no control run read)"
        toward = reading.toward * (a.centroid_y - base_y)
        assert reading.control_count is not None
        if (
            control is not None
            and control.lamp_family == reading.lamp_family
            and analyses.get(control.name) is not None
            and analyses[control.name].count > 0
        ):
            base_count = analyses[control.name].mean_count
            count_source = f"the control's read mean {fmt(base_count, 2)}"
        else:
            # The birth's convention, read on the control world and on the
            # tool's bar: every click after the first reads the derived
            # count plus one.
            base_count = float(reading.control_count + 1)
            count_source = (
                f"the derived {reading.control_count} plus the birth's convention's one count "
                "(no control run of this family read)"
            )
        delta = a.mean_count - base_count
        print(
            f"  {COMPUTATION} the arrival count less the control's ({count_source}): {fmt(delta, 2)} "
            f"counts (the ratio {fmt(delta / base_count, 4)}); the centroid's shift toward the "
            f"mass {fmt(toward, 2)} pixels against {base_source}"
        )
        arrival = pins["arrival_count"]
        if reading.lamp_family == "light":
            verdicts.pin(
                "the light row's arrival count less its control (DETECTOR): the read delay, no advance",
                delta,
                float(arrival["pin"]),
                float(arrival["bracket"]),
                f"(the wall's {arrival['wall_delay']} less the two clocks' stretch at {arrival['clocks_rate']} "
                "of the tick; a light row sped up refutes)",
            )
            centroid = pins["centroid_toward_mass"]
            arrivals_ok = verdicts.pin(
                "the lever-arm centroid toward the mass (DETECTOR) under the arrivals count",
                toward,
                float(centroid["arrivals"]),
                float(centroid["bracket"]),
            )
            crossing_ok = verdicts.pin(
                "the lever-arm centroid toward the mass (DETECTOR) under the crossing count",
                toward,
                float(centroid["crossing"]),
                float(centroid["bracket"]),
            )
            if arrivals_ok and not crossing_ok:
                answer = "the row's push reads the arrivals at its Node (the law as coded)"
            elif crossing_ok and not arrivals_ok:
                answer = "the row's push counts the crossings (the click count's term on a row)"
            elif arrivals_ok and crossing_ok:
                answer = "both inside: the bracket does not separate them at this grain"
            else:
                answer = "off both: the straight-path form or the read k_a(b) is refuted, not the count"
            print(f"  the deciding pin's answer: {answer}")
        else:
            verdicts.pin(
                "the advance, the arrival count less the control's (DETECTOR), conditional on k_a(b)",
                delta,
                float(arrival["advance"]),
                float(arrival["bracket"]),
                f"(the wall {arrival['wall_delay']}, the push {arrival['push_advance']}; the count itself {fmt(a.mean_count, 2)})",
            )
            verdicts.exact(
                "the mass world earlier than the control (a fall, not the wall alone)",
                delta < 0,
                f"{fmt(delta, 2)} counts",
            )
            centroid = pins["centroid_toward_mass"]
            verdicts.pin(
                "the centroid toward the mass (DETECTOR), conditional on k_a(b)",
                toward,
                float(centroid["pin"]),
                float(centroid["bracket"]),
                f"({centroid['crossing']} under the crossing count: not separable on the massive row)",
            )
        ratio = pins["count_ratio"]
        verdicts.pin(
            "the count ratio of consecutive clicks (DETECTOR)",
            None if a.count_ratio is None else float(a.count_ratio),
            float(ratio["pin"]),
            float(ratio["bracket"]),
        )
        verdicts.exact(
            "no click of the family on a face",
            not reading.face_clicks,
            f"{reading.face_clicks or 'none'}",
        )
    print(
        f"{verdicts.failed_checks} record check(s) failed; {verdicts.inside} reading(s) inside, "
        f"{verdicts.outside} outside, none moved"
    )
    return 1 if verdicts.failed_checks else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="the folder holding the run folders")
    parser.add_argument("--register", type=Path, default=REGISTER, help="the pins (expectations.json)")
    args = parser.parse_args(argv)
    readings = find_runs(args.root)
    if not readings:
        print(f"no newton_side run under {args.root}", file=sys.stderr)
        return 2
    register = json.loads(args.register.read_text(encoding="utf-8"))
    return report(readings, register)


if __name__ == "__main__":
    sys.exit(main())
