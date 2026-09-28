"""The worlds of record of the 24 experiments laid out in the law's form (ALGEBRA.md #what-a-body-is): every body its family, its Nodes with their counts, its momentum's two levels and its phase denominator; the givers their emitter, stocks and moment; the sets by block or by positions; the readings the GameBoard check plan asks for. The counts follow the Boss's rules of record (#1198, 20:18Z and 20:36Z): a mirror or a wall at MIRROR quanta per Node, a window at WINDOW, one-armed givings by a mirror one Link behind the giver, the moving clock at VELOCITY Links per interval with the transverse mirror across the motion. Every mode number (the giver's norm, the clock, the phase's pair) is the generator's (tools/body_generator.py) and is not computed here: the emitter's norm is carried from the shipped fall world until the generator writes it. Run from the repository root: python examples/events/experiments/lay_out_worlds.py; it rewrites every world file under this folder and nothing else."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SHARED_UNIVERSE = "examples/events/generated/universe.json"  # the shipped families' rows, no divisor
UNIVERSE = (
    "examples/events/experiments/universe.json"  # the rows of record: the held rows with `divisor`
)
DIVISOR = {
    "gravity": 40000,
    "charge": 40000,
}  # E_s per held row: at least 4 Gamma on the fall's chain (approval 1); the redshift's and the charge's per approvals 3 and 7 to set
ENGINE = "examples/events/engine_start.json"
STEPS = 1024  # N, the phase's steps of every world of record at lambda 4
DENOMINATOR = 1024  # every body's phase denominator, the pair (m, j) the generator fills
GAMMA = 10000  # the universe's node clock, cited for the expectations' formulas only
MOMENTUM_UNIT = 64  # Q, the universe's momentum unit (W = 3 Q M)
MIRROR = 8000  # a mirror or a wall: above B's line c > Gamma (1 - sin(k / 2)) at lambda 4 (2,929) and 16 (8,050)
WINDOW = 2000  # a window: the giver where its arm passes, a screen, a polariser, the falling body
NORM = {"norm": 180255439696889394, "norm_denominator": 3948169}  # carried from generated/fall.json
VELOCITY = Fraction(
    1, 5
)  # the moving bodies' v in Links per interval, below matter's 0.25 and light's 0.447
LIGHT_SPEED = 0.44721  # the given light's group velocity at lambda 4, 1 / sqrt 5 (approval 4)


def box(x0: int, x1: int, y0: int, y1: int, z0: int, z1: int) -> list[list[int]]:
    """Every Node of the box with both ends included."""
    return [[x, y, z] for x in range(x0, x1 + 1) for y in range(y0, y1 + 1) for z in range(z0, z1 + 1)]


def body(
    nodes: list[list[int]], count: int, momentum: list[int] | None = None, **keys: Any
) -> dict[str, Any]:
    """A body in the law's form at one count per Node, at rest unless a momentum is named."""
    return {
        "family": "matter",
        "nodes": [{"node": node, "count": count} for node in nodes],
        "momentum": list(momentum or [0, 0, 0]),
        "momentum_before": list(momentum or [0, 0, 0]),
        "phase_denominator": DENOMINATOR,
        **keys,
    }


def giver(
    nodes: list[list[int]], count: int, stock: int, weight: int = 1, **keys: Any
) -> dict[str, Any]:
    """A giving body: the emitter of light (the charge family) with its stock and its moment."""
    emitter = {"family": "charge", "weight": weight, **NORM}
    return body(nodes, count, moment=[0, 0, 1], emitter=emitter, stocks={"charge": stock}, **keys)


def momentum_of(nodes: list[list[int]], count: int, velocity: Fraction) -> list[int]:
    """The momentum n = W v along x with W = 3 Q M, M the body's quanta; exact by construction."""
    quanta = len(nodes) * count
    n = 3 * MOMENTUM_UNIT * quanta * velocity
    if n.denominator != 1:
        raise ValueError(
            f"the momentum {n} of a body of {quanta} quanta at v = {velocity} is no integer"
        )
    return [int(n), 0, 0]


def world(
    shape: list[int],
    boundary: dict[str, str],
    ticks: int,
    measured: list[dict[str, Any]],
    detectors: list[dict[str, Any]],
    readings: list[dict[str, Any]],
    face_depth: int = 32,
    universe: str = UNIVERSE,
) -> dict[str, Any]:
    document: dict[str, Any] = {
        "shape": shape,
        "boundary": boundary,
        "ticks": ticks,
        "N": STEPS,
        "engine": ENGINE,
        "universe": universe,
        "measured": measured,
        "detectors": detectors,
        "readings": readings,
    }
    if any(kind == "open" for kind in boundary.values()):
        document["face_depth"] = face_depth
    return document


def reading(name: str, kind: str, every: int, **target: Any) -> dict[str, Any]:
    return {"name": name, "kind": kind, **target, "every": every}


def write(folder: str, name: str, document: dict[str, Any], expectation: dict[str, Any]) -> None:
    path = HERE / folder / f"{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    path.with_suffix(".expectation.json").write_text(
        json.dumps(expectation, indent=1) + "\n", encoding="utf-8"
    )


