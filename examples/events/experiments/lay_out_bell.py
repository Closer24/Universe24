"""The six worlds of record of BELL (h), experiment 11 of the 24, laid out in the law's form on the owner's design (#1198, 22:00Z; docs/HIGHLIGHTS.md "Where a tensor enters"; #1315, the law's text at its head a866a87e): an emitter firing one arm at a crystal body, a slab of 3 x 3 x 1 Nodes in the tube's mouth (the key `crystal`, an empty object declaring nothing else; the row's one Node by default gives way to the cube where the one-Node equivalence fails, stated with its test: the generator's bound mode of a one-Node crystal at 2001 on [800, 1200] holds 3.4 percent of its form inside the Node and the slab 58 percent, the Experimenter's 04:40 Israel of 2026-09-28, Cheshbon's 01:23Z and the Closer's 04:28 Israel; on this plane of 241 x 60 x 1 the row's cube is the slab), whose taking click of the arriving record and giving click of one pair record of rank 2 (two identical labels, each a half quantum; its rotation the crystal's own, no key for the wavelength) send the pair from its Ports in opposite senses along x, a polariser at each end and two detectors, each clicking its own label alone by its own ladder at its own interval. BELL IN ONE SERIES (the owner's decision, 22:13Z): the four chains with fixed polariser angles (as Aspect 1981), the chain `bell_switching` with the angles switched in flight by each polariser's own clock (as Aspect 1982; the card of #1315: `angles`, two exact pairs, and `every`, the period in intervals), and the control `bell_switching_crystal_1000`, the same run with the crystal at another count: S must come out identical, else it is a bug of the engine. The owner's word of 22:35Z: the correlation lies in the amplitude of the pair record that spread from the crystal to both sides, nobody correlates at the click, each detector gives a click of its own label at its own time from the amplitude that reached it; so the output carries the two detectors' click times, and the tool coincidences.py pairs them by the pair record and within the window this file declares, reporting S twice. THE BLIND EXPECTATION is #1315's one form, taken from Mathematician B's text without the Experimenter's direction: E(a, b) = cos 2(a - b), each side's marginal one half at every setting, S = 2 sqrt 2 = 2.83 at the settings 0, pi / 4, pi / 8, 3 pi / 8; the Experimenter's own expectation against nature (Nature24 archived) is the same number, so a run that separates from 2.83 is a finding against the row and against nature alike. The runs on the owner's word when the crystal and the switching are on main. The board is a plane: the emitter of 3 x 3 Nodes at the bottom fires along +y inside a tube of mirrors up to the crystal (rule 2: one arm), the crystal's slab stands in the tube's mouth across the channel of three Nodes' height, the polarisers and the far bodies stand on the crystal's row along x at equal distances from the slab's faces (the two paths' delays equal, within the window, as (h) asks). The four chains differ in the two angle pairs alone: a = (1024, 0) and a2 = (1024, 424) (pi / 4), b = (1024, 204) (pi / 8) and b2 = (1024, 684) (3 pi / 8), the angle 2 atan(j / 1024). The counts follow the Boss's rules of record: the emitter, the crystal, the polarisers and the far bodies are windows at WINDOW quanta per Node, the tube's mirrors at MIRROR. Run from the repository root: python examples/events/experiments/lay_out_bell.py; it rewrites the six world files under bell/ and nothing else."""

from __future__ import annotations

import math
import sys
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from typing import Any

from lay_out_worlds import (  # noqa: E402
    FEED_FINDING,
    STEPS,
    body,
    box,
    giver,
    reading,
    world,
    write,
)

