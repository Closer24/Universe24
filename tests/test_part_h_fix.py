"""Part H, the fix pass before the owner reads (both hands' lines of 2026-10-10 on the whole local trial, the advisor's 6092354791 and the mathematician's 6092368671, the Boss's merged list 6092388848). MUST 1: the null window's re-lay keeps the fold: `meeting.relaid` with no direction named lays each Node of the region in the direction standing there, so the taker's twist and the source's fold (the lattice momentum given at a click) survive a body's null close instead of being discarded unbooked (one_photon's atom kept -32,040 only to its next close at 96 before). MUST 5: a region taker (the two slits' screens, bell's sides) takes no +p of its own, so it folds no source: the source is drawn and named, its outstanding count down by one, `recoil` reads "unpaid by the region" and `lost` "P lost to the region" (`meeting.unpaid`, `credit.click_node`), the body's P unchanged."""

import time

import numpy as np

from event_universe import meeting, node, world_files
from event_universe.lattice import Lattice
from event_universe.reports import LOST_TO_LAY, LOST_TO_REGION, LOST_TO_TAKER, UNPAID_BY_REGION
from event_universe.world_files import load_world
from tests import laws
from tests.laws import EVENTS
from tests.test_part_f_momentum import one_photon_board, world_beside
from tests.test_part_g_recoil import RUN, emit_and_take_world, levels_floor

ATOM_P = -32040  # one_photon's two-Node atom at count 1: the quarter turn's reach, the hands' 32,040


