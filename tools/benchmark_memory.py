"""Measure one complete headless run; use a fresh process for comparable OS peaks."""

import argparse
import hashlib
import json
import shutil
import sys
import tracemalloc
from pathlib import Path

import event_universe
from event_universe.core.local_execution import validate_execution_options
from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization, source_fingerprint


def process_memory():
    """OS process lifetime peak; includes interpreter workers, excludes child processes."""
    result = {"peak_resident_bytes": None, "resident_bytes": None, "private_bytes": None}
    try:
        if sys.platform == "win32":
            import ctypes
            from ctypes import wintypes

            class Counters(ctypes.Structure):
                _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
                    (name, ctypes.c_size_t)
                    for name in (
                        "PeakWorkingSetSize",
                        "WorkingSetSize",
                        "QuotaPeakPagedPoolUsage",
                        "QuotaPagedPoolUsage",
                        "QuotaPeakNonPagedPoolUsage",
                        "QuotaNonPagedPoolUsage",
                        "PagefileUsage",
                        "PeakPagefileUsage",
                        "PrivateUsage",
                    )
                ]

            kernel = ctypes.WinDLL("kernel32", use_last_error=True)
            psapi = ctypes.WinDLL("psapi", use_last_error=True)
            kernel.GetCurrentProcess.restype = wintypes.HANDLE
            psapi.GetProcessMemoryInfo.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(Counters),
                wintypes.DWORD,
            ]
            psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
            counters = Counters()
            counters.cb = ctypes.sizeof(counters)
            if not psapi.GetProcessMemoryInfo(
                kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb
            ):
                raise ctypes.WinError(ctypes.get_last_error())
            result.update(
                peak_resident_bytes=counters.PeakWorkingSetSize,
                resident_bytes=counters.WorkingSetSize,
                private_bytes=counters.PrivateUsage,
            )
        elif sys.platform in ("linux", "darwin"):
            import resource

            maximum = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            result["peak_resident_bytes"] = int(maximum * (1 if sys.platform == "darwin" else 1024))
    except (ImportError, OSError) as error:
        result["unavailable_reason"] = str(error)
    return result


def benchmark(
    initialization,
    output,
    *,
    ticks=None,
    workers=1,
    parallel_threshold=64,
    chunk_size=32,
    trace_python=False,
):
    """Keep all canonical artifacts and propagate failures after saving memory evidence."""
    validate_execution_options(workers, parallel_threshold, chunk_size)
    if ticks is not None and (type(ticks) is not int or ticks < 0):
        raise ValueError("ticks must be a nonnegative integer")
    if trace_python and workers != 1:
        raise ValueError("Python allocation tracing requires serial workers=1")
    if (trace_python or workers != 1) and tracemalloc.is_tracing():
        raise ValueError("Python allocation tracing is already active; use a fresh process")
    validate_output_path(output)
    output = output.resolve()
    if initialization.resolve().is_relative_to(output):
        raise ValueError("original initialization must be outside memory benchmark output")
    if output.exists() and any(output.iterdir()):
        raise ValueError("memory benchmark output must be empty")
    # Freeze only input data, before the measured audited-run interval.
    with initialization.open("rb") as source:
        initialization_hash = hashlib.file_digest(source, "sha256").hexdigest()
    fingerprint = source_fingerprint()
    output.mkdir(parents=True, exist_ok=True)
    frozen, report, run = output / "input.json", output / "memory.json", output / "run"
    frozen.touch()
    report.touch()
    with ArtifactLease(output, [frozen, report], keep_alive_with=[run]):
        shutil.copyfile(initialization, frozen)
        with frozen.open("rb") as source:
            if hashlib.file_digest(source, "sha256").hexdigest() != initialization_hash:
                raise RuntimeError("initialization changed while freezing benchmark input")
        before = process_memory()
        failure = None
        allocations = None
        if trace_python:
            tracemalloc.start()
        try:
            run_initialization(
                frozen,
                run,
                ticks=ticks,
                workers=workers,
                parallel_threshold=parallel_threshold,
                chunk_size=chunk_size,
            )
        except BaseException as error:
            failure = error
        finally:
            after = process_memory()
            if trace_python:
                current, peak = tracemalloc.get_traced_memory()
                allocations = {
                    "current_bytes": current,
                    "peak_bytes": peak,
                    "scope": "Python allocations during audited serial run; not RSS",
                }
                tracemalloc.stop()
        final_fingerprint = source_fingerprint()
        if final_fingerprint != fingerprint and failure is None:
            failure = RuntimeError("source changed during benchmark; rerun against a stable checkout")
        metadata = (
            json.loads((run / "run.json").read_text(encoding="utf-8"))
            if (run / "run.json").exists()
            else {}
        )
        report.write_text(
            json.dumps(
                {
                    "python": sys.version,
                    "package_path": str(Path(event_universe.__file__).resolve()),
                    "source_sha256": fingerprint,
                    "source_after_sha256": final_fingerprint,
                    "source_unchanged": fingerprint == final_fingerprint,
                    "initialization": str(initialization.resolve()),
                    "initialization_sha256": initialization_hash,
                    "execution": metadata.get("execution"),
                    "run_status": metadata.get("status", "failed"),
                    "requested_ticks": metadata.get("requested_ticks", ticks),
                    "completed_ticks": metadata.get("completed_ticks"),
                    "tick": metadata.get("tick"),
                    "failure": None
                    if failure is None
                    else {"type": type(failure).__name__, "message": str(failure)},
                    "process_memory": {
                        "before": before,
                        "after": after,
                        "scope": "OS resident peak is process lifetime, not a run delta; current readings bracket the audited run. Includes same-process interpreter workers; excludes MPI or other child processes. Use a fresh CLI process for comparisons.",
                    },
                    "python_allocations": allocations,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        if failure is not None:
            raise failure
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--init", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ticks", type=int)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--parallel-threshold", type=int, default=64)
    parser.add_argument("--chunk-size", type=int, default=32)
    parser.add_argument("--trace-python", action="store_true")
    args = vars(parser.parse_args())
    args["initialization"] = args.pop("init")
    print(benchmark(**args))


if __name__ == "__main__":
    main()