LAW_TEXT = "#1315 merged 22:54Z (its head 8a154951, the text of a866a87e unchanged)"
STOCK = 64  # the emitter's givings; the pairs are the crystal's clicks among them
GIVING_COUNT = 2001  # the count per Node of the emitter and of the crystal, the two givers: `least_residues` (500) needs the giver's shell wheel above it, W = 45,000 at 2001 where 2000 gives 45 and is refused (Cheshbon's 00:31Z; the Closer's 03:38 Israel); the polarisers and the plus bodies stay windows at WINDOW
CONTROL_COUNT = 1001  # the control's crystal (1000 gives the same W = 45)
ANGLES: dict[str, list[int]] = {
    "a": [1024, 0],
    "a2": [1024, 424],
    "b": [1024, 204],
    "b2": [1024, 684],
}  # the exact pairs of the base files, the angle 2 atan(j / 1024): 0, pi / 4, pi / 8, 3 pi / 8
NOMINAL: dict[str, float] = {
    "a": 0.0,
    "a2": 0.25,
    "b": 0.125,
    "b2": 0.375,
}  # the settings in turns of pi
CHAINS: tuple[tuple[str, str], ...] = (("a", "b"), ("a", "b2"), ("a2", "b"), ("a2", "b2"))
SWITCH_ANGLES: dict[str, tuple[str, str]] = {"left": ("a", "a2"), "right": ("b", "b2")}
SWITCH_PERIOD: dict[str, int] = {
    "left": 7,
    "right": 11,
}  # the switching chain: each polariser alternates its two settings every so many intervals by its own clock; the periods coprime and both far below the flight of 58 Links at 0.447 (about 130 intervals), so one flight sees many switches
CRYSTAL = [120, 40, 0]  # the centre Node of the crystal's slab (its `level` reading and its centre)
CRYSTAL_SLAB = (
    119,
    121,
    39,
    41,
)  # the slab of 3 x 3 x 1 Nodes in the tube's mouth, across the channel of three Nodes' height (y = 39..41), the pair leaving its faces at x = 119 and 121
ROW = 40  # the y of the crystal's row, where the polarisers and the far bodies stand
CHANNEL_MIRROR = 4000  # every wall of Bell (the channel's walls, the tube's two blocks, the back mirror) at the mirror line and a margin (the Closer's 09:33 Israel, one G = 100,000 for the universe of record): a wall of four Nodes is a mirror for a wavelength above that wavelength's line Gamma (1 - sin(pi / lambda)) (3,402 at the pump's lambda 4.36, 3,133 at the pair's 4.15 on the files of 08:21 Israel); at 9,000 the walls' gravity tent pulled the bodies (4 levels per Link at the emitter at the divisor 40,000), at 4,000 the tent is 2.2 times lower; the levels at the load and the lines on this head's files are in the expectations
ANALYSER = 2000  # the polarisers and the plus bodies: a window for the pair on the files of this head (Cheshbon's 05:33Z: the level inside about 1,800, below the pair's line 3,133 at lambda 4.15 and the pump's 3,402 at 4.36; 4,500 was a mirror for both), so the pair reaches the detectors; the pump passing beside the crystal reaches them too and stands in the books as labels taken by a body that is no detector; the count that is a mirror for the pump and a window for the pair (between the two lines) is the crystal's design (its count against the pump's rotation in this cavity), set from the generator's table after the generator of the clean form
WALL_GAP = 5  # Nodes between every window body and a wall (Cheshbon's 04:22Z and 04:28Z): the bound charge's well of a wall decays 0.127 per Link at [1, 2], 1,029 at the Node beside a wall of 9,000 and 0 in integers six Links away, so a window one Node from a wall falls into it (the feed reads the tail's slope: the emitter's momentum -66,712 per interval at two Links) and five Nodes away feels no force
WINDOW_GAP = (
    4  # Nodes between two window bodies: the tail of a body of 4,500 is 0 in integers five Links away
)
TUBE = (
    119 - WALL_GAP - 4,
    119 - WALL_GAP - 1,
    121 + WALL_GAP + 1,
    121 + WALL_GAP + 4,
)  # the tube's two walls, x = 110..113 and 127..130, five Nodes from the emitter's columns, each the inner column range of one block with the channel's bottom wall on its side (walls()); the mouth 114..126
BACK_MIRROR = box(
    TUBE[0] - WALL_GAP, TUBE[3] + WALL_GAP, 12 - WALL_GAP - 4, 12 - WALL_GAP - 1, 0, 0
)  # the emitter's back mirror, a box across x = 105..135 at y = 3..6: five Nodes below the emitter's bottom row and below the tube's blocks, five Nodes beyond each block on x (Cheshbon's 05:01Z: bodies are boxes alone; the gap between the mirror and the blocks is a labyrinth of five Nodes, a bounded geometric loss of the pump to the face)
CHANNEL = (
    CRYSTAL_SLAB[2] - WALL_GAP - 3 - 4,
    CRYSTAL_SLAB[2] - WALL_GAP - 3 - 1,
    CRYSTAL_SLAB[3] + WALL_GAP + 3 + 1,
    CRYSTAL_SLAB[3] + WALL_GAP + 3 + 4,
)  # the channel's bottom wall y = 27..30 and top wall y = 50..53: the crystal's rows 39..41 eight Nodes from each, the polarisers' 19 rows (y = 31..49) five from each
CHANNEL_ROWS = (
    CHANNEL[1] + 1,
    CHANNEL[2] - 1,
)  # y = 31..49, the channel's height between the walls; the polarisers and the plus bodies span it
CHANNEL_X = (
    60 + 3 + WALL_GAP,
    180 - 3 - WALL_GAP,
)  # the channel's walls run x = 68..172: five Nodes from the polarisers' near columns at 62 and 178
ARMS = {
    "left": CRYSTAL_SLAB[0] - 62,
    "right": 178 - CRYSTAL_SLAB[1],
}  # Links from the slab's faces to each polariser's near face: equal (57 and 57), so the two labels' delays are equal

COINCIDENCE_WINDOW = 24  # intervals: a left click and a right click within it are one pair (the owner's 22:26Z, as Aspect's window); the tool coincidences.py reads it here; (h) asks the giving's period above it and the two paths' delays within it; MathB's 23:36Z (EXPLORATORY): the arrival's spread by dispersion over 58 Links about 8 to 10 intervals, the giving's period about 50 to 60, so a window of 16 to 32; the plus set stands on the polariser's far face so its click follows the minus set's by about 5 intervals (3 Links at the pair's group velocity 0.55), not 75 as with the far cubes of the first layout
SETTINGS = {
    "left": {"a": ANGLES["a"], "a2": ANGLES["a2"]},
    "right": {"b": ANGLES["b"], "b2": ANGLES["b2"]},
}


def radians(pair: list[int]) -> float:
    """The polariser's angle from its pair (1024, j): 2 atan(j / 1024)."""
    return 2 * math.atan2(pair[1], pair[0])


