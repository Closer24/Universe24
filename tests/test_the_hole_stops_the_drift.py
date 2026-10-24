"""The board's own hole is the Node's own level before, twice: the quantum is the drift, the write stops it (ALGEBRA.md, The board reads itself, the dated sentence of 2026-10-24 on the Boss's ruling over the bound-click hand's measurement; `meeting_board.stopped_at`): the seed's record at a meeting Node keeps the level it had before the interval's drift and drifts no more, the write reading nothing but the Node's own two levels, so that the Node's own quanta pay, nothing is made at the Links, and a hole on the uniform sea is the seed's own origin; on the tests' small universe (den 1,021) and the bare torus under the engine's own hole seed."""

from __future__ import annotations

import numpy as np

from event_universe import meeting_board, records, seed, world_files
from event_universe.lattice import Lattice
from event_universe.loader import universe
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import bare_torus, uniform_sea


def hole_seed(tmp_path, monkeypatch, cube, intervals, lines):  # type: ignore[no-untyped-def]
    """The bare torus of `cube` Nodes a side under the engine's own hole seed, every output line kept."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(
        universe, "volume_pair", lambda den, gamma: (den, den)
    )  # the massless holder, by name
    return Lattice(load_world(bare_torus(tmp_path, cube, intervals)), output=lines.append)


def light_of(board):  # type: ignore[no-untyped-def]
    """The seed family's share summed over the board, and its share per Node, in the current's units."""
    found = np.asarray(board.share_of(board.world.seed)[0], dtype=object)
    return int(found.sum()), found


def watched(monkeypatch):  # type: ignore[no-untyped-def]
    """The light's summed share before and after every close's writes, kept per interval by a spy on the board's own close."""
    real, kept = meeting_board.closed, {}

    def spy(board, begun):  # type: ignore[no-untyped-def]
        before = light_of(board)[0]
        real(board, begun)
        kept[board.interval] = (before, light_of(board)[0])

    monkeypatch.setattr(meeting_board, "closed", spy)
    return kept


def births_at(lines, interval):  # type: ignore[no-untyped-def]
    return [
        tuple(row["nodes"][0])
        for row in lines
        if row.get("event") == "birth" and row["interval"] == interval
    ]


