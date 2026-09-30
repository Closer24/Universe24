"""Bell's reader by the comb (DETECTOR, the one measurement; ALGEBRA.md row (h); the advisor, #1515 comment 5910272948 C): a run's output read against Bell's world's expectation file. A landing is a click line on one of the two screens (the expectation's `sides`, the detectors' names) of the family, naming the whole that entered (`whole`, the whole line's: [message, n], the whole n of that message, or n alone); a pair is the two mirror wholes, the whole n of a message with the whole n of its mirror (`mirrors`, the expectation's rows of [left message, right message]; an n alone pairs across the sides). Every landing is an outcome: at a setting a (a position on the screen in Links) +1 where cos(Phi(y) - a) > 0 and -1 under, Phi(y) = 2 pi (y - `fringe_centre`) / `spacing` the fringe phase of its row, read in integers as (y - fringe_centre - a) about the spacing within a quarter turn of 0 on either side; a pair's outcome on a screen is the sign of its landings' outcomes summed (none where they cancel). E(a, b) is the mean over the pairs with an outcome on both screens of the product of the left outcome at a and the right outcome at b, at the expectation's settings (a and a' on the left, b and b' on the right), and S = E(a, b) - E(a, b') + E(a', b) + E(a', b'); E as a curve in a + b is E over every pair of positions, averaged by a + b about the spacing, with its values at the expectation's sums (`curve.links`); the coincidence map is the coincident pairs' landings binned by Phi_A + Phi_B over `bins` bins of the turn (the ridge), its visibility (most - least) over (most + least); each screen's single-side pattern is its landings per row with the local maxima; the GameBoard check counts the pairs with one landing on each screen and those at mirror rows (y_A + y_B twice the centre); a landing naming no whole counts in the pattern alone. The tool holds no number.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/bell_clicks.py --world <world>.json --output <world>.output.json --expectation <expectation>.json
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from event_universe.loader.keys import AXES
from event_universe.world_files import load_world

SIDE_SETTINGS = {"left": "a", "right": "b"}  # the settings' names per side in the expectation


def comb(row: int, centre: int, setting: int, spacing: int) -> int:
    """A landing's outcome at a setting: +1 where cos(Phi(y) - a) > 0 and -1 under, with Phi(y) - a = 2 pi (y - centre - a) / spacing, so +1 where (y - centre - a) taken about the spacing lies within a quarter turn of 0 on either side."""
    turned = (row - centre - setting) % spacing
    return 1 if 2 * 2 * turned < spacing or 2 * 2 * turned > 3 * spacing else -1


def sign(total: int) -> int:
    """The sign of a sum of outcomes, 0 where they cancel."""
    return (total > 0) - (total < 0)


def outcome(rows: list[int], centre: int, setting: int, spacing: int) -> int:
    """A pair's outcome on one screen at a setting: the sign of its landings' outcomes summed."""
    return sign(sum(comb(row, centre, setting, spacing) for row in rows))


def pair_of(whole: object, mirrors: list[list[int]]) -> tuple[int, int] | None:
    """The pair a landing's whole belongs to: [message, n] is the whole n of the mirrors' row holding that message, n alone the pair (0, n); None where the whole names no mirrored message."""
    if isinstance(whole, int):
        return (0, whole)
    if not isinstance(whole, list) or len(whole) != 2:
        return None
    message, index = int(whole[0]), int(whole[1])
    for row, pair in enumerate(mirrors):
        if message in pair:
            return (row, index)
    return None


def fraction(values: list[int]) -> list[int]:
    """The mean of a list of outcomes' products as [numerator, denominator], [0, 1] over nothing."""
    mean = Fraction(sum(values), len(values)) if values else Fraction(0)
    return [mean.numerator, mean.denominator]


def maxima_of(row: list[int]) -> list[int]:
    """The local maxima of a pattern: a position above both neighbours, the ends compared with their one neighbour."""
    found = []
    for at, value in enumerate(row):
        near = [row[at - 1]] if at > 0 else []
        near += [row[at + 1]] if at < len(row) - 1 else []
        if near and all(value > other for other in near):
            found.append(at)
    return found


