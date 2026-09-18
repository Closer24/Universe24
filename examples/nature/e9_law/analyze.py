"""Read the records of E9 repeated under the law of the bit (docs/EXPERIMENTS.md,
2026-09-18): the three worlds of `make_worlds.py` run through the runner, the
screen's marks replayed by `../a1_law/record_screen.py` (`screen.json`, when
present: the shadows each mark turned back per tick, the push J at its Node,
the phases), and the scan of `scan_fill.py`. A Renderer of records (Highlights
3.29): it reads `run.json`, `events.jsonl`, `screen.json` and `scan.json` and
never the engine. Prints the readings and writes `record.json`.

Run:  python examples/nature/e9_law/analyze.py RUNS_DIR [--scan scan.json] [--record record.json]
where RUNS_DIR holds one directory per world (`tools/run_series.py`'s layout,
`<name>/run/run.json`).
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORLDS = ("ring_screen", "ring_screen_clock", "ring_screen_clock_fill1")


def components(value):
    return [value] if isinstance(value, int) else list(value)


def ledger_line(entry: dict, family: str) -> dict:
    line = entry["fields"][family]
    return {key: (components(v) if key != "balanced" else v) for key, v in line.items()}


def analyze(directory: Path) -> dict:
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    world = json.loads((directory / "initialization.json").read_text(encoding="utf-8"))
    events = [
        json.loads(line)
        for line in (directory / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    kinds = Counter(event["event"] for event in events)
    clicks = [e for e in events if e["event"] == "detector_click"]
    audit = metadata.get("audit", [])
    last = audit[-1] if audit else None
    marks = metadata.get("detector_marks", [])
    (electron,) = [f for f in world["spatial_fields"]]
    return {
        "model": metadata["model"],
        "status": metadata["status"],
        "error": metadata.get("error"),
        "requested_ticks": metadata["requested_ticks"],
        "completed_ticks": metadata["completed_ticks"],
        "elapsed_seconds": round(float(metadata["elapsed_seconds"]), 2),
        "source_sha256": metadata["source_sha256"],
        "initialization_sha256": metadata["initialization_sha256"],
        "dense_field": metadata.get("dense_field"),
        "K": metadata.get("K"),
        "phase_width": int(world.get("N", 1 << int(electron.get("phase_bits", 6)))),
        "clock": bool(electron.get("clock")),
        "fill": world["initial_field"]["electron"]["fill"],
        "ring_amount": world["emissions"][0]["amount"],
        "owners": metadata["shadow_families"][0]["owners"],
        "initial_totals": metadata["initial_totals"],
        "final_totals": metadata["final_totals"],
        "escaped_totals": metadata["escaped_totals"],
        "real_content": metadata.get("real_content"),
        "shadow_content": metadata.get("shadow_content"),
        "conserved_at_every_completed_tick": metadata["conserved_at_every_completed_tick"],
        "real_conserved": metadata.get("real_conserved"),
        "ledger_last": None
        if last is None
        else {
            "tick": last["tick"],
            "electron": ledger_line(last, "electron"),
            "momentum": ledger_line(last, "momentum"),
            "real": last.get("real"),
            "shadow": last.get("shadow"),
        },
        "events": dict(sorted(kinds.items())),
        "clicks": len(clicks),
        "marks": [
            {"position": m["position"], "real": m["resident"]["real"], "shadow": m["resident"]["shadow"]}
            for m in marks
        ],
        "screen": screen_reading(directory),
    }


def extrema(profile: list[int], ys: list[int]) -> dict:
    maxima = [
        (ys[i], profile[i])
        for i in range(1, len(profile) - 1)
        if profile[i] > profile[i - 1] and profile[i] >= profile[i + 1]
    ]
    minima = [
        (ys[i], profile[i])
        for i in range(1, len(profile) - 1)
        if profile[i] < profile[i - 1] and profile[i] <= profile[i + 1]
    ]
    return {"maxima": maxima, "minima": minima}


def screen_reading(directory: Path) -> dict | None:
    """What the screen's marks turned back, from the Recorder's replay."""
    path = directory / "screen.json"
    if not path.exists():
        return None
    screen = json.loads(path.read_text(encoding="utf-8"))
    ticks = screen["ticks"]
    positions = [tuple(p) for p in screen["screen"]]
    ys = [p[1] for p in positions]
    n, j = screen["n"], screen["j"]
    returned = [sum(n[t][k] for t in range(1, ticks + 1)) for k in range(len(positions))]
    push = [
        [sum(j[t][k][axis] for t in range(1, ticks + 1)) for axis in range(3)]
        for k in range(len(positions))
    ]
    push_x = [p[0] for p in push]
    phases: Counter[str] = Counter()
    for row in screen["phases"]:
        phases.update(row)
    per_tick = [sum(n[t]) for t in range(ticks + 1)]
    return {
        "ticks": ticks,
        "marks": [list(p) for p in positions],
        "y": ys,
        "returned": returned,
        "peak": [max(n[t][k] for t in range(1, ticks + 1)) for k in range(len(positions))],
        "first_arrival": [
            next((t for t in range(1, ticks + 1) if n[t][k]), None) for k in range(len(positions))
        ],
        "push": push,
        "push_x": push_x,
        "peak_push_x": [
            max((j[t][k][0] for t in range(1, ticks + 1)), key=abs) for k in range(len(positions))
        ],
        "returned_per_tick_peak": (max(per_tick), per_tick.index(max(per_tick))),
        "returned_total": sum(returned),
        "phases": dict(sorted(phases.items(), key=lambda kv: int(kv[0]))),
        "things_resident": sum(sum(row) for row in screen["things_resident"]),
        "wall_returned_total": sum(screen["wall_returned"]),
        "wall_returned_peak": max(screen["wall_returned"]),
        "probes": {
            key: {"peak": max(row), "peak_tick": row.index(max(row)), "last": row[-1]}
            for key, row in screen["probes"].items()
        },
        "extrema_returned": extrema(returned, ys),
        "extrema_push": extrema(push_x, ys),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", type=Path)
    parser.add_argument("--scan", type=Path, default=HERE / "scan.json")
    parser.add_argument("--record", type=Path, default=HERE / "record.json")
    args = parser.parse_args()
    record = {"worlds": {}, "scan": json.loads(args.scan.read_text(encoding="utf-8"))}
    for name in WORLDS:
        directory = args.runs / name / "run"
        if (directory / "run.json").exists():
            record["worlds"][name] = analyze(directory)
    print("| World | Fill | Clock | Status | Completed ticks | Error | Shadows at the start | Clicks |")
    print("| --- | ---: | --- | --- | ---: | --- | ---: | ---: |")
    for name, row in record["worlds"].items():
        print(
            f"| {name} | {row['fill']} | {row['clock']} | {row['status']} | {row['completed_ticks']} "
            f"| {row['error']} | {row['initial_totals']['electron'][0]} | {row['clicks']} |"
        )
    print()
    print("| Fill | Admitted | Shadows at the start | Completed ticks | Failed at tick | Error |")
    print("| ---: | --- | ---: | ---: | ---: | --- |")
    for row in record["scan"]["rows"]:
        print(
            f"| {row['fill']} | {row['admitted']} | {row.get('initial_shadows')} | {row.get('completed_ticks')} "
            f"| {row['failed_tick']} | {row['error']} |"
        )
    for name, row in record["worlds"].items():
        screen = row["screen"]
        if screen is None:
            continue
        print(f"\n## {name}: the screen (replayed)")
        print(
            f"returned {screen['returned_total']} quanta over {screen['ticks']} ticks (peak per tick "
            f"{screen['returned_per_tick_peak']}); phases {screen['phases']}; things resident "
            f"{screen['things_resident']}; the wall returned {screen['wall_returned_total']} "
            f"(peak {screen['wall_returned_peak']}); probes {screen['probes']}"
        )
        print(f"extrema of the returned amount {screen['extrema_returned']}; of the push {screen['extrema_push']}")
        print("| mark | returned | peak | first | J (x, y, z) | peak J_x |")
        print("| --- | ---: | ---: | ---: | --- | ---: |")
        for k, mark in enumerate(screen["marks"]):
            print(
                f"| {tuple(mark)} | {screen['returned'][k]} | {screen['peak'][k]} | {screen['first_arrival'][k]} "
                f"| {tuple(screen['push'][k])} | {screen['peak_push_x'][k]} |"
            )
    args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print(args.record)


if __name__ == "__main__":
    main()