def test_the_holed_nodes_own_quanta_pay_and_nothing_is_made_at_the_links_on_the_3_cube(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """Conservation at the click and no cascade on the 3-cube (ALGEBRA.md, The board reads itself, the dated sentence of 2026-10-24: the Node's own quanta paying, the owner's point that the entanglement of clicks is the conservation of energy at a click): at every close the light's summed share after the hole's write is at most its share before (nothing made at the Links), at a close with a birth it falls (the pair paid by the light; the fall's size is the course's and not the law's: the close reads the interval's start and the hole is written on the state the step left, so a Node read at three whole quanta may have moved most of them to its Links by the write), and every hole stands at a Node the close read a whole quantum at (no cascade: a Node is holed by its own meeting alone, an orbit of the cube's 48 meeting together where its Nodes read one number); the light's summed share above zero at every interval and several births over the run (the former write to (0, 0) made 7.68 quanta at the first close, holed 1, 7, 18 and 20 Nodes at the closes 2 to 5 and spent the sea to exactly zero; the frame's mean of the level before, measured between, took 2.09 at the first close and made light between adjacent holes on the 5-cube)."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = hole_seed(tmp_path, monkeypatch, 3, 40, lines)
    kept, born, met = watched(monkeypatch), {}, {}
    real = meeting_board.meetings
    monkeypatch.setattr(
        meeting_board, "meetings", lambda b, i, s, f: met.setdefault(b.interval, real(b, i, s, f))
    )
    for _ in range(40):
        board.step()
        born[board.interval] = births_at(lines, board.interval)
        assert light_of(board)[0] > 0
        assert all(any(at == a for a, _w, _r in met[board.interval]) for at in born[board.interval])
    for interval, (before, after) in kept.items():
        assert after <= before and (
            after < before or not born[interval]
        )  # paid by the light, nothing made
    assert sum(len(found) for found in born.values()) > 3


def test_the_5_cube_keeps_its_light_above_zero_under_the_holes(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The 5-cube under the same hole for 20 intervals: the light's summed share above zero at every interval where the former write spent it to exactly zero by the end of 8, births at several closes and no close holing every Node; the write makes no light at any close, where the frame's mean of the level before made 10 to 172 quanta per close at the closes 5 to 10 between adjacent holes each written to its own frame (the 60-interval runs, 131 births against 405, named in ALGEBRA.md's dated sentence)."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = hole_seed(tmp_path, monkeypatch, 5, 20, lines)
    nodes = int(np.prod(board.shape))
    for _ in range(20):
        board.step()
        assert light_of(board)[0] > 0
        assert len(births_at(lines, board.interval)) < nodes
    assert len({row["interval"] for row in lines if row.get("event") == "birth"}) > 3


def test_a_hole_on_the_uniform_sea_is_the_seeds_own_origin(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The seed is untouched and the hole is its form (ALGEBRA.md, The uniform seed is a lay; The board reads itself, the dated sentence): the seed lays (v, 0) at every Node but the origin, (0, 0), and `stopped_at` on the seed's own state at the origin returns (0, 0), the seed's hole; on the uniform sea by name (every Node at the drift, no hole) stepped three intervals, the sea drifts by v at every Node and `stopped_at` at any Node returns the Node's level before twice, so a hole written there is the seed's kink exactly: the Node at the level it had before this interval's drift, the drift stopped, one quantum absent (the six Ports' mean of both levels, the first form measured, returns the Node's own levels on a uniform frame and so writes nothing there, kept by name)."""
    board = hole_seed(tmp_path, monkeypatch, 3, 4, [])
    light = board.world.seed
    first = records.record_slice(board.families[light], 0).start
    line, drift = board.states[light].lines[first], seed.drift_of(board.world.quantum_action)
    assert (int(line.now[seed.ORIGIN]), int(line.before[seed.ORIGIN])) == (0, 0)
    assert (int(line.now[1, 2, 0]), int(line.before[1, 2, 0])) == (drift, 0)
    assert meeting_board.stopped_at(board, light, first, seed.ORIGIN) == (0, 0)
    monkeypatch.setattr(seed, "uniform_seed", uniform_sea)
    sea = hole_seed(tmp_path, monkeypatch, 3, 4, [])
    for _ in range(3):
        sea.step()
    line, at = sea.states[light].lines[first], (1, 2, 0)
    level = int(line.before[at])
    assert int(line.now[at]) - level == drift
    assert meeting_board.stopped_at(sea, light, first, at) == (level, level)


def test_the_first_draw_by_the_digits_falls_at_a_share_between_one_and_two_quanta_and_writes_its_credit(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The Born side (ALGEBRA.md, The board reads itself: where one whole quantum stands with a share above it, the second quantum is the click's whether, drawn by the Node's read of itself and its Links): on the 3-cube the first meeting met by the draw stands at one whole quantum with a remainder above zero and below the unit, the draw's weights are that remainder against the unit less it, and the close writes the credit line and the birth line at that Node (the former write to (0, 0) left every meeting at two whole quanta or more, no draw on either seed)."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = hole_seed(tmp_path, monkeypatch, 3, 40, lines)
    unit, meetings, draws = board.credit.units[board.world.seed], {}, []
    real_meetings, real_drawn = meeting_board.meetings, meeting_board.drawn_from

    def drawn(number, weights, label, read):  # type: ignore[no-untyped-def]
        found = real_drawn(number, weights, label, read)
        draws.append((board.interval, label, list(weights), found[0]))
        return found

    monkeypatch.setattr(
        meeting_board,
        "meetings",
        lambda b, i, s, f: meetings.setdefault(b.interval, real_meetings(b, i, s, f)),
    )
    monkeypatch.setattr(meeting_board, "drawn_from", drawn)
    while not any(port == 0 for _i, _l, _w, port in draws) and board.interval < 40:
        board.step()
    interval, label, weights, port = next(draw for draw in draws if draw[3] == 0)
    at = next(at for at, whole, rest in meetings[interval] if str(list(at)) in label)
    whole, rest = next((whole, rest) for a, whole, rest in meetings[interval] if a == at)
    assert whole == 1 and 0 < rest < unit and weights == [rest, unit - rest]
    place = int(np.ravel_multi_index(at, board.shape))
    credits = [row for row in lines if row.get("event") == "credit" and row["interval"] == interval]
    assert any(row["node_detector"] == place and row["count"] == 1 for row in credits)
    assert at in births_at(lines, interval)


def test_the_run_back_is_exact_through_the_closes_that_hole(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The hole's write is a lay logged in the books and undone by the run back as every lay is (ALGEBRA.md, The lay's inverse): eight intervals of the 3-cube hole seed forward through several closes that hole and birth, then eight back, every family's lines and write remainders equal bit for bit at every interval and the interval back at 0."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = hole_seed(tmp_path, monkeypatch, 3, 12, lines)
    states = [board_state(board)]
    for _ in range(8):
        board.step()
        states.append(board_state(board))
    assert sum(1 for row in lines if row.get("event") == "birth") >= 2
    back = 0
    for k in range(8):
        board.step_inverse()
        back += same_state(board_state(board), states[7 - k])
    assert (back, board.interval) == (8, 0)
