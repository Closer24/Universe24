"""THE TWO SLITS (g) with light, the first look of the de Broglie Experimenter (ALGEBRA.md #the-rows-against-nature (g); the row (j) follows with a matter record when Cheshbon gives the lighter family's row): the world laid out in the law's form (ALGEBRA.md #what-a-body-is) from the numbers Cheshbon writes on #1325 before any run, every physical value in the files and none in the engine. The apparatus, as the recipe rules of record say: a giving body of 3 x 3 Nodes in a tube of mirrors (one arm along +x), a wall body with two openings d Links apart at a count above the mirror's line of ALGEBRA.md #the-paces, and a screen body L Links beyond the wall's far face carrying the detector sets in strips on its own face, each strip one named detector (a set on its body's own Nodes, docs/ENGINE.md, the world file). The mode file beside the world is the generator's (tools/body_generator.py --out); nothing here is a mode number. Run from the repository root: python examples/events/experiments/de_broglie/lay_out_two_slits.py [--out <folder>]; it rewrites the world, its expectation and its universe file under this folder (or the folder named) and nothing else."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ENGINE = "examples/events/engine_start.json"
# the universe of record beside Bell's worlds (the held rows with `divisor`, the generator's amplitude
# bound), or the shipped generated universe until #1331 is on main; the two slits' universe file is
# written beside the world with the given family's clock key at the record's wavelength (rule 6)
UNIVERSE_OF_RECORD = (
    "examples/events/experiments/universe.json",
    "examples/events/generated/universe.json",
)
STEPS = 1024  # N, the phase's steps of every world of record
DENOMINATOR = 1024  # every body's phase denominator, the pair (m, j) the generator fills
NORM = {
    "norm": 180255439696889394,
    "norm_denominator": 3948169,
}  # the giver's norm, as Bell's files carry it
GIVING_FAMILY = "charge"  # the light; the matter record of (j) names the lighter family here
WORLD_NAME = "two_slits_light"

# THE NUMBERS TO SET FROM CHESHBON'S LINE ON #1325 (asked 05:08 Israel time, 2026-09-28); until his
# line these are the Experimenter's proposal, and a run on them is a first look and says so.
WAVELENGTH_CLOCK = [
    354,
    1,
]  # the given family's clock [p, q]: lambda_q = 2 N q / p = 5.785 Links, the giver's own wavelength on the light band (Cheshbon's line of 02:18Z, 2026-09-28), rule 6
GIVER_COUNT = 2001  # the giver's count per Node (`least_residues`: the shell wheel above 500 at 2001)
MIRROR = (
    9000  # the tube's and the wall's count per Node, above the mirror's line at the record's wavelength
)
WINDOW = 2000  # the screen's count per Node, a window
OPENING = 4  # the width of each opening in Nodes
SLIT_DISTANCE = 16  # d, the distance between the two openings' centres in Links
SCREEN_DISTANCE = 97  # L, from the wall's far face to the screen's face in Links
STRIP = 4  # the height of one strip of the screen in Nodes
STOCK = 400  # the giver's stock of quanta
TICKS = 4500  # the run's length in intervals: the last giving within ~4,000, the flight of 124 Links at the group velocity 0.518 (Cheshbon, 02:18Z)
FACE_DEPTH = 8

WALL_X = 40  # the wall's near face; the wall is 4 Nodes thick
WALL_THICKNESS = 4
SCREEN_THICKNESS = 4
HEIGHT = (
    256  # the GameBoard's y extent; the wall and the screen span the interior between the face slabs
)


def box(x0: int, x1: int, y0: int, y1: int) -> list[list[int]]:
    """Every Node of the box on the one layer, both ends included."""
    return [[x, y, 0] for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]


def body(nodes: list[list[int]], count: int, **keys: Any) -> dict[str, Any]:
    """A body of matter in the law's form at one count per Node, at rest."""
    return {
        "family": "matter",
        "nodes": [{"node": node, "count": count} for node in nodes],
        "momentum": [0, 0, 0],
        "momentum_before": [0, 0, 0],
        "phase_denominator": DENOMINATOR,
        **keys,
    }


def universe_beside(folder: Path) -> str:
    """The universe file of record copied beside the world with the given family's clock at the record's wavelength; the repository path the world names."""
    source = next((ROOT / path for path in UNIVERSE_OF_RECORD if (ROOT / path).exists()), None)
    if source is None:
        raise FileNotFoundError("no universe file of record in the tree")
    document = json.loads(source.read_text(encoding="utf-8"))
    for family in document["families"]:
        if family["name"] == GIVING_FAMILY:
            family["clock"] = list(WAVELENGTH_CLOCK)
    path = folder / "universe.json"
    path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    return path.resolve().relative_to(ROOT).as_posix()


