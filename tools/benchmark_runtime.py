"""Paired host timings with identical physical inputs, events and HTML sampling.

Run from a candidate checkout, passing a separate immutable baseline worktree.
Every sample uses a fresh process and the existing HTML generator. Timings do
not include imports or post-run equality hashing. No timing threshold is a test.
"""

import argparse
import hashlib
import json
import os
import platform
import statistics
import subprocess
import sys
import time
from pathlib import Path

CASES = {
    "sparse_trail": ("moving_source.json", 800, 20),
    "outward_field": ("moving_source.json", 20, 2),
    "finite_field": ("finite_fields.json", 40, 4),
    "ray_field": ("isotropic_rays.json", 24, 2),
    "shared_clock": ("finite_fields.json", 20, 2),
    "quantum_contact": ("quantum/repeated_contacts.json", 48, 4),
}
PHYSICAL_KEYS = (
    "model",
    "schema_version",
    "boundary",
    "status",
    "error",
    "requested_ticks",
    "completed_ticks",
    "tick",
    "initial_totals",
    "final_totals",
    "local_conservation",
    "source_totals",
    "conserved_at_every_completed_tick",
    "dissipation_totals",
    "localized_totals",
    "escaped_totals",
    "accounting_balanced_at_every_completed_tick",
    "fields",
    "disturbance_types",
    "shape",
    "link_ticks",
    "computation",
    "spatial_accounting",
)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def worker(repo, initialization, output, stride, workers):
    sys.path.insert(0, str(repo / "src"))
    from event_universe import __file__ as source_file
    from event_universe.core.disturbance_engine import DisturbanceEngine
    from event_universe.diagnostics import disturbance_render
    from event_universe.runner import run_initialization, source_fingerprint

    if not Path(source_file).resolve().is_relative_to((repo / "src").resolve()):
        raise RuntimeError("the worker imported a different checkout")
    identity = source_fingerprint()
    stepping = 0.0
    rendering = 0.0
    frames_seen = []
    original_step = DisturbanceEngine.step
    original_render = disturbance_render.render_disturbances

    def measured_step(world):
        nonlocal stepping
        started = time.perf_counter()
        try:
            return original_step(world)
        finally:
            stepping += time.perf_counter() - started

    def measured_render(frames, *args, **kwargs):
        nonlocal rendering
        frames_seen.append(frames)
        started = time.perf_counter()
        try:
            return original_render(frames, *args, **kwargs)
        finally:
            rendering += time.perf_counter() - started

    DisturbanceEngine.step = measured_step
    disturbance_render.render_disturbances = measured_render
    started = time.perf_counter()
    run_initialization(initialization, output, visualize=True, frame_stride=stride, node_workers=workers)
    elapsed = time.perf_counter() - started
    if identity != source_fingerprint():
        raise RuntimeError("source changed during a measurement")
    metadata = json.loads((output / "run.json").read_text())
    if metadata["status"] != "completed" or not metadata["accounting_balanced_at_every_completed_tick"]:
        raise RuntimeError("a benchmark must complete and retain every accounting check")
    result = {
        "total_seconds": elapsed,
        "step_seconds": stepping,
        "render_seconds": rendering,
        "runner_elapsed_seconds": metadata["elapsed_seconds"],
        "source_sha256": identity,
        "initialization_sha256": metadata["initialization_sha256"],
        "state_sha256": hashlib.sha256((output / "state.json").read_bytes()).hexdigest(),
        "events_sha256": hashlib.sha256((output / "events.jsonl").read_bytes()).hexdigest(),
        "sampled_frames_sha256": digest(frames_seen),
        "physical_metadata_sha256": digest({k: metadata[k] for k in PHYSICAL_KEYS if k in metadata}),
        "execution": metadata["execution"],
        "html": str(output / "run.html"),
        "python": sys.version,
    }
    (output / "timing.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


def inputs(baseline, destination, cases):
    destination.mkdir(parents=True, exist_ok=True)
    paths = {}
    for case in cases:
        source, ticks, _stride = CASES[case]
        raw = json.loads((baseline / "examples" / source).read_text())
        raw["ticks"] = ticks
        if case == "sparse_trail":
            raw.pop("spatial_fields")
            raw.pop("emissions")
            raw["shape"] = [1001, 3, 3]
            raw["seeds"][0]["position"] = [0, 1, 1]
        if case == "shared_clock":
            raw["spatial_computation_delay"] = True
        path = destination / f"{case}.json"
        path.write_text(json.dumps(raw, indent=2) + "\n")
        paths[case] = path
    return paths


def benchmark(args):
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError("use a new output directory")
    output.mkdir(parents=True, exist_ok=True)
    repositories = {"baseline": args.baseline.resolve(), "candidate": args.candidate.resolve()}
    cases = list(CASES) if not args.cases else args.cases
    paths = inputs(repositories["baseline"], output / "inputs", cases)
    script = Path(__file__).resolve()
    results = {case: {name: [] for name in repositories} for case in cases}
    witnesses = {}
    # One warmup pair is excluded. Alternate which checkout runs first.
    for sample in range(args.repeats + 1):
        for case in cases:
            names = ("baseline", "candidate") if sample % 2 == 0 else ("candidate", "baseline")
            for name in names:
                repo = repositories[name]
                run = output / "runs" / case / f"{name}-{sample}"
                env = os.environ.copy()
                env["PYTHONPATH"] = str(repo / "src")
                process = subprocess.run(
                    [
                        sys.executable,
                        str(script),
                        "--worker",
                        "--repo",
                        str(repo),
                        "--initialization",
                        str(paths[case]),
                        "--output",
                        str(run),
                        "--stride",
                        str(CASES[case][2]),
                        "--node-workers",
                        str(args.node_workers),
                    ],
                    cwd=repo,
                    env=env,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                value = json.loads(process.stdout)
                signature = tuple(
                    value[key]
                    for key in (
                        "initialization_sha256",
                        "state_sha256",
                        "events_sha256",
                        "sampled_frames_sha256",
                        "physical_metadata_sha256",
                    )
                )
                if case in witnesses and witnesses[case] != signature:
                    raise RuntimeError(f"physical output changed: {case}/{name}/{sample}")
                witnesses[case] = signature
                if sample:
                    results[case][name].append(value)
                print(
                    f"{case} {name} {sample}: {value['total_seconds']:.6f}s; exact output agrees",
                    flush=True,
                )
                (output / "samples.json").write_text(json.dumps(results, indent=2) + "\n")
    summary = {}
    for case, versions in results.items():
        before = statistics.median(v["total_seconds"] for v in versions["baseline"])
        after = statistics.median(v["total_seconds"] for v in versions["candidate"])
        summary[case] = {
            "baseline_median_seconds": before,
            "candidate_median_seconds": after,
            "seconds_saved": before - after,
            "percent_saved": 100 * (1 - after / before),
            "speedup": before / after,
            "equal_physical_outputs": True,
            "baseline_range_seconds": [
                min(v["total_seconds"] for v in versions["baseline"]),
                max(v["total_seconds"] for v in versions["baseline"]),
            ],
            "candidate_range_seconds": [
                min(v["total_seconds"] for v in versions["candidate"]),
                max(v["total_seconds"] for v in versions["candidate"]),
            ],
            "ticks": CASES[case][1],
            "frame_stride": CASES[case][2],
        }
    report = {
        "python": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "node_workers": args.node_workers,
        "repeats": args.repeats,
        "warmup_pairs": 1,
        "timing_scope": "after imports: initialization, stepping, all audits, event writing, snapshots, HTML",
        "summary": summary,
        "samples": results,
    }
    (output / "benchmark.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--cases", nargs="+", choices=CASES)
    parser.add_argument("--node-workers", type=int, default=1)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--initialization", type=Path)
    parser.add_argument("--stride", type=int, default=1)
    args = parser.parse_args()
    if args.worker:
        if args.repo is None or args.initialization is None:
            parser.error("worker requires repo and initialization")
        worker(
            args.repo.resolve(),
            args.initialization.resolve(),
            args.output.resolve(),
            args.stride,
            args.node_workers,
        )
    else:
        if args.baseline is None or args.candidate is None or args.repeats < 1:
            parser.error("baseline, candidate and a positive repeat count are required")
        benchmark(args)


if __name__ == "__main__":
    main()
