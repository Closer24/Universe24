"""The hole is the write that takes what the birth books and nothing else (ALGEBRA.md, The board reads itself, the hole's clause of 2026-10-24 on the builder's derivation, #2187; `meeting_board.take_of`, `refused_by`): at a born Node the seed record's before is kept and its now moved toward it, one level at a time, until the frame's seven shares, by the share's own form on the state the write acts on, have fallen by the children's walls summed; the last level's excess named on the birth line; the close refused by name where the full stop would take less than the walls, and, the Boss's default of the same day, where a child's lay would be refused, nothing born and nothing taken either way, the light standing; every face read before any write; the books the board's charge by construction; on the tests' small universe (den 1,021)."""

from __future__ import annotations

import numpy as np

from event_universe import credit, digits, meeting_board, share, world_files
from event_universe.lattice import Lattice
from event_universe.loader import universe
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import bare_torus


def hole_seed(tmp_path, monkeypatch, cube, intervals, lines):  # type: ignore[no-untyped-def]
    """The bare torus of `cube` Nodes a side under the engine's own hole seed, every output line kept."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(
        universe, "volume_pair", lambda den, gamma: (den, den)
    )  # the massless holder, by name
    return Lattice(load_world(bare_torus(tmp_path, cube, intervals)), output=lines.append)


def light_of(board):  # type: ignore[no-untyped-def]
    """The seed family's share summed over the board, in the current's units."""
    return int(np.asarray(board.share_of(board.world.seed)[0], dtype=object).sum())


def watched(monkeypatch):  # type: ignore[no-untyped-def]
    """The light's summed share before and after every close's writes, kept per interval by a spy on the board's own close."""
    real, kept = meeting_board.closed, {}

    def spy(board, begun):  # type: ignore[no-untyped-def]
        before = light_of(board)
        real(board, begun)
        kept[board.interval] = (before, light_of(board))

    monkeypatch.setattr(meeting_board, "closed", spy)
    return kept


def events(lines, kind, interval):  # type: ignore[no-untyped-def]
    return [row for row in lines if row.get("event") == kind and row["interval"] == interval]


def apart(nodes, shape):  # type: ignore[no-untyped-def]
    """Whether no two of the Nodes are one Link apart on the torus."""
    frames = [digits.frame_of(tuple(at), shape, (True, True, True))[1:] for at in nodes]
    return all(
        tuple(b) not in frame for a, frame in zip(nodes, frames, strict=True) for b in nodes if b != a
    )


