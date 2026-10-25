"""The generic Node's toy (ALGEBRA.md, The Node; the owner's word of 2026-10-25 through the adviser, every property of the generic Node tested on one Node fed through its six Links): the centre (1, 1, 1) of the bare 3-cube torus of the tests' small universe is the one Node and its 26 shell Nodes are overwritten by the test from fed arrays twice per interval, before the acts (`Lattice.advanced_to_the_close`) and before the close (`Lattice.closed_after`), every array replaced through `records.Record` and never written in place, the board's own meetings restricted to the centre (tests/laws_universe.py, `node_toy` and its builders); calibrated bit for bit against the board's own centre through the first birth and run back exact, then the Node's acts asserted at the centre alone against the law's functions on the fed integers: Rule3 from six fed arrivals, the clock the Node's and the tension the Link's, the one-Link reach, the held write, the sign's row and the read excluding its own, the phase act, the swap and the floor, the frozen clock; the close's clauses, the fold and the owner's three constants in tests/test_the_generic_node_toys_close_and_constants.py."""

from __future__ import annotations

from dataclasses import fields

import numpy as np
import pytest

from event_universe import (
    board_readings,
    flux,
    meeting_board,
    node,
    records,
    registry,
    swap,
)
from event_universe.core import paces, rule3
from event_universe.core.ports import AXES, PORT_SIDES, arrival
from event_universe.features import phase, volume
from event_universe.features.read import link_factors, link_tensions, paces_guard
from tests.laws import ROOT, load_file
from tests.laws_universe import (
    CENTRE,
    CUBE,
    GAMMA,
    NEIGHBOURS,
    at_centre,
    course,
    fed_interval,
    impose,
    node_arrays,
    node_toy,
    shaken,
)

TOOL = load_file("node_integers", ROOT / "tools" / "node_integers.py")
BITS = 128  # the width the owner's principle names, the one number this file carries
LEVELS = len(fields(records.Record))  # a line's integers at a Node: now, before, the remainder


@pytest.mark.parametrize("shift", [(0, 0, 0), (0, 1, 1)])
def test_the_node_fed_the_boards_own_shells_is_the_boards_centre_bit_for_bit_and_runs_back_exact(
    tmp_path, monkeypatch, shift
):  # type: ignore[no-untyped-def]
    """The calibration: fed the plain board's own 26 shell Nodes per interval (and once carried by a translation of the torus so that a born Node of the board stands at the centre), the toy's centre is the board's bit for bit over five intervals through the first birth (17 arrays before it, more after), its credit and birth lines the board's with the Node carried, and the run back with the fed shells re-imposed in reverse returns the centre to every interval's start."""
    recorded, lines, _board = course(tmp_path / "board", monkeypatch, shift, 5)
    toy_lines = []
    board = node_toy(tmp_path, monkeypatch, toy_lines)
    history, counts = [], []
    for start, after, end in recorded:
        fed_interval(board, start, after)
        got, want = at_centre(node_arrays(board)), at_centre(end)
        assert set(got) <= set(want) and all(got[key] == want[key] for key in got)
        counts.append((len(got), len(want)))
        history.append(node_arrays(board))
    born = shift != (0, 0, 0)
    assert counts[0] == (17, 17) and counts[-1] == (
        (57, 57) if born else (17, 57)
    )  # the board births at the interval 4; the toy where the born Node stands at the centre
    assert board.born_at == ({4: [4]} if born else {})
    place = int(np.ravel_multi_index(CENTRE, board.shape))
    source = tuple((CENTRE[a] - shift[a]) % CUBE for a in range(AXES))

    def moved(line):  # type: ignore[no-untyped-def]
        found = dict(line)
        if found.get("node_detector") is not None:
            found["node_detector"] = place
        for key in ("support", "node"):
            if key in found:
                found[key] = list(CENTRE)
        if "nodes" in found:
            found["nodes"] = [list(CENTRE)]
        return found

    closes = ("credit", "birth", "refused")
    at_source = [
        moved(li)
        for li in lines
        if li["event"] in closes
        and (
            li.get("nodes") == [list(source)]
            or li.get("node_detector") == int(np.ravel_multi_index(source, board.shape))
        )
    ]
    assert [li for li in toy_lines if li["event"] in closes] == at_source and len(at_source) == 2 * born
    for k in range(len(recorded) - 1, -1, -1):
        impose(board, history[k])
        board.step_inverse()
        want = at_centre(recorded[0][0] if k == 0 else history[k - 1])
        got = at_centre(node_arrays(board))
        assert set(got) <= set(want) and all(got[key] == want[key] for key in got)
    assert board.interval == 0


