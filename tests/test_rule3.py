"""Rule3 in one place (core/rule3.py; ALGEBRA.md #the-line, #the-direction, #the-interval): one function steps every record in either direction, the isotropic rule is the same call with equal paces, and no other file of src/ writes this arithmetic."""

from __future__ import annotations

import random
import re
from pathlib import Path

import numpy as np

from event_universe.core.rule3 import ISOTROPIC, coefficients, form_term, rule3, rule_total_bound
from event_universe.events import detector_law
from event_universe.world_files import parse_nature_beam_world
from tests.worlds import emitter_world

ROOT = Path(__file__).resolve().parents[1]
SOURCE, GAMMA = ROOT / "src" / "event_universe", 10_000


def old_isotropic(
    num: int, den: int, gamma: int, content: int, weak_field: bool
) -> tuple[int, int, int]:
    """The engine's `rule_coefficients` before the cut (events/rule.py of main 6d2a92e2), the oracle: (R, S, w) of the weak-field rule, or of the plain first-order rule."""
    pace = gamma - content
    if not weak_field:
        return pace * num, 6 * den * content, 3 * den * gamma
    squares = pace * pace
    gamma_squared = gamma * gamma
    self_coefficient = (
        12 * den * gamma_squared - 6 * (squares + gamma_squared) * (den - num) - 12 * num * squares
    )
    return 2 * squares * num, self_coefficient, 6 * den * gamma_squared


def old_axes(
    num: int, den: int, gamma: int, content: int, axis_contents: tuple[int, int, int]
) -> tuple[tuple[int, int, int], int, int]:
    """The engine's `axis_rule_coefficients` before the cut, the oracle of the four paces."""
    pace = gamma - content
    paces, gamma_squared = [pace - axis_contents[axis] for axis in range(3)], gamma * gamma
    reads = (2 * paces[0] ** 2 * num, 2 * paces[1] ** 2 * num, 2 * paces[2] ** 2 * num)
    squares = paces[0] ** 2 + paces[1] ** 2 + paces[2] ** 2
    self_coefficient = (
        12 * den * gamma_squared - 6 * (pace * pace + gamma_squared) * (den - num) - 4 * num * squares
    )
    return reads, self_coefficient, 6 * den * gamma_squared


def test_the_coefficients_are_the_two_old_functions_and_the_isotropic_ones_at_zero_axis_contents():
    """With the axis contents zero the isotropic rule's (R, R, R), S, w term for term; with them the four paces' reads; `weak_field` False the plain rule; the vacuum 2 Gamma^2 times the plain rule."""
    rng = random.Random(3)
    for _ in range(500):
        num, den = rng.randint(1, 1000), rng.randint(1, 1000)
        gamma = rng.choice([1, 100, GAMMA])
        content = rng.randint(-gamma + 1, gamma - 1)
        axis_contents = (rng.randint(-50, 50), rng.randint(-50, 50), rng.randint(-50, 50))
        for weak_field in (True, False):
            read, self_coefficient, wall = old_isotropic(num, den, gamma, content, weak_field)
            assert coefficients(num, den, gamma, content, weak_field=weak_field) == (
                (read, read, read),
                self_coefficient,
                wall,
            )
        assert coefficients(num, den, gamma, content, axis_contents) == old_axes(
            num, den, gamma, content, axis_contents
        )
        assert coefficients(num, den, gamma, content, (0, 0, 0)) == coefficients(
            num, den, gamma, content
        )
        # the vacuum c = 0: 2 Gamma^2 times the plain rule (the levels bit for bit)
        assert coefficients(num, den, gamma, 0) == ((2 * gamma**2 * num,) * 3, 0, 6 * den * gamma**2)
        # a tensor along x alone slows the x read and the own term by 4 num (p_x^2 - p_0^2)
        pace, axis_pace = gamma - content, gamma - content - axis_contents[0]
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
        num, den = rng.randint(1, 1000), rng.randint(1, 1000)
        gamma = rng.choice([1, GAMMA])
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


def test_every_step_of_the_engine_goes_through_the_one_rule(monkeypatch):
    """The engine's records step and step back through rule3 alone (+1 forward, -1 back, a spy on the one name the engine imports), and the operation primitive of the register is rule3 itself."""
    calls, real_rule = {"forward": 0, "backward": 0}, detector_law.rule3

    def spy_rule(*args: object) -> object:
        calls["forward" if len(args) < 8 or args[7] == 1 else "backward"] += 1
        return real_rule(*args)

    monkeypatch.setattr(detector_law, "rule3", spy_rule)
    simulation = detector_law.DetectorLawSimulation(
        parse_nature_beam_world(emitter_world(stock=1, ticks=4))
    )
    assert simulation.register.at("the operation", "(i)") is rule3
    simulation.step()
    assert calls["forward"] >= len(simulation.held_component_records()) and calls["backward"] == 0
    simulation.step_inverse()
    assert calls["backward"] >= 1 and simulation.books()["balanced"]


# A Node's level goes to its six neighbours only through the Ports: the one shift of an array across a Link is core/ports.py's `arrival`, the send and the receive; every reading of a neighbour's level (the transport's arrival sums, the flux at a Port, the shell of a body) takes it from there.
SHIFT_HOME = {"src/event_universe/core/ports.py": {"arrival"}}
SHIFT_TOKENS = re.compile(r"np\.roll\(|\._shift\(|\.take\(")


def test_no_other_code_moves_a_level_from_one_node_to_another():
    """Every shift of an array across Nodes in src/ is core/ports.py's `arrival` (no np.roll, no take, no shift elsewhere: the loop reads its neighbours through the Ports), and no function of src/ is a split of its own."""
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
    assert "src/event_universe/events/detector_law.py" not in found
    for home, functions in SHIFT_HOME.items():
        assert found.pop(home) == functions
    assert found == {}, found
    # the engine, core and the folders hold no split of their own (the loader's parse of the refused key `splits` in world.py is a refusal, not a step, and goes with world.py)
    stepping = [SOURCE / "events" / "detector_law.py", *sorted((SOURCE / "core").glob("*.py"))]
    stepping += sorted((SOURCE / "features").rglob("*.py"))
    for path in stepping:
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.FunctionDef):
                assert "split" not in node.name.lower(), f"{path.name}: {node.name}"


def test_a_run_stepped_forward_and_back_returns_bit_for_bit():
    """Rule3 with the direction -1 undoes +1 exactly: the emitter world eight intervals forward and eight back returns every record's levels, remainders and the held levels bit for bit (ALGEBRA.md #the-direction)."""
    simulation = detector_law.DetectorLawSimulation(
        parse_nature_beam_world(emitter_world(stock=1, ticks=8))
    )
    start = {
        key: (live.now.copy(), live.before.copy(), live.remainder.copy())
        for key, live in simulation.records.items()
    }
    held = {key: record.now.copy() for key, record in simulation.held_records.items()}
    for _ in range(8):
        simulation.step()
    for _ in range(8):
        simulation.step_inverse()
    for key, (now, before, remainder) in start.items():
        live = simulation.records[key]
        assert np.array_equal(live.now, now) and np.array_equal(live.before, before)
        assert np.array_equal(live.remainder, remainder)
    for key, level in held.items():
        assert np.array_equal(simulation.held_records[key].now, level)
