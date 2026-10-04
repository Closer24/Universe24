"""The NodeReader (ALGEBRA.md, The NodeReader is one declaration kind for every experiment; the owner's words of 2026-10-03, a reader with Nodes alone is never on one Node and a reader with a record of its own may stand on one; src/event_universe/meeting.py, loader/node_reader_declaration.py, loader/world.py): a record declared a reader over a connected region, laid in the weights' proportion, its outer Links cut and its inner Links open, taking and giving at one drawn Node of the region, every click a click line naming the reader and never a Node, the write's Node in the GAMEBOARD lay and face lines beside it."""

import ast
import json
import math

import numpy as np

from event_universe import meeting, node, node_reader, world_files
from event_universe.features.click import amplitude, spread, squared
from event_universe.game_board import GameBoard
from event_universe.loader.derived import count_wall
from event_universe.loader.node_reader_declaration import node_reader_of
from event_universe.loader.universe import universe_of
from event_universe.loader.world import bodies_of
from event_universe.world_files import load_world
from tests.laws import BACK, EVENTS, ROOT, TOOL, TOP, booked, chain_body_world, refused

TOP_PAIR = (TOP[0], TOP[1])  # the band's top as a resonance, cos Omega = 0


def test_a_record_declared_a_reader_over_two_nodes_takes_gives_and_stays(tmp_path, monkeypatch):
    """The reader over a region (ALGEBRA.md, The NodeReader is one declaration kind for every experiment; the owner's words of 2026-10-03): the ion's three-part record declared over two adjacent Nodes in equal counts, the lay A_n^2 = A^2 / n at each, the share credited 1 by the count's rounding, the loader admitting it and refusing a region in pieces by name, the outer Links cut and the inner Link open (`meeting.cut`), the uniform mode at cos omega_0 = num / den to the bit over one window, the taking's hole at the Node drawn by the drive's share, the giving laid at the Node drawn by the record's share. The meeting at a Node (ALGEBRA.md, The click writes on the GameBoard (j) and (k); the owner's words of 2026-10-03; src/event_universe/meeting.py, loader/node_reader_declaration.py): a record of a plane family of three parts declared at one Node in its parts (S at the count 1, P and D at 0) with a transition S to P fed by a drive's plane wave, a giving P to S at the lifetime 2 onto a light row and its own window of 1, beside a counter with the world's draw. (i) The loader: the parts' count in two parts, a transition naming no part, a weight of 0 and a rate without the draw are refused by name; the generator lays the drive and no entry for the record. (ii) The lay: the record's share reads 1 at its Node in the S lines alone, and its Links cut it stays there (the twin without the draw MATCH over 30 intervals back to the lay). (iii) The clicks: the first click takes the drive's quantum into P at the Node, the drive's record there after the face's two intervals the twin's two levels scaled below themselves and not 0 (the hole of a dense record, the drive at 55 quanta per Node, 2026-10-03) and its count in the books down by one, the record's P lines carrying the count and the S lines 0, the two boards differing at that Node alone; a later click gives one quantum to the light row and the counter credits it at a window's end (the world of 20 intervals, the counter's window 15), and where the credit took the row's count to 0 the erasing front begins at the entry Node: one erasure line per interval at the distances 1 to 5, and the same run without the front (its fronts dropped each interval) holds every level beyond the ball, the Link-metric distance above the intervals since the click, bit for bit (the front invisible ahead of itself); every click of the reader is one credit line, the one click line kind (the taking's and the giving's alike: the reader `body 0`, the family, the part before and after, the count moved and left, the family taken from or given to, the reader's clock and the window), carrying no Node, the Node written read from the GAMEBOARD lay lines of the write and the face books of the hole; the null window's re-lays that changed a level leave the same line labelled GAMEBOARD at the count 0. (iv) The acts from outside the Node as lines (the mathematician's 193 and 195 with the advisor's second, two hands): every line a lay changed at the Node writes one GAMEBOARD-labelled `lay` line with its levels and remainder before and after (the taking's four ion lines, the giving's light line, the null windows'), every face presented writes one `face` line carrying the value the books hold; the back-in-time gate (tools/back_in_time.py) reads MATCH over the whole run across the takings, the givings, the null windows, the credit and the fronts, the faces presented from the lines and the lays undone from theirs, and on the shipped Zeno and anticoincidence worlds, one step more returning the start. (v) The booking identity per act at every step on the ion, the drive and the light (tests/laws.py, `booked`): the share identity within the floors plus the face term at the hole's two intervals and at every shell of the front, and the lays' change of the share form local to the Node and its six neighbours, exact. (vi) The conversion's list through the one act: the drive at -1 and two other rows at +1 at the Node, no draw and the generator's state untouched, the counts moved by the row, one whole quantum laid on each row at the massless rotation, the two levels alike, and the dense drive's partial hole after two intervals, its levels standing below themselves and not 0. (vii) The generator consumed the same whether or not a count-0 record's inflow is booked: the anticoincidence world with the second record's window at 60 and the seed 2, run with the front and without it over 170 intervals, gives the same one taking (the first record's at 48) and the same generator states, the second record's its seed (its open window after the click draws nothing), while the far packet's level at its top is erased in the one run and stands in the other. (viii) The one-in-flight limit is not built, by name: the light row's count rises by one per giving before the counter's window and no giving is refused; the Zeno world gives nothing and its drive's count stands above 1."""
    universe = json.loads((EVENTS / "shelved_ion" / "mercury_ion.json").read_text(encoding="utf-8"))
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    at, beside = [3, 3, 2], [4, 3, 2]  # the region: two Nodes adjacent along x, in equal counts
    parts = [{"part": k, "name": n, "count": int(k == 0)} for k, n in enumerate("SPD")]
    draw = {"window": 1, "seed": 25, "multiplier": 6364136223846793005, "increment": 1}
    nodes = [
        {"node": at, "weight": 1},
        {"node": beside, "weight": 1},
    ]  # the lay's weights, the count once
    record = {"family": "ion", "nodes": nodes, "parts": parts, "node_reader": draw}
    record["transitions"] = [
        {"from": "S", "to": "P", "drive": "strong_drive", "weight": 1, "resonance": [2, 3]}
    ]
    record["rates"] = [{"from": "P", "to": "S", "lifetime": 8, "gives_to": "fluorescence"}]
    drive = {"family": "strong_drive", "along": "x", "wave": [1, 2], "phase": [0, 1], "amplitude": 600}
    drive.update(top={"x": [0, 7], "y": [0, 5], "z": [0, 3]}, edge={"x": 0, "y": 0, "z": 0})
    counter = {
        "name": "counter",
        "positions": [[0, y, z] for y in range(6) for z in range(4)],
    }
    world = dict(shape=[8, 6, 4], boundary=dict(x="periodic", y="periodic", z="periodic"), ticks=23)
    world.update(universe="u.json", engine="e.json", bodies=[record], messages=[drive])
    world.update(node_readers=[counter], draw={**draw, "window": 18, "seed": 24})
    (path := tmp_path / "w.json").write_text(json.dumps(world), encoding="utf-8")
    twin = {k: v for k, v in world.items() if k != "draw"}
    twin["bodies"] = [{k: v for k, v in record.items() if k in ("family", "nodes", "parts")}]
    (plain := tmp_path / "t.json").write_text(json.dumps(twin), encoding="utf-8")
    TOOL.main(["--input", str(path)]), TOOL.main(["--input", str(plain)])
    assert json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"] == []
    families, quanta = universe_of(universe)[1], {"ion": 0, "strong_drive": 1, "fluorescence": 3}
    wrong = {"one part": {**record, "parts": [{**p, "count": 1} for p in parts]}}
    wrong["parts are"] = {**record, "transitions": [{**record["transitions"][0], "to": "X"}]}
    wrong["weight"] = {**record, "transitions": [{**record["transitions"][0], "weight": 0}]}
    wrong["no `node_reader`"] = {k: v for k, v in record.items() if k != "node_reader"}
    edge = {**record["transitions"][0], "resonance": [1, 4]}  # cos Omega below 1 / 3: cos k below -1
    wrong["above the axis band's top"] = {**record, "transitions": [edge]}
    for word, body in wrong.items():
        refused(word, node_reader_of, body, "bodies[0]", families, 0, quanta, 1)
    node_reader_of(
        {**record, "transitions": [{**edge, "resonance": [1, 3]}]}, "bodies[0]", families, 0, quanta, 1
    )  # 3 num = den: the band's edge, cos k = -1, admitted
    apart = {**record, "nodes": [nodes[0], {"node": [3, 5, 2], "weight": 1}]}  # in pieces
    action = universe["integers"]["quantum_action"]
    counted = {**record, "nodes": [{"node": at, "count": 1}, nodes[1]]}  # a count on a reader's Node
    for word, body in (("in pieces", apart), ("unknown key 'count'", counted)):
        refused(word, bodies_of, [body], None, "", families, (6, 6, 4), 9000, (), action)
    alone = {**twin, "messages": [], "node_readers": []}  # the record alone: its uniform mode
    (rest := tmp_path / "r.json").write_text(json.dumps(alone), encoding="utf-8")
    TOOL.main(["--input", str(rest)])
    quiet, pair = GameBoard(load_world(rest)), universe["families"][0]["pair"]
    one_node = amplitude(
        1, action, (pair[0], pair[1])
    )  # A = isqrt(A^2), A^2 = T den^2 div (2 (den^2 - num^2))
    spread_to = spread(squared(1, action, (pair[0], pair[1])), (1, 2))  # A_n = isqrt(A^2 div 2)
    assert (pair, one_node, spread_to) == ([1, 1299], 128, 90)  # the ion's pair: A^2 = T div 2 = 16,384
    at_two_three = (amplitude(1, 32768, (2, 3)), spread(squared(1, 32768, (2, 3)), (1, 2)))
    assert (
        at_two_three
        == (
            148,
            104,
        )
    )  # one quantum of the invariant, A^2 = T / (2 sin omega) = 21,981 at T 32,768, [2, 3] (the law's L798)
    assert 2 * 104**2 == 21632 < 21981 == squared(1, 32768, (2, 3))  # the two Nodes' squares under A^2
    there, next_to = tuple(at), tuple(beside)
    levels = [[int(quiet.states[0].lines[0].now[n]) for n in (there, next_to)]]
    assert levels[0] == [spread_to, spread_to]  # the lay over the two Nodes in equal counts
    wall_c = count_wall(quiet.families[0], action)
    laid_share = int(quiet.share_of(0)[0][[there[0], next_to[0]], 3, 2].sum())
    assert (quiet.credit.counts[0], 1000 * laid_share // wall_c) == (
        1,
        977,
    )  # 0.977 W_c over two, credited 1
    cuts = meeting.cut(quiet, 0)
    assert cuts is not None and [int(c.sum()) for c in cuts] == [
        2,
        2,
        4,
        4,
        4,
        4,
    ]  # the boundary's 10 Links
    assert not cuts[0][there] and not cuts[1][next_to]  # the inner Link open from both ends
    assert (
        cuts[1][there] and cuts[0][next_to] and cuts[0][2, 3, 2] and cuts[1][5, 3, 2]
    )  # outer, both ends
    for _ in range(
        18
    ):  # one window: the uniform mode at cos omega_0 = num / den, Chebyshev's recurrence
        quiet.step()
        levels.append([int(quiet.states[0].lines[0].now[n]) for n in (there, next_to)])
    assert all(a == b for a, b in levels)  # the two Nodes alike, the mode uniform
    num, den = pair  # Chebyshev's recurrence of the uniform mode, den (l_(t+1) + l_(t-1)) = 2 num l_t
    residues = [
        den * (levels[t + 1][0] + levels[t - 1][0]) - 2 * num * levels[t][0] for t in range(1, 18)
    ]
    assert (
        max(map(abs, residues)) <= den
    )  # within one level of the division act: cos omega_0 = num / den
    board, other = GameBoard(load_world(path), (lines := []).append), GameBoard(load_world(plain))
    names = [f.name for f in board.families]
    ion, drv, light = (names.index(n) for n in ("ion", "strong_drive", "fluorescence"))
    here, gamma, unit, weak = tuple(at), board.world.node_clock, board.unit, names.index("weak_drive")
    region = (here, tuple(beside))
    assert board.credit.counts[ion] == 1 and int(board.quanta(ion)[0].sum()) <= 1
    assert all(int(line.now[n]) == 0 for line in board.states[ion].lines[2:] for n in region)
    assert BACK.verdict(GameBoard(load_world(plain)), 30)["verdict"] == "MATCH"
    draws, node_draws, book = (
        [],
        [],
        {},
    )  # the generator's draws, the write's Node draws, the inflow book
    real_draw, real_node, real_book = (
        node_reader.drawn,
        node_reader.drawn_node,
        node_reader.booked_inflow,
    )

    def counted_draw(*args):  # type: ignore[no-untyped-def]
        draws.append(board.tick)
        return real_draw(*args)

    def noted_node(b, books, weights):  # type: ignore[no-untyped-def]
        node_draws.append((board.tick, list(weights)))
        return real_node(b, books, weights)

    def kept_book(b, books, drive, came):  # type: ignore[no-untyped-def]
        real_book(b, books, drive, came)
        book[drive] = list(books.intake[drive])

    for name, found in (
        ("drawn", counted_draw),
        ("drawn_node", noted_node),
        ("booked_inflow", kept_book),
    ):
        monkeypatch.setattr(node_reader, name, found)
    while not (clicks := [x for x in lines if x["event"] == "credit" and x["label"] == "NODEREADER"]):
        booked(board, monkeypatch, ion, drv, light), other.step()  # the booking identity at every act
    reader = board.credit.bodies[
        0
    ]  # the turn's read: the drive projected on the reader's normalised mode
    read = [int(other.states[drv].lines[0].now[tuple(np.add(n, board.offset))]) for n in region]
    total = sum(d * a for d, a in zip(read, reader.amplitudes, strict=True))
    assert (list(reader.amplitudes), reader.norm) == ([90, 90], 127)  # A_i = 90, A = isqrt(2 x 90^2)
    assert meeting.arriving(other, reader, drv) == (1 if total >= 0 else -1) * ((abs(total) + 63) // 127)
    assert draws.count(board.tick) == 2 and [t for t, _ in node_draws] == [
        board.tick
    ]  # one draw per click
    assert node_draws[0][1] == [max(w, 0) for w in book[drv]]  # the Node by the window's inflow per Node
    first, click = clicks[0], ("P", "S", "strong_drive", None, 1, "body 0")
    words = ("realised", "before", "taken", "given", "count", "node_reader")
    assert tuple(first[k] for k in words) == click and first["tick"] == board.tick
    assert "node" not in first and first["left"] == board.credit.counts[drv]  # the click names no Node
    assert set(first) == set(
        credits_keys
        := "event label tick family node_reader window proper windows before realised kept count left taken given".split()
    )
    holes = {f.at for f in board.credit.faces[board.tick + 1] if f.family == drv}  # the hole's faces
    assert len(holes) == 1 and (hole_at := next(iter(holes))) in region  # the taking's one drawn Node
    assert (
        book[drv][region.index(hole_at)] > 0
    )  # the Node the quantum entered through, its inflow booked
    written = {tuple(x["node"]["at"]) for x in lines if x["event"] == "lay" and x["tick"] == board.tick}
    assert written == set(region)  # the GAMEBOARD lay lines of the write name the Nodes, the click none
    was, now = (dict(p for f in BACK.snapshot(b) for p in f) for b in (other, board))
    assert {tuple(map(int, w)) for k in was for w in np.argwhere(was[k] != now[k])} == set(region)
    here = hole_at
    assert board.credit.counts[drv] == other.credit.counts[drv] - 1
    in_s, in_p = (
        any(int(x.now[n]) for x in board.states[ion].lines[k : k + 2] for n in region) for k in (0, 2)
    )
    assert board.credit.counts[ion] == 1 and in_p and not in_s
    p_re, p_im = (int(now[f"ion.lines[{k}].now"][here]) for k in (2, 3))  # the part entered, after
    size = spread(squared(1, board.world.quantum_action, board.families[ion].pair), (1, 2))  # P over two
    assert abs(p_re * p_re + p_im * p_im - size * size) <= 2 * size and (p_re, p_im) != (size, 0)
    walls = {k: node.rule_of(board.families[k], gamma, 0, None, unit)[2] for k in (ion, drv)}
    assert int(now["ion.lines[2].remainder"][here]) == walls[ion] // 2  # the taker at the lay's origin
    leaving = int(other.states[drv].lines[0].now[here])  # b, the leaving level at the first face
    [booked(board, monkeypatch, ion, drv, light) for _ in (0, 1)]  # the hole: the face's two intervals
    hole, twin = board.states[drv].lines[0], (other.step(), other.step(), other.states[drv].lines[0])[2]
    v, first_root = int(twin.before[here]), int(hole.before[here])
    assert min(v, leaving) < first_root < max(v, leaving)  # the first face's root between v and b (265)
    second, v_next = int(hole.now[here]), int(twin.now[here])  # the second face's root, the rest (265)
    assert second != 0 and min(v_next, first_root) <= second <= max(
        v_next, first_root
    )  # between v and b
    drop = int(other.total_share(drv)[0]) - int(board.total_share(drv)[0])
    rounding = 2 * max(abs(v), abs(leaving)) * board.credit.units[drv] // board.world.quantum_action
    assert (
        0 < drop <= board.credit.units[drv] + rounding
    )  # one quantum within one level's rounding at the drive's amplitude A: 6 den A of the form, 2 A / T of W_c = 3 den T (266)
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
    given = [line for line in lines if line["event"] == "credit" and line["given"]]
    nulls = [line for line in lines if line["event"] == "credit" and line["label"] == "GAMEBOARD"]
    assert all(n["realised"] == n["before"] and n["count"] == 0 and "node" not in n for n in nulls)
    assert all(
        set(g) == set(credits_keys) and "node" not in g and g["node_reader"] == "body 0" for g in given
    )
    gave_at = {
        tuple(x["node"]["at"])
        for x in lines
        if x["event"] == "lay" and x["tick"] == given[0]["tick"] and x["family"] == "fluorescence"
    }
    assert len(gave_at) == 1 and gave_at <= set(
        region
    )  # the giving's quantum laid at one drawn Node of the region
    credits = [line for line in lines if line["event"] == "credit" and line["family"] == "fluorescence"]
    erased = [line for line in lines if line["event"] == "erasure"]
    assert given and given[0]["before"] == "P" and board.credit.counts[light] == len(given)
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
    assert {x["label"] for x in lays} == {"GAMEBOARD"} and board.credit.counts[
        light
    ] >= 1  # none refused
    key, kept = ("line", "port", "tick", "value"), sum(board.credit.faces.values(), [])
    faced = {(f.family, f.at, *(getattr(f, k) for k in key)) for f in kept}
    logged = {(names.index(x["family"]), tuple(x["node"]["at"]), *(x[k] for k in key)) for x in faces}
    assert logged == {f for f in faced if f[4] <= board.tick} and logged  # the lines the books' values
    assert BACK.verdict(GameBoard(load_world(path)), 23)["verdict"] == "MATCH"  # every act crossed
    fresh = GameBoard(load_world(path), (conv := []).append)  # the conversion's list through the one act
    counts, items = dict(fresh.credit.counts), [meeting.Item(drv, None, None, -1, (here,))]
    items += [meeting.Item(k, None, None, 1, (here,), TOP_PAIR, 1) for k in (weak, light)]
    assert meeting.click_act(fresh, 7, None, [1], [items]) == (
        0,
        7,
    )  # one outcome: no draw, the state kept
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
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", ROOT)  # the shipped reader worlds
    zeno, photon = EVENTS / "zeno" / "zeno_4.json", EVENTS / "anticoincidence" / "one_photon.json"
    loaded = BACK.snapshot(z := GameBoard(load_world(zeno), (zlines := []).append))
    assert BACK.verdict(z, 48)["verdict"] == "MATCH" and z.step_inverse() is None  # the lays, the start
    assert BACK.first_difference(loaded, BACK.snapshot(z)) is None and z.tick == 0
    assert any(x["event"] == "credit" and x["taken"] for x in zlines) and not any(
        x.get("given") for x in zlines
    )
    assert (
        max(z.credit.counts.values()) > 1
    )  # the drive's record of many quanta, no giving in this world
    assert BACK.verdict(GameBoard(load_world(photon)), 40)["verdict"] == "MATCH"
    world = json.loads(photon.read_text(encoding="utf-8"))  # a window open after the click
    world["bodies"][1]["node_reader"]["window"], runs = (
        60,
        [],
    )  # the second record's window open after the click
    for body in world["bodies"]:
        body["node_reader"]["seed"] = 2  # a seed whose draw at 48 takes at the first record alone
    (split := tmp_path / "split.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(split)])
    for front in (True, False):  # the count-0 record's inflow erased by the front, or standing
        b = GameBoard(load_world(split), (sl := []).append)
        [(b.step(), front or b.credit.fronts.clear()) for _ in range(170)]
        ph, b_at = (
            [f.name for f in b.families].index("photon"),
            [141, 0, 0],
        )  # the far packet's top at 170
        took = [(x["tick"], x["node_reader"]) for x in sl if x["event"] == "credit" and x["taken"]]
        level = int(b.states[ph].lines[0].now[tuple(np.add(b_at, b.offset))])
        runs.append((took, [k.state for k in b.credit.bodies], b.credit.counts[ph], level))
    assert runs[0][:3] == runs[1][:3] and len(runs[0][0]) == 1  # one taking, the generators alike
    assert runs[0][1][1] == world["bodies"][1]["node_reader"]["seed"] and runs[0][2] == 0  # no draw
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
    lay |= {("lay", "written")}  # the one lay act's write step, every door's (ALGEBRA.md, the principle)
    assert writers == rule3 | lay  # nothing writes a NodeState but Rule3, the lay and the face


def test_a_reader_with_its_own_record_stands_on_one_node(tmp_path):
    """The relation seen from its two ends (ALGEBRA.md, The NodeReader is one declaration kind for every experiment): the shipped Zeno reader declared at one Node alone is admitted by the loader; its lay is the whole amplitude, A_1 = A, and its norm A, so the resonant turn reads the drive's level at the Node exactly, (|d| A + A div 2) div A = |d|; its six Links are cut; the record alone rotates in the uniform mode at cos omega_0 = num / den, Chebyshev's recurrence within one level over a window; the click line names no Node while the taking's hole and the write's lay lines stand at the only Node, and the back-in-time gate crosses the run; a reader with Nodes alone at one Node is still refused by name, since through one Node what enters leaves and the net current over a passing wave is about 0."""
    world = json.loads((EVENTS / "zeno" / "zeno_4.json").read_text(encoding="utf-8"))
    world["bodies"][0]["nodes"] = world["bodies"][0]["nodes"][:1]  # the reader at one Node
    at = tuple(world["bodies"][0]["nodes"][0]["node"])
    record = {k: v for k, v in world["bodies"][0].items() if k in ("family", "nodes", "parts")}
    files = {"one": world, "plain": {**world, "bodies": [record]}}
    files["alone"] = {**world, "bodies": [record], "messages": []}  # the record alone
    files["bare"] = {**world, "bodies": [], "node_readers": [{"name": "bare", "positions": [list(at)]}]}
    paths = {name: tmp_path / f"{name}.json" for name in files}
    for name, content in files.items():
        paths[name].write_text(json.dumps(content), encoding="utf-8")
    bare = paths["bare"]  # a reader with Nodes alone at one Node: still refused by name
    refused("never one Node", lambda: (TOOL.main(["--input", str(bare)]), load_world(bare)))
    for name in ("one", "plain", "alone"):
        TOOL.main(["--input", str(paths[name])])
    board = GameBoard(load_world(paths["one"]), (lines := []).append)
    plain, alone = GameBoard(load_world(paths["plain"])), GameBoard(load_world(paths["alone"]))
    names = [f.name for f in board.families]
    atom, drv = names.index("atom"), names.index("pulse")
    (num, den), action = board.families[atom].pair, board.world.quantum_action
    here, reader = tuple(np.add(at, board.offset)), board.credit.bodies[0]
    one = amplitude(1, action, (num, den))  # A = isqrt(T den^2 div (2 (den^2 - num^2)))
    assert (list(reader.amplitudes), reader.norm, one) == ([one], one, 128)  # A_1 = A, the whole lay
    assert int(board.states[atom].lines[0].now[here]) == one
    cuts = meeting.cut(board, atom)
    assert cuts is not None and all(int(c.sum()) == 2 and c[here] for c in cuts)  # six Links cut
    levels = [int(alone.states[atom].lines[0].now[here])]
    for _ in range(12):
        alone.step()
        levels.append(int(alone.states[atom].lines[0].now[here]))
    residues = [den * (levels[t + 1] + levels[t - 1]) - 2 * num * levels[t] for t in range(1, 12)]
    assert max(map(abs, residues)) <= den  # the uniform mode at the cut Node, cos omega_0 = num / den
    clicks = [x for x in lines if x["event"] == "credit" and x["count"]]  # none before the run
    while board.tick < 48 and not clicks:
        board.step(), plain.step()
        level = int(plain.states[drv].lines[0].now[here])  # d, the drive's level at the Node
        assert meeting.arriving(plain, reader, drv) == level  # the turn reads |d| exactly, signed
        clicks = [x for x in lines if x["event"] == "credit" and x["count"]]
    first = clicks[0]
    assert "node" not in first and (first["node_reader"], first["label"]) == ("body 0", "NODEREADER")
    assert (first["before"], first["realised"], first["taken"], first["count"]) == ("g", "e", "pulse", 1)
    holes = {f.at for f in board.credit.faces[board.tick + 1] if f.family == drv}
    written = {tuple(x["node"]["at"]) for x in lines if x["event"] == "lay" and x["tick"] == board.tick}
    assert holes == written == {at}  # the only Node drawn: the hole and the write there, the click none
    assert BACK.verdict(GameBoard(load_world(paths["one"])), 48)["verdict"] == "MATCH"


def test_a_count_is_one_quantum_of_the_invariant_in_the_familys_own_wall(tmp_path, monkeypatch):
    """A count is one quantum of the invariant, the form T sin omega_0 of the family's gap (the two hands' word on #1793's R8): the taker's lay carries 2 A^2 sin omega = T per quantum per line to the unit, the family's wall is W_c sin omega_0 by one root on the whole product and 3 den T for a massless family, the [1, 1299] amplitude is unchanged, and the generator lays a body's declared count in that unit (the books' count of a bound body at the lay is the share at the Nodes' paces under its own well, a reading above the declaration on main before this branch, 13 for 6 on the tests' chain, and no part of this change)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL, 7)
    board = GameBoard(load_world(world))
    names, action = [family.name for family in board.families], board.world.quantum_action
    matter, light = board.families[names.index("matter")], board.families[names.index("charge")]
    num, den = matter.pair
    gap, laid = den * den - num * num, squared(1, action, matter.pair)
    assert (
        laid == squared(1, action, (2, 3)) == 21981 and action == 32768
    )  # T / (2 sin omega_0) to the unit
    assert (
        action - 2 <= 2 * laid * math.isqrt(gap) // den <= action
    )  # 2 A^2 sin omega = T, two roots' units
    assert (
        squared(1, action, (1, 1299)) == 16384 and amplitude(1, action, (1, 1299)) == 128
    )  # bit for bit
    assert count_wall(light, action) == 3 * 6000 * action  # the bolometer's W_c for a massless family
    assert (
        count_wall(matter, action) == math.isqrt(9 * action**2 * gap) == 439628852
    )  # W_c sin omega_0 to the unit
    laid_body = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    assert (
        laid_body["count"] == laid_body["carried"] == 7
    )  # the generator lays the declaration in that unit