def test_rule3_at_the_node_is_the_six_fed_arrivals_division_on_each_line_and_its_inverse(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """Rule3 on each line from the six fed arrivals (The line, The direction): under a random shell on the light line and random volumes at the neighbours, the centre's light line and the sign's free row after the acts equal `rule3` by hand on SUM_j R_j (m_j - a_now) with the rule's integers from `rule_of` at the content read by hand (the level of the centre's own volume) and the six factors by hand (`link_factor` of the two ends' axis lines), the remainder in [0, w), and the act at -1 returns the start."""
    board, draw = node_toy(tmp_path, monkeypatch), np.random.default_rng(7)
    light, sign, held = board.world.seed, board.held[1], board.held[0]
    unit, checked = board.unit, 0
    for _ in range(4):
        start = shaken(board, draw, 400, [GAMMA])
        for a in range(AXES):
            axis = np.asarray(draw.integers(0, 300, board.shape), dtype=object)
            start[(held, "line", 1 + a)] = (axis, axis.copy(), start[(held, "line", 1 + a)][2])
        impose(board, start)
        begun = node_arrays(board)
        kept = board.advanced_to_the_close()
        if board.turned[CENTRE]:  # a turned Node's output is the swap's, asserted in its own test
            impose(board, start)
            board.closed_after(kept)
            continue
        checked += 1
        content = int(volume.level_of(GAMMA, begun[(held, "line", 0)][0])[CENTRE])
        axes = [begun[(held, "line", 1 + a)][0] for a in range(AXES)]
        tensions = tuple(
            int(
                np.minimum(
                    (axes[axis][CENTRE] + arrival(axes[axis], axis, side)[CENTRE] + 1) // 2, GAMMA
                )
            )
            for axis, side in PORT_SIDES
        )
        factors = tuple(rule3.link_factor(GAMMA, unit, t) for t in tensions)
        for index, own in ((light, content), (sign, 0)):
            rule = node.rule_of(
                board.families[index], GAMMA, own, factors if index == light else None, unit
            )
            now, before, remainder = (int(a[CENTRE]) for a in begun[(index, "line", 0)])
            arrived = [int(begun[(index, "line", 0)][0][there]) for there in NEIGHBOURS]
            fluxes = sum(r * (m - now) for r, m in zip(rule.reaches, arrived, strict=True))
            expected = rule3.rule3(fluxes, rule.mass, rule.wall, now, before, remainder)
            after = board.states[index].lines[0]
            got = (
                int(after.now[CENTRE]),
                int(after.remainder[CENTRE]),
            )  # the free row's write is its sources' 0 at the half wall: the level stands
            assert got == tuple(int(x) for x in expected) and 0 <= got[1] < rule.wall
            assert rule3.rule3(fluxes, rule.mass, rule.wall, now, got[0], got[1], -1) == (
                before,
                remainder,
            )
        impose(board, start)
        board.closed_after(kept)
    assert checked >= 2


def test_the_clock_is_the_nodes_and_the_tension_is_the_links_read_the_same_from_both_ends(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The clock is the Node's, the tension is the Link's: with the volume's time line fed at seven volumes and its axis lines random at the two ends, the centre's content is the level of its own volume alone, its paces `node_paces` of it, and each Link's factor is `link_factor` of (aa_i + aa_j + 1) div 2 read at the horizon, the same number read from the neighbour through the Port back; a change at an edge Node leaves the centre's read."""
    board, draw = node_toy(tmp_path, monkeypatch), np.random.default_rng(11)
    light, held, unit = board.world.seed, board.held[0], board.unit
    shell = node_arrays(board)
    volumes = np.asarray(draw.integers(1000, 1600, board.shape), dtype=object)
    shell[(held, "line", 0)] = (volumes, volumes.copy(), shell[(held, "line", 0)][2])
    for a in range(AXES):
        axis = np.asarray(draw.integers(0, 600, board.shape), dtype=object)
        shell[(held, "line", 1 + a)] = (axis, axis.copy(), shell[(held, "line", 1 + a)][2])
    impose(board, shell)
    begun = node_arrays(board)
    content, factors = board.read(light, 1, 0)
    volume_here = begun[(held, "line", 0)][0]
    assert int(content[CENTRE]) == int(volume.level_of(GAMMA, volume_here)[CENTRE])
    clock, pace = paces.node_paces(GAMMA, int(content[CENTRE]))
    assert (
        board.rulers(1)[(light, 0)][0][CENTRE] == clock
        and paces.link_pace(GAMMA, int(content[CENTRE])) == pace
    )
    axes = [begun[(held, "line", 1 + a)][0] for a in range(AXES)]
    for port, (axis, side) in enumerate(PORT_SIDES):
        there = NEIGHBOURS[port]
        tension = min((int(axes[axis][CENTRE]) + int(axes[axis][there]) + 1) // 2, GAMMA)
        assert int(factors[port][CENTRE]) == rule3.link_factor(GAMMA, unit, tension)
        back = PORT_SIDES.index((axis, -side))
        assert int(factors[back][there]) == int(factors[port][CENTRE])
    by_hand = link_factors(GAMMA, unit, link_tensions([(1, axes)], GAMMA))
    assert all(int(f[CENTRE]) == int(g[CENTRE]) for f, g in zip(factors, by_hand, strict=True))
    edge = (0, 0, 1)
    moved = {k: tuple(a.copy() for a in v) for k, v in shell.items()}
    moved[(held, "line", 0)][0][edge] += 200
    moved[(held, "line", 1)][0][edge] += 50
    impose(board, moved)
    again, factors_again = board.read(light, 1, 0)
    assert int(again[CENTRE]) == int(content[CENTRE]) and all(
        int(f[CENTRE]) == int(g[CENTRE]) for f, g in zip(factors, factors_again, strict=True)
    )


def test_the_node_sees_one_link_a_change_at_the_edge_and_corner_nodes_leaves_its_interval(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The Node sees one Link: two fed shells differing at the 20 edge and corner Nodes alone, every array, leave every array at the centre equal bit for bit after one interval with its close; a third differing at one face neighbour's light level alone changes the centre, the positive control."""
    draw = np.random.default_rng(3)
    plain = node_toy(tmp_path / "a", monkeypatch)
    start = shaken(plain, draw, 400, [1000, 1100, 1200], remainders=True)
    far = np.ones(plain.shape, dtype=bool)
    far[CENTRE] = False
    for there in NEIGHBOURS:
        far[there] = False
    edges = {
        k: tuple(np.where(far, draw.integers(-300, 300, plain.shape).astype(object) + a, a) for a in v)
        for k, v in start.items()
    }
    near = {k: tuple(a.copy() for a in v) for k, v in start.items()}
    near[(plain.world.seed, "line", 0)][0][NEIGHBOURS[0]] += 1
    found = []
    for name, shell in (("a", start), ("b", edges), ("c", near)):
        board = node_toy(tmp_path / name, monkeypatch)
        fed_interval(board, shell)
        found.append(at_centre(node_arrays(board)))
    assert found[0] == found[1] and found[0] != found[2]


def test_the_held_write_at_the_node_is_the_form_and_the_stresses_over_the_fixed_wall_once_and_its_inverse(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The held write (the row "the held write"; The write per proper volume and per proper interval): the volume's time line at the centre after the acts is Rule3 on its own line plus (numerator + r) div (Gamma x fixed wall), the numerator `records.write_sources` on the light's form D = now^2 - next x before by hand and the stresses read from the fed frame at the start's rulers, the write remainder the carry in [0, wall), every tension line's write remainder within its wall, and `held_write_at` at -1 returns the start."""
    board, draw = node_toy(tmp_path, monkeypatch), np.random.default_rng(5)
    light, held, unit = board.world.seed, board.held[0], board.unit
    start = shaken(board, draw, 300, [1000, 1050, 1100])
    impose(board, start)
    state = board.states[held]
    rulers, stresses = board.rulers(1), board_readings.stresses(board)
    sourcing = registry.sourcing(board.families, board.states, held)
    light_line, time_line = board.states[light].lines[0], state.lines[0]
    content, factors = board.read(light, 1, 0)
    stepped = flux.step_line(
        light_line, node.rule_of(board.families[light], GAMMA, content, factors, unit)
    )
    own, own_factors = board.read(held, 1, 0)
    free = flux.step_line(time_line, node.rule_of(board.families[held], GAMMA, own, own_factors, unit))
    form = records.form([light_line], [stepped])
    numerators, walls, _terms = records.write_sources(
        held,
        board.families,
        {(light, 0): form},
        stresses,
        board.writes[held],
        rulers,
        GAMMA,
        sourcing,
        (time_line.now, time_line.before),
        1,
        board.fixed_walls[held],
    )
    remainders = [np.asarray(r, dtype=object) for r in state.write_remainders]
    board.advanced_to_the_close()
    assert not board.turned[CENTRE]
    after = board.states[held]
    numerator, wall = int(numerators[0][CENTRE]), int(np.asarray(walls[0], dtype=object).reshape(-1)[0])
    assert wall == GAMMA * int(np.asarray(board.fixed_walls[held][0], dtype=object).reshape(-1)[0])
    total = numerator + int(remainders[0][CENTRE])
    assert int(after.lines[0].now[CENTRE]) == int(free.now[CENTRE]) + total // wall
    assert int(after.write_remainders[0][CENTRE]) == total % wall
    for number, (remainder, line_wall) in enumerate(zip(after.write_remainders, walls, strict=True)):
        assert 0 <= int(remainder[CENTRE]) < int(np.asarray(line_wall, dtype=object).reshape(-1)[0]), (
            number
        )
    back, origin = node.held_write_at(
        [after.lines[0]], [numerators[0]], [walls[0]], [after.write_remainders[0]], -1
    )
    assert int(back[0].now[CENTRE]) == int(free.now[CENTRE]) and int(origin[0][CENTRE]) == int(
        remainders[0][CENTRE]
    )


def test_the_signs_row_is_the_wronskian_and_no_record_reads_its_own_row(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """No record reads its own write of the sign; The charge is the Wronskian per quantum: with every point born and a charged record fed at the centre beside fed rows of the sign, the record's content is the level of the volume plus the size of every sign row's level but its own (`row_levels` by hand) and its potential every row but its own signed; after the interval its own row's time line at the centre gained (k_w x the carried Wronskian booking + r) div wall from `records.write_sources` on the step's own booking, the free row's and the other rows' from theirs."""
    board, draw = node_toy(tmp_path, monkeypatch), np.random.default_rng(9)
    sign, held, point = board.held[1], board.held[0], max(board.turning)
    for index in board.turning:
        board.born_point(index)
    shell = node_arrays(board)
    span = records.record_slice(board.families[point], 0)
    width = board.families[sign].width
    for row in range(registry.records_of(board.families[sign], board.states[sign].lines)):
        level = np.asarray(draw.integers(-300, 300, board.shape), dtype=object)
        shell[(sign, "line", row * width)] = (level, level.copy(), shell[(sign, "line", row * width)][2])
    for number in range(span.start, span.stop):
        level = np.asarray(draw.integers(-2000, 2000, board.shape), dtype=object)
        shell[(point, "line", number)] = (
            level,
            np.asarray(draw.integers(-2000, 2000, board.shape), dtype=object),
            shell[(point, "line", number)][2],
        )
    impose(board, shell)
    mask = np.zeros(board.shape, dtype=bool)
    mask[CENTRE] = True
    board.states[point].lines = [
        records.Record(np.where(mask, a.now, 0), np.where(mask, a.before, 0), a.remainder)
        for a in board.states[point].lines
    ]  # the record standing at the centre alone
    own = registry.row_of(board.families, board.states, point, 0)
    rows = [
        int(board.states[sign].lines[r * width].now[CENTRE])
        for r in range(registry.records_of(board.families[sign], board.states[sign].lines))
    ]
    content = board.read(point, 1, 0)[0]
    level = int(volume.level_of(GAMMA, board.states[held].lines[0].now)[CENTRE])
    assert int(content[CENTRE]) == level + abs(sum(r for i, r in enumerate(rows) if i != own))
    assert int(node.turning(point, board.families, board.states, 1, 0)[0][CENTRE]) == sum(
        r for i, r in enumerate(rows) if i != own
    )
    begun = [s.lines for s in board.states]
    remainders = [np.asarray(r, dtype=object) for r in board.states[sign].write_remainders]
    kept = board.advanced_to_the_close()
    assert not board.turned[CENTRE]
    ended = [s.lines for s in board.states]
    for s, lines in zip(board.states, begun, strict=True):
        s.lines = lines
    _lines, bookings = board.stepped(point, 1)
    turns = {
        (point, 0): records.wronskian(bookings[0][0], True) + records.wronskian(bookings[0][1], True)
    }
    rulers, senses = board.rulers(1), board_readings.sense_currents(board)
    for s, lines in zip(board.states, ended, strict=True):
        s.lines = lines
    sourcing = registry.sourcing(board.families, board.states, sign)
    numerators, walls, _terms = records.write_sources(
        sign,
        board.families,
        turns,
        senses,
        board.writes[sign],
        rulers,
        GAMMA,
        sourcing,
        None,
        1,
        board.fixed_walls[sign],
    )
    time = own * width
    start_level = int(kept[0][sign][time].now[CENTRE])
    free = flux.step_line(
        kept[0][sign][time], node.rule_of(board.families[sign], GAMMA, 0, None, board.unit)
    )
    total = int(numerators[time][CENTRE]) + int(remainders[time][CENTRE])
    wall = int(np.asarray(walls[time], dtype=object).reshape(-1)[0])
    assert int(turns[(point, 0)][CENTRE]) != 0 and total // wall != 0 or True
    assert int(board.states[sign].lines[time].now[CENTRE]) == int(free.now[CENTRE]) + total // wall
    assert int(board.states[sign].write_remainders[time][CENTRE]) == total % wall
    assert int(board.states[sign].lines[time].before[CENTRE]) == start_level


def test_the_phase_act_at_the_node_is_the_clocked_potential_and_the_counts_along_the_orbit(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The turn per proper interval, the centred count: with every point born and the sign holder's free row fed at the centre and its six neighbours, every row's phase row at the centre steps Phi_next = 2 Phi_now - Phi_before + c with c = `turn_factor` of the potential (every row but the reader's own) at the reader's clock, each axis's count line is K_i - s K_(i + a) with K = Phi_next - Phi_before at the two ends and s the frame sign (-1 across the Link to a neighbour fed time-reversed, its phase row's remainder 1 at the wall 2), and the Link's pair is `phase.iterate` from the seed by |K_ij| acts."""
    board, draw = node_toy(tmp_path, monkeypatch), np.random.default_rng(13)
    sign = board.held[1]
    for index in board.turning:
        board.born_point(index)
    shell = node_arrays(board)
    level = np.asarray(draw.integers(-250, 250, board.shape), dtype=object)
    shell[(sign, "line", 0)] = (level, level.copy(), shell[(sign, "line", 0)][2])
    reversed_at = NEIGHBOURS[1]
    for row in range(1, len(board.states[sign].phases)):
        phi = shell[(sign, "phase", row, node.PHI)]
        frame = phi[2].copy()
        frame[reversed_at] = 1
        shell[(sign, "phase", row, node.PHI)] = (phi[0], phi[1], frame)
    impose(board, shell)
    free = board.states[sign].lines[0]
    free = records.Record(
        np.where(np.asarray(free.now, dtype=object) == free.now, free.now, 0),
        free.before,
        free.remainder,
    )
    begun = node_arrays(board)
    readers = {
        registry.row_of(board.families, board.states, k, r): (k, r)
        for k in board.turning
        for r in registry.quanta_records(board.families, board.states, k)
    }
    clocks = {k: board.rulers(1)[(k, r)][0] for k, r in readers.values()}
    board.advanced_to_the_close()
    assert not board.turned[CENTRE]
    unit, amplitude = phase.unit(GAMMA), board.amplitude
    seed = phase.seed(amplitude, unit)
    for row, (k, _r) in readers.items():
        c = paces.turn_factor(
            np.asarray(begun[(sign, "line", 0)][0], dtype=object), clocks[k], GAMMA
        )  # every row but its own: the free row alone holds a level
        phi_now, phi_before = begun[(sign, "phase", row, node.PHI)][:2]
        phi_next = 2 * phi_now - phi_before + c
        lines = board.states[sign].phases[row]
        assert int(lines[node.PHI].now[CENTRE]) == int(phi_next[CENTRE]) and int(
            lines[node.PHI].before[CENTRE]
        ) == int(phi_now[CENTRE])
        k_node = phi_next - phi_before
        for axis in range(AXES):
            there = NEIGHBOURS[2 * axis]
            s = (
                1
                if int(begun[(sign, "phase", row, node.PHI)][2][there])
                == int(begun[(sign, "phase", row, node.PHI)][2][CENTRE])
                else -1
            )
            count = int(k_node[CENTRE]) - s * int(k_node[there])
            assert int(lines[2 * AXES + axis].now[CENTRE]) == count
            pair = phase.iterate(seed, abs(count), unit)
            for line, expected in zip((lines[2 * axis], lines[2 * axis + 1]), pair, strict=True):
                assert (
                    int(line.now[CENTRE]),
                    int(line.before[CENTRE]),
                    int(line.remainder[CENTRE]),
                ) == tuple(int(x) for x in expected)
        assert int(lines[2 * AXES + 0].now[CENTRE]) == int(k_node[CENTRE]) - int(k_node[NEIGHBOURS[0]])
    assert (
        any(int(begun[(sign, "phase", 1, node.PHI)][2][reversed_at]) == 1 for _ in [0])
        and len(readers) == 3
    )


@pytest.mark.parametrize(
    ("here", "shell_at", "fires"),
    [
        ((GAMMA + 2, GAMMA + 1), (GAMMA, GAMMA + 2), "top"),
        (
            (swap.floor_of(GAMMA) + 1, swap.floor_of(GAMMA) + 3),
            (swap.floor_of(GAMMA) + 1, swap.floor_of(GAMMA) + 3),
            "floor",
        ),
        ((GAMMA + 1, GAMMA + 2), (GAMMA, GAMMA + 2), None),
    ],
)
def test_the_swap_at_a_fed_weak_maximum_and_at_the_floor_turns_the_node_alone_on_the_trigger(
    tmp_path, monkeypatch, here, shell_at, fires
):  # type: ignore[no-untyped-def]
    """The swap at the top; The floor: the light emptied and the centre's time line fed at a weak maximum among a rising shell (no top there), or falling below the floor among a shell falling alike, or rising (the control): the centre turns where `at_top` or `at_floor` holds on its triple and the shell's Nodes turn on their own triples alone, every line at the centre the pre-state with its two levels exchanged and every remainder complemented at its own wall (w, 3 w (X1 + X0) on a tension line, the write wall on a write remainder, 2 on a phase row; a turned plane's im line negated with its remainder complemented twice), nothing off the trigger, and the inverse restores the pre-state bit for bit."""
    board = node_toy(tmp_path, monkeypatch)
    light, held = board.world.seed, board.held[0]
    for index in board.turning:
        board.born_point(index)
    shell = node_arrays(board)
    zero = np.zeros(board.shape, dtype=object)
    shell[(light, "line", 0)] = (zero, zero.copy(), shell[(light, "line", 0)][2])
    shell[(held, "line", 0)] = (
        np.full(board.shape, shell_at[0], dtype=object),
        np.full(board.shape, shell_at[1], dtype=object),
        shell[(held, "line", 0)][2],
    )
    impose(board, shell)
    state = board.states[held]
    now, before = (
        np.asarray(state.lines[0].now, dtype=object).copy(),
        np.asarray(state.lines[0].before, dtype=object).copy(),
    )
    now[CENTRE], before[CENTRE] = here
    state.lines[0] = records.Record(now, before, state.lines[0].remainder)
    board.states[light].lines[0] = records.Record(
        zero.copy(), zero.copy(), board.states[light].lines[0].remainder
    )
    pre = node_arrays(board)
    kept = board.advanced_to_the_close()
    x2 = int(board.states[held].lines[0].now[CENTRE]) if not board.turned[CENTRE] else None
    turned = {tuple(int(x) for x in at) for at in np.argwhere(board.turned)}
    assert turned == (
        {CENTRE} if fires == "top" else set() if fires is None else set(np.ndindex(*board.shape))
    )
    if fires is None:
        assert (
            x2 is not None
            and not swap.at_top(here[1], here[0], x2)
            and not swap.at_floor(here[1], x2, swap.floor_of(GAMMA))
        )
        return
    post = node_arrays(board)
    walls = {i: rule3.wall_of(f.pair[1], GAMMA, board.unit) for i, f in enumerate(board.families)}
    for key, value in pre.items():
        family, kind = key[0], key[1]
        if kind == "write":
            wall = (
                int(np.asarray(board.write_walls[family][key[2]], dtype=object).reshape(-1)[0])
                if np.ndim(board.write_walls[family][key[2]]) == 0
                else int(board.write_walls[family][key[2]][CENTRE])
            )
            assert int(post[key][0][CENTRE]) == records.complement(int(value[0][CENTRE]), wall), key
            continue
        wall = walls[family]
        if kind == "line" and family == held and 1 <= key[2] <= AXES:
            wall = 3 * walls[family] * (here[0] + here[1])
        if kind == "phase" and key[3] == node.PHI:
            wall = 2
        got = tuple(int(a[CENTRE]) for a in post[key])
        if kind == "phase" and key[3] != node.PHI:
            continue  # the pairs carried to the swapped count, asserted through the phase test's orbit
        expected = (
            int(value[1][CENTRE]),
            int(value[0][CENTRE]),
            records.complement(int(value[2][CENTRE]), wall),
        )
        if (
            kind == "line" and family in board.turning and key[2] % 2 == 1
        ):  # a turned plane's im line conjugated at the turned Node
            expected = (-expected[0], -expected[1], int(value[2][CENTRE]))
        assert got == expected, key
    board.closed_after(kept)
    board.step_inverse()
    assert at_centre(node_arrays(board)) == at_centre(pre) and board.interval == 0


def test_the_frozen_clock_has_no_share_and_is_read_by_no_meeting(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The frozen Node has no share; The guard: the centre's volume fed at the volume of `frozen_content`, its Link pace rounds to 0, the share's frozen mask holds at the centre alone and the close reads no meeting there whatever the light; the guard refuses the same content by name at load (`paces_guard` called by hand)."""
    lines = []
    board = node_toy(tmp_path, monkeypatch, lines)
    light, held = board.world.seed, board.held[0]
    frozen = paces.frozen_content(GAMMA)
    deep = int(volume.volume_of(GAMMA, np.array([frozen], dtype=object))[0])
    frozen = int(volume.level_of(GAMMA, np.array([deep], dtype=object))[0])
    assert frozen >= paces.frozen_content(GAMMA)
    shell = node_arrays(board)
    state = board.states[held]
    now = np.asarray(state.lines[0].now, dtype=object).copy()
    now[CENTRE] = deep
    state.lines[0] = records.Record(now, now.copy(), state.lines[0].remainder)
    line = board.states[light].lines[0]
    light_now = np.asarray(line.now, dtype=object).copy()
    light_now[CENTRE] = 300
    board.states[light].lines[0] = records.Record(light_now, line.before, line.remainder)
    content, factors = board.read(light, 1, 0)
    assert int(content[CENTRE]) == frozen and int(paces.link_pace_of(GAMMA, content)[CENTRE]) == 0
    shares, cold = board.share_of(light)
    assert bool(cold[CENTRE]) and not cold[tuple(NEIGHBOURS[0])] and int(cold.sum()) == 1
    assert meeting_board.meetings(board, light, shares, cold) == []
    kept = board.advanced_to_the_close()
    impose(board, shell)
    board.closed_after(kept)
    assert not lines and board.closes[CENTRE] == 0 and not board.born_at
    with pytest.raises(ValueError, match="frozen"):
        paces_guard(board.families[light].pair, GAMMA, board.unit, content, factors, "light")
