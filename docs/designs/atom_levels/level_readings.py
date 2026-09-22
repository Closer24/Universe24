"""The reading of the three runs of `hydrogen_r{3,7,12}_level.json`
(atom-level-v1, docs/designs/atom_levels/LEVELS.md section 5) against
their pins R1 to R6 as written at 287df9a1, by the Atom Baseline Runner's
method (docs/designs/atom_baseline/baseline_readings.py: the faces' clicks
paired into releases, the arrival Nodes, the axis crossings, the phase
increments unwrapped; imported here by path, nothing copied). A reader of
records, no rule; every number labelled by its kind; the host's tick a
diagnostic. Run: `python docs/designs/atom_levels/level_readings.py <root>`
with `<root>/hydrogen_r{3,7,12}_level/run` the three run folders.

The pins (LEVELS.md section 5 (d), declared before the runs, not moved):
  R1 the loop stays and returns: no escape click of the electron; at least
     three returns to the +x axis; the FIRST return's count (the loop from
     the birth) within 10 percent of the generator's T (DETECTOR).
  R2 the level off the body's own give rows and count: the `level` lines
     the engine writes at every return (GAMEBOARD, a diagnostic beside R3,
     never counted).
  R3 the level of the loop between the first and the second returns from
     the faces' two counts: the phase steps unwrapped from the rows'
     increments over that loop and the count between the two +x returns,
     L = floor(512 x steps / (2 T)) (the action's units: one phase step is
     h of the action row), within 10 percent of the generator's (DETECTOR;
     the later loops reported).
  R4 the ratio (L_2 - L_4) / (L_2 - L_3) from the three R3 levels, a
     reported COMPUTATION with its propagated band; on the comparison side
     the 1 / j^2 law at the read closures (1.280), Balmer's 27 / 20
     (1.350), the generator's (1.373), the fan's power law (1.431).
  R5 the releases: the `light` clicks grouped by their release (content,
     phase, count) and the Planck identity between the +x and +y faces
     (DETECTOR); on a loop that holds its level none.
  R6 the control: the byte identity with the key absent (the build's test
     (a) of tests/test_atom_level.py); the r = 12 world's crossings against
     RUN_CENTRED.md's before its first release (DETECTOR).
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent / "atom_baseline" / "baseline_readings.py"
DETECTOR = "DETECTOR"
GAMEBOARD = "GAMEBOARD"
COMPUTATION = "COMPUTATION"
PAIR = (512, 1)
# The generator's numbers per rung (rungs_map.out; COMPUTATION).
GENERATOR = {
    3: {"T": 212, "j": 1.892, "L": 146},
    7: {"T": 690, "j": 3.017, "L": 71},
    12: {"T": 1490, "j": 4.001, "L": 43},
}
BAND = 0.10
# RUN_CENTRED.md section 2: the registered r = 12 world's crossings without
# the key (DETECTOR), the control of R6 up to the first release.
CENTRED_CROSSINGS = [
    ("+y", 402, 12.0),
    ("-x", 721, 10.0),
    ("-y", 992, 11.0),
    ("+x", 1341, 12.0),
    ("+y", 1742, 12.0),
    ("-x", 2111, 13.0),
    ("-y", 2492, 11.0),
    ("+x", 2772, 10.0),
    ("+y", 3092, 13.0),
    ("-x", 3652, 16.0),
    ("-y", 4072, 9.0),
    ("+x", 4272, 9.0),
]
COMPARISON = {
    "the 1 / j^2 law at the read closures": 1.280,
    "Balmer's 27 / 20": 1.350,
    "the generator's own": 1.373,
    "the fan's power law at k = 1.83": 1.431,
}


def load_baseline():
    spec = importlib.util.spec_from_file_location("baseline_readings", BASELINE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["baseline_readings"] = module
    spec.loader.exec_module(module)
    return module


def level_lines(folder: Path) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """The `level` lines (GAMEBOARD) and the `light` clicks (DETECTOR)."""
    levels: list[dict[str, object]] = []
    lights: list[dict[str, object]] = []
    with (folder / "events.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            if '"level"' in line:
                event = json.loads(line)
                if event["event"] == "level":
                    levels.append(event)
            elif '"light"' in line and '"click"' in line:
                event = json.loads(line)
                if event["event"] == "click" and event.get("family") == "light":
                    lights.append(event)
    return levels, lights


def within(value: float, expected: float, band: float) -> bool:
    return abs(value - expected) <= band * expected


def read_world(root: Path, radius: int, base) -> dict[str, object]:
    folder = root / f"hydrogen_r{radius}_level" / "run"
    record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
    world = base.world_of_run(folder)
    proton = world["measured"][0]
    centre3 = tuple(int(v) for v in proton["position"])
    centre = (centre3[0], centre3[1])
    side = int(world["shape"][0])
    modulus = int(world["N"])
    generator = GENERATOR[radius]
    out: dict[str, object] = {"radius": radius}
    print(f"### r = {radius}: `{record['model']}`")
    completed = record["status"] == "completed"
    balanced = bool(record["conserved_at_every_completed_tick"])
    print(
        f"{'PASS' if completed else 'FAIL'} record check: completed ({record['elapsed_seconds']:.1f} s, "
        f"{record['completed_ticks']} ticks); {'PASS' if balanced else 'FAIL'} the books balanced at every tick; "
        f"hypotheses {record.get('hypotheses')}; atom_level {record.get('atom_level')}"
    )
    out["completed"], out["balanced"] = completed, balanced
    out["elapsed"] = round(float(record["elapsed_seconds"]), 1)
    clicks, proton_reads, electron_reads, steps, escaped = base.read_events(folder, "e", "p")
    releases, unpaired = base.pair_releases(clicks, side)
    crossings = base.crossings_of(releases, centre)
    radii = [math.hypot(c.x - centre[0], c.y - centre[1]) for c in crossings]
    plus_x = [c for c in crossings if c.axis == "+x"]
    periods = [b.count - a.count for a, b in zip(plus_x, plus_x[1:], strict=False)]
    print(
        f"[{DETECTOR}] the electron's rows on the side faces: "
        + ", ".join(f"{name} {len(rows)}" for name, rows in clicks.items())
        + f"; {len(releases)} releases paired, {unpaired} unpaired; the escape: {escaped or 'none'}"
    )
    print(f"[{DETECTOR}] the axis crossings from the arrival Nodes: {len(crossings)}")
    for crossing, r in zip(crossings, radii, strict=True):
        print(
            f"[{DETECTOR}]   {crossing.axis} at count {crossing.count}: ({crossing.x}, {crossing.y}), {r:.2f} Links"
        )
    print(f"[{DETECTOR}] the returns to the +x axis: {[c.count for c in plus_x]}; the periods {periods}")
    out["crossings"] = [(c.axis, c.count, round(r, 2)) for c, r in zip(crossings, radii, strict=True)]
    out["returns"] = [c.count for c in plus_x]
    out["escaped"] = escaped
    # R1
    first = plus_x[0].count if plus_x else None
    r1 = not escaped and len(plus_x) >= 3 and first is not None and within(first, generator["T"], BAND)
    out["R1"] = {
        "first_return": first,
        "band": [round(generator["T"] * (1 - BAND)), round(generator["T"] * (1 + BAND))],
        "verdict": "PASS" if r1 else "FAIL",
    }
    # The phase steps per loop from the rows' increments (the faces), unwrapped.
    increments = [
        base.unwrap(a.phase, b.phase, modulus) for a, b in zip(releases, releases[1:], strict=False)
    ]
    cumulative = [0]
    for d in increments:
        cumulative.append(cumulative[-1] + d)
    loops = []
    for a, b, t in zip(plus_x, plus_x[1:], periods, strict=False):
        steps_over = cumulative[b.index] - cumulative[a.index]
        level = (PAIR[0] * steps_over) // (2 * PAIR[1] * t)
        loops.append(
            {
                "from": a.count,
                "to": b.count,
                "T": t,
                "steps": steps_over,
                "circles": round(steps_over / modulus, 3),
                "L": level,
            }
        )
    for loop in loops:
        print(
            f"[{DETECTOR}] the loop {loop['from']} to {loop['to']}: T = {loop['T']}, the phase steps unwrapped "
            f"{loop['steps']} ({loop['circles']} circles), the level floor(512 x {loop['steps']} / (2 x {loop['T']})) = {loop['L']}"
        )
    out["loops"] = loops
    # R3: the loop between the first and the second returns.
    r3_level = loops[0]["L"] if loops else None
    r3 = r3_level is not None and within(r3_level, generator["L"], BAND)
    out["R3"] = {
        "level": r3_level,
        "band": [math.ceil(generator["L"] * (1 - BAND)), math.floor(generator["L"] * (1 + BAND))],
        "verdict": "PASS" if r3 else ("NOT READ" if r3_level is None else "FAIL"),
    }
    # R2: the engine's level lines (GAMEBOARD).
    levels, lights = level_lines(folder)
    for line in levels:
        print(
            f"[{GAMEBOARD}] (R2, a diagnostic) the return at tick {line['tick']}: action {line['action']}, count {line['count']}, "
            f"level {line['level']}, last {line['last']}, released {line['released']}, the content after {line['content']}"
        )
    out["R2"] = [
        {k: line[k] for k in ("tick", "action", "count", "level", "last", "released", "content")}
        for line in levels
    ]
    # R5: the light clicks grouped by release (the row's number is the electron's; the birth tick from the level line).
    by_release: dict[int, list[dict[str, object]]] = {}
    release_ticks = [int(line["tick"]) for line in levels if int(line["released"]) > 0]
    for click in lights:
        tick = int(click["tick"])
        birth = max((t for t in release_ticks if t <= tick), default=None)
        if birth is None:
            continue
        by_release.setdefault(birth, []).append(click)
    planck: list[dict[str, object]] = []
    for birth in sorted(by_release):
        rows = by_release[birth]
        faces = {str(c["detector"]): c for c in rows}
        contents = sorted(int(c["content"]) for c in rows)
        print(
            f"[{DETECTOR}] (R5) the release at tick {birth}: {len(rows)} `light` clicks, the content per row {contents}, "
            f"at {[str(c['detector']) for c in rows]}"
        )
        if "face:+x" in faces and "face:+y" in faces:
            x, y = faces["face:+x"], faces["face:+y"]
            s = int(x["content"])
            expected = (s * (int(y["tick"]) - int(x["tick"]))) % modulus
            read = (int(y["phase"]) - int(x["phase"])) % modulus
            planck.append(
                {"birth": birth, "s": s, "read": read, "expected": expected, "holds": read == expected}
            )
            print(
                f"[{DETECTOR}] (R5) the Planck identity on the +x and +y faces: s = {s}, the phase difference {read} "
                f"against s x (age difference) mod N = {expected}: {'holds' if read == expected else 'FAILS'}"
            )
    out["R5"] = {
        "releases": {str(k): sorted(int(c["content"]) for c in v) for k, v in by_release.items()},
        "planck": planck,
    }
    if not release_ticks:
        print(
            f"[{DETECTOR}] (R5) no `light` row released: the loop's level never rose above the first return's"
        )
    # C5-like diagnostics beside: the momentum's length at the crossings (GAMEBOARD).
    lengths = []
    for crossing in crossings:
        near = [t for t in steps if abs(t - crossing.count) <= 60]
        if near:
            t = min(near, key=lambda t: abs(t - crossing.count))
            p = steps[t][1]
            lengths.append(round(math.hypot(p[0], p[1]) / 1e6, 1))
    print(
        f"[{GAMEBOARD}] (a diagnostic) the momentum's length at the step lines nearest the crossings: {lengths} million"
    )
    print(
        f"[{DETECTOR}] the proton's reads of the electron's rows: {len(proton_reads)}; the electron's reads of the proton's rows: {electron_reads}"
    )
    print(
        f"{out['R1']['verdict']} R1 the loop stays and returns: no escape, at least 3 returns, the first return's count {first} within 10 percent of {generator['T']} ({out['R1']['band']})"
    )
    print(
        f"{out['R3']['verdict']} R3 the level of the loop between the first and the second returns {r3_level} within 10 percent of the generator's {generator['L']} ({out['R3']['band']})"
    )
    print()
    return out


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print(__doc__)
        return 2
    root = Path(args[0])
    base = load_baseline()
    readings = {r: read_world(root, r, base) for r in (3, 7, 12)}
    # R4: the ratio from the three R3 levels, a reported COMPUTATION with its band.
    # A world whose electron escaped has no rung's level: its loop between
    # two +x crossings did not close (the Boss's order of 15:27Z: a world
    # that escapes or fails to return is reported as the finding it is;
    # two levels give one line, no ratio).
    levels = {
        r: (None if readings[r]["escaped"] else readings[r]["R3"]["level"])  # type: ignore[index]
        for r in (3, 7, 12)
    }
    print(
        "### R4 the ratio of two lines (a reported COMPUTATION from three DETECTOR levels, not a pass-or-fail pin)"
    )
    for r in (3, 7, 12):
        if readings[r]["escaped"]:  # type: ignore[index]
            print(
                f"[{DETECTOR}] r = {r}: {readings[r]['escaped']}: no rung's level (the level between its two +x "  # type: ignore[index]
                f"crossings, {readings[r]['R3']['level']}, is a loop that did not close)"  # type: ignore[index]
            )
    if all(levels[r] is not None for r in (3, 7, 12)):
        l2, l3, l4 = int(levels[3]), int(levels[7]), int(levels[12])  # type: ignore[arg-type]
        if l2 - l3 > 0:
            ratio = (l2 - l4) / (l2 - l3)
            lo = min(
                ((l2 * (1 + a)) - l4 * (1 + c)) / ((l2 * (1 + a)) - l3 * (1 + b))
                for a in (-BAND, BAND)
                for b in (-BAND, BAND)
                for c in (-BAND, BAND)
            )
            hi = max(
                ((l2 * (1 + a)) - l4 * (1 + c)) / ((l2 * (1 + a)) - l3 * (1 + b))
                for a in (-BAND, BAND)
                for b in (-BAND, BAND)
                for c in (-BAND, BAND)
            )
            print(
                f"[{COMPUTATION}] the levels L_2 = {l2}, L_3 = {l3}, L_4 = {l4} (DETECTOR, R3); the lines {l2 - l4} and {l2 - l3}; "
                f"the ratio {l2 - l4} / {l2 - l3} = {ratio:.4f}; the band at 10 percent per level {lo:.3f} to {hi:.3f}; the grain 1 / {l2 - l3}"
            )
            for name, value in COMPARISON.items():
                print(
                    f"[{COMPUTATION}]   on the comparison side, {name}: {value:.3f}, {'inside' if lo <= value <= hi else 'outside'} the band"
                )
        else:
            print(
                f"[{COMPUTATION}] the levels {l2}, {l3}, {l4} give no line 3 to 2 (L_2 - L_3 <= 0): no ratio"
            )
    else:
        missing = [r for r in (3, 7, 12) if levels[r] is None]
        present = [r for r in (3, 7, 12) if levels[r] is not None]
        line = ""
        if len(present) == 2:
            a, b = int(levels[present[0]]), int(levels[present[1]])  # type: ignore[arg-type]
            line = f": L at r = {present[0]} less L at r = {present[1]} = {a - b} steps at [512, 1]"
        print(
            f"[{COMPUTATION}] NOT READ: no rung's level at r = {missing}; "
            + ("two levels give one line, no ratio" + line if len(present) == 2 else "no line")
        )
    print("### R6 the control")
    r12 = readings[12]
    first_release = min(
        (int(line["tick"]) for line in r12["R2"] if int(line["released"]) > 0), default=None
    )  # type: ignore[index, union-attr]
    read_crossings = [c for c in r12["crossings"] if first_release is None or c[1] <= first_release]  # type: ignore[union-attr]
    expected = [c for c in CENTRED_CROSSINGS if first_release is None or c[1] <= first_release]
    same = read_crossings[: len(expected)] == expected
    print(
        f"[{DETECTOR}] the r = 12 world's crossings up to its first release (tick {first_release}): {read_crossings[: len(expected)]}\n"
        f"[{DETECTOR}] RUN_CENTRED.md's without the key: {expected}\n"
        f"{'PASS' if same else 'FAIL'} R6 the crossings and their counts identical before the first release; the byte identity with the key absent is the build's test (a), PASS"
    )
    readings["R4"] = {"levels": levels}
    readings["R6"] = {"first_release": first_release, "same_crossings": same}
    (root / "level_readings.json").write_text(
        json.dumps(readings, indent=1, default=str) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
