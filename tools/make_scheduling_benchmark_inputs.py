"""Write ordinary sparse and dense initialization files for scheduler comparisons."""

import argparse
import json
from pathlib import Path

from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_initial_state
from event_universe.retention import ArtifactLease, validate_output_path


def configuration(sparse):
    return {
        "schema_version": 1,
        "model_id": "scheduler-comparison-v1",
        "shape": [10000, 12, 1],
        "slots_per_cell": 4,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": 500 if sparse else 100,
        "operation_costs": {operation: 1 for operation in OPERATIONS},
        "fields": [
            {
                "name": "inventory",
                "components": 1,
                "units": "configured unit",
                "signed": True,
                "conserved": True,
            }
        ],
        "disturbance_types": [
            {
                "name": "parcel",
                "fields": ["inventory"],
                "defaults": {"inventory": 1},
                "transport": (
                    {"mode": "move", "weights": [1, 0, 0, 0, 0, 0]} if sparse else {"mode": "hold"}
                ),
                "updates": [],
            }
        ],
        "couplings": [],
        "seeds": [
            {"position": [x, y, 0], "type": "parcel"}
            for x in range(1 if sparse else 10)
            for y in range(1 if sparse else 10)
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    validate_output_path(args.output)
    if args.output.exists() and any(args.output.iterdir()):
        parser.error("benchmark input output directory must be empty")
    inputs = [
        (args.output / f"{name}.json", configuration(name == "sparse")) for name in ("sparse", "dense")
    ]
    for path, raw in inputs:
        if path.exists():
            parser.error(f"benchmark input already exists: {path}")
        parse_initial_state(raw)
    args.output.mkdir(parents=True, exist_ok=True)
    with ArtifactLease(args.output.parent, [args.output.resolve()]):
        for path, raw in inputs:
            path.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
            print(path.resolve())


if __name__ == "__main__":
    main()
