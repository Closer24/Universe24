"""The meeting's gates (ALGEBRA.md #the-click-is-the-meeting, the pair's form and the GHZ gate; HIGHLIGHTS.md, One test world and one gate): a record of several parts laid as one event and never summed at a Node, the NodeDetector's read of the parts' signed level sums (the parts line) and the joint-share reader pairing the parts across the sides (tools/bell_gate.py, the gate's arithmetic beside the engine's sides' draws): the exact algebra at Bell's four settings and at the GHZ patterns, the local credits as the fence, the determinism of equal parts, and the two gates' four worlds each (examples/events/bell, examples/events/ghz) end to end with the back-in-time gate MATCH; Bell and the GHZ are gates and never results. The click written on the lattice (src/event_universe/credit.py, features/click): the NodeDetector's draw inside the run and its write at one Node, the board exact between clicks."""

import json
import math
from fractions import Fraction

import numpy as np

from event_universe import resonance, take
from event_universe.emission import laid_by_count
from event_universe.lattice import Lattice
from event_universe.loader.draw import (
    pattern_of,
    patterns_of_the_law,
)
from event_universe.loader.node_detector_declaration import Transition
from event_universe.loader.universe import universe_of
from event_universe.loader.world import node_detectors_of
from event_universe.world_files import load_world
from tests.laws import (
    EVENTS,
    GATE,
    refused,
)
from tests.laws_content import (
    ONE_PHOTON,
    TWO_ATOMS,
    ZENO_1,
    ZENO_4,
    ZENO_ATOM,
    content_world,
    opened,
)

A, A2, B, B2 = ((1, 0), (1, 1), (12, 5), (5, 12))  # the CHSH settings as the declared bases (p, q)
ORDER, CHSH = ((A, B), (A, B2), (A2, B), (A2, B2)), (1, -1, 1, 1)  # CHSH's four worlds and S's signs
FENCE = {GATE.parts_shares: Fraction(238, 169), GATE.local_sums: Fraction(240, 169)}  # the local credits
P, Q, X, Y = (1, 0), (0, 1), (1, 0), (1, 1)  # a part reading p or q; the GHZ settings x, y (0, pi / 4)
PATTERNS = ((P, P, Q, Q), (P, Q, P, Q), (P, (0, -1), (0, -1), (-1, 0)))  # the GHZ patterns A, B, C
MERMIN = (((X, Y, Y), (Y, X, Y), (Y, Y, X), (X, X, X)), (1, 1, 1, -1))  # Mermin's four worlds and signs


def side(*parts: tuple[int, int]) -> dict[int, list[list[int]]]:
    return {interval: [list(part) for part in parts] for interval in range(1, 4)}


def credits(sides, order, patterns, form=GATE.joint):  # type: ignore[no-untyped-def]
    shares = [form(sides, [GATE.ports_of(*sp) for sp in zip(s, patterns, strict=True)]) for s in order]
    return shares, [GATE.correlation(found) for found in shares]


def test_the_ghz_gate_pairs_four_parts_on_three_sides_exactly(tmp_path):
    """(i) Equal parts on three sides read with the GHZ patterns A (p, p, q, q), B (p, q, p, q), C (p, -q, -q, -p): the eight shares are cos^2(a + b + c) / 4 at an even number of - ports and sin^2(a + b + c) / 4 at an odd, so at (x, y, y), (y, x, y) and (y, y, x) the even shares 0 and the odd 1 / 4 with E_3 = -1, at (x, x, x) the even 1 / 4 and the odd 0 with E_3 = 1, at ((12, 5), x, x) the even 36 / 169 and E_3 = 119 / 169; every single-side and every pairwise E 0 (the marginals 1 / 2); M = -4 (|M| = 4 beside local realism's 2); the three local credits give M = -1 each; the loader refuses by name a pattern of [0, 0], a pattern without a basis, a pattern of the wrong length against the records the world lays and a pattern in a world laying no record of several parts. The four shipped GHZ worlds (examples/events/ghz) are read under the one meeting in tests/test_the_one_meeting.py, one test each."""
    three = [side((3, 1), (3, 1), (3, 1), (3, 1))] * 3
    shares, found = credits(three, *MERMIN[:1], PATTERNS)
    for joint, settings in zip(shares, MERMIN[0], strict=True):
        total, even = sum(joint.values()), Fraction(settings == (X, X, X), 4)
        odd = Fraction(1, 4) - even
        assert all(joint[k] / total == (odd if k.count("minus") % 2 else even) for k in joint)
        assert not any(GATE.correlation(joint, c) for c in ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2)))
    assert found == [-1, -1, -1, 1] and GATE.combination(found, MERMIN[1]) == -4
    (joint,), (e_3,) = credits(three, ((B, X, X),), PATTERNS)
    assert e_3 == Fraction(119, 169) and joint[("plus",) * 3] / sum(joint.values()) == Fraction(36, 169)
    fenced = [GATE.combination(credits(three, MERMIN[0], PATTERNS, f)[1], MERMIN[1]) for f in FENCE]
    assert fenced == [-1] * len(FENCE)
    refused(r"\[0, 0\]", pattern_of, [[1, 0], [0, 0]], "node_detectors[0].pattern", (1, 0))
    row = {"name": "d", "positions": [[0, 0, 0], [1, 0, 0]], "pattern": [[1, 0]]}
    refused("none is declared", node_detectors_of, [row], (2, 1, 1), 0, (), ())
    families = universe_of(json.loads((EVENTS / "ghz.json").read_text(encoding="utf-8")))[1]
    refused("pattern of 3 parts", patterns_of_the_law, [("d", (P,) * 3)], [len(families) - 1], families)
    refused("no record of several parts", patterns_of_the_law, [("d", (P,) * 4)], [], families)


