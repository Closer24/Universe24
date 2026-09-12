"""Review saved trajectories and recheck faulted final states with the same engine."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from audit import HERE, classify, run_case

from event_universe.retention import ArtifactLease
from event_universe.runner import source_fingerprint


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    metadata = json.loads((args.input / "metadata.json").read_text())
    if metadata["source_fingerprint"] != source_fingerprint():
        raise ValueError("Review requires the recorded engine fingerprint")
    results = json.loads((args.input / "results.json").read_text())
    if len(results) != len(metadata["planned_cases"]):
        raise ValueError("The source suite is incomplete")
    args.output.mkdir(parents=True, exist_ok=False)
    with ArtifactLease(args.output.parent, [args.output]):
        reviewed = []
        for result in results:
            name = result["case"]
            source = args.input / name
            if result["fault"]:
                raw = json.loads((source / "initial.json").read_text())
                updated = run_case((name, raw, str(args.output)))
                if updated["trace_sha256"] != result["trace_sha256"]:
                    raise ValueError("Fault replay changed the physical event trace")
                updated["fault_replayed_with_final_state_check"] = True
            else:
                shutil.copytree(source, args.output / name)
                trajectory = json.loads((source / "trajectory.json").read_text())
                updated = {**result, **classify(trajectory, trajectory[-1]["probe"] is None, None)}
            (args.output / name / "result.json").write_text(json.dumps(updated, indent=2))
            reviewed.append(updated)
            print(name, updated["classification"], flush=True)
        metadata["reviewed_source_directory"] = str(args.input)
        metadata["experiment_files_sha256"] = {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.iterdir() if p.is_file()
        }
        (args.output / "metadata.json").write_text(json.dumps(metadata, indent=2))
        (args.output / "results.json").write_text(json.dumps(reviewed, indent=2))


if __name__ == "__main__":
    main()
