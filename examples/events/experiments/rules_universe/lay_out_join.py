"""WORLD (d) OF THE RULE'S OWN UNIVERSE: THE CLICK JOINS AND PARTS (ALGEBRA.md #the-rows-against-nature, THE RULE'S OWN UNIVERSE, THE BOUND BODY IS ONE NODE, THE CLICK JOINS AND PARTS; the owner's decision of 2026-09-28, 13:02 Israel time, through the Closer: the rule's universe is the finish line, world (d) to the de Broglie Experimenter). Two worlds on one universe file: THE JOIN, two bound bodies of one Node each, the count 3,000 (above the edge 0.2255 Gamma = 2,706 and under the horizon Gamma div 2 = 6,000), two Links apart so that their tails overlap (kappa = 0.45 per Link at 3,000, the tail ends within three Links): the law's row is a run of clicks toward the deeper whose last ends the smaller's record, one record for the joined cluster; THE PARTING, the same two bodies five Links apart, beyond both tails: no click. The universe is the rule's own, built here from the universe of record with Cheshbon's table of 13:03 Israel time (Gamma = 12,000, a multiple of 6; the twist table regenerated for it; the two real fields' divisors 1, the well is the count; the matter pair [2, 3]; T = 1), until the universe file of record of the rule's universe (planck.json) lands beside universe.json and this script names it instead. Every count is the law's; no number of a run enters here. Run from the repository root: python examples/events/experiments/rules_universe/lay_out_join.py [--out <folder>]; the three files are written under this folder and nothing else."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "examples" / "events"))
from make_universe import twist_table  # noqa: E402  (the repository's own generator of the twist table)

UNIVERSE_OF_RECORD = "examples/events/experiments/universe.json"
UNIVERSE_NAME = "rules_universe.json"
ENGINE = "examples/events/engine_start.json"
GAMMA = 12_000  # the Node clock, a multiple of 6: every pair exact over it
QUANTUM_ACTION = 1  # T, the one unit
MATTER_PAIR = [2, 3]  # cos omega_0 = 2 / 3, the first pair past the exact bands
DIVISOR = 1  # the well is the count
COUNT = 3_000  # each body's count, in [0.2255 Gamma, Gamma div 2) = [2,706, 6,000)
JOIN_DISTANCE = 2  # Links between the two Nodes: the tails overlap (the tail ends within three Links)
PART_DISTANCE = 5  # Links between the two Nodes: beyond both tails
TICKS = 300  # the run's length in intervals: the Experimenter's proposal until Cheshbon's blind number of clicks
STEPS = 1024  # N, the phase's steps
DENOMINATOR = 1024  # every body's phase denominator
FACE_DEPTH = 3
SHAPE = [24, 9, 1]
AXIS_Y = 4  # the bodies' row
LEFT_X = 9  # the first body's Node; the second at LEFT_X + the distance


def rules_universe(folder: Path) -> str:
    """The rule's own universe, written beside the worlds: the universe of record with Cheshbon's table; the path the worlds name, relative to the repository root where the folder lies under it."""
    document = json.loads((ROOT / UNIVERSE_OF_RECORD).read_text(encoding="utf-8"))
    integers = document["integers"]
    integers["node_clock"] = GAMMA
    integers["quantum_action"] = QUANTUM_ACTION
    integers["twist_table"] = twist_table(GAMMA)
    for family in document["families"]:
        if "held" in family:
            family["held"] = {**family["held"], "divisor": DIVISOR}
        if family["name"] == "matter":
            family["pair"] = list(MATTER_PAIR)
    path = folder / UNIVERSE_NAME
    path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def pixel(x: int) -> dict[str, Any]:
    """A bound body of one Node at rest: the count in the Node, no momentum."""
    return {
        "family": "matter",
        "nodes": [{"node": [x, AXIS_Y, 0], "count": COUNT}],
        "momentum": [0, 0, 0],
        "momentum_before": [0, 0, 0],
        "phase_denominator": DENOMINATOR,
    }


def world(universe: str, distance: int) -> dict[str, Any]:
    """Two bound bodies of one Node on the row, `distance` Links apart; the readings: the matter level at both Nodes every interval, its support and total, both bodies' momentum, the records alive."""
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
        "measured": [pixel(LEFT_X), pixel(right)],
        "detectors": [],
        "readings": readings,
        "face_depth": FACE_DEPTH,
    }


def expectation(name: str, distance: int) -> dict[str, Any]:
    """The blind expectation: the law's row in words (THE CLICK JOINS AND PARTS), the numbers Cheshbon gives before the run, the reversible row over the whole run; no number of a run."""
    joins = distance <= 3
    return {
        "format": "world-expectation-v1",
        "status": "BLIND: the row of THE CLICK JOINS AND PARTS; Cheshbon's numbers before the run; no number of a run here",
        "row": (
            "ALGEBRA.md THE CLICK JOINS AND PARTS: two bound bodies of one Node at the count 3,000 on the rule's own universe "
            f"(Gamma = 12,000, the divisors 1, the pair [2, 3], T = 1), {distance} Links apart: "
            + (
                "their tails overlap (kappa = 0.45 per Link, the tail ends within three Links), the count's line reads the overlap and clicks, "
                "the tail biased toward the deeper, so one gives quantum by quantum to the other until its count falls under the edge "
                "0.2255 Gamma = 2,706 and dissolves; one record for the joined cluster (the one non-local act)"
                if joins
                else "beyond both tails the Link's current leaves no remainder crossing T: no click, the two bodies stay parted, two records"
            )
        ),
        "DETECTOR": [],
        "blind": {
            "row": "Cheshbon's numbers of 13:03 Israel time (2026-09-28) before the run; the count of clicks and the first click's interval asked on #1325",
            "edge_quanta_per_node": 2706,
            "horizon_quanta_per_node": 6000,
            "tail_kappa_per_link_at_3000": 0.45,
            "clicks_expected": "a run of clicks toward the deeper until the smaller's record ends"
            if joins
            else 0,
            "records_at_the_end": 1 if joins else 2,
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
    args = parser.parse_args()
    folder = args.out.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    universe = rules_universe(folder)
    for name, distance in (("join", JOIN_DISTANCE), ("part", PART_DISTANCE)):
        (folder / f"{name}.json").write_text(
            json.dumps(world(universe, distance), indent=1) + "\n", encoding="utf-8"
        )
        (folder / f"{name}.expectation.json").write_text(
            json.dumps(expectation(name, distance), indent=1) + "\n", encoding="utf-8"
        )
    print(json.dumps({"universe": universe, "worlds": ["join", "part"], "count": COUNT, "gamma": GAMMA}))


if __name__ == "__main__":
    main()