def correlation(left: float, right: float) -> float:
    """The row (h) as #1315 writes it, the blind expectation: E(a, b) = cos 2(a - b) over all pairs, from the labels' clicks (the first click takes a row of R(-a) at one half each, the second's shares cos^2 (a - b) and sin^2 (a - b))."""
    return math.cos(2 * (left - right))


def nature(left: float, right: float) -> float:
    """Nature's correlation for a maximally entangled pair, cos 2(a - b): the Experimenter's expectation against nature, the same function as the row's."""
    return math.cos(2 * (left - right))


def marginal(pairs: int) -> int:
    """Each side's far-set (plus) clicks over the pairs: one half at every setting (no signalling), the row (h)."""
    return round(pairs / 2)


def s_value(of: Callable[[float, float], float] = correlation) -> float:
    """S = E(a, b) - E(a, b2) + E(a2, b) + E(a2, b2) on the four chains' exact angles: 2 sqrt 2 = 2.8284 for the row and for nature alike."""
    e = {(left, right): of(radians(ANGLES[left]), radians(ANGLES[right])) for left, right in CHAINS}
    return e[("a", "b")] - e[("a", "b2")] + e[("a2", "b")] + e[("a2", "b2")]


def blind_expectation() -> dict[str, Any]:
    """#1315's one form of the row (h), the blind expectation without the Experimenter's direction: E per cell on the exact pairs, the marginals one half, S = 2 sqrt 2; the run says."""
    cells = {
        f"{one}_{other}": round(correlation(radians(ANGLES[one]), radians(ANGLES[other])), 4)
        for one, other in CHAINS
    }
    return {
        "E": cells,
        "marginal": "one half at each side at every setting",
        "S": round(s_value(), 4),
        "share_inside": {
            "test": "the one-Node equivalence of the crystal's row (ALGEBRA.md, the crystal: one Node by default, a cube where the equivalence fails, stated with its test): the share of the crystal's bound mode inside its own Nodes, the mode file's `share_inside` of the crystal body (the generator's reading of the mode's form at the count in the world's own well), the slab standing where the one Node fails to hold its quanta",
            "one_node_at_2001_in_the_world": 0.034,  # read in the clamp's well of 04:40 Israel, not recomputed
            "slab_3x3x1_at_2001_in_the_world": 0.499,
            "slab_3x3x1_at_1001_in_the_world_the_control": 0.150,
            "slab_3x3x1_at_2001_closed_box_alone": 0.58,
            "read": "the world's numbers from the mode files of 2026-09-28 07:33 Israel, the generator's on the start folder's rest of the three held rows of the universe of record (gravity and the free charge the sum at 40,000, at most 81 on the board; the bound charge `polarisation` [1, 2] at the divisor 1, the well of every body's own count, one Node of gap between every window body and a wall: the emitter's 3 x 3 at 2001 holds 0.499 in the same well and stands at 1,583 to 1,892, the crystal the same, below the pump's window line 2,929; the polarisers and the plus bodies of 4,500 stand at 3,567 to 4,371, above the pump's line 2,929 and below the pair's line 6,388 (mirrors for the pump, windows for the pair); the channel's walls of 9,000 hold 7,144 to 8,948, above the pair's mirror line 6,388, the tube's walls of 8,000 6,339 to 7,654, the tube's interior 0, gravity at most 56; every window body five Nodes from every wall and four from the next window body, so no body is pulled); the mode files carry entries for the givers alone (the emitter and the crystal; a wall, a polariser and a far body load as content alone, Cheshbon's 03:35Z), the polarisers' 0.742 and the walls' 0.945 to 0.979 read at the generation of 06:25 Israel that computed every body; the closed box alone (EXPLORATORY, [800, 1200], Gamma 10^4) 0.58, the Experimenter's 04:40 Israel; Cheshbon's 01:23Z: on this plane the row's cube is the slab; the Closer's 04:28 Israel: approved by the law; a share read at a run against these is a finding on the crystal's row",
        },
        "mathb_23_36Z": {
            "sd_of_S_by_pairs_per_cell": {"64": 0.177, "256": 0.088, "1024": 0.044},
            "same_outcome_counts_at_64": "54.6 +- 2.8 in the three positive cells, 9.4 +- 2.8 in a_b2; the marginals 32 +- 4",
            "pairs_per_giving": "Cheshbon's 01:23Z on the slab: the block across the whole channel takes nearly every pump quantum, so the pairs per pump quantum are at least 0.9, not about one half; the stock 64 gives about 60 pairs per chain, and 256 and 1024 coincidences per cell need the stock about 280 and 1100; the two crystal counts give the same S, E, marginals and yield within the spread, a difference a finding against the crystal's row",
            "pair_in_flight": "the pair's rotation is the crystal's own (the law's crystal row: the conservation fixes the sum of the labels' rotations, the crystal the division; half the pump's only in the symmetric case), read from the crystal's clock in the mode file, and its wavelength the band's at that rotation: on the mode files of 07:33 Israel the crystal's 0.6266 gives lambda 5.58 and the emitter's 0.6727 the pump's 5.16 (Cheshbon's 04:47Z, correcting 8.5 written from the crystal's clock as if half the pump's); the group velocity about 0.55, the flight of 57 Links about 105 intervals on both sides",
        },
        "row": f"{LAW_TEXT}: one form, the local law with the click's one non-local act alone (one label ends everywhere at once, the other goes on as the taken row); the owner's 22:35Z: the correlation lies in the pair record's amplitude spread to both sides and each detector clicks alone from the amplitude that reached it; no cell tuned; S reported twice, by the pair record and within the coincidence window; the joint-click form and the |S| <= 2 local form of the earlier text are deleted from the law",
    }


