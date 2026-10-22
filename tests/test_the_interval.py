"""The hypothesis's construction (ALGEBRA.md, The board's interval is no observable; The mean's velocity is the content's; The motion of gravity's row is a hill at the symmetry's weight; The hill's weight is the write's mix; The form's own clock; The factor carried; the hypotheses under their own names, 2026-10-22; DESIGN section 3, T3 to T8), construction alone and no world of the experiment: the form's own clock as one power of the write (T6), the hill's weight's integer and its rounding (T3), the premise as a test (T4), the run back refused by name under the key (T5), the mix's weight following the Node's own sources (T7) and the end's booking switch (T8); the declaration and the attractor stand in tests/test_the_uniform_mode.py (T1, T2 and T9), the builders in tests/laws_interval.py."""

import inspect
import math
import re
from dataclasses import replace

import numpy as np
import pytest

from event_universe import board_readings, records, world_files
from event_universe.core import paces
from event_universe.features.held_write import held_write
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import BACK
from tests.laws_interval import GAMMA, laid_torus, light_torus, lockstep, universe_at_weight_one


def test_the_forms_own_clock_books_a_count_once_and_the_write_dims_as_the_pairs_integer(
    tmp_path, monkeypatch
):
    """T6, the form's own clock (ALGEBRA.md, The write per proper volume and per proper interval, The form's own clock; loader/universe.booking_of, loader/derived.FamilyRule.power and exponent, records.write_sources): on the 3-cube torus under the law's key with gravity declaring `booking: form` the booking's power is 1 and the row's exponents 6 for its own massless pair and 5 for matter's gapped pair (7 and 6 under `count`, the law), the write's numerator over 60 intervals is `paces.write_factor(D, p, p, p, p_0, Gamma, 1)` bit for bit, the Wronskian's power on a count, and gravity's level after each write the held write's own (features/held_write) with the remainder after it, under `count` the same at the power 2; the write's dimming read from the first and the last interval as -ln(s_t / s_0) / (U_t - U_0) lies within 0.3 of 4.8 under the key (between 4 and 5: the form's clock's e^(-4 U) with the record's own sine running) and within 0.3 of 5.8 without it (between 5 and 6), the eras hand's and the kinematics hand's exponents for [4000, 6000] at small U; the genericity hand's line: one power of the write, no other act."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    exponents = {}
    for booking, power in (("form", 1), ("count", 2)):
        universe_at_weight_one(tmp_path, gravity={"booking": booking})
        board = Lattice(load_world(laid_torus(tmp_path, f"clock_{booking}", uniform="carried")))
        names = [family.name for family in board.families]
        gravity, matter = board.families[names.index("gravity")], board.families[names.index("matter")]
        assert (gravity.power, gravity.exponent(), matter.exponent(power)) == (
            power,
            3 + power + 2,
            3 + power + 1,
        )
        assert (gravity.form_clock, matter.exponent()) == (
            power == 1,
            3 + 2 + 1,
        )  # a reader's own power the law's
        wall, numerators = board.walls(names.index("gravity"))[0], []
        for step in lockstep(board, names.index("gravity"), names.index("matter"), 60):
            form = step["now"] * step["now"] - step["next"] * step["before_record"]
            clock, pace = paces.node_paces(
                GAMMA, step["level"]
            )  # matter reads gravity at 1, the content
            numerator = int(paces.write_factor(np.array(form), pace, pace, pace, clock, GAMMA, power))
            level, carried = held_write(
                2 * step["level"] - step["before"], numerator, wall, step["remainder"]
            )
            assert (step["after"], step["remainder_after"]) == (int(level), int(carried))
            numerators.append((step["level"] / GAMMA, numerator))
        (first_u, first), (last_u, last) = numerators[0], numerators[-1]
        exponents[booking] = -math.log(last / first) / (last_u - first_u)
        assert last_u - first_u > 0.5  # the content moved: the exponent read over a span of U
    assert abs(exponents["form"] - 4.8) < 0.3 and abs(exponents["count"] - 5.8) < 0.3, exponents


def test_the_hills_weight_is_the_pairs_integer_rounded_once_at_the_read_on_either_kind():
    """T3, the hill's weight (paces.motion_weight; ALGEBRA.md, The hill's weight is the write's mix): one form at T 36,000 gives 30 at the exponent 5 and 36 at 6 exactly (Gamma divides n E_s T), at T 32,768 gives 27 (27.31 rounded half up) and 33 (32.77); two sources equal at the exponents 5 and 6 give the harmonic mix rounded, 33 at T 36,000 (32.73) at the Node where both source and the one form's 36 where the first is 0; the fallback where every source is 0 gives rounded(own E_s T, Gamma), 36 at the own exponent 6, and so does the call with no source (the one-form K of the row's key `weight: gap`); the same integers on the hardware's integers and on Python's (the array's kind kept), and no division where the sources are 0."""
    nodes, sixes = np.array([100, 200]), (36, 36)
    assert tuple(paces.motion_weight([nodes], [5], 36000, GAMMA, 6)) == (30, 30)
    assert tuple(paces.motion_weight([nodes], [6], 36000, GAMMA, 6)) == sixes
    assert tuple(paces.motion_weight([nodes], [5], 32768, GAMMA, 6)) == (27, 27)
    assert tuple(paces.motion_weight([nodes], [6], 32768, GAMMA, 6)) == (33, 33)
    mixed = [np.array([100, 0]), np.array([100, 100])]
    assert tuple(paces.motion_weight(mixed, [5, 6], 36000, GAMMA, 6)) == (33, 36)
    assert tuple(paces.motion_weight([np.array([0, 0])], [5], 36000, GAMMA, 6)) == sixes
    assert (
        paces.motion_weight([], [], 36000, GAMMA, 6) == 36
        and paces.motion_weight([], [], 36000, GAMMA, 5) == 30
    )
    exact = [np.asarray(source, dtype=object) for source in mixed]
    found = paces.motion_weight(exact, [5, 6], 36000, GAMMA, 6)
    assert tuple(found) == (33, 36) and found.dtype == np.dtype(object) and type(found[0]) is int
    assert paces.motion_weight([np.array(100), np.array(100)], [5, 6], 36000, GAMMA, 6) == 33
    assert paces.exponent_products([5, 6]) == (30, [6, 5]) and paces.exponent_products([]) == (1, [])


def test_the_premise_is_a_test_a_uniform_shift_changes_no_act_and_the_velocity_is_no_datum_of_the_seed(
    tmp_path, monkeypatch
):
    """T4, the premise as a test (ALGEBRA.md, The board's interval is no observable: a uniform level is a change of units, and so is its change from interval to interval; The mean's velocity is the content's): (a) the hill's term `paces.motion_term(now + c, before + c, K, wall)` equals `motion_term(now, before, K, wall)` bit for bit for random integer arrays and shifts, the kinetic form reading no level, and the one function returns the term with the divisor, the wall itself in the one-sided form; `paces.motion_weight` reads no level, its arguments the sources, the exponents, the wall, the clock and the own exponent alone (its signature); (b) the velocity no datum of the seed: the T2 board from rest and the same board with a uniform velocity of 10 levels per interval written by the test on gravity's time line before the first step (before = now - 10 at every Node, the test's own write on the state and no lay) both reach the constraint's residual within 10 percent of 0 by dU 0.5 (the derivation's e^(-5 dU) from either side) and agree in U at the end within 3 percent."""
    draw = np.random.default_rng(24)
    for shift in (-7, 3, 60):
        now, before = draw.integers(-60, 60, (3, 3, 3)), draw.integers(-60, 60, (3, 3, 3))
        weight = draw.integers(27, 37, (3, 3, 3))
        term, divisor = paces.motion_term(now + shift, before + shift, weight, 36000)
        plain = paces.motion_term(now, before, weight, 36000)
        assert np.array_equal(term, plain[0]) and divisor == plain[1] == 36000
        assert np.array_equal(term, -(weight * (now - before) ** 2))
    assert tuple(inspect.signature(paces.motion_weight).parameters) == (
        "sources",
        "exponents",
        "wall",
        "gamma",
        "own",
    )
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_at_weight_one(tmp_path, gravity={"booking": "form"})
    ends = []
    for name, kick in (("rest", 0), ("kicked", 10)):
        board = Lattice(load_world(laid_torus(tmp_path, name, interval="unobservable")))
        names = [family.name for family in board.families]
        g, m = names.index("gravity"), names.index("matter")
        line = board.states[g].lines[0]
        board.states[g].lines[0] = replace(
            line, before=line.before - kick
        )  # the test's own write, no lay
        course = lockstep(board, g, m, 100)
        residual = [step["eras"].residual[0] / step["eras"].residual[1] - 1 for step in course]
        start = course[0]["level"] / GAMMA
        within = [
            step["after"] / GAMMA - start
            for step, r in zip(course, residual, strict=True)
            if abs(r) < 0.1
        ]
        assert within and within[0] <= 0.5, (name, within[:1], residual[::10])
        ends.append(course[-1]["after"] / GAMMA)
    assert abs(ends[0] / ends[1] - 1) < 0.03, ends


def test_the_run_back_is_refused_by_name_under_the_key_and_the_gate_reads_refused_never_miss(
    tmp_path, monkeypatch
):
    """T5, the run back under the key (ALGEBRA.md, The inverse, the clause of 2026-10-22; Lattice.motion_back; tools/back_in_time.py): `Lattice.step_inverse` on the T2 board after one step raises by name, the message naming the hill (not injective, the reversibility hand's Theorem 2's rate c (2 v - 1) / Gamma), the stored velocity as a second carried integer against the decision of 2026-10-19 and the units' row as a board act refused by the owner's locality decision of 2026-10-22, no key for either, and the state untouched by the refusal; `tools/back_in_time.verdict` on the same world returns REFUSED with the reason and no MISS."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_at_weight_one(tmp_path, gravity={"booking": "form"})
    path = laid_torus(tmp_path, "back", interval="unobservable")
    board = Lattice(load_world(path))
    board.step()
    kept = BACK.snapshot(board)
    with pytest.raises(RuntimeError, match="not injective") as refusal:
        board.step_inverse()
    words = (
        "Theorem 2",
        "c \\(2 v - 1\\) / Gamma",
        "decision of 2026-10-19",
        "locality decision of 2026-10-22",
        "no key",
    )
    assert all(re.search(word, str(refusal.value)) for word in words) and board.interval == 1
    assert BACK.first_difference(kept, BACK.snapshot(board)) is None  # the refusal touched nothing
    verdict = BACK.verdict(Lattice(load_world(path)), 3)
    assert (
        verdict["verdict"] == "REFUSED" and "MISS" not in verdict["verdict"] and verdict["interval"] == 4
    )
    assert "not injective" in str(verdict["reason"]) and "array" not in verdict


