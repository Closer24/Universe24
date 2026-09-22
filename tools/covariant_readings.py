"""The readings of series S, the covariant readings (`covariant-readings-v1`;
`examples/events/covariant/`), read from the runner's record and compared
with the pins of `expectations.json`, written before the runs.

Usage: `PYTHONPATH=src python tools/covariant_readings.py <runs root>
[--register examples/events/covariant/expectations.json]`. The root holds
the runs `tools/run_series.py` wrote (`<root>/<world>/run/`), told apart by
the model of their record (`beam-covariant-j4_muon_<name>-v1` and
`rays-hubble-stars-covariant-none-space-v1`). Every line is one of two
kinds ([the register](../docs/EXPERIMENTS.md), "Two kinds of readings"):
DETECTOR, a detector's record or a measured event's own record (the
products' clicks on the +x face of the J4 bar; the centre's pointer of the
coasting world, whose z is read by `tools/hubble_stars_readings.py`'s own
rule; the body's `become` line, its Node and its `counted`, the body's own
record), or GAMEBOARD, the host's view (E' at load and E'_0, the `energy`
lines and their ticks, the pace over the late window from the step lines,
the invariant E'^2 <= W < (E' + 1)^2 at every interval, the intervals owed
to proper time, the comparisons). The tick of a line is the record's
ordering, a GameBoard number (the clock audit of 2026-09-22, record 678):
the `become` line is the detector record and its `counted` the clock's
reading; a click's tick orders the record, the product's age being the
reading of its flight.
Since the audit of record 567 (the model owner's rule, records 562 and
564) a GAMEBOARD number is a diagnostic: printed with its expectation,
never a verdict, never counted inside or outside; each names the detector
reading behind it, not yet read. The record checks (completed, the books
balanced at every tick, the invariant on every line) fail the tool; a
reading outside its pin is printed with its numbers and never moved.
With `--register` the run blocks (the source sha256, the digests of the
record, the readings) are written into the expectations file under
`runs`, the pins untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EXPECTATIONS = ROOT / "examples" / "events" / "covariant" / "expectations.json"
MUON_PREFIX = "beam-covariant-"
STARS_MODEL = "rays-hubble-stars-record-covariant-none-space-v1"
DETECTOR = "DETECTOR"
GAMEBOARD = "GAMEBOARD"


@dataclass
class Reading:
    name: str
    folder: Path
    completed: bool
    balanced: bool
    ticks: int
    elapsed: float
    fingerprint: str
    hypotheses: list[str]
    report: dict[str, object]
    digests: dict[str, str]
    become: dict[str, object] | None = None
    clicks: list[dict[str, object]] = field(default_factory=list)
    energy_lines: int = 0
    invariant_failures: int = 0
    most_comparisons: int = 0
    first_energy: dict[int, dict[str, object]] = field(default_factory=dict)
    self_creations: dict[int, list[int]] = field(default_factory=dict)
    waited: dict[str, int] = field(default_factory=dict)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_run(folder: Path) -> Reading:
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    model = str(record["model"])
    name = (
        model[len(MUON_PREFIX) : -len("-v1")]
        if model.startswith(MUON_PREFIX)
        else "coasting_none_covariant"
    )
    reading = Reading(
        name=name,
        folder=folder,
        completed=record["status"] == "completed",
        balanced=bool(record["conserved_at_every_completed_tick"]),
        ticks=int(record["completed_ticks"]),
        elapsed=float(record["elapsed_seconds"]),
        fingerprint=str(record["source_sha256"]),
        hypotheses=list(record["hypotheses"]),
        report=dict(record.get("covariant_readings", {})),
        digests={
            "state_sha256": digest(folder / "state.json"),
            "audit_sha256": hashlib.sha256(
                json.dumps(record.get("audit", [])).encode("utf-8")
            ).hexdigest(),
            "events_sha256": digest(folder / "events.jsonl"),
        },
        waited={
            str(k): int(v)
            for k, v in dict(record.get("covariant_readings", {}).get("waited", {})).items()
        },
    )
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for text in stream:
            if '"energy"' not in text and '"become"' not in text and '"face:' not in text:
                continue
            event = json.loads(text)
            kind = event["event"]
            if kind == "energy":
                reading.energy_lines += 1
                number = int(event["number"])
                energy, square = int(event["energy"]), int(event["square"])
                if not energy * energy <= square < (energy + 1) * (energy + 1):
                    reading.invariant_failures += 1
                reading.most_comparisons = max(reading.most_comparisons, int(event["comparisons"]))
                reading.first_energy.setdefault(number, event)
                if event["creating"]:
                    reading.self_creations.setdefault(number, []).append(int(event["tick"]))
            elif kind == "become":
                reading.become = event
            elif kind == "click" and str(event.get("detector", "")).startswith("face:"):
                reading.clicks.append(event)
    return reading


def find_runs(root: Path) -> list[Reading]:
    found = []
    for path in sorted(root.rglob("run.json")):
        if path.parent.name == "resolved_view":
            continue
        record = json.loads(path.read_text(encoding="utf-8"))
        model = str(record.get("model", ""))
        if model.startswith(MUON_PREFIX) or model == STARS_MODEL:
            found.append(read_run(path.parent))
    return found


def load_tool(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def heading_age(steps: int) -> int:
    """The least age at which a heading row has made `steps` Manhattan steps
    (the engine's flight table on the default table)."""
    from event_universe.events.nature_beam import direction_flight
    from event_universe.events.world import HEADING_OFFSET, parse_nature_beam_world

    world = parse_nature_beam_world(
        {
            "law": "beam",
            "model_id": "flight",
            "shape": [3, 1, 1],
            "ticks": 0,
            "K": 64,
            "release": [1, 1],
            "families": [{"name": "d", "quantum": 1}],
            "measured": [{"position": [1, 0, 0], "family": "d", "amount": 1, "fixed": True}],
        }
    )
    flight = direction_flight(world.directions)
    heading = np.array([HEADING_OFFSET])
    age = 0
    while int(flight.manhattan_steps(heading, np.array([age]))[0]) < steps:
        age += 1
    return age


def resolved_view(folder: Path) -> Path:
    """A view of the run's folder whose `initialization.json` is the resolved
    world (the shipped world places catalog definitions, which the runner
    expands into `resolved_initialization.json`; `hubble_stars_readings.py`
    reads the inline world): the record files linked, nothing copied."""
    resolved = folder / "resolved_initialization.json"
    if not resolved.exists():
        return folder
    view = folder.parent / "resolved_view"
    view.mkdir(exist_ok=True)
    for name in ("run.json", "events.jsonl"):
        link = view / name
        if not link.exists():
            link.symlink_to(folder / name)
    (view / "initialization.json").write_bytes(resolved.read_bytes())
    return view


def diagnostic(
    lines: list[str],
    diagnostics: dict[str, object],
    key: str,
    ok: bool,
    text: str,
    behind: str,
    found: object,
    expected: object,
) -> None:
    """A GAMEBOARD number beside its expectation: a diagnostic line, out of
    the verdicts (records 562 and 564; the audit of record 567), recorded
    under `diagnostics` with its kind."""
    diagnostics[key] = {"kind": GAMEBOARD, "found": found, "expected": expected, "agrees": ok}
    lines.append(
        f"  [{GAMEBOARD}] (a diagnostic, not counted) {text}: {'agrees' if ok else 'differs'}; "
        f"the detector reading behind it, {behind}, not yet read"
    )


def fmt(value: float) -> str:
    return f"{value:.4f}"


def muon_lines(
    reading: Reading, expected: dict[str, object]
) -> tuple[list[str], list[bool], dict[str, object]]:
    """The J4 readings against the pins; returns the lines, the verdicts and
    the registered readings."""
    lines: list[str] = []
    verdicts: list[bool] = []
    registered: dict[str, object] = {}
    decay = dict(expected["decay"])  # type: ignore[call-overload]
    click = dict(expected["click"])  # type: ignore[call-overload]
    first = reading.first_energy.get(1, {})
    registered["energy_at_load"] = int(first.get("energy", -1))
    registered["rest_energy"] = int(first.get("rest", -1))
    diagnostics: dict[str, object] = {}
    registered["diagnostics"] = diagnostics
    ok = (
        registered["energy_at_load"] == expected["energy_at_load"]
        and registered["rest_energy"] == expected["rest_energy"]
    )
    diagnostic(
        lines,
        diagnostics,
        "energy_at_load",
        ok,
        f"E' at load {registered['energy_at_load']} (E'_0 {registered['rest_energy']}): "
        f"expected {expected['energy_at_load']} ({expected['rest_energy']})",
        "the products' clicks and the centre's pointer under the identity (series S)",
        [registered["energy_at_load"], registered["rest_energy"]],
        [expected["energy_at_load"], expected["rest_energy"]],
    )
    become_tick = None if reading.become is None else int(reading.become["tick"])
    become_node = None if reading.become is None else list(reading.become["node"])  # type: ignore[arg-type]
    registered["become_tick"], registered["become_node"] = become_tick, become_node
    design_ok = become_tick is not None and abs(become_tick - float(decay["design"])) <= float(
        decay["tolerance"]
    )
    derived_ok = become_tick == int(decay["derived_tick"]) and become_node == list(decay["derived_node"])
    verdicts += [design_ok, derived_ok]
    lines.append(
        f"  [{DETECTOR}] the `become` line (the 64th self-creation, the body's own record) at tick {become_tick} at {become_node}: "
        f"the design's {decay['design']} +- {decay['tolerance']}: {'inside' if design_ok else 'OUTSIDE'}"
        + (
            ""
            if design_ok
            else f" by {abs(become_tick - float(decay['design'])) - float(decay['tolerance']):.1f}"
        )
        + f"; the derived {decay['derived_tick']} at {decay['derived_node']}: {'inside' if derived_ok else 'OUTSIDE'}"
    )
    creations = reading.self_creations.get(1, [])
    sixty_fourth = creations[63] if len(creations) >= 64 else None
    # The `energy` line is ENGINE.md's GameBoard row and its tick the
    # record's ordering: the identity with the `become` line's tick is a
    # diagnostic, out of the verdicts (the clock audit of 2026-09-22); the
    # `become` line above is the detector record.
    diagnostic(
        lines,
        diagnostics,
        "sixty_fourth_energy_line_tick",
        sixty_fourth == become_tick,
        f"the 64th `creating` energy line at tick {sixty_fourth} against the `become` line's tick "
        f"{become_tick} (the record's ordering)",
        "the `become` line's `counted`, the body's own clock (above, DETECTOR)",
        sixty_fourth,
        become_tick,
    )
    beta = [c for c in reading.clicks if c["family"] == "beta" and c["detector"] == "face:+x"]
    click_tick = None if not beta else int(beta[0]["tick"])
    registered["beta_click_tick"] = click_tick
    registered["beta_click_content"] = None if not beta else int(beta[0]["content"])
    design_ok = click_tick is not None and abs(click_tick - int(click["design"])) <= int(
        click["tolerance"]
    )
    derived_ok = click_tick == int(click["derived_tick"])
    verdicts += [design_ok, derived_ok]
    lines.append(
        f"  [{DETECTOR}] the product `beta`'s click on face:+x at tick {click_tick} (content "
        f"{registered['beta_click_content']}; the tick is the record's ordering, the product's age the "
        "reading of its flight, the clock audit of 2026-09-22): "
        f"the design's {click['design']} +- {click['tolerance']}: "
        f"{'inside' if design_ok else 'OUTSIDE'}; the derived {click['derived_tick']}: "
        f"{'inside' if derived_ok else 'OUTSIDE'}"
    )
    if click_tick is not None:
        back = click_tick - heading_age(int(click["steps_to_the_face"]))
        registered["decay_tick_derived_back_from_the_click"] = back
        lines.append(
            f"  [{DETECTOR}] the decay's tick derived back from the click by the flight table "
            f"({click['steps_to_the_face']} steps of a heading row): {back} (the design's {decay['design']}; "
            f"named as derived)"
        )
    ok = reading.invariant_failures == 0 and reading.energy_lines >= reading.ticks
    registered["energy_lines"] = reading.energy_lines
    registered["most_comparisons"] = reading.most_comparisons
    registered["waited"] = reading.waited
    diagnostic(
        lines,
        diagnostics,
        "invariant",
        ok,
        f"the invariant E'^2 <= W < (E' + 1)^2 on {reading.energy_lines} energy lines: "
        f"{reading.invariant_failures} failures; the most comparisons in one frame "
        f"{reading.most_comparisons}; intervals owed to proper time {reading.waited}",
        "the product's click tick against the decay's derived tick (above)",
        reading.invariant_failures,
        0,
    )
    return lines, verdicts, registered


def coasting_lines(
    reading: Reading, expected: dict[str, object]
) -> tuple[list[str], list[bool], dict[str, object]]:
    lines: list[str] = []
    verdicts: list[bool] = []
    registered: dict[str, object] = {}
    tool = load_tool("hubble_stars_readings_tool", ROOT / "tools" / "hubble_stars_readings.py")
    run = tool.read_run(resolved_view(reading.folder))
    star = run.stars[str(expected["star"])]
    pin = dict(expected["z"])  # type: ignore[call-overload]
    window = (int(pin["window"][0]), int(pin["window"][1]))  # type: ignore[index]
    point = tool.window_point(run, star, window)
    z = None if point is None else float(point.z)
    registered["z"] = z
    ok = z is not None and not math.isnan(z) and float(pin["pin"][0]) <= z <= float(pin["pin"][1])  # type: ignore[index]
    verdicts.append(ok)
    lines.append(
        f"  [{DETECTOR}] {expected['star']}'s 1 + z from the centre's pointer over {list(window)}: z = "
        f"{'nan' if z is None else fmt(z)}: the pin {pin['pin']} (the design's {pin['design']}; the centres "
        f"{fmt(float(pin['centre_continuum']))} and {fmt(float(pin['centre_heading']))}; the register's "
        f"{pin['registered_without_the_key']} without the key): {'inside' if ok else 'OUTSIDE'}"
    )
    first = reading.first_energy.get(star.number, {})
    energy_at_load = int(first.get("energy", -1))
    rest = int(first.get("rest", -1))
    registered["energy_at_load_at_the_grain"], registered["rest_energy_at_the_grain"] = (
        energy_at_load,
        rest,
    )
    ok = (
        energy_at_load == expected["energy_at_load_at_the_grain"]
        and rest == expected["rest_energy_at_the_grain"]
    )
    diagnostics: dict[str, object] = {}
    registered["diagnostics"] = diagnostics
    diagnostic(
        lines,
        diagnostics,
        "energy_at_load_at_the_grain",
        ok,
        f"{expected['star']}'s E' / g at load {energy_at_load} (E'_0 / g {rest}, gamma "
        f"{energy_at_load / max(rest, 1):.5f}): expected {expected['energy_at_load_at_the_grain']} "
        f"({expected['rest_energy_at_the_grain']}, gamma {float(expected['gamma']):.5f})",
        "the star's 1 + z from the centre's pointer (above, DETECTOR)",
        [energy_at_load, rest],
        [expected["energy_at_load_at_the_grain"], expected["rest_energy_at_the_grain"]],
    )
    steps = [t for t in star.steps if window[0] <= t < window[1]]
    pace = len(steps) / (window[1] - window[0])
    registered["pace_in_the_late_window"] = pace
    ok = abs(pace - float(expected["pace"])) <= 0.01
    diagnostic(
        lines,
        diagnostics,
        "pace_in_the_late_window",
        ok,
        f"{expected['star']}'s pace over the late window {pace:.4f} Links per interval "
        f"({len(steps)} steps, the step lines): p / E' = {float(expected['pace']):.4f} within 0.01",
        "the star's arrivals at the centre (the click ticks and ages, DETECTOR)",
        pace,
        float(expected["pace"]),
    )
    ok = reading.invariant_failures == 0 and reading.energy_lines >= reading.ticks
    registered["energy_lines"] = reading.energy_lines
    registered["most_comparisons"] = reading.most_comparisons
    registered["waited"] = reading.waited
    diagnostic(
        lines,
        diagnostics,
        "invariant",
        ok,
        f"the invariant on {reading.energy_lines} energy lines: {reading.invariant_failures} "
        f"failures; the most comparisons in one frame {reading.most_comparisons}; "
        f"intervals owed to proper time by {expected['star']} (number {star.number}) "
        f"{reading.waited.get(str(star.number))}",
        "the star's 1 + z from the centre's pointer (above, DETECTOR)",
        reading.invariant_failures,
        0,
    )
    off = list(reading.report.get("off_identity", []))  # type: ignore[arg-type]
    lines.append(
        f"  [{GAMEBOARD}] the load-time diagnostic: {len(off)} paid families off 3 h n = Q S d (the first "
        f"{off[0] if off else None}); `books` {reading.report.get('books')}"
    )
    return lines, verdicts, registered


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("root", type=Path, help="The folder of the runs (tools/run_series.py --out)")
    parser.add_argument("--expectations", type=Path, default=EXPECTATIONS)
    parser.add_argument("--register", type=Path, help="Write the run blocks into this expectations file")
    args = parser.parse_args(argv)
    expected = json.loads(args.expectations.read_text(encoding="utf-8"))
    runs = find_runs(args.root)
    if not runs:
        print(f"no run of series S under {args.root}")
        return 1
    failed = 0
    inside = 0
    total = 0
    diagnostics = 0
    blocks: dict[str, object] = {}
    print(
        f"Every line is [{DETECTOR}] (a detector's record or a measured event's own record: the only kind "
        f"reality has) or [{GAMEBOARD}] (the host's view: a diagnostic, printed with its expectation, never "
        "a verdict, records 562 and 564); the pins are examples/events/covariant/expectations.json, "
        "written before the runs."
    )
    for reading in runs:
        print(
            f"{reading.name}: {reading.ticks} intervals, {reading.elapsed:.1f} s, hypotheses {reading.hypotheses}"
        )
        checks = reading.completed and reading.balanced and reading.invariant_failures == 0
        print(
            f"  record checks: completed {reading.completed}, balanced {reading.balanced}, the invariant "
            f"failures {reading.invariant_failures}: {'PASS' if checks else 'FAIL'}"
        )
        if not checks:
            failed += 1
        pins = expected["worlds"].get(reading.name)
        if pins is None:
            print("  no pins for this world")
            failed += 1
            continue
        if reading.name.startswith("j4_muon"):
            lines, verdicts, registered = muon_lines(reading, pins)
        else:
            lines, verdicts, registered = coasting_lines(reading, pins)
        for line in lines:
            print(line)
        inside += sum(verdicts)
        total += len(verdicts)
        diagnostics += len(registered.get("diagnostics", {}))  # type: ignore[arg-type]
        blocks[reading.name] = {
            "source_sha256": reading.fingerprint,
            "completed_ticks": reading.ticks,
            "elapsed_seconds": round(reading.elapsed, 1),
            "hypotheses": reading.hypotheses,
            **reading.digests,
            "readings": registered,
            "inside": sum(verdicts),
            "of": len(verdicts),
        }
    print(
        f"{failed} record check(s) failed; {inside} reading(s) inside, {total - inside} outside; "
        f"{diagnostics} GameBoard diagnostic(s) printed and not counted"
    )
    if args.register is not None:
        document = json.loads(args.register.read_text(encoding="utf-8"))
        document.setdefault("runs", {}).update(blocks)
        args.register.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(f"registered {len(blocks)} run block(s) in {args.register}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
