"""Read the runs of series S, the clock's word, against `expectations.json`
and write `readings.json` beside them (the measured block the register's
entry quotes; no number typed by hand).

    PYTHONPATH=src python examples/events/clock_word/read_runs.py <runs dir>

Per world: DETECTOR, the lamp's light at x = 110: 1 + z the inverse slope
of the birth ordinal (`record & 0xFFFFFFFF`) against the click's tick in
each window, the click rate, the age read, the escape (every ordinal up to
the last click arrived); the lamp's clock from its `birth` lines (the count
it owes per self-creation, k = intervals per birth - 1 in the intervals
whose light the window sees, and the first birth it misses after the crowd's
rows arrive); GAMEBOARD, a replay of the world's first twenty intervals on
the engine: the first interval at which the lamp's clock counts and the
count then and in the steady state. The verdict per world is one of three:
`met` (the detector's 1 + z inside the pin's tolerance in both windows),
`moved` (outside it, within five tolerances, the order of the four worlds
as pinned), `failed` (otherwise). The host's cost is read from the runner's
`summary.json` and reported apart from the readings.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.events import NatureBeamSimulation  # noqa: E402
from event_universe.world_loading import load_world  # noqa: E402

DETECTOR, LAMP = 1, 2


def slope(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    return sxy / sxx


def replay_first_count(path: Path, intervals: int = 20) -> dict[str, object]:
    """GAMEBOARD: the lamp's clock count per interval on a replay."""
    loaded = load_world(path.read_bytes(), base_dir=path.parent, root=path.parents[1])
    sim = NatureBeamSimulation(loaded.world)
    counts = []
    for _ in range(intervals):
        sim.step()
        counts.append(int(sim.measured[LAMP].counted))
    first = next((t + 1 for t, c in enumerate(counts) if c), None)
    return {
        "kind": "GAMEBOARD",
        "first_counting_tick": first,
        "count_at_first_tick": counts[first - 1] if first else None,
        "steady_count": counts[-1],
        "presence_at_the_end": int(sim.measured[LAMP].presence),
    }


def read_world(runs: Path, name: str, pinned: dict, expected: dict) -> dict[str, object]:
    run = runs / name / "run"
    events = [json.loads(line) for line in (run / "events.jsonl").open(encoding="utf-8")]
    births = sorted(e["tick"] for e in events if e["event"] == "birth" and e.get("measured") == LAMP)
    clicks = sorted(
        (e["tick"], e["record"] & 0xFFFFFFFF, e["age"])
        for e in events
        if e["event"] == "click" and e.get("measured") == DETECTOR and "record" in e
    )
    flight = pinned["flight"]
    windows: dict[str, object] = {}
    inside = True
    for lo, hi in expected["windows"]:
        sel = [c for c in clicks if lo <= c[0] < hi]
        z = 1 / slope([float(c[0]) for c in sel], [float(c[1]) for c in sel])
        own = [b for b in births if lo - flight <= b < hi - flight]
        k_read = (hi - lo) / len(own) - 1
        ok = abs(z - pinned["one_plus_z"]) <= pinned["tolerance"]
        inside = inside and ok
        windows[f"{lo}-{hi}"] = {
            "one_plus_z": z,
            "inside": bool(ok),
            "clicks_per_interval": len(sel) / (hi - lo),
            "age_read": [sel[0][2], sel[-1][2]],
            "lamp_k_read": k_read,
            "clicks": len(sel),
        }
    ordinals = [c[1] for c in clicks]
    first_row = pinned["first_row_tick"]
    missing = [t for t in range(first_row, first_row + 40) if t not in births]
    worst = max(abs(w["one_plus_z"] - pinned["one_plus_z"]) for w in windows.values())
    verdict = "met" if inside else ("moved" if worst <= 5 * pinned["tolerance"] else "failed")
    return {
        "kind": "DETECTOR",
        "windows": windows,
        "births": len(births),
        "clicks": len(clicks),
        "ordinals_missing": (max(ordinals) - len(ordinals)) if ordinals else None,
        "first_missing_birth_after_the_rows": missing[0] if missing else None,
        "replay": replay_first_count(HERE / f"{name}.json"),
        "verdict": verdict,
    }


def main() -> None:
    runs = Path(sys.argv[1])
    expected = json.loads((HERE / "expectations.json").read_text(encoding="utf-8"))
    summary = json.loads((runs / "summary.json").read_text(encoding="utf-8"))
    readings: dict[str, object] = {"format": "clock-word-readings-v1", "worlds": {}, "ratios": {}}
    for name, pinned in expected["worlds"].items():
        r = read_world(runs, name, pinned, expected)
        readings["worlds"][name] = r
        z = [w["one_plus_z"] for w in r["windows"].values()]
        print(
            f"{name} ({pinned['word']} word, {pinned['distance']} Links): DETECTOR 1 + z "
            + ", ".join(f"{v:.4f}" for v in z)
            + f" (pinned {pinned['one_plus_z']:.3f} +- {pinned['tolerance']}); rate "
            + ", ".join(f"{w['clicks_per_interval']:.3f}" for w in r["windows"].values())
            + f"; age {r['windows'][list(r['windows'])[0]]['age_read'][0]}; lamp k read "
            + ", ".join(f"{w['lamp_k_read']:.3f}" for w in r["windows"].values())
            + f"; ordinals missing {r['ordinals_missing']}; first birth missed after the rows: tick "
            f"{r['first_missing_birth_after_the_rows']}; GAMEBOARD replay: the clock counts from tick "
            f"{r['replay']['first_counting_tick']} ({r['replay']['count_at_first_tick']}, then "
            f"{r['replay']['steady_count']} = {r['replay']['steady_count'] / expected['flux']:.0f} F; "
            f"pinned tick {pinned['first_row_tick']}, {pinned['counted']}); verdict {r['verdict'].upper()}"
        )
    for word in ("presence", "age"):
        k = {}
        for name, pinned in expected["worlds"].items():
            if pinned["word"] == word:
                w = readings["worlds"][name]["windows"]
                k[pinned["distance"]] = sum(v["one_plus_z"] - 1 for v in w.values()) / len(w)
        ratio = k[6] / k[3]
        pin = expected["ratios"][word]["k_6_over_k_3"]
        readings["ratios"][word] = {
            "k_3": k[3],
            "k_6": k[6],
            "k_6_over_k_3": ratio,
            "pinned": pin,
            "inside": bool(abs(ratio - pin) <= expected["ratio_tolerance"]),
        }
        print(
            f"the {word} word: k at 3 {k[3]:.4f}, at 6 {k[6]:.4f}, the ratio {ratio:.3f} (pinned {pin:.3f} +- {expected['ratio_tolerance']}, {'inside' if readings['ratios'][word]['inside'] else 'OUTSIDE'})"
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
    print("host cost (apart from the readings):", json.dumps(host))
    (runs / "readings.json").write_text(json.dumps(readings, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
