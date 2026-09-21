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

- `proton_electron.json` (the page "The quarks"): series R's registered
  `q1_proton_line` (the quark bodies u d u at (9..11, 10, 10) holding one
  unit of `glue` each, the same families, fan and width) with one more
  free family `e` (one unit of content, the charge -7344 per unit: minus
  the register's proton, no strong column) and one body of it at
  (3, 10, 10) thrown at the line with the momentum 2 x 10^13 label units on
  +x (one Link per about 1.4 self-creations at the width 2^37), 600
  intervals: what a fast electron does to a proton of three quarks under
  the law as it is (the contact through the table hands its momentum to
  the quark it hits; nothing confines).
- `clock_6.json` (the page "The clock's word"): series U's (formerly P) registered
  `crowd_clock/still_3` (a lamp at rest at (10, 4, 4) inside a crowd of two
  `mass` sources three Links away on +y and +z, F = 4915 units per interval
  each on the fan of nine, the detector at x = 110) with the two sources
  moved to six Links, (10, 10, 4) and (10, 4, 10), on a bar of 121 x 15 x 15;
  30 intervals: the presence and the age moment of the crowd's rows at the
  lamp's Node read off the GameBoard at the two distances (the physicist's
  two-crowd pin, docs/designs/clock_age/NOTE.md section 6).

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
                "lamp": {"rate": [1, 1], "wheel": [1, 64], "directions": fan},
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
                "lamp": {"rate": [1, 1], "wheel": [1, 64], "directions": beam},
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


def proton_electron() -> dict[str, object]:
    """Series R's proton line as registered, plus the thrown electron."""
    base = json.loads((HERE.parent / "quarks" / "q1_proton_line.json").read_text(encoding="utf-8"))
    world = dict(base)
    world["model_id"] = "gallery-proton_electron-demonstration-v1"
    world["ticks"] = 600
    families = list(base["families"])
    families.append({"name": "e", "quantum": 0, "charge": -ELECTRON_CHARGE, "phase": False})
    world["families"] = families
    measured = [dict(m) for m in base["measured"]]
    measured.append(
        {
            "position": [3, 10, 10],
            "family": "e",
            "amount": 1,
            "fixed": False,
            "momentum": [ELECTRON_KICK, 0, 0],
            "directions": list(measured[0]["directions"]),
        }
    )
    world["measured"] = measured
    return world


# The register's proton charge (4 per unit on 1836 units of `p`; series R's
# u carries 2/3 of it, its d -1/3); the electron's whole charge is minus it.
ELECTRON_CHARGE = 7344
# The throw: one Link per (Q S M + p) / p self-creations with Q = 64,
# S = 2^37 (series R's width) and M = 1, so 1.44 self-creations per Link.
ELECTRON_KICK = 2 * 10**13


def clock_6() -> dict[str, object]:
    """Series U's (formerly P) still_3 with the crowd's two sources at six Links."""
    base = json.loads((HERE.parent / "crowd_clock" / "still_3.json").read_text(encoding="utf-8"))
    world = dict(base)
    world["model_id"] = "gallery-clock_6-demonstration-v1"
    world["shape"] = [base["shape"][0], 15, 15]
    world["ticks"] = 30
    measured = []
    for entry in base["measured"]:
        entry = dict(entry)
        if entry["family"] == "mass":
            x, y, z = entry["position"]
            entry["position"] = [x, 4 + (y - 4) * 2, 4 + (z - 4) * 2]
        measured.append(entry)
    world["measured"] = measured
    return world


def main() -> None:
    for name, world in (
        ("beam_fan", beam_fan()),
        ("clicks_plate", clicks_plate()),
        ("collision", collision()),
        ("proton_electron", proton_electron()),
        ("clock_6", clock_6()),
    ):
        (HERE / f"{name}.json").write_text(json.dumps(world) + "\n", encoding="utf-8")
        print(name)


if __name__ == "__main__":
    main()
