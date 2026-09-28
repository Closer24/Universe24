"""THE ONE-QUBIT WORLDS OF (k) THE TWO-QUBIT COMPUTER on the rule's own universe at Gamma 6,000, the optics sieves of single pixels (ALGEBRA.md #the-rows-against-nature (k) and (l) MACH-ZEHNDER; #the-paces, THE BAND AT A PACE; THE SCREEN IS A CLUSTER; the owner's word of 2026-09-28, 16:57 Israel; Cheshbon's lines of 17:10, 17:23 and 17:36 Israel on #1325 and the Closer's orders of 17:22 and 17:43): one qubit is a record's two arms after the splitter of (l), its gates the splitter, a window body as a phase gate and the polariser. At Gamma 24 the row cannot be built from bound bodies (Cheshbon, 17:10: every bound pixel at 24 is a mirror for the giver's light and the bisection to s = 1/2 falls between integers), and a continuous wall of bound pixels exists at no Gamma (17:23: adjacent pixels cross the horizon together; the first look of pull request #1452: the content 864 at a wall Node at 24, 44,079 at a mirror band's centre at 6,000), so every optical body is a sieve of single pixels at the period 2, a plane of 5 x 5 = 25 pixels on the beam's cross-section of 9 x 9, an effective medium for the light of wavelength 7.6 whose plane average is set by the pixels' tails (17:36): the mirror three planes of pixels of 1,500 two Links apart (the plane average 2,091 above the mirror line 1,795; s = 0.954 for one plane, 1.000 for three); the phase gate planes of pixels of 2,500 two Links apart along the arm (s = 0.006 per plane, the phase 0.54 radians per plane: three planes 1.63, near a quarter turn; six planes 3.26, near a half turn); the splitter one plane on the diagonal (1, 1) at the count where the sieve's reflected share crosses one half by bisection on his table (between 1,700 at 0.65 and 2,000 at 0.005, about 1,800, the band 1,750 to 1,900); the sets planes of pixels of 1,500, a mirror that takes (the click at the pixel). The board is a box 48 x 48 x 9, open on x and y and closed on z: the giving pixel of the horizon (2,700 on the law, its rotation 0.468, the light's wavelength 7.6) fires along +x at the first splitter; the reflected share turns along +y and the transmitted share goes on along +x; a mirror on each arm turns the arms toward the second splitter, whose two exits carry the two sets: the cross exit along +x (each arm reflected once and transmitted once at the splitters) and the straight exit along +y; no tube round the channels, the light that wanders ends at the open faces and the books count it. THE BLIND EXPECTATION (Cheshbon, 17:36, no pin): the shares of the clicks 4 s (1 - s) cos^2 (Delta / 2) at the cross exit and one minus that at the straight exit: at equal arms 1.00 (0.95 to 1.00) at the cross exit and 0 at the straight; with the six-plane gate 0.00 (0 to 0.04) at the cross exit; with the three-plane gate cos^2 (0.815) = 0.47 (0.40 to 0.55); the band plus or minus 0.05 at 100 clicks. The controlled phase g_c^2 A^2 / (4 Gamma) of (k) is exactly 0 on the file (no read at a weight g_c: the reads are derived at the weight 1, a light record writes no level another record reads, no sourced row), and through a pixel (a control quantum's click into one plane of the gate moving one pixel's count by one) about 2 x 10^-4 radians, not measurable; so (h)'s E stands at cos 2(a - b) = 1, 0.707, 0, -0.707 at the four settings, and (k) at 6,000 is (h) without a gate; a controlled phase of order one is a hypothesis under its own name. The giver's clock pair and tail are derived from Cheshbon's rotation by the band's line (2 cos omega_b over 2^16; cosh kappa = 3 (den / num) cos omega_b - 2, his kappas of 15:50 recovered at 2,000 and 1,500) until his own numbers replace them. Run from the repository root: python examples/events/experiments/quantum_computer/lay_out_qubits.py; it rewrites the worlds, their expectations and (with the universe file in the tree) their mode files under this folder and nothing else."""

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
PERIOD = 2  # the sieves' period (Cheshbon, 17:23 and 17:36): pixels every second Node across a plane, the planes two Links apart; a period below the wavelength makes the plane an effective medium
SIEVE_SHARES: dict[int, float] = {
    1700: 0.65,
    2000: 0.005,
}  # Cheshbon's table of 17:36 Israel: the reflected share s of one plane sieve at the period 2 by the count of its pixels (the plane average 1,700 and 848), for the giver's light at Gamma 6,000 on the law; the splitter by bisection between them
SPLITTER_BAND = (1750, 1900)  # Cheshbon's band on the splitter's count (about 1,800)
MIRROR = (
    1500,
    3,
)  # a mirror: three plane sieves of pixels of 1,500 two Links apart (the plane average 2,091 above the mirror line 1,795; s = 0.954 for one plane, 1.000 for three)
GATES: dict[str, tuple[int, int, float, tuple[float, float]]] = {
    "half": (2500, 6, 3.26, (0.0, 0.04)),
    "quarter": (2500, 3, 1.63, (0.40, 0.55)),
}  # the phase gates (the pixels' count, the planes, Cheshbon's phase in radians, his band on the cross share): 2,500 turns 0.54 per plane at s = 0.006 per plane
TAKER = 1500  # the two sets: a plane sieve of pixels of 1,500 each, a mirror that takes (the click at the pixel), the detector's block
BEAM = 9  # the beam's cross-section, 9 x 9 Nodes: 5 x 5 pixels per plane at the period 2
HALF = BEAM // 2  # the cross-section's half-width
CORNER = {
    "x0": 14,
    "y0": 14,
    "x1": 34,
    "y1": 34,
}  # the four corners of the square: the first splitter at (x0, y0), the mirrors at (x0, y1) and (x1, y0), the second splitter at (x1, y1); the arms 20 Links, above two wavelengths
GIVER_X = 6  # the giving pixel's Node on the beam's axis, eight Links behind the first splitter's centre, two beyond the face slab
FACE_DEPTH = 4
SHAPE = [48, 48, BEAM]
AXIS_Z = HALF  # the beam's axis on z, the middle of the closed axis
EXIT = 5  # the sets stand this many Links beyond the second splitter's corner
TICKS = 1500  # the run's length: the flight round the square (about 40 Links at the light's group velocity, about 100 intervals) many times over the giver's stock