CHAIN = {"x": "open", "y": "periodic", "z": "periodic"}
SUM_LINE = (
    "the hold's write is A SUM, one form (the owner's word, 21:36Z): each held family's row carries its "
    "divisor E_s (the universe file of record beside these worlds), the field outside a body is Laplace's "
    "over E_s and the pull between two bodies is the sum's, a = (c_+ - c_-) / (Gamma D) with c from that rest, "
    "the approver's number per world; the counts of rules 1 and 2 stand; the frame takes `divisor` with the "
    "hold's line (the mathematician's PR), and the rest's numbers are the generator's on the fast rest"
)
FEED_FINDING = SUM_LINE  # the name the other layout modules import


def under_a_load(gap: int, delta: int, measurement: float, what: str) -> str:
    """The line the owner reads per world, under the sum: the two bodies named, their gap and their counts' difference, and the measurement's own time; the closing time is the approver's on the rest over E_s."""
    return (
        f"under the sum, {what}: a gap of {gap} Links between counts {delta} apart, the measurement's "
        f"{measurement:.0f} intervals; the closing time from the sum's rest over E_s is the approver's"
    )


CONTACT = (
    "under the sum, the mirror one Link behind the giver is in contact with it from the start; what the "
    "count's line does at contact under the sum's rest is the approver's"
)


def the_fall() -> None:
    """Newton's fall (i): the giver of 30 Nodes with a mirror one Link behind it, the falling window."""
    giver_nodes, mirror_nodes, falling_nodes = (
        box(185, 214, 0, 0, 0, 0),
        box(181, 184, 0, 0, 0, 0),
        box(285, 287, 0, 0, 0, 0),
    )
    heavy, falling = 3600, WINDOW
    measured = [giver(giver_nodes, heavy, 64), body(falling_nodes, falling), body(mirror_nodes, MIRROR)]
    detectors = [{"name": "at_fall", "block": 1}, {"name": "at_heavy", "block": 0}]
    readings = [
        reading("fall_momentum", "momentum", 10, body=1),
        reading("fall_centre", "centre", 10, body=1),
        reading("heavy_momentum", "momentum", 10, body=0),
        reading("mirror_momentum", "momentum", 10, body=2),
        *[
            reading(f"gravity_at_{x}", "level", 100, family="gravity", node=[x, 0, 0])
            for x in (220, 250, 280, 284, 288)
        ],
        reading("light_rows", "rows", 20, family="charge"),
    ]
    # the chain rest between the clamps (THE START, ALGEBRA.md L596): linear from the giver's face to the
    # falling body's near face, and from its far face to the open face's 0
    slope_between = Fraction(falling - heavy, 285 - 214)
    c_minus = heavy + slope_between * (284 - 214)
    c_plus = falling + Fraction(0 - falling, 400 - 287) * (288 - 287)
    a = Fraction(c_plus - c_minus, GAMMA * 4)  # per interval^2, toward the giver (negative x)
    quanta = 3 * falling
    weight = 3 * MOMENTUM_UNIT * quanta
    touch = (2 * 70 / float(-a)) ** 0.5
    document = world([400, 1, 1], CHAIN, 3000, measured, detectors, readings)
    expectation = {
        "format": "world-expectation-v1",
        "lacks": "the loader's reader of a giving body in the law's form (Nature24's mode-file reader), the fast rest (#1287) and the mode file by the generator (the giver's norm, its clock by rule 6, its window period), the row (i) THE FALL on main; "
        + FEED_FINDING,
        "row": f"ALGEBRA.md #the-rows-against-nature (i) THE FALL on the chain 400 x 1 x 1 open on x: the heavy giver of 30 Nodes of {heavy} quanta at x = 185..214 giving light (N = {STEPS}, lambda_q = 4), a mirror of 4 Nodes of {MIRROR} at x = 181..184 one Link behind it (rule 2: the back arm parked, one arm toward the falling body), the falling window of 3 Nodes of {falling} at x = 285..287 released at rest; the [1, 1] rest linear between the clamps: c(284) = {float(c_minus):.1f}, c(288) = {float(c_plus):.1f}, c_+ - c_- = {float(c_plus - c_minus):.1f} over D = 4, a = {float(-a):.6f} Links per interval^2 toward the giver (Gamma = {GAMMA}); W = 3 Q M = {weight}, the momentum grows by a W = {float(-a) * weight:.0f} per interval; the centre at 286 - a t^2 / 2; the touch (70 Links) at t = {touch:.0f} at {float(-a) * touch:.3f} Links per interval, below the wall; the given records travel at {LIGHT_SPEED}; the numbers by approval 1's method on this file's integers, blind, before any run",
        "DETECTOR": [
            {
                "detector": "at_fall",
                "count": 45,
                "band": 4,
                "row": "the records reaching the falling body before the touch under a one-armed giving (approval 1: 45 of 64; 31 with two arms); the k-th record given at k times the window period of the giver's mode (the generator's number), its wait (70 - a t^2 / 2) / 0.44721",
            },
            {
                "detector": "at_fall",
                "mean_interval": 76,
                "band": 8,
                "row": "the mean wait from the giving over those clicks, approval 1's number on the shipped counts; recomputed on this file's a by the same method when the mode file names the window period",
            },
        ],
        "GAMEBOARD": [
            {
                "body": 1,
                "interval": 200,
                "momentum": [-round(float(-a) * weight * 200), 0, 0],
                "band": max(3000, round(float(-a) * weight * 20)),
                "row": "the momentum growing by a W per interval toward the giver (the feed's row), a diagnostic and no measurement",
            },
            {
                "body": 1,
                "interval": 200,
                "centre": [round(286 - float(-a) * 200**2 / 2), 0, 0],
                "band": 2,
                "row": "the centre at 286 - a t^2 / 2",
            },
            {
                "body": 1,
                "interval": 300,
                "centre": [round(286 - float(-a) * 300**2 / 2), 0, 0],
                "band": 3,
                "row": "the same at 300",
            },
            {
                "body": 0,
                "interval": 200,
                "momentum": [0, 0, 0],
                "band": round(float(-a) * weight * 200 * 20),
                "row": "the giver's momentum: the opposite sign of the falling body's (action and reaction) or none, the discriminating diagnostic between the hold's two writes; the band admits either",
            },
        ],
        "GAMEBOARD_checks": [
            "(i) `gravity_at_*` at interval 0 and 100: the rest linear between the clamps within one unit per Node, no transient after the start (a transient names the start's call missing)",
            "(ii) `light_rows` over the first 60 intervals: one arm toward the falling body, the back arm parked between the mirror and the giver's back face; two free arms name the mirror missing",
            "(iii) `fall_momentum` every 10 intervals: linear growth by a W with a from the levels read, not from this file; `heavy_momentum` and `mirror_momentum`: the reaction",
            "(iv) `fall_centre`: 286 - a t^2 / 2 within a Link, the touch near t = " + f"{touch:.0f}",
            "then the DETECTOR reading in kind: the waits shrinking as the body falls; a body falls toward the denser one",
        ],
    }
    expectation["under_the_sum"] = (
        "the fall itself is the load's pull on the falling window (the measurement); "
        + CONTACT.replace("6,000 above the giver's window", "4,400 above the giver's 3,600")
    )
    write("fall", "fall", document, expectation)


