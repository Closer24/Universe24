"""THE ONE-QUBIT WORLDS OF (k) THE TWO-QUBIT COMPUTER on the rule's own universe at Gamma 6,000 (ALGEBRA.md #the-rows-against-nature (k) and (l) MACH-ZEHNDER; #the-paces, THE BAND AT A PACE; THE SCREEN IS A CLUSTER; the owner's word of 2026-09-28, 16:57 Israel; Cheshbon's blind numbers of 17:10 Israel on #1325 and the Closer's order of 17:22): one qubit is a record's two arms after the splitter of (l), its gates the splitter, a window body as a phase gate and the polariser. At Gamma 24 the row cannot be built from bound bodies (Cheshbon, 17:10: every bound pixel at 24 is a mirror for the giver's light, s at least 0.9, and the bisection to s = 1/2 falls between integers), so the worlds are laid at Gamma 6,000 on `examples/events/planck_6000.json`, the run of record after 24, named until the file is on main. The board is a plane open on x and y (periodic z of extent one): the giving pixel of the horizon (2,700 on the law, its rotation 0.468, the light's wavelength 7.6, the mirror line 1,795) fires light at the first splitter, a diagonal of Nodes one Node deep along the beam at the count where Cheshbon's transfer-matrix table of the reflected share crosses one half by bisection (about 1,600, a bound body above the threshold 1,353); the reflected share turns along +y and the transmitted share goes on along +x; a mirror on each arm (a diagonal band three Nodes thick at 2,300, s = 0.99) turns the arms toward the second splitter, whose two exits carry the two sets: the cross exit along +x (each arm reflected once and transmitted once at the splitters) and the straight exit along +y. No tube of walls stands round the channels: a wall of hundreds of Nodes at the gravity divisor 1 buries its own pace (the first look at 24 in pull request #1452: the content 864 at a wall Node), so the light that wanders ends at the open faces and the books count it. The phase gate is a window body across the transmitted arm, `depth` Nodes deep at a count below the mirror line: Cheshbon's 1,500 over 3 Nodes for a half turn (3.11 radians, pi - 0.03) and 1,400 over 2 for near a quarter turn (1.76, pi / 2 + 0.19), the window returning 23 to 36 percent (a loss by name). THE BLIND EXPECTATION (Cheshbon, 17:10, no pin): the shares of the clicks 4 s (1 - s) cos^2 (Delta / 2) at the cross exit and one minus that at the straight exit: at equal arms 1.00 (0.97 to 1.0) at the cross exit and 0 at the straight; with the half-turn gate 0.00 (0 to 0.03) at the cross exit; with the quarter-turn gate 0.41; the band plus or minus 0.05 at 100 clicks and 0.1 at 30. The controlled phase g_c^2 A^2 / (4 Gamma) of (k) is exactly 0 on the file (no read at a weight g_c: the reads are derived at the weight 1, a light record writes no level another record reads, no sourced row), and through a pixel (a control quantum's click into the gate's body moving its count by one) 5 x 10^-3 radians over three Nodes, below the band; so (h)'s E stands at cos 2(a - b) = 1, 0.707, 0, -0.707 at the four settings, and (k) at 6,000 is (h) without a gate; a controlled phase of order one is a hypothesis under its own name. The giver's clock pair and tail are derived from Cheshbon's rotation by the band's line (2 cos omega_b over 2^16; cosh kappa = 3 (den / num) cos omega_b - 2, his kappas of 15:50 recovered at 2,000 and 1,500) until his own numbers replace them. Run from the repository root: python examples/events/experiments/quantum_computer/lay_out_qubits.py; it rewrites the worlds, their expectations and (with the universe file in the tree) their mode files under this folder and nothing else."""

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
    PLANCK_6000,
    body,
    reading,
    world,
)

