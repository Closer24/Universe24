"""WORLD (c) OF THE RULE'S OWN UNIVERSE: THE FALL AS THE CLICKS' BIAS (ALGEBRA.md THE RULE'S OWN UNIVERSE, THE BOUND BODY IS ONE NODE, THE UNIVERSE IS BOUND; the owner's decision of 2026-09-28, 13:01 Israel; the Closer's assignment of 13:34; Cheshbon's layout and blind numbers of 13:09): a bound body of one Node on the matter pair [2, 3] (3,000 quanta, above the edge 0.2255 Gamma = 2,706) beside a cluster of pixels along +x (THE SCREEN IS A CLUSTER, Cheshbon 14:55 Israel: the heavy body is a sieve of bound pixels, a tent of held content is not a body), and a control with no cluster. The tail of the body's record on the two sides of its Node is the GameBoard reading (Cheshbon: the tail's ratio toward the well over away e^(-kappa_plus) / e^(-kappa_minus) = 1.025, 1.053 and 1.122 for the tents 50, 100 and 200, kappa_minus = 0.446), and the fall is the clicks' bias: the tail's remainder crosses T earlier on the well's side, so the count's line moves the body's quanta toward the well in the same ratio (51.2, 51.3 and 52.9 percent of the moves), read from the body's centre by fall_bias.py until a reading of the count's moves exists. Run from the repository root: python examples/events/experiments/rules_universe/lay_out_fall.py; it writes the control and one world per cluster with their expectation and mode files (the pixels' modes through tools/pixel_mode.py)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from lay_out_axes import (  # noqa: E402  (the pixels' modes through the tool)
    RECORD,
    edges,
    gamma_of,
    pixel_mode,
)
from lay_out_join import DENOMINATOR, ENGINE, STEPS  # noqa: E402

COUNT = 10  # the falling pixel's count at Gamma = 24 (Cheshbon's table of 15:22 Israel: the pixels 8 to 11 on the law; (a), (b), (c) at 10, b = 6); 4,400 on 12,000 was the second run
BAND = 0.15  # the band on every blind number at Gamma = 24: one quantum, plus or minus 10 to 15 percent (Cheshbon 15:22 Israel)
CLUSTERS: dict[str, dict[str, int] | None] = {
    "control": None,
    "sieve_1": {"pixels": 1, "spacing": 2, "count": 8, "distance": 2},
    "sieve_2": {"pixels": 2, "spacing": 2, "count": 8, "distance": 2},
    "sieve_4": {"pixels": 4, "spacing": 2, "count": 8, "distance": 2},
}  # THE SCREEN IS A CLUSTER (Cheshbon 14:55 Israel, the Closer 14:59): the heavy body is a cluster of pixels, a sieve along +x beyond the falling pixel: `pixels` how many, `spacing` the sieve's period in Links, `count` per pixel, `distance` in Links from the falling pixel to the first; Cheshbon's sieve at Gamma = 24 (15:22 Israel, item 6: pixels of 8 at the period 2), one, two and four of them in place of the tents 50, 100 and 200, the first two Links from the falling pixel (the click's reach at 24 about 3 to 4 Links, item 5c); None the control with no cluster
TAIL_RATIO: dict[
    str, float
] = {}  # the tail's ratio toward the cluster over away is under the rounding at Gamma = 24 (Cheshbon 15:22 Israel, item 5e: a shift of kappa about 0.05); read at 12,000, the second run (the Closer 15:30)
BIAS = {
    "sieve_1": 0.51,
    "sieve_2": 0.51,
    "sieve_4": 0.51,
}  # the blind share of the count's moves toward the cluster at Gamma = 24 by Cheshbon's line of 13:09 (the moves' bias in the tails' ratio) from his shift of 15:22, item 5e: about 0.05, so 0.51 within one quantum
KAPPA_AWAY = 1.269  # the tail's decay per Link away from the cluster at 10 on the law at Gamma = 24 (Cheshbon 15:22 Israel)
PLANCK = "examples/events/planck.json"  # the rule's own universe of record (#1411, #1419): three rows over Gamma, gravity [12000, 12000] at the divisor 1, charge [12000, 12000] at 400,000, matter [8000, 12000], T = 1; the polarisation and the third are messages and not in the file (the Closer 13:52, 14:29)
TICKS = 1000  # the run's length: the Experimenter's proposal until Cheshbon's number of moves
WIDTH = 3  # the chain's y and z: three wide, periodic, six Ports with a neighbour each
MARGIN = 4  # Links of chain beyond the last pixel and before the falling one, the faces open
FACE_DEPTH = 1
AXIS = [1, 1]  # the row's y and z
BODY_X = MARGIN  # the falling pixel's Node; the cluster toward +x, the well's side


def one_node(x: int, count: int) -> dict[str, Any]:
    """A body of one Node at rest on the row: the count in the Node, no momentum (a body with no giving and no momentum loads as content alone unless its mode carries a record)."""
    return {
        "family": "matter",
        "nodes": [{"node": [x, *AXIS], "count": count}],
        "momentum": [0, 0, 0],
        "momentum_before": [0, 0, 0],
        "phase_denominator": DENOMINATOR,
    }


def cluster_nodes(cluster: dict[str, int] | None) -> list[int]:
    """The x of every pixel of the cluster: from BODY_X + distance, one every `spacing` Links, `pixels` of them; none for the control."""
    if cluster is None:
        return []
    first = BODY_X + int(cluster["distance"])
    return [first + k * int(cluster["spacing"]) for k in range(int(cluster["pixels"]))]


def shape_of(cluster: dict[str, int] | None) -> list[int]:
    """The chain's length: the falling pixel, the cluster and MARGIN Links beyond its last pixel."""
    last = max(cluster_nodes(cluster), default=BODY_X)
    return [last + MARGIN + 1, WIDTH, WIDTH]