def light_clock_chain(name: str, velocity: Fraction, ticks: int) -> None:
    """The light clock on the chain (the row (e) at rest and the longitudinal clock in motion): the giver of 27 Nodes at x = 131..133, the back mirror of 36 at 127..130, the front mirror of 36 at 190..193, the gap 56 Links; all three at the same v along x."""
    giver_nodes, back_nodes, front_nodes = (
        box(131, 133, 0, 2, 0, 2),
        box(127, 130, 0, 2, 0, 2),
        box(190, 193, 0, 2, 0, 2),
    )
    measured = [
        giver(giver_nodes, WINDOW, 64, weight=3, momentum=momentum_of(giver_nodes, WINDOW, velocity)),
        body(front_nodes, MIRROR, momentum_of(front_nodes, MIRROR, velocity)),
        body(back_nodes, MIRROR, momentum_of(back_nodes, MIRROR, velocity)),
    ]
    detectors = [{"name": "at_well", "block": 0}]
    readings = [
        reading("giver_centre", "centre", 10, body=0),
        reading("front_mirror_centre", "centre", 10, body=1),
        reading("giver_momentum", "momentum", 100, body=0),
        reading("light_rows", "rows", 10, family="charge"),
        reading("light_total", "total", 100, family="charge"),
        reading("matter_total", "total", 100, family="matter"),
    ]
    rest_mean, rest_first = (2 * 56 + 3 + 2) / LIGHT_SPEED, (2 * 56 + 2) / LIGHT_SPEED
    v = float(velocity)
    gamma_u = 1 / (1 - (v / LIGHT_SPEED) ** 2) ** 0.5
    document = world([1500, 3, 3], CHAIN, ticks, measured, detectors, readings)
    if velocity == 0:
        row = f"ALGEBRA.md #the-rows-against-nature (e) THE MOVING CLOCK, the clock at rest (the reference of the transverse and the longitudinal clocks): the giver of 3 x 3 x 3 Nodes of {WINDOW} at x = 131..133 (a window), its back mirror of 36 Nodes of {MIRROR} at 127..130 one Link behind (rule 2: the back arm folded forward), the front mirror of 36 at 190..193, the gap 56 Links; the given quantum (lambda_q = 4, the group velocity {LIGHT_SPEED}) goes out and back: the mean click interval at the giver's own set (2 x 56 + 3 + 2) / {LIGHT_SPEED} = {rest_mean:.1f}, the first click (2 x 56 + 2) / {LIGHT_SPEED} = {rest_first:.1f}; the record turns at the mirror (a total mirror at {MIRROR}: nothing tunnels through 4 Nodes, B's correction of 20:13Z); written before any run"
        pins = [
            {
                "detector": "at_well",
                "mean_interval": round(rest_mean),
                "band": 9,
                "row": "the mean click interval over the stock of 64, the round trip at the group velocity",
            },
            {
                "detector": "at_well",
                "first_click": round(rest_first),
                "band": 8,
                "row": "the least wait since the giving: the head's round trip",
            },
        ]
        board = [
            {
                "body": 0,
                "interval": 1000,
                "centre": [132, 1, 1],
                "band": 1,
                "row": "the giver at rest within a Link; a drift names the feed's pull toward the mirror (the finding in `lacks`)",
            }
        ]
    else:
        long_mean = rest_mean / (1 - (v / LIGHT_SPEED) ** 2)
        row = f"ALGEBRA.md #the-rows-against-nature (e), the LONGITUDINAL clock in motion, its own row (the Boss's rule 3: the contraction test): the rest clock's three bodies at v = {v} Links per interval along x (n = W v exactly, W = 3 Q M per body), the light along the motion; in the GameBoard's frame the round trip is D / (u - v) + D / (u + v) = (2 D / u) gamma_u^2 with u = {LIGHT_SPEED} the light's group velocity and gamma_u = 1 / sqrt(1 - v^2 / u^2) = {gamma_u:.4f}: the mean click interval {rest_mean:.1f} x {gamma_u**2:.4f} = {long_mean:.1f} under the law as written (the body's Nodes do not contract); nature's contracted clock would read {rest_mean * gamma_u:.1f} (gamma_u alone), the row first; the moving bodies are the generator's packets at the phase (m, j) of v (the mode's largest group velocity 0.25, approvals 4 and 17); written before any run"
        pins = [
            {
                "detector": "at_well",
                "mean_interval": round(long_mean),
                "band": 10,
                "row": "the law's blind number: the rest interval times gamma_u^2, no contraction line in the law; gamma_u alone (the contraction) is the finding to name if read",
            }
        ]
        board = [
            {
                "body": 0,
                "interval": 1000,
                "centre": [132 + round(v * 1000), 1, 1],
                "band": 2,
                "row": f"the giver's centre at 132 + v t, v = {v}: the count's line moving its count",
            },
            {
                "body": 0,
                "interval": 1000,
                "momentum": momentum_of(giver_nodes, WINDOW, velocity),
                "band": 200000,
                "row": "the momentum constant in motion where the field between the bodies is flat; a drift names the feed (the finding in `lacks`)",
            },
        ]
    expectation = {
        "format": "world-expectation-v1",
        "lacks": "the loader's reader of a giving body in the law's form, the fast rest (#1287) and the mode file by the generator (the norm, the clock by rule 6, the phase's pair of the moving bodies); "
        + FEED_FINDING,
        "row": row,
        "DETECTOR": pins,
        "GAMEBOARD": board,
        "GAMEBOARD_checks": [
            "(i) `light_rows` every 10 intervals: the record leaves the giver toward the front mirror, the back arm folded through the window giver; it reaches the front mirror and turns (nothing beyond x = 193); it ends at the giver's set",
            "(ii) `giver_centre` and `front_mirror_centre`: at rest within a Link over the run, in motion at x_0 + v t within a Link, the gap 56 kept",
            "(iii) `matter_total`: the norm's leak per Link of travel below the law's 3 x 10^-5 (L612); `light_total`: one record's norm per giving window, none lost between the mirrors",
            "then the DETECTOR reading in kind: a periodic tick; in motion the tick lengthened",
        ],
    }
    expectation["under_the_sum"] = (
        under_a_load(56, MIRROR - WINDOW, rest_mean, "the giver against its front mirror")
        + "; "
        + CONTACT
    )
    write("light_clock", name, document, expectation)


