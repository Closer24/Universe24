"""Audit helper: run initialization files headlessly through the CLI and tabulate run.json.

usage: PYTHONPATH=src python examples/research/entity-audit/run_headless.py --output DIR LABEL=INIT.json ...

Every run goes to DIR/runs/LABEL; the rows are appended to DIR/runs/summary.json.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("specs", nargs="+", help="LABEL=path/to/initialization.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (cwd of every run)")
    args = parser.parse_args()
    env = dict(os.environ, PYTHONPATH=str(args.root / "src"))
    rows = []
    for spec in args.specs:
        label, init = spec.split("=", 1)
        out_dir = args.output / "runs" / label
        cmd = [sys.executable, "-m", "event_universe", "--init", init, "--output", str(out_dir)]
        t0 = time.perf_counter()
        proc = subprocess.run(cmd, cwd=args.root, env=env, capture_output=True, text=True)
        wall = round(time.perf_counter() - t0, 3)
        row = {
            "label": label,
            "init": init,
            "exit": proc.returncode,
            "wall_seconds": wall,
            "command": " ".join(
                ["PYTHONPATH=src python -m event_universe --init", init, "--output", str(out_dir)]
            ),
        }
        rj = out_dir / "run.json"
        if rj.exists():
            m = json.loads(rj.read_text())
            row.update(
                status=m.get("status"),
                completed_ticks=m.get("completed_ticks"),
                requested_ticks=m.get("ticks"),
                conserved=m.get("conserved_at_every_completed_tick"),
                accounting_balanced=m.get("accounting_balanced_at_every_completed_tick"),
                elapsed_seconds=m.get("elapsed_seconds"),
                final_totals=m.get("final_totals"),
                escaped=m.get("escaped_totals"),
                failure=m.get("failure") or m.get("error"),
                run_keys=sorted(m.keys()),
            )
        if proc.returncode != 0:
            row["stderr_tail"] = proc.stderr.strip()[-1500:]
        row["stdout_tail"] = proc.stdout.strip()[-400:]
        rows.append(row)
        print(
            json.dumps(
                {k: v for k, v in row.items() if k not in ("run_keys", "command", "stdout_tail")}
            ),
            flush=True,
        )
    summary = args.output / "runs" / "summary.json"
    summary.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(summary.read_text()) if summary.exists() else []
    summary.write_text(json.dumps(existing + rows, indent=1))


if __name__ == "__main__":
    main()