def window_conditions() -> dict[str, Any]:
    """The two conditions (h) puts on the host's window for the same number within it: every pair's two clicks inside the window (the paths' delays within it) and no other pair's (the giving's period above it)."""
    return {
        "arms": ARMS,
        "delay_difference": abs(ARMS["left"] - ARMS["right"]),
        "window": COINCIDENCE_WINDOW,
        "row": f"the two labels leave the crystal's Node in the same interval and fly {ARMS['left']} and {ARMS['right']} Links to the polarisers' near faces (about 105 intervals at the pair's group velocity 0.55, MathB's 23:36Z, EXPLORATORY), so their delays differ by {abs(ARMS['left'] - ARMS['right'])} intervals; the plus set on the polariser's far face clicks about 5 intervals after the minus set (3 Links); the arrival's spread by dispersion about 8 to 10 intervals; all within the window of {COINCIDENCE_WINDOW}; the giving's period: the emitter's mode period in the mode file is 8 (the clock [6662300, 4803839], the tube five Nodes wider on each side than the emitter) and the loop gives at a fraction of the whole period (the wait at or above (2 u + 1) P / (2 V), u read at every click), so a giving every 8 intervals or less, about 5 on average, 4 to 5 pairs in flight within the window of 24 over the flight of 105 (Cheshbon's 02:05Z, correcting his 23:36Z); so S by the pair record stands at 2.8284 whatever the rate, and S within the window is diluted, E_window = E x p with p the share of the right pairings, the lost or crossed pairs random pairings at E = 0 in their share, p toward 1 with the pairing by the clicks' order on both sides (equal flights, the givings' order kept) up to the losses; where a pair's clicks fall outside the window or two pairs' inside it, the lost or crossed pairs read as random pairings at E = 0 in their share, so S within the window falls below S by the pair record by that share",
    }


UNDER_THE_SUM = (
    "under the sum with the bound charge (the owner's word of 06:00, 06:12 and 06:33 Israel, Cheshbon's 03:12Z): "
    "gravity and the free charge are the sum at 40,000 (the field between the bodies at most 56), and the bound "
    "charge `polarisation` [1, 2] at the divisor 1 is the well of every body's own count; five Nodes between "
    "every window body and a wall and four between window bodies (Cheshbon's 04:22Z and 04:28Z: the wall's well "
    "decays 0.127 per Link and pulls a body two Links away onto it; at six Links its tail is 0 in integers), so at "
    "the load (the files of 08:21 Israel, four boxes of walls) the emitter and the crystal hold 1,583 to 1,892; the "
    "polarisers and the plus bodies of 2,000 hold 1,585 to 1,943; the channel's top wall of 9,000 7,144 to 8,855 and "
    "the two blocks 7,145 to 9,000, the back mirror of 8,000 6,350 to 7,871; gravity at most 133; the tail beside a "
    "wall 1,015, 0 in integers at the bodies five Nodes away; the wavelengths from the mode files' clocks by the "
    "band (cos k = 6 cos omega - 2 for the light [1, 2], cos omega = clock[0] / (4 clock[1])): the emitter's "
    "[6819814, 4803839] gives the pump lambda 4.36 and the crystal's [6585916, 4803839] the pair 4.15 (the "
    "control's crystal of 1001, [7600500, 4803839], 5.29), and a wall of four Nodes is a mirror above the line "
    "Gamma (1 - sin(pi / lambda)): 3,402 for the pump, 3,133 for the pair (4,403 for the control's pair), so the "
    "polarisers of 2,000 are windows for both on these files (4,500 was a mirror for both; Cheshbon's 04:47Z read 5.16 "
    "and 5.58 on the files of 07:33 Israel, lines 4,284 and 4,662): the crystal's count against the pump's rotation "
    "is the design that puts the polarisers between the two lines, set with the generator of the clean form; the "
    "mode files are the generator's on that rest, entries for the emitter and the crystal alone, the profile at an "
    "eighth of the unit and the two levels of the standing mode; nothing of Bell reads a held level (the polariser "
    "and the ladder alone)"
)
NATURE = (
    "against nature (the Experimenter's expectation, Nature24 archived): for a maximally entangled pair nature "
    "gives E(a, b) = cos 2(a - b) at every pair of settings and marginals of one half at each detector whatever "
    "the setting; at the settings 0, pi / 4 and pi / 8, 3 pi / 8 the CHSH sum is S = 2 sqrt 2 = 2.8284, and Aspect's "
    "1982 experiment with the settings switched in flight read S = 2.697 +- 0.015 (the detectors' efficiency "
    "lowering it below 2.83, above 2 by 46 sigma); the law's row (h) at #1315 gives the same E, the same marginals "
    "and the same S, so nature and the row are not separated by this experiment: a run at 64 pairs reads S within "
    "0.42 of 2.83 (two sigma) for both, and S at or below 2 (two sigma below 2.83 at 64 pairs) is a finding "
    "against the row and against nature alike, S within the window below S by the pair record by more than the "
    "lost pairs' share a finding on the window's conditions"
)
RUNTIME = (
    "EXPLORATORY, one load of bell_a_b's stripped copy on this machine (Python 3.14, no interval): the parse "
    "0.13 s, the build 0.01 s, the board 14460 Nodes; the interval's cost from the probes of this session about "
    "0.01 s on a board of this size, so 4000 intervals about 40 s and a chain at 1024 pairs (the emitter's stock "
    "over the crystal's share, about 12,000 intervals) about 2 min"
)


