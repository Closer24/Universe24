"""Read the runs of series X, Poisson after a detector, against
`expectations.json` and write `readings.json` beside them (the measured
block the register's entry quotes; no number typed by hand).

    PYTHONPATH=src python examples/events/shell_clock/read_runs.py <runs dir>

THE CLICK LINES ALONE ARE READ (the model owner's word of 2026-09-22,
records 562 and 564: no experiment reads the GameBoard, only after a
detector; a GameBoard reading serves diagnostics and bug fixing alone).
Per world the tool opens `events.jsonl`, keeps the `click` lines of the
detector (measured event 1, the one entity that detects here) and reads
from them alone: in each window 1 + z, the inverse slope of the birth
ordinal (`record & 0xFFFFFFFF`) against the click's tick, series T's
reading; the click rate; the age the click carries (the flight); and over
the whole run whether any ordinal is missing (the light escaping whole).
The lamp's count k is 1 + z - 1, and the three pinned ratios of k follow
from the worlds' readings. Nothing is read from the store, from
`state.json`, from the lamp's own record or from the shell's sources, and
no world is replayed.

The verdict per world is one of three: `met` (1 + z inside the pin's
bracket in both windows), `moved` (outside it but within three brackets)
and `failed` (otherwise); per ratio, `met` when the reading is within the
register's `ratio_tolerance` of the map's pin. The host's cost is read from
the runner's `summary.json` and reported apart from the readings.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DETECTOR = 1


def slope(xs: list[float], ys: list[float]) -> float:
    """The least-squares slope of ys against xs (series T's reading)."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    return sxy / sxx


def clicks_of(run: Path) -> list[tuple[int, int, int]]:
    """The detector's click lines of one run: (the tick, the birth ordinal,
    the age the click carries), in tick order. The one reading of this
    series; no other line of the record is opened."""
    found = []
    with (run / "events.jsonl").open(encoding="utf-8") as lines:
        for line in lines:
            event = json.loads(line)
            if event.get("event") == "click" and event.get("measured") == DETECTOR:
                if "record" in event:
                    found.append((event["tick"], event["record"] & 0xFFFFFFFF, event["age"]))
    return sorted(found)


def read_world(runs: Path, name: str, pinned: dict, expected: dict) -> dict[str, object]:
    """One world's reading: the windows, the count k and the verdict."""
    clicks = clicks_of(runs / name / "run")
    windows: dict[str, object] = {}
    inside = True
    low, high = pinned["k_bracket"]
    for lo, hi in expected["windows"]:
        selected = [c for c in clicks if lo <= c[0] < hi]
        one_plus_z = 1 / slope([float(c[0]) for c in selected], [float(c[1]) for c in selected])
        k = one_plus_z - 1
        ok = low - 1e-9 <= k <= high + 1e-9
        inside = inside and ok
        windows[f"{lo}-{hi}"] = {
            "one_plus_z": one_plus_z,
            "k": k,
            "inside": bool(ok),
            "clicks_per_interval": len(selected) / (hi - lo),
            "age_read": [selected[0][2], selected[-1][2]],
            "clicks": len(selected),
        }
    ordinals = [c[1] for c in clicks]
    read_k = sum(w["k"] for w in windows.values()) / len(windows)
    span = max(high - pinned["k"], pinned["k"] - low, 1e-6)
    worst = max(abs(w["k"] - pinned["k"]) for w in windows.values())
    verdict = "met" if inside else ("moved" if worst <= 3 * span else "failed")
    return {
        "kind": "DETECTOR",
        "word": pinned["word"],
        "radius": pinned["radius"],
        "inside_the_shell": pinned["inside"],
        "windows": windows,
        "k": read_k,
        "one_plus_z": 1 + read_k,
        "pinned_k": pinned["k"],
        "clicks": len(clicks),
        "ordinals_missing": (max(ordinals) - len(ordinals)) if ordinals else None,
        "verdict": verdict,
    }


def main() -> None:
    runs = Path(sys.argv[1])
    expected = json.loads((HERE / "expectations.json").read_text(encoding="utf-8"))
    summary = json.loads((runs / "summary.json").read_text(encoding="utf-8"))
    readings: dict[str, object] = {
        "format": "shell-clock-readings-v1",
        "kind": "DETECTOR",
        "read_from": (
            "the click lines of the detector in events.jsonl alone (the owner's word of "
            "2026-09-22, records 562 and 564); no store, no state.json, no replay"
        ),
        "worlds": {},
        "ratios": {},
    }
    for name, pinned in expected["worlds"].items():
        reading = read_world(runs, name, pinned, expected)
        readings["worlds"][name] = reading
        print(
            f"{name} (the {pinned['word'] or 'control'} word, r = {pinned['radius']}, "
            f"{'inside' if pinned['inside'] else 'outside'}): DETECTOR 1 + z "
            + ", ".join(f"{w['one_plus_z']:.4f}" for w in reading["windows"].values())
            + f" (pinned {pinned['one_plus_z']:.4f}, k in "
            f"[{pinned['k_bracket'][0]:.4f}, {pinned['k_bracket'][1]:.4f}]); k read "
            f"{reading['k']:.4f}; rate "
            + ", ".join(f"{w['clicks_per_interval']:.3f}" for w in reading["windows"].values())
            + f"; age {reading['windows'][next(iter(reading['windows']))]['age_read'][0]}; "
            f"clicks {reading['clicks']}; ordinals missing {reading['ordinals_missing']}; "
            f"verdict {reading['verdict'].upper()}"
        )
    k = {name: readings["worlds"][name]["k"] for name in expected["worlds"]}
    read_ratios = {
        "inside_age": k["age_2"] / k["age_4"],
        "inside_presence": k["presence_2"] / k["presence_4"],
        "outside_age": k["age_12"] / k["age_4"],
    }
    tolerance = expected["ratio_tolerance"]
    for key, value in read_ratios.items():
        pin = expected["ratios"][key]
        met = abs(value - pin["pinned"]) <= tolerance
        flat = abs(value - 1.0) <= tolerance
        readings["ratios"][key] = {
            "kind": "DETECTOR",
            "reading": pin["reading"],
            "read": value,
            "pinned": pin["pinned"],
            "continuum": pin["continuum"],
            "tolerance": tolerance,
            "met": bool(met),
            "flat": bool(flat),
        }
        print(
            f"{key}: DETECTOR {value:.4f} (pinned {pin['pinned']:.6f} +- {tolerance}, the continuum "
            f"{pin['continuum']}): the pin {'MET' if met else 'MISSED'}; flat within the tolerance: "
            f"{'YES' if flat else 'NO'}"
        )
    host = {
        row["world"]: {
            "runner_seconds": row["runner_seconds"],
            "wall_seconds": row["wall_seconds"],
            "peak_rss_mb": row["peak_rss_mb"],
            "events_sha256": row["events_sha256"],
            "state_sha256": row["state_sha256"],
        }
        for row in summary
    }
    readings["host"] = host
    print("host cost (GAMEBOARD, apart from the readings):", json.dumps(host))
    (runs / "readings.json").write_text(json.dumps(readings, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