def light_clock_transverse(name: str, velocity: Fraction, ticks: int) -> None:
    """The transverse light clock (rule 3: the mirror across the motion): the tube of mirrors around the giver on the y axis, the front mirror 56 Links up the y axis, every body at v along x; y periodic so the light meets nothing but the mirror."""
    x0 = 140
    giver_nodes = box(x0, x0 + 2, 40, 42, 0, 2)
    back_nodes = box(x0, x0 + 2, 36, 39, 0, 2)
    front_nodes = box(x0, x0 + 2, 99, 102, 0, 2)
    left_nodes = box(x0 - 4, x0 - 1, 36, 42, 0, 2)
    right_nodes = box(x0 + 3, x0 + 6, 36, 42, 0, 2)
    measured = [
        giver(giver_nodes, WINDOW, 64, weight=3, momentum=momentum_of(giver_nodes, WINDOW, velocity)),
        body(front_nodes, MIRROR, momentum_of(front_nodes, MIRROR, velocity)),
        body(back_nodes, MIRROR, momentum_of(back_nodes, MIRROR, velocity)),
        body(left_nodes, MIRROR, momentum_of(left_nodes, MIRROR, velocity)),
        body(right_nodes, MIRROR, momentum_of(right_nodes, MIRROR, velocity)),
    ]
    detectors = [{"name": "at_well", "block": 0}]
    readings = [
        reading("giver_centre", "centre", 10, body=0),
        reading("front_mirror_centre", "centre", 10, body=1),
        reading("giver_momentum", "momentum", 100, body=0),
        reading("light_rows", "rows", 10, family="charge"),
        reading("light_total", "total", 100, family="charge"),
        reading("matter_total", "total", 100, family="matter"),
    ]
    rest_mean, rest_first = (2 * 56 + 3 + 2) / LIGHT_SPEED, (2 * 56 + 2) / LIGHT_SPEED
    v = float(velocity)
    gamma_u = 1 / (1 - (v / LIGHT_SPEED) ** 2) ** 0.5
    document = world(
        [1000, 160, 3],
        {"x": "open", "y": "periodic", "z": "periodic"},
        ticks,
        measured,
        detectors,
        readings,
    )
    if velocity == 0:
        row = f"ALGEBRA.md #the-rows-against-nature (e) THE MOVING CLOCK, the transverse clock at rest: the giver of 3 x 3 x 3 Nodes of {WINDOW} at x = {x0}..{x0 + 2}, y = 40..42, its back mirror of {MIRROR} at y = 36..39, two side mirrors at x = {x0 - 4}..{x0 - 1} and {x0 + 3}..{x0 + 6} (the tube: the giving's four arms folded into the one along +y), the front mirror at y = 99..102, the gap 56 Links along y; the mean click interval (2 x 56 + 3 + 2) / {LIGHT_SPEED} = {rest_mean:.1f}, the first click {rest_first:.1f}; written before any run"
        pins = [
            {
                "detector": "at_well",
                "mean_interval": round(rest_mean),
                "band": 9,
                "row": "the round trip along y at the group velocity",
            },
            {
                "detector": "at_well",
                "first_click": round(rest_first),
                "band": 8,
                "row": "the head's round trip",
            },
        ]
        board = [
            {
                "body": 0,
                "interval": 1000,
                "centre": [x0 + 1, 41, 1],
                "band": 1,
                "row": "the giver at rest within a Link",
            }
        ]
    else:
        moving_mean = rest_mean * gamma_u
        row = f"ALGEBRA.md #the-rows-against-nature (e) THE MOVING CLOCK, the transverse clock at v = {v} Links per interval along x (n = W v exactly per body; the five bodies the generator's packets at one phase): the light crosses the gap 56 along y while the clock moves, the round trip 2 D / sqrt(u^2 - v^2) = (2 D / u) gamma_u with u = {LIGHT_SPEED} and gamma_u = {gamma_u:.4f}: the mean click interval {rest_mean:.1f} x {gamma_u:.4f} = {moving_mean:.1f}, the row's dilation on the lattice's own light speed (the dispersion's factor at the world's k replaces gamma_u when the mode file names k); the resting transverse clock reads {rest_mean:.1f}; written before any run"
        pins = [
            {
                "detector": "at_well",
                "mean_interval": round(moving_mean),
                "band": 10,
                "row": "the rest interval times gamma_u: the moving clock ticks slower (nature: time dilation)",
            }
        ]
        board = [
            {
                "body": 0,
                "interval": 1000,
                "centre": [x0 + 1 + round(v * 1000), 41, 1],
                "band": 2,
                "row": f"the giver's centre at x_0 + v t along x, v = {v}, its y unchanged",
            },
            {
                "body": 1,
                "interval": 1000,
                "centre": [x0 + 1 + round(v * 1000), 100, 1],
                "band": 2,
                "row": "the front mirror keeps pace: the gap 56 along y kept",
            },
        ]
    expectation = {
        "format": "world-expectation-v1",
        "lacks": "the loader's reader of a giving body in the law's form, the fast rest (#1287) on a box of 1000 x 160 x 3 (the clamp costs hours before it), the mode file by the generator (the packets' phase at v along x, the generator's one axis); "
        + FEED_FINDING,
        "row": row,
        "DETECTOR": pins,
        "GAMEBOARD": board,
        "GAMEBOARD_checks": [
            "(i) `light_rows` every 10 intervals: the record leaves the giver along +y alone (the tube folds the other three arms), reaches the front mirror and turns, returns to the moving giver's set; in motion its path in the GameBoard's frame is the diagonal",
            "(ii) `giver_centre`, `front_mirror_centre`: x_0 + v t within a Link, the y of each unchanged, the gap 56 kept",
            "(iii) `matter_total`: the packets' norm leak per Link below 3 x 10^-5; `light_total`: no record lost in the tube",
            "then the DETECTOR reading in kind: the moving clock slower than the resting one by gamma_u",
        ],
    }
    expectation["under_the_sum"] = (
        under_a_load(56, MIRROR - WINDOW, rest_mean, "the giver against its front mirror")
        + "; "
        + CONTACT
    )
    write("light_clock", name, document, expectation)


