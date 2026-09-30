"""Bell's reader by the comb (DETECTOR, the one measurement; ALGEBRA.md row (h); the advisor, #1515 comment 5909819308): a run's output read against Bell's world's expectation file, per pair the landings on each screen and their outcomes at the settings, and over the train the correlation E at every pair of settings, S at the CHSH settings, the coincidence fringe's visibility and each screen's single-side pattern, beside the blind row; the readings of several runs pooled. Every number is the world's files' and the run's output's: the two screens are the expectation's detectors (`sides`), the pairs the expectation's list, each with the interval its two peaks reach the screens' near faces (`peak`) and its window for reference, the pace the expectation's ([Links, intervals]); a click line on a screen (a landing) belongs to the pair whose peak passes its Node nearest in time, the distance measured from the screen's near face along the beam (`along`, the source at `source`, the near face the screen's Node nearest it); a landing's outcome at a setting a (a position on its screen in Links) is +1 where cos(Phi(y) - a) > 0 and -1 under, Phi(y) = 2 pi (y - `fringe_centre`) / `spacing` the fringe phase of its row, read in integers as the quarter turns of (y - fringe_centre - a) about the spacing; a pair's outcome on a screen is the sign of its landings' outcomes summed (none where they cancel); E(a, b) is the mean over the pairs with an outcome on both screens of the product of the left outcome at a and the right outcome at b; S = E(a, b) - E(a, b') + E(a', b) + E(a', b') with a, a' the left settings and b, b' the right ones; the coincidence fringe is those pairs' landings binned by the rows' phase sum over `bins` bins of the turn, its visibility (most - least) over (most + least); the tool holds no number.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/bell_clicks.py --world <world>.json --output <world>.output.json --expectation <expectation>.json
    PYTHONPATH=src python tools/bell_clicks.py --pool <reading>.json ...
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from event_universe.loader.keys import AXES
from event_universe.world_files import load_world


def nearest(peaks: list[int], pace: tuple[int, int], away: int, tick: int) -> int:
    """The pair whose peak passes a Node `away` Links beyond the screen's near face nearest to `tick`: the peak reaches the near face at `peaks[k]` and moves `pace` Links per `pace` intervals; the earliest of equals."""
    links, intervals = pace
    return min(range(len(peaks)), key=lambda k: (abs(links * (tick - peaks[k]) - intervals * away), k))


def comb(row: int, centre: int, setting: int, spacing: int) -> int:
    """A landing's outcome at a setting: +1 where cos(Phi(y) - a) > 0 and -1 under, with Phi(y) - a = 2 pi (y - centre - a) / spacing, so +1 where (y - centre - a) taken about the spacing lies within a quarter turn of 0 on either side."""
    turned = (row - centre - setting) % spacing
    return 1 if 2 * 2 * turned < spacing or 2 * 2 * turned > 3 * spacing else -1


def sign(total: int) -> int:
    """The sign of a sum of outcomes, 0 where they cancel."""
    return (total > 0) - (total < 0)


def correlations(pairs: list[dict[str, Any]], settings: dict[str, list[int]]) -> dict[str, list[int]]:
    """E at every pair of a left and a right setting over the pairs with an outcome on both screens, as [numerator, denominator]."""
    found = {}
    for i, a in enumerate(settings["a"]):
        for j, b in enumerate(settings["b"]):
            products = [
                pair["outcomes"]["left"][i] * pair["outcomes"]["right"][j]
                for pair in pairs
                if "left" in pair["outcomes"] and "right" in pair["outcomes"]
            ]
            value = Fraction(sum(products), len(products)) if products else Fraction(0)
            found[f"{a} {b}"] = [value.numerator, value.denominator]
    return found


