"""Freeze the exact source bytes used for a bounded research execution."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

from research.experiments.run import write_json

ROOT = Path(__file__).resolve().parents[2]


def freeze_sources(output, paths, *, metadata=None):
    """Copy explicit repository sources before execution and retain their hashes.

    The caller declares all producer dependencies, frozen protocols, seeds,
    tensor, geometry and budgets in metadata. This is provenance, not an
    acceptance rule. No board or recording is read or changed here.
    """
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError("Refusing to overwrite " + str(output))
    selected = sorted({(ROOT / path).resolve() for path in paths})
    if not selected:
        raise ValueError("Explicit executed source files are required")
    payloads = {}
    for path in selected:
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError("Source must be a repository file: " + str(path))
        if path.is_relative_to(output):
            raise ValueError("Snapshot cannot contain itself")
        payloads[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    manifest = {
        "format": "universe24-clock-selection-source-snapshot-v1",
        "base_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "base_tree": subprocess.check_output(
            ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip(),
        "working_status": subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            cwd=ROOT, text=True),
        "source_sha256": {name: hashlib.sha256(data).hexdigest()
                          for name, data in payloads.items()},
        "environment": {"python": platform.python_version(),
                        "interpreter": sys.executable,
                        "platform": platform.platform(), "machine": platform.machine(),
                        "logical_processors": os.cpu_count()},
        "metadata": {} if metadata is None else metadata,
        "scientific_acceptance": "Not evaluated by source preservation",
    }
    output.mkdir(parents=True, exist_ok=False)
    for name, data in payloads.items():
        target = output / "source" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    write_json(output / "manifest.json", manifest)
    if not verify_sources(output)["live_sources_unchanged"]:
        raise RuntimeError("Source changed while it was being preserved")
    return manifest


def verify_sources(snapshot):
    """Check archived and live bytes separately; return all mismatches."""
    snapshot = Path(snapshot).resolve()
    manifest = json.loads((snapshot / "manifest.json").read_text())
    if manifest.get("format") != "universe24-clock-selection-source-snapshot-v1":
        raise ValueError("Unsupported source snapshot")
    archived, live = [], []
    for name, expected in manifest["source_sha256"].items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Invalid source path")
        for base, failures in ((snapshot / "source", archived), (ROOT, live)):
            path = base / relative
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                failures.append(name)
    return {"files": len(manifest["source_sha256"]),
            "archive_verified": not archived,
            "live_sources_unchanged": not live,
            "archive_mismatches": archived, "live_mismatches": live}
