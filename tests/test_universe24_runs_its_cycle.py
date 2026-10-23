"""The test of the law's course for Universe24, the one universe (examples/events/universe24/, the three-dimensional torus with matter laid as clumps, light as a uniform family and one NodeDetector; ALGEBRA.md, The one Node, The swap at the top, The carried momentum, The stress is the Links'): the same world small, the 3-cube torus with one clump of matter, the light family at the uniform level 636 with the velocity 190 and the detector on two Nodes, read from the shipped universe file's declarations with the gap widened to [990, 1000] so that the course is ten times shorter in the test's seconds (the top within 40 intervals where the shipped gap tops near 300; the gap is a run parameter, the project's and not nature's). The clauses: (1) the one Node runs it: the loader accepts the shipped world and refuses a former key added to a copy (the world's `interval`, the held row's `booking`); (2) the stages in order on the small torus: the rise from the seed at rest, X'' below 0 at the clump's Node on the rise (the dust's pull), the fifth act's fires at the top (staggered, Node by Node, within ten intervals of the clump's own top), the fall, and the law's course on this small structured board past its former end, the crunch at 78 (X at most 0 at a Node, refused by name before The floor of 2026-10-23): the Node turns at the floor, the least volume with a reading, and the run goes on with every X at or above it (the shipped 5-cube returns to X above the seed and rises again, its log the record); (3) light's velocity is the first integral: after the first interval every Node's light level has moved by exactly v, forward at a standing Node and backward at a turned one, and at every fire the turned Nodes' light velocity is reversed bit for bit (the two levels exchanged); (4) the run back through the fires is exact, 40 of 40 states, the inverse firing where the forward run fired; (5) the clicks are history kept: the run back writes no click and removes none, the forward clicks' intervals never decrease; (6) the shipped eras log's first lines are the shipped world's own, the readings of eight intervals equal to the log's bit for bit beside the elapsed seconds; (7) what the clicks change, read and not assumed: the same small world with the detector removed from the world file and nothing else changed runs the same course bit for bit at every interval, since a region NodeDetector without a draw reports its click and writes nothing the board reads (the click's write on the lattice is the draw's, ALGEBRA.md, The click's read of the board), so the two courses are equal throughout and the clicks are a reading of the course and not an act on it; and (8) without clicks the course runs back bit for bit: the detector-less board's run back of its whole course of 70 intervals is exact at every interval through every staggered fire (the bijection, nothing lost), and the tops come in their order, the clump's Node first and the board's volume after it (the staggered turn), the second bang not reached on this small board, which crunches, where the shipped 5-cube tops at 319 and again at 1,061."""

import copy
import json
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import swap, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world
from tests.laws import board_state, same_state
from tests.laws_universe import (
    AFTER_TOP,
    BEFORE_TOP,
    CLUMP,
    CUBE,
    ERAS,
    GAMMA,
    LEVEL,
    LOG,
    RESONANCES,
    SPEED,
    UNIVERSE,
    WORLD,
    flat,
    small_world,
)


def test_the_one_node_accepts_the_shipped_universe_and_refuses_a_former_key() -> None:
    world = json.loads(WORLD.read_text(encoding="utf-8"))
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    mode = json.loads(WORLD.with_suffix(".mode.json").read_text(encoding="utf-8"))
    files = {world["universe"]: universe, "universe.mode.json": mode}
    from event_universe.loader.world import parse_world

    parse_world(world, files, input_digest(world))  # (1) the shipped world, accepted
    former = copy.deepcopy(world)
    former["interval"] = "unobservable"
    with pytest.raises(ValueError, match="unknown key 'interval'"):
        parse_world(former, files, input_digest(former))
    held = copy.deepcopy(universe)
    held["families"][0]["held"]["booking"] = "form"
    with pytest.raises(ValueError, match="unknown key 'booking'"):
        parse_world(world, {**files, world["universe"]: held}, input_digest(world))


