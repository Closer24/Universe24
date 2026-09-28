"""THE ONE-QUBIT WORLDS OF (k) THE TWO-QUBIT COMPUTER on the rule's own universe (ALGEBRA.md #the-rows-against-nature (k) and (l) MACH-ZEHNDER; #the-paces, THE BAND AT A PACE; the owner's word of 2026-09-28, 16:57 Israel): one qubit is a record's two arms after the splitter of (l), its gates the splitter, a window body as a phase gate and the polariser. The board is a plane open on x and y (periodic z of extent one, as Bell's): a giving pixel of the matter pair fires light along a tube of walls at the first splitter, a diagonal of Nodes one Node deep along the beam at a count inside the record's band; the reflected share turns along +y and the transmitted share goes on along +x; a mirror on each arm (a diagonal band three Nodes thick at a count above the mirror's line) turns the arms toward the second splitter, whose two exits carry the two sets: the cross exit along +x (each arm reflected once and transmitted once at the splitters) and the straight exit along +y. The phase gate is a window body across one arm, `depth` Nodes deep along the beam at a count below the mirror's line: the phase (k_in - k) l of (k) with 1 - cos k_in = (Gamma / p)^2 (1 - cos k) at the window's pace p. THE BLIND EXPECTATION (the run says, no pin): the shares of the clicks 4 s (1 - s) cos^2 (Delta / 2) at the cross exit and one minus that at the straight exit, Delta the arms' phase difference, s the splitter's reflected share (one half at Cheshbon's count by bisection; the file's count stands until his line); at equal arms every click at the cross exit; with the gate the phase is written twice, at the level once in the Link and at the level twice (THE LEVEL ENTERS THE LINK TWICE AND THE CLOCK ONCE), and the run separates the two readings. Every count follows the rule's universe at Gamma 24 (Cheshbon's table of 15:22 and 15:43 Israel: the giving pixel 8 with his clock pair; the light's wavelength 5 to the Link); the two-qubit world (the crystal's pair record, (h)'s E with the controlled phase) waits for Bell's world at 24 and Cheshbon's numbers. Run from the repository root: python examples/events/experiments/quantum_computer/lay_out_qubits.py; it rewrites the worlds, their expectations and their mode files under this folder and nothing else."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "src"), str(HERE.parent)]

import pixel_mode  # noqa: E402
from lay_out_worlds import (  # noqa: E402
    PAIRS_AT_24,
    PLANCK,
    RULE_GAMMA,
    body,
    given_wavelength,
    pixel,
    reading,
    world,
)

GAMMA = RULE_GAMMA  # the rule's universe's node clock, cited for the expectation's formulas only
WAVELENGTH = given_wavelength(
    PAIRS_AT_24[8][:2]
)  # the given light's wavelength to the Link from the giver's clock pair (5 at the count 8)
GIVER_COUNT = (
    8  # the giving pixel (Cheshbon's table of 15:22: the pixels 8 to 11 realisable, the giver 8)
)
STOCK = 12  # the giver's stock, the horizon at 24 (lay_out_worlds: a stock of 200 is refused as a pace that could reach 0)
MIRROR = 7  # a wall and a mirror: the highest count the pace guard of today admits (the content 3 c below Gamma, the light's finding of 16:58 Israel); a mirror for lambda 5 with the level twice in the Link (the line Gamma (1 - sin(pi / lambda)) / 2 = 5.4) and a window with the level once (10.8): the run says which
SPLITTER = 3  # the splitter's count, inside the record's band under both readings of the level; its reflected share s is Cheshbon's by bisection (the row (l)) and his count replaces this one before any registered run
GATES = {
    "quarter": (2, 5),
    "half": (3, 6),
}  # the phase gates: (count, depth) of the window body across the transmitted arm, laid near a quarter turn (1.55 radians) and a half turn (3.27) with the level twice in the Link; 0.68 and 1.30 with the level once (gate_phase below)
WALL = 2  # the walls' thickness in Nodes: through one Node of a wall of 7 at the level twice the light's evanescent factor is e^(-1.55) per Node
CHANNEL = 3  # the channel's width in Nodes between the walls
HALF = 2  # the diagonals' half-length: a diagonal of 2 HALF + 1 Nodes across the channel and the walls' corner
CORNER = {
    "x0": 12,
    "y0": 12,
    "x1": 32,
    "y1": 32,
}  # the four corners of the square: the first splitter at (x0, y0), the mirrors at (x0, y1) and (x1, y0), the second splitter at (x1, y1)
GIVER_X = 7  # the giving pixel's Node on the beam's row, in the tube behind the first splitter
FACE_DEPTH = 4
SHAPE = [44, 44, 1]
TAKER = 3  # the two sets' bodies at the exits, windows across the channel one Node deep (a set is a body's Nodes: the detector names its block), at the splitter's count
EXIT = 5  # the sets stand this many Links beyond the second splitter's corner, inside the face slab's margin
TICKS = 600  # the run's length: the flight round the square (about 40 Links at the light's group velocity 0.45, about 90 intervals) many times over the giver's stock


def diagonal(cx: int, cy: int, thickness: int) -> list[list[int]]:
    """The Nodes of a diagonal band along the direction (1, 1) centred on (cx, cy): every Node of the square of half-side HALF whose offset from the diagonal, |(x - cx) - (y - cy)|, is within (thickness - 1) div 2, a solid band; a mirror along (1, 1) turns +x into +y and +y into +x."""
    reach = (thickness - 1) // 2
    return [
        [x, y, 0]
        for x in range(cx - HALF, cx + HALF + 1)
        for y in range(cy - HALF, cy + HALF + 1)
        if abs((x - cx) - (y - cy)) <= reach
    ]


def box(x0: int, x1: int, y0: int, y1: int) -> list[list[int]]:
    """Every Node of the box on the plane with both ends included."""
    return [[x, y, 0] for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]


def channel() -> set[tuple[int, int]]:
    """The channel's Nodes on the plane: the tube from behind the giver to the first splitter and on along the transmitted arm, the reflected arm, the two arms toward the second splitter, and the two exits' tubes beyond it, each CHANNEL Nodes wide."""
    x0, y0, x1, y1 = CORNER["x0"], CORNER["y0"], CORNER["x1"], CORNER["y1"]
    half = CHANNEL // 2
    nodes: set[tuple[int, int]] = set()
    for x in range(GIVER_X - 1, x1 + half + 1):  # the tube and the transmitted arm along +x
        nodes.update((x, y) for y in range(y0 - half, y0 + half + 1))
    for y in range(y0 - half, y1 + half + 1):  # the reflected arm along +y
        nodes.update((x, y) for x in range(x0 - half, x0 + half + 1))
    for x in range(x0 - half, x1 + EXIT + 2):  # the upper arm and the cross exit's tube along +x
        nodes.update((x, y) for y in range(y1 - half, y1 + half + 1))
    for y in range(y0 - half, y1 + EXIT + 2):  # the right arm and the straight exit's tube along +y
        nodes.update((x, y) for x in range(x1 - half, x1 + half + 1))
    return nodes


def walls(occupied: set[tuple[int, int, int]]) -> list[list[int]]:
    """The walls: every Node within WALL Nodes of the channel (the Chebyshev distance) that is not the channel's and not an earlier body's (the diagonals and the gate), one body; the tubes close behind the giver and beyond each exit's set."""
    inside = channel()
    nodes: set[tuple[int, int]] = set()
    for x, y in inside:
        for dx in range(-WALL, WALL + 1):
            for dy in range(-WALL, WALL + 1):
                node = (x + dx, y + dy)
                if node not in inside and (node[0], node[1], 0) not in occupied:
                    nodes.add(node)
    return [[x, y, 0] for x, y in sorted(nodes)]


