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

    import numpy as np

    from event_universe import flux, records, world_files
    from event_universe.core import paces
    from event_universe.core.ports import Wrap
    from event_universe.core.rule3 import rule_integers
    from event_universe.features.click import Face
    from event_universe.lattice import Lattice
    from event_universe.loader.universe import FAMILY_KEYS, universe_of
    from event_universe.world_files import load_world
    from tests.laws import BACK, EVENTS, PACKET, ROOT, TOOL, UNIVERSE, refused, slit_world

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

    # the row 26 act (the gate runs across the click and the write is the whole re-lay) ran the Zeno n = 4 world over 168 intervals with its twin and three run backs, 125 s on the suite's clock, and left on 2026-10-24; its sentence stands in tests/test_the_chain_world.py (B4, the inverse through the absorption and the emission MATCH) and in the records' gate tables (examples/events/bell/blind_and_reading.md, back_in_time MATCH)

    # the row 40 engine clause (the credit books the conserved form's own current through the front Ports) is deleted at the landing (2026-10-23): its breaker world, a wrapped chain of 8 with two regions and a draw and no lay, is one the loader refuses under the derived window (no lay with an end passes a declared region), and without a draw the regions book nothing; the claim stands in the clicks table and in tests/test_the_node_detector.py's booking of the front's current
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
        by_name = {
            8,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            21,
            22,
            27,
        }  # the lines no run here exercises: they stand by name alone (12 since the landing of 2026-10-23, its caller the row 40 world the loader refuses under the derived window; 13 to 16, 19 and 27 since 2026-10-24, their caller the row 26 act's Zeno world, whose run left the suite under its bound)
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
        the_loader_refuses_a_familys_third_key_by_name,
        two_records_laid_equal_are_identical_and_one_apart_diverge_at_one_link_per_interval,
        the_owners_shout_is_the_inventory_of_the_write_sites_outside_rule3,
        the_engines_derivation_ledger_names_a_function_per_act,
    ):
        started = time.perf_counter()
        print(f"{act.__name__}: {act()} ({time.perf_counter() - started:.2f} s)")
