"""The meeting's gates (ALGEBRA.md #the-click-is-the-meeting, the pair's form and the GHZ gate; HIGHLIGHTS.md, One experiment and one gate): a record of several parts laid as one event and never summed at a Node, the instrument's read of the parts' signed level sums (the parts line) and the joint-share reader pairing the parts through the root across the sides (tools/bell_gate.py): the exact algebra at Bell's four settings and at the GHZ patterns, the local credits as the fence, the determinism of equal parts, and the two gates' four worlds each (examples/events/bell, examples/events/ghz) end to end with the back-in-time gate MATCH; Bell and the GHZ are gates and never results. The click written on the GameBoard (src/event_universe/credit.py, features/click): the instrument's draw inside the run and its write at one Node, the board exact between clicks."""

import ast
import json
import math
from fractions import Fraction

import numpy as np

from event_universe import meeting, node, resonance, world_files
from event_universe.core import paces
from event_universe.features.click import amplitude, hole_factor
from event_universe.game_board import GameBoard
from event_universe.loader.instrument import (
    Transition,
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
    row = {"name": "d", "positions": [[0, 0, 0], [1, 0, 0]], "pattern": [[1, 0]]}
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
    """The click written on the GameBoard (ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision of 2026-10-02; features/click, src/event_universe/credit.py): Bell's shipped world a b with the instrument's window cut to 40 over its 100 intervals, beside its twin without the key. (i) One credit line per side at 40 and at 80: the result the window, the detector's proper time at the close (the board's tick in the vacuum) and the index of the window closed, the region, the port realised, the parts kept and the count 1, the record's count down by one per window, no Node (the hole's Nodes in the face lines); at 40 the two boards differ at the two written Nodes alone (the one-Node test), and at the written Node every line of the record is 0 in its three arrays (the hole, as the receding face removes a share) where the twin's levels stand. (ii) The inverse is exact between clicks: from 100 back to 80 every array returns bit for bit, the step back across the click misses, and the twin goes from 40 back to the lay, MATCH. (iii) The record's count: at 0 the instrument credits nothing over the same 40 intervals, the reports the same lines with no credit line among them; the `instrument` key refused by name with a window of 0 and without its seed."""
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
    assert [(c["proper"], c["windows"]) for c in credits] == [(40, 1), (40, 1), (80, 2), (80, 2)]
    report = set(
        "event label tick family detector window proper windows realised kept count left".split()
    )
    assert all(set(c) == report and c["label"] == "DETECTOR" for c in credits)  # never a Node
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
    """The meeting at a Node (ALGEBRA.md, The click writes on the GameBoard (j) and (k); the owner's words of 2026-10-03; src/event_universe/meeting.py, loader/instrument.py): a record of a plane family of three parts declared at one Node in its parts (S at the count 1, P and D at 0) with a transition S to P fed by a drive's plane wave, a giving P to S at the lifetime 2 onto a light row and its own window of 1, beside a counter with the world's instrument. (i) The loader: the parts' count in two parts, a transition naming no part, a weight of 0, a rate without the instrument and a record of two Nodes are refused by name; the generator lays the drive and no entry for the record. (ii) The lay: the record's share reads 1 at its Node in the S lines alone, and its Links cut it stays there (the twin without the instrument MATCH over 30 intervals back to the lay). (iii) The clicks: the first jump takes the drive's quantum into P at the Node, the drive's record there after the face's two intervals the twin's two levels scaled below themselves and not 0 (the hole of a dense record, the drive at 55 quanta per Node, 2026-10-03) and its count in the books down by one, the record's P lines carrying the count and the S lines 0, the two boards differing at that Node alone; a later jump gives one quantum to the light row and the counter credits it at a window's end (the world of 20 intervals, the counter's window 15), and where the credit took the row's count to 0 the erasing front begins at the entry Node: one erasure line per interval at the distances 1 to 5, and the same run without the front (its fronts dropped each interval) holds every level beyond the ball, the Link-metric distance above the intervals since the click, bit for bit (the front invisible ahead of itself); every jump names the one Node as a GameBoard diagnostic, and the null window's re-lays that changed a level leave their own GAMEBOARD-labelled jump lines. (iv) The acts from outside the Node as lines (the mathematician's 193 and 195 with the advisor's second, two hands): every line a lay changed at the Node writes one GAMEBOARD-labelled `lay` line with its levels and remainder before and after (the taking's four ion lines, the giving's light line, the null windows'), every face presented writes one `face` line carrying the value the books hold; the back-in-time gate (tools/back_in_time.py) reads MATCH over the whole run across the takings, the givings, the null windows, the credit and the fronts, the faces presented from the lines and the lays undone from theirs, and on the shipped Zeno and anticoincidence worlds, one step more returning the start. (v) The booking identity per act at every step on the ion, the drive and the light (tests/laws.py, `booked`): the share identity within the floors plus the face term at the hole's two intervals and at every shell of the front, and the lays' change of the share form local to the Node and its six neighbours, exact. (vi) The conversion's list through the one act: the drive at -1 and two other rows at +1 at the Node, no draw and the generator's state untouched, the counts moved by the row, one whole quantum laid on each row at the massless rotation, the two levels alike, and the dense drive's partial hole after two intervals, its levels standing below themselves and not 0. (vii) The generator consumed the same whether or not a count-0 record's inflow is booked: the anticoincidence world with the first record's window at 10, run with the front and without it, gives the same one taking and the same generator states, the second record's its seed (its open window after the click draws nothing), while the light's level at its Node is erased in the one run and stands in the other. (viii) The one-in-flight limit is not built, by name: the light row's count rises by one per giving before the counter's window and no giving is refused; the Zeno world gives nothing and its drive's count stands above 1."""
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
        refused(word, node_instrument_of, body, "measured[0]", families, 0, quanta, 1)
    two = {**record, "nodes": record["nodes"] + [{"node": [3, 4, 2], "count": 1}]}
    refused("one Node", bodies_of, [two], None, "", families, (6, 6, 4), 9000, ())
    board, other = GameBoard(load_world(path), (lines := []).append), GameBoard(load_world(plain))
    names = [f.name for f in board.families]
    ion, drv, light = (names.index(n) for n in ("ion", "strong_drive", "fluorescence"))
    here, gamma, unit, weak = tuple(at), board.world.node_clock, board.unit, names.index("weak_drive")
    assert int(board.quanta(ion)[0][here]) == 1 == int(board.quanta(ion)[0].sum())
    assert all(int(line.now[here]) == 0 for line in board.states[ion].lines[2:])
    assert BACK.verdict(GameBoard(load_world(plain)), 30)["verdict"] == "MATCH"
    while not (clicks := [x for x in lines if x["event"] == "jump" and x["label"] == "DETECTOR"]):
        booked(board, monkeypatch, ion, drv, light), other.step()  # the booking identity at every act
    first, click = clicks[0], ("P", "S", "strong_drive", None)
    assert (first["realised"], first["left"], first["taken"], first["given"]) == click
    assert first["node"] == {"label": "GAMEBOARD", "at": at} and first["tick"] == board.tick
    was, now = (dict(p for f in BACK.snapshot(b) for p in f) for b in (other, board))
    assert {tuple(map(int, w)) for k in was for w in np.argwhere(was[k] != now[k])} == {here}
    assert board.credit.counts[drv] == other.credit.counts[drv] - 1
    in_s, in_p = (any(int(x.now[here]) for x in board.states[ion].lines[k : k + 2]) for k in (0, 2))
    assert int(board.quanta(ion)[0][here]) == 1 and in_p and not in_s
    p_re, p_im = (int(now[f"ion.lines[{k}].now"][here]) for k in (2, 3))  # the part entered, after
    size = amplitude(1, board.world.quantum_action, board.families[ion].pair)  # one quantum laid in P
    assert abs(p_re * p_re + p_im * p_im - size * size) <= 2 * size and (p_re, p_im) != (size, 0)
    walls = {k: node.rule_of(board.families[k], gamma, 0, None, unit)[2] for k in (ion, drv)}
    assert int(now["ion.lines[2].remainder"][here]) == walls[ion] // 2  # the taker at the lay's origin
    [booked(board, monkeypatch, ion, drv, light) for _ in (0, 1)]  # the hole: the face's two intervals
    hole, twin = board.states[drv].lines[0], (other.step(), other.step(), other.states[drv].lines[0])[2]
    assert all(
        0 < abs(int(getattr(hole, k)[here])) < abs(int(getattr(twin, k)[here]))
        for k in ("now", "before")
    )
    assert 0 <= int(hole.remainder[here]) < walls[drv]  # the giver's remainder Rule3's own
    still = GameBoard(load_world(path))  # the same run without the front: its fronts dropped each step
    [still.step() for _ in range(still.tick, board.tick)]
    for _ in range(board.tick, 23):
        booked(board, monkeypatch, ion, drv, light), still.step(), still.credit.fronts.clear()
        for index, origin, since in board.credit.fronts:  # the theorem: nothing differs beyond the ball
            gap = np.abs(np.indices(board.shape) - np.reshape(origin, (3, 1, 1, 1)))
            far = (
                np.minimum(gap, np.reshape(board.shape, (3, 1, 1, 1)) - gap).sum(0) > board.tick - since
            )
            for a, b in zip(board.states[index].lines, still.states[index].lines, strict=True):
                assert (a.now[far] == b.now[far]).all() and (a.before[far] == b.before[far]).all()
    given = [line for line in lines if line["event"] == "jump" and line["given"]]
    nulls = [line for line in lines if line["event"] == "jump" and line["label"] == "GAMEBOARD"]
    assert all(n["realised"] == n["left"] and "levels" not in n["node"] for n in nulls)
    credits = [line for line in lines if line["event"] == "credit" and line["family"] == "fluorescence"]
    erased = [line for line in lines if line["event"] == "erasure"]
    assert given and given[0]["left"] == "P" and board.credit.counts[light] == len(given)
    assert (
        credits == [] and erased == []
    )  # the given quanta, sources in time at one Node of a periodic box, reach the counter's plane below half a quantum in the window: the integer board's floor on a spreading quantum (the mathematician's 221), the front then never begun here (its theorem in tests/test_the_draw.py)
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
    assert all(
        0 < abs(int(getattr(fresh.states[drv].lines[0], k)[here])) for k in ("now", "before")
    )  # dense
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
        [(b.step(), front or b.credit.fronts.clear()) for _ in range(40)]
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
    lay |= {("meeting", "relaid"), ("giving", "laid_increment"), ("giving", "laid_by_count")}
    assert writers == rule3 | lay  # nothing writes a NodeState but Rule3, the lay and the face


def test_a_record_converted_whole_at_its_node_lays_the_table_at_the_rate(tmp_path):
    """The conversion, the fifth list of the one act (ALGEBRA.md, A family's declaration, item 5; the two hands of 2026-10-03, #1572 comments 5963954612 (c), 5964082980, 5964520368 and 5964754600; src/event_universe/conversion.py, loader/instrument.py `conversion_of`): the neutron conversion's committed world (examples/events/neutron_conversion) at the rate 1 and the window 2, so the first window, closing at the second interval, draws it. (i) The loader: a rate of 0, a record out of the body's own family, an empty table, a sense on a record of real lines, a conversion beside parts and one without the instrument are refused by name. (ii) The lay: the three lines at the Node at (95, -76) by the invariant, A_l^2 = T den div (2 s x 3), the instrument's count 1. (iii) The click: one conversion line naming the instrument, the three families out and the Node as a diagnostic; the neutron's three lines (0, 0) at the Node and its count 0; each record out given one whole quantum by the count on its first line, (128, 128) at A^2 = T div 2, its other lines 0, the credit's counts 1 each and the share 1 per quantum at the Node (the two hands); one lay line per line the write changed, the record's three and the three first lines out, and the back-in-time gate MATCH across the conversion from them; no second conversion, no front (the body cut) and no null window of a record of one part."""
    folder = EVENTS / "neutron_conversion"
    families = universe_of(json.loads((folder / "nucleons.json").read_text(encoding="utf-8")))[1]
    world = json.loads((folder / "neutron_conversion.json").read_text(encoding="utf-8"))
    table = (body := world["measured"][0])["conversion"]
    body["conversion"]["rate"], body["instrument"]["window"], world["ticks"] = 1, 2, 4
    (path := tmp_path / "w.json").write_text(json.dumps(world), encoding="utf-8")
    quanta = {f.name: k for k, f in enumerate(families) if f.quanta}
    rows = {"from 1": {"rate": 0}, "other than": {"to": ["neutron"]}, "lists the": {"to": []}}
    rows["at none"] = {"sense": 1}
    wrong = {word: {**body, "conversion": {**table, **row}} for word, row in rows.items()}
    wrong["no parts"] = {**body, "parts": []}
    wrong["no `instrument`"] = {k: v for k, v in body.items() if k != "instrument"}
    for word, entry in wrong.items():
        refused(word, node_instrument_of, entry, "measured[0]", families, quanta["neutron"], quanta, 1)
    board = GameBoard(load_world(path), (lines := []).append)
    n, p, e, nu = (quanta[name] for name in ("neutron", "proton", "electron", "antineutrino"))

    def levels(k):
        return [(int(r.now[4, 4, 4]), int(r.before[4, 4, 4])) for r in board.states[k].lines]

    assert levels(n) == [(95, -76)] * 3 and board.credit.bodies[0].counts == [1]
    board.step(), board.step()
    [first] = [line for line in lines if line["event"] == "conversion"]  # one conversion line
    assert first["window"] == [1, 2] and first["node"] == {"label": "GAMEBOARD", "at": [4, 4, 4]}
    assert (first["into"], first["detector"], first["label"]) == (table["to"], "measured 0", "DETECTOR")
    assert levels(n) == [(0, 0)] * 3 and board.credit.bodies[0].counts == [0]
    assert levels(p) == [(128, 128)] + [(0, 0)] * 5 and levels(e) == [(128, 128), (0, 0)]
    assert levels(nu) == [(128, 128)] and [board.credit.counts[k] for k in (p, e, nu)] == [1, 1, 1]
    assert [int(board.quanta(k)[0][4, 4, 4]) for k in (p, e, nu)] == [1, 1, 1]
    laid = [(line["family"], line["line"]) for line in lines if line["event"] == "lay"]
    assert laid == [("neutron", k) for k in range(3)] + [(f, 0) for f in table["to"]]
    board.step(), board.step()
    assert [x["event"] for x in lines if x["event"] not in ("click", "lay", "field")] == ["conversion"]
    assert BACK.verdict(GameBoard(load_world(path)), 3)["verdict"] == "MATCH"  # across the conversion


def test_the_resonant_two_mode_act_turns_by_the_planes_size_once_per_window():
    """The resonant two-mode act (ALGEBRA.md #what-is-open, item 50, the two-quadrature form; the mathematician's 223 (c) and 224 (2)(c), #1572 comments 5965727937 and 5966081562, the advisor's seconds, 5965918924 and 5966129376, two hands; src/event_universe/resonance.py and `meeting.turned_labels`): (i) the scale R is derived from the width's room, the file's amplitude bound and the record's window, the largest power of two with 2 (R A W)^2 inside the room, 2^12 at A = 9,266 and W = 48, 2^11 at W = 96 and 2^14 at W = 12, nothing declared; (ii) the two reference records advance by the giving's one recurrence (giving.advanced, through `gathered` at the level 0) and stay within 7 levels of R cos(Omega t) and R sin(Omega t) over 100 intervals at [2, 3]; (iii) a resonant arrival A cos(Omega t + phi) at A = 1,000 over W = 48 turns by A W / 2 within 2 percent at the phases 0, 0.7, pi / 2 and 2.5 (the hands' 23,724 to 24,289 against 24,000), where the magnitude form accumulated (2 / pi) A W at every frequency; (iv) the arrival at [1, 3]'s frequency against the pair [2, 3] turns by less than 2 percent of the resonant turn at W = 48 (sinc(delta W / 2) = 0.007 with the counter-rotating residue) and by sinc within 0.02 at W = 12 (0.30 against 0.31); (v) on the shipped Zeno world zeno_4 (the window 12) the labels stand at their start through the window's first eleven intervals while the two sums gather, and at the twelfth the sums are read once and begin again with the window: the root once per window, the instrument's act; (vi) the window's turn is applied as W equal sub-turns with the carry (`resonance.sheared`), so the labels' angle at the Zeno world's n = 1 is 48 x 2 arctan(9,408 / (12,000 x 48)) = 1.568 and not the one shear's 1.330, the tangent half-angle's compression the advisor's second found on the first build."""
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


def test_the_hole_of_a_dense_record_removes_one_quantums_share_and_the_phase_stands():
    """The hole of a dense record (the mathematician's 237 and 244 with the advisor's seconds, #1572 comments 5967012316, 5967123679 and 5967913000, two hands; features/click `hole_factor`, `target_of`, `rest_of`, `meeting.faced`): the shipped Zeno n = 2 world, whose drive holds about 2.6 quanta's share at the instrument's Node (s above W_rec), at the trial seed 2, beside its untouched twin. (i) The factor: (0, 1) where O + C is at most the unit; the root of f^2 O + f C = s - W_rec above it, within the root's own rounding. (ii) The taking at 24: the first face scales the level it writes by the factor within one level (the record's level before at 26 the twin's times f), the second removes the rest of the quantum, both levels standing below the twin's and not 0, the count down by one, no front begun. (iii) The back-in-time gate reads MATCH across the dense taking over the run, the face's inverse presenting the kept values whatever the target."""
    zeno = EVENTS / "zeno" / "zeno_2.json"
    assert hole_factor(5, 0, 5) == (0, 1) == hole_factor(3, 1, 5) == hole_factor(0, 9, 5)
    numerator, denominator = hole_factor(3000, -1200, 400)  # O, C, W_rec: f^2 3000 - 1200 f = 1400
    assert abs(numerator / denominator - (1200 + (1200**2 + 4 * 3000 * 1400) ** 0.5) / 6000) < 1e-3
    board, twin = GameBoard(load_world(zeno), (lines := []).append), GameBoard(load_world(zeno))
    board.credit.bodies[0].state, pulse = 2, [f.name for f in board.families].index("pulse")
    unit, at, count = board.credit.units[pulse], (4, 4, 2), board.credit.counts[pulse]
    for _ in range(26):
        board.step(), twin.step()
    jumps = [x for x in lines if x["event"] == "jump" and x["label"] == "DETECTOR"]
    assert [x["tick"] for x in jumps] == [24] and jumps[0]["taken"] == "pulse"
    hole = board.credit.faces[25][0].hole
    assert hole is not None and hole.factor is not None and 0 < hole.factor[0] < hole.factor[1]
    mine, its = board.states[pulse].lines[0], twin.states[pulse].lines[0]
    now, before = (int(mine.now[at]), int(mine.before[at])), (int(its.now[at]), int(its.before[at]))
    assert abs(now[1] - before[1] * hole.factor[0] / hole.factor[1]) <= 1.5  # the first face's level
    assert 0 < abs(now[0]) < abs(before[0]) and board.credit.counts[pulse] == count - 1
    assert (
        not board.credit.fronts
        and board.credit.faces[26][0].scaled
        and not board.credit.faces[25][0].scaled
    )
    gate = GameBoard(load_world(zeno))
    gate.credit.bodies[0].state = 2
    assert BACK.verdict(gate, 47)["verdict"] == "MATCH"  # across the dense taking's two faces


def test_the_two_faces_remove_exactly_one_quantum_from_a_dense_record():
    """The exact removal (the mathematician's 244, section 1, with the booking identity's face term, tests/laws.py: a face changes the record's form by (a* - before) R_face (value - arrival)): the Zeno n = 2 world at the seed 2 beside its twin. (i) The first face's factor is the root of f^2 O + f C = s - W_rec on the Node's own numbers at its interval, O = w (a^2 + b^2) - S a b and C = -a SUM_j R_j b_j - b SUM_j R_j a_j with the neighbours' levels through the Ports, W_rec in the form's own units at the Node, 2 p_i^2 G^2 W_rec, recomputed here from the twin at the click. (ii) After the two faces the record's share over the board is the twin's less one quantum within one level's share at the Node (0.9965 of W_rec at this seed, the second face removing exactly the rest); the share the engine reads at the Node alone is above s - W_rec (1.85 against 1.67 quanta), the Link terms with the six neighbours landing on them, a finding by name beside the record's own number."""
    zeno = EVENTS / "zeno" / "zeno_2.json"
    board, twin = GameBoard(load_world(zeno)), GameBoard(load_world(zeno))
    board.credit.bodies[0].state, pulse = 2, [f.name for f in board.families].index("pulse")
    family, gamma, at = board.families[pulse], board.world.node_clock, (4, 4, 2)
    unit = board.credit.units[pulse]
    for _ in range(24):
        board.step(), twin.step()
    record, (content, factors) = twin.states[pulse].lines[0], twin.read(pulse, 1, 0)
    reads, coefficient, wall = node.rule_of(family, gamma, content, factors, twin.unit)
    here, pick = (
        [int(np.asarray(r)[at]) if np.ndim(r) else int(r) for r in reads],
        lambda v: int(np.asarray(v)[at]) if np.ndim(v) else int(v),
    )
    a, b = int(record.now[at]), int(record.before[at])
    arrivals = sum(here[p] * int(node.ports(record.now, twin.wrap)[p][at]) for p in range(6))
    befores = sum(here[p] * int(node.ports(record.before, twin.wrap)[p][at]) for p in range(6))
    own = int(wall) * (a * a + b * b) - pick(coefficient) * a * b
    links = -(a * befores + b * arrivals)
    pace = int(paces.link_pace_of(gamma, pick(content)))
    weight = 2 * pace * pace * twin.unit * twin.unit  # the share's weight at the Node
    assert (own + links) > unit * weight > 0  # dense: the form's share at the Node above a quantum
    board.step(), twin.step(), board.step(), twin.step()
    hole = board.credit.faces[25][0].hole
    assert hole is not None and hole.unit == unit * weight
    assert hole.factor == hole_factor(own, links, unit * weight) and 0 < hole.removed < hole.unit
    totals = [int(x.total_share(pulse)[0]) for x in (twin, board)]
    level = int(wall) * (2 * abs(int(board.states[pulse].lines[0].now[at])) + 1)  # one level's share
    assert abs(totals[0] - totals[1] - unit) <= level / weight + 1  # one quantum left the record
    left = int(board.share_of(pulse)[0][at]) / unit
    assert 1.6 < left < 2.0 and left > int(twin.share_of(pulse)[0][at]) / unit - 1  # the Node alone