def band_of_s(pairs: int) -> float:
    """S's two-sigma band from the draw's binomial band on each chain's E at the row's shares: sigma_E = 2 sqrt(p (1 - p) / n) with p the same-outcome share, summed in quadrature over the four chains."""
    shares = [
        (1 + correlation(radians(ANGLES[left]), radians(ANGLES[right]))) / 2 for left, right in CHAINS
    ]
    return 2 * math.sqrt(sum((2 * math.sqrt(p * (1 - p) / pairs)) ** 2 for p in shares))


def convergence() -> str:
    bands = ", ".join(f"{pairs} pairs: S within {band_of_s(pairs):.2f}" for pairs in (64, 256, 1024))
    return (
        "the runs in order, no pin before the GAMEBOARD section is read: (1) one chain at the stock 64, the "
        "GAMEBOARD checks alone (the emitter's one arm up the tube, the crystal's two clicks and the pair leaving its "
        "Ports along -x and +x, the pair turned at the polarisers, the own set before the far one, the centres); "
        "(2) the four chains at 64, 256 and 1024 PAIRS (the crystal's giving clicks; the emitter's stock is the pairs "
        "over the crystal's share of the arriving record, the approver's number, read on the first run and set "
        f"in the files), S with its two-sigma band from the draw's binomial band on each E: {bands}; the row's "
        "2.83 read at 64 pairs against the bound 2, E within 0.02 at 1024; (3) the pair's rotation read "
        "from the crystal's giving line (rule 5) before any S is compared; the switching chain (`bell_switching`, the angles "
        "switched in flight) in the same series, its pairs four times a chain's for the same band since each pair "
        "lands in one of the four cells, and its control at the crystal's other count with S identical; S counted twice "
        "on every run, by the pair record and within the window; the runtime per chain: the load of one "
        "chain measured in `runtime` below, the intervals the probes' 0.01 s each on this board (EXPLORATORY)"
    )


def walls() -> list[dict[str, Any]]:
    """The mirrors of the channel and the tube (rule 1: above the mirror line, four Nodes thick, nothing tunnels), four boxes and nothing else (Cheshbon's 05:01Z: a box's own well pulls it nowhere; a U's inner face reads its own tail through the feed and the body flies; two touching bodies pull each other whatever their counts): the channel's top wall (y = 50..53, at CHANNEL_MIRROR) along the crystal's row between the polarisers; on each side one block from the tube's wall up through the channel's bottom wall (x = 68..113 and 127..172, y = 12..30, at CHANNEL_MIRROR), the tube's mouth x = 114..126 open between them; the back mirror across x = 105..135 at y = 3..6 (at MIRROR), five Nodes below the blocks and the emitter; every wall five Nodes from every window body (WALL_GAP), so the bound charge's well of a wall pulls no body; the pump that passes beside the crystal goes on to the polarisers (ANALYSER); the channel guides the pair to the polarisers instead of the open faces (the owner's 23:08Z: the photons that wander)."""
    bottom = BACK_MIRROR[-1][1] + WALL_GAP + 1  # y = 12, the blocks' lowest row, five above the mirror
    return [
        body(box(CHANNEL_X[0], CHANNEL_X[1], CHANNEL[2], CHANNEL[3], 0, 0), CHANNEL_MIRROR),
        body(box(CHANNEL_X[0], TUBE[1], bottom, CHANNEL[1], 0, 0), CHANNEL_MIRROR),
        body(box(TUBE[2], CHANNEL_X[1], bottom, CHANNEL[1], 0, 0), CHANNEL_MIRROR),
        body(BACK_MIRROR, CHANNEL_MIRROR),
    ]


