"""The one lay act (ALGEBRA.md, No write from outside Rule3 wakes the massless row's zero mode; `src/event_universe/lay.py`): every write from outside Rule3 is one call of `laid`, the division act taking the uniform part out of each level's change, the guard refusing by name a lay that moves one of the two sums, the write step at the lay's Nodes with the remainder at the division's origin and one lay line per written Node."""

import json

import numpy as np
import pytest

from event_universe import lay, world_files
from event_universe.lattice import Lattice
from event_universe.loader.derived import count_wall
from event_universe.loader.universe import universe_of
from event_universe.loader.world import bodies_of
from event_universe.world_files import load_world
from tests.laws import (
    BACK,
    EVENTS,
    TOOL,
    ion_world,
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
    board = Lattice(load_world(path), (lines := []).append)
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
    """Every door of the act on a massless record changes the two sums by 0 and the back-in-time gate reads MATCH across it (ALGEBRA.md, No write from outside Rule3 wakes the massless row's zero mode: the loader's lay of the file's levels, `Lattice.lay`; the source in time's increments over its span, `giving.given_quantum`; the open board's packet, `giving.laid_packet`): the act's change read from its lay lines (the loader's lay has none, the sums themselves 0 at the start), the division act's leftover units among them, since `lay.written` is the one place that writes a level from outside Rule3 and the host's tool crosses every write from the lay lines."""
    if door == "the loader's lay":  # the scratch world beside its universe
        monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
        path, name, intervals = slit_world(tmp_path, TOOL), "charge", 6
    elif door == "the source in time":
        path, name, intervals = EVENTS / "resonance" / "resonant.json", "pulse", 112  # the giving at 61
    else:
        path, name, intervals = packet_world(tmp_path, TOOL), "pulse", 20
    board = Lattice(load_world(path), (lines := []).append)
    index = [f.name for f in board.families].index(name)
    assert not lines and board.families[index].pair[0] == board.families[index].pair[1]
    line = board.states[index].lines[0]
    assert (int(line.now.sum(dtype=object)), int(line.before.sum(dtype=object))) == (0, 0)
    for _ in range(intervals):
        board.step()
    lays = [c for c in lines if c["event"] == "lay" and c["family"] == name]
    assert (door == "the loader's lay") == (not lays)
    assert [sum(c["after"][k] - c["before"][k] for c in lays) for k in (0, 1)] == [0, 0]
    assert BACK.verdict(Lattice(load_world(path)), intervals)["verdict"] == "MATCH"


def test_a_taking_writes_nothing_on_a_dense_record_and_the_books_carry_the_deficit(
    tmp_path, monkeypatch
):
    """The undepleted beam (ALGEBRA.md, The click writes on the lattice; the two hands' line at the owner's word for the simple solution; `meeting.faced`, `credit.Books.deficits`, `Lattice.books`): on the ion-like world, a periodic box of 8 by 6 by 5 (one odd extent, so that the staggered mode (-1)^(x + y + z + t), the band's top, is no exact mode of the board), the drive's record of several quanta per Node (its booked share at the ion's two Nodes above its quantum W_rec) is taken by the ion over 170 intervals: no face is booked for the drive and no front begins from it, its three arrays stand bit for bit as the twin's without the ion at every interval (the drive reads no holder, so its step is the same Rule3), its four sums (plain and staggered of now and before, sigma = (-1)^(x + y + z) over the board) and its largest level printed with the twin's and equal; the books' count down by one per taking, the deficit the takings' count and the share in quanta the count plus the deficit within the share's drift over the run in quanta (the books' `drift`, Rule3's own rounding, over W_c, and one quantum of the reading's rounding; the books' line and the tolerance printed); the back-in-time gate reads MATCH over the run across the takings, the ion's lays crossed from their lines."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path, alone = (ion_world(tmp_path, TOOL, ticks=170, body=body) for body in (True, False))
    board, twin = Lattice(load_world(path), (lines := []).append), Lattice(load_world(alone))
    drive = [f.name for f in board.families].index("strong_drive")
    unit, count, region = board.credit.units[drive], board.credit.counts[drive], ((3, 3, 2), (4, 3, 2))
    taken = board.mask(region)
    assert int(board.share_of(drive, 1, taken)[0][taken].min()) > unit  # dense at the ion's two Nodes
    sigma = (-1) ** np.indices(board.shape).sum(axis=0)

    def read(b):
        line = b.states[drive].lines[0]
        sums = [int((s * a).sum(dtype=object)) for a in (line.now, line.before) for s in (1, sigma)]
        return sums, int(np.abs(line.now).max()), (line.now, line.before, line.remainder)

    for _ in range(170):
        board.step(), twin.step()
        mine, its = read(board), read(twin)
        assert mine[:2] == its[:2]
        assert all(np.array_equal(a, b) for a, b in zip(mine[2], its[2], strict=True))
    takings = [c for c in lines if c["event"] == "credit" and c["taken"] == "strong_drive"]
    books, its_books = board.books()["strong_drive"], twin.books()["strong_drive"]
    print(
        f"the drive's sums [now, staggered now, before, staggered before] {mine[0]} and the twin's {its[0]}"
    )
    print(
        f"the largest level {mine[1]} and {its[1]}, {len(takings)} takings, the books {books}, the twin's {its_books}"
    )
    assert len(takings) >= 2 and not any(
        f.family == drive for fs in board.credit.faces.values() for f in fs
    )
    assert all(f.family != drive for f in board.credit.fronts)
    assert (books["count"], books["deficit"]) == (count - len(takings), len(takings))
    wall = count_wall(board.families[drive], board.world.quantum_action)
    within = abs(books["drift"]) // wall + 1  # the share's drift in quanta and the reading's rounding
    print(f"the share in quanta {books['quanta']} against the count plus the deficit within {within}")
    assert books["quanta"] == its_books["quanta"] and books["drift"] == its_books["drift"]
    assert abs(books["quanta"] - books["count"] - books["deficit"]) <= within
    assert BACK.verdict(Lattice(load_world(path)), 169)["verdict"] == "MATCH"