def reading(world: Path, output: Path, expectation: Path) -> dict[str, object]:
    """The reading of one run: the landings per side and per pair, each pair's outcomes at its side's settings, E at the settings, S, the curve in a + b, the ridge, the single-side patterns and the GameBoard check, beside the blind rows."""
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    lines = json.loads(output.read_text(encoding="utf-8"))["lines"]
    loaded = load_world(world)
    across = AXES.index(expected["across"])
    centre, spacing, bins = (
        int(expected["fringe_centre"]),
        int(expected["spacing"]),
        int(expected["bins"]),
    )
    sides: dict[str, str] = {side: str(name) for side, name in expected["sides"].items()}
    declared = {row.name for row in loaded.detectors}
    if not set(sides.values()) <= declared:
        raise ValueError(
            f"the expectation's sides {sides} are not the world's detectors {sorted(declared)}"
        )
    by_name = {name: side for side, name in sides.items()}
    mirrors = [[int(m) for m in row] for row in expected.get("mirrors", [])]
    settings = {side: [int(v) for v in values] for side, values in expected["settings"].items()}
    landed: dict[tuple[int, int], dict[str, list[int]]] = {}
    pattern: dict[str, dict[int, int]] = {side: {} for side in sides}
    unnamed = 0
    for line in lines:
        if line.get("event") != "click" or line.get("family") != expected["family"]:
            continue
        side = by_name.get(str(line.get("detector")))
        if side is None:
            continue
        row = int(list(line["node"])[across])  # type: ignore[call-overload]
        pattern[side][row] = pattern[side].get(row, 0) + 1
        key = pair_of(line.get("whole"), mirrors)
        if key is None:
            unnamed += 1
            continue
        landed.setdefault(key, {side: [] for side in sides})[side].append(row)
    pairs: list[dict[str, Any]] = []
    for key in sorted(landed):
        rows = landed[key]
        outcomes = {}
        for side in sides:
            found = [outcome(rows[side], centre, a, spacing) for a in settings[SIDE_SETTINGS[side]]]
            if rows[side] and all(found):
                outcomes[side] = found
        pairs.append({"whole": list(key), "landings": rows, "outcomes": outcomes})
    coincident = [pair for pair in pairs if len(pair["outcomes"]) == 2]
    (a, a_prime), (b, b_prime) = settings["a"], settings["b"]
    correlation = {}
    for i, left in enumerate(settings["a"]):
        for j, right in enumerate(settings["b"]):
            products = [
                pair["outcomes"]["left"][i] * pair["outcomes"]["right"][j] for pair in coincident
            ]
            correlation[f"{left} {right}"] = fraction(products)
    e = {key: Fraction(*value) for key, value in correlation.items()}
    s_value = e[f"{a} {b}"] - e[f"{a} {b_prime}"] + e[f"{a_prime} {b}"] + e[f"{a_prime} {b_prime}"]
    sums: list[list[int]] = [[] for _ in range(spacing)]
    for left in range(spacing):
        for right in range(spacing):
            for pair in coincident:
                product = outcome(pair["landings"]["left"], centre, left, spacing) * outcome(
                    pair["landings"]["right"], centre, right, spacing
                )
                if product:
                    sums[(left + right) % spacing].append(product)
    curve = [fraction(values) for values in sums]
    ridge = [0] * bins
    for pair in coincident:
        for left in pair["landings"]["left"]:
            for right in pair["landings"]["right"]:
                ridge[((left - centre + right - centre) % spacing) * bins // spacing] += 1
    most, least = max(ridge), min(ridge)
    visibility = Fraction(most - least, most + least) if most + least else Fraction(0)
    patterns = {
        side: [rows.get(y, 0) for y in range(max(rows, default=-1) + 1)]
        for side, rows in pattern.items()
    }
    single = [pair for pair in pairs if all(len(rows) == 1 for rows in pair["landings"].values())]
    mirrored = [p for p in single if p["landings"]["left"][0] + p["landings"]["right"][0] == 2 * centre]
    return {
        "verdict": "DETECTOR",
        "family": expected["family"],
        "settings": settings,
        "degrees": expected.get("degrees"),
        "wholes": expected.get("wholes"),
        "landings": {side: sum(rows.values()) for side, rows in pattern.items()},
        "unnamed": unnamed,
        "pairs": pairs,
        "coincidences": len(coincident),
        "correlation": correlation,
        "S": [s_value.numerator, s_value.denominator],
        "curve": curve,
        "curve_at": {
            str(link): curve[int(link) % spacing] for link in expected.get("curve", {}).get("links", [])
        },
        "ridge": ridge,
        "visibility": [visibility.numerator, visibility.denominator],
        "pattern": patterns,
        "maxima": {side: maxima_of(rows) for side, rows in patterns.items()},
        "check": {"pairs": len(pairs), "two_landings": len(single), "mirror_rows": len(mirrored)},
        "blind": expected.get("blind"),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--world", type=Path, required=True, help="the world file the run ran")
    parser.add_argument("--output", type=Path, required=True, help="the run's output file")
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    args = parser.parse_args(argv)
    print(json.dumps(reading(args.world, args.output, args.expectation)))


if __name__ == "__main__":
    main()
