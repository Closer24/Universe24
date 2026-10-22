"""The hypothesis's construction (ALGEBRA.md, The board's interval is no observable; The mean's velocity is the content's; The motion of gravity's row is a hill at the symmetry's weight; The hill's weight is the write's mix; The form's own clock; The factor carried; the hypotheses under their own names, 2026-10-22; DESIGN section 3, T3 to T8), construction alone and no world of the experiment: the form's own clock as one power of the write (T6), the hill's weight's integer and its rounding (T3), the premise as a test (T4), the run back refused by name under the key (T5), the mix's weight following the Node's own sources (T7) and the end's booking switch (T8); the declaration and the attractor stand in tests/test_the_uniform_mode.py (T1, T2 and T9), the builders in tests/laws_interval.py."""

import inspect
import json
import math
from dataclasses import replace

import numpy as np
import pytest

from event_universe import board_readings, records, world_files
from event_universe.core import paces
from event_universe.features.held_write import held_write
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import BACK, refused
from tests.laws_interval import (
    GAMMA,
    laid_torus,
    light_cube,
    light_torus,
    lockstep,
    uniform_world,
    universe_at_weight_one,
)


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
    """T3, the hill's weight (paces.motion_weight; ALGEBRA.md, The hill's weight is the write's mix): one form at T 36,000 gives 30 at the exponent 5 and 36 at 6 exactly (Gamma divides n E_s T), and 24 at the trace's d + 1 = 4 (The stress's trace is the time line's, one K for every mix), at T 32,768 gives 27 (27.31 rounded half up) and 33 (32.77); two sources equal at the exponents 5 and 6 give the harmonic mix rounded, 33 at T 36,000 (32.73) at the Node where both source and the one form's 36 where the first is 0; the fallback where every source is 0 gives rounded(own E_s T, Gamma), 36 at the own exponent 6, and so does the call with no source (the one-form K of the row's key `weight: gap`); the same integers on the hardware's integers and on Python's (the array's kind kept), and no division where the sources are 0."""
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
    assert paces.motion_weight([], [], 36000, GAMMA, 4) == 24  # the trace's one K, (d + 1) E_s T / Gamma


