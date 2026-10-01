"""Rule3 in one place (core/rule3.py; ALGEBRA.md #the-line, #the-direction, #the-interval): one function steps every record in either direction, the isotropic rule is the same call with equal paces, and no other file of src/ writes this arithmetic; and the generic Node is closed for building (HIGHLIGHTS.md): the NodeState is the records and the writes' remainders alone, one Rule3 division per part and one write per held part per interval, the readings write nothing, the output click and field only, ENGINE.md's table the code's."""

from __future__ import annotations

import ast
import dataclasses
import random
import re
import sys
from pathlib import Path

import numpy as np

import event_universe.world_files as world_files
from event_universe import growth, node, share
from event_universe.core import rule3 as core
from event_universe.core.rule3 import (
    ISOTROPIC,
    NO_READ,
    coefficients,
    form_term,
    rule3,
    rule_total_bound,
)
from event_universe.game_board import GameBoard
from event_universe.world_files import load_world
from tests.laws import chain_body_world, load_file

ROOT = Path(__file__).resolve().parents[1]
SOURCE, GAMMA = ROOT / "src" / "event_universe", 10_000
TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
BACK = load_file("back_in_time", ROOT / "tools" / "back_in_time.py")


def law_isotropic(num: int, den: int, gamma: int, c: int, weak_field: bool) -> tuple[int, int, int]:
    """The law's line at a Node with the axis contents zero, the oracle (ALGEBRA.md #the-line, #the-paces): p_0^2 = (Gamma - c)^2 + c^2, p_a = Gamma - 2 c, R = 2 num p_a^2, S = 12 den Gamma^2 - 12 (den - num) p_0^2 - 12 num p_a^2, w = 6 den Gamma^2; or the plain first-order rule."""
    if not weak_field:
        return (gamma - c) * num, 6 * den * c, 3 * den * gamma
    clock_squared, link_squared, gamma_squared = (gamma - c) ** 2 + c * c, (gamma - 2 * c) ** 2, gamma**2
    self_coefficient = (
        12 * den * gamma_squared - 12 * (den - num) * clock_squared - 12 * num * link_squared
    )
    return 2 * link_squared * num, self_coefficient, 6 * den * gamma_squared


def law_axes(
    num: int, den: int, gamma: int, content: int, axis_contents: tuple[int, int, int]
) -> tuple[tuple[int, int, int], int, int]:
    """The law's line with the four paces, the oracle: p_a = Gamma - 2 c - t_a on each axis, the clock's square as above."""
    pace = gamma - content
    paces, gamma_squared = [gamma - 2 * content - t for t in axis_contents], gamma * gamma
    reads = (2 * paces[0] ** 2 * num, 2 * paces[1] ** 2 * num, 2 * paces[2] ** 2 * num)
    squares = paces[0] ** 2 + paces[1] ** 2 + paces[2] ** 2
    clock_squared = pace * pace + content * content
    self_coefficient = 12 * den * gamma_squared - 12 * (den - num) * clock_squared - 4 * num * squares
    return reads, self_coefficient, 6 * den * gamma_squared


