"""The mode file of a one-Node body (ALGEBRA.md #the-primitives, THE BOUND BODY IS ONE NODE, THE RULE'S OWN UNIVERSE): for every measured body of one declared Node with a count c, the record at its Node as the profile isqrt(c) there at both levels (c T = a^2 at T = 1, the amplitude the count's root), its bound rotation's clock pair [a, b] (2 cos omega_b in integers, Cheshbon's line per count) given on the command line and never held in the tool, the family's pair from the universe file, the twist as the generator writes it (round(unit omega / (4 Gamma)), ALGEBRA.md #the-primitives) and `world_digest` the world's one digest; a body that is not one Node, or a count with no pair given, is refused by name. Usage: `python tools/pixel_mode.py --input <world.json> --clock <count> <a> <b> [--clock ...] [--out <world.mode.json>]`."""

from __future__ import annotations

import argparse
import json
from math import acos, isqrt
from pathlib import Path
from typing import Any

from event_universe.world_files import input_digest, world_files


def clock_table(pairs: list[list[int]]) -> dict[int, tuple[int, int]]:
    """The clock pair per count from the command line's `--clock count a b` entries, a count named twice refused."""
    table: dict[int, tuple[int, int]] = {}
    for count, a, b in pairs:
        if count in table:
            raise ValueError(f"--clock {count} is given twice")
        if a < 1 or b < 1:
            raise ValueError(
                f"--clock {count} {a} {b}: a and b are positive integers, 2 cos omega as a rational"
            )
        table[count] = (a, b)
    return table


def pixel_entry(
    number: int,
    body: dict[str, Any],
    shape: tuple[int, int, int],
    pair: list[int],
    clock: tuple[int, int],
    twist_scale: int,
) -> dict[str, Any]:
    """One body's entry: the profile over the whole board (x-major, one integer per Node) with isqrt(count) at the body's Node, its clock, pair and twist."""
    nodes = body.get("nodes")
    if not isinstance(nodes, list) or len(nodes) != 1:
        raise ValueError(
            f"measured[{number}] is not a body of one declared Node: this tool writes the pixel's record alone"
        )
    (x, y, z), count = nodes[0]["node"], int(nodes[0]["count"])
    profile = [0] * (shape[0] * shape[1] * shape[2])
    profile[(x * shape[1] + y) * shape[2] + z] = isqrt(count)
    a, b = clock
    twist = round(twist_scale * acos(a / (2 * b)))
    return {
        "family": body["family"],
        "pair": pair,
        "count": count,
        "amplitude": isqrt(count),
        "clock": [a, b],
        "twist": twist,
        "profile": profile,
    }


def pixel_mode(document: dict[str, Any], clocks: dict[int, tuple[int, int]]) -> dict[str, Any]:
    """The mode document of a world of one-Node bodies: `world_digest` and `bodies`, one entry per measured event in the world's order."""
    universe = world_files(document)[document["universe"]]
    pairs = {family["name"]: list(family["pair"]) for family in universe["families"]}
    gamma = int(document.get("node_clock", universe["integers"]["node_clock"]))
    twist_scale = int(universe["integers"]["twist_table"]["unit"]) // (4 * gamma)
    shape = tuple(int(side) for side in document["shape"])
    bodies = []
    for number, body in enumerate(document.get("measured", [])):
        count = (
            int(body["nodes"][0]["count"])
            if isinstance(body.get("nodes"), list) and body["nodes"]
            else None
        )
        if count not in clocks:
            raise ValueError(
                f"measured[{number}] has the count {count} and no --clock pair was given for it"
            )
        bodies.append(
            pixel_entry(
                number,
                body,
                (shape[0], shape[1], shape[2]),
                pairs[body["family"]],
                clocks[count],
                twist_scale,
            )
        )
    return {"world_digest": input_digest(document), "bodies": bodies}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="the world file of one-Node bodies")
    parser.add_argument(
        "--clock",
        type=int,
        nargs=3,
        action="append",
        metavar=("COUNT", "A", "B"),
        required=True,
        help="the clock pair [a, b] of the bound rotation for every body of that count (2 cos omega_b as a rational, b at least isqrt(count))",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="the mode file to write; beside the world as <world>.mode.json when omitted",
    )
    args = parser.parse_args(argv)
    document = json.loads(args.input.read_text(encoding="utf-8"))
    mode = pixel_mode(document, clock_table(args.clock))
    out = args.out if args.out is not None else args.input.with_suffix(".mode.json")
    out.write_text(json.dumps(mode) + "\n", encoding="utf-8")
    for body in mode["bodies"]:
        print(json.dumps({key: value for key, value in body.items() if key != "profile"}))


if __name__ == "__main__":
    main()
