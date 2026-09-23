"""The readings of the ring worlds of `flow-link-v1` (`examples/events/flow_link/`),
read from the runner's record and compared with the pins of
`expectations.json`, written before the run (DESIGN.md section 4,
ALGEBRA.md section 4 of docs/designs/flow_weight/).

Usage: `PYTHONPATH=src python tools/flow_link_readings.py <runs root>
[--window-start 200] [--register examples/events/flow_link/expectations.json]`.
The root holds the runs `tools/run_series.py` wrote (`<root>/<world>/run/`),
told apart by the model of their record (`rays-flow-link-ring-b<b>-[control-]g<gamma>-v1`);
every ring world is read against the control of its b and gamma in the
same root. Every line is one of three kinds ([the register](../docs/EXPERIMENTS.md),
"Two kinds of readings"; the model owner's rule of record 281: only a
detector's reading is a measurement):

- DETECTOR: the screen's clicks (one-Node `wave` pixels reading `age`):
  per start (a lamp, its measured number) the clicks in the window, the
  arrival Node's shift (dy, dz) against the control's arrival Node (the
  count-weighted mean over the start's clicks, and the modal pixel), the
  radial shift toward the mass's line -(dy y + dz z) / r in Links and the
  tangential shift, the click's age less the control's (the delay); the
  ring's means over its starts; the count of starts moved by 0, 1, 2, 3
  Nodes (by the modal pixel).
- COMPUTATION (the host's arithmetic on a DETECTOR reading, labelled so): C_nodes = (the mean
  radial shift / 26) x b x 4 pi S / (3 q), the Nodes' own conversion
  (record 872 (e)), and C_ring = C_nodes / (the lever-arm factor the
  algebra stated before the run), against the expected 2 c_f x 0.990 x
  L / sqrt(L^2 + b^2) on the clock's G M within the grain. Einstein's 4 on
  the comparison side only (record 817); nothing pinned as nature's.
- HOST: the run's seconds and the record's digests.

The record checks (completed, the books balanced at every tick, the
identity `flow-link-v1` under `hypotheses`, `flow_link: true`) fail the
tool; a reading outside its pin is printed with its numbers and never
moved. With `--register` the run blocks (the source sha256, the digests,
the readings and the verdicts) are written into the expectations file
under `runs`, the pins untouched. The calibration copies
(`calibration_mass_g*.json`, the registered optical worlds under the key)
are read by `tools/lensing_readings.py` against the registered controls,
not here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from event_universe.world_loading import world_of_run
from event_universe.trimmed_record import refuse_trimmed_record

ROOT = Path(__file__).resolve().parents[1]
EXPECTATIONS = ROOT / "examples" / "events" / "flow_link" / "expectations.json"
MODEL = re.compile(r"^rays-flow-link-ring-b(?P<b>\d+)-(?P<control>control-)?g(?P<gamma>\d)-v1$")
IDENTITY = "flow-link-v1"
SCREEN_PREFIX = "screen_"
# The window of the reading: clicks from this tick on (a row born after the
# crowd has filled the box, about 118 intervals, arrives after about 210).
WINDOW_START = 200
DETECTOR, COMPUTATION, GAMEBOARD, HOST = "DETECTOR", "COMPUTATION", "GAMEBOARD", "HOST"


@dataclass
class Start:
    number: int
    y: int  # about the mass's line
    z: int
    clicks: int = 0
    sum_dy: float = 0.0
    sum_dz: float = 0.0
    age_sum: int = 0
    pixels: Counter = field(default_factory=Counter)

    @property
    def r(self) -> float:
        return math.sqrt(self.y * self.y + self.z * self.z)

    def mean(self, centre: tuple[int, int]) -> tuple[float, float]:
        if not self.clicks:
            return (math.nan, math.nan)
        return (self.sum_dy / self.clicks - centre[0], self.sum_dz / self.clicks - centre[1])

    def modal(self, centre: tuple[int, int]) -> tuple[int, int]:
        (y, z), _ = self.pixels.most_common(1)[0]
        return (y - centre[0], z - centre[1])

    @property
    def age(self) -> float:
        return self.age_sum / self.clicks if self.clicks else math.nan


@dataclass
class Reading:
    name: str
    folder: Path
    b: int
    gamma: int
    control: bool
    completed: bool
    balanced: bool
    ticks: int
    elapsed: float
    fingerprint: str
    hypotheses: list[str]
    flow_link: object
    digests: dict[str, str]
    centre: tuple[int, int]
    window: tuple[int, int]
    starts: dict[int, Start] = field(default_factory=dict)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_run(folder: Path, window_start: int) -> Reading | None:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    match = MODEL.match(str(record["model"]))
    if match is None:
        return None
    document = world_of_run(folder)
    shape = [int(c) for c in document["shape"]]  # type: ignore[index]
    centre = (shape[1] // 2, shape[2] // 2)
    ticks = int(record["completed_ticks"])
    reading = Reading(
        name=str(record["model"])[len("rays-flow-link-") : -len("-v1")].replace("-", "_"),
        folder=folder,
        b=int(match["b"]),
        gamma=int(match["gamma"]),
        control=match["control"] is not None,
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        ticks=ticks,
        elapsed=float(record["elapsed_seconds"]),
        fingerprint=str(record["source_sha256"]),
        hypotheses=list(record["hypotheses"]),
        flow_link=record.get("flow_link"),
        digests={
            "state_sha256": digest(folder / "state.json"),
            "audit_sha256": hashlib.sha256(json.dumps(record.get("audit", [])).encode()).hexdigest(),
            "events_sha256": digest(folder / "events.jsonl"),
        },
        centre=centre,
        window=(window_start, ticks + 1),
    )
    for index, entry in enumerate(document["measured"]):  # type: ignore[union-attr]
        if "lamp" in entry:  # type: ignore[operator]
            position = entry["position"]  # type: ignore[index]
            reading.starts[index + 1] = Start(
                index + 1, int(position[1]) - centre[0], int(position[2]) - centre[1]
            )
    lo, hi = reading.window
    refuse_trimmed_record(folder)
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if '"click"' not in line or '"screen_' not in line:
                continue
            event = json.loads(line)
            if event.get("event") != "click" or not str(event.get("detector", "")).startswith(
                SCREEN_PREFIX
            ):
                continue
            tick = int(event["tick"])
            if not lo <= tick < hi:
                continue
            start = reading.starts.get(int(event["number"]))
            if start is None:
                continue
            amount = int(event["amount"])
            node = event["node"]
            start.clicks += amount
            start.sum_dy += amount * int(node[1])
            start.sum_dz += amount * int(node[2])
            start.age_sum += amount * int(event["age"])
            start.pixels[(int(node[1]), int(node[2]))] += amount
    return reading


def find_runs(root: Path, window_start: int) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        reading = read_run(path.parent, window_start)
        if reading is not None:
            found.append(reading)
    return found


def fmt(value: float, digits: int = 3) -> str:
    return "nan" if math.isnan(value) else f"{value:.{digits}f}"


def verdict(inside: bool) -> str:
    return "inside" if inside else "OUTSIDE"


@dataclass
class Result:
    lines: list[str]
    inside: int = 0
    outside: int = 0
    failed: int = 0
    block: dict[str, object] = field(default_factory=dict)


def read_ring(reading: Reading, control: Reading | None, pin: dict[str, object]) -> Result:
    out = Result([])
    out.lines.append(
        f"{reading.name}: b = {reading.b}, gamma {reading.gamma}, {len(reading.starts)} starts; "
        f"{reading.ticks} intervals, {reading.elapsed:.1f} s ({HOST}); the window {reading.window[0]} .. {reading.window[1] - 1}"
    )
    for name, ok in (
        ("completed", reading.completed),
        ("the books balanced at every tick", reading.balanced),
        (f"the identity {IDENTITY} under hypotheses", IDENTITY in reading.hypotheses),
        ("flow_link: true in run.json", reading.flow_link is True),
        ("the control run present", control is not None),
    ):
        if not ok:
            out.failed += 1
            out.lines.append(f"  RECORD CHECK FAILED: {name}")
    if not reading.completed:
        # The runner's log beside the run (`tools/run_series.py`'s layout):
        # the refusal that stopped the run, a HOST reading of the register.
        log = reading.folder.parent / "log.txt"
        refusal = (
            next(
                (
                    line.strip()
                    for line in reversed(log.read_text(encoding="utf-8").splitlines())
                    if "Error" in line
                ),
                "(no log)",
            )
            if log.exists()
            else "(no log)"
        )
        out.lines.append(f"  {HOST}: the run stopped after {reading.ticks} intervals: {refusal[:400]}")
        out.block = {"refusal": refusal[:400]}
        return out
    if control is None:
        return out
    radial: list[float] = []
    tangential: list[float] = []
    delays: list[float] = []
    moved: Counter = Counter()
    per_start: dict[str, object] = {}
    expected_nodes = pin["arrival_nodes"]["value"]  # type: ignore[index]
    nodes_agree = 0
    out.lines.append(
        f"  {DETECTOR}: per start (y, z): clicks; the arrival Node's shift (dy, dz), the mean and the modal; "
        f"the radial shift (Links); the delay (intervals); the map's (dy, dz)"
    )
    for number, start in sorted(reading.starts.items()):
        base = control.starts.get(number)
        if base is None or not base.clicks or not start.clicks:
            out.failed += 1
            out.lines.append(
                f"    ({start.y:+d},{start.z:+d}): no clicks in the window (RECORD CHECK FAILED)"
            )
            continue
        b_dy, b_dz = base.mean(control.centre)
        m_dy, m_dz = start.mean(reading.centre)
        dy, dz = m_dy - b_dy, m_dz - b_dz
        c_dy, c_dz = base.modal(control.centre)
        p_dy, p_dz = start.modal(reading.centre)
        modal = (p_dy - c_dy, p_dz - c_dz)
        r = start.r
        radial_shift = -(dy * start.y + dz * start.z) / r
        tangential_shift = (dy * (-start.z) + dz * start.y) / r
        delay = start.age - base.age
        radial.append(radial_shift)
        tangential.append(tangential_shift)
        delays.append(delay)
        moved[abs(modal[0]) + abs(modal[1])] += 1
        key = f"({start.y},{start.z})"
        expected = expected_nodes.get(key)  # type: ignore[union-attr]
        agrees = expected is not None and list(modal) == list(expected)
        nodes_agree += agrees
        per_start[key] = {
            "clicks": start.clicks,
            "shift_mean": [round(dy, 3), round(dz, 3)],
            "shift_modal": list(modal),
            "radial_shift": round(radial_shift, 4),
            "delay": round(delay, 3),
            "map": expected,
            "agrees": agrees,
        }
        out.lines.append(
            f"    ({start.y:+d},{start.z:+d}): {start.clicks:4d}; ({dy:+.2f}, {dz:+.2f}) modal ({modal[0]:+d}, {modal[1]:+d}); "
            f"{radial_shift:+.3f}; {delay:+.2f}; map {tuple(expected) if expected else None}{' ok' if agrees else ''}"
        )
    count = len(radial)
    if not count:
        return out
    mean_radial = sum(radial) / count
    sd_radial = math.sqrt(sum((v - mean_radial) ** 2 for v in radial) / max(1, count - 1))
    mean_tangential = sum(tangential) / count
    mean_delay = sum(delays) / count
    constants = pin["_constants"]  # type: ignore[index]
    nodes_conversion = float(constants["nodes_conversion"])
    half = int(constants["path_half_length"])
    c_nodes = mean_radial / half * reading.b * nodes_conversion
    lever = float(pin["c_ring"]["lever_arm_factor"])  # type: ignore[index]
    c_ring = c_nodes / lever
    checks = [
        (
            "radial_shift",
            DETECTOR,
            "the ring's mean radial shift of the arrival Node (Links)",
            mean_radial,
            float(pin["radial_shift"]["value"]),
            float(pin["radial_shift"]["tolerance"]),
        ),  # type: ignore[index]
        (
            "tangential_shift",
            DETECTOR,
            "the ring's mean tangential shift (Links)",
            mean_tangential,
            float(pin["tangential_shift"]["value"]),
            float(pin["tangential_shift"]["tolerance"]),
        ),  # type: ignore[index]
        (
            "delay",
            DETECTOR,
            "the ring's mean delay (intervals)",
            mean_delay,
            float(pin["delay"]["value"]),
            float(pin["delay"]["tolerance"]),
        ),  # type: ignore[index]
        (
            "c_nodes",
            COMPUTATION,
            "C_nodes = (mean radial shift / 26) x b x 4 pi S / (3 q)",
            c_nodes,
            float(pin["c_nodes"]["value"]),
            float(pin["c_nodes"]["tolerance"]),
        ),  # type: ignore[index]
        (
            "c_ring",
            COMPUTATION,
            f"C_ring = C_nodes / {lever} (the stated lever-arm factor) against the expected 2 c_f x 0.990 x L / sqrt(L^2 + b^2)",
            c_ring,
            float(pin["c_ring"]["expected"]),
            float(pin["c_ring"]["grain"]),
        ),  # type: ignore[index]
    ]
    block: dict[str, object] = {
        "starts": count,
        "moved_by_0_1_2_3_nodes": [moved[k] for k in range(4)],
        "arrival_nodes_agreeing_with_the_map": nodes_agree,
        "radial_shift_sd": round(sd_radial, 4),
        "per_start": per_start,
    }
    out.lines.append(
        f"  {DETECTOR}: starts moved by 0 / 1 / 2 / 3 Nodes (modal): {moved[0]} / {moved[1]} / {moved[2]} / {moved[3]} "
        f"(the map's {' / '.join(str(v) for v in pin['arrival_nodes']['moved_by_0_1_2_3_nodes'])}); "  # type: ignore[index]
        f"arrival Nodes agreeing with the map's {nodes_agree} of {count}; the radial shifts' sd {sd_radial:.3f}"
    )
    for key, kind, line, value, expected, tolerance in checks:
        inside = abs(value - expected) <= tolerance + 1e-9
        out.inside += inside
        out.outside += not inside
        block[key] = {
            "value": round(value, 4),
            "expected": expected,
            "tolerance": tolerance,
            "inside": inside,
        }
        out.lines.append(
            f"  {kind}: {line}: {fmt(value)} against {expected} +- {tolerance} ({verdict(inside)}"
            f"{'' if inside else f', by {abs(value - expected) - tolerance:.3f}'})"
        )
    # The residual of C_ring in grains beside the strict pin: the design's
    # verdict sentence (DESIGN.md section 0, the reviewer's must-fix line)
    # reads 2 c_f within the two factors "to one to three grains", and its
    # own algebra sits 1.0 / 2.4 / 1.4 grains off at b = 3 / 6 / 8, gamma 1.
    grain = float(pin["c_ring"]["grain"])  # type: ignore[index]
    residual = (c_ring - float(pin["c_ring"]["expected"])) / grain  # type: ignore[index]
    algebra = (float(pin["c_ring"]["value"]) - float(pin["c_ring"]["expected"])) / grain  # type: ignore[index]
    block["c_ring_residual_grains"] = round(residual, 2)
    block["c_ring_algebra_residual_grains"] = round(algebra, 2)
    out.lines.append(
        f"  {COMPUTATION}: C_ring's residual from the expected in grains: {residual:+.2f} (the algebra's own "
        f"{algebra:+.2f} at this b and gamma; the design's verdict sentence: within one to three grains)"
    )
    as_built = float(pin["radial_shift"]["as_built"])  # type: ignore[index]
    out.lines.append(
        f"  {DETECTOR}: the mean radial shift against the law as built ({as_built}): "
        f"{'the key is in the run' if abs(mean_radial - as_built) > abs(mean_radial - float(pin['radial_shift']['value'])) else 'NEARER THE LAW AS BUILT'}"  # type: ignore[index]
    )
    out.lines.append(
        f"  {COMPUTATION}: C_ring bare against 4: {fmt(c_ring)} (Einstein's 4 on the comparison side only, record 817; "
        f"the expected {pin['c_ring']['expected']} carries the shells' {pin['c_ring']['shells_factor']} and the path's {pin['c_ring']['path_factor']})"  # type: ignore[index]
    )
    out.block = block
    return out


def read_control(reading: Reading) -> Result:
    out = Result([])
    out.lines.append(
        f"{reading.name}: the control, b = {reading.b}, gamma {reading.gamma}; {reading.ticks} intervals, "
        f"{reading.elapsed:.1f} s ({HOST})"
    )
    for name, ok in (
        ("completed", reading.completed),
        ("the books balanced at every tick", reading.balanced),
        (f"the identity {IDENTITY} under hypotheses", IDENTITY in reading.hypotheses),
    ):
        if not ok:
            out.failed += 1
            out.lines.append(f"  RECORD CHECK FAILED: {name}")
    ages = [s.age for s in reading.starts.values() if s.clicks]
    own = sum(1 for s in reading.starts.values() if s.clicks and s.modal(reading.centre) == (s.y, s.z))
    out.lines.append(
        f"  {DETECTOR}: {len(ages)} of {len(reading.starts)} starts click in the window; {own} arrive at their own (y, z); "
        f"the mean age {fmt(sum(ages) / len(ages) if ages else math.nan, 2)} intervals "
        f"(the clock's word unchanged: no crowd, the key reads nothing)"
    )
    out.block = {
        "starts_clicking": len(ages),
        "starts_at_their_own_node": own,
        "mean_age": round(sum(ages) / len(ages), 3) if ages else None,
    }
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("root", type=Path)
    parser.add_argument("--window-start", type=int, default=WINDOW_START)
    parser.add_argument("--expectations", type=Path, default=EXPECTATIONS)
    parser.add_argument(
        "--register", action="store_true", help="write the run blocks into the expectations file"
    )
    parser.add_argument(
        "--runs-key",
        default="runs",
        help="the key of the expectations file the run blocks are written under (a re-run on another head keeps the first run's blocks)",
    )
    args = parser.parse_args(argv)
    register = json.loads(args.expectations.read_text(encoding="utf-8"))
    readings = find_runs(args.root, args.window_start)
    if not readings:
        print(f"no flow-link ring run under {args.root}")
        return 1
    controls = {(r.b, r.gamma): r for r in readings if r.control}
    inside = outside = failed = 0
    runs: dict[str, object] = {}
    for reading in readings:
        if reading.control:
            result = read_control(reading)
        else:
            pin = dict(register["worlds"][reading.name])
            pin["_constants"] = register["constants"]
            result = read_ring(reading, controls.get((reading.b, reading.gamma)), pin)
        print("\n".join(result.lines))
        inside += result.inside
        outside += result.outside
        failed += result.failed
        runs[reading.name] = {
            "source_sha256": reading.fingerprint,
            "completed_ticks": reading.ticks,
            "elapsed_seconds": round(reading.elapsed, 3),
            "hypotheses": reading.hypotheses,
            "flow_link": reading.flow_link,
            "window_start": args.window_start,
            **reading.digests,
            **result.block,
            "readings": {
                "inside": result.inside,
                "outside": result.outside,
                "record_checks_failed": result.failed,
            },
        }
    print(f"\n{failed} record checks failed, {inside} readings inside, {outside} outside; nothing moved")
    if args.register:
        register[args.runs_key] = {**register.get(args.runs_key, {}), **runs}
        args.expectations.write_text(json.dumps(register, indent=1) + "\n", encoding="utf-8")
        print(f"the run blocks written to {args.expectations}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
