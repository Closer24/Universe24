"""The meeting's gates (ALGEBRA.md #the-click-is-the-meeting, the pair's form and the GHZ gate; HIGHLIGHTS.md, One experiment and one gate): a record of several parts laid as one event and never summed at a Node, the NodeDetector's read of the parts' signed level sums (the parts line) and the joint-share reader pairing the parts across the sides (tools/bell_gate.py, the gate's arithmetic beside the engine's sides' draws): the exact algebra at Bell's four settings and at the GHZ patterns, the local credits as the fence, the determinism of equal parts, and the two gates' four worlds each (examples/events/bell, examples/events/ghz) end to end with the back-in-time gate MATCH; Bell and the GHZ are gates and never results. The click written on the lattice (src/event_universe/credit.py, features/click): the NodeDetector's draw inside the run and its write at one Node, the board exact between clicks."""

import json
import math
from fractions import Fraction

import numpy as np

from event_universe import resonance, twist
from event_universe.emission import laid_by_count
from event_universe.lattice import Lattice
from event_universe.loader.draw import (
    basis_of,
    draw_of,
    pattern_of,
    patterns_of_the_law,
)
from event_universe.loader.node_detector_declaration import Transition
from event_universe.loader.universe import shape_of, universe_of
from event_universe.loader.world import node_detectors_of
from event_universe.world_files import load_world
from tests import laws
from tests.laws import (
    BACK,
    EVENTS,
    GATE,
    ROOT,
    TOOL,
    load_file,
    refused,
)
from tests.laws_content import (
    ONE_PHOTON,
    TWO_ATOMS,
    ZENO_1,
    ZENO_2,
    ZENO_4,
    ZENO_ATOM,
    content_world,
    opened,
)
from tests.laws_read import redeclared

BELL, GHZ = (load_file(f"{n}_build", EVENTS / n / "build_world.py") for n in ("bell", "ghz"))
PAIR = ((1, 0), (0, 1))  # the pair's pattern: the + port reads (p, q), the - port (-q, p)
A, A2, B, B2 = ((1, 0), (1, 1), (12, 5), (5, 12))  # the CHSH settings as the declared bases (p, q)
ORDER, CHSH = ((A, B), (A, B2), (A2, B), (A2, B2)), (1, -1, 1, 1)  # CHSH's four worlds and S's signs
MEETING = [Fraction(119, 169), Fraction(-119, 169), Fraction(120, 169), Fraction(120, 169)]
FENCE = {GATE.parts_shares: Fraction(238, 169), GATE.local_sums: Fraction(240, 169)}  # the local credits
UNEQUAL = (Fraction(363518, 128609), Fraction(66625, 128609), [760, 761])  # S, P(A+), rho at r = 19/20
P, Q, X, Y = (1, 0), (0, 1), (1, 0), (1, 1)  # a part reading p or q; the GHZ settings x, y (0, pi / 4)
PATTERNS = ((P, P, Q, Q), (P, Q, P, Q), (P, (0, -1), (0, -1), (-1, 0)))  # the GHZ patterns A, B, C
MERMIN = (((X, Y, Y), (Y, X, Y), (Y, Y, X), (X, X, X)), (1, 1, 1, -1))  # Mermin's four worlds and signs


def side(*parts: tuple[int, int]) -> dict[int, list[list[int]]]:
    return {interval: [list(part) for part in parts] for interval in range(1, 4)}


def credits(sides, order, patterns, form=GATE.joint):  # type: ignore[no-untyped-def]
    shares = [form(sides, [GATE.ports_of(*sp) for sp in zip(s, patterns, strict=True)]) for s in order]
    return shares, [GATE.correlation(found) for found in shares]


