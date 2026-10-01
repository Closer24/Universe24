"""The meeting's gate (ALGEBRA.md #the-click-is-the-meeting, the pair's form; HIGHLIGHTS.md, One experiment and one gate): the pair family of two real lines laid as one event and never summed at a Node, the instrument's read of the parts' signed level sums (the parts line) and the joint-share reader pairing the parts through the root (tools/bell_gate.py): the exact algebra at the four settings and for unequal parts, the three local credits as the fence, the determinism of equal parts, and the four small worlds of examples/events/bell end to end with the back-in-time gate MATCH; Bell is a gate and never a result."""

import json
from fractions import Fraction

import pytest

from event_universe.game_board import GameBoard
from event_universe.loader.world import basis_of, universe_of
from event_universe.world_files import load_world
from tests.laws import BACK, ROOT, RUN, TOOL, load_file

GATE = load_file("bell_gate", ROOT / "tools" / "bell_gate.py")
BUILD = load_file("bell_build", ROOT / "examples" / "events" / "bell" / "build_world.py")
BELL = ROOT / "examples" / "events" / "bell"
A, A2, B, B2 = ((1, 0), (1, 1), (12, 5), (5, 12))  # the CHSH settings as the declared bases (p, q)
ORDER = ((A, B), (A, B2), (A2, B), (A2, B2))  # S = E(a, b) - E(a, b') + E(a', b) + E(a', b')
MEETING = [Fraction(119, 169), Fraction(-119, 169), Fraction(120, 169), Fraction(120, 169)]
FENCE = {GATE.parts_shares: Fraction(238, 169), GATE.local_sums: Fraction(240, 169)}  # the local credits
UNEQUAL = (Fraction(363518, 128609), Fraction(66625, 128609), [760, 761])  # S, P(A+), rho at r = 19/20
WINDOW = range(1, 4)


def side(first: tuple[int, int], second: tuple[int, int]) -> dict[int, list[list[int]]]:
    return {tick: [list(first), list(second)] for tick in WINDOW}


def credits(a, b, pairs=ORDER, form=GATE.joint):  # type: ignore[no-untyped-def]
    found = [form(a, b, GATE.ports_of(x), GATE.ports_of(y)) for x, y in pairs]
    correlations = [GATE.correlation(s) for s in found]
    return correlations, GATE.chsh(correlations), [GATE.marginal(s) for s in found]