GAMMA = 6000  # the run of record after 24 (the owner's word of 15:44 Israel), cited for the expectation's formulas only
SUFFIX = "_6000"  # the worlds' names carry the Gamma that is not the file of record's, as the other experiments' do
TAIL_UNIT = 65536  # the clock pair's and the tail's denominator of tools/pixel_mode.py
GIVER_COUNT = 2700  # the horizon pixel on the law (Cheshbon, 17:10 Israel): its rotation 0.468, the light's wavelength 7.6, the mirror line 1,795
GIVER_ROTATION = 0.468  # omega_b of the giver's bound mode, Cheshbon's number of 17:10 Israel
MATTER_PAIR = (4000, 6000)  # the matter pair of planck_6000.json, for the tail's line alone
STOCK = 100  # the giver's stock: Cheshbon's band of plus or minus 0.05 on the shares is at 100 clicks
WAVELENGTH = (
    8  # the light's wavelength to the Link, 7.6 by Cheshbon's line (cos k = 3 cos omega_b - 2 on [1, 1])
)
SPLITTER_SHARES: dict[int, float] = {
    1400: 0.232,
    1500: 0.357,
    1700: 0.648,
    2000: 0.920,
    2300: 0.989,
    2600: 0.999,
}  # Cheshbon's table of 17:10 Israel: the reflected share s of one Node at the count c for the giver's light at Gamma 6,000 on the law (a transfer matrix on Rule3's equation along a chain, k across 0), the splitter by bisection between 1,500 and 1,700
MIRROR = 2300  # a mirror on each arm: s = 0.99 in Cheshbon's table
GATES: dict[str, tuple[int, int, float]] = {
    "half": (1500, 3, 3.11),
    "quarter": (1400, 2, 1.76),
}  # the phase gates (count, depth, Cheshbon's phase in radians): 1,500 turns 1.038 per Node, three Nodes pi - 0.03; 1,400 turns 0.878 per Node, two Nodes pi / 2 + 0.19
GATE_LOSS = (
    0.23,
    0.36,
)  # the window returns 23 to 36 percent (Cheshbon, 17:10), a loss by name lowering the visibility
TAKER = 1400  # the two sets' bodies at the exits, windows across the channel one Node deep below the mirror line (a set is a body's Nodes: the detector names its block)
CHANNEL = 3  # the beam's width in Nodes across which the diagonals and the sets stand
HALF = 2  # the diagonals' half-length: a diagonal of 2 HALF + 1 Nodes across the beam's width and one Node beyond on each side
CORNER = {
    "x0": 14,
    "y0": 14,
    "x1": 34,
    "y1": 34,
}  # the four corners of the square: the first splitter at (x0, y0), the mirrors at (x0, y1) and (x1, y0), the second splitter at (x1, y1); the arms 20 Links, above two wavelengths
GIVER_X = 6  # the giving pixel's Node on the beam's row, eight Links behind the first splitter, two beyond the face slab
FACE_DEPTH = 4
SHAPE = [48, 48, 1]
EXIT = 5  # the sets stand this many Links beyond the second splitter's corner
TICKS = 1500  # the run's length: the flight round the square (about 40 Links at the light's group velocity, about 100 intervals) many times over the giver's stock


def diagonal(cx: int, cy: int, thickness: int) -> list[list[int]]:
    """The Nodes of a diagonal band along the direction (1, 1) centred on (cx, cy): every Node of the square of half-side HALF whose offset from the diagonal, |(x - cx) - (y - cy)|, is within (thickness - 1) div 2, a solid band; a mirror along (1, 1) turns +x into +y and +y into +x."""
    reach = (thickness - 1) // 2
    return [
        [x, y, 0]
        for x in range(cx - HALF, cx + HALF + 1)
        for y in range(cy - HALF, cy + HALF + 1)
        if abs((x - cx) - (y - cy)) <= reach
    ]


def exit_nodes(which: str) -> list[list[int]]:
    """The set's body at an exit: the beam's width, one Node deep, EXIT Links beyond the second splitter's corner along +x (the cross exit) or +y (the straight exit)."""
    x1, y1, half = CORNER["x1"], CORNER["y1"], CHANNEL // 2
    if which == "cross":
        return [[x1 + EXIT, y, 0] for y in range(y1 - half, y1 + half + 1)]
    return [[x, y1 + EXIT, 0] for x in range(x1 - half, x1 + half + 1)]


