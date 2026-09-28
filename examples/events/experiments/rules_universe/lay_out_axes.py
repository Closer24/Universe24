"""WORLDS (a) AND (b) OF THE RULE'S OWN UNIVERSE: THE WHITE PIXEL AND THE PULLED PIXEL (ALGEBRA.md THE RULE'S OWN UNIVERSE, THE BOUND BODY IS ONE NODE, THE COLOURS ARE THE THREE AXES; the owner's word of 2026-09-28, 13:41 and 13:44 Israel; Cheshbon's line of 13:46 and the Closer's assignment of 13:52): the colours are the three tallies sigma_a of the count's line, one per axis, and a white body is a pixel of the matter pair [2, 3] whose tallies balance at rest: an isotropic tail carries no net current through any Port, the remainders on +x, -x, +y, -y, +z, -z are equal and the net tally on every axis is 0. (a) `white_pixel`: one bound body of one Node of 3,000 quanta (above the edge 0.2255 Gamma = 2,706) at rest in the middle of a chain, a detector on it; Cheshbon's blind numbers: the raw clicks about 10^3 per interval through each of the six Ports, 1 : 1 : 1 over the axes, the net 0 : 0 : 0, the first click at interval 1 under T = 1. (b) `pulled_pixel_<d>`: the same pixel pulled along x by a second pixel of 3,000 (a body under the edge, 1,000, disperses within about ten intervals and its pull passes) at d = 2, 4 and 6 Links; the pull is the transfer rate omega_b e^(-kappa d), falling with the distance, no constant tension and no linear potential: the net tally along x about 1,000, 410 and 170 quanta per interval at the pulse's peak, y and z 0, the net over the axes 1 : 0 : 0 and the raw 1 : 1 : 1. The reader axis_tallies.py reads both from the clicks' tallies at the detector. Run from the repository root: python examples/events/experiments/rules_universe/lay_out_axes.py; it writes the four worlds and their expectation files beside the universe file of world (d); the pixel's mode file is the clock's tool's."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from lay_out_join import DENOMINATOR, ENGINE, ROOT, STEPS, UNIVERSE_NAME  # noqa: E402

COUNT = 3_000  # the pixel's count, in [0.2255 Gamma, Gamma div 2) = [2,706, 6,000): it binds itself
PULLS = (0, 2, 4, 6)  # the second pixel's distance in Links along x; 0 the white pixel alone
NET_X = {
    2: 1000,
    4: 410,
    6: 170,
}  # Cheshbon's blind number of 13:46 Israel: the net tally along x, quanta per interval at the pulse's peak
RAW_PER_PORT = 1000  # Cheshbon's blind number: the raw clicks (both signs) per interval through each of the six Ports, about
TICKS = 300  # the run's length in intervals: the Experimenter's proposal until Cheshbon's number of intervals
SHAPE = [15, 3, 3]  # a chain along x, open at both ends, three wide: six Ports with a neighbour each
FACE_DEPTH = 1
AXIS = [1, 1]  # the row's y and z
BODY_X = 4  # the white pixel's Node; the second pixel toward +x


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
    net = [NET_X[pull], 0, 0] if pull else [0, 0, 0]
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
            "row": "Cheshbon's numbers of 13:46 Israel time (2026-09-28) before the run: the raw clicks about 10^3 per interval through each of the six Ports, 1 : 1 : 1 over the axes; at rest the net 0 : 0 : 0; pulled at 2, 4 and 6 Links the net tally along x about 1,000, 410 and 170 quanta per interval at the pulse's peak (M omega_b e^(-kappa d)), y and z 0, the net 1 : 0 : 0; the first click at interval 1 under T = 1; a puller under the edge (1,000) disperses within about ten intervals",
            "edge_quanta_per_node": 2706,
            "horizon_quanta_per_node": 6000,
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
            "band": None,
            "row": "axis_tallies.py reads the clicks at the pixel's detector: per axis the net tally (the sum of the tallies' components) and the raw (the sum of their magnitudes), the net per interval at the peak interval, the net and the raw over the axes, the first click's interval; MATCH within `band` of `net_per_interval` on every axis once Cheshbon writes it, else the reading alone; the net 0 on every axis reads white (DETECTOR: the clicks; the tallies a reading of them)",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE, help="the folder the files are written into")
    args = parser.parse_args()
    folder = args.out.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    universe = (folder / UNIVERSE_NAME).relative_to(ROOT).as_posix()
    for pull in PULLS:
        name = f"pulled_pixel_{pull}" if pull else "white_pixel"
        (folder / f"{name}.json").write_text(
            json.dumps(world(universe, pull), indent=1) + "\n", encoding="utf-8"
        )
        (folder / f"{name}.expectation.json").write_text(
            json.dumps(expectation(pull), indent=1) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
