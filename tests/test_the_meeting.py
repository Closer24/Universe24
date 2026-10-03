"""The meeting's gates (ALGEBRA.md #the-click-is-the-meeting, the pair's form and the GHZ gate; HIGHLIGHTS.md, One experiment and one gate): a record of several parts laid as one event and never summed at a Node, the instrument's read of the parts' signed level sums (the parts line) and the joint-share reader pairing the parts through the root across the sides (tools/bell_gate.py): the exact algebra at Bell's four settings and at the GHZ patterns, the local credits as the fence, the determinism of equal parts, and the two gates' four worlds each (examples/events/bell, examples/events/ghz) end to end with the back-in-time gate MATCH; Bell and the GHZ are gates and never results. The click written on the GameBoard (src/event_universe/credit.py, features/click): the instrument's draw inside the run and its write at one Node, the board exact between clicks."""

import ast
import json
from fractions import Fraction

import numpy as np

from event_universe import meeting, node, world_files
from event_universe.features.click import amplitude
from event_universe.game_board import GameBoard
from event_universe.loader.instrument import (
    basis_of,
    instrument_of,
    node_instrument_of,
    pattern_of,
    patterns_of_the_law,
)
from event_universe.loader.universe import shape_of, universe_of
from event_universe.loader.world import bodies_of, detectors_of
from event_universe.world_files import load_world
from tests.laws import BACK, EVENTS, ROOT, RUN, TOOL, TOP, booked, load_file, refused

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
        equal = all(len(set(map(tuple, p["levels"]))) == 1 and p["label"] == "DETECTOR" for p in parts)
        credits = [line for line in lines if line["event"] == "credit"]
        assert parts and equal and credits and all(c["tick"] == c["window"][1] for c in credits)
        board = GameBoard(load_world(folder / f"{name}.json"))
        assert BACK.verdict(board, board.world.ticks - 2)["verdict"] == "MATCH"  # exact before the click
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
    refused("setting", GATE.ports_of, (1,), PAIR)
    refused("orthogonal", GATE.ports_of, A, ((1, 1),))
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
    fenced = [GATE.combination(credits(three, MERMIN[0], PATTERNS, f)[1], MERMIN[1]) for f in FENCE]
    assert fenced == [-1] * len(FENCE)
    refused(r"\[0, 0\]", pattern_of, [[1, 0], [0, 0]], "detectors[0].pattern", (1, 0))
    row = {"name": "d", "positions": [[0, 0, 0], [1, 0, 0]], "pattern": [[1, 0]], "transition": TOP}
    refused("none is declared", detectors_of, [row], (2, 1, 1), 0, (), ())
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
    """The click written on the GameBoard (ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision of 2026-10-02; features/click, src/event_universe/credit.py): Bell's shipped world a b with the instrument's window cut to 40 over its 100 intervals, beside its twin without the key. (i) One credit line per side at 40 and at 80: the result the window, the region, the port realised, the parts kept and the count 1, the record's count down by one per window, the one Node beside as a GameBoard diagnostic; at 40 the two boards differ at the two written Nodes alone (the one-Node test), and at the written Node every line of the record is 0 in its three arrays (the hole, as the receding face removes a share) where the twin's levels stand. (ii) The inverse is exact between clicks: from 100 back to 80 every array returns bit for bit, the step back across the click misses, and the twin goes from 40 back to the lay, MATCH. (iii) The record's count: at 0 the instrument credits nothing over the same 40 intervals, the reports the same lines with no credit line among them; the `instrument` key refused by name with a window of 0 and without its seed."""
    world = json.loads((EVENTS / "bell" / "bell_a_b.json").read_text(encoding="utf-8"))
    world["instrument"]["window"], draw = 40, dict(world["instrument"])
    (cut := tmp_path / "cut.json").write_text(json.dumps(world), encoding="utf-8")
    world.pop("instrument")
    (twin := tmp_path / "twin.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(cut)]), TOOL.main(["--input", str(twin)])
    board, plain = GameBoard(load_world(cut), (lines := []).append), GameBoard(load_world(twin))
    kept = {}
    for _ in range(100):
        board.step(), kept.__setitem__(board.tick, BACK.snapshot(board))
        board.tick <= 41 and plain.step()
    credits = [line for line in lines if line["event"] == "credit"]
    pair = next(i for i, f in enumerate(board.families) if f.name == "light_pair")
    at = [(c["tick"], c["detector"], c["count"], c["window"][0], c["left"]) for c in credits]
    left = board.credit.counts[pair]
    assert at == [(40, "left", 1, 1, left + 1), (40, "right", 1, 1, left + 1)] + at[2:]
    assert at[2:] == [(80, "left", 1, 41, left), (80, "right", 1, 41, left)]
    was, now = dict(p for f in kept[41] for p in f), dict(p for f in BACK.snapshot(plain) for p in f)
    assert {c["node"]["label"] for c in credits} == {"GAMEBOARD"}  # the one Node a diagnostic beside
    report = set("event label tick family detector window realised kept count left".split())
    assert all(set(c) == report | {"node"} and c["label"] == "DETECTOR" for c in credits)  # never a Node
    written = {tuple(np.add(c["node"]["at"], plain.offset)) for c in credits[:2]}
    assert {tuple(map(int, at)) for k in was for at in np.argwhere(was[k] != now[k])} == written
    w, keys = (
        tuple(np.add(credits[0]["node"]["at"], plain.offset)),
        [k for k in was if "light_pair" in k],
    )
    assert len(credits[0]["kept"]) == 1 and credits[1]["kept"] == [0, 1]
    levels = [k for k in keys if k.endswith("now") or k.endswith("before")]  # the face: now 0 at 41
    assert all(was[k][w] == 0 for k in levels if k.endswith("now")) and any(now[k][w] != 0 for k in keys)
    assert all(dict(p for f in kept[42] for p in f)[k][w] == 0 for k in levels)  # both levels 0 at 42
    for _ in range(99):
        board.step_inverse()  # the faces presented again: the inverse crosses the clicks bit for bit
        assert BACK.first_difference(kept[board.tick], BACK.snapshot(board)) is None
    assert BACK.verdict(GameBoard(load_world(twin)), 39)["verdict"] == "MATCH"
    empty = GameBoard(load_world(cut), (none := []).append)
    empty.credit.counts[pair] = 0
    for _ in range(40):
        empty.step()
    before = [line for line in lines if line["tick"] <= 40 and line["event"] != "credit"]
    assert none == before and empty.credit.state == draw["seed"]  # no credit line, no draw consumed
    refused("window", instrument_of, {**draw, "window": 0}, "instrument")
    refused("lacks", instrument_of, {"window": 1}, "instrument")


def test_a_record_declared_an_instrument_at_one_node_takes_gives_and_stays(tmp_path, monkeypatch):
    """The meeting at a Node (ALGEBRA.md, The click writes on the GameBoard (j) and (k); the owner's words of 2026-10-03; src/event_universe/meeting.py, loader/instrument.py): a record of a plane family of three parts declared at one Node in its parts (S at the count 1, P and D at 0) with a transition S to P fed by a drive's plane wave, a giving P to S at the lifetime 2 onto a light row and its own window of 1, beside a counter with the world's instrument. (i) The loader: the parts' count in two parts, a transition naming no part, a weight of 0, a rate without the instrument and a record of two Nodes are refused by name; the generator lays the drive and no entry for the record. (ii) The lay: the record's share reads 1 at its Node in the S lines alone, and its Links cut it stays there (the twin without the instrument MATCH over 30 intervals back to the lay). (iii) The clicks: the first jump takes the drive's quantum into P at the Node, the drive's record 0 there in its three arrays (the hole) and its count in the books down by one, the record's P lines carrying the count and the S lines 0, the two boards differing at that Node alone; a later jump gives one quantum to the light row and the counter credits it at a window's end (the world of 20 intervals, the counter's window 15), and where the credit took the row's count to 0 the erasing front begins at the entry Node: one erasure line per interval at the distances 1 to 5, and the same run without the front (its fronts dropped each interval) holds every level beyond the ball, the Link-metric distance above the intervals since the click, bit for bit (the front invisible ahead of itself); every jump names the one Node as a GameBoard diagnostic, and the null window's re-lays that changed a level leave their own GAMEBOARD-labelled jump lines. (iv) The acts from outside the Node as lines (the mathematician's 193 and 195 with the advisor's second, two hands): every line a lay changed at the Node writes one GAMEBOARD-labelled `lay` line with its levels and remainder before and after (the taking's four ion lines, the giving's light line, the null windows'), every face presented writes one `face` line carrying the value the books hold; the back-in-time gate (tools/back_in_time.py) reads MATCH over the whole run across the takings, the givings, the null windows, the credit and the fronts, the faces presented from the lines and the lays undone from theirs, and on the shipped Zeno and anticoincidence worlds, one step more returning the start. (v) The booking identity per act at every step on the ion, the drive and the light (tests/laws.py, `booked`): the share identity within the floors plus the face term at the hole's two intervals and at every shell of the front, and the lays' change of the share form local to the Node and its six neighbours, exact. (vi) The conversion's list through the one act: the drive at -1 and two other rows at +1 at the Node, no draw and the generator's state untouched, the counts moved by the row, one whole quantum laid on each row at the massless rotation, the two levels alike, and the drive's hole after two intervals. (vii) The generator consumed the same whether or not a count-0 record's inflow is booked: the anticoincidence world with the first record's window at 10, run with the front and without it, gives the same one taking and the same generator states, the second record's its seed (its open window after the click draws nothing), while the light's level at its Node is erased in the one run and stands in the other. (viii) The one-in-flight limit is not built, by name: the light row's count rises by one per giving before the counter's window and no giving is refused; the Zeno world gives nothing and its drive's count stands above 1."""
    universe = json.loads((EVENTS / "shelved_ion" / "mercury_ion.json").read_text(encoding="utf-8"))
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    at, parts = [3, 3, 2], [{"part": k, "name": n, "count": int(k == 0)} for k, n in enumerate("SPD")]
    draw = {"window": 1, "seed": 25, "multiplier": 6364136223846793005, "increment": 1}
    record = {"family": "ion", "nodes": [{"node": at, "count": 1}], "parts": parts, "instrument": draw}
    record["transitions"] = [
        {"from": "S", "to": "P", "drive": "strong_drive", "weight": 1, "resonance": [2, 3]}
    ]
    record["rates"] = [{"from": "P", "to": "S", "lifetime": 2, "gives_to": "fluorescence"}]
    drive = {"family": "strong_drive", "along": "x", "wave": [1, 2], "amplitude": 600}
    drive.update(top={"x": [0, 5], "y": [0, 5], "z": [0, 3]}, edge={"x": 0, "y": 0, "z": 0})
    counter = {
        "name": "counter",
        "positions": [[0, y, z] for y in range(6) for z in range(4)],
        "transition": TOP,
    }
    world = dict(shape=[6, 6, 4], boundary=dict(x="periodic", y="periodic", z="periodic"), ticks=23)
    world.update(universe="u.json", engine="e.json", measured=[record], messages=[drive])
    world.update(detectors=[counter], instrument={**draw, "window": 18, "seed": 24})
    (path := tmp_path / "w.json").write_text(json.dumps(world), encoding="utf-8")
    twin = {k: v for k, v in world.items() if k != "instrument"}
    twin["measured"] = [{k: v for k, v in record.items() if k in ("family", "nodes", "parts")}]
    (plain := tmp_path / "t.json").write_text(json.dumps(twin), encoding="utf-8")
    TOOL.main(["--input", str(path)]), TOOL.main(["--input", str(plain)])
    assert json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"] == []
    families, quanta = universe_of(universe)[1], {"ion": 0, "strong_drive": 1, "fluorescence": 3}
    wrong = {"one part": {**record, "parts": [{**p, "count": 1} for p in parts]}}
    wrong["parts are"] = {**record, "transitions": [{**record["transitions"][0], "to": "X"}]}
    wrong["weight"] = {**record, "transitions": [{**record["transitions"][0], "weight": 0}]}
    wrong["no `instrument`"] = {k: v for k, v in record.items() if k != "instrument"}
    for word, body in wrong.items():
        refused(word, node_instrument_of, body, "measured[0]", families[0], 0, quanta, 1)
    two = {**record, "nodes": record["nodes"] + [{"node": [3, 4, 2], "count": 1}]}
    refused("one Node", bodies_of, [two], None, "", families, (6, 6, 4), 9000, ())
    board, other = GameBoard(load_world(path), (lines := []).append), GameBoard(load_world(plain))
    names = [f.name for f in board.families]
    ion, drv, light = (names.index(n) for n in ("ion", "strong_drive", "fluorescence"))
    here, gamma, unit, weak = tuple(at), board.world.node_clock, board.unit, names.index("weak_drive")
    assert int(board.quanta(ion)[0][here]) == 1 == int(board.quanta(ion)[0].sum())
    assert all(int(line.now[here]) == 0 for line in board.states[ion].lines[2:])
    assert BACK.verdict(GameBoard(load_world(plain)), 30)["verdict"] == "MATCH"
    clicks = [line for line in lines if line["event"] == "jump" and line["label"] == "DETECTOR"]
    while not clicks:
        booked(board, monkeypatch, ion, drv, light), other.step()  # the booking identity at every act
        clicks = [line for line in lines if line["event"] == "jump" and line["label"] == "DETECTOR"]
    first, click = clicks[0], ("P", "S", "strong_drive", None)
    assert (first["realised"], first["left"], first["taken"], first["given"]) == click
    assert first["node"] == {"label": "GAMEBOARD", "at": at} and first["tick"] == board.tick
    was = dict(p for f in BACK.snapshot(other) for p in f)
    now = dict(p for f in BACK.snapshot(board) for p in f)
    assert {tuple(map(int, w)) for k in was for w in np.argwhere(was[k] != now[k])} == {here}
    assert board.credit.counts[drv] == other.credit.counts[drv] - 1
    in_s, in_p = (any(int(x.now[here]) for x in board.states[ion].lines[k : k + 2]) for k in (0, 2))
    assert int(board.quanta(ion)[0][here]) == 1 and in_p and not in_s
    p_re, p_im = (int(now[f"ion.lines[{k}].now"][here]) for k in (2, 3))  # the part entered, after
    size = amplitude(1, board.world.quantum_action, board.families[ion].pair)  # one quantum laid in P
    assert abs(p_re * p_re + p_im * p_im - size * size) <= 2 * size and (p_re, p_im) != (size, 0)
    walls = {k: node.rule_of(board.families[k], gamma, 0, None, unit)[2] for k in (ion, drv)}
    assert int(now["ion.lines[2].remainder"][here]) == walls[ion] // 2  # the taker at the lay's origin
    [
        booked(board, monkeypatch, ion, drv, light) for _ in (0, 1)
    ]  # the hole: the face term, two intervals
    hole = board.states[drv].lines[0]
    assert (int(hole.now[here]), int(hole.before[here])) == (0, 0)
    assert 0 <= int(hole.remainder[here]) < walls[drv]  # the giver's remainder Rule3's own
    still = GameBoard(load_world(path))  # the same run without the front: its fronts dropped each step
    for _ in range(still.tick, board.tick):
        still.step()
    extent = np.reshape(board.shape, (3, 1, 1, 1))
    for _ in range(board.tick, 23):
        booked(board, monkeypatch, ion, drv, light), still.step(), still.credit.fronts.clear()
        for index, origin, since in board.credit.fronts:  # the theorem: nothing differs beyond the ball
            gap = np.abs(np.indices(board.shape) - np.reshape(origin, (3, 1, 1, 1)))
            far = np.minimum(gap, extent - gap).sum(0) > board.tick - since
            for a, b in zip(board.states[index].lines, still.states[index].lines, strict=True):
                assert (a.now[far] == b.now[far]).all() and (a.before[far] == b.before[far]).all()
    given = [line for line in lines if line["event"] == "jump" and line["given"]]
    nulls = [line for line in lines if line["event"] == "jump" and line["label"] == "GAMEBOARD"]
    assert all(n["realised"] == n["left"] and "levels" not in n["node"] for n in nulls)
    credits = [line for line in lines if line["event"] == "credit" and line["family"] == "fluorescence"]
    erased = [line for line in lines if line["event"] == "erasure"]
    assert given and given[0]["left"] == "P" and credits and credits[0]["tick"] == 18
    assert board.credit.counts[light] + len(credits) == len(given)
    first_front = [e["distance"] for e in erased if e["origin"] == erased[0]["origin"]]
    assert erased and first_front == list(range(1, 6))
    assert all(e["family"] == "fluorescence" and e["label"] == "GAMEBOARD" for e in erased)
    assert all(e["nodes"] > 0 for e in erased)
    lays, faces = [x for x in lines if x["event"] == "lay"], [x for x in lines if x["event"] == "face"]
    kinds = {
        t: {(x["family"], x["line"]) for x in lays if x["tick"] == t} for t in {x["tick"] for x in lays}
    }
    assert kinds[first["tick"]] == {("ion", k) for k in range(4)}  # the taking: two parts, four lines
    assert all(("fluorescence", 0) in kinds[g["tick"]] for g in given)  # every giving laid its quantum
    assert {x["label"] for x in lays} == {"GAMEBOARD"} and board.credit.counts[light] > 1  # none refused
    key, kept = ("line", "port", "tick", "value"), sum(board.credit.faces.values(), [])
    faced = {(f.family, f.at, *(getattr(f, k) for k in key)) for f in kept}
    logged = {(names.index(x["family"]), tuple(x["node"]["at"]), *(x[k] for k in key)) for x in faces}
    assert logged == {f for f in faced if f[4] <= board.tick} and logged  # the lines the books' values
    assert BACK.verdict(GameBoard(load_world(path)), 23)["verdict"] == "MATCH"  # every act crossed
    fresh = GameBoard(load_world(path), (conv := []).append)  # the conversion's list through the one act
    counts, items = dict(fresh.credit.counts), [meeting.Item(drv, None, None, -1, (here,))]
    items += [meeting.Item(k, None, None, 1, (here,), TOP_PAIR, 1) for k in (weak, light)]
    assert meeting.click(fresh, 7, None, [1], [items]) == (0, 7)  # one outcome: no draw, the state kept
    moved = {k: fresh.credit.counts[k] - counts[k] for k in (drv, weak, light)}  # the counts by the row
    assert moved == {drv: -1, weak: 1, light: 1} and int(fresh.quanta(light)[0].sum()) == 1
    laid = [(x["family"], x["line"], [x["after"][k] - x["before"][k] for k in (0, 1)]) for x in conv]
    glow = amplitude(
        1, fresh.world.quantum_action, TOP_PAIR
    )  # one quantum at the band's top in one interval
    assert laid == [("weak_drive", 0, [glow, 0]), ("fluorescence", 0, [glow, 0])]
    fresh.step(), fresh.step()
    assert all(int(getattr(fresh.states[drv].lines[0], k)[here]) == 0 for k in ("now", "before"))
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", ROOT)  # the shipped instrument worlds
    zeno, photon = EVENTS / "zeno" / "zeno_4.json", EVENTS / "anticoincidence" / "one_photon.json"
    loaded = BACK.snapshot(z := GameBoard(load_world(zeno), (zlines := []).append))
    assert BACK.verdict(z, 48)["verdict"] == "MATCH" and z.step_inverse() is None  # the lays, the start
    assert BACK.first_difference(loaded, BACK.snapshot(z)) is None and z.tick == 0
    assert any(x["event"] == "jump" for x in zlines) and not any(x.get("given") for x in zlines)
    assert (
        max(z.credit.counts.values()) > 1
    )  # the drive's record of many quanta, no giving in this world
    assert BACK.verdict(GameBoard(load_world(photon)), 40)["verdict"] == "MATCH"
    world = json.loads(photon.read_text(encoding="utf-8"))  # a window open after the click
    world["measured"][0]["instrument"]["window"], runs = 10, []
    (split := tmp_path / "split.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(split)])
    for front in (True, False):  # the count-0 record's inflow erased by the front, or standing
        b = GameBoard(load_world(split), (sl := []).append)
        for _ in range(40):
            b.step(), front or b.credit.fronts.clear()
        ph, b_at = [f.name for f in b.families].index("photon"), world["measured"][1]["nodes"][0]["node"]
        took = [(x["tick"], x["detector"]) for x in sl if x["event"] == "jump" and x["taken"]]
        level = int(b.states[ph].lines[0].now[tuple(np.add(b_at, b.offset))])
        runs.append((took, [k.state for k in b.credit.bodies], b.credit.counts[ph], level))
    assert runs[0][:3] == runs[1][:3] and len(runs[0][0]) == 1  # one taking, the generators alike
    assert runs[0][1][1] == world["measured"][1]["instrument"]["seed"] and runs[0][2] == 0  # no draw
    assert runs[0][3] == 0 != runs[1][3]  # the count-0 wave erased, or standing
    writers = set()  # every function of the engine that assigns a record's lines
    for module in (ROOT / "src" / "event_universe").rglob("*.py"):
        for f in ast.walk(ast.parse(module.read_text(encoding="utf-8"))):
            for n in (n for n in ast.walk(f) if isinstance(n, (ast.Assign, ast.AugAssign))):
                targets = n.targets if isinstance(n, ast.Assign) else [n.target]
                if isinstance(f, ast.FunctionDef) and any(".lines" in ast.unparse(t) for t in targets):
                    writers.add((module.stem, f.name))
    rule3 = {("game_board", "step"), ("game_board", "step_inverse"), ("game_board", "hold")}
    lay = {("game_board", "start"), ("bookings", "booked_sources"), ("growth", "resized")}
    lay |= {("meeting", "relaid"), ("giving", "laid_increment")}
    assert writers == rule3 | lay  # nothing writes a NodeState but Rule3, the lay and the face
