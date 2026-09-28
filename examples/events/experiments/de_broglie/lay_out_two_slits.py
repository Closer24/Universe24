"""THE TWO SLITS (g) with light, the first look of the de Broglie Experimenter (ALGEBRA.md #the-rows-against-nature (g); the row (j) follows with a matter record when Cheshbon gives the lighter family's row): the world laid out in the law's form (ALGEBRA.md #what-a-body-is) from the numbers Cheshbon writes on #1325 before any run, every physical value in the files and none in the engine. The apparatus, as the recipe rules of record say: a giving body of 3 x 3 Nodes in a tube of mirrors (one arm along +x), a wall body with two openings d Links apart at a count above the mirror's line of ALGEBRA.md #the-paces, and a screen body L Links beyond the wall's far face carrying the detector sets in strips on its own face, each strip one named detector (a set on its body's own Nodes, docs/ENGINE.md, the world file). The mode file beside the world is the generator's (tools/body_generator.py --out); nothing here is a mode number. Run from the repository root: python examples/events/experiments/de_broglie/lay_out_two_slits.py [--out <folder>]; it rewrites the world and its expectation under this folder (or the folder named) and nothing else; the world names the universe of record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ENGINE = "examples/events/engine_start.json"
# the universe of record, the one file of the universe (the Closer's word of 08:04 Israel: one universe, no copy);
# the given record's wavelength is the generator's reading `wavelength` of the mode file (#1353), no key
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
E_S_CHARGE = 300_000  # E_s of the charge, the free number alpha of the universe (Cheshbon 06:43Z; the Closer 11:43 Israel: in the world's universe until PR-1b)
WORLD_NAME = "two_slits_light"

# THE NUMBERS TO SET FROM CHESHBON'S LINE ON #1325 (asked 05:08 Israel time, 2026-09-28); until his
# line these are the Experimenter's proposal, and a run on them is a first look and says so.
GIVER_COUNT = 2001  # the giver's count per Node (`least_residues`: the shell wheel above 500 at 2001)
MIRROR = 9000  # the tube's and the wall's count per Node, four Nodes thick: the form of record (Cheshbon's line of 04:07Z), above the mirror's line Gamma (1 - sin(pi / lambda)) = 2,929 at the record's wavelength 4 (Bell's walls, #1371); the thinning to 4,000 under the conformal term of #1375 (the level entered the Link twice at 9,000) left with its revert (#1399)
SCREEN = 9000  # the screen's count per Node: the mirror's, the strips booking the one-way inward flux at their Ports (the owner's word through the Closer; Cheshbon's yes, 02:27Z)
OPENING = 4  # the width of each opening in Nodes
SLIT_DISTANCE = 16  # d, the distance between the two openings' centres in Links
SCREEN_DISTANCE = 97  # L, from the wall's far face to the screen's face in Links
STRIP = 4  # the height of one strip of the screen in Nodes
STOCK = 400  # the giver's stock of quanta
TICKS = 6000  # the run's length in intervals: the last giving within ~4,000, the flight of 124 Links at the group velocity 0.518 and the returns from the mirror screen (Cheshbon's yes, 02:27Z)
FACE_DEPTH = 8
GAP = 5  # empty Nodes between a giver or a window and a wall (the owner's word: five, the bound charge's tail below two levels at four)

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


def universe_of_record() -> str:
    """The repository path of the universe file of record; no key of the wavelength (the generator's reading)."""
    source = next((path for path in UNIVERSE_OF_RECORD if (ROOT / path).exists()), None)
    if source is None:
        raise FileNotFoundError("no universe file of record in the tree")
    return source


def universe_of_the_first_look(folder: Path) -> str:
    """The universe of the first look, written beside the world: the universe of record with the number the record does not carry yet (the Closer's word of 11:43 Israel, until PR-1b writes it in the record): the charge row's divisor E_s(charge) = 300,000 (the coupling alpha, agreed with Cheshbon 06:43Z: the train tens of periods). The quantum action T is not written: the loop of main reads the giving's coupling as the emitter's weight over 1 and the close at the emitter's norm until (M_pol, E_s) and T enter the loop (PR-1b and the giving's line), so a record at the generator's scale c T drives the given light above the amplitude bound within ten intervals (the refusal of 11:53 Israel); the first look runs at the file's norm, the train's length read after those lines. The repository path the world names."""
    document = json.loads((ROOT / universe_of_record()).read_text(encoding="utf-8"))
    for family in document["families"]:
        if family["name"] == GIVING_FAMILY:
            family["held"] = {**family["held"], "divisor": E_S_CHARGE}
    path = folder / "universe_first_look.json"
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
    # the tube's mirrors GAP Nodes away from the giver on its three closed sides (Cheshbon's geometric line
    # of 04:07Z: the bound charge's tail at a wall of 9000 falls to under two levels four Links out, so a
    # window body stands three empty Nodes from every wall); the mouth open toward +x
    tube = (
        box(14 - GAP - 4, 14 - GAP - 1, giver_y0 - GAP - 3, giver_y0 + GAP + 5)
        + box(14 - GAP, 16, giver_y0 - GAP - 3, giver_y0 - GAP - 1)
        + box(14 - GAP, 16, giver_y0 + GAP + 3, giver_y0 + GAP + 5)
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
        body(screen_nodes, SCREEN),
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
        "universe": universe_of_the_first_look(folder),
        "measured": measured,
        "detectors": strips,
        "readings": readings,
        "face_depth": FACE_DEPTH,
    }


# CHESHBON'S BLIND EXPECTATION OF THE STRIPS (#1325, 02:18Z and 02:30Z, 2026-09-28; lambda = 5.785, d = 16,
# L = 97; the exact shares of (g): the two arms' phases k . r on the band's surface with Huygens' sum over each
# opening's four Nodes; the paraxial cos^2 (pi d y / (lambda L)) under the envelope beside them for the
# comparison): his strips are numbered 0..63 over y = 0..255 (the centre 31.5); the strips here start at the
# face slab's edge (y = FACE_DEPTH), so his strip j is the strip j - FACE_DEPTH // STRIP here. The count per
# strip is the share of the stock and its band two binomial sd (the draw's, "The rows against nature").
CHESHBON_EXACT = [
    0.0078,
    0.0092,
    0.0107,
    0.0121,
    0.0135,
    0.0145,
    0.0152,
    0.0151,
    0.0143,
    0.0126,
    0.0100,
    0.0068,
    0.0036,
    0.0011,
    0.0002,
    0.0018,
    0.0064,
    0.0136,
    0.0224,
    0.0307,
    0.0363,
    0.0370,
    0.0323,
    0.0231,
    0.0123,
    0.0036,
    0.0003,
    0.0044,
    0.0150,
    0.0290,
    0.0417,
    0.0487,
    0.0477,
    0.0389,
    0.0254,
    0.0119,
    0.0027,
    0.0005,
    0.0053,
    0.0150,
    0.0257,
    0.0340,
    0.0373,
    0.0353,
    0.0288,
    0.0202,
    0.0116,
    0.0050,
    0.0012,
    0.0002,
    0.0016,
    0.0044,
    0.0077,
    0.0107,
    0.0131,
    0.0146,
    0.0152,
    0.0151,
    0.0143,
    0.0131,
    0.0118,
    0.0103,
    0.0088,
    0.0074,
]
CHESHBON_PARAXIAL = [
    0.0001,
    0.0000,
    0.0005,
    0.0017,
    0.0037,
    0.0055,
    0.0063,
    0.0052,
    0.0027,
    0.0004,
    0.0007,
    0.0051,
    0.0128,
    0.0210,
    0.0257,
    0.0241,
    0.0163,
    0.0065,
    0.0006,
    0.0035,
    0.0158,
    0.0329,
    0.0469,
    0.0506,
    0.0417,
    0.0243,
    0.0075,
    0.0006,
    0.0081,
    0.0271,
    0.0485,
    0.0614,
    0.0594,
    0.0435,
    0.0218,
    0.0049,
    0.0010,
    0.0111,
    0.0290,
    0.0450,
    0.0509,
    0.0442,
    0.0286,
    0.0120,
    0.0018,
    0.0014,
    0.0088,
    0.0187,
    0.0251,
    0.0251,
    0.0191,
    0.0107,
    0.0036,
    0.0003,
    0.0009,
    0.0034,
    0.0057,
    0.0063,
    0.0051,
    0.0031,
    0.0013,
    0.0003,
    0.0000,
    0.0001,
]


def strips_expected(document: dict[str, Any]) -> list[dict[str, Any]]:
    """The expectation's `strips`: per named strip Cheshbon's exact share and the paraxial one, the count on the stock and the band of two binomial sd."""
    offset = FACE_DEPTH // STRIP
    found = []
    for mine, strip in enumerate(document["detectors"]):
        his = mine + offset
        exact = CHESHBON_EXACT[his]
        sd = (STOCK * exact * (1 - exact)) ** 0.5
        found.append(
            {
                "detector": strip["name"],
                "cheshbon_strip": his,
                "share": exact,
                "paraxial_share": CHESHBON_PARAXIAL[his],
                "count": round(STOCK * exact),
                "sd": round(sd, 2),
                "band": max(1, round(2 * sd)),
                "row": "Cheshbon's blind exact share of the clicks on the screen (02:30Z), the paraxial cos^2 beside it; the count on the stock 400, the band two binomial sd",
            }
        )
    return found


def expectation(document: dict[str, Any]) -> dict[str, Any]:
    """The expectation file's frame: the row, the form of the world, the GAMEBOARD checks; the DETECTOR shares per strip enter from Cheshbon's line and no run."""
    return {
        "format": "world-expectation-v1",
        "status": "FIRST LOOK: the strips' shares await Cheshbon's blind expectation on #1325 (asked 05:08 Israel time, 2026-09-28); no number here is compared before his line",
        "row": (
            f"ALGEBRA.md #the-rows-against-nature (g) THE TWO SLITS: the giver of 3 x 3 Nodes of {GIVER_COUNT} "
            f"in a tube of {MIRROR} (one arm along +x), the wall of {WALL_THICKNESS} x {HEIGHT - 2 * FACE_DEPTH} Nodes of {MIRROR} "
            f"with two openings of {OPENING} Nodes d = {SLIT_DISTANCE} Links apart, the screen of {SCREEN} L = {SCREEN_DISTANCE} Links "
            f"beyond the wall's far face carrying {len(document['detectors'])} strips of {STRIP} Nodes on its face, each strip one detector; "
            "the record's wavelength lambda_q is the giver's rotation on the light band (cos k = 3 cos omega_b den / num - 2), "
            "the generator's reading `wavelength` in the mode file, the recoil's and the wall L's (#1353), no key of the files; "
            "the strips' shares cos^2 (pi d y / (lambda L)) under one opening's envelope, the exact term the two arms' phases k . r (Cheshbon's line); "
            f"the stock {STOCK}; written before any run"
        ),
        "DETECTOR": [],
        "strips": strips_expected(document),
        "blind": {
            "row": "Cheshbon's table of the blind numbers (08:21Z and 08:24Z) on the universe of record as it stands, written before the run: the algebra's column; the engine's column and the difference are the report's",
            "wavelength_links": 4,
            "fringe_spacing_links": {
                "value": 24.25,
                "band": "half a strip on every maximum",
                "formula": "lambda L / d with lambda 4, d 16, L 97; about six strips of four",
            },
            "envelope_links": {
                "value": 97,
                "formula": "lambda L / a, about four fringes in half the envelope",
            },
            "group_velocity_links_per_interval": 0.518,
            "train_periods": {
                "value": 29.5,
                "band": 0.5,
                "intervals": 236,
                "row": "the train at E_s(charge) 300,000 on the core before the conformal term; the generator's `train` on the core of main is the algebra on the form (Cheshbon 07:12Z section 6); read in the loop after PR-1b and the giving's line",
            },
        },
        "GAMEBOARD": [
            {
                "reversible": TICKS,
                "row": "HIGHLIGHTS line 33 (the owner, 09:31 Israel): the whole run forward and back on a fresh copy of the world, every row of the GameBoard bit for bit, the click keeps the click (the runner's row, #1377); a diagnostic, MATCH or MISS with the first interval and Node that deviate",
            }
        ],
        "GAMEBOARD_checks": [
            "(0) `reversible`: the run returns to its start bit for bit; a MISS names the engine's defect before any reading of the strips is believed",
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
    expected["GAMEBOARD"] += [
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
