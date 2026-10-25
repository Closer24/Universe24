"""The properties the engine shows, each with a small test on a run (the owner's word of 2026-10-25: every property with a small test; specified by two blind hands and built by a third): on the bare 3-cube of the tests' small universe at den 1,021 under the law's hole seed, the Links lengthen on the running board and in the clicks, a Node's clock reverses at its own top on the course, the uniform sea turns at every Node at once and runs its rise back, gravity's sign on two boards, the dilation's sign by hand, the horizon forced at the wall, the frozen clock, the one-Link reach of the whole interval, the uniform sea a fixed point of the remainders, only a bound body clicks, and the sign's write travelling one Link per interval; every expected value derived from the law's integers, a by-hand line or a comparison between two boards or two intervals, no interval and no count of the course typed (ALGEBRA.md, the clauses named at each test)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, NamedTuple

import numpy as np
import pytest

from event_universe import bound_body, digits, seed, share, shear, swap, world_files
from event_universe.act import born_items, born_table, click
from event_universe.core import paces
from event_universe.core.ports import arrival
from event_universe.core.rule3 import rule_integers, wall_of
from event_universe.features import volume
from event_universe.features.read import link_factors, link_tensions
from event_universe.lattice import Lattice
from event_universe.loader.derived import count_wall
from event_universe.records import complement
from event_universe.reports import PROPER
from event_universe.world_files import load_world
from tests.laws import ROOT, board_state, load_file, same_state
from tests.laws_universe import CUBE, GAMMA, bare_torus, light_emptied, time_line_set, uniform_sea

ERAS = load_file("eras_tool_on_a_run", ROOT / "tools" / "eras.py")
INTERVALS = 40  # the hole seed's run the lengthening, the clicks and the bodies' credits are read on: the run's length alone, every stop below read from the run's own lines
SHORT = 12  # the two boards' run of gravity's sign, the run's length alone
CENTRE = (1, 1, 1)  # the Node set by hand where one is: the cube's centre, two Links from the hole
CORNER = (1, 1, 0)  # the Node raised by one level for the one-Link reach, no neighbour of the hole
State = list[tuple[list[tuple[Any, Any, Any]], list[Any]]]


class Run(NamedTuple):
    board: Lattice
    lines: list[dict[str, Any]]
    clocks: list[Any]  # the seed's clock at every Node at each interval's start
    volumes: list[Any]  # the volume's level X at every Node after each interval
    time: tuple[list[int], list[int]]  # the time line's two levels before the last interval


def hole_board(
    folder: Path, cube: int = CUBE, intervals: int = INTERVALS
) -> tuple[Lattice, list[dict[str, Any]]]:
    """The hole seed on the bare torus of the tests' small universe written in `folder`, the repository root pointed there, every output line kept."""
    folder.mkdir(exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    lines: list[dict[str, Any]] = []
    return Lattice(load_world(bare_torus(folder, cube, intervals)), output=lines.append), lines


def levels(board: Lattice, index: int) -> tuple[Any, Any]:
    """A family's first line's two levels copied as Python's integers, (now, before)."""
    line = board.states[index].lines[0]
    return np.asarray(line.now, dtype=object).copy(), np.asarray(line.before, dtype=object).copy()


def pair_laid(board: Lattice, at: tuple[int, int, int]) -> None:
    """The lone pair laid at one Node by the birth's own path (act.born_table, born_items, click): the list two light quanta make, one record per child."""
    light, action = board.world.seed, board.world.quantum_action
    assert light is not None
    table = born_table(board.families, light, action, 2 * count_wall(board.families[light], action), 1)
    click(board, born_items(board.families, table, (at,)))


def apart(a: State, b: State) -> set[tuple[int, ...]]:
    """The Nodes at which two states of `board_state` differ in any line's level or remainder or any write remainder."""
    found: set[tuple[int, ...]] = set()
    for (lines_a, writes_a), (lines_b, writes_b) in zip(a, b, strict=True):
        pairs = [
            (u, v) for x, y in zip(lines_a, lines_b, strict=True) for u, v in zip(x, y, strict=True)
        ]
        for u, v in pairs + list(zip(writes_a, writes_b, strict=True)):
            found |= {tuple(int(i) for i in d) for d in np.argwhere(np.asarray(u != v, dtype=bool))}
    return found


def mirrored(board: Lattice, after: State, before: State) -> bool:
    """Whether `after` is `before` under the fifth act's image (swap.swapped): every line's two levels exchanged, a plane's sense lines negated with their remainders kept, every other line's remainder complemented at its wall; the carried tension lines' remainders and the write remainders, at walls of their own, left aside."""
    gamma, unit = board.world.node_clock, board.unit
    for index, family in enumerate(board.families):
        wall = wall_of(family.pair[1], gamma, unit)
        tension = set(shear.shear_lines(family)) if shear.carried(family) else set()
        for number, ((n1, b1, r1), (n2, b2, r2)) in enumerate(
            zip(after[index][0], before[index][0], strict=True)
        ):
            if family.plane and number % 2:
                good = np.array_equal(n1, -b2) and np.array_equal(b1, -n2) and np.array_equal(r1, r2)
            else:
                good = np.array_equal(n1, b2) and np.array_equal(b1, n2)
                good = good and (number in tension or np.array_equal(r1, complement(r2, wall)))
            if not good:
                return False
    return True


@pytest.fixture(scope="module")
def hole_run(tmp_path_factory: pytest.TempPathFactory) -> Run:
    """The hole seed on the bare 3-cube stepped once for the module: per interval the seed's clock at every Node at the start and the volume's level X at every Node at the end, every output line and the board at the end, the repository root left as found."""
    kept = world_files.REPOSITORY_ROOT
    board, lines = hole_board(tmp_path_factory.mktemp("hole"))
    world_files.REPOSITORY_ROOT = kept
    light, held = board.world.seed, board.held[0]
    assert light is not None
    clocks, volumes, time = [], [], ([0], [0])
    for _ in range(INTERVALS):
        clocks.append(np.asarray(board.rulers(1)[(light, 0)][0], dtype=object))
        time = tuple(ERAS.whole(level) for level in levels(board, held))
        board.step()
        volumes.append(levels(board, held)[0])
    return Run(board, lines, clocks, volumes, (time[0], time[1]))


def test_the_links_lengthen_on_the_running_board(hole_run: Run) -> None:
    """The paces compose; The carried momentum (X = Gamma (Gamma / p_0)^4): on the hole seed the summed volume X never falls interval to interval and ends above the seed's; at the end every Node's X stands above Gamma; at every interval the clock read at the next start is at or below Gamma wherever X is at or above Gamma and below Gamma wherever X reaches the first level's volume, and the clock, the proper count's increment, is non-increasing in X across the Nodes; the eras tool's Link length is non-decreasing in X."""
    board, nodes = hole_run.board, int(np.prod(hole_run.board.shape))
    sums = [int(x.sum()) for x in hole_run.volumes]
    assert (
        all(a <= b for a, b in zip(sums, sums[1:], strict=False)) and sums[-1] > sums[0] >= nodes * GAMMA
    )
    assert (hole_run.volumes[-1] > GAMMA).all()
    first = int(
        volume.volume_of(GAMMA, np.array([1], dtype=object))[0]
    )  # the least X reading the level 1
    for x, clock in zip(hole_run.volumes, hole_run.clocks[1:], strict=False):
        assert (clock[x >= GAMMA] <= GAMMA).all() and (clock[x >= first] < GAMMA).all()
        ordered = [
            c for _x, c in sorted(zip(x.reshape(-1).tolist(), clock.reshape(-1).tolist(), strict=True))
        ]
        assert all(a >= b for a, b in zip(ordered, ordered[1:], strict=False))
    line = ERAS.node_lines(board, hole_run.time, [1] * nodes)
    lengths = [length for _x, length in sorted(zip(line["X"], line["length"], strict=True))]
    assert all(a <= b for a, b in zip(lengths, lengths[1:], strict=False)) and lengths[0] > 1


def test_the_lengthening_is_read_in_the_clicks(hole_run: Run) -> None:
    """The click's view (PROPER); The clock near matter: at the Node credited most often, between successive credits of one record the proper never outruns the interval (the clock at or below Gamma), and the pace delta proper over delta interval of the last pair is at or below the first pair's and below 1: the spacing of a body's clicks lengthens in the board's intervals as the Links do."""
    tracks: dict[tuple[tuple[int, ...], tuple[int, ...]], list[tuple[int, int]]] = {}
    for line in hole_run.lines:
        if line["event"] == "credit":
            key = (tuple(line["support"]), tuple(line["identity"]))
            tracks.setdefault(key, []).append((line["interval"], line[PROPER]))
    found = max(tracks.values(), key=len)
    assert len(found) >= 3
    pairs = [(b[1] - a[1], b[0] - a[0]) for a, b in zip(found, found[1:], strict=False)]
    assert all(0 < proper <= interval for proper, interval in pairs)
    (first_proper, first_interval), (last_proper, last_interval) = pairs[0], pairs[-1]
    assert last_proper * first_interval <= first_proper * last_interval and last_proper < last_interval


def test_the_clock_reverses_at_a_nodes_own_top_on_the_course(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The swap at the top; The inverse: the hole seed stepped to the first interval at which a Node whose light moves turns; the fifth act's triple, the kept before, the kept now and the step's own output read by a spy on swap.stepped, fires swap.at_top or swap.at_floor exactly where the board reads turned, at_top at that Node; there the light's and the volume's (now, before) are the kept (before, now) and the light's velocity is negated, while at every unturned neighbour the level now is not the kept before; one step back restores the kept state bit for bit."""
    board, _lines = hole_board(tmp_path)
    light, held = board.world.seed, board.held[0]
    assert light is not None
    outputs: dict[int, Any] = {}
    real = swap.stepped

    def spied(b: Lattice, kept_state: swap.Kept) -> None:
        outputs[b.interval] = levels(b, held)[0]
        real(b, kept_state)

    monkeypatch.setattr(swap, "stepped", spied)
    while True:
        kept, (now, before), (x_now, x_before) = (
            board_state(board),
            levels(board, light),
            levels(board, held),
        )
        board.step()
        moving = board.turned & np.asarray(now != before, dtype=bool)
        if moving.any():
            break
    triple = (x_before, x_now, outputs[board.interval])
    fired = swap.at_top(*triple) | swap.at_floor(triple[0], triple[2], swap.floor_of(GAMMA))
    at = tuple(int(i) for i in np.argwhere(moving)[0])
    assert (fired == board.turned).all() and swap.at_top(*triple)[at]
    after, x_after = board.states[light].lines[0], board.states[held].lines[0]
    assert (int(after.now[at]), int(after.before[at])) == (int(before[at]), int(now[at]))
    assert (int(x_after.now[at]), int(x_after.before[at])) == (int(x_before[at]), int(x_now[at]))
    assert int(after.now[at]) - int(after.before[at]) == int(before[at]) - int(now[at]) != 0
    frame = [
        tuple(int(i) for i in node) for node in digits.frame_of(at, board.shape, board.world.periodic)
    ]
    unturned = [node for node in frame[1:] if not board.turned[node]]
    assert unturned and all(int(after.now[node]) != int(before[node]) for node in unturned)
    board.step_inverse()
    assert same_state(board_state(board), kept)


def test_the_uniform_sea_turns_at_every_node_at_once_and_runs_its_rise_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The swap at the top (the uniform board's closed orbit): the uniform sea laid by name on the 3-cube, stepped until the fifth act turns every Node in one interval and then on while the mirror of the rise holds no act (the births and the clicks go only forward); from the turn's interval t* the state at t* + k is the state at t* - 1 - k under the act's image (`mirrored`) for every k of that stretch; the summed X is largest at the top, falls at every interval of the mirror and ends below the top's."""
    monkeypatch.setattr(seed, "uniform_seed", uniform_sea)
    board, lines = hole_board(tmp_path, CUBE, 24 * CUBE**3)
    nodes, held, cap = int(np.prod(board.shape)), board.held[0], 8 * CUBE**3
    states, sums = [board_state(board)], []
    while not (board.swaps and board.swaps[-1][0] == board.interval and board.swaps[-1][2] == nodes):
        assert board.interval < cap
        board.step()
        states.append(board_state(board))
        sums.append(int(levels(board, held)[0].sum()))
    top = board.interval
    reach = top - 1 - max(line["interval"] for line in lines if line["interval"] < top)
    while board.interval < top + reach and not any(line["interval"] >= top for line in lines):
        board.step()
        states.append(board_state(board))
        sums.append(int(levels(board, held)[0].sum()))
    mirror = min(reach, board.interval - top - any(line["interval"] >= top for line in lines))
    assert 0 < mirror and all(
        mirrored(board, states[top + k], states[top - 1 - k]) for k in range(mirror)
    )
    assert sums[top - 2] == max(sums) and all(
        a > b for a, b in zip(sums[top - 1 :], sums[top : mirror + top], strict=False)
    )
    assert sums[-1] < sums[top - 2]


def test_gravitys_sign_on_two_boards(tmp_path: Path) -> None:
    """A family's write is one act; The clock near matter: two bare 3-cubes under the hole seed, one with the lone pair laid at the hole by the birth's own path, stepped alike; at that Node the laid board's X stands above the bare board's after the first interval and at the end, and its proper count at or below the bare board's at every interval and below it at the end: the record's form deepens the volume where it stands and slows the clock there; the run back exact."""
    bare, _ = hole_board(tmp_path / "bare")
    laid, _ = hole_board(tmp_path / "laid")
    held, at = laid.held[0], seed.ORIGIN
    pair_laid(laid, at)
    kept, deeper, slower = [board_state(laid)], [], []
    for _ in range(SHORT):
        bare.step()
        laid.step()
        kept.append(board_state(laid))
        deeper.append(int(levels(laid, held)[0][at]) - int(levels(bare, held)[0][at]))
        slower.append(int(bare.proper_count[at]) - int(laid.proper_count[at]))
    assert deeper[0] > 0 and deeper[-1] > 0 and all(s >= 0 for s in slower) and slower[-1] > 0
    for k in range(SHORT):
        laid.step_inverse()
        assert same_state(board_state(laid), kept[SHORT - 1 - k])


def test_the_dilations_sign_by_hand(tmp_path: Path) -> None:
    """The clock near matter; The paces compose: the light emptied and the volume line set by hand at the cube's centre to the volume of the level Gamma div 10, Gamma elsewhere; at the first interval's start the clock there is below Gamma and every other Node's is Gamma; after the cube's side of intervals the proper count there is below every other Node's."""
    board, _ = hole_board(tmp_path)
    light = board.world.seed
    assert light is not None
    light_emptied(board)
    x = np.full(board.shape, GAMMA, dtype=object)
    x[CENTRE] = int(volume.volume_of(GAMMA, np.array([GAMMA // 10], dtype=object))[0])
    time_line_set(board, x, x.copy())
    clock, others = np.asarray(board.rulers(1)[(light, 0)][0], dtype=object), ~board.mask((CENTRE,))
    assert int(clock[CENTRE]) < GAMMA and (clock[others] == GAMMA).all()
    for _ in range(CUBE):
        board.step()
    proper = np.asarray(board.proper_count, dtype=object)
    assert int(proper[CENTRE]) < int(proper[others].min())


def test_the_horizon_is_forced_at_the_wall(tmp_path: Path) -> None:
    """The horizon; The guard (Q = 0 at the tension Gamma): on the hole seed the volume holder's x axis line set by hand along the hole's x ring at Gamma, Gamma and -Gamma, so that the Link from the hole to its +x neighbour reads the tension Gamma and every other Link 0: the tensions and factors by hand (features/read on the axis lines) equal the engine's read, that Link's factor 0 at both ends and G^2 on every other Port, tools/eras.horizon_links names that Link alone; one interval: the +x neighbour's light steps as Rule3 by hand with that Port's reach 0 and not as the plain rule, the hole turns at its top; the run back exact; the ring's levels at half the wall re-couple the Link, its factor above 0 and no Link at the wall."""
    board, _ = hole_board(tmp_path)
    light, held, unit = board.world.seed, board.held[0], board.unit
    assert light is not None
    origin, near, far = seed.ORIGIN, (1, *seed.ORIGIN[1:]), (2, *seed.ORIGIN[1:])
    state, family = board.states[held], board.families[light]

    def ring(level: int) -> None:
        axis = np.asarray(state.lines[1].now, dtype=object).copy()
        axis[origin], axis[near], axis[far] = level, level, -level
        state.lines[1] = state.lines[1].__class__(axis, axis.copy(), state.lines[1].remainder)

    ring(GAMMA)
    axes = [(1, [np.asarray(state.lines[1 + a].now, dtype=object) for a in range(3)])]
    tensions = link_tensions(axes, GAMMA)
    factors = link_factors(GAMMA, unit, tensions)
    content, read = board.read(light)
    assert all(np.array_equal(a, b) for a, b in zip(factors, read, strict=True))
    assert (
        int(tensions[0][origin]) == int(tensions[1][near]) == GAMMA
        and int(factors[0][origin]) == int(factors[1][near]) == 0
    )
    assert sum(int((np.asarray(f) == unit * unit).sum()) for f in factors) == 6 * CUBE**3 - 2
    shape = board.shape
    assert ERAS.horizon_links(board) == [
        [int(np.ravel_multi_index(origin, shape)), int(np.ravel_multi_index(near, shape))]
    ]
    kept, (now, before) = board_state(board), levels(board, light)
    remainder = np.asarray(board.states[light].lines[0].remainder, dtype=object).copy()
    board.step()
    clock, pace = paces.node_paces(
        GAMMA, int(np.asarray(content)[near]) if np.ndim(content) else int(content)
    )
    arrivals = [int(arrival(now, axis, side)[near]) for axis in range(3) for side in (1, -1)]
    stepped = []
    for ports in ((int(f[near]) for f in factors), (unit * unit,) * 6):
        reads, own, wall, _mass = rule_integers(*family.pair, GAMMA, clock, pace, tuple(ports), unit)
        total = (
            own * int(now[near])
            - wall * int(before[near])
            + sum(r * m for r, m in zip(reads, arrivals, strict=True))
        )
        stepped.append((total + int(remainder[near])) // wall)
    assert int(board.states[light].lines[0].now[near]) == stepped[0] != stepped[1]
    assert board.turned[origin] and not board.turned[near]
    board.step_inverse()
    assert same_state(board_state(board), kept)
    ring(GAMMA // 2)
    coupled = board.read(light)[1]
    assert 0 < int(coupled[0][origin]) < unit * unit and ERAS.horizon_links(board) == []


def test_the_frozen_clock_holds_and_births_nothing(tmp_path: Path) -> None:
    """The paces compose (a collapse ends in a frozen clock); The frozen Node has no share; The board reads itself: on the hole seed the volume line at one Node set by hand to volume_of(Gamma, frozen_content(Gamma)), the least volume whose Link pace rounds to 0; at every interval's start to the first crediting close that Node alone is frozen under the seed's read, its clock above 0 and below Gamma, its three axis paces 0 and its X unchanged; at that close no credit and no birth names it while every one of its six neighbours is credited; the run back exact."""
    board, lines = hole_board(tmp_path)
    light, held = board.world.seed, board.held[0]
    assert light is not None
    at, nodes = (0, 0, 1), board.shape
    frozen = int(volume.volume_of(GAMMA, np.array([paces.frozen_content(GAMMA)], dtype=object))[0])
    x = np.full(nodes, GAMMA, dtype=object)
    x[at] = frozen
    time_line_set(board, x, x.copy())
    kept = [board_state(board)]
    while not any(line["event"] == "credit" for line in lines):
        clock, axes = board.rulers(1)[(light, 0)]
        cold = board.share_of(light)[1]
        assert bool(cold[at]) and int(cold.sum()) == 1 and 0 < int(clock[at]) < GAMMA
        assert [int(a[at]) for a in axes] == [0, 0, 0] and int(levels(board, held)[0][at]) == frozen
        board.step()
        kept.append(board_state(board))
    credited = {tuple(line["support"]) for line in lines if line["event"] == "credit"}
    born = {tuple(node) for line in lines if line["event"] == "birth" for node in line["nodes"]}
    frame = [tuple(int(i) for i in node) for node in digits.frame_of(at, nodes, board.world.periodic)]
    assert at not in credited | born and set(frame[1:]) <= credited
    steps = board.interval
    for k in range(steps):
        board.step_inverse()
        assert same_state(board_state(board), kept[steps - 1 - k])


@pytest.mark.parametrize("cube", [CUBE, CUBE + 2])
def test_the_whole_interval_reaches_one_link(tmp_path: Path, cube: int) -> None:
    """The interval's dependency radius is one Link; Only local: two bare cubes under the hole seed, on one the light's level now raised by one level at a Node no neighbour of the hole; after one interval the two boards differ, in every line, remainder and write remainder, at that Node and its six neighbours alone, on every axis; after the step back at that Node alone."""
    a, _ = hole_board(tmp_path / "a", cube)
    b, _ = hole_board(tmp_path / "b", cube)
    light = b.world.seed
    assert light is not None
    line, now = b.states[light].lines[0], levels(b, light)[0]
    now[CORNER] += 1
    b.states[light].lines[0] = line.__class__(now, line.before, line.remainder)
    frame = {tuple(int(i) for i in node) for node in digits.frame_of(CORNER, b.shape, b.world.periodic)}
    assert len(frame) == 7 and seed.ORIGIN not in frame
    a.step()
    b.step()
    assert apart(board_state(a), board_state(b)) == frame
    a.step_inverse()
    b.step_inverse()
    assert apart(board_state(a), board_state(b)) == {CORNER}


def test_the_uniform_sea_is_a_fixed_point_of_the_remainders(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The uniform seed is a lay (Rule3 on a uniform record keeps every remainder at the origin); The board reads itself: the uniform sea laid by name, stepped to its first births; at every interval before them the light's remainder stands at the half wall at every Node, every line of every family is alike at every Node, digits.at_origin holds at every Node's frame so no whether is drawn, and no credit is written; at the birth interval a birth falls at every Node alike."""
    monkeypatch.setattr(seed, "uniform_seed", uniform_sea)
    board, lines = hole_board(tmp_path)
    light = board.world.seed
    assert light is not None
    half = board.half_wall(light)
    frames = [digits.frame_of(at, board.shape, board.world.periodic) for at in np.ndindex(*board.shape)]
    while not any(line["event"] == "birth" for line in lines):
        assert board.interval < 2 * CUBE**3
        assert (np.asarray(board.states[light].lines[0].remainder, dtype=object) == half).all()
        assert all(
            len(set(np.asarray(level, dtype=object).reshape(-1).tolist())) == 1
            for state in board.states
            for line in state.lines
            for level in (line.now, line.before)
        )
        assert all(
            digits.at_origin(board, [(index, frame) for index in board.order]) for frame in frames
        )
        assert not any(line["event"] == "credit" for line in lines)
        board.step()
    births = [line for line in lines if line["event"] == "birth"]
    assert {tuple(node) for line in births for node in line["nodes"]} == {
        tuple(frame[0]) for frame in frames
    }
    assert (
        len({line["interval"] for line in births}) == 1
        and len({len(line["children"]) for line in births}) == 1
    )


def test_only_a_bound_body_clicks(hole_run: Run) -> None:
    """Only a bound body clicks; The bound body's click is the Node's act: on the hole seed's run every credit of the light falls at a birth at its Node (the two light quanta meeting), every other credit is a body's, a record of a charged plane family with the kind the width of its lines, and the massless pair is no body."""
    board, credits = hole_run.board, [line for line in hole_run.lines if line["event"] == "credit"]
    light = board.world.seed
    births = {
        (line["interval"], tuple(node))
        for line in hole_run.lines
        if line["event"] == "birth"
        for node in line["nodes"]
    }
    assert credits and any(line["identity"][0] == light for line in credits)
    assert any(line["identity"][0] != light for line in credits)
    for line in credits:
        family = board.families[line["identity"][0]]
        assert line["kind"] == family.width
        if line["identity"][0] == light:
            assert (line["interval"], tuple(line["support"])) in births
        else:
            assert share.charged(family) and family.plane
    assert light not in {index for index, _record in bound_body.body_records(board)}


def test_the_signs_write_travels_one_link_per_interval(tmp_path: Path) -> None:
    """Light is born by the write; No record reads its own write of the sign; The interval's dependency radius is one Link: the lone pair laid by the birth's own path at the cube's centre of the bare 3-cube; the holder of the sign's rows are 0 at every Node before the first interval, non-zero at that Node alone after one interval and at the Node and its six neighbours alone after two."""
    board, _ = hole_board(tmp_path)
    sign = next(index for index, family in enumerate(board.families) if family.wronskian)
    pair_laid(board, CENTRE)
    frame = {
        tuple(int(i) for i in node)
        for node in digits.frame_of(CENTRE, board.shape, board.world.periodic)
    }
    written = []
    for _ in range(3):
        rows, width = board.states[sign].lines, board.families[sign].width
        summed = sum(
            np.abs(np.asarray(rows[r * width].now, dtype=object)) for r in range(len(rows) // width)
        )
        written.append(
            {tuple(int(i) for i in node) for node in np.argwhere(np.asarray(summed != 0, dtype=bool))}
        )
        board.step()
    assert written == [set(), {CENTRE}, frame]
