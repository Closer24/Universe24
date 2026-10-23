"""The hypothesis's construction (ALGEBRA.md, The board's interval is no observable; The mean's velocity is the content's; The form's own clock; The factor carried; The stress's trace is the time line's; the hypotheses under their own names, 2026-10-22; the momentum hand's derivation M12a of the volume form, read cold by the reader; DESIGN section 3, T3 to T8), construction alone and no world of the test of the law's course: the form's own clock as one power of the write (T6), the volume form's two functions, one division and one search (T3), the premise as a test, the volume's write reading its own level both ways and the velocity no datum of the seed (T4), the run back MATCH at every interval under the key at a wall that never moves (T5), the trace as the time line's with the tension lines traceless (T7), the finding of the second smoke as a test, and the carried factor at the moving wall under the law's key and at the wall fixed per Node under the hypothesis's (T8); the declaration and the attractor stand in tests/test_the_uniform_mode.py (T1, T2 and T9), the builders in tests/laws_interval.py."""

import bisect
import json
import math
from dataclasses import dataclass, replace

import numpy as np

from event_universe import board_readings, flux, node, records, world_files
from event_universe.core import paces
from event_universe.core.rule3 import division_forward
from event_universe.features import volume
from event_universe.features.held_write import held_write
from event_universe.lattice import Lattice
from event_universe.plane import NO_FACE
from event_universe.world_files import load_world
from tests.laws import BACK, refused
from tests.laws_interval import (
    GAMMA,
    WIDTH,
    laid_torus,
    light_cube,
    light_torus,
    lockstep,
    one_number,
    uniform_world,
    universe_at_weight_one,
    volume_universe,
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


@dataclass(frozen=True)
class Row:
    """A held row's rule as the start reads it, the one flag the volume's two start functions read."""

    motion_volume: bool


def test_the_volume_of_a_level_and_the_level_of_a_volume_are_one_division_and_one_search_each_the_others_inverse():
    """T3, the volume form's two functions (features/volume `volume_of`, `level_of`, `clock_zero`, `EXPONENT`, `at_start`, `started`, `levels_read`; the momentum hand's derivation M12a read cold by the reader; the acts table: the volume one division D, the reading a search S): the exponent is d + 1 = 4; the volume of the vacuum's level 0 is Gamma itself (Gamma^5 over Gamma^4); over every level from -Gamma + 1 to 7,100 the volumes X(a) = ceil(Gamma^5 / p_0(a)^4) never fall as the level rises and, from the level 0 up, rise at exactly the levels where the clock's integer pace falls (two levels sharing one clock share one volume: the clock's own staircase, p_0 falling by less than one unit per level below Gamma, and the volume's unit coarser than the level's in a hill, X(-Gamma) = 110), and the level of a volume is the staircase's inverse bit for bit, the largest level whose volume is at most X, at every X(a), at every X(a) - 1 and at a random X between (the test's bisection on the volumes' list, the oracle), so that a level whose volume rises at the next level reads back from its own volume; the arrays come back in the shape given as Python's integers; the clock's zero at Gamma 6,000 is 56,352 (the paces' text), the clock's own power above 0 at 56,351 and 0 there, and the reading of a volume beyond every pace rests at 56,351, the clock's last pace; a volume at most 0 at a Node is refused by name, and one below the deepest hill's is refused by name; `at_start` turns every row's flag off and `started` converts a record's two levels to volumes once with its remainder kept, the line itself for a row at its level; `levels_read` passes a level array through and reads a volume array."""
    assert volume.EXPONENT == 4 and int(volume.volume_of(GAMMA, np.array(0))) == GAMMA
    levels = np.arange(-GAMMA + 1, 7101)
    volumes = volume.volume_of(GAMMA, levels)
    staircase = [int(x) for x in volumes]  # the oracle's staircase reaches 100 levels past the probes
    assert volumes.dtype == np.dtype(object) and all(
        x <= y for x, y in zip(staircase, staircase[1:], strict=False)
    )
    clocks = [paces.clock(GAMMA, int(a)) for a in levels]
    for a, x, y, p, q in zip(levels, staircase, staircase[1:], clocks, clocks[1:], strict=False):
        assert a < 0 or (x < y) == (q < p), (a, x, y, p, q)  # the volume rises where the clock falls
    draw = np.random.default_rng(12)
    probed = staircase[:-100]
    below = [x - 1 for x in probed if x > staircase[0]]
    probes = probed + below + [int(x) for x in draw.integers(staircase[0], probed[-1], 300)]
    inverse = [int(levels[bisect.bisect_right(staircase, x) - 1]) for x in probes]
    assert [int(a) for a in volume.level_of(GAMMA, np.array(probes, dtype=object))] == inverse
    rising = [a for a, x, y in zip(levels[:-100], staircase, staircase[1:], strict=False) if x < y]
    assert np.array_equal(volume.level_of(GAMMA, volume.volume_of(GAMMA, np.array(rising))), rising)
    grid = draw.integers(-500, 3000, (3, 3, 3))
    found = volume.volume_of(GAMMA, grid)
    assert found.shape == (3, 3, 3) and type(found[0, 0, 0]) is int
    assert np.array_equal(
        volume.level_of(GAMMA, found),
        [
            [[int(levels[bisect.bisect_right(staircase, int(x)) - 1]) for x in row] for row in plane]
            for plane in found
        ],
    )
    assert volume.clock_zero(GAMMA) == 56352 and paces.clock_alone(GAMMA, 56352) == 0
    assert paces.clock_alone(GAMMA, 56351) > 0 and int(volume.level_of(GAMMA, np.array(10**40))) == 56351
    refused("at most 0", volume.level_of, GAMMA, np.array([GAMMA, 0]))
    assert int(volume.volume_of(GAMMA, np.array(-GAMMA))) == 110
    refused("lies below -6000", volume.level_of, GAMMA, np.array([109]))
    assert volume.at_start((Row(True), Row(False))) == (Row(False), Row(False))
    line = records.Record(grid, grid - 7, np.full((3, 3, 3), 5))
    assert volume.started(GAMMA, Row(False), line) is line
    converted = volume.started(GAMMA, Row(True), line)
    assert np.array_equal(converted.now, found) and converted.remainder is line.remainder
    assert np.array_equal(converted.before, volume.volume_of(GAMMA, grid - 7))
    assert volume.levels_read(GAMMA, grid, False) is grid
    assert np.array_equal(volume.levels_read(GAMMA, found, True), volume.level_of(GAMMA, found))


def test_the_premise_is_a_test_the_volumes_write_reads_its_own_level_both_ways_and_the_velocity_is_no_datum_of_the_seed(
    tmp_path, monkeypatch
):
    """T4, the premise as a test (ALGEBRA.md, The board's interval is no observable: a uniform level is a change of units, and so is its change from interval to interval; The mean's velocity is the content's; records.write_sources, node.read_lines, features/volume): (a) on the T2 torus under the key the numerators from `records.write_sources` with the row's two levels given are the sources' numerators times (d + 1) X, X the level the direction starts from (now forward, before backward: the inverse reads the post-state's before, the reversibility hand's Theorem 1), over the wall Gamma E_s T, bit for bit against the same call without the levels, the axis lines' numerators and walls untouched; (b) every read of gravity's time line is the level reading: `node.read_lines` gives matter the content `volume.level_of(X)` at every Node, so the clocks and the Links' factors read a level and never the volume (the paces compose on the level); (c) the velocity no datum of the seed: the torus from rest and the same torus with a velocity of 10 levels per interval written by the test on gravity's time line before the first step (before the volume of the level 10 below now at every Node, the test's own write on the state and no lay) merge over 100 intervals: the level reading's velocity agrees within 3 levels per interval from the fortieth interval on, the level at the end within 3 percent, the board's residual `nature` rising from -1 (from -0.99 on the kicked start) at every tenth interval on both, and the reader's constraint of the volume's Lagrangian, E = 0 as X'^2 / (2 X X'') - 1 read by the test from the record's own X and its write, within 0.1 of 0 in the mean from the sixtieth interval on both and within 0.2 at every interval (the write's integer staircase, 8 or 9 units of X per interval on this torus, jitters the reading; reached from rest as -X_0 / X, the derivation's -e^(-(d + 1) U), the source's own dimming beyond e^(-4 U) keeping it a little under)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    volume_universe(tmp_path)
    board = Lattice(load_world(laid_torus(tmp_path, "premise", interval="unobservable")))
    names = [family.name for family in board.families]
    g, m = names.index("gravity"), names.index("matter")
    kept = [replace(r, now=r.now.copy(), before=r.before.copy()) for r in board.states[m].lines]
    stresses = board_readings.stresses(board)
    board.step()
    line, rulers, write = board.states[g].lines[0], board.rulers(-1), board.writes[g]
    forms = {(m, 0): records.form(kept, board.lines_of(m, 0))}
    plain = records.write_sources(g, board.families, forms, stresses, write, rulers, GAMMA)
    for direction, level in ((1, line.now), (-1, line.before)):
        motion = (line.now, line.before)
        found = records.write_sources(
            g, board.families, forms, stresses, write, rulers, GAMMA, motion, direction
        )
        expected = (
            volume.EXPONENT * np.asarray(level, dtype=object) * np.asarray(plain[0][0], dtype=object)
        )
        assert np.array_equal(np.asarray(found[0][0], dtype=object), expected)
        assert found[1][0] == GAMMA * plain[1][0] and found[1][1:] == plain[1][1:]
        assert all(np.array_equal(a, b) for a, b in zip(found[0][1:], plain[0][1:], strict=True))
    content, _axes = node.read_lines(m, board.families, board.states, 1, GAMMA)
    assert np.array_equal(np.asarray(content, dtype=object), volume.level_of(GAMMA, line.now))
    courses = {}
    for name, kick in (("rest", 0), ("kicked", 10)):
        board = Lattice(load_world(laid_torus(tmp_path, name, interval="unobservable")))
        line = board.states[g].lines[0]
        before = volume.volume_of(GAMMA, volume.level_of(GAMMA, line.now) - kick)
        board.states[g].lines[0] = replace(line, before=before)  # the test's own write, no lay
        course = lockstep(board, g, m, 100)
        residual = [step["eras"].nature[0] / step["eras"].nature[1] - 1 for step in course]
        assert -1 <= residual[0] < -0.98 + kick / 100 and residual[0] > -1 - kick  # the kick's velocity
        assert all(b > a for a, b in zip(residual[::10], residual[10::10], strict=False)), name
        volumes = [course[0]["level"]] + [step["after"] for step in course]
        speed = [b - a for a, b in zip(volumes, volumes[1:], strict=False)]
        force = [b - a for a, b in zip(speed, speed[1:], strict=False)]
        energy = [
            v * v / (2 * x * f) - 1 for x, v, f in zip(volumes[1:], speed[1:], force, strict=False)
        ]
        late = energy[60:]  # the force's integer staircase, 8 or 9 units of X, jitters each reading
        assert abs(sum(late) / len(late)) < 0.1 and all(abs(e) < 0.2 for e in late), (name, late[::10])
        courses[name] = [step["eras"].level for step in course]
    rest, kicked = courses["rest"], courses["kicked"]
    velocities = [(b - a, d - c) for a, b, c, d in zip(rest, rest[1:], kicked, kicked[1:], strict=False)]
    assert all(abs(v - w) <= 3 for v, w in velocities[40:]) and kicked[0] > rest[0]
    assert abs(rest[-1] / kicked[-1] - 1) < 0.03, (rest[-1], kicked[-1])


def test_the_run_back_under_the_key_matches_at_every_interval_at_a_wall_that_never_moves(
    tmp_path, monkeypatch
):
    """T5, the run back under the key (ALGEBRA.md, The inverse; the reversibility hand's Theorem 1; features/volume; Lattice.fixed_walls; tools/back_in_time.py): every numerator and wall of the volume's write is a function of the post-state at a wall that never moves (Gamma E_s T under `factor: rounded`; Gamma E_s T times the Node's factor wall at the rest's paces under `factor: carried`), and Rule3's own line on X keeps its double root, so `Lattice.step_inverse` returns every level and remainder bit for bit at every interval: the gate's verdict is MATCH over 30 intervals on the T2 torus under either factor, over 16 on the light cube (the three waves, a non-uniform board whose paces differ from Node to Node, where the symmetric hill's run back missed and the carried factor's moving wall folds) under either factor, and over 16 on the torus kicked as T4 kicks it (the velocity in the record); the verdict names the intervals, the first interval 1 and no end, and nothing unreturning (the hill's names gone from the gate). The run back MATCH 200 of 200 on the second run's world is the test by name in the eras' log of the run (docs/ENGINE.md section 10, item 17)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    for factor in ("rounded", "carried"):
        volume_universe(tmp_path, factor)
        torus = laid_torus(tmp_path, f"torus_{factor}", interval="unobservable")
        cube = light_cube(tmp_path, f"cube_{factor}", 400, interval="unobservable")
        for path, intervals in ((torus, 30), (cube, 16)):
            verdict = BACK.verdict(Lattice(load_world(path)), intervals)
            expected = {"verdict": "MATCH", "intervals": intervals, "interval": 1, "ended": None}
            assert verdict == expected, (path.name, verdict)
    board = Lattice(load_world(torus))
    g = [family.name for family in board.families].index("gravity")
    line = board.states[g].lines[0]
    before = volume.volume_of(GAMMA, volume.level_of(GAMMA, line.now) - 10)
    board.states[g].lines[0] = replace(
        line, before=before
    )  # the kicked torus, the velocity in the record
    assert BACK.verdict(board, 16)["verdict"] == "MATCH"


def test_the_stresss_trace_is_the_time_lines_and_the_tension_lines_take_the_traceless_parts(
    tmp_path, monkeypatch
):
    """T7, the trace's test (ALGEBRA.md, The stress's trace is the time line's, a hypothesis under its own name, 2026-10-22; the pressure hand's derivation and the reader's build line; loader/universe.pressure_of, records.pressure_term, records.write_sources): on the 3-cube torus at T 36,000 and the width 92 with the uniform matter record and one light plane wave along x at the wave [2, 3], gravity declaring `booking: form` and `pressure: trace` under the hypothesis's key with the factor rounded and under the law's key with the factor carried, over 20 intervals (a) the three tension lines' numerators from `records.write_sources` sum to 0 at every Node exactly under the carry (the traceless parts 3 T_aa - SUM_b T_bb over the trace's three, no rounding of their own) and within the sources' two roundings under the rounding; (b) the time line's numerator is the write weight times the forms' scaled sum less the pressure term at the carried wall's scale, bit for bit (`records.scaled_sum`, `records.pressure_term`, the trace over three of each source's stress parts in the energy's units, one rounding per source per Node), under the key times (d + 1) X at the wall Gamma E_s T where the row's levels are given (the volume's write); (c) under the key the row carries its volume at the trace's exponent 4 and under the law's key the level itself; (d) the sum of the three tension lines' mean velocities over the board stays within 2 levels per interval of 0 (the isotropic part drained: the x line at two thirds of its stress, the y and z lines at minus a third each, the shear's double root the law keeps), while under the law's `pressure: tension` on the same lay it grows past 10 levels per interval by the twentieth interval (the x line's mean accelerated by the wave's stress, the finding of the smoke). The declaration: `pressure` at a word other than `tension` or `trace`, `trace` on the holder of the sign and `trace` at a quantum action Gamma does not divide four times are refused by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    growth = {}
    cases = (
        ("trace", "rounded", "interval"),
        ("trace", "carried", "uniform"),
        ("tension", "rounded", "uniform"),
    )
    for pressure, factor, law in cases:
        keys = {"booking": "form", "pressure": pressure, "factor": factor}
        universe_at_weight_one(tmp_path, 36000, WIDTH, gravity=keys)
        world = {law: "unobservable" if law == "interval" else "carried"}
        board = Lattice(load_world(light_torus(tmp_path, f"{pressure}_{factor}", 400, **world)))
        names = [family.name for family in board.families]
        g, m, light = names.index("gravity"), names.index("matter"), names.index("light")
        gravity, means = board.families[g], []
        assert gravity.pressure_trace == (pressure == "trace") and gravity.factor_carried == (
            factor == "carried"
        )
        assert gravity.motion_volume == (law == "interval") and volume.EXPONENT == 4
        for _ in range(20):
            kept = {
                i: [replace(r, now=r.now.copy(), before=r.before.copy()) for r in board.states[i].lines]
                for i in (m, light)
            }
            stresses = board_readings.stresses(board)
            board.step()
            rulers, write = board.rulers(-1), board.writes[g]
            forms = {(i, 0): records.form(kept[i], board.lines_of(i, 0)) for i in (m, light)}
            numerators, walls, _terms = records.write_sources(
                g, board.families, forms, stresses, write, rulers, GAMMA
            )
            axes = sum(np.asarray(numerators[1 + a], dtype=object) for a in range(3))
            if pressure == "trace":
                assert int(np.abs(axes).max()) <= (0 if factor == "carried" else 2)
                sources = {s: forms.get(s, 0) for s in records.row_sources(board.families, g, 0)}
                energy, scale, _ = records.scaled_sum(
                    g, board.families, sources, rulers, GAMMA, 1, factor == "carried"
                )
                pressed = records.pressure_term(
                    g, board.families, stresses, rulers, GAMMA, gravity.power
                )
                time = np.asarray(gravity.write * (energy - pressed * scale), dtype=object)
                assert np.array_equal(np.asarray(numerators[0], dtype=object), time)
                assert int(np.asarray(pressed).sum()) > 0
                if gravity.motion_volume:
                    line = board.states[g].lines[0]
                    moved = records.write_sources(
                        g, board.families, forms, stresses, write, rulers, GAMMA, (line.now, line.before)
                    )
                    volumes = volume.EXPONENT * np.asarray(line.now, dtype=object) * time
                    assert np.array_equal(np.asarray(moved[0][0], dtype=object), volumes)
                    assert moved[1][0] == GAMMA * walls[0] == GAMMA * 36000
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
    """The finding of the second smoke as a test (ALGEBRA.md, The stress's trace is the time line's; The closed lattice has no rest, read for the axis lines; the reader's build line of 2026-10-22): on the 3-cube torus at T 36,000 and the width 92 with the uniform matter record and three light plane waves alike, one along each axis at the wave [2, 3] (`light_cube`, the isotropic lay of the test of the law's course), gravity's three tension lines are massless held lines whose k = 0 mode is Rule3's double root, so under the law's key with `pressure: tension` the waves' positive mean stress, a write of about one level per interval into each line's mean, accumulates as a velocity of the mean that nothing drains: each tension line's mean velocity grows past 10 levels per interval by the twentieth interval, the three alike, toward the Links' freezing at Gamma (the smoke's 5,905 at the sixtieth interval of the test world); under the hypothesis's key with `pressure: trace` and the carried factor at the wall fixed per Node, the trace goes to the time line and the traceless parts of an isotropic lay are 0 in the mean, so each line's mean velocity stays within one level per interval of 0 over the 20 intervals and the means within 10 levels of 0 (the k > 0 ringing and the carry's drift), the three lines' means alike at every interval (the cube's symmetry: the lines are each other's images under the axes' permutation) and their sum at every Node within 8 levels of 0 (the step's split, flux.step_traceless, and the traceless write: the isotropic part moved by the remainders' carries alone). The guard's lower side (features/read.link_tensions; the fourth smoke of 2026-10-22, the Links' factors and the writes negative past Gamma with no refusal): the x tension line written past Gamma by the test on the board, the next step is refused by name at the read, the message naming the tension, the factor and the pace below 0 and the guard's lower side."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    courses = {}
    for pressure in ("tension", "trace"):
        keys = {"booking": "form", "pressure": pressure, "factor": "carried"}
        universe_at_weight_one(tmp_path, 36000, WIDTH, gravity=keys)
        world = {"interval": "unobservable"} if pressure == "trace" else {"uniform": "carried"}
        board = Lattice(load_world(light_cube(tmp_path, f"cube_{pressure}", 400, **world)))
        names = [family.name for family in board.families]
        g, means = names.index("gravity"), []
        for _ in range(20):
            board.step()
            lines = board.states[g].lines
            sums = [int(np.asarray(lines[1 + a].now, dtype=object).sum()) for a in range(3)]
            assert sums[0] == sums[1] == sums[2]  # the cube's symmetry: the three lines' means alike
            means.append(sums[0] / 27)
            total = sum(np.asarray(lines[1 + a].now, dtype=object) for a in range(3))
            assert (
                pressure == "tension" or int(np.abs(total).max()) <= 8
            )  # the three lines' sum per Node
        courses[pressure] = [b - a for a, b in zip(means[:-1], means[1:], strict=True)], means
    velocities, means = courses["trace"]
    assert all(abs(v) <= 1 for v in velocities) and all(abs(level) <= 10 for level in means)
    velocities, means = courses["tension"]
    assert (
        velocities[-1] > 10
        and all(b >= a for a, b in zip(velocities[2:], velocities[3:], strict=False))
        and means[-1] > 100
    )
    line = board.states[g].lines[
        1
    ]  # the x tension line driven past Gamma by the test's own write, no lay
    board.states[g].lines[1] = replace(line, now=line.now + 2 * GAMMA)
    board.step()  # the horizon (ALGEBRA.md, The horizon, 2026-10-23): the Link at the wall is read at the wall, its factor 0, and the run goes on where the former reading refused it by name ("exceeds Gamma", the guard's lower side)
    assert any(int(np.asarray(f).min()) == 0 for f in board.read(board.order[0])[1])


def test_the_carried_factor_is_the_one_division_at_the_wall_per_node_and_the_rounding_stays_bit_for_bit(
    tmp_path, monkeypatch
):
    """T8, the end's booking switch (DESIGN 0 (iii); ALGEBRA.md, The write per proper volume and per proper interval, the clause of 2026-10-22; loader/universe.factor_of, loader/derived.shared_clock, paces.write_factor_terms, records.write_sources, records.walls_at, node.held_write_at, Lattice.fixed_walls): (a) `paces.write_factor_terms` returns a product and a wall, Gamma^power p_0^(3 - power), whose quotient rounded half up is `write_factor`'s value bit for bit at every Node of a random state at both powers; (b) on the T2 torus at T 36,000 under the law's key with gravity declaring `booking: form` and `factor: carried` the write's wall at every Node is E_s T Gamma p_0^2 at the rest's clock, kept for the run (`Lattice.fixed_walls`, the carried factor's one form under either key: a wall moving with the clock folds the run back and is no form), the write remainders born at its half (`records.walls_at`, `records.write_origins`), one remainder per held line stands below its wall at every Node in the wall's kind (Python's integers under the carry, the axis lines' walls beyond the hardware's width), the lines keep the lattice's kind, and over 40 intervals each interval's level after the write is bit for bit the Rule3-stepped level plus (rounded(k_w w D p^3 W, E_s T Gamma p_0^2) + r) div W with W the fixed wall and p, p_0 the interval's own paces (the ratio of the walls inside the numerator, rounded once) and the engine's own remainder (the lockstep board's paces p_i on every axis, the tensions 0); (c) the carried board's level stays within 6 levels of the rounded board's over the 40 intervals (the carry below one level per Node); (d) `factor` at a word other than `rounded` or `carried` is refused by name, and `factor: carried` on a row whose sources read the content at differing weights is refused by name with the readers; (e) under the law's key with `factor: carried` the run back MATCHES over 20 intervals (the reversibility hand's Theorem 1: the wall fixed, the numerator from the paces of the interval's start, read from the post-state's before); (f) under the hypothesis's key the carried factor divides at the wall fixed per Node for the run (the Boss's decision of 2026-10-22 on the text hand's model): on the torus with gravity's time line set by the test to the volume of the level Gamma (U = 1) and a source of form 5 at every Node, the rounded factor's write is 0 (5 e^(-4) below one half, 0 for ever under the rounding), the fixed wall's numerator is the carried product times the rest's wall over the interval's wall rounded once, above 0, at the wall kept from the start, and the held write at that wall over 20,000 intervals with the numerator held gives the quotients' sum (n N + r_0) div W exactly, from 1 up: the fraction carried, the write alive."""
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
        board = Lattice(load_world(laid_torus(tmp_path, f"end_{factor}", uniform="carried")))
        names = [family.name for family in board.families]
        g, m = names.index("gravity"), names.index("matter")
        wall, kind = board.walls(g)[0], board.states[g].lines[0].now.dtype
        assert board.families[g].factor_carried == (factor == "carried") and wall == 36000
        fixed = one_number(board.fixed_walls[g][0]) if factor == "carried" else wall
        assert fixed == wall * (GAMMA * paces.clock(GAMMA, 60) ** 2 if factor == "carried" else 1)
        assert one_number(board.states[g].write_remainders[0]) == fixed // 2  # born at the half wall
        course = lockstep(board, g, m, 40)
        for step in course:
            form = step["now"] * step["now"] - step["next"] * step["before_record"]
            clock, pace = paces.node_paces(GAMMA, step["level"])
            booked = (
                int(paces.rounded(form * pace**3 * fixed, wall * GAMMA * clock * clock))
                if factor == "carried"
                else int(paces.write_factor(np.array(form), pace, pace, pace, clock, GAMMA, 1))
            )
            numerator, divisor = booked + step["remainder"], fixed
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
    assert verdict == {"verdict": "MATCH", "intervals": 20, "interval": 1, "ended": None}
    volume_universe(tmp_path, "carried")
    board = Lattice(load_world(laid_torus(tmp_path, "deep", interval="unobservable")))
    names = [family.name for family in board.families]
    g, m = names.index("gravity"), names.index("matter")
    deep = volume.volume_of(GAMMA, np.full(board.shape, GAMMA, dtype=object))
    board.states[g].lines[0] = replace(board.states[g].lines[0], now=deep, before=deep)
    rulers, write, fixed = board.rulers(1), board.writes[g], board.fixed_walls[g]
    small = {(m, 0): np.full(board.shape, 5, dtype=object)}
    clock, pace = paces.node_paces(GAMMA, GAMMA)
    assert int(paces.write_factor(np.array(5), pace, pace, pace, clock, GAMMA, 1)) == 0  # dead
    found = records.write_sources(g, board.families, small, {}, write, rulers, GAMMA, None, 1, fixed)
    held = one_number(fixed[0])
    numerator = int(paces.rounded(5 * pace**3 * held, 36000 * GAMMA * clock * clock))
    assert one_number(found[0][0]) == numerator > 0 and found[1][0] is fixed[0]
    assert held == 36000 * GAMMA * paces.clock(GAMMA, 60) ** 2
    level, remainder, quotients = one_number(deep), held // 2, 0
    for _ in range(20000):
        after, remainder = held_write(
            level, volume.EXPONENT * level * numerator, GAMMA * held, remainder
        )
        quotients, level = quotients + int(after) - level, int(after)
    assert (
        quotients
        == (20000 * volume.EXPONENT * one_number(deep) * numerator + held // 2) // (GAMMA * held)
        >= 1
    )


def test_the_tension_lines_step_as_the_shears_momentum_at_the_volumes_wall_and_run_back_exactly(
    tmp_path, monkeypatch
):
    """The shear's momentum (flux.step_momentum, shear.stepped, shear.written, shear.born; ALGEBRA.md, The shear's momentum is carried at the volume's wall, a proposal of 2026-10-23 from the cube's group of 48, the symmetry hand's derivation read cold by the reader): on the light torus (one wave along x, the paces differing along x), (a) the three tension lines are born with their remainder at half the volume's wall, 3 w X_0, Python's integers; (b) one interval of the board gives each tension line the one carried division on the traceless part of its own Links' sum with the wall 3 w (X_now + X_next), the velocity carried in at 3 w (X_before + X_now) and the Links' term at 2 X_now, X the time line's volume before, at and after the interval (after its step and its write), the step's remainder bit for bit against the hand's arithmetic; (c) where the three volumes are one the act is the law's step `flux.step_traceless` bit for bit with the remainder 2 X times the law's; (d) the act is a bijection whose inverse is the same function at -1 with the remainders complemented at the wall they enter, on 40 random Node-intervals with the volumes growing and shrinking; (e) the board's step back returns the start bit for bit after one interval and after 60 (the time line's inverse before the tension lines'); (f) over 120 intervals the three lines' sum at every Node keeps the carries' pin (within 3 levels per interval, the means within 12 of 0) while the x line's mean, which the law as written drove past 1,000 by the wave's stress along x, stays below 1,000: the anisotropic k = 0 mode drained."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_at_weight_one(tmp_path, 36000, WIDTH)
    board = Lattice(load_world(light_torus(tmp_path, "split", 400)))
    g = [family.name for family in board.families].index("gravity")
    lines, wall3, faces = board.states[g].lines, 6 * board.half_wall(g), [NO_FACE] * 3
    big, half = np.asarray, 3 * board.half_wall(g)
    volume = big(lines[0].now, dtype=object)
    assert all(
        np.array_equal(big(lines[1 + a].remainder, dtype=object), wall3 * volume) for a in range(3)
    )
    begun, start = [list(s.lines) for s in board.states], BACK.snapshot(board)
    content, factors = node.read(g, board.families, board.states, 1, board.wrap, GAMMA, board.unit)
    rule = node.rule_of(board.families[g], GAMMA, content, factors, board.unit)
    board.step()
    after, own = board.states[g].lines, begun[g][1:4]
    fluxes = [big(flux.link_fluxes(line.now, rule.reaches, board.wrap, 0), dtype=object) for line in own]
    entered = wall3 * (volume + big(after[0].now, dtype=object))
    born = wall3 * (volume + big(begun[g][0].before, dtype=object))
    for a, line in enumerate(own):
        now, before = big(line.now, dtype=object), big(line.before, dtype=object)
        numerator = entered * now + born * (now - before) + division_forward(entered - born, 2, 0)[0]
        numerator = numerator + 2 * volume * (3 * fluxes[a] - sum(fluxes) - 3 * rule.mass * now)
        carried = division_forward(numerator, entered, line.remainder)[1]
        assert np.array_equal(big(after[1 + a].remainder, dtype=object), carried)
        assert np.array_equal(after[1 + a].before, line.now)
    law = [replace(line, remainder=np.full(line.now.shape, half)) for line in own]
    scaled = [replace(line, remainder=2 * volume * big(line.remainder, dtype=object)) for line in law]
    one = flux.step_momentum(scaled, rule, board.wrap, 1, faces, (begun[g][0].now,) * 3)
    for was, same in zip(flux.step_traceless(law, rule, board.wrap, 1, faces), one, strict=True):
        assert np.array_equal(was.now, same.now)
        assert np.array_equal(2 * volume * big(was.remainder, dtype=object), same.remainder)
    draw, shape = np.random.default_rng(17), own[0].now.shape
    for _ in range(40):
        x = [big(draw.integers(6000, 10**6, size=shape), dtype=object) for _ in range(3)]
        carry = division_forward(wall3 * (x[0] + x[1]), 10**9, 0)[0]
        carry = big(draw.integers(0, 10**9, size=shape), dtype=object) * carry
        levels = [draw.integers(-(10**5), 10**5, size=shape) for _ in range(6)]
        trial = [records.Record(levels[2 * a], levels[2 * a + 1], carry) for a in range(3)]
        forward = flux.step_momentum(trial, rule, board.wrap, 1, faces, (x[0], x[1], x[2]))
        back = flux.step_momentum(forward, rule, board.wrap, -1, faces, (x[2], x[1], x[0]))
        for was, now in zip(trial, back, strict=True):
            assert np.array_equal(was.now, now.now) and np.array_equal(was.before, now.before)
            assert np.array_equal(big(was.remainder, dtype=object), now.remainder)
    board.step_inverse()
    assert BACK.first_difference(start, BACK.snapshot(board)) is None
    any(board.step() for _ in range(60))
    any(board.step_inverse() for _ in range(60))
    assert BACK.first_difference(start, BACK.snapshot(board)) is None
    sums, speeds = [], []
    for _ in range(120):
        board.step()
        lines = board.states[g].lines
        total = sum(big(lines[1 + a].now, dtype=object) for a in range(3))
        before = sum(big(lines[1 + a].before, dtype=object) for a in range(3))
        speeds.append(int(np.abs(total - before).max()))
        sums.append(float(total.sum()) / 27)
    assert max(speeds) <= 3 and max(abs(s) for s in sums) <= 12, (max(speeds), sums[::12])
    assert abs(float(big(lines[1].now, dtype=object).sum()) / 27) < 1000
