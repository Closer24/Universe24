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
import resource
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.events import NatureBeamSimulation  # noqa: E402
from event_universe.snapshot_writer import write_snapshot  # noqa: E402
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

    # The whole record, the per-row click lines counted among the kinds.
    simulation = NatureBeamSimulation(world, observer=observer, keep_row_clicks=True)
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


def is_row_click(event: dict[str, object]) -> bool:
    """The measure rule's per-row `click` line (`_apply_plan`): the one kind
    the runner leaves out by default (`--keep-row-clicks` keeps it, PR
    #1026). It carries a
    `reading` and a `push`; the face, border and body click lines carry a
    `momentum` and no `reading`."""
    return event.get("event") == "click" and "reading" in event


def measure_writer(path: Path, intervals: int, mode: str, out: Path) -> dict[str, object]:
    """HOST: the share of a run's wall time spent writing its record, the
    runner's own loop replicated (`run.py`: a record line per event into
    `events.jsonl` through a 1 MiB buffer, the books per interval kept for
    the audit, `state.json` streamed and `run.json` dumped at the end).
    `mode` is "on" (every line, the record under `--keep-row-clicks`), "off"
    (the per-row click lines dropped by this tool's own guard, the runner's
    default) or "memory"
    (every line held in memory and written once at the end). The files go
    under `out` and are deleted after the measurement; no reading is taken."""
    loaded = load_world(path.read_bytes(), base_dir=path.parent)
    world = loaded.world
    folder = out / f"{path.stem}_{mode}"
    folder.mkdir(parents=True, exist_ok=True)
    timing = {"dumps": 0.0, "write": 0.0, "books": 0.0, "flush": 0.0, "state": 0.0, "run_json": 0.0}
    counts = {"lines": 0, "bytes": 0, "dropped": 0}
    held: list[str] = []
    stream = (folder / "events.jsonl").open("w", encoding="utf-8", buffering=1 << 20)

    def record(event: dict[str, object]) -> None:
        if mode == "off" and is_row_click(event):
            counts["dropped"] += 1
            return
        t0 = time.perf_counter()
        line = json.dumps(event) + "\n"
        t1 = time.perf_counter()
        timing["dumps"] += t1 - t0
        counts["lines"] += 1
        counts["bytes"] += len(line)
        if mode == "memory":
            held.append(line)
        else:
            stream.write(line)
            timing["write"] += time.perf_counter() - t1

    # Every line reaches `record`; `mode` alone decides what is dropped.
    simulation = NatureBeamSimulation(world, observer=record, keep_row_clicks=True)
    audit: list[dict[str, object]] = []
    refusal: str | None = None
    ticks = min(intervals, world.ticks) if world.ticks else intervals
    started = time.perf_counter()
    done = 0
    for _ in range(ticks):
        try:
            simulation.step()
        except (OverflowError, ValueError) as error:
            refusal = f"refused at interval {simulation.tick}: {error}"
            break
        t0 = time.perf_counter()
        audit.append(simulation.books())
        timing["books"] += time.perf_counter() - t0
        done += 1
    compute_end = time.perf_counter()
    t0 = time.perf_counter()
    if mode == "memory":
        stream.write("".join(held))
    stream.close()
    timing["flush"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    with (folder / "state.json").open("w", encoding="utf-8") as state_stream:
        write_snapshot(simulation, state_stream)
        state_stream.write("\n")
    timing["state"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    metadata: dict[str, object] = {"audit": audit, "intervals": done}
    layer = getattr(simulation, "layer", None)
    if layer is not None:
        metadata["layer"] = layer.report()
        metadata["gathers"] = getattr(layer, "gathers", [])
    (folder / "run.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    timing["run_json"] = time.perf_counter() - t0
    total = time.perf_counter() - started
    sizes = {name: (folder / name).stat().st_size for name in ("events.jsonl", "state.json", "run.json")}
    for name in sizes:
        (folder / name).unlink()
    folder.rmdir()
    writing = timing["dumps"] + timing["write"] + timing["flush"] + timing["state"] + timing["run_json"]
    live = sum(int(store.size) for store in simulation.stores)
    return {
        "world": str(path),
        "mode": mode,
        "intervals": done,
        "refusal": refusal,
        "seconds_total": total,
        "seconds_compute": compute_end - started - timing["dumps"] - timing["write"] - timing["books"],
        "seconds_books": timing["books"],
        "seconds_dumps": timing["dumps"],
        "seconds_write": timing["write"],
        "seconds_flush_end": timing["flush"],
        "seconds_state": timing["state"],
        "seconds_run_json": timing["run_json"],
        "seconds_writing_all": writing,
        "share_writing": writing / total if total else 0.0,
        "share_dumps": timing["dumps"] / total if total else 0.0,
        "share_write_calls": timing["write"] / total if total else 0.0,
        "lines": counts["lines"],
        "lines_dropped": counts["dropped"],
        "bytes_events": counts["bytes"],
        "bytes_per_interval": counts["bytes"] / max(1, done),
        "held_bytes_memory_mode": sum(len(line) for line in held),
        "sizes": sizes,
        "live_rows_end": live,
        "peak_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0,
    }


def print_writer(r: dict[str, object]) -> None:
    print(
        f"HOST writer {r['world']} mode={r['mode']}: {r['intervals']} intervals, total {r['seconds_total']:.1f} s; "
        f"compute {r['seconds_compute']:.1f} s, books {r['seconds_books']:.2f} s, json.dumps {r['seconds_dumps']:.2f} s, "
        f"stream.write {r['seconds_write']:.2f} s, end flush {r['seconds_flush_end']:.2f} s, state.json {r['seconds_state']:.2f} s, "
        f"run.json {r['seconds_run_json']:.2f} s; writing all {r['seconds_writing_all']:.2f} s = {100 * r['share_writing']:.1f} percent "
        f"(dumps {100 * r['share_dumps']:.1f}, write calls {100 * r['share_write_calls']:.1f}); lines {r['lines']} (dropped {r['lines_dropped']}), "
        f"events.jsonl {r['sizes']['events.jsonl']} bytes ({r['bytes_per_interval']:.0f} per interval), state.json {r['sizes']['state.json']}, "
        f"run.json {r['sizes']['run.json']}; held in memory {r['held_bytes_memory_mode']} bytes; live rows at the end {r['live_rows_end']}; "
        f"peak RSS {r['peak_rss_mb']:.0f} MB" + (f"; {r['refusal']}" if r["refusal"] else "")
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("worlds", nargs="+", type=Path)
    parser.add_argument("--intervals", type=int, default=300)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument(
        "--writer",
        choices=["on", "off", "memory"],
        default=None,
        help="HOST: measure the record writer's share of the wall time in this mode instead of profiling",
    )
    args = parser.parse_args()
    if args.writer is not None:
        out = args.out if args.out is not None else Path("artifacts") / "profile_run"
        for path in args.worlds:
            print_writer(measure_writer(path, args.intervals, args.writer, out))
        return
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
