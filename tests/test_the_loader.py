"""The loader's refusals by name, each called by hand on the loader's own function with no world run (ENGINE.md section 4, the files' keys; the architect's audit of 2026-10-03, the loader's pieces with no test of their own)."""

import json

from event_universe import world_files
from event_universe.game_board import GameBoard
from event_universe.loader import faces, keys, lay, messages, mode, universe
from event_universe.loader.derived import PLANE_LINE, REAL_LINE
from event_universe.world_files import load_world
from tests.laws import EVENTS, PACKET, TOOL, refused, slit_world, universe_beside


def test_the_loader_refuses_every_wrong_key_of_the_files_by_name(tmp_path):
    """Every refusal of the loader's own functions, by name and with no world run: the keys (an object, an unknown key, a lacking key, an integer's bounds, a Node's form and the Nodes beyond an inner face, a range's form, a repository path with no file, a record's line weights on a plane, at the wrong length and all 0, a read at the weight 0); the mode file (a level's sparse and dense forms, a family not the record's, the second level pair declared halfway or on a family of real lines, a level above the amplitude bound or beyond an inner face, a sense without a rotation, another world's digest, a missing entry); the lay (the kind, stop with the repeat, the tolerance's form, the seed, the profile with the one-Node seed and its form) and the budget (the least T is the law's inequality's least power of two, 81 den^6 e_num^4 c^2 T^2 >= 1024 num^4 n^2 e_den^4 (den^2 - num^2), and the gate refuses a universe below it); the faces (a receding face on a periodic axis, its sides and a side's word, the inner faces' list, axis and gaps, faces that leave no Node) and the open faces' layer without its receding side; the messages (the list, a lay by the count on a holder of the content, whole or count without tick, the family, the axis, the wave's form and p = 0, the phase's and a transverse wave number's form); the universe (a held row with a dimension, its sources and act, the rotation without the Wronskian, a family without a dimension, its lines' kinds and a mixed record, a shape's form, the Link unit not a power of two, the families' list, a name twice, a row without reads, the pair's form, |num| = den on a massive pair, a rest on the holder of the sign)."""
    universe_beside(tmp_path, charged=True)
    document = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    families = universe.universe_of(document)[1]
    matter, charged = (next(f for f in families if f.name == name) for name in ("matter", "charged"))
    shape, zeros, beside = (4, 2, 1), [0] * 8, {"world_digest": "d", "bodies": [], "messages": []}
    held, one = {"sources": ["form"], "level_weight": 1, "write_weight": 1, "act": "pace"}, [1, *[0] * 7]
    packet = {"family": "matter", "along": "x", "wave": [1, 2], "phase": [0, 1], "amplitude": 1}
    packet.update(top={"x": [0, 0], "y": [0, 0], "z": [0, 0]}, edge={"x": 0, "y": 0, "z": 0})
    pulse = {"family": "gravity", "whole": [0, 0, 0], "count": 1, "tick": 1}  # a holder, no quanta
    face = {"sides": ["low"], "largest": 9, "layers": 1}

    def level(family=matter, read=None, beyond=(), **moving):
        """A mode entry of the family, its levels 0 but for `moving`, read as the record of `read`."""
        levels = {"now": zeros, "before": zeros, **moving}
        entry = {"family": family.name, "pair": list(family.pair), "moving": levels}
        return mode.levels_of(entry, "m", read or family, shape, 10, beyond)

    def laid(**keys):
        return lay.lay_of({"kind": "repeat", "seed": "one_node", **keys}, "lay")

    def receding(boundary="open", **keys):
        return faces.receding_of({"x": {**face, **keys}}, shape, {"x": boundary})

    def rows(*entries):
        return universe.universe_of({**document, "families": list(entries)})

    def sent(**keys):
        return messages.messages_of([{**packet, **keys}], beside, "d", families, shape, 10, ())

    def unphased():  # a message without its phase: refused by name, no phase by omission
        bare = {k: v for k, v in packet.items() if k != "phase"}
        return messages.messages_of([bare], beside, "d", families, shape, 10, ())

    def unacted():  # a held row without its act: refused by name, no act by omission
        return universe.shape_of({"held": {k: v for k, v in held.items() if k != "act"}}, "r")

    refusals = [
        ("must be an object", lambda: keys.keyed(3, "k", ("a",), ())),
        ("unknown key 'b'", lambda: keys.keyed({"b": 1}, "k", ("a",), ())),
        ("lacks the key 'a'", lambda: keys.keyed({}, "k", ("a",), ("a",))),
        ("integer from 1 through 3", lambda: keys.integer(4, "n", 1, 3)),
        (r"must be a Node \[x, y, z\]", lambda: keys.node_of([1, 2], "node", shape)),
        ("beyond the board's inner face", lambda: keys.node_of([1, 1, 0], "node", shape, ((1, 1, 0),))),
        (r"must be a range \[first, last\]", lambda: keys.span_of([1], "span", 4)),
        ("no file stands at that repository path", lambda: keys.document_at({}, "u.json", "u")),
        ("weights the lines of a plane", lambda: keys.weights_of([1, 1], "weights", 2, True)),
        (
            "one integer weight per line of the record, 2 here",
            lambda: keys.weights_of([1], "w", 2, False),
        ),
        ("weights every line of the record at 0", lambda: keys.weights_of([0, 0], "w", 2, False)),
        ("each holder's name to the weight", lambda: keys.reads_of([], "reads")),
        ("read at the weight 0 is no read", lambda: keys.reads_of({"gravity": 0}, "reads")),
        (
            "nonzero Nodes must be flat x-major",
            lambda: mode.pairs_of({"at": [8], "values": [1]}, "l", 8),
        ),
        ("must be 8 integers, one per Node", lambda: mode.pairs_of([1, 2], "level", 8)),
        ("is of the family 'charged' with the pair", lambda: level(charged, matter)),
        ("im_now and im_before together", lambda: level(im_now=zeros)),
        ("lines are no plane", lambda: level(im_now=zeros, im_before=zeros)),
        ("above the amplitude bound A = 10", lambda: level(now=[11, *[0] * 7])),
        ("nothing is laid there", lambda: level(beyond=((0, 0, 0),), now=one)),
        ("a sense without a rotation", lambda: level(charged, im_now=one, im_before=zeros)),
        (
            "is not this world's digest",
            lambda: mode.mode_entries({"world_digest": "a", "bodies": []}, "b", ""),
        ),
        ("has no entry in the mode file", lambda: mode.entry_of([], 0, "bodies[0]")),
        ("kind is one of", lambda: laid(kind="spread")),
        ("stop is declared with the lay 'fixed_point'", lambda: laid(stop=1)),
        (r"tolerance must be \[num, den\]", lambda: laid(tolerance=[1])),
        ("seed is one of", lambda: laid(seed="spread")),
        (r"profile \[centre, neighbour\] is declared with the seed", lambda: laid(profile=[1, 4])),
        (r"profile must be \[centre, neighbour\]", lambda: laid(seed="compact", profile=[1])),
        (
            "below the least T",
            lambda: lay.budget_gate(
                laid(tolerance=[1, 100], confidence=[32, 1]), [(2, 3)], [50], 400, 32768
            ),
        ),
        ("stands on an open or closed axis", lambda: receding("periodic")),
        ("sides lists", lambda: receding(sides=[])),
        ("a side is one of", lambda: receding(sides=["up"])),
        ("faces must be a list", lambda: faces.faces_of({}, shape)),
        ("axis is one of", lambda: faces.faces_of([{"axis": "w", "at": 1, "gaps": []}], shape)),
        ("gaps must be a list", lambda: faces.faces_of([{"axis": "x", "at": 1, "gaps": {}}], shape)),
        (
            "faces leave no Node",
            lambda: faces.faces_of([{"axis": "x", "at": x, "gaps": []} for x in range(4)], shape),
        ),
        ("messages must be a list", lambda: messages.wholes_of({}, families, shape, (), 10)),
        (
            "a family of quanta for a lay by the count",
            lambda: messages.wholes_of([pulse], families, shape, (), 10),
        ),
        (
            "without `tick`",
            lambda: messages.messages_of(
                [{"family": "matter", "whole": [0, 0, 0]}], None, "d", families, shape, 10, ()
            ),
        ),
        ("must name a family of the universe", lambda: sent(family="light")),
        ("along is one of", lambda: sent(along="w")),
        (r"wave must be \[p, q\]", lambda: sent(wave=[1])),
        ("wave's p is 0", lambda: sent(wave=[0, 2])),
        (r"phase must be \[r, s\]", lambda: sent(phase=[1])),
        ("lacks the key 'phase'", unphased),
        ("lacks the key 'seed'", lambda: lay.lay_of({"kind": "repeat"}, "lay")),
        ("confidence, the budget's confidence", lambda: laid(tolerance=[1, 100])),
        ("lacks the key 'act'", unacted),
        (r"transverse.y must be \[r, s\]", lambda: sent(transverse={"y": [1]})),
        (
            "is a held row and declares no dimension",
            lambda: universe.shape_of({"held": {}, "dimension": 1}, "r"),
        ),
        ("held.sources is one of", lambda: universe.shape_of({"held": {**held, "sources": ["x"]}}, "r")),
        ("held.act is one of", lambda: universe.shape_of({"held": {**held, "act": "x"}}, "r")),
        (
            "the act of the holder of the sign",
            lambda: universe.shape_of({"held": {**held, "act": "rotation"}}, "r"),
        ),
        ("lacks the key 'dimension'", lambda: universe.shape_of({}, "r")),
        ("lists its lines' kinds", lambda: universe.shape_of({"dimension": ["x"]}, "r")),
        (
            "mixes real lines and planes",
            lambda: universe.shape_of({"dimension": [REAL_LINE, PLANE_LINE]}, "r"),
        ),
        (
            r"as a shape is \[parts, dimension\]",
            lambda: universe.shape_of({"dimension": [1, 2, 3]}, "r"),
        ),
        (
            "link_unit must be a power of two",
            lambda: universe.universe_of(
                {**document, "integers": {**document["integers"], "link_unit": 3}}
            ),
        ),
        ("families must be a list", lambda: universe.universe_of({**document, "families": {}})),
        ("name must be a name of its own", lambda: rows(*document["families"], document["families"][0])),
        ("lacks the key 'reads'", lambda: rows({"name": "a", "pair": [2, 3], "dimension": 1})),
        (
            r"pair must be \[num, den\]",
            lambda: rows({"name": "a", "pair": [2], "dimension": 1, "reads": {}}),
        ),
        (
            "a massive pair has den above",
            lambda: rows({"name": "a", "pair": [-3, 3], "dimension": 1, "reads": {}}),
        ),
        (
            "only the massless row of the content rests",
            lambda: rows(
                {
                    "name": "a",
                    "pair": [1, 1],
                    "reads": {},
                    "held": {**held, "sources": ["wronskian"], "rest": 5},
                }
            ),
        ),
    ]
    for match, call in refusals:
        refused(match, call)
    least, left = lay.least_action((2, 3), 400, 50, (1, 100), (32, 1)), 81 * 3**6 * 50**2  # e_num = 1
    right = 1024 * 2**4 * 400**2 * 100**4 * (3 * 3 - 2 * 2)  # the law's inequality, T a power of two
    assert least & (least - 1) == 0 and left * least * least >= right > left * least * least // 4
    fixed = lay.lay_of({"kind": "fixed_point", "stop": 2, "passes": 30, "seed": "one_node"}, "lay")
    assert fixed == lay.Lay("fixed_point", 2, 30, None, None, "one_node", None)
    layer = faces.layer_of(shape, (True, False, False), 1, (faces.RecedingFace(0, 1, 9, 1),))
    assert layer == ((0, 0, 0), (0, 1, 0))  # the high side recedes: the low face's two Nodes alone


