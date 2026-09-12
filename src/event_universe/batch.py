"""Run independent initialized worlds in bounded, isolated worker processes."""

import argparse
import hashlib
import json
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from event_universe.initialization import parse_initial_json
from event_universe.retention import ArtifactLease, cleanup_expired, validate_output_path
from event_universe.runner import run_initialization


def _run_job(initialization: Path, output: Path, ticks: int | None) -> dict[str, Any]:
    """Keep normal runner artifacts and propagate physical failure into the summary."""
    try:
        run_initialization(initialization, output, ticks=ticks)
    except Exception as error:
        return {"status": "failed", "error": str(error), "worker_pid": os.getpid()}
    return {"status": "completed", "error": None, "worker_pid": os.getpid()}


def run_batch(
    initializations: list[Path], output: Path, *, workers: int | None = None, ticks: int | None = None
) -> Path:
    """Freeze validated inputs before dispatch; each world retains every runner check."""
    if not initializations:
        raise ValueError("at least one initialization is required")
    if workers is None:
        workers = min(4, os.process_cpu_count() or 1, len(initializations))
    if type(workers) is not int or workers < 1:
        raise ValueError("workers must be a positive integer")
    if ticks is not None and (type(ticks) is not int or ticks < 0):
        raise ValueError("ticks must be a nonnegative integer")
    workers = min(workers, len(initializations))
    output = output.resolve()
    validate_output_path(output)
    sources = []
    for path in initializations:
        if path.resolve().is_relative_to(output):
            raise ValueError("original initializations must be outside the batch output")
        source = path.read_bytes()
        parse_initial_json(source)
        sources.append(source)
    if output.exists() and any(output.iterdir()):
        raise ValueError("use an empty batch output directory to preserve earlier artifacts")
    cleanup_expired(output.parent)
    output.mkdir(parents=True, exist_ok=True)
    inputs = output / "inputs"
    inputs.mkdir()
    summary = output / "batch.json"
    summary.write_text("{}\n", encoding="utf-8")
    destinations = [output / f"run-{index:04d}" for index in range(len(sources))]
    started = time.perf_counter()
    jobs: list[dict[str, Any]] = []
    for index, (path, source) in enumerate(zip(initializations, sources, strict=True)):
        jobs.append(
            {
                "index": index,
                "original_initialization": str(path.resolve()),
                "initialization_sha256": hashlib.sha256(source).hexdigest(),
                "input": f"inputs/{index:04d}.json",
                "output": destinations[index].name,
                "status": "pending",
                "error": None,
            }
        )

    def save(status: str) -> None:
        summary.write_text(
            json.dumps(
                {
                    "status": status,
                    "workers": workers,
                    "ticks_override": ticks,
                    "elapsed_seconds": time.perf_counter() - started,
                    "jobs": jobs,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    with ArtifactLease(output, [inputs, summary], keep_alive_with=destinations):
        for index, source in enumerate(sources):
            (inputs / f"{index:04d}.json").write_bytes(source)
        save("running")
        pool = None
        try:
            pool = ProcessPoolExecutor(
                max_workers=workers, mp_context=multiprocessing.get_context("spawn")
            )
            futures = {
                pool.submit(_run_job, inputs / f"{index:04d}.json", destination, ticks): index
                for index, destination in enumerate(destinations)
            }
            for future in as_completed(futures):
                index = futures[future]
                try:
                    jobs[index].update(future.result())
                except Exception as error:
                    jobs[index].update(status="failed", error=str(error))
                save("running")
        except BaseException as error:
            # Python 3.14 clears these handles in terminate_workers(); retain our
            # own workers so returning also means their writer leases are closed.
            if pool is not None:
                processes = tuple((getattr(pool, "_processes", None) or {}).values())
                pool.terminate_workers()
                for process in processes:
                    process.join(timeout=5)
                    if process.is_alive():
                        process.kill()
                        process.join(timeout=5)
            status = "failed" if isinstance(error, Exception) else "interrupted"
            for job in jobs:
                if job["status"] == "pending":
                    job.update(status=status, error=f"batch execution {status}: {error}")
            save(status)
            raise
        finally:
            if pool is not None:
                pool.shutdown(wait=True, cancel_futures=True)
        save("completed" if all(job["status"] == "completed" for job in jobs) else "failed")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run independent headless worlds in parallel.")
    parser.add_argument("--init", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, help="Worker limit; defaults to at most four processes")
    parser.add_argument("--ticks", type=int, help="Override every world's requested duration")
    args = parser.parse_args()
    try:
        path = run_batch(args.init, args.output, workers=args.workers, ticks=args.ticks)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Batch failed: {error}\n")
    print(path)
    if json.loads(path.read_text(encoding="utf-8"))["status"] != "completed":
        parser.exit(1, "One or more runs failed; inspect batch.json and each run's evidence.\n")


if __name__ == "__main__":
    main()
