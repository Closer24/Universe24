"""Run the preregistered candidate controls through the canonical simulator."""

import argparse
import json
from pathlib import Path

from joint_configuration import build_joint_document
from strong_configuration import build_strong_document

from event_universe.runner import run_initialization

NUCLEAR_CONTROLS = {
    "nuclear_capture": {},
    "nuclear_disabled": {"coupling": 0},
    "nuclear_boost": {"boost": 1, "emission": 0},
    "nuclear_subthreshold": {
        "initial_bound": 1,
        "emission": 0,
        "excitation_left": 334944581,
        "excitation_right": 334944582,
    },
    "nuclear_threshold_zero_kick": {
        "initial_bound": 1,
        "emission": 0,
        "excitation_left": 334944582,
        "excitation_right": 334944582,
    },
    "nuclear_dissociation": {
        "initial_bound": 1,
        "emission": 0,
        "release_kick": 940032,
        "excitation_left": 335414598,
        "excitation_right": 335414598,
    },
}


def run_document(document: dict, output: Path, *, carriers_only: bool = False) -> Path:
    """Save exactly one requested world, including raw every-tick states and HTML."""
    output.parent.mkdir(parents=True, exist_ok=True)
    initialization = output.parent / f"{output.name}-initialization.json"
    if initialization.exists():
        raise ValueError("preserve earlier initialization evidence; choose a fresh output name")
    initialization.write_text(json.dumps(document, indent=2) + "\n")
    content = "carriers" if carriers_only else "all"
    return run_initialization(
        initialization, output, visualize=True, state_trace=content, frame_content=content
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--suite", choices=("nuclear", "electron"), required=True)
    parser.add_argument("--ticks", type=int)
    parser.add_argument("--force-numerator", type=int)
    parser.add_argument("--force-denominator", type=int)
    args = parser.parse_args()
    if args.suite == "nuclear":
        for name, parameters in NUCLEAR_CONTROLS.items():
            document = build_strong_document(
                parameters=parameters,
                shape=(9, 9, 9),
                ticks=args.ticks if args.ticks is not None else 32,
            )
            print(run_document(document, args.output / name), flush=True)
    else:
        if args.force_numerator is None or args.force_denominator is None:
            parser.error("electron runs require the published calibration coefficient")
        document = build_joint_document(
            electron_parameters={
                "force_numerator": args.force_numerator,
                "force_denominator": args.force_denominator,
            },
            shape=(41, 41, 41),
            ticks=args.ticks if args.ticks is not None else 832,
        )
        print(run_document(document, args.output, carriers_only=True), flush=True)


if __name__ == "__main__":
    main()
