"""The reading of the one run of `hydrogen_r12_centred.json` (centred-step-v1,
docs/designs/atom_give/CENTRED_STEP.md section 4) against its pins C1 to
C5, by the Atom Baseline Runner's method (docs/designs/atom_baseline/
baseline_readings.py: the faces' clicks paired into releases, the arrival
Nodes, the axis crossings; imported here by path, nothing copied). A
reader of records, no rule; the host's tick a labelled diagnostic. Run:
`python docs/designs/atom_give/centred_readings.py <run folder>`.

The pins (CENTRED_STEP.md section 4, declared before the run, not moved
after it):
  C1 the loop stays: no escape face click of the electron in the run and at
     least 12 quarter crossings (DETECTOR); an escape = FAIL.
  C2 every crossing within 9 to 20 Links from the proton's Node, the first
     four within 10 to 15 (DETECTOR, the arrival Nodes); one outside = FAIL.
  C3 three to four returns to the +x axis in 7500 intervals, every period
     within 1400 to 2000 (DETECTOR); outside = FAIL.
  C4 the momentum's length at the crossings within 200 to 350 million
     (GAMEBOARD, the step lines; a diagnostic, not counted).
  C5 the circles per return, reported and not pinned (DETECTOR).
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent / "atom_baseline" / "baseline_readings.py"

PIN_CROSSINGS_AT_LEAST = 12
PIN_RADIUS = (9.0, 20.0)
PIN_FIRST_FOUR = (10.0, 15.0)
PIN_RETURNS = (3, 4)
PIN_PERIOD = (1400, 2000)
PIN_MOMENTUM = (200e6, 350e6)
DETECTOR = "DETECTOR"
GAMEBOARD = "GAMEBOARD"


def load_baseline():
    spec = importlib.util.spec_from_file_location("baseline_readings", BASELINE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["baseline_readings"] = module
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print(__doc__)
        return 2
    folder = Path(args[0])
    base = load_baseline()
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    world = base.world_of_run(folder)
    proton, electron = world["measured"]
    centre3 = tuple(int(v) for v in proton["position"])
    centre = (centre3[0], centre3[1])
    side = int(world["shape"][0])
    modulus = int(world["N"])
    electron_family, proton_family = str(electron["family"]), str(proton["family"])
    verdicts: list[tuple[str, bool | None]] = []

    completed = record["status"] == "completed"
    balanced = bool(record["conserved_at_every_completed_tick"])
    ticks = int(record["completed_ticks"])
    print(
        f"{'PASS' if completed else 'FAIL'} record check: completed ({record['elapsed_seconds']:.1f} s, {ticks} ticks)"
    )
    print(f"{'PASS' if balanced else 'FAIL'} record check: the books balanced at every completed tick")
    print(
        f"[{GAMEBOARD}] world `{record['model']}`: centred_step {world.get('centred_step', False)}, "
        f"hypotheses {record.get('hypotheses')}, the electron's declared momentum {electron['momentum']}, "
        f"start {electron['position']}, the proton at {centre3}"
    )
    print()

    clicks, proton_reads, electron_reads, steps, escaped = base.read_events(
        folder, electron_family, proton_family
    )
    releases, unpaired = base.pair_releases(clicks, side)
    crossings = base.crossings_of(releases, centre)
    print(
        f"[{DETECTOR}] the electron's rows clicked on the side faces: "
        + ", ".join(f"{name} {len(rows)}" for name, rows in clicks.items())
        + f"; {len(releases)} releases paired, {unpaired} clicks unpaired"
    )
    print(f"[{DETECTOR}] the escape: {escaped or 'none: the electron is on the board at the end'}")
    radii = [math.hypot(c.x - centre[0], c.y - centre[1]) for c in crossings]
    print(f"[{DETECTOR}] the axis crossings read from the arrival Nodes: {len(crossings)}")
    for crossing, radius in zip(crossings, radii, strict=True):
        print(
            f"[{DETECTOR}]   {crossing.axis} at count {crossing.count}: the electron at ({crossing.x}, {crossing.y}), {radius:.2f} Links from the proton"
        )
    plus_x = [c for c in crossings if c.axis == "+x"]
    periods = [b.count - a.count for a, b in zip(plus_x, plus_x[1:], strict=False)]
    print(
        f"[{DETECTOR}] the returns to the +x axis: {len(plus_x)} at {[c.count for c in plus_x]}; the periods {periods}"
    )
    # C1
    verdicts.append(
        (
            f"C1 the loop stays: no escape face click and at least {PIN_CROSSINGS_AT_LEAST} quarter crossings (read {len(crossings)} crossings; {escaped or 'no escape'})",
            not escaped and len(crossings) >= PIN_CROSSINGS_AT_LEAST,
        )
    )
    # C2
    inside = all(PIN_RADIUS[0] <= r <= PIN_RADIUS[1] for r in radii) and all(
        PIN_FIRST_FOUR[0] <= r <= PIN_FIRST_FOUR[1] for r in radii[:4]
    )
    verdicts.append(
        (
            f"C2 every crossing within {PIN_RADIUS[0]:.0f} to {PIN_RADIUS[1]:.0f} Links, the first four within {PIN_FIRST_FOUR[0]:.0f} to {PIN_FIRST_FOUR[1]:.0f} (read {[round(r, 2) for r in radii]})",
            inside if radii else None,
        )
    )
    # C3
    ok3 = PIN_RETURNS[0] <= len(plus_x) <= PIN_RETURNS[1] and all(
        PIN_PERIOD[0] <= t <= PIN_PERIOD[1] for t in periods
    )
    verdicts.append(
        (
            f"C3 {PIN_RETURNS[0]} to {PIN_RETURNS[1]} returns to the +x axis with every period within {PIN_PERIOD} (read {len(plus_x)} returns, the periods {periods})",
            ok3 if plus_x else None,
        )
    )
    # C4, GAMEBOARD, not counted: the momentum's length at the step line nearest each crossing.
    lengths = []
    for crossing in crossings:
        near = [t for t in steps if abs(t - crossing.count) <= 60]
        if near:
            t = min(near, key=lambda t: abs(t - crossing.count))
            p = steps[t][1]
            lengths.append(math.hypot(p[0], p[1]))
    print(
        f"[{GAMEBOARD}] (a diagnostic, not counted) the momentum's length at the step lines nearest the crossings: {[round(x / 1e6, 1) for x in lengths]} million label units (the pin C4: 200 to 350)"
    )
    # C5, reported: the circles per return from the releases' phases, the baseline's method.
    increments = [
        base.unwrap(a.phase, b.phase, modulus) for a, b in zip(releases, releases[1:], strict=False)
    ]
    cumulative = [0]
    for d in increments:
        cumulative.append(cumulative[-1] + d)
    circles = [
        (cumulative[b.index] - cumulative[a.index]) / modulus
        for a, b in zip(plus_x, plus_x[1:], strict=False)
    ]
    print(
        f"[{DETECTOR}] C5 (reported, not pinned) the circles per return from the rows' phases: {[f'{j:.3f}' for j in circles]}"
    )
    print(
        f"[{DETECTOR}] the proton's reads of the electron's rows: {len(proton_reads)}; the electron's reads of the proton's rows: {electron_reads}"
    )
    print()
    for label, ok in verdicts:
        print(f"{'NOT READ' if ok is None else 'PASS' if ok else 'FAIL'} {label}")
    passed = sum(1 for _, ok in verdicts if ok)
    failed = sum(1 for _, ok in verdicts if ok is False)
    unread = sum(1 for _, ok in verdicts if ok is None)
    print(
        f"{passed} PASS, {failed} FAIL, {unread} NOT READ of {len(verdicts)} pins (DETECTOR); the GameBoard lines above are diagnostics, not counted"
    )
    return 0 if completed and balanced else 1


if __name__ == "__main__":
    sys.exit(main())