def exit_nodes(which: str) -> list[list[int]]:
    """The set's body at an exit: the channel's width, one Node deep, EXIT Links beyond the second splitter's corner along +x (the cross exit) or +y (the straight exit)."""
    x1, y1, half = CORNER["x1"], CORNER["y1"], CHANNEL // 2
    if which == "cross":
        return [[x1 + EXIT, y, 0] for y in range(y1 - half, y1 + half + 1)]
    return [[x, y1 + EXIT, 0] for x in range(x1 - half, x1 + half + 1)]


def gate_nodes(count_depth: tuple[int, int]) -> list[list[int]]:
    """The window body across the transmitted arm: the channel's width, `depth` Nodes deep along +x, midway between the first splitter and the mirror."""
    _, depth = count_depth
    x0, x1, y0 = CORNER["x0"], CORNER["x1"], CORNER["y0"]
    start = (x0 + x1) // 2 - depth // 2
    return box(start, start + depth - 1, y0 - CHANNEL // 2, y0 + CHANNEL // 2)


def wave_number() -> float:
    """The light's wave number k = 2 pi / lambda at the giver's wavelength to the Link."""
    return 2 * math.pi / WAVELENGTH


def inside_wave_number(count: int, level_entries: int) -> float | None:
    """k_in inside a window of the count at the level entering the Link `level_entries` times (THE BAND AT A PACE, [1, 1]): 1 - cos k_in = (Gamma / p)^2 (1 - cos k), p = Gamma - level_entries x count; None where the record is evanescent (a mirror)."""
    p = GAMMA - level_entries * count
    if p <= 0:
        return None
    value = 1 - (GAMMA / p) ** 2 * (1 - math.cos(wave_number()))
    return math.acos(value) if -1 <= value <= 1 else None


def gate_phase(count_depth: tuple[int, int], level_entries: int) -> float | None:
    """The phase gate's turn (k_in - k) l over the depth l, radians; None where the window is a mirror at that reading of the level."""
    count, depth = count_depth
    k_in = inside_wave_number(count, level_entries)
    return None if k_in is None else (k_in - wave_number()) * depth


def mirror_line(level_entries: int) -> float:
    """The count above which a body is a total mirror for the light: p < Gamma sin(k / 2), the level entering `level_entries` times."""
    return GAMMA * (1 - math.sin(wave_number() / 2)) / level_entries


def shares(s: float, delta: float) -> dict[str, float]:
    """The row (l): 4 s (1 - s) cos^2 (Delta / 2) of the clicks at the cross exit and one minus that at the straight exit."""
    cross = 4 * s * (1 - s) * math.cos(delta / 2) ** 2
    return {"cross_exit": round(cross, 4), "straight_exit": round(1 - cross, 4)}


def mode_file(name: str, document: dict[str, Any]) -> None:
    """The mode file beside the world: the giver's entry from tools/pixel_mode.py with Cheshbon's pair for its count (the Closer's order of 15:32 Israel: twist 0, the wavelength by his line); every other body loads as content alone."""
    giver_only = {**document, "measured": document["measured"][:1]}
    entry = pixel_mode.pixel_mode(giver_only, PAIRS_AT_24)["bodies"][0]
    entry["twist"] = 0
    entry["wavelength"] = WAVELENGTH
    universe = json.loads((ROOT / document["universe"]).read_text(encoding="utf-8"))
    pairs = {family["name"]: list(family["pair"]) for family in universe["families"]}
    bodies: list[dict[str, Any]] = [entry]
    for item in document["measured"][1:]:
        bodies.append(
            {
                "family": item["family"],
                "pair": pairs[item["family"]],
                "mode": "none: no giving and no momentum, the body loads as content alone",
            }
        )
    mode = {"world_digest": pixel_mode.input_digest(document), "bodies": bodies}
    (HERE / f"{name}.mode.json").write_text(json.dumps(mode) + "\n", encoding="utf-8")


def one_qubit(name: str, gate: tuple[int, int] | None) -> None:
    """One world: the giver in its tube, the two splitters, the two mirrors, the walls, the phase gate where named, and the two sets at the exits."""
    x0, y0, x1, y1 = CORNER["x0"], CORNER["y0"], CORNER["x1"], CORNER["y1"]
    measured = [
        pixel(
            [GIVER_X, y0, 0],
            GIVER_COUNT,
            GAMMA,
            q=1,
            moment=[0, 0, 1],
            emitter={"family": "charge", "weight": 1, "norm": 1, "norm_denominator": 1},
            stocks={"charge": STOCK},
        ),
        body(diagonal(x0, y0, 1), SPLITTER),
        body(diagonal(x1, y1, 1), SPLITTER),
        body(diagonal(x0, y1, 3), MIRROR),
        body(diagonal(x1, y0, 3), MIRROR),
        body(exit_nodes("cross"), TAKER),
        body(exit_nodes("straight"), TAKER),
    ]
    if gate is not None:
        measured.append(body(gate_nodes(gate), gate[0]))
    occupied: set[tuple[int, int, int]] = set()
    for index, item in enumerate(measured):
        nodes = {(int(n[0]), int(n[1]), int(n[2])) for n in (line["node"] for line in item["nodes"])}
        if nodes & occupied:
            raise ValueError(
                f"measured[{index}] shares a Node with an earlier body: {sorted(nodes & occupied)[0]}"
            )
        occupied |= nodes
    measured.append(body(walls(occupied), MIRROR))
    detectors = [
        {"name": "cross_exit", "block": 5},
        {"name": "straight_exit", "block": 6},
    ]
    readings = [
        reading("light_rows", "rows", 20, family="charge"),
        reading("at_first_splitter", "level", 1, family="charge", node=[x0, y0, 0]),
        reading("on_the_transmitted_arm", "level", 1, family="charge", node=[(x0 + x1) // 2, y0, 0]),
        reading("on_the_reflected_arm", "level", 1, family="charge", node=[x0, (y0 + y1) // 2, 0]),
        reading("at_second_splitter", "level", 1, family="charge", node=[x1, y1, 0]),
        reading("giver_clock", "cycle", 1, body=0),
        reading("giver_centre", "centre", 100, body=0),
        reading("records_alive", "alive", 20),
    ]
    document = world(
        SHAPE,
        {"x": "open", "y": "open", "z": "periodic"},
        TICKS,
        measured,
        detectors,
        readings,
        face_depth=FACE_DEPTH,
        universe=PLANCK,
    )
    phases = {
        "level_once": None if gate is None else gate_phase(gate, 1),
        "level_twice": None if gate is None else gate_phase(gate, 2),
    }
    expected = {key: (None if value is None else shares(0.5, value)) for key, value in phases.items()}
    expectation = {
        "format": "world-expectation-v1",
        "row": (
            f"ALGEBRA.md #the-rows-against-nature (k) THE TWO-QUBIT COMPUTER, one qubit: the row (l) MACH-ZEHNDER on the plane {SHAPE[0]} x {SHAPE[1]} x 1 of the rule's universe at Gamma {GAMMA}; the giving pixel of {GIVER_COUNT} at x = {GIVER_X} on the row y = {y0} in a tube of walls of {MIRROR}, {WALL} Nodes thick (one wall body round every channel, closed behind the giver and beyond each exit's set), giving light of lambda {WAVELENGTH} to the Link with the stock {STOCK}; the first splitter a diagonal of {2 * HALF + 1} Nodes of {SPLITTER} along (1, 1) at ({x0}, {y0}), one Node deep along the beam; the mirrors diagonal bands three Nodes thick of {MIRROR} at ({x0}, {y1}) and ({x1}, {y0}); the second splitter at ({x1}, {y1}); the arms equal by the square ({x1 - x0} Links each way); the cross exit's set a body of {TAKER} per Node across the channel {EXIT} Links beyond the second splitter along +x and the straight exit's along +y; "
            + (
                "no phase gate"
                if gate is None
                else f"the phase gate a window of {gate[0]} per Node, {gate[1]} Nodes deep, across the transmitted arm"
            )
            + "; written before any run, no pin: the run says"
        ),
        "DETECTOR": [],
        "blind_expectation": {
            "shares_at_equal_arms": shares(0.5, 0.0),
            "shares_with_the_gate": expected,
            "gate_phase_radians": phases,
            "splitter_share": "s = 1/2 at Cheshbon's count by bisection (the row (l)); the file's count stands until his line, and the shares with the file's s are 4 s (1 - s) at the cross exit at equal arms",
            "row": "the row (l): the clicks' shares 4 s (1 - s) cos^2 (Delta / 2) at the cross exit and one minus that at the straight exit, Delta = (k_in - k) l the gate's phase (the row (k), the window body as a phase gate); the two readings of the level (once in the Link, or twice: THE LEVEL ENTERS THE LINK TWICE AND THE CLOCK ONCE) give two phases and the run separates them; the band is the draw's on the stock's clicks, sqrt(p (1 - p) / n) per exit",
        },
        "lines": {
            "wavelength": WAVELENGTH,
            "wave_number": round(wave_number(), 4),
            "mirror_line_level_once": round(mirror_line(1), 2),
            "mirror_line_level_twice": round(mirror_line(2), 2),
            "inside_wave_number_at_the_splitter": {
                "level_once": inside_wave_number(SPLITTER, 1),
                "level_twice": inside_wave_number(SPLITTER, 2),
            },
            "row": "THE BAND AT A PACE for light ([1, 1]): a body is a total mirror where its count exceeds Gamma (1 - sin(k / 2)) over the level's entries; the walls and the mirrors at 7 are mirrors with the level twice and windows with the level once (a finding on the level's entry, not on the row); the pace guard of today refuses a count of 8 and above at 24 (the content 3 c at or beyond Gamma, the light's finding of 16:58 Israel), so 7 is the file's mirror until the guard's line",
        },
        "GAMEBOARD": [
            {
                "body": 0,
                "interval": TICKS - 100,
                "centre": [GIVER_X, y0, 0],
                "band": 0,
                "row": "the giver's pixel on its Node",
            },
            {
                "reversible": TICKS,
                "row": "THE REVERSIBLE ROW: the whole run forward and back to its start on a fresh copy, every row of the GameBoard bit for bit, the clicks kept",
            },
        ],
        "GAMEBOARD_checks": [
            "(i) `light_rows` every 20 intervals and `at_first_splitter`: the record along the tube to the first splitter, then two arms (the row (l): the record's rows show the two arms)",
            "(ii) `on_the_transmitted_arm` against `on_the_reflected_arm`: the two arms' levels of one order (s near one half); one arm empty names the splitter's count a mirror or a vacuum",
            "(iii) `at_second_splitter`: the two arms meeting; `records_alive`: the records in flight and the labels left at the end",
            "then the DETECTOR reading in kind: the clicks per exit, their shares against the row's forms, the books (the quanta given, the clicks per detector, the labels ended at a face, the labels left on the GameBoard)",
        ],
        "lacks": "Cheshbon's blind numbers on #1325: the splitter's count by bisection, the phase gate's count and depth, the level's entries in the Link; the two-qubit world (the crystal's pair record of (h) at 24 and the controlled phase g_c^2 A^2 / (4 Gamma)) after Bell's world at 24; the pace guard's line for a count of 8 and above at 24",
    }
    (HERE / f"{name}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    (HERE / f"{name}.expectation.json").write_text(
        json.dumps(expectation, indent=1) + "\n", encoding="utf-8"
    )
    mode_file(name, document)


def main() -> None:
    one_qubit("one_qubit", None)
    for name, gate in GATES.items():
        one_qubit(f"one_qubit_{name}", gate)


if __name__ == "__main__":
    main()