def two_slits(folder: Path) -> dict[str, Any]:
    """The world: the giver in its tube, the wall with two openings, the screen with its strips, the readings of the GameBoard check plan."""
    interior = range(FACE_DEPTH, HEIGHT - FACE_DEPTH)
    middle = (HEIGHT - 1) / 2  # the axis of the apparatus, between two Nodes
    half = SLIT_DISTANCE / 2
    left_opening = {y for y in interior if abs(y + 0.5 - (middle + 0.5 - half)) < OPENING / 2}
    right_opening = {y for y in interior if abs(y + 0.5 - (middle + 0.5 + half)) < OPENING / 2}
    if len(left_opening) != OPENING or len(right_opening) != OPENING:
        raise ValueError("the openings do not fall on whole Nodes; choose d and the width together")
    giver_y0 = int(middle + 0.5) - 1
    giver_nodes = box(14, 16, giver_y0, giver_y0 + 2)
    tube = (
        box(10, 13, giver_y0, giver_y0 + 2)
        + box(10, 16, giver_y0 - 3, giver_y0 - 1)
        + box(10, 16, giver_y0 + 3, giver_y0 + 5)
    )
    wall_x1 = WALL_X + WALL_THICKNESS - 1
    wall_nodes = [
        [x, y, 0]
        for x in range(WALL_X, wall_x1 + 1)
        for y in interior
        if y not in left_opening and y not in right_opening
    ]
    screen_x = wall_x1 + SCREEN_DISTANCE
    screen_nodes = box(screen_x, screen_x + SCREEN_THICKNESS - 1, interior.start, interior.stop - 1)
    strips = [
        {
            "name": f"strip_{k:02d}",
            "positions": [[screen_x, y, 0] for y in range(y0, y0 + STRIP)],
        }
        for k, y0 in enumerate(range(interior.start, interior.stop, STRIP))
    ]
    emitter = {"family": GIVING_FAMILY, "weight": 1, **NORM}
    measured = [
        body(giver_nodes, GIVER_COUNT, moment=[0, 0, 1], emitter=emitter, stocks={GIVING_FAMILY: STOCK}),
        body(wall_nodes, MIRROR),
        body(screen_nodes, WINDOW),
        body(tube, MIRROR),
    ]
    centre_y = int(middle + 0.5)
    left_y = min(left_opening) + OPENING // 2
    right_y = min(right_opening) + OPENING // 2
    readings = [
        {"name": f"{s['name']}_clicks", "kind": "clicks", "detector": s["name"]} for s in strips
    ] + [
        {"name": "light_rows", "kind": "rows", "family": GIVING_FAMILY, "every": 100},
        {"name": "light_support", "kind": "support", "family": GIVING_FAMILY, "every": 50},
        {
            "name": "at_left_opening",
            "kind": "level",
            "family": GIVING_FAMILY,
            "node": [WALL_X + 1, left_y, 0],
            "every": 10,
        },
        {
            "name": "at_right_opening",
            "kind": "level",
            "family": GIVING_FAMILY,
            "node": [WALL_X + 1, right_y, 0],
            "every": 10,
        },
        {
            "name": "behind_the_wall",
            "kind": "level",
            "family": GIVING_FAMILY,
            "node": [WALL_X + 20, FACE_DEPTH + 40, 0],
            "every": 10,
        },
        {
            "name": "before_the_screen",
            "kind": "level",
            "family": GIVING_FAMILY,
            "node": [screen_x - 1, centre_y, 0],
            "every": 10,
        },
        {"name": "giver_centre", "kind": "centre", "body": 0, "every": 500},
        {"name": "wall_centre", "kind": "centre", "body": 1, "every": 500},
        {"name": "screen_centre", "kind": "centre", "body": 2, "every": 500},
        {"name": "giver_cycle", "kind": "cycle", "body": 0, "every": 100},
        {"name": "records_alive", "kind": "alive", "every": 100},
    ]
    shape = [screen_x + SCREEN_THICKNESS + FACE_DEPTH + 8, HEIGHT, 1]
    return {
        "shape": shape,
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "ticks": TICKS,
        "N": STEPS,
        "engine": ENGINE,
        "universe": universe_beside(folder),
        "measured": measured,
        "detectors": strips,
        "readings": readings,
        "face_depth": FACE_DEPTH,
    }


# CHESHBON'S BLIND EXPECTATION OF THE STRIPS (#1325, 02:18Z, 2026-09-28; lambda = 5.785, d = 16, L = 97, the
# stock 400; the exact two-arm phases k . r on the surface's wavevector with Huygens' sum over each opening's
# four Nodes): his strips are numbered 0..63 over y = 0..255 (the centre 31.5); the strips here start at the
# face slab's edge (y = FACE_DEPTH), so his strip j is the strip j - FACE_DEPTH // STRIP here. The share per strip
# and its binomial sd on the stock; the band read as two sd (the draw's, "The rows against nature").
CHESHBON_STRIPS = {
    31: (0.049, 4.3),
    32: (0.049, 4.3),
    21: (0.037, 3.8),
    42: (0.037, 3.8),
    6: (0.015, 2.4),
    56: (0.015, 2.4),
    14: (0.0005, 0.5),
    26: (0.0005, 0.5),
    37: (0.0005, 0.5),
    49: (0.0005, 0.5),
}


