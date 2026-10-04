"""The meeting's gates (ALGEBRA.md #the-click-is-the-meeting, the pair's form and the GHZ gate; HIGHLIGHTS.md, One experiment and one gate): a record of several parts laid as one event and never summed at a Node, the NodeReader's read of the parts' signed level sums (the parts line) and the joint-share reader pairing the parts through the root across the sides (tools/bell_gate.py): the exact algebra at Bell's four settings and at the GHZ patterns, the local credits as the fence, the determinism of equal parts, and the two gates' four worlds each (examples/events/bell, examples/events/ghz) end to end with the back-in-time gate MATCH; Bell and the GHZ are gates and never results. The click written on the GameBoard (src/event_universe/credit.py, features/click): the NodeReader's draw inside the run and its write at one Node, the board exact between clicks."""

import json
import math
from fractions import Fraction

import numpy as np

from event_universe import meeting, node, resonance, world_files
from event_universe.game_board import GameBoard
from event_universe.giving import laid_by_count
from event_universe.loader.derived import count_wall, row_of
from event_universe.loader.draw import (
    Draw,
    Generator,
    basis_of,
    draw_of,
    pattern_of,
    patterns_of_the_law,
)
from event_universe.loader.node_reader_declaration import (
    Transition,
    node_reader_of,
)
from event_universe.loader.universe import shape_of, universe_of
from event_universe.loader.world import node_readers_of
from event_universe.world_files import load_world
from tests.laws import BACK, EVENTS, ROOT, RUN, TOOL, TOP, load_file, refused

TOP_PAIR = (TOP[0], TOP[1])  # the band's top as a resonance, cos Omega = 0

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
    build.main(["--design", str(build.HERE / "design.json"), "--folder", str(folder)])
    expected = json.loads((folder / "expectation.json").read_text(encoding="utf-8"))
    for name in expected["runs"].values():
        TOOL.main(["--input", str(folder / f"{name}.json")])
        assert RUN.run_input(str(folder / f"{name}.json"), str(folder))["verdict"] == "LAWFUL"
        lines = json.loads((folder / f"{name}.output.json").read_text(encoding="utf-8"))["lines"]
        parts = [line for line in lines if line["event"] == "parts"]
        equal = all(len(set(map(tuple, p["levels"]))) == 1 and p["label"] == "NODEREADER" for p in parts)
        credits = [line for line in lines if line["event"] == "credit"]
        assert parts and equal and credits and all(c["tick"] == c["window"][1] for c in credits)
        board = GameBoard(load_world(folder / f"{name}.json"))
        assert BACK.verdict(board, 4)["verdict"] == "MATCH"  # exact before the click, the gate per step
    outputs = [folder / f"{name}.output.json" for name in expected["runs"].values()]
    read, name = GATE.reading(folder / "expectation.json", outputs), expected["combination"]["name"]
    assert read[name] == expected["blind"][name]
    assert read["correlation"] == expected["blind"]["correlation"]
    assert read["marginals"] == expected["blind"]["marginals"]
    return read, expected


def test_the_meeting_is_the_pairing_through_the_root_and_the_engine_implements_it_exactly(tmp_path):
    """(i) Equal parts on both sides over a window whose middle interval reports 0 (no 0 / 0 under the window rule): E = ((p p' + q q')^2 - (p q' - q p')^2) / ((p^2 + q^2) (p'^2 + q'^2)) at the four settings, S = 478 / 169 exactly and the marginal 1 / 2 whatever the partner's setting; the local credits on the same reports: by the parts' shares S = 238 / 169 (E = cos 2a cos 2b), by the local sums 240 / 169 (sin 2a sin 2b), by the sign 2 (the tie at (1, 0) reads 0, read with the worlds). (ii) What a formula reader fails: the parts (20, 19) against (1, 1), r = 19 / 20, give S = 363518 / 128609 (2.8265), the marginal 66625 / 128609 (0.518) at (12, 5) for both partner settings and rho = 760 / 761; parts (1, 0) give S = 238 / 169 (rho = 0); a setting of one coefficient and a pattern whose ports are not orthogonal are refused by name. (iii) The four worlds of examples/events/bell/design.json built with their mode files (the pair family at the dimension [2, 1]; the regions' bases the settings, their pattern the pair's) and run: the parts equal at every interval, the reader gives E = 119 / 169, -119 / 169, 120 / 169, 120 / 169, S = 478 / 169 and the marginals 1 / 2 exactly, the local credits 238 / 169, 240 / 169 and 2, the ratio and rho 1 and one pair drawn per world, the blind file carrying the same S before the run; a part raised one level at one Node is not equal after the run and reads the ratio off 1; the loader refuses by name a dimension shape of three numbers and a basis of zeros; the back-in-time gate says MATCH on each world over its run."""
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
    assert (m["ratios"], m["rho"], m["label"]) == ([[19, 20]], UNEQUAL[2], "GAMEBOARD")
    rho_zero = credits([side((1, 1), (0, 0)), b], ORDER, (PAIR, PAIR))[1]
    assert GATE.combination(rho_zero, CHSH) == FENCE[GATE.parts_shares]
    refused("setting", GATE.ports_of, (1,), PAIR), refused("orthogonal", GATE.ports_of, A, ((1, 1),))
    read, expected = gate_worlds(BELL, tmp_path)
    assert [Fraction(*read["correlation"][k]) for k in expected["order"]] == MEETING
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
    refused("not all 0", basis_of, [0, 0], "node_readers[0].basis")


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
    fenced = [GATE.combination(credits(three, MERMIN[0], PATTERNS, f)[1], MERMIN[1]) for f in FENCE]
    assert fenced == [-1] * len(FENCE)
    refused(r"\[0, 0\]", pattern_of, [[1, 0], [0, 0]], "node_readers[0].pattern", (1, 0))
    row = {"name": "d", "positions": [[0, 0, 0], [1, 0, 0]], "pattern": [[1, 0]]}
    refused("none is declared", node_readers_of, [row], (2, 1, 1), 0, (), ())
    families = universe_of(json.loads((EVENTS / "ghz.json").read_text(encoding="utf-8")))[1]
    refused("pattern of 3 parts", patterns_of_the_law, [("d", (P,) * 3)], [len(families) - 1], families)
    refused("no record of several parts", patterns_of_the_law, [("d", (P,) * 4)], [], families)
    read, expected = gate_worlds(GHZ, tmp_path)
    assert read["M"] == [-4, 1] and list(read["correlation"].values()) == [[-1, 1]] * 3 + [[1, 1]]
    ms = ("M_by_the_parts_shares", "M_by_the_local_sums", "M_by_the_sign")
    assert all(read[c] == [-1, 1] for c in ms)
    worlds = [read["worlds"][name] for name in expected["runs"].values()]
    assert [w["shares"] for w in worlds] == list(expected["blind"]["shares"].values())
    assert all(len(w["drawn"]) == 3 and w["mismatch"]["ratios"] == [[1, 1]] * 3 for w in worlds)
    assert all(w["sub_correlations"] == dict.fromkeys(("a b", "a c", "b c"), [0, 1]) for w in worlds)


