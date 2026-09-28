"""WORLDS (a) AND (b) OF THE RULE'S OWN UNIVERSE: THE WHITE PIXEL AND THE PULLED PIXEL (ALGEBRA.md THE RULE'S OWN UNIVERSE, THE BOUND BODY IS ONE NODE, THE COLOURS ARE THE THREE AXES; the owner's word of 2026-09-28, 13:41 and 13:44 Israel; Cheshbon's line of 13:46 and the Closer's assignment of 13:52): the colours are the three tallies sigma_a of the count's line, one per axis, and a white body is a pixel of the matter pair [2, 3] whose tallies balance at rest: an isotropic tail carries no net current through any Port, the remainders on +x, -x, +y, -y, +z, -z are equal and the net tally on every axis is 0. (a) `white_pixel`: one bound body of one Node of 3,000 quanta (above the edge 0.2255 Gamma = 2,706) at rest in the middle of a chain, a detector on it; Cheshbon's blind numbers: the raw clicks about 10^3 per interval through each of the six Ports, 1 : 1 : 1 over the axes, the net 0 : 0 : 0, the first click at interval 1 under T = 1. (b) `pulled_pixel_<d>`: the same pixel pulled along x by a second pixel of 3,000 (a body under the edge, 1,000, disperses within about ten intervals and its pull passes) at d = 2, 4 and 6 Links; the pull is the transfer rate omega_b e^(-kappa d), falling with the distance, no constant tension and no linear potential: the net tally along x about 1,000, 410 and 170 quanta per interval at the pulse's peak, y and z 0, the net over the axes 1 : 0 : 0 and the raw 1 : 1 : 1. The reader axis_tallies.py reads both from the clicks' tallies at the detector. Run from the repository root: python examples/events/experiments/rules_universe/lay_out_axes.py; it writes the four worlds and their expectation files beside the universe file of world (d); the pixel's mode file is the clock's tool's."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

from event_universe.world_files import input_digest  # the mode file names the world by its digest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[3] / "tools"))
from lay_out_join import (  # noqa: E402
    CLOCK_UNIT,
    DENOMINATOR,
    ENGINE,
    PIXELS,
    QUANTUM_ACTION,
    ROOT,
    STEPS,
)
from pixel_mode import (  # noqa: E402  (the generator of the rule's universe, #1417)
    TAIL_UNIT,
    pixel_entry,
)

COUNT = 4_400  # the pixel's count on the engine of today (the level once): the bound window is 4,133 <= c <= about 5,900 (Cheshbon 14:39 Israel), the Closer's word of 14:47: (a) and (c) on 4,400; 3,000 again with the corrected term
PIXEL_NUMBERS = {
    **PIXELS,
    4_400: {"omega_b": 0.8290, "kappa": 0.283, "a": 88_553},
}  # Cheshbon's numbers per count on the engine of today (14:39 Israel: 4,400 gives omega_b 0.8290, the period 7.58, kappa 0.283, t 0.754) beside lay_out_join's table
PULLS = (0, 2, 4, 6)  # the second pixel's distance in Links along x; 0 the white pixel alone
TAIL = {
    3_000: 41_943,
    4_000: 23_724,
    4_400: 49_395,
    5_000: 34_734,
    6_000: 24_904,
}  # Cheshbon's tail factor t = e^(-kappa) over 2^16 per count (14:12 Israel; the Closer 14:16), stated in integers
EDGE_RATIO = (
    0.2255,
    0.3444,
)  # the edge of the bound body over Gamma: under the corrected term (ALGEBRA.md THE BOUND BODY IS ONE NODE) and on the engine of today, the level once (Cheshbon 14:12 and 14:39 Israel)


def gamma_of(universe: str) -> int:
    """The Node clock Gamma of the universe file the worlds name (12,000 today; 24 by the owner's word of 15:11 Israel)."""
    return int(json.loads((ROOT / universe).read_text(encoding="utf-8"))["integers"]["node_clock"])


def edges(gamma: int) -> dict[str, int]:
    """The blind section's numbers from Gamma alone: the edge under the term, the edge on the engine of today and the horizon Gamma div 2."""
    return {
        "edge_quanta_per_node": round(EDGE_RATIO[0] * gamma),
        "edge_quanta_per_node_level_once": round(EDGE_RATIO[1] * gamma),
        "horizon_quanta_per_node": gamma // 2,
    }


BAND = 0.3  # the band on every blind number, the Closer's word of 14:16 Israel: plus or minus 30 percent
RAW_PER_PORT = 1000  # Cheshbon's blind number of 13:46 Israel at 3,000: the raw clicks (both signs) per interval through each of the six Ports, about
PLANCK = "examples/events/planck.json"  # the rule's own universe of record (#1411, #1419): three rows over Gamma, gravity [12000, 12000] at the divisor 1, charge [12000, 12000] at 400,000, matter [8000, 12000], T = 1; the polarisation and the third are messages and not in the file (the Closer 13:52, 14:29)
TICKS = 300  # the run's length in intervals: the Experimenter's proposal until Cheshbon's number of intervals
SHAPE = [15, 3, 3]  # a chain along x, open at both ends, three wide: six Ports with a neighbour each
FACE_DEPTH = 1
AXIS = [1, 1]  # the row's y and z
BODY_X = 4  # the white pixel's Node; the second pixel toward +x


def net_along_x(count: int, distance: int) -> int:
    """Cheshbon's blind number of 13:46 Israel for the pull: the net tally along the axis about M omega_b e^(-kappa d) quanta per interval at the pulse's peak (1,000, 410 and 170 at 3,000 and 2, 4, 6 Links), with omega_b and kappa of the count on the engine of the day."""
    numbers = PIXEL_NUMBERS[count]
    return round(count * numbers["omega_b"] * math.exp(-numbers["kappa"] * distance))


def one_node(x: int, count: int) -> dict[str, Any]:
    """A body of one Node at rest on the row: the count in the Node, no momentum (a body with no giving and no momentum loads as content alone unless its mode carries a record)."""
    return {
        "family": "matter",
        "nodes": [{"node": [x, *AXIS], "count": count}],
        "momentum": [0, 0, 0],
        "momentum_before": [0, 0, 0],
        "phase_denominator": DENOMINATOR,
    }


def neighbours(x: int) -> list[list[int]]:
    """The Node and its six neighbours, one through each Port."""
    node = [x, *AXIS]
    return [node] + [
        [node[0] + dx, node[1] + dy, node[2] + dz]
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    ]


def pixel_mode(document: dict[str, Any], tail: bool) -> dict[str, Any]:
    """The mode file of the pixels by the generator of the rule's universe, `tools/pixel_mode.py` (#1417; Cheshbon's line of 14:12 Israel, the owner's word of 14:32: a body is its count at its Node and its record is the bound state from the count alone): each pixel's entry from the tool's `pixel_entry` with the clock pair [a, den] and the tail's factor t over 2^16 of its count from Cheshbon's table `PIXELS` (b = isqrt(c T den div (2 den - a)) at the Node, round(b t^d) at the Manhattan distance d, the twist as the generator's); without `tail` the factor is 0 (the Node alone, a diagnostic); a body under the edge binds no record and stays content alone; the world's digest names the world."""
    universe = json.loads((ROOT / document["universe"]).read_text(encoding="utf-8"))
    pairs = {family["name"]: list(family["pair"]) for family in universe["families"]}
    integers = universe["integers"]
    twist_scale = int(integers["twist_table"]["unit"]) // (4 * int(integers["node_clock"]))
    bodies = []
    for number, body in enumerate(document["measured"]):
        count = int(body["nodes"][0]["count"])
        if (
            count not in PIXEL_NUMBERS
        ):  # a body under the edge (no bound rotation of its own) binds no record: content alone
            bodies.append(
                {
                    "family": body["family"],
                    "pair": pairs[body["family"]],
                    "mode": "none: content alone, under the edge",
                }
            )
            continue
        numbers = PIXEL_NUMBERS[count]
        a = numbers.get("a") or round(2 * math.cos(numbers["omega_b"]) * CLOCK_UNIT)
        factor = TAIL.get(count) or round(math.exp(-numbers["kappa"]) * TAIL_UNIT) if tail else 0
        row = (a, CLOCK_UNIT, factor)
        entry = pixel_entry(
            number, body, document, pairs[body["family"]], QUANTUM_ACTION, row, twist_scale
        )
        bodies.append({**entry, "omega_b": numbers["omega_b"], "kappa": numbers["kappa"]})
    return {"world_digest": input_digest(document), "bodies": bodies}


def world(universe: str, pull: int) -> dict[str, Any]:
    """The pixel at BODY_X with a detector on it and, where `pull` is above 0, the second pixel `pull` Links toward +x with a detector of its own; the readings: the matter level at the pixel's Node and its six neighbours every interval (the tail through every Port), the matter rows, each body's centre and momentum every interval (the momentum a reading of the record's current), the support and total, the records alive."""
    measured = [one_node(BODY_X, COUNT)] + ([one_node(BODY_X + pull, COUNT)] if pull else [])
    detectors = [{"name": "at_pixel", "block": 0}] + (
        [{"name": "at_puller", "block": 1}] if pull else []
    )
    readings: list[dict[str, Any]] = [
        {"name": f"matter_{i}", "kind": "level", "family": "matter", "node": node, "every": 1}
        for i, node in enumerate(neighbours(BODY_X))
    ]
    for body in range(len(measured)):
        readings += [
            {"name": f"centre_{body}", "kind": "centre", "body": body, "every": 1},
            {"name": f"momentum_{body}", "kind": "momentum", "body": body, "every": 1},
        ]
    readings += [
        {"name": "matter_rows", "kind": "rows", "family": "matter", "every": 10},
        {"name": "matter_support", "kind": "support", "family": "matter", "every": 5},
        {"name": "matter_total", "kind": "total", "family": "matter", "every": 5},
        {"name": "records_alive", "kind": "alive", "every": 10},
    ]
    return {
        "shape": SHAPE,
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": TICKS,
        "N": STEPS,
        "engine": ENGINE,
        "universe": universe,
        "measured": measured,
        "detectors": detectors,
        "readings": readings,
        "face_depth": FACE_DEPTH,
    }


def expectation(pull: int) -> dict[str, Any]:
    """The blind expectation: the law's row in words (THE COLOURS ARE THE THREE AXES), Cheshbon's numbers before the run, the reversible row; the `axes` section axis_tallies.py reads (the net tally per axis at the pulse's peak, the raw over the axes, the first click, the band Cheshbon's)."""
    net = [net_along_x(COUNT, pull), 0, 0] if pull else [0, 0, 0]
    return {
        "format": "world-expectation-v1",
        "status": "BLIND: the row of THE COLOURS ARE THE THREE AXES; Cheshbon's numbers before the run; no number of a run here",
        "row": (
            f"ALGEBRA.md THE COLOURS ARE THE THREE AXES, THE BOUND BODY IS ONE NODE: a bound body of one Node of {COUNT} quanta on the matter pair [2, 3] "
            "of the rule's own universe (Gamma = 12,000, the divisors 1, T = 1); the colours are the three tallies of the count's line, one per axis, "
            + (
                f"and a second pixel of {COUNT} quanta {pull} Links along +x pulls it: the transfer rate omega_b e^(-kappa d) falls with the distance (no constant tension, no linear potential), the clicks' tallies lean along x and balance on y and z: the pull is the clicks' bias along one axis"
                if pull
                else "and at rest they balance: an isotropic tail carries no net current through any Port, the net tally 0 on every axis: the pixel is white"
            )
        ),
        "DETECTOR": [],
        "blind": {
            "row": "Cheshbon's numbers of 13:46 Israel time (2026-09-28) before the run: the raw clicks about 10^3 per interval through each of the six Ports, 1 : 1 : 1 over the axes; at rest the net 0 : 0 : 0; pulled at 2, 4 and 6 Links the net tally along x about M omega_b e^(-kappa d) quanta per interval at the pulse's peak (1,000, 410 and 170 at 3,000 under the corrected term; at 5,000 on the engine of today with omega_b 0.778 and kappa 0.63 by the same line), y and z 0, the net 1 : 0 : 0; the first click at interval 1 under T = 1; a puller under the edge disperses within about ten intervals; the band plus or minus 30 percent (the Closer 14:16)",
            **edges(gamma_of(PLANCK)),
            "raw_clicks_per_port_per_interval": RAW_PER_PORT,
            "net_tally_per_interval": net,
            "first_click": 1,
        },
        "GAMEBOARD": [
            {
                "reversible": TICKS,
                "row": "the whole run forward and back on a fresh copy, every row bit for bit, the clicks keep the clicks; a diagnostic, MATCH or MISS with the first interval and Node that deviate",
            }
        ],
        "axes": {
            "detector": "at_pixel",
            "net_per_interval": net,
            "raw_ratio": [1, 1, 1],
            "first_click": 1,
            "band": BAND,
            "row": "axis_tallies.py reads the clicks at the pixel's detector: per axis the net tally (the sum of the tallies' components) and the raw (the sum of their magnitudes), the net per interval at the peak interval, the net and the raw over the axes, the first click's interval; MATCH within `band` of `net_per_interval` on every axis once Cheshbon writes it, else the reading alone; the net 0 on every axis reads white (DETECTOR: the clicks; the tallies a reading of them)",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE, help="the folder the files are written into")
    parser.add_argument("--no-tail", action="store_true", help="the mode files without the tail")
    args = parser.parse_args()
    folder = args.out.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    universe = PLANCK
    for pull in PULLS:
        name = f"pulled_pixel_{pull}" if pull else "white_pixel"
        document = world(universe, pull)
        (folder / f"{name}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        (folder / f"{name}.mode.json").write_text(
            json.dumps(pixel_mode(document, not args.no_tail)) + "\n", encoding="utf-8"
        )
        (folder / f"{name}.expectation.json").write_text(
            json.dumps(expectation(pull), indent=1) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
