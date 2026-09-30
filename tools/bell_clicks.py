"""Bell's reader by the contrast (DETECTOR, the one measurement; ALGEBRA.md row (h); the owner's decision of 2026-09-30, 14:15, via the advisor, #1515 comments 5912822802 and 5912958018): the runs' output files read against Bell's expectation file. Per run and per side, each region of the screen (the expectation's `sides`, a region's name with its rows) has its share, what it saw over the run (the `seen` lines, the net inflow through its front boundary, the density that entered) over the side's total, and beside it its entries (the click lines); the two ports of a setting, the + and - outputs of the polariser, are the unions of the regions in the comb's two half-rows about the setting's position (+ on the rows from three before the position to four after it in each fringe, the half-row centred half a row above the position so that the regions of four rows tile the half-fringes), their shares the regions' shares summed (a region straddling a half-row's edge, at a curve position, weighted by the comb's mean over its rows); the contrast is their difference over their sum. The side credited by the sign (`sign` in the expectation, side A) credits every quantum to the larger port; the side declared by the contrast (`contrast`, side B) credits the larger port for the fraction of the run's quanta equal to the contrast, the quantile remainders per quantum, and counts nothing for the rest (a setting whose two ports share alike clicks not at all). Among the coincidences, E(a, b) is the product of the two sides' outcomes weighted by B's clicks over the runs, one run per pair angle; S = E(a, b) - E(a, b') + E(a', b) + E(a', b') at the settings; E as a curve in a + b at the curve's positions (the right side at its first setting); B's efficiency per setting is its clicks over its quanta. Beside it, for comparison, the reading by the shares (the draw between the ports by their shares, E the product of the two sides' marginals averaged over the runs). The single-side patterns per region, over W_c the quanta, are the GameBoard check (the fringes shifted by the run's angle). The settings, the regions, the family, the curve and the two sides' declarations are the expectation file's; the tool holds no number.

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
    """A row's outcome at a setting: +1 on the rows from a quarter fringe less one row before the setting's position to a quarter fringe after it (the half-row centred half a row above the position), taken about the spacing, and -1 on the other half of each fringe."""
    half = spacing // 2
    turned = (row - centre - setting + half // 2 - 1) % spacing
    return 1 if turned < half else -1


def weight(rows: list[int], centre: int, setting: int, spacing: int) -> Fraction:
    """A region's weight at a setting: the mean of its rows' outcomes, +1 or -1 where the region lies inside one half-fringe."""
    return Fraction(sum(comb(row, centre, setting, spacing) for row in rows), len(rows))


def pair(value: Fraction) -> list[int]:
    """A fraction as [numerator, denominator]."""
    return [value.numerator, value.denominator]


def sign(value: Fraction) -> int:
    """The sign of a fraction: +1, -1, or 0 at 0."""
    return (value > 0) - (value < 0)


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


def shares_of(seen: dict[str, int]) -> dict[str, Fraction]:
    """The regions' shares of a side's total, 0 everywhere where the side saw nothing."""
    total = sum(seen.values())
    return {name: Fraction(value, total) if total else Fraction(0) for name, value in seen.items()}


def ports(
    shares: dict[str, Fraction],
    rows: dict[str, list[int]],
    setting: int,
    centre: int,
    spacing: int,
) -> tuple[Fraction, Fraction]:
    """The two ports' shares at a setting: the + port's the regions' shares weighted by (1 + w) / 2 and the - port's by (1 - w) / 2, w the comb's mean over the region (a region inside one half-fringe wholly one port's)."""
    plus = minus = Fraction(0)
    for name, share in shares.items():
        w = weight(rows[name], centre, setting, spacing)
        plus += share * (1 + w) / 2
        minus += share * (1 - w) / 2
    return plus, minus


def contrast(plus: Fraction, minus: Fraction) -> Fraction:
    """The contrast of a setting's two ports: their difference over their sum, 0 where nothing arrived."""
    return abs(plus - minus) / (plus + minus) if plus + minus else Fraction(0)


