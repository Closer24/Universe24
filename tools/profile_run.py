"""A HOST tool: profile a few hundred intervals of registered worlds and
print, per world, the seconds per interval, the live rows per interval,
the Nodes the live rows occupy per interval, the record bytes per interval
(what the runner's `events.jsonl` writer would write, counted and not
written) and the top functions by cumulative time (cProfile).

Nothing here is a reading of any kind: no number of the physics is taken,
compared or registered; the outputs are HOST measurements of the engine's
run and stay out of the register (docs/designs/engine_run/RUN_AUDIT.md,
the owner's order of 2026-09-23, "the system runs smoothly ... no long
runs"). The world files are read as shipped and not written.

    PYTHONPATH=src python tools/profile_run.py [--intervals 300] [--out DIR] WORLD.json ...
"""

from __future__ import annotations

import argparse
import cProfile
import io
import json
import pstats
import re
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.events import NatureBeamSimulation  # noqa: E402
from event_universe.world_loading import load_world  # noqa: E402


def profile_world(path: Path, intervals: int) -> dict[str, object]:
    loaded = load_world(path.read_bytes(), base_dir=path.parent)
    world = loaded.world  # already parsed by the loader
    counter = {"bytes": 0, "lines": 0, "kinds": {}}

    def observer(event: dict[str, object]) -> None:
        # The runner writes json.dumps(event) + "\n" per event line.
        counter["bytes"] += len(json.dumps(event)) + 1
        counter["lines"] += 1
        kind = str(event.get("event", "?"))
        counter["kinds"][kind] = counter["kinds"].get(kind, 0) + 1

    simulation = NatureBeamSimulation(world, observer=observer)
    per_interval: list[dict[str, float]] = []
    profiler = cProfile.Profile()
    ticks = min(intervals, world.ticks) if world.ticks else intervals
    refusal: str | None = None
    for _ in range(ticks):
        before_bytes, before_lines = counter["bytes"], counter["lines"]
        started = time.perf_counter()
        profiler.enable()
        try:
            simulation.step()
        except (OverflowError, ValueError) as error:
            # The law's refusal of the world at this interval (a physics
            # event, recorded here as HOST information only: the interval
            # and the message, nothing read from it).
            profiler.disable()
            refusal = f"refused at interval {simulation.tick}: {error}"
            break
        profiler.disable()
        elapsed = time.perf_counter() - started
        live = sum(int(store.size) for store in simulation.stores)
        nodes = (
            np.concatenate([store.node[: store.size] for store in simulation.stores if store.size])
            if live
            else np.zeros(0, dtype=np.int64)
        )
        occupied = int(np.unique(nodes).size)
        per_interval.append(
            {
                "seconds": elapsed,
                "live_rows": live,
                "nodes_occupied": occupied,
                "record_bytes": counter["bytes"] - before_bytes,
                "record_lines": counter["lines"] - before_lines,
            }
        )
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative").print_stats(12)
    top = [
        line.rstrip().replace(str(ROOT) + "/", "")
        for line in stream.getvalue().splitlines()
        if re.match(r"\s*[\d/]+\s", line)
    ][:10]
    n = max(1, len(per_interval))
    total_nodes = int(np.prod(world.shape))
    summary = {
        "world": str(path.resolve().relative_to(ROOT))
        if path.resolve().is_relative_to(ROOT)
        else str(path),
        "shape": list(world.shape),
        "gameboard_nodes": total_nodes,
        "intervals": len(per_interval),
        "refusal": refusal,
        "seconds_total": sum(p["seconds"] for p in per_interval),
        "seconds_per_interval_mean": sum(p["seconds"] for p in per_interval) / n,
        "seconds_per_interval_last_50": sum(p["seconds"] for p in per_interval[-50:])
        / max(1, len(per_interval[-50:])),
        "live_rows_mean": sum(p["live_rows"] for p in per_interval) / n,
        "live_rows_max": max((p["live_rows"] for p in per_interval), default=0),
        "nodes_occupied_mean": sum(p["nodes_occupied"] for p in per_interval) / n,
        "nodes_occupied_max": max((p["nodes_occupied"] for p in per_interval), default=0),
        "record_bytes_per_interval_mean": sum(p["record_bytes"] for p in per_interval) / n,
        "record_lines_per_interval_mean": sum(p["record_lines"] for p in per_interval) / n,
        "record_kinds": counter["kinds"],
        "top_functions_cumulative": top,
        "per_interval": per_interval,
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("worlds", nargs="+", type=Path)
    parser.add_argument("--intervals", type=int, default=300)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    results = []
    for path in args.worlds:
        summary = profile_world(path, args.intervals)
        results.append(summary)
        print(
            f"HOST {summary['world']}: {summary['intervals']} intervals, "
            f"{summary['seconds_per_interval_mean'] * 1000:.1f} ms per interval (last 50: "
            f"{summary['seconds_per_interval_last_50'] * 1000:.1f} ms), live rows mean {summary['live_rows_mean']:.0f} "
            f"(max {summary['live_rows_max']}), Nodes occupied mean {summary['nodes_occupied_mean']:.0f} "
            f"(max {summary['nodes_occupied_max']}) of {summary['gameboard_nodes']}, record "
            f"{summary['record_bytes_per_interval_mean']:.0f} bytes and {summary['record_lines_per_interval_mean']:.1f} lines per interval; "
            f"kinds {summary['record_kinds']}"
            + (f"; {summary['refusal']}" if summary["refusal"] else "")
        )
        for line in summary["top_functions_cumulative"]:
            print("   ", line)
    if args.out is not None:
        args.out.mkdir(parents=True, exist_ok=True)
        for summary in results:
            name = Path(summary["world"]).stem
            (args.out / f"{name}.json").write_text(
                json.dumps(summary, indent=1) + "\n", encoding="utf-8"
            )
        print(f"HOST written under {args.out}")


if __name__ == "__main__":
    main()