def gate_nodes(depth: int) -> list[list[int]]:
    """The window body across the transmitted arm: the beam's width, `depth` Nodes deep along +x, midway between the first splitter and the mirror."""
    x0, x1, y0 = CORNER["x0"], CORNER["x1"], CORNER["y0"]
    start = (x0 + x1) // 2 - depth // 2
    return [
        [x, y, 0]
        for x in range(start, start + depth)
        for y in range(y0 - CHANNEL // 2, y0 + CHANNEL // 2 + 1)
    ]


def share_at(count: int) -> float:
    """The reflected share at a count read on Cheshbon's table by the line between its two nearest rows."""
    counts = sorted(SPLITTER_SHARES)
    if count <= counts[0]:
        return SPLITTER_SHARES[counts[0]]
    if count >= counts[-1]:
        return SPLITTER_SHARES[counts[-1]]
    below = max(c for c in counts if c <= count)
    above = min(c for c in counts if c >= count)
    if above == below:
        return SPLITTER_SHARES[below]
    weight = (count - below) / (above - below)
    return SPLITTER_SHARES[below] + weight * (SPLITTER_SHARES[above] - SPLITTER_SHARES[below])


def splitter_count() -> int:
    """The splitter's count by bisection on the table to the reflected share one half (the row (l)), to the whole quantum."""
    low, high = min(SPLITTER_SHARES), max(SPLITTER_SHARES)
    while high - low > 1:
        middle = (low + high) // 2
        if share_at(middle) < 0.5:
            low = middle
        else:
            high = middle
    return high if abs(share_at(high) - 0.5) < abs(share_at(low) - 0.5) else low


def giver_pair() -> tuple[int, int, int]:
    """The giver's clock pair [a, 2^16] (2 cos omega_b) and its tail t = e^-kappa over 2^16 from Cheshbon's rotation by the band's line, cosh kappa = 3 (den / num) cos omega_b - 2 (his kappas 1.015 at 2,000 and 0.446 at 1,500 recovered), for tools/pixel_mode.py until his own numbers."""
    num, den = MATTER_PAIR
    cosine = math.cos(GIVER_ROTATION)
    kappa = math.acosh(3 * den / num * cosine - 2)
    return round(2 * cosine * TAIL_UNIT), TAIL_UNIT, round(math.exp(-kappa) * TAIL_UNIT)


def shares(s: float, delta: float) -> dict[str, float]:
    """The row (l): 4 s (1 - s) cos^2 (Delta / 2) of the clicks at the cross exit and one minus that at the straight exit."""
    cross = 4 * s * (1 - s) * math.cos(delta / 2) ** 2
    return {"cross_exit": round(cross, 4), "straight_exit": round(1 - cross, 4)}


def mode_file(name: str, document: dict[str, Any]) -> None:
    """The mode file beside the world: the giver's entry from tools/pixel_mode.py with the derived pair (twist 0 and the wavelength by the line, the Closer's order of 15:32 Israel); every other body loads as content alone; nothing written while the universe file is not in the tree."""
    if not (ROOT / document["universe"]).exists():
        print(f"{name}: no mode file, {document['universe']} is not in the tree yet")
        return
    giver_only = {**document, "measured": document["measured"][:1]}
    entry = pixel_mode.pixel_mode(giver_only, {GIVER_COUNT: giver_pair()})["bodies"][0]
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


def one_qubit(name: str, gate: tuple[int, int, float] | None) -> None:
    """One world: the giver, the two splitters, the two mirrors, the two sets at the exits, and the phase gate where named."""
    x0, y0, x1, y1 = CORNER["x0"], CORNER["y0"], CORNER["x1"], CORNER["y1"]
    splitter = splitter_count()
    measured = [
        body(
            [[GIVER_X, y0, 0]],
            GIVER_COUNT,
            q=1,
            moment=[0, 0, 1],
            emitter={"family": "charge", "weight": 1, "norm": 1, "norm_denominator": 1},
            stocks={"charge": STOCK},
        ),
        body(diagonal(x0, y0, 1), splitter),
        body(diagonal(x1, y1, 1), splitter),
        body(diagonal(x0, y1, 3), MIRROR),
        body(diagonal(x1, y0, 3), MIRROR),
        body(exit_nodes("cross"), TAKER),
        body(exit_nodes("straight"), TAKER),
    ]
    if gate is not None:
        measured.append(body(gate_nodes(gate[1]), gate[0]))
    occupied: set[tuple[int, int, int]] = set()
    for index, item in enumerate(measured):
        nodes = {(int(n[0]), int(n[1]), int(n[2])) for n in (line["node"] for line in item["nodes"])}
        if nodes & occupied:
            raise ValueError(
                f"measured[{index}] shares a Node with an earlier body: {sorted(nodes & occupied)[0]}"
            )
        occupied |= nodes
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
        universe=PLANCK_6000,
    )
    s = share_at(splitter)
    delta = 0.0 if gate is None else gate[2]
    expectation = {
        "format": "world-expectation-v1",
        "row": (
            f"ALGEBRA.md #the-rows-against-nature (k) THE TWO-QUBIT COMPUTER, one qubit: the row (l) MACH-ZEHNDER on the plane {SHAPE[0]} x {SHAPE[1]} x 1 of the rule's universe at Gamma {GAMMA} ({PLANCK_6000}); the giving pixel of {GIVER_COUNT} (the horizon on the law, its rotation {GIVER_ROTATION}) at x = {GIVER_X} on the row y = {y0}, giving light of wavelength 7.6 with the stock {STOCK}; the first splitter a diagonal of {2 * HALF + 1} Nodes of {splitter} along (1, 1) at ({x0}, {y0}), one Node deep along the beam, the count by bisection on Cheshbon's table to s = 1/2 (s = {s:.3f} there); the mirrors diagonal bands three Nodes thick of {MIRROR} at ({x0}, {y1}) and ({x1}, {y0}) (s = 0.99); the second splitter at ({x1}, {y1}); the arms equal by the square ({x1 - x0} Links each way); the cross exit's set a body of {TAKER} per Node across the beam {EXIT} Links beyond the second splitter along +x and the straight exit's along +y; no walls (a cluster of hundreds of Nodes buries its pace at the divisor 1); "
            + (
                "no phase gate"
                if gate is None
                else f"the phase gate a window of {gate[0]} per Node, {gate[1]} Nodes deep, across the transmitted arm, Cheshbon's phase {gate[2]} radians"
            )
            + "; written before any run, no pin: the run says"
        ),
        "DETECTOR": [],
        "blind_expectation": {
            "shares": shares(s, delta),
            "cheshbon_17_10_israel": (
                "at equal arms 1.00 (0.97 to 1.0) at the cross exit and 0 at the straight; the half-turn gate 1,500 x 3 gives 0.00 (0 to 0.03) at the cross exit; the quarter-turn gate 1,400 x 2 gives 0.41; the band plus or minus 0.05 at 100 clicks and 0.1 at 30; the window returns 23 to 36 percent, a loss by name lowering the visibility to the window's 4 s (1 - s)"
            ),
            "gate_phase_radians": delta,
            "gate_loss": None if gate is None else list(GATE_LOSS),
            "controlled_phase": "g_c^2 A^2 / (4 Gamma) is exactly 0 on the file (the reads derived at the weight 1, a light record writing no level another record reads, no sourced row); through a pixel (a control quantum's click into the gate's body moving its count by one, k' moving by 1.6 x 10^-3 radians per Node per quantum) 5 x 10^-3 radians over three Nodes, below the band; a controlled phase of order one is a hypothesis under its own name",
            "E_of_h": {
                "0": 1.0,
                "pi/8": 0.707,
                "pi/4": 0.0,
                "3pi/8": -0.707,
                "row": "cos 2(a - b) at the four settings, the controlled phase within 5 x 10^-3 of it: (k) at 6,000 is (h) without a gate (Cheshbon, 17:10 Israel)",
            },
            "row": "the row (l): the clicks' shares 4 s (1 - s) cos^2 (Delta / 2) at the cross exit and one minus that at the straight exit, Delta = (k_in - k) l the gate's phase (the row (k), the window body as a phase gate); the band is the draw's on the clicks, sqrt(p (1 - p) / n) per exit",
        },
        "lines": {
            "wavelength": 7.6,
            "wave_number": 0.826,
            "mirror_line": 1795,
            "bound_threshold": 1353,
            "splitter_table": SPLITTER_SHARES,
            "splitter_count": splitter,
            "giver_pair": list(giver_pair()),
            "row": "Cheshbon's lines of 17:10 Israel at Gamma 6,000 on the law (the level twice in the Link): the giver's light at 7.6, the mirror line 1,795, the bound threshold 1,353, the reflected share per count from the transfer matrix on Rule3's equation; the giver's pair derived from his rotation by the band's line until his own numbers; at Gamma 24 no bound body is a splitter for the light and the row is not laid there",
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
            "(i) `light_rows` every 20 intervals and `at_first_splitter`: the record from the giver to the first splitter, then two arms (the row (l): the record's rows show the two arms)",
            "(ii) `on_the_transmitted_arm` against `on_the_reflected_arm`: the two arms' levels of one order (s near one half); one arm empty names the splitter's count a mirror or a vacuum",
            "(iii) `at_second_splitter`: the two arms meeting; `records_alive`: the records in flight and the labels left at the end",
            "then the DETECTOR reading in kind: the clicks per exit, their shares against the row's forms, the books (the quanta given, the clicks per detector, the labels ended at a face, the labels left on the GameBoard)",
        ],
        "lacks": "the universe file planck_6000.json on main (pull request #1450); Cheshbon's own clock pair and tail for the giver of 2,700 (derived here from his rotation); the two-qubit world (the crystal's pair record of (h) at 6,000) after Bell's world at 6,000; the pace guard's reading of a cluster's own wells at the divisor 1 (the diagonals of 5 and 13 Nodes)",
    }
    (HERE / f"{name}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    (HERE / f"{name}.expectation.json").write_text(
        json.dumps(expectation, indent=1) + "\n", encoding="utf-8"
    )
    mode_file(name, document)


def main() -> None:
    one_qubit(f"one_qubit{SUFFIX}", None)
    for name, gate in GATES.items():
        one_qubit(f"one_qubit_{name}{SUFFIX}", gate)


if __name__ == "__main__":
    main()
