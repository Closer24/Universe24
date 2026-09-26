"""THE RULE IN ONE PLACE (the model owner's question of 2026-09-26 through the Boss, 16:33Z;
ALGEBRA.md 9.57 (1), 9.50 (8), (9) and (13), 9.91 (2); the operation's cut of issue #1154;
src/event_universe/core/rule3.py).

One function steps every record at every Node, the body's Node record included; its inverse
stands beside it; the conserved form's Node term is read from the same integers; the isotropic
rule is the same call with the three paces equal (the axis contents zero); the coefficients are
the two functions of the engine before the cut, term for term; no other file of src/ writes this
arithmetic; the operation primitive of the register is rule3 itself. Bit for bit on every
shipped world: the suites' digests and the shipped worlds' record."""

from __future__ import annotations

import random
import re
from pathlib import Path

import numpy as np

from event_universe.core.rule3 import (
    ISOTROPIC,
    coefficients,
    form_term,
    rule3,
    rule3_inverse,
    rule_total_bound,
)
from event_universe.events import detector_law
from event_universe.world_files import parse_nature_beam_world
from tests.test_emitter import emitter_world

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "event_universe"
GAMMA = 10_000


def old_isotropic(
    num: int, den: int, gamma: int, content: int, weak_field: bool
) -> tuple[int, int, int]:
    """The engine's `rule_coefficients` before the cut (events/rule.py of main 6d2a92e2), the
    oracle: (R, S, w) of the weak-field rule, or of the plain first-order rule."""
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
    paces = [pace - axis_contents[axis] for axis in range(3)]
    gamma_squared = gamma * gamma
    reads = (2 * paces[0] ** 2 * num, 2 * paces[1] ** 2 * num, 2 * paces[2] ** 2 * num)
    squares = paces[0] ** 2 + paces[1] ** 2 + paces[2] ** 2
    self_coefficient = (
        12 * den * gamma_squared - 6 * (pace * pace + gamma_squared) * (den - num) - 4 * num * squares
    )
    return reads, self_coefficient, 6 * den * gamma_squared


def test_the_coefficients_are_the_two_old_functions_and_the_isotropic_ones_at_zero_axis_contents():
    """One function of the paces: with the axis contents zero it is the isotropic rule's
    (R, R, R), S, w term for term (4 num x 3 p^2 = 12 num p^2); with them the four paces'
    reads; `weak_field` False the plain first-order rule; `ISOTROPIC` is the default."""
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
    assert ISOTROPIC == (0, 0, 0)


def test_the_one_rule_steps_forward_and_back_exactly_on_integers_and_int64_arrays():
    """w a_next + r' = SUM_a R_a arr_a + S a_now - w a_before + r with 0 <= r' < w, and the
    inverse returns a_before and r exactly; on int64 arrays the sum over the axes equals R
    times the six-sum bit for bit (the ring's arithmetic), the dtype kept."""
    rng = random.Random(5)
    for _ in range(500):
        num, den = rng.randint(1, 1000), rng.randint(1, 1000)
        gamma = rng.choice([1, GAMMA])
        content = rng.randint(-gamma + 1, gamma - 1)
        reads, self_coefficient, wall = coefficients(
            num, den, gamma, content, (rng.randint(-30, 30), rng.randint(-30, 30), rng.randint(-30, 30))
        )
        arrivals = (
            rng.randint(-(10**6), 10**6),
            rng.randint(-(10**6), 10**6),
            rng.randint(-(10**6), 10**6),
        )
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
        assert rule3_inverse(reads, arrivals, self_coefficient, wall, nxt, now, carried) == (
            before,
            remainder,
        )
    generator = np.random.default_rng(9)
    shape = (4, 3, 2)
    num = np.full(shape, 800, dtype=np.int64)
    den = np.full(shape, 809, dtype=np.int64)
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
    back, remainder_back = rule3_inverse(reads, arrivals, self_coefficient, wall, nxt, now, carried)
    assert np.array_equal(back, before) and np.array_equal(remainder_back, remainder)


def test_the_forms_node_term_and_the_load_bound_read_the_same_integers():
    """The form's Node term w (now^2 + before^2) - S now before and the load bound 6 A R + A |S|
    + w (A + 1) are read from the one function's integers."""
    reads, self_coefficient, wall = coefficients(800, 809, GAMMA, 250)
    assert form_term(self_coefficient, wall, 7, -3) == wall * (49 + 9) + self_coefficient * 21
    amplitude = 1 << 20
    assert rule_total_bound(800, 809, GAMMA, 250, amplitude, True) == 6 * amplitude * abs(
        reads[0]
    ) + amplitude * abs(self_coefficient) + wall * (amplitude + 1)