def test_one_photons_atom_keeps_its_momentum_past_the_null_close(tmp_path, monkeypatch):
    """MUST 1 (the advisor's run): one_photon's atom takes at 48 with the quarter turn applied ("P lost to the taker"), its P_x -32,040; its window of 48 closes with no click at 96 and 144, and the re-lay there keeps the fold: P_x at 95, 96, 97 and the run's end (170) all -32,040 (before the fix 0 from 96); printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board, lines = one_photon_board(tmp_path)
    atom = next(i for i, f in enumerate(board.families) if f.name == "atom")
    read = {}
    for _ in range(board.world.intervals):
        board.step()
        if board.interval in (48, 95, 96, 97, 144, board.world.intervals):
            read[board.interval] = meeting.fan_momentum(board, atom)[0]
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    assert len(credits) == 1 and credits[0]["interval"] == 48
    assert credits[0]["lost"] == [LOST_TO_TAKER, LOST_TO_LAY]
    end = board.world.intervals
    floor = levels_floor(board, atom, board.mask(board.credit.bodies[0].nodes))
    assert read[48] == ATOM_P
    assert all(abs(read[t] - ATOM_P) <= floor for t in (95, 96, 97, 144, end)), (read, floor)
    print(
        f"Part H (MUST 1): one_photon's atom P_x at 48 {read[48]}, at 95 {read[95]}, at 96 {read[96]}, "
        f"at 97 {read[97]}, at 144 {read[144]}, at the end ({end}) {read[end]}; the floor {floor}"
    )


def test_the_emit_and_take_world_conserves_p_past_the_emitters_null_close(tmp_path, monkeypatch):
    """MUST 1, Part G's world with the emitter's window SHORTER than the run (48 against 200, Part G's 240 hid the loss): body 0 emits at 61 and body 1 takes at 144 with the two receivers; both bodies' windows close with no click at 192, after the click and before the run's end, and P over the board and the two bodies is still conserved to the floor at the run's end; the reversal with the books MATCHes over 200; the integers printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    started = time.perf_counter()
    path = emit_and_take_world(tmp_path, list(range(6)), list(range(12, 18)), window=48)
    board = Lattice(load_world(path), (lines := []).append)
    atom = next(i for i, f in enumerate(board.families) if f.name == "atom")
    light = next(i for i, f in enumerate(board.families) if f.name == "pulse")
    before, after, floor = None, None, None
    for _ in range(RUN):
        if not any(c["event"] == "credit" for c in lines):
            before = meeting.fan_momentum(board, light)[0] + meeting.fan_momentum(board, atom)[0]
        board.step()
        taken = [c for c in lines if c["event"] == "credit" and c["absorbed"] == "pulse"]
        if taken and after is None and not board.credit.fronts and board.credit.counts[light] == 0:
            after = (
                board.interval,
                meeting.fan_momentum(board, light)[0],
                meeting.fan_momentum(board, atom)[0],
            )
            at = np.zeros(board.shape, dtype=bool)
            for books in board.credit.bodies:
                at |= board.mask(books.nodes)
            floor = levels_floor(board, atom, at) + 2
    taken = [c for c in lines if c["event"] == "credit" and c["absorbed"] == "pulse"]
    assert len(taken) == 1 and taken[0]["source"] == "body 0" and taken[0]["lost"] is None
    click = taken[0]["interval"]
    closes = [b.windows for b in board.credit.bodies]
    assert all(windows * 48 > click for windows in closes)  # a null close of each body after the click
    assert before == 0 and after is not None and floor is not None
    end = (meeting.fan_momentum(board, light)[0], meeting.fan_momentum(board, atom)[0])
    assert abs(after[1] + after[2] - before) <= floor, (before, after, floor)
    assert abs(end[0] + end[1] - before) <= floor, (before, end, floor)
    print(
        f"Part H (MUST 1, the shorter window): the click at {click}, p = {taken[0]['momentum']}, recoil {taken[0]['recoil']}; "
        f"P before the emission {before}, after the front passed (interval {after[0]}) the light's {after[1]} and the "
        f"two bodies' {after[2]}, the total {after[1] + after[2]}; the bodies' windows closed {closes} times, the last with no "
        f"click at {max(closes) * 48}; at the run's end ({RUN}) the light's {end[0]} and the bodies' {end[1]}, the total "
        f"{end[0] + end[1]}; the floor {floor}"
    )
    verdict = laws.BACK.verdict(Lattice(load_world(path)), RUN)
    assert verdict["verdict"] == "MATCH", verdict
    print(
        f"Part H (MUST 1, the shorter window): {RUN} forward and back: MATCH; {time.perf_counter() - started:.1f} s"
    )


def region_takes_world(tmp_path):  # type: ignore[no-untyped-def]
    """The resonance world rewritten beside tmp_path: body 0 the emitter on six Nodes (excited, [2, 3], lifetime 48, its window 48), body 1 dropped, and the declared region `counter` over every other Node of the chain of 48 (the chain's complement of the body, as shelved_ion's counter is the board's: a region a pulse passes through books no net inflow), the world's draw at the window 48."""

    def edit(world):  # type: ignore[no-untyped-def]
        world["intervals"] = RUN
        world["bodies"][0]["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in range(6)]
        world["bodies"][0]["node_detector"]["window"] = 48
        del world["bodies"][1]
        world["node_detectors"] = [{"name": "counter", "positions": [[x, 0, 0] for x in range(6, 48)]}]
        world["draw"] = {
            "window": 48,
            "seed": 24,
            "multiplier": 6364136223846793005,
            "increment": 1442695040888963407,
        }

    return world_beside(tmp_path, EVENTS / "resonance" / "resonant.json", edit)


def test_a_region_taker_names_the_source_and_folds_nothing(tmp_path, monkeypatch):
    """MUST 5: a body's light credited by a declared region: the credit line's `source` names body 0, `recoil` reads "unpaid by the region", `lost` ["P lost to the region"], the emitter's outstanding count down by one, and the body's P_x unchanged across the region's click (nothing folded); printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(region_takes_world(tmp_path)), (lines := []).append)
    atom = next(i for i, f in enumerate(board.families) if f.name == "atom")
    light = next(i for i, f in enumerate(board.families) if f.name == "pulse")
    giver = board.credit.bodies[0]
    weight = board.families[atom].pair[0]
    read = {}
    for _ in range(RUN):
        board.step()
        read[board.interval] = node.momentum_of(weight, board.lines_of(atom, giver.record), board.wrap)[
            0
        ]
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]
    region = [c for c in credits if c["node_detector"] == "counter"]
    assert len(region) == 1 and region[0]["family"] == "pulse"
    click = region[0]
    assert click["source"] == "body 0" and click["recoil"] == UNPAID_BY_REGION
    assert click["lost"] == [LOST_TO_REGION] and click["momentum"][0] != 0
    assert board.credit.emitters[light][0].outstanding == 0
    t = click["interval"]
    assert read[t - 1] == read[t] == read[t + 1], (read[t - 1], read[t], read[t + 1])
    print(
        f"Part H (MUST 5): the region takes at {t}: p = {click['momentum']}, source {click['source']}, "
        f"recoil {click['recoil']!r}, lost {click['lost']}; the body's P_x at {t - 1}, {t}, {t + 1}: "
        f"{read[t - 1]}, {read[t]}, {read[t + 1]} (unchanged); the emitter's outstanding count 0"
    )
