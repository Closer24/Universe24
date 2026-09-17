"""Write ``ray-recording.json`` beside a runner record by replaying it (a Recorder).

The runner writes no per-tick ray listing, so the phase of every Link and the
ray-event fields (``steps``, ``outbound``, ``event_ports``, ``event_shares``,
``detector``) are not in its record. This tool replays the preserved
``initialization.json`` through the Simulation API for the recorded number of
ticks, captures every tick with ``examples/generic-ray-coupling/evidence.capture``
(the copy of resident and Link rays the evidence tests use), checks that the
replay's event stream equals the runner's ``events.jsonl`` line for line and
that the source fingerprint equals ``run.json``'s, and only then writes the
sidecar. It is a Recorder in the sense of Highlights 3.29 and 3.30: it reads
the engine to store evidence; the Renderer (``extract.py``, ``viewer.html``)
reads only records.

Run:  PYTHONPATH=src python tools/ray_viewer/record_sidecar.py RUN [--out FILE]
where RUN is a ``run.json`` file or the directory that holds it.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

from event_universe import Simulation
from event_universe.configuration_validation import prepare_initialization
from event_universe.json_documents import parse_json_document
from event_universe.runner import source_fingerprint

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "examples" / "generic-ray-coupling" / "evidence.py"
COPIED_KEYS = (
    "model",
    "source_sha256",
    "initialization_sha256",
    "status",
    "completed_ticks",
    "requested_ticks",
    "shape",
    "boundary",
    "initial_totals",
    "final_totals",
    "escaped_totals",
    "source_totals",
)


def capture_function() -> Any:
    """The evidence tool's ``capture``, loaded from its file (it is not a package)."""
    spec = importlib.util.spec_from_file_location("ray_coupling_evidence", EVIDENCE)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load {EVIDENCE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.capture


def replay(run: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Replay the record and return its metadata and the per-tick frames."""
    directory = run if run.is_dir() else run.parent
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    source = (directory / "initialization.json").read_bytes()
    if hashlib.sha256(source).hexdigest() != metadata["initialization_sha256"]:
        raise ValueError("initialization.json differs from the run's initialization_sha256")
    if source_fingerprint() != metadata["source_sha256"]:
        raise ValueError("this source tree is not the one that made the run (source_sha256)")
    capture = capture_function()
    initial = prepare_initialization(parse_json_document(source)).initial
    events: list[dict[str, Any]] = []
    frames: list[dict[str, Any]] = []
    with Simulation(initial, observer=events.append) as world:
        frames.append(capture(world))
        for _ in range(int(metadata["completed_ticks"])):
            world.step()
            frames.append(capture(world))
        finals = {name: list(values) for name, values in world.totals().items()}
    if finals != {k: list(v) for k, v in metadata["final_totals"].items()}:
        raise ValueError("the replay's final totals differ from run.json")
    recorded = [
        json.loads(line)
        for line in (directory / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    replayed = [json.loads(json.dumps(event)) for event in events]
    if replayed != recorded:
        raise ValueError(f"the replay's {len(replayed)} events differ from the {len(recorded)} recorded")
    return metadata, frames


def write_sidecar(run: Path, out: Path | None = None) -> Path:
    metadata, frames = replay(run)
    directory = run if run.is_dir() else run.parent
    target = out or directory / "ray-recording.json"
    sidecar: dict[str, Any] = {key: metadata.get(key) for key in COPIED_KEYS}
    sidecar["recorded_by"] = (
        "tools/ray_viewer/record_sidecar.py: replay through Simulation + evidence.capture"
    )
    sidecar["frames"] = frames
    target.write_text(json.dumps(sidecar) + "\n", encoding="utf-8")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path, help="run.json or the directory that holds it")
    parser.add_argument("--out", type=Path, help="default: ray-recording.json beside run.json")
    args = parser.parse_args()
    target = write_sidecar(args.run, args.out)
    print(json.dumps({"sidecar": str(target), "bytes": target.stat().st_size}))


if __name__ == "__main__":
    main()
