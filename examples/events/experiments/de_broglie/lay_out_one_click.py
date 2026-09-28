"""THE ONE-CLICK HEALTH LOOK (the owner's word of 2026-09-28, 07:06 Israel time, through the Closer): before an experiment's first look, one click on a small GameBoard, read at the Nodes themselves (GAMEBOARD, labelled so) and at one detector: a giving body of 3 x 3 Nodes with one quantum in stock, in a tube of mirrors three empty Nodes from it (its mouth open toward +x), a window body across the beam carrying one detector strip on its face, a mirror body beyond it, and the faces open; the readings: the light's level at Nodes along the beam every interval, its rows every few intervals (the record's centroid, its wavelength by the sign changes along the beam, its largest level against the amplitude bound, the levels on both sides of the window and of the mirror), the giver's centre and the records alive; the strip's click is the one measurement (DETECTOR). Every count is the two slits' (the wall's and the tube's 9000, the window's 2000, the giver's 2001), the universe the one of record. Run from the repository root: python examples/events/experiments/de_broglie/lay_out_one_click.py [--out <folder>]; the world is written under this folder and nothing else; it names the universe of record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from lay_out_two_slits import (
    DENOMINATOR,
    ENGINE,
    GAP,
    GIVER_COUNT,
    GIVING_FAMILY,
    MIRROR,
    NORM,
    STEPS,
    body,
    box,
    universe_of_record,
)

HERE = Path(__file__).resolve().parent
WORLD_NAME = "one_click"
WINDOW = (
    2000  # the window's count per Node, below the mirror's line of "The paces" at the giver's wavelength
)
STOCK = 1  # one quantum
TICKS = 400  # the flight to the mirror and back
FACE_DEPTH = 8
SHAPE = [96, 40, 1]
BEAM_Y = 19  # the beam's axis, the giver's middle row
GIVER_X = 14  # the giver's near face; its far face at GIVER_X + 2 gives toward +x
WINDOW_X = 40  # the window's near face, 4 Nodes thick
MIRROR_X = 70  # the mirror's near face, 4 Nodes thick
STRIP = range(
    BEAM_Y - 4, BEAM_Y + 4
)  # the detector strip on the window's face, eight Nodes about the beam


def one_click() -> dict[str, Any]:
    """The world: the giver in its tube, the window with its strip, the mirror, the readings along the beam."""
    interior = range(FACE_DEPTH, SHAPE[1] - FACE_DEPTH)
    y0 = BEAM_Y - 1
    giver_nodes = box(GIVER_X, GIVER_X + 2, y0, y0 + 2)
    tube = (
        box(GIVER_X - GAP - 4, GIVER_X - GAP - 1, y0 - GAP - 3, y0 + GAP + 5)
        + box(GIVER_X - GAP, GIVER_X + 2, y0 - GAP - 3, y0 - GAP - 1)
        + box(GIVER_X - GAP, GIVER_X + 2, y0 + GAP + 3, y0 + GAP + 5)
    )
    window = box(WINDOW_X, WINDOW_X + 3, interior.start, interior.stop - 1)
    mirror = box(MIRROR_X, MIRROR_X + 3, interior.start, interior.stop - 1)
    emitter = {"family": GIVING_FAMILY, "weight": 1, **NORM}
    measured = [
        body(giver_nodes, GIVER_COUNT, moment=[0, 0, 1], emitter=emitter, stocks={GIVING_FAMILY: STOCK}),
        body(tube, MIRROR),
        body(window, WINDOW),
        body(mirror, MIRROR),
    ]
    detectors = [{"name": "window_strip", "positions": [[WINDOW_X, y, 0] for y in STRIP]}]
    along = [
        GIVER_X + 5,
        30,
        WINDOW_X - 1,
        WINDOW_X + 1,
        WINDOW_X + 5,
        55,
        MIRROR_X - 1,
        MIRROR_X + 1,
        MIRROR_X + 6,
        85,
    ]
    readings = (
        [{"name": "strip_clicks", "kind": "clicks", "detector": "window_strip"}]
        + [
            {
                "name": f"beam_x{x}",
                "kind": "level",
                "family": GIVING_FAMILY,
                "node": [x, BEAM_Y, 0],
                "every": 1,
            }
            for x in along
        ]
        + [
            {"name": "light_rows", "kind": "rows", "family": GIVING_FAMILY, "every": 5},
            {"name": "light_support", "kind": "support", "family": GIVING_FAMILY, "every": 5},
            {"name": "giver_centre", "kind": "centre", "body": 0, "every": 50},
            {"name": "giver_momentum", "kind": "momentum", "body": 0, "every": 10},
            {"name": "window_momentum", "kind": "momentum", "body": 2, "every": 10},
            {"name": "mirror_momentum", "kind": "momentum", "body": 3, "every": 10},
            {"name": "records_alive", "kind": "alive", "every": 10},
        ]
    )
    return {
        "shape": SHAPE,
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "ticks": TICKS,
        "N": STEPS,
        "engine": ENGINE,
        "universe": universe_of_record(),
        "measured": measured,
        "detectors": detectors,
        "readings": readings,
        "face_depth": FACE_DEPTH,
    }


def expectation() -> dict[str, Any]:
    """The expectation file of the health look: no DETECTOR share (one click, in kind), the GAMEBOARD row `reversible` over the whole run (HIGHLIGHTS line 33, the runner's row of #1377); the five lines are read from the output by one_click.py."""
    return {
        "format": "world-expectation-v1",
        "status": "HEALTH LOOK: one click in kind at the strip; no number of a run here",
        "row": "the one-click health look before the two slits' first look (the owner's word of 07:06 Israel through the Closer): the strip's click is the one measurement, every other reading is GAMEBOARD",
        "DETECTOR": [],
        "GAMEBOARD": [
            {
                "reversible": TICKS,
                "row": "the whole run forward and back on a fresh copy, every row bit for bit, the click keeps the click; a diagnostic, MATCH or MISS with the first interval and Node that deviate",
            }
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE, help="the folder the files are written into")
    args = parser.parse_args()
    folder = args.out.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    document = one_click()
    (folder / f"{WORLD_NAME}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    (folder / f"{WORLD_NAME}.expectation.json").write_text(
        json.dumps(expectation(), indent=1) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "world": str(folder / f"{WORLD_NAME}.json"),
                "bodies": [len(b["nodes"]) for b in document["measured"]],
                "denominator": DENOMINATOR,
            }
        )
    )


if __name__ == "__main__":
    main()
