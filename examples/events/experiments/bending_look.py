"""The one-click look at THE BENDING (ALGEBRA.md #the-rows-against-nature (b); the Closer's word of 2026-09-28, 10:56 Israel): the two worlds of `bending/` run headless by the runner (`tools/run_inputs.py`, the expectation files beside them compared by it), then five lines from the outputs, Cheshbon's number before each reading and its verdict after: (1) DETECTOR, the centroid's shift of the strips' clicks against the twin (`tools/beam_centroid.py`); (2) GAMEBOARD, the redshift's ratio in the well (`tools/well_clocks.py`) with the twin's control; (3) the law's ratio, the level twice over once, beside the deflection angle read over the clock's shift (GAMEBOARD); (4) GAMEBOARD, the reversible row of both worlds; (5) GAMEBOARD, the bodies' centre pins and the run's books. Only the first line is a measurement. Run from the repository root, after the finish line: python examples/events/experiments/bending_look.py --out runs/bending; --look reads the outputs already there without running."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

import beam_centroid  # noqa: E402
import well_clocks  # noqa: E402

WORLDS = ("bending", "bending_twin")


def run(world_dir: Path, out_dir: Path) -> int:
    """Both worlds through the runner in one call, two processes, the summary lines printed by it; the runner's exit code."""
    command = [
        sys.executable,
        str(ROOT / "tools" / "run_inputs.py"),
        "--out",
        str(out_dir),
        "--jobs",
        "2",
    ]
    command += [str(world_dir / f"{name}.json") for name in WORLDS]
    environment = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    return subprocess.run(command, check=False, env=environment, cwd=ROOT).returncode


def decimal(pair: list[int] | None, places: int = 2) -> str:
    return "none" if pair is None else f"{float(Fraction(*pair)):.{places}f}"


def verdict(read: list[int] | None, expected: float | None, band: float) -> str:
    if read is None or expected is None:
        return "FIRST LOOK" if read is not None else "MISS (no reading)"
    return "MATCH" if abs(Fraction(*read) - Fraction(str(expected))) <= Fraction(str(band)) else "MISS"


def look(world_dir: Path, out_dir: Path) -> dict[str, Any]:
    """The five lines from the outputs beside the expectation files; the report returned with them."""
    paths = {name: (world_dir / f"{name}.json", out_dir / f"{name}.output.json") for name in WORLDS}
    outputs = {name: json.loads(paths[name][1].read_text(encoding="utf-8")) for name in WORLDS}
    expectation = json.loads(
        paths["bending"][0].with_suffix(".expectation.json").read_text(encoding="utf-8")
    )
    centroid = beam_centroid.report([paths["bending"], paths["bending_twin"]])
    wells = {name: well_clocks.report(*paths[name]) for name in WORLDS}
    row, well = expectation["CENTROID"], expectation["WELL"]
    shift = centroid.get("shift")
    ratio = wells["bending"]["shift_ratio"]
    clock = wells["bending"]["clock_cycle_shift"]
    angle = None if shift is None else Fraction(*shift) / int(row["screen_distance"])
    over_clock = (
        None if angle is None or not clock or Fraction(*clock) == 0 else angle / Fraction(*clock)
    )
    pins = {name: outputs[name].get("pins", []) for name in WORLDS}
    reversible = {
        name: [p["verdict"] for p in pins[name] if p.get("kind") == "reversible"] for name in WORLDS
    }
    centres = {name: [p["verdict"] for p in pins[name] if p.get("kind") == "centre"] for name in WORLDS}
    books = {name: centroid["this" if name == "bending" else "twin"] for name in WORLDS}
    lines = [
        f"1. DETECTOR   the centroid's shift, this minus the twin: {decimal(shift)} Links "
        f"(this {decimal(centroid['this']['centroid'])}, twin {decimal(centroid['twin']['centroid'])}); "
        f"before the run {row['shift']} within {row['band']} ({row['before_the_axis_pace_term']} before the axis-pace "
        f"term, the row's {row['row_as_written']}) -- {verdict(shift, row['shift'], row['band'])}",
        f"2. GAMEBOARD  the redshift's ratio, the light's wave number shift over the matter clock's cycle shift in "
        f"the well: {decimal(ratio)}; before the run {well['shift_ratio']} within {well['shift_ratio_band']} "
        f"({well['shift_ratio_before_the_conformal_term']} before the conformal term) -- "
        f"{verdict(ratio, well['shift_ratio'], well['shift_ratio_band'])}; the twin's control, its clock ratio "
        f"{decimal(wells['bending_twin']['clock_ratio'], 4)} (1)",
        f"3. THE LAW    the level twice over once: {row['level_twice_over_once']} ({row['shift']} / "
        f"{row['before_the_axis_pace_term']}, the algebra's line, no reading of one run); beside it GAMEBOARD, the "
        f"deflection angle read, shift / L = {decimal(None if angle is None else [angle.numerator, angle.denominator], 5)}, "
        f"over the clock's relative shift in the well {decimal(clock, 5)}: "
        f"{decimal(None if over_clock is None else [over_clock.numerator, over_clock.denominator])}",
        f"4. GAMEBOARD  the reversible row, the whole run forward and back: bending {reversible['bending']}, "
        f"twin {reversible['bending_twin']}",
        f"5. GAMEBOARD  the bodies at rest, the centre pins: bending {centres['bending']}, twin {centres['bending_twin']}; "
        f"the books: bending {books['bending']['clicks_in_strips']} clicks in the strips, "
        f"{books['bending']['clicks_elsewhere']} elsewhere, {books['bending']['records_alive']} records alive; twin "
        f"{books['bending_twin']['clicks_in_strips']} in the strips, {books['bending_twin']['clicks_elsewhere']} elsewhere",
    ]
    return {"kind": "the one-click look", "lines": lines, "centroid": centroid, "wells": wells}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[-1])
    parser.add_argument("--out", type=Path, required=True, help="the directory of the outputs")
    parser.add_argument("--look", action="store_true", help="read the outputs there without running")
    parser.add_argument("--worlds", type=Path, default=Path(__file__).resolve().parent / "bending")
    arguments = parser.parse_args(argv)
    if not arguments.look and run(arguments.worlds, arguments.out) != 0:
        print("the run is not LAWFUL in both worlds; the outputs name the refusal")
        return 1
    found = look(arguments.worlds, arguments.out)
    print("\n".join(found["lines"]))
    (arguments.out / "bending.look.json").write_text(
        json.dumps(found, indent=1) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
