"""Run configured mass-field timing probes and inspect saved ordinary-engine output.

All observations are read-only world/event audits. The normal runner owns the
simulation, accounting, failure trace and existing HTML playback generation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from importlib.resources import files
from pathlib import Path

from configuration import document, expectations
from observe import assess

from event_universe.runner import run_initialization, source_fingerprint

HERE = Path(__file__).resolve().parent


def read_recording(path: Path) -> dict:
    """Read the renderer's recorded state; never reconstruct physical trajectories."""
    document = path.read_text(encoding="utf-8")
    marker = '<script id="recording" type="application/json">'
    if marker not in document:
        raise ValueError("the existing HTML renderer recording is missing")
    recording = json.loads(document.split(marker, 1)[1].split("</script>", 1)[0])
    if not recording.get("frames"):
        raise ValueError("the existing HTML recording has no snapshots")
    return recording


def run_case(initialization: Path, output: Path) -> dict:
    """Retain source identity, accounting and every-tick canonical playback."""
    before = source_fingerprint()
    raw = json.loads(initialization.read_text(encoding="utf-8"))
    if raw.get("event_program") is not None or any(
        field.get("bonded") or field.get("kerengonen") for field in raw.get("spatial_fields", [])
    ):
        raise ValueError("this candidate admits no quantum program or stochastic ray owner")
    error = None
    try:
        run_initialization(initialization, output, visualize=True, frame_stride=1)
    except Exception as failure:
        error = f"{type(failure).__name__}: {failure}"
    after = source_fingerprint()
    if before != after:
        raise RuntimeError("simulated source changed during the experiment")
    metadata_path = output / "run.json"
    if not metadata_path.exists():
        raise RuntimeError(error or "the ordinary runner produced no run metadata")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    recording = read_recording(output / "run.html")
    events = [
        json.loads(line) for line in (output / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    return {
        "name": initialization.stem,
        "metadata": metadata,
        "events": events,
        "frames": recording["frames"],
        "error": error,
        "source_sha256": before,
        "renderer_sha256": hashlib.sha256(
            files("event_universe").joinpath("ui_assets", "playback.html").read_bytes()
        ).hexdigest(),
        "python_version": platform.python_version(),
        "randomness_validation": "Validated deterministic profile: no quantum program or stochastic ray owner",
        "initialization_sha256": hashlib.sha256(initialization.read_bytes()).hexdigest(),
        "visualization": str(output / "run.html"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--case", choices=list(expectations()["cases"]), action="append")
    args = parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        parser.error("use a new or empty output directory")
    args.output.mkdir(parents=True, exist_ok=True)
    inputs = args.output / "inputs"
    inputs.mkdir()
    results = []
    audits = []
    for name in args.case or expectations()["cases"]:
        initialization = inputs / f"{name}.json"
        initialization.write_text(json.dumps(document(name), indent=2) + "\n", encoding="utf-8")
        case = run_case(initialization, args.output / name)
        results.append({key: value for key, value in case.items() if key not in {"events", "frames"}})
        audits.append(assess(case, name))
        print(case["visualization"], flush=True)
    (args.output / "summary.json").write_text(
        json.dumps({"runs": results, "acceptance": audits}, indent=2) + "\n", encoding="utf-8"
    )
    if any(case["error"] for case in results) or any(not audit["passed"] for audit in audits):
        raise SystemExit("one or more acceptance checks failed; preserved evidence is in summary.json")


if __name__ == "__main__":
    main()
