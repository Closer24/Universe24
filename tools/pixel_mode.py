"""The mode file of a one-Node body (ALGEBRA.md #the-primitives, THE BOUND BODY IS ONE NODE, THE RULE'S OWN UNIVERSE; Cheshbon's line of 2026-09-28, 14:12 Israel): for every measured body of one declared Node with a count c, its bound mode at rest over the whole board, the amplitude at its Node b = isqrt(c T den div (2 den - a)) from the form D = now^2 - next x before at rest (the count c = D div T) with its bound rotation's clock pair [a, den] (2 cos omega_b in integers), the tail on every other Node round(b t^d) with d the Manhattan distance to the pixel (the shorter way on a periodic axis) and t = e^-kappa as an integer over 2^16, until the level falls below 1; both levels the profile (the standing phase); the clock pair and the tail per count given on the command line and never held in the tool, the family's pair from the universe file, the twist as the generator writes it (round(unit omega / (4 Gamma))) and `world_digest` the world's one digest; a body that is not one Node, or a count with no pair given, is refused by name. Usage: `python tools/pixel_mode.py --input <world.json> --clock <count> <a> <den> --tail <count> <t> [...] [--out <world.mode.json>]`."""

from __future__ import annotations

import argparse
import json
from math import acos, isqrt
from pathlib import Path
from typing import Any

from event_universe.world_files import input_digest, world_files

TAIL_UNIT = 1 << 16  # the tail's factor per Link t is given as an integer over 2^16 (Cheshbon's line)


def clock_table(clocks: list[list[int]], tails: list[list[int]]) -> dict[int, tuple[int, int, int]]:
    """The clock pair [a, den] and the tail's factor (t x 2^16) per count from the command line's `--clock count a den` and `--tail count t` entries; a count named twice, a count with one of the two alone, or a value below 1, refused by name."""
    table: dict[int, tuple[int, int, int]] = {}
    tail_of: dict[int, int] = {}
    for count, tail in tails:
        if count in tail_of:
            raise ValueError(f"--tail {count} is given twice")
        if tail < 1:
            raise ValueError(f"--tail {count} {tail}: the tail's factor is positive (t over 2^16)")
        tail_of[count] = tail
    for count, a, den in clocks:
        if count in table:
            raise ValueError(f"--clock {count} is given twice")
        if min(a, den) < 1 or a >= 2 * den:
            raise ValueError(
                f"--clock {count} {a} {den}: a and den positive with a below 2 den (2 cos omega_b as a rational)"
            )
        if count not in tail_of:
            raise ValueError(f"--clock {count} has no --tail {count} <t> beside it")
        table[count] = (a, den, tail_of.pop(count))
    if tail_of:
        raise ValueError(f"--tail {min(tail_of)} has no --clock {min(tail_of)} <a> <den> beside it")
    return table


def amplitude(count: int, action: int, clock: tuple[int, int]) -> int:
    """The amplitude of the bound mode at the pixel from the form at rest: b = isqrt(c T den div (2 den - a))."""
    a, den = clock
    return isqrt(count * action * den // (2 * den - a))


def tail_level(level: int, tail: int, distance: int) -> int:
    """The level at a Node `distance` Links from the pixel: round(b t^d) in integers, t = tail / 2^16."""
    scale = TAIL_UNIT**distance
    return (level * tail**distance + scale // 2) // scale


def profile_of(
    node: tuple[int, int, int],
    shape: tuple[int, int, int],
    periodic: tuple[bool, bool, bool],
    level: int,
    tail: int,
) -> list[int]:
    """The profile over the whole board (x-major, one integer per Node): the amplitude at the pixel and round(b t^d) at every Node at the Manhattan distance d (the shorter way on a periodic axis), 0 where the level falls below 1."""
    profile = []
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                distance = 0
                for here, there, side, wrap in zip((x, y, z), node, shape, periodic, strict=True):
                    gap = abs(here - there)
                    distance += min(gap, side - gap) if wrap else gap
                profile.append(tail_level(level, tail, distance))
    return profile


def pixel_entry(
    number: int,
    body: dict[str, Any],
    world: dict[str, Any],
    pair: list[int],
    action: int,
    row: tuple[int, int, int],
    twist_scale: int,
) -> dict[str, Any]:
    """One body's entry: its family's pair, its count, the amplitude b, the clock [a, den], the tail's factor over 2^16, the twist and the profile over the whole board."""
    nodes = body.get("nodes")
    if not isinstance(nodes, list) or len(nodes) != 1:
        raise ValueError(
            f"measured[{number}] is not a body of one declared Node: this tool writes the pixel's record alone"
        )
    (x, y, z), count = nodes[0]["node"], int(nodes[0]["count"])
    shape = tuple(int(side) for side in world["shape"])
    periodic = tuple(world["boundary"][axis] == "periodic" for axis in "xyz")
    a, den, tail = row
    level = amplitude(count, action, (a, den))
    profile = profile_of(
        (x, y, z), (shape[0], shape[1], shape[2]), (periodic[0], periodic[1], periodic[2]), level, tail
    )
    twist = round(twist_scale * acos(a / (2 * den)))
    return {
        "family": body["family"],
        "pair": pair,
        "count": count,
        "amplitude": level,
        "clock": [a, den],
        "tail": [tail, TAIL_UNIT],
        "twist": twist,
        "profile": profile,
    }


def pixel_mode(document: dict[str, Any], clocks: dict[int, tuple[int, int, int]]) -> dict[str, Any]:
    """The mode document of a world of one-Node bodies: `world_digest` and `bodies`, one entry per measured event in the world's order."""
    universe = world_files(document)[document["universe"]]
    pairs = {family["name"]: list(family["pair"]) for family in universe["families"]}
    integers = universe["integers"]
    gamma = int(document.get("node_clock", integers["node_clock"]))
    if "quantum_action" not in integers:
        raise ValueError(
            "the universe file declares no quantum_action T: the count c = D div T needs it"
        )
    action = int(integers["quantum_action"])
    twist_scale = int(integers["twist_table"]["unit"]) // (4 * gamma)
    bodies = []
    for number, body in enumerate(document.get("measured", [])):
        nodes = body.get("nodes")
        count = int(nodes[0]["count"]) if isinstance(nodes, list) and nodes else None
        if count not in clocks:
            raise ValueError(
                f"measured[{number}] has the count {count} and no --clock and --tail rows were given for it"
            )
        bodies.append(
            pixel_entry(
                number, body, document, pairs[body["family"]], action, clocks[count], twist_scale
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
        metavar=("COUNT", "A", "DEN"),
        required=True,
        help="for every body of that count: the clock pair [a, den] of the bound rotation, 2 cos omega_b as a rational",
    )
    parser.add_argument(
        "--tail",
        type=int,
        nargs=2,
        action="append",
        metavar=("COUNT", "T"),
        required=True,
        help="for every body of that count: the tail's factor per Link t = e^-kappa as an integer over 2^16",
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="the mode file to write; beside the world as <world>.mode.json when omitted",
    )
    args = parser.parse_args(argv)
    document = json.loads(args.input.read_text(encoding="utf-8"))
    mode = pixel_mode(document, clock_table(args.clock, args.tail))
    out = args.out if args.out is not None else args.input.with_suffix(".mode.json")
    out.write_text(json.dumps(mode) + "\n", encoding="utf-8")
    for body in mode["bodies"]:
        reading = {key: value for key, value in body.items() if key != "profile"}
        reading["support"] = sum(1 for level in body["profile"] if level)
        print(json.dumps(reading))


if __name__ == "__main__":
    main()
