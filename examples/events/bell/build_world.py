"""Bell's world's builder (the advisor's sketch and its correction, #1515 comments 5908460763 (3) and 5909819308; ALGEBRA.md row (h)): from a design file (`design.json` beside it, every number of the world) and the loader's count wall W_c, a flat board with the source at its centre column, a train of pairs of mirror packets of the light family leaving both ways, each pair at its blind emission angle (the two packets with opposite transverse wave numbers, the message key `transverse`), two symmetric two-gap walls the train's length from the source and a screen beyond each, one detector per screen with its remainders by the design's blind rule; the cold twin without the remainders; and the expectation file (the pairs' windows, the settings as positions on the screens, the blind row). Every number of the world is the design's and stands in the world files, none in the engine; W_c is the loader's.

Run from the checkout with PYTHONPATH set to its src:

    PYTHONPATH=src python examples/events/bell/build_world.py [--design <design>.json] [--folder <folder>] [--name <name>] [--first-pair N]

then lay the packets with the generator, `PYTHONPATH=src python tools/pixel_mode.py --input <world>.json`, for each world written; a long train is several runs of the world with `first_pair` continued.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from event_universe.loader.derived import count_wall
from event_universe.loader.world import universe_of

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]  # the checkout, the design's repository paths' root
GOLDEN_DIGITS = 60
getcontext().prec = GOLDEN_DIGITS
EPSILON = Decimal(10) ** (-GOLDEN_DIGITS // 2)


def series(angle: Decimal, term: Decimal, first: int) -> Decimal:
    """A sine's or a cosine's series at the context's precision: the terms from `term` on, each the last times -angle^2 over the next two factorial steps from `first`."""
    total, step = term, first
    while abs(term) > EPSILON:
        term = -term * angle * angle / (step * (step + 1))
        total += term
        step += 2
    return total


def sine(angle: Decimal) -> Decimal:
    """The sine of an angle in radians by its series."""
    return series(angle, angle, 2)


def cosine(angle: Decimal) -> Decimal:
    """The cosine of an angle in radians by its series."""
    return series(angle, Decimal(1), 1)


def arctangent(inverse: int) -> Decimal:
    """arctan(1 / inverse) by its series at the context's precision."""
    x = Decimal(1) / inverse
    term, total, step = x, x, 1
    while abs(term) > EPSILON:
        term = -term * x * x
        step += 2
        total += term / step
    return total


PI = 2 * 2 * (2 * 2 * arctangent(5) - arctangent(239))  # Machin's formula


def golden_fraction(index: int) -> Decimal:
    """The golden ratio's fractional part of an index, frac(index x (sqrt 5 - 1) / 2), the blind rule, spread as evenly as any sequence."""
    turned = index * (Decimal(5).sqrt() - 1) / 2
    return turned - int(turned)


def gap_distance(gaps: list[list[int]]) -> Fraction:
    """The distance d between the two gaps' centres across the beam."""
    (a, b), (c, e) = gaps
    return Fraction(c + e - a - b, 2)


def transverse(design: dict[str, Any], pair: int) -> list[int]:
    """The pair's transverse wave number as the fraction of pi per Link [r, s] at the design's resolution: q_n = k sin theta_n, sin theta_n = (lambda / 2 d) (2 frac(n x 0.618...) - 1) with n the pair's index in the sequence, k = pi p / q and lambda = 2 q / p; rounded to the nearest step."""
    rule, steps = design["angle"], int(design["angle"]["steps"])
    if rule["rule"] != "golden":
        raise ValueError(f"the design's angle rule is golden, got {rule}")
    p, q = (int(v) for v in design["wave"])
    wavelength = Fraction(2 * q, p)
    blind = golden_fraction(int(design["first_pair"]) + pair)
    sine = wavelength / (2 * gap_distance(design["gaps"])) * (2 * Fraction(blind) - 1)
    return [round(Fraction(p, q) * sine * steps), steps]


def remainders(rule: dict[str, Any], rank: int, count: int, wall: int, nodes: int) -> list[int]:
    """One detector's declared count remainders, one per Node (`rank` its first Node's place over the screens' Nodes in the declared order, `nodes` the screens' Nodes in all): the rule `even` per Node, the n-th Node at (n + offset) / nodes of W_c, `offset` a fraction [r, s] (the advisor's [1, 2]: no Node at the bottom wall); or the rule `golden` per Node (frac((n + offset) x 0.618...) x W_c, `offset` an integer); floored to integers."""
    if rule["rule"] == "even" and rule["per"] == "node":
        offset = Fraction(int(rule["offset"][0]), int(rule["offset"][1]))
        return [int((rank + index + offset) * wall / nodes) for index in range(count)]
    if rule["rule"] != "golden" or rule["per"] != "node":
        raise ValueError(f"the design's remainder rule is even per node or golden per node, got {rule}")
    offset = int(rule["offset"])
    return [int(golden_fraction(rank + index + offset) * wall) for index in range(count)]


