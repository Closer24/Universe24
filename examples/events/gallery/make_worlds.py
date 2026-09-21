"""The demonstration worlds of the visual gallery (`docs/pages/gallery/`).

Three small worlds of the one engine, written for the pages of the gallery
where no registered world shows the story (the model owner's request of
2026-09-21 for the visualisation pages). They are demonstrations: nothing
here is a registered experiment and no number read off them enters the
register; a page made from one says so.

- `beam_fan.json` (the page "The beam"): an open plane of 41 x 41 (z
  periodic with an extent of 1), a lamp of the paid family `light` at the
  centre releasing one unit per self-creation on every primitive in-plane
  direction with |a| + |b| <= 6 (the fan), content 2^25 at K = 2^22 (the
  turn 8 steps of 64 per self-creation, every unit costing 8 content:
  E = h f), 60 intervals: the rows spread on the digital lines of the fan,
  the phase as the lamp's clock at the release.
- `clicks_plate.json` (the page "The clicks"): an open plane of 31 x 11, a
  lamp of `light` at (1, 5) releasing one unit per self-creation on five
  directions within 5 degrees of +x (the heading and (24, +-1, 0),
  (12, +-1, 0): a narrow beam, series K's), content 2^25 at K = 2^22, and
  a plate at x = 29 of eleven measured events of the paid family
  `apparatus` declared as the one-Node `wave` detectors `plate_<y>` (the
  pixels), 110 intervals: every record's rows end on the plate and its one
  click lands on one pixel by the ladder's rungs and its wheel value u.
- `collision.json` (the page "The collision"): an open cube of 9 x 9 x 9
  with no measured event, six declared rows of `light` of one number and
  content: a head-on pair on the x axis meeting at (4, 4, 4), and a triple
  (+x, -x, +y) meeting at (4, 4, 1); 30 intervals: the collision table's
  permutation at a Node of free space (the head-on pair parks on the rest
  slots, turns to another axis and leaves; the triple's odd unit goes on).

Run `python examples/events/gallery/make_worlds.py` to write them again.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = "../entities/families.json"


def in_plane_fan(bound: int) -> list[list[int]]:
    """Every primitive vector (a, b, 0) with 0 < |a| + |b| <= bound, in a
    fixed order (by angle)."""
    vectors = [
        (a, b)
        for a in range(-bound, bound + 1)
        for b in range(-bound, bound + 1)
        if 0 < abs(a) + abs(b) <= bound and math.gcd(abs(a), abs(b)) == 1
    ]
    vectors.sort(key=lambda v: math.atan2(v[1], v[0]))
    return [[a, b, 0] for a, b in vectors]


def beam_fan() -> dict[str, object]:
    bound = 6
    fan = in_plane_fan(bound)
    return {
        "law": "beam",
        "model_id": "gallery-beam-fan-demonstration-v1",
        "shape": [41, 41, 1],
        "boundary": {"z": "periodic"},
        "ticks": 60,
        "K": 1 << 22,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "directions": [v for v in fan if abs(v[0]) + abs(v[1]) > 1],
        "entity_definitions": FAMILIES,
        "entities": [{"name": "photon", "definition": "photon", "position": [0, 0, 0]}],
        "measured": [
            {
                "position": [20, 20, 0],
                "family": "light",
                "amount": 1 << 25,
                "phase": 0,
                "fixed": True,
                "lamp": {"rate": [1, 1], "directions": fan},
            }
        ],
    }


def clicks_plate() -> dict[str, object]:
    beam = [[1, 0, 0], [24, 1, 0], [24, -1, 0], [12, 1, 0], [12, -1, 0]]
    plate_x = 29
    return {
        "law": "beam",
        "model_id": "gallery-clicks-plate-demonstration-v1",
        "shape": [31, 11, 1],
        "boundary": {"z": "periodic"},
        "ticks": 110,
        "K": 1 << 22,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "directions": beam[1:],
        "entity_definitions": FAMILIES,
        "entities": [
            {"name": "photon", "definition": "photon", "position": [0, 0, 0]},
            {"name": "apparatus_material", "definition": "apparatus_material", "position": [0, 0, 0]},
        ],
        "measured": [
            {
                "position": [1, 5, 0],
                "family": "light",
                "amount": 1 << 25,
                "phase": 0,
                "fixed": True,
                "lamp": {"rate": [1, 1], "directions": beam},
            }
        ]
        + [
            {"position": [plate_x, y, 0], "family": "apparatus", "amount": 1, "fixed": True}
            for y in range(11)
        ],
        "detectors": [
            {"name": f"plate_{y}", "positions": [[plate_x, y, 0]], "threshold": 1, "reading": "wave"}
            for y in range(11)
        ],
    }


def collision() -> dict[str, object]:
    def row(position: list[int], direction: list[int]) -> dict[str, object]:
        return {
            "position": position,
            "family": "light",
            "number": 1,
            "direction": direction,
            "amount": 1,
            "phase": 0,
            "age": 0,
        }

    return {
        "law": "beam",
        "model_id": "gallery-collision-demonstration-v1",
        "shape": [9, 9, 9],
        "boundary": "open",
        "ticks": 30,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "directions": [[1, 1, 0]],
        "entity_definitions": FAMILIES,
        "entities": [{"name": "photon", "definition": "photon", "position": [0, 0, 0]}],
        "measured": [],
        "in_transit": [
            # The head-on pair on x, meeting at (4, 4, 4) at the fifth interval.
            row([1, 4, 4], [1, 0, 0]),
            row([7, 4, 4], [-1, 0, 0]),
            # The triple +x, -x, +y meeting at (4, 4, 1): the pair parks and
            # the odd unit goes on (the table's class "+x -x +y").
            row([1, 4, 1], [1, 0, 0]),
            row([7, 4, 1], [-1, 0, 0]),
            row([4, 1, 1], [0, 1, 0]),
            # A lone unit on a diagonal of the plane: a spectator of the
            # table, straight and unchanged.
            row([0, 0, 7], [1, 1, 0]),
        ],
    }


def main() -> None:
    for name, world in (
        ("beam_fan", beam_fan()),
        ("clicks_plate", clicks_plate()),
        ("collision", collision()),
    ):
        (HERE / f"{name}.json").write_text(json.dumps(world) + "\n", encoding="utf-8")
        print(name)


if __name__ == "__main__":
    main()