def test_the_mixs_weight_follows_the_nodes_own_sources_as_light_dims_faster_than_matter(
    tmp_path, monkeypatch
):
    """T7, the mix's weight follows the sources (ALGEBRA.md, The hill's weight is the write's mix; board_readings.eras): a 3-cube torus at T 36,000 with the uniform matter record and a massless light plane wave along x at the wave [2, 3] (k = 2 pi / 3, the one wave the 3-cube closes), both reading gravity at 1, under the key with `booking: form`: the eras give the two families' writes per interval, both above 0, the hill's weight's least and largest between 30 and 36 at every interval (the pairs' integers 5 and 6) and never rising from one interval to the next, the largest at the end below the least at the start, as light's write dims faster than matter's (the exponent 6 against 5: the ratio of the two writes falling over every span of ten intervals, the records' rotations jittering it within a span, above 1 at the start, light's era, and below 1 at the end, matter's, the crossing the board reads; monotone pins, no number), the mix's exponent between 5 and 6 and falling (the Node-mean weight itself jitters by the roundings at the Nodes, not pinned), the tension lines along x nonzero and along y and z zero (the wave's stress on its axis alone, ALGEBRA.md, The tension), and the velocity above 0 from the first interval."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_at_weight_one(tmp_path, action=36000, gravity={"booking": "form"})
    board = Lattice(load_world(light_torus(tmp_path, "mix", 400, interval="unobservable")))
    names = [family.name for family in board.families]
    g, m, light = names.index("gravity"), names.index("matter"), names.index("light")
    assert (board.families[m].exponent(1), board.families[light].exponent(1)) == (5, 6)
    means, mixes = [], []
    for _ in range(40):
        kept = {
            i: [
                records.Record(r.now.copy(), r.before.copy(), r.remainder) for r in board.states[i].lines
            ]
            for i in (m, light)
        }
        board.step()
        forms = {(i, 0): records.form(kept[i], board.lines_of(i, 0)) for i in (m, light)}
        read = board_readings.eras(board, g, forms, board.rulers(-1))
        writes = dict(read.writes)  # the charge's record, light's own in the rule's universe, writes 0
        assert (
            writes["matter"] > 0 and writes["light"] > 0 and set(writes) == {"matter", "light", "charge"}
        )
        assert 30 <= read.weight_low <= read.weight_high <= 36 and read.level > read.before
        means.append((read.weight_low, read.weight_high, writes["light"] / writes["matter"]))
        mixes.append(read.mix[0] / read.mix[1])
    for low, high in zip(means, means[1:], strict=False):  # the weight's bounds never rise
        assert high[0] <= low[0] and high[1] <= low[1]
    for low, high in zip(means, means[10:], strict=False):  # the ratio falls over every span of ten
        assert high[2] < low[2]
    assert means[-1][1] < means[0][0] and means[0][2] > 1 > means[-1][2]  # light's era, then matter's
    assert all(5 < mix < 6 for mix in mixes) and mixes[-1] < mixes[0] - 0.05
    tensions = [int(np.abs(line.now).max()) for line in board.states[g].lines[1:4]]
    assert tensions[0] > 0 and tensions[1] == tensions[2] == 0
