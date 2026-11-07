"""Describe all retained confirmation-search recordings for generic replay."""
import argparse
import hashlib
import json
from pathlib import Path

from research.signal_clocks.run import write_json


def package(directory):
    directory = Path(directory)
    protocol = directory / "protocol.frozen.json"
    summary = json.loads((directory / "result.json").read_text())
    entries = []
    for folder in sorted((directory / "cases").iterdir()):
        trace = folder / "states.jsonl"
        result_path = folder / "result.json"
        if not trace.exists() or not result_path.exists():
            raise ValueError("Incomplete retained run cannot be silently omitted: " + str(folder))
        result = json.loads(result_path.read_text())
        detector = result["locations"]["detector"]
        readouts = [{"id": f"memory-{a}-{b}", "label": label, "kind": "all_equal", "clauses": [
            {"address": detector[0], "component": "r", "equals": str(a)},
            {"address": detector[1], "component": "r", "equals": str(b)}]}
            for a, b, label in ((2, 4, "Initial remainder pair"), (4, 2, "Candidate waiting pair"), (0, 0, "Candidate confirmed pair"))]
        entries.append({"id": folder.name, "title": folder.name.replace("-", " "),
            "description": "A complete recording from a prospectively fixed waiting/confirmation search. No candidate in this family passed its strict four-control acceptance test. A momentary waiting or confirmed remainder pair alone is not acceptance. All 48 receiver-channel arithmetic events remain available. Other board nodes may click. No physical light or path approval is established.",
            "trace": str(trace.relative_to(directory)), "trace_sha256": hashlib.sha256(trace.read_bytes()).hexdigest(),
            "view": {"position": result["locations"]["origin"], "channel": 0}, "readouts": readouts})
    if len(entries) != summary["runs_completed"]:
        raise ValueError("Recorded experiment count differs from completed-run manifest")
    if summary["passing_cases"]:
        raise ValueError("This negative-family descriptor must be revised before packaging a positive result")
    descriptor = {"format": "universe24-signal-clock-presentation-v1", "title": "Confirmation search: complete negative families and controls",
        "protocol": {"path": "protocol.frozen.json", "sha256": hashlib.sha256(protocol.read_bytes()).hexdigest()},
        "cases": entries}
    write_json(directory / "presentation.json", descriptor)
    return {"directory": str(directory), "experiments": len(entries)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directories", nargs="+", type=Path)
    for directory in parser.parse_args().directories:
        print(json.dumps(package(directory)), flush=True)
