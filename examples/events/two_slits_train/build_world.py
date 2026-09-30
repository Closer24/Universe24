"""The train world's builder (the advisor, #1515 comment 5907540901, at the owner's word: one world for the dilution series and the anticorrelation, the warm screen declared by the file): from a design file (`design.json` beside it, every number of the world) and the loader's count wall W_c, the two slits' geometry shifted along x by the train's length, a train of single-quantum packets of the light family behind the wall, the screen a slab of groups, one detector per column of the design's range across the beam, each group's declared count remainders by the design's blind rule (the even rule per Node, (n + offset) / N of W_c, or the golden ratio's fractional parts per group or per Node), floored to integers; and the cold twin, the same world without the remainders. Every number of the world is the design's and stands in the world files, none in the engine; W_c is the loader's.

Run from the checkout with PYTHONPATH set to its src:

    PYTHONPATH=src python examples/events/two_slits_train/build_world.py [--design <design>.json] [--folder <folder>] [--name <name>] [--whole]

then lay the packets with the generator, `PYTHONPATH=src python tools/pixel_mode.py --input <world>.json`, for each world written.
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
GOLDEN_DIGITS = 60


def golden_fraction(index: int) -> Decimal:
    """The golden ratio's fractional part of an index, frac(index x (sqrt 5 - 1) / 2), the advisor's blind rule, spread as evenly as any sequence."""
    getcontext().prec = GOLDEN_DIGITS
    turned = index * (Decimal(5).sqrt() - 1) / 2
    return turned - int(turned)


def remainders(rule: dict[str, Any], rank: int, slab: int, wall: int, nodes: int) -> list[int]:
    """One group's declared count remainders, one per Node of its slab (the group's rank in the declared order, `nodes` the screen's Nodes in all): the rule `even` per Node, the n-th Node of the screen at (n + offset) / nodes of W_c, `offset` a fraction [r, s] (the advisor's [1, 2]: no Node at the bottom wall); or the rule `golden` per group (one value, frac((rank + offset) x 0.618...) x W_c at every Node) or per Node (frac((rank x slab + index + offset) x 0.618...) x W_c), `offset` an integer; floored to integers."""
    if rule["rule"] == "even" and rule["per"] == "node":
        offset = Fraction(int(rule["offset"][0]), int(rule["offset"][1]))
        return [int((rank * slab + index + offset) * wall / nodes) for index in range(slab)]
    if rule["rule"] != "golden" or rule["per"] not in ("group", "node"):
        raise ValueError(
            f"the design's remainder rule is even per node, or golden per group or node, got {rule}"
        )
    offset = int(rule["offset"])
    if rule["per"] == "group":
        return [int(golden_fraction(rank + offset) * wall)] * slab
    return [int(golden_fraction(rank * slab + index + offset) * wall) for index in range(slab)]


def world(design: dict[str, Any], wall: int, warm: bool, whole: bool = False) -> dict[str, object]:
    """The world file from the design: the shift is the train's length, packets x spacing; the leading packet's top the design's before the wall, every next one a spacing behind; the slab from the screen's coordinate beyond the shift, one detector per column of the design's range with its slab's Nodes and, on the warm screen, its remainders; the far face `beyond_slab` beyond the slab, receding as the design's `receding` key declares (the world's key, passed as written); the ticks from the pace."""
    slits, packets, spacing = design["slits"], int(design["packets"]), int(design["spacing"])
    slab, shift = int(design["slab"]), packets * spacing
    first = int(slits["screen"]) + shift
    gaps = [{"y": list(gap), "z": [0, 0]} for gap in slits["gaps"]]
    messages = [
        {
            "family": design["family"],
            "along": "x",
            "wave": list(design["wave"]),
            "amplitude": int(design["amplitude"]),
            "top": {"x": [top, top], "y": list(design["across"]), "z": [0, 0]},
            "edge": {"x": int(design["edge_along"]), "y": int(design["edge_across"]), "z": 0},
        }
        for top in (int(slits["first_top"]) + shift - spacing * k for k in range(packets))
    ]
    for index, message in enumerate(messages):
        if (
            whole
        ):  # the count laid whole at one Node, a key the loader refuses until the light family's line
            low, high = design["across"]
            column = int(low) + int(golden_fraction(index) * (int(high) - int(low)))
            message["whole"] = [message["top"]["x"][0], column, 0]
    detectors = []
    columns = range(int(design["columns"][0]), int(design["columns"][1]) + 1)
    for rank, column in enumerate(columns):
        entry: dict[str, object] = {"name": f"screen {column}"}
        entry["positions"] = [[x, column, 0] for x in range(first, first + slab)]
        if warm:
            values = remainders(design["remainder"], rank, slab, wall, len(columns) * slab)
            entry["remainder"] = {design["family"]: values[0] if len(set(values)) == 1 else values}
        detectors.append(entry)
    pace = design["pace"]
    ticks = int(pace["peak_at_slab"]) + int(pace["slab_intervals"]) * packets + int(pace["margin"])
    return {
        "shape": [first + slab + int(design["beyond_slab"]), int(design["height"]), 1],
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "face_depth": 1,
        "faces": [{"axis": "x", "at": int(slits["wall"]) + shift, "gaps": gaps}],
        "ticks": ticks,
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [],
        "messages": messages,
        "detectors": detectors,
        "receding": design["receding"],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument(
        "--name", default="two_slits_train", help="the world's name; the cold twin adds _cold"
    )
    parser.add_argument(
        "--whole",
        action="store_true",
        help="declare each packet's count laid whole at one Node (its top's x, a y by the blind rule y_n = 4 + frac(n x 0.618...) x 40); the loader refuses the key until the light family's line lays it",
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    universe = json.loads(Path(design["universe"]).read_text(encoding="utf-8"))
    _integers, families = universe_of(universe)
    family = next(family for family in families if family.name == design["family"])
    wall = count_wall(family, int(universe["integers"]["quantum_action"]))
    args.folder.mkdir(parents=True, exist_ok=True)
    for suffix, warm in (("", True), ("_cold", False)):
        path = args.folder / f"{args.name}{suffix}.json"
        document = world(design, wall, warm, args.whole)
        path.write_text(json.dumps(document) + "\n", encoding="utf-8")
        summary = {"world": str(path), "wall": wall, "warm": warm, "shape": document["shape"]}
        print(json.dumps({**summary, "packets": design["packets"], "ticks": document["ticks"]}))


if __name__ == "__main__":
    main()