# the rule's own lines: the Node's term, the step's second level, the inverse's and the form's
RULE_ARITHMETIC = (
    r"self_coefficient \* (now|before)\b",
    r"wall \* before\b",
    r"wall \* now \+ remainder",
    r"now \* now \+ before \* before",
)


def test_no_other_file_of_src_writes_the_rules_arithmetic():
    """(d) of the model owner's target: the rule is written once, in core/rule3.py; every other
    file of src/ calls it."""
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
    assert all(re.search(pattern, own) for pattern in RULE_ARITHMETIC)


def test_every_step_of_the_engine_goes_through_the_one_rule(monkeypatch):
    """The engine's records step and step back through core.rule alone (a spy on the two names
    the engine imports), and the operation primitive of the register is rule3 itself."""
    calls = {"rule": 0, "rule3_inverse": 0}
    real_rule, real_inverse = detector_law.rule3, detector_law.rule3_inverse

    def spy_rule(*args: object) -> object:
        calls["rule"] += 1
        return real_rule(*args)

    def spy_inverse(*args: object) -> object:
        calls["rule3_inverse"] += 1
        return real_inverse(*args)

    monkeypatch.setattr(detector_law, "rule3", spy_rule)
    monkeypatch.setattr(detector_law, "rule3_inverse", spy_inverse)
    simulation = detector_law.DetectorLawSimulation(
        parse_nature_beam_world(emitter_world(stock=1, ticks=4))
    )
    assert simulation.register.at("the operation", "(i)") is rule3
    simulation.step()
    stepped = calls["rule"]
    assert stepped >= len(simulation.held_component_records())
    if hasattr(simulation, "step_inverse"):
        simulation.step_inverse()
        assert calls["rule3_inverse"] >= 1
    assert simulation.books()["balanced"]


# THE SPLIT IS BUILT FROM THE RULE TOO (the model owner's word through the Boss, record 2234): a
# Node's level goes to its six neighbours only through rule3's own send, receive, wait and
# operation; the split has no function of its own. The functions that shift an array across
# Nodes, each with its reason: the transport (send and receive, the arrival sums rule3 reads) and
# the readings of a neighbour's level at a Port (the flux booked at the Node, no level written);
# a shift of a mask or of an index (the shell, the sets' Ports) moves no level.
LEVEL_SHIFTERS = {
    "_shift": "the one shift of an array across a Link, the send and the receive",
    "_neighbours": "the six neighbours' sum, the receive",
    "_axis_sums": "the arrival sums per axis, the receive rule3 reads",
    "_arrival": "one neighbour's level after the transport, the receive",
    "inward_flux": "the neighbour's levels read at a detector's Ports for the booking, no level written",
    "body_outward_flux": "the neighbour's levels read at a body's outer Ports for the window, no level written",
}
INDEX_SHIFTERS = {"shell_mask", "_flux_ports", "_inflow_ports"}


def test_no_other_code_moves_a_level_from_one_node_to_another():
    """Record 2234: every shift of an array across Nodes in src/ sits in a named function of the
    transport or of a Port's reading, and no function of src/ is a split of its own."""
    import ast

    found: dict[str, set[str]] = {}
    for path in sorted(SOURCE.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        if "np.roll(" not in text and "._shift(" not in text:
            continue
        tree = ast.parse(text)
        spans = [
            (node.lineno, node.end_lineno or node.lineno, node.name)
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        ]
        for match in re.finditer(r"np\.roll\(|self\._shift\(", text):
            line = text.count("\n", 0, match.start()) + 1
            inner = max((span for span in spans if span[0] <= line <= span[1]), key=lambda span: span[0])
            found.setdefault(path.relative_to(ROOT).as_posix(), set()).add(inner[2])
    engine = found.pop("src/event_universe/events/detector_law.py")
    assert engine <= set(LEVEL_SHIFTERS) | INDEX_SHIFTERS, engine - set(LEVEL_SHIFTERS) - INDEX_SHIFTERS
    assert {name for name in found if not name.startswith("src/event_universe/diagnostics/")} == set(), (
        found
    )
    # the engine, core and the folders hold no split of their own (the loader's parse of the
    # refused key `splits` in world.py is a refusal, not a step, and goes with world.py)
    stepping = [SOURCE / "events" / "detector_law.py", *sorted((SOURCE / "core").glob("*.py"))]
    stepping += sorted((SOURCE / "features").rglob("*.py"))
    for path in stepping:
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.FunctionDef):
                assert "split" not in node.name.lower(), f"{path.name}: {node.name}"