def test_the_click_is_written_at_one_node_and_the_board_is_exact_between_clicks(tmp_path):
    """The click written on the GameBoard (ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision of 2026-10-02; features/click, src/event_universe/credit.py): Bell's shipped world a b with the draw's window cut to 40 over its 100 intervals, beside its twin without the key. (i) One credit line per side at 40 and at 80: the result the window, the node_reader's proper time at the close (the board's tick in the vacuum) and the index of the window closed, the region, the port realised, the parts kept and the count 1, the record's count down by one per window, no Node (the hole's Nodes in the face lines); at 40 the two boards differ at the two written Nodes alone (the one-Node test), and at the written Node every line of the record is 0 in its three arrays (the hole, as the receding face removes a share) where the twin's levels stand. (ii) The inverse is exact between clicks: from 100 back to 80 every array returns bit for bit, the step back across the click misses, and the twin goes from 40 back to the lay, MATCH. (iii) The record's count: at 0 the draw credits nothing over the same 40 intervals, the reports the same lines with no credit line among them; the `draw` key refused by name with a window of 0 and without its seed."""
    world = json.loads((EVENTS / "bell" / "bell_a_b.json").read_text(encoding="utf-8"))
    world["draw"]["window"], draw = 40, dict(world["draw"])
    (cut := tmp_path / "cut.json").write_text(json.dumps(world), encoding="utf-8")
    world.pop("draw")
    (twin := tmp_path / "twin.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(cut)]), TOOL.main(["--input", str(twin)])
    board, plain = GameBoard(load_world(cut), (lines := []).append), GameBoard(load_world(twin))
    kept = {}
    for _ in range(100):
        board.step(), kept.__setitem__(board.tick, BACK.snapshot(board))
        board.tick <= 41 and plain.step()
    credits = [line for line in lines if line["event"] == "credit"]
    pair = next(i for i, f in enumerate(board.families) if f.name == "light_pair")
    at = [(c["tick"], c["node_reader"], c["count"], c["window"][0], c["left"]) for c in credits]
    left = board.credit.counts[pair]
    assert at == [(40, "left", 1, 1, left + 1), (40, "right", 1, 1, left + 1)] + at[2:]
    assert at[2:] == [(80, "left", 1, 41, left), (80, "right", 1, 41, left)]
    was, now = dict(p for f in kept[41] for p in f), dict(p for f in BACK.snapshot(plain) for p in f)
    assert [(c["proper"], c["windows"]) for c in credits] == [(40, 1), (40, 1), (80, 2), (80, 2)]
    report = set(
        "event label tick family node_reader window proper windows before realised kept count left taken given".split()
    )
    assert all(set(c) == report and c["label"] == "NODEREADER" for c in credits)  # never a Node
    holes = [
        f for f in lines if f["event"] == "face" and f["tick"] == 41
    ]  # the hole's Nodes, the tool's
    written = {tuple(np.add(f["node"]["at"], plain.offset)) for f in holes}
    assert {tuple(map(int, at)) for k in was for at in np.argwhere(was[k] != now[k])} == written
    w, keys = sorted(written)[0], [k for k in was if "light_pair" in k]
    assert len(credits[0]["kept"]) == 1 and credits[1]["kept"] == [0, 1]
    levels = [k for k in keys if k.endswith("now") or k.endswith("before")]  # the face: now 0 at 41
    assert all(was[k][w] == 0 for k in levels if k.endswith("now")) and any(now[k][w] != 0 for k in keys)
    assert all(dict(p for f in kept[42] for p in f)[k][w] == 0 for k in levels)  # both levels 0 at 42
    for _ in range(99):  # the faces presented again and the lays crossed from their lines
        (
            BACK.crossed(board, lines),
            board.step_inverse(),
        )  # lines: the inverse crosses the clicks bit for bit
        assert BACK.first_difference(kept[board.tick], BACK.snapshot(board)) is None
    assert BACK.verdict(GameBoard(load_world(twin)), 39)["verdict"] == "MATCH"
    empty = GameBoard(load_world(cut), (none := []).append)
    empty.credit.counts[pair] = 0
    for _ in range(40):
        empty.step()
    before = [line for line in lines if line["tick"] <= 40 and line["event"] != "credit"]
    assert none == before and empty.credit.state == draw["seed"]  # no credit line, no draw consumed
    refused("window", draw_of, {**draw, "window": 0}, "draw")
    refused("lacks", draw_of, {"window": 1}, "draw")


def test_a_record_converted_whole_at_its_node_lays_the_table_at_the_rate(tmp_path):
    """The conversion, the fifth list of the one act (ALGEBRA.md, A family's declaration, item 5; the two hands of 2026-10-03, #1572 comments 5963954612 (c), 5964082980, 5964520368 and 5964754600; src/event_universe/conversion.py, loader/node_reader_declaration.py `conversion_of`): the neutron conversion's committed world (examples/events/neutron_conversion) at the rate 1 and the window 2, so the first window, closing at the second interval, draws it. (i) The loader: a rate of 0, a record out of the body's own family, an empty table, a sense on a record of real lines, a conversion beside parts and one without its draw are refused by name. (ii) The lay: the three lines at the Node at (95, -76) by the invariant, A_l^2 = T den div (2 s x 3), the reader's count 1. (iii) The click: one conversion line naming the reader, the three families out and the Node as a diagnostic; the neutron's three lines (0, 0) at the Node and its count 0; each record out given one whole quantum by the count on every laid line alike, A_l^2 = T div (2 laid): the antineutrino's real line (128, 128), the electron's plane (128, 0) and (0, 128) and the proton's three planes (73, 0) and (0, -73) each at the senses the table declares (`giving.laid_by_count`), the credit's counts 1 each and the share 1 per quantum at the Node (the two hands; the proton's 0.976 rounding to 1); one lay line per line the write changed, the record's three, the proton's six, the electron's two and the antineutrino's one, and the back-in-time gate MATCH across the conversion from them; no second conversion, no front (the body cut) and no null window of a record of one part."""
    folder = EVENTS / "neutron_conversion"
    families = universe_of(json.loads((folder / "nucleons.json").read_text(encoding="utf-8")))[1]
    world = json.loads((folder / "neutron_conversion.json").read_text(encoding="utf-8"))
    table = (body := world["bodies"][0])["conversion"]
    body["conversion"]["rate"], body["node_reader"]["window"], world["ticks"] = 1, 2, 4
    (path := tmp_path / "w.json").write_text(json.dumps(world), encoding="utf-8")
    quanta = {f.name: k for k, f in enumerate(families) if f.quanta}
    rows = {"from 1": {"rate": 0}, "other than": {"to": ["neutron"]}, "lists the": {"to": []}}
    rows["at none"], rows["without its sense"] = {"sense": 1}, {"to": ["proton"]}  # a plane's entry
    wrong = {word: {**body, "conversion": {**table, **row}} for word, row in rows.items()}
    wrong["no parts"] = {**body, "parts": []}
    wrong["no `node_reader`"] = {k: v for k, v in body.items() if k != "node_reader"}
    for word, entry in wrong.items():
        refused(word, node_reader_of, entry, "bodies[0]", families, quanta["neutron"], quanta, 1)
    board = GameBoard(load_world(path), (lines := []).append)
    n, p, e, nu = map(quanta.__getitem__, names := ("neutron", "proton", "electron", "antineutrino"))

    region = [(4, 4, 4), (5, 4, 4)]  # the record's two Nodes, the lay in equal weights

    def levels(k, at=(4, 4, 4)):
        return [(int(r.now[at]), int(r.before[at])) for r in board.states[k].lines]

    for at in (
        region
    ):  # the three lines at each Node by the invariant over two, A_l^2 = T den div (2 s x 3 x 2)
        assert levels(n, at) == [(67, -54)] * 3
    assert board.credit.bodies[0].counts == [1]
    board.step(), board.step()
    [first] = [line for line in lines if line["event"] == "conversion"]  # one conversion line
    assert first["window"] == [1, 2] and first["node"]["label"] == "GAMEBOARD"
    drawn = tuple(first["node"]["at"])  # the records out at the one Node of the region the draw picked
    assert drawn in region and (other := next(at for at in region if at != drawn))
    assert (first["into"], first["node_reader"], first["label"]) == (
        [*names[1:]],
        "body 0",
        "NODEREADER",
    )
    assert all(levels(n, at) == [(0, 0)] * 3 for at in region) and board.credit.bodies[0].counts == [0]
    assert levels(p, drawn) == [(73, 0), (0, -73)] * 3 and levels(e, drawn) == [(128, 0), (0, 128)]
    assert levels(nu, drawn) == [(128, 128)] and [board.credit.counts[k] for k in (p, e, nu)] == [
        1,
        1,
        1,
    ]
    assert all(
        levels(k, other)[0] == (0, 0) for k in (p, e, nu)
    )  # the other Node of the region untouched
    assert [int(board.quanta(k)[0][drawn]) for k in (p, e, nu)] == [1, 1, 1]
    laid = [(line["family"], line["line"]) for line in lines if line["event"] == "lay"]
    assert laid == [("neutron", k) for k in range(3) for _ in region] + [
        (f, k) for f, m in zip(names[1:], (6, 2, 1), strict=True) for k in range(m)
    ]  # the record's lines once per Node of its region, the records out at the drawn Node
    board.step(), board.step()
    others = (
        "click",
        "lay",
        "density",
        "parts",
    )  # the region `around` holds the record's second Node: its parts read
    assert [x["event"] for x in lines if x["event"] not in others] == ["conversion"]
    assert BACK.verdict(GameBoard(load_world(path)), 3)["verdict"] == "MATCH"  # across the conversion


def test_a_given_plane_is_laid_on_every_plane_alike_with_the_tables_sense_and_writes_the_sign_row(
    tmp_path,
):
    """The lay by the count with the sense (round F of the board of 2026-10-03, the neutron reading's row 2; the two hands' one-Node lay, #1572 comments 5964520368 and 5964754600; the worker's four points to both hands, 5967852499, and the mathematician's 244 on them, 5967913000: the quarter turn, every plane alike, the sense in the conversion's table per record out; src/event_universe/giving.py `laid_by_count` and `given_lines`, loader/node_reader_declaration.py `conversion_of`): (i) the loader: a `to` entry of a plane family is {family, sense}, the sense +1 or -1 (the shipped world's proton -1 and electron +1); a plane family named without its sense, a record of real lines with one, a sense of 0 or 2 and an entry with another key are refused by name. (ii) The lay, on the committed world at the rate 1 and the window 1 (the conversion drawn at the first interval, the weights [1, 0]): every laid line alike, A_l^2 = T div (2 laid), the electron's plane at (128, 0) and (0, 128), the proton's three planes at (73, 0) and (0, -73) each (the fixed point of 5,461), the antineutrino's real line (128, 128); the Wronskians at the Node 16,384 and -15,987 (3 x 73^2, the root's rounding), the senses opposite; the share at the Node 1 quantum each (the proton's 0.976 of W_c rounding to 1), the books and the share agreeing; twelve lay lines, the neutron's three, the proton's six, the electron's two and the antineutrino's one, and the back-in-time gate MATCH across the conversion from them. (iii) The sign row: the holder's rows 0 at the Node before the conversion and the free row 0 throughout; from the conversion on the proton's row and the electron's row are written at the Node, each record's W over the wall E_s T about half a level per interval carried, the first level other than 0 within four intervals the record's sense, -1 and +1."""
    folder = EVENTS / "neutron_conversion"
    families = universe_of(json.loads((folder / "nucleons.json").read_text(encoding="utf-8")))[1]
    world = json.loads((folder / "neutron_conversion.json").read_text(encoding="utf-8"))
    quanta = {f.name: k for k, f in enumerate(families) if f.quanta}
    body, region = world["bodies"][0], [(4, 4, 4), (5, 4, 4)]  # the record's two Nodes
    proton, electron, antineutrino = table = body["conversion"]["to"]
    assert (proton["sense"], electron["sense"], antineutrino) == (-1, 1, "antineutrino")
    wrong = {
        "without its sense": ["proton"],
        "real lines at none": [{"family": "antineutrino", "sense": 1}],
        "got 0": [{**proton, "sense": 0}],
        "from -1 through 1": [{**electron, "sense": 2}],
        "unknown key": [{**proton, "weight": 1}],
    }
    for word, outs in wrong.items():
        entry = {**body, "conversion": {**body["conversion"], "to": outs}}
        refused(word, node_reader_of, entry, "bodies[0]", families, quanta["neutron"], quanta, 1)
    body["conversion"]["rate"], body["node_reader"]["window"], world["ticks"] = 1, 1, 6
    (path := tmp_path / "w.json").write_text(json.dumps(world), encoding="utf-8")
    board = GameBoard(load_world(path), (lines := []).append)
    p, e, nu = outs = [quanta[row["family"] if isinstance(row, dict) else row] for row in table]
    sign = next(k for k, f in enumerate(board.families) if f.wronskian)

    at = (
        4,
        4,
        4,
    )  # the records out at the one Node of the region the conversion's draw picks, read below

    def levels(k):
        return [(int(r.now[at]), int(r.before[at])) for r in board.states[k].lines]

    def sign_rows():
        return [int(line.now[at]) for line in board.states[sign].lines[: board.families[sign].records]]

    assert all(sign_rows() == [0, 0, 0] for at in region)
    board.step()  # the first window closes at the first interval and the conversion is drawn
    [converted] = [x for x in lines if x["event"] == "conversion"]
    at = tuple(converted["node"]["at"])  # the drawn Node, a diagnostic of the line
    assert converted["tick"] == 1 and at in region and sign_rows() == [0, 0, 0]
    assert levels(p) == [(73, 0), (0, -73)] * 3 and levels(e) == [(128, 0), (0, 128)]
    assert levels(nu) == [(128, 128)] and [board.credit.counts[k] for k in outs] == [1, 1, 1]
    wronskians = [int(np.asarray(node.wronskian(board.states[k].lines, True))[at]) for k in (p, e)]
    assert wronskians == [
        -15987,
        16384,
    ]  # 3 x (-73^2) and T div 2: the senses opposite, the root's rounding
    assert [int(board.quanta(k)[0][at]) for k in outs] == [
        1,
        1,
        1,
    ]  # the count's unit, the share rounded
    laid = [(x["family"], x["line"]) for x in lines if x["event"] == "lay"]
    assert laid[:6] == [(body["family"], k) for k in range(3) for _ in region] and len(laid) == 15
    assert laid[6:12] == [(proton["family"], k) for k in range(6)]  # the records out at the drawn Node
    assert laid[12:] == [(electron["family"], 0), (electron["family"], 1), (antineutrino, 0)]
    first = {row_of(board.families, k, 0): 0 for k in (p, e)}  # the rows the two records own
    for _ in range(4):
        board.step()
        first = {row: found or sign_rows()[row] for row, found in first.items()}
        assert sign_rows()[0] == 0  # the free row, owned by no record, untouched
    assert [first[row_of(board.families, k, 0)] for k in (p, e)] == [-1, 1]  # the first write the sense
    assert BACK.verdict(GameBoard(load_world(path)), 3)["verdict"] == "MATCH"  # across the conversion


def test_the_resonant_two_mode_act_turns_by_the_planes_size_once_per_window():
    """The resonant two-mode act (ALGEBRA.md #what-is-open, item 50, the two-quadrature form; the mathematician's 223 (c) and 224 (2)(c), #1572 comments 5965727937 and 5966081562, the advisor's seconds, 5965918924 and 5966129376, two hands; src/event_universe/resonance.py and `meeting.turned_labels`): (i) the scale R is derived from the width's room, the file's amplitude bound and the record's window, the largest power of two with 2 (R A W)^2 inside the room, 2^12 at A = 9,266 and W = 48, 2^11 at W = 96 and 2^14 at W = 12, nothing declared; (ii) the two reference records advance by the giving's one recurrence (giving.advanced, through `gathered` at the level 0) and stay within 7 levels of R cos(Omega t) and R sin(Omega t) over 100 intervals at [2, 3]; (iii) a resonant arrival A cos(Omega t + phi) at A = 1,000 over W = 48 turns by A W / 2 within 2 percent at the phases 0, 0.7, pi / 2 and 2.5 (the hands' 23,724 to 24,289 against 24,000), where the magnitude form accumulated (2 / pi) A W at every frequency; (iv) the arrival at [1, 3]'s frequency against the pair [2, 3] turns by less than 2 percent of the resonant turn at W = 48 (sinc(delta W / 2) = 0.007 with the counter-rotating residue) and by sinc within 0.02 at W = 12 (0.30 against 0.31); (v) on the shipped Zeno world zeno_4 (the window 12) the labels stand at their start through the window's first eleven intervals while the two sums gather, and at the twelfth the sums are read once and begin again with the window: the root once per window, the NodeReader's act; (vi) the window's turn is applied as W equal sub-turns with the carry (`resonance.sheared`), so the labels' angle at the Zeno world's n = 1 is 48 x 2 arctan(9,408 / (12,000 x 48)) = 1.568 and not the one shear's 1.330, the tangent half-angle's compression the advisor's second found on the first build."""
    omega, detuned, bound, room = math.acos(2 / 3), math.acos(1 / 3), 9266, 2**63 - 1
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
    board = GameBoard(load_world(EVENTS / "zeno" / "zeno_4.json"))
    books = board.credit.bodies[0]
    start, gathered = list(books.labels), books.references[0]
    for _ in range(11):
        board.step()
        assert books.labels == start and (gathered.in_phase, gathered.quadrature) != (0, 0)
    board.step()
    assert (gathered.in_phase, gathered.quadrature) == (0, 0) and books.elapsed == 0
    turned = [resonance.sheared(10**6, 0, 9408, pieces, 6000) for pieces in (48, 1)]
    angles = [math.atan2(v, u) for u, v in turned]
    assert abs(angles[0] - 1.5680) <= 0.002 and abs(angles[1] - 1.330) <= 0.002  # the sub-turns add


def test_the_pulsed_gates_window_is_bounded_by_the_probes_lays_and_closes_at_its_taking(
    tmp_path, monkeypatch
):
    """The pulsed gate (ALGEBRA.md, The pulsed gate, the window of a body bounded by the lays' schedule; the two hands of 2026-10-03, #1572 comments 5967698811, 5967783614 and 5967913000; src/event_universe/meeting.py `laid_whole`, `probe_arrived`, `probe_click`, loader/messages.py `wholes_of`, loader/draw.py `generator_of`): the Zeno body at one Node of a minimal periodic box with no drive laid, a probe (a neutral real line) laid whole by the count at its Node at the ticks 3 and 7, the body's transition of g into itself at the probe's family and its generator alone. (i) The loader: a `window` beside the probe, a `weight` on the probe's transition, `whole` or `count` without `tick`, a tick beyond the run and a body without a probe lacking its window are refused by name; the body's draw is the generator and a window's draw a Draw. (ii) The window stands from the lay to the probe's tick: no close before it, the generator at its seed, the body dark under the probe alone; at the tick the probe is laid by the count ((128, 128) on its line at the Node, its count 1, one lay line), the window closes and the one draw reads the labels' squares: from g untouched the probe's click is certain, the body re-laid in g, one jump line labelled NODEREADER with the window [1, 3], the body's proper time 3 and the window's index 1, `taken` and `given` the probe's family, no face on the probe and its count standing. (iii) With the labels carried to e by hand (the turn's cos^2 0, sin^2 the unit) the drive's taking is certain at the next probe: the jump at 7 reads e by the drive with the window [4, 7] and the index 2, the drive's count down by one and its two faces at the Node, the probe's record untouched again; the body's windows 2 and the scale of its reference records the run's ticks' (`resonance.scale_of`). (iv) On the shipped pulsed world `zeno_pulsed_4` the probe's ticks are 192, 384, 576 and 768 and the back-in-time gate reads MATCH over 200 intervals, across the first probe's lay and its click."""
    folder = EVENTS / "zeno_pulsed"
    universe = json.loads((folder / "pulsed_atom.json").read_text(encoding="utf-8"))
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    draw = {"seed": 25, "multiplier": 6364136223846793005, "increment": 1442695040888963407}
    parts = [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}]
    ways, drive = (("g", "e"), ("e", "g")), {"drive": "pulse", "weight": 1, "resonance": [2, 3]}
    turns, probe = [{"from": a, "to": b, **drive} for a, b in ways], {"from": "g", "to": "g"}
    probe["drive"] = "probe"
    region = [{"node": [1, 1, 1], "weight": 1}, {"node": [2, 1, 1], "weight": 1}]  # two adjacent Nodes
    record = {"family": "atom", "nodes": region, "parts": parts}
    record.update(transitions=[*turns, probe], rates=[], node_reader=draw)
    lays = [{"family": "probe", "whole": [1, 1, 1], "count": 1, "tick": t} for t in (3, 7)]
    world = dict(shape=[3, 3, 3], boundary=dict(x="periodic", y="periodic", z="periodic"), ticks=9)
    world.update(universe="u.json", engine="e.json", bodies=[record], messages=lays, node_readers=[])
    (path := tmp_path / "w.json").write_text(json.dumps(world), encoding="utf-8")
    families, quanta = universe_of(universe)[1], {"atom": 0, "pulse": 1, "probe": 2}
    wrong = {"beside a probe": {**record, "node_reader": {**draw, "window": 1}}}
    wrong["no weight"] = {**record, "transitions": [*turns, {**probe, "weight": 1}]}
    wrong["lacks the key 'window'"] = {**record, "transitions": turns}
    for word, body in wrong.items():
        refused(word, node_reader_of, body, "bodies[0]", families, 0, quanta, 1)
    assert node_reader_of(record, "bodies[0]", families, 0, quanta, 1).draw == Generator(**draw)
    assert isinstance(draw_of({**draw, "window": 1}, "node_reader"), Draw)
    untimed = {k: v for k, v in lays[0].items() if k != "tick"}
    for word, message in (("without `tick`", untimed), ("tick", {**lays[0], "tick": 10})):
        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps({**world, "messages": [message]}), encoding="utf-8")
        refused(word, load_world, bad)
    board = GameBoard(load_world(path), (lines := []).append)
    names = [f.name for f in board.families]
    pulse, probed = names.index("pulse"), names.index("probe")
    here, books = tuple(np.add([1, 1, 1], board.offset)), board.credit.bodies[0]
    room, bound = board.world.width, board.world.amplitude_bound
    assert books.references[0].scale == resonance.scale_of(room, bound, 9)
    for tick in (1, 2):  # the window stands: no close, no draw, no lay
        board.step()
        assert (books.elapsed, books.state, books.windows) == (tick, 25, 0)
    assert not lines and meeting.dark(board, books) and board.credit.counts[probed] == 0
    board.step()  # the probe's tick: the lay by the count, the close, the probe's click certain from g
    line, wall = board.states[probed].lines[0], books.labels[0]
    assert (int(line.now[here]), int(line.before[here])) == (128, 128)
    assert (board.credit.counts[probed], int(board.quanta(probed)[0][here])) == (1, 1)
    jumps = [x for x in lines if x["event"] == "credit"]
    keys = ("label", "tick", "window", "proper", "windows", "realised", "before", "taken", "given")
    click = ("NODEREADER", 3, [1, 3], 3, 1, "g", "g", "probe", "probe")
    assert [tuple(x[k] for k in keys) for x in jumps] == [click] and books.labels == [wall, 0]
    laid = [(x["family"], x["tick"]) for x in lines if x["event"] == "lay"]
    assert laid == [
        ("probe", 3),
        ("atom", 3),
        ("atom", 3),
    ]  # the probe's lay, then the re-lay in g at both Nodes
    assert not board.credit.faces and (books.elapsed, books.windows, books.part) == (0, 1, 0)
    assert books.state != 25
    board.credit.counts[pulse] = 1  # one quantum of the drive in the books
    books.labels, state = [0, wall], books.state  # the labels carried to e by hand: cos^2 0
    for _ in range(4):
        board.step()
    jumps = [x for x in lines if x["event"] == "credit" and x["label"] == "NODEREADER"]
    taking = ("NODEREADER", 7, [4, 7], 7, 2, "e", "g", "pulse", None)
    assert [tuple(x[k] for k in keys) for x in jumps[1:]] == [taking] and state != books.state
    assert (books.part, board.credit.counts[pulse], board.credit.counts[probed]) == (1, 0, 2)
    faces = {(f.family, f.tick) for faces in board.credit.faces.values() for f in faces}
    assert faces == {(pulse, 8), (pulse, 9)} and (books.windows, books.clock) == (2, [7, 0])
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", ROOT)
    pulsed = folder / "zeno_pulsed_4.json"
    shipped = json.loads(pulsed.read_text(encoding="utf-8"))
    assert [m["tick"] for m in shipped["messages"] if "tick" in m] == [192, 384, 576, 768]
    assert BACK.verdict(GameBoard(load_world(pulsed)), 200)["verdict"] == "MATCH"


