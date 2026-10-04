"""The one lay act (ALGEBRA.md, No write from outside Rule3 wakes the massless row's zero mode; `src/event_universe/lay.py`): every write from outside Rule3 is one call of `laid`, the division act taking the uniform part out of each level's change, the guard refusing by name a lay that moves one of the two sums, the write step at the lay's Nodes with the remainder at the division's origin and one lay line per written Node."""

import json

import numpy as np

from event_universe import lay
from event_universe.game_board import GameBoard
from event_universe.loader.universe import universe_of
from event_universe.loader.world import bodies_of
from event_universe.world_files import load_world
from tests.laws import EVENTS, TOOL, refused


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
    refused("'light'", lay.guarded, "light", True, 7, 0, lay.IN_SPACE)
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