def test_the_meeting_is_the_pairing_through_the_root_and_the_engine_implements_it_exactly(tmp_path):
    """(i) Equal parts on both sides over a window whose middle interval reports 0 (no 0 / 0 under the window rule): E = ((p p' + q q')^2 - (p q' - q p')^2) / ((p^2 + q^2) (p'^2 + q'^2)) at the four settings, S = 478 / 169 exactly and the marginal 1 / 2 whatever the partner's setting; the local credits on the same reports: by the parts' shares S = 238 / 169 (E = cos 2a cos 2b), by the local sums 240 / 169 (sin 2a sin 2b), by the sign 2 (the tie at (1, 0) reads 0). (ii) What a formula reader fails: the parts (20, 19) against (1, 1), r = 19 / 20, give S = 363518 / 128609 (2.8265), the marginal 66625 / 128609 (0.518) at (12, 5) for both partner settings and rho = 760 / 761; parts (1, 0) give S = 238 / 169 (rho = 0); no report gives no credit; the coefficients reversed on one side give S = 2 / 169 (about 0); a basis of one coefficient is refused by name. (iii) The four worlds of examples/events/bell/design.json built into a folder with their mode files (the pair family at the dimension [2, 1], two real lines; the regions' bases the settings) and run by the runner: every parts line reports the two parts equal at every interval (the determinism of equal parts), labelled the detector's; the reader gives E = 119 / 169, -119 / 169, 120 / 169, 120 / 169, S = 478 / 169 and the marginal 1 / 2 exactly, the local credits 238 / 169, 240 / 169 and 2, r = rho = 1 and one pair drawn per world, the blind file carrying the same S before the run; a part raised one level at one Node is not equal after the run and reads r off 1; the loader refuses by name a dimension shape of three numbers and a basis of zeros; the back-in-time gate says MATCH on each world over its run."""
    a, b, equal = side((7, -3), (7, -3)), side((5, 11), (5, 11)), side((1, 1), (1, 1))
    a[2] = b[2] = [[0, 0], [0, 0]]
    assert credits(a, b) == (MEETING, Fraction(478, 169), [Fraction(1, 2)] * 4)
    assert [credits(a, b, form=form)[1] for form in FENCE] == list(FENCE.values())
    outcomes = [GATE.sign_of(GATE.side_sums(a, GATE.ports_of(x))) for x in (A, A2)]
    outcomes += [GATE.sign_of(GATE.side_sums(b, GATE.ports_of(y))) for y in (B, B2)]
    assert outcomes == [0, 1, 1, 1]  # by the sign S = 0 - 0 + 1 + 1 = 2 exactly
    unequal, mirrored = side((20, 20), (19, 19)), ((B, A), (B2, A), (B, A2), (B2, A2))
    _found, meeting, marginals = credits(unequal, equal, pairs=mirrored)
    assert meeting == UNEQUAL[0] and marginals[0] == marginals[2] == UNEQUAL[1]
    mismatch = GATE.mismatch(unequal, equal, 2)
    assert (mismatch["r"], mismatch["rho"], mismatch["label"]) == ([19, 20], UNEQUAL[2], "GAMEBOARD")
    assert credits(side((1, 1), (0, 0)), b)[1] == FENCE[GATE.parts_shares]  # rho = 0
    assert GATE.correlation(GATE.joint({}, b, GATE.ports_of(A), GATE.ports_of(B))) is None
    assert credits(a, b, pairs=((A, B2), (A, B), (A2, B2), (A2, B)))[1] == Fraction(2, 169)
    with pytest.raises(ValueError, match="a pair"):
        GATE.ports_of((1,))
    BUILD.main(["--design", str(BELL / "design.json"), "--folder", str(tmp_path)])
    expected = json.loads((tmp_path / "expectation.json").read_text(encoding="utf-8"))
    outputs = [tmp_path / f"{name}.output.json" for name in expected["runs"].values()]
    for name in expected["runs"].values():
        TOOL.main(["--input", str(tmp_path / f"{name}.json")])
        assert RUN.run_input(str(tmp_path / f"{name}.json"), str(tmp_path))["verdict"] == "LAWFUL"
        lines = json.loads((tmp_path / f"{name}.output.json").read_text(encoding="utf-8"))["lines"]
        parts = [line for line in lines if line["event"] == "parts"]
        assert parts and all(line["levels"][0] == line["levels"][1] for line in parts)
        assert all(line["label"] == "DETECTOR" and "node" not in line for line in parts)
        board = GameBoard(load_world(tmp_path / f"{name}.json"))
        assert BACK.verdict(board, board.world.ticks)["verdict"] == "MATCH"
    read = GATE.reading(tmp_path / "expectation.json", outputs)
    assert read["S"] == [478, 169] == expected["blind"]["S"] and read["marginal"] == [[1, 2]] * 4
    assert [Fraction(*read["correlation"][key]) for key in expected["order"]] == MEETING
    assert (read["S_by_the_parts_shares"], read["S_by_the_local_sums"]) == ([238, 169], [240, 169])
    assert read["S_by_the_sign"] == [2, 1] == expected["blind"]["by_the_sign"]["S"]
    for world in read["worlds"].values():
        assert world["mismatch"]["r"] == [1, 1] == world["mismatch"]["rho"] and len(world["drawn"]) == 2
        assert world["intervals_reported"] > 0 and all(q[0] > 0 for q in world["quanta"].values())
    lines: list[dict[str, object]] = []
    path = tmp_path / f"{expected['runs'][expected['order'][0]]}.json"
    board = GameBoard(load_world(path), lines.append)
    pair = [f.name for f in board.families].index(expected["family"])
    board.states[pair].lines[1].now[board.shape[0] // 2, 0, 0] += 1  # one part a level off
    for _ in range(board.world.ticks):
        board.step()
    assert (board.states[pair].lines[0].now != board.states[pair].lines[1].now).any()
    assert GATE.one_world(path, lines, expected)["mismatch"]["r"] != [1, 1]
    universe = json.loads((ROOT / "examples" / "events" / "pair.json").read_text(encoding="utf-8"))
    universe["families"][-1]["dimension"] = [2, 1, 1]
    with pytest.raises(ValueError, match=r"as a shape is \[parts, dimension\]"):
        universe_of(universe)
    with pytest.raises(ValueError, match="not all 0"):
        basis_of([0, 0], "detectors[0].basis")