def geometry(design: dict[str, Any]) -> dict[str, int]:
    """The board from the design: the walls' distance (at least the train's reach), the screens' distance (the walls' plus L), the length and the source column; refused by name where the train does not fit between the source and the walls."""
    spacing, pairs = int(design["spacing"]), int(design["pairs"])
    reach = int(design["first_offset"]) + spacing * (pairs - 1) + int(design["edge_along"])
    wall = int(design["wall_distance"])
    if reach >= wall:
        raise ValueError(
            f"the train reaches {reach} Links from the source and the walls stand {wall} away: every pair is laid between the source and the walls"
        )
    screen = wall + int(design["screen_offset"])
    length = 2 * (screen + int(design["slab"]) + int(design["beyond_slab"]))
    return {"wall": wall, "screen": screen, "length": length, "source": length // 2}


def band_pace(design: dict[str, Any], pair: int) -> Decimal:
    """A pair's packets' pace along x in Links per interval from the generator's band (ALGEBRA.md #the-generator; tools/pixel_mode.py): cos omega = (cos k_x + cos k_y + 1) / 3 and the pace sin k_x / (3 sin omega), k_x = pi p / q the design's wave number and k_y = pi r / s the pair's transverse one; a tilted packet is slower along x, and at k_y = 0 this is the design's pace (12 Links in 22 intervals)."""
    p, q = (int(v) for v in design["wave"])
    r, s = transverse(design, pair)
    along, across = PI * p / q, PI * r / s
    band = (cosine(along) + cosine(across) + 1) / 3
    return sine(along) / (3 * (1 - band * band).sqrt())


def drift(design: dict[str, Any], pair: int) -> Decimal:
    """A pair's packets' displacement across the beam by the time they reach the walls, in Links: the band's group velocity across over along, sin k_y / sin k_x, times the distance from the top to the wall (a GameBoard number: the tilt's drift, off the board where it exceeds the rows beside the packet)."""
    p, q = (int(v) for v in design["wave"])
    r, s = transverse(design, pair)
    away = int(design["wall_distance"]) - int(design["first_offset"]) - pair * int(design["spacing"])
    return away * sine(PI * r / s) / sine(PI * p / q)


def peak_at_screen(design: dict[str, Any], pair: int) -> int:
    """The interval a pair's peaks reach the screens' near faces: the tops' distance to them (the screens' less the tops') at the pair's band pace, rounded down."""
    away = geometry(design)["screen"] - int(design["first_offset"]) - pair * int(design["spacing"])
    return int(Decimal(away) / band_pace(design, pair))


def world(design: dict[str, Any], wall: int, warm: bool) -> dict[str, object]:
    """The world file from the design: the board, the two symmetric walls with their gaps, the train of pairs (each pair two mirror packets at opposite transverse wave numbers, the tops `first_offset` + n x `spacing` from the source on the side each leaves toward, moving away from it: the snapshot of an emission in sequence, the earliest pair the farthest out), the two screens as detectors with their remainders on the warm screens, the ticks from the pace (the latest peak's arrival, the slab's transit and the margin)."""
    found = geometry(design)
    source, spacing, slab = found["source"], int(design["spacing"]), int(design["slab"])
    gaps = [{"y": list(gap), "z": [0, 0]} for gap in design["gaps"]]
    messages = []
    for pair in range(int(design["pairs"])):
        away = int(design["first_offset"]) + pair * spacing
        sideways = transverse(design, pair)
        for sign, top in ((1, source + away), (-1, source - away)):
            messages.append(
                {
                    "family": design["family"],
                    "along": "x",
                    "wave": [sign * int(design["wave"][0]), int(design["wave"][1])],
                    "amplitude": int(design["amplitude"]),
                    "top": {"x": [top, top], "y": list(design["across"]), "z": [0, 0]},
                    "edge": {"x": int(design["edge_along"]), "y": int(design["edge_across"]), "z": 0},
                    "transverse": {"y": [sign * sideways[0], sideways[1]]},
                }
            )
    detectors = []
    rows = range(int(design["height"]))
    nodes = 2 * slab * len(rows)
    for side, sign in (("left", -1), ("right", 1)):
        near = source + sign * found["screen"]
        columns = sorted(range(near, near + sign * slab, sign))
        entry: dict[str, object] = {"name": side}
        entry["positions"] = [[x, y, 0] for y in rows for x in columns]
        if warm:
            values = remainders(
                design["remainder"], len(detectors) * slab * len(rows), slab * len(rows), wall, nodes
            )
            entry["remainder"] = {design["family"]: values}
        detectors.append(entry)
    pace = design["pace"]
    last = max(peak_at_screen(design, pair) for pair in range(int(design["pairs"])))
    return {
        "shape": [found["length"], int(design["height"]), 1],
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "face_depth": 1,
        "faces": [
            {"axis": "x", "at": at, "gaps": gaps}
            for at in (source - found["wall"], source + found["wall"])
        ],
        "ticks": last + int(pace["slab_intervals"]) + int(pace["margin"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [],
        "messages": messages,
        "detectors": detectors,
    }


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The expectation file: per pair the interval its peaks reach the screens (at its band pace) and its window, its transverse wave number and its drift across the beam at the wall, the band's pace plain and at the largest tilt, the sides' detectors, the settings as positions in Links (a and a' on the left, b and b' on the right, from their degrees at the fringe spacing lambda L / d), the fringe's centre and spacing, the comb's bins, and the blind row (the advisor: E = 0.203 cos(a + b), S = 0.57 and the coincidence fringe's visibility 0.50 under the count's line as it stands; nature E = 0.405 cos(a + b), S = 1.15 and the visibility 1.00; Bell's bound 0.71)."""
    p, q = (int(v) for v in design["wave"])
    spacing = Fraction(2 * q, p) * int(design["screen_offset"]) / gap_distance(design["gaps"])
    if spacing.denominator != 1:
        raise ValueError(f"the fringe spacing lambda L / d is {spacing}, not a whole number of Links")
    settings = {}
    for side, degrees in design["settings"].items():
        links = [Fraction(int(angle) * spacing, 360) for angle in degrees]
        if any(link.denominator != 1 for link in links):
            raise ValueError(f"the settings {degrees} are not whole Links at the spacing {spacing}")
        settings[side] = [int(link) for link in links]
    pairs = [
        {
            "peak": peak_at_screen(design, n),
            "window": [
                peak_at_screen(design, n),
                peak_at_screen(design, n) + int(design["pace"]["slab_intervals"]),
            ],
            "index": int(design["first_pair"]) + n,
            "transverse": transverse(design, n),
            "drift": float(round(drift(design, n), 1)),
        }
        for n in range(int(design["pairs"]))
    ]
    return {
        "comment": "Bell's world's blind expectation (the advisor, #1515 comments 5908460763 and 5909819308; ALGEBRA.md row (h)), written before the run from design.json: DETECTOR. Per pair the interval its two peaks reach the screens' near faces (the design's pace) and its window; a landing (a click on a screen) belongs to the pair whose peak passes its Node nearest in time. The reading is the comb: a landing's outcome at a setting a (a position on its screen in Links) is +1 where cos(Phi(y) - a) > 0 and -1 under, Phi(y) = 2 pi (y - fringe_centre) / spacing the fringe phase of its row; a pair's outcome on a screen is the sign of its landings' outcomes summed; E(a, b) is the mean over the pairs with a landing on both screens of the product of the left outcome at a and the right outcome at b; S = E(a, b) - E(a, b') + E(a', b) + E(a', b'); the coincidence fringe is the pairs' landings binned by Phi_A + Phi_B, its visibility (most - least) over (most + least). Blind under the count's line as it stands: E = 0.203 cos(a + b), S = 0.57, the visibility 0.50; nature: E = 0.405 cos(a + b), S = 1.15, the visibility 1.00; Bell's bound for any local line 0.71. The GameBoard check: each screen's single-side pattern flat over the train within the rounding, and two landings per pair. On the cold twin no landing at all.",
        "family": design["family"],
        "across": "y",
        "along": "x",
        "source": geometry(design)["source"],
        "pace": [int(design["pace"]["links"]), int(design["pace"]["intervals"])],
        "band_pace": {
            "plain": float(
                round(sine(PI * p / q) / (3 * (1 - ((cosine(PI * p / q) + 2) / 3) ** 2).sqrt()), 4)
            ),
            "tilted_most": float(
                round(min(band_pace(design, n) for n in range(int(design["pairs"]))), 4)
            ),
        },
        "sides": {"left": "left", "right": "right"},
        "settings": settings,
        "degrees": design["settings"],
        "fringe_centre": int(design["fringe_centre"]),
        "spacing": int(spacing),
        "bins": int(design["bins"]),
        "pairs": pairs,
        "blind": {"correlation": "0.203 cos(a + b)", "S": 0.57, "visibility": 0.5},
        "nature": {"correlation": "0.405 cos(a + b)", "S": 1.15, "visibility": 1.0},
        "bound": 0.71,
        "cold": {"landings": 0},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument("--name", default="bell", help="the world's name; the cold twin adds _cold")
    parser.add_argument(
        "--first-pair", type=int, default=None, help="the sequence's start, over the design's"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    if args.first_pair is not None:
        design["first_pair"] = args.first_pair
    universe = json.loads((ROOT / design["universe"]).read_text(encoding="utf-8"))
    _integers, families = universe_of(universe)
    family = next(family for family in families if family.name == design["family"])
    wall = count_wall(family, int(universe["integers"]["quantum_action"]))
    args.folder.mkdir(parents=True, exist_ok=True)
    for suffix, warm in (("", True), ("_cold", False)):
        path = args.folder / f"{args.name}{suffix}.json"
        document = world(design, wall, warm)
        path.write_text(json.dumps(document) + "\n", encoding="utf-8")
        summary = {"world": str(path), "wall": wall, "warm": warm, "shape": document["shape"]}
        print(
            json.dumps(
                {
                    **summary,
                    "pairs": design["pairs"],
                    "first_pair": design["first_pair"],
                    "ticks": document["ticks"],
                }
            )
        )
    target = args.folder / "expectation.json"
    target.write_text(json.dumps(expectation(design), indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(target)}))


if __name__ == "__main__":
    main()