def test_a_massless_message_lays_no_uniform_mode_and_the_board_refuses_one_that_does(
    tmp_path, monkeypatch
):
    """A massless packet's two levels each sum to 0 over the board on the committed worlds (the generator's `uniform_removed`, ALGEBRA.md, The message lay), and a mode entry whose level sums otherwise is refused by name at the board's construction, through the one lay act's guard (`GameBoard.lay`, `lay.guarded`; the loader builds no board and refuses nothing of this)."""
    for world in ("anticoincidence/one_photon", "two_slits/two_slits", "bell/bell_a_b"):
        board = GameBoard(load_world(EVENTS / f"{world}.json"), lambda line: None)
        for index, family in enumerate(board.families):
            if family.quanta and family.pair[0] == family.pair[1]:
                line = board.states[index].lines[0]
                assert int(line.now.sum(dtype=object)) == 0 and int(line.before.sum(dtype=object)) == 0
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = slit_world(tmp_path, TOOL)  # the generator's packet: the two sums 0, admitted at the door
    mode_path = path.with_suffix(".mode.json")
    mode, board = json.loads(mode_path.read_text(encoding="utf-8")), GameBoard(load_world(path))
    laid = board.states[[f.name for f in board.families].index("charge")].lines[0]
    assert int(laid.now.sum(dtype=object)) == 0 and int(laid.before.sum(dtype=object)) == 0
    for word in ("now", "before"):  # one level moved by 2 at one Node: the act's guard refuses by name
        moved = json.loads(json.dumps(mode))
        moved["messages"][0]["moving"][word]["values"][0] += 2
        mode_path.write_text(json.dumps(moved), encoding="utf-8")
        refusal = refused("wakes the zero mode", lambda: GameBoard(load_world(path)))
        assert f"SUM {word} by 2" in str(refusal) and "'charge'" in str(refusal)