def summary(
    pairs: list[dict[str, Any]], expected: dict[str, Any], landings: dict[str, dict[str, int]]
) -> dict[str, object]:
    """The summary over the pairs: E, S, the coincidences, the coincidence fringe's bins and visibility, the single-side patterns, beside the blind row."""
    settings = {side: [int(v) for v in values] for side, values in expected["settings"].items()}
    correlation = correlations(pairs, settings)
    (a, a_prime), (b, b_prime) = settings["a"], settings["b"]
    e = {key: Fraction(*value) for key, value in correlation.items()}
    s_value = e[f"{a} {b}"] - e[f"{a} {b_prime}"] + e[f"{a_prime} {b}"] + e[f"{a_prime} {b_prime}"]
    spacing, centre, bins = (
        int(expected["spacing"]),
        int(expected["fringe_centre"]),
        int(expected["bins"]),
    )
    counts = [0] * bins
    for pair in pairs:
        if "left" in pair["outcomes"] and "right" in pair["outcomes"]:
            for left in pair["landings"]["left"]:
                for right in pair["landings"]["right"]:
                    phase = (left - centre + right - centre) % spacing
                    counts[phase * bins // spacing] += 1
    most, least = max(counts), min(counts)
    visibility = Fraction(most - least, most + least) if most + least else Fraction(0)
    return {
        "verdict": "DETECTOR",
        "family": expected["family"],
        "settings": settings,
        "degrees": expected.get("degrees"),
        "pairs": pairs,
        "coincidences": sum(
            1 for pair in pairs if "left" in pair["outcomes"] and "right" in pair["outcomes"]
        ),
        "landings": {side: sum(rows.values()) for side, rows in landings.items()},
        "pattern": {
            side: [rows.get(y, 0) for y in range(max(rows, default=-1) + 1)]
            for side, rows in landings.items()
        },
        "correlation": correlation,
        "S": [s_value.numerator, s_value.denominator],
        "coincidence_fringe": counts,
        "visibility": [visibility.numerator, visibility.denominator],
        "blind": expected.get("blind"),
        "nature": expected.get("nature"),
        "bound": expected.get("bound"),
    }


def reading(world: Path, output: Path, expectation: Path) -> dict[str, object]:
    """The reading of one run: per pair the landings' rows on each screen, attributed by the nearest peak, and its outcomes at that screen's settings; then the summary."""
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    lines = json.loads(output.read_text(encoding="utf-8"))["lines"]
    loaded = load_world(world)
    along, across = AXES.index(expected["along"]), AXES.index(expected["across"])
    source, centre, spacing = (
        int(expected["source"]),
        int(expected["fringe_centre"]),
        int(expected["spacing"]),
    )
    sides: dict[str, str] = {side: str(name) for side, name in expected["sides"].items()}
    rows = {row.name: row for row in loaded.detectors}
    near = {
        side: min((node[along] for node in rows[name].positions), key=lambda x: abs(x - source))
        for side, name in sides.items()
    }
    peaks = [int(pair["peak"]) for pair in expected["pairs"]]
    pace = (int(expected["pace"][0]), int(expected["pace"][1]))
    settings = {side: [int(v) for v in values] for side, values in expected["settings"].items()}
    by_side = {"left": "a", "right": "b"}
    landed: list[dict[str, list[int]]] = [{side: [] for side in sides} for _ in peaks]
    pattern: dict[str, dict[int, int]] = {side: {} for side in sides}
    for line in lines:
        if line.get("event") != "click" or line.get("family") != expected["family"]:
            continue
        side = next((side for side, name in sides.items() if line.get("detector") == name), None)
        if side is None:
            continue
        node = [int(i) for i in list(line["node"])]  # type: ignore[call-overload]
        k = nearest(peaks, pace, abs(node[along] - near[side]), int(str(line["tick"])))
        landed[k][side].append(node[across])
        pattern[side][node[across]] = pattern[side].get(node[across], 0) + 1
    pairs = []
    for k, pair in enumerate(expected["pairs"]):
        outcomes = {}
        for side in sides:
            totals = [
                sum(comb(y, centre, a, spacing) for y in landed[k][side])
                for a in settings[by_side[side]]
            ]
            if landed[k][side] and all(sign(total) for total in totals):
                outcomes[side] = [sign(total) for total in totals]
        pairs.append({**pair, "landings": landed[k], "outcomes": outcomes})
    return summary(pairs, expected, pattern)


def pooled(readings: list[Path]) -> dict[str, object]:
    """The readings of several runs of one world pooled: their pairs together under the first reading's expectation numbers."""
    documents = [json.loads(path.read_text(encoding="utf-8")) for path in readings]
    first = documents[0]
    pairs = [pair for document in documents for pair in document["pairs"]]
    landings: dict[str, dict[str, int]] = {}
    for document in documents:
        for side, rows in document["pattern"].items():
            kept = landings.setdefault(side, {})
            for y, count in enumerate(rows):
                kept[y] = kept.get(y, 0) + count
    expected = {key: first[key] for key in ("family", "settings", "degrees", "blind", "nature", "bound")}
    expected.update(spacing=first["spacing"], fringe_centre=first["fringe_centre"], bins=first["bins"])
    return summary(
        pairs, expected, {side: {int(y): n for y, n in rows.items()} for side, rows in landings.items()}
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--world", type=Path, help="the world file the run ran")
    parser.add_argument("--output", type=Path, help="the run's output file")
    parser.add_argument("--expectation", type=Path, help="the blind expectation file")
    parser.add_argument("--pool", type=Path, nargs="*", help="readings of several runs to pool")
    args = parser.parse_args(argv)
    if args.pool:
        print(json.dumps(pooled(args.pool)))
        return
    if not (args.world and args.output and args.expectation):
        parser.error("a reading needs --world, --output and --expectation, or --pool the readings")
    found = reading(args.world, args.output, args.expectation)
    found.update(spacing=json.loads(args.expectation.read_text(encoding="utf-8"))["spacing"])
    found.update(fringe_centre=json.loads(args.expectation.read_text(encoding="utf-8"))["fringe_centre"])
    found.update(bins=json.loads(args.expectation.read_text(encoding="utf-8"))["bins"])
    print(json.dumps(found))


if __name__ == "__main__":
    main()
