"""WORLD (c) OF THE RULE'S OWN UNIVERSE: THE FALL AS THE CLICKS' BIAS (ALGEBRA.md THE RULE'S OWN UNIVERSE, THE BOUND BODY IS ONE NODE, THE UNIVERSE IS BOUND; the owner's decision of 2026-09-28, 13:01 Israel; the Closer's assignment of 13:34; Cheshbon's layout and blind numbers of 13:09): a bound body of one Node on the matter pair [2, 3] (3,000 quanta, above the edge 0.2255 Gamma = 2,706) beside a tent of the held gravity, a content-only body of 50, 100 or 200 quanta at the neighbouring Node (under the divisor 1 the well is the count, so the tent lays a pace gradient over the body), and a control with no tent. The tail of the body's record on the two sides of its Node is the GameBoard reading (Cheshbon: the tail's ratio toward the well over away e^(-kappa_plus) / e^(-kappa_minus) = 1.025, 1.053 and 1.122 for the tents 50, 100 and 200, kappa_minus = 0.446), and the fall is the clicks' bias: the tail's remainder crosses T earlier on the well's side, so the count's line moves the body's quanta toward the well in the same ratio (51.2, 51.3 and 52.9 percent of the moves), read from the body's centre by fall_bias.py until a reading of the count's moves exists. Run from the repository root: python examples/events/experiments/rules_universe/lay_out_fall.py; it writes the four worlds and their expectation files beside the universe file of world (d); the mode files come from tools/body_generator.py."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from lay_out_axes import pixel_mode  # noqa: E402  (the pixels' mode files by the recipe)
from lay_out_join import DENOMINATOR, ENGINE, ROOT, STEPS, UNIVERSE_NAME  # noqa: E402

COUNT = 3_000  # the body's count, in [0.2255 Gamma, Gamma div 2) = [2,706, 6,000): it binds itself
TENTS = (
    0,
    50,
    100,
    200,
)  # the tent's count at the neighbouring Node, Cheshbon's layout of 13:09 Israel; 0 the control without a tent
TAIL_RATIO = {
    50: 1.025,
    100: 1.053,
    200: 1.122,
}  # Cheshbon's blind number: the tail toward the well over the tail away, e^(-kappa_plus) / e^(-kappa_minus), kappa_minus = 0.446
BIAS = {
    50: 0.512,
    100: 0.513,
    200: 0.529,
}  # Cheshbon's blind number: the share of the count's moves toward the well
KAPPA_AWAY = 0.446  # the tail's decay per Link away from the well at 3,000
TICKS = 1000  # the run's length: the Experimenter's proposal until Cheshbon's number of moves
SHAPE = [9, 3, 3]  # Cheshbon's board: the chain of 9 along x, open at both ends, three wide
FACE_DEPTH = 1
AXIS = [1, 1]  # the row's y and z
BODY_X = 4  # the body's Node; the tent one Link toward +x, the well's side
TENT_X = 5


def one_node(x: int, count: int) -> dict[str, Any]:
    """A body of one Node at rest on the row: the count in the Node, no momentum (a body with no giving and no momentum loads as content alone unless its mode carries a record)."""
    return {
        "family": "matter",
        "nodes": [{"node": [x, *AXIS], "count": count}],
        "momentum": [0, 0, 0],
        "momentum_before": [0, 0, 0],
        "phase_denominator": DENOMINATOR,
    }


def world(universe: str, tent: int) -> dict[str, Any]:
    """The body at BODY_X and, where the tent's count is above 0, the tent at TENT_X; the readings: the matter level at the body's Node and at both neighbours every interval (the tail on both sides), the gravity level at the three Nodes (the tent's field), the matter rows (the level over the board), the body's centre and momentum, the support and total, the records alive."""
    measured = [one_node(BODY_X, COUNT)] + ([one_node(TENT_X, tent)] if tent else [])
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
        "shape": SHAPE,
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


def expectation(tent: int) -> dict[str, Any]:
    """The blind expectation: the law's row in words (THE UNIVERSE IS BOUND: the fall is the clicks' bias), Cheshbon's numbers before the run, the reversible row; the `fall` section fall_bias.py reads (the tail's ratio and the moves' bias, the band Cheshbon's)."""
    ratio, bias = TAIL_RATIO.get(tent), BIAS.get(tent)
    return {
        "format": "world-expectation-v1",
        "status": "BLIND: the row of THE UNIVERSE IS BOUND, the fall as the clicks' bias; Cheshbon's numbers before the run; no number of a run here",
        "row": (
            f"ALGEBRA.md THE UNIVERSE IS BOUND, THE BOUND BODY IS ONE NODE: a bound body of one Node of {COUNT} quanta on the matter pair [2, 3] "
            "of the rule's own universe (Gamma = 12,000, the divisors 1, T = 1), its tail evanescent by kappa = 0.446 per Link, "
            + (
                f"beside a tent of the held gravity, a content-only body of {tent} quanta one Link toward +x: the well is the count, so the pace on the well's side is lower, the local band nearer the record's rotation, the tail longer there, and the tail's remainder crosses T earlier on that side: the fall is the clicks' bias toward the well, no force"
                if tent
                else "with no tent, the control: the tail alike on both sides, the count's moves unbiased, the body's centre standing within a Link"
            )
        ),
        "DETECTOR": [],
        "blind": {
            "row": "Cheshbon's numbers of 13:09 Israel time (2026-09-28) before the run: the tail's ratio toward the well over away e^(-kappa_plus) / e^(-kappa_minus) = 1.025, 1.053 and 1.122 for the tents 50, 100 and 200 (kappa_minus = 0.446); the count's moves biased toward the well in the same ratio: 51.2, 51.3 and 52.9 percent; the control 1 and 50 percent",
            "edge_quanta_per_node": 2706,
            "horizon_quanta_per_node": 6000,
            "tail_kappa_per_link_away": KAPPA_AWAY,
            "tail_ratio_well_over_away": ratio if tent else 1.0,
            "moves_toward_well_share": bias if tent else 0.5,
        },
        "GAMEBOARD": [
            {
                "reversible": TICKS,
                "row": "the whole run forward and back on a fresh copy, every row bit for bit, the clicks keep the clicks; a diagnostic, MATCH or MISS with the first interval and Node that deviate",
            }
        ],
        "fall": {
            "body": [BODY_X, *AXIS],
            "well_side": [TENT_X, *AXIS],
            "far_side": [BODY_X - 1, *AXIS],
            "axis": 0,
            "tail_ratio": ratio if tent else 1.0,
            "bias": bias if tent else 0.5,
            "band": None,
            "row": "fall_bias.py reads the tail's ratio from the matter levels at the two neighbours (the largest level on the well's side over the largest on the far side, GAMEBOARD) and the moves' bias from the body's centre along the axis (the moves toward the well over all moves, the count's line's clicks as the centre shows them); MATCH within `band` once Cheshbon writes it, else the reading alone",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE, help="the folder the files are written into")
    parser.add_argument("--no-tail", action="store_true", help="the mode files without the tail")
    args = parser.parse_args()
    folder = args.out.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    universe = (folder / UNIVERSE_NAME).relative_to(ROOT).as_posix()
    for tent in TENTS:
        name = f"fall_tent_{tent}"
        document = world(universe, tent)
        (folder / f"{name}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        (folder / f"{name}.mode.json").write_text(
            json.dumps(pixel_mode(document, not args.no_tail)) + "\n", encoding="utf-8"
        )
        (folder / f"{name}.expectation.json").write_text(
            json.dumps(expectation(tent), indent=1) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()
