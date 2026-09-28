"""The hold's folder: every division through core.rule3, forward then back exact; the dipole's terms; the refusals; the card bound, the loop's hold being this folder's line."""

import json
import random
from pathlib import Path

import pytest

from event_universe.core.register import folder_of
from event_universe.core.rule3 import division_back, division_forward
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.hold import (
    ACTS,
    CROSS_TERMS,
    DECLARATION,
    THE_ADVANCE,
    THE_INVERSE,
    THE_LOAD,
    THE_REWRITE,
    THE_UNHOLD,
    HoldOwn,
    HoldStart,
    HoldTerm,
    apply,
)
from event_universe.world_files import parse_nature_beam_world
from tests.running import stamped
from tests.worlds import emitter_world

ROOT, ENGINE_START = Path(__file__).resolve().parents[1], "examples/events/engine_start.json"


def test_forward_then_back_returns_the_state_exactly_and_the_load_writes_the_first_value_twice():
    """Rule3's division act forward and its direction -1 back: an advance then an inverse returns the state; the value before is the ceiling form; at the load both levels are the first value."""
    rng = random.Random(7)
    for _ in range(300):
        wall = rng.randint(1, 10**6)
        numerator, carry = rng.randint(-(10**9), 10**9), rng.randint(0, wall - 1)
        value, carried = division_forward(numerator, wall, carry)
        assert (value, carried) == divmod(numerator + carry, wall)
        value_before, carry_before = division_back(numerator, wall, value, carried)
        assert carry_before == carry and value_before == -((carry - numerator) // wall)
    term = HoldTerm("content", (1, 3, 6), (1, 4, 2), None, 1, 1)
    loaded = apply(term, HoldStart(THE_LOAD, 64, (3120, 0, 0), 12480, None), HoldOwn({}, {}))
    assert loaded.time_level == 0 and dict(loaded.own.values)[(1,)] == 64 * 4 * 3120 // 12480 == 64
    assert all(now == before for _part, _node, now, before in loaded.parts)
    advanced = apply(term, HoldStart(THE_ADVANCE, 64, (3120, 0, 0), 12480, None), loaded.own)
    assert advanced.time_level == 64  # the count over the divisor 1, this interval's source
    assert [(p, b) for p, _k, _n, b in advanced.parts] == [(p, n) for p, _k, n, _b in loaded.parts]
    rewritten = apply(term, HoldStart(THE_REWRITE, 64, (3120, 0, 0), 12480, None), advanced.own)
    assert rewritten.own == advanced.own
    assert all(n == b == dict(advanced.own.values)[(p,)] for p, _k, n, b in rewritten.parts)
    back = apply(term, HoldStart(THE_INVERSE, 64, (3120, 0, 0), 12480, None), advanced.own)
    assert dict(back.own.values) == dict(loaded.own.values)
    assert dict(back.own.carries) == dict(loaded.own.carries)
    # the vector part over the row's divisor E_s as the time part, per Node at a body in the law's form
    over = HoldTerm("content", (1, 3), (1, 4), None, 1, 7)
    nodes = ((("n", 4, 0, 0), 50), (("n", 5, 0, 0), 14))
    whole = apply(over, HoldStart(THE_LOAD, 64, (3120, 0, 0), 12480, None), HoldOwn({}, {}))
    each = apply(over, HoldStart(THE_LOAD, 64, (3120, 0, 0), 12480, None, nodes), HoldOwn({}, {}))
    first = 4 * 64 * 3120 // (7 * 12480)
    assert [(k, n) for _p, k, n, _b in whole.parts] == [(None, first), (None, 0), (None, 0)]
    assert [(k, n) for p, k, n, _b in each.parts if p == 1] == [
        (k, 4 * c * 3120 // (7 * 12480)) for k, c in nodes
    ]
    assert dict(each.own.carries)[(1, 4, 0, 0)] == 4 * 50 * 3120 % (7 * 12480)


def test_the_dipoles_terms_are_the_table_of_9_91_3():
    """A spin S at the body's Node writes sigma x (S x e_j)_i at the Node + sigma e_j (S x e_x = (0, S_z, -S_y) and cyclic); the moment the same over the divisor 2; a zero vector writes no dipole."""

    def cross(vector, j):
        out = [0, 0, 0]
        for i, component, sign in CROSS_TERMS[j]:
            out[i] = sign * vector[component]
        return tuple(out)

    assert cross((1, 2, 3), 0) == (0, 3, -2) and cross((1, 2, 3), 1) == (-3, 0, 1)
    assert cross((1, 2, 3), 2) == (2, -1, 0)
    gravity = HoldTerm("content", (1, 3, 6), (1, 4, 2), "spin", 1, 1)
    writes = apply(gravity, HoldStart(THE_LOAD, 5, (0, 0, 0), 15, (0, 0, 1)), HoldOwn({}, {}))
    assert keyed(writes.dipoles) == {((1, 0, 1), 1), ((1, 0, -1), -1), ((0, 1, 1), -1), ((0, 1, -1), 1)}
    charge = HoldTerm("sign", (1, 3), (1, 1), "moment", 2, 1)
    first = apply(charge, HoldStart(THE_LOAD, 1, (0, 0, 0), 3, (0, 0, 1)), HoldOwn({}, {}))
    assert keyed(first.dipoles) == {((1, 0, 1), 0), ((1, 0, -1), -1), ((0, 1, 1), -1), ((0, 1, -1), 0)}
    assert all(carry == 1 for key, carry in first.own.carries.items() if key[0] == "d")
    second = apply(charge, HoldStart(THE_ADVANCE, 1, (0, 0, 0), 3, (0, 0, 1)), first.own)
    assert keyed(second.dipoles) == {((1, 0, 1), 1), ((1, 0, -1), 0), ((0, 1, 1), 0), ((0, 1, -1), 1)}
    unheld = apply(charge, HoldStart(THE_UNHOLD, 1, (0, 0, 0), 3, (0, 0, 1)), second.own)
    assert keyed(unheld.dipoles) == {(key, now) for key, now, _b in second.dipoles}
    assert dict(unheld.own.carries) == dict(first.own.carries)
    assert dict(unheld.own.values) == dict(first.own.values)
    assert act(gravity, HoldStart(THE_LOAD, 5, (0, 0, 0), 15, (0, 0, 0))).dipoles == ()
    no_dipole = HoldTerm("content", (1,), (1,), "spin", 1, 1)
    assert act(no_dipole, HoldStart(THE_LOAD, 5, (0, 0, 0), 15, (0, 0, 1))).dipoles == ()


def keyed(dipoles):
    return {(key, now) for key, now, _b in dipoles}


def term_of(count, parts, factors, dipole, divisor):
    return HoldTerm(count, parts, factors, dipole, divisor, 1)


def act(term, start):
    return apply(term, start, HoldOwn({}, {}))


def test_the_refusals_by_name():
    with pytest.raises(ValueError, match="count word is 'mass'"):
        act(term_of("mass", (1,), (1,), None, 1), HoldStart(THE_LOAD, 1, (0, 0, 0), 1, None))
    with pytest.raises(ValueError, match="act is one of"):
        act(term_of("content", (1,), (1,), None, 1), HoldStart("the hop", 1, (0, 0, 0), 1, None))
    with pytest.raises(ValueError, match="go group for group"):
        act(term_of("content", (1, 3), (1,), None, 1), HoldStart(THE_LOAD, 1, (0, 0, 0), 1, None))
    with pytest.raises(ValueError, match="from 1"):
        act(term_of("content", (1,), (1,), None, 1), HoldStart(THE_LOAD, 1, (0, 0, 0), 0, None))
    with pytest.raises(ValueError, match="divisor E_s is from 1"):
        act(HoldTerm("content", (1,), (1,), None, 1, 0), HoldStart(THE_LOAD, 1, (0, 0, 0), 1, None))
    assert ACTS == (THE_LOAD, THE_ADVANCE, THE_REWRITE, THE_INVERSE, THE_UNHOLD)


def test_the_source_adds_the_count_over_the_divisor_each_interval_and_steps_back():
    """The time part is this interval's increment (count + r) div E_s with the remainder carried, 0 at the load; the inverse returns the increment it subtracts and steps the store back."""
    term = HoldTerm("content", (1,), (1,), None, 1, 7)
    loaded = apply(term, HoldStart(THE_LOAD, 10, (0, 0, 0), 1, None), HoldOwn({}, {}))
    own = loaded.own  # the load's division leaves the remainder 3 on the body; no increment is written
    assert loaded.time_level == 0
    increments = []
    for _ in range(7):
        writes = apply(term, HoldStart(THE_ADVANCE, 10, (0, 0, 0), 1, None), own)
        own, increments = writes.own, increments + [writes.time_level]
    assert increments == [1, 2, 1, 2, 1, 2, 1] and sum(increments) == 10  # exact over seven intervals
    back = apply(term, HoldStart(THE_INVERSE, 10, (0, 0, 0), 1, None), own)
    assert (back.time_level, dict(back.own.carries)[(0,)], dict(back.own.values)[(0,)]) == (1, 0, 2)


def test_the_vector_and_tensor_parts_enter_over_the_divisor_at_the_time_parts_scale():
    """The three parts are one source at one scale (ALGEBRA.md the hold's row, #1340): the vector part factor x s x n_a div (E_s W) and the tensor part factor x s x n_a n_b div (E_s W^2), so each interval the vector part stands to the time part's increment as factor x n_a / W and the tensor part as factor x n_a^2 / W^2, each within one unit of its own carried division."""
    term = HoldTerm("content", (1, 3, 6), (1, 4, 2), None, 1, 7)
    own = apply(term, HoldStart(THE_LOAD, 64, (3120, 0, 0), 12480, None), HoldOwn({}, {})).own
    for _ in range(50):
        writes = apply(term, HoldStart(THE_ADVANCE, 64, (3120, 0, 0), 12480, None), own)
        own, time, vector, tensor = writes.own, writes.time_level, writes.parts[0][2], writes.parts[3][2]
        assert (
            abs(vector * 12480 - 4 * 3120 * time) <= 12480 + 4 * 3120
        )  # the x part against the increment
        assert abs(tensor * 12480**2 - 2 * 3120**2 * time) <= 12480**2 + 2 * 3120**2  # the xx part


def test_the_declaration_is_the_ledgers_row():
    """ "the hold" at (iv), the word the right side, the writes a family's level at a Node and a body's remainders, its function `apply`; the register finds the folder bound: the loop calls `apply`."""
    assert DECLARATION.name == "the hold" and folder_of("the hold") == "hold"
    assert DECLARATION.place == "(iv)" and DECLARATION.word == "the right side"
    assert DECLARATION.writes == ("a family's level at a Node", "a body's remainders")
    assert DECLARATION.function is apply and DECLARATION.built
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=2)))
    registered = simulation.register.declarations["the hold"]
    assert registered.binder is None and registered.function is apply


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_a_body_in_the_laws_form_sources_each_node_by_the_count_there(tmp_path):
    """The hold's row on a body in the law's form (ALGEBRA.md #what-a-body-is; ENGINE.md the `nodes` row): a held family's time part at each of the body's Nodes gains (the count declared THERE + r) div E_s each interval by the carried division with a remainder of its own, never the body's whole count at every Node. Two runs from the load's level 0 (THE START left out: its rest depends on the divisor) at two divisors, one above the body's whole count and one twice its largest count and above, differ after the first interval by the increments alone: (2 c div E_s) - (c div E_s) at a Node of count c under the first and 0 under the second, so the difference is 1 at the one Node whose count is at least half the first divisor and 0 elsewhere, where the whole count would make the two runs agree at every Node."""
    counts = {(4, 0, 0): 5, (5, 0, 0): 7, (6, 0, 0): 1}
    whole, largest = sum(counts.values()), max(counts.values())
    universe = json.loads(
        (ROOT / "examples/events/experiments/universe.json").read_text(encoding="utf-8")
    )
    body = {"family": "matter", "momentum": [0, 0, 0], "momentum_before": [0, 0, 0]}
    body["nodes"] = [{"node": list(node), "count": count} for node, count in counts.items()]
    levels, strip = {}, {"name": "strip", "positions": [[6, 0, 0]]}
    for divisor in (whole + 1, 2 * largest + 1):
        for row in universe["families"]:
            row.get("held", {}).update(divisor=divisor)
        (tmp_path / f"universe_{divisor}.json").write_text(json.dumps(universe), encoding="utf-8")
        boundary = {**dict.fromkeys("xyz", "periodic"), "x": "closed"}
        board = {"shape": [16, 1, 1], "boundary": boundary, "N": 64}
        files = {"universe": str(tmp_path / f"universe_{divisor}.json"), "engine": ENGINE_START}
        document = stamped({**board, **files, "ticks": 2, "measured": [body], "detectors": [strip]})
        simulation = DetectorLawSimulation(parse_nature_beam_world(document))
        gravity = [family.name for family in simulation.families].index("gravity")
        simulation.step()
        levels[divisor] = simulation.held_records[gravity].now.copy()
    difference = levels[whole + 1] - levels[2 * largest + 1]
    expected = {node: 2 * c // (whole + 1) - c // (whole + 1) for node, c in counts.items()}
    assert {node: int(difference[node]) for node in counts} == expected and sum(expected.values()) == 1
    assert int(abs(difference).sum()) == 1  # that Node alone; the whole count would gain 1 at each