def across() -> list[int]:
    """The pixels' offsets across the beam at the period: -4, -2, 0, 2, 4 on a cross-section of 9."""
    return list(range(-HALF, HALF + 1, PERIOD))


def diagonal_plane(cx: int, cy: int, offset: int) -> list[list[int]]:
    """One plane sieve on the diagonal (1, 1) through (cx + offset, cy): the pixels (cx + offset + i, cy + i, z) at the period along the diagonal and along z, 25 on the cross-section; a plane along (1, 1) turns +x into +y and +y into +x, and parallel planes stand at offsets of the period along x."""
    return [[cx + offset + i, cy + i, AXIS_Z + j] for i in across() for j in across()]


def mirror_planes(cx: int, cy: int) -> list[list[int]]:
    """The mirror's planes on the diagonal through (cx, cy): MIRROR[1] plane sieves, the period apart along x, centred on the corner."""
    count = MIRROR[1]
    offsets = [PERIOD * (k - (count - 1) / 2) for k in range(count)]
    return [node for offset in offsets for node in diagonal_plane(cx, cy, round(offset))]


def cross_plane(x: int, cy: int) -> list[list[int]]:
    """One plane sieve across the beam along +x at the column x: the pixels (x, cy + i, z) at the period."""
    return [[x, cy + i, AXIS_Z + j] for i in across() for j in across()]


def straight_plane(cx: int, y: int) -> list[list[int]]:
    """One plane sieve across the beam along +y at the row y: the pixels (cx + i, y, z) at the period."""
    return [[cx + i, y, AXIS_Z + j] for i in across() for j in across()]


def gate_nodes(planes: int) -> list[list[int]]:
    """The phase gate across the transmitted arm: `planes` plane sieves the period apart along +x, midway between the first splitter and the mirror."""
    x0, x1, y0 = CORNER["x0"], CORNER["x1"], CORNER["y0"]
    start = (x0 + x1) // 2 - PERIOD * (planes - 1) // 2
    return [node for k in range(planes) for node in cross_plane(start + PERIOD * k, y0)]


def share_at(count: int) -> float:
    """The reflected share at a count read on Cheshbon's table by the line between its two nearest rows."""
    counts = sorted(SIEVE_SHARES)
    if count <= counts[0]:
        return SIEVE_SHARES[counts[0]]
    if count >= counts[-1]:
        return SIEVE_SHARES[counts[-1]]
    below = max(c for c in counts if c <= count)
    above = min(c for c in counts if c >= count)
    if above == below:
        return SIEVE_SHARES[below]
    weight = (count - below) / (above - below)
    return SIEVE_SHARES[below] + weight * (SIEVE_SHARES[above] - SIEVE_SHARES[below])


