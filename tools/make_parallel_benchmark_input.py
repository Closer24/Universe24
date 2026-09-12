"""Build a dense local rational-interaction control from the existing reference law."""

import argparse
import json
from pathlib import Path

from event_universe.initialization import parse_initial_state
from event_universe.retention import ArtifactLease, validate_output_path

ROOT = Path(__file__).resolve().parents[1]


def configuration(cells=256, ticks=20):
    """Repeated held-pair scattering measures local work, not realistic trajectories."""
    if type(cells) is not int or cells < 1 or type(ticks) is not int or ticks < 0:
        raise ValueError("cells must be positive and ticks nonnegative integers")
    raw = json.loads((ROOT / "examples/particle-contracts/electron-proton.json").read_text())
    raw.update(
        model_id="held-rational-pair-performance-control-v1",
        shape=[cells, 1, 1],
        ticks=ticks,
        normal_budget=1_000_000_000,
    )
    for kind in raw["disturbance_types"]:
        kind["transport"] = {"mode": "hold"}
    for rule in raw["interactions"]:
        # Exercise the existing reversible local transaction on every cycle.
        rule.pop("when", None)
    raw["seeds"] = [
        {"position": [x, 0, 0], "type": kind["name"]}
        for x in range(cells)
        for kind in raw["disturbance_types"]
    ]
    parse_initial_state(raw)
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cells", type=int, default=256)
    parser.add_argument("--ticks", type=int, default=20)
    args = parser.parse_args()
    validate_output_path(args.output)
    if args.output.exists() and any(args.output.iterdir()):
        parser.error("benchmark input output directory must be empty")
    raw = configuration(args.cells, args.ticks)
    args.output.mkdir(parents=True, exist_ok=True)
    path = args.output / "rational-pairs.json"
    with ArtifactLease(args.output.parent, [args.output.resolve()]):
        path.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
    print(path.resolve())


if __name__ == "__main__":
    main()
