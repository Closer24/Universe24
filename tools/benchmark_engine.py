"""Measure host stepping and audited headless runs with exact physical trace digests."""

import argparse
import hashlib
import json
import os
import statistics
import sys
import time
from dataclasses import asdict
from pathlib import Path

import event_universe
from event_universe import Simulation
from event_universe.initialization import parse_initial_json
from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization, source_fingerprint


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def physical_state(world):
    """Include frozen proposals and carried fractions; exclude derived host indices."""
    result = {
        "tick": world.tick,
        "faulted": world.faulted,
        "cells": [(p, asdict(c)) for p, c in sorted(world._cells.items())],
        "links": [
            (p, [None if v is None else asdict(v) for v in slots]) for p, slots in world._links.items()
        ],
        "sources": world.source_totals(),
        "escaped": world.escaped_totals(),
        "dissipation": world.dissipation_totals(),
        "computation": world.computation_report(),
    }
    if world._spatial is not None:
        spatial = world._spatial
        result["spatial"] = {
            "cells": [(p, asdict(c)) for p, c in sorted(spatial.cells.items())],
            "links": [
                (p, [None if v is None else asdict(v) for v in slots])
                for p, slots in spatial.links.items()
            ],
            "sources": spatial.sources,
            "reactions": spatial.reactions,
            "transformations": spatial.transformations,
            "accounting": spatial.accounting(),
        }
    if world.event_space is not None:
        result["causal_events"] = [asdict(event) for event in world.event_space.events]
    return result


def trace(initial, ticks):
    events = hashlib.sha256()
    event_count = 0

    def receive(event):
        nonlocal event_count
        events.update(json.dumps(event, sort_keys=True).encode() + b"\n")
        event_count += 1

    world = Simulation(initial, observer=receive)
    hashes = [_digest(physical_state(world))]
    failure = None
    for _ in range(ticks):
        try:
            world.step()
        except Exception as error:
            failure = {"type": type(error).__name__, "message": str(error)}
        hashes.append(_digest(physical_state(world)))
        if failure is not None:
            break
    return {
        "state_hashes": hashes,
        "events_sha256": events.hexdigest(),
        "events": event_count,
        "error": failure,
        "tick": world.tick,
    }


def benchmark(path, output, ticks, repeats):
    source = path.read_bytes()
    initial = parse_initial_json(source)
    count = initial.ticks if ticks is None else ticks
    evidence = trace(initial, count)
    stepping = []
    # One unmeasured warmup; every measured repetition gets a fresh world.
    for repeat in range(repeats + 1):
        world = Simulation(initial)
        started = time.perf_counter()
        for _ in range(count):
            try:
                world.step()
            except Exception:
                break
        elapsed = time.perf_counter() - started
        if _digest(physical_state(world)) != evidence["state_hashes"][-1]:
            raise AssertionError("timed stepping differs from the observed physical trace")
        if repeat:
            stepping.append(elapsed)
    audited = []
    for repeat in range(repeats):
        destination = output / f"audit-{repeat:03d}"
        started = time.perf_counter()
        failure = None
        try:
            run_initialization(path, destination, ticks=count)
        except Exception as error:
            failure = {"type": type(error).__name__, "message": str(error)}
        audited.append(time.perf_counter() - started)
        metadata = json.loads((destination / "run.json").read_text(encoding="utf-8"))
        if failure != evidence["error"]:
            raise AssertionError("audited runner failure differs from the physical trace")
        if metadata["initialization_sha256"] != hashlib.sha256(source).hexdigest():
            raise AssertionError("benchmark input changed during execution")
    return {
        "initialization": str(path.resolve()),
        "initialization_sha256": hashlib.sha256(source).hexdigest(),
        "ticks": count,
        "repeats": repeats,
        "stepping_seconds": stepping,
        "stepping_median_seconds": statistics.median(stepping),
        "audited_seconds": audited,
        "audited_median_seconds": statistics.median(audited),
        "trace": evidence,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ticks", type=int)
    parser.add_argument("--repeat", type=int, default=3)
    args = parser.parse_args()
    if args.repeat < 1 or (args.ticks is not None and args.ticks < 0):
        parser.error("repeat must be positive and ticks nonnegative")
    validate_output_path(args.output)
    args.output = args.output.resolve()
    if any(path.resolve().is_relative_to(args.output.resolve()) for path in args.init):
        parser.error("original inputs must be outside benchmark output")
    if args.output.exists() and any(args.output.iterdir()):
        parser.error("benchmark output must be empty")
    args.output.mkdir(parents=True, exist_ok=True)
    report = args.output / "benchmark.json"
    report.touch()
    fingerprint = source_fingerprint()
    cases = [args.output / f"case-{index:03d}" for index in range(len(args.init))]
    with ArtifactLease(args.output, [report], keep_alive_with=cases):
        results = [
            benchmark(path, folder, args.ticks, args.repeat)
            for path, folder in zip(args.init, cases, strict=True)
        ]
        if source_fingerprint() != fingerprint:
            raise RuntimeError("source changed during benchmark; rerun against a stable checkout")
        report.write_text(
            json.dumps(
                {
                    "python": sys.version,
                    "package_path": str(Path(event_universe.__file__).resolve()),
                    "source_sha256": fingerprint,
                    "logical_cpus": os.process_cpu_count(),
                    "gil_enabled": sys._is_gil_enabled(),
                    "scope": "headless; one core warmup; timing excludes trace hashing; audited timing includes all runner checks and event I/O",
                    "cases": results,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    print(report.resolve())


if __name__ == "__main__":
    main()