def test_the_resonant_two_mode_act_turns_by_the_planes_size_once_per_window(tmp_path):
    """The resonant two-mode act (ALGEBRA.md #what-is-open, item 50, the two-quadrature form; the mathematician's 223 (c) and 224 (2)(c), #1572 comments 5965727937 and 5966081562, the advisor's seconds, 5965918924 and 5966129376, two hands; src/event_universe/resonance.py and `meeting.turned_labels`): (i) the scale R is derived from the width's room, the file's amplitude bound and the record's window, the largest power of two with 2 (R A W)^2 inside the room, 2^12 at A = 9,266 and W = 48, 2^11 at W = 96 and 2^14 at W = 12, nothing declared; (ii) the two reference records advance by the emission's one recurrence (emission.advanced, through `gathered` at the level 0) and stay within 7 levels of R cos(Omega t) and R sin(Omega t) over 100 intervals at [2, 3]; (iii) a resonant arrival A cos(Omega t + phi) at A = 1,000 over W = 48 turns by A W / 2 within 2 percent at the phases 0, 0.7, pi / 2 and 2.5 (the hands' 23,724 to 24,289 against 24,000), where the magnitude form accumulated (2 / pi) A W at every frequency; (iv) the arrival at [1, 3]'s frequency against the pair [2, 3] turns by less than 2 percent of the resonant turn at W = 48 (sinc(delta W / 2) = 0.007 with the counter-rotating residue) and by sinc within 0.02 at W = 12 (0.30 against 0.31); (v) on the Zeno n = 4 world's declaration (`ZENO_4`, the world deleted 2026-10-20 at the ninth, inlined under the content of the born universe with its box opened along x as the content's sink): the body's window is the lay's passage derived at load, 21, and the declared window 12, Zeno's n, is refused by name with W = 21; the labels stand at their start through the window's first twenty intervals while the two sums gather, and at the twenty-first the sums are read once and begin again with the window (re-pinned 2026-10-20 under the content; eleven and the twelfth at the declared 12 before): the root once per window, the NodeDetector's act; (vi) the window's turn is applied as one hop by the phase line's pair at the window's angle with the carried division (`resonance.window_pair`, `resonance.hopped`, Part C), so the labels' angle at the Zeno world's n = 1 is 9,408 / 6,000 = 1.568 to the angle's rounding (tests/test_part_c2_window.py)."""
    omega, detuned, bound, room = math.acos(2 / 3), math.acos(1 / 3), 6949, 2**63 - 1
    assert [resonance.scale_of(room, bound, w) for w in (48, 96, 12)] == [2**12, 2**11, 2**14]
    scale, transitions = resonance.scale_of(room, bound, 48), (Transition(0, 1, 1, 1, (2, 3)),)
    references = resonance.references_of(scale, transitions)
    for t in range(1, 101):
        resonance.gathered(references, transitions, {1: 0})
        cosine, sine = references[0].cosine[0], references[0].sine[0]
        assert abs(cosine - scale * math.cos(omega * t)) <= 7 >= abs(sine - scale * math.sin(omega * t))

    def turn(frequency: float, phase: float, window: int) -> int:
        fresh = resonance.references_of(scale, transitions)
        for t in range(window):
            resonance.gathered(fresh, transitions, {1: round(1000 * math.cos(frequency * t + phase))})
        return resonance.window_turn(fresh[0], 1)

    phases = (0, 0.7, math.pi / 2, 2.5)
    assert all(abs(turn(omega, phi, 48) - 24000) <= 480 for phi in phases)  # A W / 2 at every phase
    assert all(turn(detuned, phi, 48) < 480 for phi in phases)  # sinc(delta W / 2), the residue
    sinc = abs(math.sin((detuned - omega) * 6) / ((detuned - omega) * 6))
    assert all(abs(turn(detuned, phi, 12) / 6000 - sinc) <= 0.02 for phi in phases)
    board = Lattice(
        load_world(content_world(tmp_path, "zeno_4", ZENO_4, ZENO_ATOM, opened))
    )  # the content, the box opened along x (2026-10-20)
    books = board.credit.bodies[0]
    window = (
        books.declared.draw.window
    )  # the lay's passage over the body, derived at load on the opened box

    def keyed(world):  # type: ignore[no-untyped-def]
        opened(world)
        world["bodies"][0]["node_detector"]["window"] = 12  # Zeno's n = 4 as the declared key

    assert window == 21  # re-pinned 2026-10-20 under the content; the declared 12 before
    refused("W = 21", load_world, content_world(tmp_path / "keyed", "zeno_4", ZENO_4, ZENO_ATOM, keyed))
    start, gathered = list(books.labels), books.references[0]
    for _ in range(window - 1):
        board.step()
        assert books.labels == start and (gathered.in_phase, gathered.quadrature) != (0, 0)
    board.step()
    assert (gathered.in_phase, gathered.quadrature) == (0, 0) and books.elapsed == 0
    hopped = resonance.hopped(10**6, 0, *resonance.window_pair(9408, 6000, board.amplitude))
    assert abs(math.atan2(hopped[1], hopped[0]) - 9408 / 6000) <= 1e-6  # the hop at the window's angle


