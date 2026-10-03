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
from event_universe.core import paces
from event_universe.core import rule3 as core
from event_universe.core.rule3 import NO_READ, coefficients, form_term, link_factor, rule3
from event_universe.game_board import GameBoard
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK, TOOL, chain_body_world

ROOT = Path(__file__).resolve().parents[1]
SOURCE, GAMMA = ROOT / "src" / "event_universe", 10_000


def law_line(num, den, gamma, clock, pace, factors=None, unit=1):
    square = unit * unit
    reads = tuple(2 * num * pace**2 * q for q in (factors or [square] * 6))
    self_coefficient = 12 * (den * gamma**2 - (den - num) * clock**2) * square - sum(reads)
    return reads, self_coefficient, 6 * den * gamma**2 * square


def test_the_coefficients_are_the_laws_line_and_the_isotropic_ones_at_zero_axis_contents():
    """With no Links' factors the uniform level's six reads (R,) x 6, S, w term for term at the composed paces of a content (the clock and the Node's pace the module's two functions, core/paces.py), at the Link unit G the integers G^2 times the unit's; with the six Links' factors the six Ports' reads, each the Node's pace squared times its Link's factor, the same factor read from either end; the vacuum's paces 2 Gamma^2 times the plain rule; the Link's factor Q = (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2, G^2 at no tension, 0 at the tension Gamma, 264 at G = 16 and the tension -153 at Gamma 10,000 (a hill above G^2), resolved to Gamma / (2 G^2); the band's rotation at k = 0 carries the clock's square and light's band on a chain the Node's pace squared, the level entering the Link twice, exact in rationals. The vacuum's paces give 2 Gamma^2 times the plain rule, the levels bit for bit; a factor on the +x Link alone changes that Port's read and the own term by 2 num p^2 (Q - 1); the band at k = 0 is 2 cos omega = (6 R + S) / w = 2 - 2 f (1 - num / den) with f = p_0^2 / Gamma^2 the clock's square (the Link's pace cancels at k = 0), and light on a chain cos omega = 1 - f_a (1 - cos k) / 3 with f_a = p_i^2 / Gamma^2, p_i = p_0^2 / Gamma to the unit, at cos k = 1, 0 and -1 (ALGEBRA.md #the-paces)."""
    rng = random.Random(3)
    for _ in range(500):
        num, den, gamma = rng.randint(1, 1000), rng.randint(1, 1000), rng.choice([1, 100, GAMMA])
        content, unit = rng.randint(-gamma + 1, gamma - 1), rng.choice([1, 2, 16])
        factors = tuple(unit * unit + rng.randint(-50, 50) for _ in range(6))
        clock, p = paces.node_paces(gamma, content)
        assert coefficients(num, den, gamma, clock, p) == law_line(num, den, gamma, clock, p)
        found = coefficients(num, den, gamma, clock, p, factors, unit)
        assert found == law_line(num, den, gamma, clock, p, factors, unit)
        plain = coefficients(num, den, gamma, clock, p, None, unit)
        assert coefficients(num, den, gamma, clock, p, (unit * unit,) * 6, unit) == plain
        (read, *_), self_iso, wall = coefficients(num, den, gamma, clock, p)
        assert plain == ((read * unit * unit,) * 6, self_iso * unit * unit, wall * unit * unit)
        vacuum = ((2 * gamma**2 * num,) * 6, 0, 6 * den * gamma**2)
        assert coefficients(num, den, gamma, gamma, gamma) == vacuum
        q = factors[0]
        along = (2 * q * p**2 * num,) + (read,) * 5, self_iso - 2 * num * p**2 * (q - 1), wall
        assert coefficients(num, den, gamma, clock, p, (q,) + (1,) * 5) == along
    assert (link_factor(GAMMA, 16, 0), link_factor(GAMMA, 16, GAMMA)) == (256, 0)
    assert link_factor(GAMMA, 16, -153) == 264 and link_factor(GAMMA, 16, GAMMA // 512) == 255
    for num, den, c in ((800, 809, 500), (3200, 3227, 2000), (1, 1, 0), (1, 1, 2000)):
        p_0, p_i = paces.clock(GAMMA, c), paces.link_pace(GAMMA, c)
        (read, *_), self_coefficient, wall = coefficients(num, den, GAMMA, p_0, p_i)
        clock, link = Fraction(p_0 * p_0, GAMMA**2), Fraction(p_i * p_i, GAMMA**2)
        assert Fraction(6 * read + self_coefficient, wall) == 2 - 2 * clock * (1 - Fraction(num, den))
        for cosine in (1, 0, -1):
            band = Fraction(read * (2 * cosine + 4) + self_coefficient, 2 * wall)
            assert num != den or band == 1 - link * (1 - cosine) / 3


def test_the_one_rule_steps_forward_and_back_exactly_on_integers_and_int64_arrays():
    """w a_next + r' = SUM over the six Ports of R_ij arr_j + S a_now - w a_before + r with 0 <= r' < w, the inverse exact; on int64 arrays at a uniform level the sum over the Ports equals R times the six-sum bit for bit, the dtype kept. The form's Node term w (now^2 + before^2) - S now before and the load bound 6 A R + A |S| + w (A + 1) are read from the one function's integers."""
    rng = random.Random(5)
    for _ in range(500):
        num, den, gamma = rng.randint(1, 1000), rng.randint(1, 1000), rng.choice([1, GAMMA])
        content = rng.randint(-gamma + 1, gamma - 1)
        factors = tuple(16 * 16 - rng.randint(0, 30) for _ in range(6))
        clock, pace = paces.node_paces(gamma, content)
        reads, self_coefficient, wall = coefficients(num, den, gamma, clock, pace, factors, 16)
        *arrivals, now, before = (rng.randint(-(10**6), 10**6) for _ in range(8))
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
    arrivals = tuple(generator.integers(-(10**6), 10**6, shape, dtype=np.int64) for _ in range(6))
    now, before = (generator.integers(-(10**6), 10**6, shape, dtype=np.int64) for _ in range(2))
    reads, self_coefficient, wall = coefficients(num, den, GAMMA, *paces.node_paces(GAMMA, content))
    remainder = generator.integers(0, 10**9, shape, dtype=np.int64) % wall
    nxt, carried = rule3(reads, arrivals, self_coefficient, wall, now, before, remainder)
    total = reads[0] * sum(arrivals) + self_coefficient * now - wall * before + remainder
    assert nxt.dtype == np.int64 and np.array_equal(nxt, np.floor_divide(total, wall))
    assert np.array_equal(carried, total - wall * nxt)
    back = rule3(reads, arrivals, self_coefficient, wall, now, nxt, carried, -1)
    assert np.array_equal(back, (before, remainder))
    reads, self_coefficient, wall = coefficients(800, 809, GAMMA, *(own := paces.node_paces(GAMMA, 250)))
    assert form_term(self_coefficient, wall, 7, -3) == wall * (49 + 9) + self_coefficient * 21
    bound = 6 * (1 << 20) * abs(reads[0]) + (1 << 20) * abs(self_coefficient) + wall * ((1 << 20) + 1)
    assert core.rule_total_bound(800, 809, GAMMA, *own, 1 << 20) == bound


RULE_LINES = (r"self_coefficient \* now\b", r"wall \* other\b", r"direction \* total \+ carry")
RULE_LINES += (r"direction \* quotient", r"now \* now \+ before \* before")
RULE_ARITHMETIC = RULE_LINES + (r"self_coefficient \* before\b", r"wall \* before\b")
RULE_ARITHMETIC += (r"wall \* now \+ remainder", r"direction \* carry\b")


def test_no_other_file_of_src_writes_the_rules_arithmetic():
    """(d) of the model owner's target: the rule is written once, in core/rule3.py; every other file of src/ calls it (RULE_LINES, the rule's own lines: the Node's term, the far level's, the carry's and the form's; RULE_ARITHMETIC adds the old two-function form, refused anywhere in src/ as well). Every shift of an array across Nodes in src/ is core/ports.py's `shifted` (no np.roll, no take, no shift elsewhere: a Node's level goes to its six neighbours only through the Ports, read through `arrival` under the board's face rule, and every reading of a neighbour's level, Rule3's arrival sums, the currents at a Port, a body's shell and region, takes it from there), and no function of src/ is a split of its own. The Node, the GameBoard, core and the folders hold no split of their own."""
    offenders = []
    for path in sorted(p for p in SOURCE.rglob("*.py") if p.name != "rule3.py"):
        text = path.read_text(encoding="utf-8")
        for match in (m for pattern in RULE_ARITHMETIC for m in re.finditer(pattern, text)):
            line = text.count("\n", 0, match.start()) + 1
            offenders.append(f"{path.relative_to(ROOT)}:{line} {match.group(0)}")
    assert not offenders, offenders
    assert all(re.search(p, (SOURCE / "core" / "rule3.py").read_text()) for p in RULE_LINES)
    SHIFT_HOME = {"src/event_universe/core/ports.py": {"shifted"}}
    SHIFT_TOKENS, found = re.compile(r"np\.roll\(|\._shift\(|\.take\("), {}
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
    assert {home: found.pop(home) for home in SHIFT_HOME} == SHIFT_HOME and found == {}, found
    stepping = [SOURCE / "node.py", SOURCE / "game_board.py", *SOURCE.glob("core/*.py")]
    for path in stepping + list(SOURCE.glob("features/*/*.py")):
        for item in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            assert not (isinstance(item, ast.FunctionDef) and "split" in item.name.lower()), path.name


LAW_INTEGERS, RULE_LINE_INTEGERS = frozenset({0, 1, 2, 3, 6}), frozenset({4, 12})


def test_no_integer_beyond_the_laws_own_enters_the_engine_or_the_tools():
    """No integer literal in src/event_universe or in any tool that touches the engine's arrays (the owner, 2026-09-30: every coordinate, gap, wavelength, width, amplitude, count and window comes from the world's files) beyond the law's own (LAW_INTEGERS: 0 and 1, the identity and the direction, -1 the inverse and the hole; 2, the halves, W_c div 2, the half wall, the axis contents' rounding, two levels; 3, the three axes, 3 den; 6, the six Ports, 6 den; and in Rule3's own line, core/rule3.py alone, 4 and 12 of S = 12 den Gamma^2 - 12 (den - num) p_0^2 - 4 num SUM p_a^2, RULE_LINE_INTEGERS): every other number is a file's key or the rule's own act, so a number cannot enter the engine again. The root leaves everywhere (the owner, 2026-09-30): no file of src/ or tools/ imports `isqrt` or `math`, or calls a name `isqrt` or `sqrt`; the loader and the generator read the fixed point of the division act, and the run reads no root. The names gate (HIGHLIGHTS.md **The engine works only with families of dimension one**; the owner, 2026-10-01, 03:25): no string literal stands in src/event_universe outside docstrings, the messages of `raise` and `assert` and f-strings, but in the loader (the files' key tables), in reports.py (the output's words), in world_files.py (the host's files) and in the package's version; so no act or reading of the engine names a family, a key or a kind, and a family name cannot enter the engine again."""
    texts = {p: p.read_text(encoding="utf-8") for p in sorted((ROOT / "tools").glob("*.py"))}
    tools = [p for p, text in texts.items() if re.search(r"^(from|import) event_universe\b", text, re.M)]
    assert {"pixel_mode", "back_in_time", "run_inputs", "click_counts"} <= {p.stem for p in tools}
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
            importing = isinstance(item, ast.Import | ast.ImportFrom)
            imported = [a.name for a in item.names] if importing else []
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


NODE_STATE = {"lines": "list[Record]", "write_remainders": "list[np.ndarray]"}
TABLE_ROW = re.compile(r"^\| `([a-z_]+)`")  # a row of ENGINE.md's NodeState table, its first column


def test_the_generic_node_is_closed_for_building(tmp_path, monkeypatch):
    """The generic Node is closed for building (HIGHLIGHTS.md; the owner, 2026-10-01): per family, per line, two levels and Rule3's remainder; per held line, one write of its sources by one division with one remainder; nothing else at a Node, every other number a reading of the record; one shape of state for every family. (a) The NodeState holds lines (now, before, Rule3's remainder), as many as the loader derives for the family (a family of quanta's dimension, a held row's sources' count), and one write remainder per held line and nothing else, one shape for every family; (b) on the chain with a rotating body (every kind of family: a plane of two lines, a family of one line, the holder of the sign, two rows with a gap, the massless row with its axis lines) one interval forward and one back make exactly one Rule3 division per line, the level each line started from that call's own, and exactly one write per held line, and every reading the engine exposes leaves every line bit for bit; (c) the output over the run is click and field lines only, every click naming a declared region and never a Node; (d) ENGINE.md's NodeState table lists exactly the fields of (a). The width is the run's declaration (the owner, 2026-10-01, 02:35): the loader's one site maps `integers.width` to the arrays' kind, the hardware's 64-bit integers at or under the host's signed bits and Python's integers above them (`loader.world.kind_of`); the chain world run at the width 63 and at 127 over forty intervals gives the same click and field lines and the same books bit for bit, every array of the wider run an array of Python integers; no other file of src names an integer's kind."""
    assert {f.name: f.type for f in dataclasses.fields(node.NodeState)} == NODE_STATE
    assert [f.name for f in dataclasses.fields(node.Record)] == ["now", "before", "remainder"]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = GameBoard(load_world(chain_body_world(tmp_path, TOOL, senses=(1,))), (lines := []).append)
    for family, state in zip(board.families, board.states, strict=True):
        assert len(state.lines) == family.lines
        assert len(state.write_remainders) == family.lines * family.held
    assert sorted(len(s.lines) for s in board.states) == [1, 1, 2, 2, 4]  # the sign: 2 rows
    calls, original = [], core.rule3

    def counting(*args):  # type: ignore[no-untyped-def]
        reads, _arrivals, _numerator, wall, now, other, remainder = args[:7]  # the call's kind, no state
        plain = reads is NO_READ and type(now) is int and (now == 1) and (other == 0)
        write = plain and type(wall) is int and isinstance(remainder, np.ndarray)
        arrays = isinstance(now, np.ndarray) and isinstance(other, np.ndarray)  # a step: reads on arrays
        kind = "write" if write else "step" if reads is not NO_READ and arrays else None
        calls.append((kind, id(args[4])))  # the call's kind and its level now, nothing kept
        return original(*args)

    engine = [m for m in list(sys.modules.values()) if getattr(m, "__name__", "").startswith("event_")]
    for module in [m for m in engine if m.__dict__.get("rule3") is original]:
        monkeypatch.setattr(module, "rule3", counting)
    for direction, act in ((1, board.step), (-1, board.step_inverse)):
        calls.clear(), act()
        records = [record for state in board.states for record in state.lines]
        steps = [begun for kind, begun in calls if kind == "step"]
        begun = {id(getattr(record, "before" if direction == 1 else "now")) for record in records}
        assert len(steps) == len(records) and begun == set(steps)  # one call each, on the level it began
        assert sum(k == "write" for k, _ in calls) == sum(len(s.write_remainders) for s in board.states)
    kept = BACK.snapshot(board)
    calls.clear()
    for index, (family, state) in enumerate(zip(board.families, board.states, strict=True)):
        if family.quanta:
            share.family_share(family, state.lines, board.wrap, board.world.node_clock)
            node.currents_of(family.pair[0], state.lines, board.wrap)
            node.stresses_of(family.pair[0], state.lines, board.wrap)
            node.wronskian(state.lines, family.plane), node.form(state.lines, state.lines)
            board.quanta(index)
    assert board.books() and all(kind != "write" for kind, _ in calls)  # the readings write nothing
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
    sources = {p.relative_to(ROOT): p.read_text(encoding="utf-8") for p in sorted(SOURCE.rglob("*.py"))}
    named = [f"{p}: {m.group(0)}" for p, text in sources.items() for m in INTEGER_KINDS.finditer(text)]
    assert named == ["src/event_universe/loader/world.py: np.int64"], named


INTEGER_KINDS = re.compile(r"np\.u?int(?:8|16|32|64|p)?\b|np\.iinfo|\"int64\"|dtype=np\.")


def test_the_composed_paces_are_the_laws_two_functions_of_the_content_and_their_factors():
    """The clock p_0(c) = Gamma (1 - 1 / Gamma)^c to the unit, (Gamma - 1)^c over Gamma^(c - 1) rounded half up, floor(exact + 1 / 2) in exact fractions, the fraction turned over for a hill (c below 0), by the memo's running fraction and by the power alone bit for bit; the Link's pace the clock twice, p_0^2 over Gamma rounded once; both Gamma at the vacuum; the Link's pace rounds to 0 at the content 28,206 at Gamma 6,000 (the clock 54 there, `frozen_content`, by the power alone, the memo kept to the run's contents) and the clock at 56,352; the group law Gamma p(c_1 + c_2) = p(c_1) p(c_2) within the roundings' floor, (p_1 + p_2 + Gamma) div 2 + 1 on the clock and three times it on the Link's pace, and not to zero, most pairs differing; the vectorised entries give the memo's value at every Node in the array's kind, the hardware's integers and Python's, on a narrow range (one table) and a sparse spread (the distinct values), the same after the memo is cleared; the write's factor is the source at the vacuum's paces for a count (two proper-interval powers) and for a Wronskian (one) alike, and elsewhere ((D p_x div Gamma) p_y div Gamma) p_z div p_0 on a count and ((D p_x div Gamma) p_y div p_0) p_z div p_0 on a Wronskian, one axis at a time (every intermediate within A^2 Gamma, inside 63 bits where A^2 Gamma^3 is not), 0 at a frozen clock; the turn's factor the angle at the vacuum and angle p_0 div Gamma elsewhere."""
    gamma, half, small = 6_000, Fraction(1, 2), range(-13, 1_300, 13)
    spread, zeros = [*small, 3_000], (0, 28_206, 56_351, 56_352)
    clocks = {c: paces.clock(gamma, c) for c in spread}
    assert clocks == {c: int(Fraction(gamma) * Fraction(gamma - 1, gamma) ** c + half) for c in spread}
    assert clocks == {c: paces.clock_alone(gamma, c) for c in spread}
    assert all(paces.link_pace(gamma, c) == int(Fraction(clocks[c] ** 2, gamma) + half) for c in spread)
    assert [paces.clock_alone(gamma, c) for c in zeros] == [gamma, 54, 1, 0]
    links = [paces.rounded(paces.clock_alone(gamma, c) ** 2, gamma) for c in (0, 28_205, zeros[1])]
    assert links == [gamma, 1, 0] and paces.frozen_content(gamma) == zeros[1]
    for f, times in ((paces.clock, 1), (paces.link_pace, 3)):
        off = [gamma * f(gamma, a + b) - f(gamma, a) * f(gamma, b) for a in small for b in small]
        room = [times * ((clocks[a] + clocks[b] + gamma) // 2 + 1) for a in small for b in small]
        assert all(abs(d) <= g for d, g in zip(off, room, strict=True))
        assert 2 * sum(d != 0 for d in off) > len(off)
    plain, entries = (paces.clock, paces.link_pace), (paces.clock_of, paces.link_pace_of)
    narrow, sparse = np.arange(-7, 53).reshape(5, 4, 3), np.array(spread[-60:]).reshape(5, 4, 3)
    for held in (narrow, sparse, narrow.astype(object), sparse.astype(object)):
        found, flat = [f(gamma, held) for f in entries], held.ravel().tolist()
        paces.clear_memo()
        assert all(np.array_equal(a, f(gamma, held)) for a, f in zip(found, entries, strict=True))
        assert all(a.dtype == held.dtype for a in found)
        assert [a.ravel().tolist() for a in found] == [[f(gamma, c) for c in flat] for f in plain]
    at, counts = np.full((2, 1, 1), gamma, dtype=np.int64), np.array([[[7]], [[2**40]]], dtype=np.int64)
    one = [paces.write_factor(counts, at, at, at, at, gamma, k) for k in (2, 1)]
    assert all(f.tolist() == counts.tolist() for f in [*one, paces.turn_factor(counts, at, gamma)])
    p = [paces.link_pace(gamma, c) for c in (300, 400, 500)] + [paces.clock(gamma, 400)]
    axis = (2**40 * p[0] + gamma // 2) // gamma * p[1]
    count = ((axis + gamma // 2) // gamma * p[2] + p[3] // 2) // p[3]
    wronskian = ((axis + p[3] // 2) // p[3] * p[2] + p[3] // 2) // p[3]
    both = [paces.write_factor(2**40, *p, gamma, k) for k in (2, 1)]
    assert both == [count, wronskian] and count != wronskian
    assert [paces.write_factor(9, 0, 0, 0, 0, gamma, k) for k in (2, 1)] == [0, 0]
    assert paces.turn_factor(gamma + 1, p[3], gamma) == ((gamma + 1) * p[3] + gamma // 2) // gamma