def test_the_loader_refuses_a_massless_family_on_a_box_periodic_on_three_even_axes(
    tmp_path, monkeypatch
):
    """The board against the massless row's second double root (`loader/world.even_box_refused`; the mathematician's reading of the shelved ion's refusal): on the tests' universe, whose gravity and charge rows are massless (the first named), a box of 4 by 4 by 2 periodic on all three axes is refused by name at load, the message naming the family, the shape, the staggered mode (-1)^(x + y + z + t) walked by Rule3's own rounding and the way out (printed); the same box with one odd extent, 4 by 4 by 3, and the even box with its x axis open are admitted, the mode a bounded response there."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_beside(tmp_path)
    world = dict(boundary=dict(x="periodic", y="periodic", z="periodic"), ticks=1, universe="u.json")
    world.update(engine="e.json", bodies=[], messages=[], node_readers=[])

    def written(name, **changes):
        (path := tmp_path / f"{name}.json").write_text(
            json.dumps({**world, **changes}), encoding="utf-8"
        )
        return path

    refusal = str(refused("staggered mode", load_world, written("even", shape=[4, 4, 2])))
    print(refusal)
    assert "'gravity'" in refusal and "[4, 4, 2]" in refusal and "odd extent or open it" in refusal
    assert GameBoard(load_world(written("odd", shape=[4, 4, 3]))).shape == (4, 4, 3)
    opened = dict(x="open", y="periodic", z="periodic")
    assert (
        GameBoard(load_world(written("open", shape=[4, 4, 2], boundary=opened, face_depth=1))).shape[0]
        == 4
    )


def test_the_loader_derives_the_pair_of_two_bound_records(tmp_path):
    """The pair of two bound records (ALGEBRA.md, a hypothesis under its own name; tools/derivations/two_body.py): from two [2, 3] rows at the declared den 6,000 the loader derives the relative part's pair [5237, 6000] and the centre's [2449, 6000] by the division act (the floats' 5,237.2 and 2,449.5), their inertias 3 tan omega one half and twice the record's within the pair's rounding; refused by name: a massless constituent, a name declared later or never, a den below 1, both parts or neither, a pair of three numbers."""
    universe_beside(tmp_path)
    document = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))

    def row(name, pair):
        return {"name": name, "pair": pair, "dimension": 2, "reads": {}}

    rows = [*document["families"], row("a", [2, 3]), row("b", [2, 3])]
    relative, centre = {"relative_of": ["a", "b"], "den": 6000}, {"centre_of": ["a", "b"], "den": 6000}
    families = universe.universe_of(
        {**document, "families": [*rows, row("mu", relative), row("M", centre)]}
    )[1]
    pairs = {family.name: family.pair for family in families}
    assert (pairs["mu"], pairs["M"]) == ((5237, 6000), (2449, 6000))
    inertia = {name: (den * den - num * num) ** 0.5 / num for name, (num, den) in pairs.items()}
    assert abs(inertia["mu"] / inertia["a"] - 0.5) < 2e-3 and abs(inertia["M"] / inertia["a"] - 2) < 2e-3
    for pair, match in (
        ({"relative_of": ["a", "gravity"], "den": 6000}, "massive pair of positive num"),
        ({"relative_of": ["a", "nobody"], "den": 6000}, "no family declared before it"),
        ({"relative_of": ["a", "b"], "den": 0}, "den must be an integer from 1"),
        ({**relative, **centre}, "one of the two parts"),
        ({"den": 6000}, "one of the two parts"),
        ([2, 3, 4], "must be \\[num, den\\]"),
    ):
        refused(match, universe.universe_of, {**document, "families": [*rows, row("x", pair)]})