def test_every_line_is_born_at_the_half_wall_and_a_lone_massless_quantum_stays_bounded(tmp_path):
    """The law's line of the start (the owner's word of 2026-10-03, #1572 comment 5968627499 (255); the mathematician's 254 with the advisor's 5968491596, two hands): every Node's remainder is born at the half wall, the vacuum (0, 0, w div 2), the lay's origin and the start's alike, so that the one rounding of Rule3 is half up at every Node and no neighbour reads a floor. A Node holding no level and the half wall steps to itself exactly; and one massless quantum laid whole by the count at one Node of the shipped Zeno box, 8 by 8 by 5 periodic on all three axes (one odd extent; the uniform mode is a double root of the rule on any periodic board), stays bounded: the lattice's half-up rule reads the largest level 50 at the interval 200, printed from the run (on the former 8 by 8 by 4 box it read 172, the reals 242 and the floor grew as t^2 to 6,268, Worker PULSE's 5968413761)."""
    world = json.loads(
        json.dumps(ZENO_1)
    )  # the deleted zeno_1's box, inlined: no body, no content, no sink needed
    world.update(bodies=[], packets=[], node_detectors=[], intervals=200)
    path = tmp_path / "box.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    board = Lattice(load_world(path))
    pulse = next(index for index, family in enumerate(board.families) if family.name == "pulse")
    half = board.half_wall(pulse)
    assert half > 0 and all(
        (line.remainder == board.half_wall(index)).all()
        for index in board.order
        for line in board.states[index].lines
    )
    board.step()
    line = board.states[pulse].lines[0]
    assert not line.now.any() and not line.before.any() and (line.remainder == half).all()
    laid_by_count(board, take.Item(pulse, None, None, 1, ((4, 4, 2),), pair=(6000, 6000)))
    for _ in range(200):
        board.step()
    largest = int(np.abs(board.states[pulse].lines[0].now).max())
    print(f"the lone quantum's largest level at the interval 200 on the box {board.shape}: {largest}")
    assert largest < 300, largest  # bounded: 50 by the lattice's rule on this box, 6,268 under the floor


def test_the_absorption_removes_the_photon_and_the_front_leaves_the_board_dark(tmp_path):
    """The committed one-photon world at the lay without the uniform mode (ALGEBRA.md, The click writes on the lattice (3) and (6)): one atom takes at its window's close (the taking atom's close, 60 under the derived window of 2026-10-23, 63 at the declared window re-pinned 2026-10-20; which takes is the taking atom's read of the board) and the count falls to 0; the light's share over the lattice never rises above the lay's by more than the hole's and the front's transient (one part in seven, the known one), and once the front has swept both packets the share is 0 exactly, the board dark."""
    board = Lattice(
        load_world(content_world(tmp_path, "one_photon", ONE_PHOTON, TWO_ATOMS)), (lines := []).append
    )  # the content, 2026-10-20
    photon, shares = [f.name for f in board.families].index("photon"), []
    laid = board.books()["photon"]["share"]
    for _ in range(262):  # dark by 237 at the latest (the click at 61 or 62, the front after it)
        board.step()
        shares.append(board.books()["photon"]["share"])
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    (taken,) = [c for c in credits if c["absorbed"]]  # one absorption, at the taking atom's close
    print(f"the photon taken at {taken['interval']} by {taken['node_detector']}, {taken['window']}")
    assert (
        taken["interval"] == 60 and taken["interval"] == taken["window"][1]
    )  # the derived window's close 60 (63 at the declared window, re-pinned 2026-10-20; the derived window of 2026-10-23)
    assert board.credit.counts[photon] == 0
    assert laid > 0 and max(shares) * 7 <= laid * 8 and shares[-1] == 0
    after = {x["event"] for x in lines if x["interval"] > taken["interval"]}
    assert after <= {"erasure", "face", "credit", "lay"}
