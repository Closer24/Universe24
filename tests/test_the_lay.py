"""The one lay act (ALGEBRA.md, No write from outside Rule3 wakes the massless row's zero mode; `src/event_universe/lay.py`): every write from outside Rule3 is one call of `laid`, the division act taking the uniform part out of each level's change, the guard refusing by name a lay that moves one of the two sums, the write step at the lay's Nodes with the remainder at the division's origin and one lay line per written Node."""

import json

import numpy as np
import pytest

from event_universe import lay, meeting, world_files
from event_universe.game_board import GameBoard
from event_universe.loader.universe import universe_of
from event_universe.loader.world import bodies_of
from event_universe.world_files import load_world
from tests.laws import (
    BACK,
    EVENTS,
    TOOL,
    ion_world,
    link_distance,
    packet_box,
    packet_world,
    refused,
    slit_world,
)


def test_the_division_act_keeps_the_two_sums_and_the_guard_refuses_a_lay_that_moves_one():
    """The principle's one division act (ALGEBRA.md, The message lay (h); `lay.division_act`, `lay.shares_of`, `lay.corrected`, `lay.guarded`): a level summing to 7 over four Nodes weighted 1, 3, 3, 1 has -7 divided back floor by floor, (-1, -3, -3, -1) short by one unit, the leftover to the heaviest Node first, so the level [1, 4, 3, -1] is laid as [0, 2, 0, -2] and sums to 0; a level summing to 0 as it stands, or weighted nowhere, is returned as it is; the guard: a massless lay whose weights carry nothing refuses by name with the family and the two changes, a gapped family's lay and a lay handed no weights are laid as given, and in time the span's increments are kept at the sum 0 and the first moment 0 (`lay.laid_in_time`, the branch's division act in time bit for bit, `lay.division_act_in_time`). The shipped two slits' mode file is the generator's through the act, bit for bit."""
    level, weights = np.array([1, 4, 3, -1], dtype=object), np.array([1, 3, 3, 1], dtype=object)
    assert lay.shares_of(-7, [1, 3, 3, 1]) == [-1, -2, -3, -1]
    assert list(lay.division_act(level, weights)) == [0, 2, 0, -2]
    assert lay.division_act(level - level, weights) is not None and list(
        lay.division_act(level, weights * 0)
    ) == [1, 4, 3, -1]
    now, before = lay.corrected("light", True, (level, level * 2), weights)
    assert (int(now.sum()), int(before.sum())) == (0, 0) and list(before) == [0, 3, 1, -4]
    refused("wakes the zero mode", lay.corrected, "light", True, (level, level), weights * 0)
    refused("'light'", lay.guarded, "light", True, 7, 0, False)
    assert (
        lay.corrected("matter", False, (level, level), weights)[0] is level
    )  # a gapped family: as given
    assert (
        lay.corrected("light", True, (level, level), None)[1] is level
    )  # no weights: laid as built, named
    fixed = lay.laid_in_time("light", True, [73, 49, -8, -60], [55, 55, 54, 54])
    assert sum(fixed) == 0 and sum(t * d for t, d in enumerate(fixed)) == 0
    assert lay.laid_in_time("matter", False, [73, 49, -8, -60], [55, 55, 54, 54]) == [73, 49, -8, -60]
    world = EVENTS / "two_slits" / "two_slits.json"
    shipped = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))
    document = json.loads(world.read_text(encoding="utf-8"))
    assert TOOL.pixel_mode(document)["messages"] == shipped["messages"]


def test_the_write_step_lays_at_the_nodes_with_the_remainder_at_the_origin_and_one_lay_line_each(
    tmp_path,
):
    """The write step of the act (`lay.laid`, `lay.written`): on the Zeno box without bodies a massless record's change of (+5, -5) at two Nodes and (+2, -2) before them, weighted alike, adds the levels, leaves the two sums as it found them, sets the remainder of every written Node to the origin it is handed (the half wall, a Node moved off it included where the lay names it) and reports one lay line per written Node with [now, before, remainder] before and after; a Node named by the lay with no change and its remainder at the origin reports none; the faced Node is left to the faces."""
    world = json.loads((EVENTS / "zeno" / "zeno_1.json").read_text(encoding="utf-8"))
    world.update(bodies=[], messages=[], node_readers=[], ticks=4)
    (path := tmp_path / "box.json").write_text(json.dumps(world), encoding="utf-8")
    board = GameBoard(load_world(path), (lines := []).append)
    pulse = [f.name for f in board.families].index("pulse")
    half, record = board.half_wall(pulse), board.states[pulse].lines[0]
    first, second, third = (2, 2, 1), (3, 2, 1), (4, 2, 1)
    record.remainder[third] = 0  # a Node off the origin, named by the lay with no change
    now, before, weights = (np.zeros(board.shape, dtype=object) for _ in range(3))
    now[first], now[second], before[first], before[second] = 5, -5, 2, -2
    weights[first] = weights[second] = 3
    named = np.zeros(board.shape, dtype=bool)
    named[first] = named[second] = named[third] = True
    lay.laid(board, pulse, 0, (now, before), weights, half, named)
    line = board.states[pulse].lines[0]
    assert (int(line.now[first]), int(line.now[second]), int(line.before[first])) == (5, -5, 2)
    assert int(line.now.sum(dtype=object)) == 0 and int(line.before.sum(dtype=object)) == 0
    assert int(line.remainder[third]) == half and (line.remainder == half).all()
    assert [(c["node"]["at"], c["before"], c["after"]) for c in lines] == [
        ([2, 2, 1], [0, 0, half], [5, 2, half]),
        ([3, 2, 1], [0, 0, half], [-5, -2, half]),
        ([4, 2, 1], [0, 0, 0], [0, 0, half]),
    ]
    faced = np.zeros(board.shape, dtype=bool)
    faced[first] = True
    lay.laid(board, pulse, 0, (-now, -before), weights, half, None, faced)
    assert (int(line.now[first]), int(board.states[pulse].lines[0].now[second])) == (5, 0)
    assert len(lines) == 4 and lines[-1]["node"]["at"] == [3, 2, 1] and lines[-1]["line"] == 0


