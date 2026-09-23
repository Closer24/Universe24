"""Read the runs of the k_a(b) lamp world pair against `expectations.json`
and write `readings.json` beside them (the measured block RUN_13_2A.md's
STEP 2 quotes; no number typed by hand).

    PYTHONPATH=src python examples/events/lamp_shell/read_lamps.py <runs dir>

THE CLICK LINES ALONE ARE READ (the model owner's word of 2026-09-22,
records 562 and 564). Per world the tool opens `events.jsonl`, keeps every
`click` line that carries a `record` (a face's or a screen pixel's or
another lamp's click of a lamp's row), groups them by `number` (the
emitter's measured number, the lamp) and reads per lamp, over the window,
1 + k as the inverse slope of the birth ordinal (`record & 0xFFFFFFFF`)
against the click's tick, series T's reading (`shell_clock/read_runs.py`'s
`slope`, imported); then the shell mean, the plane ring's mean and the
deciding ratio (COMPUTATION on the clicks), each against its pin, PASS or
FAIL; the controls at 1.0000. Nothing is read from the store, from
`state.json` or from the lamps' own records, and no world is replayed.
The host's cost is read from the runner's `summary.json` and reported
apart.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "shell_clock_read_runs", HERE.parent / "shell_clock" / "read_runs.py"
)
assert _SPEC is not None and _SPEC.loader is not None
_READ_RUNS = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_READ_RUNS)
slope = _READ_RUNS.slope


def clicks_by_lamp(run: Path, window: list[int]) -> dict[int, list[tuple[int, int]]]:
    """Per emitter number the (tick, birth ordinal) of every click of its
    rows in the window, in tick order; the one reading of this series."""
    found: dict[int, list[tuple[int, int]]] = {}
    with (run / "events.jsonl").open(encoding="utf-8") as lines:
        for line in lines:
            event = json.loads(line)
            if event.get("event") != "click" or "record" not in event:
                continue
            tick = event["tick"]
            if not window[0] <= tick < window[1]:
                continue
            found.setdefault(int(event["number"]), []).append((tick, event["record"] & 0xFFFFFFFF))
    return {k: sorted(v) for k, v in found.items()}


def births_by_lamp(run: Path, window: list[int]) -> dict[int, list[tuple[int, int]]]:
    """Per lamp the (tick, birth ordinal) of its own `birth` lines in the
    window (the lamp's own record, a detector's own record: DETECTOR),
    read beside the clicks so that the click ticks' jitter (the flight's
    residue at birth, up to one tick) can be told from the clock."""
    found: dict[int, list[tuple[int, int]]] = {}
    with (run / "events.jsonl").open(encoding="utf-8") as lines:
        for line in lines:
            if '"birth"' not in line:
                continue
            event = json.loads(line)
            if event.get("event") != "birth" or "record" not in event:
                continue
            tick = event["tick"]
            if not window[0] <= tick < window[1]:
                continue
            found.setdefault(int(event["measured"]), []).append((tick, event["record"] & 0xFFFFFFFF))
    return {k: sorted(v) for k, v in found.items()}


def lamp_k(points: list[tuple[int, int]]) -> float:
    return 1 / slope([float(t) for t, _ in points], [float(j) for _, j in points]) - 1


def inside(value: float, bracket: list[float]) -> bool:
    return bracket[0] - 1e-12 <= value <= bracket[1] + 1e-12


def main() -> None:
    runs = Path(sys.argv[1])
    expected = json.loads((HERE / "expectations.json").read_text(encoding="utf-8"))
    window = expected["constants"]["window"]
    world_names = list(expected["worlds"])
    mass_name = next(name for name in world_names if "control" not in name)
    control_name = expected["worlds"][mass_name]["control"]
    pins = expected["worlds"][mass_name]
    summary = (
        json.loads((runs / "summary.json").read_text(encoding="utf-8"))
        if (runs / "summary.json").exists()
        else None
    )

    # `format` marks the file as a record, not a world, for the tests that
    # read every JSON under examples/ as a world unless it says otherwise.
    readings: dict[str, object] = {"format": "lamp-shell-readings-v1", "window": window, "worlds": {}}
    mass_clicks = clicks_by_lamp(runs / mass_name / "run", window)
    control_clicks = clicks_by_lamp(runs / control_name / "run", window)
    mass_births = births_by_lamp(runs / mass_name / "run", window)
    lamps = pins["lamps"]
    per_lamp: dict[str, object] = {}
    ks: list[float] = []
    plane: list[float] = []
    lamp_fails = 0
    births_off = 0
    control_fails = 0
    missing = 0
    # The engine numbers the measured events from 1 in the world's list
    # order (a click line's `measured` and `number`); the pins are keyed by
    # the list index, so the lamp of pin i carries the number i + 1.
    for number, pin in lamps.items():
        n = int(number) + 1
        if n not in mass_clicks or n not in control_clicks:
            missing += 1
            per_lamp[number] = {"node": pin["node"], "missing": True}
            continue
        k = lamp_k(mass_clicks[n])
        k_control = lamp_k(control_clicks[n])
        ok = abs(k - pin["k"]["value"]) <= pin["k"]["tolerance"] + 1e-12
        ok_control = abs(k_control) <= 1e-9
        lamp_fails += not ok
        control_fails += not ok_control
        ks.append(k)
        k_births = lamp_k(mass_births[n]) if n in mass_births else None
        births_off += (
            k_births is not None and abs(k_births - pin["k"]["value"]) > pin["k"]["tolerance"] + 1e-12
        )
        if pin["node"][0] == 0:
            plane.append(k)
        per_lamp[number] = {
            "node": pin["node"],
            "clicks": len(mass_clicks[n]),
            "k": k,
            "k_from_own_births": k_births,
            "pinned": pin["k"]["value"],
            "age_moment_pinned": pin["age_moment"]["value"],
            "inside": bool(ok),
            "control_k": k_control,
            "control_inside": bool(ok_control),
        }
    k_shell = sum(ks) / len(ks)
    k_plane = sum(plane) / len(plane)
    ratio = (0.731 / 26) / k_shell
    verdicts = {
        "k_shell": {
            "kind": "COMPUTATION on the DETECTOR readings",
            "value": k_shell,
            "pinned": pins["k_shell"]["value"],
            "bracket": pins["k_shell"]["bracket"],
            "verdict": "PASS" if inside(k_shell, pins["k_shell"]["bracket"]) else "FAIL",
            "lamps": len(ks),
        },
        "k_plane": {
            "kind": "COMPUTATION on the DETECTOR readings",
            "value": k_plane,
            "pinned": pins["k_plane"]["value"],
            "bracket": pins["k_plane"]["bracket"],
            "verdict": "PASS" if inside(k_plane, pins["k_plane"]["bracket"]) else "FAIL",
            "lamps": len(plane),
        },
        "ratio": {
            "kind": "COMPUTATION on two DETECTOR readings",
            "value": ratio,
            "through_lever_arm": ratio / 0.683,
            "pinned": pins["ratio"]["value"],
            "bracket": pins["ratio"]["bracket"],
            "verdict": "PASS" if inside(ratio, pins["ratio"]["bracket"]) else "FAIL",
        },
        "lamps_off_their_pin": {
            "kind": "DETECTOR",
            "count": lamp_fails,
            "of": len(ks),
            "verdict": "PASS" if lamp_fails == 0 else "FAIL",
        },
        "lamps_off_their_pin_by_own_births": {
            "kind": "DETECTOR (the lamp's own record), beside the declared click reading, no pin",
            "count": births_off,
            "of": len(ks),
        },
        "controls_off_1": {
            "kind": "DETECTOR",
            "count": control_fails,
            "of": len(ks),
            "verdict": "PASS" if control_fails == 0 else "FAIL",
        },
        "lamps_missing": missing,
    }
    readings["worlds"][mass_name] = {"verdicts": verdicts, "lamps": per_lamp}
    readings["host"] = {"kind": "HOST", "summary": summary}
    (runs / "readings.json").write_text(json.dumps(readings, indent=1) + "\n", encoding="utf-8")
    print(f"window {window}; lamps read {len(ks)} of {len(lamps)} (missing {missing})")
    for name, v in verdicts.items():
        print(f"  {name}: {json.dumps(v)}")
    worst = max(
        per_lamp.values(), key=lambda r: abs(r.get("k", 0) - r.get("pinned", 0)) if "k" in r else 0
    )
    print(f"  the worst lamp: {json.dumps(worst)}")
    if summary:
        for row in (
            summary if isinstance(summary, list) else summary.get("worlds", summary.get("runs", []))
        ):
            print(f"  HOST: {json.dumps(row)[:400]}")


if __name__ == "__main__":
    main()
