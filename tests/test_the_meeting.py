"""The meeting's gates (ALGEBRA.md #the-click-is-the-meeting, the pair's form and the GHZ gate; HIGHLIGHTS.md, One experiment and one gate): a record of several parts laid as one event and never summed at a Node, the instrument's read of the parts' signed level sums (the parts line) and the joint-share reader pairing the parts through the root across the sides (tools/bell_gate.py): the exact algebra at Bell's four settings and at the GHZ patterns, the local credits as the fence, the determinism of equal parts, and the two gates' four worlds each (examples/events/bell, examples/events/ghz) end to end with the back-in-time gate MATCH; Bell and the GHZ are gates and never results."""

from __future__ import annotations

import json
from fractions import Fraction

from event_universe.game_board import GameBoard
from event_universe.loader.instrument import basis_of, pattern_of, patterns_of_the_law
from event_universe.loader.world import detectors_of, shape_of, universe_of
from event_universe.world_files import load_world
from tests.laws import BACK, EVENTS, ROOT, RUN, TOOL, load_file, refused

GATE = load_file("bell_gate", ROOT / "tools" / "bell_gate.py")
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
    return {tick: [list(part) for part in parts] for tick in range(1, 4)}


def credits(sides, order, patterns, form=GATE.joint):  # type: ignore[no-untyped-def]
    shares = [form(sides, [GATE.ports_of(*sp) for sp in zip(s, patterns, strict=True)]) for s in order]
    return shares, [GATE.correlation(found) for found in shares]


def gate_worlds(build, folder):  # type: ignore[no-untyped-def]
    """A gate's four worlds built from its design into `folder` with the blind, laid, run by the runner (LAWFUL; every parts line's parts equal, labelled the detector's and naming no Node) and gated back in time over the run (MATCH), then read against the blind: the reading and the expectation."""
    build.main(["--design", str(build.HERE / "design.json"), "--folder", str(folder)])
    expected = json.loads((folder / "expectation.json").read_text(encoding="utf-8"))
    for name in expected["runs"].values():
        TOOL.main(["--input", str(folder / f"{name}.json")])
        assert RUN.run_input(str(folder / f"{name}.json"), str(folder))["verdict"] == "LAWFUL"
        lines = json.loads((folder / f"{name}.output.json").read_text(encoding="utf-8"))["lines"]
        parts = [line for line in lines if line["event"] == "parts"]
        assert parts and all(
            len(set(map(tuple, p["levels"]))) == 1 and p["label"] == "DETECTOR" for p in parts
        )
        board = GameBoard(load_world(folder / f"{name}.json"))
        assert BACK.verdict(board, board.world.ticks)["verdict"] == "MATCH"
    outputs = [folder / f"{name}.output.json" for name in expected["runs"].values()]
    return GATE.reading(folder / "expectation.json", outputs), expected