def test_a_taking_from_a_dense_record_is_read_in_the_books_and_writes_nothing():
    """The undepleted beam (ALGEBRA.md, The click writes on the GameBoard; the two hands' line at the owner's word for the simple solution; `meeting.faced`, `credit.Books.deficits`, `GameBoard.books`): the shipped Zeno n = 2 world, whose drive holds about 2.6 quanta's share at the reader's Node (the booked share the credit reads there above the record's quantum W_rec), at the trial seed 2, beside its untouched twin. The taking at 24, g to e climbing, books no face and no front, the drive's three arrays stand bit for bit as the twin's over the run (the drive reads no holder: the same Rule3 step), so its share at the Node and over the board is the twin's, printed; the count down by one, the deficit 1 and the share in quanta the count plus the deficit within the share's drift over the run in quanta (the books' `drift` over W_c and one quantum of the reading's rounding, printed); the return, e to g descending by the pulse at a later window's close (`meeting.exchange`, stimulated emission), gives the quantum back into the dense pulse: nothing laid, no source in time, the count back to the start and the deficit 0, the arrays the twin's still; the back-in-time gate MATCH across the taking and the return, the atom's lays crossed from their lines."""
    zeno = EVENTS / "zeno" / "zeno_2.json"
    board, twin = GameBoard(load_world(zeno), (lines := []).append), GameBoard(load_world(zeno))
    board.credit.bodies[0].state, pulse = 2, [f.name for f in board.families].index("pulse")
    at, count, unit = (4, 4, 2), board.credit.counts[pulse], board.credit.units[pulse]
    for _ in range(24):
        board.step(), twin.step()
    booked_share = int(board.share_of(pulse)[0][at])
    assert booked_share > unit  # dense: the booked share at the Node above the record's quantum
    returns: list[dict] = []
    while board.tick < 480 and not returns:
        board.step(), twin.step()
        for key in ("now", "before", "remainder"):
            mine, its = (getattr(b.states[pulse].lines[0], key) for b in (board, twin))
            assert np.array_equal(mine, its)  # the undepleted beam: nothing written on the drive
        if board.tick == 48:
            books, its_books = board.books()["pulse"], twin.books()["pulse"]
        returns = [x for x in lines if x["event"] == "credit" and x["given"] == "pulse"]
    jumps = [x for x in lines if x["event"] == "credit" and x["label"] == "NODEREADER" and x["taken"]]
    assert [x["tick"] for x in jumps][:1] == [24] and jumps[0]["taken"] == "pulse"
    assert not any(f.family == pulse for faces in board.credit.faces.values() for f in faces)
    assert not board.credit.fronts and not board.credit.sources
    print(
        f"the Zeno drive's booked share at the Node {booked_share} over W_rec {unit}, the books {books}"
    )
    assert (books["count"], books["deficit"], books["quanta"]) == (count - 1, 1, its_books["quanta"])
    within = abs(books["drift"]) // count_wall(board.families[pulse], board.world.quantum_action) + 1
    print(f"the share in quanta {books['quanta']} against the count plus the deficit within {within}")
    assert abs(books["quanta"] - books["count"] - books["deficit"]) <= within
    assert books["share"] == its_books["share"] and books["drift"] == its_books["drift"]
    cycled = board.books()["pulse"]
    print(f"the return at {returns[0]['tick']} after {len(jumps)} takings: the books {cycled}")
    assert (cycled["count"], cycled["deficit"]) == (count - len(jumps) + 1, len(jumps) - 1)
    gate = GameBoard(load_world(zeno))
    gate.credit.bodies[0].state = 2
    assert (
        BACK.verdict(gate, returns[0]["tick"])["verdict"] == "MATCH"
    )  # across the taking and the return


