"""Rule3 in one place (core/rule3.py; ALGEBRA.md #the-line, #the-direction, #the-interval): one function steps every record in either direction, the isotropic rule is the same call with equal paces, and no other file of src/ writes this arithmetic."""

from __future__ import annotations

import random
import re
from pathlib import Path

import numpy as np

from event_universe.core.rule3 import ISOTROPIC, coefficients, form_term, rule3, rule_total_bound

ROOT = Path(__file__).resolve().parents[1]
SOURCE, GAMMA = ROOT / "src" / "event_universe", 10_000


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
            assert coefficients(num, den, gamma, content, weak_field=weak_field) == (
                (read, read, read),
                self_coefficient,
                wall,
            )
        assert coefficients(num, den, gamma, content, axis_contents) == law_axes(
            num, den, gamma, content, axis_contents
        )
        assert coefficients(num, den, gamma, content, (0, 0, 0)) == coefficients(
            num, den, gamma, content
        )
        # the vacuum c = 0: 2 Gamma^2 times the plain rule (the levels bit for bit)
        assert coefficients(num, den, gamma, 0) == ((2 * gamma**2 * num,) * 3, 0, 6 * den * gamma**2)
        # a tensor along x alone slows the x read and the own term by 4 num (p_x^2 - p_link^2), the Link's pace Gamma - 2 c
        pace, axis_pace = gamma - 2 * content, gamma - 2 * content - axis_contents[0]
        (read, *_), self_iso, wall = coefficients(num, den, gamma, content)
        assert coefficients(num, den, gamma, content, (axis_contents[0], 0, 0)) == (
            (2 * axis_pace**2 * num, read, read),
            self_iso - 4 * num * (axis_pace**2 - pace**2),
            wall,
        )
    assert ISOTROPIC == (0, 0, 0)


def test_the_one_rule_steps_forward_and_back_exactly_on_integers_and_int64_arrays():
    """w a_next + r' = SUM_a R_a arr_a + S a_now - w a_before + r with 0 <= r' < w, the inverse exact; on int64 arrays the sum over the axes equals R times the six-sum bit for bit, the dtype kept."""
    rng = random.Random(5)
    for _ in range(500):
        num, den, gamma = rng.randint(1, 1000), rng.randint(1, 1000), rng.choice([1, GAMMA])
        content = rng.randint(-gamma + 1, gamma - 1)
        reads, self_coefficient, wall = coefficients(
            num, den, gamma, content, (rng.randint(-30, 30), rng.randint(-30, 30), rng.randint(-30, 30))
        )
        arrivals = tuple(rng.randint(-(10**6), 10**6) for _ in range(3))
        now, before = rng.randint(-(10**6), 10**6), rng.randint(-(10**6), 10**6)
        remainder = rng.randint(0, wall - 1)
        total = (
            sum(read * arrival for read, arrival in zip(reads, arrivals, strict=True))
            + self_coefficient * now
            - wall * before
            + remainder
        )
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
RULE_LINES = (
    r"self_coefficient \* now\b",
    r"wall \* other\b",
    r"direction \* total \+ carry",
    r"direction \* quotient",
    r"now \* now \+ before \* before",
)
RULE_ARITHMETIC = RULE_LINES + (
    r"self_coefficient \* before\b",
    r"wall \* before\b",
    r"wall \* now \+ remainder",
    r"direction \* carry\b",
)


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


# A Node's level goes to its six neighbours only through the Ports: the one shift of an array across a Link is core/ports.py's `arrival`; every reading of a neighbour's level (Rule3's arrival sums, the currents at a Port, a body's shell and region) takes it from there.
SHIFT_HOME = {"src/event_universe/core/ports.py": {"arrival"}}
SHIFT_TOKENS = re.compile(r"np\.roll\(|\._shift\(|\.take\(")


def test_no_other_code_moves_a_level_from_one_node_to_another():
    """Every shift of an array across Nodes in src/ is core/ports.py's `arrival` (no np.roll, no take, no shift elsewhere: the Node reads its neighbours through the Ports), and no function of src/ is a split of its own."""
    import ast

    found: dict[str, set[str]] = {}
    for path in sorted(SOURCE.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        if not SHIFT_TOKENS.search(text):
            continue
        tree = ast.parse(text)
        spans = [
            (node.lineno, node.end_lineno or node.lineno, node.name)
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        ]
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
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.FunctionDef):
                assert "split" not in node.name.lower(), f"{path.name}: {node.name}"


# The integers the law writes and the engine may hold: 0 and 1 (the identity and the direction, -1 the inverse and the hole), 2 (the halves: W_c div 2, the half wall, the axis contents' rounding, two levels), 3 (the three axes, 3 den) and 6 (the six Ports, 6 den); in Rule3's own line (core/rule3.py) also 4 and 12 of S = 12 den Gamma^2 - 12 (den - num) p_0^2 - 4 num SUM p_a^2.
LAW_INTEGERS = frozenset({0, 1, 2, 3, 6})
RULE_LINE_INTEGERS = frozenset({4, 12})


def test_no_integer_beyond_the_laws_own_enters_the_engine_or_the_generator():
    """No integer literal in src/event_universe or tools/pixel_mode.py beyond the law's own (LAW_INTEGERS; Rule3's line's 4 and 12 in core/rule3.py alone): every other number is a file's key or the rule's own act, so a number cannot enter the engine again."""
    import ast

    found = []
    for path in [*sorted(SOURCE.rglob("*.py")), ROOT / "tools" / "pixel_mode.py"]:
        allowed = LAW_INTEGERS | (RULE_LINE_INTEGERS if path.name == "rule3.py" else frozenset())
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Constant) and type(node.value) in (int, float, complex):
                if node.value not in allowed or type(node.value) is not int:
                    found.append(f"{path.relative_to(ROOT)}:{node.lineno} {node.value!r}")
    assert not found, found
