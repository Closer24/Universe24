"""Rule3 in one place (core/rule3.py; ALGEBRA.md #the-line, #the-direction, #the-interval): one function steps every record in either direction, the isotropic rule is the same call with equal paces, and no other file of src/ writes this arithmetic; and the generic Node is closed for building (HIGHLIGHTS.md): the NodeState is the lines and the writes' remainders alone, one shape for every family, one Rule3 division per line and one write per held line per interval, the readings write nothing, the output click and field only, ENGINE.md's table the code's."""

import ast
import dataclasses
import json
import random
import re
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

import event_universe.world_files as world_files
from event_universe import node, share
from event_universe.core import rule3 as core
from event_universe.core.rule3 import ISOTROPIC, NO_READ, coefficients, form_term, rule3
from event_universe.game_board import GameBoard
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK, TOOL, chain_body_world

ROOT = Path(__file__).resolve().parents[1]
SOURCE, GAMMA = ROOT / "src" / "event_universe", 10_000


def law_line(num, den, gamma, content, axis_contents=(0, 0, 0), weak_field=True):  # type: ignore[no-untyped-def]
    """The law's line at a Node, the oracle (ALGEBRA.md #the-line, #the-paces): p_0^2 = (Gamma - c)^2 + c^2, p_a = Gamma - 2 c - t_a, R_a = 2 num p_a^2, S = 12 den Gamma^2 - 12 (den - num) p_0^2 - 4 num SUM p_a^2, w = 6 den Gamma^2; or the plain first-order rule."""
    if not weak_field:
        return ((gamma - content) * num,) * 3, 6 * den * content, 3 * den * gamma
    paces = [gamma - 2 * content - t for t in axis_contents]
    clock_squared, squares = (gamma - content) ** 2 + content**2, sum(p**2 for p in paces)
    self_coefficient = 12 * den * gamma**2 - 12 * (den - num) * clock_squared - 4 * num * squares
    return tuple(2 * p**2 * num for p in paces), self_coefficient, 6 * den * gamma**2


def test_the_coefficients_are_the_laws_line_and_the_isotropic_ones_at_zero_axis_contents():
    """With the axis contents zero the isotropic rule's (R, R, R), S, w term for term; with them the four paces' reads; `weak_field` False the plain rule; the vacuum 2 Gamma^2 times the plain rule; the band's rotation at k = 0 carries the clock's square and light's band on a chain the Link's pace squared, exact in rationals."""
    rng = random.Random(3)
    for _ in range(500):
        num, den, gamma = rng.randint(1, 1000), rng.randint(1, 1000), rng.choice([1, 100, GAMMA])
        content = rng.randint(-gamma + 1, gamma - 1)
        axis_contents = (rng.randint(-50, 50), rng.randint(-50, 50), rng.randint(-50, 50))
        for weak_field in (True, False):
            expected = law_line(num, den, gamma, content, weak_field=weak_field)
            assert coefficients(num, den, gamma, content, weak_field=weak_field) == expected
        assert coefficients(num, den, gamma, content, axis_contents) == law_line(
            num, den, gamma, content, axis_contents
        )
        assert coefficients(num, den, gamma, content, ISOTROPIC) == coefficients(
            num, den, gamma, content
        )
        # the vacuum c = 0: 2 Gamma^2 times the plain rule (the levels bit for bit)
        assert coefficients(num, den, gamma, 0) == ((2 * gamma**2 * num,) * 3, 0, 6 * den * gamma**2)
        # a tensor along x alone slows the x read and the own term by 4 num (p_x^2 - p_link^2), the Link's pace Gamma - 2 c
        pace, axis_pace = gamma - 2 * content, gamma - 2 * content - axis_contents[0]
        (read, *_), self_iso, wall = coefficients(num, den, gamma, content)
        along = (2 * axis_pace**2 * num, read, read), self_iso - 4 * num * (axis_pace**2 - pace**2), wall
        assert coefficients(num, den, gamma, content, (axis_contents[0], 0, 0)) == along
    assert ISOTROPIC == (0, 0, 0)
    # the band at k = 0, 2 cos omega = (6 R + S) / w = 2 - 2 f (1 - num / den) with f = p_0^2 / Gamma^2 the clock's square (the Link's pace cancels at k = 0); light on a chain, cos omega = 1 - f_a (1 - cos k) / 3 with f_a = (Gamma - 2 c)^2 / Gamma^2, the level entering the Link twice, at cos k = 1, 0 and -1 (ALGEBRA.md #the-paces)
    for num, den, c in ((800, 809, 500), (3200, 3227, 2000), (1, 1, 0), (1, 1, 2000)):
        (read, _, _), self_coefficient, wall = coefficients(num, den, GAMMA, c)
        clock = Fraction((GAMMA - c) ** 2 + c * c, GAMMA**2)
        link = Fraction((GAMMA - 2 * c) ** 2, GAMMA**2)
        assert Fraction(6 * read + self_coefficient, wall) == 2 - 2 * clock * (1 - Fraction(num, den))
        for cosine in (1, 0, -1):
            band = Fraction(read * (2 * cosine + 4) + self_coefficient, 2 * wall)
            assert num != den or band == 1 - link * (1 - cosine) / 3