def test_a_giving_into_a_dense_record_is_read_in_the_books_and_lays_nothing(tmp_path):
    """The undepleted beam at the giving (ALGEBRA.md, The click writes on the GameBoard; the two hands' line: a quantum given into a beam adds to the mode coherently in nature, and a one-Node lay into a dense record is the same point defect the dense hole was; `meeting.written`, `meeting.faced`, `giving.given_quantum`): the Zeno n = 2 world with a rate e to g at the lifetime 8 giving to the pulse itself, the dense record at the reader's Node, at the trial seed 2, beside the pulse alone (the return by the rate or by the transition's descent, `meeting.exchange`, both givings into the beam): the takings and the giving write nothing on the pulse, whose three arrays stand bit for bit as the pulse alone over the run, no source in time begins and no lay line names the pulse, the count down by one per taking and up by one per giving, the deficit the takings less the givings (the books' line printed); the sparse giving's own tests stand in `tests/test_the_giving.py`."""
    world = json.loads((EVENTS / "zeno" / "zeno_2.json").read_text(encoding="utf-8"))
    world["bodies"][0]["rates"] = [{"from": "e", "to": "g", "lifetime": 8, "gives_to": "pulse"}]
    world["ticks"] = 480
    (path := tmp_path / "zeno_rate.json").write_text(json.dumps(world), encoding="utf-8")
    (alone := tmp_path / "pulse_alone.json").write_text(
        json.dumps({**world, "bodies": []}), encoding="utf-8"
    )
    TOOL.main(["--input", str(path)]), TOOL.main(["--input", str(alone)])
    board, twin = GameBoard(load_world(path), (lines := []).append), GameBoard(load_world(alone))
    board.credit.bodies[0].state, pulse = 2, [f.name for f in board.families].index("pulse")
    count, given = board.credit.counts[pulse], []
    while board.tick < world["ticks"] and not given:
        board.step(), twin.step()
        given = [c for c in lines if c["event"] == "credit" and c["given"] == "pulse"]
    taken = [c for c in lines if c["event"] == "credit" and c["taken"] == "pulse"]
    assert given and taken and given[0]["tick"] > taken[0]["tick"]  # a taking, then the giving back
    for key in ("now", "before", "remainder"):
        assert np.array_equal(
            getattr(board.states[pulse].lines[0], key), getattr(twin.states[pulse].lines[0], key)
        )
    assert not board.credit.sources and not any(
        c["family"] == "pulse" for c in lines if c["event"] == "lay"
    )
    books = board.books()["pulse"]
    print(
        f"the Zeno pulse after {len(taken)} takings and {len(given)} giving at {board.tick}: the books {books}"
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
    world = json.loads((EVENTS / "zeno" / "zeno_1.json").read_text(encoding="utf-8"))
    world.update(bodies=[], messages=[], node_readers=[], ticks=200)
    path = tmp_path / "box.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    board = GameBoard(load_world(path))
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
    laid_by_count(board, meeting.Item(pulse, None, None, 1, ((4, 4, 2),), pair=(6000, 6000)))
    for _ in range(200):
        board.step()
    largest = int(np.abs(board.states[pulse].lines[0].now).max())
    print(f"the lone quantum's largest level at the interval 200 on the box {board.shape}: {largest}")
    assert largest < 300, largest  # bounded: 50 by the lattice's rule on this box, 6,268 under the floor


def test_the_taking_removes_the_photon_and_the_front_leaves_the_board_dark():
    """The committed one-photon world at the lay without the uniform mode (ALGEBRA.md, The click writes on the GameBoard (3) and (6)): one atom takes at the window's close and the count falls to 0; the light's share over the GameBoard never rises above the lay's by more than the hole's and the front's transient (one part in seven, the known one), and once the front has swept both packets the share is 0 exactly, the board dark."""
    board = GameBoard(load_world(EVENTS / "anticoincidence" / "one_photon.json"), (lines := []).append)
    photon, shares = [f.name for f in board.families].index("photon"), []
    laid = board.books()["photon"]["share"]
    for _ in range(200):
        board.step()
        shares.append(board.books()["photon"]["share"])
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEREADER" and c["taken"]]
    assert len(credits) == 1 and credits[0]["tick"] == 48 and board.credit.counts[photon] == 0
    assert laid > 0 and max(shares) * 7 <= laid * 8 and shares[-1] == 0
    assert all(
        line["event"] == "erasure"
        for line in lines
        if line["tick"] > 48 and line["event"] not in ("face", "credit", "lay")
    )


def test_a_body_among_several_drives_takes_each_by_its_own_transfer_share(tmp_path, monkeypatch):
    """The taking among several drives (ALGEBRA.md, The click writes on the GameBoard (f); The two-mode line; `meeting.turned_labels`, `took`): two atoms, each with the transitions g to e by `photon` and by `photon_b`, one packet of each laid at the centre toward one atom, the left atom's window closing first while `photon`'s count stands: a drive's weight at a body is its own transfer share, so the left atom takes `photon_b`, the drive that passed it, and the right `photon`; with `photon_b` removed the one drive's share is the composed label squared bit for bit at both atoms, and `photon`'s share at each atom is the same number in both worlds."""
    seen, turned = [], meeting.turned_labels

    def kept(board, books):  # the labels and the shares at the window's close, before the click
        turned(board, books)
        shares = getattr(books, "shares", {})  # none before the fix: the clicks' assertion fails
        seen.append((list(books.labels), {t.drive: s for t, s in shares.items()}))

    monkeypatch.setattr(meeting, "turned_labels", kept)
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
    folder, clicks = EVENTS / "anticoincidence", {}
    for drives in (("photon", "photon_b"), ("photon",)):
        universe = json.loads((folder / "two_atoms.json").read_text(encoding="utf-8"))
        universe["families"] += [{**universe["families"][1], "name": d} for d in drives[1:]]
        (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
        world = json.loads((folder / "two_photons.json").read_text(encoding="utf-8"))
        world.update(shape=[64, 1, 1], universe="u.json", engine="e.json")
        for body, at, window in zip(world["bodies"], (15, 47), (44, 56), strict=True):
            body["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in (at, at + 1)]
            body["node_reader"] = {**body["node_reader"], "window": window}
            body["transitions"] = [{**body["transitions"][0], "drive": d} for d in drives]
        for message, x, family in zip(world["messages"], (32, 31), ("photon", "photon_b"), strict=True):
            message.update(top={**message["top"], "x": [x, x]}, family=family)
        world["messages"] = [m for m in world["messages"] if m["family"] in drives]
        (path := tmp_path / f"{len(drives)}.json").write_text(json.dumps(world), encoding="utf-8")
        TOOL.main(["--input", str(path)])
        board = GameBoard(load_world(path), (lines := []).append)
        while board.tick < 56:
            board.step()
        clicks[drives] = [(c["tick"], c["node_reader"], c["taken"]) for c in lines if c.get("taken")]
    assert clicks["photon", "photon_b"] == [(44, "body 0", "photon_b"), (56, "body 1", "photon")]
    assert clicks[("photon",)] == [(56, "body 1", "photon")]
    two, one = seen[:2], seen[2:]  # the closes at 44 and 56 per world; the drives photon 1, photon_b 2
    print(f"takings by the drives' shares {clicks['photon', 'photon_b']}; the left atom's {two[0][1]}")
    assert [labels[1] ** 2 for labels, _ in one] == [shares[1] for _, shares in one]  # one drive
    assert [shares[1] for _, shares in two] == [shares[1] for _, shares in one]  # photon's own share
    assert two[0][1][1] * 1000 < two[0][1][2] and two[1][1][2] * 1000 < two[1][1][1]