def test_the_premise_is_a_test_a_uniform_shift_changes_no_act_and_the_velocity_is_no_datum_of_the_seed(
    tmp_path, monkeypatch
):
    """T4, the premise as a test (ALGEBRA.md, The board's interval is no observable: a uniform level is a change of units, and so is its change from interval to interval; The mean's velocity is the content's): (a) the hill's term `paces.motion_term(now + c, before + c, K, wall)` equals `motion_term(now, before, K, wall)` bit for bit for random integer arrays and shifts, the kinetic form reading no level, and the one function returns the term with the divisor, the wall plus K (now - before) forward and less it backward, the symmetric hill's, the same under the shift; `paces.motion_weight` reads no level, its arguments the sources, the exponents, the wall, the clock and the own exponent alone (its signature); (b) the velocity no datum of the seed: the T2 board from rest and the same board with a uniform velocity of 10 levels per interval written by the test on gravity's time line before the first step (before = now - 10 at every Node, the test's own write on the state and no lay) both reach the constraint's residual within 10 percent of 0 by dU 0.5 (the derivation's e^(-5 dU) from either side) and agree in U at the end within 3 percent."""
    draw = np.random.default_rng(24)
    for shift in (-7, 3, 60):
        now, before = draw.integers(-60, 60, (3, 3, 3)), draw.integers(-60, 60, (3, 3, 3))
        weight = draw.integers(27, 37, (3, 3, 3))
        term, divisor = paces.motion_term(now + shift, before + shift, weight, 36000)
        plain = paces.motion_term(now, before, weight, 36000)
        assert np.array_equal(term, plain[0]) and np.array_equal(divisor, plain[1])
        assert np.array_equal(term, -(weight * (now - before) ** 2))
        assert np.array_equal(divisor, 36000 + weight * (now - before))
        back = paces.motion_term(now + shift, before + shift, weight, 36000, -1)
        assert np.array_equal(back[0], term) and np.array_equal(back[1], 36000 - weight * (now - before))
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
    """T5, the run back under the key (ALGEBRA.md, The inverse, the clause of 2026-10-22; Lattice.motion_back; the symmetric hill's derivation M11j, 1.2 and 1.3; tools/back_in_time.py): on the T2 board stepped 100 intervals the forward act names the intervals whose run back fails (`Lattice.unreturning`, `paces.motion_returns`), and the names are the engine's own numbers read back: an interval is named iff at some Node the carry in r lay at or above the backward wall E_s T - K v_out, v_out = a(t + 1) - a(t) the row's velocity after the interval (the lockstep board, one number at every Node), and the names are not empty (the rate 2 c H per Node per interval at the start's velocities); the run back from the top is exact bit for bit at every interval down to the first named one, the same function at -1 (the snapshot of each interval's start recovered, levels and remainders of every family), and there `Lattice.step_inverse` raises by name, the message naming the interval, the backward wall, the Jacobian theorem and its rate, the reversibility hand's Theorem 2, the stored velocity against the decision of 2026-10-19 and the units' row as a board act refused by the owner's locality decision of 2026-10-22, no key for either, and touching nothing; `BACK.verdict` on the same world over 100 intervals reads REFUSED at that interval with the reason, the intervals named and the count matched above it, never MISS."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_at_weight_one(tmp_path, gravity={"booking": "form"})
    path = laid_torus(tmp_path, "back", interval="unobservable")
    board = Lattice(load_world(path))
    names = [family.name for family in board.families]
    g, m = names.index("gravity"), names.index("matter")
    wall, kept = board.walls(g)[0], [BACK.snapshot(board)]
    course = lockstep(board, g, m, 100)
    kept += [step["snapshot"] for step in course]
    folded = {
        t + 1
        for t, step in enumerate(course)
        if step["remainder"] >= wall - step["eras"].weight_low * (step["after"] - step["level"])
    }
    assert folded and board.unreturning == folded and max(folded) <= 100
    first = max(folded)
    while board.interval > first:
        board.step_inverse()
        assert BACK.first_difference(kept[board.interval], BACK.snapshot(board)) is None
    before = BACK.snapshot(board)
    with pytest.raises(RuntimeError, match="not injective") as refusal:
        board.step_inverse()
    words = (
        f"interval {first} ",
        "backward wall W - K v_out",
        "Jacobian theorem",
        "2 c H",
        "Theorem 2",
        "decision of 2026-10-19",
        "locality decision of 2026-10-22",
        "no key",
    )
    assert all(word in str(refusal.value) for word in words) and board.interval == first
    assert BACK.first_difference(before, BACK.snapshot(board)) is None  # the refusal touched nothing
    verdict = BACK.verdict(Lattice(load_world(path)), 99)
    assert verdict["verdict"] == "REFUSED" and verdict["interval"] == first and "array" not in verdict
    assert "not injective" in str(verdict["reason"]) and verdict["unreturning"] == sorted(folded)
    assert verdict["matched"] == 100 - first  # every interval above the first named one ran back exact


def test_the_stresss_trace_is_the_time_lines_and_the_tension_lines_take_the_traceless_parts(
    tmp_path, monkeypatch
):
    """T7, the trace's test (ALGEBRA.md, The stress's trace is the time line's, a hypothesis under its own name, 2026-10-22; the pressure hand's derivation and the reader's build line; loader/universe.pressure_of, records.pressure_term, records.write_sources, records.hill_weight): on the 3-cube torus at T 36,000 with the uniform matter record and one light plane wave along x at the wave [2, 3], gravity declaring `booking: form` and `pressure: trace` with the factor rounded and carried in turn, over 20 intervals (a) the three tension lines' numerators from `records.write_sources` sum to 0 at every Node exactly under the carry (the traceless parts 3 T_aa - SUM_b T_bb over the trace's three, no rounding of their own) and within the sources' two roundings under the rounding; (b) the time line's numerator is the write weight times the forms' scaled sum less the pressure term at the carried wall's scale, bit for bit (`records.scaled_sum`, `records.pressure_term`, the trace over three of each source's stress parts in the energy's units, one rounding per source per Node); (c) the hill's weight is 24 at every Node, the trace's one integer (d + 1) E_s T / Gamma, read by `board_readings.eras`; (d) the sum of the three tension lines' mean velocities over the board stays within 2 levels per interval of 0 (the isotropic part drained: the x line at two thirds of its stress, the y and z lines at minus a third each, the shear's double root the law keeps), while under the law's `pressure: tension` on the same lay it grows past 10 levels per interval by the twentieth interval (the x line's mean accelerated by the wave's stress, the finding of the smoke) with the mix's weights 30 to 36 as the law has them. The declaration: `pressure` at a word other than `tension` or `trace`, `trace` on the holder of the sign and `trace` at a quantum action Gamma does not divide four times are refused by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    growth = {}
    for pressure, factor in (("trace", "rounded"), ("trace", "carried"), ("tension", "rounded")):
        keys = {"booking": "form", "pressure": pressure, "factor": factor}
        universe_at_weight_one(tmp_path, action=36000, gravity=keys)
        board = Lattice(
            load_world(light_torus(tmp_path, f"{pressure}_{factor}", 400, interval="unobservable"))
        )
        names = [family.name for family in board.families]
        g, m, light = names.index("gravity"), names.index("matter"), names.index("light")
        gravity, means = board.families[g], []
        assert gravity.pressure_trace == (pressure == "trace") and gravity.factor_carried == (
            factor == "carried"
        )
        for _ in range(20):
            kept = {
                i: [replace(r, now=r.now.copy(), before=r.before.copy()) for r in board.states[i].lines]
                for i in (m, light)
            }
            stresses = board_readings.stresses(board)
            board.step()
            rulers, forms = board.rulers(-1), {}
            forms = {(i, 0): records.form(kept[i], board.lines_of(i, 0)) for i in (m, light)}
            numerators, _walls, _weight = records.write_sources(
                g, board.families, forms, stresses, board.writes[g], rulers, GAMMA, None, 1
            )
            axes = sum(np.asarray(numerators[1 + a], dtype=object) for a in range(3))
            read = board_readings.eras(board, g, forms, rulers)
            if pressure == "trace":
                assert int(np.abs(axes).max()) <= (0 if factor == "carried" else 2)
                sources = {s: forms.get(s, 0) for s in records.row_sources(board.families, g, 0)}
                energy, scale, _ = records.scaled_sum(
                    g, board.families, sources, rulers, GAMMA, 1, factor == "carried"
                )
                pressed = records.pressure_term(
                    g, board.families, stresses, rulers, GAMMA, gravity.power
                )
                assert np.array_equal(
                    np.asarray(numerators[0], dtype=object),
                    np.asarray(gravity.write * (energy - pressed * scale), dtype=object),
                )
                assert read.weight_low == read.weight_high == 24 and int(np.asarray(pressed).sum()) > 0
            else:
                assert 30 <= read.weight_low <= read.weight_high <= 36
            means.append(
                [
                    float(np.asarray(board.states[g].lines[1 + a].now, dtype=object).sum()) / 27
                    for a in range(3)
                ]
            )
        velocities = [
            [b - a for a, b in zip(early, late, strict=True)]
            for early, late in zip(means[:-1], means[1:], strict=True)
        ]
        growth[(pressure, factor)] = [sum(v) for v in velocities]
    assert all(abs(v) <= 2 for key in (("trace", "rounded"), ("trace", "carried")) for v in growth[key])
    assert (
        growth[("tension", "rounded")][-1] > 10
        and growth[("tension", "rounded")][-1] > growth[("tension", "rounded")][5]
    )
    universe_at_weight_one(tmp_path, action=36000, gravity={"pressure": "mix"})
    worded = refused(
        "held.pressure is one of", load_world, uniform_world(tmp_path, "pword", interval="unobservable")
    )
    assert "'mix'" in str(worded) and "'tension', 'trace'" in str(worded)
    universe_at_weight_one(tmp_path, action=36000, charge={"pressure": "trace"})
    signed = refused(
        "carries no tension line", load_world, uniform_world(tmp_path, "psign", interval="unobservable")
    )
    assert "The stress's trace" in str(signed)
    universe_at_weight_one(
        tmp_path, gravity={"pressure": "trace"}
    )  # T 32,768: Gamma does not divide 4 E_s T
    walled = refused(
        "does not divide", load_world, uniform_world(tmp_path, "pwall", interval="unobservable")
    )
    assert "131072" in str(walled) and "(d + 1) E_s T" in str(walled)


def test_an_isotropic_lays_tension_lines_stay_flat_under_the_trace_and_run_away_without_it(
    tmp_path, monkeypatch
):
    """The finding of the second smoke as a test (ALGEBRA.md, The stress's trace is the time line's; The closed lattice has no rest, read for the axis lines; the reader's build line of 2026-10-22): on the 3-cube torus at T 36,000 with the uniform matter record and three light plane waves alike, one along each axis at the wave [2, 3] (`light_cube`, the experiment's isotropic lay), gravity's three tension lines are massless held lines whose k = 0 mode is Rule3's double root, so under the law's `pressure: tension` the waves' positive mean stress, a write of about one level per interval into each line's mean, accumulates as a VELOCITY of the mean that nothing drains: each tension line's mean velocity grows past 10 levels per interval by the twentieth interval, the three alike, toward the Links' freezing at Gamma (the smoke's 5,905 at the sixtieth interval of the test world); under `pressure: trace` the trace goes to the time line and the traceless parts of an isotropic lay are 0 in the mean, so each line's mean velocity stays within one level per interval of 0 over the 20 intervals and the means within 10 levels of 0 (the k > 0 ringing and the carry's drift), the three lines' means alike at every interval (the cube's symmetry: the lines are each other's images under the axes' permutation), the hill's weight 24."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    courses = {}
    for pressure in ("tension", "trace"):
        keys = {"booking": "form", "pressure": pressure, "factor": "carried"}
        universe_at_weight_one(tmp_path, action=36000, gravity=keys)
        board = Lattice(
            load_world(light_cube(tmp_path, f"cube_{pressure}", 400, interval="unobservable"))
        )
        names = [family.name for family in board.families]
        g, m, light = names.index("gravity"), names.index("matter"), names.index("light")
        means = []
        for _ in range(20):
            kept = {
                i: [replace(r, now=r.now.copy(), before=r.before.copy()) for r in board.states[i].lines]
                for i in (m, light)
            }
            board.step()
            forms = {(i, 0): records.form(kept[i], board.lines_of(i, 0)) for i in (m, light)}
            read = board_readings.eras(board, g, forms, board.rulers(-1))
            assert (read.weight_low, read.weight_high) == (
                (24, 24) if pressure == "trace" else (read.weight_low, read.weight_high)
            )
            sums = [
                int(np.asarray(board.states[g].lines[1 + a].now, dtype=object).sum()) for a in range(3)
            ]
            assert sums[0] == sums[1] == sums[2]  # the cube's symmetry: the three lines' means alike
            means.append(sums[0] / 27)
        courses[pressure] = [b - a for a, b in zip(means[:-1], means[1:], strict=True)], means
    velocities, means = courses["trace"]
    assert all(abs(v) <= 1 for v in velocities) and all(abs(level) <= 10 for level in means)
    velocities, means = courses["tension"]
    assert (
        velocities[-1] > 10
        and all(b >= a for a, b in zip(velocities[2:], velocities[3:], strict=False))
        and means[-1] > 100
    )


def test_the_carried_factor_is_the_one_division_at_the_wall_per_node_and_the_rounding_stays_bit_for_bit(
    tmp_path, monkeypatch
):
    """T8, the end's booking switch (DESIGN 0 (iii); ALGEBRA.md, The write per proper volume and per proper interval, the clause of 2026-10-22; loader/universe.factor_of, loader/derived.shared_clock, paces.write_factor_terms, records.write_sources, node.held_write_at): (a) `paces.write_factor_terms` returns a product and a wall, Gamma^power p_0^(3 - power), whose quotient rounded half up is `write_factor`'s value bit for bit at every Node of a random state at both powers; (b) on the T2 torus at T 36,000 with gravity declaring `booking: form` and `factor: carried` the write's wall at every Node is E_s T Gamma p_0^2 at the record's clock, one remainder per held line stands as before and below its wall at every Node in the wall's kind (Python's integers under the carry, the axis lines' walls beyond the hardware's width), the lines keep the lattice's kind, and over 40 intervals each interval's level after the write is bit for bit the Rule3-stepped level plus (k_w w D p^3 - K v^2 Gamma p_0^2 + r) div (E_s T Gamma p_0^2 + K v Gamma p_0^2) with the engine's own remainder and K the rounding's 30 (the symmetric hill and its weight at the carried wall's scale; the lockstep board's paces p_i on every axis, the tensions 0); (c) the carried board's level stays within 6 levels of the rounded board's over the 40 intervals (the carry below one level per Node; its fraction changes meaning as the wall moves with the clock, 5 levels measured by the interval 40); (d) `factor` at a word other than `rounded` or `carried` is refused by name, and `factor: carried` on a row whose sources read the content at differing weights is refused by name with the readers; (e) under the law's key `uniform: carried` with `factor: carried` and no hill the run back MATCHES over 20 intervals (the reversibility hand's Theorem 1: the wall and the numerator from the paces of the interval's start, read from the post-state's before)."""
    draw = np.random.default_rng(8)
    for power in (1, 2):
        count, clock = draw.integers(-(10**7), 10**7, (3, 3, 3)), draw.integers(3000, 6001, (3, 3, 3))
        p = [draw.integers(3000, 6000, (3, 3, 3)) for _ in range(3)]
        product, wall = paces.write_factor_terms(count, p[0], p[1], p[2], clock, GAMMA, power)
        assert np.array_equal(
            np.asarray(paces.rounded(product, wall)).astype(np.int64),
            paces.write_factor(count, p[0], p[1], p[2], clock, GAMMA, power),
        )
        assert np.array_equal(wall, GAMMA**power * np.asarray(clock, dtype=object) ** (3 - power))
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    levels = {}
    for factor in ("carried", "rounded"):
        universe_at_weight_one(tmp_path, action=36000, gravity={"booking": "form", "factor": factor})
        board = Lattice(load_world(laid_torus(tmp_path, f"end_{factor}", interval="unobservable")))
        names = [family.name for family in board.families]
        g, m = names.index("gravity"), names.index("matter")
        wall, kind = board.walls(g)[0], board.states[g].lines[0].now.dtype
        assert board.families[g].factor_carried == (factor == "carried") and wall == 36000
        course = lockstep(board, g, m, 40)
        for step in course:
            form = step["now"] * step["now"] - step["next"] * step["before_record"]
            clock, pace = paces.node_paces(GAMMA, step["level"])
            scale = GAMMA * clock * clock if factor == "carried" else 1
            booked = (
                form * pace**3
                if factor == "carried"
                else int(paces.write_factor(np.array(form), pace, pace, pace, clock, GAMMA, 1))
            )
            velocity = step["level"] - step["before"]
            numerator = booked - 30 * scale * velocity * velocity + step["remainder"]
            divisor = wall * scale + 30 * scale * velocity
            assert step["eras"].weight_low == step["eras"].weight_high == 30
            assert step["after"] == 2 * step["level"] - step["before"] + numerator // divisor
            assert step["remainder_after"] == numerator - divisor * (numerator // divisor) < divisor
        assert len(board.states[g].write_remainders) == len(board.states[g].lines)
        assert board.states[g].lines[0].now.dtype == kind  # the lines keep the lattice's kind
        assert (board.states[g].write_remainders[0].dtype == kind) == (factor == "rounded")  # the wall's
        levels[factor] = [step["after"] for step in course]
    assert max(abs(c - r) for c, r in zip(levels["carried"], levels["rounded"], strict=True)) <= 6
    universe_at_weight_one(tmp_path, gravity={"factor": "exact"})
    worded = refused(
        "held.factor is one of", load_world, uniform_world(tmp_path, "word", interval="unobservable")
    )
    assert "'exact'" in str(worded) and "'rounded', 'carried'" in str(worded)
    universe_at_weight_one(tmp_path, gravity={"factor": "carried"})
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    universe["families"].append(
        {"name": "light", "pair": [6000, 6000], "reads": {"gravity": 2}, "dimension": 1}
    )
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    apart = refused(
        "differing weights", load_world, uniform_world(tmp_path, "apart", interval="unobservable")
    )
    assert "'gravity'" in str(apart) and "light" in str(apart) and "shared clock" in str(apart)
    universe_at_weight_one(tmp_path, action=36000, gravity={"booking": "form", "factor": "carried"})
    verdict = BACK.verdict(Lattice(load_world(laid_torus(tmp_path, "law", uniform="carried"))), 20)
    assert verdict["verdict"] == "MATCH" and verdict["intervals"] == 20 and verdict["unreturning"] == []