def two_slits(name: str, universe: str, wavelength: int, wall: int, stock: int) -> None:
    """The two slits (g): the giver in a tube of mirrors at x = 10..16, the wall of 4 x 248 at x = 40..43 with the openings at y = 118..121 and 134..137 (d = 16 between their centres), the screen of 4 x 256 at x = 140..143 with 64 strips of 4 Nodes on its own face, L = 100."""
    openings = set(range(118, 122)) | set(range(134, 138))
    giver_nodes = box(14, 16, 126, 128, 0, 0)
    tube = box(10, 13, 126, 128, 0, 0) + box(10, 16, 123, 125, 0, 0) + box(10, 16, 129, 131, 0, 0)
    wall_nodes = [[x, y, 0] for x in range(40, 44) for y in range(256) if y not in openings]
    screen_nodes = box(140, 143, 0, 255, 0, 0)
    measured = [
        giver(giver_nodes, WINDOW, stock, weight=3),
        body(wall_nodes, wall),
        body(screen_nodes, WINDOW),
        body(tube, wall),
    ]
    detectors = [
        {"name": f"screen_{k:02d}", "positions": [[140, 4 * k + j, 0] for j in range(4)]}
        for k in range(64)
    ]
    readings = [
        reading("light_support", "support", 50, family="charge"),
        reading("behind_the_wall", "level", 10, family="charge", node=[60, 60, 0]),
        reading("behind_the_wall_high", "level", 10, family="charge", node=[60, 200, 0]),
        reading("at_left_opening", "level", 10, family="charge", node=[41, 119, 0]),
        reading("at_right_opening", "level", 10, family="charge", node=[41, 135, 0]),
        reading("screen_centre", "level", 10, family="charge", node=[139, 128, 0]),
        reading("light_rows", "rows", 100, family="charge"),
        reading("wall_centre", "centre", 500, body=1),
        reading("screen_centre_body", "centre", 500, body=2),
        reading("giver_centre", "centre", 500, body=0),
    ]
    spacing = wavelength * 100 / 16
    document = world(
        [160, 256, 1],
        {"x": "open", "y": "open", "z": "periodic"},
        6000,
        measured,
        detectors,
        readings,
        face_depth=8,
        universe=universe,
    )
    diagnostic = (
        " the lattice's own diagnostic beside the world of record at lambda 16 (rule 4): the strips 23 and 40 here against the continuum's 25 and 38 (approval 8), the anisotropy of the light cone at lambda 4 (approval 22)"
        if wavelength == 4
        else " the world of record (rule 4): the continuum's strips 25 and 38 (approval 8)"
    )
    expectation = {
        "format": "world-expectation-v1",
        "lacks": "the loader's reader of a giving body in the law's form, the set on a body's own Nodes (Nature24's loader follow-up (a): the strips are `positions` on the screen's face), the fast rest (#1287) on a box of 160 x 256 (hours before it), the mode file by the generator (the giver's norm, the clock by rule 6 against the clock key of the universe file named here); "
        + FEED_FINDING,
        "row": f"ALGEBRA.md #the-rows-against-nature (g) THE TWO SLITS at lambda_q = {wavelength} (the charge family's clock [{2 * STEPS // wavelength}, 1] on N = {STEPS}, 2 N q / p): the giver of 9 Nodes of {WINDOW} at x = 14..16, y = 126..128 in a tube of {wall} (rule 2 in two dimensions: the back and side arms folded into the one along +x), the wall of 4 x 248 Nodes of {wall} at x = 40..43 with two openings of 4 Nodes at y = 118..121 and 134..137 (d = 16), the screen of 4 x 256 Nodes of {WINDOW} at x = 140..143 (L = 100) carrying 64 strips of 4 Nodes on its face; the strips' shares cos^2 (pi d y / (lambda_q L)) under one opening's envelope, the bright strips lambda_q L / d = {spacing:.0f} Links apart;{diagnostic}; the stock {stock} (rule 4: hundreds); written before any run",
        "DETECTOR": [
            {
                "detector": "screen_32",
                "count": round(stock * 0.06),
                "band": round(2 * (stock * 0.06) ** 0.5),
                "row": "the central bright strip's share of the stock, the envelope's peak: the formula's number on this file's integers is the approver's (approval 8 on the world of record); placeholder from the cos^2 shares' normalisation over the envelope",
            },
        ],
        "GAMEBOARD": [
            {
                "body": 1,
                "interval": 3000,
                "centre": [41, 127, 0],
                "band": 1,
                "row": "the wall at rest within a Link (the recoil per click below a Link; the feed's pull the finding in `lacks`)",
            },
            {
                "body": 2,
                "interval": 3000,
                "centre": [141, 127, 0],
                "band": 1,
                "row": "the screen at rest within a Link",
            },
        ],
        "GAMEBOARD_checks": [
            "(i) `behind_the_wall` and `behind_the_wall_high` (x = 60, away from the openings) and `light_support`: 0 behind an opaque wall but at the two openings' cones; `at_left_opening`, `at_right_opening`: the record's level in the openings",
            "(ii) `light_rows` every 100 intervals: one record leaves the tube along +x, two parts pass the openings, spread and meet on the screen",
            "(iii) `giver_centre`, `wall_centre`, `screen_centre_body`: within a Link over the run",
            "then the DETECTOR reading in kind: bright and dark strips alternate, the spacing lambda_q L / d, one record at a time (Young's fringes)",
        ],
    }
    expectation["under_the_sum"] = (
        under_a_load(
            40 - 17,
            wall - WINDOW,
            130 / (0.5699 if wavelength == 16 else LIGHT_SPEED),
            "the giver against the wall",
        )
        + "; "
        + CONTACT
    )
    write("two_slits", name, document, expectation)