def test_the_hole_takes_what_the_birth_books_and_makes_nothing_on_the_3_cube(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The hole's clause on the 3-cube over 40 intervals: at every close the light's summed share after the writes is at most the share before (nothing made), and where the born Nodes stand apart the fall equals the births' taken summed, each the children's walls plus an excess at or above 0 and below the last level's step; a refused close with no birth leaves the light standing; the light above zero at every interval and several births; the course's own numbers (18 births, 72 refusals) are the course's and not asserted."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = hole_seed(tmp_path, monkeypatch, 3, 40, lines)
    kept = watched(monkeypatch)
    for _ in range(40):
        board.step()
        assert light_of(board) > 0
    for interval, (before, after) in kept.items():
        births, refused = events(lines, "birth", interval), events(lines, "refused", interval)
        assert after <= before
        assert all(0 <= row["excess"] < row["step"] and row["walls"] > 0 for row in births)
        assert all(row["taken"] == row["walls"] + row["excess"] for row in births)
        if births and apart([row["nodes"][0] for row in births], board.shape):
            assert before - after == sum(row["taken"] for row in births)
        if refused and not births:
            assert after == before and all(
                row["amount"] < row["bound"] for row in refused if row["cause"] == "stop"
            )
    assert sum(len(events(lines, "birth", t)) for t in kept) > 3


def test_the_5_cube_keeps_its_light_above_zero_and_makes_nothing_under_the_takes(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The 5-cube under the exact take for 20 intervals: the light's summed share above zero at every interval, at most the share before after every close's writes, births at several closes and no close holing every Node."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = hole_seed(tmp_path, monkeypatch, 5, 20, lines)
    kept, nodes = watched(monkeypatch), int(np.prod(board.shape))
    for _ in range(20):
        board.step()
        assert light_of(board) > 0
        assert len(events(lines, "birth", board.interval)) < nodes
    assert all(after <= before for before, after in kept.values())
    assert len({row["interval"] for row in lines if row.get("event") == "birth"}) > 3


def test_a_full_stop_that_cannot_pay_refuses_by_name_and_the_light_stands(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The refusal by name (the hole's clause): on the 3-cube at den 1,021 a close whose full stop would take less than the children's walls is logged refused with the cause "stop" and its two numbers, the take below the walls, nothing is born at that close and the light's summed share stands through its writes."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = hole_seed(tmp_path, monkeypatch, 3, 12, lines)
    kept = watched(monkeypatch)
    for _ in range(12):
        board.step()
    stops = [row for row in lines if row.get("event") == "refused" and row["cause"] == "stop"]
    assert stops and all(row["amount"] < row["bound"] for row in stops)
    for row in stops:
        assert not events(lines, "birth", row["interval"])
        assert kept[row["interval"]][0] == kept[row["interval"]][1]


def test_every_take_is_read_before_any_hole_is_written(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """Every face before any write (the hole's clause): within every close of the 3-cube every read of the frame's shares precedes the first hole written, so the takes of a close are read on the one state the write acts on and the order of the Nodes enters no number."""
    board, order = hole_seed(tmp_path, monkeypatch, 3, 16, []), []
    real_read, real_laid = meeting_board.taken_at, meeting_board.laid
    monkeypatch.setattr(
        meeting_board,
        "taken_at",
        lambda *a: (order.append((board.interval, "read")), real_read(*a))[1],
    )
    monkeypatch.setattr(
        meeting_board, "laid", lambda *a: (order.append((board.interval, "write")), real_laid(*a))[1]
    )
    for _ in range(16):
        board.step()
    for interval in {t for t, _kind in order}:
        kinds = [kind for t, kind in order if t == interval]
        assert "write" not in kinds or kinds.index("write") > max(
            i for i, k in enumerate(kinds) if k == "read"
        )
    assert any(kind == "write" for _t, kind in order)


def test_nothing_is_booked_without_its_lay_and_the_first_births_charge_is_the_books(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The Boss's default of 2026-10-24: a close whose children's lay would be refused births nothing and takes nothing, so no quantum is booked without its lay: on the 3-cube over 40 intervals every charged family's deficit stays 0 and its books count the children its birth lines name, the refusals of the cause "lay" name a share above the unit, and at a family's first birth the charge read from the board (`credit.count_of`, over T div 2) equals the books. Measured and named, not asserted: a lay onto a Node where the family's earlier wave stands below one unit superposes with it and the Wronskian's cross terms move the charge off the count (the eight corners at the close 16: the charge 24 against the books' 20), the architect's open sentence (FURTHER_RESEARCH.md)."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = hole_seed(tmp_path, monkeypatch, 3, 40, lines)
    charged, first = [k for k in board.order if share.charged(board.families[k])], {}
    for _ in range(40):
        board.step()
        for k in charged:
            name, births = board.families[k].name, [row for row in lines if row.get("event") == "birth"]
            laid = sum(row["children"].count(name) for row in births)
            assert board.credit.deficits.get(k, 0) == 0 and board.credit.counts[k] == laid, (
                board.interval
            )
            if laid and k not in first:
                first[k] = credit.count_of(board, k) == laid
    lays = [row for row in lines if row.get("event") == "refused" and row["cause"] == "lay"]
    assert first and all(first.values()) and lays and all(row["amount"] > row["bound"] for row in lays)


def test_the_first_draw_by_the_digits_falls_at_a_share_between_one_and_two_quanta_and_writes_its_credit(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The Born side (ALGEBRA.md, The board reads itself): on the 3-cube the first meeting met by the draw and not refused stands at one whole quantum with a remainder above zero and below the unit, the draw's weights are that remainder against the unit less it, and the close writes the credit line and the birth line at that Node."""
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
    credited = []
    while not credited and board.interval < 40:
        board.step()
        for interval, label, weights, port in draws:
            if port == 0 and interval == board.interval:
                at = next(a for a, _w, _r in meetings[interval] if str(list(a)) in label)
                place = int(np.ravel_multi_index(at, board.shape))
                if any(row["node_detector"] == place for row in events(lines, "credit", interval)):
                    credited.append((interval, at, weights))
    interval, at, weights = credited[0]
    whole, rest = next((w, r) for a, w, r in meetings[interval] if a == at)
    assert whole == 1 and 0 < rest < unit and weights == [rest, unit - rest]
    assert any(list(at) in row["nodes"] for row in events(lines, "birth", interval))


def test_the_run_back_is_exact_through_the_closes_that_hole(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The hole's write is a lay logged in the books and undone by the run back as every lay is (ALGEBRA.md, The lay's inverse): eight intervals of the 3-cube hole seed forward through its first close and back, every state the forward run's bit for bit."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = hole_seed(tmp_path, monkeypatch, 3, 12, lines)
    states = [board_state(board)]
    for _ in range(8):
        board.step()
        states.append(board_state(board))
    assert any(row.get("event") == "birth" for row in lines)
    back = 0
    for k in range(8):
        board.step_inverse()
        back += same_state(board_state(board), states[7 - k])
    assert (back, board.interval) == (8, 0)
