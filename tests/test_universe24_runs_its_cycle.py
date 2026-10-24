"""The test of the law's course for Universe24, the one world (examples/events/universe24/; the fold of 2026-10-24, the owner's word: the file is the universe at nature's den, the board's shape and the run's length alone, no body, no detector, no option key; ALGEBRA.md, The one Node, The uniform seed is a lay, The board reads itself, The swap at the top, The carried momentum): (1) the bare file loads with no mode file, its seed the light family; (11) on the small bare torus the seed is one quantum of light on every Node, the board bangs from it and births the electron pairs at the first meeting with the Node's index on the click's line, the books' count the cap; and the declared seed's small structured board of 2026-10-23 (tests/laws_universe.small_world: the 3-cube torus with one clump of matter at the pair [600, 1000], the light family at the uniform level 636 with the velocity 190 and the detector on two Nodes, gravity's gap widened to [990, 1000] so that the course is ten times shorter) kept by name with its readings, (2) to (10): the rise from the seed, the deceleration, the fifth act's fires at the top, the fall, the light's velocity reversed bit for bit at every turned Node, the clicks kept one way through the run back, the detector writing nothing the board reads, the instrument's clicks at the derived cadence 15 and the two instruments' clicks by stage. The former file's own numbers (2026-10-23, six bodies, two instruments, 1,500 intervals) stand in examples/events/universe24/notes.md as the declared seed's reading."""

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


def test_the_fold_accepts_the_bare_world_and_refuses_a_former_key() -> None:
    """(1) The one world's file is the universe, the shape and the run's length alone and parses with no mode file, its seed the light family and no body and no reader (the two keys optional since 2026-10-24, required to then; the declared seed's file of 2026-10-23 named six bodies and an empty node_detectors list); the former key `interval` and the held row's former key `booking` refused by name; the same world naming the two keys as empty lists declares an empty board and is not seeded (the former path, every former test world bit for bit)."""
    world = json.loads(WORLD.read_text(encoding="utf-8"))
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    files = {world["universe"]: universe}
    from event_universe.loader.world import parse_world

    assert (
        set(world) == {"universe", "shape", "intervals"} and not WORLD.with_suffix(".mode.json").exists()
    )
    parsed = parse_world(world, files, input_digest(world))  # (1) the bare world, accepted
    assert parsed.seed is not None and parsed.families[parsed.seed].name == "light"
    assert not parsed.bodies and not parsed.node_detectors and not parsed.packets
    emptied = {
        **world,
        "bodies": [],
        "node_detectors": [],
    }  # an empty board declared: no seed, as before
    assert parse_world(emptied, files, input_digest(emptied)).seed is None
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
    credits = [
        int(line["interval"])  # type: ignore[call-overload]
        for line in lines
        if line.get("event") == "credit" and line.get("before") != line.get("realised")
    ]  # the run's own clicks log: the clicks counted by stage are its lines by stage, the sentence and no literal
    assert (len(before), len(after)) == (
        sum(1 for t in credits if t <= top),
        sum(1 for t in credits if t > top),
    ), (written, top)
    assert (len(before), len(after)) == (BEFORE_TOP, AFTER_TOP), (
        written,
        top,
    )  # the counts as read from the run under the content register (the Boss's word, 2026-10-24: the register the content rooms' alone; at the merge base 3 and 1, the sign holder's W = 0 write room then the register's artefact)


def test_the_bare_torus_is_seeded_with_light_bangs_and_births_the_pairs_at_the_first_meeting(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """(11) The folded sentences on the small bare torus, the 3-cube with the one world's universe at nature's den and nothing declared (ALGEBRA.md, The uniform seed is a lay; The board reads itself; 2026-10-24): the seed is light at one quantum on every Node, the level now the drift 189 (189^2 <= 36,000 < 190^2) and the level before 0, 27 quanta on the board and 27 in the books; the bang from the seed, X rising from Gamma at every Node alike while no birth has parted them; the first meeting, where the light's share reads two whole quanta at a Node, births the proton pair there at the senses -1 and 1 (the heaviest pair within the two quanta's own energy, the law's sentence of 2026-10-24: two whole quanta of light at the top's unit W_c carry at least 2 W_c, the proton pair's walls 1.99175 W_c; the former clause, the lightest within the top's threshold, birthed the electron pair here, 2026-10-23 to 2026-10-24) with the click's line naming the Node's x-major index, every Node alike birthing at once (27 pairs), each paying by the hole at its own Node (everything local, the owner's word of 04:2x UTC), the light's levels then 0 at every Node and its count read 0, the proton's 54; the former cap by the books' count (13 pairs in the lattice's order, the light's count 1) was the one non-local act, removed the same day."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "u.json").write_text(UNIVERSE.read_text(encoding="utf-8"), encoding="utf-8")
    bare = {"universe": "u.json", "shape": [CUBE] * 3, "intervals": 60}
    (path := tmp_path / "bare.json").write_text(json.dumps(bare), encoding="utf-8")
    lines: list[dict[str, Any]] = []
    board = Lattice(load_world(path), output=lines.append)
    names, light = [family.name for family in board.families], board.world.seed
    assert light is not None and names[light] == "light"
    seed = board.states[light].lines[0]
    assert flat(seed.now) == [189] * CUBE**3 and flat(seed.before) == [0] * CUBE**3
    assert flat(board.quanta(light)[0]) == [1] * CUBE**3 and board.credit.counts[light] == CUBE**3
    g = board.held[0]
    xs = lambda: flat(board.states[g].lines[0].now)  # noqa: E731
    assert xs() == [GAMMA] * CUBE**3  # the seed at rest
    births: list[dict[str, Any]] = []
    while not births and board.interval < 60:
        alike = xs()
        board.step()
        births = [line for line in lines if line.get("event") == "birth"]
    assert births and len(set(alike)) == 1 and alike[0] > GAMMA  # the bang, uniform to the birth
    first = births[0]["interval"]
    assert len(births) == CUBE**3 and all(b["interval"] == first for b in births)  # every Node alike
    assert all(b["children"] == ["proton"] * 2 and b["senses"] == [-1, 1] for b in births)
    credits = [line for line in lines if line.get("event") == "credit"]
    assert sorted(c["node_detector"] for c in credits) == list(range(CUBE**3))  # the Nodes by index
    assert all(c["absorbed"] == "light" and c["realised"] == "proton" for c in credits)
    spent = board.states[light].lines[0]  # the record's line after the holes
    assert flat(spent.now) == [0] * CUBE**3 and flat(spent.before) == [0] * CUBE**3  # the holes
    assert board.credit.counts[light] == 0 and board.credit.counts[names.index("proton")] == 2 * CUBE**3