def test_the_one_rule_steps_forward_and_back_exactly_on_integers_and_int64_arrays():
    """w a_next + r' = SUM_a R_a arr_a + S a_now - w a_before + r with 0 <= r' < w, the inverse exact; on int64 arrays the sum over the axes equals R times the six-sum bit for bit, the dtype kept. The form's Node term w (now^2 + before^2) - S now before and the load bound 6 A R + A |S| + w (A + 1) are read from the one function's integers."""
    rng = random.Random(5)
    for _ in range(500):
        num, den, gamma = rng.randint(1, 1000), rng.randint(1, 1000), rng.choice([1, GAMMA])
        content = rng.randint(-gamma + 1, gamma - 1)
        contents = (rng.randint(-30, 30), rng.randint(-30, 30), rng.randint(-30, 30))
        reads, self_coefficient, wall = coefficients(num, den, gamma, content, contents)
        *arrivals, now, before = (rng.randint(-(10**6), 10**6) for _ in range(5))
        remainder = rng.randint(0, wall - 1)
        total = sum(read * arrival for read, arrival in zip(reads, arrivals, strict=True))
        total += self_coefficient * now - wall * before + remainder
        nxt, carried = rule3(reads, arrivals, self_coefficient, wall, now, before, remainder)
        assert (nxt, carried) == (total // wall, total % wall) and 0 <= carried < wall
        back = rule3(reads, arrivals, self_coefficient, wall, now, nxt, carried, -1)
        assert back == (before, remainder)
    generator, shape = np.random.default_rng(9), (4, 3, 2)
    num, den = np.full(shape, 800, dtype=np.int64), np.full(shape, 809, dtype=np.int64)
    content = generator.integers(-3000, 3000, shape, dtype=np.int64)
    arrivals = tuple(generator.integers(-(10**6), 10**6, shape, dtype=np.int64) for _ in range(3))
    now, before = (generator.integers(-(10**6), 10**6, shape, dtype=np.int64) for _ in range(2))
    reads, self_coefficient, wall = coefficients(num, den, GAMMA, content)
    remainder = generator.integers(0, 10**9, shape, dtype=np.int64) % wall
    nxt, carried = rule3(reads, arrivals, self_coefficient, wall, now, before, remainder)
    total = reads[0] * sum(arrivals) + self_coefficient * now - wall * before + remainder
    assert nxt.dtype == np.int64 and np.array_equal(nxt, np.floor_divide(total, wall))
    assert np.array_equal(carried, total - wall * nxt)
    back, remainder_back = rule3(reads, arrivals, self_coefficient, wall, now, nxt, carried, -1)
    assert np.array_equal(back, before) and np.array_equal(remainder_back, remainder)
    reads, self_coefficient, wall = coefficients(800, 809, GAMMA, 250)
    assert form_term(self_coefficient, wall, 7, -3) == wall * (49 + 9) + self_coefficient * 21
    bound = 6 * (1 << 20) * abs(reads[0]) + (1 << 20) * abs(self_coefficient) + wall * ((1 << 20) + 1)
    assert core.rule_total_bound(800, 809, GAMMA, 250, 1 << 20, True) == bound


# the rule's own lines in core/rule3.py: the Node's term, the far level's, the carry's and the form's; the second set is the old two-function form, refused anywhere in src/ as well
RULE_LINES = (r"self_coefficient \* now\b", r"wall \* other\b", r"direction \* total \+ carry")
RULE_LINES += (r"direction \* quotient", r"now \* now \+ before \* before")
RULE_ARITHMETIC = RULE_LINES + (r"self_coefficient \* before\b", r"wall \* before\b")
RULE_ARITHMETIC += (r"wall \* now \+ remainder", r"direction \* carry\b")


def test_no_other_file_of_src_writes_the_rules_arithmetic():
    """(d) of the model owner's target: the rule is written once, in core/rule3.py; every other file of src/ calls it. Every shift of an array across Nodes in src/ is core/ports.py's `shifted` (no np.roll, no take, no shift elsewhere: the Node reads its neighbours through the Ports, `arrival`), and no function of src/ is a split of its own."""
    offenders = []
    for path in sorted(SOURCE.rglob("*.py")):
        if path == SOURCE / "core" / "rule3.py":
            continue
        text = path.read_text(encoding="utf-8")
        for match in (m for pattern in RULE_ARITHMETIC for m in re.finditer(pattern, text)):
            offenders.append(
                f"{path.relative_to(ROOT)}:{text.count('\n', 0, match.start()) + 1} {match.group(0)}"
            )
    assert not offenders, offenders
    own = (SOURCE / "core" / "rule3.py").read_text(encoding="utf-8")
    assert all(re.search(pattern, own) for pattern in RULE_LINES)

    # A Node's level goes to its six neighbours only through the Ports: the one shift of an array across a Link is core/ports.py's `shifted`, read through `arrival` under the board's face rule; every reading of a neighbour's level (Rule3's arrival sums, the currents at a Port, a body's shell and region) takes it from there.
    SHIFT_HOME = {"src/event_universe/core/ports.py": {"shifted"}}
    SHIFT_TOKENS = re.compile(r"np\.roll\(|\._shift\(|\.take\(")
    found: dict[str, set[str]] = {}
    for path in sorted(SOURCE.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        if not SHIFT_TOKENS.search(text):
            continue
        functions = [n for n in ast.walk(ast.parse(text)) if isinstance(n, ast.FunctionDef)]
        spans = [(n.lineno, n.end_lineno or n.lineno, n.name) for n in functions]
        for match in SHIFT_TOKENS.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            inner = max((span for span in spans if span[0] <= line <= span[1]), key=lambda span: span[0])
            found.setdefault(path.relative_to(ROOT).as_posix(), set()).add(inner[2])
    for home, functions in SHIFT_HOME.items():
        assert found.pop(home) == functions
    assert found == {}, found
    # the Node, the GameBoard, core and the folders hold no split of their own
    stepping = [SOURCE / "node.py", SOURCE / "game_board.py", *SOURCE.glob("core/*.py")]
    for path in stepping + list(SOURCE.glob("features/*/*.py")):
        for item in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            assert not (isinstance(item, ast.FunctionDef) and "split" in item.name.lower()), path.name


# The integers the law writes and the engine may hold: 0 and 1 (the identity and the direction, -1 the inverse and the hole), 2 (the halves: W_c div 2, the half wall, the axis contents' rounding, two levels), 3 (the three axes, 3 den) and 6 (the six Ports, 6 den); in Rule3's own line (core/rule3.py) also 4 and 12 of S = 12 den Gamma^2 - 12 (den - num) p_0^2 - 4 num SUM p_a^2.
LAW_INTEGERS, RULE_LINE_INTEGERS = frozenset({0, 1, 2, 3, 6}), frozenset({4, 12})


def tools_on_the_arrays() -> list[Path]:
    """Every tool that touches the engine's arrays: a file of tools/ that imports the package (the generator, the runner, the back-in-time gate, the reading of the clicks, the bodies' drift), found by its import lines and never listed."""
    files = sorted((ROOT / "tools").glob("*.py"))
    return [
        p
        for p in files
        if re.search(r"^(from|import) event_universe\b", p.read_text(encoding="utf-8"), re.M)
    ]


def test_no_integer_beyond_the_laws_own_enters_the_engine_or_the_tools():
    """No integer literal in src/event_universe or in any tool that touches the engine's arrays (the owner, 2026-09-30: every coordinate, gap, wavelength, width, amplitude, count and window comes from the world's files) beyond the law's own (LAW_INTEGERS; Rule3's line's 4 and 12 in core/rule3.py alone): every other number is a file's key or the rule's own act, so a number cannot enter the engine again. The root leaves everywhere (the owner, 2026-09-30): no file of src/ or tools/ imports `isqrt` or `math`, or calls a name `isqrt` or `sqrt`; the loader and the generator read the fixed point of the division act, and the run reads no root. The names gate (HIGHLIGHTS.md **The engine works only with families of dimension one**; the owner, 2026-10-01, 03:25): no string literal stands in src/event_universe outside docstrings, the messages of `raise` and `assert` and f-strings, but in the loader (the files' key tables), in reports.py (the output's words), in world_files.py (the host's files) and in the package's version; so no act or reading of the engine names a family, a key or a kind, and a family name cannot enter the engine again."""
    tools = tools_on_the_arrays()
    assert {"pixel_mode.py", "back_in_time.py", "run_inputs.py", "click_counts.py"} <= {
        p.name for p in tools
    }
    found = []
    for path in [*sorted(SOURCE.rglob("*.py")), *tools]:
        allowed = LAW_INTEGERS | (RULE_LINE_INTEGERS if path.name == "rule3.py" else frozenset())
        for item in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(item, ast.Constant) and type(item.value) in (int, float, complex):
                if item.value not in allowed or type(item.value) is not int:
                    found.append(f"{path.relative_to(ROOT)}:{item.lineno} {item.value!r}")
    assert not found, found
    found = []
    for path in sorted([*SOURCE.rglob("*.py"), *(ROOT / "tools").glob("*.py")]):
        for item in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            imported = (
                [a.name for a in item.names] if isinstance(item, ast.Import | ast.ImportFrom) else []
            )
            callee = item.func if isinstance(item, ast.Call) else None
            called = callee.id if isinstance(callee, ast.Name) else getattr(callee, "attr", "")
            if "math" in imported or any("sqrt" in name for name in imported) or "sqrt" in called:
                found.append(f"{path.relative_to(ROOT)}:{item.lineno} {imported or called}")
    assert not found, found
    found = []
    for path in sorted(SOURCE.rglob("*.py")):
        name = path.relative_to(SOURCE).as_posix()
        if name.startswith("loader/") or name in ("reports.py", "world_files.py", "__init__.py"):
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        spoken = {id(item.value) for item in ast.walk(tree) if isinstance(item, ast.Expr)}
        for item in ast.walk(tree):
            if isinstance(item, ast.Raise | ast.Assert | ast.JoinedStr):
                spoken |= {id(part) for part in ast.walk(item)}
        for item in ast.walk(tree):
            if isinstance(item, ast.Constant) and isinstance(item.value, str) and id(item) not in spoken:
                found.append(f"{path.relative_to(ROOT)}:{item.lineno} {item.value!r}")
    assert not found, found


# The generic Node is closed for building (HIGHLIGHTS.md; the owner, 2026-10-01): per family, per line, two levels and Rule3's remainder; per held line, one write of its sources by one division with one remainder; nothing else at a Node, every other number a reading of the record; one shape of state for every family.
NODE_STATE = {"lines": "list[Record]", "write_remainders": "list[np.ndarray]"}
TABLE_ROW = re.compile(r"^\| `([a-z_]+)`")  # a row of ENGINE.md's NodeState table, its first column


def call_kind(args: tuple) -> str | None:  # type: ignore[type-arg]
    """What a call of Rule3 is: "write", the division act on the level 1 with the remainder kept at every Node (features/write, `carried`), no read and no other level; "step", the three reads with the level now and the other level as arrays (a reading's plain Link term reads with no other level); None otherwise."""
    reads, _arrivals, _numerator, _wall, now, other, remainder = args[:7]
    if (
        reads is NO_READ
        and type(now) is int
        and now == 1
        and other == 0
        and isinstance(remainder, np.ndarray)
    ):
        return "write"
    return (
        "step"
        if reads is not NO_READ and isinstance(now, np.ndarray) and isinstance(other, np.ndarray)
        else None
    )


def test_the_generic_node_is_closed_for_building(tmp_path, monkeypatch):
    """(a) The NodeState holds lines (now, before, Rule3's remainder), as many as the loader derives for the family (a family of quanta's dimension, a held row's sources' count), and one write remainder per held line and nothing else, one shape for every family; (b) on the chain with a rotating body (every kind of family: a plane of two lines, a family of one line, the holder of the sign, two rows with a gap, the massless row with its axis lines) one interval forward and one back make exactly one Rule3 division per line, the level each line started from that call's own, and exactly one write per held line, and every reading the engine exposes leaves every line bit for bit; (c) the output over the run is click and field lines only, every click naming a declared region and never a Node; (d) ENGINE.md's NodeState table lists exactly the fields of (a). The width is the run's declaration (the owner, 2026-10-01, 02:35): the loader's one site maps `integers.width` to the arrays' kind, the hardware's 64-bit integers at or under the host's signed bits and Python's integers above them (`loader.world.kind_of`); the chain world run at the width 63 and at 127 over forty intervals gives the same click and field lines and the same books bit for bit, every array of the wider run an array of Python integers; no other file of src names an integer's kind."""
    assert {f.name: f.type for f in dataclasses.fields(node.NodeState)} == NODE_STATE
    assert [f.name for f in dataclasses.fields(node.Record)] == ["now", "before", "remainder"]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = GameBoard(load_world(chain_body_world(tmp_path, TOOL, senses=(1,))), (lines := []).append)
    for family, state in zip(board.families, board.states, strict=True):
        assert len(state.lines) == family.lines
        assert len(state.write_remainders) == family.lines * family.held
    assert sorted(len(s.lines) for s in board.states) == [1, 1, 1, 2, 4]
    calls: list[tuple[tuple, tuple]] = []  # type: ignore[type-arg]
    original = core.rule3

    def counting(*args):  # type: ignore[no-untyped-def]
        calls.append((args, found := original(*args)))
        return found

    engine = [m for m in list(sys.modules.values()) if getattr(m, "__name__", "").startswith("event_")]
    for module in [m for m in engine if m.__dict__.get("rule3") is original]:
        monkeypatch.setattr(module, "rule3", counting)
    for direction, act in ((1, board.step), (-1, board.step_inverse)):
        calls.clear()
        act()
        records = [record for state in board.states for record in state.lines]
        steps = [args for args, _found in calls if call_kind(args) == "step"]
        begun = {id(getattr(record, "before" if direction == 1 else "now")) for record in records}
        assert len(steps) == len(records) and begun == {
            id(args[4]) for args in steps
        }  # each line's one call
        assert sum(call_kind(args) == "write" for args, _found in calls) == sum(
            len(s.write_remainders) for s in board.states
        )
    kept = BACK.snapshot(board)
    calls.clear()
    for index, (family, state) in enumerate(zip(board.families, board.states, strict=True)):
        if family.quanta:
            share.family_share(family, state.lines, board.wrap, board.world.node_clock)
            node.currents_of(family.pair[0], state.lines, board.wrap)
            node.stresses_of(family.pair[0], state.lines, board.wrap)
            node.wronskian(state.lines, family.plane)
            node.form(state.lines, state.lines)
            board.quanta(index)
    board.books()
    assert not any(call_kind(args) == "write" for args, _found in calls)  # the readings write nothing
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
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL)
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    universe["integers"]["width"] = 127
    document = {**json.loads(world.read_text(encoding="utf-8")), "universe": "wide.json"}
    mode = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))
    mode["world_digest"] = input_digest(document)
    for name, text in (("wide", universe), ("chain_wide", document), ("chain_wide.mode", mode)):
        (tmp_path / f"{name}.json").write_text(json.dumps(text), encoding="utf-8")
    runs = []
    for path, kind in ((world, np.int64), (tmp_path / "chain_wide.json", object)):
        board = GameBoard(load_world(path), (lines := []).append)
        for _ in range(40):
            board.step()
        arrays = [a for s in board.states for r in s.lines for a in (r.now, r.remainder)]
        assert board.world.kind is kind and all(a.dtype == np.dtype(kind) for a in arrays)
        runs.append((lines, board.books()))
    assert runs[0] == runs[1] and runs[0][0]
    named = [
        f"{path.relative_to(ROOT)}: {m.group(0)}"
        for path in sorted(SOURCE.rglob("*.py"))
        for m in INTEGER_KINDS.finditer(path.read_text(encoding="utf-8"))
    ]
    assert named == ["src/event_universe/loader/world.py: np.int64"], named


INTEGER_KINDS = re.compile(r"np\.u?int(?:8|16|32|64|p)?\b|np\.iinfo|\"int64\"|dtype=np\.")