def test_the_one_meeting_reads_the_blind_at_the_sides_and_the_engine_implements_it_exactly(tmp_path):
    """(i) Equal parts on both sides over a window whose middle interval reports 0 (no 0 / 0 under the window rule): E = ((p p' + q q')^2 - (p q' - q p')^2) / ((p^2 + q^2) (p'^2 + q'^2)) at the four settings, S = 478 / 169 exactly and the marginal 1 / 2 whatever the partner's setting; the local credits on the same reports: by the parts' shares S = 238 / 169 (E = cos 2a cos 2b), by the local sums 240 / 169 (sin 2a sin 2b), by the sign 2 (the tie at (1, 0) reads 0, read with the worlds). (ii) What a formula reader fails: the parts (20, 19) against (1, 1), r = 19 / 20, give S = 363518 / 128609 (2.8265), the marginal 66625 / 128609 (0.518) at (12, 5) for both partner settings and rho = 760 / 761; parts (1, 0) give S = 238 / 169 (rho = 0); a setting of one coefficient and a pattern whose ports are not orthogonal are refused by name. (iii) The four worlds of examples/events/bell/design.json built with their mode files (the pair family at the dimension [2, 1]; the regions' bases the settings, their pattern the pair's) and run: the parts equal at every interval, the reader gives E = 119 / 169, -119 / 169, 120 / 169, 120 / 169, S = 478 / 169 and the marginals 1 / 2 exactly, the local credits 238 / 169, 240 / 169 and 2, the ratio and rho 1 and one pair drawn per world, the blind file carrying the same S before the run; a part raised one level at one Node is not equal after the run and reads the ratio off 1; the loader refuses by name a dimension shape of three numbers and a basis of zeros; the back-in-time gate says MATCH on each world over its run; the plane's reader (tools/spin_gate.py) loaded after the gate's leaves `GATE.one_world` as it was, and the perturbed world is read by it after the load (the finding of 2026-10-20: the module body rebound bell_gate.one_world to the plane's form at import, the singlet's builder importing it for `at_equal_parts` and the builders' test loading every builder in the process the gate's worlds are read in, and in the one worker that ran the builders' test first the perturbed world was refused by the Gram check where its mismatch is read, one failure in three full checks)."""
    a, b, equal = side((7, -3), (7, -3)), side((5, 11), (5, 11)), side((1, 1), (1, 1))
    a[2] = b[2] = [[0, 0], [0, 0]]
    shares, found = credits([a, b], ORDER, (PAIR, PAIR))
    assert found == MEETING and GATE.combination(found, CHSH) == Fraction(478, 169)
    assert [GATE.marginal(s) for s in shares] == [Fraction(1, 2)] * 4
    found = {f: GATE.combination(credits([a, b], ORDER, (PAIR, PAIR), f)[1], CHSH) for f in FENCE}
    assert found == FENCE
    unequal, mirrored = side((20, 20), (19, 19)), tuple((y, x) for x, y in ORDER)
    shares, found = credits([unequal, equal], mirrored, (PAIR, PAIR))
    assert GATE.combination(found, CHSH) == UNEQUAL[0]
    assert GATE.marginal(shares[0]) == GATE.marginal(shares[2]) == UNEQUAL[1]
    m = GATE.mismatch([unequal, equal], 2)
    assert (m["ratios"], m["rho"], m["label"]) == ([[19, 20]], UNEQUAL[2], "LATTICE")
    rho_zero = credits([side((1, 1), (0, 0)), b], ORDER, (PAIR, PAIR))[1]
    assert GATE.combination(rho_zero, CHSH) == FENCE[GATE.parts_shares]
    refused("setting", GATE.ports_of, (1,), PAIR), refused("orthogonal", GATE.ports_of, A, ((1, 1),))
    read, expected = laws.gate_worlds(BELL, tmp_path)
    assert [Fraction(*read["correlation"][k]) for k in expected["order"]] == MEETING
    assert (read["S_by_the_parts_shares"], read["S_by_the_local_sums"]) == ([238, 169], [240, 169])
    assert read["S_by_the_sign"] == [2, 1] == expected["blind"]["by_the_sign"]["S"]
    for world in read["worlds"].values():
        assert world["mismatch"]["ratios"] == [[1, 1]] and world["mismatch"]["rho"] == [1, 1]
        assert len(world["drawn"]) == 2 and all(q[0] > 0 for q in world["quanta"].values())
    path = tmp_path / f"{expected['runs'][expected['order'][0]]}.json"
    board = Lattice(load_world(path), (lines := []).append)
    board.states[-1].lines[1].now[board.shape[0] // 2, 0, 0] += 1  # the pair's one part a level off
    for _ in range(board.world.intervals):
        board.step()
    assert (board.states[-1].lines[0].now != board.states[-1].lines[1].now).any()
    before = GATE.one_world  # loaded after the gate's, as the singlet's builder imports it
    load_file("spin_gate", ROOT / "tools" / "spin_gate.py")
    assert GATE.one_world is before  # tools/spin_gate.py rebinds nothing at import
    assert GATE.one_world(path, lines, expected)["mismatch"]["ratios"] != [[1, 1]]
    refused(r"as a shape is \[parts, dimension\]", shape_of, {"dimension": [2, 1, 1]}, "families[0]")
    refused("not all 0", basis_of, [0, 0], "node_detectors[0].basis")


def test_the_ghz_gate_pairs_four_parts_on_three_sides_exactly(tmp_path):
    """(i) Equal parts on three sides read with the GHZ patterns A (p, p, q, q), B (p, q, p, q), C (p, -q, -q, -p): the eight shares are cos^2(a + b + c) / 4 at an even number of - ports and sin^2(a + b + c) / 4 at an odd, so at (x, y, y), (y, x, y) and (y, y, x) the even shares 0 and the odd 1 / 4 with E_3 = -1, at (x, x, x) the even 1 / 4 and the odd 0 with E_3 = 1, at ((12, 5), x, x) the even 36 / 169 and E_3 = 119 / 169; every single-side and every pairwise E 0 (the marginals 1 / 2); M = -4 (|M| = 4 beside local realism's 2); the three local credits give M = -1 each; the loader refuses by name a pattern of [0, 0], a pattern without a basis, a pattern of the wrong length against the records the world lays and a pattern in a world laying no record of several parts. (ii) The four worlds of examples/events/ghz/design.json (the GHZ family at the dimension [4, 1] on a square board, three beams to three regions) are built with the blind, laid and run two at a time in the next test."""
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


def ghz_gates_read(keys, tmp_path):  # type: ignore[no-untyped-def]
    (read, expected), f = laws.gate_worlds(GHZ, tmp_path, keys), GATE.fraction
    b, order, signs = expected["blind"], expected["order"], expected["combination"]["signs"]
    local = ("by_the_parts_shares", "by_the_local_sums", "by_the_sign")  # the three local credits
    for key, w in read.items():
        assert w["shares"] == b["shares"][key] and w["marginals"] == b["marginals"][key]
        assert (
            f(w["correlation"]) == f(b["correlation"][key]) and w["mismatch"]["ratios"] == [[1, 1]] * 3
        )
        assert w["sub_correlations"] == b["sub_correlations"][key] and len(w["drawn"]) == 3
        assert all(f(w[c]) == f(b[c]["correlation"][key]) for c in local)
    assert all(v == dict.fromkeys(("a b", "a c", "b c"), [0, 1]) for v in b["sub_correlations"].values())
    assert list(b["correlation"].values()) == [[-1, 1]] * 3 + [[1, 1]] and b["M"] == [-4, 1]
    assert GATE.combination((f(b["correlation"][k]) for k in order), signs) == -4
    found = [GATE.combination((f(b[c]["correlation"][k]) for k in order), signs) for c in local]
    assert found == [-1] * 3 == [f(b[c]["M"]) for c in local]


def test_the_ghz_gates_first_pair_x_y_y_and_y_x_y_reads_the_blind_exactly(tmp_path):
    """(ii) The GHZ folder built from its design and its first pair of worlds run, x y y and y x y (the clock gives each pair its own test; `laws.gate_worlds`): every world LAWFUL, its parts lines equal across the parts, its credit lines at the window's close, the back-in-time gate MATCH over 4 intervals; each world's eight shares, E_3, marginals, sub-correlations and the three local credits' correlations the blind's, one triple drawn per world, its mismatch ratios [1, 1] on every side; and the blind's four E_3 (-1 at x y y, y x y, y y x and +1 at x x x) combine to M = -4 by the gate's signs, |M| = 4 beside local realism's 2, where each local credit's combine to -1 (`ghz_gates_read`)."""
    ghz_gates_read(("x y y", "y x y"), tmp_path)


def test_the_ghz_gates_second_pair_y_y_x_and_x_x_x_reads_the_blind_exactly(tmp_path):
    """(ii) The second pair of the GHZ folder's worlds, y y x and x x x, run and read as the first (`ghz_gates_read`): with the first pair every world of the folder is run, none dropped."""
    ghz_gates_read(("y y x", "x x x"), tmp_path)


def test_the_click_is_written_at_one_node_and_the_board_is_exact_between_clicks(tmp_path):
    """The click written on the lattice (ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision of 2026-10-02; features/click, src/event_universe/credit.py): Bell's shipped world a b with the draw's window cut to 40 over its 100 intervals, beside its twin without the key. (i) At the first close, 40, the beams' share through each side stands below a whole quantum, so no side clicks (the side's gate, the reader's F4 of 2026-10-20, `lists.readings`); one credit line per side at 80: the result the window, the node_detector's proper time at the close (the board's intervals at the vacuum's clock p_0 = Gamma - c_vac, 79 at the declared rest 60) and the index of the window closed, 2, the region, the port realised, the parts kept and the count 1, the record's count down by one, no Node (the hole's Nodes in the face lines); after the click at 80 the two boards differ at the two written Nodes (the holes, the one-Node write of the count) and along the record the write at the birth rewrote, the part the first side zeroed standing at 0 everywhere and the held rows it sources moved with it (the click writes, the owner's word of 2026-10-20; the second side's write on the one surviving part the identity), and at the written Node every line of the record is 0 in its three arrays (the hole, as the receding face removes a share) where the twin's levels stand. (ii) The inverse is exact after the click down to it: from 100 back to 80 every array returns bit for bit (the holes crossed from the face lines); below 80 the inverse returns the realised past, which differs from the frames the forward run kept before the first close, the possibilities' run (the step back across the first click misses, as the law says); and the twin goes from 40 back to the lay, MATCH. (iii) The record's count: at 0 the draw credits nothing over the same 80 intervals, the reports the same lines but the click's (the credit lines and the write's lay lines at the birth); the `draw` key refused by name with a window of 0 and without its seed."""
    world = redeclared(json.loads((EVENTS / "bell" / "bell_a_b.json").read_text(encoding="utf-8")))
    world["draw"]["window"], draw = 40, dict(world["draw"])
    (cut := tmp_path / "cut.json").write_text(json.dumps(world), encoding="utf-8")
    world.pop("draw")
    (twin := tmp_path / "twin.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(cut)]), TOOL.main(["--input", str(twin)])
    board, plain = Lattice(load_world(cut), (lines := []).append), Lattice(load_world(twin))
    kept = {}
    for _ in range(100):
        board.step(), kept.__setitem__(board.interval, BACK.snapshot(board))
        board.interval <= 81 and plain.step()
    credits = [line for line in lines if line["event"] == "credit"]
    pair = next(i for i, f in enumerate(board.families) if f.name == "light_pair")
    at = [(c["interval"], c["node_detector"], c["count"], c["window"][0], c["left"]) for c in credits]
    left, clock = board.credit.counts[pair], board.world.node_clock - max(f.rest for f in board.families)
    assert at == [(80, "left", 1, 41, left), (80, "right", 1, 41, left)]  # nothing through at 40
    was, now = dict(p for f in kept[81] for p in f), dict(p for f in BACK.snapshot(plain) for p in f)
    proper = [(n * clock // board.world.node_clock, 2) for n in (80, 80)]
    assert [(c["proper"], c["windows"]) for c in credits] == proper  # p_0 = Gamma - c_vac: 79 at 60
    keys = "event label interval family node_detector window proper windows before realised kept"
    words = f"{keys} count left absorbed emitted momentum fan twist shortfall lost source recoil"
    report = set(f"{words} order scale board_count".split())  # Part F's, C3's, G's and the sides' words
    assert all(set(c) - {"bias_bound"} == report and c["label"] == "NODEDETECTOR" for c in credits)
    assert all(c["bias_bound"]["g"] < c["bias_bound"]["total"] for c in credits if "bias_bound" in c)
    holes = [f for f in lines if f["event"] == "face" and f["interval"] == 81]  # the hole's Nodes
    written = {tuple(np.add(f["node"]["at"], plain.offset)) for f in holes}
    differing = {
        tuple(map(int, a)) for k in was for a in np.argwhere(was[k] != now[k])
    }  # the holes, the write
    assert written <= differing and any(not was[f"light_pair.lines[{k}].now"].any() for k in range(2))
    w, keys = sorted(written)[0], [k for k in was if "light_pair" in k]
    assert len(credits[0]["kept"]) == 1 and credits[1]["kept"] == [0, 1]
    levels = [k for k in keys if k.endswith("now") or k.endswith("before")]  # the face: now 0 at 81
    assert all(was[k][w] == 0 for k in levels if k.endswith("now")) and any(now[k][w] != 0 for k in keys)
    assert all(dict(p for f in kept[82] for p in f)[k][w] == 0 for k in levels)  # both levels 0 at 82
    for _ in range(99):  # the faces presented again and the lays crossed from their lines, bit for bit
        BACK.crossed(board, lines)
        board.step_inverse()
        same = BACK.first_difference(kept[board.interval], BACK.snapshot(board)) is None
        assert same == (
            board.interval >= 80
        )  # below the click the realised past, the possibilities' kept
    assert BACK.verdict(Lattice(load_world(twin)), 39)["verdict"] == "MATCH"
    empty = Lattice(load_world(cut), (none := []).append)
    empty.credit.counts[pair] = 0
    for _ in range(80):
        empty.step()
    before = [c for c in lines if c["interval"] <= 80 and c["event"] not in ("credit", "lay")]
    assert none == before  # no click's line, no draw
    refused("window", draw_of, {**draw, "window": 0}, "draw")
    refused("unknown key 'seed'", draw_of, {"window": 1, "seed": 1}, "draw")  # no generator, no key


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


def test_a_absorption_from_a_dense_record_is_read_in_the_books_and_writes_nothing(tmp_path):
    """The undepleted beam (ALGEBRA.md, The click writes on the lattice; the two hands' line at the owner's word for the simple solution; `twist.faced`, `credit.Books.deficits`, `Lattice.books`): the shipped Zeno n = 2 world, whose drive holds about 2.6 quanta's share at the reader's Node (the booked share the credit reads there above the record's quantum W_rec), under the read of the board, beside its untouched twin. The absorption at 42, g to e climbing (re-pinned 2026-10-20 under the content of the born universe, the box opened along x as the content's sink and the window the lay's passage derived at load, 21: the second close, the first at 21 null; 72 and then 24 on the deleted world under the generator), books no face and no front, the drive's three arrays stand bit for bit as the twin's over the run (the drive reads no holder: the same Rule3 step), so its share at the Node and over the board is the twin's, printed; the count down by one, the deficit 1 and the share in quanta the count plus the deficit within the share's drift over the run in quanta (the books read at 84, between the absorption and the return; the books' `drift` over W_c and one quantum of the reading's rounding, printed); the return, e to g descending by the pulse at a later window's close, 84 (`lists.exchange`, stimulated emission; 96 before), emits the quantum back into the dense pulse: nothing laid, no source in time, the count back to the start and the deficit 0, the arrays the twin's still; the back-in-time gate MATCH across the absorption and the return, the atom's lays crossed from their lines."""
    zeno = content_world(
        tmp_path, "zeno_2", ZENO_2, ZENO_ATOM, opened
    )  # the content, the box opened along x (2026-10-20)
    board, twin = Lattice(load_world(zeno), (lines := []).append), Lattice(load_world(zeno))
    pulse = [f.name for f in board.families].index("pulse")
    at, count, unit = (4, 4, 2), board.credit.counts[pulse], board.credit.units[pulse]
    returns, books, its_books, booked_share = [], None, None, None
    while board.interval < 480 and not returns:
        board.step(), twin.step()
        for key in ("now", "before", "remainder"):
            mine, its = (getattr(b.states[pulse].lines[0], key) for b in (board, twin))
            assert np.array_equal(mine, its)  # the undepleted beam: nothing written on the drive
        taken = [x["interval"] for x in lines if x["event"] == "credit" and x["absorbed"]]
        if taken and booked_share is None:  # the absorption's interval: the drive's share at the Node
            booked_share = int(board.share_of(pulse)[0][at])
        if books is None and taken and board.interval == taken[0] + 12:  # the next close after it
            books, its_books = board.books()["pulse"], twin.books()["pulse"]  # the hole's deficit booked
        returns = [x for x in lines if x["event"] == "credit" and x["emitted"] == "pulse"]
    assert booked_share is not None and booked_share > unit  # dense: above the record's quantum
    assert books is not None and its_books is not None
    credits = [x for x in lines if x["event"] == "credit" and x["label"] == "NODEDETECTOR"]
    jumps = [x for x in credits if x["absorbed"]]
    assert [x["interval"] for x in jumps][:1] == [42] and jumps[0][
        "absorbed"
    ] == "pulse"  # the read's, 2026-10-20
    assert not any(f.family == pulse for faces in board.credit.faces.values() for f in faces)
    assert not board.credit.fronts and not board.credit.sources
    print(
        f"the Zeno drive's booked share at the Node {booked_share} over W_rec {unit}, the books {books}"
    )
    assert (books["count"], books["deficit"], books["quanta"]) == (count - 1, 1, its_books["quanta"])
    within = abs(books["drift"]) // board.credit.units[pulse] + 1  # the drift in W_rec (C1)
    print(f"the share in quanta {books['quanta']} against the count plus the deficit within {within}")
    assert abs(books["quanta"] - books["count"] - books["deficit"]) <= within
    assert books["share"] == its_books["share"] and books["drift"] == its_books["drift"]
    cycled = board.books()["pulse"]
    print(f"the return at {returns[0]['interval']} after {len(jumps)} absorptions: the books {cycled}")
    assert (cycled["count"], cycled["deficit"]) == (count - len(jumps) + 1, len(jumps) - 1)
    gate = Lattice(load_world(zeno))
    assert (
        BACK.verdict(gate, returns[0]["interval"])["verdict"] == "MATCH"
    )  # across the absorption and the return


def test_a_emission_into_a_dense_record_is_read_in_the_books_and_lays_nothing(tmp_path):
    """The undepleted beam at the emission (ALGEBRA.md, The click writes on the lattice; the two hands' line: a quantum given into a beam adds to the mode coherently in nature, and a one-Node lay into a dense record is the same point defect the dense hole was; `act.written`, `twist.faced`, `emission.emitted_quantum`): the Zeno n = 2 world's declaration (`ZENO_2`, inlined; re-pinned 2026-10-20 under the content of the born universe, the box opened along x as the content's sink, the declared window 24 kept since the rate's lay has no end on the axes across) with a rate e to g at the lifetime 8 emission to the pulse itself, the dense record at the reader's Node, under the read of the board, beside the pulse alone (the return by the rate or by the transition's descent, `lists.exchange`, both emissions into the beam): the absorptions and the emission write nothing on the pulse, whose three arrays stand bit for bit as the pulse alone over the run, no source in time begins and no lay line names the pulse, the count down by one per absorption and up by one per emission, the deficit the absorptions less the emissions (the books' line printed); the sparse emission's own tests stand in `tests/test_the_emission.py`."""

    def rated(world):  # type: ignore[no-untyped-def]
        opened(
            world
        )  # the content's sink; the rate's lay has no end across, so the declared window stays
        world["bodies"][0]["rates"] = [{"from": "e", "to": "g", "lifetime": 8, "gives_to": "pulse"}]
        world["bodies"][0]["node_detector"]["window"] = ZENO_2["bodies"][0]["node_detector"]["window"]
        world["intervals"] = 480

    path = content_world(tmp_path, "zeno_rate", ZENO_2, ZENO_ATOM, rated)  # the content, 2026-10-20
    world = json.loads(path.read_text(encoding="utf-8"))
    (alone := tmp_path / "pulse_alone.json").write_text(
        json.dumps({**world, "bodies": []}), encoding="utf-8"
    )
    TOOL.main(["--input", str(alone)])
    board, twin = Lattice(load_world(path), (lines := []).append), Lattice(load_world(alone))
    pulse = [f.name for f in board.families].index("pulse")
    count, given = board.credit.counts[pulse], []
    while board.interval < world["intervals"] and not given:
        board.step(), twin.step()
        given = [c for c in lines if c["event"] == "credit" and c["emitted"] == "pulse"]
    taken = [c for c in lines if c["event"] == "credit" and c["absorbed"] == "pulse"]
    assert given and taken and given[0]["interval"] > taken[0]["interval"]  # absorbed, then emitted
    for key in ("now", "before", "remainder"):
        assert np.array_equal(
            getattr(board.states[pulse].lines[0], key), getattr(twin.states[pulse].lines[0], key)
        )
    assert not board.credit.sources and not any(
        c["family"] == "pulse" for c in lines if c["event"] == "lay"
    )
    books = board.books()["pulse"]
    print(
        f"the Zeno pulse after {len(taken)} absorptions and {len(given)} emission at {board.interval}: the books {books}"
    )
    assert (books["count"], books["deficit"]) == (
        count - len(taken) + len(given),
        len(taken) - len(given),
    )
    assert (
        books["quanta"] == twin.books()["pulse"]["quanta"]
        and books["share"] == twin.books()["pulse"]["share"]
    )


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
    laid_by_count(board, twist.Item(pulse, None, None, 1, ((4, 4, 2),), pair=(6000, 6000)))
    for _ in range(200):
        board.step()
    largest = int(np.abs(board.states[pulse].lines[0].now).max())
    print(f"the lone quantum's largest level at the interval 200 on the box {board.shape}: {largest}")
    assert largest < 300, largest  # bounded: 50 by the lattice's rule on this box, 6,268 under the floor


def test_the_absorption_removes_the_photon_and_the_front_leaves_the_board_dark(tmp_path):
    """The committed one-photon world at the lay without the uniform mode (ALGEBRA.md, The click writes on the lattice (3) and (6)): one atom takes at its window's close (the taking atom's close, 63 under the content of the born universe, re-pinned 2026-10-20, the two closes 61 and 62 before it; which takes is the taking atom's read of the board) and the count falls to 0; the light's share over the lattice never rises above the lay's by more than the hole's and the front's transient (one part in seven, the known one), and once the front has swept both packets the share is 0 exactly, the board dark."""
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
        taken["interval"] == 63 and taken["interval"] == taken["window"][1]
    )  # re-pinned 2026-10-20: 63
    assert board.credit.counts[photon] == 0
    assert laid > 0 and max(shares) * 7 <= laid * 8 and shares[-1] == 0
    after = {x["event"] for x in lines if x["interval"] > taken["interval"]}
    assert after <= {"erasure", "face", "credit", "lay"}