def splitter_count() -> int:
    """The splitter's count by bisection on the table to the reflected share one half (the row (l): the half at the count found by bisection, on the sieve's count), to the whole quantum, refused outside Cheshbon's band."""
    low, high = min(SIEVE_SHARES), max(SIEVE_SHARES)
    falling = share_at(high) < share_at(
        low
    )  # a sieve's share falls with its pixels' count (the tail shortens)
    while high - low > 1:
        middle = (low + high) // 2
        if (share_at(middle) < 0.5) != falling:
            low = middle
        else:
            high = middle
    found = high if abs(share_at(high) - 0.5) < abs(share_at(low) - 0.5) else low
    if not SPLITTER_BAND[0] <= found <= SPLITTER_BAND[1]:
        raise ValueError(f"the splitter's count {found} lies outside Cheshbon's band {SPLITTER_BAND}")
    return found


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


def one_qubit(name: str, gate: tuple[int, int, float, tuple[float, float]] | None) -> None:
    """One world: the giver, the two splitters, the two mirrors, the two sets at the exits, and the phase gate where named; every optical body one sieve, its pixels the body's Nodes."""
    x0, y0, x1, y1 = CORNER["x0"], CORNER["y0"], CORNER["x1"], CORNER["y1"]
    splitter = splitter_count()
    measured = [
        body(
            [[GIVER_X, y0, AXIS_Z]],
            GIVER_COUNT,
            q=1,
            moment=[0, 0, 1],
            emitter={"family": "charge", "weight": 1, "norm": 1, "norm_denominator": 1},
            stocks={"charge": STOCK},
        ),
        body(diagonal_plane(x0, y0, 0), splitter),
        body(diagonal_plane(x1, y1, 0), splitter),
        body(mirror_planes(x0, y1), MIRROR[0]),
        body(mirror_planes(x1, y0), MIRROR[0]),
        body(cross_plane(x1 + EXIT, y1), TAKER),
        body(straight_plane(x1, y1 + EXIT), TAKER),
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
        reading("at_first_splitter", "level", 1, family="charge", node=[x0, y0, AXIS_Z]),
        reading(
            "on_the_transmitted_arm", "level", 1, family="charge", node=[(x0 + x1) // 2, y0, AXIS_Z]
        ),
        reading("on_the_reflected_arm", "level", 1, family="charge", node=[x0, (y0 + y1) // 2, AXIS_Z]),
        reading("at_second_splitter", "level", 1, family="charge", node=[x1, y1, AXIS_Z]),
        reading("giver_clock", "cycle", 1, body=0),
        reading("giver_centre", "centre", 100, body=0),
        reading("records_alive", "alive", 20),
    ]
    document = world(
        SHAPE,
        {"x": "open", "y": "open", "z": "closed"},
        TICKS,
        measured,
        detectors,
        readings,
        face_depth=FACE_DEPTH,
        universe=PLANCK_6000,
    )
    s = share_at(splitter)
    delta = 0.0 if gate is None else gate[2]
    band = (0.95, 1.0) if gate is None else gate[3]
    expectation = {
        "format": "world-expectation-v1",
        "row": (
            f"ALGEBRA.md #the-rows-against-nature (k) THE TWO-QUBIT COMPUTER, one qubit: the row (l) MACH-ZEHNDER on the box {SHAPE[0]} x {SHAPE[1]} x {SHAPE[2]} of the rule's universe at Gamma {GAMMA} ({PLANCK_6000}), open on x and y, closed on z; every optical body a sieve of single pixels at the period {PERIOD} (THE SCREEN IS A CLUSTER: a continuous wall of bound pixels exists at no Gamma), a plane 5 x 5 = 25 pixels on the beam's cross-section of {BEAM} x {BEAM}; the giving pixel of {GIVER_COUNT} (the horizon on the law, its rotation {GIVER_ROTATION}) at x = {GIVER_X} on the axis y = {y0}, z = {AXIS_Z}, giving light of wavelength 7.6 with the stock {STOCK}; the first splitter one plane sieve on the diagonal (1, 1) at ({x0}, {y0}) of pixels of {splitter}, the count by bisection on Cheshbon's table of the sieve's reflected share to s = 1/2 (s = {s:.3f} there, his band {SPLITTER_BAND[0]} to {SPLITTER_BAND[1]}); the mirrors {MIRROR[1]} plane sieves of pixels of {MIRROR[0]} two Links apart on the diagonals at ({x0}, {y1}) and ({x1}, {y0}) (s = 1.000 for three planes); the second splitter at ({x1}, {y1}); the arms equal by the square ({x1 - x0} Links each way); the cross exit's set a plane sieve of pixels of {TAKER} across the beam {EXIT} Links beyond the second splitter along +x and the straight exit's along +y (a mirror that takes, the click at the pixel); no tube, the wandering light ends at the open faces; "
            + (
                "no phase gate"
                if gate is None
                else f"the phase gate {gate[1]} plane sieves of pixels of {gate[0]} two Links apart across the transmitted arm, Cheshbon's phase {gate[2]} radians (0.54 per plane, s = 0.006 per plane)"
            )
            + "; written before any run, no pin: the run says"
        ),
        "DETECTOR": [],
        "blind_expectation": {
            "shares": shares(s, delta),
            "cross_share_band": list(band),
            "cheshbon_17_36_israel": (
                "at equal arms 1.00 (0.95 to 1.00) at the cross exit and 0.00 at the straight (the mirror without loss, the splitter 4 s (1 - s) at least 0.96 at s = 0.5 plus or minus 0.1); the six-plane gate (Delta = 3.26) 0.00 (0 to 0.04) at the cross exit; the three-plane gate (Delta = 1.63) cos^2 (0.815) = 0.47 (0.40 to 0.55); the gate's loss 0.6 percent per plane; the band plus or minus 0.05 at 100 clicks"
            ),
            "gate_phase_radians": delta,
            "controlled_phase": "g_c^2 A^2 / (4 Gamma) is exactly 0 on the file (the reads derived at the weight 1, a light record writing no level another record reads, no sourced row); through a pixel (a control quantum's click into one plane of the gate, one pixel's count moving by one) about 2 x 10^-4 radians, not measurable; a controlled phase of order one is a hypothesis under its own name",
            "E_of_h": {
                "0": 1.0,
                "pi/8": 0.707,
                "pi/4": 0.0,
                "3pi/8": -0.707,
                "row": "cos 2(a - b) at the four settings, the controlled phase within 2 x 10^-4 of it: (k) at 6,000 is (h) without a gate (Cheshbon, 17:10 and 17:36 Israel)",
            },
            "row": "the row (l): the clicks' shares 4 s (1 - s) cos^2 (Delta / 2) at the cross exit and one minus that at the straight exit, Delta = (k_in - k) l the gate's phase (the row (k), the window body as a phase gate, here a sieve whose plane average sets k_in); the band is the draw's on the clicks, sqrt(p (1 - p) / n) per exit",
        },
        "lines": {
            "wavelength": 7.6,
            "wave_number": 0.826,
            "mirror_line": 1795,
            "bound_threshold": 1353,
            "plane_average_at_the_period_2": {
                "1500": 2091,
                "1700": 1700,
                "2000": 848,
                "2500": 858,
                "2700": 909,
            },
            "sieve_table": SIEVE_SHARES,
            "splitter_count": splitter,
            "giver_pair": list(giver_pair()),
            "row": "Cheshbon's lines of 17:10 and 17:36 Israel at Gamma 6,000 on the law (the level twice in the Link): the giver's light at 7.6, the mirror line 1,795, the bound threshold 1,353; a plane sieve at the period 2 is an effective medium whose plane average is the pixels plus their tails in the holes (a pixel near the threshold with a long tail fills the holes and makes a mirror, a deep pixel with a short tail leaves the plane nearly transparent); the reflected share per plane from the transfer matrix on Rule3's equation; the giver's pair derived from his rotation by the band's line until his own numbers; at Gamma 24 no bound body is a splitter for the light and the row is not laid there",
        },
        "GAMEBOARD": [
            {
                "body": 0,
                "interval": TICKS - 100,
                "centre": [GIVER_X, y0, AXIS_Z],
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
        "lacks": "Cheshbon's own clock pair and tail for the giver of 2,700 (derived here from his rotation); the two-qubit world (the crystal's pair record of (h) at 6,000) after Bell's world at 6,000; the pace guard's reading of a sieve's pixels at the divisor 1 (every pixel below the horizon by his line: 2,091 plus the wells below 3,000)",
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