def one_run(lines: list[dict[str, object]], expected: dict[str, Any], wall: int) -> dict[str, Any]:
    """One run's reading: per side the seen, the entries and the quanta per region, the side's quanta, and at each setting (and each curve position) the two ports' shares, the outcome (the larger port's sign), the contrast and the marginal (the + port's share less the - port's, the reading by the shares)."""
    centre, spacing = int(expected["fringe_centre"]), int(expected["spacing"])
    settings = {side: [int(v) for v in values] for side, values in expected["settings"].items()}
    curve = [int(v) for v in expected.get("curve", {}).get("links", [])]
    found: dict[str, Any] = {
        "seen": {},
        "entries": {},
        "quanta": {},
        "side_quanta": {},
        "outcome": {},
        "contrast": {},
        "marginal": {},
        "curve_outcome": {},
        "curve_contrast": {},
        "curve_marginal": {},
    }
    for side, regions in expected["sides"].items():
        rows = {name: [int(r) for r in value] for name, value in regions.items()}
        saw, entries = totals(lines, str(expected["family"]), list(rows))
        shares = shares_of(saw)
        found["seen"][side] = saw
        found["entries"][side] = entries
        found["quanta"][side] = {name: value // wall for name, value in saw.items()}
        found["side_quanta"][side] = sum(saw.values()) // wall
        for kind, positions in (("", settings[SIDE_SETTINGS[side]]), ("curve_", curve)):
            read = [ports(shares, rows, at, centre, spacing) for at in positions]
            found[f"{kind}outcome"][side] = [sign(plus - minus) for plus, minus in read]
            found[f"{kind}contrast"][side] = [contrast(plus, minus) for plus, minus in read]
            found[f"{kind}marginal"][side] = [plus - minus for plus, minus in read]
    return found


def clicks_of(run: dict[str, Any], side: str, kind: str = "") -> list[Fraction]:
    """A side's clicks per setting in one run: its quanta times the contrast where the side is declared by the contrast, and every quantum where it credits by the sign."""
    quanta = Fraction(run["side_quanta"][side])
    if run["by"][side] == "contrast":
        return [quanta * value for value in run[f"{kind}contrast"][side]]
    return [quanta for _ in run[f"{kind}contrast"][side]]


def reading(world: Path, outputs: list[Path], expectation: Path) -> dict[str, object]:
    """The reading of the runs: per run the outcomes, the contrasts and the clicks, and over the runs E at the settings among the coincidences (the outcomes' product weighted by the clicks of both sides), S, the curve in a + b, B's efficiency per setting, the reading by the shares beside it, the single-side patterns summed, and the blind rows."""
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
    by = {str(expected["sign"]): "sign", str(expected["contrast"]): "contrast"}
    if set(by) != set(expected["sides"]):
        raise ValueError(f"the expectation declares {by} for the sides {list(expected['sides'])}")
    settings = {side: [int(v) for v in values] for side, values in expected["settings"].items()}
    runs = []
    for path in outputs:
        run = one_run(json.loads(path.read_text(encoding="utf-8"))["lines"], expected, wall)
        run["by"] = by
        run["clicks"] = {side: clicks_of(run, side) for side in expected["sides"]}
        run["curve_clicks"] = {side: clicks_of(run, side, "curve_") for side in expected["sides"]}
        runs.append(run)
    count = len(runs)

    def coincidence(left: str, right: str, i: int, j: int) -> Fraction:
        """E over the runs at the left side's setting i and the right side's j: the outcomes' product weighted by the coincidences, the smaller of the two sides' clicks in each run."""
        weighted = total = Fraction(0)
        for run in runs:
            pairs = min(run[f"{left}clicks"]["left"][i], run[f"{right}clicks"]["right"][j])
            weighted += pairs * run[f"{left}outcome"]["left"][i] * run[f"{right}outcome"]["right"][j]
            total += pairs
        return weighted / total if total else Fraction(0)

    correlation = {
        f"{a} {b}": coincidence("", "", i, j)
        for i, a in enumerate(settings["a"])
        for j, b in enumerate(settings["b"])
    }
    (a, a_prime), (b, b_prime) = settings["a"], settings["b"]
    s_value = (
        correlation[f"{a} {b}"]
        - correlation[f"{a} {b_prime}"]
        + correlation[f"{a_prime} {b}"]
        + correlation[f"{a_prime} {b_prime}"]
    )
    curve_links = [int(v) for v in expected.get("curve", {}).get("links", [])]
    curve = [coincidence("curve_", "", i, 0) for i in range(len(curve_links))]
    efficiency = {
        side: [
            sum((run["clicks"][side][i] for run in runs), Fraction(0))
            / sum((Fraction(run["side_quanta"][side]) for run in runs), Fraction(0))
            if any(run["side_quanta"][side] for run in runs)
            else Fraction(0)
            for i in range(len(settings[SIDE_SETTINGS[side]]))
        ]
        for side in expected["sides"]
    }
    by_shares = {
        f"{a} {b}": sum(
            (run["marginal"]["left"][i] * run["marginal"]["right"][j] for run in runs), Fraction(0)
        )
        / count
        for i, a in enumerate(settings["a"])
        for j, b in enumerate(settings["b"])
    }
    by_shares_s = (
        by_shares[f"{a} {b}"]
        - by_shares[f"{a} {b_prime}"]
        + by_shares[f"{a_prime} {b}"]
        + by_shares[f"{a_prime} {b_prime}"]
    )
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
        "by": by,
        "correlation": {key: pair(value) for key, value in correlation.items()},
        "S": pair(s_value),
        "curve": [pair(value) for value in curve],
        "curve_at": {
            str(link + settings["b"][0]): pair(curve[index]) for index, link in enumerate(curve_links)
        },
        "efficiency": {side: [pair(v) for v in values] for side, values in efficiency.items()},
        "by_the_shares": {
            "correlation": {key: pair(value) for key, value in by_shares.items()},
            "S": pair(by_shares_s),
        },
        "per_run": [
            {
                "outcome": run["outcome"],
                "contrast": {
                    side: [pair(v) for v in values] for side, values in run["contrast"].items()
                },
                "clicks": {side: [pair(v) for v in values] for side, values in run["clicks"].items()},
                "marginal": {
                    side: [pair(v) for v in values] for side, values in run["marginal"].items()
                },
                "side_quanta": run["side_quanta"],
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
