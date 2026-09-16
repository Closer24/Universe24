"""Run a finite coherent-mode benchmark through the active generic engine.

This module prepares input and reads recorded output. All physical transitions
remain configured expressions evaluated by event_universe.Simulation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from event_universe.runner import run_initialization

PHASE_MATRICES = {
    "zero": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    "quarter": [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
    "half": [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
}


def configuration(phase: str = "zero", amplitude: int = 25) -> dict:
    """Select an immutable phase law and initial numerator before execution."""
    raw = json.loads(Path(__file__).with_name("initialization.json").read_text())
    raw["seeds"][0]["values"]["amplitude"] = [amplitude, 0, 0]
    expression = raw["disturbance_types"][1]["updates"][2]["expression"]
    expression["args"][1]["args"][1]["matrix"] = PHASE_MATRICES[phase]
    return raw


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=tuple(PHASE_MATRICES), default="zero")
    parser.add_argument("--amplitude", type=int, default=25)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    initialization = args.output / "input.json"
    initialization.write_text(json.dumps(configuration(args.phase, args.amplitude), indent=2) + "\n")
    # The requested HTML comes from the same run and the existing renderer.
    result = run_initialization(initialization, args.output / "run", visualize=True)
    print(result)


if __name__ == "__main__":
    main()
