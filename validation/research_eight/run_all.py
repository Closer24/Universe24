"""Run eight source-only research audits; passing is not physical acceptance."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
FOLDER = Path(__file__).resolve().parent


def main():
    scripts = sorted(FOLDER.glob("0[1-8]_*.py"))
    if len(scripts) != 8 or {p.name[:2] for p in scripts} != {f"{i:02}" for i in range(1, 9)}:
        raise RuntimeError("Require exactly one completed audit for each of the eight reviews")
    out = ROOT / "runs/research_eight"
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for script in scripts:
        module = "validation.research_eight." + script.stem
        log = out / (script.stem + ".log")
        started = time.monotonic()
        with log.open("w") as stream:
            try:
                result = subprocess.run([sys.executable, "-m", module], cwd=ROOT,
                                        stdout=stream, stderr=subprocess.STDOUT, timeout=300)
                code = result.returncode
            except subprocess.TimeoutExpired:
                code = 124
        row = {"module": module, "exit_code": code,
               "status": "passed" if code == 0 else "failed",
               "seconds": round(time.monotonic() - started, 3),
               "source_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
               "log": str(log.relative_to(ROOT))}
        results.append(row)
        print(json.dumps(row), flush=True)
    report = {"schema": "universe24/research-eight/audit-run/1",
              "research_base": "621fc1f55800e50e1db5f6a30ce24bb83716a49a",
              "python": sys.version.split()[0], "audits": results,
              "checks_status": "passed" if all(r["exit_code"] == 0 for r in results) else "failed",
              "interpretation": "Checks include expected physical failures and algebraic obstructions.",
              "general_einstein_acceptance": "not_established",
              "operational_clock_acceptance": "not_established",
              "combined_48_channel_solution": "not_established"}
    (out / "audit_manifest.json").write_text(json.dumps(report, indent=2) + "\n")
    return int(report["checks_status"] != "passed")


if __name__ == "__main__":
    raise SystemExit(main())
