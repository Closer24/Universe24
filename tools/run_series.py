"""Run the worlds of a series as separate processes, one per core.

A series is a list of world files, run one after the other through
`event_universe.runner.run_initialization`. This tool launches those runs in
parallel: every world in its own process (`python -m
event_universe --init WORLD --output OUT/<name>/run`), at most `--jobs` at
once (the machine's cores by default), each with its own log (`OUT/<name>/
log.txt`, the child's stdout and stderr) and its own artifacts directory, and
a summary table at the end (`OUT/summary.md`, `OUT/summary.json`, printed):
the status, the ticks, the runner's seconds, the child's wall seconds, its
peak RSS, the digests of `state.json`, of the ledger (`audit` of `run.json`)
and of `events.jsonl`, and the conservation flag. The engine is untouched: a
run is the runner's, deterministic, and its files are byte for byte those of
the same world run alone.

Run with PYTHONPATH set to the checkout's src (the children run the package
this process imports):

    PYTHONPATH=src python tools/run_series.py --jobs 4 --out runs/events \\
        examples/events/one_content.json examples/events/two_contents.json

`--ticks` overrides every world's duration, `--python` names the interpreter
of the children (this one by default). A world's name is its file stem; two
worlds of one name are refused. The output directory of a run must be empty
or absent, as the runner requires.

`--list FILE` reads a JSON list of worlds (`examples/events/gate_set.json`,
the gate set replayed at every commit of an integration: `{"worlds":
[{"path": ..., "ticks": ..., "cap": ...}, ...]}`), resolves each `path`
relative to the file and runs those worlds, each at its listed `ticks`
(`--fast`: at its `cap`, the interval by which the world's coverage is
complete); `--ticks` still overrides every world's duration. `--compare
SUMMARY.json` reads an earlier run's summary and prints, per world, whether
`state.json`, the ledger and `events.jsonl` are identical or changed, and
exits 1 on a change or on a world missing on either side: the replay's
verdict in one command.

    PYTHONPATH=src python tools/run_series.py --list examples/events/gate_set.json \\
        --jobs 4 --out runs/gate/head --compare runs/gate/base/summary.json

`--wall-seconds N` and `--memory-mb M` guard the host; both are off by default
and nothing changes without them. A world whose run exceeds N seconds of wall
clock is killed and reported as `not completed: wall N s`. With `--memory-mb`
the child sets its own address-space bound (`resource.setrlimit(RLIMIT_AS)`,
M MB, before it imports the package) and a run stopped by that bound (a
`MemoryError`, a library that cannot be mapped, the OS refusing memory) is
reported as `not completed: memory M MB`. The other worlds continue; the tool
exits 1 as for any world not completed, and `--compare` reports the status.

    PYTHONPATH=src python tools/run_series.py --jobs 4 --out runs/gate/head \\
        --wall-seconds 600 --memory-mb 4096 --list examples/events/gate_set.json

`--keep-row-clicks` passes the runner's option of the same name to every
child: the record `events.jsonl` with the per-row `click` lines of the
measured events (a GameBoard diagnostic, most of a long run's bytes; the
detector's reading is the `record` and `gather` lines, written either way),
the record as it was before the option, and `run.json` without
`omit_row_clicks`. Off by default (the model owner, 2026-09-23, record 1296
of docs/LOG_2026-09-20.md): the lines are left out and `run.json` carries
`omit_row_clicks` true, so the `events_sha256` of a default run differs from
a digest registered with the lines by the omitted lines alone; the gate
set's digests (`gate_set.json`) are replayed under the option.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import signal
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

COLUMNS = (
    "world",
    "status",
    "ticks",
    "runner_seconds",
    "wall_seconds",
    "peak_rss_mb",
    "state_sha256",
    "state_bytes",
    "audit_sha256",
    "events_sha256",
    "conserved",
)

# The digests `--compare` reads, in the order they are reported.
DIGESTS = ("state_sha256", "audit_sha256", "events_sha256")

# What a child stopped by its address-space bound writes to its log: the
# interpreter's error, the loader's when a library cannot be mapped, the OS's.
MEMORY_MARKS = ("MemoryError", "failed to map segment", "Cannot allocate memory")

# The child under `--memory-mb`: the bound set before the package is imported,
# then the module run exactly as `python -m event_universe` runs it.
MEMORY_BOOTSTRAP = (
    "import resource, runpy; limit = {megabytes} * 1024 * 1024; "
    "resource.setrlimit(resource.RLIMIT_AS, (limit, limit)); "
    "runpy.run_module('event_universe', run_name='__main__', alter_sys=True)"
)

# The wall guard polls the child this often.
POLL_SECONDS = 0.05


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _wait(pid: int, started: float, wall_seconds: float | None) -> tuple[int, object, bool]:
    """Reap the child with its resource usage: at once without a wall limit,
    otherwise polled and killed once the limit has passed since `started`.
    Returns the wait status, the usage and whether the guard stopped it."""
    if wall_seconds is None:
        _, status, usage = os.wait4(pid, 0)
        return status, usage, False
    while True:
        done, status, usage = os.wait4(pid, os.WNOHANG)
        if done:
            return status, usage, False
        if time.perf_counter() - started > wall_seconds:
            # The pid is ours until reaped below, so the signal cannot miss.
            os.kill(pid, signal.SIGKILL)
            _, status, usage = os.wait4(pid, 0)
            return status, usage, True
        time.sleep(POLL_SECONDS)


def run_one(
    world: Path,
    directory: Path,
    *,
    ticks: int | None,
    python: str,
    environment: dict[str, str],
    wall_seconds: float | None = None,
    memory_mb: int | None = None,
    keep_row_clicks: bool = False,
) -> dict[str, object]:
    """One world in its own process; returns its row of the summary. Under
    `wall_seconds` the child is killed past that wall clock; under `memory_mb`
    it bounds its own address space at that many MB. A run a guard stopped is
    reported `not completed: wall N s` or `not completed: memory M MB`.
    `keep_row_clicks` passes the runner's `--keep-row-clicks` to the child
    (the record with its per-row click lines; off by default)."""
    directory.mkdir(parents=True, exist_ok=True)
    run_dir = directory / "run"
    if memory_mb is None:
        command = [python, "-m", "event_universe"]
    else:
        command = [python, "-c", MEMORY_BOOTSTRAP.format(megabytes=memory_mb)]
    command += ["--init", str(world), "--output", str(run_dir)]
    if ticks is not None:
        command += ["--ticks", str(ticks)]
    if keep_row_clicks:
        command.append("--keep-row-clicks")
    started = time.perf_counter()
    with (directory / "log.txt").open("w", encoding="utf-8") as log:
        log.write(" ".join(command) + "\n")
        log.flush()
        child = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, env=environment)
        status, usage, stopped = _wait(child.pid, started, wall_seconds)
    wall = time.perf_counter() - started
    code = os.waitstatus_to_exitcode(status)
    guard = None
    if stopped:
        guard = f"not completed: wall {wall_seconds:g} s"
    elif memory_mb is not None and code:
        text = (directory / "log.txt").read_text(encoding="utf-8", errors="replace")
        if any(mark in text for mark in MEMORY_MARKS):
            guard = f"not completed: memory {memory_mb} MB"
    row: dict[str, object] = {
        "world": world.stem,
        "path": str(world),
        "exit_code": code,
        "status": "failed" if code else "completed",
        "ticks": None,
        "runner_seconds": None,
        "wall_seconds": round(wall, 3),
        # ru_maxrss is in kilobytes on Linux.
        "peak_rss_mb": round(usage.ru_maxrss / 1024.0, 1),
        "state_sha256": None,
        "state_bytes": None,
        "audit_sha256": None,
        "events_sha256": None,
        "conserved": None,
    }
    record = run_dir / "run.json"
    if record.exists():
        metadata = json.loads(record.read_text(encoding="utf-8"))
        row["status"] = str(metadata.get("status", row["status"]))
        row["ticks"] = metadata.get("completed_ticks")
        row["runner_seconds"] = round(float(metadata.get("elapsed_seconds", 0.0)), 3)
        row["audit_sha256"] = _digest(json.dumps(metadata.get("audit", [])).encode("utf-8"))
        row["conserved"] = metadata.get("conserved_at_every_completed_tick")
        if "standing_field" in metadata:
            row["standing_field"] = metadata["standing_field"]
    state = run_dir / "state.json"
    if state.exists():
        data = state.read_bytes()
        row["state_sha256"] = _digest(data)
        row["state_bytes"] = len(data)
    events = run_dir / "events.jsonl"
    if events.exists():
        row["events_sha256"] = _digest(events.read_bytes())
    if guard is not None:
        row["status"] = guard
    return row


def read_list(path: Path, *, fast: bool = False) -> tuple[list[Path], dict[Path, int]]:
    """The worlds of a list file (`{"worlds": [{"path", "ticks", "cap"}, ...]}`),
    each path resolved relative to the file, and the duration each runs at: its
    listed `ticks`, or its `cap` under `fast` (its `ticks` when it has none)."""
    document = json.loads(path.read_text(encoding="utf-8"))
    entries = document.get("worlds") if isinstance(document, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"the list names no worlds: {path}")
    worlds: list[Path] = []
    durations: dict[Path, int] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise ValueError(f"an entry of the list names no path: {path}")
        world = (path.parent / entry["path"]).resolve()
        duration = entry.get("cap", entry.get("ticks")) if fast else entry.get("ticks")
        if duration is not None:
            durations[world] = int(duration)
        worlds.append(world)
    return worlds, durations


def compare(rows: list[dict[str, object]], earlier: list[dict[str, object]]) -> list[tuple[str, str]]:
    """The verdict per world against an earlier summary's rows, in the order
    of `rows` then the earlier worlds missing here: `identical` when the run
    completed and every digest the earlier row recorded is the same, otherwise
    what differs (the digests that changed, a failed run, a world missing on
    one side, an earlier row without digests)."""
    before = {str(row["world"]): row for row in earlier}
    after = {str(row["world"]): row for row in rows}
    verdicts: list[tuple[str, str]] = []
    for name in [*after, *(name for name in before if name not in after)]:
        if name not in before:
            verdicts.append((name, "missing from the earlier summary"))
        elif name not in after:
            verdicts.append((name, "missing from this run"))
        elif after[name].get("status") != "completed":
            verdicts.append((name, f"{after[name].get('status')} in this run"))
        elif not any(digest in before[name] for digest in DIGESTS):
            verdicts.append((name, "no digests in the earlier summary"))
        else:
            differing = [
                digest
                for digest in DIGESTS
                if digest in before[name] and before[name][digest] != after[name].get(digest)
            ]
            verdicts.append((name, "identical" if not differing else "changed: " + ", ".join(differing)))
    return verdicts


def run_series(
    worlds: list[Path],
    out: Path,
    *,
    jobs: int | None = None,
    ticks: int | None = None,
    python: str | None = None,
    durations: dict[Path, int] | None = None,
    wall_seconds: float | None = None,
    memory_mb: int | None = None,
    keep_row_clicks: bool = False,
) -> list[dict[str, object]]:
    """Every world in its own process, at most `jobs` at once; the rows of the
    summary in the order of `worlds`, written beside the runs. `ticks` overrides
    every world's duration; otherwise a world listed in `durations` runs for
    that many intervals and the others for their declared `ticks`. The guards
    `wall_seconds` and `memory_mb` are those of `run_one`, off when None;
    `keep_row_clicks` is passed to every child (`run_one`), off by default."""
    names = [world.stem for world in worlds]
    if len(set(names)) != len(names):
        raise ValueError("two worlds of a series must not share a name")
    for world in worlds:
        if not world.is_file():
            raise ValueError(f"world file not found: {world}")
    if wall_seconds is not None and wall_seconds < 0:
        raise ValueError("--wall-seconds must not be negative")
    if memory_mb is not None and memory_mb <= 0:
        raise ValueError("--memory-mb must be positive")
    if memory_mb is not None and not hasattr(resource, "RLIMIT_AS"):
        raise ValueError("--memory-mb needs RLIMIT_AS, which this host lacks")
    workers = max(1, jobs if jobs is not None else (os.cpu_count() or 1))
    interpreter = python or sys.executable
    environment = dict(os.environ)
    if python is None:
        # The children run the package this process imports, whichever checkout
        # put it on the path (pytest's `pythonpath` reaches sys.path only).
        import event_universe

        root = str(Path(event_universe.__file__).resolve().parents[1])
        environment["PYTHONPATH"] = os.pathsep.join(
            [root, *filter(None, [environment.get("PYTHONPATH")])]
        )
    out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(
            pool.map(
                lambda world: run_one(
                    world,
                    out / world.stem,
                    ticks=ticks if ticks is not None else (durations or {}).get(world),
                    python=interpreter,
                    environment=environment,
                    wall_seconds=wall_seconds,
                    memory_mb=memory_mb,
                    keep_row_clicks=keep_row_clicks,
                ),
                worlds,
            )
        )
    (out / "summary.json").write_text(json.dumps(rows, indent=1) + "\n", encoding="utf-8")
    (out / "summary.md").write_text(table(rows), encoding="utf-8")
    return rows


def table(rows: list[dict[str, object]]) -> str:
    """The summary as a Markdown table, the digests shortened to twelve characters."""
    lines = ["| " + " | ".join(COLUMNS) + " |", "| " + " | ".join("---" for _ in COLUMNS) + " |"]
    for row in rows:
        cells = []
        for column in COLUMNS:
            value = row.get(column)
            if column.endswith("sha256") and isinstance(value, str):
                value = value[:12]
            cells.append("" if value is None else str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("worlds", nargs="*", type=Path, help="World files of the series")
    parser.add_argument("--out", type=Path, required=True, help="Directory of the runs and the summary")
    parser.add_argument("--jobs", type=int, help="Runs at once (default: the machine's cores)")
    parser.add_argument("--ticks", type=int, help="Override every world's duration")
    parser.add_argument("--python", help="Interpreter of the children (default: this one)")
    parser.add_argument(
        "--list",
        type=Path,
        help="A JSON list of worlds (examples/events/gate_set.json): paths relative to the file, each run at its listed ticks",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="With --list: run each world to its listed cap, the interval by which its coverage is complete",
    )
    parser.add_argument(
        "--compare",
        type=Path,
        help="An earlier run's summary.json: print identical or changed per world, exit 1 on a change",
    )
    parser.add_argument(
        "--wall-seconds",
        type=float,
        help="Kill a world's run past this wall clock and report it not completed (default: no limit)",
    )
    parser.add_argument(
        "--memory-mb",
        type=int,
        help="Bound each run's address space (RLIMIT_AS) at this many MB and report a run it stops (default: no limit)",
    )
    parser.add_argument(
        "--keep-row-clicks",
        action="store_true",
        help="Run every world with the runner's --keep-row-clicks: the record with its per-row click lines, as registered (default: the lines left out, run.json marked omit_row_clicks)",
    )
    args = parser.parse_args()
    if args.fast and args.list is None:
        parser.error("--fast needs --list")
    try:
        worlds: list[Path] = list(args.worlds)
        durations: dict[Path, int] = {}
        if args.list is not None:
            listed, durations = read_list(args.list, fast=args.fast)
            worlds = listed + worlds
        if not worlds:
            raise ValueError("no worlds: name world files or pass --list FILE")
        rows = run_series(
            worlds,
            args.out,
            jobs=args.jobs,
            ticks=args.ticks,
            python=args.python,
            durations=durations,
            wall_seconds=args.wall_seconds,
            memory_mb=args.memory_mb,
            keep_row_clicks=args.keep_row_clicks,
        )
    except ValueError as error:
        parser.exit(1, f"Series refused: {error}\n")
    print(table(rows), end="")
    failed = any(row["status"] != "completed" for row in rows)
    if args.compare is not None:
        verdicts = compare(rows, json.loads(args.compare.read_text(encoding="utf-8")))
        for world, verdict in verdicts:
            print(f"{world}: {verdict}")
        failed = failed or any(verdict != "identical" for _, verdict in verdicts)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