def test_the_region_rule_refuses_a_node_named_twice_and_reads_the_extent_through_the_wrap(
    tmp_path, monkeypatch
):
    """The loader's region rule against two admissions the advisor's breaker found over the engine at 7756546d (#1793; `loader/world.regions_of_the_law` with `loader/faces.extent_across`): (a) a region naming one Node twice, [[2, 2, 2], [2, 2, 2]], admitted before as a region of two Nodes while it stands on one, is refused by name with the reader and the Node, and a region of two distinct Nodes is admitted; (b) under the slit world's message, the wave [1, 4] along x and so a half wavelength of 4 Nodes across y, a region at y = 0 and y = 4 of a board 5 Nodes on y periodic on y is 2 Nodes across through the wrap, read before as 5 from its least to its greatest coordinate, and is refused by name with the extent 2, while on y open the two Nodes meet through no wrap and the region is refused as one in pieces, the connection rule standing before the extent's; the extent's arithmetic on the ring of 5 written by hand: 0 and 4 are 2 Nodes across wrapped and 5 open, 1, 2 and 3 are 3 either way, the whole ring 5 and one coordinate 1 (every refusal's words printed)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_beside(tmp_path)
    world = dict(shape=[4, 4, 3], boundary=dict(x="periodic", y="periodic", z="periodic"), ticks=1)
    world.update(universe="u.json", engine="e.json", bodies=[])
    for name, positions in (("twice", [[2, 2, 2], [2, 2, 2]]), ("two", [[2, 2, 2], [2, 2, 1]])):
        readers = [{"name": name, "positions": positions}]
        (tmp_path / f"{name}.json").write_text(json.dumps({**world, "node_readers": readers}), "utf-8")
    refusal = str(refused("names the Node", load_world, tmp_path / "twice.json"))
    print(refusal)
    assert "'twice'" in refusal and "[[2, 2, 2]] twice" in refusal
    assert load_world(tmp_path / "two.json").node_readers[0].positions == ((2, 2, 2), (2, 2, 1))
    narrow = {**PACKET, "top": {**PACKET["top"], "y": [0, 4]}}  # the slit's packet over 5 Nodes of y
    board = dict(shape=[24, 5, 1], messages=[narrow])
    board["node_readers"] = [{"name": "ring", "positions": [[20, 0, 0], [20, 4, 0]]}]
    wrapped = slit_world(
        tmp_path, TOOL, "wrap", boundary=dict(x="open", y="periodic", z="periodic"), **board
    )
    refusal = str(refused("under half the wavelength", load_world, wrapped))
    print(refusal)
    assert (
        "'ring' is 2 Node(s) across the y axis, read through its wrap" in refusal and "[1, 4]" in refusal
    )
    print(refused("not one connected region", load_world, slit_world(tmp_path, TOOL, "open", **board)))
    assert faces.extent_across([0, 4], 5, True) == 2 and faces.extent_across([0, 4], 5, False) == 5
    assert [faces.extent_across(c, 5, True) for c in ([1, 2, 3], range(5), [2, 2])] == [3, 5, 1]