def bell(left: str, right: str) -> None:
    """One chain of BELL at the settings named: the one-arm emitter in its tube, the crystal's slab in the tube's mouth, the two polarisers and the two far bodies on the crystal's row."""
    emitter_nodes = box(119, 121, 12, 14, 0, 0)
    left_nodes = box(60, 62, CHANNEL_ROWS[0], CHANNEL_ROWS[1], 0, 0)
    right_nodes = box(178, 180, CHANNEL_ROWS[0], CHANNEL_ROWS[1], 0, 0)
    left_far = box(60 - WINDOW_GAP - 3, 60 - WINDOW_GAP - 1, CHANNEL_ROWS[0], CHANNEL_ROWS[1], 0, 0)
    right_far = box(180 + WINDOW_GAP + 1, 180 + WINDOW_GAP + 3, CHANNEL_ROWS[0], CHANNEL_ROWS[1], 0, 0)
    measured = [
        giver(emitter_nodes, GIVING_COUNT, STOCK),
        body(
            left_nodes,
            ANALYSER,
            polariser={"angle": list(ANGLES[left]), "sets": ["left_plus", "left_minus"]},
        ),
        body(
            right_nodes,
            ANALYSER,
            polariser={"angle": list(ANGLES[right]), "sets": ["right_plus", "right_minus"]},
        ),
        body(left_far, ANALYSER),
        body(right_far, ANALYSER),
        body(box(*CRYSTAL_SLAB, 0, 0), GIVING_COUNT, crystal={}),
        *walls(),
    ]
    detectors = [
        {"name": "left_minus", "block": 1},
        {"name": "right_minus", "block": 2},
        {"name": "left_plus", "block": 3},
        {"name": "right_plus", "block": 4},
    ]
    readings = [
        reading("light_rows", "rows", 20, family="charge"),
        reading("at_crystal", "level", 1, family="charge", node=list(CRYSTAL)),
        reading("at_left_polariser", "level", 10, family="charge", node=[61, ROW, 0]),
        reading("at_right_polariser", "level", 10, family="charge", node=[179, ROW, 0]),
        reading("emitter_centre", "centre", 1000, body=0),
        reading("crystal_centre", "centre", 1000, body=5),
        reading("records_alive", "alive", 100),
    ]
    theta_left, theta_right = radians(ANGLES[left]), radians(ANGLES[right])
    e = correlation(theta_left, theta_right)
    nominal = correlation(NOMINAL[left] * math.pi, NOMINAL[right] * math.pi)
    same, different = round((1 + e) / 2 * STOCK), round((1 - e) / 2 * STOCK)
    document = world(
        [241, 60, 1],
        {"x": "open", "y": "open", "z": "periodic"},
        4000,
        measured,
        detectors,
        readings,
        face_depth=8,
    )
    expectation = {
        "format": "world-expectation-v1",
        "lacks": f"the crystal ({LAW_TEXT}: a body of matter on one Node with the key `crystal`, declaring nothing else; its folder and the loop's hook none on main; the pair record of rank 2 with two identical labels of a half quantum each, its rotation the crystal's own, no key for the wavelength; the labels' clicks, one click line per label with the pair's record identity, where main writes one click per record), the polariser's loop hook (#1309), the charge family's `least_residues` in the universe file, the mode file by the generator (the norm, the clock by rule 6), the hold's line taking the universe of record's `divisor`; the crystal's share of the arriving record (the pairs per giving) is the approver's; "
        + FEED_FINDING,
        "row": f"ALGEBRA.md #the-rows-against-nature (h) BELL on the owner's design (22:00Z) and {LAW_TEXT}: the plane 241 x 60 x 1 open on x and y; the emitter of 3 x 3 Nodes of {GIVING_COUNT} at x = 119..121, y = 12..14 fires one arm along +y (its back mirror of {CHANNEL_MIRROR} a box across x = {BACK_MIRROR[0][0]}..{BACK_MIRROR[-1][0]} at y = 3..6, five Nodes below it; the tube's two walls the inner columns of two blocks of {CHANNEL_MIRROR}, x = {CHANNEL_X[0]}..{TUBE[1]} and {TUBE[2]}..{CHANNEL_X[1]} from y = 12 up through the channel's bottom wall y = {CHANNEL[1]}, five Nodes from its columns and from the mirror; bodies are boxes alone, Cheshbon's 05:01Z; the mouth x = 114..126 open, the pump beside the crystal on to the polarisers, windows for both wavelengths at {ANALYSER}: rule 2), the stock {STOCK} givings (N = {STEPS}, lambda_q = 4); the crystal a slab of 3 x 3 x 1 Nodes of {GIVING_COUNT} at x = {CRYSTAL_SLAB[0]}..{CRYSTAL_SLAB[1]}, y = {CRYSTAL_SLAB[2]}..{CRYSTAL_SLAB[3]} in the tube's mouth, across a channel of nineteen rows between the channel's walls of {CHANNEL_MIRROR} four Nodes thick (y = {CHANNEL[0]}..{CHANNEL[1]} and {CHANNEL[2]}..{CHANNEL[3]} for x = {CHANNEL_X[0]}..{CHANNEL_X[1]}, eight Nodes from the crystal's rows, the top wall its back mirror; the one-Node equivalence fails, `share_inside` below, so the row's cube stands here as the slab) takes the arriving record by its click and in the same interval gives one pair record (rank 2, two identical labels of a half quantum each) from its Ports along -x and +x (the angles fixed as Aspect 1981; the pair's rotation the crystal's own, no key; the switching chain and the crystal-count control beside these four in one series); the left polariser of 3 x 19 Nodes of {ANALYSER} at x = 60..62 and the right at 178..180 across the channel's rows y = {CHANNEL_ROWS[0]}..{CHANNEL_ROWS[1]} (mirrors for the pump, windows for the pair: the record enters; {ARMS['left']} Links each from the crystal), the settings {left} = {theta_left:.4f} and {right} = {theta_right:.4f} radians (the exact pairs {ANGLES[left]} and {ANGLES[right]}), each with its own set (minus) offered before its far set (plus) on the plus body of 3 x 19 Nodes of {ANALYSER} four Nodes beyond the polariser's far face at x = 53..55 and 185..187 (MathB's 23:36Z: the plus click about 5 intervals after the minus click of the same pair, within the window; the far cubes of the first layout put it 75 intervals later and emptied the window); each label clicks alone at its own detector at its own interval; the numbers of record: E({left}, {right}) = cos 2({left} - {right}) = {e:.4f} on the exact pairs (the nominal {nominal:.4f}), the marginals one half = {marginal(STOCK)} of {STOCK} pairs at each far set, S = {s_value():.4f} = 2 sqrt 2 over the four chains, the row's and nature's one number; S at or below 2 is a finding, no cell is tuned; S counted twice by coincidences.py, by the pair record and within the window of {COINCIDENCE_WINDOW} intervals; written before any run",
        "DETECTOR": [],  # no pin chosen: the blind expectation carries the numbers, the run decides
        "correlation": {
            "E": round(e, 4),
            "E_nominal": round(nominal, 4),
            "E_nature": round(nature(theta_left, theta_right), 4),
            "same": same,
            "different": different,
            "marginal": marginal(STOCK),
            "row": f"the pairs matched by the pair record's identity (the two labels' click lines carry it) and again within the window: the same outcomes at the two ends (both plus or both minus) (1 + E) / 2 x {STOCK} = {same}, the different outcomes (1 - E) / 2 x {STOCK} = {different}, E = (same - different) / pairs = {e:.4f} on this chain by the row (h); compared across the four chains as S = E(a,b) - E(a,b2) + E(a2,b) + E(a2,b2) = {s_value():.4f}; nature's cos 2(a - b) = {nature(theta_left, theta_right):.4f}, the same",
        },
        "GAMEBOARD": [
            {
                "body": 0,
                "interval": 1000,
                "centre": [120, 13, 0],
                "band": 1,
                "row": "the emitter at rest within a Link (the recoil per giving below a Link)",
            },
            {
                "body": 5,
                "interval": 1000,
                "centre": list(CRYSTAL),
                "band": 1,
                "row": "the crystal's slab in place",
            },
            {
                "body": 1,
                "interval": 1000,
                "centre": [61, ROW, 0],
                "band": 1,
                "row": "the left polariser at rest within a Link",
            },
            {
                "body": 2,
                "interval": 1000,
                "centre": [179, ROW, 0],
                "band": 1,
                "row": "the right polariser at rest within a Link",
            },
        ],
        "convergence": convergence(),
        "runtime": RUNTIME,
        "nature": NATURE,
        "coincidence_window": COINCIDENCE_WINDOW,
        "window_conditions": window_conditions(),
        "settings": SETTINGS,
        "blind_expectation": blind_expectation(),
        "GAMEBOARD_checks": [
            "(i) `light_rows` every 20 intervals: the emitter's one arm up the tube (nothing along -y or the sides beyond the mirrors), the record arriving at the crystal's Node; `at_crystal` every interval: the level rising at the crystal, its taking click and its giving click in one interval; then the pair leaving the crystal's Ports along -x and +x on the row y = 40, one record of rank 2",
            "(ii) `at_left_polariser` and `at_right_polariser` every 10 intervals: the pair's label turned back by the setting's angle at the polariser's Nodes, the own set (minus) offered before the far set (plus); a label passing untouched names the hook missing",
            "(iii) `emitter_centre`, `crystal_centre` and the polarisers' centres: within a Link over the run",
            "(iv) `records_alive` every 100 intervals: the emitter's record until the crystal's click, then the one pair record until its two clicks (rank 2, then rank 1 after the first label's click)",
            "then the DETECTOR reading in kind: the marginals one half at each side, E = cos 2(a - b) per chain, S = 2 sqrt 2 by the row; the same S within the window where every pair's two clicks fall inside it and no other pair's",
        ],
    }
    expectation["under_the_sum"] = UNDER_THE_SUM
    write("bell", f"bell_{left}_{right}", document, expectation)