def strips_expected(document: dict[str, Any]) -> list[dict[str, Any]]:
    """The expectation's `strips`: Cheshbon's share per named strip, the count on the stock and the band of two sd."""
    offset = FACE_DEPTH // STRIP
    names = {k: strip["name"] for k, strip in enumerate(document["detectors"])}
    found = []
    for his, (share, sd) in sorted(CHESHBON_STRIPS.items()):
        mine = his - offset
        if mine in names:
            found.append(
                {
                    "detector": names[mine],
                    "cheshbon_strip": his,
                    "share": share,
                    "count": round(STOCK * share),
                    "sd": sd,
                    "band": round(2 * sd),
                    "row": "Cheshbon's blind share (02:18Z) of the clicks on the screen at the stock 400; the band two binomial sd",
                }
            )
    return found


def expectation(document: dict[str, Any]) -> dict[str, Any]:
    """The expectation file's frame: the row, the form of the world, the GAMEBOARD checks; the DETECTOR shares per strip enter from Cheshbon's line and no run."""
    wavelength = 2 * STEPS * WAVELENGTH_CLOCK[1] / WAVELENGTH_CLOCK[0]
    return {
        "format": "world-expectation-v1",
        "status": "FIRST LOOK: the strips' shares await Cheshbon's blind expectation on #1325 (asked 05:08 Israel time, 2026-09-28); no number here is compared before his line",
        "row": (
            f"ALGEBRA.md #the-rows-against-nature (g) THE TWO SLITS: the giver of 3 x 3 Nodes of {GIVER_COUNT} "
            f"in a tube of {MIRROR} (one arm along +x), the wall of {WALL_THICKNESS} x {HEIGHT - 2 * FACE_DEPTH} Nodes of {MIRROR} "
            f"with two openings of {OPENING} Nodes d = {SLIT_DISTANCE} Links apart, the screen of {WINDOW} L = {SCREEN_DISTANCE} Links "
            f"beyond the wall's far face carrying {len(document['detectors'])} strips of {STRIP} Nodes on its face, each strip one detector; "
            f"the given family's clock {WAVELENGTH_CLOCK} (lambda_q = {wavelength:g} Links for the recoil); the record's wavelength "
            "on the GameBoard is the giver's rotation on the light band (cos k = 3 cos omega_b - 2), the generator's number in the mode file; "
            "the strips' shares cos^2 (pi d y / (lambda L)) under one opening's envelope, the exact term the two arms' phases k . r (Cheshbon's line); "
            f"the stock {STOCK}; written before any run"
        ),
        "DETECTOR": [],
        "strips": strips_expected(document),
        "GAMEBOARD": [],
        "GAMEBOARD_checks": [
            "(i) `behind_the_wall` (away from the openings) stays 0 behind the opaque wall; `at_left_opening` and `at_right_opening` carry the record's level in the openings",
            "(ii) `light_rows` every 100 intervals: one record leaves the tube along +x, two parts pass the openings, spread and meet on the screen",
            "(iii) `giver_centre`, `wall_centre`, `screen_centre`: within a Link over the run; `giver_cycle`: the giver's own period, the generator's",
            "then the DETECTOR reading in kind: bright and dark strips alternate about the axis, the spacing lambda L / d (Young's fringes), one record at a time",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=HERE,
        help="the folder the files are written into (this folder by default)",
    )
    args = parser.parse_args()
    folder = args.out.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    document = two_slits(folder)
    expected = expectation(document)
    expected["GAMEBOARD"] = [
        {"body": number, "interval": TICKS // 2, "centre": centre, "band": 1, "row": row}
        for number, centre, row in (
            (1, [WALL_X + WALL_THICKNESS // 2, HEIGHT // 2, 0], "the wall at rest within a Link"),
            (
                2,
                [document["detectors"][0]["positions"][0][0] + SCREEN_THICKNESS // 2, HEIGHT // 2, 0],
                "the screen at rest within a Link",
            ),
        )
    ]
    (folder / f"{WORLD_NAME}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    (folder / f"{WORLD_NAME}.expectation.json").write_text(
        json.dumps(expected, indent=1) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "world": str(folder / f"{WORLD_NAME}.json"),
                "shape": document["shape"],
                "strips": len(document["detectors"]),
                "bodies": [len(b["nodes"]) for b in document["measured"]],
            }
        )
    )


if __name__ == "__main__":
    main()
