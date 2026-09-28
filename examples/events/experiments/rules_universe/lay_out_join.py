"""WORLD (d) OF THE RULE'S OWN UNIVERSE: THE CLICK JOINS AND PARTS (ALGEBRA.md #the-rows-against-nature, THE RULE'S OWN UNIVERSE, THE BOUND BODY IS ONE NODE, THE CLICK JOINS AND PARTS; the owner's decision of 2026-09-28, 13:02 Israel time, through the Closer: the rule's universe is the finish line, world (d) to the de Broglie Experimenter). Two worlds on one universe file: THE JOIN, two bound bodies of one Node each, the counts 5,000 and 6,000 on the engine of today (Cheshbon's line of 14:12 Israel time: with the level read once the edge of the bound body is 0.345 Gamma = 4,136, so 3,000 and 4,000 disperse and 5,000 binds; the Closer's word of 13:03 named 3,000 and 4,000, the counts under the corrected term, the edge 2,706), two Links apart so that their tails overlap (kappa = 0.63 per Link at 5,000 and 0.98 at 6,000): the law's row is a run of clicks from the smaller to the deeper whose last ends the smaller's record, one record for the joined cluster; THE FAR JOIN (the world named `part`), the same two bodies five Links apart: Cheshbon's line of 13:18 Israel time (the Closer's word of 13:22) says the click's reach under T = 1 is where a_1 a_2 e^(-kappa d) falls under T, about 18 Links and not three, so at five Links the tails still overlap and there is no parting: the slow join, the transfer cycle about 11 intervals, the dissolution in about 30 to 70 intervals; a parting needs eighteen Links and is not laid here. The universe is the rule's own, built here from the universe of record with Cheshbon's table of 13:03 Israel time (Gamma = 12,000, a multiple of 6; the twist table regenerated for it; the two real fields' divisors 1, the well is the count; the matter pair [2, 3]; T = 1), until the universe file of record of the rule's universe (planck.json) lands beside universe.json and this script names it instead. Every count is the law's; no number of a run enters here. Run from the repository root: python examples/events/experiments/rules_universe/lay_out_join.py [--out <folder>]; the three files are written under this folder and nothing else."""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from event_universe.world_files import input_digest  # the mode file names the world by its digest

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent

UNIVERSE_OF_RECORD = "examples/events/planck.json"  # the rule's own universe of record (#1411): three rows, Gamma = 12,000, T = 1, the twist table at 4 Gamma 2^16
UNIVERSE_NAME = "rules_universe_over_gamma.json"  # a file of its own beside Bell's worlds' rules_universe.json, which keeps the form of #1403
ENGINE = "examples/events/engine_start.json"
GAMMA = 12_000  # the Node clock, a multiple of 6: every pair exact over it
QUANTUM_ACTION = 1  # T, the one unit
PAIRS_OVER_GAMMA = {
    "gravity": [1, 1],
    "charge": [1, 1],
    "matter": [8_000, 12_000],
}  # the three rows of planck.json (the Closer 13:52), the matter pair written over Gamma and the two real fields as [1, 1] (the loader derives their ranks from the pair [1, 1] itself; written as [12000, 12000] it refuses the spin's step by name) (Cheshbon 13:09, 14:12: THE WALL IS ONE, w = 6 Gamma^3; the loader's reduction to lowest terms shrank the walls and raised A to 1,334,399,890, so the count's line's int64 bound refused the world at interval 1, the finding of 13:58); the polarisation and the third are messages under the divisor 1 and leave the file
MATTER_PAIR = PAIRS_OVER_GAMMA["matter"]  # cos omega_0 = 2 / 3, the first pair past the exact bands
DIVISORS = {
    "gravity": 1,
    "charge": 400_000,
}  # the well is the count; the charge's divisor derived from Gamma, 0.86 (Gamma div 2)^(3 / 2), one quantum per window (Cheshbon's #1410, planck.json of #1411)
ENGINES = {  # the counts and the edge per engine (Cheshbon 14:12 Israel time): on the engine of today (the level read once) the edge is 0.345 Gamma = 4,136, so 3,000 and 4,000 disperse and 5,000 binds; with the corrected term the edge is 0.2255 Gamma = 2,706 and the counts return to 3,000 and 4,000 (the Closer 14:30)
    "today": {"small": 5_000, "deep": 6_000, "edge": 4_136},
    "term": {"small": 3_000, "deep": 4_000, "edge": 2_706},
}
COUNT_SMALL = ENGINES["today"]["small"]  # the smaller body's count; main() sets the three from --engine
COUNT_DEEP = ENGINES["today"]["deep"]  # the deeper body's count: the tail biased toward it
EDGE = ENGINES["today"]["edge"]  # the edge of the bound body
JOIN_DISTANCE = 2  # Links between the two Nodes: the tails overlap (the tail ends within three Links)
PART_DISTANCE = 5  # Links between the two Nodes: the tails still overlap (the click's reach is about 18), the slow join
TICKS = 300  # the run's length in intervals: the Experimenter's proposal until Cheshbon's blind number of clicks
STEPS = 1024  # N, the phase's steps
PIXELS = {  # Cheshbon's numbers per count (14:12 Israel time): the bound rotation omega_b and the tail's kappa per Link on the engine of today (the level once); 3,000 and 4,000 under the corrected term (13:39, 13:41)
    3_000: {"omega_b": 0.8105, "kappa": 0.446, "a": 90_326, "t": 41_943},
    4_000: {"omega_b": 0.6578, "kappa": 1.02, "a": 103_722, "t": 23_724},
    5_000: {"omega_b": 0.778, "kappa": 0.63, "a": 93_270, "t": 34_734},
    6_000: {"omega_b": 0.674, "kappa": 0.98, "a": 102_340, "t": 24_904},
    7_000: {"omega_b": 0.564, "kappa": 1.20},
}
CLOCK_UNIT = 1 << 16  # den of the clock pair [a, den], 2 cos omega_b = a / den (Cheshbon 13:51)
TAIL_UNIT = 1 << 16  # the tail's ratio t = e^(-kappa) as a pair over 2^16 (Cheshbon 14:12)
DENOMINATOR = 1024  # every body's phase denominator
FACE_DEPTH = 3
SHAPE = [32, 9, 1]
AXIS_Y = 4  # the bodies' row
LEFT_X = 7  # the smaller body's Node; the deeper at LEFT_X + the distance


def rules_universe(folder: Path) -> str:
    """The rule's own universe of record with its three rows written over Gamma (the pairs' numerators m over Gamma, THE WALL IS ONE), written beside the worlds; the path the worlds name, relative to the repository root where the folder lies under it. When planck.json itself carries the pairs over Gamma the worlds name it directly."""
    document = json.loads((ROOT / UNIVERSE_OF_RECORD).read_text(encoding="utf-8"))
    document["families"] = [
        {**family, "pair": list(PAIRS_OVER_GAMMA[family["name"]])}
        for family in document["families"]
        if family["name"] in PAIRS_OVER_GAMMA
    ]
    for family in document["families"]:
        if "held" in family:
            family["held"] = {**family["held"], "divisor": DIVISORS[family["name"]]}
    path = folder / UNIVERSE_NAME
    path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def pixel(x: int, count: int) -> dict[str, Any]:
    """A bound body of one Node at rest: the count in the Node, no momentum."""
    return {
        "family": "matter",
        "nodes": [{"node": [x, AXIS_Y, 0], "count": count}],
        "q": 1,  # THE SIGN IS THE BODY'S: a body of the rule's universe is its count at its Node and its q (the owner's word of 14:32 Israel time)
        "momentum": [0, 0, 0],
        "momentum_before": [0, 0, 0],
        "phase_denominator": DENOMINATOR,
    }


def world(universe: str, distance: int) -> dict[str, Any]:
    """Two bound bodies of one Node on the row, the smaller at the left and the deeper `distance` Links to its right; the readings: the matter level at both Nodes every interval, its support and total, both bodies' momentum, the records alive."""
    right = LEFT_X + distance
    readings: list[dict[str, Any]] = [
        {"name": f"matter_x{x}", "kind": "level", "family": "matter", "node": [x, AXIS_Y, 0], "every": 1}
        for x in (LEFT_X, right)
    ] + [
        {"name": "matter_support", "kind": "support", "family": "matter", "every": 5},
        {"name": "matter_total", "kind": "total", "family": "matter", "every": 5},
        {"name": "left_momentum", "kind": "momentum", "body": 0, "every": 10},
        {"name": "right_momentum", "kind": "momentum", "body": 1, "every": 10},
        {"name": "records_alive", "kind": "alive", "every": 10},
    ]
    return {
        "shape": SHAPE,
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "ticks": TICKS,
        "N": STEPS,
        "engine": ENGINE,
        "universe": universe,
        "measured": [pixel(LEFT_X, COUNT_SMALL), pixel(right, COUNT_DEEP)],
        "detectors": [],
        "readings": readings,
        "face_depth": FACE_DEPTH,
    }


