"""Run the worlds of a series as separate processes, one per core.

A series is a list of world files, run one after the other through
`event_universe.runner.run_initialization`. This tool launches those runs in
parallel: every world in its own process (`python -m
event_universe --init WORLD --output OUT/<name>/run`), at most `--jobs` at
once (the machine's cores by default), each with its own log (`OUT/<name>/
log.txt`, the child's stdout and stderr) and its own artifacts directory, and
a summary table at the end (`OUT/summary.md`, `OUT/summary.json`, printed):
the status, the ticks, the runner's seconds, the child's wall seconds, its
peak RSS, the digests of `state.json` and of the ledger (`audit` of
`run.json`), and the conservation flag. The engine is untouched: a run is the
runner's, deterministic, and its files are byte for byte those of the same
world run alone.

Run with PYTHONPATH set to the checkout's src (the children run the package
this process imports):

    PYTHONPATH=src python tools/run_series.py --jobs 4 --out runs/events \\
        examples/events/one_content.json examples/events/two_contents.json

`--ticks` overrides every world's duration, `--python` names the interpreter of the children (this one by default). A world's name is its
file stem; two worlds of one name are refused. The output directory of a
run must be empty or absent, as the runner requires.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
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
    "conserved",
)


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_one(
    world: Path,
    directory: Path,
    *,
    ticks: int | None,
    python: str,
    environment: dict[str, str],
) -> dict[str, object]:
    """One world in its own process; returns its row of the summary."""
    directory.mkdir(parents=True, exist_ok=True)
    run_dir = directory / "run"
    command = [python, "-m", "event_universe", "--init", str(world), "--output", str(run_dir)]
    if ticks is not None:
        command += ["--ticks", str(ticks)]
    started = time.perf_counter()
    with (directory / "log.txt").open("w", encoding="utf-8") as log:
        log.write(" ".join(command) + "\n")
        log.flush()
        child = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, env=environment)
        _, status, usage = os.wait4(child.pid, 0)
    wall = time.perf_counter() - started
    code = os.waitstatus_to_exitcode(status)
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
    return row


def run_series(
    worlds: list[Path],
    out: Path,
    *,
    jobs: int | None = None,
    ticks: int | None = None,
    python: str | None = None,
) -> list[dict[str, object]]:
    """Every world in its own process, at most `jobs` at once; the rows of the
    summary in the order of `worlds`, written beside the runs."""
    names = [world.stem for world in worlds]
    if len(set(names)) != len(names):
        raise ValueError("two worlds of a series must not share a name")
    for world in worlds:
        if not world.is_file():
            raise ValueError(f"world file not found: {world}")
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
                    ticks=ticks,
                    python=interpreter,
                    environment=environment,
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
    parser.add_argument("worlds", nargs="+", type=Path, help="World files of the series")
    parser.add_argument("--out", type=Path, required=True, help="Directory of the runs and the summary")
    parser.add_argument("--jobs", type=int, help="Runs at once (default: the machine's cores)")
    parser.add_argument("--ticks", type=int, help="Override every world's duration")
    parser.add_argument("--python", help="Interpreter of the children (default: this one)")
    args = parser.parse_args()
    try:
        rows = run_series(
            args.worlds,
            args.out,
            jobs=args.jobs,
            ticks=args.ticks,
            python=args.python,
        )
    except ValueError as error:
        parser.exit(1, f"Series refused: {error}\n")
    print(table(rows), end="")
    if any(row["status"] != "completed" for row in rows):
        sys.exit(1)


if __name__ == "__main__":
    main()