def bell_switching(crystal_count: int = GIVING_COUNT, suffix: str = "") -> None:
    """The switching chain: the board of the fixed-angle chains with both polarisers switching their settings in flight by their own clocks (the owner's 22:10Z, as Aspect 1982; the card of #1315: `angles` and `every`): the left between a and a2 every 7 intervals, the right between b and b2 every 11; one world reads the four correlations, the setting of each click derived by the tool from the click's interval and the polariser's card (the angle read at the passage, never at the giving)."""
    emitter_nodes = box(119, 121, 12, 14, 0, 0)
    left_nodes = box(60, 62, CHANNEL_ROWS[0], CHANNEL_ROWS[1], 0, 0)
    right_nodes = box(178, 180, CHANNEL_ROWS[0], CHANNEL_ROWS[1], 0, 0)
    left_far = box(60 - WINDOW_GAP - 3, 60 - WINDOW_GAP - 1, CHANNEL_ROWS[0], CHANNEL_ROWS[1], 0, 0)
    right_far = box(180 + WINDOW_GAP + 1, 180 + WINDOW_GAP + 3, CHANNEL_ROWS[0], CHANNEL_ROWS[1], 0, 0)
    switching = {
        side: {"angles": [list(ANGLES[name]) for name in names], "every": SWITCH_PERIOD[side]}
        for side, names in SWITCH_ANGLES.items()
    }  # the card of #1315: two exact pairs and the period, by the body's own clock
    measured = [
        giver(emitter_nodes, GIVING_COUNT, 4 * STOCK),
        body(
            left_nodes,
            ANALYSER,
            polariser={**switching["left"], "sets": ["left_plus", "left_minus"]},
        ),
        body(
            right_nodes,
            ANALYSER,
            polariser={**switching["right"], "sets": ["right_plus", "right_minus"]},
        ),
        body(left_far, ANALYSER),
        body(right_far, ANALYSER),
        body(box(*CRYSTAL_SLAB, 0, 0), crystal_count, crystal={}),
        *walls(),
    ]
    detectors = [
        {"name": "left_minus", "block": 1},
        {"name": "right_minus", "block": 2},
        {"name": "left_plus", "block": 3},
        {"name": "right_plus", "block": 4},
    ]
    readings = [
        reading("light_rows", "rows", 20, family="charge"),
        reading("at_crystal", "level", 1, family="charge", node=list(CRYSTAL)),
        reading("emitter_centre", "centre", 1000, body=0),
        reading("crystal_centre", "centre", 1000, body=5),
        reading("records_alive", "alive", 100),
    ]
    cells = blind_expectation()["E"]
    document = world(
        [241, 60, 1],
        {"x": "open", "y": "open", "z": "periodic"},
        16000,
        measured,
        detectors,
        readings,
        face_depth=8,
    )
    expectation = {
        "format": "world-expectation-v1",
        "lacks": f"one series with the fixed-angle chains (the owner's 22:13Z); THE SWITCHING card of {LAW_TEXT} (`angles`, two exact pairs, and `every`, the period from 1, by the polariser's own clock; the angle read at the record's passage) is not in the engine (Main Loop's pull request, read when it opens); then everything the fixed-angle chains lack: the crystal's row, its key, its folder and hook, the labels' clicks, #1309, `least_residues`, the mode file, the hold's line for `divisor`; "
        + FEED_FINDING,
        "row": f"ALGEBRA.md #the-rows-against-nature (h) BELL, the switching chain (as Aspect 1982; {LAW_TEXT}; the crystal at {crystal_count} quanta, the pair's rotation the crystal's own, no key): the board of the fixed-angle chains with the left polariser switching between a = {radians(ANGLES['a']):.4f} and a2 = {radians(ANGLES['a2']):.4f} radians every {SWITCH_PERIOD['left']} intervals and the right between b = {radians(ANGLES['b']):.4f} and b2 = {radians(ANGLES['b2']):.4f} every {SWITCH_PERIOD['right']} intervals, both by their own clocks, the periods coprime and far below the label's flight of about 130 intervals, so the setting a label meets is fixed after the pair left the crystal (the locality loophole closed as in nature's experiment); the emitter's stock {4 * STOCK} givings for {STOCK} pairs per cell; each click's setting derived by the tool from its interval and the card, the four correlations read from one world: E per cell by the row {cells}, S = {s_value():.4f} = 2 sqrt 2, the row's and nature's one number; S counted twice, by the pair record and within the window of {COINCIDENCE_WINDOW}; written before any run",
        "DETECTOR": [],  # no pin chosen: the blind expectation carries the numbers, the run decides
        "correlation": {
            "cells": cells,
            "S": round(s_value(), 4),
            "S_nature": round(s_value(nature), 4),
            "marginal": marginal(4 * STOCK),
            "row": "each click's setting is the one its polariser held at the click's interval by its card (the tool's `setting_at`); the pairs sorted into the four cells by the two settings, E per cell = (same - different) / the cell's pairs, S over the four cells from one world, twice (by the pair record, within the window); the row (h)'s numbers",
        },
        "GAMEBOARD": [
            {
                "body": 0,
                "interval": 1000,
                "centre": [120, 13, 0],
                "band": 1,
                "row": "the emitter at rest within a Link",
            },
            {
                "body": 5,
                "interval": 1000,
                "centre": list(CRYSTAL),
                "band": 1,
                "row": "the crystal's slab in place",
            },
        ],
        "runtime": RUNTIME,
        "nature": NATURE,
        "coincidence_window": COINCIDENCE_WINDOW,
        "window_conditions": window_conditions(),
        "settings": SETTINGS,
        "blind_expectation": blind_expectation(),
        "convergence": "in the one series with the fixed-angle chains: 64 pairs per cell (the stock 256) for S within 0.42, then 256 per cell (1024) for 0.21, then 1024 per cell (4096) for 0.11; the settings' switching read in the output before any cell is filled; the control at the crystal's other count (bell_switching_crystal_1000 against bell_switching) must give S identical within the draw's band, else a bug of the engine; the runtime four times a fixed-angle chain's per band",
        "GAMEBOARD_checks": [
            "(i) `light_rows` and `at_crystal` as in the fixed-angle chains: the one arm up the tube, the crystal's two clicks, the pair along -x and +x",
            "(ii) the polarisers' settings switching every 7 and 11 intervals by their own clocks: the tool derives each click's setting from its interval and the card; a run whose four cells are not all filled names the switching missing",
            "(iii) the centres within a Link; (iv) `records_alive`: one pair record per crystal click",
            "then the DETECTOR reading in kind: the four cells' E from one world, S = 2 sqrt 2 by the row and by nature; the control's S identical",
        ],
    }
    expectation["under_the_sum"] = UNDER_THE_SUM
    write("bell", f"bell_switching{suffix}", document, expectation)


def main() -> None:
    for left, right in CHAINS:
        bell(left, right)
    bell_switching()
    bell_switching(crystal_count=CONTROL_COUNT, suffix="_crystal_1000")


if __name__ == "__main__":
    main()