def test_the_meeting_is_the_pairing_through_the_root_and_the_engine_implements_it_exactly(tmp_path):
    """(i) Equal parts on both sides over a window whose middle interval reports 0 (no 0 / 0 under the window rule): E = ((p p' + q q')^2 - (p q' - q p')^2) / ((p^2 + q^2) (p'^2 + q'^2)) at the four settings, S = 478 / 169 exactly and the marginal 1 / 2 whatever the partner's setting; the local credits on the same reports: by the parts' shares S = 238 / 169 (E = cos 2a cos 2b), by the local sums 240 / 169 (sin 2a sin 2b), by the sign 2 (the tie at (1, 0) reads 0, read with the worlds). (ii) What a formula reader fails: the parts (20, 19) against (1, 1), r = 19 / 20, give S = 363518 / 128609 (2.8265), the marginal 66625 / 128609 (0.518) at (12, 5) for both partner settings and rho = 760 / 761; parts (1, 0) give S = 238 / 169 (rho = 0); a setting of one coefficient and a pattern whose ports are not orthogonal are refused by name. (iii) The four worlds of examples/events/bell/design.json built with their mode files (the pair family at the dimension [2, 1]; the regions' bases the settings, their pattern the pair's) and run: the parts equal at every interval, the reader gives E = 119 / 169, -119 / 169, 120 / 169, 120 / 169, S = 478 / 169 and the marginals 1 / 2 exactly, the local credits 238 / 169, 240 / 169 and 2, the ratio and rho 1 and one pair drawn per world, the blind file carrying the same S before the run; a part raised one level at one Node is not equal after the run and reads the ratio off 1; the loader refuses by name a dimension shape of three numbers and a basis of zeros; the back-in-time gate says MATCH on each world over its run."""
    a, b, equal = side((7, -3), (7, -3)), side((5, 11), (5, 11)), side((1, 1), (1, 1))
    a[2] = b[2] = [[0, 0], [0, 0]]
    shares, found = credits([a, b], ORDER, (PAIR, PAIR))
    assert found == MEETING and GATE.combination(found, CHSH) == Fraction(478, 169)
    assert [GATE.marginal(s) for s in shares] == [Fraction(1, 2)] * 4
    for form, value in FENCE.items():
        assert GATE.combination(credits([a, b], ORDER, (PAIR, PAIR), form)[1], CHSH) == value
    unequal, mirrored = side((20, 20), (19, 19)), tuple((y, x) for x, y in ORDER)
    shares, found = credits([unequal, equal], mirrored, (PAIR, PAIR))
    assert GATE.combination(found, CHSH) == UNEQUAL[0]
    assert GATE.marginal(shares[0]) == GATE.marginal(shares[2]) == UNEQUAL[1]
    m = GATE.mismatch([unequal, equal], 2)
    assert (m["ratios"], m["rho"], m["label"]) == ([[19, 20]], UNEQUAL[2], "GAMEBOARD")
    rho_zero = credits([side((1, 1), (0, 0)), b], ORDER, (PAIR, PAIR))[1]
    assert GATE.combination(rho_zero, CHSH) == FENCE[GATE.parts_shares]
    refused("setting", GATE.ports_of, (1,), PAIR)
    refused("orthogonal", GATE.ports_of, A, ((1, 1),))
    read, expected = gate_worlds(BELL, tmp_path)
    assert read["S"] == [478, 169] == expected["blind"]["S"]
    assert [Fraction(*read["correlation"][key]) for key in expected["order"]] == MEETING
    assert all(found == {"a": [1, 2], "b": [1, 2]} for found in read["marginals"].values())
    assert (read["S_by_the_parts_shares"], read["S_by_the_local_sums"]) == ([238, 169], [240, 169])
    assert read["S_by_the_sign"] == [2, 1] == expected["blind"]["by_the_sign"]["S"]
    for world in read["worlds"].values():
        assert world["mismatch"]["ratios"] == [[1, 1]] and world["mismatch"]["rho"] == [1, 1]
        assert len(world["drawn"]) == 2 and all(q[0] > 0 for q in world["quanta"].values())
    path = tmp_path / f"{expected['runs'][expected['order'][0]]}.json"
    board = GameBoard(load_world(path), (lines := []).append)
    board.states[-1].lines[1].now[board.shape[0] // 2, 0, 0] += 1  # the pair's one part a level off
    for _ in range(board.world.ticks):
        board.step()
    assert (board.states[-1].lines[0].now != board.states[-1].lines[1].now).any()
    assert GATE.one_world(path, lines, expected)["mismatch"]["ratios"] != [[1, 1]]
    refused(r"as a shape is \[parts, dimension\]", shape_of, {"dimension": [2, 1, 1]}, "families[0]")
    refused("not all 0", basis_of, [0, 0], "detectors[0].basis")


def test_the_ghz_gate_pairs_four_parts_through_the_root_on_three_sides_exactly(tmp_path):
    """(i) Equal parts on three sides read with the GHZ patterns A (p, p, q, q), B (p, q, p, q), C (p, -q, -q, -p): the eight shares are cos^2(a + b + c) / 4 at an even number of - ports and sin^2(a + b + c) / 4 at an odd, so at (x, y, y), (y, x, y) and (y, y, x) the even shares 0 and the odd 1 / 4 with E_3 = -1, at (x, x, x) the even 1 / 4 and the odd 0 with E_3 = 1, at ((12, 5), x, x) the even 36 / 169 and E_3 = 119 / 169; every single-side and every pairwise E 0 (the marginals 1 / 2); M = -4 (|M| = 4 beside local realism's 2); the three local credits give M = -1 each; the loader refuses by name a pattern of [0, 0], a pattern without a basis, a pattern of the wrong length against the records the world lays and a pattern in a world laying no record of several parts. (ii) The four worlds of examples/events/ghz/design.json (the GHZ family at the dimension [4, 1] on a square board, three beams to three regions) built with the blind, laid and run: the parts equal, the eight shares, E_3, the marginals, the pairwise E and M = -4 from the engine's reports the blind's exactly, the local credits -1, the ratios 1, one triple drawn per world, MATCH on each world over its run."""
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
    for form in FENCE:
        assert GATE.combination(credits(three, MERMIN[0], PATTERNS, form)[1], MERMIN[1]) == -1
    refused(r"\[0, 0\]", pattern_of, [[1, 0], [0, 0]], "detectors[0].pattern", (1, 0))
    row = {"name": "d", "positions": [[0, 0, 0], [1, 0, 0]], "pattern": [[1, 0]]}
    refused("none is declared", detectors_of, [row], (2, 1, 1), 0, (), ())
    families = universe_of(json.loads((EVENTS / "ghz.json").read_text(encoding="utf-8")))[1]
    refused("pattern of 3 parts", patterns_of_the_law, [("d", (P,) * 3)], [len(families) - 1], families)
    refused("no record of several parts", patterns_of_the_law, [("d", (P,) * 4)], [], families)
    read, expected = gate_worlds(GHZ, tmp_path)
    assert read["M"] == [-4, 1] == expected["blind"]["M"]
    assert [read["correlation"][key] for key in expected["order"]] == [[-1, 1]] * 3 + [[1, 1]]
    for credit in ("M_by_the_parts_shares", "M_by_the_local_sums", "M_by_the_sign"):
        assert read[credit] == [-1, 1]
    worlds = [read["worlds"][name] for name in expected["runs"].values()]
    assert [w["shares"] for w in worlds] == list(expected["blind"]["shares"].values())
    assert all(len(w["drawn"]) == 3 and w["mismatch"]["ratios"] == [[1, 1]] * 3 for w in worlds)
    assert read["marginals"] == dict.fromkeys(expected["order"], dict.fromkeys("abc", [1, 2]))
    assert all(w["sub_correlations"] == dict.fromkeys(("a b", "a c", "b c"), [0, 1]) for w in worlds)