def test_the_loader_refuses_a_source_in_time_below_its_period_naming_the_least_admitted_span():
    """The span condition (ALGEBRA.md, No write from outside Rule3 wakes the massless row's zero mode, the engine's declared problem 2; `loader/node_reader_declaration.holding_period`, `giving.holds_period`): the resonance world's giver at [2, 3] with the lifetime 4 is refused by name, the least admitted span 8 (tau Omega >= 2 pi, num / den <= cos(2 pi / tau) by the rotation act), and admitted at 8; a giving at [5414, 6000] needs 15."""
    world = json.loads((EVENTS / "resonance" / "resonant.json").read_text(encoding="utf-8"))
    universe = json.loads((EVENTS / "zeno" / "zeno_atom.json").read_text(encoding="utf-8"))
    families, action = universe_of(universe)[1], universe["integers"]["quantum_action"]
    shape = tuple(world["shape"])

    def rows(lifetime, resonance):
        body = json.loads(json.dumps(world["bodies"][0]))
        body["rates"][0]["lifetime"] = lifetime
        body["transitions"][0]["resonance"] = resonance
        return [body]

    refusal = refused(
        "least admitted span is 8",
        bodies_of,
        rows(4, [2, 3]),
        None,
        "",
        families,
        shape,
        9000,
        (),
        action,
    )
    assert "lifetime 4" in str(refusal) and "[2, 3]" in str(refusal)
    assert bodies_of(rows(8, [2, 3]), None, "", families, shape, 9000, (), action)[0].reader is not None
    refused(
        "least admitted span is 15",
        bodies_of,
        rows(14, [5414, 6000]),
        None,
        "",
        families,
        shape,
        9000,
        (),
        action,
    )


@pytest.mark.parametrize("door", ["the loader's lay", "the source in time", "the open board's packet"])
def test_every_door_leaves_the_two_sums_and_the_gate_reads_match_across_its_lay(
    door, tmp_path, monkeypatch
):
    """Every door of the act on a massless record changes the two sums by 0 and the back-in-time gate reads MATCH across it (ALGEBRA.md, No write from outside Rule3 wakes the massless row's zero mode: the loader's lay of the file's levels, `GameBoard.lay`; the source in time's increments over its span, `giving.given_quantum`; the open board's packet, `giving.laid_packet`): the act's change read from its lay lines (the loader's lay has none, the sums themselves 0 at the start), the division act's leftover units among them, since `lay.written` is the one place that writes a level from outside Rule3 and the host's tool crosses every write from the lay lines."""
    if door == "the loader's lay":  # the scratch world beside its universe
        monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
        path, name, intervals = slit_world(tmp_path, TOOL), "charge", 6
    elif door == "the source in time":
        path, name, intervals = EVENTS / "resonance" / "resonant.json", "pulse", 92
    else:
        path, name, intervals = packet_world(tmp_path, TOOL), "pulse", 20
    board = GameBoard(load_world(path), (lines := []).append)
    index = [f.name for f in board.families].index(name)
    assert not lines and board.families[index].pair[0] == board.families[index].pair[1]
    line = board.states[index].lines[0]
    assert (int(line.now.sum(dtype=object)), int(line.before.sum(dtype=object))) == (0, 0)
    for _ in range(intervals):
        board.step()
    lays = [c for c in lines if c["event"] == "lay" and c["family"] == name]
    assert (door == "the loader's lay") == (not lays)
    assert [sum(c["after"][k] - c["before"][k] for c in lays) for k in (0, 1)] == [0, 0]
    assert BACK.verdict(GameBoard(load_world(path)), intervals)["verdict"] == "MATCH"