def test_the_small_universe_rises_decelerates_turns_falls_and_keeps_its_clicks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    clicks: list[dict[str, object]] = []
    board = Lattice(load_world(small_world(tmp_path)), output=clicks.append)
    (tmp_path / "blind").mkdir()
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path / "blind")
    blind_board = Lattice(load_world(small_world(tmp_path / "blind", detector=False)))
    blind_board.output = lambda line: None
    assert (
        not blind_board.node_detectors and board.node_detectors
    )  # (7) the same world, the detector removed
    names = [family.name for family in board.families]
    g, light = board.held[0], names.index("light")
    at = np.ravel_multi_index(tuple(CLUMP), board.shape)
    time_line = lambda: board.states[g].lines[0]  # noqa: E731
    light_line = lambda: board.states[light].lines[0]  # noqa: E731
    xs, states, lights = (
        [flat(time_line().now)],
        {0: board_state(board)},
        {0: (flat(light_line().now), flat(light_line().before))},
    )
    assert (
        xs[0] == [GAMMA] * CUBE**3 and flat(time_line().before) == [GAMMA] * CUBE**3
    )  # the seed at rest
    end = 70
    alike = 0
    for t in range(1, end + 1):
        board.step()
        blind_board.step()
        alike += same_state(board_state(board), board_state(blind_board))
        xs.append(flat(time_line().now))
        states[t] = board_state(board)
        lights[t] = (flat(light_line().now), flat(light_line().before))
    assert (
        alike == end and blind_board.swaps == board.swaps
    )  # (7) equal throughout: the click writes nothing the board reads
    clump = [x[at] for x in xs]
    top = max(range(len(clump)), key=lambda t: clump[t])
    volume_top = max(range(len(xs)), key=lambda t: sum(xs[t]))
    assert top < volume_top, (
        top,
        volume_top,
    )  # (8) the tops in their order: the clump's Node first, the board after it
    assert 20 < top < 50 and clump[1] > GAMMA, (top, clump[:3])  # (2) the rise from the seed
    velocity = [b - a for a, b in zip(clump, clump[1:], strict=False)]
    assert velocity[top - 2] > 0 and velocity[top - 2] < velocity[top - 12], velocity[
        top - 14 : top
    ]  # X'' below 0 on the rise
    fires = {s[0]: s[2] for s in board.swaps if s[1] == 1}
    at_top = [t for t in fires if t > 5]
    assert at_top and abs(min(at_top) - top) <= 10, (
        fires,
        top,
    )  # the fifth act fires at the top, staggered
    assert clump[end] < clump[top] and min(xs[end]) < min(xs[top]), (clump[end], clump[top])  # the fall
    for t in sorted(
        fires
    ):  # (3) the turned Nodes' light velocity reversed bit for bit, the two levels exchanged
        (pre_now, pre_before), (post_now, post_before) = lights[t - 1], lights[t]
        x_pre_now, x_pre_before, x_post_now = xs[t - 1], flat(states[t - 1][g][0][0][1]), xs[t]
        turned = [
            i
            for i in range(CUBE**3)
            if x_post_now[i] == x_pre_before[i] <= x_pre_now[i]
            and (post_now[i], post_before[i]) == (pre_before[i], pre_now[i])
        ]
        assert len(turned) >= fires[t], (t, len(turned), fires[t])
    first_now, first_before = lights[1]
    assert all(
        (n, b) in ((LEVEL + SPEED, LEVEL), (LEVEL - SPEED, LEVEL))
        for n, b in zip(first_now, first_before, strict=True)
    )
    assert (
        first_now.count(LEVEL - SPEED) == fires[1]
        and first_now.count(LEVEL + SPEED) == CUBE**3 - fires[1]
    )
    kept = [line for line in clicks if line.get("event") == "click"]
    intervals = [int(line["interval"]) for line in kept]  # type: ignore[call-overload]
    assert kept and intervals == sorted(intervals) and intervals[-1] <= end
    back, during = 0, []
    board.output = during.append
    for k in range(40):  # (4) the run back through the fires at the top
        board.step_inverse()
        back += same_state(board_state(board), states[end - 1 - k])
    assert back == 40
    assert {s[0] for s in board.swaps if s[1] == -1} == {t for t in fires if t > end - 40}
    assert (
        during == [] and [line for line in clicks if line.get("event") == "click"] == kept
    )  # (5) history kept
    board.output = clicks.append
    whole = 0  # (8) without clicks the whole course runs back bit for bit through every fire
    for k in range(end):
        blind_board.step_inverse()
        whole += same_state(board_state(blind_board), states[end - 1 - k])
    assert whole == end and sorted(s[0] for s in blind_board.swaps if s[1] == -1) == sorted(fires)
    floor = swap.floor_of(
        board.world.node_clock
    )  # the floor (ALGEBRA.md, The floor, 2026-10-23): the former reading ended this small board by the crunch at 78, X at most 0 refused by name; the Node turns at the floor instead and the run goes on
    stood = board.interval  # end - 40 after the run back of (4)
    for _ in range(120):  # past the former crunch at 78
        board.step()
    assert board.interval == stood + 120 > 78
    assert int(np.asarray(time_line().now, dtype=object).min()) >= floor


def test_the_shipped_eras_log_opens_with_the_shipped_worlds_own_readings() -> None:
    shipped = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines()[1:9]]
    board = Lattice(load_world(WORLD))
    board.output = lambda line: None
    lines: list[dict[str, Any]] = []
    for expected in shipped:
        kept = ERAS.kept_lines(board)
        board.step()
        line = ERAS.interval_line(board, kept, 0.0)
        ERAS.volume_residuals(lines[-1] if lines else None, line)
        lines.append(line)
        found, stamped = dict(line), dict(expected)
        found.pop("seconds"), stamped.pop("seconds")
        assert json.loads(json.dumps(found)) == stamped, line[
            "interval"
        ]  # (6) the log is the world's own