def bending(name: str, heavy: int | None, gap: int, ticks: int, stock: int) -> None:
    """The bending (b) on Cheshbon's line (#1325, 05:41Z and 05:43Z): the board 300 x 120 x 1 (z of extent 1, the [1, 1] rest Poisson's of the plane), the heavy body of 30 x 30 Nodes of `heavy` centred at (60, 60), the giver of 3 x 3 Nodes of 2,001 in a tube of mirrors along +x with the beam's axis `gap` + 1 Nodes above the body's face (b = `gap` free Links), the screen at x = 260 (L = 200 from the body's centre) carrying one strip per Node across its whole face; beside the beam two small matter clocks of 3 x 3 Nodes of 2,001, one in the well at the beam's level (mirrored below the body) and one far from it, and the light's level at a Node deep in the well and at one outside, every interval (the redshift's second reading, GAMEBOARD); `heavy` None lays the twin with no heavy body, the same beam, screen and clocks, so that the centroid's shift is the difference of two DETECTOR readings (tools/beam_centroid.py). Nothing here is run."""
    face, centre, side = 74, 60, 30  # the heavy body's top face, its centre, its side
    axis = face + gap + 1  # the beam's axis: `gap` free Nodes between the face and the beam
    clock_y = centre - (side // 2) - gap - 1  # the clock in the well, mirrored below the body
    giver_count, clock_count = 2001, 2001
    giver_nodes = box(14, 16, axis - 1, axis + 1, 0, 0)
    tube = (
        box(10, 13, axis - 1, axis + 1, 0, 0)
        + box(10, 16, axis - 4, axis - 2, 0, 0)
        + box(10, 16, axis + 2, axis + 4, 0, 0)
    )
    screen_x, height = 260, 120
    screen_nodes = box(screen_x, screen_x + 3, 0, height - 1, 0, 0)
    heavy_box = (centre - side // 2, centre + side // 2 - 1, centre - side // 2, face)  # 45..74
    measured = [
        giver(giver_nodes, giver_count, stock, weight=3),
        body(tube, MIRROR),
        body(screen_nodes, WINDOW),
        body(box(centre - 1, centre + 1, clock_y - 1, clock_y + 1, 0, 0), clock_count),
        body(box(199, 201, 19, 21, 0, 0), clock_count),
    ]
    if heavy is not None:
        measured.append(body(box(*heavy_box, 0, 0), heavy))
    detectors = [{"name": f"screen_{y:03d}", "positions": [[screen_x, y, 0]]} for y in range(height)]
    deep, outside = [centre, axis, 0], [200, axis, 0]
    readings = [
        reading("light_support", "support", 50, family="charge"),
        reading("light_rows", "rows", 100, family="charge"),
        reading("light_deep_in_the_well", "level", 1, family="charge", node=deep),
        reading("light_outside_the_well", "level", 1, family="charge", node=outside),
        reading("clock_in_the_well", "cycle", 1, body=3),
        reading("clock_far_away", "cycle", 1, body=4),
        *[
            reading(f"{what}_centre", "centre", 500, body=k)
            for k, what in enumerate(("giver", "tube", "screen", "clock_in_the_well", "clock_far_away"))
        ],
        *[
            reading(f"gravity_on_the_axis_{x}", "level", 500, family="gravity", node=[x, axis, 0])
            for x in (15, 40, 60, 80, 120, 200, 259)
        ],
    ]
    if heavy is not None:
        readings.append(reading("heavy_centre", "centre", 500, body=5))
        readings.append(reading("heavy_momentum", "momentum", 500, body=5))
    document = world(
        [300, height, 1],
        {"x": "open", "y": "open", "z": "periodic"},
        ticks,
        measured,
        detectors,
        readings,
        face_depth=8,
    )
    distance = screen_x - centre  # L: the body's centre to the screen's face
    last = (ticks - 1) - (ticks - 1) % 500  # the last interval the centre readings (every 500) reach
    expectation: dict[str, Any] = {
        "format": "world-expectation-v1",
        "row": (
            f"ALGEBRA.md #the-rows-against-nature (b) THE BENDING on the board 300 x {height} x 1 (z periodic of extent 1, "
            f"the [1, 1] rest Poisson's of the plane, c(r) = (3 S / 2 pi) ln(R / r)): the giver of 9 Nodes of {giver_count} "
            f"at x = 14..16 on the axis y = {axis} in a tube of {MIRROR} (the beam along +x), "
            + (
                f"the heavy body of {side} x {side} Nodes of {heavy} at x = {heavy_box[0]}..{heavy_box[1]}, "
                f"y = {heavy_box[2]}..{heavy_box[3]} (S = {side * side * heavy} / E_s; its face b = {gap} free Links "
                f"below the axis), "
                if heavy is not None
                else "no heavy body (the twin: the same beam, screen and clocks, the centroid's reference), "
            )
            + f"the screen of 4 x {height} Nodes of {WINDOW} at x = {screen_x}..{screen_x + 3} carrying {height} strips "
            f"of one Node on its face (L = {distance} Links from the body's centre); the centroid of the clicks over "
            f"the strips shifted toward the body against the twin; under the gravity divisor E_s = 100,000 "
            f"(Cheshbon's line and the fall's need; the Experimenters' number, #1352) the level on the axis beside "
            f"the body c_b = 71 (GAMEBOARD, the plane's rest), U_b = c_b / (2 Gamma) = 3.5 x 10^-3; three numbers "
            f"for one world (Cheshbon, 05:43Z): (a) the engine as it stands, the pace squared in the read "
            f"coefficient, theta = (d2 omega / dk_perp2)(d omega / dc) INT (dc / db) dy / v_g^2: 10.9 Links; "
            f"(b) the conformal pace: 3.9; (c) conformal with a locally Lorentzian band: 2.4, nature's 4 U_b "
            f"(the row as written: 4 U_b L = 2.8, the plane's logarithm its uncertainty); the engine must show (a) "
            f"on today's law, and the distance to (c) is the conformal pace's line; the band the rounding's 0.5 "
            f"Link plus the draw's (the beam's transverse spread at the screen over the root of the clicks, "
            f"Cheshbon's number pending); a beam that touches the body is reflected, not bent, so the record's "
            f"support stays off the body's Nodes; the tube and the body are mirrors for the light by the bound "
            f"charge's row (polarisation [1, 2] at the divisor 1, the universe of record after Bell's pull request); "
            f"written before any run"
        ),
        "DETECTOR": [],
        "WELL": {
            "rows": "light_rows",
            "levels": ["light_deep_in_the_well", "light_outside_the_well"],
            "clocks": ["clock_in_the_well", "clock_far_away"],
            "axis_y": axis,
            "windows": [[heavy_box[0], heavy_box[1]], [185, 214]],
            "row": "tools/well_clocks.py reads these (GAMEBOARD): the light's wavelength along the axis beside the body and far from it, its period at the two Nodes (conserved: the ratio 1), the matter clocks' mean cycles in the well and far away; in the twin every ratio is 1",
        },
        "CENTROID": {
            "strips": "screen_",
            "twin": "bending_twin",
            "shift": -10.9,
            "band": 0.5,
            "nature": -2.4,
            "row_as_written": -2.8,
            "row": "the centroid of the strips' clicks (y in Nodes, exact fraction) minus the twin's; the body lies at y below the axis, so a shift toward it is negative: the engine's own (a) -10.9 within 0.5 Link, the rounding's band, the draw's band to be added; nature's (c) -2.4 and the row's -2.8 beside it, never tuned to",
        },
        "GAMEBOARD": [
            {
                "body": 0,
                "interval": last,
                "centre": [15, axis, 0],
                "band": 1,
                "row": "the giver at rest within a Link",
            },
            {
                "body": 2,
                "interval": last,
                "centre": [screen_x + 1, height // 2 - 1, 0],
                "band": 1,
                "row": "the screen at rest within a Link",
            },
            {
                "body": 3,
                "interval": last,
                "centre": [centre, clock_y, 0],
                "band": 1,
                "row": "the clock in the well within a Link (its fall by the wave's law over the run below a Link)",
            },
        ],
        "GAMEBOARD_checks": [
            f"(i) `gravity_on_the_axis_*` at interval 0: the plane's rest, c = 71 at x = {centre} beside the body under E_s = 100,000, falling as the logarithm away from it, 0 in the twin; no transient after the start",
            "(ii) `light_rows` every 100 intervals: one record leaves the tube along +x, passes the body without touching it, reaches the screen; `light_support` never on the heavy body's Nodes",
            f"(iii) the redshift's second reading (Cheshbon, 05:43Z): `light_deep_in_the_well` at ({centre}, {axis}) against `light_outside_the_well` at (200, {axis}), every interval: the record's rotation per interval is the giver's at both (Rule3 is time-invariant with static paces), so the light's shift shows in its wave number, read from `light_rows` along the axis near x = {centre} against near x = 200 (the wavelength in the well against outside: d omega / dc at fixed k is 2.8 / Gamma per level today, 1 / Gamma conformal); `clock_in_the_well` against `clock_far_away` (the matter clock, `cycle`): 0.64 / Gamma per level today, 1 / Gamma conformal, so the two shifts stand 4.4 apart today and coincide under the conformal pace; the twin's clock in the well equals the far one (the control)",
            "(iv) `giver_centre`, `tube_centre`, `screen_centre`, `heavy_centre`, the clocks' centres: within a Link over the run",
            "(v) light bending light (the source's row, a record sourcing gravity by D_i div T times omega_r / omega_m): a train of one quantum sources about 0.9 quanta over some 35 Nodes, c of order 10^-5 levels under E_s = 100,000, 0 in integers: not measurable, as in nature; the reciprocity stands in the books, not in a reading",
            "then the DETECTOR reading in kind: the strips' centroid on the axis in the twin and toward the body in the world of record, one record at a time",
        ],
    }
    if heavy is not None:
        expectation["GAMEBOARD"].append(
            {
                "body": 5,
                "interval": last,
                "centre": [centre - 1, centre - 1, 0],
                "band": 1,
                "row": "the heavy body at rest within a Link",
            }
        )
    write("bending", name, document, expectation)


def universe_of_record() -> None:
    """The universe file of record beside the worlds: the shipped rows with `divisor` inside every held row (the hold's write as a sum, the owner's word; the frame's `held` card takes the key since #1312, a key at the family's top level is refused); the numbers are the approvals'."""
    document = json.loads((ROOT / SHARED_UNIVERSE).read_text(encoding="utf-8"))
    for family in document["families"]:
        if "held" in family:
            family["held"]["divisor"] = DIVISOR[family["name"]]
    (ROOT / UNIVERSE).write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")


def universe_at(wavelength: int, path: Path) -> str:
    """The shared universe file with the charge family's clock at the wavelength (2 N q / p on N = 1024), written beside the world."""
    document = json.loads((ROOT / UNIVERSE).read_text(encoding="utf-8"))
    for family in document["families"]:
        if family["name"] == "charge":
            family["clock"] = [2 * STEPS // wavelength, 1]
    path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    return path.relative_to(ROOT).as_posix()


def main() -> None:
    universe_of_record()
    the_fall()
    light_clock_chain("light_clock_rest", Fraction(0), 4800)
    light_clock_chain("light_clock_longitudinal_moving", VELOCITY, 3600)
    light_clock_transverse("light_clock_transverse_rest", Fraction(0), 4800)
    light_clock_transverse("light_clock_transverse_moving", VELOCITY, 3600)
    (HERE / "two_slits").mkdir(exist_ok=True)
    two_slits(
        "two_slits_lambda_16",
        universe_at(16, HERE / "two_slits" / "universe_lambda_16.json"),
        16,
        9000,
        400,
    )
    two_slits("two_slits_lambda_4", UNIVERSE, 4, MIRROR, 400)
    (HERE / "bending").mkdir(exist_ok=True)
    bending("bending", 9000, 8, 5000, 400)
    bending("bending_twin", None, 8, 5000, 400)


if __name__ == "__main__":
    main()