def test_the_restoring_front_keeps_the_telegraph_like_worlds_mean_level_within_a_few_units(
    tmp_path, monkeypatch
):
    """The restoring front, the hole's local form (ALGEBRA.md, The click writes on the GameBoard (6); `front.restoring`, `front.restored`, `meeting.written`): on the ion-like world, a periodic box of 192 Nodes with the drive's record of 1,171 quanta taken by the ion over 170 intervals (three takings, the last after the interval 100), every front in the books is a restoring one, the drive's count stands, and the drive's mean level over the board stays within 5 units through the run (4.7 at most), where the engine without the restoring front drifts to -403 by the interval 170 (the hole's uniform mode standing until the last taking, the engine's declared problem 3); the fluorescence, given and never taken here, within one unit."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = GameBoard(load_world(ion_world(tmp_path, TOOL, ticks=170)), (lines := []).append)
    names = [f.name for f in board.families]
    drive, light = names.index("strong_drive"), names.index("fluorescence")
    means: dict[int, list[float]] = {drive: [], light: []}
    for _ in range(170):
        board.step()
        for index, found in means.items():
            found.append(int(board.states[index].lines[0].now.sum(dtype=object)) / 192)
        assert all(f.restoring is not None for f in board.credit.fronts)  # no count reached 0
    taken = [c for c in lines if c["event"] == "credit" and c["taken"] == "strong_drive"]
    assert len(taken) >= 3 and taken[-1]["tick"] > 100 and board.credit.counts[drive] >= 1
    assert max(abs(m) for m in means[drive]) <= 5, max(abs(m) for m in means[drive])
    assert max(abs(m) for m in means[light]) <= 1


def test_the_restoring_front_writes_at_its_reach_and_restores_the_velocity_sum_exactly(
    tmp_path, monkeypatch
):
    """The restoring front's three clauses (ALGEBRA.md, The restoring front, the hole's local form; `front.scheduled`, `front.content_of`, `features/click.Hole.kicks`): a packet of 22 quanta on the periodic box of 8 by 6 by 4 takes one hole by hand at the interval 5 at (4, 2, 1), the count 21, beside its twin without the hole. Locality: every share is written at the interval of the front's reach, the lay line's Node at the Link distance exactly t - 5 - 1 from the hole at the interval t, the first at 7 (one interval behind the causal bound, as the erasure is), none beyond and none at the hole's Node, the faces'. The sums: the two faces' kicks, R_face (value - arrival) each, change the velocity invariant w (SUM now - SUM before) + SUM r by -39 w here, where the law's nominal -(now_i - before_i) is -41 (over 25 holes on this packet the nominal misses the faces' own change by up to 162 units, so the content is the faces'); once the front has ended the invariant equals the twin's exactly and stays so over 40 intervals, while the level sums differ from the twin's by one constant uniform level, about (now_i - before_i) times the restoration's mean delay over the Nodes (within 3 units of the mean, the offset printed), moving only by the remainders' walk."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = packet_box(tmp_path, TOOL)
    board, twin = GameBoard(load_world(path), (lines := []).append), GameBoard(load_world(path))
    index, at, nodes = [f.name for f in board.families].index("fluorescence"), (4, 2, 1), 192
    wall = 2 * board.half_wall(index)

    def sums(b):
        line = b.states[index].lines[0]
        now, before, rest = (int(a.sum(dtype=object)) for a in (line.now, line.before, line.remainder))
        return now, before, wall * (now - before) + rest

    for _ in range(5):
        board.step(), twin.step()
    line = board.states[index].lines[0]
    taken = (int(line.now[at]), int(line.before[at]))
    meeting.written(board, [meeting.Item(index, None, None, -1, (at,))])
    (front,) = board.credit.fronts
    assert front.restoring is not None and board.credit.counts[index] == 21 and taken == (-46, -87)
    kicks: list[int] = []
    while board.credit.fronts:
        board.step(), twin.step()
        if board.tick == 7:
            kicks = [k for hole in front.restoring.holes[0] for k in hole.kicks]
            assert len(kicks) == 2 and sums(board)[2] - sums(twin)[2] == sum(kicks)  # the faces' own
    assert sum(kicks) == -39 * wall and -(taken[0] - taken[1]) == -41  # the law's nominal, missed by 2
    lays = [c for c in lines if c["event"] == "lay"]
    assert lays and {c["tick"] for c in lays} <= set(range(7, board.tick + 1))
    assert all(link_distance(c["node"]["at"], at, (8, 6, 4)) == c["tick"] - 5 - 1 for c in lays)
    assert all(tuple(c["node"]["at"]) != at for c in lays)
    offsets = []
    for _ in range(40):
        board.step(), twin.step()
        mine, its = sums(board), sums(twin)
        assert mine[2] == its[2]  # the velocity invariant restored exactly
        offsets.append((mine[0] - its[0], mine[1] - its[1]))
    spread = max(o[0] for o in offsets) - min(o[0] for o in offsets)
    assert spread <= 2 * nodes, spread  # the remainders' walk
    assert all(abs(o[0]) <= 3 * nodes and abs(o[1]) <= 3 * nodes for o in offsets), offsets[-1]