def test_the_click_parts_the_course_at_its_first_write_and_the_run_back_reaches_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """(9) The click variant on the small world: the same world with one instrument body at one Node reading the light (the clicks world's absorber, its window derived at load as its own beat, one period of the resonance [902, 1000] in whole intervals, 15, since the standing light has no passage end; the declared 12 the former reading), stepped beside the world without it for 36 intervals: the two courses part BEFORE the first click, at the interval 3, since the instrument is content, one quantum of the absorber family at one Node whose form writes into the time line as every record's does, and the clicks are written on the lattice at the windows' closes 15 and 30 (the credit lines and their lays); the run back from the end is exact at every state to the interval 0 THROUGH the three clicks, every lay at an interval above 0 logged in the books and crossed back (ALGEBRA.md, The click writes on the lattice, The lay's inverse: with the books the board runs back through the click, the click's irreversibility the draw's choice of the future and not the past's recovery), and the clicks are history kept, none written on the run back and none removed, their intervals never decreasing. The reading before the lay's inverse, named: on the tree before it the run back was exact down to the last click's interval and missed first at the state before it."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    plain = Lattice(load_world(small_world(tmp_path, detector=False)))
    plain.output = lambda line: None
    (tmp_path / "click").mkdir()
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path / "click")
    lines: list[dict[str, object]] = []
    clicking = Lattice(
        load_world(small_world(tmp_path / "click", detector=False, absorber=True)), output=lines.append
    )
    end, states, first = 36, {0: board_state(clicking)}, None
    for t in range(1, end + 1):
        plain.step()
        clicking.step()
        states[t] = board_state(clicking)
        plain_state = board_state(plain)
        alike = all(
            same_state([a], [b]) for a, b in zip(states[t][: len(plain_state)], plain_state, strict=True)
        )  # the shared families' lines, the absorber's own left out
        if not alike and first is None:
            first = t
    credits = [int(line["interval"]) for line in lines if line.get("event") == "credit"]  # type: ignore[call-overload]
    assert credits and all(c % 15 == 0 for c in credits), (
        credits
    )  # the clicks at the windows' closes, the derived beat 15
    assert first is not None and first < credits[0], (
        first,
        credits,
    )  # the instrument is content: its one quantum's write parts the courses before any click (the interval 3 here), and the first click is written at 15
    kept = [dict(line) for line in lines if line.get("event") == "credit"]
    during: list[dict[str, object]] = []
    clicking.output = during.append
    back, miss = 0, None
    for k in range(end):
        clicking.step_inverse()
        if same_state(board_state(clicking), states[end - 1 - k]):
            back += 1
        elif miss is None:
            miss = end - 1 - k
    assert (back, miss) == (end, None), (
        back,
        miss,
        credits,
    )  # exact to the interval 0 through the three clicks
    assert during == [] and [dict(line) for line in lines if line.get("event") == "credit"] == kept
    assert credits == sorted(
        credits
    )  # the clicks kept in the books' history, their intervals never decreasing


def test_two_instruments_clicks_counted_by_stage_on_the_small_world(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """(10) The many-clicks reading on the small structured board (the owner's rule: every test of the law's course on a structured board): two instrument bodies at [2, 2, 2] and [0, 2, 0] with the resonances [810, 1000] and [868, 1000], their derived beats 11 and 13 (distinct beats, the two draws on distinct intervals but their common multiples), the course stepped to the interval 70 (the clump's top near 40, the crunch past 77): the clicks written (a transition realised at a window's close) counted by stage, before the board's top and after it, read and not assumed and asserted as read; the clicks are history kept, their intervals never decreasing, and both instruments click."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    lines: list[dict[str, object]] = []
    board = Lattice(
        load_world(small_world(tmp_path, detector=False, absorber=True, resonances=RESONANCES)),
        output=lines.append,
    )
    g = board.held[0]
    volumes = []
    for _ in range(70):
        board.step()
        volumes.append(sum(flat(board.states[g].lines[0].now)))
    top = volumes.index(max(volumes)) + 1
    assert 20 < top < 50, top
    written = [
        (int(line["interval"]), str(line["node_detector"]), str(line["realised"]))  # type: ignore[call-overload]
        for line in lines
        if line.get("event") == "credit" and line.get("before") != line.get("realised")
    ]
    assert written and [w[0] for w in written] == sorted(w[0] for w in written)  # history kept, one way
    assert len({w[1] for w in written}) == 2, written  # both instruments click
    before, after = [w for w in written if w[0] <= top], [w for w in written if w[0] > top]
    assert (len(before), len(after)) == (BEFORE_TOP, AFTER_TOP), (written, top)  # the counts as read
