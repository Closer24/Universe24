"""The support-only step, a host shortcut: a record's rows are zero outside its box, which grows one Link per interval; with and without the boxes the runs are the same bit for bit, forward and back, and outside the box the levels and the remainder stay zero. HOST cost only."""

from __future__ import annotations

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world
from tests.bodies import block_world
from tests.running import planted
from tests.worlds import PERIODIC, emitter_world

# A, the amplitude unit of the planted rows: the worlds' amplitude_bound (ALGEBRA.md #the-line;
# the engine's constant UNIT retired by the model owner's record 2089, BUILD.md section 26 item 57)
UNIT = 1 << 20


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
        assert np.array_equal(live.now, other.now) and np.array_equal(live.before, other.before)
        assert np.array_equal(live.remainder, other.remainder)
        assert live.pointers == other.pointers and live.absorbed == other.absorbed


def test_a_record_wrapping_a_periodic_board_steps_and_returns_the_same(monkeypatch) -> None:
    document = block_world([14, 10, 6], PERIODIC, [800, 809], [], ticks=100)
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
    """The mathematician's check before the merge (ALGEBRA.md #the-primitives): on a CLOSED axis (mirrors) a window's edge inside the board reads zero beyond it, as the whole-board step does (the board's faces reflect nothing by themselves: a mirror is a body of light's kind, the face beyond the last Node has no Node); a planted record 10 Links from the closed face steps 6 intervals with its box short of the face and the same 6 on the whole board, bit for bit, then reaches the face and stays bit-equal for 30 more."""
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