def world(universe: str, cluster: dict[str, int] | None) -> dict[str, Any]:
    """The falling pixel at BODY_X and the cluster's pixels along +x; the readings: the matter level at the falling pixel's Node and at both neighbours every interval (the tail on both sides), the gravity level at the three Nodes (the cluster's well), the matter rows, the falling pixel's centre and momentum, the support and total, the records alive."""
    measured = [one_node(BODY_X, COUNT)] + [
        one_node(x, int(cluster["count"])) for x in cluster_nodes(cluster)
    ]
    readings: list[dict[str, Any]] = (
        [
            {"name": f"matter_x{x}", "kind": "level", "family": "matter", "node": [x, *AXIS], "every": 1}
            for x in (BODY_X - 1, BODY_X, BODY_X + 1)
        ]
        + [
            {
                "name": f"gravity_x{x}",
                "kind": "level",
                "family": "gravity",
                "node": [x, *AXIS],
                "every": 100,
            }
            for x in (BODY_X - 1, BODY_X, BODY_X + 1)
        ]
        + [
            {"name": "matter_rows", "kind": "rows", "family": "matter", "every": 10},
            {"name": "body_centre", "kind": "centre", "body": 0, "every": 1},
            {"name": "body_momentum", "kind": "momentum", "body": 0, "every": 10},
            {"name": "matter_support", "kind": "support", "family": "matter", "every": 5},
            {"name": "matter_total", "kind": "total", "family": "matter", "every": 5},
            {"name": "records_alive", "kind": "alive", "every": 10},
        ]
    )
    return {
        "shape": shape_of(cluster),
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": TICKS,
        "N": STEPS,
        "engine": ENGINE,
        "universe": universe,
        "measured": measured,
        "detectors": [],
        "readings": readings,
        "face_depth": FACE_DEPTH,
    }


def expectation(name: str, cluster: dict[str, int] | None) -> dict[str, Any]:
    """The blind expectation: the law's row in words (THE UNIVERSE IS BOUND: the fall is the clicks' bias; THE SCREEN IS A CLUSTER: the heavy body a cluster of pixels), Cheshbon's numbers before the run where written, the reversible row; the `fall` section fall_bias.py reads (the tail's ratio and the moves' bias, the band 0.3)."""
    ratio, bias = TAIL_RATIO.get(name), BIAS.get(name)
    return {
        "format": "world-expectation-v1",
        "status": "BLIND: the row of THE UNIVERSE IS BOUND, the fall as the clicks' bias toward a cluster of pixels; Cheshbon's numbers before the run; no number of a run here",
        "row": (
            f"ALGEBRA.md THE UNIVERSE IS BOUND, THE BOUND BODY IS ONE NODE, THE SCREEN IS A CLUSTER: a bound body of one Node of {COUNT} quanta on the matter pair "
            "of the rule's own universe (Gamma = 12,000, the divisors 1, T = 1), its tail evanescent, "
            + (
                f"beside a cluster of {cluster['pixels']} pixels of {cluster['count']} quanta every {cluster['spacing']} Links along +x, the first {cluster['distance']} Links away: the wells of the cluster's pixels lower the pace on that side, the local band nearer the record's rotation, the tail longer there, and the tail's remainder crosses T earlier on that side: the fall is the clicks' bias toward the cluster, no force"
                if cluster
                else "with no cluster, the control: the tail alike on both sides, the count's moves unbiased, the body's centre standing within a Link"
            )
        ),
        "DETECTOR": [],
        "blind": {
            "row": "Cheshbon's numbers before the run (THE SCREEN IS A CLUSTER, 14:55 Israel time, 2026-09-28; the cluster's numbers asked at 15:05): the tail's ratio toward the cluster over away and the count's moves biased toward the cluster in the same ratio; the control 1 and 50 percent; the band plus or minus 30 percent (the Closer 14:16)",
            **edges(gamma_of(PLANCK)),
            "record": {"count": COUNT, **RECORD.get(COUNT, {})},
            "sieve_record": None
            if cluster is None
            else {"count": cluster["count"], **RECORD.get(int(cluster["count"]), {})},
            "tail_kappa_per_link_away": KAPPA_AWAY,
            "tail_ratio_well_over_away": ratio if cluster else 1.0,
            "moves_toward_well_share": bias if cluster else 0.5,
            "cluster": cluster,
        },
        "GAMEBOARD": [
            {
                "reversible": TICKS,
                "row": "the whole run forward and back on a fresh copy, every row bit for bit, the clicks keep the clicks; a diagnostic, MATCH or MISS with the first interval and Node that deviate",
            }
        ],
        "fall": {
            "body": [BODY_X, *AXIS],
            "well_side": [BODY_X + 1, *AXIS],
            "far_side": [BODY_X - 1, *AXIS],
            "axis": 0,
            "tail_ratio": ratio if cluster else 1.0,
            "bias": bias if cluster else 0.5,
            "band": BAND,
            "row": "fall_bias.py reads the tail's ratio from the matter levels at the two neighbours (the largest level on the cluster's side over the largest on the far side, GAMEBOARD) and the moves' bias from the body's centre along the axis (the moves toward the cluster over all moves, the count's line's clicks as the centre shows them); MATCH within `band` of Cheshbon's numbers once written, else the reading alone",
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
    for label, cluster in CLUSTERS.items():
        name = f"fall_{label}"
        document = world(universe, cluster)
        (folder / f"{name}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        (folder / f"{name}.mode.json").write_text(
            json.dumps(pixel_mode(document, not args.no_tail)) + "\n", encoding="utf-8"
        )
        (folder / f"{name}.expectation.json").write_text(
            json.dumps(expectation(label, cluster), indent=1) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
