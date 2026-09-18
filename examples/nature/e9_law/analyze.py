"""Read the records of E9 repeated under the law of the bit (docs/EXPERIMENTS.md,
2026-09-18): the three worlds of `make_worlds.py` run through the runner, which
the engine refuses at a corner, and the scan of `scan_fill.py`. A Renderer of
records (Highlights 3.29): it reads `run.json`, `events.jsonl` and `scan.json`
and never the engine. Prints the readings and writes `record.json`.

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
        "ray_slots": electron["ray_slots"],
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
    print("| Ray slots | Fill | Admitted | Failed at tick | Error |")
    print("| ---: | ---: | --- | ---: | --- |")
    for row in record["scan"]["rows"]:
        print(
            f"| {row['ray_slots']} | {row['fill']} | {row['admitted']} | {row['failed_tick']} | {row['error']} |"
        )
    args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print(args.record)


if __name__ == "__main__":
    main()