def pixel_mode(document: dict[str, Any]) -> dict[str, Any]:
    """The mode file of the two pixels by Cheshbon's line of 14:12 Israel time (the Moving Clock's tool `tools/pixel_mode.py` writes the same when it carries the tail): the bound state's profile in integers, the amplitude at the Node b = isqrt(c T den div (2 den - a)) from the clock pair [a, den] (the form D = now^2 - next before at rest with now = before = b gives the count c = D div T), the tail on the neighbours b t^n rounded at the Manhattan distance n Links, t = e^(-kappa) as a pair over 2^16, until the level falls under 1; both time levels equal at every Node (the standing phase); the world's digest names the world."""
    shape = document["shape"]
    count = shape[0] * shape[1] * shape[2]
    bodies = []
    for body in document["measured"]:
        node = body["nodes"][0]
        c = node["count"]
        numbers = PIXELS[c]
        a = numbers.get("a") or round(
            2 * math.cos(numbers["omega_b"]) * CLOCK_UNIT
        )  # the stated pair over 2^16 where given (Cheshbon 13:51, the Closer 14:17)
        amplitude = math.isqrt(c * QUANTUM_ACTION * CLOCK_UNIT // (2 * CLOCK_UNIT - a))
        tail = numbers.get("t") or round(
            math.exp(-numbers["kappa"]) * TAIL_UNIT
        )  # the stated pair over 2^16 where given (Cheshbon 14:12, the Closer 14:16)
        x0, y0, z0 = node["node"]
        profile = [0] * count
        for x in range(shape[0]):
            for y in range(shape[1]):
                for z in range(shape[2]):
                    distance = abs(x - x0) + abs(y - y0) + abs(z - z0)
                    level = amplitude * tail**distance // TAIL_UNIT**distance
                    if level >= 1:
                        profile[(x * shape[1] + y) * shape[2] + z] = level
        bodies.append(
            {
                "family": body["family"],
                "pair": list(MATTER_PAIR),
                "profile": profile,
                "clock": [a, CLOCK_UNIT],
                "moving": {"now": profile, "before": list(profile)},
                "recipe": {
                    "row": "Cheshbon 14:12: b = isqrt(c T den div (2 den - a)) at the Node, b t^n on the neighbours at the Manhattan distance n, t = e^(-kappa) over 2^16, both levels equal",
                    "count": c,
                    "amplitude": amplitude,
                    "tail_over_2_16": tail,
                    "omega_b": numbers["omega_b"],
                    "kappa": numbers["kappa"],
                },
            }
        )
    return {"rest": {}, "bodies": bodies, "world_digest": input_digest(document)}


def write_mode(world_path: Path, document: dict[str, Any]) -> None:
    """The mode file beside the world: by the Moving Clock's tool `tools/pixel_mode.py` (the generator of the rule's universe, the owner's word of 14:32 Israel time: the input a count at a Node with the clock pair and the tail's ratio, the output the bound state) where the tool is in the tree, else by the recipe here until it lands."""
    tool = ROOT / "tools" / "pixel_mode.py"
    if not tool.exists():
        world_path.with_suffix(".mode.json").write_text(
            json.dumps(pixel_mode(document)) + "\n", encoding="utf-8"
        )
        return
    command = [
        sys.executable,
        str(tool),
        "--input",
        str(world_path),
        "--out",
        str(world_path.with_suffix(".mode.json")),
    ]
    for body in document["measured"]:
        c = body["nodes"][0]["count"]
        numbers = PIXELS[c]
        a = numbers.get("a") or round(2 * math.cos(numbers["omega_b"]) * CLOCK_UNIT)
        t = numbers.get("t") or round(math.exp(-numbers["kappa"]) * TAIL_UNIT)
        command += ["--clock", str(c), str(a), str(CLOCK_UNIT), "--tail", str(c), str(t)]
    subprocess.run(command, check=True, cwd=ROOT, env={**os.environ, "PYTHONPATH": str(ROOT / "src")})


def expectation(name: str, distance: int) -> dict[str, Any]:
    """The blind expectation: the law's row in words (THE CLICK JOINS AND PARTS), the numbers Cheshbon gives before the run, the reversible row over the whole run; no number of a run."""
    near = distance <= 3
    return {
        "format": "world-expectation-v1",
        "status": "BLIND: the row of THE CLICK JOINS AND PARTS; Cheshbon's numbers before the run; no number of a run here",
        "row": (
            f"ALGEBRA.md THE CLICK JOINS AND PARTS: two bound bodies of one Node, the counts {COUNT_SMALL:,} and {COUNT_DEEP:,} (the edge {EDGE:,} on the engine of today, Cheshbon 14:12), on the rule's own universe "
            f"(Gamma = 12,000, the divisors 1, the pair [2, 3], T = 1), {distance} Links apart: "
            + (
                "their tails overlap (kappa per Link in the blind numbers), the count's line reads the overlap and clicks, "
                "the tail biased toward the deeper, so the smaller gives quantum by quantum to the deeper until its count falls under the edge "
                "0.2255 Gamma = 2,706 and dissolves; one record for the joined cluster (the one non-local act)"
                if near
                else "the tails still overlap (the click's reach under T = 1 is about 18 Links, Cheshbon 13:18), so there is no parting at five Links: the slow join, the transfer cycle about 11 intervals, the smaller dissolved in about 30 to 70 intervals, one record"
            )
        ),
        "DETECTOR": [],
        "blind": {
            "row": "Cheshbon's numbers of 13:03 and 13:18 Israel time (2026-09-28) before the run: under T = 1 every remainder crosses, the first click at interval 1; the join at two Links (the overlap 0.41, the transfer about 0.33 radians per interval) dissolves the smaller within about 3 to 10 intervals; at five Links (the overlap 0.107, 0.087 radians per interval) within about 30 to 70; the click's reach is about 18 Links, so neither world parts",
            "edge_quanta_per_node": EDGE,
            "horizon_quanta_per_node": 6000,
            "counts": [COUNT_SMALL, COUNT_DEEP],
            "tail_kappa_per_link": {str(c): PIXELS[c]["kappa"] for c in (COUNT_SMALL, COUNT_DEEP)},
            "bound_rotation": {str(c): PIXELS[c]["omega_b"] for c in (COUNT_SMALL, COUNT_DEEP)},
            "click_reach_links": 18,
            "first_click_interval": 1,
            "dissolution_intervals": [3, 10] if near else [30, 70],
            "clicks_expected": "a run of clicks from the smaller to the deeper until the smaller's record ends",
            "records_at_the_end": 1,
        },
        "GAMEBOARD": [
            {
                "reversible": TICKS,
                "row": "the whole run forward and back on a fresh copy, every row bit for bit, the clicks keep the clicks; a diagnostic, MATCH or MISS with the first interval and Node that deviate",
            }
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE, help="the folder the files are written into")
    parser.add_argument(
        "--engine",
        choices=sorted(ENGINES),
        default="today",
        help="the counts and the edge: today (the level read once) or term (the corrected term)",
    )
    args = parser.parse_args()
    global COUNT_SMALL, COUNT_DEEP, EDGE  # noqa: PLW0603  (the script's three numbers from the option)
    COUNT_SMALL, COUNT_DEEP, EDGE = (ENGINES[args.engine][key] for key in ("small", "deep", "edge"))
    folder = args.out.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    universe = rules_universe(folder)
    for name, distance in (("join", JOIN_DISTANCE), ("part", PART_DISTANCE)):
        document = world(universe, distance)
        (folder / f"{name}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        write_mode(folder / f"{name}.json", document)
        (folder / f"{name}.expectation.json").write_text(
            json.dumps(expectation(name, distance), indent=1) + "\n", encoding="utf-8"
        )
    print(
        json.dumps(
            {
                "universe": universe,
                "worlds": ["join", "part"],
                "counts": [COUNT_SMALL, COUNT_DEEP],
                "gamma": GAMMA,
            }
        )
    )


if __name__ == "__main__":
    main()
