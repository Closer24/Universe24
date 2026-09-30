"""Bell's reading (ALGEBRA.md row (h); the owner's decision of 2026-09-30, 14:15, Bell by the detector's contrast, #1515 comment 5912822802; the advisor's corrected instrument, #1563 comment 5918198102, the setting as the comb's shift, 5918297124): eight runs, one per pair angle, each a world with the pair's angle laid as the two lobes' relative phase, read against the blind expectation file. Per run and side the ports at each setting are unions of the screen's regions the expectation names (the + port about the central maximum, the - port about the two first minima, displaced by the setting), each port's inflow its regions' net front inflows summed over the run (the `seen` lines). The ports are calibrated over the eight runs (the advisor): P_+ and P_- their mean inflows at that setting, d = s_+ / P_+ - s_- / P_- per run, D half its swing over the runs; the outcome is the sign of d and the contrast |d| / D. The side the file names `sign` credits every quantum in its ports to the larger port; the side it names `contrast` credits the larger port for the fraction of its quanta equal to the contrast and counts nothing for the rest. E(a, b) among the coincidences over the runs (the outcomes' product weighted by the smaller of the two sides' clicks), S at the CHSH settings, the efficiency per side and setting (the clicks over the light in the ports), the settings' phases calibrated from the same runs (the advisor, 5918622391: the calibrated difference over the run phases fitted to A cos(u - delta), delta the setting's phase, the mirror on the left) with E = cos(delta_A + delta_B) at them beside, the reading by the shares beside it (the product of the two sides' normalised differences), the single-side patterns per region (the quanta over W_c) and the visibility from the u = 0 world, all in exact fractions; the whole crossings at the regions' boundaries counted beside as the count's line's diagnostic, `crossings`. DETECTOR.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/bell_clicks.py --world examples/events/bell/bell_0.json --expectation examples/events/bell/expectation.json --outputs runs/bell/bell_v.output.json runs/bell/bell_0.output.json ...
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import atan2, cos, degrees, pi, sin
from pathlib import Path
from typing import Any

from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world

SIDE_SETTINGS = {"left": "b", "right": "a"}  # the side and its setting's name


def pair(value: Fraction) -> list[int]:
    """A fraction as [numerator, denominator] for the file."""
    return [value.numerator, value.denominator]


def sign(value: Fraction) -> int:
    """The sign of a difference: +1, -1, or 0 at a tie."""
    return (value > 0) - (value < 0)


def totals(
    lines: list[dict[str, object]], family: str, regions: list[str]
) -> tuple[dict[str, int], dict[str, int]]:
    """Per region what it saw over the run (the `seen` lines' net inflows summed) and its whole crossings (the click lines counted), of one family."""
    saw = {name: 0 for name in regions}
    crossings = {name: 0 for name in regions}
    for line in lines:
        if line.get("family") != family or line.get("detector") not in saw:
            continue
        name = str(line["detector"])
        if line.get("event") == "seen":
            saw[name] += int(str(line["inflow"]))
        elif line.get("event") == "click":
            crossings[name] += 1
    return saw, crossings


def one_run(lines: list[dict[str, object]], expected: dict[str, Any]) -> dict[str, Any]:
    """One run's totals: per side the seen and the whole crossings per region, and per setting the two ports' inflows (the regions the expectation names summed)."""
    found: dict[str, Any] = {"seen": {}, "crossings": {}, "ports": {}}
    for side, regions in expected["sides"].items():
        saw, crossings = totals(lines, str(expected["family"]), list(regions))
        found["seen"][side] = saw
        found["crossings"][side] = crossings
        found["ports"][side] = {
            setting: {port: sum(saw[name] for name in names) for port, names in ports.items()}
            for setting, ports in expected["ports"][side].items()
        }
    return found


def calibrated(runs: list[dict[str, Any]], side: str, setting: str, wall: int) -> dict[str, list[Any]]:
    """A side's ports at one setting calibrated over the runs (the advisor, #1563 comment 5918198102): the light in the ports per run in quanta, the difference d = s_+ / P_+ - s_- / P_- with P the ports' means, the outcome its sign, the contrast |d| over half its swing over the runs, and the normalised difference itself (the reading by the shares)."""
    plus = [Fraction(run["ports"][side][setting]["plus"]) for run in runs]
    minus = [Fraction(run["ports"][side][setting]["minus"]) for run in runs]
    mean_plus, mean_minus = sum(plus, Fraction(0)) / len(runs), sum(minus, Fraction(0)) / len(runs)
    difference = [
        (a / mean_plus if mean_plus else Fraction(0)) - (b / mean_minus if mean_minus else Fraction(0))
        for a, b in zip(plus, minus, strict=True)
    ]
    half_swing = (max(difference) - min(difference)) / 2
    normalised = [d / half_swing if half_swing else Fraction(0) for d in difference]
    return {
        "light": [(a + b) / wall for a, b in zip(plus, minus, strict=True)],
        "difference": difference,
        "outcome": [sign(d) for d in difference],
        "contrast": [abs(n) for n in normalised],
        "normalised": normalised,
    }


def phase_of(difference: list[Fraction], turns: int, side: str) -> float:
    """A setting's phase in radians: the calibrated difference over the runs, the run k at the pair's phase (k + 1/2) / turns of the turn (its mirror on the left), fitted to A cos(u - delta) by its first harmonic (the advisor, #1563 comment 5918622391); atan2 gives 0 where nothing was read."""
    mirror = -1 if side == "left" else 1
    angles = [mirror * 2 * pi * (k + Fraction(1, 2)) / turns for k in range(turns)]
    along = sum(float(d) * cos(u) for d, u in zip(difference, angles, strict=True))
    across = sum(float(d) * sin(u) for d, u in zip(difference, angles, strict=True))
    return atan2(across, along)


def reading(world: Path, outputs: list[Path], expectation: Path) -> dict[str, object]:
    """The reading of the runs against the expectation: the runs' ports calibrated per side and setting, the clicks (side A's light, side B's light times its contrast), E at the four settings among the coincidences, S, the efficiencies, the reading by the shares, the single-side patterns, the visibility from the u = 0 world and the whole crossings beside; the blind row copied from the expectation."""
    loaded = load_world(world)
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    family = next(f for f in loaded.families if f.name == expected["family"])
    wall = count_wall(family, loaded.quantum_action)
    runs, visibility_run = [], None
    for path in outputs:
        output = json.loads(path.read_text(encoding="utf-8"))
        name = Path(str(output["input"])).stem
        run = one_run(output["lines"], expected)
        run["name"] = name
        if name == expected.get("visibility_world"):
            visibility_run = run
        else:
            runs.append(run)
    runs.sort(key=lambda run: int(str(run["name"]).rsplit("_", 1)[1]))
    turns = len(runs)
    if expected["sign"] == expected["contrast"]:
        raise ValueError("the expectation declares one side by the sign and the other by the contrast")
    by = {expected["sign"]: "sign", expected["contrast"]: "contrast"}
    sides = {
        side: {setting: calibrated(runs, side, setting, wall) for setting in expected["ports"][side]}
        for side in expected["sides"]
    }
    clicks = {
        side: {
            setting: [
                light * (contrast if by[side] == "contrast" else 1)
                for light, contrast in zip(values["light"], values["contrast"], strict=True)
            ]
            for setting, values in settings.items()
        }
        for side, settings in sides.items()
    }
    phases = {
        side: {
            setting: phase_of(values["difference"], turns, side) for setting, values in settings.items()
        }
        for side, settings in sides.items()
    }
    correlation: dict[str, list[int]] = {}
    by_the_shares: dict[str, list[int]] = {}
    cosines: dict[str, float] = {}
    for a, right in sides["right"].items():
        for b, left in sides["left"].items():
            weights = [min(x, y) for x, y in zip(clicks["right"][a], clicks["left"][b], strict=True)]
            total = sum(weights)
            product = sum(
                oa * ob * w for oa, ob, w in zip(right["outcome"], left["outcome"], weights, strict=True)
            )
            correlation[f"{a} {b}"] = pair(product / total if total else Fraction(0))
            shares = sum(
                na * nb for na, nb in zip(right["normalised"], left["normalised"], strict=True)
            ) / len(runs)
            by_the_shares[f"{a} {b}"] = pair(shares)
            cosines[f"{a} {b}"] = round(cos(phases["right"][a] + phases["left"][b]), 3)
    (a, a_prime), (b, b_prime) = (list(sides["right"]), list(sides["left"]))
    e = {key: Fraction(*value) for key, value in correlation.items()}
    s_value = e[f"{a} {b}"] - e[f"{a} {b_prime}"] + e[f"{a_prime} {b}"] + e[f"{a_prime} {b_prime}"]
    efficiency = {
        side: {
            setting: pair(
                sum(clicks[side][setting]) / sum(values["light"])
                if sum(values["light"])
                else Fraction(0)
            )
            for setting, values in settings.items()
        }
        for side, settings in sides.items()
    }
    patterns = {
        side: {
            name: sum(run["seen"][side][name] for run in runs) // wall
            for name in expected["sides"][side]
        }
        for side in expected["sides"]
    }
    crossings = {
        side: {
            name: sum(run["crossings"][side][name] for run in runs) for name in expected["sides"][side]
        }
        for side in expected["sides"]
    }
    visibility = None
    if visibility_run is not None:
        visibility = {}
        for side in expected["sides"]:
            quanta = {name: Fraction(v, wall) for name, v in visibility_run["seen"][side].items()}
            top, bottom = max(quanta.values()), min(quanta.values())
            visibility[side] = pair((top - bottom) / (top + bottom) if top + bottom else Fraction(0))
    return {
        "verdict": "DETECTOR",
        "runs": [run["name"] for run in runs],
        "by": by,
        "settings": expected["settings"],
        "degrees": expected.get("degrees"),
        "per_run": [
            {
                "name": run["name"],
                "light": {
                    side: {k: pair(v["light"][i]) for k, v in s.items()} for side, s in sides.items()
                },
                "difference": {
                    side: {k: pair(v["difference"][i]) for k, v in s.items()}
                    for side, s in sides.items()
                },
                "outcome": {
                    side: {k: v["outcome"][i] for k, v in s.items()} for side, s in sides.items()
                },
                "contrast": {
                    side: {k: pair(v["contrast"][i]) for k, v in s.items()} for side, s in sides.items()
                },
            }
            for i, run in enumerate(runs)
        ],
        "correlation": correlation,
        "S": pair(s_value),
        "phases": {
            side: {k: round(degrees(v), 1) for k, v in v_side.items()} for side, v_side in phases.items()
        },
        "cosines": cosines,
        "S_cosines": round(
            cosines[f"{a} {b}"]
            - cosines[f"{a} {b_prime}"]
            + cosines[f"{a_prime} {b}"]
            + cosines[f"{a_prime} {b_prime}"],
            3,
        ),
        "efficiency": efficiency,
        "by_the_shares": {"correlation": by_the_shares},
        "patterns": patterns,
        "crossings": crossings,
        "visibility": visibility,
        "blind": expected["blind"],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--world", type=Path, required=True, help="one of the runs' world files")
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    parser.add_argument("--outputs", type=Path, nargs="+", required=True, help="the runs' output files")
    args = parser.parse_args(argv)
    print(json.dumps(reading(args.world, args.outputs, args.expectation), indent=1))


if __name__ == "__main__":
    main()
