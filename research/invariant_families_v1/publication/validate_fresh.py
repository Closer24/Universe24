"""Validate the exact staged follow-up without rerunning registered studies."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def main():
    setup = json.loads((HERE / "staged_checkout.json").read_text())
    fresh = Path(setup["fresh_checkout"])
    temporary = Path(setup["temporary_directory"])
    temporary.mkdir(exist_ok=False)
    env = dict(os.environ, PYTHONPATH="/workspace/scratch/1966445260ce/clock-python-deps",
               TMPDIR=str(temporary), TMP=str(temporary), TEMP=str(temporary))
    commands = [
        ("environment", [sys.executable, "-c", "import sys,mpmath,z3,json; print(json.dumps({'python':sys.version,'mpmath':mpmath.__version__,'z3':z3.get_version_string()}))"]),
        ("historical_restore", [sys.executable, "-m", "research.experiments.materialize_evidence"]),
        ("historical_check", [sys.executable, "-m", "research.experiments.materialize_evidence", "--check-only"]),
        ("clock_restore", [sys.executable, "-m", "research.clock_selection.archive", "materialize"]),
        ("clock_check", [sys.executable, "-m", "research.clock_selection.archive", "materialize", "--check-only"]),
        ("new_evidence", [sys.executable, "-m", "research.invariant_families_v1.verify_evidence"]),
        ("full_tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
        ("impulse", [sys.executable, "-m", "universe24", "--config", "examples/impulse.json", "--audit"]),
        ("signed_impulse", [sys.executable, "-m", "universe24", "--config", "examples/signed_impulse.json", "--audit"]),
        ("old_index", [sys.executable, "-m", "research.clock_selection.run", "verify-index", "--index", "research/clock_selection/evidence/index_final/index.json"]),
    ]
    receipt = {**setup, "started_utc": datetime.now(timezone.utc).isoformat(),
               "dependency_directory": env["PYTHONPATH"], "commands": [],
               "scope": "Fresh exact staged tree, declared archived and directly tracked evidence, full tests and required CLI audits. No new registered research run.",
               "complete": False, "passed": False}
    output = HERE / "fresh_validation.json"
    if output.exists():
        raise FileExistsError(output)
    for name, command in commands:
        start = time.monotonic()
        result = subprocess.run(command, cwd=fresh, env=env, capture_output=True, timeout=900)
        logs = {}
        for label, raw in (("stdout", result.stdout), ("stderr", result.stderr)):
            path = HERE / f"fresh_{name}.{label}.txt"
            path.write_bytes(raw)
            logs[label] = {"file": path.name, "bytes": len(raw),
                           "sha256": hashlib.sha256(raw).hexdigest()}
        receipt["commands"].append({"name": name, "command": command,
                                    "returncode": result.returncode,
                                    "wall_seconds": time.monotonic() - start, "logs": logs})
        output.write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps({"check": name, "returncode": result.returncode}), flush=True)
        if result.returncode:
            raise RuntimeError("Validation failed: " + name)
    protected = ["universe24", "research/reference", "research/components",
                 "research/presenter", "research/experiments", "research/staged_blocks"]
    diff = subprocess.check_output(["git", "diff", "--name-only", setup["baseline_commit"],
                                    "--", *protected], cwd=fresh, text=True)
    if diff:
        raise RuntimeError("Protected source changed: " + diff)
    receipt.update(complete=True, passed=True, protected_runtime_diff=[],
                   finished_utc=datetime.now(timezone.utc).isoformat())
    output.write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
