def test_each_engine_row_of_the_claims_table_holds_inside_its_fence_and_breaks_outside(
    tmp_path, monkeypatch
):
    """The claims table's rows of kind (e) (the paper's claims table (kept outside this tree): the marked sentences' rows 26, 27, 76 and 133, the hand-named rows E.1 to E.3, the results table's row 1 and S.61, with S.59's re-lay (R332) and S.42's credit current (R307) as the engine holds them) as unit tests on the engine, one nested function per row, each quoting the row's opening words and its breaker and asserting the claim inside its fence and the break outside it, and the owner's shout (#1793 comment 5982567335: logic at a Node that is not of Rule3's form is shouted) as the inventory of the engine's write sites outside core/rule3, each with its law line; one function, so that the file is the test alone and the tests' ratchet's room, given per named function, covers it (tools/tests_shape.py; ENGINE.md section 9); S.62 has no engine breaker beyond the provenance and no row here."""
    import ast
    import contextlib
    import copy
    import importlib
    import json
    import sys
    import time
    from math import atan2, degrees, isqrt

    import numpy as np

    from event_universe import flux, node_detector, readings, records, world_files
    from event_universe.core import paces
    from event_universe.core.ports import Wrap
    from event_universe.core.rule3 import rule_integers
    from event_universe.features.click import Face
    from event_universe.lattice import Lattice
    from event_universe.loader.derived import quanta_records
    from event_universe.loader.universe import FAMILY_KEYS, universe_of
    from event_universe.reports import front
    from event_universe.world_files import load_world
    from tests.laws import BACK, EVENTS, PACKET, ROOT, TOOL, UNIVERSE, refused, slit_world
    from tests.laws_content import ZENO_4, ZENO_ATOM, opened, with_content
    from tests.laws_read import redeclared

    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    source, called = ROOT / "src" / "event_universe", set()
    packet = {**PACKET, "top": {"x": [3, 3], "y": [0, 4], "z": [0, 4]}, "edge": {"x": 2, "y": 0, "z": 0}}
    wrapped = dict(x="open", y="periodic", z="periodic")  # the box: x open, y and z of extent 5 wrapping
    box = slit_world(
        tmp_path, TOOL, "box", shape=[12, 5, 5], boundary=wrapped, faces=[], packets=[packet]
    )

    def seen(frame, event, _arg):  # the engine functions a run calls, S.61's rows read under the profile
        if event == "call" and frame.f_code.co_filename.startswith(str(source)):
            called.add((frame.f_code.co_filename[len(str(source)) + 1 :], frame.f_code.co_qualname))

    @contextlib.contextmanager
    def profiled():
        sys.setprofile(seen)
        try:
            yield
        finally:
            sys.setprofile(None)

    def same(a, b):
        return all(np.array_equal(getattr(a, k), getattr(b, k)) for k in ("now", "before", "remainder"))

    def arrays_of(snapshot):
        return dict(pair for family in snapshot for pair in family)

    def the_step_is_reversible_to_the_bit():
        """Row 27 and the results table's row 1, "The whole run therefore goes back: N intervals forward and N back return every array of every family bit for bit, provided every number an act read at an interval's start is kept" and "Rule3's step is reversible to the bit"; the breaker: random states on 2x2x2 to 4x4x4 boards (every face kind, the pairs [1, 1] to [4000, 6000], uneven Link factors, the width 63) forward then the inverse bit for bit, a face's kept value presented again on the way back; outside, a face that moves between the step and its inverse, or a face forgotten, the read not kept; the whole lattice's gate on the box here, on the closed cube in tests/test_the_node.py and on the one rule's integers in tests/test_rule3.py."""
        draw, wraps = np.random.default_rng(1), [Wrap(True, True, True), Wrap(False, True, True)]
        wraps, kind = [*wraps, Wrap(False, False, False)], np.int64
        tried = misses = 0
        for shape in ((2, 2, 2), (3, 3, 3), (4, 4, 4), (3, 2, 4)):
            for wrap in wraps:
                for num, den in ((1, 1), (2, 3), (4000, 6000), (-1, 2)):
                    content = draw.integers(-30, 60, shape).astype(kind)
                    factors = tuple((256 + draw.integers(-40, 40, shape)).astype(kind) for _ in range(6))
                    clock, pace = paces.node_paces(6000, content)
                    rule = rule_integers(num, den, 6000, clock, pace, factors, 16)
                    now, before = (draw.integers(-60, 60, shape).astype(np.int64) for _ in (0, 1))
                    remainder = draw.integers(0, 2**40, shape).astype(object) % int(rule.wall)
                    record = records.Record(now, before, remainder.astype(np.int64))
                    back = flux.step_line(flux.step_line(record, rule, wrap), rule, wrap, -1)
                    tried, misses = tried + 1, misses + (not same(back, record))
        assert (tried, misses) == (48, 0)
        shape, closed, periodic = (3, 3, 3), Wrap(False, True, True), Wrap(True, True, True)
        content = draw.integers(-30, 60, shape).astype(np.int64)
        clock, pace = paces.node_paces(6000, content)
        rule = rule_integers(2, 3, 6000, clock, pace, None, 16)
        now, before = (draw.integers(-60, 60, shape).astype(np.int64) for _ in (0, 1))
        record = records.Record(now, before, np.full(shape, int(rule.wall) // 2, dtype=np.int64))
        face = Face(0, 0, (1, 1, 1), (0,), 1)
        with profiled():
            after = flux.step_line(record, rule, closed, 1, 0, ([face], (0, 0, 0)))
        assert face.value is not None and int(after.now[1, 1, 1]) == 0  # the hole to 0 at the Node
        assert same(flux.step_line(after, rule, closed, -1, 0, ([face], (0, 0, 0))), record)
        forgotten, moved = (
            flux.step_line(after, rule, closed, -1),
            flux.step_line(after, rule, periodic, -1),
        )
        off = int((moved.before != before).sum()), int((forgotten.before != before).sum())
        assert off[0] > shape[1] * shape[2] and off[1] == 1  # outside: the read not kept
        with profiled():  # the load, the start and the guard under the profile as well
            board = Lattice(load_world(box))
            kept = {board.interval: BACK.snapshot(board)}
            for _ in range(4):
                board.step(), kept.__setitem__(board.interval, BACK.snapshot(board))
            for _ in range(4):
                board.step_inverse()
                assert BACK.first_difference(kept[board.interval], BACK.snapshot(board)) is None
        return (
            f"{tried} random boards, {misses} misses; the face's value {face.value} presented again returns; "
            f"the face moved from closed to periodic: {off[0]} of {now.size} Nodes' level before differ, "
            f"the face forgotten: {off[1]}; the box 4 forward and 4 back MATCH"
        )

    def the_gate_runs_across_the_click_and_the_write_is_the_whole_re_lay():
        """Row 26, "The back-in-time gate is exact between clicks, and runs across a click and the erasure intervals that follow it, treating the values a NodeDetector presented at its Ports as given", and S.59's engine clause (R332: a body's write is its whole re-lay); under the content (2026-10-20) the window's turn is scaled to the body's own proper interval by its clock (`meeting.turned_labels`, `paces.turn_factor`), so the test's re-derivation of the entered direction at the vacuum's clock stands about nine degrees from the engine's write, which is pinned at the first Node with its magnitude the whole lay's, the fold to the other Node read from it (at the content 0 the two agreed bit for bit); the breaker: the Zeno n = 4 world's declaration (deleted 2026-10-20 at the ninth, inlined under the content of the born universe, its box opened along x as the content's sink and its window the lay's passage derived at load, 21) and its click at 42, the body's absorption of its dense drive (72 on the shipped world under the generator); between the writes (the null close's re-lay at 21, which under the content moves the standing body's four lines and writes their lay lines, and the absorption at 42) back bit for bit with nothing crossed, across the click with the lays crossed from their lines MATCH (tests/test_the_meeting.py and tests/test_the_node_detector.py hold the shipped gates); outside, the blind run back with nothing crossed misses first at the latest write, the content holder's write remainder the first array to differ (atom.lines at the content 0); outside, the step back across the click with nothing crossed misses at the lay's Node, the draw forward only; the write at 72 the whole re-lay, the part entered at the standing levels of one quantum over the two Nodes in the leaving part's sense and in its direction turned by the arriving record's phase, atan2(Y', X) of the window's two sums (the phase passes with the quantum, ALGEBRA.md L739 and the ledger's row 16), the part left at 0, every remainder at the lay's origin, where the twin without the draw reads and writes nothing; the expected levels the law's own integers and no engine function, written here from the drive's levels at the Nodes over the window (a_t = SUM d_i A_i div A half up, the reference records by Chebyshev's line at the declared pair, X and Y' over the window, N = isqrt(X^2 + Y'^2), the direction (90 X div N, 90 Y' div N) at the amplitude A_i and the level before by the record's own rotation, the mathematician's reading of the witness, #1793 comment 5983031085), the float turn one level off in im through the act's two floors."""
        world = opened(json.loads(json.dumps(ZENO_4)))  # the Zeno n = 4 declaration under the content
        (tmp_path / "zu.json").write_text(json.dumps(with_content(ZENO_ATOM)), encoding="utf-8")
        redeclared(world).update(universe="zu.json")
        record = {k: v for k, v in world["bodies"][0].items() if k in ("family", "nodes", "parts")}
        paths = {name: tmp_path / f"{name}.json" for name in ("drawn", "undrawn")}
        for name, bodies in (("drawn", world["bodies"]), ("undrawn", [record])):
            paths[name].write_text(json.dumps({**world, "bodies": bodies}), encoding="utf-8")
            TOOL.main(["--input", str(paths[name])])
        twin, undrawn_at, drive, previous = Lattice(load_world(paths["undrawn"])), {}, [], None
        body = world["bodies"][0]
        at = [tuple(int(v) for v in n["node"]) for n in body["nodes"]]
        pulse = [f.name for f in twin.families].index(body["transitions"][0]["drive"])
        with profiled():  # the reader's books made at the load, S.61's line 27, under the profile too
            board = Lattice(load_world(paths["drawn"]), (lines := []).append)
            kept = {board.interval: BACK.snapshot(board)}
            for _ in range(75):
                if not any(x["event"] == "credit" and x["count"] for x in lines):
                    previous = copy.deepcopy(board)  # the board before the first click
                board.step(), twin.step()
                kept[board.interval] = BACK.snapshot(board)
                undrawn_at[twin.interval] = BACK.snapshot(twin)
                drive.append([int(twin.states[pulse].lines[0].now[n]) for n in at])  # d_i, a_t's read
        credits, lays = ([x for x in lines if x["event"] == event] for event in ("credit", "lay"))
        clicks = [x for x in credits if x["count"]]  # the absorption; the null closes' re-lays beside it
        writes = sorted(
            {x["interval"] for x in lays}
        )  # every write of the body: a null re-lay or the click
        click_at = clicks[0]["interval"]  # the first click, the body's read of the board at a close
        since = max(w for w in writes if w < click_at)  # the null close's re-lay before the click
        between, undrawn = previous, undrawn_at[click_at]  # the board before it, the twin at it
        window = board.world.bodies[0].detector.draw.window  # the lay's passage derived at load, 21
        assert window == 21 and click_at % window == 0 and previous is not None  # at a close, 2026-10-20
        assert (click_at, writes[: writes.index(click_at)]) == (
            42,
            [21],
        )  # the null re-lay at 21 before it
        assert (
            len([x for x in lays if x["interval"] == click_at]) == 8
        )  # the re-lay's four lines at two Nodes
        for _ in range(click_at - 1 - since):  # between the writes: nothing crossed, bit for bit
            between.step_inverse()
            assert BACK.first_difference(kept[between.interval], BACK.snapshot(between)) is None
        blind, miss = copy.deepcopy(board), None  # outside: back across the click with nothing crossed
        for _ in range(75):
            blind.step_inverse()
            if (found := BACK.first_difference(kept[blind.interval], BACK.snapshot(blind))) is not None:
                miss = (blind.interval, *found)
                break
        last = writes[-1]  # the blind run back crosses the latest write first
        assert miss is not None and miss[0] == last - 1  # the latest write's interval, uncrossed
        assert (
            miss[1] == "gravity.write_remainders[0]"
        )  # the holder's write remainder first (2026-10-20)
        for _ in range(75):  # across the click with the lays crossed from their lines
            BACK.crossed(board, lines), board.step_inverse()
            assert BACK.first_difference(kept[board.interval], BACK.snapshot(board)) is None
        atom = [f.name for f in board.families].index(body["family"])
        (num, den), action = board.families[atom].pair, board.world.quantum_action
        first, second = (
            next(
                x
                for x in lays
                if x["line"] == k and tuple(x["node"]["at"]) == at[0] and x["interval"] == click_at
            )
            for k in (0, 1)
        )
        (re, re_before), (im, im_before) = first["before"][:2], second["before"][:2]
        sense = 1 if re * im_before - im * re_before >= 0 else -1
        gap, (rn, rd) = den * den - num * num, body["transitions"][0]["resonance"]
        amp = isqrt(isqrt((action * den) ** 2 // (4 * gap)) // len(at))
        norm, scale, bound = max(isqrt(len(at) * amp * amp), 1), 1, board.world.amplitude_bound
        while 2 * (2 * scale * bound * window) ** 2 <= board.world.width:
            scale *= 2
        cosine = (scale, (scale * rn + rd // 2) // rd)  # (r_0, r_-1)
        sine = (0, -(isqrt(scale * scale * (rd * rd - rn * rn)) // rd))  # (r'_0, r'_-1)
        sums = [0, 0]
        for interval, levels in enumerate(drive, 1):
            total = sum(d * amp for d in levels)
            arrived = (abs(total) + norm // 2) // norm * (1 if total >= 0 else -1)
            if click_at - window < interval <= click_at:
                sums = [sums[0] + arrived * cosine[0], sums[1] + arrived * sine[0]]
            cosine, sine = (((2 * rn * r + rd // 2) // rd - p, r) for r, p in (cosine, sine))
        size = isqrt(sums[0] ** 2 + sums[1] ** 2)
        turned = ((re * sums[0] - im * sums[1]) // size, (re * sums[1] + im * sums[0]) // size)
        length, root = isqrt(turned[0] ** 2 + turned[1] ** 2), isqrt(gap)
        entered = (turned[0] * amp // length, turned[1] * amp // length)
        e0, e1 = entered
        before = ((e0 * num - sense * e1 * root) // den, (e1 * num + sense * e0 * root) // den)
        written, stood, half = arrays_of(kept[click_at]), arrays_of(undrawn), board.half_wall(atom)

        def read(a, here, *ks):  # [re now, re before, im now, im before] of a part's two lines
            return [int(a[f"atom.lines[{k}].{w}"][here]) for k in ks for w in ("now", "before")]

        vacuum_pace = [
            entered[0],
            before[0],
            entered[1],
            before[1],
        ]  # the re-derivation at the vacuum's clock
        direction = read(
            written, at[0], 2, 3
        )  # the engine's write at the first Node: the whole lay entered
        assert (
            direction
            == [
                68,
                -59,
                59,
                67,
            ]
        )  # pinned 2026-10-20 under the content with the twist deleted (the fold's quarter turn had turned it to [58, -69, 69, 57]); the vacuum pace's form beside
        assert (
            isqrt(direction[0] ** 2 + direction[2] ** 2)
            == isqrt(entered[0] ** 2 + entered[1] ** 2)
            == amp
        )
        apart = degrees(atan2(direction[2], direction[0]) - atan2(entered[1], entered[0]))
        for here in at:
            assert read(written, here, 2, 3) == list(
                direction
            )  # the whole lay entered at every Node, nothing written for the piece's momentum
            assert read(written, here, 0, 1) == [0, 0, 0, 0] == read(stood, here, 2, 3)  # left; e
            same_until = read(arrays_of(undrawn_at[since - 1]), here, 0, 1)  # the twin's g, unwritten
            assert same_until == read(
                arrays_of(kept[since - 1]), here, 0, 1
            )  # one board before the re-lay
            assert read(arrays_of(undrawn_at[since]), here, 0, 1) != read(
                arrays_of(kept[since]), here, 0, 1
            )
            assert all(int(written[f"atom.lines[{k}].remainder"][here]) == half for k in range(4))
        assert sums[1] != 0 and entered != (re, im)  # the arrival's phase is not 0: the direction turned
        return (
            f"the click at {clicks[0]['interval']} with {len(lays)} lay lines; between the writes {since} and {click_at} "
            f"back bit for bit; across it with the lays crossed MATCH; without the crossing MISS at "
            f"{miss[0]}, {miss[1]} at {miss[2]}; the re-lay of one quantum over {len(at)} Nodes: the leaving "
            f"direction ({re}, {im}) at the sense {sense} turned by the arrival (X, Y') = {tuple(sums)} at R = "
            f"{scale}, {degrees(atan2(sums[1], sums[0])):.3f} degrees, to {entered} with the level before {before} at the "
            f"vacuum's clock, the engine's write {direction} at the body's own clock, {apart:.2f} degrees apart "
            f"(the vacuum pace's form {vacuum_pace}); the part left at 0, remainders {half}"
        )

    def the_credit_books_the_conserved_forms_current():
        """S.42's and the clicks table's row 40 engine clause (R307: the credit books the conserved form's own current through the front Ports, the Link's factor squared the one weight); the breaker: a chain of 8 with two declared regions of two Nodes in the tests' universe at random levels, the content holder's axis lines at 0 and then within 12, one interval: the booked inflow per boundary Node equals the sum over the region's front Ports of Q_ij F_ij from the engine's own read and currents, and equals G^2 times the plain current where no Link carries tension; outside, under tension the plain current misses it; the share identity over a passage stands in tests/test_the_node_detector.py."""
        draw = {"window": 3}
        regions = [{"name": "left", "positions": [[1, 0, 0], [2, 0, 0]]}]
        regions.append({"name": "right", "positions": [[5, 0, 0], [6, 0, 0]]})
        world = dict(shape=[8, 1, 1], boundary=wrapped, face_depth=1, intervals=4, universe="u.json")
        world.update(bodies=[], draw=draw, node_detectors=regions)
        (chain := tmp_path / "chain.json").write_text(json.dumps(world), encoding="utf-8")
        agreed, plain_too = 0, {}
        for tension in (0, 12):
            board, levels = Lattice(load_world(chain)), np.random.default_rng(3)
            for index, (family, state) in enumerate(zip(board.families, board.states, strict=True)):
                origin = np.full(board.shape, board.half_wall(index), dtype=board.kind)
                if family.quanta:
                    shape = (2, *board.shape)
                    picks = [levels.integers(-300, 300, shape).astype(board.kind) for _ in state.lines]
                    state.lines = [records.Record(now, before, origin) for now, before in picks]
                if family.held and not family.wronskian:  # a well, and axis lines where asked
                    well = levels.integers(0, 40, board.shape).astype(board.kind)
                    state.lines[0] = records.Record(well, well.copy(), state.lines[0].remainder)
                    for k in range(1, len(state.lines)):
                        axis = levels.integers(-tension, tension + 1, board.shape).astype(board.kind)
                        state.lines[k] = records.Record(axis, axis.copy(), state.lines[k].remainder)
            own, union, expected = board.declared_board(), node_detector.node_detector_nodes(board), {}
            for detector in [r for r in board.node_detectors if r.declared]:
                facing = front(detector.nodes, board.wrap, union, own)
                for index in board.order:
                    weighed = plain = np.zeros(board.shape, dtype=object)
                    for number in quanta_records(board.families, index):
                        record = board.lines_of(index, number)
                        currents = readings.currents_of(
                            board.families[index].pair[0], record, board.wrap
                        )
                        factors = board.read(index, 1, number)[1]
                        for port in range(6):
                            flow = np.where(facing[port], currents[port].astype(object), 0)
                            factor = np.broadcast_to(np.asarray(factors[port]), board.shape)
                            weighed, plain = weighed + factor.astype(object) * flow, plain + flow
                    expected[index, detector.name] = (weighed, plain)
            board.step()
            square = board.unit * board.unit
            for (index, name), (weighed, plain) in expected.items():
                book = board.credit.intake.get((index, name), {})
                booked = {tuple(int(v) for v in k): sum(v) for k, v in book.items()}
                assert booked == {n: int(weighed[n]) for n in np.ndindex(board.shape) if weighed[n] != 0}
                scaled = {n: square * int(plain[n]) for n in np.ndindex(board.shape) if plain[n] != 0}
                agreed, plain_too[tension, index, name] = agreed + 1, booked == scaled
            with profiled():  # the window of 3 closes: the credit's one division (S.61, line 12)
                board.step(), board.step()
        assert all(plain_too[k] for k in plain_too if k[0] == 0)
        assert not all(plain_too[k] for k in plain_too if k[0] == 12)
        return (
            f"{agreed} books of (tension, family, region) equal to the sum over the front Ports of Q_ij F_ij; "
            f"equal to G^2 times the plain current at {sorted(k for k, ok in plain_too.items() if ok)}, "
            f"not at {sorted(k for k, ok in plain_too.items() if not ok)}"
        )

    def the_loader_refuses_a_familys_third_key_by_name():
        """Row 76, "(i) a family is a band of the rule, and its row holds only its two keys; (ii) there are three exact massive rotations"; the breaker: the loader on the tests' universe, a family's row with a key beyond its own refused by name, its own keys admitted ((ii) the row above's, kind (a)); here every row of the tests' universe with a key beyond the loader's five refused by name, the refusal naming the row and the keys it may hold, a row without its pair refused by name, and every shipped universe file admitted with its families."""
        document = json.loads(UNIVERSE.read_text(encoding="utf-8"))
        rows = document["families"]
        for k, row in enumerate(rows):
            others = [*rows[:k], {**row, "band": [1, 3]}, *rows[k + 1 :]]
            bad = {**document, "families": others}
            found = refused(rf"families\[{k}\] holds the unknown key 'band'", universe_of, bad)
            assert str(list(FAMILY_KEYS)) in str(
                found
            )  # the loader names its own keys, `exchange` among them
        bare = {k: v for k, v in rows[0].items() if k != "pair"}
        refused("lacks the key 'pair'", universe_of, {**document, "families": [bare, *rows[1:]]})
        shipped = {}
        for path in sorted(EVENTS.rglob("*.json")):
            if not path.name.endswith(".mode.json"):
                document = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(document, dict) and set(document) == {"integers", "families"}:
                    shipped[path.relative_to(EVENTS).as_posix()] = len(universe_of(document)[1])
        assert len(shipped) >= 10 and all(shipped.values())
        return (
            f"{len(rows)} rows of the tests' universe each refused by name with a key beyond its own, a row without its "
            f"pair refused by name; {len(shipped)} shipped universe files admitted, their families {shipped}"
        )

    def two_records_laid_equal_are_identical_and_one_apart_diverge_at_one_link_per_interval():
        """Row 133, "The two parts of one beam, laid equal, are two records of one family stepped by the same line along the same path, and they are identical bit for bit"; the breaker: two records of one family laid equal on the tests' universe and stepped by the engine, every array equal bit for bit at every interval; laid one level apart at one Node they differ and the difference propagates at one Link per interval, the causal bound; here two lattices of the box, the light packet laid alike, 20 intervals bit for bit; the twins with one level more at one Node of the packet and with 200 more differ, every differing Node within t Links of it in the Link metric at the interval t, the kick of 200 reaching t exactly, the kick of one riding the carried remainders behind it within the causal bound and never swallowed, its reach printed ([1, 1, 2, 3, 4, 5] at the packet laid at the content-0 band, [1, 1, 2, 2, 2, 3] at the packet laid at the declared rest's paces: a one-level difference crosses a floor boundary at the frontier only where the remainders admit it; the one-Link reach of every act is tests/test_the_node.py's)."""
        first, second, at = Lattice(load_world(box)), Lattice(load_world(box)), (6, 2, 2)
        light = [f.name for f in first.families].index("charge")
        kicked = {kick: copy.deepcopy(first) for kick in (1, 200)}
        for kick, board in kicked.items():
            board.states[light].lines[0].now[at] += kick
        extents, reach = first.shape, {kick: [] for kick in kicked}

        def distance(here):  # the Link metric about `at`: x open, y and z wrapping
            dx, dy, dz = (abs(int(here[a]) - at[a]) for a in range(3))
            return dx + min(dy, extents[1] - dy) + min(dz, extents[2] - dz)

        def apart(a, b):  # the Nodes at which two lattices' arrays differ
            arrays = zip(sum(BACK.snapshot(a), []), sum(BACK.snapshot(b), []), strict=True)
            return [n for (_, x), (_, y) in arrays for n in np.argwhere(x != y)]

        for interval in range(1, 21):
            first.step(), second.step()
            assert not apart(first, second)  # bit for bit
            for kick, board in kicked.items() if interval <= 6 else ():
                board.step()
                reach[kick].append(far := max(distance(n) for n in apart(first, board)))
                assert far <= interval  # the causal bound
        assert reach[200] == list(range(1, 7))
        assert all(1 <= far <= t for t, far in enumerate(reach[1], 1))  # never swallowed, causal
        return (
            f"two lattices laid alike identical bit for bit over 20 intervals; the farthest differing Node "
            f"per interval, in Links: the kick of 200 {reach[200]}, the kick of 1 {reach[1]}"
        )

    def the_owners_shout_is_the_inventory_of_the_write_sites_outside_rule3():
        """Rows E.1 to E.3, "The engine holds no number, no formula, no family name and no flag, and every primitive is one folder found by its name", "Each act is a call of Rule3 on whole-board arrays of integers at a declared width, every neighbour read through a Port" and "It holds no number of physics, no formula, no family's name and no flag"; the breaker, the owner's rule (#1793 comment 5982567335): every act of the engine on a Node's levels is Rule3's one line or the division act with the half, and logic found at a Node that is not of Rule3's form is shouted; here the inventory of every function of src/event_universe that writes a Node's levels or remainder outside core/rule3, an assignment into a line's `now`, `before` or `remainder` or into a NodeState's `lines` or `write_remainders`, a `Record(...)` built or a `replace(...)` of those fields (an ast walk over the state's own names, no arithmetic read), each with the law's line its own docstring stands on; a site the inventory does not name fails by the function's name, the shout, a named site that is gone fails too, and tools/record_code_shape.py counts the same sites per file."""
        law = (
            "ALGEBRA.md",
            "Rule3",
            "features/",
        )  # a law line by its anchor, the rule by its name or an act by its folder
        fields, state = {"now", "before", "remainder"}, {"lines", "write_remainders"}

        def owner(item, parents):  # the qualified name of the function an ast node stands in
            names = []
            while item in parents:
                names += [item.name] if isinstance(item, ast.FunctionDef | ast.ClassDef) else []
                item = parents[item]
            return ".".join(reversed(names))

        def writes(item):  # the sites of one ast node, by kind
            if isinstance(item, ast.Assign | ast.AugAssign | ast.AnnAssign):
                targets = item.targets if isinstance(item, ast.Assign) else [item.target]
                walked = (a for t in targets for a in ast.walk(t) if isinstance(a, ast.Attribute))
                return [f"assigns .{a.attr}" for a in walked if a.attr in fields | state]
            if isinstance(item, ast.Call):
                func = item.func
                callee = func.id if isinstance(func, ast.Name) else getattr(func, "attr", None)
                if callee == "Record":
                    return ["builds a Record"]
                if callee == "replace":
                    return [f"replaces .{k.arg}" for k in item.keywords if k.arg in fields]
            return []

        found, docs = {}, {}
        for path in sorted(source.rglob("*.py")):
            if path == source / "core" / "rule3.py":
                continue
            tree, name = ast.parse(path.read_text(encoding="utf-8")), path.relative_to(source).as_posix()
            parents = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
            for item in ast.walk(tree):
                key = f"{name}::{owner(item, parents)}"
                for site in writes(item):
                    found.setdefault(key, []).append(f"{item.lineno} {site}")
                if isinstance(item, ast.FunctionDef):
                    docs[key] = ast.get_docstring(item) or ""
        unnamed = sorted(name for name in found if not any(word in docs.get(name, "") for word in law))
        assert not unnamed, (
            f"shout: a write site outside Rule3 whose function names no law line: {unnamed}"
        )
        for name in sorted(found):
            print(f"  {name}: {', '.join(found[name])}")
        sites = sum(len(v) for v in found.values())
        return f"{len(found)} functions with {sites} write sites outside core/rule3, each naming its law line"

    def the_engines_derivation_ledger_names_a_function_per_act():
        """S.61, "The engine's derivation ledger: each of the 26 rows an engine act sourced to the law's line and a function at the clean main; the breaker calls the function on the tests' universe"; here the ledger of ALGEBRA.md (The engine's derivation ledger, 29 lines) with one engine function per line, none for the integer floor (28, a bound) and the telegraph's counter (29, a finding): every named function stands in the engine, and the lines the runs above exercise (the box and the chain in the tests' universe, the shipped Zeno world) are called in them, read under the profile; the sign current, the emission, the conversion, the front and the receding face stand by name and by nothing else, their calls in tests/test_the_bound_body.py, tests/test_the_emission.py, tests/test_the_meeting.py and tests/test_the_node.py."""
        ledger = {
            1: ("node.py", "read"),
            2: ("flux.py", "step_line"),
            3: ("core/paces.py", "node_paces"),
            4: ("node.py", "guarded"),
            5: ("features/start/__init__.py", "rest"),
            6: ("node.py", "held_write_at"),
            7: ("features/currents/__init__.py", "tension"),
            8: ("readings.py", "sense_current_of"),
            9: (
                "node.py",
                "phased",
            ),  # the sign holder rotates the plane: the Link phase by its level (Part C)
            10: ("core/ports.py", "arrival"),
            11: ("reports.py", "entering"),
            12: ("credit.py", "quanta_through"),
            13: ("lists.py", "absorption"),
            14: ("resonance.py", "window_turn"),
            15: ("features/click/__init__.py", "drawn_from"),
            16: ("lists.py", "exchange"),
            17: ("emission.py", "emitted_quantum"),
            18: None,  # the conversion left the engine on 2026-10-20 with its world, a hypothesis
            19: ("lists.py", "null_window"),
            20: ("features/click/__init__.py", "presented"),
            21: ("front.py", "erased"),
            22: ("growth.py", "resize"),
            23: ("bookings.py", "booked_sources"),
            24: ("loader/keys.py", "keyed"),
            25: ("records.py", "row_levels"),
            26: ("lattice.py", "Lattice.step_inverse"),
            27: ("resonance.py", "references_of"),
            28: None,
            29: None,
        }
        by_name = {8, 17, 18, 21, 22}  # the lines no run here exercises: they stand by name alone
        for line, act in ledger.items():
            if act is None:
                print(f"  line {line}: no engine function, a bound or a finding by name")
                continue
            path, qualname = act
            dotted = path.removesuffix(".py").removesuffix("/__init__").replace("/", ".")
            module = importlib.import_module(f"event_universe.{dotted}")
            function = module
            for part in qualname.split("."):
                function = getattr(function, part)
            assert callable(function), act
            ran = (path, qualname) in called
            assert ran == (line not in by_name), (line, act, ran)
            print(f"  line {line}: {path}::{qualname} {'called' if ran else 'stands by name'}")
        named = sum(act is not None for act in ledger.values())
        return f"{named} lines with a function, {named - len(by_name)} called in the runs above, {len(by_name)} by name"

    def the_rows_of_the_deleted_worlds_stand_at_the_tag():
        """H4 (iv) of the reader's ruling of 2026-10-20: the claims table's rows that reported a deleted world's run (S.50's telegraph, long:S.57's anticoincidence, long:S.59's Zeno curve) stand at the tag with the mark, the claim standing at the tag v1.1.0 where the tree no longer runs the world; no other row carries it."""
        table = json.loads(
            (ROOT / "papers" / "one_rule" / "claims_breakers.json").read_text(encoding="utf-8")
        )
        mark = "world deleted 2026-10-20 at the ninth; the claim stands at the tag v1.1.0"
        marked = {key for key, row in table.items() if row.get("mark") == mark}
        assert marked == {"S.50", "long:S.57", "long:S.59"} and not any(
            "mark" in row and row["mark"] != mark for row in table.values()
        ), marked
        return f"{len(marked)} rows marked: {sorted(marked)}"

    for act in (
        the_step_is_reversible_to_the_bit,
        the_rows_of_the_deleted_worlds_stand_at_the_tag,
        the_gate_runs_across_the_click_and_the_write_is_the_whole_re_lay,
        the_credit_books_the_conserved_forms_current,
        the_loader_refuses_a_familys_third_key_by_name,
        two_records_laid_equal_are_identical_and_one_apart_diverge_at_one_link_per_interval,
        the_owners_shout_is_the_inventory_of_the_write_sites_outside_rule3,
        the_engines_derivation_ledger_names_a_function_per_act,
    ):
        started = time.perf_counter()
        print(f"{act.__name__}: {act()} ({time.perf_counter() - started:.2f} s)")
