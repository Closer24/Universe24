"""THE SUPPORT-ONLY STEP, A SHORTCUT OF THE HOST (the model owner's question of 2026-09-25
through the Boss, record 2039: "can we shorten the run somehow?"; BUILD.md section 26 item
43): a record's rows are zero outside its box, the box grows by one Link per interval, the
one rule is evaluated on the grown box and zeros are written elsewhere. The law is untouched
(the same integers at every Node); the tests say so bit for bit: (1) the emitter's chain run
600 intervals with the boxes and without gives the same lines, the same rows, remainders and
boxes' complements zero; (2) a planted record with random rows near a corner of a periodic
board, wrapping every axis as its box grows, steps forward 40 and back 40 the same with the
boxes and without, and returns to its rows; (3) the invariant: outside a record's box its two
levels and its remainder are zero at every interval. HOST cost only; no physics."""

from __future__ import annotations

import numpy as np

from event_universe.events.detector_law import UNIT, DetectorLawSimulation
from event_universe.events.world import parse_nature_beam_world
from tests.test_body_record import PERIODIC
from tests.test_emitter import emitter_world
from tests.test_flux_reading import planted
from tests.test_massive_record import block_world


def without_boxes(monkeypatch) -> None:
    """Every record's box the whole board: the whole-board step, as before item 43."""
    monkeypatch.setattr(DetectorLawSimulation, "support_box", staticmethod(lambda *arrays: None))


def outside_is_zero(simulation: DetectorLawSimulation) -> None:
    for live in simulation.records.values():
        if live.box is None:
            continue
        mask = np.ones(simulation.shape, dtype=bool)
        mask[tuple(slice(lo, hi) for lo, hi in live.box)] = False
        assert (
            not live.now[mask].any() and not live.before[mask].any() and not live.remainder[mask].any()
        )


def test_the_emitter_chain_steps_the_same_with_the_boxes_and_without(monkeypatch) -> None:
    document = emitter_world(stock=6, ticks=600)
    with_lines: list[dict] = []
    boxed = DetectorLawSimulation(parse_nature_beam_world(document), observer=with_lines.append)
    for _ in range(600):
        boxed.step()
        outside_is_zero(boxed)
    assert any(live.box is not None for live in boxed.records.values()) or with_lines
    without_boxes(monkeypatch)
    plain_lines: list[dict] = []
    plain = DetectorLawSimulation(parse_nature_beam_world(document), observer=plain_lines.append)
    for _ in range(600):
        plain.step()
    assert all(live.box is None for live in plain.records.values())
    assert with_lines == plain_lines and len(with_lines) > 20
    assert sorted(boxed.records) == sorted(plain.records)
    for identity, live in boxed.records.items():
        other = plain.records[identity]
        assert np.array_equal(live.now, other.now)
        assert np.array_equal(live.before, other.before)
        assert np.array_equal(live.remainder, other.remainder)
        assert live.pointers == other.pointers and live.absorbed == other.absorbed


def test_a_record_wrapping_a_periodic_board_steps_and_returns_the_same(monkeypatch) -> None:
    document = block_world([14, 10, 6], PERIODIC, [800, 809], [], ticks=100)
    document["age_bound"] = 100000  # a periodic board keeps every ray: the store's bound
    rng = np.random.default_rng(43)
    now = np.zeros((14, 10, 6), dtype=np.int64)
    before = np.zeros((14, 10, 6), dtype=np.int64)
    now[11:14, 0:2, 4:6] = rng.integers(-UNIT, UNIT, size=(3, 2, 2))
    before[11:14, 0:2, 4:6] = rng.integers(-UNIT, UNIT, size=(3, 2, 2))
    boxed = DetectorLawSimulation(parse_nature_beam_world(document))
    live = planted(boxed, 0, now.copy(), before.copy(), np.zeros(now.shape, dtype=np.int64))
    live.box = boxed.support_box(live.now, live.before)
    assert live.box == ((11, 14), (0, 2), (4, 6))
    boxed.records[live.identity] = live
    plain = DetectorLawSimulation(parse_nature_beam_world(document))
    other = planted(plain, 0, now.copy(), before.copy(), np.zeros(now.shape, dtype=np.int64))
    assert other.box is None
    plain.records[other.identity] = other
    for _ in range(40):
        boxed.step()
        plain.step()
        outside_is_zero(boxed)
        assert np.array_equal(live.now, other.now) and np.array_equal(live.remainder, other.remainder)
    # the box wrapped every axis: the whole board, the step then the plain one
    assert live.box is None
    for _ in range(40):
        boxed.step_inverse()
        plain.step_inverse()
        assert np.array_equal(live.now, other.now) and np.array_equal(live.remainder, other.remainder)
    assert np.array_equal(live.now, now) and np.array_equal(live.before, before)
    assert not live.remainder.any()


def test_the_box_grows_by_one_link_and_stops_at_an_open_face() -> None:
    document = block_world(
        [30, 1, 1], {"x": "closed", "y": "periodic", "z": "periodic"}, [800, 809], [], ticks=50
    )
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    now = np.zeros((30, 1, 1), dtype=np.int64)
    now[3, 0, 0] = UNIT
    live = planted(simulation, 0, now, np.zeros_like(now), np.zeros_like(now))
    live.box = simulation.support_box(live.now, live.before)
    assert live.box == ((3, 4), (0, 1), (0, 1))
    simulation.records[live.identity] = live
    for step in range(1, 4):
        simulation.step()
        assert live.box == ((3 - step, 4 + step), (0, 1), (0, 1))
        outside_is_zero(simulation)
    simulation.step()
    assert live.box == ((0, 8), (0, 1), (0, 1))  # the open face at 0: no Node beyond it
    for _ in range(30):
        simulation.step()
    assert live.box is None  # the whole chain: the plain step


def test_a_box_short_of_a_closed_face_reads_zero_beyond_it_like_the_whole_board(monkeypatch) -> None:
    """The mathematician's check before the merge (ALGEBRA.md 9.68 (3)): on a CLOSED axis
    (mirrors) a window's edge inside the board reads zero beyond it, as the whole-board step
    does (the board's faces reflect nothing by themselves: a mirror is a body of light's kind,
    the face beyond the last Node has no Node); a planted record 10 Links from the closed face
    steps 6 intervals with its box short of the face and the same 6 on the whole board, bit
    for bit, then reaches the face and stays bit-equal for 30 more."""
    boundary = {"x": "closed", "y": "periodic", "z": "periodic"}
    document = block_world([40, 1, 1], boundary, [800, 809], [], ticks=50)
    now = np.zeros((40, 1, 1), dtype=np.int64)
    now[29:31, 0, 0] = UNIT // 2
    boxed = DetectorLawSimulation(parse_nature_beam_world(document))
    live = planted(boxed, 0, now.copy(), np.zeros_like(now), np.zeros_like(now))
    live.box = boxed.support_box(live.now, live.before)
    boxed.records[live.identity] = live
    plain = DetectorLawSimulation(parse_nature_beam_world(document))
    other = planted(plain, 0, now.copy(), np.zeros_like(now), np.zeros_like(now))
    plain.records[other.identity] = other
    for step in range(36):
        boxed.step()
        plain.step()
        if step < 6:
            assert live.box is not None and live.box[0][1] < 40  # short of the closed face at 39
        outside_is_zero(boxed)
        assert np.array_equal(live.now, other.now) and np.array_equal(live.remainder, other.remainder)
    assert live.box is None or live.box[0][1] == 40
