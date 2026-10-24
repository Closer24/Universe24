"""The volume form's construction under the law of one Node (ALGEBRA.md, The board's interval is no observable; The mean's velocity is the content's; The form's own clock; The factor carried; The stress's trace is the time line's; the hypotheses under their own names, 2026-10-22; the momentum hand's derivation M12a of the volume form, read cold by the reader; DESIGN section 3, T3 to T8), construction alone and no world of the test of the law's course: the form's own clock as one power of the write (T6), the volume form's two functions, one division and one search (T3), the premise as a test, the volume's write reading its own level both ways and the velocity no datum of the seed (T4), the run back MATCH at every interval at a wall that never moves (T5), the trace as the time line's with the tension lines traceless (T7), the finding of the second smoke as a test, and the carried factor at the wall fixed per Node (T8); the declaration and the attractor stand in tests/test_the_uniform_mode.py (T1, T2 and T9), the builders in tests/laws_interval.py."""

import bisect
import json
import math
from dataclasses import dataclass, replace

import numpy as np
import pytest

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
    """T6, the form's own clock (ALGEBRA.md, The write per proper volume and per proper interval, The form's own clock; loader/derived.FamilyRule.power and exponent, records.write_sources): under the law of one Node every count source is booked once, so the holder of the content's booking power is 1 and its exponent in the board's interval 3 + 1 + 2, a reader's own exponent 3 + 1 + 1 (`exponent`); on the 3-cube torus with the uniform matter record over 100 intervals in lockstep the write's factor at every interval is `paces.write_factor` at the power 1 scaled to the wall fixed per Node, and the time line's increment is the volume's write ((d + 1) X c + r) div (Gamma times the fixed wall) by `held_write`, bit for bit; the factor read against the level U = a / Gamma falls as e^(-4.8 U) within 0.3 over a span of U above 0.5 (the form's own clock: the count's two proper-interval powers less one). Uniform by nature: this test's claim is the k = 0 line's, the one write's arithmetic on a level uniform over the board, so its board is uniform (the owner's rule of 2026-10-23: the tests of the law's course run on a structured board; the uniform board stands here as the null case of that one line)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    volume_universe(tmp_path)
    board = Lattice(load_world(laid_torus(tmp_path, "clock")))
    names = [family.name for family in board.families]
    gravity, matter = board.families[names.index("gravity")], board.families[names.index("matter")]
    assert (gravity.power, gravity.exponent(), matter.exponent(1)) == (1, 3 + 1 + 2, 3 + 1 + 1)
    assert (
        not gravity.wronskian and matter.exponent() == 3 + 1 + 1
    )  # every count source booked once: a reader's own power 1
    g, m = names.index("gravity"), names.index("matter")
    wall, fixed, numerators = board.walls(g)[0], one_number(board.fixed_walls[g][0]), []
    for step in lockstep(board, g, m, 100):
        form = step["now"] * step["now"] - step["next"] * step["before_record"]
        a = int(volume.level_of(GAMMA, np.array(step["level"])))
        clock, pace = paces.node_paces(GAMMA, a)  # matter reads gravity at 1, the level reading
        numerator = int(paces.write_factor(np.array(form), pace, pace, pace, clock, GAMMA, 1))
        scaled = int(paces.rounded(form * pace**3 * fixed, wall * GAMMA * clock * clock))
        level, carried = held_write(
            2 * step["level"] - step["before"],
            volume.EXPONENT * step["level"] * scaled,
            GAMMA * fixed,
            step["remainder"],
        )
        assert (step["after"], step["remainder_after"]) == (int(level), int(carried))
        numerators.append((a / GAMMA, numerator))
    (first_u, first), (last_u, last) = numerators[0], numerators[-1]
    assert last_u - first_u > 0.5  # the content moved: the exponent read over a span of U
    exponent = -math.log(last / first) / (last_u - first_u)
    assert abs(exponent - 4.8) < 0.3, exponent


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
    """T4, the premise as a test (ALGEBRA.md, The board's interval is no observable: a uniform level is a change of units, and so is its change from interval to interval; The mean's velocity is the content's; records.write_sources, node.read_lines, features/volume): (a) on the T2 torus the numerators from `records.write_sources` with the row's motion given are the volume's, (d + 1) X_now times the plain numerator forward and (d + 1) X_before times it backward, the time line's wall Gamma times the plain wall per Node (the carried factor's, 36,000 times the scale at the Node's paces) and the axis lines' walls and numerators unchanged, and the content a reader reads is the level reading of the volume; (b) the torus from rest and the same torus kicked by the test's own write of the level before (10 levels), both over 100 intervals in lockstep: the nature residual starts at -1 (the kick's velocity above it) and rises in both, the energy identity v^2 / (2 X X'') holds within 0.2 after the sixtieth interval, the two courses' velocities agree within 3 levels per interval after the fortieth and the levels within 3 percent at the end: the velocity is the content's and no datum of the seed. Uniform by nature: this test's claim is the k = 0 line's, the one write's arithmetic on a level uniform over the board, so its board is uniform (the owner's rule of 2026-10-23: the tests of the law's course run on a structured board; the uniform board stands here as the null case of that one line)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    volume_universe(tmp_path)
    board = Lattice(load_world(laid_torus(tmp_path, "premise")))
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
        assert np.array_equal(found[1][0], GAMMA * plain[1][0])  # the wall per Node, Gamma times
        assert all(np.array_equal(a, b) for a, b in zip(found[1][1:], plain[1][1:], strict=True))
        assert all(np.array_equal(a, b) for a, b in zip(found[0][1:], plain[0][1:], strict=True))
    content, _axes = node.read_lines(m, board.families, board.states, 1, GAMMA)
    assert np.array_equal(np.asarray(content, dtype=object), volume.level_of(GAMMA, line.now))
    courses = {}
    for name, kick in (("rest", 0), ("kicked", 10)):
        board = Lattice(load_world(laid_torus(tmp_path, name)))
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


def test_the_run_back_matches_at_every_interval_at_a_wall_that_never_moves(tmp_path, monkeypatch):
    """T5, the run back (ALGEBRA.md, The inverse; the reversibility hand's Theorem 1; features/volume; Lattice.fixed_walls; tools/back_in_time.py): every numerator and wall of the volume's write is a function of the post-state at a wall that never moves, Gamma E_s T times the Node's fixed wall at the rest's paces, so the run back MATCHES at every interval: the T2 torus over 30 intervals and the light cube (three waves alike on the torus) over 16, both by the gate's own verdict; the torus kicked by the test's own write of the level before (10 levels) over 16. Uniform by nature: this test's claim is the k = 0 line's, the one write's arithmetic on a level uniform over the board, so its board is uniform (the owner's rule of 2026-10-23: the tests of the law's course run on a structured board; the uniform board stands here as the null case of that one line)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    volume_universe(tmp_path)
    torus = laid_torus(tmp_path, "torus")
    cube = light_cube(tmp_path, "cube", 400)
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
    """T7, the trace's test (ALGEBRA.md, The stress's trace is the time line's, 2026-10-22; the pressure hand's derivation and the reader's build line; records.pressure_term, records.write_sources; the law of one Node: the trace on every holder of the content, no key): on the 3-cube torus at T 36,000 and the width 92 with the uniform matter record and one light plane wave along x, twenty intervals: at every interval the three tension lines' numerators from `records.write_sources` sum to 0 exactly at every Node (the traceless parts inside the carried factor's one rounding), the time line's numerator is the row's write times the sources' energy less the pressure term scaled to the carried wall (`pressure_term` above 0, the light's stress), and with the row's motion given the volume's write (d + 1) X_now times it over Gamma times the wall per Node, a multiple of 36,000; the tension lines' means move by at most 2 levels per interval over the run (no isotropic stress stretches the rulers)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    volume_universe(tmp_path)
    board = Lattice(load_world(light_torus(tmp_path, "trace", 400)))
    names = [family.name for family in board.families]
    g, m, light = names.index("gravity"), names.index("matter"), names.index("light")
    gravity, means = board.families[g], []
    assert gravity.held and not gravity.wronskian and gravity.motion_volume
    assert volume.EXPONENT == 4
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
        assert int(np.abs(axes).max()) == 0
        sources = {s: forms.get(s, 0) for s in records.row_sources(board.families, g, 0)}
        energy, scale, _ = records.scaled_sum(g, board.families, sources, rulers, GAMMA, 1)
        pressed = records.pressure_term(g, board.families, stresses, rulers, GAMMA, gravity.power)
        time = np.asarray(gravity.write * (energy - pressed * scale), dtype=object)
        assert np.array_equal(np.asarray(numerators[0], dtype=object), time)
        assert int(np.asarray(pressed).sum()) > 0
        line = board.states[g].lines[0]
        moved = records.write_sources(
            g, board.families, forms, stresses, write, rulers, GAMMA, (line.now, line.before)
        )
        volumes = volume.EXPONENT * np.asarray(line.now, dtype=object) * time
        assert np.array_equal(np.asarray(moved[0][0], dtype=object), volumes)
        assert np.array_equal(moved[1][0], GAMMA * walls[0])  # Gamma times the wall per Node
        assert int(np.asarray(walls[0]).min()) >= 36000 and (np.asarray(walls[0]) % 36000 == 0).all()
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
    assert all(abs(sum(v)) <= 2 for v in velocities)


def test_an_isotropic_lays_tension_lines_stay_flat_under_the_trace(tmp_path, monkeypatch):
    """The finding of the second smoke as a test (ALGEBRA.md, The stress's trace is the time line's; The closed lattice has no rest, read for the axis lines; the reader's build line of 2026-10-22): on the 3-cube torus at T 36,000 and the width 92 with the uniform matter record and three light plane waves alike, one along each axis (the isotropic lay, its stress's trace the pressure), twenty intervals: the three tension lines' means are alike at every interval by the cube's symmetry, their sum per Node within 8 levels, the means within 10 levels and their velocities within 1 level per interval (the trace in the time line, the traceless parts 0 for an isotropic stress: no stretch of the rulers); and the guard by name: the x tension line driven past Gamma by the test's own write refuses the step naming the guard's lower side."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    volume_universe(tmp_path)
    board = Lattice(load_world(light_cube(tmp_path, "cube", 400)))
    names = [family.name for family in board.families]
    g, means = names.index("gravity"), []
    for _ in range(20):
        board.step()
        lines = board.states[g].lines
        sums = [int(np.asarray(lines[1 + a].now, dtype=object).sum()) for a in range(3)]
        assert sums[0] == sums[1] == sums[2]  # the cube's symmetry: the three lines' means alike
        means.append(sums[0] / 27)
        total = sum(np.asarray(lines[1 + a].now, dtype=object) for a in range(3))
        assert int(np.abs(total).max()) <= 8  # the three lines' sum per Node
    velocities = [b - a for a, b in zip(means[:-1], means[1:], strict=True)]
    assert all(abs(v) <= 1 for v in velocities) and all(abs(level) <= 10 for level in means)
    line = board.states[g].lines[
        1
    ]  # the x tension line driven past Gamma by the test's own write, no lay
    board.states[g].lines[1] = replace(line, now=line.now + 2 * GAMMA)
    board.step()  # the horizon (ALGEBRA.md, The horizon, 2026-10-23): the Link at the wall is read at the wall, its factor 0, and the run goes on where the former reading refused it by name ("exceeds Gamma", the guard's lower side)
    assert any(int(np.asarray(f).min()) == 0 for f in board.read(board.order[0])[1])


def test_the_carried_factor_is_the_one_division_at_the_wall_per_node_and_the_rounding_stays_bit_for_bit(
    tmp_path, monkeypatch
):
    """T8, the carried factor (ALGEBRA.md, The write per proper volume and per proper interval, the clause of 2026-10-22; loader/derived.shared_clock, paces.write_factor_terms, records.write_sources, records.walls_at, node.held_write_at, Lattice.fixed_walls; the law of one Node: every held row's write at the carried factor, no key): (a) `paces.write_factor_terms` gives the product and the wall whose one rounding is `paces.write_factor`, the wall Gamma^power p_0^(3 - power); (b) on the 3-cube torus with the uniform matter record the wall fixed per Node is E_s T Gamma p_0(60)^2 (the rest's paces), the write remainder born at its half, and over 40 intervals in lockstep the time line's increment is the one division of (d + 1) X times the form scaled to the fixed wall plus the carried remainder by Gamma times the fixed wall, the remainder below the divisor, one write remainder per line; (c) the shared clock's gate: a second reader of gravity at another weight is refused by name; (d) the run back MATCH over 20 intervals; (e) the deep well: a form of 5 at the content Gamma, 0 under the rounded factor's one rounding (dead), writes a positive numerator at the fixed wall and over 20,000 writes the quotients sum to the one division of the carried total (no write below half a level is lost for ever). Uniform by nature: this test's claim is the k = 0 line's, the one write's arithmetic on a level uniform over the board, so its board is uniform (the owner's rule of 2026-10-23: the tests of the law's course run on a structured board; the uniform board stands here as the null case of that one line)."""
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
    volume_universe(tmp_path)
    board = Lattice(load_world(laid_torus(tmp_path, "end")))
    names = [family.name for family in board.families]
    g, m = names.index("gravity"), names.index("matter")
    wall = board.walls(g)[0]
    assert g in board.fixed_walls and wall == 36000
    fixed = one_number(board.fixed_walls[g][0])
    assert fixed == wall * GAMMA * paces.clock(GAMMA, 60) ** 2
    assert one_number(board.states[g].write_remainders[0]) == fixed // 2  # born at the half wall
    for step in lockstep(board, g, m, 40):
        form = step["now"] * step["now"] - step["next"] * step["before_record"]
        a = int(volume.level_of(GAMMA, np.array(step["level"])))
        clock, pace = paces.node_paces(GAMMA, a)
        booked = int(paces.rounded(form * pace**3 * fixed, wall * GAMMA * clock * clock))
        numerator, divisor = volume.EXPONENT * step["level"] * booked + step["remainder"], GAMMA * fixed
        assert step["after"] == 2 * step["level"] - step["before"] + numerator // divisor
        assert step["remainder_after"] == numerator - divisor * (numerator // divisor) < divisor
    assert len(board.states[g].write_remainders) == len(board.states[g].lines)
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    universe["families"].append(
        {"name": "light", "pair": [6000, 6000], "reads": {"gravity": 2}, "dimension": 1}
    )
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    apart = refused(
        "the read weight is one for every reader", load_world, uniform_world(tmp_path, "apart")
    )
    assert (
        "light" in str(apart) and "gravity" in str(apart)
    )  # the loader refuses the weight 2 itself (2026-10-24); the shared clock's refusal of differing weights ("differing weights", "shared clock") stood until then, kept by name in derived.shared_clock
    volume_universe(tmp_path)
    verdict = BACK.verdict(Lattice(load_world(laid_torus(tmp_path, "law"))), 20)
    assert verdict == {"verdict": "MATCH", "intervals": 20, "interval": 1, "ended": None}
    board = Lattice(load_world(laid_torus(tmp_path, "deep")))
    deep = volume.volume_of(GAMMA, np.full(board.shape, GAMMA, dtype=object))
    board.states[g].lines[0] = replace(board.states[g].lines[0], now=deep, before=deep)
    rulers, write, fixed_walls = board.rulers(1), board.writes[g], board.fixed_walls[g]
    small = {(m, 0): np.full(board.shape, 5, dtype=object)}
    clock, pace = paces.node_paces(GAMMA, GAMMA)
    assert int(paces.write_factor(np.array(5), pace, pace, pace, clock, GAMMA, 1)) == 0  # dead
    found = records.write_sources(
        g, board.families, small, {}, write, rulers, GAMMA, None, 1, fixed_walls
    )
    held = one_number(fixed_walls[0])
    numerator = int(paces.rounded(5 * pace**3 * held, 36000 * GAMMA * clock * clock))
    assert one_number(found[0][0]) == numerator > 0 and np.array_equal(found[1][0], fixed_walls[0])
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


def test_the_singular_point_x_at_0_has_no_reading_no_clock_and_no_node():  # type: ignore[no-untyped-def]
    """ALGEBRA.md, the singular point (approved by the owner on 2026-10-23): X = 0 is the singular point of the law's domain, where the volume carries no level, the clock no pace and the Node nothing to read; the volume's reading refuses it by name at X = 0 and below (features/volume `level_of`, "at most 0"), while the vacuum's volume X(0) reads the level 0 and the deepest volumes above 0 read their levels; the time line's fall to it is the crunch the test of the law's course ends on (tests/test_universe24_runs_its_cycle.py)."""
    gamma = 6000  # the rule's Gamma
    for x in (0, -1, -1513):
        with pytest.raises(ValueError, match="at most 0"):
            volume.level_of(gamma, np.array([x], dtype=object))
    vacuum = int(np.asarray(volume.volume_of(gamma, np.array([0], dtype=object))).reshape(-1)[0])
    assert int(np.asarray(volume.level_of(gamma, np.array([vacuum], dtype=object))).reshape(-1)[0]) == 0
    with pytest.raises(
        ValueError, match="below"
    ):  # the volume 1, the last above the singular point, reads a level below -Gamma, refused by name too
        volume.level_of(gamma, np.array([1], dtype=object))
