"""Execute independent research controls; never combine their evolution laws."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


LANES = (
    "heldout_geometry", "bitgrowth_algebra", "gauge_clock_bridge",
    "complexity_selection", "compatible_geometry", "matter_backreaction",
)
ROOT = Path(__file__).resolve().parents[2]


def run(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    results = []
    for lane in LANES:
        destination = (out / f"{lane}.json").resolve()
        command = [sys.executable, "-m", f"validation.synthesis.{lane}",
                   "--out", str(destination)]
        source = ROOT / "validation" / "synthesis" / f"{lane}.py"
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        start = time.monotonic()
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        (out / f"{lane}.stdout.log").write_text(completed.stdout)
        (out / f"{lane}.stderr.log").write_text(completed.stderr)
        record = {
            "lane": lane, "command": command,
            "exit_code": completed.returncode,
            "elapsed_seconds": round(time.monotonic() - start, 3),
            "source_sha256": source_hash,
            "evidence": str(destination),
            "evidence_exists": destination.is_file(),
        }
        if destination.is_file():
            record["evidence_sha256"] = hashlib.sha256(destination.read_bytes()).hexdigest()
            record["result"] = json.loads(destination.read_text())
        results.append(record)
        print(json.dumps({k: v for k, v in record.items() if k != "result"}), flush=True)
    report = {
        "schema": "universe24/integration-research-controls/1",
        "source_revision": revision,
        "purpose": "Independent falsifying controls and integration requirements, not one combined physical tensor",
        "execution_complete": all(r["exit_code"] == 0 and r["evidence_exists"] for r in results),
        "physical_acceptance": "not_established",
        "lanes": results,
    }
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/synthesis"))
    args = parser.parse_args()
    result = run(args.out)
    raise SystemExit(0 if result["execution_complete"] else 1)


if __name__ == "__main__":
    main()
