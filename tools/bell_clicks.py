"""Bell's reader (DETECTOR, the one measurement; ALGEBRA.md row (h); the advisor's design at the owner's word of 2026-09-30, #1515 comments 5912573191 and 5911802610): the runs' output files read against Bell's expectation file. Per run and per side, each region of the screen (the expectation's `sides`, a region's name with its rows) has its share, what it saw over the run (the `seen` lines, the net inflow at its boundary, the amplitudes the instrument saw) over the side's total, and beside it its entries (the click lines); the comb on a half-row about a setting's position, +1 on the rows y_a - 4 to y_a + 3 of each fringe and -1 on the other eight, gives every region a weight, the mean of its rows' outcomes (+1 or -1 inside one half-fringe); the marginal at a setting is the sum over the regions of the weight times the share, the + output's share less the - output's, the two detectors of the setting; E(a, b) is the product of the two sides' marginals, the sides independent given the record, S = E(a, b) - E(a, b') + E(a', b) + E(a', b') at the settings, and E as a curve in a + b at the curve's positions (the right side at its first setting); over the runs, one per angle, E, S and the curve are averaged, exact in fractions. The single-side patterns per region, over W_c the quanta, are the GameBoard check (the fringes at the spacing, shifted by the run's angle). The settings, the regions, the family and the curve are the expectation file's; the tool holds no number.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/bell_clicks.py --world <world>.json --expectation <expectation>.json --outputs <run>.output.json ...
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world

SIDE_SETTINGS = {"left": "a", "right": "b"}  # the settings' names per side in the expectation


def comb(row: int, centre: int, setting: int, spacing: int) -> int:
    """A row's outcome at a setting: +1 on the rows from a quarter fringe before the setting's position to a quarter fringe after it, taken about the spacing, and -1 on the other half of each fringe."""
    half = spacing // 2
    turned = (row - centre - setting + half // 2) % spacing
    return 1 if turned < half else -1


def weight(rows: list[int], centre: int, setting: int, spacing: int) -> Fraction:
    """A region's weight at a setting: the mean of its rows' outcomes, +1 or -1 where the region lies inside one half-fringe."""
    return Fraction(sum(comb(row, centre, setting, spacing) for row in rows), len(rows))


def pair(value: Fraction) -> list[int]:
    """A fraction as [numerator, denominator]."""
    return [value.numerator, value.denominator]


def totals(
    lines: list[dict[str, object]], family: str, regions: list[str]
) -> tuple[dict[str, int], dict[str, int]]:
    """Per region what it saw over the run (the `seen` lines' net inflows summed) and its entries (the click lines counted), of one family."""
    saw = {name: 0 for name in regions}
    entries = {name: 0 for name in regions}
    for line in lines:
        if line.get("family") != family or line.get("detector") not in saw:
            continue
        name = str(line["detector"])
        if line.get("event") == "seen":
            saw[name] += int(str(line["inflow"]))
        elif line.get("event") == "click":
            entries[name] += 1
    return saw, entries


def marginals(
    shares: dict[str, Fraction],
    rows: dict[str, list[int]],
    settings: list[int],
    centre: int,
    spacing: int,
) -> list[Fraction]:
    """A side's marginals at its settings: the weighted sum over its regions of the comb's weight times the region's share."""
    return [
        sum(
            (weight(rows[name], centre, setting, spacing) * share for name, share in shares.items()),
            Fraction(0),
        )
        for setting in settings
    ]


def shares_of(seen: dict[str, int]) -> dict[str, Fraction]:
    """The regions' shares of a side's total, 0 everywhere where the side saw nothing."""
    total = sum(seen.values())
    return {name: Fraction(value, total) if total else Fraction(0) for name, value in seen.items()}


def one_run(lines: list[dict[str, object]], expected: dict[str, Any], wall: int) -> dict[str, Any]:
    """One run's reading: per side the seen and the entries per region, the shares, the marginals at the settings and at the curve's positions, and E at the settings' products."""
    centre, spacing = int(expected["fringe_centre"]), int(expected["spacing"])
    settings = {side: [int(v) for v in values] for side, values in expected["settings"].items()}
    curve = [int(v) for v in expected.get("curve", {}).get("links", [])]
    found: dict[str, Any] = {
        "seen": {},
        "entries": {},
        "quanta": {},
        "marginals": {},
        "curve_marginals": {},
    }
    for side, regions in expected["sides"].items():
        rows = {name: [int(r) for r in value] for name, value in regions.items()}
        saw, entries = totals(lines, str(expected["family"]), list(rows))
        shares = shares_of(saw)
        found["seen"][side] = saw
        found["entries"][side] = entries
        found["quanta"][side] = {name: value // wall for name, value in saw.items()}
        found["marginals"][side] = marginals(
            shares, rows, settings[SIDE_SETTINGS[side]], centre, spacing
        )
        found["curve_marginals"][side] = marginals(shares, rows, curve, centre, spacing)
    left, right = found["marginals"]["left"], found["marginals"]["right"]
    found["correlation"] = {
        f"{a} {b}": left[i] * right[j]
        for i, a in enumerate(settings["a"])
        for j, b in enumerate(settings["b"])
    }
    first_right = found["curve_marginals"]["right"][0] if curve else Fraction(0)
    found["curve"] = [value * first_right for value in found["curve_marginals"]["left"]]
    return found


def reading(world: Path, outputs: list[Path], expectation: Path) -> dict[str, object]:
    """The reading of the runs: per run the marginals and E, and over the runs E at the settings, S, the curve in a + b, the single-side patterns summed, beside the blind rows."""
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    loaded = load_world(world)
    family = next(f for f in loaded.families if f.name == expected["family"])
    wall = count_wall(family, loaded.quantum_action)
    declared = {row.name for row in loaded.detectors}
    for side, regions in expected["sides"].items():
        if not set(regions) <= declared:
            raise ValueError(
                f"the expectation's {side} regions {sorted(regions)} are not the world's detectors"
            )
    settings = {side: [int(v) for v in values] for side, values in expected["settings"].items()}
    runs = [
        one_run(json.loads(path.read_text(encoding="utf-8"))["lines"], expected, wall)
        for path in outputs
    ]
    count = len(runs)
    correlation = {
        key: sum((run["correlation"][key] for run in runs), Fraction(0)) / count
        for key in runs[0]["correlation"]
    }
    (a, a_prime), (b, b_prime) = settings["a"], settings["b"]
    s_value = (
        correlation[f"{a} {b}"]
        - correlation[f"{a} {b_prime}"]
        + correlation[f"{a_prime} {b}"]
        + correlation[f"{a_prime} {b_prime}"]
    )
    curve = [
        sum((run["curve"][at] for run in runs), Fraction(0)) / count
        for at in range(len(runs[0]["curve"]))
    ]
    patterns = {
        side: {name: sum(run["quanta"][side][name] for run in runs) for name in expected["sides"][side]}
        for side in expected["sides"]
    }
    return {
        "verdict": "DETECTOR",
        "family": expected["family"],
        "runs": count,
        "settings": settings,
        "degrees": expected.get("degrees"),
        "correlation": {key: pair(value) for key, value in correlation.items()},
        "S": pair(s_value),
        "curve": [pair(value) for value in curve],
        "curve_at": {
            str(link): pair(curve[index])
            for index, link in enumerate(expected.get("curve", {}).get("links", []))
        },
        "per_run": [
            {
                "marginals": {
                    side: [pair(v) for v in values] for side, values in run["marginals"].items()
                },
                "correlation": {key: pair(value) for key, value in run["correlation"].items()},
                "quanta": run["quanta"],
                "entries": run["entries"],
            }
            for run in runs
        ],
        "patterns": patterns,
        "entries": {
            side: {
                name: sum(run["entries"][side][name] for run in runs) for name in expected["sides"][side]
            }
            for side in expected["sides"]
        },
        "blind": expected.get("blind"),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--world", type=Path, required=True, help="one of the runs' world files (the detectors)"
    )
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    parser.add_argument(
        "--outputs", type=Path, nargs="+", required=True, help="the runs' output files, one per angle"
    )
    args = parser.parse_args(argv)
    print(json.dumps(reading(args.world, args.outputs, args.expectation)))


if __name__ == "__main__":
    main()