def test_the_coefficients_are_the_laws_line_and_the_isotropic_ones_at_zero_axis_contents():
    """With the axis contents zero the isotropic rule's (R, R, R), S, w term for term; with them the four paces' reads; `weak_field` False the plain rule; the vacuum 2 Gamma^2 times the plain rule."""
    rng = random.Random(3)
    for _ in range(500):
        num, den, gamma = rng.randint(1, 1000), rng.randint(1, 1000), rng.choice([1, 100, GAMMA])
        content = rng.randint(-gamma + 1, gamma - 1)
        axis_contents = (rng.randint(-50, 50), rng.randint(-50, 50), rng.randint(-50, 50))
        for weak_field in (True, False):
            read, self_coefficient, wall = law_isotropic(num, den, gamma, content, weak_field)
            expected = ((read, read, read), self_coefficient, wall)
            assert coefficients(num, den, gamma, content, weak_field=weak_field) == expected
        axes = law_axes(num, den, gamma, content, axis_contents)
        assert coefficients(num, den, gamma, content, axis_contents) == axes
        assert coefficients(num, den, gamma, content, (0, 0, 0)) == coefficients(
            num, den, gamma, content
        )
        # the vacuum c = 0: 2 Gamma^2 times the plain rule (the levels bit for bit)
        assert coefficients(num, den, gamma, 0) == ((2 * gamma**2 * num,) * 3, 0, 6 * den * gamma**2)
        # a tensor along x alone slows the x read and the own term by 4 num (p_x^2 - p_link^2), the Link's pace Gamma - 2 c
        pace, axis_pace = gamma - 2 * content, gamma - 2 * content - axis_contents[0]
        (read, *_), self_iso, wall = coefficients(num, den, gamma, content)
        reads = (2 * axis_pace**2 * num, read, read)
        along = self_iso - 4 * num * (axis_pace**2 - pace**2)
        assert coefficients(num, den, gamma, content, (axis_contents[0], 0, 0)) == (reads, along, wall)
    assert ISOTROPIC == (0, 0, 0)


