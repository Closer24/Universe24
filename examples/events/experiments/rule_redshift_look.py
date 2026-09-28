"""The one-click look at world (e) of the rule's own universe (ALGEBRA.md, THE RULE'S OWN UNIVERSE; the owner's decision of 2026-09-28, 13:02 Israel): the two worlds of `rule/` (`rule_redshift`, its twin) run headless by the runner (`tools/run_inputs.py`, the expectation files beside them compared by it), then five lines from the outputs, Cheshbon's number before each reading and its verdict after: (1) DETECTOR, the taker's mean click interval against the pin; (2) GAMEBOARD, the two pixels' clock ratio (`tools/well_clocks.py`) against Cheshbon's, with the twin's control; (3) GAMEBOARD, the light's periods beside each pixel (conserved in flight, the ratio 1) and its wavelengths (the stretch); (4) GAMEBOARD, the reversible row of both worlds; (5) GAMEBOARD, the pixels' centre pins and the books. Only the first line is a measurement. Run from the repository root: python examples/events/experiments/rule_redshift_look.py --out runs/rule_redshift; --look reads the outputs already there without running; --diagnostic labels every line GAMEBOARD (a run on an engine before the corrected giving)."""

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

import well_clocks  # noqa: E402

NAME = "rule_redshift"  # the world at Gamma 24 and its twin; --suffix _6000 names the run of record after it


def run(world_dir: Path, out_dir: Path, names: tuple[str, str]) -> int:
    """Both worlds through the runner in one call, two processes, the summary lines printed by it; the runner's exit code."""
    command = [
        sys.executable,
        str(ROOT / "tools" / "run_inputs.py"),
        "--out",
        str(out_dir),
        "--jobs",
        "2",
    ]
    command += [str(world_dir / f"{name}.json") for name in names]
    environment = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    return subprocess.run(command, check=False, env=environment, cwd=ROOT).returncode


def decimal(pair: list[int] | None, places: int = 3) -> str:
    return "none" if pair is None else f"{float(Fraction(*pair)):.{places}f}"


def verdict(read: list[int] | None, expected: float | None, band: float | None) -> str:
    if read is None:
        return "MISS (no reading)"
    if expected is None or band is None:
        return "FIRST LOOK"
    return "MATCH" if abs(Fraction(*read) - Fraction(str(expected))) <= Fraction(str(band)) else "MISS"


def look(world_dir: Path, out_dir: Path, diagnostic: bool, names: tuple[str, str]) -> dict[str, Any]:
    """The five lines from the outputs beside the expectation files; the report returned with them."""
    paths = {name: (world_dir / f"{name}.json", out_dir / f"{name}.output.json") for name in names}
    outputs = {name: json.loads(paths[name][1].read_text(encoding="utf-8")) for name in names}
    expectation = json.loads(
        paths[names[0]][0].with_suffix(".expectation.json").read_text(encoding="utf-8")
    )
    wells = {name: well_clocks.report(*paths[name]) for name in names}
    well, this = expectation["WELL"], wells[names[0]]
    pins = {name: outputs[name].get("pins", []) for name in names}
    clicks = {name: [p for p in pins[name] if p.get("kind") == "mean_interval"] for name in names}
    reversible = {
        name: [p["verdict"] for p in pins[name] if p.get("kind") == "reversible"] for name in names
    }
    centres = {name: [p["verdict"] for p in pins[name] if p.get("kind") == "centre"] for name in names}
    counts = {name: sum(int(c) for c in outputs[name].get("counts", {}).values()) for name in names}
    taker = clicks[names[0]][0] if clicks[names[0]] else None
    first = "GAMEBOARD " if diagnostic else "DETECTOR  "
    band = well.get("clock_ratio_band")
    lines = [
        f"1. {first} the taker's mean click interval: {'none' if taker is None else taker['read']} intervals "
        f"(the twin's {'none' if not clicks[names[1]] else clicks[names[1]][0]['read']}); before the run "
        f"{'none' if taker is None else taker['pin']} within {'none' if taker is None else taker['band']} -- "
        f"{'MISS (no pin)' if taker is None else taker['verdict']}",
        f"2. GAMEBOARD  the pixels' clock ratio, {well['clocks'][0]} over {well['clocks'][1]}: {decimal(this['clock_ratio'])} "
        f"(the cycles {decimal(this['clock_cycles'][0])} and {decimal(this['clock_cycles'][1])}); before the run "
        f"{well.get('clock_ratio')} ({well.get('clock_ratio_with_the_term')} with the term, the giver's period "
        f"{well.get('giver_period')}) -- {verdict(this['clock_ratio'], well.get('clock_ratio'), band)}; the twin's "
        f"control {decimal(wells[names[1]]['clock_ratio'])} (1)",
        f"3. GAMEBOARD  the light beside each pixel: the periods {decimal(this['light_periods'][0])} and "
        f"{decimal(this['light_periods'][1])}, their ratio {decimal(this['light_period_ratio'])} (conserved: 1); the "
        f"wavelengths {[decimal(w['wavelength']) for w in this['wavelengths']]}, the wave number's shift "
        f"{decimal(this['light_wave_number_shift'])}, over the clock's {decimal(this['clock_cycle_shift'])}: "
        f"{decimal(this['shift_ratio'])}; before the run {well.get('shift_ratio')}",
        f"4. GAMEBOARD  the reversible row, the whole run forward and back: {names[0]} {reversible[names[0]]}, "
        f"twin {reversible[names[1]]}",
        f"5. GAMEBOARD  the pixels on their Nodes, the centre pins: {names[0]} {centres[names[0]]}, twin "
        f"{centres[names[1]]}; the books: {counts[names[0]]} clicks, {outputs[names[0]].get('records_alive')} "
        f"records alive; twin {counts[names[1]]} clicks, {outputs[names[1]].get('records_alive')} alive",
    ]
    if diagnostic:
        lines.insert(
            0,
            "DIAGNOSTIC (GAMEBOARD): a run on an engine before the corrected giving, no number against the expectation",
        )
    return {"kind": "the one-click look", "diagnostic": diagnostic, "lines": lines, "wells": wells}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[-1])
    parser.add_argument("--out", type=Path, required=True, help="the directory of the outputs")
    parser.add_argument("--look", action="store_true", help="read the outputs there without running")
    parser.add_argument("--diagnostic", action="store_true", help="label every line GAMEBOARD")
    parser.add_argument("--worlds", type=Path, default=Path(__file__).resolve().parent / "rule")
    parser.add_argument(
        "--suffix", default="", help="the worlds' name suffix: _6000 for the run of record after 24"
    )
    arguments = parser.parse_args(argv)
    names = (f"{NAME}{arguments.suffix}", f"{NAME}{arguments.suffix}_twin")
    if not arguments.look and run(arguments.worlds, arguments.out, names) != 0:
        print("the run is not LAWFUL in both worlds; the outputs name the refusal")
        return 1
    found = look(arguments.worlds, arguments.out, arguments.diagnostic, names)
    print("\n".join(found["lines"]))
    (arguments.out / f"{names[0]}.look.json").write_text(
        json.dumps(found, indent=1) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