def test_the_one_rule_steps_forward_and_back_exactly_on_integers_and_int64_arrays():
    """w a_next + r' = SUM_a R_a arr_a + S a_now - w a_before + r with 0 <= r' < w, the inverse exact; on int64 arrays the sum over the axes equals R times the six-sum bit for bit, the dtype kept."""
    rng = random.Random(5)
    for _ in range(500):
        num, den, gamma = rng.randint(1, 1000), rng.randint(1, 1000), rng.choice([1, GAMMA])
        content = rng.randint(-gamma + 1, gamma - 1)
        contents = (rng.randint(-30, 30), rng.randint(-30, 30), rng.randint(-30, 30))
        reads, self_coefficient, wall = coefficients(num, den, gamma, content, contents)
        arrivals = tuple(rng.randint(-(10**6), 10**6) for _ in range(3))
        now, before = rng.randint(-(10**6), 10**6), rng.randint(-(10**6), 10**6)
        remainder = rng.randint(0, wall - 1)
        total = sum(read * arrival for read, arrival in zip(reads, arrivals, strict=True))
        total += self_coefficient * now - wall * before + remainder
        nxt, carried = rule3(reads, arrivals, self_coefficient, wall, now, before, remainder)
        assert (nxt, carried) == (total // wall, total % wall) and 0 <= carried < wall
        stepped_back = (before, remainder)
        assert rule3(reads, arrivals, self_coefficient, wall, now, nxt, carried, -1) == stepped_back
    generator, shape = np.random.default_rng(9), (4, 3, 2)
    num, den = np.full(shape, 800, dtype=np.int64), np.full(shape, 809, dtype=np.int64)
    content = generator.integers(-3000, 3000, shape, dtype=np.int64)
    arrivals = tuple(generator.integers(-(10**6), 10**6, shape, dtype=np.int64) for _ in range(3))
    now = generator.integers(-(10**6), 10**6, shape, dtype=np.int64)
    before = generator.integers(-(10**6), 10**6, shape, dtype=np.int64)
    reads, self_coefficient, wall = coefficients(num, den, GAMMA, content)
    remainder = generator.integers(0, 10**9, shape, dtype=np.int64) % wall
    nxt, carried = rule3(reads, arrivals, self_coefficient, wall, now, before, remainder)
    six_sum = arrivals[0] + arrivals[1] + arrivals[2]
    total = reads[0] * six_sum + self_coefficient * now - wall * before + remainder
    assert nxt.dtype == np.int64 and np.array_equal(nxt, np.floor_divide(total, wall))
    assert np.array_equal(carried, total - wall * nxt)
    back, remainder_back = rule3(reads, arrivals, self_coefficient, wall, now, nxt, carried, -1)
    assert np.array_equal(back, before) and np.array_equal(remainder_back, remainder)


def test_the_forms_node_term_and_the_load_bound_read_the_same_integers():
    """The form's Node term w (now^2 + before^2) - S now before and the load bound 6 A R + A |S| + w (A + 1) are read from the one function's integers."""
    reads, self_coefficient, wall = coefficients(800, 809, GAMMA, 250)
    assert form_term(self_coefficient, wall, 7, -3) == wall * (49 + 9) + self_coefficient * 21
    amplitude = 1 << 20
    assert rule_total_bound(800, 809, GAMMA, 250, amplitude, True) == 6 * amplitude * abs(
        reads[0]
    ) + amplitude * abs(self_coefficient) + wall * (amplitude + 1)


# the rule's own lines in core/rule3.py: the Node's term, the far level's, the carry's and the form's; the second set is the old two-function form, refused anywhere in src/ as well
RULE_LINES = (r"self_coefficient \* now\b", r"wall \* other\b", r"direction \* total \+ carry")
RULE_LINES += (r"direction \* quotient", r"now \* now \+ before \* before")
RULE_ARITHMETIC = RULE_LINES + (r"self_coefficient \* before\b", r"wall \* before\b")
RULE_ARITHMETIC += (r"wall \* now \+ remainder", r"direction \* carry\b")


def test_no_other_file_of_src_writes_the_rules_arithmetic():
    """(d) of the model owner's target: the rule is written once, in core/rule3.py; every other file of src/ calls it."""
    offenders = []
    for path in sorted(SOURCE.rglob("*.py")):
        if path == SOURCE / "core" / "rule3.py":
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in RULE_ARITHMETIC:
            for match in re.finditer(pattern, text):
                line = text.count("\n", 0, match.start()) + 1
                offenders.append(f"{path.relative_to(ROOT)}:{line} {match.group(0)}")
    assert not offenders, offenders
    own = (SOURCE / "core" / "rule3.py").read_text(encoding="utf-8")
    assert all(re.search(pattern, own) for pattern in RULE_LINES)


# A Node's level goes to its six neighbours only through the Ports: the one shift of an array across a Link is core/ports.py's `shifted`, read through `arrival` under the board's face rule; every reading of a neighbour's level (Rule3's arrival sums, the currents at a Port, a body's shell and region) takes it from there.
SHIFT_HOME = {"src/event_universe/core/ports.py": {"shifted"}}
SHIFT_TOKENS = re.compile(r"np\.roll\(|\._shift\(|\.take\(")


def test_no_other_code_moves_a_level_from_one_node_to_another():
    """Every shift of an array across Nodes in src/ is core/ports.py's `shifted` (no np.roll, no take, no shift elsewhere: the Node reads its neighbours through the Ports, `arrival`), and no function of src/ is a split of its own."""
    found: dict[str, set[str]] = {}
    for path in sorted(SOURCE.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        if not SHIFT_TOKENS.search(text):
            continue
        tree = ast.parse(text)
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        spans = [(node.lineno, node.end_lineno or node.lineno, node.name) for node in functions]
        for match in SHIFT_TOKENS.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            inner = max((span for span in spans if span[0] <= line <= span[1]), key=lambda span: span[0])
            found.setdefault(path.relative_to(ROOT).as_posix(), set()).add(inner[2])
    for home, functions in SHIFT_HOME.items():
        assert found.pop(home) == functions
    assert found == {}, found
    # the Node, the GameBoard, core and the folders hold no split of their own
    stepping = [SOURCE / "node.py", SOURCE / "game_board.py", *sorted((SOURCE / "core").glob("*.py"))]
    stepping += sorted((SOURCE / "features").rglob("*.py"))
    for path in stepping:
        for item in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(item, ast.FunctionDef):
                assert "split" not in item.name.lower(), f"{path.name}: {item.name}"


# The integers the law writes and the engine may hold: 0 and 1 (the identity and the direction, -1 the inverse and the hole), 2 (the halves: W_c div 2, the half wall, the axis contents' rounding, two levels), 3 (the three axes, 3 den) and 6 (the six Ports, 6 den); in Rule3's own line (core/rule3.py) also 4 and 12 of S = 12 den Gamma^2 - 12 (den - num) p_0^2 - 4 num SUM p_a^2.
LAW_INTEGERS = frozenset({0, 1, 2, 3, 6})
RULE_LINE_INTEGERS = frozenset({4, 12})


def tools_on_the_arrays() -> list[Path]:
    """Every tool that touches the engine's arrays: a file of tools/ that imports the package (the generator, the runner, the back-in-time gate, the reading of the clicks), found by its imports and never listed."""
    found = []
    for path in sorted((ROOT / "tools").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        modules = [node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        modules += [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names]
        if any(module.split(".")[0] == "event_universe" for module in modules):
            found.append(path)
    return found


def test_no_integer_beyond_the_laws_own_enters_the_engine_or_the_tools():
    """No integer literal in src/event_universe or in any tool that touches the engine's arrays (the owner, 2026-09-30: every coordinate, gap, wavelength, width, amplitude, count and window comes from the world's files) beyond the law's own (LAW_INTEGERS; Rule3's line's 4 and 12 in core/rule3.py alone): every other number is a file's key or the rule's own act, so a number cannot enter the engine again."""
    tools = tools_on_the_arrays()
    names = {path.name for path in tools}
    assert {"pixel_mode.py", "back_in_time.py", "run_inputs.py", "click_counts.py"} <= names
    found = []
    for path in [*sorted(SOURCE.rglob("*.py")), *tools]:
        allowed = LAW_INTEGERS | (RULE_LINE_INTEGERS if path.name == "rule3.py" else frozenset())
        for item in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(item, ast.Constant) and type(item.value) in (int, float, complex):
                if item.value not in allowed or type(item.value) is not int:
                    found.append(f"{path.relative_to(ROOT)}:{item.lineno} {item.value!r}")
    assert not found, found


def test_no_root_is_imported_or_called_anywhere_in_src_or_tools():
    """The root leaves everywhere (the owner, 2026-09-30): no file of src/ or tools/ imports `isqrt` or `math`, or calls a name `isqrt` or `sqrt`; the loader and the generator read the fixed point of the division act, and the run reads no root."""
    found = []
    for path in sorted([*SOURCE.rglob("*.py"), *(ROOT / "tools").glob("*.py")]):
        for item in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(item, ast.Import) and any(alias.name == "math" for alias in item.names):
                found.append(f"{path.relative_to(ROOT)}:{item.lineno} import math")
            if isinstance(item, ast.ImportFrom) and any("sqrt" in alias.name for alias in item.names):
                found.append(f"{path.relative_to(ROOT)}:{item.lineno} from {item.module} import a root")
            if isinstance(item, ast.Call):
                callee = item.func
                name = callee.id if isinstance(callee, ast.Name) else getattr(callee, "attr", "")
                if "sqrt" in name:
                    found.append(f"{path.relative_to(ROOT)}:{item.lineno} {name}")
    assert not found, found


# The generic Node is closed for building (HIGHLIGHTS.md; the owner, 2026-10-01): per family, per part, two levels and Rule3's remainder; per held part, one write of its sources by one division with one remainder; nothing else at a Node, every other number a reading of the record.
NODE_STATE = {"levels": "Record | None", "second": "Record | None", "parts": "list[Record]"}
NODE_STATE["write_remainders"] = "list[np.ndarray]"
TABLE_ROW = re.compile(r"^\| `([a-z_]+)`")  # a row of ENGINE.md's NodeState table, its first column


def is_write(args: tuple) -> bool:  # type: ignore[type-arg]
    """Whether a call of Rule3 is one write: the division act on the level 1 with the remainder kept at every Node (features/write, `carried`), no read and no other level."""
    reads, _arrivals, _numerator, _wall, now, other, remainder = args[:7]
    division = reads is NO_READ and type(now) is int and now == 1 and other == 0
    return division and isinstance(remainder, np.ndarray)


def is_step(args: tuple) -> bool:  # type: ignore[type-arg]
    """Whether a call of Rule3 is one step of a record: the three reads with the level now and the other level as arrays (a reading's plain Link term reads with no other level)."""
    return args[0] is not NO_READ and isinstance(args[4], np.ndarray) and isinstance(args[5], np.ndarray)


def test_the_generic_node_is_closed_for_building(tmp_path, monkeypatch):
    """(a) The NodeState holds the records per part (now, before, Rule3's remainder) and one write remainder per held part and nothing else, and the growth's and the gate's arrays beside the records name only the writes' remainders; (b) on the chain with a rotating body (every kind of family: a family of quanta with its second pair, the holder of the sign, two rows with a gap, the massless row with its axis parts) one interval forward and one back make exactly one Rule3 division per part, the level each record started from that call's own, and exactly one write per held part, and every reading the engine exposes leaves every record bit for bit; (c) the output over the run is click and field lines only, every click naming a declared region and never a Node; (d) ENGINE.md's NodeState table lists exactly the fields of (a)."""
    assert {f.name: f.type for f in dataclasses.fields(node.NodeState)} == NODE_STATE
    assert [f.name for f in dataclasses.fields(node.Record)] == ["now", "before", "remainder"]
    assert set(growth.SCALARS) == set(BACK.SCALARS) == {"write_remainders"}
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    lines: list[dict[str, object]] = []
    board = GameBoard(load_world(chain_body_world(tmp_path, TOOL, senses=(1,))), lines.append)
    calls: list[tuple[tuple, tuple]] = []  # type: ignore[type-arg]
    original = core.rule3

    def counting(*args):  # type: ignore[no-untyped-def]
        found = original(*args)
        calls.append((args, found))
        return found

    engine = [m for m in list(sys.modules.values()) if getattr(m, "__name__", "").startswith("event_")]
    for module in [m for m in engine if m.__dict__.get("rule3") is original]:
        monkeypatch.setattr(module, "rule3", counting)
    for direction, act in ((1, board.step), (-1, board.step_inverse)):
        calls.clear()
        act()
        records = [record for state in board.states for record in node.records(state)]
        steps = [args for args, _found in calls if is_step(args)]
        assert len(steps) == len(records)
        begun = {id(getattr(record, "before" if direction == 1 else "now")) for record in records}
        assert begun == {id(args[4]) for args in steps}  # the level each record's one call started from
        assert sum(is_write(args) for args, _found in calls) == sum(len(s.parts) for s in board.states)
    kept = BACK.snapshot(board)
    calls.clear()
    for index, (family, state) in enumerate(zip(board.families, board.states, strict=True)):
        if state.levels is not None and state.second is not None:
            share.family_share(family, (state.levels, state.second), board.wrap, board.world.node_clock)
            node.currents_of(family, state, board.wrap)
            node.stresses_of(family, state, board.wrap)
            node.sense_sign(state, board.shape)
            node.wronskian(state.levels, state.second)
            node.form(state.levels, state.second)
            board.quanta(index)
    board.books()
    assert not any(is_write(args) for args, _found in calls)  # the readings write nothing
    assert BACK.first_difference(kept, BACK.snapshot(board)) is None  # and every array stands
    for _ in range(60):
        board.step()
    regions = {row.name for row in board.world.detectors} | {"face"}
    assert lines and {str(line["event"]) for line in lines} <= {"click", "field"}
    clicks = [line for line in lines if line["event"] == "click"]
    assert clicks and all(line["detector"] in regions and "node" not in line for line in clicks)
    engine_rows = (ROOT / "docs" / "ENGINE.md").read_text(encoding="utf-8").splitlines()
    table = [m.group(1) for line in engine_rows if (m := TABLE_ROW.match(line))]
    assert set(table) == set(NODE_STATE) and len(table) == len(NODE_STATE)
